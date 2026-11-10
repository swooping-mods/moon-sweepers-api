"""Public native ABI and deterministic runtime plans need no game files."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from test_interfaces import provider, consumer
from test_runtimes import managed
from moon_mod_api.runtime_plan import encode, MAGIC


class RuntimePlanChecks(unittest.TestCase):
    def test_plan_is_deterministic_and_excludes_managed_entries(self):
        a, b, plugin = provider(), consumer(), managed()
        values = {mod["id"]: mod for mod in (a, b, plugin)}
        order = [a["id"], b["id"], plugin["id"]]
        data = encode(values, order)
        self.assertEqual(data[:12], MAGIC + (2).to_bytes(4, "little"))
        self.assertEqual(data, encode(dict(reversed(list(values.items()))), order))
        self.assertNotIn(plugin["id"].encode(), data)

    def test_reverse_dependency_order_and_duplicate_selection_reject(self):
        a, b = provider(), consumer()
        values = {mod["id"]: mod for mod in (a, b)}
        with self.assertRaisesRegex(ValueError, "dependency-first"):
            encode(values, [b["id"], a["id"]])
        with self.assertRaisesRegex(ValueError, "selection"):
            encode(values, [a["id"], a["id"]])

    def test_optional_absence_omits_runtime_requirement(self):
        value = consumer(optional=True)
        data = encode({value["id"]: value}, [value["id"]])
        self.assertNotIn(b"other-authors-library", data)
        self.assertEqual(encode({}, []), MAGIC + b"\0\0\0\0")

    def test_public_services_input_camera_compile_without_loader_typedefs(self):
        root = Path(__file__).resolve().parents[1]
        source = '''#include "moon_sweepers/runtime.h"
#include "moon_sweepers/input.h"
#include "moon_sweepers/camera.h"
_Static_assert(sizeof(MoonServicePublicationV1)==32,"base");
_Static_assert(sizeof(MoonServicePublicationLimitsV1)==48,"capacities");
int main(void){return moon_runtime_api_valid(0)||moon_input_api_valid(0)||moon_camera_api_valid(0);}
'''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "consumer.c"
            path.write_text(source)
            for target in ([], ["--target=x86_64-pc-windows-msvc"]):
                subprocess.run(["clang", *target, "-std=c11", "-Wall", "-Wextra", "-Werror",
                                "-I", str(root / "include"), "-fsyntax-only", str(path)], check=True)
