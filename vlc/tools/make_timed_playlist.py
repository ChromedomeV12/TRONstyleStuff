"""Create a VLC XSPF playlist with per-track start/stop points from CSV."""
import argparse
import csv
import math
from pathlib import Path
import xml.etree.ElementTree as ET

XSPF='http://xspf.org/ns/0/'
VLC='http://www.videolan.org/vlc/playlist/ns/0/'
APP='http://www.videolan.org/vlc/playlist/0'
ET.register_namespace('',XSPF)
ET.register_namespace('vlc',VLC)

def seconds(value):
    parts=value.strip().split(':')
    if len(parts)>3 or any(not p for p in parts):raise ValueError('Use seconds, MM:SS, or HH:MM:SS.')
    nums=[float(p) for p in parts]
    if any(not math.isfinite(n) or n<0 for n in nums):raise ValueError('Times must be finite and nonnegative.')
    if len(nums)>1 and (any(n>=60 for n in nums[1:]) or any(n!=int(n) for n in nums[:-1])):
        raise ValueError('Clock times require whole hours/minutes and seconds below 60.')
    total=0
    for n in nums:total=total*60+n
    return total

def build(source):
    root=ET.Element(f'{{{XSPF}}}playlist',version='1')
    ET.SubElement(root,f'{{{XSPF}}}title').text=source.stem
    tracks=ET.SubElement(root,f'{{{XSPF}}}trackList')
    with source.open(newline='',encoding='utf-8-sig') as stream:
        reader=csv.DictReader(stream)
        if not reader.fieldnames or not {'file','start','stop'}.issubset(reader.fieldnames):
            raise ValueError('CSV needs file,start,stop columns; title is optional.')
        for index,row in enumerate(reader,1):
            try:
                path=Path(row['file']).expanduser()
                if not path.is_absolute():path=source.parent/path
                path=path.resolve()
                if not path.is_file():raise ValueError(f'Media file not found: {path}')
                start=seconds(row['start'] or '0')
                stop=seconds(row['stop']) if row['stop'] else None
                if stop is not None and stop<=start:raise ValueError('Stop must be later than start.')
                track=ET.SubElement(tracks,f'{{{XSPF}}}track')
                ET.SubElement(track,f'{{{XSPF}}}location').text=path.as_uri()
                ET.SubElement(track,f'{{{XSPF}}}title').text=row.get('title') or path.stem
                ext=ET.SubElement(track,f'{{{XSPF}}}extension',application=APP)
                ET.SubElement(ext,f'{{{VLC}}}option').text=f'start-time={start:g}'
                if stop is not None:ET.SubElement(ext,f'{{{VLC}}}option').text=f'stop-time={stop:g}'
            except (ValueError,TypeError,KeyError) as exc:
                raise ValueError(f'CSV row {index+1}: {exc}') from exc
    if not len(tracks):raise ValueError('CSV contains no tracks.')
    ET.indent(root)
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if args.output.suffix.lower()!='.xspf':parser.error('Output must have the .xspf extension.')
    try:
        data=build(args.csv.resolve())
        with args.output.open('xb') as out:out.write(data)
    except (ValueError,OSError) as exc:parser.exit(1,f'{exc}\n')
    print(f'Created {args.output}. Open it in VLC; transitions are hard cuts, not crossfades.')

if __name__=='__main__':main()
