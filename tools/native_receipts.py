"""Validate source-bound native-host results; receipts are local evidence only."""
from pathlib import Path
import hashlib,json
from emit_core import source_fingerprint
from release_checks import tests_fingerprint
TESTS={'portable_shared','rb_invariants','unicode_exhaustive','guard_pages','core','metadata','reports'}
def validate(receipt,binary,system,machine):
 if receipt.get('status')!='PASS' or receipt.get('execution')!='native_host':raise ValueError('Native execution did not pass')
 if receipt.get('os')!=system or receipt.get('machine')!=machine:raise ValueError('Wrong native host tuple')
 if receipt.get('source_fingerprint')!=source_fingerprint() or receipt.get('tests_fingerprint')!=tests_fingerprint():raise ValueError('Stale native receipt')
 if set(receipt.get('tests',[]))!=TESTS or len(receipt.get('tests',[]))!=7:raise ValueError('Native tests missing')
 if receipt.get('library_sha256')!=hashlib.sha256(Path(binary).read_bytes()).hexdigest():raise ValueError('Native binary differs')
 root=Path(__file__).resolve().parents[1];expected=len(json.loads((root/'api.json').read_text()))
 if receipt.get('api_methods')!=expected or type(receipt.get('assertions')) is not int or receipt['assertions']<=0:raise ValueError('Native method coverage missing')
 return True
