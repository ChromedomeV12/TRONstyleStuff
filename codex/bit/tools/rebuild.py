"""Rebuild either retained atlas with the installed Work Pets tools, offline.

This does not invoke the separate desktop hatch-pet workflow or install a pet.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pet-tools', type=Path, required=True)
    parser.add_argument('--variant', choices=['published','replacement'], default='published')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(); tools = args.pet_tools.resolve()
    out = (args.output or ROOT/'build'/args.variant).resolve()
    project = json.loads((ROOT/'project.json').read_text())
    record = project['published' if args.variant == 'published' else 'validated_replacement']
    if out == ROOT or out.is_relative_to(ROOT/'assets'):
        raise SystemExit('Use a separate build directory; retained assets are read-only inputs.')
    if (out/'final/spritesheet.png').exists():
        raise SystemExit('Choose a fresh output directory; do not repeat cleanup on an existing final atlas.')
    def run(name, *params):
        result = subprocess.run([sys.executable, str(tools/name), *map(str,params)], capture_output=True, text=True)
        if result.returncode:
            print(result.stdout); print(result.stderr, file=sys.stderr); raise SystemExit(result.returncode)
    def render(stage):
        profile = 'approved-draft' if args.variant == 'replacement' else 'published'
        subprocess.run([sys.executable, str(ROOT/'tools/render.py'), stage, '--output', str(out), '--idle-profile', profile], check=True)

    run('prepare_pet_run.py', '--pet-name', 'Bit', '--reference', ROOT/'assets/published/base.png',
        '--description', 'Rigid equal-edge blue-white geometric companion.', '--output-dir', out, '--chroma-key', '#FF7F00')
    render('standard')
    run('extract_strip_frames.py', '--decoded-dir', out/'decoded', '--output-dir', out/'frames', '--method', 'auto', '--chroma-key', '#FF7F00')
    if args.variant == 'replacement':
        # A wider idle family changes the extractor's shared horizontal center.
        # Translate the complete row once to retain the original neutral anchor;
        # do not recenter individual frames or alter the approved relative motion.
        with Image.open(ROOT/project['published']['atlas']) as published:
            original = published.convert('RGBA').crop((0,0,192,208))
        with Image.open(out/'frames/idle/00.png') as first:
            current = first.convert('RGBA')
        oldbox, newbox = original.getbbox(), current.getbbox()
        if (oldbox[2]-oldbox[0],oldbox[3]-oldbox[1]) != (newbox[2]-newbox[0],newbox[3]-newbox[1]):
            raise SystemExit('Neutral size changed; a shared translation cannot repair this.')
        delta_x,delta_y = oldbox[0]-newbox[0],oldbox[1]-newbox[1]
        for path in sorted((out/'frames/idle').glob('*.png')):
            with Image.open(path) as opened: frame=opened.convert('RGBA')
            shifted=Image.new('RGBA',frame.size);shifted.alpha_composite(frame,(delta_x,delta_y));shifted.save(path)
        (out/'qa/idle-registration.json').write_text(json.dumps({'shared_translation':[delta_x,delta_y],'relative_motion_preserved':True})+'\n')
    def bottom(image): return image.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()[3]
    idle = Image.open(sorted((out/'frames/idle').glob('*.png'))[0]).convert('RGBA')
    paths = sorted((out/'frames/jumping').glob('*.png'))
    jump = [Image.open(p).convert('RGBA') for p in paths]
    delta = bottom(idle)-bottom(jump[0])
    for path, frame in zip(paths,jump):
        shifted = Image.new('RGBA',frame.size); shifted.alpha_composite(frame,(0,delta)); shifted.save(path)
    (out/'qa/jump-registration.json').write_text(json.dumps({'shared_delta_y':delta,'relative_motion_preserved':True})+'\n')
    run('inspect_frames.py','--frames-root',out/'frames','--json-out',out/'qa/frames.json','--require-components')
    run('compose_atlas.py','--frames-root',out/'frames','--output',out/'final/standard.png')
    render('cardinals')
    run('extract_cardinal_anchors.py','--strip',out/'decoded/look-cardinals.png','--output-dir',out/'qa/anchors','--json-out',out/'qa/cardinals.json','--chroma-key','#FF7F00')
    run('compose_cardinal_anchor_strip.py','--anchors-dir',out/'qa/anchors','--output',out/'references/cardinals.png')
    render('row9')
    run('assemble_extended_atlas.py','--base-atlas',out/'final/standard.png','--look-row-9',out/'decoded/look-row-9.png','--registered-row-output',out/'qa/registered-row9.png','--registration-manifest-output',out/'qa/registration.json','--chroma-key','#FF7F00')
    render('row10')
    run('assemble_extended_atlas.py','--base-atlas',out/'final/standard.png','--registered-row-9',out/'qa/registered-row9.png','--row-9-registration',out/'qa/registration.json','--look-row-10',out/'decoded/look-row-10.png','--output',out/'final/raw.png','--chroma-key','#FF7F00')
    run('despill_chroma_edges.py',out/'final/raw.png','--output',out/'final/spritesheet.png','--chroma-key','#FF7F00','--json-out',out/'qa/chroma.json')
    run('validate_atlas.py',out/'final/spritesheet.png','--require-v2','--chroma-key','#FF7F00','--json-out',out/'qa/atlas.json')
    run('make_contact_sheet.py',out/'final/spritesheet.png','--output',out/'qa/contact-sheet.png')
    run('render_animation_previews.py','--frames-root',out/'frames','--output-dir',out/'previews')
    expected = record['sha256']
    actual = hashlib.sha256((out/'final/spritesheet.png').read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'Rebuild hash mismatch: {actual}. Inspect version/encoding differences; this is not an accepted replacement.')
    result = {'ok':True,'variant':args.variant,'matches_retained_encoded_bytes':True,'sha256':actual}
    if args.variant == 'replacement':
        with Image.open(ROOT/project['published']['atlas']) as opened: old=opened.convert('RGBA')
        with Image.open(out/'final/spritesheet.png') as opened: new=opened.convert('RGBA')
        unchanged = old.crop((0,208,1536,2288)).tobytes()==new.crop((0,208,1536,2288)).tobytes()
        if not unchanged: raise SystemExit('A non-idle row changed unexpectedly.')
        result['rows_1_through_10_pixel_identical']=unchanged
        result['idle_source_sha256']=hashlib.sha256((out/'decoded/idle.png').read_bytes()).hexdigest()
        if result['idle_source_sha256'] != record['idle_source_sha256']:
            raise SystemExit('Approved idle source changed.')
    (out/'qa/reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__': main()
