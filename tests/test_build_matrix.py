#!/usr/bin/env python3
"""Run independent compiler optimization configurations against the full core."""
from pathlib import Path
import hashlib,json,os,shlex,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from emit_core import source_fingerprint
cc=shlex.split(os.environ.get('CC','cc'));results=[]
for opt in ['O0','O2','O3','Os']:
 build=ROOT/'build-matrix'/opt;build.mkdir(parents=True,exist_ok=True);library=build/'libCMotiveAndObjective-1.0.0.so'
 flags=['-'+opt,'-std=c11','-fstack-protector-strong','-Werror=implicit-function-declaration','-Werror=incompatible-pointer-types','-Werror=return-type']
 subprocess.run(cc+flags+['-fPIC','-shared',str(ROOT/'build/CMotiveAndObjective.c'),'-o',str(library),'-Wl,--no-undefined,-z,relro,-z,now,-z,noexecstack,-soname,libCMotiveAndObjective-1.0.0.so,--version-script='+str(ROOT/'build-support/exports.map')],check=True,timeout=120)
 subprocess.run([sys.executable,str(ROOT/'tests/test_core.py'),str(library),str(build/'test-result.json')],check=True,timeout=180)
 subprocess.run([sys.executable,str(ROOT/'tests/check_dependencies.py'),str(library)],check=True,timeout=30)
 for fixture in ['abi_smoke','rb_invariants','guard_pages','unicode_exhaustive']:
  binary=build/fixture
  includes=['-I',str(ROOT/'include'),'-I',str(ROOT/'build')]
  link=[str(library),'-Wl,-rpath,'+str(build)] if fixture=='abi_smoke' else []
  subprocess.run(cc+flags+includes+[str(ROOT/'tests'/(fixture+'.c')),'-o',str(binary)]+link,check=True,timeout=120)
  subprocess.run([str(binary)],check=True,timeout=180)
 report=json.loads((build/'test-result.json').read_text());results.append({'optimization':opt,'library_sha256':report['library_sha256'],'assertions':report['assertions'],'status':'PASS'})
 print('Optimization '+opt+': PASS',flush=True)
report={'status':'PASS','source_fingerprint':source_fingerprint(),'configurations':results,'compiler':subprocess.check_output(cc+['--version'],text=True).splitlines()[0]}
(ROOT/'evidence/build-matrix-report.json').write_text(json.dumps(report,indent=2)+'\n')
