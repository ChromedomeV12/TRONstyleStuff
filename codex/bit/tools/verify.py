"""Verify retained source/assets and run the installed official pet validators."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def run(script, *args):
    result = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
    if result.returncode:
        print(result.stdout); print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pet-tools', type=Path, required=True, help='Installed create-pet scripts directory')
    parser.add_argument('--output', type=Path, default=ROOT/'build/verification')
    args = parser.parse_args(); tools = args.pet_tools.resolve(); out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    project = json.loads((ROOT/'project.json').read_text())
    atlas = ROOT/project['published']['atlas']; mesh_path = ROOT/project['geometry']['mesh']
    assert hashlib.sha256(atlas.read_bytes()).hexdigest() == project['published']['sha256'], 'Published atlas changed'
    assert hashlib.sha256(mesh_path.read_bytes()).hexdigest() == project['geometry']['sha256'], 'Approved mesh changed'
    with np.load(mesh_path, allow_pickle=False) as mesh:
        vertices, faces, edges = mesh['vertices'], mesh['faces'], mesh['edges']
        assert vertices.shape == (32,3) and faces.shape == (60,3) and edges.shape == (90,2)
        error = float(np.abs(np.linalg.norm(vertices[edges[:,0]]-vertices[edges[:,1]], axis=1)-2).max())
        assert error < 1e-12

    parity = {}
    for profile, asset_dir in [('published','published'), ('approved-draft','approved-idle-draft')]:
        render_out = out/profile
        run(ROOT/'tools/render.py', 'idle', '--output', render_out, '--idle-profile', profile)
        generated = Image.open(render_out/'decoded/idle.png').convert('RGBA')
        retained = Image.open(ROOT/f'assets/{asset_dir}/idle-source-strip.png').convert('RGBA')
        parity[profile] = np.array_equal(np.asarray(generated), np.asarray(retained))
        assert parity[profile], f'{profile} renderer differs from retained source strip'

    for file in (ROOT/'assets/approved-idle-draft').glob('*.gif'):
        with Image.open(file) as image:
            durations = []
            for i in range(image.n_frames):
                image.seek(i); durations.append(image.info['duration'])
            assert durations == project['approved_idle_draft']['duration_ms'], f'Timing changed: {file.name}'

    run(tools/'validate_atlas.py', atlas, '--require-v2', '--chroma-key', '#FF7F00', '--json-out', out/'atlas-validation.json')
    run(tools/'measure_direction_continuity.py', atlas, '--json-out', out/'continuity.json')
    run(tools/'validate_pet_quality.py', atlas,
        '--atlas-validation', out/'atlas-validation.json',
        '--chroma-report', ROOT/'reports/chroma-cleanup.json',
        '--frame-review', ROOT/'reports/standard-frames.json',
        '--direction-semantics', ROOT/'reports/direction-semantics.json',
        '--continuity', out/'continuity.json', '--json-out', out/'quality.json')
    quality = json.loads((out/'quality.json').read_text())
    assert quality['ok']
    result = {'ok': True, 'published_atlas_sha256': project['published']['sha256'],
              'mesh_max_edge_error': error, 'idle_source_pixel_parity': parity,
              'bundled_structural_validation': True, 'bundled_quality_validation': True,
              'quality_warning_count': len(quality['warnings']),
              'scope': 'Local retained assets only; no current-server verification or deployment.'}
    (out/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
