"""Capture checked scalar/typed-buffer calls for architecture-independent replay."""
import ctypes as C,hashlib,json,os
from pathlib import Path
class Recorder:
 def __init__(self,api):
  self.api=api;self.rows=[];self.count={};self.excluded={'ArrayVectorI64','BinaryHeapI64','SortedMapI64','QueueI64','SListI64','DListI64','RedBlackTreeI64','HashMapI64','HashSetI64','MultiMapI64','StackI64','Csv','Pcg32'}
 def snapshot(self,a,args):
  if a['cls'] in self.excluded or self.count.get(a['cls']+'.'+a['name'],0)>=10:return None
  buffers=[];values=[];seen=set()
  for (_,typ),value in zip(a['params'],args):
   if not typ.endswith('*'):values.append({'type':typ,'value':int(value)});continue
   if value is None:values.append({'type':typ,'null':True});continue
   obj=getattr(value,'_obj',value)
   if id(obj) in seen:return None
   seen.add(id(obj))
   if not isinstance(obj,(C.Array,C._SimpleCData)):return None
   seq=list(obj) if isinstance(obj,C.Array) else [obj.value]
   if not seq or len(seq)>1024 or not all(type(x)==int for x in seq):return None
   values.append({'type':typ,'before':seq});buffers.append((len(values)-1,obj))
  return values,buffers
 def capture(self,a,args,run):
  snap=self.snapshot(a,args);result=run()
  if snap is not None:
   values,buffers=snap
   for i,obj in buffers:values[i]['after']=list(obj) if isinstance(obj,C.Array) else [obj.value]
   key=a['cls']+'.'+a['name'];self.count[key]=self.count.get(key,0)+1
   self.rows.append({'api':a,'args':values,'result':result})
  return result
 def write(self,directory,source_fp,tests_fp):
  d=Path(directory);d.mkdir(parents=True,exist_ok=True)
  expected={a['cls']+'.'+a['name'] for a in self.api if a['cls'] not in self.excluded}
  assert set(self.count)==expected,expected-set(self.count)
  types={'I32':'int32_t','U32':'uint32_t','I64':'int64_t','U64':'uint64_t','Uchar':'uint8_t','Void':'void'}
  def ct(t):return ct(t[:-1])+'*' if t.endswith('*') else types[t]
  def number(x):
   if x<0:return '(-INT64_C('+str(-x-1)+')-1)'
   return 'UINT64_C('+str(x)+')'
  lines=['/* Generated only after the independent Python suite passed. */','#include <stdint.h>','#include <stddef.h>','#include <string.h>','#ifdef CMO_DYNAMIC_TEST','#include "CMotiveAndObjective.h"','#define INST(c) void*','#else','#include "CMotiveAndObjective.c"','#define INST(c) c*','#endif','static uint64_t cmo_checks;','void cmo_fail(void);','#define CHECK(x) do{ cmo_checks++; if(!(x)) cmo_fail(); }while(0)']
  for a in self.api:
   symbol='CMotiveAndObjective__'+a['cls']+'__'+a['name'];params=['INST('+a['cls']+')']+[ct(t) for n,t in a['params']]
   lines.append('static '+ct(a['returns'])+' (*volatile FP_'+a['cls']+'_'+a['name']+')('+','.join(params)+')='+symbol+';')
  lines.append('static void scalar_replay(void){')
  for row in self.rows:
   a=row['api'];cls=a['cls'];lines.append('{ INST('+cls+') self=CMotiveAndObjective__'+cls+'__new(); CHECK(self!=NULL);');args=['self']
   for i,v in enumerate(row['args']):
    t=v['type'];name='b'+str(i)
    if 'before' in v:
     lines.append(ct(t[:-1])+' '+name+'[]={'+','.join(map(number,v['before']))+'};');args.append(name)
    elif v.get('null'):args.append('NULL')
    else:args.append('('+ct(t)+')'+number(v['value']))
   expression='FP_'+cls+'_'+a['name']+'('+','.join(args)+')'
   if a['returns']=='Void':lines.append(expression+';')
   else:lines.append('CHECK('+expression+'==('+ct(a['returns'])+')'+number(row['result'])+');')
   for i,v in enumerate(row['args']):
    if 'after' in v:
     lines.append('{ '+ct(v['type'][:-1])+' expected[]={'+','.join(map(number,v['after']))+'}; for(size_t k=0;k<sizeof(expected)/sizeof(expected[0]);k++) CHECK(b'+str(i)+'[k]==expected[k]); }')
   lines.append('CMotiveAndObjective__'+cls+'__delete(self); }')
  lines+=['}','#ifdef CMO_CONTAINER_TEST','#include "portable_containers.h"','#endif','int main(void){ scalar_replay();','#ifdef CMO_CONTAINER_TEST','container_replay();','#endif','return 0; }']
  source='\n'.join(lines)+'\n';(d/'portable_replay.c').write_text(source)
  report={'status':'CAPTURED_AFTER_PASS','source_fingerprint':source_fp,'tests_fingerprint':tests_fp,'scalar_methods':len(expected),'cases':len(self.rows),'methods':sorted(expected),'replay_sha256':hashlib.sha256(source.encode()).hexdigest()};(d/'vectors.json').write_text(json.dumps(report,indent=2)+'\n')
