#!/usr/bin/env python3
"""Emit the core with a fail-closed, pinned, minimal compiler-runtime profile.

Class code is preserved byte for byte. Only the compiler's unused prelude is
removed; the two allocation definitions are copied from the pinned runtime.
This is a compatibility path for the current C-emission compiler, not a new ABI.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def source_fingerprint():
    paths = [ROOT / n for n in ['VERSION', 'ITERATION', 'api.json',
             'tools/emit_core.py', 'build-support/dependency-policy.json']]
    for folder in ['src', 'include/CMotiveAndObjective']:
        paths.extend(p for p in (ROOT / folder).rglob('*') if p.is_file())
    digest = hashlib.sha256()
    for path in sorted(paths):
        name = path.relative_to(ROOT).as_posix().encode()
        data = path.read_bytes()
        digest.update(len(name).to_bytes(8, 'big') + name)
        digest.update(len(data).to_bytes(8, 'big') + data)
    return digest.hexdigest()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def specialize(source, runtime, policy):
    marker = 'typedef struct AlgorithmsI64 {'
    if source.count(marker) != 1:
        raise ValueError('Expected exactly one core class boundary')
    prelude, body = source.split(marker, 1)
    body = marker + body
    if sha(prelude.encode()) != policy['compiler_prelude_sha256']:
        raise ValueError('Compiler prelude changed; review the runtime profile')
    if sha(runtime.encode()) != policy['compiler_runtime_sha256']:
        raise ValueError('Compiler runtime changed; review the allocator semantics')
    # Strip comments and literals only for validation, never from emitted code.
    tokens = re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', ' ', body, flags=re.S)
    if re.search(r'^\s*#', tokens, re.M):
        raise ValueError('Unexpected preprocessor directive in generated core')
    calls = set(re.findall(r'\b([A-Za-z_]\w*)\s*\(', tokens))
    allowed = {'if', 'while', 'for', 'switch', 'return', 'sizeof', 'memset', 'CMotive_New', 'CMotive_Delete'}
    unexpected = {n for n in calls if n not in allowed and not n.startswith('CMotiveAndObjective__')}
    if unexpected:
        raise ValueError('Unapproved generated helper calls: ' + ', '.join(sorted(unexpected)))
    allocators = policy['allocation_definitions']
    if any(runtime.count(line) != 1 for line in allocators):
        raise ValueError('Allocator definitions do not match pinned runtime')
    return ('/* CMotive core: generated class bodies unchanged; minimal runtime profile.\n'
            ' * Allocator definitions: Copyright (c) 2026 CMotive contributors, MIT.\n'
            ' * See toolchain/CMotive-LICENSE-MIT.txt. */\n'
            '#include <stdint.h>\n#include <stddef.h>\n#include <stdlib.h>\n#include <string.h>\n'
            + 'const char CMO_Source_Fingerprint[] = "CMO-SOURCE-SHA256:' + source_fingerprint() + '";\n'
            + '\n'.join(allocators) + '\n' + body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', required=True)
    parser.add_argument('--compiler-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cmo-emit-') as temp:
        raw = Path(temp) / 'core.c'
        subprocess.run([str(Path(args.compiler).resolve()), '-I', str(ROOT / 'include'),
                        '--emit-c', str(ROOT / 'src/CMotiveAndObjective.CMOT'), '-o', str(raw)], check=True)
        policy = json.loads((ROOT / 'build-support/dependency-policy.json').read_text())
        runtime = (args.compiler_root / 'lib/Sys/runtime.c').read_text()
        result = specialize(raw.read_text(), runtime, policy)
    args.output.write_text(result)


if __name__ == '__main__':
    main()
