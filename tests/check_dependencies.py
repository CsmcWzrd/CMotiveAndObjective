#!/usr/bin/env python3
"""Fail-closed Linux ELF release audit; no third-party Python packages needed."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from emit_core import source_fingerprint


def audit(library, policy):
    fingerprint = source_fingerprint()
    if b'CMO-SOURCE-SHA256:' + fingerprint.encode() + b'\0' not in library.read_bytes():
        raise ValueError('Library is stale relative to the maintained source/profile')
    def readelf(*args):
        return subprocess.check_output(['readelf', '-W', *args, str(library)], text=True,
                                       env={**os.environ, 'LC_ALL': 'C'})
    dynamic = readelf('-d')
    needed = sorted(re.findall(r'\(NEEDED\).*\[(.*?)\]', dynamic))
    if needed != sorted(policy['linux_needed']):
        raise ValueError('Unexpected OS/library dependency set: ' + repr(needed))
    if re.search(r'\((?:RPATH|RUNPATH)\)', dynamic):
        raise ValueError('Release library must not embed runtime search paths')
    if 'BIND_NOW' not in dynamic:
        raise ValueError('Immediate relocation binding is required')
    imports = {}
    for line in readelf('--dyn-syms').splitlines():
        fields = line.split()
        if len(fields) >= 8 and fields[6] == 'UND':
            name = fields[7].split('@')[0]
            imports[name] = fields[4]
    required = set(policy['linux_required_imports'])
    optional = set(policy['linux_optional_imports'])
    weak = set(policy['linux_optional_weak_imports'])
    if required - imports.keys() or imports.keys() - required - optional - weak:
        raise ValueError('Unapproved imports or missing allocator: ' + repr(imports))
    if any(imports[n] != 'WEAK' for n in weak & imports.keys()):
        raise ValueError('Compiler instrumentation imports must be weak')
    segments = readelf('-l')
    stacks = [line for line in segments.splitlines() if line.strip().startswith('GNU_STACK')]
    if len(stacks) != 1 or 'E' in ''.join(stacks[0].split()[6:-1]):
        raise ValueError('Non-executable stack required')
    if not any(line.strip().startswith('GNU_RELRO') for line in segments.splitlines()):
        raise ValueError('RELRO segment required')
    for line in segments.splitlines():
        if line.strip().startswith('LOAD'):
            flags = ''.join(line.split()[6:-1])
            if 'W' in flags and 'E' in flags:
                raise ValueError('Writable executable segment rejected')
    return {'status': 'PASS', 'profile': policy['profile'],
            'source_fingerprint': fingerprint,
            'library_sha256': hashlib.sha256(library.read_bytes()).hexdigest(),
            'needed': needed, 'imports': imports, 'full_relro': True,
            'executable_stack': False, 'runtime_search_path': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('library', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    policy_path = ROOT / 'build-support/dependency-policy.json'
    report = audit(args.library, json.loads(policy_path.read_text()))
    report['policy_sha256'] = hashlib.sha256(policy_path.read_bytes()).hexdigest()
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
