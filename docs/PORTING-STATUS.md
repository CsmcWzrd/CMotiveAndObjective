# Porting status, iteration 43

The implemented core has 36 public classes and 227 methods. Typed STL APIs are
preserved. RESTORED-APIS.md defines restored functionality. PHOBOS-MODULES.md and
REMAINING-PHOBOS.md document exact snapshot coverage and remaining work. No claim
of full Phobos parity is made. Excluded external-library wrappers remain excluded.

The pinned compiler emits C. Native class code generation, full generic templates,
and integration of the custom-register standalone assembly are outstanding. A
minimal C-emission profile keeps OS allocator definitions, not the unused runtime.

Native full-suite evidence is Linux x86_64. Six compiled-core CPU modes, Linux
ELF cross-builds, Windows PE audits and macOS Mach-O audits add portability
evidence. Native Windows/macOS/ARM tests are still required. The native-host kit
runs those tests on available systems and binds receipts to source/test hashes.
