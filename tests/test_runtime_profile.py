#!/usr/bin/env python3
"""Regression checks for removal of injected runtime and dependency rejection."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    emit = module(ROOT / 'tools/emit_core.py')
    check = module(ROOT / 'tests/check_dependencies.py')
    compiler, compiler_root = sys.argv[1:3]
    policy = json.loads((ROOT / 'build-support/dependency-policy.json').read_text())
    runtime = (Path(compiler_root) / 'lib/Sys/runtime.c').read_text()
    with tempfile.TemporaryDirectory() as temp:
        raw_path = Path(temp) / 'raw.c'
        subprocess.run([compiler, '-I', str(ROOT / 'include'), '--emit-c',
                        str(ROOT / 'src/CMotiveAndObjective.CMOT'), '-o', str(raw_path)], check=True)
        raw = raw_path.read_text()
        trimmed = emit.specialize(raw, runtime, policy)
        marker = 'typedef struct AlgorithmsI64 {'
        assert trimmed[trimmed.index(marker):] == emit.portable_declarations(raw[raw.index(marker):])
        assert 'runtime.c' not in trimmed and 'cmotive_sys_' not in trimmed
        assert 'CMotive_Cleanup_' not in trimmed
        for cls in policy['retained_stl_classes']:
            assert f'CMotiveAndObjective__{cls}__new' in trimmed
        for source, rt in [(raw.replace('CMotive frontend', 'different frontend'), runtime),
                           (raw, runtime + '\n'),
                           (raw + '\nvoid bad(void){cmotive_sys_net_socket_tcp();}\n', runtime),
                           (raw + '\n#include "wrapper.h"\n', runtime),
                           (raw.replace(marker, ''), runtime)]:
            try:
                emit.specialize(source, rt, policy)
            except ValueError:
                continue
            raise AssertionError('Changed runtime or wrapper was accepted')
        # Real linker fixtures ensure dependency and hardening gates reject ELF
        # images with unresolved symbols, extra libraries, RPATH or lazy binding.
        source = Path(temp) / 'probe.c'
        source.write_text('#include <stdlib.h>\nvoid *probe(void){return calloc(1,8);}\n'
                          'void release(void*p){free(p);}\n'
                          '#ifdef BAD_IMPORT\nextern void unwanted_wrapper(void);\nvoid bad(void){unwanted_wrapper();}\n#endif\n')
        marker = 'CMO-SOURCE-SHA256:' + emit.source_fingerprint()
        source.write_text(source.read_text() + 'const char source_id[]="' + marker + '";\n')
        library = Path(temp) / 'probe.so'
        base = ['cc', '-shared', '-fPIC', str(source), '-o', str(library),'-Wl,-soname,libCMotiveAndObjective-1.0.0.so']
        hardening = ['-Wl,-z,relro,-z,now,-z,noexecstack']
        subprocess.run(base + hardening, check=True)
        check.audit(library, policy, exports={'probe','release','source_id'})
        cases = [hardening + ['-DBAD_IMPORT'], hardening + ['-Wl,--no-as-needed', '-lm'],
                 hardening + ['-Wl,-rpath,/tmp'], ['-Wl,-z,lazy'],
                 ['-Wl,-z,now,-z,norelro'], ['-Wl,-z,now,-z,execstack'],
                 hardening+['-Wl,-soname,unexpected.so'],hardening+['-fvisibility=hidden']]
        for flags in cases:
            subprocess.run(base + flags, check=True)
            try:
                check.audit(library, policy, exports={'probe','release','source_id'})
            except ValueError:
                continue
            raise AssertionError('Unsafe/dependency-injected ELF image accepted: ' + repr(flags))
        raw=bytearray(library.read_bytes());raw[18:20]=(183).to_bytes(2,'little');library.write_bytes(raw)
        try:check.audit(library,policy,exports={'probe','release','source_id'})
        except ValueError:pass
        else:raise AssertionError('Wrong-machine ELF accepted')
        source.write_text(source.read_text().replace(marker, 'CMO-SOURCE-SHA256:' + '0' * 64))
        subprocess.run(base + hardening, check=True)
        try:
            check.audit(library, policy, exports={'probe','release','source_id'})
        except ValueError:
            pass
        else:
            raise AssertionError('Stale source fingerprint accepted')
    print('Runtime profile: PASS; class bodies unchanged; STL retained; 15 negative cases rejected')


if __name__ == '__main__':
    main()
