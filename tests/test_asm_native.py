#!/usr/bin/env python3
"""Linux x86/x86_64 freestanding callers. No C startup code, ABI shim or libc."""
from pathlib import Path
import argparse,json,platform,subprocess,errno
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--build-dir',type=Path,default=ROOT/'build-asm');args=p.parse_args()
if platform.system()!='Linux' or platform.machine()!='x86_64':raise SystemExit('Native harness requires a Linux x86_64 host with i386 execution support')
results=[]
for bits,arch in [(32,'x86'),(64,'x86_64')]:
    directory=args.build_dir/(arch+'-le');directory.mkdir(parents=True,exist_ok=True)
    r0,r1,r2=('%edi','%esi','%ecx') if bits==32 else ('%r10','%r11','%r8')
    word='l' if bits==32 else 'q'
    def address(label,reg):return ('    movl $'+label+','+reg+'\n') if bits==32 else ('    leaq '+label+'(%rip),'+reg+'\n')
    def value(n,reg):return '    mov'+word+' $'+str(n)+','+reg+'\n'
    def call(name):return '    call CMO_Asm_'+name+'\n'
    def check(n):return '    cmp'+word+' $'+str(n)+','+r0+'\n    jne .Lfail\n'
    def compare(label,count):return address('buffer',r0)+address(label,r1)+value(count,r2)+call('CompareBytes')+check(0)
    s='.code'+str(bits)+'\n.text\n.globl _start\n_start:\n'
    s+=value(0x12345678,'%ebx' if bits==32 else '%rbx')+value(0x11223344,'%ebp' if bits==32 else '%rbp')
    s+=address('buffer',r0)+value(0xa5,r1)+value(16,r2)+call('FillBytes')+compare('filled',16)
    s+=address('buffer',r0)+address('input',r1)+value(9,r2)+call('CopyBytes')+compare('input',9)
    s+=address('buffer+1',r0)+address('buffer',r1)+value(8,r2)+call('MoveBytes')+compare('moved',9)
    s+=address('input',r0)+value(20,r2)+call('StrnLength')+check(8)
    s+=address('word_bytes',r0)+call('LoadU32LE')+check(0x78563412)
    s+=address('word_bytes',r0)+call('LoadU32BE')+check(0x12345678)
    s+=address('buffer+1',r0)+value(0x12345678,r1)+call('StoreU32LE')
    s+=address('buffer+1',r0)+call('LoadU32BE')+check(0x78563412)
    s+=address('buffer+1',r0)+value(0x12345678,r1)+call('StoreU32BE')
    s+=address('buffer+1',r0)+call('LoadU32LE')+check(0x78563412)
    s+='    cmpl $0x12345678,%ebx\n    jne .Lfail\n    cmpl $0x11223344,%ebp\n    jne .Lfail\n'
    if bits==32:s+='    xorl %ebx,%ebx\n    jmp .Lexit\n.Lfail:\n    movl $1,%ebx\n.Lexit:\n    movl $1,%eax\n    int $0x80\n'
    else:s+='    xorl %edi,%edi\n    jmp .Lexit\n.Lfail:\n    movl $1,%edi\n.Lexit:\n    movl $60,%eax\n    syscall\n'
    s+='.data\ninput: .asciz "abcdefgh"\nmoved: .ascii "aabcdefgh"\nfilled: .fill 16,1,0xa5\nword_bytes: .byte 0x12,0x34,0x56,0x78\n.bss\n.p2align 4\nbuffer: .space 32\n.section .note.GNU-stack,"",@progbits\n'
    source=directory/'native-caller.s';source.write_text(s);obj=directory/'native-caller.o';exe=directory/'native-caller'
    subprocess.run(['as','--'+str(bits),str(source),'-o',str(obj)],check=True)
    subprocess.run(['ld','-m','elf_i386' if bits==32 else 'elf_x86_64','-static','-e','_start',str(obj),str(directory/'primitives.o'),'-o',str(exe)],check=True)
    try:subprocess.run([str(exe.resolve())],check=True)
    except OSError as error:
        if bits==32 and error.errno==errno.ENOEXEC:
            results.append({'target':arch+'-le','status':'NOT RUN','reason':'Host kernel does not execute ELF32; use the CPU emulator test'})
            print(arch+': native execution unavailable (ELF32 kernel support)',flush=True)
            continue
        raise
    results.append({'target':arch+'-le','status':'PASS','execution':'native CPU, freestanding Linux executable','routines_exercised':9})
    print(arch+': native freestanding caller PASS',flush=True)
(args.build_dir/'native-test-report.json').write_text(json.dumps({'status':'PASS_WITH_SKIP' if any(r['status']!='PASS' for r in results) else 'PASS','targets':results},indent=2)+'\n')
