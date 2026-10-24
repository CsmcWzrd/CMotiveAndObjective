# Public method signatures

Generated from .HMOT declarations. Contracts are in [API.md](API.md).

## AlgorithmsI64

`I64 Find(data: I64*, n: I64, value: I64)`  
`I64 Count(data: I64*, n: I64, value: I64)`  
`I64 LowerBound(data: I64*, n: I64, value: I64)`  
`I64 UpperBound(data: I64*, n: I64, value: I64)`  
`I64 BinarySearch(data: I64*, n: I64, value: I64)`  
`I32 IsSorted(data: I64*, n: I64)`  
`I32 Reverse(data: I64*, n: I64)`  
`I32 RotateLeft(data: I64*, n: I64, by: U64)`  
`I64 UniqueAdjacent(data: I64*, n: I64)`  
`I32 Fill(data: I64*, n: I64, value: I64)`  
`I64 MinIndex(data: I64*, n: I64)`  
`I64 MaxIndex(data: I64*, n: I64)`  
`I32 HeapSort(data: I64*, n: I64)`  
`I32 MergeSort(data: I64*, n: I64, workspace: I64*, capacity: I64)`  
`I32 SumChecked(data: I64*, n: I64, initial: I64, out: I64*)`  

## ArrayVectorI64

`I32 Bind(storage: I64*, capacity: I64)`  
`I64 Length()`  
`I64 Capacity()`  
`I32 PushBack(value: I64)`  
`I32 PopBack(out: I64*)`  
`I32 At(index: I64, out: I64*)`  
`I32 Set(index: I64, value: I64)`  
`I32 Insert(index: I64, value: I64)`  
`I32 Erase(index: I64)`  
`Void Clear()`  
`I32 Sort()`  

## Ascii

`I32 IsAscii(c: I32)`  
`I32 IsUpper(c: I32)`  
`I32 IsLower(c: I32)`  
`I32 IsAlpha(c: I32)`  
`I32 IsDigit(c: I32)`  
`I32 IsAlnum(c: I32)`  
`I32 IsHexDigit(c: I32)`  
`I32 IsWhite(c: I32)`  
`I32 IsBlank(c: I32)`  
`I32 IsControl(c: I32)`  
`I32 IsGraph(c: I32)`  
`I32 IsPrint(c: I32)`  
`I32 IsPunct(c: I32)`  
`I32 ToLower(c: I32)`  
`I32 ToUpper(c: I32)`  
`I32 HexValue(c: I32)`  

## Base64

`I64 EncodedLength(n: I64)`  
`I32 Value(c: I32)`  
`I64 Encode(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  
`I64 Decode(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  

## BinaryHeapI64

`I32 Bind(storage: I64*, capacity: I64)`  
`I64 Length()`  
`I32 Push(value: I64)`  
`I32 Peek(out: I64*)`  
`I32 Pop(out: I64*)`  
`Void Clear()`  

## BitManip

`I32 PopCount(x: U64)`  
`I32 CountLeadingZeros(x: U64)`  
`I32 CountTrailingZeros(x: U64)`  
`U64 RotateLeft(x: U64, shift: U32)`  
`U64 RotateRight(x: U64, shift: U32)`  
`U64 ByteSwap(x: U64)`  
`U64 ReverseBits(x: U64)`  
`I32 IsPowerOfTwo(x: U64)`  

## Bytes

`I32 Compare(a: Uchar*, an: I64, b: Uchar*, bn: I64)`  
`I64 Find(data: Uchar*, n: I64, needle: Uchar*, length: I64)`  
`I64 CountByte(data: Uchar*, n: I64, value: Uchar)`  
`I32 ToLowerAscii(data: Uchar*, n: I64)`  
`I32 ToUpperAscii(data: Uchar*, n: I64)`  

## CheckedInt

`I32 Add(a: I64, b: I64, out: I64*)`  
`I32 Subtract(a: I64, b: I64, out: I64*)`  
`I32 Multiply(a: I64, b: I64, out: I64*)`  
`I32 Divide(a: I64, b: I64, out: I64*)`  
`I32 Negate(a: I64, out: I64*)`  

## Checksums

`U32 Crc32(data: Uchar*, n: I64, previous: U32)`  
`U32 Adler32(data: Uchar*, n: I64, previous: U32)`  

## DListI64

`I64 Length()`  
`I32 PushFront(value: I64)`  
`I32 PushBack(value: I64)`  
`I32 PopFront(out: I64*)`  
`I32 Front(out: I64*)`  
`I32 Back(out: I64*)`  
`I32 At(index: I64, out: I64*)`  
`I32 RemoveFirst(value: I64)`  
`Void* Begin()`  
`Void* Next(cursor: Void*)`  
`I32 Read(cursor: Void*, out: I64*)`  
`Void Clear()`  
`I32 PopBack(out: I64*)`  
`Void* Last()`  
`Void* Previous(cursor: Void*)`  

## Date

`I32 IsLeapYear(year: I32)`  
`I32 DaysInMonth(year: I32, month: I32)`  
`I32 IsValid(year: I32, month: I32, day: I32)`  
`I64 DaysSinceEpoch(year: I32, month: I32, day: I32)`  
`I32 Weekday(year: I32, month: I32, day: I32)`  

## HashMapI64

`I32 Bind(keys: I64*, values: I64*, states: Uchar*, capacity: I64)`  
`I64 Length()`  
`I64 Capacity()`  
`I32 Put(key: I64, value: I64)`  
`I32 Get(key: I64, out: I64*)`  
`I32 Contains(key: I64)`  
`I32 Remove(key: I64)`  
`I64 NextSlot(previous: I64)`  
`I32 KeyAt(slot: I64, out: I64*)`  
`I32 ValueAt(slot: I64, out: I64*)`  
`Void Clear()`  

## HashSetI64

`I32 Bind(keys: I64*, states: Uchar*, capacity: I64)`  
`I64 Length()`  
`I64 Capacity()`  
`I32 Insert(key: I64)`  
`I32 Contains(key: I64)`  
`I32 Remove(key: I64)`  
`I64 NextSlot(previous: I64)`  
`I32 KeyAt(slot: I64, out: I64*)`  
`Void Clear()`  

## Hex

`I64 Encode(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  
`I64 Decode(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  

## IntegerMath

`U64 Gcd(a: U64, b: U64)`  
`U64 Sqrt(x: U64)`  
`I32 Lcm(a: U64, b: U64, out: U64*)`  
`I32 Power(x: U64, exponent: U32, out: U64*)`  

## IntegerText

`I64 FormatU64(value: U64, base: I32, out: Uchar*, capacity: I64)`  
`I32 ParseU64(data: Uchar*, n: I64, base: I32, out: U64*)`  
`I64 FormatI64(value: I64, base: I32, out: Uchar*, capacity: I64)`  
`I32 ParseI64(data: Uchar*, n: I64, base: I32, out: I64*)`  

## MultiMapI64

`I32 Bind(keys: I64*, values: I64*, capacity: I64)`  
`I64 Length()`  
`I64 Capacity()`  
`I32 Insert(key: I64, value: I64)`  
`I64 Count(key: I64)`  
`I64 FindNext(key: I64, previous: I64)`  
`I32 KeyAt(index: I64, out: I64*)`  
`I32 ValueAt(index: I64, out: I64*)`  
`I32 RemoveOne(key: I64)`  
`I64 RemoveAll(key: I64)`  
`Void Clear()`  

## QueueI64

`I32 Bind(storage: I64*, capacity: I64)`  
`I64 Length()`  
`I64 Capacity()`  
`I32 PushBack(value: I64)`  
`I32 PopFront(out: I64*)`  
`I32 Front(out: I64*)`  
`Void Clear()`  

## RedBlackTreeI64

`I64 Length()`  
`I32 Insert(value: I64)`  
`I32 Remove(value: I64)`  
`I32 Contains(value: I64)`  
`Void* Begin()`  
`Void* Last()`  
`Void* Next(cursor: Void*)`  
`Void* Previous(cursor: Void*)`  
`I32 Read(cursor: Void*, out: I64*)`  
`Void* LowerBound(value: I64)`  
`Void* UpperBound(value: I64)`  
`Void Clear()`  

## SListI64

`I64 Length()`  
`I32 PushFront(value: I64)`  
`I32 PushBack(value: I64)`  
`I32 PopFront(out: I64*)`  
`I32 Front(out: I64*)`  
`I32 Back(out: I64*)`  
`I32 At(index: I64, out: I64*)`  
`I32 RemoveFirst(value: I64)`  
`Void* Begin()`  
`Void* Next(cursor: Void*)`  
`I32 Read(cursor: Void*, out: I64*)`  
`Void Clear()`  

## Sha256

`I32 Digest(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  

## SortedMapI64

`I32 Bind(keys: I64*, values: I64*, capacity: I64)`  
`I64 Length()`  
`I64 Capacity()`  
`I32 Put(key: I64, value: I64)`  
`I32 Get(key: I64, out: I64*)`  
`I32 Contains(key: I64)`  
`I32 Remove(key: I64)`  
`I32 KeyAt(index: I64, out: I64*)`  
`I32 ValueAt(index: I64, out: I64*)`  
`Void Clear()`  

## StackI64

`I32 Bind(storage: I64*, capacity: I64)`  
`I64 Length()`  
`I64 Capacity()`  
`I32 Push(value: I64)`  
`I32 Peek(out: I64*)`  
`I32 Pop(out: I64*)`  
`Void Clear()`  

## Uri

`I64 EncodedLength(data: Uchar*, n: I64)`  
`I64 EncodeComponent(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  
`I64 DecodeComponent(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  

## Utf16

`I32 DecodeFirst(data: Uchar*, n: I64, bigEndian: I32, consumed: I32*)`  
`I64 Count(data: Uchar*, n: I64, bigEndian: I32)`  
`I32 Encode(cp: U32, out: Uchar*, capacity: I64, bigEndian: I32)`  

## Utf8

`I32 DecodeFirst(data: Uchar*, n: I64, consumed: I32*)`  
`I64 Count(data: Uchar*, n: I64)`  
`I32 Encode(cp: U32, out: Uchar*, capacity: I64)`  
`I64 DecodeTo32(data: Uchar*, n: I64, out: U32*, capacity: I64)`  
`I64 EncodedLength32(data: U32*, n: I64)`  
`I64 EncodeFrom32(data: U32*, n: I64, out: Uchar*, capacity: I64)`  

## Uuid

`I32 Parse(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  
`I32 Format(data: Uchar*, n: I64, out: Uchar*, capacity: I64)`  
`I32 Version(data: Uchar*, n: I64)`  
`I32 Variant(data: Uchar*, n: I64)`  
`I32 IsNil(data: Uchar*, n: I64)`  

