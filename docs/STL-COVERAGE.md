# Typed STL/container coverage — iteration 3

The supplied Phobos container families now have working I64 implementations.
This is typed coverage, not complete generic Phobos or C++ STL compatibility.
All library code uses .CMOT source and .HMOT headers. No unsupported generic
template files are shipped: the bundled compiler skips arbitrary Template classes.

| Phobos family | CMotive class | Storage and operations |
|---|---|---|
| std.container.array | ArrayVectorI64 | Borrowed buffer; indexed access, push/pop, insert/erase, sort |
| std.container.binaryheap | BinaryHeapI64 | Borrowed min-heap; push/pop/peek |
| std.container.slist | SListI64 | Owned nodes; front/back insertion, pop front, remove first match, forward cursor |
| std.container.dlist | DListI64 | Owned nodes; push/pop at either end, remove first match, forward/reverse cursors |
| std.container.rbtree | RedBlackTreeI64 | Owned unique-key ordered set; balanced insert/delete, search, lower/upper bounds, forward/reverse cursors |
| Additional typed ordered map | SortedMapI64 | Borrowed parallel arrays; sorted unique I64 keys and I64 values, update/search/delete/indexed iteration |
| Additional typed queue | QueueI64 | Borrowed ring buffer; constant-time push back/pop front/peek |

## Ownership, errors and iterator validity

ArrayVectorI64, BinaryHeapI64, SortedMapI64 and QueueI64 borrow caller-owned
storage and never grow past Bind capacity. SortedMapI64 key/value storage must
not overlap. Rebinding/Clear reset logical contents but do not free storage.

SListI64, DListI64 and RedBlackTreeI64 allocate nodes using CMotive New and
release them using Delete. Clear and destruction release all nodes. Never copy
an owning container by value: that would duplicate its ownership pointers.
C ABI users own one __new/__delete handle pair. CMotive source users must avoid
shallow assignment of owning containers. Allocation failures return -2 without
changing contents. The allocation-failure tests exercise this behavior explicitly.

Push/Insert return 0 for a newly inserted value. RedBlackTreeI64.Insert returns
1 for an existing value, without adding a duplicate. Remove/Pop/At/Read return
-1 for absent values, empty containers, invalid indexes or null output arguments.
Output scalars are unchanged on errors and must not alias container storage.
Linked-list duplicate values are allowed; RemoveFirst removes the first match.

Begin returns the first node cursor, Last returns the final node where supported.
Next and Previous advance in iteration order; a null cursor represents the end.
Read copies the cursor's value into the output scalar. Cursors are borrowed
Void* values, not owning handles: do not delete them. A cursor must be null or
point to a live node of the same container. Erasing a node invalidates its cursor;
Clear/destruction invalidate all cursors. Other insertions, balancing rotations
and unrelated erasures preserve cursors to surviving nodes. Invalid/dangling or
foreign cursors cannot be validated and must not be passed to these APIs.

## Complexity

Linked-list push front/back and pop front are O(1); DList pop back is O(1).
At and RemoveFirst are O(n). Tree Insert/Remove/Contains/bounds are O(log n);
cursor steps are O(log n) worst case and amortized O(1) for a full traversal.
Tree Clear repeatedly removes the root, O(n log n), using no recursive call stack.
SortedMap lookup is O(log n), insertion/removal O(n). Vector and heap operations
have their usual fixed-capacity costs. No custom comparators or allocators exist.

## Still missing

Arbitrary element/key/value types, template range adapters, allocator policies,
multisets/multimaps, hash containers, and Phobos's full container/range interfaces
are not implemented. The Phobos snapshot does not supply B/B+Tree containers;
this iteration does not claim to add them or all containers from earlier CMotive
projects. General template support requires compiler work.

The compiler does not emit forward typedefs for self-referential class fields.
Internal node links therefore use Void*, converted to typed node pointers in
CMotive methods. Internal node/helper headers remain .HMOT and their generated
symbols are hidden from the shared-library ABI.

All iteration-2 STL methods are retained by the iteration-3 API baseline.
Removing unused compiler built-in wrappers does not remove these independently
implemented CMotive containers. See DEPENDENCIES.md.
