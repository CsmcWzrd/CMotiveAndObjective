/* Independent small public-API container models; BSL-1.0. */
#define M(c,m) FP_##c##_##m
#define NEW(c) INST(c) self=CMotiveAndObjective__##c##__new(); CHECK(self!=NULL)
#define DEL(c) CMotiveAndObjective__##c##__delete(self)
static void container_replay(void){
int64_t lo=INT64_MIN,hi=INT64_MAX,v=0;
{ NEW(ArrayVectorI64);
int64_t storage[8]; CHECK(M(ArrayVectorI64,Bind)(self,storage,8)==0);CHECK(M(ArrayVectorI64,Capacity)(self)==8);
CHECK(M(ArrayVectorI64,PushBack)(self,hi)==0);CHECK(M(ArrayVectorI64,Insert)(self,0,lo)==0);CHECK(M(ArrayVectorI64,PushBack)(self,0)==0);
CHECK(M(ArrayVectorI64,Set)(self,2,1)==0);M(ArrayVectorI64,Sort)(self);CHECK(M(ArrayVectorI64,At)(self,0,&v)==0&&v==lo);
CHECK(M(ArrayVectorI64,Length)(self)==3);CHECK(M(ArrayVectorI64,Erase)(self,1)==0);CHECK(M(ArrayVectorI64,PopBack)(self,&v)==0&&v==hi);M(ArrayVectorI64,Clear)(self);CHECK(M(ArrayVectorI64,Length)(self)==0);
DEL(ArrayVectorI64); }
{ NEW(BinaryHeapI64);
int64_t storage[8];CHECK(M(BinaryHeapI64,Bind)(self,storage,8)==0);CHECK(M(BinaryHeapI64,Push)(self,hi)==0);CHECK(M(BinaryHeapI64,Push)(self,lo)==0);CHECK(M(BinaryHeapI64,Length)(self)==2);CHECK(M(BinaryHeapI64,Peek)(self,&v)==0&&v==lo);CHECK(M(BinaryHeapI64,Pop)(self,&v)==0&&v==lo);M(BinaryHeapI64,Clear)(self);CHECK(M(BinaryHeapI64,Length)(self)==0);
DEL(BinaryHeapI64); }
{ NEW(StackI64);
int64_t storage[8];CHECK(M(StackI64,Bind)(self,storage,8)==0);CHECK(M(StackI64,Capacity)(self)==8);CHECK(M(StackI64,Push)(self,lo)==0);CHECK(M(StackI64,Push)(self,hi)==0);CHECK(M(StackI64,Length)(self)==2);CHECK(M(StackI64,Peek)(self,&v)==0&&v==hi);CHECK(M(StackI64,Pop)(self,&v)==0&&v==hi);M(StackI64,Clear)(self);CHECK(M(StackI64,Length)(self)==0);
DEL(StackI64); }
{ NEW(QueueI64);
int64_t storage[8];CHECK(M(QueueI64,Bind)(self,storage,8)==0);CHECK(M(QueueI64,Capacity)(self)==8);CHECK(M(QueueI64,PushBack)(self,lo)==0);CHECK(M(QueueI64,PushBack)(self,hi)==0);CHECK(M(QueueI64,Length)(self)==2);CHECK(M(QueueI64,Front)(self,&v)==0&&v==lo);CHECK(M(QueueI64,PopFront)(self,&v)==0&&v==lo);M(QueueI64,Clear)(self);CHECK(M(QueueI64,Length)(self)==0);
DEL(QueueI64); }
{ NEW(SortedMapI64);
int64_t keys[8],values[8];uint8_t states[8];CHECK(M(SortedMapI64,Bind)(self,keys,values,8)==0);CHECK(M(SortedMapI64,Capacity)(self)==8);CHECK(M(SortedMapI64,Put)(self,lo,hi)==0);CHECK(M(SortedMapI64,Length)(self)==1);CHECK(M(SortedMapI64,Contains)(self,lo)==1);CHECK(M(SortedMapI64,Get)(self,lo,&v)==0&&v==hi);int64_t slot=0;CHECK(M(SortedMapI64,KeyAt)(self,slot,&v)==0&&v==lo);CHECK(M(SortedMapI64,ValueAt)(self,slot,&v)==0&&v==hi);CHECK(M(SortedMapI64,Remove)(self,lo)==0);M(SortedMapI64,Clear)(self);CHECK(M(SortedMapI64,Length)(self)==0);
DEL(SortedMapI64); }
{ NEW(HashMapI64);
int64_t keys[8],values[8];uint8_t states[8];CHECK(M(HashMapI64,Bind)(self,keys,values,states,8)==0);CHECK(M(HashMapI64,Capacity)(self)==8);CHECK(M(HashMapI64,Put)(self,lo,hi)==0);CHECK(M(HashMapI64,Length)(self)==1);CHECK(M(HashMapI64,Contains)(self,lo)==1);CHECK(M(HashMapI64,Get)(self,lo,&v)==0&&v==hi);int64_t slot=M(HashMapI64,NextSlot)(self,-1);CHECK(M(HashMapI64,KeyAt)(self,slot,&v)==0&&v==lo);CHECK(M(HashMapI64,ValueAt)(self,slot,&v)==0&&v==hi);CHECK(M(HashMapI64,Remove)(self,lo)==0);M(HashMapI64,Clear)(self);CHECK(M(HashMapI64,Length)(self)==0);
DEL(HashMapI64); }
{ NEW(HashSetI64);
int64_t keys[8];uint8_t states[8];CHECK(M(HashSetI64,Bind)(self,keys,states,8)==0);CHECK(M(HashSetI64,Capacity)(self)==8);CHECK(M(HashSetI64,Insert)(self,lo)==0);CHECK(M(HashSetI64,Length)(self)==1);CHECK(M(HashSetI64,Contains)(self,lo)==1);int64_t slot=M(HashSetI64,NextSlot)(self,-1);CHECK(M(HashSetI64,KeyAt)(self,slot,&v)==0&&v==lo);CHECK(M(HashSetI64,Remove)(self,lo)==0);M(HashSetI64,Clear)(self);
DEL(HashSetI64); }
{ NEW(MultiMapI64);
int64_t keys[8],values[8];CHECK(M(MultiMapI64,Bind)(self,keys,values,8)==0);CHECK(M(MultiMapI64,Capacity)(self)==8);CHECK(M(MultiMapI64,Insert)(self,lo,hi)==0);CHECK(M(MultiMapI64,Insert)(self,lo,lo)==0);CHECK(M(MultiMapI64,Length)(self)==2);CHECK(M(MultiMapI64,Count)(self,lo)==2);CHECK(M(MultiMapI64,FindNext)(self,lo,-1)==0);CHECK(M(MultiMapI64,KeyAt)(self,0,&v)==0&&v==lo);CHECK(M(MultiMapI64,ValueAt)(self,0,&v)==0&&v==hi);CHECK(M(MultiMapI64,RemoveOne)(self,lo)==0);CHECK(M(MultiMapI64,RemoveAll)(self,lo)==1);M(MultiMapI64,Clear)(self);
DEL(MultiMapI64); }
{ NEW(SListI64);
CHECK(M(SListI64,PushFront)(self,lo)==0);CHECK(M(SListI64,PushBack)(self,hi)==0);CHECK(M(SListI64,Length)(self)==2);CHECK(M(SListI64,Front)(self,&v)==0&&v==lo);CHECK(M(SListI64,Back)(self,&v)==0&&v==hi);CHECK(M(SListI64,At)(self,1,&v)==0&&v==hi);void* cursor=M(SListI64,Begin)(self);CHECK(M(SListI64,Read)(self,cursor,&v)==0&&v==lo);cursor=M(SListI64,Next)(self,cursor);CHECK(M(SListI64,Read)(self,cursor,&v)==0&&v==hi);CHECK(M(SListI64,RemoveFirst)(self,hi)==0);CHECK(M(SListI64,PopFront)(self,&v)==0&&v==lo);M(SListI64,Clear)(self);CHECK(M(SListI64,Length)(self)==0);
DEL(SListI64); }
{ NEW(DListI64);
CHECK(M(DListI64,PushFront)(self,lo)==0);CHECK(M(DListI64,PushBack)(self,hi)==0);CHECK(M(DListI64,Length)(self)==2);CHECK(M(DListI64,Front)(self,&v)==0&&v==lo);CHECK(M(DListI64,Back)(self,&v)==0&&v==hi);CHECK(M(DListI64,At)(self,1,&v)==0&&v==hi);void* cursor=M(DListI64,Begin)(self);CHECK(M(DListI64,Read)(self,cursor,&v)==0&&v==lo);cursor=M(DListI64,Next)(self,cursor);CHECK(M(DListI64,Read)(self,cursor,&v)==0&&v==hi);cursor=M(DListI64,Last)(self);cursor=M(DListI64,Previous)(self,cursor);CHECK(M(DListI64,Read)(self,cursor,&v)==0&&v==lo);CHECK(M(DListI64,PopBack)(self,&v)==0&&v==hi);CHECK(M(DListI64,PushBack)(self,hi)==0);CHECK(M(DListI64,RemoveFirst)(self,hi)==0);CHECK(M(DListI64,PopFront)(self,&v)==0&&v==lo);M(DListI64,Clear)(self);CHECK(M(DListI64,Length)(self)==0);
DEL(DListI64); }
{ NEW(RedBlackTreeI64);
CHECK(M(RedBlackTreeI64,Insert)(self,hi)==0);CHECK(M(RedBlackTreeI64,Insert)(self,lo)==0);CHECK(M(RedBlackTreeI64,Insert)(self,0)==0);CHECK(M(RedBlackTreeI64,Length)(self)==3);CHECK(M(RedBlackTreeI64,Contains)(self,lo)==1);void* cursor=M(RedBlackTreeI64,Begin)(self);CHECK(M(RedBlackTreeI64,Read)(self,cursor,&v)==0&&v==lo);cursor=M(RedBlackTreeI64,Next)(self,cursor);CHECK(M(RedBlackTreeI64,Read)(self,cursor,&v)==0&&v==0);cursor=M(RedBlackTreeI64,Last)(self);cursor=M(RedBlackTreeI64,Previous)(self,cursor);CHECK(M(RedBlackTreeI64,Read)(self,cursor,&v)==0&&v==0);cursor=M(RedBlackTreeI64,LowerBound)(self,lo);CHECK(M(RedBlackTreeI64,Read)(self,cursor,&v)==0&&v==lo);cursor=M(RedBlackTreeI64,UpperBound)(self,lo);CHECK(M(RedBlackTreeI64,Read)(self,cursor,&v)==0&&v==0);CHECK(M(RedBlackTreeI64,Remove)(self,0)==0);M(RedBlackTreeI64,Clear)(self);
DEL(RedBlackTreeI64); }
{ NEW(Pcg32);
M(Pcg32,Seed)(self,42,54);CHECK(M(Pcg32,Next)(self)==UINT32_C(2707161783));uint32_t result=99;CHECK(M(Pcg32,Bounded)(self,1,&result)==0&&result==0);
DEL(Pcg32); }
{ NEW(Csv);
uint8_t input[]={'"','a',',','b','"',',','x',13,10},out[8];int32_t end=99;CHECK(M(Csv,Bind)(self,input,sizeof(input))==0);CHECK(M(Csv,Next)(self,out,8,&end)==3&&end==0);CHECK(out[0]=='a'&&out[1]==','&&out[2]=='b');CHECK(M(Csv,Next)(self,out,8,&end)==1&&end==1&&out[0]=='x');
DEL(Csv); }
}
#undef M
#undef NEW
#undef DEL
