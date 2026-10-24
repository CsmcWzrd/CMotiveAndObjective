# GNU make. CMotive maintained sources, generated C intermediate.
CMOTIVE_ROOT ?= $(CURDIR)/toolchain/cmotive-0.3.0-selfhost
CMOTIVE ?= $(CMOTIVE_ROOT)/build/bin/cmotive
CC ?= cc
PYTHON ?= python3
BUILD ?= build
PREFIX ?= /usr/local
DESTDIR ?=
CFLAGS ?= -O2 -std=c11
LDFLAGS ?=
ASAN_OPTIONS ?= detect_leaks=0
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
EXT = dylib
RPATH = @loader_path
SHARED_FLAGS = -dynamiclib -Wl,-install_name,@rpath/libCMotiveAndObjective-1.0.0.dylib -Wl,-exported_symbols_list,build-support/exports.macos
else
EXT = so
RPATH = $$ORIGIN
SHARED_FLAGS = -shared -Wl,-soname,libCMotiveAndObjective-1.0.0.so -Wl,--version-script=build-support/exports.map
endif
LIB = $(BUILD)/libCMotiveAndObjective-1.0.0.$(EXT)
HEADERS = $(wildcard include/CMotiveAndObjective/*.HMOT include/CMotiveAndObjective/Internal/*.HMOT)
RUNTIME = $(wildcard $(CMOTIVE_ROOT)/lib/Sys/*.[ch])
.PHONY: all test clean install cmotive-test sanitize sanitize-full check-api
all: $(LIB)
$(BUILD):
	mkdir -p "$@"
$(BUILD)/CMotiveAndObjective.c: src/CMotiveAndObjective.CMOT $(HEADERS) $(CMOTIVE) | $(BUILD)
	"$(CMOTIVE)" -I "$(CURDIR)/include" --emit-c "$<" -o "$@"
$(LIB): $(BUILD)/CMotiveAndObjective.c $(RUNTIME) build-support/exports.map build-support/exports.macos build-support/exports.def
	$(CC) $(CFLAGS) -fPIC -I"$(CMOTIVE_ROOT)/lib/Sys" $(SHARED_FLAGS) "$<" -o "$@" $(LDFLAGS) -pthread -lm
$(BUILD)/abi_smoke: tests/abi_smoke.c include/CMotiveAndObjective.h $(LIB)
	$(CC) $(CFLAGS) -Iinclude "$<" "$(LIB)" -Wl,-rpath,'$(RPATH)' -o "$@" $(LDFLAGS)
$(BUILD)/rb_invariants: tests/rb_invariants.c $(BUILD)/CMotiveAndObjective.c
	$(CC) $(CFLAGS) -I"$(BUILD)" -I"$(CMOTIVE_ROOT)/lib/Sys" "$<" -o "$@" $(LDFLAGS) -pthread -lm
test: $(BUILD)/abi_smoke $(BUILD)/rb_invariants cmotive-test check-api
	"$(BUILD)/abi_smoke"
	"$(BUILD)/rb_invariants"
	$(PYTHON) tests/test_core.py "$(LIB)" "$(BUILD)/test-result.json"
check-api:
	$(PYTHON) tests/check_metadata.py
cmotive-test: | $(BUILD)
	"$(CMOTIVE)" -I "$(CURDIR)/include" tests/smoke.CMOT -o "$(BUILD)/cmotive-smoke"
	"$(BUILD)/cmotive-smoke"
sanitize:
	$(MAKE) -f build-support/GNUmakefile.mk BUILD=build-sanitize CFLAGS='-O1 -g -std=c11 -fsanitize=address,undefined -fno-omit-frame-pointer' LDFLAGS='-fsanitize=address,undefined' build-sanitize/abi_smoke build-sanitize/rb_invariants
	ASAN_OPTIONS='$(ASAN_OPTIONS)' UBSAN_OPTIONS=halt_on_error=1 ./build-sanitize/abi_smoke
	ASAN_OPTIONS='$(ASAN_OPTIONS)' UBSAN_OPTIONS=halt_on_error=1 ./build-sanitize/rb_invariants
sanitize-full: sanitize
	$(PYTHON) tools/run_sanitized.py "$(CURDIR)/build-sanitize/libCMotiveAndObjective-1.0.0.so"
install: all
	mkdir -p "$(DESTDIR)$(PREFIX)/lib" "$(DESTDIR)$(PREFIX)/include/CMotiveAndObjective"
	cp "$(LIB)" "$(DESTDIR)$(PREFIX)/lib/"
	cp include/CMotiveAndObjective.h "$(DESTDIR)$(PREFIX)/include/"
	cp -R include/CMotiveAndObjective/. "$(DESTDIR)$(PREFIX)/include/CMotiveAndObjective/"
	mkdir -p "$(DESTDIR)$(PREFIX)/share/doc/CMotiveAndObjective"
	cp LICENSE_1_0.txt docs/*.md "$(DESTDIR)$(PREFIX)/share/doc/CMotiveAndObjective/"
clean:
	rm -rf build build-sanitize
