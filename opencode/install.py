#!/usr/bin/env python3
"""Install and select the native OpenCode v2 TRON theme."""
import argparse,datetime,json,os,pathlib,shutil
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--config-dir',type=pathlib.Path,default=pathlib.Path(os.environ.get('XDG_CONFIG_HOME',str(pathlib.Path.home()/'.config')))/'opencode')
args=parser.parse_args()
directory=args.config_dir.expanduser().resolve()
settings=directory/'cli.json'
before=json.loads(settings.read_text(encoding='utf-8-sig')) if settings.exists() else {}
after={**before,'theme':{**before.get('theme',{}),'name':'TRON','mode':'dark'}}
source=pathlib.Path(__file__).with_name('TRON.json')
document=json.loads(source.read_text(encoding='utf8'))
if 'base' not in document or 'dark' not in document: raise SystemExit('Expected an OpenCode v2 theme.')
backup=directory/'backups'/('tron-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
if settings.exists(): shutil.copy2(settings,backup/'cli.json')
destination=directory/'themes/TRON.json'
destination.parent.mkdir(parents=True,exist_ok=True)
if destination.exists(): shutil.copy2(destination,backup/'TRON.json')
shutil.copy2(source,destination)
settings.write_text(json.dumps(after,indent=2)+'\n',encoding='utf8')
assert json.loads(settings.read_text(encoding='utf8'))==after
assert destination.read_bytes()==source.read_bytes()
print(f'Installed and selected TRON in {directory}; backup: {backup}')
