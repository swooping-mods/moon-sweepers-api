# Building API 0.2.0 verification — 2026-11-10

Added the public Build Menu ABI 1 declarations, kinds 193–384 (192 extra types),
stable-key/ID coordination, initial kind-193 reservation and common ABI/reuse
conventions. Existing binary ABI names/layouts and saved Power Pole identity are
preserved. New optional package metadata detects cross-provider ID conflicts and
rejects providers beyond a selected framework's declared range. Old framework
manifests default to their historical maximum 224.

`python3 tools/check.py`: **12 tests passed**, no skips/exclusions. Includes five
building cases covering public C compilation, 224/255/256/384 boundaries,
namespaces, actual package resolver conflict/capability checks, retired-ID
reservation and the old kind-193/key pair. `python3 tools/export.py` emits the
0.2.0 SDK archive and SHA256SUMS. The loader's reviewed snapshot has 18 payload
files and its corresponding 41-case host/Qt check passed.

The existing development project separately qualifies native placement/save and
a fresh reload of kinds 225, 256 and 384 alongside saved kind 193, with instance
IDs retained. Its owning report is
`moon-sweepers-modding/verification/2026-11-10-build-api-384.md`; this SDK's host
tests are not being counted as native execution. No co-op or missing-mod recovery
is qualified.

Evidence: ignored `artifacts/building-api-checks.json`, `artifacts/moon-sweepers-api-0.2.0.zip`
and `artifacts/SHA256SUMS`; current contracts in `specs/building-api.md`. This
feature change has not been pushed or published; earlier source-baseline
publication is a separate milestone. No dependencies or project license added.
