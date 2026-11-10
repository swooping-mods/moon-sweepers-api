# Moon Sweepers API specs

Current implementation and contracts for `swooping-mods/moon-sweepers-api`.

Proposed generalization is tracked in [the design map](../design/_readme.md);
it does not extend the implemented contracts listed below.

| Spec | Owning source | Read when |
|---|---|---|
| [Interaction adapter](interaction.md) | `include/moon_sweepers/{interaction,interaction_registry,input_host}.h` | Changing exclusive interaction arbitration, physical capture, actor admission or adapter boundaries |
| [Mod-provided interface contracts](interfaces.md) | `python/moon_mod_api/{interfaces,runtimes,packages}.py` | Changing backend support, framework discovery metadata, optional API dependencies or provider capabilities |
| [Native runtime services](runtime-services.md) | `include/moon_sweepers/{services,input,camera}*.h`, `python/moon_mod_api/runtime_plan.py` | Changing publication, typed frames, shared input/camera helpers or the native startup plan |
| [API and package boundaries](contracts.md) | `include/`, `python/`, `tools/check.py`, `tools/export.py` | Changing ABI, package rules, author tools, SDK snapshots or CI |
| [Building definitions and saved identity](building-api.md) | `include/moon_sweepers/build_menu/`, `python/moon_mod_api/build_items.py`, `docs/registries/buildings.json` | Adding buildable items, reserving IDs or changing cross-mod save contracts |

The usage guides are under `docs/`. Rollout choices belong outside specs.
