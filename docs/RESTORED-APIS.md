# Restored API contracts, iterations 24–34

All existing 199 methods and typed STL classes remain. New headers are .HMOT;
maintained compilation units remain .CMOT. None uses an external library wrapper.
Pointers must refer to valid storage for declared sizes. Input and output spans
must be disjoint unless an existing method explicitly permits overlap. No new
API retains input pointers except the borrowed Csv cursor. Objects need caller
synchronization when shared across threads.

| Class | Contract |
|---|---|
| Endian | Read/Write 1,2,4,8 byte unsigned integers, explicit byte order 0=LE,1=BE. Status 0 succeeds; -1 invalid arguments/capacity; -2 write overflow. Output unchanged on failure. |
| ByteStrings | TrimAscii returns start/length; SplitNext uses cursor=0 initially, -1 after last field, status 1 at EOF. Empty and trailing fields retained. SubstituteByte returns replaced byte count. Invalid args -1. |
| Utf32 | Explicit order, Unicode scalars only. DecodeFirst resets consumed to zero on error; -1 arguments, -2 malformed. Encode capacity checked before writes. Count validates entire span. |
| Checksums CRC64 | Reflected ECMA polynomial C96C5795D7870F42 and ISO D800000000000000, all-ones init/final xor as supplied Phobos. Invalid spans return 0, matching existing checksum convention. |
| Pcg32 | Seed before first use. Per-object PCG-XSH-RR state; stream is reduced to 63 bits. Bounded uses rejection sampling, rejects bound 0 and null output without advancing state. Not cryptographic. |
| Csv | Bind borrows input until next Bind/destruction; empty document has no fields. Next returns field byte length; rowEnd marks newline/EOF; -4 EOF, -3 capacity, -2 syntax, -1 arguments. No NUL terminator. Empty fields/newline-only records are a single empty field. CRLF/LF/CR accepted. Output/cursor/rowEnd unchanged on error; retry is supported. |
| JsonString | Encode emits quoted UTF-8, controls as u00XX escapes. Decode accepts exactly one literal with strict UTF-8 and surrogate pairing. Returns byte length, -1 args/capacity, -2 malformed. Output unchanged on failure. EncodedLength uses -2 for invalid input span/encoding. |
| JsonTokens | Validate returns token count. Tokenize emits exact byte start/length plus types: object open=1,array open=2,object close=3,array close=4,string=5,number=6,true=7,false=8,null=9. Keys are string tokens; commas/colons omitted. Caller I32 workspace has depth entries; -1 args/workspace/output capacity, -2 grammar. Workspace may change on failure; token outputs do not. No AST or generic JSONValue. Number syntax is validated without float conversion. |
| VarInt | Canonical base128 U64; I64 uses ZigZag. Encode returns 1..10 bytes, -1 capacity/args. Decode status 0, -1 args, -2 truncated/overflow/noncanonical; consumed reset to zero, value unchanged on error. Concatenated records allowed via consumed length. |
| Base64Url | Canonical unpadded RFC4648 URL alphabet. Decode rejects padding, ordinary +/ alphabet, whitespace and nonzero unused bits. Return byte length; -1 arguments/shape/capacity, -2 alphabet/tail bits. Output unchanged on failure. |

The generated compatibility header still reflects the pinned C-emission backend.
Standalone CMO-REG-1 assembly primitives remain independent of that backend.
ISO C normalization adds one byte only to unused compiler PublicData helper
structs; real class layouts and public signatures are unchanged.
