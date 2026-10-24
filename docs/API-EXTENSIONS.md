# Additional typed STL and codec contracts

These are self-contained CMotive classes. Source signatures are generated in
API-SIGNATURES.md. Every instance must be live, and mutable instances need caller
synchronization. Output scalars must not alias container storage. Borrowed buffers
must remain allocated, writable and large enough for the declared capacity.
Distinct buffers (including the hash state bytes) must not overlap. Bind rejects
negative capacities or null positive-capacity buffers before changing state.
A zero capacity accepts null buffers. Clear/Bind reset contents without freeing
borrowed storage. There is no implicit growth or external C++ container library.

HashMapI64 uses caller-owned key/value I64 arrays and a Uchar state array, with
bounded linear probing and reusable tombstones. Put inserts or updates (including
updates when full), returning 0 or -1 when a new key has no free slot. Get and
Remove return -1 when absent; failed Get preserves its output. Contains returns
0/1. HashSetI64 uses only keys and state bytes; Insert returns 0 new, 1 already
present, -1 full. Both have Length, Capacity, Clear, NextSlot and KeyAt; the map
also has ValueAt. NextSlot(-1) begins and -1 ends. Slots are physical indices,
not insertion-order or dense indices. Mutation may invalidate slot iteration;
start a fresh traversal afterward. Hashing is deterministic and noncryptographic,
with O(capacity) worst-case operations; do not treat it as collision-attack
resistance. Arrays/state bytes must not be modified while bound to a container.

MultiMapI64 uses parallel borrowed key/value arrays, retains duplicate keys and
preserves insertion order. Insert returns 0/-1, RemoveOne erases the first match
and returns 0/-1; RemoveAll returns the removed count. Count counts matches.
FindNext(key,-1) begins indexed traversal and -1 ends. KeyAt/ValueAt use dense
indices; removal invalidates indices at/after the removed item. Scan/removal
costs are O(n). Length/Capacity/Clear have the same borrowed-storage contract.

StackI64 is a fixed-capacity LIFO stack: Push returns 0/-1; Peek and Pop return
0/-1 and preserve the output on failure. Length/Capacity/Clear/Bind have the same
borrowed-storage contract. All operations except binding storage are O(1).

AlgorithmsI64.MergeSort sorts ascending using a caller-owned I64 workspace with
capacity >= n. The two arrays must not overlap; exact alias is rejected. It is a
bottom-up merge sort, O(n log n) time and O(n) borrowed workspace, selecting the
left item on equal values. n <= 1 requires no workspace. Invalid arguments return
-1 before changing data/workspace; success returns 0. Declared n/capacity must
refer to real allocated spans, as for the other raw-buffer APIs.

AlgorithmsI64.SumChecked folds I64 values into an initial I64 sum. It checks each
addition, returning -2 on intermediate overflow, -1 on invalid arguments, and 0
on success. The output is written only on success, including n=0 (initial).
An overflowing intermediate sum is an error even if later values would cancel it.

Utf8.DecodeTo32 converts a byte span to Unicode scalar U32 values. EncodeFrom32
converts U32 scalars to UTF-8; EncodedLength32 validates/measures them. Capacities
are U32 elements for DecodeTo32 and bytes for EncodeFrom32. Return values are
output element/byte counts, -1 invalid arguments/capacity and -2 invalid encoding
or scalar. All validation precedes output writes. Input/output spans must not
overlap. U32 values are scalars in host representation, not an on-disk UTF-32
byte-order contract. Embedded NULs are valid; no terminator is appended.

Utf16 operates on bytes, with bigEndian strictly 0 (LE) or 1 (BE). DecodeFirst
returns a scalar and writes a byte count, clearing consumed to zero on error;
Count validates/counts the entire span; Encode writes 2 or 4 bytes. No automatic
BOM detection/removal occurs: U+FEFF is an ordinary scalar. Lone/reversed surrogate
pairs, odd trailing bytes, truncation and surrogate scalar inputs are rejected.
Return -1 indicates invalid arguments/capacity, -2 invalid encoding/scalar.
DecodeFirst requires a nonempty span; Count accepts an empty null span. No
terminator is appended and no host-aligned U16 load is used.

IntegerText parses/formats I64 and U64 in bases 2..36, without locale or libc
conversion routines. Formatting returns a byte count, lower-case digits and a
minus sign for negative I64; it appends no NUL. Parsing requires a nonempty exact
span with no whitespace, separators or base prefixes, accepts either digit case,
and accepts one leading + or - for I64 only. Leading zeros are allowed. Returns
0 success, -1 bad arguments/base, -2 malformed text/digit, -3 numeric overflow;
output scalars are unchanged on error. If a prefix already overflows, -3 is
returned before any later malformed suffix is inspected. Format returns -1 on
bad arguments/capacity with no writes. No third-party conversion wrapper is used.
