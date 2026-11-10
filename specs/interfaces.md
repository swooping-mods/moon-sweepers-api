# Mod-provided interface package contracts

## Human input

The 2026-11-10 generalization request requires independently owned frameworks as
ordinary mods, supporting the user's mods, Mars and other authors. See the
[design](../design/mod-platform.md) for the wider objective.

## Current implementation

`python/moon_mod_api/interfaces.py` validates optional `provides` and
`requires_apis` metadata. Interfaces have owner-qualified stable keys, explicit
ABI, table byte sizes and bounded integer capacities. Mandatory requirements
also need an ordinary package dependency. Optional requirements do not select
providers; when selected, providers must satisfy the API and precede the
consumer. The package resolver detects API dependency cycles, incompatible
ABI/size/limits and foreign API namespaces without recognizing framework IDs.
The owner prefix uses the ordinary package key grammar, including digit-leading
identities; service suffix segments retain their letter-leading grammar.

Native packages v6/v7 with `runtime_api_abi: 1` marks a package requiring the shared runtime interface
protocol. SDK 0.6 supplies the C publication/lookup/frame contracts and native
startup plan; the standalone loader implements them. Metadata alone never
publishes a table: [runtime services](runtime-services.md) requires actual
publication to match the deployed declarations before provider startup commits.
Consumers reject unsupported runtime requirements before deployment. SDK 0.5
also permits the reviewed managed backend to declare native API requirements
with `runtime_api_abi: 1`; managed packages cannot publish native tables. A target
must advertise native readiness ABI 1 before deploying this opt-in consumer.
The source-only C# `RuntimeClient` checks the resident loader/table exports,
waits without blocking for Ready and performs cached native lookup. It does not
order arbitrary BepInEx Load methods or register managed callbacks during native
startup. Domain wrappers remain owned and versioned by each framework. Native v1–v5 packages
also cannot opt into that metadata: requiring v6 makes old loaders reject it.
Native v7 additionally requires a nonempty `requires_host` capability map.

`runtimes.host_requirements` validates native v7 host adapter requirements:
up to 32 names matching `[a-z][a-z0-9_]{0,63}` with exact positive uint32 ABIs.
`resolve` and `require_available` accept `host_capabilities`; `None` means offline
inspection, while a target supplies a map (empty when absent/null). Missing or
incompatible adapters reject before deployment. A target repeats this check at
preparation to catch runtime replacement after selection. Package v7 deliberately
makes older validators refuse these mandatory requirements; existing v6 package
admission and C service ABI 1 are unchanged. Framework publication remains
owner-qualified through `requires_apis`, separate from host adapters.

`build_items.py` accepts an explicit `build_api` referencing a mandatory API
requirement. The selected provider advertises `build_menu_max_kind` within
193–384. Existing saved numeric kinds/keys and global collision checks remain.
Legacy manifests retain their original `build-menu-framework` dependency and
historical 224 fallback; this compatibility rule does not privilege new providers.
See [building identity](building-api.md) and the [author guide](../docs/interfaces.md).

`runtimes.py` accepts the reviewed managed backend without a particular plugin
GUID or author. Identity/data namespace collisions are checked case-insensitively
and native hook-role markers remain unavailable to managed plugins. Native and
managed exclusive hook conflicts use one resolver. Companion tools remain
separate. Optional external provenance is validated but never fetched.

## Verification and limits

`tests/test_interfaces.py` exercises independent providers/consumers, optional
selection and cycles, ABI/prefix/capacity refusal, alternative building API
ownership and collisions across different building providers.
`tests/test_runtimes.py` exercises an unrelated managed archive through actual
pack/examine/install/readback, mixed dependency/hook checks, unavailable backends,
namespace collisions and provenance refusal. Payloads are synthetic inert bytes.
Run `python3 tools/check.py` and `python3 tools/export.py`.

SDK 0.4 adds runtime, input and camera C contracts while preserving the existing
hook layouts and game-save format. Loader tests execute independent public-SDK
provider/consumer calls with the production C registry and startup-plan parser.
These host checks do not establish native Windows game/world/co-op behavior or
improved performance. The workshop's native framework migration and independent
SDK export have their own checks; this SDK gate does not substitute for them.
The optional compiled managed fixture exercises actual C# to C lookup and typed
calls, readiness/ABI refusal, identity bounds and GC lifetime. It requires an
already installed compiler/runtime and explicitly skips without one. Actual
managed framework presentation/game-thread admission remains separate
qualification; a successful FFI call alone does not establish those gates.

## AI Inferred

Owner-qualified interfaces keep provider selection explicit and avoid loader
special cases. Capacity comparisons express caller needs while runtime checks
must still validate the actual published table. The existing conservative
cross-backend exclusive-hook rule is retained until composition is demonstrated.
