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


## SDK 0.5 managed native-service consumers — 2026-11-10

SDK 0.5 adds a provider-neutral source C# connector and explicit native startup
readiness without changing the frozen 40-byte runtime table. Managed packages
may declare native `requires_apis` with runtime API ABI 1; native publication
remains owned by dependency-ordered native v6 ModStart. Selection/preparation
require target readiness ABI 1. The connector only inspects the resident loader,
returns pending without lookup and caches connector delegates. Domain wrappers
cache their resolved tables/typed delegates after Ready; RuntimeClient.TryFind
itself repeats native lookup on every call.
Framework-specific wrappers remain with their ordinary owning mods.

The complete API gate passes **38 tests**, zero skips/exclusions, with installed
`MOON_API_DOTNET` explicitly set. Actual compiled C# to C checks cover missing
exports, ABI/size/null-function refusal, pending/failed/unknown readiness,
numeric owners and service grammar, real typed results and delegate lifetime
through forced GC and 10,000 calls. The first managed manifest fixture retained
native-only hook markers; removing those fixture fields corrected its validation
failure. No SDK implementation relaxation was needed for that failure.

Snapshot `artifacts/registry-sdk-0.5.0-managed-consumers` contains **34 files**;
both standalone and workshop consumers explicitly verify the same pin.
The standalone complete gate passes **98 tests**, zero skips/exclusions,
including production C startup readiness after owner commit/hook installation
and refusal before game copying when readiness capability is absent, invalid
or replaced after selection. Strict AMD64 compile/link/export checks pass.
Its new runtime is `b36b175e623d018c920a3c8153074af6da42ea1452094a531e78d3d2592620e0`.
The previous qualified runtime and managed archive remain historical exact
candidates; their game results are not transferred to this one.

The workshop's framework-owned Hints C# wrapper compiles from a relocated source
export against the native production parser/registry under Clang and GCC. Actual
calls cover UTF-8, copied input, native frame expiry, wrong-thread refusal,
independent keys, disposal, stable-slot capacity and forced GC. A warmed host
batch of 10,000 Publish calls allocates zero current-thread managed bytes.
Compilation against retained Windows .NET 6 metadata also passes. An initial
metadata compile accidentally included a native runtime DLL; filtering by the
PE CLI directory corrected that tooling input error. These results qualify
host FFI/lifetimes, not same-frame Unity hint presentation or FPS.

The source exporter now retains public C headers plus explicitly public managed
source roots. Five exporter tests, thirteen relocated strict C consumers, one
compiled managed fixture and **47 workshop loader tests** pass. Export aliases,
private siblings and source additions during sealing reject. The new export has
73 headers across ten frameworks and two C# files. No .NET installation is
required to export or compile C-only consumers.

A separate private native-provider/managed-consumer game startup candidate is
prepared under the workshop's `artifacts/api-generalization/managed-bridge-sdk05`.
It uses only an original arithmetic diagnostic and the screened optional host;
its pending bounded game proof does not qualify Hints UI or borrow/live-object
admission. The normal delivered runtime `51549df4...`, Shop candidate and user
library/default seeds are preserved during GPS's separate proof/import hold.


The separate live native/managed startup candidate subsequently **passes** at
workshop run `0d29a1c5a6d343a0841a50b33b9d1bab`. Its standalone archive is
`3d052bd99dbdf1572fb4b76d09216a8fe92cdc8349d3bd1efc34cc594921a2c9`,
using runtime b36 and the unchanged screened adapter 2132. Native events record
ordinary provider commit and runtime-services-ready. The managed consumer sees
Ready, obtains typed result 42, survives forced GC and executes exactly 10,000
native calls with zero current-thread managed allocation in that batch. The
original managed interop/component/prefix-postfix/restoration probe also passes.
Actual initial state was already Ready, so real Pending timing is not claimed;
that branch remains host-tested. This headless startup diagnostic establishes
neither loaded-world/save behavior on b36 nor same-frame Hints presentation.
The owned process is intentionally stopped after observables; no normal-exit
claim is made. Prefix/profile/source/loader/SDK/driver/probe preservation and
process-group cleanup pass, and the queue was explicitly released to GPS.

Exact receipts and bounded limits are retained in the workshop's
`artifacts/api-generalization/managed-bridge-sdk05/live-qualification.json`.
Its frozen default native runtime still lacks the new readiness export; the
workshop source/preparation gate refuses opted-in consumers until a separately
reviewed source sync/runtime upgrade. No frozen default or user library import
is performed by this bridge qualification.


A final standalone host gate passes **99 tests**, zero skips/exclusions, adding
an actual production seal/readiness check for a managed-only empty native plan.
This covers the distinct no-native-ModStart startup path without adding another
game run to the released slot. The b36 production runtime bytes are unchanged.

### Workshop SDK 0.5 startup qualification

Workshop runtime `370919027f2be02082bbb97ee3611f95b203934e4c6ea0696a72cb6b1a80d77e`
passes run `51556b359b47452da8b1560c87b397c0` through its own nested SDK and
Python loader. Independent native provider/managed consumer: Ready, typed 42,
forced GC, exactly 10,000 native calls, zero managed bytes in the measured batch.
Initial state was Ready; Pending timing remains host-tested. Original interop
probe and prefix/profile/source/input preservation pass. Explicit cleanup receipt
confirms process group 3404052 absent. No loaded-world/save, Hints legend-order,
co-op, native Windows or frame-time claim. Frozen default runtime 51549 and its
receipt were preserved.

### Generic host-adapter capability admission

SDK 0.6 introduces native package v7 `requires_host`, a bounded exact-ABI map
independent of mod/provider identities. Existing native v6 and managed readiness
contracts remain unchanged. Offline inspection omits the target; selection and
preparation pass an explicit map, empty for absent/null runtime receipts.

The complete API gate passes **43 tests**, no skips/exclusions, including an
actual inert v7 archive round trip, wire-plan package number, independent
capability names, exact ABI matching, invalid metadata/receipt boundaries and
ordinary v6 compatibility. A separate subprocess using the retained SDK 0.5
snapshot refuses a registry-only v7 descriptor as `Unsupported mod runtime`.
An initial diagnostic using shared hooks stopped at the old hook-role gate;
the registry-only repeat isolates unsupported-package-ABI refusal.

The standalone consumer gate passes **101 tests**, no skips/exclusions: actual
v7 package intake, before-copy refusal, cached selection recheck after runtime
replacement and production v7 service publication/calls under Clang/GCC
ASan/UBSan. These checks qualify host admission; the independently owned
interaction engine adapter is not promoted by this schema change.


A read-only workshop audit after the GPS joint import verifies all **58** normal
library payloads and resolves the exact **55** current selections with SDK 0.6
against delivered native v1–v6 capabilities. The user state hash remains
`9498a9dcca171ff574ac73804c5e9e528ebf7e115d6f0104c0c59c6dffee57c1`;
runtime `51549df4...` and receipt `65f2801f...` remain exact. No preparation or
library/default writes occurred. Workshop loader tests pass **47**. Its interim
34-file Python/docs pin verifies and relocated SDK isolation passes; the combined
native-source pin gate detects the interaction owner's ongoing `dispatch.h`
edits and remains pending a stable reviewed source checkpoint.


The later source-inventory reconciliation inspects all **59** authoring
manifests (57 native, two companions), recording exact metadata hashes in
`artifacts/generalization-review/inventory-sdk06.json`. The central study and
project research snapshot now distinguish the original 52-mod baseline from
seven later providers/consumers. Existing local link targets pass **95** checks;
no external sources or code are acquired. This metadata reconciliation does not
transfer qualified library results to in-progress source changes.

The standalone complete **101-test** gate also passes after extending host
capability refusal and cached-selection replacement coverage to both installed
and private modes. Neither rejection path copies or deploys game files.

### Public interaction contracts and canonical runtime mirror

The checked workshop source checkpoint supplies the portable Interaction ABI 1
contract: table 32 bytes, action 40, state 32 and take(handle, actor). SDK 0.6
retains InputApiV1's 64-byte ABI 1 table and separates exclusive interaction
admission from observational input. Public docs describe borrowed actors, input
epochs, domain gates, copied names and resident callbacks.

The complete API gate passes **44 tests**, no skips/exclusions, with actual
Clang/GCC ASan/UBSan interaction arbitration, snapshot/capture/modifier/release,
rollback and capacity cases plus host/Windows AMD64 layouts. Initial strict GCC
compilation exposed misleading indentation in three statement boundaries; line
breaks fix the warnings without changing behavior. No warning suppression is
needed for these exported helpers.

The final source snapshot `artifacts/registry-sdk-0.6.0-interaction` contains
**37 files**, explicitly pinned in both loaders. The workshop expanded runtime
source pin verifies **16 headers**. Its shared-pin checks pass 2; production
proxy/interaction checks pass 3, including a real Unity hit binding fixture that
starts with zero RaycastHit size; startup-plan checks pass 10. Its new current
native adapter is host-qualified, not yet gameplay-qualified by this record.

Review caught a proposed implicit local-actor filter on every typed frame
subscriber. That changed unrelated callbacks when another mod enabled
interactions, violating the existing each-observed-walker contract. The mirror
omits that filter while preserving interaction preflight and actor-specific take.
Production regression fixtures in both loader lanes now deliver callbacks for
two distinct walkers with an input adapter active. Domain first-frame-latch
admission remains owned by Unit/Sound implementations.

The standalone complete gate passes **102 tests**, no skips/exclusions, and its
new source bundle passes strict freestanding Windows AMD64 compile/link/export
checks. Installed-game bootstrap behavior is preserved during the mirror. The
workshop receipt `artifacts/api-generalization/host-capabilities-sdk06/canonical-mirror.json`
binds the integration checks, expanded pin and intentional adjustments. Common
source holds are explicitly released. Delivered runtime `51549df4...` and receipt
`65f2801f...` remain exact; no user library/default seed promotion occurs. New
interaction engine/world behavior and domain changes require separate receipts.


### SDK 0.6.1 bounded polling and held-remap repair

The new native E-held to Q-rebind fixture rejects the previous adapter at its
still-held E interception assertion under both Clang/GCC. The adapter now keeps
captured keys in its Unity snapshot through release even when the current chord
changes. The portable core snapshots registered bindings, modifier aliases and
latched captures, including a supplied snapshot aliasing its previous down array.
The table layouts and generic frame contract are unchanged.

The complete API gate passes 44 tests; the loader's concurrently expanded complete gate
passes 113 tests, no skips/exclusions. The focused workshop pin/proxy/interaction gate
passes 5, and its additional native polling-budget fixture passes under both
sanitized compilers. The SDK 0.6.1 pin has 38 files (including the independent
native-authoring guide added by the adapter transfer); its expanded source pin
has 43 headers, and the standalone native author SDK verifies 37 headers.

A new opt-in core profiler in the loader executes production code with separate
translation units, sanitizer/count verification and independent digest parity.
Both compilers reject the wrong-owner cached-table negative control. Clean timing
runs are separate. The matched E-only core workload verifies 255 to 4 physical
polls/epoch at 3, 16 and 128 actions, with unchanged query counts. The actual native
adapter fixture reports 6 OS polls for its E/mouse/W epoch. Raw receipts and timing
limits live in the loader's existing runtime-services spec. Small cheap-array
workloads can incur extra mask construction cost; no FPS or whole-game speedup
is claimed. Win64 trap, Unity, rendering, managed/mixed and co-op costs remain
separate acceptance boundaries.

Common source holds are released and frozen 51549 remains unchanged. Exact fix
inputs and before/after logs are bound by workshop
`artifacts/api-generalization/host-capabilities-sdk06/bounded-input-fix.json`.
The old d4a628 startup/hook-ready attempts do not qualify this later candidate's
loaded-world behavior; its interaction owner is rebuilding for a separate proof.

## Framework-owned late presentation candidate

Hints 0.2 keeps its original ABI1/24 table and adds a separate presentation
ABI1/24 service, capacity32. Its provider admits late callbacks immediately
before native legend composition. Existing consumers keep their original API
requirement; explicit additional requirements survive metadata refresh. The
core registry, native startup transaction and runtime ABI are unchanged.

The source-only managed wrapper caches typed delegates, roots active callback
state until successful unsubscribe, contains callback exceptions and rejects
foreign-thread disposal. Twenty-nine focused workshop checks pass, including
actual production composition and C# reverse callbacks, forced GC and a warmed
10,000-call zero-allocation batch. The old registry and ownership restoration
checks also pass under Clang/GCC ASan/UBSan. Full canonical API gate44 and
standalone loader gate113 pass with no skipped/excluded checks. Exact logs and
candidate identities are in workshop
`artifacts/api-generalization/hints-presentation/verification.json`.

Native candidate DLL2c8df144... and managed probe88e0a816... are isolated from
the delivered library/runtime. Private preparation succeeds with exact profile
and prefix restoration, without starting a game. The first loaded attempt failed
in the original diagnostic's TMP text scanner before any callback was observed;
the scanner has been corrected and rebuilt. A subsequent shared-game-lock
refusal started no game. Both failures remain retained; neither establishes or
disproves the provider's loaded-world legend contract. World presentation,
controller/co-op behavior and game frame-time effects remain unqualified.

An offline check using the actual archived Hints0.1.3, new0.2 and original
managed consumer packages rejects 0.1.3 for its missing presentation service;
0.2 resolves in provider-before-consumer order. This checks the independently
declared service requirement, not just a package version comparison. Receipt:
workshop `artifacts/api-generalization/hints-presentation/package-compatibility.json`.

### Exact original Hints world proof

Workshop run `05381177cfc64588be5d20640943889d` passes the complete original
managed Hints scenario. Exact nativeDLL2c8df144/packagea04efed4 and managed
consumer88e0a816 use frozen native runtime370919/adapter2132c03e. There are0
callbacks at the main menu. Forced-GC subscription, rendered native label show,
disable restoration, re-enable and successful unsubscribe restoration pass.
Actual native QuitToDesktop exits0. Plugin/runtime errors are empty; source,
profile and prefix gates pass and owned launcher/display/group PIDs are absent.
All four functional screenshots were inspected. Earlier failures remain failed.

The latest workshop suite passes40 and final native-client/export checks pass8;
the independent Hints SDK verifies40 headers and3 managed sources. Exact74
producer-input bytes are sealed under the same verification index. A later CPU
source rebuild37fad0 differs after the public client header extension and is
explicitly unqualified; it does not replace the exact qualified2c8 archive.
Normal delivered51549/receipt65f280 are untouched. All-mod closures, controllers,
co-op, arbitrary managed plugins and game FPS are not qualified by this proof.

### Subsequent normal-bundle integration

The owning delivery agent promoted the separately qualified joint55 closure
using workshop `artifacts/interaction-exclusive/delivery-1794320177754536986.json`,
SHA256 `8abd2e14d2a1af5923f1f9a60b27090d87bf82e3ec86a814cb4cb27fbb16f5cb`.
It retains runtime dc89ccf9 and the exact Hints a04efed4/2c8df144 package, all55
selections and three other library entries. The current core SDK remains the
38-file snapshot bcc4c3da; the compatibility sdk/v1 subtree has its separate
28-file map. The independent Hints export remains separate from that core tree.
No native rebuild, package restamp or game preparation/launch occurred during
integration. Independent final readback is pending at this record's update.

This later coordinated delivery supersedes earlier statements about retaining
51549 as the normal default. It does not change the exact runtime370919 scope
of the original managed Hints world proof; dc89/joint55 has its separate native
qualification. Frozen candidate SDKs, source exports and receipts are unchanged.
