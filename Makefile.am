AUTOMAKE_OPTIONS = foreign
include $(srcdir)/build-support/headers.mk
cmolibdir = $(libdir)
cmolib_DATA = libCMotiveAndObjective-1.0.0.@CMO_EXT@
include_HEADERS = include/CMotiveAndObjective.h
cmoincludedir = $(includedir)/CMotiveAndObjective
cmoinclude_HEADERS = $(cmo_public_headers)
cmointernaldir = $(includedir)/CMotiveAndObjective/Internal
cmointernal_HEADERS = $(cmo_internal_headers)
dist_doc_DATA = docs/API.md docs/API-SIGNATURES.md docs/STL-COVERAGE.md docs/PORTING-STATUS.md docs/VERIFICATION.md
EXTRA_DIST = src asm api.json tests tools docs cmake build-support upstream toolchain VERSION ITERATION LICENSE_1_0.txt CMakeLists.txt README.md Makefile.linux Makefile.mac Makefile.windows
BUILT_SOURCES = CMotiveAndObjective.c
CLEANFILES = CMotiveAndObjective.c cmotive-smoke.c cmotive-smoke libCMotiveAndObjective-1.0.0.@CMO_EXT@ abi_smoke rb_invariants test-result.json
CMotiveAndObjective.c: $(srcdir)/src/CMotiveAndObjective.CMOT $(addprefix $(srcdir)/,$(cmo_header_files)) $(CMOTIVE)
	"$(CMOTIVE)" -I "$(abs_srcdir)/include" --emit-c "$(abs_srcdir)/src/CMotiveAndObjective.CMOT" -o "$@"
libCMotiveAndObjective-1.0.0.@CMO_EXT@: CMotiveAndObjective.c $(CMOTIVE_ROOT)/lib/Sys/runtime.c $(srcdir)/build-support/exports.map $(srcdir)/build-support/exports.macos
	$(CC) $(CFLAGS) -std=c11 -fPIC -I"$(CMOTIVE_ROOT)/lib/Sys" @CMO_SHARED@ @CMO_EXPORTS@ $< -o $@ $(LDFLAGS) -pthread -lm
check-local: libCMotiveAndObjective-1.0.0.@CMO_EXT@
	$(CC) $(CFLAGS) -std=c11 -I"$(abs_srcdir)/include" "$(srcdir)/tests/abi_smoke.c" ./libCMotiveAndObjective-1.0.0.@CMO_EXT@ -Wl,-rpath,"$(abs_builddir)" -o abi_smoke $(LDFLAGS)
	./abi_smoke
	$(CC) $(CFLAGS) -std=c11 -I"$(abs_builddir)" -I"$(CMOTIVE_ROOT)/lib/Sys" "$(srcdir)/tests/rb_invariants.c" -o rb_invariants $(LDFLAGS) -pthread -lm
	./rb_invariants
	"$(CMOTIVE)" -I "$(abs_srcdir)/include" --emit-c "$(abs_srcdir)/tests/smoke.CMOT" -o cmotive-smoke.c
	$(CC) $(CFLAGS) -std=c11 -I"$(CMOTIVE_ROOT)/lib/Sys" cmotive-smoke.c -o cmotive-smoke $(LDFLAGS) -pthread -lm
	./cmotive-smoke
	$(PYTHON) "$(srcdir)/tests/test_core.py" "$(abs_builddir)/libCMotiveAndObjective-1.0.0.@CMO_EXT@" test-result.json
	$(PYTHON) "$(srcdir)/tests/check_metadata.py"
