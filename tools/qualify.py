#!/usr/bin/env python3
"""Final implemented-core qualification. Never asserts full-product GA readiness."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
from emit_core import source_fingerprint
from release_checks import tests_fingerprint,validate_report
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--compiler-root',required=True,type=Path);p.add_argument('--cmake',required=True);p.add_argument('--ctest',required=True);p.add_argument('--autotools-env',required=True);p.add_argument('--autoreconf',required=True);a=p.parse_args()
def run(cmd):subprocess.run([str(x) for x in cmd],cwd=ROOT,check=True,timeout=600)
run(['make','-f','Makefile.linux','CMOTIVE_ROOT='+str(a.compiler_root),'sanitize-full'])
run([sys.executable,ROOT/'tests/verify_build.py','--compiler',a.compiler_root/'build/bin/cmotive','--compiler-root',a.compiler_root,'--library',ROOT/'build/libCMotiveAndObjective-1.0.0.so','--build-dir',ROOT/'build/verify'])
run([sys.executable,ROOT/'tests/test_build_matrix.py'])
run([sys.executable,ROOT/'tests/test_build_systems.py','--compiler-root',a.compiler_root,'--cmake',a.cmake,'--ctest',a.ctest,'--autotools-env',a.autotools_env,'--autoreconf',a.autoreconf])
run([sys.executable,ROOT/'tests/test_asm.py','--build-dir',ROOT/'build-asm'])
run([sys.executable,ROOT/'tests/test_asm_native.py','--build-dir',ROOT/'build-asm'])
report=json.loads((ROOT/'build/test-result.json').read_text());validate_report(report,ROOT/'build/libCMotiveAndObjective-1.0.0.so')
for filename in ['build-matrix-report.json','build-systems-report.json']:
 value=json.loads((ROOT/'evidence'/filename).read_text());assert value['status']=='PASS' and value['source_fingerprint']==source_fingerprint(),filename
headers=json.loads((ROOT/'build/verify/verify-build.json').read_text())
sanitized=json.loads((ROOT/'build-sanitize/full-sanitized-test-result.json').read_text());validate_report(sanitized,ROOT/'build-sanitize/libCMotiveAndObjective-1.0.0.so')
assembly=json.loads((ROOT/'build-asm/test-report.json').read_text());assert assembly['status']=='PASS'
import shutil
for source,target in [('build/test-result.json','core-test-report.json'),('build-sanitize/full-sanitized-test-result.json','sanitized-core-report.json'),('build/verify/verify-build.json','core-header-and-export-report.json'),('build/dependency-report.json','dependency-report.json'),('build-asm/test-report.json','asm-test-report.json'),('build-asm/native-test-report.json','asm-native-report.json')]:shutil.copy2(ROOT/source,ROOT/'evidence'/target)
blockers=[
 {'id':'NATIVE_FRONTEND','detail':'Pinned frontend emits C; CMO-REG-1 is not integrated into class calls or the allocator.'},
 {'id':'GENERIC_TEMPLATES','detail':'Arbitrary template instantiation is not supported by the pinned frontend; typed containers are adapted APIs.'},
 {'id':'PHOBOS_PARITY','detail':'The supplied 174-module snapshot is only partially ported. Remaining implementable modules and permitted OS services are documented.'},
 {'id':'PLATFORM_QUALIFICATION','detail':'Full core execution is verified on Linux x86_64 only; Windows/macOS and full ARM/x86 core qualification remain outstanding.'},
 {'id':'LIFETIME_AND_RACE_QUALIFICATION','detail':'Tracked ownership and concurrency tests pass, but LSan inspection is unavailable and a ThreadSanitizer pass is not claimed.'}]
readiness={'status':'NOT_GA','production_ready':False,'quality_level':'verified implemented-core candidate','iteration':23,'continuation_checkpoints':20,'source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'api_methods':len(json.loads((ROOT/'api.json').read_text())),'public_classes':27,'headers':headers['standalone_headers'],'exports':headers['abi_exports'],'behavioral_assertions':report['assertions'],'unicode_scalars':1112064,'native_unicode_checks':23365381,'hardware_guard_checks':3630,'blockers':blockers}
(ROOT/'docs/PRODUCTION-READINESS.json').write_text(json.dumps(readiness,indent=2)+'\n')
# Verify that the production gate refuses to relabel this candidate as GA.
probe=subprocess.run([sys.executable,str(ROOT/'tools/package.py'),'--output',str(ROOT.parent/'blocked-ga-probe'),'--require-production'],capture_output=True,text=True)
assert probe.returncode!=0 and 'Production promotion blocked' in probe.stderr,probe.stderr
components={'schema':'CMotive-component-inventory-1','runtime_dependencies':['OS C runtime; libc.so.6 on verified Linux'],'excluded_external_wrappers':['curl','ODBC','SQLite','zlib'],'licenses':{'maintained_library_and_tests':'BSL-1.0','pinned_compiler_and_original_allocator_definitions':'MIT'},'pinned_inputs':json.loads((ROOT/'tools/source-pins.json').read_text()),'test_only_tools':['Python standard library','Unicorn CPU emulator','pyelftools','Zig assembly build driver','GCC sanitizers'],'native_assembly_runtime_dependencies':[]}
(ROOT/'docs/COMPONENTS.json').write_text(json.dumps(components,indent=2)+'\n')
summary={'status':'PASS_FOR_IMPLEMENTED_CORE','production_ready':False,'source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'normal_binary_sha256':report['library_sha256'],'sanitized_binary_sha256':sanitized['library_sha256'],'normal_and_sanitized_assertions_each':report['assertions'],'headers':headers,'production_gate_rejection':'PASS'}
(ROOT/'evidence/final-qualification.json').write_text(json.dumps(summary,indent=2)+'\n')
verification=f'''# Verification — iteration 23 — 24 October 2026

Twenty continuation checkpoints (4–23) have been completed. The implemented core
is a verified candidate, **not a full-production/GA release**. Production promotion
is explicitly refused while PRODUCTION-READINESS.json lists outstanding blockers.
Version 1.0.0 remains the requested output filename/version.

## Current scope

27 public classes, 199 methods and 32 .HMOT headers (five internal helpers).
All 149 original methods and all original STL functionality remain. Four additional
typed containers provide HashMapI64, HashSetI64, MultiMapI64 and StackI64. New
algorithms include caller-workspace merge sort, checked sum, UTF-16 LE/BE,
UTF-8/scalar transcoding and strict I64/U64 text conversion in bases 2..36.
API-EXTENSIONS.md specifies capacities, error atomicity, lifetimes and complexity.
All maintained library algorithms use CMotive, with no third-party library wrapper.

The Linux ELF uses the pinned minimal C-emission compiler profile and system
calloc/free plus compiler/optimizer OS-runtime helpers. Its sole DT_NEEDED is
libc.so.6. External curl, ODBC, SQLite and zlib wrappers are excluded. The original
upstream/compiler ZIPs are provenance inputs, not linked library implementations.

## Executed checks

| Check | Result |
|---|---|
| Full behavioral suite | PASS: {report['assertions']:,} assertions, 199/199 methods |
| Same full suite with ASan/UBSan | PASS; detect_leaks=0, halt_on_error=1 |
| Exhaustive UTF-8 and UTF-16 LE/BE | PASS: 1,112,064 scalars, 23,365,381 native checks |
| Independent Unicode oracle | PASS: aggregate byte hashes match Python codecs |
| Gregorian cycle | PASS: 146,097 dates checked against Python datetime |
| Native hardware guard pages | PASS: 3,630 checks; source/output bounds and full hash tables |
| Owning containers | PASS: 52,000 RB invariant operations, destructor stress, 100 nth-allocation cut points, tracked allocations return to zero |
| Adversarial hashing | PASS: discovered collisions, tombstones, full tables and duplicate updates |
| Concurrency | PASS: 12 independent container workers, 100,872 checks; plus original stateless stress |
| Malformed codecs | PASS: 12,500 inputs, five seeds, independent strict oracles and failure output preservation |
| GCC optimization matrix | PASS: O0, O2, O3, Os; complete behavior and native fixtures per configuration |
| Strict warnings | PASS: implicit declarations, incompatible pointers and return types are errors |
| GNU Make / CMotive consumer | PASS, including all new classes |
| Fresh CMake / CTest | PASS: all 10 tests |
| Installed CMake package consumer | PASS |
| Autoconf/Automake check/install/distcheck | PASS |
| Installed CMotive consumers | PASS: CMake and Autotools installations; all headers byte-matched |
| Standalone headers / ABI | PASS: 32 headers, exact 253 exported API symbols |
| Linux dependency and ELF audit | PASS: target, SONAME, imports, exports, RELRO, NOW, non-executable stack, no writable executable segments or runtime search paths |
| Negative release fixtures | PASS: 15 profile/ELF rejection cases and eight invalid/stale behavioral reports |
| Production promotion guard | PASS: refuses GA promotion because blockers remain |

The normal suite uses independent Python arithmetic/codecs/container models.
Method-call coverage is measured; branch coverage and a complete security audit
are not claimed. Output spans must actually exist for their declared lengths.
Mutable shared containers require caller synchronization. Hashing is not designed
as collision-attack resistance; fixed capacities and worst-case costs are documented.

The normal and sanitized binary hashes are:

- Normal: {report['library_sha256']}
- ASan/UBSan: {sanitized['library_sha256']}

## Assembly layer

The nine unchanged CMO-REG-1 primitives have no C ABI wrappers or libc imports.
All six ELF CPU/endian modes pass 115,733 emulated checks: x86 LE, x86_64 LE,
ARM32 LE/BE8 and ARM64 LE/BE. The x86_64 freestanding assembly caller passes
natively; native ELF32 execution is unsupported by this host. ARM execution is
emulated, not physical-hardware qualification. x86 has no big-endian execution
mode; explicit BE data loads/stores are supported. COFF/Mach-O assembly adaptations
and direct compiler integration remain unfinished. These checks were rerun for
this final checkpoint; the packager also validates exact source/artifact hashes.

## Production limitations

The current frontend is a C-emission backend, with no arbitrary template
instantiation or direct CMO-REG-1 class-call integration. Full Phobos parity and
OS-service APIs are incomplete. Full Windows/macOS/ARM core execution remains
unverified; no DLL/dylib or ARM core production binary is fabricated. LSan cannot
inspect processes here, and no ThreadSanitizer pass is claimed. Tracked allocation
and concurrent tests support the tested paths, not global leak/race freedom.

Every checkpoint includes its full source/binary ZIP, test log and SHA-256 in the
continuation history. Final ZIP/TAR packaging is deterministic and the exact
release binary must match current source/test fingerprints and measured coverage.
All 174 supplied upstream file hashes and compiler/source pins remain verified.
'''
(ROOT/'docs/VERIFICATION.md').write_text(verification)
print(json.dumps(summary),flush=True)
