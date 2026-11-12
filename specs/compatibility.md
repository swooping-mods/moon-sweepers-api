# Forward compatibility and game adapter contracts

## Human input

The 2026-11-11 request treats vanilla and modded capabilities as one base for an
unchanged feature, checked dynamically against known hashes/versions, with clear
player-facing compatibility results.

## Current implementation

SDK 0.7 owns native v8's broker-only `game_adapter.h` and the pure
`compatibility.py` evaluator/admission helper. The loader owns reviewed profiles,
native implementations, hashing, integrity, evidence trust and presentation.
The SDK carries no default game hashes and never downloads or executes a mod.

V8 requires `game_access: adapter`, `game_api_abi: 1`, `runtime_api_abi: 1` and an
explicit `requires_game` map of logical ABI/minimum-size/capacity needs. Empty
direct game requirements permit framework-only consumers; selected dependencies
are still checked transitively. Supplied `game.hashes` remain extra restrictions.
Legacy native and managed packages retain pins and cannot add the new fields.
V8 forbids raw hook claims/roles and uses `MoonLab_ModStart_v8`: 24-byte context,
32-byte game broker and the unchanged 40-byte runtime table. It retains the
runtime ABI marker. No domain or module base is passed. Both game and v8-scoped
runtime lookup accept only this owner's declared ABI/prefix during startup;
callers cache typed pointers. Global legacy/managed runtime lookup is unchanged.

`MoonGameClockV1` is one typed semantic contract: 16-byte table, 32-byte sample,
game-thread frame admission, scaled Unity time/delta and zero-extended unsigned32
frame count. Declared startup lookup and later service admission are separate.
V8 consumers must not dereference legacy borrowed walker arguments.

The next source contract is `unity.time-scale` ABI 1: independent 16-byte table
and 16-byte sample (`size`, `abi`, `float time_scale`, zero `reserved`). It reads
the configured Unity timeScale already bound by Sound, including pause at zero;
it does not infer scale from clock delta or expose a setter. Sampling requires
the same admitted game-thread frame, valid caller size/ABI/reserved and a finite
nonnegative result. Failure preserves caller storage. Its table validator accepts
compatible prefixes and rejects missing callbacks. Clock ABI1 and v8 context
layouts stay unchanged. A header is not a runtime offer: the loader candidate
does not advertise this on the production profile before its deferred gates.
Sound still has raw world/audio bindings and keeps its legacy pins and independently
versioned framework tables. Managed plugins require a separate future contract.

Reviewed profile digests cover every canonical JSON field except `digest`,
including physical bindings/layouts. Profiles require all three original game
hashes. Actual runtime adapter metadata must advertise the same digest and exact
capabilities; v8 additionally requires explicit `native_package_abis` support.
Loader-supplied `legacy_profile_ids` stops matching partial pins from admitting
a legacy backend on another profile. Existing offline resolver behavior remains
when that explicit policy is absent.

Reports return allowed/status, global/per-mod coded reasons, requirement details,
dependency order and full content selection digest. `resolve` calls the same
admission helper. Existing framework ownership, optional-provider rules, cycles,
conflicts, capacities and archive integrity remain. Incompatible providers are
propagated to consumers even when a consumer has no direct vanilla needs.

Statuses distinguish unknown, incompatible and requirements-matched. Verified
status requires trusted evidence with explicit boolean success bound to all selected manifest/payload digests,
complete selection, profile digest, native runtime SHA and startup/world/co-op
scope. Author verification strings do not count. No qualification records or
real future-release compatibility claims are built into the SDK.
The loader validates scope-specific gates before constructing evidence. A
failed, absent or nonboolean result never qualifies; evidence lists over 128
rows are not accepted for verified promotion.

The [guide](../docs/compatibility.md) owns author usage; [runtime services](runtime-services.md)
owns plan encoding. Core headers/evaluator use the normal pinned SDK export.

## Verification and limits

`test_compatibility.py` packs one unchanged inert v8 archive for two synthetic
targets; checks legacy/managed pins, partial-pin provider refusal, transitive and
optional frameworks, ABI/size/capacity limits, explicit native support, malformed
provider reporting, physical binding mutation and scoped evidence invalidation.
It verifies exact legacy/v2 wire bytes and compiles/executes a standalone header
consumer. Host checks do not qualify another real game build, migrated framework,
managed forward compatibility, world/save behavior or multiplayer.

The 2026-11-12 source pass adds focused synthetic `test_time_scale_contract.py`
admission cases and extends the standalone C header consumer. The pure Python
cases can run without compilation; the C consumer, full `tools/check.py`, SDK
export, loader host/native fixtures and real engine sampling remain deferred
while the workstation is in use. Later gates must verify descriptor/output
atomicity, no engine calls on refused admission, pause/resume and profile offer
identity before enabling the candidate. No new runtime qualification is claimed.
