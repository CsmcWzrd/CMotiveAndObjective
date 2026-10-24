/* Native test fixture only. BSL-1.0. Golden FNV digests from Python codecs. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "CMotiveAndObjective.c"
#define A(c,m) CMotiveAndObjective__##c##__##m
static unsigned long checks;
#define CHECK(x) do{checks++;if(!(x)){fprintf(stderr,"Unicode check at line %d scalar %x\n",__LINE__,cp);exit(1);}}while(0)
static uint64_t hash(uint64_t h,unsigned char*p,int n){for(int i=0;i<n;i++)h=(h^p[i])*UINT64_C(0x100000001b3);return h;}
int main(void){
 uint32_t cp=0;Utf8*u=A(Utf8,new)();Utf16*v=A(Utf16,new)();CHECK(u&&v);
 uint64_t hashes[3]={UINT64_C(0xcbf29ce484222325),UINT64_C(0xcbf29ce484222325),UINT64_C(0xcbf29ce484222325)};unsigned long scalars=0;
 for(cp=0;cp<0x110000;cp++){
  unsigned char out[8];memset(out,0xa5,sizeof out);int32_t used=99;
  if(cp>=0xd800&&cp<=0xdfff){CHECK(A(Utf8,Encode)(u,cp,out,4)==-2);CHECK(out[0]==0xa5);for(int mode=0;mode<2;mode++){CHECK(A(Utf16,Encode)(v,cp,out,4,mode)==-2);CHECK(out[0]==0xa5);}continue;}
  int n=A(Utf8,Encode)(u,cp,out,4);CHECK(n>=1&&n<=4);CHECK(out[n]==0xa5);hashes[0]=hash(hashes[0],out,n);
  CHECK(A(Utf8,DecodeFirst)(u,out,n,&used)==(int32_t)cp);CHECK(used==n);CHECK(A(Utf8,Count)(u,out,n)==1);
  if(n>1){CHECK(A(Utf8,DecodeFirst)(u,out,n-1,&used)==-2);CHECK(used==0);}
  for(int mode=0;mode<2;mode++){
   memset(out,0xa5,sizeof out);n=A(Utf16,Encode)(v,cp,out,4,mode);CHECK(n==(cp<65536?2:4));CHECK(out[n]==0xa5);hashes[1+mode]=hash(hashes[1+mode],out,n);
   CHECK(A(Utf16,DecodeFirst)(v,out,n,mode,&used)==(int32_t)cp);CHECK(used==n);CHECK(A(Utf16,Count)(v,out,n,mode)==1);
   CHECK(A(Utf16,DecodeFirst)(v,out,n-1,mode,&used)==-2);CHECK(used==0);
  }scalars++;
 }
 CHECK(scalars==1112064);
 CHECK(hashes[0]==UINT64_C(0x957cc0987e6013e5));
 CHECK(hashes[1]==UINT64_C(0x6a25a430597ec325));
 CHECK(hashes[2]==UINT64_C(0xdb2251e4a4b64525));
 A(Utf8,delete)(u);A(Utf16,delete)(v);printf("Exhaustive Unicode: PASS; %lu scalars; %lu checks\n",scalars,checks);return 0;
}
