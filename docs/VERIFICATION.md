# Verification — iteration 3 — 24 October 2026

This report distinguishes the selected standalone assembly-runtime scope from the
CMotive core's existing compiler backend. Neither result certifies complete Phobos
parity or a fully native, production-ready compiler/library.

## Custom-register assembly runtime

Nine routines implement byte copy, overlap-safe move, fill, unsigned comparison,
bounded string length, and LE/BE U32 loads/stores. CMO-REG-1 is a custom register
convention. No C wrapper, libc import, C startup or C compiler language is used.
The assembly CMake project declares LANGUAGES NONE. Zig 0.17.0 is used solely as
assembler/linker/archive driver; sources passed to it are .s files.

| Target | Assemble/link | CPU-emulated execution | Native execution |
|---|---|---|---|
| x86 LE (i386+) | PASS | PASS | NOT RUN: host rejects ELF32 execution |
| x86_64 LE | PASS | PASS | PASS: freestanding Linux assembly caller |
| ARM32 LE (ARMv7-A) | PASS | PASS | NOT RUN: no physical ARM host |
| ARM32 BE8 | PASS | PASS | NOT RUN: no physical ARM host |
| ARM64 LE | PASS | PASS | NOT RUN: no physical ARM host |
| ARM64 BE | PASS | PASS | NOT RUN: no physical ARM host |

CPU emulation: **115,733 assertions across six targets**, Unicorn 2.1.4.
Tests check register preservation, stack balance, return addresses, zero-length
null-pointer operations, memory sentinels, page-edge spans, overlapping moves,
unsigned ordering, explicit endian accesses and native data-endian mode. ELF
machine/class/endian flags, absence of dynamic sections and absence of unresolved
symbols are checked. ARM32 uses BE8, not BE32 instruction decoding. A separate
A64 word-load probe verifies BE data state while instruction bytes remain LE.

x86 has no native big-endian CPU mode. Both BE and LE data formats are supported
there through explicit load/store routines. The sources/static archives currently
use ELF; Windows COFF and macOS Mach-O adaptations remain unverified/unimplemented.
The native x86_64 test exercises all nine routines, entered from assembly _start
and exited using the Linux kernel syscall convention, without C startup code.

The current CMotive frontend does **not** call CMO-REG-1 directly. Its C backend,
allocator and platform runtime are not replaced by these primitives. No claim of
end-to-end C ABI removal is made. The standalone assembly ZIP contains this native
layer separately, without the core's legacy C compatibility fixtures.

## CMotive core regression and hardening

21 public classes, 149 methods, 25 .HMOT files including four internal node/helper
headers. Maintained CMotive implementation files use .CMOT and .HMOT; no unsupported
generic template stubs or renamed D files are shipped. Assembly retains its true
.s extension. Genuine C compatibility fixtures retain .c/.h extensions.

Host: Linux x86_64, glibc 2.39, GCC 13.3.0. Compiler: CMotive 0.3.0-selfhost from
the retrieved 30 August 2026 archive, preserved unchanged with its SHA-256 pin.

| Check | Result |
|---|---|
| GNU Make build and CMotive source consumer | PASS |
| Full behavioral suite | PASS: 500,684 assertions; 149/149 methods exercised |
| Full behavioral suite against ASan/UBSan library | PASS; leak detection disabled |
| Native bounds/encoding/container stress | PASS |
| Red-black tree invariant checks | PASS: 52,000 checked operations plus destruction stress |
| Allocation-failure atomicity and tracked node cleanup | PASS |
| Eight concurrent stateless callers | PASS: 14,400 native-operation checks |
| Compatibility and STL retention | PASS: all 84 original and all 149 iteration-2 signatures retained |
| Generated manifest/header/export drift | PASS |
| Every standalone CMotive header | PASS: 25 headers compile |
| Existing compiler-backend export allowlist | PASS: 149 methods + 42 generated new/delete entries |
| Shipped library compiler runtime | Unused prelude/wrappers removed; only original allocation definitions retained |
| OS/runtime dependency audit | PASS: libc.so.6 only; imports allowlisted |
| Linux link protections | PASS: full RELRO, immediate binding, non-executable stack; no RPATH or writable executable segments |
| Minimal profile and release rejection fixtures | PASS: unchanged class bodies, retained STL, 12 negative cases rejected |
| Source/profile freshness | PASS: embedded fingerprint matches maintained inputs |
| CMake build / CTest | PASS: all seven tests |
| CMake installation, installed package consumer, installed .HMOT consumer | PASS |
| Autoconf 2.71 / Automake 1.16.5 build, check and install | PASS |
| Automake distribution build/check/install/uninstall/clean validation | PASS: make distcheck |
| Autotools-installed .HMOT consumer | PASS; internal header hierarchy retained |
| Legacy C and C++ backend compatibility clients | PASS; not the assembly interface |
| Full core Windows/macOS/ARM64 builds | NOT RUN |
| LeakSanitizer | UNVERIFIED: process inspection unavailable |

The deterministic suite uses seed 391724 and independent Python oracles: arithmetic,
math/bisect/heapq/datetime, codecs, zlib, hashlib.sha256, urllib percent encoding,
uuid and list/dict/deque/set models. All 149 methods are exercised; this is call
coverage, not a measured branch-coverage claim. SHA-256 includes standard vectors,
block/padding boundaries, randomized inputs and the million-'a' case.

The independent native red-black checker verifies ordering, parent pointers, root
color, red-child restrictions, equal black heights and element counts. Its test-only
allocator tracking injects failures into node/handle allocation, verifies unchanged
contents on failure, and checks allocation balance after destruction of populated
lists and trees. This supports these tested ownership paths, not global leak freedom.

A compiler-generated global cleanup stack was a concurrency risk in automatic helper
objects. Stateless helpers now use explicit Zero initialization, avoiding those
shared writes. A generated-code guard and concurrent tests protect this workaround;
they do not repair arbitrary application code generated by the same compiler.

ASan/UBSan run with detect_leaks=0 and halt_on_error=1. LeakSanitizer previously failed
on restricted process inspection, so no LSan pass is claimed. The full core binary
is still a C-emission backend artifact, SHA-256:
84d10c70866063b9ddf8ae450497bb55f476c9b514a058eac028ba887549cbdb

Source/provenance checks cover all 174 supplied D files. API/STL coverage and all
remaining modules/compiler restrictions are documented separately. General templates,
complete Phobos APIs, native frontend integration, physical ARM qualification and
full Windows/macOS library validation remain outstanding.

## Iteration 3 dependency changes

The production Linux ELF is 75,816 bytes, versus 129,952 bytes for iteration 2
with the same optimized GNU Make configuration (about 42% smaller). The compiler's
generic runtime prelude is absent, including unused networking, threading,
filesystem, I/O and built-in container wrappers. All CMotive class bodies are
preserved byte-for-byte, and all 149 methods and eight typed STL/algorithm classes
remain present. Existing .CMOT/.HMOT names and custom-register assembly remain.

The audited Linux imports are system calloc/free, optimizer-emitted memmove,
__stack_chk_fail and four weak compiler hooks. No libcurl, ODBC, SQLite, zlib,
C++ STL, math or thread shared library is needed. The minimal profile copies
only the original pinned compiler allocation definitions; its MIT license is
included and installed. This still uses the current C-emission backend and
system C runtime; it does not establish a native CMotive class ABI.

GNU Make, CMake/CTest, installed package/header consumers, Autoconf/Automake
build/check/install and make distcheck passed for the updated profile. The full
500,684-assertion suite passes normally and under ASan/UBSan with leak detection
disabled. Header/export checks confirm 25 headers and 191 allowed ABI entries.
The separate assembly sources and prebuilt objects are unchanged; their prior
115,733-check reports remain included and the packager revalidates artifact hashes.

Twelve rejection cases cover altered prelude/runtime, native helper/include
injection, lost class boundary, unexpected ELF import/library, embedded RPATH,
lazy binding, missing RELRO, executable stack and stale source fingerprint. The
packager reruns the audit on the exact release binary and requires a matching
passing full-method test report. Reproducible ZIP/TAR output and per-file archive
contents are checked. These are regression and packaging checks, not a complete
security audit, branch-coverage measurement or cross-platform certification.
