#!/usr/bin/env python3
"""Install the Encom OMP startup widget; preserve the existing theme and shell."""
import pathlib,os,datetime,shutil,subprocess,argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--agent-dir',type=pathlib.Path,default=pathlib.Path(os.environ.get('PI_CODING_AGENT_DIR',str(pathlib.Path.home()/'.omp/agent'))))
parser.add_argument('--omp',default=str(pathlib.Path.home()/'.bun/bin/omp'))
args=parser.parse_args()
agent=args.agent_dir.expanduser().resolve()
env={**os.environ,'PI_CODING_AGENT_DIR':str(agent)}
active=pathlib.Path(subprocess.check_output([args.omp,'config','path'],env=env,text=True).strip()).resolve()
if active not in (agent,agent/'config.yml'):raise SystemExit('Unexpected profile; nothing changed.')
source=pathlib.Path(__file__).with_name('branding')
backup=agent/'backups'/('encom-branding-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
config=agent/'config.yml'
if config.exists():shutil.copy2(config,backup/'config.yml')
destination=agent/'extensions/encom-omp'
if destination.is_symlink():raise SystemExit('Refusing to replace a linked extension directory.')
if destination.exists():shutil.copytree(destination,backup/'encom-omp')
destination.mkdir(parents=True,exist_ok=True)
shutil.copy2(source/'encom-omp.ts',destination/'index.ts')
shutil.copy2(source/'art.ts',destination/'art.ts')
# setHeader is a no-op in OMP: quiet the stock welcome and show a startup widget.
subprocess.run([args.omp,'config','set','startup.quiet','true'],env=env,check=True)
print(f'Installed Encom OMP startup branding: {destination}; backup: {backup}')
