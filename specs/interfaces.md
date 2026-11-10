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

Native package v6 with `runtime_api_abi: 1` marks a package requiring the shared runtime interface
protocol. SDK 0.4 supplies the C publication/lookup/frame contracts and native
startup plan; the standalone loader implements them. Metadata alone never
publishes a table: [runtime services](runtime-services.md) requires actual
publication to match the deployed declarations before provider startup commits.
Consumers reject unsupported runtime requirements before deployment. Managed
host sequencing and cross-language wrappers still need their own implementation
and qualification. The reviewed managed backend remains available for ordinary
plugins; it cannot yet declare native interface metadata. Native v1–v5 packages
also cannot opt into that metadata: requiring v6 makes old loaders reject it.

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
improved performance. Framework migration and managed bridging remain unfinished.

## AI Inferred

Owner-qualified interfaces keep provider selection explicit and avoid loader
special cases. Capacity comparisons express caller needs while runtime checks
must still validate the actual published table. The existing conservative
cross-backend exclusive-hook rule is retained until composition is demonstrated.
