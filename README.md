# CMotiveAndObjective 1.0.0 — iteration 23

A separately maintained, self-contained CMotive library based on the supplied
Phobos snapshot, with additional typed STL containers. The current core has
**27 public classes and 199 tested methods**, with 32 .HMOT headers including five
internal helpers. Maintained source uses .CMOT/.HMOT. No generic template stubs
or renamed D code are presented as working implementations.

**Status: tested Linux core candidate; full production/GA promotion is blocked.**
See docs/PRODUCTION-READINESS.json and docs/PORTING-STATUS.md. Version 1.0.0 is the
requested filename/version, not a claim of complete Phobos parity or certification.
Twenty continuation checkpoints, iterations 4–23, are recorded in
[docs/PRODUCTION-ITERATIONS.md](docs/PRODUCTION-ITERATIONS.md).

All original STL functionality is retained. The library includes eleven typed
containers, numeric/date utilities, codecs, SHA-256, checksums, URI/UUID utilities,
UTF-8/UTF-16/scalar transcoding and checked integer text conversion. Algorithms
are CMotive implementations. External library wrappers (curl, ODBC, SQLite, zlib)
are excluded; OS facilities and self-contained replacements are permitted. The
verified Linux shared library needs only the system C runtime. See
[docs/DEPENDENCIES.md](docs/DEPENDENCIES.md).

The pinned current frontend emits C. A fail-closed minimal profile removes its
unused native wrappers and retains its original system allocation definitions;
generated class bodies remain unchanged. This is still the current compatibility
backend, not a native PCC backend. A separate assembly layer supplies nine
CMO-REG-1 custom-register primitives across six CPU/endian modes, without a C ABI
wrapper. Direct compiler integration remains unfinished. See asm/README.md.

## Build and test on Linux

Requires Python 3, GNU Make, a C11 compiler and binutils/readelf. The exact compiler
source is bundled as a provenance input, retaining its MIT license.

```sh
unzip toolchain/CMotive-v0.3.0-source.zip -d toolchain
make -C toolchain/cmotive-0.3.0-selfhost -f Makefile.linux -j2
make -f Makefile.linux -j2
make -f Makefile.linux test
make -f Makefile.linux sanitize-full
make -f Makefile.linux install PREFIX=/desired/path
```

For an existing compiler, pass CMOTIVE_ROOT=/absolute/path/to/compiler and
optionally CMOTIVE=/absolute/path/to/cmotive on each make command. Tests include
all methods, native guard pages, exhaustive Unicode, allocation failures, the
exact ABI/dependency allowlist and report freshness. Sanitizer runs disable leak
detection because this execution environment blocks LeakSanitizer inspection;
LSan and ThreadSanitizer passes are not claimed. On a supporting host, the native
sanitizer targets accept ASAN_OPTIONS=detect_leaks=1.

## CMake and Visual Studio 2022

```sh
cmake -S . -B build-cmake -DCMOTIVE_ROOT=/absolute/path/to/compiler
cmake --build build-cmake -j2
ctest --test-dir build-cmake --output-on-failure
cmake --install build-cmake --prefix /desired/path
```

The installed CMake target is CMotiveAndObjective::CMotiveAndObjective. A VS2022
wrapper solution is under build-support/vs2022; set CMOTIVE_ROOT and use the x64
configuration. Makefile.windows invokes the VS2022 CMake generator. On macOS use
Makefile.mac or CMake. Outputs are libCMotiveAndObjective-1.0.0.so on Linux,
CMotiveAndObjective-1.0.0.dll on Windows, and libCMotiveAndObjective-1.0.0.dylib on
macOS. Only the Linux x86_64 core binary is supplied and qualified here. DLL/dylib
builds and full ARM core binaries are unverified; none is fabricated.

## Autoconf and Automake

Use a clean source copy (configure writes Makefile).

```sh
autoreconf -fi
mkdir autotools-build
cd autotools-build
export CMOTIVE_ROOT=/absolute/path/to/compiler
../configure --prefix=/desired/path
make -j2
make check
make install
make distcheck
```

The final qualification runs GNU Make, CMake/CTest and Autotools, plus installed
CMotive header and CMake-package consumers. Strict-warning builds are checked at
O0/O2/O3/Os. See docs/VERIFICATION.md for actual evidence and limitations.

## API, ownership and releases

Read docs/API.md and docs/API-EXTENSIONS.md before using raw buffers or owning
containers; source signatures are in docs/API-SIGNATURES.md. CMotive consumers
include the required .HMOT implementations (tests/smoke.CMOT includes all new
classes). Legacy compatibility clients use opaque handles from the genuine .h
header. Those C test fixtures are separate from the custom-register assembly ABI.

Owning lists/trees must not be shallow-copied. Borrowed buffers must remain valid
and correctly sized; mutable shared instances require caller synchronization.
See docs/STL-COVERAGE.md for supported types, iterator validity and complexity.

Release packaging binds the exact binary, source profile, test sources, exercised
method names, dependency/export allowlist and ELF protections. --require-production
refuses promotion while documented blockers remain. Normal packaging produces a
verified core candidate and does not override that gate. Source and compiler pins,
all 174 upstream file hashes and every partial/deferred/excluded module are tracked.
