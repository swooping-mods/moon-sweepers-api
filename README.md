# Moon Sweepers API

Versioned C mod contracts and offline `.msmod` package tools for Moon Sweepers.
Target repository: `swooping-mods/moon-sweepers-api`. This is a local preparation; the organization repository has not been created by this task.

The API is a small SDK, not a web service. It owns the hook ABI, package format, integrity checks, dependency ordering and package authoring. The desktop loader implements the ABI. Shop, Equipment, Vehicle, Sound and other gameplay frameworks remain independently versioned mods.

- `include/moon_sweepers/`: standalone Windows AMD64 C11 headers.
- `python/moon_mod_api/`: standard-library package validation, resolution and authoring.
- [Hook guide](docs/hooks.md), [package contract](docs/packages.md), [mod CI](docs/mod-ci.md).
- [Repository split and release flow](https://github.com/swooping-mods): intended organization; the detailed local proposal is in the loader's `design/repository-split.md`.

Use installed Python 3.11+; no dependency installation is required:

```sh
PYTHONPATH=python python3 -m moon_mod_api validate path/to/mod.msmod
PYTHONPATH=python python3 -m moon_mod_api pack manifest.json payload/ artifacts/example.msmod
python3 tools/check.py
python3 tools/export.py
```

Authors must supply explicit game compatibility hashes. The SDK never invents compatibility pins. The packager writes hashes for every payload file and refuses to overwrite a different archive. SDK ZIPs and checksum files go to ignored `artifacts/`.

Consumers pin a reviewed API snapshot using `python3 tools/export.py --snapshot /path/to/consumer/vendored/api`; an existing snapshot with different bytes is rejected. The snapshot records every included file's SHA-256 and API version. Consumers commit it and review API updates in a PR.

GitHub Issues/PRs own API and packaging development. Nexus Mods is the main player download portal for the loader and mods. The SDK is a developer download; it is not an additional player installation requirement. No game binaries, mod assets or dependency runtimes are included, and no project license has been assigned.

Read [specs/_readme.md](specs/_readme.md) and [HANDOFF.md](HANDOFF.md) for current boundaries and verification.
