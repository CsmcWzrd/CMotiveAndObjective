/* Independent C consumer and sanitizer stress harness. BSL-1.0. */
#include "CMotiveAndObjective.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define CHECK(x) do { if(!(x)){fprintf(stderr,"ABI check failed at line %d\n",__LINE__);return 1;} } while(0)
#define FN(c,m) CMotiveAndObjective__##c##__##m
int main(void) {
 void *a=FN(AlgorithmsI64,new)(),*v=FN(ArrayVectorI64,new)(),*h=FN(BinaryHeapI64,new)();
 void *b=FN(Base64,new)(),*hex=FN(Hex,new)(),*u=FN(Utf8,new)(),*ci=FN(CheckedInt,new)();
 CHECK(a&&v&&h&&b&&hex&&u&&ci);
 int64_t data[1024],out=0; uint8_t input[257],encoded[348],decoded[258];
 for(int round=0;round<100;round++) {
  for(int i=0;i<1024;i++)data[i]=(int64_t)((i*193+round*17)%137)-68;
  CHECK(FN(AlgorithmsI64,HeapSort)(a,data,1024)==0);
  for(int i=1;i<1024;i++)CHECK(data[i-1]<=data[i]);
  CHECK(FN(ArrayVectorI64,Bind)(v,data,1024)==0);
  for(int i=0;i<1024;i++)CHECK(FN(ArrayVectorI64,PushBack)(v,i)==0);
  CHECK(FN(ArrayVectorI64,PushBack)(v,7)==-1);
  CHECK(FN(ArrayVectorI64,At)(v,-1,&out)==-1);
  CHECK(FN(ArrayVectorI64,At)(v,1024,&out)==-1);
  CHECK(FN(ArrayVectorI64,Insert)(v,0,7)==-1);
  for(int i=1023;i>=0;i--){CHECK(FN(ArrayVectorI64,PopBack)(v,&out)==0);CHECK(out==i);}
  CHECK(FN(BinaryHeapI64,Bind)(h,data,1024)==0);
  for(int i=1023;i>=0;i--)CHECK(FN(BinaryHeapI64,Push)(h,i)==0);
  CHECK(FN(BinaryHeapI64,Push)(h,-1)==-1);
  for(int i=0;i<1024;i++){CHECK(FN(BinaryHeapI64,Pop)(h,&out)==0);CHECK(out==i);}
 }
 for(int n=0;n<=257;n++) {
  for(int i=0;i<n;i++)input[i]=(uint8_t)(i*13+n);
  memset(encoded,0xa5,sizeof(encoded));memset(decoded,0xa5,sizeof(decoded));
  int64_t e=FN(Base64,Encode)(b,input,n,encoded,sizeof(encoded));CHECK(e>=0);
  CHECK(encoded[e]==0xa5);
  CHECK(FN(Base64,Decode)(b,encoded,e,decoded,n)==n);
  CHECK(!memcmp(input,decoded,(size_t)n));CHECK(decoded[n]==0xa5);
  if(n){CHECK(FN(Base64,Decode)(b,encoded,e,decoded,n-1)==-1);}
 }
 uint8_t small[4]={0xa5,0xa5,0xa5,0xa5};
 CHECK(FN(Hex,Encode)(hex,input,3,small,4)==-1);CHECK(small[0]==0xa5);
 CHECK(FN(Base64,Decode)(b,(uint8_t*)"AB==",4,small,4)==-2);CHECK(small[0]==0xa5);
 for(uint32_t cp=0;cp<=0x10ffff;cp+=31){
  int n=FN(Utf8,Encode)(u,cp,small,4); int32_t width=0;
  if(cp>=0xd800&&cp<=0xdfff){CHECK(n==-2);continue;}
  CHECK(n>=1&&n<=4);CHECK(FN(Utf8,DecodeFirst)(u,small,n,&width)==(int32_t)cp);CHECK(width==n);
 }
 out=7;CHECK(FN(CheckedInt,Add)(ci,INT64_MAX,1,&out)==-2);CHECK(out==7);
 CHECK(FN(CheckedInt,Multiply)(ci,INT64_MIN,-1,&out)==-2);
 CHECK(FN(CheckedInt,Divide)(ci,INT64_MIN,-1,&out)==-2);
 FN(AlgorithmsI64,delete)(a);FN(ArrayVectorI64,delete)(v);FN(BinaryHeapI64,delete)(h);
 FN(Base64,delete)(b);FN(Hex,delete)(hex);FN(Utf8,delete)(u);FN(CheckedInt,delete)(ci);
 puts("C ABI and memory-boundary stress: PASS"); return 0;
}
