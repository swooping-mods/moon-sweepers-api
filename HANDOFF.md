# Current milestone: private organization source push

Objective: push the reviewed moon-sweepers-api source to `swooping-mods`, as authorized by the user, using the installed GitHub CLI.

Decisions: use the private repository https://github.com/swooping-mods/moon-sweepers-api, preserving the original private visibility. Keep `main` tracking `origin/main`. Keep the index local and preserve concurrent API feature work. No PR, Nexus release, project license or additional repository is included.

State: The reviewed API baseline is published. The working tree also passes 12 focused tests, including five concurrent build-item tests; those feature edits remain uncommitted and are excluded from the source push. The published baseline matches all 11 files in the loader's tested API snapshot. Documentation now points at the organization repository. Initial source commit: `62c831cfb0ae045633ea626a937f1b18dbb1678f`. Final branch/privacy verification is recorded outside specs under `artifacts/organization-push.json`.

Next action: continue development in this checkout. Nexus pages, file IDs, uploader credentials and hosted-index integration remain separate rollout work; game, Wine, native Windows and co-op qualification were not rerun for this push.

Evidence: `verification/organization-push.md`; `artifacts/organization-push.json`; `artifacts/checks.json`; `vendored/extraction.json`; `specs/_readme.md`.
