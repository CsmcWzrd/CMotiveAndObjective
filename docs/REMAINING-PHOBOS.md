# Remaining Phobos work

The original 174 modules are preserved as provenance. The following table is an explicit backlog; partial APIs still require further design and implementation. OS services can be added without third-party wrappers where supported. Excluded curl/ODBC/SQLite/zlib wrappers are not part of the backlog.

| Module | Status | Current scope or dependency |
|---|---|---|
| std.algorithm.comparison | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.algorithm.internal | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.algorithm.iteration | partial | Adapted typed subset only; full upstream generic and package APIs remain deferred. |
| std.algorithm.mutation | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.algorithm | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.algorithm.searching | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.algorithm.setops | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.algorithm.sorting | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.array | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.ascii | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.base64 | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.bigint | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.bitmanip | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.checkedint | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.compiler | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.complex | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.concurrency | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| std.container.array | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.container.binaryheap | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.container.dlist | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.container | partial | Adapted typed subset only; full upstream generic and package APIs remain deferred. |
| std.container.rbtree | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.container.slist | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.container.util | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.conv | partial | Adapted typed subset only; full upstream generic and package APIs remain deferred. |
| std.csv | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.datetime.date | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.datetime.interval | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.datetime | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.datetime.stopwatch | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.datetime.systime | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.datetime.timezone | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.demangle | blocked-direct-port | D symbol mangling is not a CMotive ABI equivalent; a D demangler would be a separate utility. |
| std.digest.crc | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.digest.hmac | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.digest.md | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.digest.murmurhash | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.digest | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.digest.ripemd | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.digest.sha | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.encoding | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.exception | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.affix_allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.aligned_block_list | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.allocator_list | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.ascending_page_allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.bitmapped_block | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.bucketizer | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.fallback_allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.free_list | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.free_tree | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.kernighan_ritchie | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.null_allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.quantizer | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.region | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.scoped_allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.segregator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.building_blocks.stats_collector | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.common | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.gc_allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.mallocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.mmap_allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.showcase | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.allocator.typed | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.checkedint | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.logger.core | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.logger.filelogger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.logger.multilogger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.logger.nulllogger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.experimental.logger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.file | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.format | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.format.read | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.format.spec | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.format.write | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.functional | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| std.getopt | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.int128 | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.json | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.logger.core | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.logger.filelogger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.logger.multilogger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.logger.nulllogger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.logger | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.algebraic | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.constants | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.exponential | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.hardware | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.operations | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.remainder | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.rounding | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.traits | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.math.trigonometry | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.mathspecial | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.meta | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| std.mmfile | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.net.isemail | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.numeric | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.outbuffer | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.parallelism | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| std.path | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.process | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.random | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.range.interfaces | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| std.range | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.range.primitives | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| std.regex | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.signals | blocked-direct-port | D delegate/template/runtime lifetime semantics cannot be preserved directly by this compiler. |
| std.socket | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.stdint | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.stdio | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.string | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.sumtype | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| std.system | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.traits | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| std.typecons | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| std.typetuple | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| std.uni | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| std.uri | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.utf | partial | Implemented explicit typed subset; see RESTORED-APIS.md. Generic Phobos API parity remains incomplete. |
| std.uuid | partial | Typed subset implemented; remaining upstream APIs are deferred. |
| std.variant | blocked-direct-port | D compile-time type introspection, typelists, template evaluation, mixins or runtime TypeInfo have no verified equivalent in this compiler. |
| std.windows.charset | deferred-os-service | OS-supported functionality is permitted by dependency policy; a tested CMotive implementation is not yet provided. |
| std.windows.registry | deferred-os-service | OS-supported functionality is permitted by dependency policy; a tested CMotive implementation is not yet provided. |
| std.windows.syserror | deferred-os-service | OS-supported functionality is permitted by dependency policy; a tested CMotive implementation is not yet provided. |
| std.zip | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
| unittest | deferred | Not implemented; requires further porting and tests. Not a claim of impossibility. |
