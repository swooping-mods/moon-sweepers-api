"""Contract checks independent of the desktop app and game installation."""
import copy
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
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
    def test_malformed_manifest_shapes_raise_validation_errors(self):
        for value in (None, [], True, 1, 'manifest'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                packages.validate(value)
        for field in ('kind', 'abi', 'entry', 'icon'):
            for value in (None, [], {}, 1):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    packages.validate({**manifest(), field: value})

    def test_install_uses_validated_snapshot_after_download_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / 'payload'
            payload.mkdir()
            (payload / 'mod.dll').write_bytes(b'original inert payload')
            (payload / 'icon.png').write_bytes(PNG)
            description = root / 'manifest.json'
            description.write_text(json.dumps(manifest()))
            download = pack(description, payload, root / 'original.msmod')
            original_hash = hashlib.sha256(download.read_bytes()).hexdigest()
            description.write_text(json.dumps(manifest('replacement')))
            (payload / 'mod.dll').write_bytes(b'replacement inert payload')
            replacement = pack(description, payload, root / 'replacement.msmod')
            examine = packages._examine_archive
            def replace_after_validation(archive):
                result = examine(archive)
                replacement.replace(download)
                return result
            with patch.object(packages, '_examine_archive', side_effect=replace_after_validation):
                name, installed = packages.install(download, root / 'data')
            self.assertEqual(installed['id'], 'example')
            self.assertEqual(name, 'example/1.0.0-' + original_hash[:16])
            folder = root / 'data/library' / name
            self.assertEqual((folder / 'mod.dll').read_bytes(), b'original inert payload')
            self.assertEqual(packages.installed(folder), installed)
            self.assertFalse(list((root / 'data').rglob('.intake-*')))

    def test_streamed_intake_rejects_actual_size_and_corrupt_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'bad.msmod'
            path.write_bytes(b'x' * 1025)
            with patch.object(packages, 'MAX_BYTES', 1024), self.assertRaisesRegex(ValueError, '64 MiB'):
                packages.install(path, root / 'data')
            self.assertFalse((root / 'data').exists())
            if hasattr(os, 'mkfifo'):
                fifo = root / 'pipe.msmod'
                os.mkfifo(fifo)
                with self.assertRaisesRegex(ValueError, 'regular file'):
                    packages.install(fifo, root / 'data')
            value = manifest()
            value['files'] = {'mod.dll': hashlib.sha256(b'expected').hexdigest(),
                              'icon.png': hashlib.sha256(PNG).hexdigest()}
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('manifest.json', json.dumps(value))
                archive.writestr('mod.dll', b'wrong')
                archive.writestr('icon.png', PNG)
            for action in (lambda: packages.examine(path), lambda: packages.install(path, root / 'data')):
                with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                    action()
            self.assertFalse((root / 'data').exists())

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
