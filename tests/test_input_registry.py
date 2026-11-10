"""Run the shared production input harness against the exported SDK helpers."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InputRegistryChecks(unittest.TestCase):
    def test_default_edges_overrides_gates_rebinding_and_capacity(self):
        with tempfile.TemporaryDirectory() as directory:
            for compiler in ("clang", "gcc"):
                with self.subTest(compiler=compiler):
                    binary = Path(directory) / compiler
                    subprocess.run([compiler, "-std=c11", "-Wall", "-Wextra", "-Werror", "-O1",
                                    "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                                    "-I", str(ROOT / "include"),
                                    str(ROOT / "tests/native_input_registry_checks.c"), "-o", str(binary)], check=True)
                    result = subprocess.run([str(binary)], check=True, capture_output=True, text=True)
                    self.assertIn("production checks passed", result.stdout)
