/* Test fixture only. BSL-1.0. Linux hardware bounds checks, not a library wrapper. */
#define _DEFAULT_SOURCE 1
#if defined(_WIN32)
#include <windows.h>
#else
#include <sys/mman.h>
#include <unistd.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "CMotiveAndObjective.c"
#define A(c,m) CMotiveAndObjective__##c##__##m
static unsigned long checks;
#define CHECK(x) do{checks++;if(!(x)){fprintf(stderr,"guard check line %d\n",__LINE__);exit(1);}}while(0)
static size_t page;
#if defined(_WIN32)
static unsigned char*arena(void){unsigned char*p=VirtualAlloc(NULL,page*3,MEM_RESERVE|MEM_COMMIT,PAGE_NOACCESS);CHECK(p);DWORD old;CHECK(VirtualProtect(p+page,page,PAGE_READWRITE,&old));return p;}
static int release_arena(void*p){return VirtualFree(p,0,MEM_RELEASE)?0:-1;}
#else
static unsigned char *arena(void){unsigned char *p=mmap(NULL,page*3,PROT_NONE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);CHECK(p!=MAP_FAILED);CHECK(mprotect(p+page,page,PROT_READ|PROT_WRITE)==0);return p;}
static int release_arena(void*p){return munmap(p,page*3);}
#endif
int main(void){
#if defined(_WIN32)
 SYSTEM_INFO info;GetSystemInfo(&info);page=info.dwPageSize;
#else
 page=(size_t)sysconf(_SC_PAGESIZE);
#endif
 CHECK(page>=4096);
 unsigned char *x=arena(),*y=arena();
 Base64 *b=A(Base64,new)();Hex*h=A(Hex,new)();Uri*u=A(Uri,new)();Sha256*s=A(Sha256,new)();Bytes*z=A(Bytes,new)();Utf8*v=A(Utf8,new)();Utf16*w=A(Utf16,new)();
 CHECK(b&&h&&u&&s&&z&&v&&w);
 for(int n=0;n<=96;n++){
  unsigned char *in=x+2*page-n,original[96];for(int i=0;i<n;i++)in[i]=original[i]=(unsigned char)(i*73+n);
  CHECK(A(Bytes,Compare)(z,in,n,in,n)==0);CHECK(A(Bytes,CountByte)(z,in,n,0)>=0);
  int64_t size=A(Base64,EncodedLength)(b,n);unsigned char*out=y+2*page-size;
  CHECK(A(Base64,Encode)(b,in,n,out,size)==size);CHECK(A(Base64,Decode)(b,out,size,in,n)==n);CHECK(!memcmp(in,original,(size_t)n));
  size=n*2;out=y+2*page-size;CHECK(A(Hex,Encode)(h,in,n,out,size)==size);CHECK(A(Hex,Decode)(h,out,size,in,n)==n);CHECK(!memcmp(in,original,(size_t)n));
  size=A(Uri,EncodedLength)(u,in,n);out=y+2*page-size;CHECK(A(Uri,EncodeComponent)(u,in,n,out,size)==size);CHECK(A(Uri,DecodeComponent)(u,out,size,in,n)==n);CHECK(!memcmp(in,original,(size_t)n));
  CHECK(A(Sha256,Digest)(s,in,n,y+2*page-32,32)==32);
 }
 uint32_t points[]={0,0x7f,0x80,0x7ff,0x800,0xd7ff,0xe000,0xffff,0x10000,0x10ffff};
 for(unsigned i=0;i<sizeof(points)/sizeof(points[0]);i++){
  uint32_t cp=points[i];int len=cp<128?1:cp<2048?2:cp<65536?3:4;unsigned char*out=y+2*page-len;int32_t used=0;
  CHECK(A(Utf8,Encode)(v,cp,out,len)==len);CHECK(A(Utf8,DecodeFirst)(v,out,len,&used)==(int32_t)cp);CHECK(used==len);
  for(int mode=0;mode<2;mode++){len=cp<65536?2:4;out=y+2*page-len;CHECK(A(Utf16,Encode)(w,cp,out,len,mode)==len);CHECK(A(Utf16,DecodeFirst)(w,out,len,mode,&used)==(int32_t)cp);CHECK(used==len);}
 }
 for(int cap=0;cap<=31;cap++){
  unsigned char *ka=arena(),*va=arena(),*ta=arena();int64_t*keys=(int64_t*)(ka+2*page-cap*8);int64_t*values=(int64_t*)(va+2*page-cap*8);unsigned char*states=ta+2*page-cap;
  HashMapI64*map=A(HashMapI64,new)();CHECK(map);CHECK(A(HashMapI64,Bind)(map,keys,values,states,cap)==0);
  for(int i=0;i<cap;i++)CHECK(A(HashMapI64,Put)(map,i,i*7)==0);
  CHECK(A(HashMapI64,Put)(map,-1,0)==-1);
  for(int i=0;i<cap;i++){int64_t value=0;CHECK(A(HashMapI64,Get)(map,i,&value)==0);CHECK(value==i*7);CHECK(A(HashMapI64,Remove)(map,i)==0);}
  A(HashMapI64,delete)(map);CHECK(!release_arena(ka));CHECK(!release_arena(va));CHECK(!release_arena(ta));
 }
 A(Base64,delete)(b);A(Hex,delete)(h);A(Uri,delete)(u);A(Sha256,delete)(s);A(Bytes,delete)(z);A(Utf8,delete)(v);A(Utf16,delete)(w);
 CHECK(!release_arena(x));CHECK(!release_arena(y));printf("Hardware guard pages: PASS; %lu checks\n",checks);return 0;
}
