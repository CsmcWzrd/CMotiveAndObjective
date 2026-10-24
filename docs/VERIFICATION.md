# Verification — iteration 43

Twenty reconstructed checkpoints (24–43) passed sequentially. Each completed
checkpoint has a saved full-source ZIP. These are implemented-core checkpoints;
full-production promotion remains blocked. Artifact version remains 1.0.0.

Scope: 36 public classes, 227 methods,
43 maintained .HMOT headers and 299 public
ABI exports. All earlier 199 methods and typed STL classes remain. Restored
contracts are in RESTORED-APIS.md. Sources use .CMOT and headers use .HMOT.

| Check | Final result |
|---|---|
| Independent Python behavioral suite | PASS, 1,505,040 assertions, 227/227 methods |
| ASan/UBSan full suite and native fixtures | PASS; detect_leaks=0; no LSan/TSan certification |
| GCC O0/O2/O3/Os matrix | PASS, full suite and native fixtures at each level |
| Unicode native fixture | PASS, 1,112,064 scalars and 23,365,381 checks |
| Ownership/RB invariants | PASS, destructor stress and allocation-failure sweep |
| Guard pages | PASS, 3,630 hardware checks on Linux |
| CMake / installed consumer | PASS, 10 CTests and installed consumer |
| Autoconf/Automake | PASS, check/install/distcheck and installed CMotive consumers |
| Standalone headers/export audit | PASS, exact public export set and preserved baseline |
| Portable replay | PASS, all 227 methods via scalar capture and stateful models; static and real Linux shared library |
| x86/x86_64/ARM32/ARM64 compiled core | CPU-emulation PASS; ARM LE and BE included, simulated allocator, no guest OS claim |
| Linux six-target shared libraries | CROSS_BUILD_AUDIT_PASS; ELF target/exports/dependencies/hardening |
| Windows x86_64 DLL | CROSS_BUILD_AUDIT_PASS; PE exports/OS imports/ASLR/NX; native execution pending |
| macOS x86_64/ARM64 dylibs | CROSS_BUILD_AUDIT_PASS; Mach-O exports/libSystem/install name; native execution pending |
| Universal dylib | Thin slices byte-matched within fat container; native execution pending |
| Native-host kit | Linux x86_64 PASS, seven tests; Windows/macOS/ARM receipts pending |
| Custom-register assembly | PASS, 115,733 checks across six CPU modes; x86_64 native freestanding PASS |
| Release gates | Stale/incomplete reports rejected; edited ready flag cannot promote current backend |

The sole verified Linux core dependency is the OS C runtime. The Windows DLL uses
OS Kernel32/UCRT imports; macOS dylibs use libSystem. No curl/ODBC/SQLite/zlib
wrappers were added. Test-only cross tools and emulators are not library runtime
dependencies. Test allocator simulation is restricted to CPU replay images.

The pinned compiler emits C. The custom CMO-REG-1 assembly primitives have no C
wrappers, but are not integrated into class calls or the allocator. Generic
compiler templates and complete Phobos parity remain incomplete. The code is a
verified candidate for its implemented scope, not certified full production.

Source fingerprint: b5424487fc96cd061b2ac2f2351ec1b589cc788872cb45178a2a64f3259a7ec6
Tests fingerprint: 9f8503b5c5715753a0615b27c5d11616d5d6978e9b2e39d73c537a5185047ac4
Linux library SHA256: b3f59d728b4e5769d71b35e4ff694b52b1e327d406b66b5eb37e345fa7bf50d2
Sanitized library SHA256: dbdec56ec454645409a3bad724531f2dadfa7f522b7e6e618a2680840847406f
