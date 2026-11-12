"""Run the shared production input harness against the exported SDK helpers."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InputRegistryChecks(unittest.TestCase):
    def test_failed_capture_retains_session_until_acknowledged_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            for compiler in ("clang", "gcc"):
                with self.subTest(compiler=compiler):
                    binary = Path(directory) / (compiler + "-camera-begin")
                    subprocess.run([compiler, "-std=c11", "-Wall", "-Wextra", "-Werror", "-O1",
                                    "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                                    "-I", str(ROOT / "include"),
                                    str(ROOT / "tests/native_camera_begin_checks.c"), "-o", str(binary)], check=True)
                    result = subprocess.run([str(binary)], check=True, capture_output=True, text=True)
                    self.assertIn("retained release token and explicit cleanup retry passed", result.stdout)

    def test_interaction_arbitration_capture_snapshots_rollback_and_capacity(self):
        with tempfile.TemporaryDirectory() as directory:
            for compiler in ("clang", "gcc"):
                with self.subTest(compiler=compiler):
                    binary = Path(directory) / (compiler + "-interaction")
                    subprocess.run([compiler, "-std=c11", "-Wall", "-Wextra", "-Werror", "-O1",
                                    "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                                    "-I", str(ROOT / "include"),
                                    str(ROOT / "tests/native_interaction_registry_checks.c"), "-o", str(binary)], check=True)
                    result = subprocess.run([str(binary)], check=True, capture_output=True, text=True)
                    self.assertIn("interaction arbitration:", result.stdout)

    def test_exported_camera_host_exclusivity_threads_restore_and_capacity(self):
        with tempfile.TemporaryDirectory() as directory:
            for compiler in ("clang", "gcc"):
                with self.subTest(compiler=compiler):
                    binary = Path(directory) / (compiler + "-camera")
                    subprocess.run([compiler, "-std=c11", "-Wall", "-Wextra", "-Werror", "-O1",
                                    "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                                    "-I", str(ROOT / "include"),
                                    str(ROOT / "tests/native_camera_host_checks.c"), "-o", str(binary)], check=True)
                    result = subprocess.run([str(binary)], check=True, capture_output=True, text=True)
                    self.assertIn("restoration passed", result.stdout)

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
