/* CMotive custom-register runtime. BSL-1.0. No C ABI or libc calls. */
.syntax unified
.arch armv7-a
.arm
.text

.p2align 2
.globl CMO_Asm_CopyBytes
.hidden CMO_Asm_CopyBytes
.type CMO_Asm_CopyBytes,%function
CMO_Asm_CopyBytes:
    mov r0,r4
    cmp r6,#0
    beq .Lcopy_a32_done
.Lcopy_a32_loop:
    ldrb r1,[r5],#1
    strb r1,[r0],#1
    subs r6,r6,#1
    bne .Lcopy_a32_loop
.Lcopy_a32_done:
    bx lr
.size CMO_Asm_CopyBytes,.-CMO_Asm_CopyBytes

.p2align 2
.globl CMO_Asm_MoveBytes
.hidden CMO_Asm_MoveBytes
.type CMO_Asm_MoveBytes,%function
CMO_Asm_MoveBytes:
    cmp r6,#0
    beq .Lmove_a32_done
    cmp r4,r5
    bls CMO_Asm_CopyBytes
    sub r0,r4,r5
    cmp r0,r6
    bhs CMO_Asm_CopyBytes
    add r0,r4,r6
    sub r0,r0,#1
    add r5,r5,r6
    sub r5,r5,#1
.Lmove_a32_loop:
    ldrb r1,[r5],#-1
    strb r1,[r0],#-1
    subs r6,r6,#1
    bne .Lmove_a32_loop
.Lmove_a32_done:
    bx lr
.size CMO_Asm_MoveBytes,.-CMO_Asm_MoveBytes

.p2align 2
.globl CMO_Asm_FillBytes
.hidden CMO_Asm_FillBytes
.type CMO_Asm_FillBytes,%function
CMO_Asm_FillBytes:
    mov r0,r4
    cmp r6,#0
    beq .Lfill_a32_done
.Lfill_a32_loop:
    strb r5,[r0],#1
    subs r6,r6,#1
    bne .Lfill_a32_loop
.Lfill_a32_done:
    bx lr
.size CMO_Asm_FillBytes,.-CMO_Asm_FillBytes

.p2align 2
.globl CMO_Asm_CompareBytes
.hidden CMO_Asm_CompareBytes
.type CMO_Asm_CompareBytes,%function
CMO_Asm_CompareBytes:
    cmp r6,#0
    beq .Lcmp_a32_equal
.Lcmp_a32_loop:
    ldrb r0,[r4],#1
    ldrb r1,[r5],#1
    cmp r0,r1
    blo .Lcmp_a32_less
    bhi .Lcmp_a32_greater
    subs r6,r6,#1
    bne .Lcmp_a32_loop
.Lcmp_a32_equal:
    mov r4,#0
    bx lr
.Lcmp_a32_less:
    mvn r4,#0
    bx lr
.Lcmp_a32_greater:
    mov r4,#1
    bx lr
.size CMO_Asm_CompareBytes,.-CMO_Asm_CompareBytes

.p2align 2
.globl CMO_Asm_StrnLength
.hidden CMO_Asm_StrnLength
.type CMO_Asm_StrnLength,%function
CMO_Asm_StrnLength:
    mov r0,r4
    mov r1,#0
    cmp r6,#0
    beq .Llen_a32_done
.Llen_a32_loop:
    ldrb r2,[r0],#1
    cmp r2,#0
    beq .Llen_a32_done
    add r1,r1,#1
    subs r6,r6,#1
    bne .Llen_a32_loop
.Llen_a32_done:
    mov r4,r1
    bx lr
.size CMO_Asm_StrnLength,.-CMO_Asm_StrnLength

.p2align 2
.globl CMO_Asm_LoadU32LE
.hidden CMO_Asm_LoadU32LE
.type CMO_Asm_LoadU32LE,%function
CMO_Asm_LoadU32LE:
    mov r0,r4
    ldrb r4,[r0,#0]
    ldrb r1,[r0,#1]
    orr r4,r4,r1,lsl #8
    ldrb r1,[r0,#2]
    orr r4,r4,r1,lsl #16
    ldrb r1,[r0,#3]
    orr r4,r4,r1,lsl #24
    bx lr
.size CMO_Asm_LoadU32LE,.-CMO_Asm_LoadU32LE

.p2align 2
.globl CMO_Asm_LoadU32BE
.hidden CMO_Asm_LoadU32BE
.type CMO_Asm_LoadU32BE,%function
CMO_Asm_LoadU32BE:
    mov r0,r4
    ldrb r4,[r0,#0]
    lsl r4,r4,#24
    ldrb r1,[r0,#1]
    orr r4,r4,r1,lsl #16
    ldrb r1,[r0,#2]
    orr r4,r4,r1,lsl #8
    ldrb r1,[r0,#3]
    orr r4,r4,r1
    bx lr
.size CMO_Asm_LoadU32BE,.-CMO_Asm_LoadU32BE

.p2align 2
.globl CMO_Asm_StoreU32LE
.hidden CMO_Asm_StoreU32LE
.type CMO_Asm_StoreU32LE,%function
CMO_Asm_StoreU32LE:
    strb r5,[r4,#0]
    lsr r1,r5,#8
    strb r1,[r4,#1]
    lsr r1,r5,#16
    strb r1,[r4,#2]
    lsr r1,r5,#24
    strb r1,[r4,#3]
    bx lr
.size CMO_Asm_StoreU32LE,.-CMO_Asm_StoreU32LE

.p2align 2
.globl CMO_Asm_StoreU32BE
.hidden CMO_Asm_StoreU32BE
.type CMO_Asm_StoreU32BE,%function
CMO_Asm_StoreU32BE:
    lsr r1,r5,#24
    strb r1,[r4,#0]
    lsr r1,r5,#16
    strb r1,[r4,#1]
    lsr r1,r5,#8
    strb r1,[r4,#2]
    strb r5,[r4,#3]
    bx lr
.size CMO_Asm_StoreU32BE,.-CMO_Asm_StoreU32BE

.section .note.GNU-stack,"",%progbits
