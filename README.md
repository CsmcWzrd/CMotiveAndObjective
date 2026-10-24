# CMotiveAndObjective 1.0.0 — iteration 43

A class-based CMotive library adapted from the exact supplied Phobos snapshot.
This is a verified candidate for the implemented core. Full production promotion
remains blocked; see docs/PRODUCTION-READINESS.json and docs/REMAINING-PHOBOS.md.

36 public classes, 227 public methods, 43 .HMOT headers (seven internal helpers),
and 299 exported ABI symbols. All earlier 199 methods and all typed STL/container
classes remain. No external-library wrappers were introduced. Maintained source
uses .CMOT/.CMTV and headers/templates use .HMOT/.HMTV.

Restored functionality includes Endian, ByteStrings, Utf32, CRC64, Pcg32, Csv,
JsonString, JsonTokens, VarInt and Base64Url. The API contracts, errors, capacities,
borrowed lifetimes and concurrency rules are in docs/RESTORED-APIS.md and docs/API.md.

The pinned CMotive 0.3.0 frontend emits C. Build tools profile its prelude to keep
only original OS allocator definitions and class bodies, with unused empty helper
structs normalized to ISO C11. This compatibility backend still has a C ABI.
Standalone CMO-REG-1 assembly primitives use a custom register ABI and have no C
wrappers; they are not integrated into class dispatch or allocation. See asm/README.md.
Generic compiler template instantiation and a native compiler backend are separate
outstanding compiler work, not silently implemented by these typed containers.

## Build

Unpack toolchain/CMotive-v0.3.0-source.zip and build that compiler, then:

```sh
make -f Makefile.linux CMOTIVE_ROOT=/absolute/path/to/compiler test
make -f Makefile.linux CMOTIVE_ROOT=/absolute/path/to/compiler install PREFIX=/desired/prefix
cmake -S . -B build-cmake -DCMOTIVE_ROOT=/absolute/path/to/compiler
cmake --build build-cmake
ctest --test-dir build-cmake --output-on-failure
```

Autoconf/Automake: `autoreconf -fi`, then out-of-tree `configure`, `make check`,
`make install`, and `make distcheck`; set CMOTIVE_ROOT and CMOTIVE to the compiler.
Makefile.mac, Makefile.windows and build-support/vs2022 are retained. Native-host
kits include reviewed generated C and run with CMake/VS2022/Apple Clang; see
docs/NATIVE-QUALIFICATION.md. Python is used for build validation/tooling, not
as a library runtime dependency.

Linux output: libCMotiveAndObjective-1.0.0.so. Windows candidate:
CMotiveAndObjective-1.0.0.dll. macOS candidate: libCMotiveAndObjective-1.0.0.dylib,
including a universal x86_64/ARM64 container. Cross-built candidates require native
host qualification before deployment. Only Linux x86_64 has full native evidence.

Final verification details and exact hashes are in docs/VERIFICATION.md. CPU
emulation, cross-build audits and native execution are reported separately.
Archives include pinned source ZIPs, tests, build descriptions, licenses and
SHA256SUMS. Runtime dependencies are OS facilities only; test tools are separate.

Library/adaptations: Boost Software License 1.0 (LICENSE_1_0.txt). Compiler and
original allocator definitions: MIT (toolchain/CMotive-LICENSE-MIT.txt). Reference
inputs retain their original notices. Cross-tool notices identify test/build tools.
