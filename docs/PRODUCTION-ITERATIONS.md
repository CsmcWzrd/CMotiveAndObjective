# Automated production iterations

Each numbered checkpoint passed GNU Make, the complete behavioral suite, API/provenance checks and the Linux dependency/profile audit. These are core-library checkpoints, not certification of the full compiler or Phobos.

| Iteration | Change | Assertions | Methods |
|---|---|---:|---:|
| 4 | Typed HashMapI64 with tombstone-safe probing and dictionary-model tests | 541,899 | 160 |
| 5 | Typed HashSetI64 with collision, deletion, full-table and set-model tests | 572,045 | 169 |
| 6 | Stable duplicate-key MultiMapI64 with indexed iteration and compaction | 659,700 | 180 |
| 7 | Typed StackI64, LIFO error atomicity and explicit new-container contracts | 673,185 | 187 |
| 8 | Nonrecursive merge sort with bounded caller workspace and oracle tests | 674,342 | 188 |
| 9 | Checked accumulation with intermediate-overflow and output-atomicity tests | 677,355 | 189 |
| 10 | Validated UTF-8 and Unicode-scalar transcoding with atomic error outputs | 682,377 | 192 |
| 11 | Explicit LE/BE UTF-16 scalar codec with strict surrogate validation | 700,485 | 195 |
| 12 | Strict checked I64/U64 text conversion across bases 2 through 36 | 758,431 | 199 |
| 13 | Hardware guard-page bounds checks for codecs, digests and full hash tables | 758,431 | 199 |
| 14 | Exhaustive Unicode scalar validation against independent codec golden hashes | 758,431 | 199 |
| 15 | Complete Gregorian 400-year cycle and supported date-range boundaries | 1,201,536 | 199 |
| 16 | Adversarial discovered hash collisions, tombstone chains and duplicate updates | 1,203,967 | 199 |
| 17 | Nth-allocation failure sweeps across owning lists and red-black trees | 1,203,967 | 199 |
| 18 | Strict-warning O0/O2/O3/Os build and complete regression matrix | 1,203,967 | 199 |
| 19 | Concurrent independent container lifetimes, mutation and populated destruction | 1,304,840 | 199 |
| 20 | Five-seed malformed codec fuzzing and failure-output preservation oracles | 1,417,340 | 199 |
| 21 | Release gates bind exact tests, method names, ELF target, exports and SONAME | 1,417,340 | 199 |
| 22 | Clean CMake and Autotools builds, native quality fixtures and installed extended consumers | 1,417,340 | 199 |
| 23 | Final sanitizer, optimization, clean-build and assembly qualification; explicit GA blockers | 1,417,340 | 199 |
| 24 | Restore checked endian-independent byte serialization | 1,425,516 | 201 |
| 25 | Restore allocation-free byte trimming splitting and substitution | 1,428,692 | 204 |
| 26 | Restore explicit little and big endian UTF-32 codec | 1,448,769 | 207 |
| 27 | Restore exact Phobos reflected CRC64 ECMA and ISO variants | 1,448,977 | 209 |
| 28 | Restore independent PCG32 streams and unbiased bounded samples | 1,475,476 | 212 |
| 29 | Restore strict CSV cursor parsing with capacity retry and atomic failure | 1,483,479 | 214 |
| 30 | Restore strict JSON string escaping Unicode and surrogate handling | 1,488,024 | 217 |
| 31 | Restore bounded iterative JSON grammar validation and token spans | 1,488,700 | 219 |
| 32 | Restore canonical unsigned varints and full-range signed ZigZag | 1,502,771 | 223 |
| 33 | Restore canonical unpadded URL-safe Base64 without external wrappers | 1,505,040 | 227 |
| 34 | Normalize compiler helper structs and unsigned literals to strict ISO C11 | 1,505,040 | 227 |
| 35 | Capture independently checked typed test vectors and replay against static and shared cores | 1,505,040 | 227 |
| 36 | Extend portable replay to all 227 methods with signed endpoint container models | 1,505,040 | 227 |
| 37 | Execute compiled core replay on x86 x86_64 ARM32 ARM64 and both ARM data byte orders | 1,505,040 | 227 |
| 38 | Cross-build and audit shared libraries for six Linux CPU and byte-order targets | 1,505,040 | 227 |
| 39 | Build Windows x64 DLL and audit exact exports OS imports ASLR and NX | 1,505,040 | 227 |
| 40 | Build macOS x64 ARM64 and universal dylibs and audit visibility and OS dependencies | 1,505,040 | 227 |
| 41 | Add source-bound native-host qualification kit and Windows hardware guard support | 1,505,040 | 227 |
| 42 | Reject stale and emulated native receipts and prevent flag-only production promotion | 1,505,040 | 227 |
| 43 | Final source-bound qualification distribution checks native runner and reproducible release candidate | 1,505,040 | 227 |
