#!/usr/bin/env python3
"""Linux/GCC: run the full Python behavioral suite against an instrumented .so."""
from pathlib import Path
import os,shlex,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
if not sys.platform.startswith('linux'):raise SystemExit('Full Python preload runner supports Linux/GCC only; use the native sanitizer tests on other hosts.')
cc=shlex.split(os.environ.get('CC','cc'))
runtime=subprocess.check_output(cc+['-print-file-name=libasan.so'],text=True).strip()
if not Path(runtime).is_file():raise SystemExit('GCC AddressSanitizer runtime not found')
env=os.environ.copy();env.update({'LD_PRELOAD':runtime,'ASAN_OPTIONS':'detect_leaks=0','UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'})
lib=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'build-sanitize/libCMotiveAndObjective-1.0.0.so').resolve()
report=lib.parent/'full-sanitized-test-result.json'
subprocess.run([sys.executable,str(ROOT/'tests/test_core.py'),str(lib),str(report)],env=env,check=True)
