"""Install TRON and select it in one Pi profile, preserving other settings."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import tempfile


def atomic_write(path, content):
    fd, temp = tempfile.mkstemp(prefix='.tron-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(content)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def install(agent_dir):
    source = Path(__file__).with_name('TRON.json').read_bytes()
    assert json.loads(source)['name'] == 'TRON'
    settings_path = agent_dir / 'settings.json'
    original = settings_path.read_bytes() if settings_path.exists() else None
    settings = json.loads(original.decode('utf-8-sig')) if original else {}
    if not isinstance(settings, dict):
        raise ValueError('Pi settings must be a JSON object; nothing changed.')
    old_theme = settings.get('theme')
    settings['theme'] = 'TRON'
    theme_path = agent_dir / 'themes' / 'TRON.json'
    previous_theme = theme_path.read_bytes() if theme_path.exists() else None
    backup = agent_dir / 'backups' / ('tron-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    backup.mkdir(parents=True, exist_ok=False)
    if original is not None:
        (backup / 'settings.json').write_bytes(original)
    if previous_theme is not None:
        (backup / 'TRON.json').write_bytes(previous_theme)
    (backup / 'restore-info.json').write_text(json.dumps({'previousTheme': old_theme,
        'settingsExisted': original is not None, 'tronExisted': previous_theme is not None}, indent=2), encoding='utf-8')
    theme_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(theme_path, source)
    atomic_write(settings_path, (json.dumps(settings, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))
    expected = json.loads(original.decode('utf-8-sig')) if original else {}
    installed = json.loads(settings_path.read_text(encoding='utf-8'))
    expected['theme'] = 'TRON'
    assert installed == expected, 'Post-install settings verification failed'
    assert theme_path.read_bytes() == source, 'Post-install theme verification failed'
    print(f'Installed: {theme_path}\nSelected: TRON (previous: {old_theme})\nBackup: {backup}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent-dir', type=Path,
                        default=Path(os.environ.get('PI_CODING_AGENT_DIR', str(Path.home() / '.pi' / 'agent'))))
    install(parser.parse_args().agent_dir.expanduser().resolve())
