#!/usr/bin/env python3
"""Register the color-only original-logo extension in Oh-My-Pi."""
import argparse, datetime, hashlib, json, os, pathlib, shutil, subprocess

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--omp',default=str(pathlib.Path.home()/'.bun/bin/omp'))
parser.add_argument('--agent-dir',type=pathlib.Path,default=pathlib.Path(os.environ.get('PI_CODING_AGENT_DIR',str(pathlib.Path.home()/'.omp/agent'))))
args=parser.parse_args()
agent=args.agent_dir.expanduser().resolve()
env={**os.environ,'PI_CODING_AGENT_DIR':str(agent)}
def get(key):
    return json.loads(subprocess.check_output([args.omp,'config','get',key,'--json'],env=env))['value']
active=pathlib.Path(subprocess.check_output([args.omp,'config','path'],env=env,text=True).strip()).resolve()
if active not in (agent,agent/'config.yml'):raise SystemExit('Unexpected configuration directory; nothing changed.')
version=subprocess.check_output([args.omp,'--version'],text=True).strip()
if '18.10.3' not in version:raise SystemExit('Logo renderer verified for Oh-My-Pi 18.10.3; review before installing on another version.')
theme=agent/'themes/TRON.json'
digest=hashlib.sha256(theme.read_bytes()).digest()
before=get('extensions')
if not isinstance(before,list):raise SystemExit('Unexpected extension setting; nothing changed.')
destination=agent/'extensions/tron-logo-colors.ts'
backup=agent/'backups'/('tron-logo-colors-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
config=agent/'config.yml'
shutil.copy2(config,backup/'config.yml')
if destination.is_symlink():raise SystemExit('Refusing to replace a linked extension.')
if destination.exists():shutil.copy2(destination,backup/destination.name)
destination.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(pathlib.Path(__file__).with_name('logo-colors')/'index.ts',destination)
entry=str(destination)
after=before if entry in before else [*before,entry]
try:
    subprocess.run([args.omp,'config','set','extensions',json.dumps(after)],env=env,check=True,stdout=subprocess.DEVNULL)
    assert get('extensions')==after
    assert hashlib.sha256(theme.read_bytes()).digest()==digest
except BaseException:
    shutil.copy2(backup/'config.yml',config)
    if (backup/destination.name).exists():shutil.copy2(backup/destination.name,destination)
    else:destination.unlink(missing_ok=True)
    raise
print(f'Installed original-logo color hook: {destination}; backup: {backup}')
