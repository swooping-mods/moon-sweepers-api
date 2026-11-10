"""Managed contracts accept independent authors without executing payloads."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from test_api import manifest, PNG
from moon_mod_api import packages
from moon_mod_api.pack import pack
from moon_mod_api.runtimes import MANAGED_KIND, MANAGED_ABI, NATIVE_ABIS


def managed(name="independent-managed"):
    value = manifest(name)
    value.pop("hook_framework_abi")
    value.pop("shared_claims")
    value.update(kind=MANAGED_KIND, abi=MANAGED_ABI,
                 bepinex={"guid": "independent." + name, "data_root": name.replace("-", "_")})
    return value


class RuntimeChecks(unittest.TestCase):
    def test_unrelated_managed_archive_round_trips_without_execution(self):
        value = managed()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / "payload"
            payload.mkdir()
            (payload / "mod.dll").write_bytes(b"Synthetic managed payload, never executed")
            (payload / "icon.png").write_bytes(PNG)
            source = root / "manifest.json"
            source.write_text(json.dumps(value))
            output = root / "independent.msmod"
            pack(source, payload, output)
            self.assertEqual(packages.examine(output)["bepinex"], value["bepinex"])
            location, installed = packages.install(output, root / "data")
            self.assertEqual(packages.installed(root / "data/library" / location), installed)

    def test_mixed_dependency_order_and_cross_backend_hook_ownership(self):
        native, plugin = manifest("native-library"), managed()
        plugin["requires"] = [native["id"]]
        values = {mod["id"]: mod for mod in (plugin, native)}
        pins = native["game"]["hashes"]
        self.assertEqual(packages.resolve(values, list(values), pins), [native["id"], plugin["id"]])
        plugin["claims"] = ["MoonWalker.Update"]
        with self.assertRaisesRegex(ValueError, "exclusively"):
            packages.resolve(values, list(values), pins)
        plugin["claims"] = ["MoonPrototypeVehicle.FixedUpdate"]
        native["vehicle_hook"] = "physics"
        with self.assertRaisesRegex(ValueError, "[Vv]ehicle"):
            packages.resolve(values, list(values), pins)

    def test_backend_availability_is_distinct_from_package_validity(self):
        value = managed()
        packages.validate(value)
        args = ({value["id"]: value}, [value["id"]], value["game"]["hashes"])
        with self.assertRaisesRegex(ValueError, "Runtime is unavailable"):
            packages.resolve(*args, available_runtimes={("native", abi) for abi in NATIVE_ABIS})
        self.assertEqual(packages.resolve(*args, available_runtimes={(MANAGED_KIND, MANAGED_ABI)}), [value["id"]])

    def test_managed_identity_and_data_namespace_collisions_are_case_insensitive(self):
        a, b = managed("first"), managed("second")
        for field in ("guid", "data_root"):
            changed = copy.deepcopy(b)
            changed["bepinex"][field] = a["bepinex"][field].upper()
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "collision"):
                packages.resolve({"first": a, "second": changed}, ["second", "first"], a["game"]["hashes"])

    def test_managed_host_namespaces_roles_and_backend_mismatch_reject(self):
        for change in (
            {"bepinex": {"guid": "author.plugin", "data_root": "Core"}},
            {"bepinex": {"guid": "author.plugin", "data_root": "CON"}},
            {"bepinex": {"guid": "author.plugin", "data_root": "../escape"}},
            {"bepinex": {"guid": "bad guid", "data_root": "Independent"}},
            {"shared_claims": ["MoonWalker.Update"]},
            {"vehicle_hook": "input"},
            {"abi": "BepInEx.IL2CPP/other"},
            {"abi": ["BepInEx.IL2CPP/other"]},
            {"kind": "native", "abi": "MoonLab_ModStart/v1"},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                packages.validate({**managed(), **change})
        value = managed()
        value["entry"] = "sub/plugin.dll"
        value["files"][value["entry"]] = "a" * 64
        with self.assertRaisesRegex(ValueError, "root DLL"):
            packages.validate(value)

    def test_external_provenance_is_generic_and_not_a_download_instruction(self):
        value = managed()
        value.update(mode="external", external={"adapter": MANAGED_KIND,
                     "repository": "https://example.com/another-author/plugin", "revision": "v1.2.3"})
        packages.validate(value)
        for url in ("file:///tmp/plugin", "https://user:password@example.com/repo", "https://example.com/repo?token=x"):
            changed = copy.deepcopy(value)
            changed["external"]["repository"] = url
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "HTTPS"):
                packages.validate(changed)


if __name__ == "__main__":
    unittest.main()
