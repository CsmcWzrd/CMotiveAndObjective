#!/usr/bin/env python3
"""Independent behavioral oracles for every hand-written public CMotive method."""
import base64, bisect, ctypes as C, datetime, heapq, json, math, random, sys, zlib
import hashlib, urllib.parse, uuid, re, collections
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from emit_core import source_fingerprint
from release_checks import tests_fingerprint
API=json.loads((ROOT/'api.json').read_text())
T={'I32':C.c_int32,'U32':C.c_uint32,'I64':C.c_int64,'U64':C.c_uint64,
   'Uchar':C.c_ubyte,'Void':None}
def typ(t):
    if t=='Void*':return C.c_void_p
    return C.POINTER(T[t[:-1]]) if t.endswith('*') else T[t]
lib=C.CDLL(str(Path(sys.argv[1]).resolve()))
rng=random.Random(391724)
checks=0
seen=set()
handles={}
calls={}
for a in API:
    name=a['cls']+'.'+a['name']
    f=getattr(lib,'CMotiveAndObjective__'+a['cls']+'__'+a['name'])
    f.argtypes=[C.c_void_p]+[typ(t) for n,t in a['params']]
    f.restype=typ(a['returns'])
    calls[name]=f
for cls in dict.fromkeys(a['cls'] for a in API):
    f=getattr(lib,'CMotiveAndObjective__'+cls+'__new'); f.argtypes=[]; f.restype=C.c_void_p
    handles[cls]=f()
    if not handles[cls]: raise MemoryError(cls)
def call(cls,method,*args):
    seen.add(cls+'.'+method)
    return calls[cls+'.'+method](handles[cls],*args)
def eq(a,b):
    global checks
    checks+=1
    if a!=b: raise AssertionError(f'check {checks}: {a!r} != {b!r}')
def buf(data):
    return (C.c_ubyte*max(1,len(data)))(*data)
def arr(data):
    return (C.c_int64*max(1,len(data)))(*data)
def test_ascii():
    for c in range(-256,512):
        alpha=65<=c<=90 or 97<=c<=122
        digit=48<=c<=57
        ps={'IsAscii':0<=c<=127,'IsUpper':65<=c<=90,'IsLower':97<=c<=122,
            'IsAlpha':alpha,'IsDigit':digit,'IsAlnum':alpha or digit,
            'IsHexDigit':digit or 65<=c<=70 or 97<=c<=102,
            'IsWhite':c==32 or 9<=c<=13,'IsBlank':c in (9,32),
            'IsControl':0<=c<32 or c==127,'IsGraph':33<=c<=126,
            'IsPrint':32<=c<=126,'IsPunct':33<=c<=126 and not (alpha or digit)}
        for n,v in ps.items(): eq(call('Ascii',n,c),int(v))
        eq(call('Ascii','ToLower',c),c+32 if 65<=c<=90 else c)
        eq(call('Ascii','ToUpper',c),c-32 if 97<=c<=122 else c)
        h=chr(c).lower() if 0<=c<128 else '?'
        eq(call('Ascii','HexValue',c),int(h,16) if h in '0123456789abcdef' else -1)
def test_bits():
    mask=2**64-1
    for x in [0,1,mask,2**63]+[rng.getrandbits(64) for _ in range(1000)]:
        eq(call('BitManip','PopCount',x),x.bit_count())
        eq(call('BitManip','CountLeadingZeros',x),64-x.bit_length())
        eq(call('BitManip','CountTrailingZeros',x),(x&-x).bit_length()-1 if x else 64)
        eq(call('BitManip','ByteSwap',x),int.from_bytes(x.to_bytes(8,'big'),'little'))
        eq(call('BitManip','ReverseBits',x),int(f'{x:064b}'[::-1],2))
        eq(call('BitManip','IsPowerOfTwo',x),int(x>0 and x&(x-1)==0))
        for s in [0,1,31,63,64,127,2**32-1]:
            n=s%64
            eq(call('BitManip','RotateLeft',x,s),((x<<n)|(x>>(64-n)))&mask)
            eq(call('BitManip','RotateRight',x,s),((x>>n)|(x<<(64-n)))&mask)
def test_integer():
    lo,hi=-(2**63),2**63-1
    vals=[lo,lo+1,-2,-1,0,1,2,hi-1,hi]
    pairs=[(a,b) for a in vals for b in vals]+[(rng.randint(lo,hi),rng.randint(lo,hi)) for _ in range(1000)]
    for a,b in pairs:
        for method,value in [('Add',a+b),('Subtract',a-b),('Multiply',a*b)]:
            out=C.c_int64(1234); rc=call('CheckedInt',method,a,b,C.byref(out))
            good=lo<=value<=hi
            eq(rc,0 if good else -2); eq(out.value,value if good else 1234)
        out=C.c_int64(1234)
        rc=call('CheckedInt','Divide',a,b,C.byref(out))
        if not b: eq(rc,-1); eq(out.value,1234)
        elif a==lo and b==-1: eq(rc,-2); eq(out.value,1234)
        else:
            eq(rc,0); eq(out.value,(abs(a)//abs(b))*(-1 if (a<0)!=(b<0) else 1))
        out=C.c_int64(1234); rc=call('CheckedInt','Negate',a,C.byref(out))
        eq(rc,-2 if a==lo else 0); eq(out.value,1234 if a==lo else -a)
    for method in ['Add','Subtract','Multiply','Divide']: eq(call('CheckedInt',method,1,2,None),-1)
    eq(call('CheckedInt','Negate',1,None),-1)
    for a,b in [(0,0),(0,7),(2**64-1,2)]+[(rng.getrandbits(64),rng.getrandbits(64)) for _ in range(500)]:
        eq(call('IntegerMath','Gcd',a,b),math.gcd(a,b))
        eq(call('IntegerMath','Sqrt',a),math.isqrt(a))
        out=C.c_uint64(1234); v=math.lcm(a,b); good=v<2**64
        eq(call('IntegerMath','Lcm',a,b,C.byref(out)),0 if good else -2)
        eq(out.value,v if good else 1234)
    for x in [0,1,2,3,100,2**64-1]:
        for n in range(70):
            out=C.c_uint64(1234); v=x**n; good=v<2**64
            eq(call('IntegerMath','Power',x,n,C.byref(out)),0 if good else -2)
            eq(out.value,v if good else 1234)
    eq(call('IntegerMath','Lcm',1,1,None),-1)
    eq(call('IntegerMath','Power',1,1,None),-1)
def test_algorithms():
    for _ in range(300):
        values=[rng.randrange(-10,11) for _ in range(rng.randrange(120))]
        n=len(values); a=arr(values)
        eq(call('AlgorithmsI64','IsSorted',a,n),int(values==sorted(values)))
        eq(call('AlgorithmsI64','Find',a,n,3),values.index(3) if 3 in values else -1)
        eq(call('AlgorithmsI64','Count',a,n,3),values.count(3))
        eq(call('AlgorithmsI64','MinIndex',a,n),values.index(min(values)) if n else -1)
        eq(call('AlgorithmsI64','MaxIndex',a,n),values.index(max(values)) if n else -1)
        eq(call('AlgorithmsI64','Reverse',a,n),0); eq(list(a)[:n],values[::-1])
        k=rng.randrange(500); a=arr(values)
        eq(call('AlgorithmsI64','RotateLeft',a,n,k),0)
        j=k%n if n else 0; eq(list(a)[:n],values[j:]+values[:j])
        a=arr(values); eq(call('AlgorithmsI64','HeapSort',a,n),0)
        v=sorted(values); eq(list(a)[:n],v)
        for x in [-15,0,3,15]:
            eq(call('AlgorithmsI64','LowerBound',a,n,x),bisect.bisect_left(v,x))
            eq(call('AlgorithmsI64','UpperBound',a,n,x),bisect.bisect_right(v,x))
            eq(call('AlgorithmsI64','BinarySearch',a,n,x),bisect.bisect_left(v,x) if x in v else -1)
        unique=list(dict.fromkeys(v)); length=call('AlgorithmsI64','UniqueAdjacent',a,n)
        eq(length,len(unique)); eq(list(a)[:length],unique)
        eq(call('AlgorithmsI64','Fill',a,n,42),0); eq(list(a)[:n],[42]*n)
    for m,extra in [('Find',[3]),('Count',[3]),('LowerBound',[3]),('UpperBound',[3]),('BinarySearch',[3]),('IsSorted',[]),('Reverse',[]),('RotateLeft',[3]),('UniqueAdjacent',[]),('Fill',[3]),('MinIndex',[]),('MaxIndex',[]),('HeapSort',[])]:
        eq(call('AlgorithmsI64',m,None,1,*extra),-1)
        eq(call('AlgorithmsI64',m,None,-1,*extra),-1)
def test_encodings():
    payloads=[b'',b'f',b'fo',b'foo',b'foob',b'fooba',b'foobar',bytes(range(256))]
    payloads += [rng.randbytes(rng.randrange(1024)) for _ in range(300)]
    for data in payloads:
        n=len(data); src=buf(data)
        eq(call('Base64','EncodedLength',n),len(base64.b64encode(data)))
        for cls,encoded in [('Base64',base64.b64encode(data)),('Hex',data.hex().encode())]:
            out=buf(b'\xa5'*(len(encoded)+8))
            eq(call(cls,'Encode',src,n,out,len(encoded)),len(encoded))
            eq(bytes(out)[:len(encoded)],encoded); eq(bytes(out)[len(encoded):],b'\xa5'*8)
            result=buf(b'\xa5'*(n+8))
            eq(call(cls,'Decode',buf(encoded),len(encoded),result,n),n)
            eq(bytes(result)[:n],data); eq(bytes(result)[n:],b'\xa5'*8)
            if n:
                before=bytes(result)
                eq(call(cls,'Decode',buf(encoded),len(encoded),result,n-1),-1); eq(bytes(result),before)
                before=bytes(out)
                eq(call(cls,'Encode',src,n,out,len(encoded)-1),-1); eq(bytes(out),before)
        eq(call('Checksums','Crc32',src,n,0),zlib.crc32(data))
        eq(call('Checksums','Adler32',src,n,1),zlib.adler32(data))
        split=n//2
        for method,start,oracle in [('Crc32',0,zlib.crc32),('Adler32',1,zlib.adler32)]:
            v=call('Checksums',method,buf(data[:split]),split,start)
            eq(call('Checksums',method,buf(data[split:]),n-split,v),oracle(data))
    for c in range(-10,300):
        table=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        eq(call('Base64','Value',c),table.index(c) if 0<=c<=255 and c in table else -1)
    for bad in [b'A===',b'====',b'=AAA',b'AA=A',b'AB==',b'AAB=',b'AA\n=',b'AA-_']:
        out=buf(b'\xa5'*16); eq(call('Base64','Decode',buf(bad),len(bad),out,16),-2); eq(bytes(out),b'\xa5'*16)
    for bad in [b'gg',b'0z']:
        out=buf(b'\xa5'*4); eq(call('Hex','Decode',buf(bad),len(bad),out,4),-2); eq(bytes(out),b'\xa5'*4)
    eq(call('Hex','Decode',buf(b'f'),1,None,0),-1)
    eq(call('Base64','Decode',buf(b'AAA'),3,None,0),-1)
    for n in [-1,2**63-1]: eq(call('Base64','EncodedLength',n),-1)
    for cls in ['Hex','Base64']:
        for method in ['Encode','Decode']:
            eq(call(cls,method,None,4,None,16),-1)
            eq(call(cls,method,None,-1,None,16),-1)
    for method in ['Crc32','Adler32']:
        eq(call('Checksums',method,None,1,123),123)
        eq(call('Checksums',method,None,-1,123),123)
def test_utf8():
    codepoints=[0,127,128,2047,2048,55295,57344,65535,65536,1114111]
    codepoints += [c for c in (rng.randrange(1114112) for _ in range(3000)) if not 55296<=c<=57343]
    for cp in codepoints:
        expected=chr(cp).encode(); out=buf(b'\xa5'*8)
        eq(call('Utf8','Encode',cp,out,4),len(expected)); eq(bytes(out)[:len(expected)],expected)
        width=C.c_int32(); eq(call('Utf8','DecodeFirst',out,len(expected),C.byref(width)),cp); eq(width.value,len(expected))
        eq(call('Utf8','Count',out,len(expected)),1)
        eq(call('Utf8','Encode',cp,out,len(expected)-1),-1)
    for bad in [b'\x80',b'\xc0\x80',b'\xe0\x80\x80',b'\xed\xa0\x80',b'\xf4\x90\x80\x80',b'\xf5\x80\x80\x80',b'\xc2',b'\xc2A']:
        width=C.c_int32(123); eq(call('Utf8','DecodeFirst',buf(bad),len(bad),C.byref(width)),-2); eq(width.value,0)
        eq(call('Utf8','Count',buf(bad),len(bad)),-2)
    for cp in [55296,57343,1114112,2**32-1]: eq(call('Utf8','Encode',cp,buf(b'xxxx'),4),-2)
    eq(call('Utf8','Count',None,0),0); eq(call('Utf8','Count',None,1),-1)
    eq(call('Utf8','DecodeFirst',None,1,None),-1)
    text='Aनमस्तेé😀\0'.encode(); eq(call('Utf8','Count',buf(text),len(text)),len(text.decode()))
    for _ in range(10000):
        data=rng.randbytes(rng.randrange(20))
        try: expected=len(data.decode('utf-8'))
        except UnicodeDecodeError: expected=-2
        eq(call('Utf8','Count',buf(data),len(data)),expected)
def test_bytes():
    for _ in range(300):
        data=rng.randbytes(rng.randrange(100)); other=rng.randbytes(rng.randrange(100)); needle=data[2:7]
        src=buf(data)
        eq(call('Bytes','Compare',src,len(data),buf(other),len(other)),(data>other)-(data<other))
        eq(call('Bytes','Find',src,len(data),buf(needle),len(needle)),data.find(needle))
        eq(call('Bytes','Find',src,len(data),buf(b'xyz'),3),data.find(b'xyz'))
        eq(call('Bytes','CountByte',src,len(data),65),data.count(65))
        eq(call('Bytes','ToLowerAscii',src,len(data)),0); eq(bytes(src)[:len(data)],data.lower())
        src=buf(data); eq(call('Bytes','ToUpperAscii',src,len(data)),0); eq(bytes(src)[:len(data)],data.upper())
    eq(call('Bytes','Compare',None,1,None,0),-2)
    eq(call('Bytes','Find',None,1,None,0),-2)
    for method,args in [('CountByte',[1]),('ToLowerAscii',[]),('ToUpperAscii',[])]: eq(call('Bytes',method,None,1,*args),-1)
def test_containers():
    cls='ArrayVectorI64'; storage=arr([0]*64); eq(call(cls,'Bind',storage,64),0)
    model=[]; out=C.c_int64()
    for _ in range(3000):
        action=rng.choice(['push','pop','insert','erase','set','sort','clear','at'])
        i=rng.randrange(-1,len(model)+2); value=rng.randrange(-10000,10000)
        if action=='push':
            ok=len(model)<64; eq(call(cls,'PushBack',value),0 if ok else -1)
            if ok: model.append(value)
        elif action=='pop':
            ok=bool(model); eq(call(cls,'PopBack',C.byref(out)),0 if ok else -1)
            if ok: eq(out.value,model.pop())
        elif action=='insert':
            ok=0<=i<=len(model) and len(model)<64; eq(call(cls,'Insert',i,value),0 if ok else -1)
            if ok: model.insert(i,value)
        elif action=='erase':
            ok=0<=i<len(model); eq(call(cls,'Erase',i),0 if ok else -1)
            if ok: model.pop(i)
        elif action=='set':
            ok=0<=i<len(model); eq(call(cls,'Set',i,value),0 if ok else -1)
            if ok: model[i]=value
        elif action=='at':
            ok=0<=i<len(model); eq(call(cls,'At',i,C.byref(out)),0 if ok else -1)
            if ok: eq(out.value,model[i])
        elif action=='sort': eq(call(cls,'Sort'),0); model.sort()
        else: call(cls,'Clear'); model.clear()
        eq(call(cls,'Length'),len(model)); eq(call(cls,'Capacity'),64); eq(list(storage)[:len(model)],model)
    call(cls,'Clear')
    for i in range(64): eq(call(cls,'PushBack',i),0)
    eq(call(cls,'PushBack',9),-1); eq(call(cls,'Insert',0,9),-1)
    eq(call(cls,'Bind',None,1),-1); eq(call(cls,'Bind',None,-1),-1)
    eq(call(cls,'At',0,None),-1); eq(call(cls,'PopBack',None),-1)
    cls='BinaryHeapI64'; eq(call(cls,'Bind',storage,64),0); model=[]
    for _ in range(3000):
        if rng.randrange(2):
            value=rng.randrange(-10000,10000); good=len(model)<64
            eq(call(cls,'Push',value),0 if good else -1)
            if good: heapq.heappush(model,value)
        else:
            good=bool(model); eq(call(cls,'Pop',C.byref(out)),0 if good else -1)
            if good: eq(out.value,heapq.heappop(model))
        eq(call(cls,'Length'),len(model)); eq(call(cls,'Peek',C.byref(out)),0 if model else -1)
        if model: eq(out.value,model[0])
    call(cls,'Clear'); eq(call(cls,'Length'),0)
    for i in range(64): eq(call(cls,'Push',64-i),0)
    eq(call(cls,'Push',0),-1)
    for i in range(64): eq(call(cls,'Pop',C.byref(out)),0); eq(out.value,i+1)
    eq(call(cls,'Bind',None,1),-1); eq(call(cls,'Bind',None,-1),-1)
    eq(call(cls,'Peek',None),-1); eq(call(cls,'Pop',None),-1)
def test_dates():
    epoch=datetime.date(1970,1,1)
    for year in [1,4,100,400,1600,1900,1969,1970,2000,2024,2100,9999]+[rng.randrange(1,10000) for _ in range(1000)]:
        eq(call('Date','IsLeapYear',year),int(year%4==0 and (year%100!=0 or year%400==0)))
        for month in range(1,13):
            date=datetime.date(year,month,1)
            import calendar
            days=calendar.monthrange(year,month)[1]
            eq(call('Date','DaysInMonth',year,month),days)
            for day in [1,days]:
                date=datetime.date(year,month,day)
                eq(call('Date','IsValid',year,month,day),1)
                eq(call('Date','DaysSinceEpoch',year,month,day),(date-epoch).days)
                eq(call('Date','Weekday',year,month,day),(date.weekday()+1)%7)
            eq(call('Date','IsValid',year,month,days+1),0)
    for y,m,d in [(0,1,1),(10000,1,1),(2023,2,29),(2024,0,1),(2024,13,1),(2024,1,0)]:
        eq(call('Date','IsValid',y,m,d),0); eq(call('Date','Weekday',y,m,d),-1)
        eq(call('Date','DaysSinceEpoch',y,m,d),-(2**63))

def test_sha256():
    values=[b'',b'abc',b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',b'a'*1000000]
    values += [bytes([n%256])*n for n in range(260)]
    values += [rng.randbytes(rng.randrange(5000)) for _ in range(700)]
    for data in values:
        out=buf(b'\xa5'*40)
        eq(call('Sha256','Digest',buf(data),len(data),out,32),32)
        eq(bytes(out)[:32],hashlib.sha256(data).digest());eq(bytes(out)[32:],b'\xa5'*8)
    for n in [-1,2**61,2**63-1]:
        out=buf(b'\xa5'*32);eq(call('Sha256','Digest',None,n,out,32),-1);eq(bytes(out),b'\xa5'*32)
    out=buf(b'\xa5'*32)
    eq(call('Sha256','Digest',None,1,out,32),-1)
    eq(call('Sha256','Digest',None,0,None,32),-1)
    eq(call('Sha256','Digest',None,0,out,31),-1);eq(bytes(out),b'\xa5'*32)
def test_uri():
    values=[b'',bytes(range(256)),b'a/b?x=1&y=2#z',b'%',b'++',b'\x00', 'नमस्ते😀'.encode()]
    values += [rng.randbytes(rng.randrange(400)) for _ in range(500)]
    for data in values:
        encoded=urllib.parse.quote_from_bytes(data,safe='-._~').encode()
        eq(call('Uri','EncodedLength',buf(data),len(data)),len(encoded))
        out=buf(b'\xa5'*(len(encoded)+8))
        eq(call('Uri','EncodeComponent',buf(data),len(data),out,len(encoded)),len(encoded))
        eq(bytes(out)[:len(encoded)],encoded);eq(bytes(out)[len(encoded):],b'\xa5'*8)
        decoded=buf(b'\xa5'*(len(data)+8))
        eq(call('Uri','DecodeComponent',buf(encoded),len(encoded),decoded,len(data)),len(data))
        eq(bytes(decoded)[:len(data)],data);eq(bytes(decoded)[len(data):],b'\xa5'*8)
        if data:
            eq(call('Uri','EncodeComponent',buf(data),len(data),out,len(encoded)-1),-1)
            eq(bytes(out)[:len(encoded)],encoded)
            eq(call('Uri','DecodeComponent',buf(encoded),len(encoded),decoded,len(data)-1),-1)
            eq(bytes(decoded)[:len(data)],data)
    for _ in range(2000):
        data=rng.randbytes(rng.randrange(40))
        if rng.randrange(2):data+=b'%'+rng.randbytes(rng.randrange(4))
        out=buf(b'\xa5'*(len(data)+8));bad=re.search(rb'%(?![0-9a-fA-F]{2})',data)
        result=call('Uri','DecodeComponent',buf(data),len(data),out,len(data))
        if bad:eq(result,-2);eq(bytes(out),b'\xa5'*(len(data)+8))
        else:
            expected=urllib.parse.unquote_to_bytes(data)
            eq(result,len(expected));eq(bytes(out)[:result],expected);eq(bytes(out)[result:],b'\xa5'*(len(data)+8-result))
    eq(call('Uri','EncodedLength',None,-1),-1);eq(call('Uri','EncodedLength',None,1),-1)
    for method in ['EncodeComponent','DecodeComponent']:
        for src,n,out,cap in [(None,1,None,9),(None,-1,None,9),(None,0,None,-1)]:eq(call('Uri',method,src,n,out,cap),-1)
    out=buf(b'\xa5'*10);eq(call('Uri','DecodeComponent',buf(b'a%GG'),4,out,10),-2);eq(bytes(out),b'\xa5'*10)
def test_uuid():
    variants={uuid.RESERVED_NCS:0,uuid.RFC_4122:1,uuid.RESERVED_MICROSOFT:2,uuid.RESERVED_FUTURE:3}
    for data in [b'\x00'*16,b'\xff'*16]+[rng.randbytes(16) for _ in range(700)]:
        obj=uuid.UUID(bytes=data);text=str(obj).encode();out=buf(b'\xa5'*44)
        eq(call('Uuid','Format',buf(data),16,out,36),36);eq(bytes(out)[:36],text);eq(bytes(out)[36:],b'\xa5'*8)
        for spelling in [text,text.upper()]:
            raw=buf(b'\xa5'*24);eq(call('Uuid','Parse',buf(spelling),36,raw,16),16)
            eq(bytes(raw)[:16],data);eq(bytes(raw)[16:],b'\xa5'*8)
        eq(call('Uuid','Version',buf(data),16),data[6]>>4)
        eq(call('Uuid','Variant',buf(data),16),variants[obj.variant])
        eq(call('Uuid','IsNil',buf(data),16),int(data==b'\0'*16))
    for i in range(36):
        bad=bytearray(b'00000000-0000-0000-0000-000000000000');bad[i]=ord('x');out=buf(b'\xa5'*16)
        eq(call('Uuid','Parse',buf(bad),36,out,16),-2);eq(bytes(out),b'\xa5'*16)
    for method,size,capacity in [('Parse',36,16),('Format',16,36)]:
        out=buf(b'\xa5'*40)
        eq(call('Uuid',method,None,size,out,capacity),-1)
        eq(call('Uuid',method,buf(b'0'*size),size,out,capacity-1),-1)
        eq(call('Uuid',method,buf(b'0'*size),size-1,out,capacity),-1)
        eq(bytes(out),b'\xa5'*40)
    for method in ['Version','Variant','IsNil']:
        eq(call('Uuid',method,None,16),-1);eq(call('Uuid',method,buf(b'0'*16),15),-1)
def test_map_queue():
    cls='SortedMapI64';out=C.c_int64()
    for capacity in [0,1,2,64]:
        keys=arr([0]*capacity);values=arr([0]*capacity);eq(call(cls,'Bind',keys,values,capacity),0);model={}
        for _ in range(1800):
            key=rng.randrange(-40,40);value=rng.randrange(-1000,1000);op=rng.randrange(5)
            if op<=1:
                ok=key in model or len(model)<capacity;eq(call(cls,'Put',key,value),0 if ok else -1)
                if ok:model[key]=value
            elif op==2:
                out.value=12345;eq(call(cls,'Get',key,C.byref(out)),0 if key in model else -1)
                eq(out.value,model.get(key,12345))
            elif op==3:
                ok=key in model;eq(call(cls,'Remove',key),0 if ok else -1)
                if ok:del model[key]
            else:call(cls,'Clear');model.clear()
            eq(call(cls,'Contains',key),int(key in model))
            eq(call(cls,'Length'),len(model));eq(call(cls,'Capacity'),capacity)
            ordered=sorted(model);eq(list(keys)[:len(model)],ordered);eq(list(values)[:len(model)],[model[k] for k in ordered])
            for i,k in enumerate(ordered):
                eq(call(cls,'KeyAt',i,C.byref(out)),0);eq(out.value,k)
                eq(call(cls,'ValueAt',i,C.byref(out)),0);eq(out.value,model[k])
        eq(call(cls,'KeyAt',-1,C.byref(out)),-1);eq(call(cls,'ValueAt',len(model),C.byref(out)),-1)
        eq(call(cls,'Bind',None,None,1),-1);eq(call(cls,'Length'),len(model))
    for method,args in [('Get',[0]),('KeyAt',[0]),('ValueAt',[0])]:eq(call(cls,method,*args,None),-1)
    eq(call(cls,'Bind',None,None,-1),-1)
    keys=arr([0,0]);values=arr([0,0]);eq(call(cls,'Bind',keys,values,2),0)
    for k in [2**63-1,-2**63]:eq(call(cls,'Put',k,k),0)
    eq(call(cls,'Put',2**63-1,42),0);eq(call(cls,'Put',0,0),-1)
    eq(list(keys),[-2**63,2**63-1]);eq(list(values),[-2**63,42])
    cls='QueueI64'
    for capacity in [0,1,2,31]:
        storage=arr([0]*capacity);eq(call(cls,'Bind',storage,capacity),0);model=collections.deque()
        for _ in range(5000):
            op=rng.randrange(10)
            if op<5:
                value=rng.randrange(-1000,1000);ok=len(model)<capacity
                eq(call(cls,'PushBack',value),0 if ok else -1)
                if ok:model.append(value)
            elif op<9:
                out.value=12345;ok=bool(model);eq(call(cls,'PopFront',C.byref(out)),0 if ok else -1)
                eq(out.value,model.popleft() if ok else 12345)
            else:call(cls,'Clear');model.clear()
            eq(call(cls,'Length'),len(model));eq(call(cls,'Capacity'),capacity)
            out.value=12345;eq(call(cls,'Front',C.byref(out)),0 if model else -1);eq(out.value,model[0] if model else 12345)
        eq(call(cls,'Bind',None,1),-1);eq(call(cls,'Length'),len(model))
    eq(call(cls,'PopFront',None),-1);eq(call(cls,'Front',None),-1);eq(call(cls,'Bind',None,-1),-1)

def cursor_values(cls,reverse=False):
    out=C.c_int64();node=call(cls,'Last' if reverse else 'Begin');values=[]
    while node:
        eq(call(cls,'Read',node,C.byref(out)),0);values.append(out.value)
        if len(values)>10000:raise AssertionError('iterator cycle')
        node=call(cls,'Previous' if reverse else 'Next',node)
    return values
def test_linked_lists():
    out=C.c_int64()
    for cls in ['SListI64','DListI64']:
        model=[]
        eq(call(cls,'Next',None),None);eq(call(cls,'Read',None,C.byref(out)),-1)
        for _ in range(2500):
            action=rng.randrange(8);value=rng.randrange(-15,16)
            if action==0:eq(call(cls,'PushFront',value),0);model.insert(0,value)
            elif action<=2:eq(call(cls,'PushBack',value),0);model.append(value)
            elif action==3:
                out.value=12345;eq(call(cls,'PopFront',C.byref(out)),0 if model else -1)
                eq(out.value,model.pop(0) if model else 12345)
            elif action==4:
                ok=value in model;eq(call(cls,'RemoveFirst',value),0 if ok else -1)
                if ok:model.remove(value)
            elif action==5 and cls=='DListI64':
                out.value=12345;eq(call(cls,'PopBack',C.byref(out)),0 if model else -1)
                eq(out.value,model.pop() if model else 12345)
            elif action==6:call(cls,'Clear');model.clear()
            else:
                i=rng.randrange(-1,len(model)+1);out.value=12345;ok=0<=i<len(model)
                eq(call(cls,'At',i,C.byref(out)),0 if ok else -1);eq(out.value,model[i] if ok else 12345)
            eq(call(cls,'Length'),len(model));eq(cursor_values(cls),model)
            if cls=='DListI64':eq(cursor_values(cls,True),model[::-1])
            for m,index in [('Front',0),('Back',-1)]:
                out.value=12345;eq(call(cls,m,C.byref(out)),0 if model else -1);eq(out.value,model[index] if model else 12345)
        for m,args in [('Front',[]),('Back',[]),('PopFront',[]),('At',[0]),('Read',[None])]:eq(call(cls,m,*args,None),-1)
        call(cls,'Clear')
        # Keep nonempty at destruction to exercise ownership cleanup.
        eq(call(cls,'PushBack',-2**63),0);eq(call(cls,'PushBack',2**63-1),0)
        eq(cursor_values(cls),[-2**63,2**63-1])
    eq(call('DListI64','Previous',None),None);eq(call('DListI64','PopBack',None),-1)
def test_red_black_tree():
    cls='RedBlackTreeI64';model=set();out=C.c_int64()
    for _ in range(7000):
        value=rng.randrange(-500,501);op=rng.randrange(10)
        if op<5:
            eq(call(cls,'Insert',value),1 if value in model else 0);model.add(value)
        elif op<9:
            good=value in model;eq(call(cls,'Remove',value),0 if good else -1);model.discard(value)
        else:call(cls,'Clear');model.clear()
        eq(call(cls,'Length'),len(model));eq(call(cls,'Contains',value),int(value in model))
        if _%20==0:
            ordered=sorted(model);eq(cursor_values(cls),ordered);eq(cursor_values(cls,True),ordered[::-1])
            for m,i in [('LowerBound',bisect.bisect_left(ordered,value)),('UpperBound',bisect.bisect_right(ordered,value))]:
                node=call(cls,m,value)
                if i==len(ordered):eq(node,None)
                else:eq(call(cls,'Read',node,C.byref(out)),0);eq(out.value,ordered[i])
    for order in [list(range(1000)),list(range(999,-1,-1)),[-2**63,2**63-1,0,-1,1]]:
        call(cls,'Clear')
        for value in order:eq(call(cls,'Insert',value),0)
        eq(cursor_values(cls),sorted(order));eq(cursor_values(cls,True),sorted(order,reverse=True))
        for value in order:eq(call(cls,'Remove',value),0)
        eq(call(cls,'Length'),0)
    for m in ['Next','Previous']:eq(call(cls,m,None),None)
    eq(call(cls,'Read',None,C.byref(out)),-1);eq(call(cls,'Read',None,None),-1)
    # Iterators to surviving nodes remain valid across insertions/rotations/deletion.
    for value in [10,20,30]:eq(call(cls,'Insert',value),0)
    cursor=call(cls,'LowerBound',20)
    for value in range(100):call(cls,'Insert',value)
    call(cls,'Remove',10);eq(call(cls,'Read',cursor,C.byref(out)),0);eq(out.value,20)

def test_concurrent_stateless_calls():
    from concurrent.futures import ThreadPoolExecutor
    def worker(seed):
        local=random.Random(seed);total=0
        for _ in range(600):
            data=local.randbytes(local.randrange(200));out=buf(b'\xa5'*800)
            size=call('Base64','Encode',buf(data),len(data),out,800)
            if bytes(out)[:size]!=base64.b64encode(data):raise AssertionError('concurrent Base64 corruption')
            if call('Utf8','Count',buf(b'A\xc3\xa9\xf0\x9f\x98\x80'),7)!=3:raise AssertionError('concurrent UTF-8 corruption')
            if call('Date','DaysSinceEpoch',2024,1,1)!=19723:raise AssertionError('concurrent Date corruption')
            total+=3
        return total
    with ThreadPoolExecutor(max_workers=8) as pool:totals=list(pool.map(worker,range(8)))
    eq(sum(totals),14400)

try:
    for test in [test_ascii,test_bits,test_integer,test_algorithms,test_encodings,test_utf8,test_bytes,test_containers,test_dates,test_sha256,test_uri,test_uuid,test_map_queue,test_linked_lists,test_red_black_tree,test_concurrent_stateless_calls]:
        test(); print(test.__name__+': PASS',flush=True)
    from production_cases import run
    run(globals())
    eq(set(calls)-seen,set())
    report={'status':'PASS','assertions':checks,'api_methods_exercised':len(seen),'api_methods_total':len(API),'seed':391724,
            'library_sha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),
            'source_fingerprint':source_fingerprint(),'tests_fingerprint':tests_fingerprint(),'methods_exercised':sorted(seen)}
    print(json.dumps(report,sort_keys=True))
    if len(sys.argv)>2: Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n')
finally:
    for cls,h in handles.items():
        f=getattr(lib,'CMotiveAndObjective__'+cls+'__delete'); f.argtypes=[C.c_void_p]; f.restype=None; f(h)
