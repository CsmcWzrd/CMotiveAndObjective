#!/usr/bin/env python3
"""Reproducible release archives with tested-binary and provenance gates."""
from pathlib import Path
import argparse,gzip,hashlib,io,json,shutil,subprocess,sys,tarfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--binary',type=Path,default=ROOT/'build/libCMotiveAndObjective-1.0.0.so')
parser.add_argument('--test-report',type=Path,default=ROOT/'build/test-result.json')
parser.add_argument('--asm-build',type=Path,default=ROOT/'build-asm');args=parser.parse_args()
subprocess.run([sys.executable,str(ROOT/'tests/check_metadata.py')],check=True)
binary=args.binary.resolve();report=json.loads(args.test_report.read_text());api=json.loads((ROOT/'api.json').read_text())
digest=hashlib.sha256(binary.read_bytes()).hexdigest()
if not (report['status']=='PASS' and report['api_methods_exercised']==len(api) and report['library_sha256']==digest):
    raise SystemExit('Binary must match a passing full-method behavioral report')
if binary.name!='libCMotiveAndObjective-1.0.0.so' or binary.read_bytes()[:4]!=b'\x7fELF':
    raise SystemExit('This release packager currently expects the Linux ELF library')
names=['README.md','LICENSE_1_0.txt','VERSION','ITERATION','api.json','Makefile','Makefile.linux','Makefile.mac','Makefile.windows','Makefile.am','configure.ac','CMakeLists.txt']
dirs=['src','include','tools','tests','docs','cmake','build-support','upstream','toolchain','evidence','.github','asm']
payload={n:(ROOT/n).read_bytes() for n in names}
for d in dirs:
    for f in sorted((ROOT/d).rglob('*')):
        if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc':payload[f.relative_to(ROOT).as_posix()]=f.read_bytes()
payload['prebuilt/linux-x86_64/'+binary.name]=binary.read_bytes()
assembly=json.loads((ROOT/'asm/contract.json').read_text())
asm_build=json.loads((args.asm_build/'build-report.json').read_text())
asm_tests=json.loads((args.asm_build/'test-report.json').read_text())
if {r['target'] for r in asm_build['targets']}!={t['name'] for t in assembly['targets']}:raise SystemExit('Assembly build target set differs')
if asm_build['contract_sha256']!=hashlib.sha256((ROOT/'asm/contract.json').read_bytes()).hexdigest():raise SystemExit('Assembly contract differs from tested build')
if asm_tests['status']!='PASS' or {r['target'] for r in asm_tests['targets']}!={t['name'] for t in assembly['targets']}:raise SystemExit('Assembly targets are not fully tested')
asm_payload={}
tested={r['target']:r for r in asm_tests['targets']}
for target,built in zip(assembly['targets'],asm_build['targets']):
    name=target['name']
    if built['target']!=name or hashlib.sha256((ROOT/'asm'/target['source']/'primitives.s').read_bytes()).hexdigest()!=built['source_sha256']:raise SystemExit('Assembly source differs from tested build')
    for file,key in [('primitives.o','object_sha256'),('libCMotiveAndObjectiveRuntime-1.0.0.a','archive_sha256')]:
        data=(args.asm_build/name/file).read_bytes()
        if hashlib.sha256(data).hexdigest()!=built[key]:raise SystemExit('Assembly artifact differs: '+name+'/'+file)
        asm_payload['prebuilt/asm/'+name+'/'+file]=data
    if hashlib.sha256((args.asm_build/name/'primitives.elf').read_bytes()).hexdigest()!=tested[name]['elf_sha256']:raise SystemExit('Tested assembly image differs')
payload.update(asm_payload)
manifest=''.join(hashlib.sha256(data).hexdigest()+'  '+name+'\n' for name,data in sorted(payload.items()))
payload['SHA256SUMS.txt']=manifest.encode()
out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);base='CMotiveAndObjective-1.0.0-core'
def mode(n):return 0o755 if n.endswith(('.py','.sh','.so')) else 0o644
with zipfile.ZipFile(out/(base+'.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,data in sorted(payload.items()):
        info=zipfile.ZipInfo(base+'/'+name,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        info.create_system=3;info.external_attr=mode(name)<<16;z.writestr(info,data)
with open(out/(base+'.tar.gz'),'wb') as file:
    with gzip.GzipFile(filename='',mode='wb',fileobj=file,mtime=0) as gz:
        with tarfile.open(fileobj=gz,mode='w') as tar:
            for name,data in sorted(payload.items()):
                info=tarfile.TarInfo(base+'/'+name);info.size=len(data);info.mode=mode(name);info.mtime=0;info.uid=info.gid=0
                tar.addfile(info,io.BytesIO(data))
with zipfile.ZipFile(out/(base+'.zip')) as z:
    if z.testzip() is not None:raise SystemExit('ZIP integrity failure')
    for name,data in payload.items():
        if z.read(base+'/'+name)!=data:raise SystemExit('ZIP payload differs: '+name)
with tarfile.open(out/(base+'.tar.gz')) as tar:
    for name,data in payload.items():
        if tar.extractfile(base+'/'+name).read()!=data:raise SystemExit('TAR payload differs: '+name)
asm_prefix='CMotiveAndObjective-1.0.0-assembly-runtime'
standalone={n:data for n,data in payload.items() if n.startswith('asm/')}
for n in ['tools/build_asm.py','tests/test_asm.py','tests/test_asm_native.py','LICENSE_1_0.txt']:
    standalone[n]=(ROOT/n).read_bytes()
standalone['README.md']=b'# Standalone assembly runtime package\n\nThis package contains the custom-register assembly primitives only.\nFull CMotive core sources are provided separately. See asm/README.md.\n'
standalone.update(asm_payload)
for n in ['build-report.json','test-report.json','native-test-report.json']:standalone['evidence/'+n]=(args.asm_build/n).read_bytes()
standalone['SHA256SUMS.txt']=''.join(hashlib.sha256(d).hexdigest()+'  '+n+'\n' for n,d in sorted(standalone.items())).encode()
with zipfile.ZipFile(out/(asm_prefix+'.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n,d in sorted(standalone.items()):
        info=zipfile.ZipInfo(asm_prefix+'/'+n,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=mode(n)<<16;z.writestr(info,d)
with zipfile.ZipFile(out/(asm_prefix+'.zip')) as z:
    if z.testzip() is not None:raise SystemExit('Assembly ZIP integrity failure')
    for n,d in standalone.items():
        if z.read(asm_prefix+'/'+n)!=d:raise SystemExit('Assembly ZIP payload differs')
shutil.copy2(binary,out/binary.name)
shutil.copy2(ROOT/'docs/VERIFICATION.md',out/'CMotiveAndObjective-1.0.0-VERIFICATION.md')
published=[base+'.zip',base+'.tar.gz',asm_prefix+'.zip',binary.name,'CMotiveAndObjective-1.0.0-VERIFICATION.md']
(out/'CMotiveAndObjective-1.0.0-SHA256SUMS.txt').write_text(''.join(hashlib.sha256((out/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in published))
print(json.dumps({'status':'PASS','archive_files':len(payload),'library_sha256':digest,'outputs':published},indent=2))
