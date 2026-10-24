#!/usr/bin/env python3
"""Assemble/link custom-register primitives; no C source, libc or ABI wrapper."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--zig',default=shutil.which('zig') or shutil.which('python-zig'));p.add_argument('--output',type=Path,default=ROOT/'build-asm');args=p.parse_args()
if not args.zig:raise SystemExit('Pass --zig /path/to/zig (Zig is used only as assembler/linker driver)')
out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
contract=json.loads((ROOT/'asm/contract.json').read_text());results=[]
for t in contract['targets']:
    directory=out/t['name'];directory.mkdir(exist_ok=True);obj=directory/'primitives.o';elf=directory/'primitives.elf';archive=directory/'libCMotiveAndObjectiveRuntime-1.0.0.a'
    source=ROOT/'asm'/t['source']/'primitives.s'
    for command in [
        [args.zig,'cc','-target',t['triple'],'-x','assembler','-c',str(source),'-o',str(obj)],
        [args.zig,'cc','-target',t['triple'],'-nostdlib','-static','-Wl,-e,CMO_Asm_CopyBytes',str(obj),'-o',str(elf)],
        [args.zig,'ar','rcs',str(archive),str(obj)]]:
        subprocess.run(command,check=True)
    results.append({'target':t['name'],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'object_sha256':hashlib.sha256(obj.read_bytes()).hexdigest(),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    print(t['name']+': assembled and linked without libc',flush=True)
(out/'build-report.json').write_text(json.dumps({'convention':contract['convention'],'assembler_driver':subprocess.check_output([args.zig,'version'],text=True).strip(),'contract_sha256':hashlib.sha256((ROOT/'asm/contract.json').read_bytes()).hexdigest(),'targets':results},indent=2)+'\n')
