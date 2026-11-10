# Local preparation verification

Date: 2026-11-10. Target: `swooping-mods/moon-sweepers-api`. Source is a selected first-party extraction, with source byte identities under `vendored/extraction.json`.

Outcome: the baseline extraction passed 7 focused tests, with no skipped or excluded tests. Concurrent build-menu/build-item work in the working tree is outside that result and is not included in the tested loader snapshot or SDK artifact. Standalone C header compilation, package role/version/path validation, dependency order/cycles, game-pin and hook-conflict checks, deterministic package authoring, payload integrity and overwrite refusal pass. SDK export produces a ZIP and SHA256SUMS. The loader consumer snapshot verifies all 11 files.

All baseline Python files parse. Both workflow YAML files parse and reference full action commit pins with read-only repository permissions. This is local structural review, not an actual GitHub Actions run. Source hygiene review found no game/compiled/asset payloads, private absolute paths, personal remote references or common credential/private-key markers in the source tree. Generated outputs are ignored. Specs routing links resolve to existing files.

Evidence: `artifacts/checks.json`, `artifacts/moon-sweepers-api-0.1.0.zip`, `artifacts/SHA256SUMS`. Generated evidence is retained locally under ignored `artifacts/`; it is not part of the new source repository's initial history.

Limits: no game, Wine, native Windows or co-op replay; no GitHub-hosted CI execution; no Nexus upload or URL liveness checks. The loader's current-game adapter and legacy ABI are preserved, not newly gameplay-qualified. No external dependencies were downloaded, organization repositories/remotes created, pushes performed or PRs opened.
