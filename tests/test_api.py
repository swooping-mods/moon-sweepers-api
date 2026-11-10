"""Contract checks independent of the desktop app and game installation."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from moon_mod_api import packages
from moon_mod_api.pack import pack
from moon_mod_api.storage import relative


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)


PNG = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(b"\0\0\0\0\xff")) + chunk(b"IEND", b"")


def manifest(name="example"):
    return {"schema": packages.SCHEMA, "id": name, "version": "1.0.0", "name": "Example",
            "summary": "Synthetic fixture", "description": "Host checks only", "author": "Tests",
            "kind": "native", "abi": "MoonLab_ModStart/v5", "hook_framework_abi": 1,
            "shared_claims": ["MoonWalker.Update"], "claims": [], "requires": [], "conflicts": [],
            "entry": "mod.dll", "icon": "icon.png",
            "game": {"id": "moon-sweepers", "appid": "5335510", "hashes": {"GameAssembly.dll": "a" * 64}},
            "files": {"mod.dll": "b" * 64, "icon.png": "c" * 64}}


class ApiChecks(unittest.TestCase):
    def test_public_headers_compile_without_loader(self):
        source = '#include "moon_sweepers/hooks.h"\nint main(void) {return moon_hook_api_valid(0);}\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "consumer.c"
            path.write_text(source)
            subprocess.run(["clang", "-std=c11", "-Wall", "-Wextra", "-Werror", "-I", str(ROOT / "include"), "-fsyntax-only", str(path)], check=True)

    def test_v5_role_requires_exact_abi(self):
        original = manifest()
        packages.validate(original)
        for update in ({"hook_framework_abi": True}, {"hook_framework_abi": 2}, {"shared_claims": []}, {"abi": "MoonLab_ModStart/v2"}):
            with self.subTest(update=update), self.assertRaises(ValueError):
                packages.validate({**original, **update})

    def test_portable_names(self):
        for name in ("../escape", "/root", "a\\b", "x:stream", "CON.txt", "a//b", "x."):
            with self.subTest(name=name), self.assertRaises(ValueError):
                relative(name)

    def test_dependency_order_and_cycles(self):
        first, second = manifest("foundation"), manifest("feature")
        second["requires"] = ["foundation"]
        mods = {"foundation": first, "feature": second}
        pins = first["game"]["hashes"]
        self.assertEqual(packages.resolve(mods, ["feature", "foundation"], pins), ["foundation", "feature"])
        with self.assertRaises(ValueError):
            packages.resolve(mods, ["feature"], pins)
        first["requires"] = ["feature"]
        with self.assertRaisesRegex(ValueError, "Circular"):
            packages.resolve(mods, list(mods), pins)

    def test_wrong_game_and_conflicting_hooks(self):
        first, second = manifest("first"), manifest("second")
        with self.assertRaises(ValueError):
            packages.resolve({"first": first}, ["first"], {})
        for item in (first, second):
            item["claims"] = ["exclusive-hook"]
        with self.assertRaises(ValueError):
            packages.resolve({"first": first, "second": second}, ["first", "second"], first["game"]["hashes"])

    def test_pack_reproducibility_integrity_and_immutability(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / "payload"
            payload.mkdir()
            (payload / "mod.dll").write_bytes(b"synthetic DLL, never executed")
            (payload / "icon.png").write_bytes(PNG)
            description = root / "manifest.json"
            description.write_text(json.dumps(manifest()))
            output = root / "example.msmod"
            pack(description, payload, output)
            original = output.read_bytes()
            pack(description, payload, output)
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual(packages.examine(output)["id"], "example")
            (payload / "mod.dll").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "different package"):
                pack(description, payload, output)
            with zipfile.ZipFile(output, "a") as archive:
                archive.writestr("unlisted.txt", "unexpected")
            with self.assertRaises(ValueError):
                packages.examine(output)

    def test_pack_requires_author_supplied_game_pins(self):
        value = manifest()
        value["game"]["hashes"] = {}
        with self.assertRaisesRegex(ValueError, "compatibility pins"):
            packages.validate(value)


if __name__ == "__main__":
    unittest.main()
