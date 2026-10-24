# Dependency policy — iteration 23

The maintained library permits self-contained algorithms and OS-provided
facilities. Third-party library wrappers are excluded. Existing STL/container
implementations remain part of the library and its regression suite.

## Included and retained

All 149 original public methods and 21 classes are retained. The current core
has 199 public methods in 27 classes, including
ArrayVectorI64, BinaryHeapI64, SListI64, DListI64, RedBlackTreeI64, SortedMapI64,
QueueI64 and AlgorithmsI64. Their algorithms remain CMotive implementations;
no C++ STL library or compiler built-in container wrapper implements them.
SHA-256, checksums, codecs, byte utilities and integer/date algorithms likewise
require no third-party runtime library. A test-side Python oracle using zlib
or hashlib does not introduce those dependencies into the shipped library.

The standalone assembly primitives remain unchanged: nine routines across six
CPU/endian modes, using CMO-REG-1 rather than C ABI wrappers. Their object files
and static archives have no unresolved symbols or dynamic dependencies.

## Excluded external wrappers

| Modules | Disposition |
|---|---|
| etc.c.curl, std.net.curl | No libcurl wrapper or HTTP/TLS replacement shipped |
| etc.c.odbc.sql, sqlext, sqltypes, sqlucode | No ODBC binding shipped |
| etc.c.sqlite3 | No SQLite binding shipped |
| etc.c.zlib, std.zlib | No zlib binding or compression replacement shipped |

The exact unmodified Phobos snapshot and compiler ZIP remain provenance inputs.
They contain upstream sources and bindings but are not linked or installed as
library implementations. The inventory explicitly marks the nine wrapper modules
excluded. A future self-contained compression/database/protocol implementation
would require its own implementation and tests; no silent success stub replaces
an excluded wrapper.

OS filesystem, process, clock, sockets, threading, Windows registry, character
conversion and system errors are permitted in principle. APIs for them have not
been implemented by this port. The Windows modules are marked deferred OS
services rather than rejected as external dependencies. No claim is made that
OS sockets alone provide HTTP/TLS semantics.

## Minimal current-compiler profile

The pinned CMotive 0.3.0 frontend emits a large generic prelude and includes all
of runtime.c even for this algorithm-only core. tools/emit_core.py replaces that
unused prelude with standard type/allocation declarations and the original two
allocation definitions copied verbatim from the pinned compiler runtime. Every
generated class body remains byte-for-byte unchanged. Exact prelude and runtime
hashes, allowed generated calls and unexpected directives are checked before
writing the output. A changed compiler fails closed and needs a reviewed profile.

The resulting shared library includes none of the compiler's unused socket,
thread, filesystem, I/O or built-in container wrappers. The implementation uses
system calloc/free for allocation; the native optimizer may emit memset, memcpy
or memmove, and stack protection may require __stack_chk_fail. Standard weak
compiler hooks are permitted. These are system C runtime facilities, not
third-party library dependencies. On tested Linux, the only DT_NEEDED entry is
libc.so.6. The core build no longer links libm, pthread or Windows ws2_32.

This profile operates on the current compiler's C intermediate. It does not
replace the frontend with a native backend, change the legacy dynamic-library
calling convention, or connect the standalone assembly convention to class calls.
CMotive application builds using the unmodified compiler directly still include
its ordinary OS runtime; the minimal profile applies to this shared library.
Windows and macOS core builds and their OS-runtime import sets remain unverified.

## Release gates

Linux shared-library builds enable strong stack protection, full RELRO,
immediate binding, a non-executable stack and undefined-symbol rejection.
The release audit checks the exact needed-library set, import allowlist,
weak-hook binding, RELRO and BIND_NOW, absence of runtime search paths, and
absence of writable executable segments. It uses Python's standard library
and readelf. Sanitizer artifacts intentionally load instrumentation runtimes;
they cannot pass the production dependency allowlist or be packaged as releases.

Tests exercise both acceptance and rejection: changed compiler/prelude, changed
runtime, injected native helper, injected include, missing class boundary,
unapproved ELF import, extra libm dependency, RPATH, lazy binding, missing RELRO
executable stack and a stale source fingerprint. API baselines prevent deletion of every iteration-2 method,
including the maintained STL functionality. The packager audits the exact binary
again and also requires its matching full-method behavioral report. An embedded
source/profile fingerprint prevents packaging an older binary after maintained
source or dependency-policy changes; it is a freshness check, not a signature.

These gates are production hardening for the implemented subset. General
Phobos/template support, native frontend integration and qualification on all
platforms remain outstanding; see PORTING-STATUS.md and VERIFICATION.md.

The expanded hash/set/multimap/stack, Unicode and integer-conversion algorithms
are self-contained CMotive implementations as well. Current Linux ELF audits
also require the correct architecture, SONAME and exact 253-symbol public ABI.
Behavioral reports bind the exact test sources and exercised method names.
