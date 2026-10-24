from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
api=json.loads((ROOT/'api.json').read_text());vectors=json.loads((ROOT/'build/portable/vectors.json').read_text())
covered=set(vectors['methods'])
covered.update(c+'.'+m for c,m in re.findall(r'M\((\w+),(\w+)\)',(ROOT/'tests/portable_containers.h').read_text()))
expected={a['cls']+'.'+a['name'] for a in api}
assert expected<=covered,expected-covered
print('Portable method coverage: PASS;',len(expected),'methods')
