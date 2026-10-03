"""Standalone source-only idle comparison. Does not access or update stored pet."""
from pathlib import Path
import importlib.util,hashlib,json,math,sys,argparse
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--pet-tools',type=Path,required=True,help='Installed create-pet scripts directory')
parser.add_argument('--output',type=Path,default=ROOT/'build/idle-comparison')
args=parser.parse_args()
SOURCE=ROOT
OUT=args.output.resolve()
OUT.mkdir(parents=True,exist_ok=True)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
renderer=load('approved_bit_renderer',SOURCE/'tools/render.py')
preview=load('bundled_preview',args.pet_tools.resolve()/'render_animation_previews.py')
poses=[(0,0,1),(.8,-.5,1.01),(1,-1,1.02),(0,-1.2,1.01),(-1,-.8,.99),(-.8,-.2,.99)]
durations=preview.ROW_DURATIONS['idle']
families={}
for name,factor in [('previous-source',1),('draft-3deg',3)]:
    folder=OUT/name;folder.mkdir(exist_ok=True)
    frames=[]
    for index,(angle,dy,brightness) in enumerate(poses):
        frame=renderer.render(f'{name}/{index:02d}',renderer.ROLL@renderer.VIEW@renderer.rz(math.radians(angle*factor)),dy,brightness)
        frame.save(folder/f'{index:02d}.png');frames.append(frame)
    families[name]=frames
    strip=Image.new('RGBA',(192*6,208))
    for i,frame in enumerate(frames):strip.alpha_composite(frame,(192*i,0))
    strip.save(OUT/f'{name}-strip.png')

BG='#111827';TEXT='#e3edf8';MUTED='#a6b8ce'
font=ImageFont.load_default(size=15)
small=ImageFont.load_default(size=12)
title=ImageFont.load_default(size=19)
def composite(frame,width):
    height=round(width*208/192)
    resized=frame.resize((width,height),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(width,height),BG);canvas.alpha_composite(resized);return canvas

rows=[(24,96),(32,155),(48,219),(64,303),(192,405)]
comparisons=[]
for i in range(6):
    canvas=Image.new('RGBA',(580,640),BG);draw=ImageDraw.Draw(canvas)
    draw.text((20,14),'Bit idle: source-only draft',font=title,fill=TEXT)
    draw.text((20,42),'Local approved source; current server sheet not fetched.',font=small,fill=MUTED)
    draw.text((138,69),'Previous: ±1°',font=font,fill=TEXT)
    draw.text((369,69),'Draft: ±3°',font=font,fill=TEXT)
    for width,y in rows:
        draw.text((16,y+3),f'{width}px',font=small,fill=MUTED)
        for col,name in enumerate(['previous-source','draft-3deg']):
            mini=composite(families[name][i],width)
            canvas.alpha_composite(mini,(round(187+230*col-width/2),y))
    draw.text((20,617),'Same 6 poses, timing, bob, lighting and exact rigid mesh.',font=small,fill=MUTED)
    comparisons.append(canvas)
preview.save_preview(comparisons,durations,OUT/'bit-idle-mini-comparison-draft.gif')
comparisons[2].save(OUT/'bit-idle-mini-comparison-draft.png')
board=Image.new('RGBA',(570,410),BG);draw=ImageDraw.Draw(board)
draw.text((10,8),'Source-only idle draft: six ordered poses at actual test size',font=small,fill=TEXT)
y=35
for width in [32,48,64]:
    height=round(width*208/192)
    for name,label in [('previous-source','Previous'),('draft-3deg','Draft ±3°')]:
        draw.text((10,y+4),f'{label} {width}px',font=small,fill=MUTED)
        for i,frame in enumerate(families[name]):
            board.alpha_composite(composite(frame,width),(140+i*70,y))
        y+=height+7
board.save(OUT/'mini-ordered-poses-draft.png')
for width in [24,32,48,64,192]:
    frames=[]
    h=round(width*208/192)
    for i in range(6):
        im=Image.new('RGBA',(width*2+16,h),BG)
        im.alpha_composite(composite(families['previous-source'][i],width),(0,0))
        im.alpha_composite(composite(families['draft-3deg'][i],width),(width+16,0))
        frames.append(im)
    preview.save_preview(frames,durations,OUT/f'comparison-{width}px-draft.gif')

metrics=[]
for width in [24,32,48,64,192]:
    record={'cell_width_pixels':width,'cell_height_pixels':round(width*208/192)}
    for name,frames in families.items():
        arrays=[np.asarray(composite(im,width).convert('RGB'),dtype=float) for im in frames]
        diffs=[float(np.mean(np.abs(arrays[(i+1)%6]-arrays[i]))) for i in range(6)]
        record[name]={'mean_adjacent_rgb_delta':sum(diffs)/6,'max_adjacent_rgb_delta':max(diffs),'loop_seam_rgb_delta':diffs[-1],'extreme_pose_rgb_delta':float(np.mean(np.abs(arrays[2]-arrays[4])))}
    metrics.append(record)

# Verify the previous-source rendering is identical to the locally approved raw
# source frames, not an assertion about current server bytes.
parity=[]
for i,im in enumerate(families['previous-source']):
    old=Image.open(SOURCE/'assets/published/idle-source-strip.png').convert('RGBA').crop((i*192,0,(i+1)*192,208))
    # The retained strip clears RGB under alpha=0 during compositing. Normalize
    # that invisible storage detail before testing exact RGBA source parity.
    normalized=Image.new('RGBA',im.size);normalized.alpha_composite(im)
    parity.append(bool(np.array_equal(np.asarray(normalized),np.asarray(old))))
report={'scope':'Standalone design draft only. Server download returned403; no stored-sheet parity assertion, pet update or final-atlas replacement.','source_renderer_sha256':hashlib.sha256((SOURCE/'tools/render.py').read_bytes()).hexdigest(),'mesh_sha256':renderer.EXPECTED,'same_as_locally_approved_source_frames':parity,'variants':{'previous_angles_degrees':[p[0] for p in poses],'draft_angles_degrees':[p[0]*3 for p in poses]},'unchanged':{'durations_ms':durations,'bob_pixels':[p[1] for p in poses],'brightness':[p[2] for p in poses],'mesh':'exact approved equal-edge mesh','palette':'approved blue-white/navy and fixed blue facet'},'max_edge_length_error':max(r['edge_max_error'] for r in renderer.reports),'mini_sizes_are_test_sizes_not_verified_app_dimensions':True,'metrics':metrics,'render_reports':renderer.reports}
(OUT/'draft-comparison-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'output':str(OUT),'source_frame_parity':all(parity),'max_edge_error':report['max_edge_length_error'],'metrics':metrics},indent=2))
