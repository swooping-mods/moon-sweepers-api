# Organization source push

Date: 2026-11-10. The user authorized pushing the reviewed API and loader repositories under `swooping-mods` and explicitly requested `gh`. The private GitHub target is https://github.com/swooping-mods/moon-sweepers-api. The installed GitHub CLI creates/inspects the repository; Git transfers the committed branch using existing host authentication.

Initial source commit: `62c831cfb0ae045633ea626a937f1b18dbb1678f`. `origin` targets this organization repository and `main` tracks `origin/main`. The index repository is outside this push. The source destination is private, matching the original development repository.

The reviewed API baseline is published. The working tree also passes 12 focused tests, including five concurrent build-item tests; those feature edits remain uncommitted and are excluded from the source push. The published baseline matches all 11 files in the loader's tested API snapshot.

Only committed reviewed source and this task's explicit documentation updates are pushed. Generated output, game files, saves, credentials and concurrent uncommitted feature work stay local. No PR or release is created.

Final remote branch SHA, local SHA, visibility, workflow status and preserved working-tree state are recorded in ignored `artifacts/organization-push.json`. Local checks are recorded in `artifacts/checks.json`. Hosted CI excludes the loader's two Qt tests, which passed locally. Game, Wine, native Windows and co-op were not run for publication.
