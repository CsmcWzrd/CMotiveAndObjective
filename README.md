# CMotiveAndObjective 1.0.0 — iteration 2

A separately maintained CMotive standard-library port based on the exact supplied
Phobos snapshot. **This is a tested and hardened core, not a completed or production-ready
Phobos port.** Read docs/PORTING-STATUS.md. No template placeholders or renamed D
files are presented as working CMotive implementations.

| Platform | Output |
|---|---|
| Linux | libCMotiveAndObjective-1.0.0.so |
| Windows | CMotiveAndObjective-1.0.0.dll and import library |
| macOS | libCMotiveAndObjective-1.0.0.dylib |

## Linux build and test

Requires C11 compiler, GNU make and Python 3 for tests. The exact compiler source
archive is included so the project does not depend on old chat download links.

```sh
unzip toolchain/CMotive-v0.3.0-source.zip -d toolchain
make -C toolchain/cmotive-0.3.0-selfhost -f Makefile.linux -j2
make -f Makefile.linux -j2
make -f Makefile.linux test
make -f Makefile.linux sanitize-full
```

The sanitizer target runs ASan/UBSan. Leak checking defaults off because this
execution environment blocks LeakSanitizer process inspection. On a host which
supports it, use `make sanitize ASAN_OPTIONS=detect_leaks=1`.

For an existing compiler, set `CMOTIVE_ROOT=/absolute/path/to/cmotive-0.3.0-selfhost`
and optionally `CMOTIVE=/absolute/path/to/cmotive` on each make command. Its root
must contain lib/Sys/runtime.c. Outputs go to build/.
`make install PREFIX=/desired/path` installs the library/headers; DESTDIR supports
staging. The maintained implementation is CMotive; the compiler emits C internally.

## CMake / Visual Studio 2022

```sh
cmake -S . -B build-cmake -DCMOTIVE_ROOT=/absolute/path/to/compiler
cmake --build build-cmake --config Release
ctest --test-dir build-cmake -C Release --output-on-failure
```

On Windows first build the bundled compiler using its own Windows instructions.
Add `-G "Visual Studio 17 2022" -A x64` to generate native VS2022 build projects.
A checked-in VS2022 build-wrapper solution is under build-support/vs2022. Set
CMotiveRoot in its project properties or CMOTIVE_ROOT in the environment. It invokes
CMake to generate the actual compilation projects. Makefile.windows uses nmake.

## Automake / Autoconf

Use a clean source copy; configure writes Makefile. Requires autoconf and automake.

```sh
autoreconf -fi
mkdir autotools-build
cd autotools-build
CMOTIVE_ROOT=/absolute/path/to/compiler ../configure --prefix=/desired/path
make
make check
make install
```

For macOS, build the compiler with Makefile.mac, then use Makefile.mac here or
CMake. GNU Make, CMake/CTest and Autoconf/Automake build routes are tested on Linux.
Windows/macOS remain unverified here.
The included prebuilt library is Linux x86_64 only.

## API and documentation

- docs/API.md: signatures, contracts, errors, ownership and buffer rules.
- docs/PHOBOS-MODULES.md: disposition of every supplied D source file.
- docs/PORTING-STATUS.md: implemented scope, exclusions and unfinished work.
- docs/VERIFICATION.md: checks actually run and their limits.
- api.json: machine-readable public method list.
- docs/STL-COVERAGE.md: typed container families, ownership and iterators.
- tools/sync_api.py --check: declaration/manifest/header/export consistency.
- tests/check_metadata.py: original ABI compatibility and source pins.
- tests/: independent Python oracles, C ABI/boundary stress, CMotive consumer,
  focused compiler capability probes.

CMotive consumers include required .HMOT implementations, as in tests/smoke.CMOT.
Shared-library consumers use opaque handles from include/CMotiveAndObjective.h;
tests/abi_smoke.c is a complete example. Full library algorithms are in .HMOT source;
the C file is only a test client. No handwritten C/C++ implementation backs the
149 methods, although the compiler itself injects its native C runtime.

## License

Boost Software License 1.0 for the new port, build files and tests. Original Phobos
notices and the bundled compiler's own license remain applicable. The Phobos
reference is not relicensed as MIT. Algorithms are adapted to CMotive class/buffer
APIs; module mapping does not claim complete or line-for-line translation.

## Iteration 2 changes

21 classes and 149 public methods. Added SHA-256, URI percent encoding, UUID
format/parse/inspect, SortedMapI64, QueueI64, SListI64, DListI64 and RedBlackTreeI64.
All five supplied Phobos container families have typed implementations; arbitrary
container templates are still blocked. Maintained library sources use .CMOT and
headers use .HMOT; genuine C ABI fixtures keep .c/.h extensions.

CMake exports an installed package: use `find_package(CMotiveAndObjective 1.0 CONFIG
REQUIRED)` and link `CMotiveAndObjective::CMotiveAndObjective`. Internal CMotive
headers retain their directory layout on all installation routes. GNU make rules
are in build-support/GNUmakefile.mk, so Makefile.linux/mac remain usable after
Autoconf writes a configured Makefile.

`make -f Makefile.linux sanitize-full` runs the complete behavioral suite through
ASan/UBSan on Linux/GCC, as well as native stress/invariant/allocation-failure
checks. On other systems, use the native `sanitize` target. LeakSanitizer is a
separate unsupported check here; tracked container allocation balance is tested.

## Assembly runtime (selected scope)

See [asm/README.md](asm/README.md). Nine runtime primitives use a custom CMotive
register convention, with no C ABI wrapper. Six CPU/endian targets are supplied,
including explicit LE/BE data operations on x86, which only executes little-endian.
The assembly layer is standalone; the current compiler still emits C and has not
been extended to call this custom convention. No full-runtime replacement is claimed.

The full-core prebuilt .so is an existing compiler C-backend regression artifact,
not a C-free/native-assembly build. Use the standalone assembly-runtime package
for CMO-REG-1 .o/.a files without C interfaces. See docs/VERIFICATION.md for limits.
