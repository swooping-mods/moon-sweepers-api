# Local preparation verification

Date: 2026-11-10. Target: `swooping-mods/moon-sweepers-api`. This historical check covered the selected first-party SDK extraction. Original extraction metadata is retained in ignored local recovery storage.

Outcome: the baseline extraction passed 7 focused tests, with no skipped or excluded tests. Concurrent build-menu/build-item work in the working tree is outside that result and is not included in the tested loader snapshot or SDK artifact. Standalone C header compilation, package role/version/path validation, dependency order/cycles, game-pin and hook-conflict checks, deterministic package authoring, payload integrity and overwrite refusal pass. SDK export produces a ZIP and SHA256SUMS. The loader consumer snapshot verifies all 11 files.

All baseline Python files parse. Both workflow YAML files parse and reference full action commit pins with read-only repository permissions. This is local structural review, not an actual GitHub Actions run. Source hygiene review found no game/compiled/asset payloads, private absolute paths, personal remote references or common credential/private-key markers in the source tree. Generated outputs are ignored. Specs routing links resolve to existing files.

Evidence: `artifacts/checks.json`, `artifacts/moon-sweepers-api-0.1.0.zip`, `artifacts/SHA256SUMS`. Generated evidence is retained locally under ignored `artifacts/`; it is not part of the new source repository's initial history.

Limits: no game, Wine, native Windows or co-op replay; no GitHub-hosted CI execution; no Nexus upload or URL liveness checks. The loader's current-game adapter and legacy ABI are preserved, not newly gameplay-qualified. No external dependencies were downloaded, organization repositories/remotes created, pushes performed or PRs opened.

## Generalization architecture review — 2026-11-10

Recorded the requested generalization goal and a proposed SDK/runtime/adapter
split in [design](../design/mod-platform.md), grounded in the central research
study and the [project snapshot](../research/mod-platform.md). Inspected all
52 workshop mod manifests (50 native, two companion), framework SDKs, managed
adapter contracts and reviewed Mars source/current retained qualification.
Existing unrelated edits and mod selections were preserved.

`python3 tools/check.py`: **12 passed**, no skips/exclusions. Synthetic independent
native manifests validate in both public and development implementations. A
synthetic independent BepInEx manifest is accepted by the workshop and rejected
by this public SDK as `Unsupported mod runtime`, confirming the current contract
gap. Source/manifest hashes and exact revisions are retained under ignored
`artifacts/generalization-review/inspection.json`; ordinary checks retain
`artifacts/checks.json`.

Authored-document review checks all 52 inventory rows and local navigation;
the initial check found one source link moved by concurrent external-mod
extraction, which was corrected to its new owner. The final result is retained
in `artifacts/generalization-review/document-check.json`.

This change documents architecture only. No runtime implementation, package
schema, C ABI, framework behavior or save data changed. Game/Windows/co-op replay,
managed bridging and performance benchmarking were not run for this review;
earlier retained Mars gameplay passes were read rather than repeated. The full
generalization objective remains unfinished.

## SDK 0.3 shared package/interface implementation — 2026-11-10

The SDK now owns native/managed backend validation, external provenance,
case-insensitive plugin/data identity checks, optional/required owner-qualified
interface dependencies, ABI/prefix/capacity checks and provider-neutral building
API selection. Existing numeric building identities and legacy package rules
remain. Native interface packages require v6 plus runtime API ABI 1 so older
loaders reject them explicitly. The existing managed backend cannot yet declare
native interfaces; that requires the pending bridge/host contract.

Both loaders pin the same complete 21-file SDK snapshot. The workshop's package
and managed-manifest modules now forward to it; its portable-layout and tamper
checks pass. The standalone loader can import a managed package, shows it as a
game mod, and refuses unavailable hosts before preparation. Both preparations
reject the unavailable native API registry. No runtime capability is inferred
from package metadata alone.

Final checks: **27 SDK tests**, **50 standalone loader tests**, and **52 focused
workshop tests** (46 loader, two SDK/portable checks, four building checks) pass.
No tests were skipped/excluded in those scopes. The standalone native bootstrap
and diagnostic cross-build/export checks pass; SDK 0.3 ZIP export passes. An
initial new test had a case-sensitive diagnostic assertion, corrected before
the final successful run.

Read-only checks validate all **53 actual installed packages** and order the
current 50-mod selection together with the exact reviewed Mars DLL as a 51-mod
set. The selection remains unchanged. This is metadata/byte-integrity evidence,
not new loaded-world or gameplay qualification.

Evidence: `artifacts/checks.json`,
`artifacts/generalization-review/api-check.log`,
`artifacts/generalization-review/catalog-regression.json`,
`artifacts/moon-sweepers-api-0.3.0.zip` and `artifacts/SHA256SUMS`.
Standalone checks/build logs are in that project's
`artifacts/generalization-review/`; workshop cycle receipts are indexed by its
`artifacts/api-contracts/generalization-checks.json`.

The runtime registry, framework SDK/publication migration, managed bridge,
production managed-adapter consolidation, gameplay/co-op and performance
qualification remain outside this implementation slice. No game, Wine or
native Windows process was started, no dependency was downloaded and no source
was pushed or published. The full generalization goal remains active.

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

## SDK 0.4 native runtime contracts — 2026-11-10

Added frozen runtime publication/lookup/frame tables, portable input/camera
contracts and bounded registry helpers, and the deterministic native startup
plan encoder. The standalone loader implements one shared API/hook/frame
registry with dependency-ordered commit, exact declaration/capacity matching,
prefix lookup and owner rollback. No global second startup phase is imposed.
The public Build Menu client now binds that registry under a recognized loader
and refuses an unavailable/incompatible table without starting another DLL.
The standalone modkit fallback and existing hook/save identities remain.

Final SDK gate: **32 tests pass**, no skips/exclusions. Separate public-client
execution under Clang and GCC ASan/UBSan checks missing/wrong runtime, wrong
domain ABI/size, no private load/start under a recognized loader, frame
subscription and the legacy fallback. Public runtime/input/camera C tables
compile for host and Windows AMD64. SDK 0.4 export and the complete **31-file**
standalone consumer snapshot verify; 36 local documentation links resolve.

The combined standalone loader gate passed **76 tests** at this checkpoint,
including independent public-SDK provider/consumer translation units calling
the production C registry under both sanitized compilers. API/thread/prefix
boundaries, every truncated plan prefix, malformed/trailing bytes, capacity
bounds, missing/failed publication and callback rollback pass. Actual inert v6
archives deploy a deterministic plan and preserve unknown edits to it. The
freestanding Windows AMD64 bootstrap/diagnostic build and exports pass.
Concurrent installed-mode additions are included in that combined gate and
have separate owning qualification; they are not attributed to this SDK change.

Evidence: `artifacts/checks.json`,
`artifacts/generalization-review/api-0.4-check.log`,
`artifacts/generalization-review/sdk-0.4-document-check.json`,
`artifacts/moon-sweepers-api-0.4.0.zip`, `artifacts/SHA256SUMS`,
`artifacts/registry-sdk-0.4.0-reviewed/snapshot.json` and the standalone loader's
`artifacts/generalization-review/loader-0.4-check.log`.

Limits: the workshop/framework migration is coordinated with its owning task;
the selected Little Helpers native closure is held unchanged during its separate
qualification window. This task ran no game, Wine, native Windows or co-op
process. Managed bridges, framework-specific end-to-end qualification and
matched performance measurements remain unfinished. No dependency was acquired,
source pushed, PR opened or release published. The full goal remains active.

### Final input integration correction

The framework integration review found two stale input-helper behaviors in the
initial SDK candidate: registering a default chord while held suppressed its
first press, and a malformed initial override left the display label empty.
Applied the final owning input-worker correction to the canonical SDK and
retained its production harness as a public-header regression. Five statement
line breaks also remove GCC misleading-indentation warnings without changing
behavior. The shared camera adapter's existing production harness now executes
against the standalone loader and canonical camera headers as well.

Final gates: **33 SDK tests** and **80 combined standalone loader tests pass**,
with no skips/exclusions; the native AMD64 build/export check passes. Both input
and camera harnesses execute under Clang/GCC ASan/UBSan. The final standalone
bootstrap hash is `30ba9036aa3cbb904239bf4251145c24fc6b33f1d62c7b04b553cf8a62c2a054`.
The final reviewed **31-file** snapshot is
`artifacts/registry-sdk-0.4.0-final/snapshot.json`; it supersedes the earlier
same-version local candidates. Final gate/build logs use `*-0.4-final-*` under
both projects' `artifacts/generalization-review/`.

The installed-mode owner repeats its Windows package/UI/Wine checks against
these final bytes before the combined local source commit. Those checks remain
separate from native Windows gameplay and actual game save/co-op qualification.
The managed-adapter owner also confirmed that current mixed package ordering
does not implement cross-backend startup readiness; the design records that
remaining boundary explicitly.

The final author-SDK export review also compiles the complete public Building
bootstrap as an independent Windows AMD64 translation unit. It found the new
connector's missing GetModuleHandleA import declaration in that bootstrap,
which the original synthetic platform fixture supplied itself. Added the import
and retained the complete-bootstrap regression: **34 SDK tests now pass** with
no skips/exclusions. The canonical snapshot is
`artifacts/registry-sdk-0.4.0-bootstrap/snapshot.json` (31 files), differing from
the preceding input-qualified snapshot only in that declaration. This does not
change loader runtime DLL behavior or its recorded hash; distribution content
and static snapshot checks must use the updated header.

### Portable camera host ownership

Independent framework SDK export review found the native Camera connector still
included a private loader implementation. Moved that exact thread-gated host
into public `camera_host.h`; the standalone loader now forwards to it. Only the
guard/include location changes; implementation bytes from the registry storage
through all callbacks/table functions match the prior host. The rebuilt runtime
DLL remains exactly `30ba9036aa3cbb904239bf4251145c24fc6b33f1d62c7b04b553cf8a62c2a054`,
so the installed-mode owner's six Wine controls still cover the same binary.
Its previously reviewed atomic implementation boundary is standalone commit
`78ccced`; the portable-host follow-up is separate.

Final SDK gate: **35 tests pass**; standalone gate: **80 pass**, no skips or
exclusions. The public host and actual loader camera adapter both execute the
production exclusivity/thread/restore-retry/capacity harness under Clang/GCC
ASan/UBSan. Native AMD64 rebuild/export checks pass. The canonical SDK snapshot
is now `artifacts/registry-sdk-0.4.0-camera-host/snapshot.json` (**32 files**),
with `*-0.4-camera-host-*` gate/build logs under each project's existing ignored
generalization verification directory. This supersedes earlier same-version
local candidates. The framework owner runs its separate relocated-SDK consumer
and native package checks. No ABI or camera algorithm changed.

## Package identity and managed deployment convergence — 2026-11-10

Aligned owner-qualified API prefixes with the existing package key grammar,
including `3d-tools`, `test-3d` and `7`; service suffixes remain letter-leading.
Invalid/trailing/doubled hyphens and uppercase package IDs still reject. The
standalone native package-ID and startup-plan parser were aligned in the
coordinated public review, including actual encoded numeric provider/consumer
contracts. **36 SDK tests pass**, with no skips/exclusions. The current pinned
SDK is `artifacts/registry-sdk-0.4.0-numeric-ids` (**32 files**); headers and C
layouts are unchanged.

The standalone loader now implements explicitly attached managed hosting in
private-copy mode, separate plugin/data namespaces, filtered native startup,
managed-only empty native plans and transactional executable-input allowlists.
Its Python deployment helper is canonical; the workshop consumes an exact
hash-pinned copy. Workshop loader **46 tests** plus the source-pin check pass.
The existing C# adapter/generator/profile/repair implementation is reused via
checked artifacts, with no second implementation or automatic downloads.

The latest combined standalone gate passes **96 tests**, no skips/exclusions.
Native AMD64 and Windows portable builds/static checks pass. Its public-review
owner ran all six bounded Wine controls against the exact produced runtime and
portable app: DLL guards, Python/Qt and real launcher paths pass. Runtime hash:
`cb93b91d582615b248b526e78e724dff00390ba060585a4cb7c5fea0c3e2bbdd`;
Windows ZIP hash:
`9119c13a8806f010a1e7e26a40279910703d6f0330552843f631c5119bf3d233`.
This includes the shared RDX stack-home prologue fix copied from its actual
GPS consumer and exercised under both sanitized C compilers.

Those package/Wine checks use the default native distribution. Real attachment
of the retained screened BepInEx bundle, standalone managed world/save/restart
and cross-backend readiness/service bridging remain separate work. Installed
mode refuses managed mods. Native Windows gameplay, co-op and arbitrary Unity/
game profiles remain unqualified. The full goal stays active; no publication
or original-game/personal-save mutation occurred.

### Offline managed attachment package

Reused the existing exact screened upstream closure and qualified original
adapter (`2132c03e66ff08f16f1ba819cefa30b46a8fbc42d3b825028f69589c025b7a0a`).
All **234 distribution files** and the recorded build inputs match. The existing
intake's extracted-file scan/static dispositions are retained, including its
stale-signature and outer-archive coverage limits; no download or scanner
update was performed. This reuse decision allows offline local packaging only
at this checkpoint, with no upstream host/plugin execution.

The canonical builder attachment and standalone `--with-bepinex` path pass.
The managed-private source ZIP verifies every host-file hash, preserves source
archives/notices, omits local intake/build directories from its receipt and
contains no game executable, GameAssembly or Steam AppID file. Its native
runtime remains the same `cb93b91d...` build; default source/Windows checksum
bytes remain unchanged. Managed ZIP hash:
`c9040a2c69b0252a3b2258babe2e7630ebd4e370c879b35c9654f72a8575a366`.
The full host gate still passes **96 tests**. Machine evidence lives in the
standalone project's `artifacts/managed-generalization/{intake-reuse,package-check}.json`
and `final-host-check.log`. The managed loaded-game/save/restart test remains
required; the existing replay currently imports the workshop Service and must
explicitly exercise the standalone code before that result can be claimed.

### Standalone managed game qualification

That packaged candidate now passes actual private Steam execution through its
own Python loader and pinned SDK. Workshop commit `db1e2dc` adds the explicit
`--use-bundle-loader` replay route, selects imports before either module family
loads, requires an unaliased artifact and private mode, and records/rechecks
actual source hashes. Seven focused profile/selection checks pass through the
owning test-cycle runner. A generated original probe icon removes the former
dependency on a bundled feature mod.

The unchanged source archive `c9040a2c...`, native proxy `cb93b91d...`, adapter
`2132c03e...` and 32-file numeric-ID SDK are the actual executed closure. In the
independent `bepinex-api` lane:

- Original managed-only probe `92232054f7bc4ee094e1ed4cfb22c583` passes native
  object calls, Harmony prefix/postfix/unpatch and injected component lifecycle.
  The proxy records the empty native plan, managed-only host and load completion.
- Fresh Mars world `e11433e56cd84f2096b0ae076cce4e40` and second-process replay
  `d3fb61e5da274a01b326e0310eda1432` pass 27 hooks with zero plugin errors,
  movement/physics callers, real MarsSessions saves, menu/MARS badge, reload and
  normal exit. The second process retains directory, gravity 3.71 and seed 19761.
- Mixed replay `b4f85925b6d04437a8f5131ea23cf7f7` additionally passes two Mars
  terminal open/close cycles with zero stacking requests, followed by exactly
  one plain Ctrl+K request. It uses the current native v6 Item Stacking package,
  SHA-256 `32c2acc4a4cf6ab8cc12f483d1e1806b32432e124a92f34f09a8d36b4d6c3e9f`.
  Save/reload, retained settings and normal exit pass again. This tests request
  arbitration, not actual placement of cargo capsules.

Every run restores its private profile/prefix and preserves source game bytes.
World/reload/badge captures were inspected; renderer is NVIDIA RTX 2080 Ti under
muted headless Gamescope. The desktop selection, personal saves and frozen
feature bundles were not changed. Full standalone gate: **96 tests pass**, no
skips; SDK gate: **36 pass**. The machine index is
`moon-sweepers-mod-loader/artifacts/managed-generalization/live-qualification.json`,
beside the two bounded activation-delta reviews and final host log.

The first mixed attempt `19d02d3f690143fda3ae7f9418ceb72d` remains failed: its
second terminal opening timed out after an observed first open/close cycle.
The successful retry uses 0.8-second holds and an explicit current native
package instead of the historical catalog fixture; those changes were not
isolated as a causal experiment. No observer check was weakened. Artificial
outdoor teleport staging remains independently failed/unqualified in these
world runs, as in the earlier adapter campaign.

These are bounded private development tests of the pinned .NET 6.0.7 closure,
reusing the exact prior intake with its stale-signature/source-equivalence
limits. There was no dependency download or public release. Native Windows,
co-op, arbitrary plugins/game profiles, all-catalog combinations and whole-game
FPS remain unqualified. Hosting alone establishes neither a typed managed
framework bridge nor cross-backend startup readiness; that part of the
generalization goal remains active.
