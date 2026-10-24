# Exact supplied Phobos snapshot inventory

Original source hashes and byte sizes are retained in phobos-inventory.json.
Partial means a tested explicit subset, not full Phobos API parity. External wrappers stay excluded.

| Module | Status | Implemented classes |
|---|---|---|
| etc.c.curl | excluded-external-dependency |  |
| etc.c.odbc.sql | excluded-external-dependency |  |
| etc.c.odbc.sqlext | excluded-external-dependency |  |
| etc.c.odbc.sqltypes | excluded-external-dependency |  |
| etc.c.odbc.sqlucode | excluded-external-dependency |  |
| etc.c.sqlite3 | excluded-external-dependency |  |
| etc.c.zlib | excluded-external-dependency |  |
| std.algorithm.comparison | partial | AlgorithmsI64, Bytes |
| std.algorithm.internal | deferred |  |
| std.algorithm.iteration | partial | AlgorithmsI64 |
| std.algorithm.mutation | partial | AlgorithmsI64 |
| std.algorithm | deferred |  |
| std.algorithm.searching | partial | AlgorithmsI64 |
| std.algorithm.setops | deferred |  |
| std.algorithm.sorting | partial | AlgorithmsI64 |
| std.array | partial | Bytes, ArrayVectorI64 |
| std.ascii | partial | Ascii |
| std.base64 | partial | Base64, Base64Url |
| std.bigint | deferred |  |
| std.bitmanip | partial | BitManip, Endian |
| std.checkedint | partial | CheckedInt |
| std.compiler | deferred |  |
| std.complex | deferred |  |
| std.concurrency | blocked-direct-port |  |
| std.container.array | partial | ArrayVectorI64 |
| std.container.binaryheap | partial | BinaryHeapI64 |
| std.container.dlist | partial | DListI64 |
| std.container | partial | ArrayVectorI64, BinaryHeapI64, SListI64, DListI64, RedBlackTreeI64, SortedMapI64, QueueI64, HashMapI64, HashSetI64, MultiMapI64, StackI64 |
| std.container.rbtree | partial | RedBlackTreeI64 |
| std.container.slist | partial | SListI64 |
| std.container.util | deferred |  |
| std.conv | partial | IntegerText |
| std.csv | partial | Csv |
| std.datetime.date | partial | Date |
| std.datetime.interval | deferred |  |
| std.datetime | deferred |  |
| std.datetime.stopwatch | deferred |  |
| std.datetime.systime | deferred |  |
| std.datetime.timezone | deferred |  |
| std.demangle | blocked-direct-port |  |
| std.digest.crc | partial | Checksums |
| std.digest.hmac | deferred |  |
| std.digest.md | deferred |  |
| std.digest.murmurhash | deferred |  |
| std.digest | deferred |  |
| std.digest.ripemd | deferred |  |
| std.digest.sha | partial | Sha256 |
| std.encoding | deferred |  |
| std.exception | deferred |  |
| std.experimental.allocator.building_blocks.affix_allocator | deferred |  |
| std.experimental.allocator.building_blocks.aligned_block_list | deferred |  |
| std.experimental.allocator.building_blocks.allocator_list | deferred |  |
| std.experimental.allocator.building_blocks.ascending_page_allocator | deferred |  |
| std.experimental.allocator.building_blocks.bitmapped_block | deferred |  |
| std.experimental.allocator.building_blocks.bucketizer | deferred |  |
| std.experimental.allocator.building_blocks.fallback_allocator | deferred |  |
| std.experimental.allocator.building_blocks.free_list | deferred |  |
| std.experimental.allocator.building_blocks.free_tree | deferred |  |
| std.experimental.allocator.building_blocks.kernighan_ritchie | deferred |  |
| std.experimental.allocator.building_blocks.null_allocator | deferred |  |
| std.experimental.allocator.building_blocks | deferred |  |
| std.experimental.allocator.building_blocks.quantizer | deferred |  |
| std.experimental.allocator.building_blocks.region | deferred |  |
| std.experimental.allocator.building_blocks.scoped_allocator | deferred |  |
| std.experimental.allocator.building_blocks.segregator | deferred |  |
| std.experimental.allocator.building_blocks.stats_collector | deferred |  |
| std.experimental.allocator.common | deferred |  |
| std.experimental.allocator.gc_allocator | deferred |  |
| std.experimental.allocator.mallocator | deferred |  |
| std.experimental.allocator.mmap_allocator | deferred |  |
| std.experimental.allocator | deferred |  |
| std.experimental.allocator.showcase | deferred |  |
| std.experimental.allocator.typed | deferred |  |
| std.experimental.checkedint | deferred |  |
| std.experimental.logger.core | deferred |  |
| std.experimental.logger.filelogger | deferred |  |
| std.experimental.logger.multilogger | deferred |  |
| std.experimental.logger.nulllogger | deferred |  |
| std.experimental.logger | deferred |  |
| std.file | deferred |  |
| std.format.internal.floats | upstream-support |  |
| std.format.internal.read | upstream-support |  |
| std.format.internal.write | upstream-support |  |
| std.format | deferred |  |
| std.format.read | deferred |  |
| std.format.spec | deferred |  |
| std.format.write | deferred |  |
| std.functional | blocked-direct-port |  |
| std.getopt | deferred |  |
| std.int128 | deferred |  |
| std.internal.attributes | upstream-support |  |
| std.internal.cstring | upstream-support |  |
| std.internal.digest.sha_SSSE3 | upstream-support |  |
| std.internal.math.biguintcore | upstream-support |  |
| std.internal.math.biguintnoasm | upstream-support |  |
| std.internal.math.biguintx86 | upstream-support |  |
| std.internal.math.errorfunction | upstream-support |  |
| std.internal.math.gammafunction | upstream-support |  |
| std.internal.memory | upstream-support |  |
| std.internal.scopebuffer | upstream-support |  |
| std.internal.test.dummyrange | upstream-support |  |
| std.internal.test.range | upstream-support |  |
| std.internal.test.uda | upstream-support |  |
| std.internal.unicode_comp | upstream-support |  |
| std.internal.unicode_decomp | upstream-support |  |
| std.internal.unicode_grapheme | upstream-support |  |
| std.internal.unicode_norm | upstream-support |  |
| std.internal.unicode_tables | upstream-support |  |
| std.internal.windows.advapi32 | upstream-support |  |
| std.json | partial | JsonString, JsonTokens |
| std.logger.core | deferred |  |
| std.logger.filelogger | deferred |  |
| std.logger.multilogger | deferred |  |
| std.logger.nulllogger | deferred |  |
| std.logger | deferred |  |
| std.math.algebraic | deferred |  |
| std.math.constants | deferred |  |
| std.math.exponential | deferred |  |
| std.math.hardware | deferred |  |
| std.math.operations | deferred |  |
| std.math | deferred |  |
| std.math.remainder | deferred |  |
| std.math.rounding | deferred |  |
| std.math.traits | deferred |  |
| std.math.trigonometry | deferred |  |
| std.mathspecial | deferred |  |
| std.meta | blocked-direct-port |  |
| std.mmfile | deferred |  |
| std.net.curl | excluded-external-dependency |  |
| std.net.isemail | deferred |  |
| std.numeric | partial | IntegerMath |
| std.outbuffer | deferred |  |
| std | deferred |  |
| std.parallelism | blocked-direct-port |  |
| std.path | deferred |  |
| std.process | deferred |  |
| std.random | partial | Pcg32 |
| std.range.interfaces | blocked-direct-port |  |
| std.range | deferred |  |
| std.range.primitives | blocked-direct-port |  |
| std.regex.internal.backtracking | upstream-support |  |
| std.regex.internal.generator | upstream-support |  |
| std.regex.internal.ir | upstream-support |  |
| std.regex.internal.kickstart | upstream-support |  |
| std.regex.internal.parser | upstream-support |  |
| std.regex.internal.tests | upstream-support |  |
| std.regex.internal.tests2 | upstream-support |  |
| std.regex.internal.thompson | upstream-support |  |
| std.regex | deferred |  |
| std.signals | blocked-direct-port |  |
| std.socket | deferred |  |
| std.stdint | deferred |  |
| std.stdio | deferred |  |
| std.string | partial | ByteStrings, Bytes |
| std.sumtype | blocked-direct-port |  |
| std.system | deferred |  |
| std.traits | blocked-direct-port |  |
| std.typecons | blocked-direct-port |  |
| std.typetuple | blocked-direct-port |  |
| std.uni | deferred |  |
| std.uri | partial | Uri |
| std.utf | partial | Utf16, Utf32, Utf8 |
| std.uuid | partial | Uuid |
| std.variant | blocked-direct-port |  |
| std.windows.charset | deferred-os-service |  |
| std.windows.registry | deferred-os-service |  |
| std.windows.syserror | deferred-os-service |  |
| std.zip | deferred |  |
| std.zlib | excluded-external-dependency |  |
| test.betterc_module_tests | upstream-support |  |
| test.dub_stdx_allocator | upstream-support |  |
| test.dub_stdx_checkedint | upstream-support |  |
| std.unicode_table_generator | upstream-support |  |
| unittest | deferred |  |
