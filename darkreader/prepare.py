"""Merge TRON into exported Dark Reader data; never edits browser profiles."""
import argparse
import copy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
BEGIN, END = '/* TRONstyleStuff:BEGIN */', '/* TRONstyleStuff:END */'


def merge_settings(settings):
    if not isinstance(settings, dict) or not isinstance(settings.get('theme'), dict):
        raise ValueError('Expected a complete Dark Reader settings export with a theme object.')
    result = copy.deepcopy(settings)
    result['theme'].update(json.loads((ROOT / 'TRON.theme.json').read_text(encoding='utf-8')))
    return result


def merge_fixes(text):
    # The first wildcard block holds common fixes; keep all other blocks intact.
    separator = re.search(r'(?m)^={2,}[ \t]*\r?$', text)
    split = separator.start() if separator else len(text)
    common, rest = text[:split], text[split:]
    lines = common.lstrip('\ufeff \r\n').splitlines()
    if not lines or lines[0].strip() != '*':
        raise ValueError('Expected the full Dynamic Theme fixes text starting with the global * block.')
    if common.count(BEGIN) != common.count(END) or common.count(BEGIN) > 1:
        raise ValueError('Malformed or duplicate TRON block; restore the original fixes first.')
    if BEGIN in common and common.index(END) < common.index(BEGIN):
        raise ValueError('TRON block markers are reversed; restore the original fixes first.')
    common = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\r?\n?', '', common, flags=re.S)
    commands = list(re.finditer(r'(?m)^[A-Z]+(?:[ \t]+[A-Z]+)*[ \t]*\r?$', common))
    css_commands = [i for i, command in enumerate(commands) if command.group().strip() == 'CSS']
    if len(css_commands) > 1:
        raise ValueError('More than one CSS section in the global block.')
    if css_commands:
        index = css_commands[0]
        insertion = commands[index + 1].start() if index + 1 < len(commands) else len(common)
        prefix, suffix = common[:insertion].rstrip(), common[insertion:]
    else:
        prefix, suffix = common.rstrip() + '\n\nCSS', ''
    overlay = (ROOT / 'TRON.css').read_text(encoding='utf-8').strip()
    return prefix + '\n\n' + overlay + '\n\n' + suffix + rest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['settings', 'fixes'])
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Choose a separate output path; keep your original as a backup.')
    original = args.input.read_text(encoding='utf-8-sig')
    try:
        output = (json.dumps(merge_settings(json.loads(original)), indent=4, ensure_ascii=False) + '\n'
                  if args.kind == 'settings' else merge_fixes(original))
    except (ValueError, IndexError) as exc:
        parser.error(str(exc))
    # Exclusive creation also prevents accidentally replacing an earlier backup.
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(output)
    print(f'Created {args.output}. Original unchanged; browser configuration not modified.')


if __name__ == '__main__':
    main()
