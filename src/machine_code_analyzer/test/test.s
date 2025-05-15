	.text
	.file	"test2.c"
	.globl	add_two_numbers                 # -- Begin function add_two_numbers
	.p2align	4, 0x90
	.type	add_two_numbers,@function
add_two_numbers:                        # @add_two_numbers
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	movq	(%rsi), %rcx
	movq	8(%rdx), %r8
	movl	(%rdx), %eax
	addl	%r8d, %eax
	addl	16(%rdx), %eax
	addl	24(%rdx), %eax
	addl	32(%rdx), %eax
	addl	40(%rdx), %eax
	addl	48(%rdx), %eax
	addl	56(%rdx), %eax
	addl	64(%rdx), %eax
	addl	72(%rdx), %eax
	movl	8(%rsi), %r9d
	addl	%ecx, %r9d
	addl	16(%rsi), %r9d
	addl	24(%rsi), %r9d
	addl	32(%rsi), %r9d
	addl	40(%rsi), %r9d
	addl	48(%rsi), %r9d
	addl	56(%rsi), %r9d
	addl	64(%rsi), %r9d
	addl	72(%rsi), %r9d
	movslq	%r9d, %r9
	cltq
	subq	%r9, %rax
	addq	%r8, %rcx
	addq	%rax, %rcx
	movq	%rcx, (%rdi)
	movq	8(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 8(%rdi)
	movq	16(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 16(%rdi)
	movq	24(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 24(%rdi)
	movq	32(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 32(%rdi)
	movq	40(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 40(%rdi)
	movq	48(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 48(%rdi)
	movq	56(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 56(%rdi)
	movq	64(%rsi), %rcx
	addq	%rax, %rcx
	addq	8(%rdx), %rcx
	movq	%rcx, 64(%rdi)
	addq	72(%rsi), %rax
	addq	8(%rdx), %rax
	movq	%rax, 72(%rdi)
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	add_two_numbers, .Lfunc_end0-add_two_numbers
	.cfi_endproc
                                        # -- End function
	.ident	"clang version 16.0.6"
	.section	".note.GNU-stack","",@progbits
	.addrsig
