#!/usr/bin/env python3
"""Execute the custom register contract directly in six CPU/endian modes.

Requires Unicorn and pyelftools for testing only. No C-ABI shim is generated.
"""
from pathlib import Path
import argparse,json,random,hashlib
import unicorn as U
import unicorn.x86_const as X
import unicorn.arm_const as A
import unicorn.arm64_const as B
from elftools.elf.elffile import ELFFile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--build-dir',type=Path,default=ROOT/'build-asm');args=p.parse_args()
contract=json.loads((ROOT/'asm/contract.json').read_text());rng=random.Random(391724);total=0;results=[]
class Machine:
    def __init__(self,target):
        self.t=target;self.mask=(1<<target['bits'])-1
        mode=U.UC_MODE_BIG_ENDIAN if target['endian']=='big' else U.UC_MODE_LITTLE_ENDIAN
        if target['source'].startswith('x86'):
            mode=U.UC_MODE_64 if target['bits']==64 else U.UC_MODE_32
            self.uc=U.Uc(U.UC_ARCH_X86,mode);prefix='UC_X86_REG_'
            self.reg=lambda n:getattr(X,prefix+n.upper());self.sp=self.reg('rsp' if target['bits']==64 else 'esp');self.pc=self.reg('rip' if target['bits']==64 else 'eip')
            regs=['rax','rbx','rcx','rdx','rsi','rdi','rbp','r8','r9','r10','r11','r12','r13','r14','r15'] if target['bits']==64 else ['eax','ebx','ecx','edx','esi','edi','ebp']
            self.lr=None
        elif target['source']=='arm32':
            # BE8 has little-endian instructions and CPSR.E=1 for data. BIG_ENDIAN
            # selects BE32 instruction decoding and must not be combined with it.
            if target['endian']=='big':mode=U.UC_MODE_ARMBE8
            self.uc=U.Uc(U.UC_ARCH_ARM,U.UC_MODE_ARM|mode);self.reg=lambda n:getattr(A,'UC_ARM_REG_'+n.upper());self.sp=A.UC_ARM_REG_SP;self.pc=A.UC_ARM_REG_PC;self.lr=A.UC_ARM_REG_LR;regs=['r'+str(i) for i in range(13)]
            eq(bool(self.uc.reg_read(A.UC_ARM_REG_CPSR)&512),target['endian']=='big')
        else:
            self.uc=U.Uc(U.UC_ARCH_ARM64,U.UC_MODE_ARM|mode);self.reg=lambda n:getattr(B,'UC_ARM64_REG_'+n.upper());self.sp=B.UC_ARM64_REG_SP;self.pc=B.UC_ARM64_REG_PC;self.lr=B.UC_ARM64_REG_LR;regs=['x'+str(i) for i in range(30)]
        with open(args.build_dir/target['name']/'primitives.elf','rb') as f:
            elf=ELFFile(f);text=elf.get_section_by_name('.text');address=text['sh_addr'];data=text.data()
            eq(elf.elfclass,target['bits']);eq(elf.little_endian,target['endian']=='little')
            eq(elf.header['e_machine'],{'x86':'EM_386','x86_64':'EM_X86_64','arm32':'EM_ARM','arm64':'EM_AARCH64'}[target['source']])
            eq(elf.get_section_by_name('.dynamic'),None)
            eq([s.name for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name and s['st_shndx']=='SHN_UNDEF'],[])
            if target['source']=='arm32' and target['endian']=='big':eq(bool(elf.header['e_flags']&0x800000),True)
            self.symbols={s.name:s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name.startswith('CMO_Asm_')}
        eq(set(self.symbols),set(contract['routines']))
        base=address&~4095;size=((address+len(data)-base+4095)//4096)*4096
        self.uc.mem_map(base,size);self.uc.mem_write(address,data)
        self.data=0x40000000;self.stack=0x60000000;self.end=0x7f000000
        self.uc.mem_map(self.data,65536);self.uc.mem_map(self.stack,65536);self.uc.mem_map(self.end,4096)
        if target['source']=='arm64':
            # Independent CPU-mode probe: LDR W12,[X9] must observe data endianness.
            # A64 instruction bytes stay little-endian in both endian modes.
            self.uc.mem_write(self.end+128,bytes.fromhex('2c0140b9'))
            self.uc.mem_write(self.data+64000,b'\x01\x02\x03\x04')
            self.uc.reg_write(B.UC_ARM64_REG_X9,self.data+64000)
            self.uc.emu_start(self.end+128,self.end+132,count=1)
            eq(self.uc.reg_read(B.UC_ARM64_REG_X12),int.from_bytes(b'\x01\x02\x03\x04',target['endian']))
        changed=set(target['args']+target['scratch']);self.preserved=[r for r in regs if r not in changed]
    def call(self,name,a=0,b=0,n=0):
        uc=self.uc;canary=0x12345678;top=self.stack+32768
        for reg in self.preserved:uc.reg_write(self.reg(reg),canary)
        for reg,value in zip(self.t['args'],[a,b,n]):uc.reg_write(self.reg(reg),value&self.mask)
        if self.lr is None:
            width=self.t['bits']//8;uc.mem_write(top-width,self.end.to_bytes(width,'little'));uc.reg_write(self.sp,top-width)
        else:uc.reg_write(self.sp,top);uc.reg_write(self.lr,self.end)
        uc.emu_start(self.symbols['CMO_Asm_'+name],self.end,count=2000000)
        eq(uc.reg_read(self.pc),self.end);eq(uc.reg_read(self.sp),top)
        if self.lr is not None:eq(uc.reg_read(self.lr),self.end)
        for reg in self.preserved:eq(uc.reg_read(self.reg(reg)),canary)
        return uc.reg_read(self.reg(self.t['args'][0]))&self.mask
    def write(self,offset,data):self.uc.mem_write(self.data+offset,bytes(data))
    def read(self,offset,n):return bytes(self.uc.mem_read(self.data+offset,n))
def eq(a,b):
    global total
    total+=1
    if a!=b:raise AssertionError(f'ASM check {total}: {a!r} != {b!r}')
for target in contract['targets']:
    start=total;m=Machine(target);d=m.data
    for n in [0,1,2,3,4,7,15,16,31,32,63,64,127,255]+[rng.randrange(256) for _ in range(80)]:
        source=rng.randbytes(n);m.write(0,source+b'\xa5'*8);m.write(4096,b'\xa5'*(n+8))
        eq(m.call('CopyBytes',d+4096,d,n),d+4096);eq(m.read(4096,n+8),source+b'\xa5'*8)
        eq(m.read(0,n+8),source+b'\xa5'*8)
        value=rng.getrandbits(target['bits']);eq(m.call('FillBytes',d+4096,value,n),d+4096)
        eq(m.read(4096,n+8),bytes([value&255])*n+b'\xa5'*8)
        other=source if rng.randrange(2) else rng.randbytes(n);m.write(4096,other+b'\0')
        eq(m.call('CompareBytes',d,d+4096,n),((source>other)-(source<other))&m.mask)
    for _ in range(160):
        data=bytearray(rng.randbytes(300));src=rng.randrange(80);dst=rng.randrange(80);n=rng.randrange(200)
        expected=data[:];expected[dst:dst+n]=data[src:src+n];m.write(0,data)
        eq(m.call('MoveBytes',d+dst,d+src,n),d+dst);eq(m.read(0,300),bytes(expected))
    for n in [0,1,2,31,127]:
        for zero in [0,n//2,n]:
            data=b'X'*zero+b'\0'+b'Z'*200;m.write(0,data)
            eq(m.call('StrnLength',d,0,n),min(zero,n))
    for _ in range(120):
        value=rng.getrandbits(32);offset=rng.randrange(1,32)
        for order in ['little','big']:
            suffix='LE' if order=='little' else 'BE';m.write(0,b'\xa5'*40)
            eq(m.call('StoreU32'+suffix,d+offset,value),d+offset)
            expected=bytearray(b'\xa5'*40);expected[offset:offset+4]=value.to_bytes(4,order)
            eq(m.read(0,40),bytes(expected));eq(m.call('LoadU32'+suffix,d+offset),value)
            opposite='BE' if suffix=='LE' else 'LE';eq(m.call('LoadU32'+opposite,d+offset),int.from_bytes(value.to_bytes(4,order),'big' if order=='little' else 'little'))
    for routine in ['CopyBytes','MoveBytes','FillBytes','CompareBytes','StrnLength']:eq(m.call(routine,0,0,0),0)
    # Page-edge spans detect a single unintended byte access past the count.
    for n in [0,1,2,3,16,64]:
        offset=65536-n
        if n:m.write(offset,b'X'*n)
        eq(m.call('CopyBytes',d+4096,d+offset,n),d+4096)
        eq(m.call('CompareBytes',d+offset,d+4096,n),0)
        eq(m.call('StrnLength',d+offset,0,n),n)
    results.append({'target':target['name'],'status':'PASS','assertions':total-start,'elf_sha256':hashlib.sha256((args.build_dir/target['name']/'primitives.elf').read_bytes()).hexdigest()})
    print(target['name']+': PASS',flush=True)
report={'status':'PASS','convention':contract['convention'],'assertions':total,'targets':results,'execution':'CPU emulation, not physical ARM hardware'}
(args.build_dir/'test-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','assertions':total,'targets':len(results)}))
