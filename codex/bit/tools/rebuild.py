"""Rebuild the last published atlas with the installed bundled pet pipeline.

This is offline reproduction, not pet creation/update. The approved idle draft
is deliberately excluded from this published build command.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pet-tools', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'build/published')
    args = parser.parse_args(); tools = args.pet_tools.resolve(); out = args.output.resolve()
    if out == ROOT or out.is_relative_to(ROOT/'assets'):
        raise SystemExit('Use a separate build directory; retained assets are read-only inputs.')
    if (out/'final/spritesheet.png').exists():
        raise SystemExit('Choose a fresh output directory; do not repeat cleanup on an existing final atlas.')
    def run(name, *params):
        result = subprocess.run([sys.executable, str(tools/name), *map(str,params)], capture_output=True, text=True)
        if result.returncode:
            print(result.stdout); print(result.stderr, file=sys.stderr); raise SystemExit(result.returncode)
    def render(stage):
        subprocess.run([sys.executable, str(ROOT/'tools/render.py'), stage, '--output', str(out)], check=True)

    run('prepare_pet_run.py', '--pet-name', 'Bit', '--reference', ROOT/'assets/published/base.png',
        '--description', 'Rigid equal-edge blue-white geometric companion.', '--output-dir', out, '--chroma-key', '#FF7F00')
    render('standard')
    run('extract_strip_frames.py', '--decoded-dir', out/'decoded', '--output-dir', out/'frames', '--method', 'auto', '--chroma-key', '#FF7F00')
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
    expected = json.loads((ROOT/'project.json').read_text())['published']['sha256']
    actual = hashlib.sha256((out/'final/spritesheet.png').read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'Rebuild hash mismatch: {actual}. Inspect version/encoding differences; this is not an accepted replacement.')
    print(json.dumps({'ok':True,'matches_published_encoded_bytes':True,'sha256':actual},indent=2))

if __name__ == '__main__': main()
