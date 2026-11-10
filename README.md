# Moon Sweepers API

Versioned C mod contracts and offline `.msmod` package tools for Moon Sweepers.
Repository: [swooping-mods/moon-sweepers-api](https://github.com/swooping-mods/moon-sweepers-api). The source is public on GitHub.

The API is a small SDK, not a web service. It owns the hook ABI, package format, integrity checks, dependency ordering and package authoring. The desktop loader implements the ABI. Shop, Equipment, Vehicle, Sound and other gameplay frameworks remain independently versioned mods.

- `include/moon_sweepers/`: standalone Windows AMD64 C11 headers.
- `python/moon_mod_api/`: standard-library package validation, resolution and authoring.
- [Hook guide](docs/hooks.md), [package contract](docs/packages.md), [mod CI](docs/mod-ci.md).
- [Building API and stable IDs](docs/building-api.md), [shared API conventions](docs/conventions.md).
- [Mod-provided interfaces](docs/interfaces.md): independent provider requirements, ABI/size/capacity checks and optional integration.
- [Generalization proposal](design/mod-platform.md) and [research evidence](research/mod-platform.md): planned runtime/adapter boundaries and independent framework SDKs; not implemented API guarantees.
- [Desktop loader and release instructions](https://github.com/swooping-mods/moon-sweepers-mod-loader/blob/main/CONTRIBUTING.md).

Use installed Python 3.11+; no dependency installation is required:

```sh
PYTHONPATH=python python3 -m moon_mod_api validate path/to/mod.msmod
PYTHONPATH=python python3 -m moon_mod_api pack manifest.json payload/ artifacts/example.msmod
python3 tools/check.py
python3 tools/export.py
```

Authors must supply explicit game compatibility hashes. The SDK never invents compatibility pins. The packager writes hashes for every payload file and refuses to overwrite a different archive. SDK ZIPs and checksum files go to ignored `artifacts/`.

Consumers pin a reviewed API snapshot using `python3 tools/export.py --snapshot /path/to/consumer/vendored/api`; an existing snapshot with different bytes is rejected. The snapshot records every included file's SHA-256 and API version. Consumers commit it and review API updates in a PR.

GitHub hosts API source, issues and code review. The desktop loader owns its player downloads and release workflow; each mod author owns their downloads. The SDK is a developer download; it is not an additional player installation requirement. No game binaries, mod assets or dependency runtimes are included, and no project license has been assigned.

Read [specs/_readme.md](specs/_readme.md) for current boundaries and verification.
