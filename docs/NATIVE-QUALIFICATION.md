# Native host qualification

Prepare a kit using tools/prepare_native.py after tools/portable.py has passed.
The kit contains reviewed generated C and typed replay inputs, maintained CMotive
sources, pinned provenance and tests. It needs Python 3, CMake 3.20+, and a C11
compiler. On Windows use the Visual Studio 2022 x64 developer prompt. On macOS
use Apple Clang and the installed SDK. No frontend executable is needed to build
the generated core in this kit. Run `python native/run_native.py` at its root.

The runner verifies every manifest input, builds a real shared library, runs
seven tests including the independent Python suite and real shared-library
replay, then emits native-build/native-receipt.json. Copy the receipt with the
matching built library back for review. A receipt reports actual runner OS and
process architecture. It is local evidence, not cryptographic attestation.

Native Windows, macOS x86_64/ARM64 and ARM Linux evidence is still required for
production qualification. CPU emulation and cross-build audits are separate
levels of evidence. Never relabel an emulation report as a native-host receipt.
