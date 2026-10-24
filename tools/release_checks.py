"""Release report freshness and method coverage checks; standard library only."""
from pathlib import Path
import hashlib,json
from emit_core import source_fingerprint
ROOT=Path(__file__).resolve().parents[1]
def tests_fingerprint():
    paths=[ROOT/'tools/release_checks.py',ROOT/'tools/emit_core.py']
    paths += [p for p in (ROOT/'tests').rglob('*') if p.is_file() and p.suffix in {'.py','.c','.CMOT','.json'}]
    h=hashlib.sha256()
    for p in sorted(paths):
        name=p.relative_to(ROOT).as_posix().encode();data=p.read_bytes()
        h.update(len(name).to_bytes(8,'big')+name+len(data).to_bytes(8,'big')+data)
    return h.hexdigest()
def validate_report(report,binary):
    expected={a['cls']+'.'+a['name'] for a in json.loads((ROOT/'api.json').read_text())}
    if report.get('status')!='PASS':raise ValueError('Behavioral suite did not pass')
    if report.get('library_sha256')!=hashlib.sha256(binary.read_bytes()).hexdigest():raise ValueError('Tested binary differs')
    if report.get('source_fingerprint')!=source_fingerprint():raise ValueError('Test report source is stale')
    if report.get('tests_fingerprint')!=tests_fingerprint():raise ValueError('Test report predates current tests')
    if report.get('api_methods_exercised')!=len(expected) or set(report.get('methods_exercised',[]))!=expected:raise ValueError('Full method coverage is missing')
    if type(report.get('assertions')) is not int or report['assertions']<=0:raise ValueError('Missing assertion count')
