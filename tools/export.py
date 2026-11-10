#!/usr/bin/env python3
"""Export an exact API snapshot or SDK ZIP using only local first-party bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.4.0"


def payload():
    return {p.relative_to(ROOT).as_posix(): p.read_bytes()
            for folder in ("include", "python", "docs")
            for p in sorted((ROOT / folder).rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def snapshot(destination):
    destination = Path(destination)
    files = payload()
    lock = {"schema": "moon-api-snapshot/v1", "repository": "moon-sweepers-api",
            "version": VERSION, "files": {n: hashlib.sha256(b).hexdigest() for n, b in files.items()}}
    files["snapshot.json"] = (json.dumps(lock, indent=2) + "\n").encode()
    if destination.exists():
        actual = {p.relative_to(destination).as_posix(): p.read_bytes()
                  for p in destination.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        if actual != files:
            raise ValueError("Snapshot exists with different bytes; review the update before replacing it")
        return destination
    destination.mkdir(parents=True)
    for name, data in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args()
    if args.snapshot:
        print(snapshot(args.snapshot))
        return
    output = ROOT / "artifacts"
    output.mkdir(exist_ok=True)
    archive = output / f"moon-sweepers-api-{VERSION}.zip"
    files = payload()
    files["README.md"] = (ROOT / "README.md").read_bytes()
    files["THIRD_PARTY_NOTICES.md"] = (ROOT / "vendored/THIRD_PARTY_NOTICES.md").read_bytes()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as target:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            target.writestr(info, data)
    (output / "SHA256SUMS").write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + "  " + archive.name + "\n")
    print(archive)


if __name__ == "__main__":
    main()
