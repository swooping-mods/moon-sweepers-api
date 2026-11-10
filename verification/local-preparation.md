# Local preparation verification

Date: 2026-11-10. Target: `swooping-mods/moon-sweepers-api`. This historical check covered the selected first-party SDK extraction. Original extraction metadata is retained in ignored local recovery storage.

Outcome: the baseline extraction passed 7 focused tests, with no skipped or excluded tests. Concurrent build-menu/build-item work in the working tree is outside that result and is not included in the tested loader snapshot or SDK artifact. Standalone C header compilation, package role/version/path validation, dependency order/cycles, game-pin and hook-conflict checks, deterministic package authoring, payload integrity and overwrite refusal pass. SDK export produces a ZIP and SHA256SUMS. The loader consumer snapshot verifies all 11 files.

All baseline Python files parse. Both workflow YAML files parse and reference full action commit pins with read-only repository permissions. This is local structural review, not an actual GitHub Actions run. Source hygiene review found no game/compiled/asset payloads, private absolute paths, personal remote references or common credential/private-key markers in the source tree. Generated outputs are ignored. Specs routing links resolve to existing files.

Evidence: `artifacts/checks.json`, `artifacts/moon-sweepers-api-0.1.0.zip`, `artifacts/SHA256SUMS`. Generated evidence is retained locally under ignored `artifacts/`; it is not part of the new source repository's initial history.

Limits: no game, Wine, native Windows or co-op replay; no GitHub-hosted CI execution; no Nexus upload or URL liveness checks. The loader's current-game adapter and legacy ABI are preserved, not newly gameplay-qualified. No external dependencies were downloaded, organization repositories/remotes created, pushes performed or PRs opened.

## Public source cleanup verification — 2026-11-10

The proposed public baseline passed all seven focused API tests, with no skips or
exclusions. Its SDK headers, Python implementation, author guides, tools and tests
match the previously hosted baseline. Local Markdown links resolve; publication
hygiene checks found no private workstation paths or common credential markers.
Retired setup/publication records and extraction metadata were moved to ignored
local recovery storage. The stale private-source claim, removed planning link and
obsolete Nexus-first download guidance were corrected.

The normal development working tree also passed 27 tests. Its two unpublished
feature commits and uncommitted SDK/runtime-interface changes remain local and
are excluded from this publication. Exact source test receipts and publication
identities are retained under ignored `artifacts/public-source-cleanup/`.
No game, native Windows or co-op test was run for this documentation cleanup.
