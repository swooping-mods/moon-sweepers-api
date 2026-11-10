# Current milestone: clean local organization repository

Objective: prepare `swooping-mods/moon-sweepers-api` for user inspection without pushing or publishing.

Decisions: split API/contracts and package tools, desktop/native loader, and metadata-only index into separate repositories. Keep the existing MoonLab native ABI. Pin the loader's first-party API snapshot by file hashes. Keep gameplay mods independently versioned; Nexus is the intended player portal, GitHub owns code/Issues/PRs. Do not assign a project license.

State: the baseline first-party extraction and focused documentation/specs are committed locally. Its 7 focused tests passed. Concurrent build-menu headers, build-item validator/tests and related documentation are present as separate uncommitted work; they are preserved and excluded from this extraction commit and tested SDK artifact. CI source checks and manual candidate workflows are defined; neither publishes. The existing development checkout was not modified by this task. Public source/Nexus endpoints remain unassigned; catalog entries remain development-only. See `verification/local-preparation.md` for checks and limits.

Next action: user reviews the committed extraction and the loader's `design/repository-split.md`; the concurrent build-item work needs its own verification and commit. After acceptance, repository creation/push, Nexus destinations/credentials and hosted-index integration are separate rollout work. No remote is configured.

Evidence: `vendored/extraction.json`; `verification/local-preparation.md`; `artifacts/checks.json`, `artifacts/moon-sweepers-api-0.1.0.zip`, `artifacts/SHA256SUMS`; `specs/_readme.md`.
