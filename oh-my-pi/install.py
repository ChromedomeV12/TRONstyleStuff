#!/usr/bin/env python3
"""Install a native Oh-My-Pi theme without touching terminal or shell settings."""
import argparse,datetime,json,os,pathlib,shutil,subprocess
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--agent-dir',type=pathlib.Path,default=pathlib.Path(os.environ.get('PI_CODING_AGENT_DIR',str(pathlib.Path.home()/'.omp/agent'))))
parser.add_argument('--omp',default=str(pathlib.Path.home()/'.bun/bin/omp'))
args=parser.parse_args()
agent=args.agent_dir.expanduser().resolve()
source=pathlib.Path(__file__).with_name('TRON.json')
theme=json.loads(source.read_text())
assert theme['name']=='TRON'
if not shutil.which(args.omp): raise SystemExit('Oh-My-Pi executable not found; pass --omp /path/to/omp.')
config=agent/'config.yml'
# Use the actual application's config writer so unrelated preferences are retained.
env={**os.environ,'PI_CODING_AGENT_DIR':str(agent)}
active_path=subprocess.check_output([args.omp,'config','path'],env=env,text=True).strip()
if pathlib.Path(active_path).expanduser().resolve() not in (agent,config):
    raise SystemExit(f'Config path mismatch: {active_path}; no files changed.')
backup=agent/'backups'/('tron-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
if config.exists(): shutil.copy2(config,backup/'config.yml')
destination=agent/'themes/TRON.json'
destination.parent.mkdir(parents=True,exist_ok=True)
if destination.exists(): shutil.copy2(destination,backup/'TRON.json')
shutil.copy2(source,destination)
subprocess.run([args.omp,'config','set','theme.dark','TRON'],env=env,check=True)
selected=subprocess.check_output([args.omp,'config','get','theme.dark'],env=env,text=True).strip().strip('"')
if selected!='TRON': raise SystemExit('Theme preference verification failed; backup retained.')
print(f'Installed {destination}; selected dark theme TRON. Backup: {backup}')
