# Reusable mod-platform research snapshot

Source: central [Moon Sweepers study](../../research/studies/moon-sweepers-mod-platform-2026-11-10/_readme.md),
snapshot 2026-11-10. Origin: the user's API/loader/generalization question, the
`swooping-mods/moon-sweepers-api` and loader repositories, and the existing
`moon-sweepers-modding` workshop. Receiving project: Moon Sweepers API. The central
study owns queries and comparisons; this copy retains the relevant local
findings. No upstream source code is copied.

## Observed baseline before generalization

The workshop has 52 mod manifests: 50 native and two companion tools. These
include seven established framework/runtime providers plus the new, untracked
Pickup Hands provider. Their ordinary dependency declarations already connect
equipment, shop, hints, vehicles, building, sound, moving units and physical toys.
Full inventory and source links: [central inventory](../../research/studies/moon-sweepers-mod-platform-2026-11-10/inventory.md).

The public SDK accepts native packages and companion tools. The workshop also
accepts BepInEx IL2CPP packages. Synthetic unrelated manifests confirm that the
public SDK rejects the managed kind accepted by the workshop. This is a real
contract gap, independent of the friend's plugin identity.

The shared native hook ABI covers only Update, LateUpdate and vehicle
FixedUpdate. Its phases all precede the original function. Mars needs real
prefix/postfix and session/save/world hooks. BepInEx support already has separate
game profiles, layout projection, binding repairs and optional compatibility
plugins in the workshop. Those are reusable foundations, not proof of arbitrary
plugin compatibility.

Current building validation explicitly recognizes `build-menu-framework` and
its capacity metadata. Other framework clients repeat fixed private dependency
path lookup and startup. General discovery and semantic event/lifetime contracts
are the useful extension points to develop.

## External precedents

- [Fabric](https://docs.fabricmc.net/develop/loader/) separates loading from
  game-specific APIs and allows framework APIs to use normal mod mechanisms.
- [SMAPI](https://stardewvalleywiki.com/Modding:Modder_Guide/APIs/Integrations)
  exposes mod-provided APIs through a registry.
- [BepInEx](https://docs.bepinex.dev/master/api/index.html) separates common and
  backend-specific support; [SKSE](https://github.com/ianpatt/skse64/blob/master/skse64/PluginAPI.h)
  demonstrates versioned native interface discovery.

## Recommendation and evidence limits

Keep API contracts/tools in this repository; separate headless runtime and
game/managed adapters within the loader project; keep independently versioned
framework SDKs and implementations with their ordinary mod packages. Details
and migration acceptance are in [the proposed design](../design/mod-platform.md).
This recommendation is AI inference, not a completed refactor.

Public API checks: 12 passed. Manifest/source inspection and synthetic validation
are recorded in ignored `artifacts/generalization-review/inspection.json` and
`artifacts/checks.json`. Earlier Mars solo/reload evidence was read, not rerun.
No game, external plugin or performance benchmark ran for this study. Existing
ABI layouts, packages, saves and local selections were not changed.


## Current implementation reference

The observations and 12-test count above describe the original study baseline,
before the implemented generalization. Current SDK 0.5 contracts, optional
managed consumer readiness and their bounded verification are indexed by
[specs](../specs/_readme.md) and the existing
[verification record](../verification/local-preparation.md). The historical
inventory and study evidence are retained rather than relabeled as current
qualification. The original external precedents inform the component split;
they do not qualify this implementation's game behavior.
