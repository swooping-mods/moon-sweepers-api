# API and package boundaries

The source repository is public at [swooping-mods/moon-sweepers-api](https://github.com/swooping-mods/moon-sweepers-api). Product contracts and author tools belong here; organization rollout records and local session notes do not.

This repository owns the public C11 AMD64 hook SDK, the `moon-mod-package/v1` contract and the standard-library package tool implementation. It does not implement a game bootstrap, UI, web service or gameplay mod.

`include/moon_sweepers/{context,hooks,vehicle_input}.h` is the authoritative C hook surface. The building SDK and saved-ID coordination are owned by [the building spec](building-api.md). The exported runtime lookup remains `MoonLab_GetHookApi_v1`, and shared hook consumers declare native package v5 (or v6 when also using the new runtime interface contract) with hook framework ABI 1. Context/subscription/table layouts and ownership/order rules are described in `docs/hooks.md`. The loader implements the functions and registration lifecycle; ABI compatibility is not a claim of game compatibility.

`python/moon_mod_api/packages.py` owns validation, integrity checks, installation and deterministic native/managed dependency resolution. `runtimes.py` owns backend identities, managed plugin/data namespaces and optional external provenance. Loaders may pass an explicit `available_runtimes` set to reject unsupported hosts independently of package validity. `docs/packages.md` describes the schema and limits. `storage.py` owns portable paths and atomic JSON storage; loader-specific locks/process ownership remain in the loader repository.

Import takes one private temporary-file snapshot of a regular source file, bounded
by the actual 64 MiB read count. Its digest, validated manifest and extracted bytes
belong to that same snapshot even if the download pathname is replaced. Validation
and extraction stream members, retaining ZIP CRC and SHA-256 checks and final
installed-tree verification. Icon admission reads its 24-byte header; the complete
icon still passes the payload hash/CRC check. Temporary snapshot storage costs up
to 64 MiB per import and is released on every exit. Malformed JSON roots and
non-string runtime/entry/icon identities produce validation errors.

`tools/benchmark_packages.py` exercises examination and a fresh import of the same
archive against an explicit Python source root. Clean time and traced allocation
runs are separate; exact manifest and installed-tree parity gate every sample.
The accepted change bounds Python allocation, with disk snapshot overhead included
in import timing. It does not establish a game-frame or universal latency gain.

`pack.py` creates deterministic immutable archives from an author manifest and complete original payload. Legacy and managed authors supply explicit game pins; native v8 instead declares its [adapter contract](compatibility.md), with any supplied pins retained as restrictions. The SDK carries no default current-game hashes. `python -m moon_mod_api` exposes `pack` and `validate`. These tools perform local file I/O only and never download or run a mod.

`tools/export.py` emits either a developer ZIP with SHA256SUMS or a first-party consumer snapshot. Snapshots contain `include/`, `python/`, source-only `managed/`, `docs/` and `snapshot.json`, recording the API version and complete file hashes. An existing differing snapshot is rejected; consumers explicitly review its replacement. Snapshot updates are content-pinned, not automatic tracking of a branch.

Current package version is 0.7.1. The SDK version, C hook ABI, manifest schema, native package ABI and individual mod versions are separate contracts. Existing MoonLab symbol spellings are intentionally retained to avoid a binary migration during source extraction. [Mod-provided interfaces](interfaces.md) owns package metadata; [runtime services](runtime-services.md) owns the new C tables and deterministic native startup plan. The loader implements publication, lookup, frame dispatch and platform input/camera adapters; this repository supplies their portable contracts and helpers.

Verification: `python3 tools/check.py` covers standalone header compilation, v5 role validation, portable paths, dependency ordering/cycles, mismatched game pins, conflicting hooks and package reproducibility/integrity/overwrite refusal. `tools/export.py` creates the candidate. GitHub checks run on pushes/PRs; a manual candidate workflow retains outputs. No publishing job or credentials are configured. Host checks do not qualify gameplay or a native Windows process.
