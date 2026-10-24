from pathlib import Path
import copy,hashlib,json,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from native_receipts import validate,TESTS
from emit_core import source_fingerprint
from release_checks import tests_fingerprint
with tempfile.TemporaryDirectory() as temp:
 binary=Path(temp)/'probe';binary.write_bytes(b'fixture')
 good={'status':'PASS','execution':'native_host','os':'FixtureOS','machine':'fixture64','source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'tests':sorted(TESTS),'library_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'api_methods':len(json.loads((ROOT/'api.json').read_text())),'assertions':1}
 assert validate(good,binary,'FixtureOS','fixture64')
 changes=[('status','FAIL'),('execution','cpu_emulation'),('os','Other'),('machine','Other'),('source_fingerprint','0'*64),('tests_fingerprint','0'*64),('tests',[]),('library_sha256','0'*64),('api_methods',0),('assertions',0)]
 for key,value in changes:
  bad=copy.deepcopy(good);bad[key]=value
  try:validate(bad,binary,'FixtureOS','fixture64')
  except ValueError:continue
  raise AssertionError('Bad native receipt accepted: '+key)
 print('Native receipt validation: PASS; 10 invalid/emulated/stale reports rejected')
