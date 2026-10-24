"""Independent reference tests for restored Phobos functionality."""
CASES=[]
def case(f):
 CASES.append(f);return f
def run(g):
 globals().update({k:v for k,v in g.items() if not k.startswith("__")})
 for f in CASES:
  f(); print(f.__name__+": PASS",flush=True)

@case
def phobos_endian():
 for width in [1,2,4,8]:
  for big in [0,1]:
   for x in [0,1,2**(width*8)-1]+[rng.getrandbits(width*8) for _ in range(200)]:
    out=buf(b'\xa5'*12);v=C.c_uint64(19)
    eq(call('Endian','Write',x,width,big,out,12),0);eq(bytes(out)[:width],x.to_bytes(width,'big' if big else 'little'));eq(bytes(out)[width:],b'\xa5'*(12-width))
    eq(call('Endian','Read',out,width,width,big,C.byref(v)),0);eq(v.value,x)
   v.value=19;eq(call('Endian','Read',out,width-1,width,big,C.byref(v)),-1);eq(v.value,19)
   before=bytes(out);eq(call('Endian','Write',0,width,big,out,width-1),-1);eq(bytes(out),before)
   if width<8:eq(call('Endian','Write',2**(width*8),width,big,out,12),-2);eq(bytes(out),before)
 for width in [-1,0,3,5,7,9]:eq(call('Endian','Read',None,8,width,0,None),-1);eq(call('Endian','Write',0,width,0,None,8),-1)


@case
def phobos_byte_strings():
 for data in [b'',b'  ',b' a\tb \n',bytes(range(256))]+[rng.randbytes(rng.randrange(80)) for _ in range(300)]:
  a=C.c_int64(77);n=C.c_int64(88);x=buf(data)
  eq(call('ByteStrings','TrimAscii',x,len(data),C.byref(a),C.byref(n)),0);eq(data[a.value:a.value+n.value],data.strip(b' \t\n\r\v\f'))
  for delimiter in [0,32,255]:
   cursor=C.c_int64();parts=[]
   while True:
    rc=call('ByteStrings','SplitNext',x,len(data),delimiter,C.byref(cursor),C.byref(a),C.byref(n))
    if rc==1:break
    eq(rc,0);parts.append(data[a.value:a.value+n.value])
   eq(parts,data.split(bytes([delimiter])))
  old=rng.randrange(256);new=rng.randrange(256)
  eq(call('ByteStrings','SubstituteByte',x,len(data),old,new),data.count(bytes([old])));eq(bytes(x)[:len(data)],data.replace(bytes([old]),bytes([new])))
 eq(call('ByteStrings','TrimAscii',None,-1,None,None),-1);eq(call('ByteStrings','SplitNext',None,1,0,None,None,None),-1);eq(call('ByteStrings','SubstituteByte',None,1,0,1),-1)


@case
def phobos_utf32():
 for big in [0,1]:
  encoding='utf-32-be' if big else 'utf-32-le'
  for cp in [0,127,128,65535,65536,1114111]+[rng.randrange(1114112) for _ in range(2000)]:
   if 55296<=cp<=57343:continue
   expected=chr(cp).encode(encoding);out=buf(b'\xa5'*8);used=C.c_int32(99)
   eq(call('Utf32','Encode',cp,out,8,big),4);eq(bytes(out),expected+b'\xa5'*4)
   eq(call('Utf32','DecodeFirst',out,4,big,C.byref(used)),cp);eq(used.value,4);eq(call('Utf32','Count',out,4,big),1)
  for cp in [55296,56320,57343,1114112,2**32-1]:
   used.value=99;out=buf(cp.to_bytes(4,'big' if big else 'little'));eq(call('Utf32','DecodeFirst',out,4,big,C.byref(used)),-2);eq(used.value,0);eq(call('Utf32','Count',out,4,big),-2)
   before=bytes(out);eq(call('Utf32','Encode',cp,out,4,big),-2);eq(bytes(out),before)
  eq(call('Utf32','Count',None,0,big),0);eq(call('Utf32','Count',None,1,big),-1)
  out=buf(b'abcd');used.value=99;eq(call('Utf32','DecodeFirst',out,3,big,C.byref(used)),-2);eq(used.value,0);eq(call('Utf32','Encode',65,out,3,big),-1);eq(bytes(out),b'abcd')


@case
def phobos_crc64():
 mask=2**64-1
 for name,poly,golden in [('Crc64ECMA',0xc96c5795d7870f42,0x995dc9bbdf1939fa),('Crc64ISO',0xd800000000000000,0xb90956c775a41001)]:
  eq(call('Checksums',name,buf(b'123456789'),9),golden)
  for data in [b'',bytes(range(256))]+[rng.randbytes(rng.randrange(400)) for _ in range(100)]:
   # Independent table oracle, matching reflected all-ones Phobos parameters.
   table=[]
   for i in range(256):
    x=i
    for j in range(8):x=(x>>1)^(poly if x&1 else 0)
    table.append(x)
   x=mask
   for b in data:x=(x>>8)^table[(x^b)&255]
   eq(call('Checksums',name,buf(data),len(data)),x^mask)
  eq(call('Checksums',name,None,1),0)


@case
def phobos_pcg32():
 mask=2**64-1
 for seed,stream in [(42,54),(0,0),(mask,mask)]+[(rng.getrandbits(64),rng.getrandbits(64)) for _ in range(30)]:
  inc=((stream<<1)|1)&mask;state=inc;state=(state+seed)&mask;state=(state*6364136223846793005+inc)&mask
  def next_ref():
   nonlocal state
   old=state;state=(old*6364136223846793005+inc)&mask;x=(((old>>18)^old)>>27)&0xffffffff;r=old>>59
   return ((x>>r)|(x<<((-r)&31)))&0xffffffff
  call('Pcg32','Seed',seed,stream)
  for _ in range(200):eq(call('Pcg32','Next'),next_ref())
  for bound in [1,2,3,17,2**31+1,2**32-1]:
   for _ in range(50):
    threshold=((1<<32)-bound)%bound
    while True:
     x=next_ref()
     if x>=threshold:break
    out=C.c_uint32(99);eq(call('Pcg32','Bounded',bound,C.byref(out)),0);eq(out.value,x%bound)
  out.value=99;eq(call('Pcg32','Bounded',0,C.byref(out)),-1);eq(out.value,99);eq(call('Pcg32','Bounded',1,None),-1)


@case
def phobos_csv():
 import csv,io
 for _ in range(150):
  records=[[ ''.join(rng.choice('ab,\"\r\n é') for _ in range(rng.randrange(15))) for _ in range(rng.randrange(1,7))] for j in range(rng.randrange(1,5))]
  stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\r\n');writer.writerows(records);data=stream.getvalue().encode();source=buf(data)
  eq(call('Csv','Bind',source,len(data)),0);out=buf(b'\xa5'*300);row_end=C.c_int32(77)
  for row in records:
   for i,value in enumerate(row):
    before=bytes(out)
    if value:
     eq(call('Csv','Next',out,0,C.byref(row_end)),-3);eq(bytes(out),before);eq(row_end.value,77)
    n=call('Csv','Next',out,300,C.byref(row_end));eq(n,len(value.encode()));eq(bytes(out)[:n],value.encode());eq(row_end.value,int(i==len(row)-1));row_end.value=77
  eq(call('Csv','Next',out,300,C.byref(row_end)),-4)
 for data in [b'"unterminated',b'"a"x',b'ab"c']:
  source=buf(data);eq(call('Csv','Bind',source,len(data)),0);out=buf(b'xxxx');flag=C.c_int32(77)
  for i in range(2):eq(call('Csv','Next',out,4,C.byref(flag)),-2);eq(bytes(out),b'xxxx');eq(flag.value,77)
 source=buf(b'a,');eq(call('Csv','Bind',source,2),0);eq(call('Csv','Next',out,4,C.byref(flag)),1);eq(flag.value,0);eq(call('Csv','Next',None,0,C.byref(flag)),0);eq(flag.value,1)
 eq(call('Csv','Bind',None,0),0);eq(call('Csv','Next',None,0,C.byref(flag)),-4);eq(call('Csv','Bind',None,1),-1)


@case
def phobos_json_string():
 for text in ['', '"\\\x00\n', 'é😀']+[''.join(chr(cp) for cp in [rng.randrange(32),rng.randrange(32,55296),rng.randrange(65536,1114112)]) for _ in range(500)]:
  data=text.encode();source=buf(data);out=buf(b'\xa5'*200);size=call('JsonString','EncodedLength',source,len(data));eq(size>=2,True)
  before=bytes(out);eq(call('JsonString','Encode',source,len(data),out,size-1),-1);eq(bytes(out),before)
  eq(call('JsonString','Encode',source,len(data),out,200),size);eq(json.loads(bytes(out)[:size]),text)
  for literal in [bytes(out)[:size],json.dumps(text,ensure_ascii=True).encode()]:
   encoded=buf(literal);target=buf(b'\xa5'*200);n=call('JsonString','Decode',encoded,len(literal),target,200);eq(n,len(data));eq(bytes(target)[:n],data)
 for literal in [b'',b'"',b'"\uD800"',b'"\uDC00"',b'"\uD800\u0041"',b'"\x00"',b'"\q"',b'"a"x',b'"\xff"']:
  target=buf(b'xxx');eq(call('JsonString','Decode',buf(literal),len(literal),target,3),-2);eq(bytes(target),b'xxx')


@case
def phobos_json_tokens():
 import re
 def reference(data):
  token=re.compile(rb'\s*("(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?|true|false|null|[{}\[\],:])')
  result=[]
  for m in token.finditer(data):
   x=m[1]
   if x in [b',',b':']:continue
   kind={b'{':1,b'[':2,b'}':3,b']':4,b'true':7,b'false':8,b'null':9}.get(x,5 if x.startswith(b'"') else 6)
   result.append((kind,m.start(1),len(x)))
  return result
 work=(C.c_int32*64)()
 for obj in [None,True,False,0,-1,1.25,'é😀',[],{},[{},[1,2],{'x':False}]]+[{'name':str(i),'items':[rng.randrange(-100,100),None,True,[]]} for i in range(100)]:
  data=json.dumps(obj,ensure_ascii=rng.choice([True,False])).encode();expected=reference(data);source=buf(data)
  eq(call('JsonTokens','Validate',source,len(data),work,64),len(expected))
  kinds=(C.c_int32*100)(*([77]*100));starts=(C.c_int64*100)(*([77]*100));lengths=(C.c_int64*100)(*([77]*100))
  eq(call('JsonTokens','Tokenize',source,len(data),kinds,starts,lengths,len(expected)-1,work,64),-1);eq(list(kinds),[77]*100);eq(list(starts),[77]*100)
  eq(call('JsonTokens','Tokenize',source,len(data),kinds,starts,lengths,100,work,64),len(expected));eq(list(zip(kinds,starts,lengths))[:len(expected)],expected)
 for data in [b'',b'01',b'1.',b'1e+',b'+1',b'[1,]',b'{"a":}',b'{1:2}',b'{}[]',b'"\uD800"',b'[',b'{"x":1,}',b'NaN',b'truefalse',b'\xff']:
  eq(call('JsonTokens','Validate',buf(data),len(data),work,64),-2)
 data=b'['*65+b'0'+b']'*65;eq(call('JsonTokens','Validate',buf(data),len(data),work,64),-1)


@case
def phobos_varint():
 def encoded(x):
  out=[]
  while x>=128:out.append((x&127)|128);x>>=7
  return bytes(out+[x])
 for signed in [False,True]:
  low=-(2**63) if signed else 0;high=2**63-1 if signed else 2**64-1
  for value in [low,high,0,1]+[rng.randint(low,high) for _ in range(1000)]:
   x=(value<<1)^(value>>63) if signed else value;expected=encoded(x);out=buf(b'\xa5'*12);kind='I64' if signed else 'U64';number=C.c_int64(77) if signed else C.c_uint64(77);used=C.c_int32(77)
   eq(call('VarInt','Encode'+kind,value,out,len(expected)-1),-1);eq(bytes(out),b'\xa5'*12)
   eq(call('VarInt','Encode'+kind,value,out,12),len(expected));eq(bytes(out)[:len(expected)],expected)
   eq(call('VarInt','Decode'+kind,out,len(expected),C.byref(number),C.byref(used)),0);eq(number.value,value);eq(used.value,len(expected))
 for data in [b'\x80',b'\x80\x00',b'\x81\x00',b'\xff'*10,b'\xff'*9+b'\x02']:
  number=C.c_uint64(77);used=C.c_int32(77);eq(call('VarInt','DecodeU64',buf(data),len(data),C.byref(number),C.byref(used)),-2);eq(number.value,77);eq(used.value,0)


@case
def phobos_base64url():
 for n in range(400):
  data=rng.randbytes(n);expected=base64.urlsafe_b64encode(data).rstrip(b'=');out=buf(b'\xa5'*600)
  eq(call('Base64Url','EncodedLength',n),len(expected));eq(call('Base64Url','Encode',buf(data),n,out,600),len(expected));eq(bytes(out)[:len(expected)],expected)
  decoded=buf(b'\xa5'*500);eq(call('Base64Url','Decode',out,len(expected),decoded,500),n);eq(bytes(decoded)[:n],data)
 for c in range(256):
  alphabet=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';eq(call('Base64Url','Value',c),alphabet.find(bytes([c])))
 for data in [b'Zg==',b'Z+',b'Z/',b'Zh',b'Zm9',b'@@']:
  out=buf(b'xxxx');eq(call('Base64Url','Decode',buf(data),len(data),out,4),-2);eq(bytes(out),b'xxxx')
 eq(call('Base64Url','Decode',buf(b'A'),1,None,0),-1)

