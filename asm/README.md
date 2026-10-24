# Native runtime primitives — CMO-REG-1

These routines implement small C-library-like operations directly in assembly.
They use the custom CMotive register contract below, **not a C calling convention**.
There is no C wrapper, C prototype, libc import or C startup code. Functions are
leaf routines, reentrant, and use no global mutable state or heap allocation.

This is the runtime-primitives scope selected for iteration 2. The existing
CMotive 0.3.0 frontend still emits C and **does not yet call these registers
directly**. The assembly layer does not replace its whole native C runtime,
allocator, OS shims, exception machinery or compiler backend. Existing C-ABI
fixtures remain solely for compatibility/testing of that compiler backend;
they are not an interface to these assembly routines. The maintained CMotive
headers are the primary CMotive source interface. Do not describe the full
library as free of C emission or its backend dependencies.

## Register contract

| CPU | A0 / result | A1 | A2 | Additional scratch registers |
|---|---|---|---|---|
| x86 (i386+) | EDI | ESI | ECX | EAX, EDX |
| x86_64 | R10 | R11 | R8 | RAX, RDX, RCX |
| ARM32 (ARMv7-A, ARM state) | R4 | R5 | R6 | R0, R1, R2, R3 |
| ARM64 (ARMv8-A) | X9 | X10 | X11 | X12, X13, X14 |

All argument/result and listed scratch registers may be changed. Other general
registers, vector/FPU registers, SP and the ARM link register are preserved.
Condition flags may change. x86 CALL/RET uses a normal machine return address;
ARM BL/BX-LR and BL/RET use LR/X30. There is no C stack-argument layout or C
return-register contract. The routines allocate no stack frame. Callers must
provide a valid machine return address and a valid stack where the CPU requires it.

The object symbols are hidden to require direct/static binding: a platform's
lazy PLT resolver may clobber registers which CMO-REG-1 uses for arguments.
Link the provided architecture-matching .o/.a directly into an assembly caller.
ELF/EABI object metadata is separate from the register contract; these functions
do not use the platform's C argument/return convention.
Do not call these functions through ctypes, a C function pointer, a C ABI import,
or a compiler-generated CMotive call until a native custom-convention bridge exists.

## Functions

| Symbol | Arguments | Result |
|---|---|---|
| CMO_Asm_CopyBytes | A0 destination, A1 source, A2 byte count; no overlap | Original destination |
| CMO_Asm_MoveBytes | A0 destination, A1 source, A2 byte count; overlap allowed | Original destination |
| CMO_Asm_FillBytes | A0 destination, A1 value (low byte), A2 byte count | Original destination |
| CMO_Asm_CompareBytes | A0 first span, A1 second span, A2 byte count | -1, 0, or 1 using unsigned byte ordering |
| CMO_Asm_StrnLength | A0 byte string, A2 maximum byte count; A1 ignored | First NUL index, bounded by A2 |
| CMO_Asm_LoadU32LE | A0 address of four readable bytes | Zero-extended little-endian U32 |
| CMO_Asm_LoadU32BE | A0 address of four readable bytes | Zero-extended big-endian U32 |
| CMO_Asm_StoreU32LE | A0 address of four writable bytes, A1 low 32-bit value | Original destination |
| CMO_Asm_StoreU32BE | A0 address of four writable bytes, A1 low 32-bit value | Original destination |

Lengths/pointers are machine-word sized. Compare's -1 has every result bit set.
Callers must provide valid readable/writable spans, without address-space wrap.
Zero counts perform no memory access and allow null pointers. No pointer bounds
checks, errno values or allocation are provided. Unaligned U32 accesses are
supported; ARM uses individual byte loads/stores. These operations provide the
specified functionality, not binary compatibility with C memcpy/memmove/etc.

## CPUs and endianness

Six targets are built: x86 LE, x86_64 LE, ARM32 LE, ARM32 BE8, ARM64 LE and
ARM64 BE. x86 CPUs have no big-endian execution mode; both BE and LE **data**
formats are supported there through LoadU32/StoreU32 routines. Byte-copy/move/
fill/compare/string operations preserve byte sequences independently of endianness.
ARM32 BE8 and ARM64 BE keep instruction bytes little-endian while using big-endian
data mode. The ARM32 ELF BE8 flag and emulator data-endian state are checked.

Assembly files use their actual `.s` extension. CMotive implementation files keep
`.CMOT` and `.HMOT`; assembly is not mislabeled as CMotive or as a template.
These GNU-syntax sources currently build ELF objects/static archives. COFF and
Mach-O directive/unwind adaptations have not been implemented or verified.

## Build and verify

From the project root, with Zig available:

```sh
python3 -m pip install -r asm/requirements-test.txt
python3 tools/build_asm.py --zig /path/to/zig
python3 tests/test_asm.py
python3 tests/test_asm_native.py
```

The Python ziglang distribution also exposes a python-zig driver, which the build
script detects. Zig is used to assemble `.s`, link without startup libraries,
and create archives; no C source is passed to it. Output is build-asm/TARGET/:
primitives.o, libCMotiveAndObjectiveRuntime-1.0.0.a and a linked image used only by the emulator.
The linked primitives.elf has no OS application entry protocol; do not execute it
as an application. The native test creates its own freestanding Linux _start.

GNU make is available through `make -f asm/Makefile ZIG=/path/to/zig test`.
A standalone CMake project enables **no C language**:

```sh
cmake -S asm -B build-asm-cmake -DZIG_EXECUTABLE=/path/to/zig
cmake --build build-asm-cmake
ctest --test-dir build-asm-cmake --output-on-failure
```

All six CPU/endian configurations pass register, stack, memory, overlapping move,
zero-length, unsigned compare and endian load/store tests in Unicorn. This is CPU
emulation, not physical ARM hardware qualification. The x86_64 Linux freestanding
caller also runs natively. Native x86 ELF32 execution is unavailable on this host;
x86 behavior is verified in the emulator. Test/build reports include artifact hashes.
