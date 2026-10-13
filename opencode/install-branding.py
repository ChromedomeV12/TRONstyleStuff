#!/usr/bin/env python3
"""Install EncomCode as a local OpenCode v2 CLI-only plugin."""
import pathlib,os,json,datetime,shutil,argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--config-dir',type=pathlib.Path,default=pathlib.Path(os.environ.get('XDG_CONFIG_HOME',str(pathlib.Path.home()/'.config')))/'opencode')
args=parser.parse_args()
directory=args.config_dir.expanduser().resolve()
settings=directory/'cli.json'
config=json.loads(settings.read_text(encoding='utf-8-sig')) if settings.exists() else {}
plugins=config.get('plugins',[])
if not isinstance(plugins,list):raise SystemExit('Expected a CLI plugin list; nothing changed.')
destination=directory/'plugins/encomcode'
if destination.is_symlink():raise SystemExit('Refusing to replace a linked plugin directory.')
backup=directory/'backups'/('encom-branding-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
if settings.exists():shutil.copy2(settings,backup/'cli.json')
if destination.exists():shutil.copytree(destination,backup/'encomcode')
shutil.copytree(pathlib.Path(__file__).with_name('branding'),destination,dirs_exist_ok=True)
# Explicit CLI-only registration also works when connected to a remote server.
entry=destination.as_posix()
if entry not in plugins:config['plugins']=[*plugins,entry]
settings.write_text(json.dumps(config,indent=2)+'\n',encoding='utf8')
print(f'Installed EncomCode CLI branding: {destination}; backup: {backup}')
