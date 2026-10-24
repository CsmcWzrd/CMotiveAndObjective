/* CMotive custom-register runtime. BSL-1.0. No C ABI or libc calls. */
.arch armv8-a
.text

.p2align 2
.globl CMO_Asm_CopyBytes
.hidden CMO_Asm_CopyBytes
.type CMO_Asm_CopyBytes,%function
CMO_Asm_CopyBytes:
    mov x12,x9
    cbz x11,.Lcopy_a64_done
.Lcopy_a64_loop:
    ldrb w13,[x10],#1
    strb w13,[x12],#1
    subs x11,x11,#1
    b.ne .Lcopy_a64_loop
.Lcopy_a64_done:
    ret
.size CMO_Asm_CopyBytes,.-CMO_Asm_CopyBytes

.p2align 2
.globl CMO_Asm_MoveBytes
.hidden CMO_Asm_MoveBytes
.type CMO_Asm_MoveBytes,%function
CMO_Asm_MoveBytes:
    cbz x11,.Lmove_a64_done
    cmp x9,x10
    b.ls CMO_Asm_CopyBytes
    sub x12,x9,x10
    cmp x12,x11
    b.hs CMO_Asm_CopyBytes
    add x12,x9,x11
    sub x12,x12,#1
    add x10,x10,x11
    sub x10,x10,#1
.Lmove_a64_loop:
    ldrb w13,[x10],#-1
    strb w13,[x12],#-1
    subs x11,x11,#1
    b.ne .Lmove_a64_loop
.Lmove_a64_done:
    ret
.size CMO_Asm_MoveBytes,.-CMO_Asm_MoveBytes

.p2align 2
.globl CMO_Asm_FillBytes
.hidden CMO_Asm_FillBytes
.type CMO_Asm_FillBytes,%function
CMO_Asm_FillBytes:
    mov x12,x9
    cbz x11,.Lfill_a64_done
.Lfill_a64_loop:
    strb w10,[x12],#1
    subs x11,x11,#1
    b.ne .Lfill_a64_loop
.Lfill_a64_done:
    ret
.size CMO_Asm_FillBytes,.-CMO_Asm_FillBytes

.p2align 2
.globl CMO_Asm_CompareBytes
.hidden CMO_Asm_CompareBytes
.type CMO_Asm_CompareBytes,%function
CMO_Asm_CompareBytes:
    cbz x11,.Lcmp_a64_equal
.Lcmp_a64_loop:
    ldrb w12,[x9],#1
    ldrb w13,[x10],#1
    cmp w12,w13
    b.lo .Lcmp_a64_less
    b.hi .Lcmp_a64_greater
    subs x11,x11,#1
    b.ne .Lcmp_a64_loop
.Lcmp_a64_equal:
    mov x9,#0
    ret
.Lcmp_a64_less:
    mov x9,#-1
    ret
.Lcmp_a64_greater:
    mov x9,#1
    ret
.size CMO_Asm_CompareBytes,.-CMO_Asm_CompareBytes

.p2align 2
.globl CMO_Asm_StrnLength
.hidden CMO_Asm_StrnLength
.type CMO_Asm_StrnLength,%function
CMO_Asm_StrnLength:
    mov x12,x9
    mov x13,#0
    cbz x11,.Llen_a64_done
.Llen_a64_loop:
    ldrb w14,[x12],#1
    cbz w14,.Llen_a64_done
    add x13,x13,#1
    subs x11,x11,#1
    b.ne .Llen_a64_loop
.Llen_a64_done:
    mov x9,x13
    ret
.size CMO_Asm_StrnLength,.-CMO_Asm_StrnLength

.p2align 2
.globl CMO_Asm_LoadU32LE
.hidden CMO_Asm_LoadU32LE
.type CMO_Asm_LoadU32LE,%function
CMO_Asm_LoadU32LE:
    mov x12,x9
    ldrb w9,[x12,#0]
    ldrb w13,[x12,#1]
    orr w9,w9,w13,lsl #8
    ldrb w13,[x12,#2]
    orr w9,w9,w13,lsl #16
    ldrb w13,[x12,#3]
    orr w9,w9,w13,lsl #24
    ret
.size CMO_Asm_LoadU32LE,.-CMO_Asm_LoadU32LE

.p2align 2
.globl CMO_Asm_LoadU32BE
.hidden CMO_Asm_LoadU32BE
.type CMO_Asm_LoadU32BE,%function
CMO_Asm_LoadU32BE:
    mov x12,x9
    ldrb w9,[x12,#0]
    lsl w9,w9,#24
    ldrb w13,[x12,#1]
    orr w9,w9,w13,lsl #16
    ldrb w13,[x12,#2]
    orr w9,w9,w13,lsl #8
    ldrb w13,[x12,#3]
    orr w9,w9,w13
    ret
.size CMO_Asm_LoadU32BE,.-CMO_Asm_LoadU32BE

.p2align 2
.globl CMO_Asm_StoreU32LE
.hidden CMO_Asm_StoreU32LE
.type CMO_Asm_StoreU32LE,%function
CMO_Asm_StoreU32LE:
    strb w10,[x9,#0]
    lsr w13,w10,#8
    strb w13,[x9,#1]
    lsr w13,w10,#16
    strb w13,[x9,#2]
    lsr w13,w10,#24
    strb w13,[x9,#3]
    ret
.size CMO_Asm_StoreU32LE,.-CMO_Asm_StoreU32LE

.p2align 2
.globl CMO_Asm_StoreU32BE
.hidden CMO_Asm_StoreU32BE
.type CMO_Asm_StoreU32BE,%function
CMO_Asm_StoreU32BE:
    lsr w13,w10,#24
    strb w13,[x9,#0]
    lsr w13,w10,#16
    strb w13,[x9,#1]
    lsr w13,w10,#8
    strb w13,[x9,#2]
    strb w10,[x9,#3]
    ret
.size CMO_Asm_StoreU32BE,.-CMO_Asm_StoreU32BE

.section .note.GNU-stack,"",%progbits
