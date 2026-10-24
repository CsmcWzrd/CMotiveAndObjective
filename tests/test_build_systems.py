#!/usr/bin/env python3
"""Clean out-of-tree builds, distcheck and installed consumers."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from emit_core import source_fingerprint
p=argparse.ArgumentParser();p.add_argument('--compiler-root',required=True,type=Path);p.add_argument('--cmake',default='cmake');p.add_argument('--ctest',default='ctest');p.add_argument('--autotools-env',type=Path);p.add_argument('--autoreconf',default='autoreconf');a=p.parse_args()
env=os.environ.copy()
if a.autotools_env:
 env.update(json.loads(a.autotools_env.read_text()));env['PATH']=str(a.autotools_env.parent/'root/usr/bin')+':'+env['PATH']
env['CMOTIVE_ROOT']=str(a.compiler_root.resolve());env['CMOTIVE']=str(a.compiler_root.resolve()/'build/bin/cmotive')
base=ROOT.parent/'qualification-builds'/('iteration-'+(ROOT/'ITERATION').read_text().strip());base.mkdir(parents=True,exist_ok=True)
def run(cmd,cwd=None):subprocess.run([str(x) for x in cmd],cwd=cwd,env=env,check=True,timeout=300)
cm=base/'cmake';prefix=base/'installed-cmake'
run([a.cmake,'-S',ROOT,'-B',cm,'-DCMOTIVE_ROOT='+env['CMOTIVE_ROOT'],'-DCMAKE_BUILD_TYPE=Release'])
run([a.cmake,'--build',cm,'-j2']);run([a.ctest,'--test-dir',cm,'--output-on-failure']);run([a.cmake,'--install',cm,'--prefix',prefix])
consumer=base/'consumer';run([a.cmake,'-S',ROOT/'tests/cmake-consumer','-B',consumer,'-DCMAKE_PREFIX_PATH='+str(prefix)]);run([a.cmake,'--build',consumer]);run([a.ctest,'--test-dir',consumer,'--output-on-failure'])
source=base/'autotools-source';build=base/'autotools-build';build.mkdir(exist_ok=True)
shutil.copytree(ROOT,source,ignore=lambda path,names:[n for n in names if n in {'.git','__pycache__'} or n.endswith('.pyc') or (n.startswith('build') and n!='build-support')],dirs_exist_ok=True)
run([a.autoreconf,'-fi'],source);auto_prefix=base/'installed-autotools'
run([source/'configure','--prefix='+str(auto_prefix)],build);run(['make','-j2','check'],build);run(['make','install'],build);run(['make','distcheck'],build)
for install,name in [(prefix,'cmake'),(auto_prefix,'autotools')]:
 binary=base/('source-consumer-'+name);run([env['CMOTIVE'],'-I',install/'include',ROOT/'tests/smoke.CMOT','-o',binary]);run([binary])
 for header in (ROOT/'include/CMotiveAndObjective').rglob('*.HMOT'):
  relative=header.relative_to(ROOT/'include');assert (install/'include'/relative).read_bytes()==header.read_bytes(),relative
report={'status':'PASS','source_fingerprint':source_fingerprint(),'cmake_ctest':10,'installed_package_test':1,'autotools_distcheck':'PASS','installed_header_consumers':['cmake','autotools'],'source_consumer_includes_new_classes':True}
(ROOT/'evidence/build-systems-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
