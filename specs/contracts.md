# API and package boundaries

This repository owns the public C11 AMD64 hook SDK, the `moon-mod-package/v1` contract and the standard-library package tool implementation. It does not implement a game bootstrap, UI, web service or gameplay mod.

`include/moon_sweepers/{context,hooks,vehicle_input}.h` is the authoritative C surface. The exported runtime lookup remains `MoonLab_GetHookApi_v1`, and SDK consumers declare native package v5 with hook framework ABI 1. Context/subscription/table layouts and ownership/order rules are described in `docs/hooks.md`. The loader implements the functions and registration lifecycle; ABI compatibility is not a claim of game compatibility.

`python/moon_mod_api/packages.py` owns validation, integrity checks, installation and deterministic native dependency resolution. `docs/packages.md` describes its schema and limits. `storage.py` owns portable paths and atomic JSON storage; loader-specific locks/process ownership remain in the loader repository.

`pack.py` creates deterministic immutable archives from an author manifest and complete original payload. An author must supply explicit game pins; the SDK carries no default current-game hashes. `python -m moon_mod_api` exposes `pack` and `validate`. These tools perform local file I/O only and never download or run a mod.

`tools/export.py` emits either a developer ZIP with SHA256SUMS or a first-party consumer snapshot. Snapshots contain `include/`, `python/`, `docs/` and `snapshot.json`, recording the API version and complete file hashes. An existing differing snapshot is rejected; consumers explicitly review its replacement. Snapshot updates are content-pinned, not automatic tracking of a branch.

Current package version is 0.1.0. The SDK version, C hook ABI, manifest schema, native package ABI and individual mod versions are separate contracts. Existing MoonLab symbol spellings are intentionally retained to avoid a binary migration during source extraction.

Verification: `python3 tools/check.py` covers standalone header compilation, v5 role validation, portable paths, dependency ordering/cycles, mismatched game pins, conflicting hooks and package reproducibility/integrity/overwrite refusal. `tools/export.py` creates the candidate. GitHub checks run on pushes/PRs; a manual candidate workflow retains outputs. No publishing job or credentials are configured. Host checks do not qualify gameplay or a native Windows process.
