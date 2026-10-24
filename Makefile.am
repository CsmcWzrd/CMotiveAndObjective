AUTOMAKE_OPTIONS = foreign
include $(srcdir)/build-support/headers.mk
cmolibdir = $(libdir)
cmolib_DATA = libCMotiveAndObjective-1.0.0.@CMO_EXT@
include_HEADERS = include/CMotiveAndObjective.h
cmoincludedir = $(includedir)/CMotiveAndObjective
cmoinclude_HEADERS = $(cmo_public_headers)
cmointernaldir = $(includedir)/CMotiveAndObjective/Internal
cmointernal_HEADERS = $(cmo_internal_headers)
dist_doc_DATA = toolchain/CMotive-LICENSE-MIT.txt docs/API.md docs/API-SIGNATURES.md docs/STL-COVERAGE.md docs/PORTING-STATUS.md docs/VERIFICATION.md docs/DEPENDENCIES.md docs/API-EXTENSIONS.md docs/PRODUCTION-ITERATIONS.md
EXTRA_DIST = native src asm api.json tests tools docs cmake build-support upstream toolchain VERSION ITERATION LICENSE_1_0.txt CMakeLists.txt README.md Makefile.linux Makefile.mac Makefile.windows
BUILT_SOURCES = CMotiveAndObjective.c
CLEANFILES = guard_pages unicode_exhaustive dependency-report.json CMotiveAndObjective.c cmotive-smoke.c cmotive-smoke libCMotiveAndObjective-1.0.0.@CMO_EXT@ abi_smoke rb_invariants test-result.json
CMotiveAndObjective.c: $(srcdir)/VERSION $(srcdir)/ITERATION $(srcdir)/api.json $(srcdir)/src/CMotiveAndObjective.CMOT $(addprefix $(srcdir)/,$(cmo_header_files)) $(CMOTIVE) $(srcdir)/tools/emit_core.py $(srcdir)/build-support/dependency-policy.json $(CMOTIVE_ROOT)/lib/Sys/runtime.c
	$(PYTHON) "$(srcdir)/tools/emit_core.py" --compiler "$(CMOTIVE)" --compiler-root "$(CMOTIVE_ROOT)" --output "$@"
libCMotiveAndObjective-1.0.0.@CMO_EXT@: CMotiveAndObjective.c $(CMOTIVE_ROOT)/lib/Sys/runtime.c $(srcdir)/build-support/exports.map $(srcdir)/build-support/exports.macos
	$(CC) $(CFLAGS) -std=c11 -fPIC @CMO_SHARED@ @CMO_EXPORTS@ @CMO_HARDEN@ $< -o $@ $(LDFLAGS)
check-local: libCMotiveAndObjective-1.0.0.@CMO_EXT@
	$(CC) $(CFLAGS) -std=c11 -I"$(abs_srcdir)/include" "$(srcdir)/tests/abi_smoke.c" ./libCMotiveAndObjective-1.0.0.@CMO_EXT@ -Wl,-rpath,"$(abs_builddir)" -o abi_smoke $(LDFLAGS)
	./abi_smoke
	$(CC) $(CFLAGS) -std=c11 -I"$(abs_builddir)" "$(srcdir)/tests/rb_invariants.c" -o rb_invariants $(LDFLAGS)
	./rb_invariants
	$(CC) $(CFLAGS) -std=c11 -I"$(abs_builddir)" "$(srcdir)/tests/unicode_exhaustive.c" -o unicode_exhaustive $(LDFLAGS)
	./unicode_exhaustive
	if test "@CMO_EXT@" = so; then set -e; $(CC) $(CFLAGS) -std=c11 -I"$(abs_builddir)" "$(srcdir)/tests/guard_pages.c" -o guard_pages $(LDFLAGS); ./guard_pages; fi
	"$(CMOTIVE)" -I "$(abs_srcdir)/include" --emit-c "$(abs_srcdir)/tests/smoke.CMOT" -o cmotive-smoke.c
	$(CC) $(CFLAGS) -std=c11 -I"$(CMOTIVE_ROOT)/lib/Sys" cmotive-smoke.c -o cmotive-smoke $(LDFLAGS) -pthread -lm
	./cmotive-smoke
	$(PYTHON) "$(srcdir)/tests/test_core.py" "$(abs_builddir)/libCMotiveAndObjective-1.0.0.@CMO_EXT@" test-result.json
	$(PYTHON) "$(srcdir)/tests/test_release_gates.py" "$(abs_builddir)/libCMotiveAndObjective-1.0.0.@CMO_EXT@" test-result.json
	$(PYTHON) "$(srcdir)/tests/check_metadata.py"
	if test "@CMO_EXT@" = so; then set -e; $(PYTHON) "$(srcdir)/tests/check_dependencies.py" "$(abs_builddir)/libCMotiveAndObjective-1.0.0.so" --report dependency-report.json; $(PYTHON) "$(srcdir)/tests/test_runtime_profile.py" "$(CMOTIVE)" "$(CMOTIVE_ROOT)"; fi
