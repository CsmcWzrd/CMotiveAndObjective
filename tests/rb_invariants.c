/* Verification fixture, not a library implementation. BSL-1.0.
 * Include generated code so an independent checker can inspect private nodes.
 */
#if !defined(_WIN32)
#ifndef _DEFAULT_SOURCE
#define _DEFAULT_SOURCE 1
#endif
#ifndef _DARWIN_C_SOURCE
#define _DARWIN_C_SOURCE 1
#endif
#endif
#include <stdlib.h>
#include <stdio.h>
static long live_allocations;
static int fail_allocations;
static void *tracked_malloc(size_t n){if(fail_allocations)return NULL;void*p=malloc(n);if(p)live_allocations++;return p;}
static void *tracked_calloc(size_t n,size_t s){if(fail_allocations)return NULL;void*p=calloc(n,s);if(p)live_allocations++;return p;}
static void tracked_free(void*p){if(p)live_allocations--;free(p);}
#define malloc tracked_malloc
#define calloc tracked_calloc
#define free tracked_free
#include "CMotiveAndObjective.c"
#undef malloc
#undef calloc
#undef free
#define CHECK(x) do{if(!(x)){fprintf(stderr,"RB invariant failure at line %d\n",__LINE__);exit(1);}}while(0)
static int64_t visited;
static int verify_node(RBNode *node,RBNode *parent,int depth,int has_lo,int64_t lo,int has_hi,int64_t hi) {
 if(!node)return 1;
 CHECK(depth<128);CHECK(node->parent==parent);
 CHECK(!has_lo||node->value>lo);CHECK(!has_hi||node->value<hi);
 RBNode *left=node->left,*right=node->right;
 CHECK(node->red==0||node->red==1);
 if(node->red){CHECK(!left||!left->red);CHECK(!right||!right->red);}
 int a=verify_node(left,node,depth+1,has_lo,lo,1,node->value);
 int b=verify_node(right,node,depth+1,1,node->value,has_hi,hi);
 CHECK(a==b);visited++;return a+(node->red?0:1);
}
static void verify(RedBlackTreeI64 *tree,int64_t expected) {
 visited=0;CHECK(!tree->root||!tree->root->red);CHECK(!tree->root||!tree->root->parent);
 verify_node(tree->root,NULL,0,0,0,0,0);CHECK(visited==expected);CHECK(tree->count==expected);
}
int main(void) {
 RedBlackTreeI64 *tree=CMotiveAndObjective__RedBlackTreeI64__new();CHECK(tree);
 uint64_t state=0x391724;unsigned char model[2048]={0};int64_t count=0;
 for(int i=0;i<40000;i++){
  state^=state<<13;state^=state>>7;state^=state<<17;int key=(int)(state%2048);
  if(state&0x10000){
   CHECK(CMotiveAndObjective__RedBlackTreeI64__Insert(tree,key)==(model[key]?1:0));
   if(!model[key]){model[key]=1;count++;}
  }else{
   CHECK(CMotiveAndObjective__RedBlackTreeI64__Remove(tree,key)==(model[key]?0:-1));
   if(model[key]){model[key]=0;count--;}
  }
  verify(tree,count);
 }
 CMotiveAndObjective__RedBlackTreeI64__Clear(tree);verify(tree,0);
 for(int pass=0;pass<2;pass++){
  for(int i=0;i<3000;i++){int key=pass?2999-i:i;CHECK(CMotiveAndObjective__RedBlackTreeI64__Insert(tree,key)==0);verify(tree,i+1);}
  for(int i=0;i<3000;i++){int key=pass?i:2999-i;CHECK(CMotiveAndObjective__RedBlackTreeI64__Remove(tree,key)==0);verify(tree,2999-i);}
 }
 fail_allocations=1;
 CHECK(CMotiveAndObjective__RedBlackTreeI64__new()==NULL);
 CHECK(CMotiveAndObjective__SListI64__new()==NULL);
 CHECK(CMotiveAndObjective__DListI64__new()==NULL);
 CHECK(CMotiveAndObjective__RedBlackTreeI64__Insert(tree,42)==-2);verify(tree,0);
 fail_allocations=0;
 CHECK(CMotiveAndObjective__RedBlackTreeI64__Insert(tree,42)==0);
 fail_allocations=1;
 CHECK(CMotiveAndObjective__RedBlackTreeI64__Insert(tree,42)==1);
 CHECK(CMotiveAndObjective__RedBlackTreeI64__Insert(tree,43)==-2);verify(tree,1);
 fail_allocations=0;
 SListI64 *sl=CMotiveAndObjective__SListI64__new();DListI64 *dl=CMotiveAndObjective__DListI64__new();CHECK(sl&&dl);
 fail_allocations=1;
 CHECK(CMotiveAndObjective__SListI64__PushBack(sl,9)==-2);
 CHECK(CMotiveAndObjective__SListI64__PushFront(sl,9)==-2);
 CHECK(CMotiveAndObjective__DListI64__PushBack(dl,9)==-2);
 CHECK(CMotiveAndObjective__DListI64__PushFront(dl,9)==-2);
 CHECK(!sl->count&&!dl->count);fail_allocations=0;
 for(int i=0;i<1000;i++){CHECK(CMotiveAndObjective__SListI64__PushBack(sl,i)==0);CHECK(CMotiveAndObjective__DListI64__PushFront(dl,i)==0);}
 CMotiveAndObjective__SListI64__delete(sl);CMotiveAndObjective__DListI64__delete(dl);
 CMotiveAndObjective__RedBlackTreeI64__Clear(tree);verify(tree,0);
 for(int i=0;i<1000;i++)CHECK(CMotiveAndObjective__RedBlackTreeI64__Insert(tree,i)==0);
 CMotiveAndObjective__RedBlackTreeI64__delete(tree);
 CHECK(live_allocations==0);
 puts("Red-black invariants, allocation-failure atomicity and tracked ownership cleanup: PASS");return 0;
}
