# Interaction contracts and adapter ownership

## Human input

The generalization goal requires reusable contracts and independently owned
frameworks. Related input work requires explicit exclusive interactions without
changing ordinary input tables or unrelated mods' callback delivery.

## Current implementation

SDK 0.6 supplies `interaction.h` and `interaction_registry.h`. The AMD64 C11
layouts are table 32 bytes, action descriptor 40 and cached state 32. ABI 1 adds
registration, repeatable sampling and `take(handle, actor)`; InputApiV1 remains
ABI 1 and 64 bytes. Registration names begin with the owning package ID and a
dot in the loader adapter, occur within ModStart and seal before gameplay.
Callback code/context are resident; names/bindings are copied.

The portable registry holds 128 interactions over the shared 512-action input
registry. It selects eligible actions using active input, priority, distance and
stable action name. Each supplied input epoch uses a coherent physical snapshot;
an optional pressed snapshot preserves short taps. Successful exclusive presses
latch the physical base key through its release epoch, including modifier-key
aliases. Gated delivery still tracks physical edges. Polling/sampling alone
does not consume the selected edge; take succeeds once per epoch.

The loader owns thread/local-actor validation, coherent engine input epochs,
device identity and native interception. Domain mods own eligibility, focus,
world, authority, reach/occlusion and action effects. The portable registry's
implementation structures are source helpers, not binary ABI tables. The
input host defaults to observational delivery; adapters opt into pre-sample
and admission macros while raw edge tracking remains separate.

Native consumers declare package v7, runtime API ABI 1 and
`requires_host: {"interaction": 1}`. Target selection and preparation must pass
actual host capabilities; absence rejects before deployment. The table getter
is `MoonLab_GetInteractionApi_v1`; callers also validate ABI, exact size and
nonnull pointers. The consumer marker is `MoonLab_InteractionApiAbi` returning 1.
There is no private fallback registry for native interception. The
[author guide](../docs/interaction.md) describes lifetime and admission.

The existing generic frame subscription still describes each observed Update
walker. Local input admission and domain frame latches must preserve that
independent contract; registering an interaction does not grant permission to
change unrelated subscribers' delivery.

## Verification and limits

The API gate passes 44 tests with no skips/exclusions. The public production
registry fixture runs under Clang/GCC ASan/UBSan without suppressing warnings,
covering overlap, independent keys, deterministic ordering, modifier aliases,
held/release capture, coherent snapshots, gating, rebinding, rollback and
capacity. Public layouts compile for host and Windows AMD64. Initial GCC
misleading-indentation errors in three statement boundaries were corrected
without changing behavior.

The engine adapter and domain consumers have separate production fixtures and
game qualification. Portable checks do not prove loaded-world input, native
interception, raycasts, save/reload, co-op or frame time. Runtime source pins
are resealed only after coherent adapter integration and its focused checks.

## AI Inferred

A separate interaction contract permits explicit consumption while retaining
the existing observational input table. Domain ownership and a loader adapter
avoid requiring each feature to patch the same native readers independently.
