# Implemented core API

The 149 maintained methods are CMotive class implementations, not native wrappers.
The compiler automatically emits C and includes its native runtime; the binary is
not freestanding or free of C runtime dependencies. These adapted typed APIs are
not drop-in Phobos APIs. No D compiler/runtime or C++ library is required.

## Memory and ownership

Use CMotive instances from .HMOT source or opaque C ABI handles from
include/CMotiveAndObjective.h. Allocate with the class's __new, check for null,
release once with __delete. Every method needs a valid, live instance. Buffers
are borrowed, owned by the caller, and must be accessible for the declared lengths.
Keep container storage alive and exclusive until the container is rebound or
destroyed. Borrowed containers never grow past supplied capacity. SListI64,
DListI64 and RedBlackTreeI64 own dynamically allocated nodes; see STL-COVERAGE.md. Lengths and
capacities are elements for I64 arrays and bytes for Uchar arrays. Do not overlap
encoder/decoder input/output buffers; output scalars must not alias inputs or
container storage. No NUL terminators are added. Empty buffers may be null.
Shared mutable buffers/containers require external synchronization.

## Contracts

- Ascii: I32 classifiers return 0 outside ASCII. Conversions preserve nonletters.
  HexValue returns -1 for nonhex input.
- BitManip: unsigned 64-bit operations; rotate counts modulo 64; leading/trailing
  zero counts of zero equal 64.
- CheckedInt: 0 success, -1 null output/divide by zero, -2 overflow; failed output
  unchanged. Overflow checked before signed arithmetic is evaluated.
- IntegerMath: Gcd(0,0)=0; Sqrt is floor square root. Lcm/Power return 0 success,
  -1 null output, -2 overflow, preserving output on failure. Power(0,0)=1.
- AlgorithmsI64: -1 invalid input; Find/BinarySearch also return -1 when absent;
  MinIndex/MaxIndex return -1 for empty. Bounds/search require ascending sorted
  input. BinarySearch returns first match. HeapSort is unstable, in-place O(n log n).
  UniqueAdjacent removes adjacent duplicates, returns logical length; tail unspecified.
  Reverse/RotateLeft/Fill return 0 success; IsSorted returns 1/0 or -1 invalid.
- Base64/Hex: byte count success, -1 invalid arguments/insufficient capacity,
  -2 malformed encoding; decoder validates all input before writing. RFC 4648
  standard Base64 alphabet and padding; whitespace, URL alphabet and nonzero
  discarded padding bits rejected. Hex emits lowercase; accepts either case.
- Utf8: DecodeFirst returns a Unicode scalar, -1 invalid argument/empty input,
  -2 malformed/truncated; consumed resets to 0 on error. Count returns scalar
  count or -1 invalid arguments/-2 malformed. Encode returns 1..4 bytes, -1 null/
  insufficient output, -2 invalid scalar. No normalization/grapheme/case-folding.
- Checksums: CRC-32/ISO-HDLC, previous=0 for new digest; Adler-32, previous=1.
  Feed prior results for streaming. Invalid input returns previous. Not cryptographic.
- Bytes: supports embedded NUL. Compare returns -1/0/1, -2 invalid arguments.
  Find returns byte index, -1 absent, -2 invalid; empty needle matches at 0.
  Case conversion modifies ASCII letters only and returns 0 or -1 invalid.
- ArrayVectorI64: borrowed contiguous storage. Bind clears length; failed Bind
  preserves old binding. 0 success, -1 invalid/null/full. Clear retains capacity.
- BinaryHeapI64: borrowed min-heap. Bind/Clear reset length; Push/Pop O(log n),
  Peek O(1). 0 success, -1 invalid/full/empty. No automatic allocation.
- Date: proleptic Gregorian, years 1..9999; weekday 0=Sunday. DaysSinceEpoch uses
  1970-01-01, INT64_MIN for invalid dates. DaysInMonth/Weekday return -1 invalid;
  IsValid returns 0. IsLeapYear tests divisibility; other APIs enforce year limits.

- Sha256.Digest: one-shot SHA-256, returns 32 bytes, or -1 for invalid pointer,
  length or insufficient capacity. Input length is 0..2^61-1 bytes (the SHA-256
  64-bit bit-length limit); output is unchanged on error. No streaming API,
  HMAC, password hashing or secure memory erasure is provided.
- Uri: byte-oriented percent encoding of URI components. EncodeComponent leaves
  only ASCII unreserved characters unescaped and emits uppercase hex. EncodedLength
  returns exact size or -1. DecodeComponent returns byte count, -1 invalid arguments/
  capacity, -2 malformed percent escapes. Literal '+' stays '+'. No Unicode or
  URI scheme/authority validation is performed. Decode validates before writing.
- Uuid: Parse accepts exactly 36 canonical hyphenated ASCII characters, case
  insensitive hex, and writes 16 bytes. Format requires 16 bytes and writes 36
  lowercase characters. Returns 16/36 success, -1 invalid arguments/capacity,
  -2 malformed Parse input. No RFC version/variant policy is enforced by Parse.
  Version extracts the high nibble of byte 6. Variant returns 0=NCS, 1=RFC,
  2=Microsoft, 3=future. IsNil tests all-zero bytes. These inspectors return -1 for
  null/non-16-byte input. No random or name-based UUID generation is supplied.
- SortedMapI64, QueueI64, SListI64, DListI64, RedBlackTreeI64: ownership,
  errors, iterator rules and complexity are specified in [STL-COVERAGE.md](STL-COVERAGE.md).

## Signatures

See [API-SIGNATURES.md](API-SIGNATURES.md), generated from the maintained .HMOT
method declarations. The manifest, C ABI header and export lists are regenerated
by tools/sync_api.py and checked for drift in every test route.

## Threads and compiler cleanup

The exported library uses explicit zero initialization for stateless helper
instances, avoiding writes to this compiler's global automatic-object cleanup
stack. The generated-code guard checks that no library method calls Cleanup_Push.
Independent containers and stateless methods can be used concurrently with
separate buffers; shared mutable containers require external synchronization.
This does not repair compiler cleanup behavior in an application's own code.
