#!/usr/bin/env python3
"""Unix build checks: each header, ABI exports and shared-cleanup avoidance."""
from pathlib import Path
import argparse,json,os,shlex,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode:raise SystemExit('Command failed: '+repr(cmd)+'\n'+r.stderr[:4000])
    return r.stdout
parser=argparse.ArgumentParser();parser.add_argument('--compiler',required=True);parser.add_argument('--compiler-root',required=True);parser.add_argument('--library',required=True);parser.add_argument('--build-dir',required=True);args=parser.parse_args()
build=Path(args.build_dir).resolve();build.mkdir(parents=True,exist_ok=True)
runtime=Path(args.compiler_root).resolve()/'lib/Sys';cc=shlex.split(os.environ.get('CC','cc'))
headers=[]
for h in sorted((ROOT/'include/CMotiveAndObjective').rglob('*.HMOT')):
    output=build/('verify-'+h.stem+'.c')
    run([args.compiler,'-I',str(ROOT/'include'),'--emit-c',str(h),'-o',str(output)])
    run(cc+['-std=c11','-Werror=implicit-function-declaration','-Werror=incompatible-pointer-types','-I',str(runtime),'-c',str(output),'-o',str(output.with_suffix('.o'))])
    headers.append(str(h.relative_to(ROOT)))
library=Path(args.library).resolve()
flags=['-gU'] if sys.platform=='darwin' else ['-D','--defined-only']
listing=run(['nm']+flags+[str(library)])
actual={line.split()[-1].split('@')[0].lstrip('_') for line in listing.splitlines() if 'CMotiveAndObjective__' in line}
expected=set((ROOT/'build-support/exported-symbols.txt').read_text().splitlines())
if actual!=expected:raise SystemExit('ABI export allowlist differs: '+str((actual-expected,expected-actual)))
source=build/'verify-combined.c'
run([args.compiler,'-I',str(ROOT/'include'),'--emit-c',str(ROOT/'src/CMotiveAndObjective.CMOT'),'-o',str(source)])
if source.read_text().count('CMotive_Cleanup_Push(')!=1:raise SystemExit('Library methods introduce compiler global cleanup-stack writes')
result={'standalone_headers':len(headers),'abi_exports':len(expected),'global_cleanup_push_calls':0,'status':'PASS'}
(build/'verify-build.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
