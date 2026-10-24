# Supplied Phobos source inventory — iteration 2

All 174 D files are listed. Partial does not mean complete or API-compatible. Deferred does not mean impossible.

| Module / file | Status | Subset / reason |
|---|---|---|
| `etc.c.curl` (`etc/c/curl.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `etc.c.odbc.sql` (`etc/c/odbc/sql.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `etc.c.odbc.sqlext` (`etc/c/odbc/sqlext.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `etc.c.odbc.sqltypes` (`etc/c/odbc/sqltypes.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `etc.c.odbc.sqlucode` (`etc/c/odbc/sqlucode.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `etc.c.sqlite3` (`etc/c/sqlite3.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `etc.c.zlib` (`etc/c/zlib.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `std.algorithm.comparison` (`std/algorithm/comparison.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.algorithm.internal` (`std/algorithm/internal.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.algorithm.iteration` (`std/algorithm/iteration.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.algorithm.mutation` (`std/algorithm/mutation.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.algorithm` (`std/algorithm/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.algorithm.searching` (`std/algorithm/searching.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.algorithm.setops` (`std/algorithm/setops.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.algorithm.sorting` (`std/algorithm/sorting.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.array` (`std/array.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.ascii` (`std/ascii.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.base64` (`std/base64.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.bigint` (`std/bigint.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.bitmanip` (`std/bitmanip.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.checkedint` (`std/checkedint.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.compiler` (`std/compiler.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.complex` (`std/complex.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.concurrency` (`std/concurrency.d`) | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| `std.container.array` (`std/container/array.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.container.binaryheap` (`std/container/binaryheap.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.container.dlist` (`std/container/dlist.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.container` (`std/container/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.container.rbtree` (`std/container/rbtree.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.container.slist` (`std/container/slist.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.container.util` (`std/container/util.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.conv` (`std/conv.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.csv` (`std/csv.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.datetime.date` (`std/datetime/date.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.datetime.interval` (`std/datetime/interval.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.datetime` (`std/datetime/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.datetime.stopwatch` (`std/datetime/stopwatch.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.datetime.systime` (`std/datetime/systime.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.datetime.timezone` (`std/datetime/timezone.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.demangle` (`std/demangle.d`) | blocked-direct-port | D symbol mangling is not a CMotive ABI equivalent; a D demangler would be a separate utility. |
| `std.digest.crc` (`std/digest/crc.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.digest.hmac` (`std/digest/hmac.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.digest.md` (`std/digest/md.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.digest.murmurhash` (`std/digest/murmurhash.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.digest` (`std/digest/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.digest.ripemd` (`std/digest/ripemd.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.digest.sha` (`std/digest/sha.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.encoding` (`std/encoding.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.exception` (`std/exception.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.affix_allocator` (`std/experimental/allocator/building_blocks/affix_allocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.aligned_block_list` (`std/experimental/allocator/building_blocks/aligned_block_list.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.allocator_list` (`std/experimental/allocator/building_blocks/allocator_list.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.ascending_page_allocator` (`std/experimental/allocator/building_blocks/ascending_page_allocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.bitmapped_block` (`std/experimental/allocator/building_blocks/bitmapped_block.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.bucketizer` (`std/experimental/allocator/building_blocks/bucketizer.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.fallback_allocator` (`std/experimental/allocator/building_blocks/fallback_allocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.free_list` (`std/experimental/allocator/building_blocks/free_list.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.free_tree` (`std/experimental/allocator/building_blocks/free_tree.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.kernighan_ritchie` (`std/experimental/allocator/building_blocks/kernighan_ritchie.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.null_allocator` (`std/experimental/allocator/building_blocks/null_allocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks` (`std/experimental/allocator/building_blocks/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.quantizer` (`std/experimental/allocator/building_blocks/quantizer.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.region` (`std/experimental/allocator/building_blocks/region.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.scoped_allocator` (`std/experimental/allocator/building_blocks/scoped_allocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.segregator` (`std/experimental/allocator/building_blocks/segregator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.building_blocks.stats_collector` (`std/experimental/allocator/building_blocks/stats_collector.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.common` (`std/experimental/allocator/common.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.gc_allocator` (`std/experimental/allocator/gc_allocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.mallocator` (`std/experimental/allocator/mallocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.mmap_allocator` (`std/experimental/allocator/mmap_allocator.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator` (`std/experimental/allocator/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.showcase` (`std/experimental/allocator/showcase.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.allocator.typed` (`std/experimental/allocator/typed.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.checkedint` (`std/experimental/checkedint.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.logger.core` (`std/experimental/logger/core.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.logger.filelogger` (`std/experimental/logger/filelogger.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.logger.multilogger` (`std/experimental/logger/multilogger.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.logger.nulllogger` (`std/experimental/logger/nulllogger.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.experimental.logger` (`std/experimental/logger/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.file` (`std/file.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.format.internal.floats` (`std/format/internal/floats.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.format.internal.read` (`std/format/internal/read.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.format.internal.write` (`std/format/internal/write.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.format` (`std/format/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.format.read` (`std/format/read.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.format.spec` (`std/format/spec.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.format.write` (`std/format/write.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.functional` (`std/functional.d`) | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| `std.getopt` (`std/getopt.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.int128` (`std/int128.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.internal.attributes` (`std/internal/attributes.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.cstring` (`std/internal/cstring.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.digest.sha_SSSE3` (`std/internal/digest/sha_SSSE3.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.math.biguintcore` (`std/internal/math/biguintcore.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.math.biguintnoasm` (`std/internal/math/biguintnoasm.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.math.biguintx86` (`std/internal/math/biguintx86.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.math.errorfunction` (`std/internal/math/errorfunction.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.math.gammafunction` (`std/internal/math/gammafunction.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.memory` (`std/internal/memory.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.scopebuffer` (`std/internal/scopebuffer.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.test.dummyrange` (`std/internal/test/dummyrange.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.test.range` (`std/internal/test/range.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.test.uda` (`std/internal/test/uda.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.unicode_comp` (`std/internal/unicode_comp.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.unicode_decomp` (`std/internal/unicode_decomp.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.unicode_grapheme` (`std/internal/unicode_grapheme.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.unicode_norm` (`std/internal/unicode_norm.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.unicode_tables` (`std/internal/unicode_tables.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.internal.windows.advapi32` (`std/internal/windows/advapi32.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.json` (`std/json.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.logger.core` (`std/logger/core.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.logger.filelogger` (`std/logger/filelogger.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.logger.multilogger` (`std/logger/multilogger.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.logger.nulllogger` (`std/logger/nulllogger.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.logger` (`std/logger/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.algebraic` (`std/math/algebraic.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.constants` (`std/math/constants.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.exponential` (`std/math/exponential.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.hardware` (`std/math/hardware.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.operations` (`std/math/operations.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math` (`std/math/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.remainder` (`std/math/remainder.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.rounding` (`std/math/rounding.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.traits` (`std/math/traits.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.math.trigonometry` (`std/math/trigonometry.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.mathspecial` (`std/mathspecial.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.meta` (`std/meta.d`) | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| `std.mmfile` (`std/mmfile.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.net.curl` (`std/net/curl.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `std.net.isemail` (`std/net/isemail.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.numeric` (`std/numeric.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.outbuffer` (`std/outbuffer.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std` (`std/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.parallelism` (`std/parallelism.d`) | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| `std.path` (`std/path.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.process` (`std/process.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.random` (`std/random.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.range.interfaces` (`std/range/interfaces.d`) | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| `std.range` (`std/range/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.range.primitives` (`std/range/primitives.d`) | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| `std.regex.internal.backtracking` (`std/regex/internal/backtracking.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex.internal.generator` (`std/regex/internal/generator.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex.internal.ir` (`std/regex/internal/ir.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex.internal.kickstart` (`std/regex/internal/kickstart.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex.internal.parser` (`std/regex/internal/parser.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex.internal.tests` (`std/regex/internal/tests.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex.internal.tests2` (`std/regex/internal/tests2.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex.internal.thompson` (`std/regex/internal/thompson.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.regex` (`std/regex/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.signals` (`std/signals.d`) | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| `std.socket` (`std/socket.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.stdint` (`std/stdint.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.stdio` (`std/stdio.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.string` (`std/string.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.sumtype` (`std/sumtype.d`) | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| `std.system` (`std/system.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.traits` (`std/traits.d`) | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| `std.typecons` (`std/typecons.d`) | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| `std.typetuple` (`std/typetuple.d`) | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| `std.uni` (`std/uni/package.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.uri` (`std/uri.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.utf` (`std/utf.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.uuid` (`std/uuid.d`) | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| `std.variant` (`std/variant.d`) | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| `std.windows.charset` (`std/windows/charset.d`) | deferred-os-service | OS-supported functionality is permitted by dependency policy; a tested CMotive implementation is not yet provided. |
| `std.windows.registry` (`std/windows/registry.d`) | deferred-os-service | OS-supported functionality is permitted by dependency policy; a tested CMotive implementation is not yet provided. |
| `std.windows.syserror` (`std/windows/syserror.d`) | deferred-os-service | OS-supported functionality is permitted by dependency policy; a tested CMotive implementation is not yet provided. |
| `std.zip` (`std/zip.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| `std.zlib` (`std/zlib.d`) | excluded-external-dependency | Excluded by dependency policy: external library wrapper. A future self-contained implementation would be a separate port, not a linked wrapper. |
| `test.betterc_module_tests` (`test/betterc_module_tests.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `test.dub_stdx_allocator` (`test/dub_stdx_allocator.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `test.dub_stdx_checkedint` (`test/dub_stdx_checkedint.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `std.unicode_table_generator` (`tools/unicode_table_generator.d`) | upstream-support | Internal implementation detail, test fixture or generator; not a separate public API promise. |
| `unittest` (`unittest.d`) | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
