from pathlib import Path
import json,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'docs/PRODUCTION-READINESS.json';original=path.read_bytes()
try:
 for readiness in [json.loads(original),{'production_ready':True,'blockers':[],'source_fingerprint':'0'*64}]:
  path.write_text(json.dumps(readiness))
  result=subprocess.run([sys.executable,str(ROOT/'tools/package.py'),'--output',str(ROOT/'build/blocked-production'),'--require-production'],capture_output=True,text=True)
  assert result.returncode and 'Production promotion blocked' in result.stderr
 print('Promotion guard: PASS; current blockers and edited ready flag cannot promote candidate')
finally:path.write_bytes(original)
