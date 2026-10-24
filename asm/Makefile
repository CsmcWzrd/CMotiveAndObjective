# Standalone assembly build. No C compiler or C ABI shim is required.
PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
PYTHON ?= python3
ZIG ?= zig
BUILD ?= $(PROJECT_ROOT)/build-asm
.PHONY: all test native-test clean
all:
	$(PYTHON) "$(PROJECT_ROOT)/tools/build_asm.py" --zig "$(ZIG)" --output "$(BUILD)"
test: all
	$(PYTHON) "$(PROJECT_ROOT)/tests/test_asm.py" --build-dir "$(BUILD)"
native-test: all
	$(PYTHON) "$(PROJECT_ROOT)/tests/test_asm_native.py" --build-dir "$(BUILD)"
clean:
	rm -rf "$(BUILD)"
