"""Synthetic reviewed targets never qualify another real game release."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest

from test_api import manifest, PNG, ROOT
from test_runtimes import managed
from moon_mod_api import compatibility as compat, packages
from moon_mod_api.pack import pack
from moon_mod_api.runtime_plan import encode, MAGIC, MAGIC_V2
from moon_mod_api.runtimes import NATIVE_ABIS


def modern(name="portable-feature", clock=True):
    value = manifest(name)
    for key in ("shared_claims", "hook_framework_abi"):
        value.pop(key)
    value.update(abi=compat.V8, runtime_api_abi=1, game_access="adapter", game_api_abi=1,
                 requires_game={"unity.clock": {"abi": 1, "min_size": 16}} if clock else {})
    value["game"].pop("hashes")
    return value


def profile(name="fixture.current", byte="a", rva=4096):
    value = {"id": name, "hashes": {n: byte * 64 for n in compat.GAME_FILES},
             "capabilities": {"unity.clock": {"abi": 1, "size": 16, "limits": {"channels": 2}}},
             "adapter_abi": 1, "bindings": {"clock": {"rva": rva, "signature": "double(void*)"}}}
    value["digest"] = compat.profile_digest(value)
    return value


def target(row=None):
    row = row or profile()
    return {"game_profile": row,
            "game_adapter": {"abi": 1, "profiles": {row["id"]: {
                "digest": row["digest"], "capabilities": copy.deepcopy(row["capabilities"])}}},
            "available_runtimes": {("native", abi) for abi in NATIVE_ABIS},
            "runtime_api_abi": 1, "runtime_readiness_abi": 1, "host_capabilities": {},
            "native_package_abis": list(NATIVE_ABIS),
            "legacy_profile_ids": {"native": ["fixture.current"], "bepinex-il2cpp": ["fixture.current"]},
            "runtime_sha256": "d" * 64}


class CompatibilityChecks(unittest.TestCase):
    def evaluate(self, values, row=None, **change):
        kwargs = target(row)
        kwargs.update(change)
        return compat.evaluate(values, list(values), kwargs["game_profile"]["hashes"] if kwargs.get("game_profile") else {}, **kwargs)

    def test_same_immutable_archive_runs_through_two_reviewed_synthetic_targets(self):
        mod = modern()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); payload = root / "payload"; payload.mkdir()
            (payload / "mod.dll").write_bytes(b"Original inert v8 fixture")
            (payload / "icon.png").write_bytes(PNG)
            source = root / "manifest.json"; source.write_text(json.dumps(mod))
            output = root / "feature.msmod"; pack(source, payload, output)
            before = hashlib.sha256(output.read_bytes()).hexdigest()
            value = packages.examine(output); original = copy.deepcopy(value)
            for row in (profile(), profile("fixture.later", "b", 8192)):
                result = self.evaluate({value["id"]: value}, row)
                self.assertEqual(result["status"], "requirements-matched")
                self.assertTrue(result["allowed"])
                self.assertEqual(result["verification"], [])
                self.assertEqual(packages.resolve({value["id"]: value}, [value["id"]], row["hashes"], **{
                    k: v for k, v in target(row).items() if k != "runtime_sha256"}), [value["id"]])
            self.assertEqual(value, original)
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), before)

    def test_legacy_pins_are_preserved_and_additional_v8_pins_are_not_ignored(self):
        legacy = manifest("legacy"); packages.validate(legacy)
        self.assertTrue(self.evaluate({"legacy": legacy})["allowed"])
        self.assertFalse(self.evaluate({"legacy": legacy}, profile("fixture.later", "b"))["allowed"])
        value = modern(); value["game"]["hashes"] = {"GameAssembly.dll": "a" * 64}
        self.assertTrue(self.evaluate({value["id"]: value})["allowed"])
        self.assertFalse(self.evaluate({value["id"]: value}, profile("fixture.later", "b"))["allowed"])
        value["game"]["hashes"] = []
        with self.assertRaisesRegex(ValueError, "pin table"):
            packages.validate(value)

    def test_matching_legacy_hash_subset_does_not_forward_a_raw_adapter(self):
        legacy = manifest("legacy-library")
        value = modern(clock=False); value["requires"] = [legacy["id"]]
        later = profile("fixture.later", "b")
        later["hashes"]["GameAssembly.dll"] = "a" * 64
        later["digest"] = compat.profile_digest(later)
        result = self.evaluate({legacy["id"]: legacy, value["id"]: value}, later)
        self.assertFalse(result["allowed"])
        self.assertIn("legacy-runtime-profile-unavailable", [r["code"] for r in result["mods"][legacy["id"]]["reasons"]])
        self.assertIn("dependency-incompatible", [r["code"] for r in result["mods"][value["id"]]["reasons"]])
        # The existing offline SDK path retains its original subset semantics.
        self.assertEqual(packages.resolve({legacy["id"]: legacy}, [legacy["id"]], later["hashes"]), [legacy["id"]])

    def test_framework_only_consumers_share_the_same_effective_base(self):
        library, value = modern("ordinary-library", False), modern(clock=False)
        library["provides"] = {"ordinary-library.catalog": {"abi": 4, "size": 64, "limits": {"items": 12}}}
        value["requires"] = [library["id"]]
        value["requires_apis"] = [{"api": "ordinary-library.catalog", "abi": 4, "min_size": 32, "limits": {"items": 10}}]
        values = {value["id"]: value, library["id"]: library}
        result = self.evaluate(values, profile("fixture.later", "b"))
        self.assertTrue(result["allowed"])
        self.assertEqual(result["order"], [library["id"], value["id"]])
        row = result["mods"][value["id"]]["requirements"][1]
        self.assertEqual(row["provider_version"], "1.0.0")
        self.assertTrue(row["satisfied"])
        library["provides"]["ordinary-library.catalog"]["limits"]["items"] = 9
        result = self.evaluate(values)
        self.assertFalse(result["allowed"])
        self.assertFalse(result["mods"][value["id"]]["requirements"][1]["satisfied"])

    def test_unselected_optional_framework_is_optional_but_selected_bad_api_refuses(self):
        library, value = modern("ordinary-library", False), modern(clock=False)
        value["requires_apis"] = [{"api": "ordinary-library.catalog", "abi": 1, "min_size": 16, "optional": True}]
        self.assertTrue(self.evaluate({value["id"]: value})["allowed"])
        self.assertFalse(self.evaluate({value["id"]: value, library["id"]: library})["allowed"])

    def test_unknown_hashes_are_not_guessed_from_version_or_author_text(self):
        value = modern(); value["verification"] = {"Build": "Verified future release"}
        row = profile(); row["version"] = "same display version"; row["digest"] = compat.profile_digest(row)
        result = compat.evaluate({value["id"]: value}, [value["id"]], {n: "f" * 64 for n in compat.GAME_FILES}, **target(row))
        self.assertEqual(result["status"], "unknown")
        self.assertFalse(result["allowed"])
        self.assertEqual(result["verification"], [])
        self.assertEqual(self.evaluate({value["id"]: value}, game_profile=None)["status"], "unknown")

    def test_profile_and_adapter_identity_include_physical_bindings(self):
        value = modern(); row = profile(); original = row["digest"]
        row["bindings"]["clock"]["rva"] += 32
        self.assertNotEqual(compat.profile_digest(row), original)
        self.assertFalse(self.evaluate({value["id"]: value}, row)["allowed"])
        row["digest"] = compat.profile_digest(row)
        kwargs = target(row); kwargs["game_adapter"]["profiles"][row["id"]]["digest"] = original
        result = compat.evaluate({value["id"]: value}, [value["id"]], row["hashes"], **kwargs)
        self.assertFalse(result["allowed"])

    def test_game_capability_abi_size_and_capacity_are_checked(self):
        value = modern(); value["requires_game"]["unity.clock"]["limits"] = {"channels": 2}
        for change in ({"abi": 2}, {"min_size": 17}, {"limits": {"channels": 3}}):
            changed = copy.deepcopy(value); changed["requires_game"]["unity.clock"].update(change)
            with self.subTest(change=change):
                self.assertFalse(self.evaluate({changed["id"]: changed})["allowed"])
        value["requires_game"] = {"missing.capability": {"abi": 1, "min_size": 16}}
        self.assertFalse(self.evaluate({value["id"]: value})["allowed"])

    def test_v8_requires_actual_native_abi_support_and_a_runtime_api(self):
        value = modern()
        for change in ({"native_package_abis": None}, {"native_package_abis": ["MoonLab_ModStart/v7"]},
                       {"runtime_api_abi": None}, {"runtime_api_abi": 2}, {"game_adapter": None}):
            with self.subTest(change=change):
                self.assertFalse(self.evaluate({value["id"]: value}, **change)["allowed"])
        with self.assertRaisesRegex(ValueError, "Native package ABI v8"):
            packages.resolve({value["id"]: value}, [value["id"]], profile()["hashes"], game_profile=profile())

    def test_legacy_and_managed_backends_cannot_opt_in_through_ignored_fields(self):
        for value in (manifest(), managed()):
            for key, field in (("game_access", "adapter"), ("game_api_abi", 1), ("requires_game", {})):
                with self.subTest(kind=value["kind"], key=key), self.assertRaisesRegex(ValueError, "native v8"):
                    packages.validate({**value, key: field})
        value = modern()
        for field in ("game_access", "game_api_abi", "requires_game", "runtime_api_abi"):
            changed = copy.deepcopy(value); changed.pop(field)
            with self.subTest(missing=field), self.assertRaises(ValueError): packages.validate(changed)

    def test_raw_hook_roles_are_not_portable_v8_requirements(self):
        changes = ({"claims": ["MoonWalker.Update"]}, {"shared_claims": ["MoonWalker.Update"]},
                   {"vehicle_hook": "input"}, {"late_update_hook": "observer"}, {"hook_framework_abi": 1})
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError): packages.validate({**modern(), **change})

    def test_unbounded_malformed_game_metadata_fails_closed(self):
        invalid = (None, [], {"Bad.Name": {"abi": 1, "min_size": 16}},
                   {"unity.clock_extra": {"abi": 1, "min_size": 16}},
                   {"clock": {"abi": 1, "min_size": 16}},
                   {"unity.clock": {"abi": True, "min_size": 16}},
                   {"unity.clock": {"abi": 1, "min_size": 0}},
                   {"unity.clock": {"abi": 1, "min_size": 65537}},
                   {"unity.clock": {"abi": 1, "min_size": 16, "optional": True}},
                   {"unity.clock": {"abi": 1, "min_size": 16, "limits": {"bad": True}}},
                   {"game.cap" + str(n): {"abi": 1, "min_size": 16} for n in range(65)})
        for table in invalid:
            with self.subTest(table=table), self.assertRaises(ValueError): packages.validate({**modern(), "requires_game": table})
        value = modern(); value["requires"] = [{}]
        self.assertFalse(self.evaluate({value["id"]: value})["allowed"])
        self.assertFalse(compat.evaluate({}, [None], {})["allowed"])

    def test_malformed_selected_provider_is_reported_without_dereferencing_its_table(self):
        value, library = modern(clock=False), modern("ordinary-library", False)
        value["requires"] = [library["id"]]
        value["requires_apis"] = [{"api": "ordinary-library.catalog", "abi": 1, "min_size": 16}]
        for malformed in ([], "bad", {"ordinary-library.catalog": []},
                          {"ordinary-library.catalog": {"abi": True, "size": 16}},
                          {"ordinary-library.catalog": {"abi": 1, "size": "bad"}}):
            library["provides"] = malformed
            with self.subTest(malformed=malformed):
                result = self.evaluate({value["id"]: value, library["id"]: library})
                self.assertEqual(result["status"], "incompatible")
                self.assertFalse(result["allowed"])

    def test_verified_evidence_binds_full_selection_runtime_profile_and_scope(self):
        library, value = modern("ordinary-library", False), modern(clock=False)
        value["requires"] = [library["id"]]; values = {library["id"]: library, value["id"]: value}
        row = profile(); kwargs = target(row)
        record = {"success": True, "selection_digest": compat.selection_digest(values, values),
                  "mod_digests": {n: compat.content_digest(v) for n, v in values.items()},
                  "profile_digest": row["digest"], "runtime_sha256": kwargs["runtime_sha256"],
                  "scope": "startup", "record": "loader-owned-review-1"}
        result = self.evaluate(values, row, evidence=[record])
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["verification"], [{"scope": "startup", "record": "loader-owned-review-1"}])
        for change in ({"runtime_sha256": "e" * 64}, {"profile_digest": "e" * 64},
                       {"selection_digest": "e" * 64}, {"mod_digests": {}}, {"scope": "everything"},
                       {"success": False}, {"success": None}, {"success": 1}, {"success": "true"}):
            with self.subTest(change=change):
                self.assertEqual(self.evaluate(values, row, evidence=[{**record, **change}])["status"], "requirements-matched")
        missing_result = {k: v for k, v in record.items() if k != "success"}
        self.assertEqual(self.evaluate(values, row, evidence=[missing_result])["status"], "requirements-matched")
        self.assertEqual(self.evaluate(values, row, evidence=[record] * (compat.MAX_EVIDENCE + 1))["status"], "requirements-matched")
        library["files"]["mod.dll"] = "f" * 64
        self.assertEqual(self.evaluate(values, row, evidence=[record])["status"], "requirements-matched")
        value["verification"] = {"Build": "Verified"}
        self.assertEqual(self.evaluate(values, row)["status"], "requirements-matched")

    def test_legacy_runtime_plan_bytes_remain_unchanged(self):
        value = manifest()
        expected = MAGIC + struct.pack("<IH", 1, 7) + b"example" + struct.pack("<III", 5, 0, 0)
        self.assertEqual(encode({value["id"]: value}, [value["id"]]), expected)

    def test_v2_runtime_plan_binds_profile_and_each_record_has_game_contract_count(self):
        legacy, value = manifest("foundation"), modern("feature")
        value["requires"] = [legacy["id"]]; value["requires_game"]["unity.clock"]["limits"] = {"channels": 1}
        row = profile()
        def text(s):return struct.pack("<H", len(s)) + s.encode("ascii")
        expected = (MAGIC_V2 + text(row["id"]) + text(row["digest"]) + struct.pack("<I", 2)
                    + text("foundation") + struct.pack("<IIII", 5, 0, 0, 0)
                    + text("feature") + struct.pack("<IIII", 8, 0, 0, 1)
                    + text("unity.clock") + struct.pack("<III", 1, 16, 1)
                    + text("channels") + struct.pack("<I", 1))
        self.assertEqual(encode({legacy["id"]: legacy, value["id"]: value}, [legacy["id"], value["id"]], game_profile=row), expected)
        with self.assertRaisesRegex(ValueError, "reviewed game profile"):
            encode({legacy["id"]: legacy, value["id"]: value}, [legacy["id"], value["id"]])

    def test_public_game_header_compiles_and_validates_the_broker_only_context(self):
        source = '''#include "moon_sweepers/game_adapter.h"
#include <assert.h>
static int scale_sample(MoonGameTimeScaleSampleV1 *out){(void)out;return 0;}
int main(void){
    MoonModContextV8 context={0};
    MoonGameTimeScaleV1 scale={sizeof(scale),MOON_GAME_TIME_SCALE_ABI,scale_sample};
    assert(!moon_mod_context_v8_valid(&context)&&!moon_game_clock_valid(0));
    assert(!moon_game_time_scale_valid(0)&&moon_game_time_scale_valid(&scale));
    scale.size--;assert(!moon_game_time_scale_valid(&scale));
    scale.size=sizeof(scale)+8;assert(moon_game_time_scale_valid(&scale));
    scale.abi++;assert(!moon_game_time_scale_valid(&scale));
    scale.abi=MOON_GAME_TIME_SCALE_ABI;scale.sample=0;assert(!moon_game_time_scale_valid(&scale));
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); path = root / "consumer.c"; path.write_text(source)
            executable = root / "consumer"
            subprocess.run(["clang", "-std=c11", "-Wall", "-Wextra", "-Werror", "-I", str(ROOT / "include"), str(path), "-o", str(executable)], check=True)
            subprocess.run([str(executable)], check=True)
