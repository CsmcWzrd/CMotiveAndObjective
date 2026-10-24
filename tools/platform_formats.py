"""Small binary format audits for produced candidates; standard library only."""
import struct
from pathlib import Path
def pe(path,expected):
 b=Path(path).read_bytes();assert b[:2]==b'MZ';pe=struct.unpack_from('<I',b,60)[0];assert b[pe:pe+4]==b'PE\0\0'
 machine,count,_,_,_,opt_size,flags=struct.unpack_from('<HHIIIHH',b,pe+4);assert machine==0x8664 and flags&0x2000
 opt=pe+24;assert struct.unpack_from('<H',b,opt)[0]==0x20b
 dll=struct.unpack_from('<H',b,opt+70)[0];assert dll&0x40 and dll&0x100
 sections=[]
 for i in range(count):
  o=opt+opt_size+40*i;vs,va,rs,rp=struct.unpack_from('<IIII',b,o+8);sf=struct.unpack_from('<I',b,o+36)[0];assert sf&0xa0000000!=0xa0000000;sections.append((va,max(vs,rs),rp,rs))
 def offset(rva):
  for va,size,rp,rs in sections:
   if va<=rva<va+size:assert rva-va<rs;return rp+rva-va
  raise ValueError('Unmapped RVA')
 def string(rva):
  p=offset(rva);return b[p:b.index(0,p)].decode('ascii')
 export_rva=struct.unpack_from('<I',b,opt+112)[0];e=offset(export_rva);n,names=struct.unpack_from('<II',b,e+24)[0],struct.unpack_from('<I',b,e+32)[0]
 exports={string(struct.unpack_from('<I',b,offset(names)+i*4)[0]) for i in range(n)};assert exports==set(expected),(exports-set(expected),set(expected)-exports)
 imports=[];rva=struct.unpack_from('<I',b,opt+120)[0]
 if rva:
  p=offset(rva)
  while any(b[p:p+20]):imports.append(string(struct.unpack_from('<I',b,p+12)[0]));p+=20
 assert all(x.lower() in {'kernel32.dll','ntdll.dll','msvcrt.dll','ucrtbase.dll'} or x.lower().startswith('api-ms-win-crt-') for x in imports),imports
 return {'format':'PE32+','exports':len(exports),'imports':imports,'aslr':True,'nx':True,'writable_executable_sections':False}
def macho(path,expected):
 b=Path(path).read_bytes();magic,cpu,sub,ft,ncmd,size,flags,res=struct.unpack_from('<8I',b);assert magic==0xfeedfacf and ft==6
 p=32;sym=None;imports=[];install=None
 for i in range(ncmd):
  cmd,n=struct.unpack_from('<II',b,p);assert n>=8 and p+n<=len(b)
  if cmd==2:sym=struct.unpack_from('<4I',b,p+8)
  if cmd in [0xc,0xd,0x80000018]:
   o=struct.unpack_from('<I',b,p+8)[0];s=b[p+o:b.index(0,p+o)].decode()
   if cmd==0xd:install=s
   else:imports.append(s)
  if cmd==0x19:
   maxprot,initprot=struct.unpack_from('<II',b,p+56);assert initprot&6!=6
  p+=n
 assert sym is not None;symoff,ns,stroff,strsize=sym;exports=set();undefined=set()
 for i in range(ns):
  idx,typ,sect,desc,value=struct.unpack_from('<IBBHQ',b,symoff+i*16)
  if not idx:continue
  name=b[stroff+idx:b.index(0,stroff+idx)].decode()
  if typ&0xe0 or not typ&1:continue
  if typ&0x0e==0:undefined.add(name)
  elif not typ&0x10:exports.add(name)
 markers={'___dso_handle','__mh_dylib_header'}
 assert exports-markers=={'_'+e for e in expected},(exports-markers-{'_'+e for e in expected},{'_'+e for e in expected}-exports)
 assert imports==['/usr/lib/libSystem.B.dylib'],imports
 allowed={'dyld_stub_binder','_calloc','_free','_memset','_memcpy','_memmove','___stack_chk_fail','___stack_chk_guard','_bzero','___bzero'}
 assert undefined<=allowed,undefined-allowed
 assert install=='@rpath/libCMotiveAndObjective-1.0.0.dylib'
 return {'format':'Mach-O64','cpu':cpu,'exports':len(exports-markers),'linker_markers':sorted(exports&markers),'imports':imports,'undefined':sorted(undefined),'install_name':install,'writable_executable_segments':False}
