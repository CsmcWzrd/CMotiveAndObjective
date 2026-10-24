#!/usr/bin/env python3
from pathlib import Path
import copy,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from release_checks import validate_report
binary=Path(sys.argv[1]);report=json.loads(Path(sys.argv[2]).read_text());validate_report(report,binary)
changes={'status':'FAIL','library_sha256':'0'*64,'source_fingerprint':'0'*64,'tests_fingerprint':'0'*64,'api_methods_exercised':0,'methods_exercised':report['methods_exercised'][:-1],'assertions':0}
for key,value in list(changes.items())+[('assertions','100')]:
 bad=copy.deepcopy(report);bad[key]=value
 try:validate_report(bad,binary)
 except ValueError:continue
 raise AssertionError('Release gate accepted '+key)
print('Test report gates: PASS; 8 invalid/stale/incomplete reports rejected')
