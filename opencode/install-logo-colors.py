#!/usr/bin/env python3
"""Install a CLI plugin that only recolors OpenCode's original logo."""
import argparse,datetime,hashlib,json,os,pathlib,shutil

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--config-dir',type=pathlib.Path,default=pathlib.Path(os.environ.get('XDG_CONFIG_HOME',str(pathlib.Path.home()/'.config')))/'opencode')
args=parser.parse_args()
directory=args.config_dir.expanduser().resolve()
settings=directory/'cli.json'
config=json.loads(settings.read_text(encoding='utf-8-sig')) if settings.exists() else {}
plugins=config.get('plugins',[])
if not isinstance(plugins,list):raise SystemExit('Unexpected plugin setting; nothing changed.')
theme=directory/'themes/TRON.json'
digest=hashlib.sha256(theme.read_bytes()).digest()
destination=directory/'plugins/tron-logo-colors'
if destination.is_symlink():raise SystemExit('Refusing to replace a linked plugin.')
backup=directory/'backups'/('tron-logo-colors-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
if settings.exists():shutil.copy2(settings,backup/'cli.json')
if destination.exists():shutil.copytree(destination,backup/'tron-logo-colors')
shutil.copytree(pathlib.Path(__file__).with_name('logo-colors'),destination,dirs_exist_ok=True)
entry=destination.as_posix()
after={**config,'plugins':plugins if entry in plugins else [*plugins,entry]}
settings.write_text(json.dumps(after,indent=2)+'\n',encoding='utf-8')
assert json.loads(settings.read_text(encoding='utf-8'))==after
assert hashlib.sha256(theme.read_bytes()).digest()==digest
print(f'Installed original-logo color hook: {destination}; backup: {backup}')
