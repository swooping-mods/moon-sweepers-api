# Reusable Moon Sweepers mod platform

## Human input

2026-11-10 request, summarized: generalize the foundation for the user's mods,
the friend's MarsSweepers and other authors; keep each mod independent and
frameworks as ordinary mods between game integration and content. Assess a
conventional API/loader split and efficient adapter-based implementation.

Status: SDK 0.4 implements shared native/managed package validation,
provider-neutral interface metadata, public runtime/input/camera contracts and
a deterministic native startup plan. The standalone loader implements the
registry and platform adapters. Workshop/framework migration, managed bridges,
gameplay and performance qualification remain active work below.
Current behavior is recorded in [contracts](../specs/contracts.md),
[interface contracts](../specs/interfaces.md) and
[building identity](../specs/building-api.md).

## Evidence and rationale

The [research snapshot](../research/mod-platform.md) links the central study,
52-mod inventory, checked source revisions and conventional precedents. The
initial SDK 0.2 was native/companion only; SDK 0.3 now owns shared managed package
rules consumed by both loader checkouts. The workshop retains more advanced
adapter hosting. Frameworks already have separate
versioned native exports. Public building rules currently know a specific
framework identity. Repeated framework connectors perform private DLL lookup
and idempotent startup. The current native hook API is intentionally three
specific pre-original hooks, not a general managed patch interface.

## AI Inferred

### Ownership and repository split

Keep the two existing main repositories. Establish component boundaries before
adding repositories. A separate runtime binary can be distributed with the
desktop application while remaining usable without its GUI.

| Component | Owns | Source home |
|---|---|---|
| Core SDK | Public runtime ABI, shared package contracts/validators, author tooling, examples and compatibility conventions | `moon-sweepers-api` |
| Desktop manager / CLI | Library selection, dependencies, private deployment, profiles, launch and diagnostics UI | `moon-sweepers-mod-loader/loader/` |
| Headless runtime | Module startup, owner identity, API publication/lookup, lifecycle, logging and common hook coordination | A distinct component in `moon-sweepers-mod-loader/runtime/` |
| Game adapter | Qualified game identities, IL2CPP/native bindings, semantic hook signatures, object/session validity and current-build repairs | Distinct loader runtime component; explicit game profile |
| Managed host adapter | Optional BepInEx/interop hosting, generated bindings and explicit bridge wrappers | Distinct optional loader runtime component |
| Framework mod | Domain implementation, provider registry, domain hooks, own public SDK, assets and independent version | Each owning mod package/source project |
| Feature mod | Gameplay, definitions, transactions, save state and optional integration | Each owning mod package/source project |
| External compatibility mod | Exact-version repairs for an externally supplied plugin | Separate package/companion beside that plugin |

Shop, Equipment, Hints, Build Menu, Vehicles, Sound, Units and Pickup Hands keep
separate package identities. A feature requires only the services it uses.
Another author's provider follows the same contracts and ownership checks.
Framework APIs can be discoverable in a shared documentation index without
moving every domain contract into the core SDK. Preserve existing public
building-header paths as compatibility exports if ownership is reorganized.

The workshop remains an authoring/test project. Consolidate production runtime
changes into one canonical source and make the workshop consume explicit pins
or build that source. Do not maintain two independently edited production
validators or dispatcher copies. A third runtime repository becomes useful only
when independent release cadence or other launcher consumers justify it.

### Small shared contract

The first general surface should cover mod identity, logging, paths/config,
runtime capabilities, required/optional dependencies, API publication/lookup,
startup phases and explicit world/session lifetime. Add individual services only
when their actual caller contracts are understood.

API lookup is qualified by owner, API name, ABI and required structure size or
supported prefix. The runtime validates ownership and compatibility; it does
not recognize a list of blessed framework IDs. Stable names are resolved once
and consumers cache typed tables. Matching capability names alone never permit
substituting a provider with incompatible semantics.

Use dependency-ordered ModStart scopes: check required committed APIs, bind
providers, publish the current mod's tables and register callbacks, then commit
only after successful startup and exact declaration matching. Activate game
hooks after all mods start. This implementation replaces the initial proposed
global publish-all/bind-all phases: existing exports expect dependencies to be
usable inside ModStart, so per-mod commit preserves that behavior. Attribute
every registration to its owner, roll back APIs/frames/hooks together on failure
and reject unresolved required APIs before play.
Keep modules and callbacks resident through process exit initially. World
teardown resets transient game state without invalidating resident API tables.
Existing ModStart/export behavior needs an explicit compatibility path; do not
reinterpret ABI 1 structures or silently change startup semantics.

Replace per-client dependency DLL lookup/startup with generic runtime lookup for
new consumers. A legacy/standalone shim can preserve existing private modkit
deployment while that path is migrated.

### Native and managed authors

Native mods retain the existing C ABI and typed callbacks. C# authors retain
normal BepInEx plugins and generated game bindings. Supply optional ergonomic
managed wrappers for shared services; bridge a framework deliberately when a
managed mod needs it. BepInEx hosting alone does not expose native framework APIs.

Each bridge defines fixed-width values, string/buffer ownership, GC/delegate
roots, main-thread requirements, error handling and session lifetime. Bind once;
avoid per-frame reflection, service-name lookup or JSON conversion across the
language boundary. Do not make native mods pay for an unused managed host.

The existing managed adapter remains one source implementation in the workshop's
`runtime/bepinex/`. Its checked builder can attach an explicit receipt plus
runtime files; a desktop integration should consume that provider rather than
copy or reimplement its C# generator/layout/repair code. Retain its complete
screened input hashes, notices/source archives and disabled-download settings.
The qualified profile is Moon Sweepers Steam 1.0.5 / Unity 6000.6 / IL2CPP 108;
other profiles and the pinned development runtime need separate qualification.
The standalone loader currently refuses managed hosting explicitly.

Current mixed package dependency ordering establishes selection closure, not a
cross-backend startup rendezvous. Native ModStart and upstream BepInEx plugin
startup are independently bootstrapped; package dependencies are not translated
into BepInDependency attributes. Cross-backend startup/service dependencies need
an explicit readiness protocol and mixed lifecycle qualification before they
can be advertised. The native registry and existing metadata-only mixed graph
checks do not provide that protocol.

Mars remains an independent external mod, with its original DLL, namespace,
gameplay, data and optional exact-version compatibility companion. It requires
Shop/Sound/etc. only when its author chooses an integration. New authors get the
same package/runtime route without another loader special case. Existing Mars
save and multiplayer protocols are not automatically replaced by shared ones.

### Hooks, persistence and performance

Offer useful semantic events and typed functions above machine contexts. Keep
game-build tokens/offsets and binding repairs with the adapter. Preserve a
documented lower-level extension path for unusual mods. Extend hook roles only
with inspected signatures, mutation/cancellation semantics and focused tests.
The existing “Late” phase remains pre-original; real postfix is a separate
contract. Harmony ordering does not establish cross-engine native/Harmony
composition. Reject unknown destructive overlap until a shared chain is proven.

Frameworks multiplex their own providers behind common hook subscriptions.
Resolve metadata and API tables at startup; publish bounded callback arrays;
make repeated reflection, unnecessary allocation and redundant world scans
measured optimization targets. Keep existing C runtime code where it serves the
contract; use C++ for a bottleneck only when measurement warrants it. C# remains
a viable authoring route. No language switch is inherently a performance win.

Preserve stable namespaced definition keys and explicit saved numeric identities,
including the implemented 193–384 building range. Transient API handles and
load-order positions are never save IDs. General capability validation must
retain domain collision checks rather than weaken them. Mode/save namespace
selection is explicit; vanilla and Mars worlds keep their respective namespaces,
and Steam/Bottles profiles remain separate. Shared persistence/network helpers
are opt-in contracts, not an automatic world format or multiplayer migration.

### Migration and acceptance intent

| Stage | Concrete result | Required evidence |
|---|---|---|
| Package convergence | One native/managed/companion contract, one validator owner, explicit runtime availability checks | Unknown runtime rejection before deployment, old package acceptance and generic third-party managed fixture |
| Generic discovery | Owner-scoped provider registry and explicit publish/bind lifecycle with compatibility shims | Independent provider/consumer, wrong ABI/size, missing provider, duplicate owner, rollback and dependency-order checks |
| Separate framework SDKs | Explicit versioned SDK bundles with independently packaged implementations | Public consumer builds without sibling source includes; old binary and saved-ID behavior retained |
| Game/managed adapters | One qualified binding owner, optional managed host and first typed framework bridge | Synthetic native/managed calls, GC/lifetime/thread checks and verified hook refusal/composition |
| End-to-end reuse | Representative equipment, building, vehicle, unit/sound and independent managed paths | Private startup, loaded world, teardown/reentry, save/restart and actual co-op for affected behavior |
| Measured performance | Comparable unmodded, native-only, managed-only and mixed workload results | Startup time, frame-time distribution, allocations and callback/bridge/query costs with matched builds and saved scenarios |

New tests must exercise behavior rather than merely search source for a desired
name. No “full generalization” claim until an independent provider and consumer
work without core special cases. Current public API checks passing establishes
the old baseline, not these proposed stages.

## Open questions

- Separate framework packages/SDKs are required by the objective; one repository
  per framework is a release/ownership choice, not a technical prerequisite.
- Choose the first managed framework consumer from an actual use case; loading
  unchanged Mars does not itself require rewriting it to use every framework.
- Determine the shared event/input/UI-allocation and native/managed patch
  composition scope from concrete consumers. A universal detour engine, hot
  unload and arbitrary-game support are not assumed by this proposal.
