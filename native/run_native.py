#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from emit_core import source_fingerprint
from release_checks import tests_fingerprint,validate_report
p=argparse.ArgumentParser();p.add_argument('--cmake',default='cmake');p.add_argument('--ctest',default='ctest');a=p.parse_args()
manifest=json.loads((ROOT/'manifest.json').read_text());assert manifest['source_fingerprint']==source_fingerprint() and manifest['tests_fingerprint']==tests_fingerprint()
for name,digest in manifest['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
build=ROOT/'native-build'
subprocess.run([a.cmake,'-S',str(ROOT/'native'),'-B',str(build),'-DCMAKE_BUILD_TYPE=Release'],check=True)
subprocess.run([a.cmake,'--build',str(build),'--config','Release','-j2'],check=True)
subprocess.run([a.ctest,'--test-dir',str(build),'-C','Release','--output-on-failure'],check=True)
libs=list(build.rglob('CMotiveAndObjective-1.0.0.dll'))+list(build.rglob('libCMotiveAndObjective-1.0.0.so'))+list(build.rglob('libCMotiveAndObjective-1.0.0.dylib'));assert len(libs)==1
report=json.loads((build/'test-result.json').read_text());validate_report(report,libs[0])
receipt={'status':'PASS','execution':'native_host','os':platform.system(),'machine':platform.machine(),'source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'library_sha256':hashlib.sha256(libs[0].read_bytes()).hexdigest(),'api_methods':report['api_methods_exercised'],'assertions':report['assertions'],'tests':['portable_shared','rb_invariants','unicode_exhaustive','guard_pages','core','metadata','reports'],'attestation':'local runner report, not cryptographic host attestation'}
(build/'native-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
