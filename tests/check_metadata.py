#!/usr/bin/env python3
"""Check ABI compatibility, generated-file consistency and exact source provenance."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'tools/sync_api.py'),'--check'],check=True)
iteration2=json.loads((ROOT/'tests/iteration2-api-baseline.json').read_text())
current=json.loads((ROOT/'api.json').read_text());baseline=json.loads((ROOT/'tests/abi-1.0.0-baseline.json').read_text())
by_name={(a['cls'],a['name']):a for a in current}
for a in baseline + iteration2:
    if by_name.get((a['cls'],a['name']))!=a:raise SystemExit('ABI baseline changed: '+a['cls']+'.'+a['name'])
pins=json.loads((ROOT/'tools/source-pins.json').read_text())
for folder,extensions in [('src',{'.CMOT','.CMTV'}),('include/CMotiveAndObjective',{'.HMOT','.HMTV'})]:
    for path in (ROOT/folder).rglob('*'):
        if not path.is_file():continue
        if path.suffix.upper() not in extensions:raise SystemExit('Unexpected CMotive code extension: '+str(path))
        if 'NativeInclude' in path.read_text():raise SystemExit('Native implementation include in CMotive code: '+str(path))
for name,digest in pins.items():
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Pinned source changed: '+name)
inventory=json.loads((ROOT/'docs/phobos-inventory.json').read_text())
with zipfile.ZipFile(ROOT/'upstream/Phobos-reference.zip') as z:
    sources={n.split('/',1)[1]:z.read(n) for n in z.namelist() if n.endswith('.d')}
    if set(sources)!={r['path'] for r in inventory}:raise SystemExit('Inventory/source file set differs')
    for row in inventory:
        if hashlib.sha256(sources[row['path']]).hexdigest()!=row['sha256']:raise SystemExit('Inventory hash mismatch')
print(f'Metadata: PASS; {len(baseline)} original signatures retained; {len(current)} current methods; {len(inventory)} upstream files verified')

policy=json.loads((ROOT/'build-support/dependency-policy.json').read_text())
for cls in policy['retained_stl_classes']:
    if not any(a['cls']==cls for a in current):raise SystemExit('STL class removed: '+cls)
for row in inventory:
    if row['module'] in policy['excluded_modules'] and row['status']!='excluded-external-dependency':
        raise SystemExit('External wrapper is not excluded: '+row['module'])
print(f'Dependency policy: PASS; all {len(iteration2)} iteration-2 methods and STL classes retained')
