# Iteration 2 — hardened core, incomplete Phobos port

Version 1.0.0 is the requested output name/version. It does not certify full
Phobos parity, production readiness, stable ABI or cross-platform verification.

The supplied snapshot contains 174 D files, without embedded release tag/commit
metadata. The unmodified reference ZIP is under upstream/. Its SHA-256 is
218efa1d7fa6cb1900d5f5dfea3921ee026c121e115bd0c41278ad87b5b92e56.
All file hashes and dispositions are in phobos-inventory.json and PHOBOS-MODULES.md.

## Implemented

21 public classes and 149 methods, including the original numeric, encoding,
byte-string and date utilities, plus SHA-256, URI component encoding, UUID text
handling and the typed STL/container families described in STL-COVERAGE.md.
25 CMotive .HMOT files include four internal node/helper headers. Public methods
use CMotive source only; .c tests and the .h C ABI header are genuine interoperability
fixtures, not CMotive files with misleading extensions. No unsupported .HMTV
placeholders or renamed D sources are shipped.

The 84 original C ABI method signatures remain unchanged. 149 methods plus 42
new/delete functions are exported; internal helpers remain hidden. This is an
adapted typed API, not a drop-in Phobos or general C++ STL implementation.

## Compiler constraints

The latest retrieved source archive, dated 2026-08-30, is
cmotive-source-selfhost-v0.3.0-qa1200-mit-runtime-fix-interop-doc.zip.
It is included unchanged under toolchain/ as CMotive-v0.3.0-source.zip.

- src/frontend/selfhost/CMotiveFrontend.CMOT, skip_template: arbitrary Template
  Class definitions are skipped. tests/compiler-probes/GenericBox.CMOT demonstrates
  the resulting failure for Box<I32>. General container/range templates therefore
  cannot currently be verified with this compiler; no template placeholders ship.
- parse_args has no -fPIC or -shared support. Build files use --emit-c followed
  by the platform C compiler/linker. Maintained methods are CMotive; this toolchain
  internally uses C emission and a native C runtime. It is not a native PCC backend.
- The lexer splits >>=, so methods use explicit shifts and assignments.
- Names starting Vector collide with a built-in special case; the class is named
  ArrayVectorI64.
- Dynamic library exports are restricted to 149 methods and 42 new/delete functions.
  The C consumer verifies separate dynamic linking. CMotive consumers currently
  include .HMOT implementations; separate external class declarations and a direct
  CMotive dynamic-class consumer are not verified.

## Excluded direct mappings

D reflection (__traits, TypeInfo), typelists/CTFE/mixins, qualifier and alias-this
semantics, delegates, D exception/GC lifetime contracts and arbitrary templates
cannot be faithfully mapped by this compiler. D demangling has no CMotive ABI
equivalent. Native C/OS bindings such as libcurl, zlib and Windows registry/code
pages/errors cannot become pure portable language logic by renaming declarations.
These direct mappings are excluded. Redesigned APIs or explicit ABI shims could
support portions in future; exclusion does not prove the underlying algorithm is
impossible in CMotive.

## Remaining original scope

Every deferred module and the remaining functions in partial modules are absent.
This includes arbitrary-type containers/ranges, hash/multi containers, big integers,
floating point/special math, CSV, JSON, regex, formatting, serialization, UUID
generation, full Unicode normalization/case folding, compression/archives, random
facilities, filesystem/IO/process/socket/
timezone/concurrency facilities and associated tests. These are not all impossible;
they require further implementation and OS services need an explicit ABI policy.
This package does not fulfill the original request to port all implementable APIs.

## Validation limits

Linux x86_64 GCC build, shared C ABI, CMotive source consumer and behavioral tests
are run locally; exact outcomes are in VERIFICATION.md. Full core-library Windows/macOS/ARM64 builds are
unverified (separate assembly targets are tested as described below). GNU Make, CMake/CTest, installation consumers and Autoconf/Automake are now
executed locally. See VERIFICATION.md for exact checks. No DLL/dylib is fabricated.

Port code, tests and build files use Boost Software License 1.0; preserve Phobos
notices and the original license. The bundled compiler retains its own license.

## Compiler/runtime hardening in this iteration

Stateless helper objects use explicit Zero initialization so library methods do
not write this compiler's global automatic-object cleanup stack. A generated-code
check and an eight-thread behavioral test guard this workaround. Owning-container
allocation-failure paths and destructor cleanup are tested using native fixture
allocation tracking. This does not certify leak freedom of every compiler/runtime
path; LeakSanitizer remains unavailable in this environment.

## Assembly runtime scope selected for iteration 2

Nine native primitives implement copy/move/fill/compare/bounded string length and
explicit LE/BE U32 loads/stores. They use CMO-REG-1 custom registers, not the C ABI.
Four .s sources build six ELF targets: x86 LE, x86_64 LE, ARM32 LE/BE8 and ARM64
LE/BE. x86 has no big-endian execution mode; its endian routines support BE data.
All six target modes are exercised by CPU emulation, and the x86_64 freestanding
caller runs natively. ELF32 native execution is not available on this host.
No C wrapper, libc import, C startup or C language build is used for this layer.
See asm/README.md for the complete contract and standalone CMake/Make build.

The scope explicitly does not replace the compiler C backend. These primitives
are not yet called directly by the current frontend; its custom-convention bridge,
allocator and OS runtime replacement remain future work. The separate assembly
ZIP contains only this native layer and its build/test tools, without C interfaces.
