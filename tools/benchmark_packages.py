#!/usr/bin/env python3
"""Measure local package validation/import time or traced Python allocation.

Run the same synthetic archive against separate baseline/candidate Python roots.
Timing and allocation runs are separate; this does not measure game frame time.
"""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import sys
import tempfile
import time
import tracemalloc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('--python-root', type=Path, default=Path(__file__).resolve().parents[1] / 'python')
    parser.add_argument('--repeats', type=int, default=7)
    parser.add_argument('--allocations', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.repeats <= 100:
        parser.error('repeats must be 1..100')
    sys.path.insert(0, str(args.python_root.resolve()))
    from moon_mod_api import packages
    expected = packages.examine(args.package)
    results = {}
    for operation in ('examine', 'install'):
        elapsed, peaks = [], []
        for _ in range(args.repeats):
            with tempfile.TemporaryDirectory(prefix='moon-package-benchmark-') as directory:
                if args.allocations:
                    tracemalloc.start()
                start = time.perf_counter_ns()
                if operation == 'examine':
                    actual = packages.examine(args.package)
                else:
                    name, actual = packages.install(args.package, directory)
                elapsed.append(time.perf_counter_ns() - start)
                if args.allocations:
                    peaks.append(tracemalloc.get_traced_memory()[1])
                    tracemalloc.stop()
                assert actual == expected
                if operation == 'install':
                    assert packages.installed(Path(directory) / 'library' / name) == expected
        results[operation] = {'nanoseconds': elapsed, 'median_ns': statistics.median(elapsed),
                              'traced_peak_bytes': peaks}
    source = Path(packages.__file__)
    print(json.dumps({'package_sha256': hashlib.sha256(args.package.read_bytes()).hexdigest(),
                      'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                      'python': sys.version, 'allocations_enabled': args.allocations,
                      'results': results}, indent=2))


if __name__ == '__main__':
    main()
