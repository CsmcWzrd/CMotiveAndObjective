# Verification — iteration 23 — 24 October 2026

Twenty continuation checkpoints (4–23) have been completed. The implemented core
is a verified candidate, **not a full-production/GA release**. Production promotion
is explicitly refused while PRODUCTION-READINESS.json lists outstanding blockers.
Version 1.0.0 remains the requested output filename/version.

## Current scope

27 public classes, 199 methods and 32 .HMOT headers (five internal helpers).
All 149 original methods and all original STL functionality remain. Four additional
typed containers provide HashMapI64, HashSetI64, MultiMapI64 and StackI64. New
algorithms include caller-workspace merge sort, checked sum, UTF-16 LE/BE,
UTF-8/scalar transcoding and strict I64/U64 text conversion in bases 2..36.
API-EXTENSIONS.md specifies capacities, error atomicity, lifetimes and complexity.
All maintained library algorithms use CMotive, with no third-party library wrapper.

The Linux ELF uses the pinned minimal C-emission compiler profile and system
calloc/free plus compiler/optimizer OS-runtime helpers. Its sole DT_NEEDED is
libc.so.6. External curl, ODBC, SQLite and zlib wrappers are excluded. The original
upstream/compiler ZIPs are provenance inputs, not linked library implementations.

## Executed checks

| Check | Result |
|---|---|
| Full behavioral suite | PASS: 1,417,340 assertions, 199/199 methods |
| Same full suite with ASan/UBSan | PASS; detect_leaks=0, halt_on_error=1 |
| Exhaustive UTF-8 and UTF-16 LE/BE | PASS: 1,112,064 scalars, 23,365,381 native checks |
| Independent Unicode oracle | PASS: aggregate byte hashes match Python codecs |
| Gregorian cycle | PASS: 146,097 dates checked against Python datetime |
| Native hardware guard pages | PASS: 3,630 checks; source/output bounds and full hash tables |
| Owning containers | PASS: 52,000 RB invariant operations, destructor stress, 100 nth-allocation cut points, tracked allocations return to zero |
| Adversarial hashing | PASS: discovered collisions, tombstones, full tables and duplicate updates |
| Concurrency | PASS: 12 independent container workers, 100,872 checks; plus original stateless stress |
| Malformed codecs | PASS: 12,500 inputs, five seeds, independent strict oracles and failure output preservation |
| GCC optimization matrix | PASS: O0, O2, O3, Os; complete behavior and native fixtures per configuration |
| Strict warnings | PASS: implicit declarations, incompatible pointers and return types are errors |
| GNU Make / CMotive consumer | PASS, including all new classes |
| Fresh CMake / CTest | PASS: all 10 tests |
| Installed CMake package consumer | PASS |
| Autoconf/Automake check/install/distcheck | PASS |
| Installed CMotive consumers | PASS: CMake and Autotools installations; all headers byte-matched |
| Standalone headers / ABI | PASS: 32 headers, exact 253 exported API symbols |
| Linux dependency and ELF audit | PASS: target, SONAME, imports, exports, RELRO, NOW, non-executable stack, no writable executable segments or runtime search paths |
| Negative release fixtures | PASS: 15 profile/ELF rejection cases and eight invalid/stale behavioral reports |
| Production promotion guard | PASS: refuses GA promotion because blockers remain |

The normal suite uses independent Python arithmetic/codecs/container models.
Method-call coverage is measured; branch coverage and a complete security audit
are not claimed. Output spans must actually exist for their declared lengths.
Mutable shared containers require caller synchronization. Hashing is not designed
as collision-attack resistance; fixed capacities and worst-case costs are documented.

The normal and sanitized binary hashes are:

- Normal: 4addd06360b0e19411496fa5f90234b8cef7d3041ba7483a51b5dad631f80702
- ASan/UBSan: f96bfaa2e9f461203bd991d7e29b998efff5aa113eccb3f1fed01d975cf41e90

## Assembly layer

The nine unchanged CMO-REG-1 primitives have no C ABI wrappers or libc imports.
All six ELF CPU/endian modes pass 115,733 emulated checks: x86 LE, x86_64 LE,
ARM32 LE/BE8 and ARM64 LE/BE. The x86_64 freestanding assembly caller passes
natively; native ELF32 execution is unsupported by this host. ARM execution is
emulated, not physical-hardware qualification. x86 has no big-endian execution
mode; explicit BE data loads/stores are supported. COFF/Mach-O assembly adaptations
and direct compiler integration remain unfinished. These checks were rerun for
this final checkpoint; the packager also validates exact source/artifact hashes.

## Production limitations

The current frontend is a C-emission backend, with no arbitrary template
instantiation or direct CMO-REG-1 class-call integration. Full Phobos parity and
OS-service APIs are incomplete. Full Windows/macOS/ARM core execution remains
unverified; no DLL/dylib or ARM core production binary is fabricated. LSan cannot
inspect processes here, and no ThreadSanitizer pass is claimed. Tracked allocation
and concurrent tests support the tested paths, not global leak/race freedom.

Every checkpoint includes its full source/binary ZIP, test log and SHA-256 in the
continuation history. Final ZIP/TAR packaging is deterministic and the exact
release binary must match current source/test fingerprints and measured coverage.
All 174 supplied upstream file hashes and compiler/source pins remain verified.
