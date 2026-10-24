/* CMotive custom-register runtime. BSL-1.0. No C ABI or libc calls. */
.code32
.text

.p2align 2
.globl CMO_Asm_CopyBytes
.hidden CMO_Asm_CopyBytes
.type CMO_Asm_CopyBytes,@function
CMO_Asm_CopyBytes:
    movl %edi,%edx
    testl %ecx,%ecx
    jz .Lcopy32_done
.Lcopy32_loop:
    movzbl (%esi),%eax
    movb %al,(%edx)
    incl %esi
    incl %edx
    decl %ecx
    jnz .Lcopy32_loop
.Lcopy32_done:
    ret
.size CMO_Asm_CopyBytes,.-CMO_Asm_CopyBytes

.p2align 2
.globl CMO_Asm_MoveBytes
.hidden CMO_Asm_MoveBytes
.type CMO_Asm_MoveBytes,@function
CMO_Asm_MoveBytes:
    testl %ecx,%ecx
    jz .Lmove32_done
    cmpl %esi,%edi
    jbe CMO_Asm_CopyBytes
    movl %edi,%edx
    subl %esi,%edx
    cmpl %ecx,%edx
    jae CMO_Asm_CopyBytes
    leal -1(%edi,%ecx),%edx
    leal -1(%esi,%ecx),%esi
.Lmove32_loop:
    movzbl (%esi),%eax
    movb %al,(%edx)
    decl %esi
    decl %edx
    decl %ecx
    jnz .Lmove32_loop
.Lmove32_done:
    ret
.size CMO_Asm_MoveBytes,.-CMO_Asm_MoveBytes

.p2align 2
.globl CMO_Asm_FillBytes
.hidden CMO_Asm_FillBytes
.type CMO_Asm_FillBytes,@function
CMO_Asm_FillBytes:
    movl %edi,%edx
    movl %esi,%eax
    testl %ecx,%ecx
    jz .Lfill32_done
.Lfill32_loop:
    movb %al,(%edx)
    incl %edx
    decl %ecx
    jnz .Lfill32_loop
.Lfill32_done:
    ret
.size CMO_Asm_FillBytes,.-CMO_Asm_FillBytes

.p2align 2
.globl CMO_Asm_CompareBytes
.hidden CMO_Asm_CompareBytes
.type CMO_Asm_CompareBytes,@function
CMO_Asm_CompareBytes:
    testl %ecx,%ecx
    jz .Lcmp32_equal
.Lcmp32_loop:
    movzbl (%edi),%eax
    movzbl (%esi),%edx
    cmpl %edx,%eax
    jb .Lcmp32_less
    ja .Lcmp32_greater
    incl %edi
    incl %esi
    decl %ecx
    jnz .Lcmp32_loop
.Lcmp32_equal:
    xorl %edi,%edi
    ret
.Lcmp32_less:
    movl $-1,%edi
    ret
.Lcmp32_greater:
    movl $1,%edi
    ret
.size CMO_Asm_CompareBytes,.-CMO_Asm_CompareBytes

.p2align 2
.globl CMO_Asm_StrnLength
.hidden CMO_Asm_StrnLength
.type CMO_Asm_StrnLength,@function
CMO_Asm_StrnLength:
    movl %edi,%edx
    xorl %eax,%eax
    testl %ecx,%ecx
    jz .Llen32_done
.Llen32_loop:
    cmpb $0,(%edx)
    je .Llen32_done
    incl %edx
    incl %eax
    decl %ecx
    jnz .Llen32_loop
.Llen32_done:
    movl %eax,%edi
    ret
.size CMO_Asm_StrnLength,.-CMO_Asm_StrnLength

.p2align 2
.globl CMO_Asm_LoadU32LE
.hidden CMO_Asm_LoadU32LE
.type CMO_Asm_LoadU32LE,@function
CMO_Asm_LoadU32LE:
    movl (%edi),%edi
    ret
.size CMO_Asm_LoadU32LE,.-CMO_Asm_LoadU32LE

.p2align 2
.globl CMO_Asm_LoadU32BE
.hidden CMO_Asm_LoadU32BE
.type CMO_Asm_LoadU32BE,@function
CMO_Asm_LoadU32BE:
    movl (%edi),%eax
    xchgb %al,%ah
    rorl $16,%eax
    xchgb %al,%ah
    movl %eax,%edi
    ret
.size CMO_Asm_LoadU32BE,.-CMO_Asm_LoadU32BE

.p2align 2
.globl CMO_Asm_StoreU32LE
.hidden CMO_Asm_StoreU32LE
.type CMO_Asm_StoreU32LE,@function
CMO_Asm_StoreU32LE:
    movl %esi,(%edi)
    ret
.size CMO_Asm_StoreU32LE,.-CMO_Asm_StoreU32LE

.p2align 2
.globl CMO_Asm_StoreU32BE
.hidden CMO_Asm_StoreU32BE
.type CMO_Asm_StoreU32BE,@function
CMO_Asm_StoreU32BE:
    movl %esi,%eax
    xchgb %al,%ah
    rorl $16,%eax
    xchgb %al,%ah
    movl %eax,(%edi)
    ret
.size CMO_Asm_StoreU32BE,.-CMO_Asm_StoreU32BE

.section .note.GNU-stack,"",@progbits
