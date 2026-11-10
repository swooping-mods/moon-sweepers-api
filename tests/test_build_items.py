import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from moon_mod_api import build_items, packages


class BuildingApiChecks(unittest.TestCase):
    def test_public_build_header_and_existing_layout(self):
        source = '''#include "moon_sweepers/build_menu/build_menu.h"
_Static_assert(MB_FIRST_KIND==193 && MB_LAST_KIND==384 && MB_LIMIT==192,"range");
_Static_assert(MB_ABI==1,"existing ABI");
static const MoonBuildDefinition item={.abi=MB_ABI,.size=sizeof(MoonBuildDefinition),
    .key="example-mod.power.relay",.kind=384,.template_kind=93};
int main(void){return item.kind!=384;}
'''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "consumer.c"
            path.write_text(source)
            subprocess.run(["clang", "-std=c11", "-Wall", "-Wextra", "-Werror", "-I",
                            str(ROOT / "include"), "-fsyntax-only", str(path)], check=True)

    def test_range_keys_and_duplicate_declarations(self):
        for kind in (193, 224, 225, 255, 256, 300, 384):
            build_items.validate_items("sample", [{"kind": kind, "key": "sample.power.item"}])
        for kind in (192, 385, -1, True, 384.0):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                build_items.validate_items("sample", [{"kind": kind, "key": "sample.power.item"}])
        for key in ("other.power.item", "sample.Power.item", "sample", "sample..item"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                build_items.validate_items("sample", [{"kind": 384, "key": key}])
        with self.assertRaises(ValueError):
            build_items.validate_items("sample", [{"kind": 193, "key": "sample.a"}, {"kind": 193, "key": "sample.b"}])

    def test_cross_mod_collision_and_dependency(self):
        first = {"id": "first", "kind": "native", "requires": ["build-menu-framework"],
                 "build_items": [{"kind": 384, "key": "first.power.item"}]}
        second = {"id": "second", "kind": "native", "requires": ["build-menu-framework"],
                  "build_items": [{"kind": 384, "key": "second.power.item"}]}
        with self.assertRaisesRegex(ValueError, "384"):
            build_items.validate_selection({"first": first, "second": second}, ["first", "second"])
        second["build_items"][0]["kind"] = 256
        build_items.validate_selection({"first": first, "second": second}, ["second", "first"])
        first["requires"] = []
        with self.assertRaisesRegex(ValueError, "dependency"):
            build_items.validate_manifest(first)

    def test_registry_preserves_existing_save_identity_and_retired_ids(self):
        registry = json.loads((ROOT / "docs/registries/buildings.json").read_text())
        build_items.validate_registry(registry)
        pole = next(e for e in registry["entries"] if e["mod"] == "manual-power-poles")
        self.assertEqual((pole["kind"], pole["key"]), (193, "manual-power-poles.power-pole"))
        changed = copy.deepcopy(registry)
        changed["entries"][0]["status"] = "retired"
        changed["entries"].append({"mod": "another", "kind": 193, "key": "another.power.item", "status": "active"})
        with self.assertRaisesRegex(ValueError, "retired"):
            build_items.validate_registry(changed)

    def test_real_package_resolver_checks_build_items(self):
        # This exercises the package selection entrypoint, not just its helper.
        pins = {"GameAssembly.dll": "a" * 64}
        def mod(name, kind=None):
            value = {"id": name, "name": name, "kind": "native", "game": {"hashes": pins},
                     "conflicts": [], "claims": [], "requires": []}
            if kind:
                value.update(requires=["build-menu-framework"], build_items=[{"kind": kind, "key": name + ".power.item"}])
            if name == "build-menu-framework":
                value["build_menu_max_kind"] = 384
            return value
        values = {name: mod(name, kind) for name, kind in (("build-menu-framework", None), ("first", 384), ("second", 384))}
        with self.assertRaisesRegex(ValueError, "384"):
            packages.resolve(values, list(values), pins)
        del values["second"]
        self.assertEqual(packages.resolve(values, list(values), pins), ["build-menu-framework", "first"])
        del values["build-menu-framework"]["build_menu_max_kind"]
        with self.assertRaisesRegex(ValueError, "through 224"):
            packages.resolve(values, list(values), pins)


if __name__ == "__main__":
    unittest.main()
