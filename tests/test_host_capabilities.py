"""Mandatory host adapters reject before deployment without naming mod owners."""
import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest

from test_api import manifest, PNG
from test_runtimes import managed
from moon_mod_api import packages
from moon_mod_api.pack import pack
from moon_mod_api.runtime_plan import encode
from moon_mod_api.runtimes import require_available


def requiring_host(name="another-author"):
    value = manifest(name)
    value.update(abi="MoonLab_ModStart/v7", runtime_api_abi=1,
                 requires_host={"interaction": 1})
    return value


class HostCapabilityChecks(unittest.TestCase):
    def test_independent_archive_round_trip_and_v7_native_plan(self):
        value = requiring_host()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / "payload"
            payload.mkdir()
            (payload / "mod.dll").write_bytes(b"Inert native archive fixture")
            (payload / "icon.png").write_bytes(PNG)
            source = root / "manifest.json"
            source.write_text(json.dumps(value))
            output = root / "host.msmod"
            pack(source, payload, output)
            self.assertEqual(packages.examine(output)["requires_host"], {"interaction": 1})
        plan = encode({value["id"]: value}, [value["id"]])
        offset = 12 + 2 + len(value["id"])
        self.assertEqual(struct.unpack_from("<I", plan, offset)[0], 7)

    def test_inspection_is_distinct_from_explicit_target_and_exact_abi(self):
        value = requiring_host()
        args = ({value["id"]: value}, [value["id"]], value["game"]["hashes"])
        self.assertEqual(packages.resolve(*args), [value["id"]])
        for actual in ({}, {"interaction": 2}, {"unrelated": 1}):
            with self.subTest(actual=actual), self.assertRaisesRegex(ValueError, "Host capability interaction"):
                packages.resolve(*args, host_capabilities=actual)
        self.assertEqual(packages.resolve(*args, host_capabilities={"interaction": 1, "other_adapter": 9}),
                         [value["id"]])

    def test_multiple_adapter_requirements_and_ordinary_v6_compatibility(self):
        value = requiring_host()
        value["requires_host"]["independent_adapter"] = 7
        with self.assertRaisesRegex(ValueError, "independent_adapter"):
            require_available(value, None, host_capabilities={"interaction": 1})
        require_available(value, None, host_capabilities={"interaction": 1, "independent_adapter": 7})
        ordinary = manifest()
        ordinary.update(abi="MoonLab_ModStart/v6", runtime_api_abi=1)
        packages.validate(ordinary)
        require_available(ordinary, None, runtime_api_abi=1, host_capabilities={})

    def test_mandatory_metadata_cannot_be_silently_ignored_by_older_backends(self):
        for base in (manifest(), managed()):
            base["requires_host"] = {"interaction": 1}
            with self.subTest(kind=base["kind"]), self.assertRaisesRegex(ValueError, "native v7"):
                packages.validate(base)
        for change in ({"requires_host": {}}, {"requires_host": None}, {"runtime_api_abi": None}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                packages.validate({**requiring_host(), **change})
        value = requiring_host()
        del value["requires_host"]
        with self.assertRaisesRegex(ValueError, "nonempty"):
            packages.validate(value)

    def test_invalid_or_unbounded_capability_metadata_and_receipts_reject(self):
        invalid = ([], "interaction", {"Interaction": 1}, {"bad.name": 1}, {"x" * 65: 1},
                   {"interaction": True}, {"interaction": 0}, {"interaction": -1},
                   {"interaction": 2**32}, {"interaction": "1"},
                   {"cap_" + str(i): 1 for i in range(33)})
        for table in invalid:
            with self.subTest(table=table), self.assertRaises(ValueError):
                packages.validate({**requiring_host(), "requires_host": table})
            with self.subTest(receipt=table), self.assertRaises(ValueError):
                require_available(requiring_host(), None, host_capabilities=table)
        value = copy.deepcopy(requiring_host())
        value["requires_host"] = {"a" * 64: 0xffffffff}
        packages.validate(value)
        require_available(value, None, host_capabilities=value["requires_host"])
