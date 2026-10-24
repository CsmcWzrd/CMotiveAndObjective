/* Test-only simulated OS allocator and memory routines. No library wrappers. */
#include <stdint.h>
#include <stddef.h>
_Alignas(16) static unsigned char heap[16777216];
static size_t used;
__attribute__((noinline)) void cmo_fail(void){for(;;){__asm__ volatile("" ::: "memory");}}
__attribute__((noinline)) void cmo_finish(void){for(;;){__asm__ volatile("" ::: "memory");}}
void *memset(void *dest,int c,size_t n){volatile unsigned char*d=dest;for(size_t i=0;i<n;i++)d[i]=(unsigned char)c;return dest;}
void *memcpy(void *dest,const void*source,size_t n){unsigned char*d=dest;const unsigned char*s=source;for(size_t i=0;i<n;i++)d[i]=s[i];return dest;}
void *memmove(void *dest,const void*source,size_t n){unsigned char*d=dest;const unsigned char*s=source;if(d<s){for(size_t i=0;i<n;i++)d[i]=s[i];}else{while(n){n--;d[n]=s[n];}}return dest;}
int memcmp(const void*a,const void*b,size_t n){const unsigned char*x=a,*y=b;for(size_t i=0;i<n;i++)if(x[i]!=y[i])return x[i]<y[i]?-1:1;return 0;}
void*calloc(size_t n,size_t s){if(s&&n>SIZE_MAX/s)return NULL;size_t amount=n*s;if(amount>sizeof(heap)-used)return NULL;size_t aligned=(amount+15)&~(size_t)15;if(aligned>sizeof(heap)-used)return NULL;void*p=heap+used;used+=aligned;memset(p,0,amount);return p;}
void free(void*p){(void)p;}
#define main replay_main
#include "portable_replay.c"
#undef main
void cmo_entry(void){if(replay_main()!=0)cmo_fail();cmo_finish();}
