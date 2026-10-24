"""Model-based checks for the automatically continued production iterations."""
def run(ctx):
    C,call,eq,arr,buf,rng=(ctx[n] for n in ('C','call','eq','arr','buf','rng'))
    if 'HashMapI64' in ctx['handles']:
        cls='HashMapI64';out=C.c_int64(918)
        for cap in [0,1,2,7,32,67]:
            keys,values,states=arr([0]*cap),arr([0]*cap),buf(b'\xff'*cap)
            eq(call(cls,'Bind',keys,values,states,cap),0);eq(call(cls,'Capacity'),cap);model={}
            for _ in range(3000):
                key=rng.choice([-(2**63),2**63-1,rng.randrange(-60,60)]);value=rng.randint(-(2**63),2**63-1);op=rng.randrange(4)
                if op==0:
                    good=key in model or len(model)<cap
                    eq(call(cls,'Put',key,value),0 if good else -1)
                    if good:model[key]=value
                elif op==1:
                    eq(call(cls,'Remove',key),0 if key in model else -1);model.pop(key,None)
                elif op==2:
                    out.value=918;eq(call(cls,'Get',key,C.byref(out)),0 if key in model else -1);eq(out.value,model.get(key,918))
                else:eq(call(cls,'Contains',key),int(key in model))
                eq(call(cls,'Length'),len(model))
            found={};slot=-1
            while True:
                slot=call(cls,'NextSlot',slot)
                if slot<0:break
                k=C.c_int64();v=C.c_int64();eq(call(cls,'KeyAt',slot,C.byref(k)),0);eq(call(cls,'ValueAt',slot,C.byref(v)),0);found[k.value]=v.value
            eq(found,model)
            eq(call(cls,'NextSlot',-2),-1)
            for method in ['KeyAt','ValueAt']:
                eq(call(cls,method,-1,C.byref(out)),-1);eq(call(cls,method,cap,C.byref(out)),-1);eq(call(cls,method,0,None),-1)
            eq(call(cls,'Get',0,None),-1)
            # Clear restores empty slots even after a table entirely of tombstones.
            call(cls,'Clear');eq(call(cls,'Length'),0)
            for i in range(cap):eq(call(cls,'Put',i,i),0)
            for i in range(cap):eq(call(cls,'Remove',i),0)
            for i in range(cap):eq(call(cls,'Put',i+100,0),0)
        eq(call(cls,'Bind',None,None,None,-1),-1);eq(call(cls,'Bind',None,None,None,1),-1)
        eq(call(cls,'Bind',keys,keys,states,cap),-1)
        print('production_hash_map: PASS',flush=True)

    if 'HashSetI64' in ctx['handles']:
        cls='HashSetI64';out=C.c_int64(918)
        for cap in [0,1,3,16,71]:
            keys,states=arr([0]*cap),buf(b'\xff'*cap);eq(call(cls,'Bind',keys,states,cap),0);eq(call(cls,'Capacity'),cap);model=set()
            for _ in range(3000):
                key=rng.randrange(-100,100);op=rng.randrange(3)
                if op==0:
                    rc=1 if key in model else 0 if len(model)<cap else -1
                    eq(call(cls,'Insert',key),rc)
                    if rc>=0:model.add(key)
                elif op==1:eq(call(cls,'Remove',key),0 if key in model else -1);model.discard(key)
                else:eq(call(cls,'Contains',key),int(key in model))
                eq(call(cls,'Length'),len(model))
            found=set();slot=-1
            while True:
                slot=call(cls,'NextSlot',slot)
                if slot<0:break
                eq(call(cls,'KeyAt',slot,C.byref(out)),0);found.add(out.value)
            eq(found,model);eq(call(cls,'NextSlot',-2),-1);eq(call(cls,'KeyAt',-1,C.byref(out)),-1);eq(call(cls,'KeyAt',0,None),-1)
            call(cls,'Clear');eq(call(cls,'Length'),0)
            for key in [-(2**63),2**63-1]:
                rc=call(cls,'Insert',key);eq(rc,0 if call(cls,'Length')<=cap and cap>0 else -1)
                if rc==0:eq(call(cls,'Remove',key),0)
        eq(call(cls,'Bind',None,None,-1),-1);eq(call(cls,'Bind',None,None,1),-1)
        print('production_hash_set: PASS',flush=True)
    if 'MultiMapI64' in ctx['handles']:
        cls='MultiMapI64';out=C.c_int64()
        for cap in [0,1,3,32]:
            keys,values=arr([0]*cap),arr([0]*cap);eq(call(cls,'Bind',keys,values,cap),0);eq(call(cls,'Capacity'),cap);model=[]
            for _ in range(1500):
                key=rng.randrange(-8,8);value=rng.randrange(-1000,1000);op=rng.randrange(5)
                if op==0:
                    eq(call(cls,'Insert',key,value),0 if len(model)<cap else -1)
                    if len(model)<cap:model.append((key,value))
                elif op==1:
                    eq(call(cls,'RemoveOne',key),0 if any(k==key for k,v in model) else -1)
                    for i,(k,v) in enumerate(model):
                        if k==key:model.pop(i);break
                elif op==2:
                    eq(call(cls,'RemoveAll',key),sum(k==key for k,v in model));model=[(k,v) for k,v in model if k!=key]
                elif op==3:eq(call(cls,'Count',key),sum(k==key for k,v in model))
                else:
                    found=[];i=-1
                    while True:
                        i=call(cls,'FindNext',key,i)
                        if i<0:break
                        found.append(i)
                    eq(found,[i for i,(k,v) in enumerate(model) if k==key])
                eq(call(cls,'Length'),len(model))
                for i,(k,v) in enumerate(model):
                    eq(call(cls,'KeyAt',i,C.byref(out)),0);eq(out.value,k);eq(call(cls,'ValueAt',i,C.byref(out)),0);eq(out.value,v)
            for m in ['KeyAt','ValueAt']:eq(call(cls,m,-1,C.byref(out)),-1);eq(call(cls,m,0,None),-1)
            eq(call(cls,'FindNext',0,-2),-1);call(cls,'Clear');eq(call(cls,'Length'),0)
        eq(call(cls,'Bind',None,None,-1),-1);eq(call(cls,'Bind',None,None,1),-1);eq(call(cls,'Bind',keys,keys,cap),-1)
        print('production_multi_map: PASS',flush=True)
    if 'StackI64' in ctx['handles']:
        cls='StackI64';out=C.c_int64(918)
        for cap in [0,1,2,31]:
            storage=arr([0]*cap);eq(call(cls,'Bind',storage,cap),0);eq(call(cls,'Capacity'),cap);model=[]
            for _ in range(1500):
                op=rng.randrange(4);value=rng.randint(-(2**63),2**63-1)
                if op==0:
                    eq(call(cls,'Push',value),0 if len(model)<cap else -1)
                    if len(model)<cap:model.append(value)
                elif op==1:
                    out.value=918;eq(call(cls,'Pop',C.byref(out)),0 if model else -1);eq(out.value,model.pop() if model else 918)
                elif op==2:
                    out.value=918;eq(call(cls,'Peek',C.byref(out)),0 if model else -1);eq(out.value,model[-1] if model else 918)
                else:call(cls,'Clear');model=[]
                eq(call(cls,'Length'),len(model))
            eq(call(cls,'Pop',None),-1);eq(call(cls,'Peek',None),-1)
        eq(call(cls,'Bind',None,-1),-1);eq(call(cls,'Bind',None,1),-1)
        print('production_stack: PASS',flush=True)
    if 'AlgorithmsI64.MergeSort' in ctx['calls']:
        cls='AlgorithmsI64'
        for n in list(range(70))+[rng.randrange(500) for _ in range(500)]:
            values=[rng.randint(-(2**63),2**63-1) for _ in range(n)];data=arr(values);scratch=arr([0]*n)
            eq(call(cls,'MergeSort',data,n,scratch,n),0);eq(list(data)[:n],sorted(values))
        data=arr([3,2,1]);scratch=arr([88]*3)
        for args in [(data,3,scratch,2),(data,3,data,3),(None,1,scratch,3),(data,-1,scratch,3),(data,3,None,3)]:
            eq(call(cls,'MergeSort',*args),-1);eq(list(data),[3,2,1]);eq(list(scratch),[88]*3)
        eq(call(cls,'MergeSort',None,0,None,0),0);eq(call(cls,'MergeSort',data,1,None,0),0)
        print('production_merge_sort: PASS',flush=True)
    if 'AlgorithmsI64.SumChecked' in ctx['calls']:
        lo,hi=-(2**63),2**63-1;out=C.c_int64()
        samples=[([hi,1],0),([lo,-1],0),([hi,1,-1],0),([lo,hi],0),([],hi)]
        samples += [([rng.randint(lo,hi) for _ in range(rng.randrange(15))],rng.randint(lo,hi)) for _ in range(1500)]
        for values,initial in samples:
            total=initial;good=True
            for v in values:
                total+=v
                if not lo<=total<=hi:good=False;break
            out.value=918;eq(call('AlgorithmsI64','SumChecked',arr(values),len(values),initial,C.byref(out)),0 if good else -2);eq(out.value,total if good else 918)
        eq(call('AlgorithmsI64','SumChecked',None,1,0,C.byref(out)),-1);eq(call('AlgorithmsI64','SumChecked',None,0,0,None),-1)
        eq(call('AlgorithmsI64','SumChecked',None,-1,0,C.byref(out)),-1)
        print('production_checked_sum: PASS',flush=True)
    if 'Utf8.DecodeTo32' in ctx['calls']:
        for _ in range(1000):
            points=[rng.randrange(0x110000) for _ in range(rng.randrange(40))];points=[v for v in points if not 0xd800<=v<=0xdfff]
            data=''.join(map(chr,points)).encode();wide=(C.c_uint32*max(1,len(points)))(*points);out32=(C.c_uint32*max(1,len(points)))();out=buf(b'\xa5'*max(1,len(data)))
            eq(call('Utf8','EncodedLength32',wide,len(points)),len(data));eq(call('Utf8','EncodeFrom32',wide,len(points),out,len(data)),len(data));eq(bytes(out)[:len(data)],data)
            eq(call('Utf8','DecodeTo32',buf(data),len(data),out32,len(points)),len(points));eq(list(out32)[:len(points)],points)
        for point in [0xd800,0xdfff,0x110000,0xffffffff]:
            wide=(C.c_uint32*1)(point);out=buf(b'\xa5'*4)
            eq(call('Utf8','EncodedLength32',wide,1),-2);eq(call('Utf8','EncodeFrom32',wide,1,out,4),-2);eq(bytes(out),b'\xa5'*4)
        wide=(C.c_uint32*2)(0x12345678,0x12345678)
        for data in [b'\xff',b'A\xf0\x80\x80\x80',b'\xed\xa0\x80']:
            eq(call('Utf8','DecodeTo32',buf(data),len(data),wide,2),-2);eq(list(wide),[0x12345678]*2)
        eq(call('Utf8','DecodeTo32',buf(b'AB'),2,wide,1),-1);eq(list(wide),[0x12345678]*2)
        eq(call('Utf8','EncodeFrom32',wide,0,None,0),0);eq(call('Utf8','EncodedLength32',None,-1),-1)
        print('production_utf32_transcode: PASS',flush=True)
    if 'Utf16' in ctx['handles']:
        for mode,codec in [(0,'utf-16-le'),(1,'utf-16-be')]:
            for point in [0,0x7f,0x80,0xd7ff,0xe000,0xffff,0x10000,0x10ffff]+[rng.randrange(0x110000) for _ in range(1500)]:
                if 0xd800<=point<=0xdfff:continue
                data=chr(point).encode(codec);out=buf(b'\xa5'*6);consumed=C.c_int32(99)
                eq(call('Utf16','Encode',point,out,4,mode),len(data));eq(bytes(out),data+b'\xa5'*(6-len(data)))
                eq(call('Utf16','DecodeFirst',buf(data),len(data),mode,C.byref(consumed)),point);eq(consumed.value,len(data));eq(call('Utf16','Count',buf(data*3),len(data)*3,mode),3)
                eq(call('Utf16','Encode',point,out,len(data)-1,mode),-1)
            for data in [b'\0',b'\x00\xd8',b'\x00\xdc',b'\x00\xd8A\0',b'A\0\0']:
                if mode:data=b''.join(data[i:i+2][::-1] for i in range(0,len(data),2))
                eq(call('Utf16','Count',buf(data),len(data),mode),-2)
            eq(call('Utf16','Count',None,0,mode),0)
        for point in [0xd800,0xdfff,0x110000]:
            out=buf(b'\xa5'*4);eq(call('Utf16','Encode',point,out,4,0),-2);eq(bytes(out),b'\xa5'*4)
        consumed=C.c_int32(99);eq(call('Utf16','DecodeFirst',None,0,0,C.byref(consumed)),-1);eq(consumed.value,0)
        eq(call('Utf16','DecodeFirst',None,0,0,None),-1);eq(call('Utf16','Count',None,0,2),-1);eq(call('Utf16','Encode',65,None,4,0),-1);eq(call('Utf16','Encode',65,buf(b'xx'),2,2),-1)
        print('production_utf16: PASS',flush=True)
    if 'IntegerText' in ctx['handles']:
        def format_int(value,base):
            sign='-' if value<0 else '';value=abs(value);digits='0123456789abcdefghijklmnopqrstuvwxyz';text=''
            while value:text=digits[value%base]+text;value//=base
            return (sign+(text or '0')).encode()
        for signed,typ,scalar,lo,hi in [(True,'I64',C.c_int64,-2**63,2**63-1),(False,'U64',C.c_uint64,0,2**64-1)]:
            for value in [lo,hi,0,1]+[rng.randint(lo,hi) for _ in range(800)]:
                for base in [2,8,10,16,36,rng.randrange(2,37)]:
                    text=format_int(value,base);out=buf(b'\xa5'*70);number=scalar(918)
                    eq(call('IntegerText','Format'+typ,value,base,out,70),len(text));eq(bytes(out),text+b'\xa5'*(70-len(text)))
                    eq(call('IntegerText','Parse'+typ,buf(text.upper()),len(text),base,C.byref(number)),0);eq(number.value,value)
                    before=bytes(out);eq(call('IntegerText','Format'+typ,value,base,out,len(text)-1),-1);eq(bytes(out),before)
            for value in [lo-1,hi+1]:
                text=str(value).encode();number=scalar(918);rc=-2 if not signed and value<0 else -3
                eq(call('IntegerText','Parse'+typ,buf(text),len(text),10,C.byref(number)),rc);eq(number.value,918)
            for text in [b'',b' ',b'+',b'-',b'12x',b'1\0',b' 1',b'1 ']:
                number=scalar(918);eq(call('IntegerText','Parse'+typ,buf(text),len(text),10,C.byref(number)),-2);eq(number.value,918)
            number=scalar(918)
            for base in [0,1,37]:
                eq(call('IntegerText','Parse'+typ,buf(b'1'),1,base,C.byref(number)),-1);eq(call('IntegerText','Format'+typ,1,base,buf(b'xxxx'),4),-1)
            eq(call('IntegerText','Parse'+typ,None,1,10,C.byref(number)),-1);eq(call('IntegerText','Parse'+typ,None,0,10,None),-1)
        number=C.c_int64();eq(call('IntegerText','ParseI64',buf(b'+123'),4,10,C.byref(number)),0);eq(number.value,123)
        print('production_integer_text: PASS',flush=True)
    # One complete Gregorian leap-cycle, independently checked against datetime.
    import datetime,calendar
    day=datetime.date(1600,1,1);end=datetime.date(2000,1,1);epoch=datetime.date(1970,1,1)
    while day<end:
        eq(call('Date','DaysSinceEpoch',day.year,day.month,day.day),(day-epoch).days)
        eq(call('Date','Weekday',day.year,day.month,day.day),(day.weekday()+1)%7)
        eq(call('Date','IsValid',day.year,day.month,day.day),1)
        if day.day==1:eq(call('Date','DaysInMonth',day.year,day.month),calendar.monthrange(day.year,day.month)[1])
        day+=datetime.timedelta(days=1)
    for year in [-(2**31),-1,0,10000,2**31-1]:
        eq(call('Date','DaysSinceEpoch',year,1,1),-(2**63));eq(call('Date','Weekday',year,1,1),-1)
    for year,month,day in [(1,1,1),(9999,12,31),(2000,2,29),(1900,2,28)]:
        eq(call('Date','DaysSinceEpoch',year,month,day),(datetime.date(year,month,day)-epoch).days)
    print('production_gregorian_cycle: PASS; 146097 dates',flush=True)
    if 'HashMapI64' in ctx['handles']:
        # Discover colliding keys through observable table placement, without
        # duplicating the implementation's hash formula in the oracle.
        out=C.c_int64()
        for cap in [1,2,17,32]:
            keys,values,states=arr([0]*cap),arr([0]*cap),buf(b'\0'*cap)
            eq(call('HashMapI64','Bind',keys,values,states,cap),0);groups={};colliders=[]
            for candidate in range(20000):
                eq(call('HashMapI64','Put',candidate,candidate),0)
                slot=list(states)[:cap].index(1);groups.setdefault(slot,[]).append(candidate)
                call('HashMapI64','Clear')
                if len(groups[slot])>=cap*2:colliders=groups[slot];break
            eq(bool(colliders),True)
            for key in colliders[:cap]:eq(call('HashMapI64','Put',key,key),0)
            for key in colliders[:cap:2]:eq(call('HashMapI64','Remove',key),0)
            survivors=colliders[1:cap:2]
            for key in survivors:eq(call('HashMapI64','Put',key,-key),0)
            eq(call('HashMapI64','Length'),len(survivors))
            for key in survivors:eq(call('HashMapI64','Get',key,C.byref(out)),0);eq(out.value,-key)
            fresh=colliders[cap:cap+cap-len(survivors)]
            for key in fresh:eq(call('HashMapI64','Put',key,key),0)
            eq(call('HashMapI64','Length'),cap)
            for key in survivors+fresh:eq(call('HashMapI64','Remove',key),0)
            eq(call('HashMapI64','Contains',-1),0)
            eq(call('HashSetI64','Bind',keys,states,cap),0)
            for key in colliders[:cap]:eq(call('HashSetI64','Insert',key),0)
            for key in colliders[:cap:2]:eq(call('HashSetI64','Remove',key),0)
            for key in survivors:eq(call('HashSetI64','Insert',key),1)
            eq(call('HashSetI64','Length'),len(survivors))
        print('production_adversarial_hash_collisions: PASS',flush=True)
    if 'HashMapI64' in ctx['handles']:
        import random
        from concurrent.futures import ThreadPoolExecutor
        classes=['HashMapI64','HashSetI64','RedBlackTreeI64','SListI64','DListI64','QueueI64','StackI64']
        constructors={c:getattr(ctx['lib'],'CMotiveAndObjective__'+c+'__new') for c in classes}
        destructors={c:getattr(ctx['lib'],'CMotiveAndObjective__'+c+'__delete') for c in classes}
        for f in destructors.values():f.argtypes=[C.c_void_p];f.restype=None
        def worker(seed):
            local=random.Random(seed);count=0;objects={c:f() for c,f in constructors.items()}
            def check(a,b):
                nonlocal count
                count+=1
                if a!=b:raise AssertionError((seed,a,b))
            def native(c,m,*args):return ctx['calls'][c+'.'+m](objects[c],*args)
            storage=[arr([0]*64) for _ in range(5)];states=[buf(b'\0'*64) for _ in range(2)];out=C.c_int64()
            try:
                for h in objects.values():check(bool(h),True)
                check(native('HashMapI64','Bind',storage[0],storage[1],states[0],64),0);check(native('HashSetI64','Bind',storage[2],states[1],64),0)
                check(native('QueueI64','Bind',storage[3],64),0);check(native('StackI64','Bind',storage[4],64),0)
                mapping={};members=set();tree=set();sl=[];dl=[]
                for i in range(500):
                    key=local.randrange(31);value=local.randrange(-10000,10000)
                    check(native('HashMapI64','Put',key,value),0);mapping[key]=value;check(native('HashMapI64','Get',key,C.byref(out)),0);check(out.value,value)
                    if i%2:
                        check(native('HashSetI64','Remove',key),0 if key in members else -1);members.discard(key)
                        check(native('RedBlackTreeI64','Remove',key),0 if key in tree else -1);tree.discard(key)
                    else:
                        check(native('HashSetI64','Insert',key),1 if key in members else 0);members.add(key)
                        check(native('RedBlackTreeI64','Insert',key),1 if key in tree else 0);tree.add(key)
                    check(native('HashSetI64','Length'),len(members));check(native('RedBlackTreeI64','Length'),len(tree))
                    if i%3==0:check(native('SListI64','PushFront',value),0);sl.insert(0,value)
                    else:
                        out.value=918;check(native('SListI64','PopFront',C.byref(out)),0 if sl else -1);check(out.value,sl.pop(0) if sl else 918)
                    check(native('DListI64','PushBack',value),0);dl.append(value)
                    if i%2:check(native('DListI64','PopFront',C.byref(out)),0);check(out.value,dl.pop(0))
                    check(native('QueueI64','PushBack',value),0);check(native('QueueI64','PopFront',C.byref(out)),0);check(out.value,value)
                    check(native('StackI64','Push',value),0);check(native('StackI64','Pop',C.byref(out)),0);check(out.value,value)
                for key,value in mapping.items():check(native('HashMapI64','Get',key,C.byref(out)),0);check(out.value,value)
                return count
            finally:
                for cls,h in objects.items():destructors[cls](h)
        with ThreadPoolExecutor(max_workers=12) as pool:totals=list(pool.map(worker,range(12)))
        ctx['checks']+=sum(totals);eq(len(totals),12)
        print('production_independent_container_concurrency: PASS; '+str(sum(totals))+' checks',flush=True)
    # Deterministic malformed-input fuzzing against independent standard codecs.
    import base64,urllib.parse,re,random
    for seed in [0,1,391724,0xc0ffee,0xdeadbeef]:
        fuzz=random.Random(seed)
        for i in range(2500):
            raw=fuzz.randbytes(fuzz.randrange(65));mode=i%6
            if mode==0:data=base64.b64encode(raw)
            elif mode==1:data=raw.hex().encode()
            elif mode==2:data=urllib.parse.quote_from_bytes(raw,safe='').encode()
            elif mode==3:data=fuzz.choice([b'AB==',b'AAB=',b'====',b'%0',b'%Q0',b'\xed\xa0\x80',b'\xf4\x90\x80\x80'])
            else:data=raw
            try:
                decoded=base64.b64decode(data,validate=True);valid=base64.b64encode(decoded)==data
            except ValueError:valid=False;decoded=b''
            out=buf(b'\xa5'*300);rc=call('Base64','Decode',buf(data),len(data),out,300)
            eq(rc,len(decoded) if valid else -1 if len(data)%4 else -2)
            eq(bytes(out),(decoded+b'\xa5'*(300-len(decoded))) if valid else b'\xa5'*300)
            valid=len(data)%2==0 and re.fullmatch(b'[0-9a-fA-F]*',data) is not None
            decoded=bytes.fromhex(data.decode('ascii')) if valid else b'';out=buf(b'\xa5'*300)
            eq(call('Hex','Decode',buf(data),len(data),out,300),len(decoded) if valid else -1 if len(data)%2 else -2)
            eq(bytes(out),decoded+b'\xa5'*(300-len(decoded)) if valid else b'\xa5'*300)
            valid=True;j=0
            while j<len(data):
                if data[j]==37:
                    if j+2>=len(data) or re.fullmatch(b'[0-9a-fA-F]{2}',data[j+1:j+3]) is None:valid=False;break
                    j+=3
                else:j+=1
            decoded=urllib.parse.unquote_to_bytes(data) if valid else b'';out=buf(b'\xa5'*300)
            eq(call('Uri','DecodeComponent',buf(data),len(data),out,300),len(decoded) if valid else -2)
            eq(bytes(out),decoded+b'\xa5'*(300-len(decoded)) if valid else b'\xa5'*300)
            for cls,endian in [('Utf8',None),('Utf16',0),('Utf16',1)]:
                codec='utf-8' if endian is None else 'utf-16-be' if endian else 'utf-16-le'
                try:expected=len(data.decode(codec,'strict'))
                except UnicodeError:expected=-2
                args=(buf(data),len(data)) if endian is None else (buf(data),len(data),endian)
                eq(call(cls,'Count',*args),expected)
    print('production_malformed_codec_fuzz: PASS; 5 seeds and 12500 inputs',flush=True)
