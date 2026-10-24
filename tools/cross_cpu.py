#!/usr/bin/env python3
"""Execute actual compiled core bodies with simulated allocator, not an OS claim."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from emit_core import source_fingerprint
from release_checks import tests_fingerprint
TARGETS={'x86-le':('x86-linux-musl','x86',32,False),'x86_64-le':('x86_64-linux-musl','x86',64,False),'arm32-le':('arm-linux-musleabihf','arm',32,False),'arm32-be':('armeb-linux-musleabi','arm',32,True),'arm64-le':('aarch64-linux-musl','aarch64',64,False),'arm64-be':('aarch64_be-linux-musl','aarch64',64,True)}
def execute(path,family,bits,big):
 import unicorn as U
 import unicorn.x86_const as X
 import unicorn.arm_const as A
 import unicorn.arm64_const as B
 from elftools.elf.elffile import ELFFile
 if family=='x86':uc=U.Uc(U.UC_ARCH_X86,U.UC_MODE_64 if bits==64 else U.UC_MODE_32);sp=X.UC_X86_REG_RSP if bits==64 else X.UC_X86_REG_ESP
 elif family=='arm':
  uc=U.Uc(U.UC_ARCH_ARM,U.UC_MODE_ARM|(U.UC_MODE_ARMBE8 if big else U.UC_MODE_LITTLE_ENDIAN));sp=A.UC_ARM_REG_SP
  uc.reg_write(A.UC_ARM_REG_C1_C0_2,uc.reg_read(A.UC_ARM_REG_C1_C0_2)|(15<<20));uc.reg_write(A.UC_ARM_REG_FPEXC,1<<30)
 else:
  uc=U.Uc(U.UC_ARCH_ARM64,U.UC_MODE_BIG_ENDIAN if big else U.UC_MODE_LITTLE_ENDIAN);sp=B.UC_ARM64_REG_SP;uc.reg_write(B.UC_ARM64_REG_CPACR_EL1,3<<20)
 with path.open('rb') as f:
  elf=ELFFile(f);assert elf.elfclass==bits and elf.little_endian!=big
  assert not elf.get_section_by_name('.dynamic')
  syms={s.name:s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols()}
  assert not [s.name for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name and s['st_shndx']=='SHN_UNDEF']
  pages={};segments=[]
  for s in elf.iter_segments():
   if s['p_type']!='PT_LOAD':continue
   start=s['p_vaddr'];end=start+s['p_memsz'];flags=s['p_flags'];perm=(U.UC_PROT_READ if flags&4 else 0)|(U.UC_PROT_WRITE if flags&2 else 0)|(U.UC_PROT_EXEC if flags&1 else 0)
   assert perm&(U.UC_PROT_WRITE|U.UC_PROT_EXEC)!=(U.UC_PROT_WRITE|U.UC_PROT_EXEC)
   for page in range(start&~4095,(end+4095)&~4095,4096):pages[page]=pages.get(page,0)|perm
   segments.append((start,s.data()))
  for page in pages:uc.mem_map(page,4096)
  for start,data in segments:uc.mem_write(start,data)
  for page,perm in pages.items():uc.mem_protect(page,4096,perm)
  entry=syms['cmo_entry'];fail=syms['cmo_fail'];finish=syms['cmo_finish'];counter=syms['cmo_checks'];assert fail!=finish
 stack=0x60000000;uc.mem_map(stack,8388608,U.UC_PROT_READ|U.UC_PROT_WRITE);uc.reg_write(sp,stack+8388592-(bits//8 if family=='x86' else 0))
 outcome=[]
 def stop(machine,address,size,user):
  outcome.append('PASS' if address==finish else 'FAIL');machine.emu_stop()
 uc.hook_add(U.UC_HOOK_CODE,stop,begin=finish,end=finish);uc.hook_add(U.UC_HOOK_CODE,stop,begin=fail,end=fail)
 uc.emu_start(entry,0,timeout=45000000,count=300000000)
 assert outcome==['PASS'],outcome
 checks=int.from_bytes(uc.mem_read(counter,8),'big' if big else 'little');assert checks>0
 return checks
p=argparse.ArgumentParser();p.add_argument('--zig',required=True);p.add_argument('--targets',nargs='+',choices=TARGETS,default=list(TARGETS));a=p.parse_args()
rows=[]
for name in a.targets:
 triple,family,bits,big=TARGETS[name];out=ROOT/'build-platform'/name;out.mkdir(parents=True,exist_ok=True);exe=out/'portable.elf'
 cmd=[a.zig,'cc','-target',triple,'-O0','-fno-sanitize=all','-std=c11','-fno-stack-protector','-ffreestanding','-fno-builtin','-nostdlib','-static','-rtlib=compiler-rt','-DCMO_CONTAINER_TEST','-I'+str(ROOT/'tests/freestanding-headers'),'-I'+str(ROOT/'build'),'-I'+str(ROOT/'build/portable'),'-I'+str(ROOT/'tests'),str(ROOT/'tests/replay_freestanding.c'),'-Wl,-e,cmo_entry','-o',str(exe)]
 if family=='arm':cmd[2:2]=['-mcpu=cortex_a7','-marm']
 subprocess.run(cmd,check=True,timeout=180)
 checks=execute(exe,family,bits,big);row={'target':name,'status':'CPU_EMULATION_PASS','checks':checks,'elf_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'native_os':False,'allocator':'test-only simulated calloc/free; bump heap','source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint()};rows.append(row);print(json.dumps(row),flush=True)
(ROOT/'evidence/cross-cpu-report.json').write_text(json.dumps({'status':'PASS','targets':rows},indent=2)+'\n')
