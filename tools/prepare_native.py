#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,re,shutil
from emit_core import source_fingerprint
from release_checks import tests_fingerprint
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
for folder in ['src','include','tools','tests','native','docs','build-support','upstream','toolchain']:
 shutil.copytree(ROOT/folder,out/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for name in ['VERSION','ITERATION','api.json','LICENSE_1_0.txt','README.md']:shutil.copy2(ROOT/name,out/name)
gen=out/'prebuilt/generated';gen.mkdir(parents=True,exist_ok=True)
for name in ['CMotiveAndObjective.c']:shutil.copy2(ROOT/'build'/name,gen/name)
for name in ['portable_replay.c','vectors.json']:shutil.copy2(ROOT/'build/portable'/name,gen/name)
expected=(ROOT/'build-support/exported-symbols.txt').read_text().splitlines();path=gen/'CMotiveAndObjective.c';content=path.read_text();pattern=r'\b((?:void\s*\*|void|int32_t|uint32_t|int64_t|uint64_t)\s*(?:'+'|'.join(map(re.escape,expected))+r')\([^;\n{}]*\);)'
content,n=re.subn(pattern,r'CMO_PUBLIC \1',content,flags=re.M);assert n==len(expected)
macro='#if defined(__GNUC__) && !defined(_WIN32)\n#define CMO_PUBLIC __attribute__((visibility("default")))\n#else\n#define CMO_PUBLIC\n#endif\n'
path.write_text(macro+content)
manifest={'source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'files':{p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file() and p.name!='manifest.json' and 'native-build' not in p.parts and '__pycache__' not in p.parts}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Prepared source-bound native host kit:',out)
