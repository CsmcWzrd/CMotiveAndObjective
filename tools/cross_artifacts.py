#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,re,struct,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from emit_core import source_fingerprint
from release_checks import tests_fingerprint
from platform_formats import pe,macho
p=argparse.ArgumentParser();p.add_argument('--zig',required=True);p.add_argument('--mode',choices=['linux','windows','macos'],required=True);a=p.parse_args()
expected=(ROOT/'build-support/exported-symbols.txt').read_text().splitlines();rows=[]
source=ROOT/'build/CMotiveAndObjective.c'
def build(name,triple,suffix,flags,content=None):
 out=ROOT/'build-platform'/name;out.mkdir(parents=True,exist_ok=True)
 src=source
 if content is not None:src=out/'visibility.c';src.write_text(content)
 lib=out/('CMotiveAndObjective-1.0.0.dll' if suffix=='dll' else 'libCMotiveAndObjective-1.0.0.'+suffix)
 subprocess.run([a.zig,'cc','-target',triple,'-O2','-std=c11',str(src),*map(str,flags),'-o',str(lib)],check=True,timeout=180)
 return lib
if a.mode=='linux':
 from elftools.elf.elffile import ELFFile
 targets={'x86-le':('x86-linux-musl',32,True),'x86_64-le':('x86_64-linux-musl',64,True),'arm32-le':('arm-linux-musleabihf',32,True),'arm32-be':('armeb-linux-musleabi',32,False),'arm64-le':('aarch64-linux-musl',64,True),'arm64-be':('aarch64_be-linux-musl',64,False)}
 for name,(triple,bits,little) in targets.items():
  lib=build(name,triple,'so',['-fPIC','-shared','-Wl,-soname,libCMotiveAndObjective-1.0.0.so','-Wl,--version-script='+str(ROOT/'build-support/exports.map'),'-Wl,-z,relro,-z,now,-z,noexecstack'])
  with lib.open('rb') as f:
   elf=ELFFile(f);assert elf.elfclass==bits and elf.little_endian==little
   exports={s.name for s in elf.get_section_by_name('.dynsym').iter_symbols() if s['st_shndx'] not in ['SHN_UNDEF','SHN_ABS'] and s['st_info']['bind'] in ['STB_GLOBAL','STB_WEAK']};assert exports==set(expected)
   tags=list(elf.get_section_by_name('.dynamic').iter_tags());needed=[t.needed for t in tags if t.entry.d_tag=='DT_NEEDED'];assert set(needed)<={'libc.so','libc.so.6'}
   assert [t.soname for t in tags if t.entry.d_tag=='DT_SONAME']==['libCMotiveAndObjective-1.0.0.so'];assert not [t for t in tags if t.entry.d_tag in ['DT_RPATH','DT_RUNPATH']]
   assert any(s['p_type']=='PT_GNU_RELRO' for s in elf.iter_segments());assert all(s['p_flags']&3!=3 for s in elf.iter_segments() if s['p_type']=='PT_LOAD');assert all(not s['p_flags']&1 for s in elf.iter_segments() if s['p_type']=='PT_GNU_STACK')
   assert any(t.entry.d_tag=='DT_BIND_NOW' or (t.entry.d_tag=='DT_FLAGS' and t.entry.d_val&8) or (t.entry.d_tag=='DT_FLAGS_1' and t.entry.d_val&1) for t in tags)
  rows.append({'target':name,'path':str(lib.relative_to(ROOT)),'sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'exports':len(exports),'imports':needed,'status':'CROSS_BUILD_AUDIT_PASS','native_os_execution':False});print(name+': ELF audit PASS',flush=True)
elif a.mode=='windows':
 lib=build('windows-x86_64','x86_64-windows-gnu','dll',['-shared',ROOT/'build-support/exports.def','-Wl,--dynamicbase,--nxcompat','-Wl,--out-implib,'+str(ROOT/'build-platform/windows-x86_64/CMotiveAndObjective.lib')]);audit=pe(lib,expected)
 rows.append({'target':'windows-x86_64','path':str(lib.relative_to(ROOT)),'sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'audit':audit,'status':'CROSS_BUILD_AUDIT_PASS','native_os_execution':False});print(json.dumps(audit),flush=True)
else:
 content=source.read_text();pattern=r'\b((?:void\s*\*|void|int32_t|uint32_t|int64_t|uint64_t)\s*(?:'+ '|'.join(map(re.escape,expected))+r')\([^;\n{}]*\);)'
 content,n=re.subn(pattern,r'__attribute__((visibility("default"))) \1',content,flags=re.M);assert n==len(expected),n
 libs=[]
 for name,triple,cpu in [('macos-x86_64','x86_64-macos-none',0x1000007),('macos-arm64','aarch64-macos-none',0x100000c)]:
  lib=build(name,triple,'dylib',['-dynamiclib','-fPIC','-fvisibility=hidden','-mmacosx-version-min=15.0','-Wl,-install_name,@rpath/libCMotiveAndObjective-1.0.0.dylib'],content);audit=macho(lib,expected);assert audit['cpu']==cpu
  rows.append({'target':name,'path':str(lib.relative_to(ROOT)),'sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'audit':audit,'status':'CROSS_BUILD_AUDIT_PASS','native_os_execution':False});libs.append((cpu,3 if cpu==0x1000007 else 0,lib.read_bytes()));print(name+': Mach-O audit PASS',flush=True)
 align=16384;data=bytearray(align);struct.pack_into('>II',data,0,0xcafebabe,2);slices=[]
 for i,(cpu,sub,body) in enumerate(libs):
  offset=(len(data)+align-1)&~(align-1);data+=bytes(offset-len(data));data+=body;struct.pack_into('>5I',data,8+i*20,cpu,sub,offset,len(body),14);slices.append((offset,body))
 out=ROOT/'build-platform/macos-universal';out.mkdir(exist_ok=True);lib=out/'libCMotiveAndObjective-1.0.0.dylib';lib.write_bytes(data)
 assert all(lib.read_bytes()[o:o+len(b)]==b for o,b in slices)
 rows.append({'target':'macos-universal','path':str(lib.relative_to(ROOT)),'sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'status':'FAT_CONTAINER_VERIFIED','native_os_execution':False})
report={'status':'CROSS_BUILD_AUDIT_PASS','source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'targets':rows}
(ROOT/('evidence/cross-'+a.mode+'-report.json')).write_text(json.dumps(report,indent=2)+'\n')
