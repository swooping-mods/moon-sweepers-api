# Native runtime services and startup plan

## Human input

The generalization request requires ordinary, separately owned framework mods
usable by independent authors. Public contracts belong to this SDK; the loader
owns executable hosting and platform/game adapters.

## Current implementation

SDK 0.4 adds `services.h` (`runtime.h` is a forwarding include). The AMD64 C11
layout is frozen as follows: publication base 32 bytes, capacity extension 48,
limit entry 16, frame subscription 32, runtime function table 40. The runtime
export is `MoonLab_GetRuntimeApi_v1`; v6 providers/consumers export
`MoonLab_RuntimeServicesAbi` returning 1. Existing hook structures/exports stay
compatible. Domain tables remain opaque pointers with independently owned ABI.
`services_client.h` supplies the Win32 connection and marker definition in one
owning bootstrap translation unit. It never loads or starts a dependency. The
public Build Menu client uses it under a recognized loader and fails closed
when a service is unavailable; only the standalone modkit uses legacy startup.

Publication is scoped to the native mod currently executing ModStart on the
bootstrap thread. The provider ID is assigned by the loader. Service suffixes
combine with that ID to form the manifest API key. Descriptor size is exactly
32 or 48; the extension has reserved zero and at most 32 named integer limits.
Actual API ABI, table byte size and capacities must exactly match declarations.
Names/limits/descriptors are borrowed only for the call and inspected
synchronously; API storage and code remain resident through process exit.

Startup follows dependency order. Each mod binds already committed providers,
publishes its own tables and registers callbacks inside its ModStart scope.
Required APIs are checked before ModStart. Successful return commits only if
every advertised table was published. Failure removes that owner's APIs,
typed frames and low-level hook subscriptions together. Hooks are activated
after all mods start. There is no global publish-all/bind-all phase or hot unload.
This preserves existing dependency-ordered ModStart behavior.

Lookup uses provider ID, service suffix, exact ABI and minimum table prefix.
Uncommitted providers are invisible. Lookup is bootstrap-thread-only during
startup and read-only from other threads after sealing; a table's own functions
define stricter thread and lifetime rules. Consumers should cache typed tables.
Typed frame observers share the existing Update registry, phase/priority/stable
registration ordering and rollback. Each callback receives a borrowed walker
for that Update invocation; it is not a once-per-render-frame world event.
No allocation or name lookup is added to callback dispatch.

`input.h` owns local action ABI 1 (registration, sample, describe, rebind,
configure, cooperative channel claim and raw-key query). `input_registry.h` and
`input_host.h` provide the portable bounded implementation: 512 actions, 32
claims, host-supplied key polling. Access is serialized on the game thread;
callers provide focus/typing/menu/world/authority gates. Actions never suppress
vanilla input. Platform polling remains in the loader.
Default registration preserves the first observed press. A changed override
inhibits an already-held new chord until release; an invalid initial override
retains the valid default binding and display label.

`camera.h` owns camera ABI 1 and begin/finish helpers. Its portable registry has
16 exclusive resource claims. The loader observes the game dispatch thread and
rejects claims before that observation or from another thread. Providers root
targets and retain snapshots, restore while the claim is held, then release.
Failed restoration retains the claim for retry. There is no implicit expiry on
world change. Camera game-state capture/restoration remains provider-owned.

### Native startup plan

`runtime_plan.encode` emits `MoonLab/runtime-plan.bin` from a validated selected
dependency order. It rejects duplicates/reversed dependencies, filters managed
entries, omits absent optional requirements, sorts API/limit names and limits
the output to 2 MiB. The loader deploys it through the same ownership/integrity
journal as the DLLs. The C parser validates all bytes before loading a mod and
checks the actual startup list and v6 DLL marker. The plan describes contracts;
it contains no executable addresses and cannot establish implementation safety.

Wire format v1 is little endian: eight-byte magic `MSAPI\x01\0\0`, uint32
native-mod count, then each mod's length-prefixed ID, uint32 package ABI number,
uint32 provided count, provided contracts, uint32 required count and required
contracts. Strings use uint16 byte lengths and ASCII, with no terminator.
Each contract contains full API key, uint32 ABI, uint32 size/minimum size,
uint32 limit count, then pairs of limit name and uint32 value. Existing package
bounds apply (64 mods, 64 APIs per mod, 256 provided APIs total, 32 limits per
contract, 65536-byte tables). Required providers must precede consumers.
Duplicate keys, incompatible requirements, invalid grammar, truncation and
trailing bytes reject. The bootstrap retains the single plan buffer for the
process lifetime; publication does not retain callers' descriptor storage.

## Verification and limits

SDK tests compile public tables for host and Windows AMD64 without loader
typedefs, and check deterministic/mixed/optional startup plans. Loader tests
compile separate provider and consumer translation units against public SDK
headers and their own domain header, then execute calls through the production
C registry under Clang/GCC ASan and UBSan. They cover wrong ABI/size/capacity,
missing/duplicate/unadvertised tables, thread boundaries, prefix lookup,
rollback, 256-API/32-limit bounds and every truncated prefix of a valid plan.
Private deployment tests cover actual v6 archives and preservation of unknown
edits to the deployed plan.
The public building-client host fixture checks both loader refusal without
private startup and legacy fallback under Clang/GCC ASan/UBSan.
The shared production input harness also runs against the exported headers
under both sanitized compilers, covering initial presses/labels, overrides,
focus/forbidden-modifier gates, rebind edges and all action/claim capacity bounds.

The standalone loader implements this protocol and exports input/camera tables;
the workshop migration is coordinated separately. Host tests and cross-builds
do not qualify a loaded game, save/reload, co-op, a managed bridge or performance.
Individual framework SDK packaging/migration remains independent work.

## AI Inferred

Synchronous declaration matching plus dependency-ordered commit allows consumers
to bind only successful providers while preserving legacy initialization order.
The registry stores opaque typed tables, avoiding per-call serialization,
reflection or language coupling. These structural choices are not measured
speedup claims.
