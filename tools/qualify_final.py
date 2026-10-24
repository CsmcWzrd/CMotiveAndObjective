#!/usr/bin/env python3
# Revalidate final bytes; never infer native execution from cross builds.
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
from emit_core import source_fingerprint
from release_checks import tests_fingerprint,validate_report
p=argparse.ArgumentParser();p.add_argument('--compiler-root',required=True,type=Path);p.add_argument('--zig',required=True);p.add_argument('--cmake',required=True);p.add_argument('--ctest',required=True);p.add_argument('--autoreconf',required=True);p.add_argument('--autotools-env',required=True);a=p.parse_args()
def run(cmd):subprocess.run([str(x) for x in cmd],cwd=ROOT,check=True,timeout=600)
run(['make','-f','Makefile.linux','CMOTIVE_ROOT='+str(a.compiler_root),'sanitize-full'])
run([sys.executable,ROOT/'tests/verify_build.py','--compiler',a.compiler_root/'build/bin/cmotive','--compiler-root',a.compiler_root,'--library',ROOT/'build/libCMotiveAndObjective-1.0.0.so','--build-dir',ROOT/'build/verify'])
run([sys.executable,ROOT/'tests/test_build_matrix.py'])
run([sys.executable,ROOT/'tests/test_build_systems.py','--compiler-root',a.compiler_root,'--cmake',a.cmake,'--ctest',a.ctest,'--autoreconf',a.autoreconf,'--autotools-env',a.autotools_env])
run([sys.executable,ROOT/'tests/test_asm.py','--build-dir',ROOT/'build-asm']);run([sys.executable,ROOT/'tests/test_asm_native.py','--build-dir',ROOT/'build-asm'])
run([sys.executable,ROOT/'tools/portable.py']);run([sys.executable,ROOT/'tools/check_portable_coverage.py'])
run([sys.executable,ROOT/'tools/cross_cpu.py','--zig',a.zig])
for mode in ['linux','windows','macos']:run([sys.executable,ROOT/'tools/cross_artifacts.py','--zig',a.zig,'--mode',mode])
kit=ROOT.parent/'native-kit43';run([sys.executable,ROOT/'tools/prepare_native.py','--output',kit]);run([sys.executable,kit/'native/run_native.py','--cmake',a.cmake,'--ctest',a.ctest])
report=json.loads((ROOT/'build/test-result.json').read_text());validate_report(report,ROOT/'build/libCMotiveAndObjective-1.0.0.so')
san=json.loads((ROOT/'build-sanitize/full-sanitized-test-result.json').read_text());validate_report(san,ROOT/'build-sanitize/libCMotiveAndObjective-1.0.0.so')
api=json.loads((ROOT/'api.json').read_text());headers=json.loads((ROOT/'build/verify/verify-build.json').read_text())
for src,dst in [('build/test-result.json','core-test-report.json'),('build-sanitize/full-sanitized-test-result.json','sanitized-core-report.json'),('build/verify/verify-build.json','core-header-and-export-report.json'),('build-asm/test-report.json','asm-test-report.json'),('build-asm/native-test-report.json','asm-native-report.json')]:shutil.copy2(ROOT/src,ROOT/'evidence'/dst)
shutil.copy2(kit/'native-build/native-receipt.json',ROOT/'evidence/native-linux-x86_64-receipt.json')
readiness=json.loads((ROOT/'docs/PRODUCTION-READINESS.json').read_text());readiness.update({'status':'NOT_GA','production_ready':False,'iteration':43,'continuation_checkpoints':20,'source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'public_classes':len({v['cls'] for v in api}),'api_methods':len(api),'headers':len(list((ROOT/'include/CMotiveAndObjective').rglob('*.HMOT'))),'exports':len((ROOT/'build-support/exported-symbols.txt').read_text().splitlines()),'behavioral_assertions':report['assertions'],'cross_execution':'six compiled-core CPU modes, simulated allocator; not native OS','native_qualified_hosts':['Linux x86_64'],'outstanding_native_hosts':['Windows x86_64','macOS x86_64','macOS ARM64','Linux ARM32','Linux ARM64']})
for b in readiness['blockers']:
 if b['id']=='PLATFORM_QUALIFICATION':b['detail']='Windows/macOS libraries cross-built and audited; compiled core replay runs in six CPU modes with a simulated allocator. Native Windows/macOS/ARM host tests remain required.'
(ROOT/'docs/PRODUCTION-READINESS.json').write_text(json.dumps(readiness,indent=2)+'\n')
verification=f'''# Verification — iteration 43

Twenty reconstructed checkpoints (24–43) passed sequentially. Each completed
checkpoint has a saved full-source ZIP. These are implemented-core checkpoints;
full-production promotion remains blocked. Artifact version remains 1.0.0.

Scope: {readiness['public_classes']} public classes, {len(api)} methods,
{readiness['headers']} maintained .HMOT headers and {readiness['exports']} public
ABI exports. All earlier 199 methods and typed STL classes remain. Restored
contracts are in RESTORED-APIS.md. Sources use .CMOT and headers use .HMOT.

| Check | Final result |
|---|---|
| Independent Python behavioral suite | PASS, {report['assertions']:,} assertions, {len(api)}/{len(api)} methods |
| ASan/UBSan full suite and native fixtures | PASS; detect_leaks=0; no LSan/TSan certification |
| GCC O0/O2/O3/Os matrix | PASS, full suite and native fixtures at each level |
| Unicode native fixture | PASS, 1,112,064 scalars and 23,365,381 checks |
| Ownership/RB invariants | PASS, destructor stress and allocation-failure sweep |
| Guard pages | PASS, 3,630 hardware checks on Linux |
| CMake / installed consumer | PASS, 10 CTests and installed consumer |
| Autoconf/Automake | PASS, check/install/distcheck and installed CMotive consumers |
| Standalone headers/export audit | PASS, exact public export set and preserved baseline |
| Portable replay | PASS, all 227 methods via scalar capture and stateful models; static and real Linux shared library |
| x86/x86_64/ARM32/ARM64 compiled core | CPU-emulation PASS; ARM LE and BE included, simulated allocator, no guest OS claim |
| Linux six-target shared libraries | CROSS_BUILD_AUDIT_PASS; ELF target/exports/dependencies/hardening |
| Windows x86_64 DLL | CROSS_BUILD_AUDIT_PASS; PE exports/OS imports/ASLR/NX; native execution pending |
| macOS x86_64/ARM64 dylibs | CROSS_BUILD_AUDIT_PASS; Mach-O exports/libSystem/install name; native execution pending |
| Universal dylib | Thin slices byte-matched within fat container; native execution pending |
| Native-host kit | Linux x86_64 PASS, seven tests; Windows/macOS/ARM receipts pending |
| Custom-register assembly | PASS, 115,733 checks across six CPU modes; x86_64 native freestanding PASS |
| Release gates | Stale/incomplete reports rejected; edited ready flag cannot promote current backend |

The sole verified Linux core dependency is the OS C runtime. The Windows DLL uses
OS Kernel32/UCRT imports; macOS dylibs use libSystem. No curl/ODBC/SQLite/zlib
wrappers were added. Test-only cross tools and emulators are not library runtime
dependencies. Test allocator simulation is restricted to CPU replay images.

The pinned compiler emits C. The custom CMO-REG-1 assembly primitives have no C
wrappers, but are not integrated into class calls or the allocator. Generic
compiler templates and complete Phobos parity remain incomplete. The code is a
verified candidate for its implemented scope, not certified full production.

Source fingerprint: {source_fingerprint()}
Tests fingerprint: {tests_fingerprint()}
Linux library SHA256: {report['library_sha256']}
Sanitized library SHA256: {san['library_sha256']}
'''
(ROOT/'docs/VERIFICATION.md').write_text(verification)
for name in ['cross-cpu-report.json','cross-linux-report.json','cross-windows-report.json','cross-macos-report.json','portable-replay.json']:
 r=json.loads((ROOT/'evidence'/name).read_text())
 if 'source_fingerprint' in r:assert r['source_fingerprint']==source_fingerprint() and r['tests_fingerprint']==tests_fingerprint(),name
 else:assert all(v['source_fingerprint']==source_fingerprint() and v['tests_fingerprint']==tests_fingerprint() for v in r['targets']),name
# Refresh narrative docs in the kit; record revised hashes without including build outputs.
for f in (ROOT/'docs').iterdir():
 if f.is_file():shutil.copy2(f,kit/'docs'/f.name)
manifest=json.loads((kit/'manifest.json').read_text());manifest['files']={p.relative_to(kit).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(kit.rglob('*')) if p.is_file() and p.name!='manifest.json' and 'native-build' not in p.parts and '__pycache__' not in p.parts};(kit/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
run([sys.executable,ROOT/'tests/test_production_promotion.py']);run([sys.executable,ROOT/'tests/test_native_receipts.py'])
print('FINAL IMPLEMENTED-CORE QUALIFICATION PASS; full production remains blocked',flush=True)
