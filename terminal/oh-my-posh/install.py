#!/usr/bin/env python3
"""Install the prompt into the current Linux user's Bash configuration."""
import datetime
import pathlib
import shutil

source = pathlib.Path(__file__).resolve().parent
home = pathlib.Path.home()
binary = home / '.local/bin/oh-my-posh'
if not binary.is_file():
    raise SystemExit('Install native Linux Oh My Posh in ~/.local/bin first; see README.md.')
bashrc = home / '.bashrc'
text = bashrc.read_text()
old = 'if command -v starship >/dev/null 2>&1; then\n  eval "$(starship init bash)"\nfi'
begin, end = '# BEGIN TRON Oh My Posh', '# END TRON Oh My Posh'
block = begin + '\n' + (source / 'bash-init.sh').read_text().rstrip() + '\n' + end
if begin in text and end in text:
    start = text.index(begin)
    finish = text.index(end, start) + len(end)
    updated = text[:start] + block + text[finish:]
elif text.count(old) == 1:
    updated = text.replace(old, block, 1)
    updated = updated.replace('# Starship\n' + begin, '# TRON prompt\n' + begin, 1)
else:
    raise SystemExit('Expected one Starship block or existing managed TRON block. Merge bash-init.sh manually to avoid duplicate prompt engines.')
backup = home / '.config/tron/backups' / datetime.datetime.now().strftime('omp-%Y%m%d-%H%M%S-%f')
backup.mkdir(parents=True)
shutil.copy2(bashrc, backup / 'bashrc')
destination = home / '.config/oh-my-posh/TRON.omp.json'
destination.parent.mkdir(parents=True, exist_ok=True)
if destination.exists():
    shutil.copy2(destination, backup / 'TRON.omp.json')
shutil.copy2(source / 'TRON.omp.json', destination)
bashrc.write_text(updated)
assert bashrc.read_text().count(begin) == 1
print(f'Installed {destination}; Bash backup: {backup / "bashrc"}')
