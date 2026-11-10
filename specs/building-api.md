# Building definitions and saved identity

## Human input

The user requested expanding building kinds through 384, shared API and cross-mod
save compatibility, and reusable conventions for future mods. Missing-mod loading
was explicitly excluded from this request. An existing user decision places power
poles in the normal Build > Power menu. Retaining the MoonLab ABI during the
API/loader/index split is an implementation choice, not a recovered user quote.

## Current implementation

`include/moon_sweepers/build_menu/{build_menu,client,bootstrap}.h` owns the public
building ABI. ABI 1, callback fields, old prefix size and exported
`MoonLab_BuildMenu_v1` name are unchanged. The range is 193–384, with 192 possible
provider definitions. The native range ends at 192. Struct layout is independent
of registry capacity.

`python/moon_mod_api/build_items.py` owns range/key validation, reservation-file
validation and cross-package collision checking. `packages.validate` checks
optional `build_items`; `packages.resolve` rejects duplicate numeric kinds and
compares provider requirements to the selected framework's `build_menu_max_kind`.
Only the native `build-menu-framework` package may declare that capability.
An older framework manifest without it defaults to the historical maximum 224.
Providers must declare their framework dependency. Undeclared legacy packages
remain subject to runtime conflict checks rather than a fictitious complete
preflight guarantee.

SDK 0.3 adds an opt-in provider-neutral `build_api` selector. It names an explicit
mandatory `requires_apis` dependency; the chosen ordinary mod advertises its
`build_menu_max_kind` capacity through `provides`. All providers still share the
same persistent numeric identity space and cross-package collision check. The
old top-level capacity field and implicit framework identity remain a legacy
path. This metadata does not implement another building runtime or shared API
registry. [Interface contract](interfaces.md).

`docs/registries/buildings.json` is the coordination registry. Kind 193 and
`manual-power-poles.power-pole` remain assigned to Manual Power Poles. Retired
IDs and keys stay occupied. Numeric kinds are persistent identities, never
load-order indexes. Namespaced definition keys are separate from instance IDs
and display categories. New keys follow `modid.category.item`; existing shorter
namespaced keys remain valid.

The runtime implementation remains in the owning development project's Build
Menu Framework 0.2.0. It extends actual native definition/catalog arrays and the
in-memory native reader maximum, keeping ordinary saved records and all existing
IDs. This repository distributes declarations and tools, not the runtime DLL.
The development checkout consumes checked first-party copies through
`tools/sync_build_api.py`; the standalone loader uses its full pinned SDK snapshot.

## Verification and limits

`tests/test_build_items.py` compiles a public consumer, checks IDs around 224/255
and 384, invalid namespaces, duplicate reservations (including retired entries),
the existing Power Pole identity, the actual package resolver and old-framework
rejection. Run the required `python3 tools/check.py` and `python3 tools/export.py`.
These host checks do not qualify native world behavior or co-op. The runtime
owner records game/save evidence separately.

## AI Inferred

The central immutable reservation file, permanent category namespace segments,
explicit capability metadata and snapshot workflow implement the requested
coordination. They do not introduce a sidecar format, automatic save migration,
new multiplayer handshake or missing-mod recovery.
