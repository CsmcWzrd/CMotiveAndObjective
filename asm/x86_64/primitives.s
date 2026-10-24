/* CMotive custom-register runtime. BSL-1.0. No C ABI or libc calls. */
.code64
.text

.p2align 2
.globl CMO_Asm_CopyBytes
.hidden CMO_Asm_CopyBytes
.type CMO_Asm_CopyBytes,@function
CMO_Asm_CopyBytes:
    movq %r10,%rdx
    testq %r8,%r8
    jz .Lcopy64_done
.Lcopy64_loop:
    movzbl (%r11),%eax
    movb %al,(%rdx)
    incq %r11
    incq %rdx
    decq %r8
    jnz .Lcopy64_loop
.Lcopy64_done:
    ret
.size CMO_Asm_CopyBytes,.-CMO_Asm_CopyBytes

.p2align 2
.globl CMO_Asm_MoveBytes
.hidden CMO_Asm_MoveBytes
.type CMO_Asm_MoveBytes,@function
CMO_Asm_MoveBytes:
    testq %r8,%r8
    jz .Lmove64_done
    cmpq %r11,%r10
    jbe CMO_Asm_CopyBytes
    movq %r10,%rdx
    subq %r11,%rdx
    cmpq %r8,%rdx
    jae CMO_Asm_CopyBytes
    leaq -1(%r10,%r8),%rdx
    leaq -1(%r11,%r8),%r11
.Lmove64_loop:
    movzbl (%r11),%eax
    movb %al,(%rdx)
    decq %r11
    decq %rdx
    decq %r8
    jnz .Lmove64_loop
.Lmove64_done:
    ret
.size CMO_Asm_MoveBytes,.-CMO_Asm_MoveBytes

.p2align 2
.globl CMO_Asm_FillBytes
.hidden CMO_Asm_FillBytes
.type CMO_Asm_FillBytes,@function
CMO_Asm_FillBytes:
    movq %r10,%rdx
    movl %r11d,%eax
    testq %r8,%r8
    jz .Lfill64_done
.Lfill64_loop:
    movb %al,(%rdx)
    incq %rdx
    decq %r8
    jnz .Lfill64_loop
.Lfill64_done:
    ret
.size CMO_Asm_FillBytes,.-CMO_Asm_FillBytes

.p2align 2
.globl CMO_Asm_CompareBytes
.hidden CMO_Asm_CompareBytes
.type CMO_Asm_CompareBytes,@function
CMO_Asm_CompareBytes:
    testq %r8,%r8
    jz .Lcmp64_equal
.Lcmp64_loop:
    movzbl (%r10),%eax
    movzbl (%r11),%ecx
    cmpl %ecx,%eax
    jb .Lcmp64_less
    ja .Lcmp64_greater
    incq %r10
    incq %r11
    decq %r8
    jnz .Lcmp64_loop
.Lcmp64_equal:
    xorq %r10,%r10
    ret
.Lcmp64_less:
    movq $-1,%r10
    ret
.Lcmp64_greater:
    movq $1,%r10
    ret
.size CMO_Asm_CompareBytes,.-CMO_Asm_CompareBytes

.p2align 2
.globl CMO_Asm_StrnLength
.hidden CMO_Asm_StrnLength
.type CMO_Asm_StrnLength,@function
CMO_Asm_StrnLength:
    movq %r10,%rdx
    xorq %rax,%rax
    testq %r8,%r8
    jz .Llen64_done
.Llen64_loop:
    cmpb $0,(%rdx)
    je .Llen64_done
    incq %rdx
    incq %rax
    decq %r8
    jnz .Llen64_loop
.Llen64_done:
    movq %rax,%r10
    ret
.size CMO_Asm_StrnLength,.-CMO_Asm_StrnLength

.p2align 2
.globl CMO_Asm_LoadU32LE
.hidden CMO_Asm_LoadU32LE
.type CMO_Asm_LoadU32LE,@function
CMO_Asm_LoadU32LE:
    movl (%r10),%r10d
    ret
.size CMO_Asm_LoadU32LE,.-CMO_Asm_LoadU32LE

.p2align 2
.globl CMO_Asm_LoadU32BE
.hidden CMO_Asm_LoadU32BE
.type CMO_Asm_LoadU32BE,@function
CMO_Asm_LoadU32BE:
    movl (%r10),%eax
    bswap %eax
    movl %eax,%r10d
    ret
.size CMO_Asm_LoadU32BE,.-CMO_Asm_LoadU32BE

.p2align 2
.globl CMO_Asm_StoreU32LE
.hidden CMO_Asm_StoreU32LE
.type CMO_Asm_StoreU32LE,@function
CMO_Asm_StoreU32LE:
    movl %r11d,(%r10)
    ret
.size CMO_Asm_StoreU32LE,.-CMO_Asm_StoreU32LE

.p2align 2
.globl CMO_Asm_StoreU32BE
.hidden CMO_Asm_StoreU32BE
.type CMO_Asm_StoreU32BE,@function
CMO_Asm_StoreU32BE:
    movl %r11d,%eax
    bswap %eax
    movl %eax,(%r10)
    ret
.size CMO_Asm_StoreU32BE,.-CMO_Asm_StoreU32BE

.section .note.GNU-stack,"",@progbits
