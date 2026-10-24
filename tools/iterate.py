#!/usr/bin/env python3
"""Run one numbered hardening checkpoint. Stops on any failed check."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,shlex
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('number',type=int);p.add_argument('title');p.add_argument('--compiler-root',type=Path,required=True);p.add_argument('--extra',action='append',default=[]);a=p.parse_args()
out=ROOT.parent/'checkpoints'/f'iteration-{a.number:02d}';out.mkdir(parents=True,exist_ok=True)
(ROOT/'ITERATION').write_text(str(a.number)+'\n')
with (out/'checks.log').open('w') as log:
 subprocess.run([sys.executable,str(ROOT/'tools/sync_api.py')],stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run(['make','-f','Makefile.linux','-j2','CMOTIVE_ROOT='+str(a.compiler_root.resolve()),'test'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1800)
 for extra in a.extra:
  subprocess.run(shlex.split(extra),cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1800)
report=json.loads((ROOT/'build/test-result.json').read_text())
ledger=ROOT/'docs/PRODUCTION-ITERATIONS.json';rows=json.loads(ledger.read_text()) if ledger.exists() else []
rows=[r for r in rows if r['iteration']!=a.number]
entry={'iteration':a.number,'title':a.title,'status':'CHECKS_PASS',**report};rows.append(entry)
ledger.write_text(json.dumps(rows,indent=2)+'\n')
notes='# Automated production iterations\n\nEach numbered checkpoint passed GNU Make, the complete behavioral suite, API/provenance checks and the Linux dependency/profile audit. These are core-library checkpoints, not certification of the full compiler or Phobos.\n\n| Iteration | Change | Assertions | Methods |\n|---|---|---:|---:|\n'
notes+=''.join(f"| {r['iteration']} | {r['title']} | {r['assertions']:,} | {r['api_methods_exercised']} |\n" for r in rows)
(ROOT/'docs/PRODUCTION-ITERATIONS.md').write_text(notes)
readme=ROOT/'README.md';text=readme.read_text();text=__import__('re').sub(r'(# CMotiveAndObjective 1\.0\.0 — iteration )\d+',lambda m:m[1]+str(a.number),text);readme.write_text(text)
with (out/'package.log').open('w') as log:
 subprocess.run([sys.executable,str(ROOT/'tools/package.py'),'--output',str(out)],stdout=log,stderr=subprocess.STDOUT,check=True)
# Keep one complete source/binary ZIP per checkpoint; other formats are rebuilt
# for the final deliverable. This directory is outside the packaged source tree.
for name in ['CMotiveAndObjective-1.0.0-core.tar.gz','CMotiveAndObjective-1.0.0-assembly-runtime.zip','libCMotiveAndObjective-1.0.0.so','CMotiveAndObjective-1.0.0-VERIFICATION.md','CMotiveAndObjective-1.0.0-SHA256SUMS.txt']:
 (out/name).unlink()
entry['archive_sha256']=hashlib.sha256((out/'CMotiveAndObjective-1.0.0-core.zip').read_bytes()).hexdigest()
(out/'checkpoint.json').write_text(json.dumps(entry,indent=2)+'\n')
print(json.dumps({k:v for k,v in entry.items() if k!="methods_exercised"}),flush=True)
