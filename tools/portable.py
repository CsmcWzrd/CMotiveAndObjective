#!/usr/bin/env python3
from pathlib import Path
import json,os,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from emit_core import source_fingerprint
from release_checks import tests_fingerprint
out=ROOT/'build/portable';out.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['CMO_RECORD_VECTORS']=str(out)
subprocess.run([sys.executable,str(ROOT/'tests/test_core.py'),str(ROOT/'build/libCMotiveAndObjective-1.0.0.so'),str(ROOT/'build/test-result.json')],env=env,check=True)
flags=['-DCMO_CONTAINER_TEST'] if (ROOT/'tests/portable_containers.h').exists() else []
results={}
for name,extra in [('static',[]),('shared',['-DCMO_DYNAMIC_TEST',str(ROOT/'build/libCMotiveAndObjective-1.0.0.so'),'-Wl,-rpath,'+str(ROOT/'build')])]:
 exe=out/('replay-'+name)
 subprocess.run(['cc','-O2','-std=c11','-pedantic-errors','-I'+str(ROOT/'build'),'-I'+str(out),'-I'+str(ROOT/'tests'),'-I'+str(ROOT/'include'),*flags,str(ROOT/'tests/replay_host.c'),*extra,'-o',str(exe)],check=True)
 results[name]=subprocess.check_output([str(exe)],text=True).strip()
report={'status':'PASS','source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'results':results,'vectors':json.loads((out/'vectors.json').read_text())}
(ROOT/'evidence/portable-replay.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
