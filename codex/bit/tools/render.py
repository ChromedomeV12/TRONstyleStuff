"""Native frames adapted from approved source/render.py under manual-technique exception.
Loads the approved mesh unchanged. Only rigid rotations/translations and light
intensity vary. Source rasterizer, palette, fixed orthographic view and shading
are retained. Native alpha comes from triangle coverage, never dark-color deletion.
"""
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

PROJECT=Path(__file__).resolve().parents[1]
P=PROJECT/'build'
MESH=PROJECT/'assets/mesh.npz'
IDLE_MULTIPLIER=1
EXPECTED='025ad41522c78555813102b1657d73e712b628b7454e5b5963439961f7a12c57'
assert hashlib.sha256(MESH.read_bytes()).hexdigest()==EXPECTED
mesh=np.load(MESH,allow_pickle=False)
v=mesh['vertices']; faces=mesh['faces']; edges=mesh['edges']
assert v.shape==(32,3) and faces.shape==(60,3) and edges.shape==(90,2)
assert np.max(np.abs(np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1)-2))<1e-12
def rx(a): return np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
def ry(a): return np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
def rz(a): return np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
VIEW=rx(1.03)@rz(.24)
CUE_FACE=46
CUE_VECTOR=v[faces[CUE_FACE]].mean(axis=0)
CAMERA_ROLL=-3
ROLL=rz(math.radians(CAMERA_ROLL))
SS=3; WIDTH=192; HEIGHT=208; W=WIDTH*SS; H=HEIGHT*SS; SCALE=23*SS
LIGHT=np.array([-.45,.7,1.]); LIGHT/=np.linalg.norm(LIGHT)
FILL=np.array([.8,-.25,.4]); FILL/=np.linalg.norm(FILL)
HALF=LIGHT+[0,0,1]; HALF/=np.linalg.norm(HALF)
reports=[]

def align(a,b):
    a=a/np.linalg.norm(a); b=b/np.linalg.norm(b); c=float(np.dot(a,b)); w=np.cross(a,b)
    if np.linalg.norm(w)<1e-12: return np.eye(3)
    K=np.array([[0,-w[2],w[1]],[w[2],0,-w[0]],[-w[1],w[0],0]])
    return np.eye(3)+K+K@K/(1+c)

def aimed(degrees,tilt=20):
    # One fixed existing triangle receives the user-approved blue brightness cue.
    # Its centroid is the aiming landmark; the whole solid rotates rigidly.
    a=math.radians(degrees+CAMERA_ROLL); t=math.radians(tilt)
    target=np.array([math.sin(a)*math.sin(t),math.cos(a)*math.sin(t),math.cos(t)])
    return ROLL@align(VIEW@CUE_VECTOR,target)@VIEW

def render(label,rotation,dy=0,brightness=1.0):
    vv=v@rotation.T
    error=float(np.max(np.abs(np.linalg.norm(vv[edges[:,0]]-vv[edges[:,1]],axis=1)-2)))
    assert error<1e-12 and np.max(np.abs(rotation.T@rotation-np.eye(3)))<1e-12
    xy=vv[:,:2]*[SCALE,-SCALE]+[W/2,(108+dy)*SS]
    zbuffer=np.full((H,W),-np.inf,np.float32)
    facebuffer=np.full((H,W),-1,np.int16)
    rgb=np.zeros((H,W,3),np.float32); em=np.zeros((H,W),np.float32)
    cue_coverage=0
    for face_index,f in enumerate(faces):
        a,b,c=vv[f]; normal=np.cross(b-a,c-a); normal/=np.linalg.norm(normal)
        if normal[2]<=0: continue
        poly=xy[f]; xmin,ymin=np.floor(poly.min(axis=0)).astype(int); xmax,ymax=np.ceil(poly.max(axis=0)).astype(int)
        xmin=max(0,xmin); ymin=max(0,ymin); xmax=min(W-1,xmax); ymax=min(H-1,ymax)
        if xmin>xmax or ymin>ymax: continue
        X,Y=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
        (x0,y0),(x1,y1),(x2,y2)=poly; den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
        if abs(den)<1e-10: continue
        u=((y1-y2)*(X-x2)+(x2-x1)*(Y-y2))/den
        w=((y2-y0)*(X-x2)+(x0-x2)*(Y-y2))/den; t=1-u-w
        z=u*a[2]+w*b[2]+t*c[2]; sl=np.s_[ymin:ymax+1,xmin:xmax+1]
        mask=(u>=0)&(w>=0)&(t>=0)&(z>zbuffer[sl]); zbuffer[sl][mask]=z[mask]
        facebuffer[sl][mask]=face_index
        L=max(0,np.dot(normal,LIGHT)); F=max(0,np.dot(normal,FILL)); spec=max(0,np.dot(normal,HALF))**15
        shade=np.array([3,18,55])+L**1.6*np.array([155,205,200])+F*np.array([8,27,43])+spec*np.array([95,85,65])
        color=np.broadcast_to(shade,(*u.shape,3)).copy()*(.96+.04*(z/3.15))[:,:,None]
        if face_index==CUE_FACE:
            color[:]=np.array([28,168,255])*(.94+.06*normal[2])
            cue_coverage=int(np.count_nonzero(mask))
        rgb[sl][mask]=color[mask]
        area=abs(den); alts=np.array([area/np.linalg.norm(poly[1]-poly[2]),area/np.linalg.norm(poly[2]-poly[0]),area/np.linalg.norm(poly[0]-poly[1])])
        dist=np.minimum(np.minimum(u*alts[0],w*alts[1]),t*alts[2]); e=np.clip(1-dist/(1.65*SCALE/88),0,1)
        em[sl][mask]=e[mask]
    coverage=np.isfinite(zbuffer)
    maskimg=Image.fromarray(np.uint8(em*255))
    bloom=np.asarray(maskimg.filter(ImageFilter.GaussianBlur(4*SCALE/88)),dtype=float)/255
    broad=np.asarray(maskimg.filter(ImageFilter.GaussianBlur(12*SCALE/88)),dtype=float)/255
    # Keep approved blue edge emission on the solid. The native contract has no
    # detached halo or opaque navy backdrop; preview compositing supplies navy.
    rgb+=bloom[:,:,None]*[20,250,800]+broad[:,:,None]*[10,150,650]
    rgb=rgb*(1-em[:,:,None]*.9)+np.array([180,246,255])*em[:,:,None]*.9
    cue_mask=facebuffer==CUE_FACE
    rgb[cue_mask]=np.array([0,235,255])*(1-em[cue_mask,None]*.5)+np.array([70,245,255])*em[cue_mask,None]*.5
    rgba=np.zeros((H,W,4),np.uint8); rgba[:,:,:3]=np.uint8(np.clip(rgb*brightness,0,255)); rgba[:,:,3]=np.uint8(coverage)*255
    rgba[~coverage,:3]=0
    img=Image.fromarray(rgba).resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
    b=img.getbbox(); assert b and b[0]>1 and b[1]>1 and b[2]<191 and b[3]<207,(label,b)
    landmark=(xy[9]/SS).tolist()
    cue_xy=(xy[faces[CUE_FACE]].mean(axis=0)/SS).tolist()
    lx,ly=np.clip(np.floor(xy[9]).astype(int),[0,0],[W-1,H-1])
    landmark_depth_gap=float(zbuffer[ly,lx]-vv[9,2])
    reports.append({'frame':label,'edge_max_error':error,'rotation':rotation.tolist(),'translation_y_pixels':dy,
                    'brightness':brightness,'bbox':list(b),'landmark_vertex':9,'landmark_xy':landmark,
                    'landmark_depth_gap':landmark_depth_gap,'landmark_visible':landmark_depth_gap<.09,'fixed_pixels_per_unit':23})
    reports[-1].update({'cue_face':CUE_FACE,'cue_centroid_xy':cue_xy,'cue_covered_supersamples_before_later_faces':cue_coverage,'cue_final_visible_supersamples':int(cue_mask.sum()),'global_camera_roll_degrees':CAMERA_ROLL})
    return img

def write_strip(state,items):
    frames=[render(f'{state}/{i:02d}',**x) for i,x in enumerate(items)]
    folder=P/'rendered-frames'/state; folder.mkdir(parents=True,exist_ok=True)
    strip=Image.new('RGBA',(WIDTH*len(frames),HEIGHT))
    for i,im in enumerate(frames): im.save(folder/f'{i:02d}.png'); strip.alpha_composite(im,(i*WIDTH,0))
    (P/'decoded').mkdir(exist_ok=True); strip.save(P/'decoded'/f'{state}.png')

def frame(rotation=ROLL@VIEW,dy=0,brightness=1): return dict(rotation=rotation,dy=dy,brightness=brightness)
def idle():
    write_strip('idle',[frame(ROLL@VIEW@rz(math.radians(a*IDLE_MULTIPLIER)),dy=y,brightness=b) for a,y,b in [(0,0,1),(.8,-.5,1.01),(1,-1,1.02),(0,-1.2,1.01),(-1,-.8,.99),(-.8,-.2,.99)]])

def standard():
    base=render('base',ROLL@VIEW); base.save(P/'decoded/base.png'); base.save(P/'references/canonical-base.png')
    idle()
    for state,deg in [('running-right',90),('running-left',270)]:
        write_strip(state,[frame(rz(math.radians(a))@aimed(deg,20),dy=y) for a,y in [(0,0),(1,-.3),(1.5,-1),(1,-1.7),(0,-2),(-1,-1.7),(-1.5,-1),(-1,-.3)]])
    write_strip('waving',[frame(ROLL@rz(math.radians(a))@VIEW,dy=y,brightness=b) for a,y,b in [(0,0,1),(-4,-1.5,1.025),(4,-1.5,1.025),(0,0,1)]])
    write_strip('jumping',[frame(ROLL@VIEW,dy=y) for y in [0,-6,-12,-6,0]])
    write_strip('failed',[frame(ROLL@rx(math.radians(a))@VIEW,dy=y,brightness=b) for a,y,b in [(0,0,1),(-2,.5,.96),(-5,1.5,.9),(-8,2.5,.84),(-9,3,.82),(-6,2,.89),(-3,1,.95),(0,0,1)]])
    write_strip('waiting',[frame(ROLL@rx(math.radians(a))@VIEW,dy=y,brightness=b) for a,y,b in [(0,0,1),(3,-.5,1.01),(6,-1,1.02),(7,-1.2,1.03),(4,-.8,1.02),(1,-.2,1.01)]])
    write_strip('running',[frame(ROLL@VIEW@rz(math.radians(a)),dy=y,brightness=b) for a,y,b in [(0,0,1),(2,-.5,1.025),(3,-1,1.04),(0,-1.2,1.025),(-3,-.8,1.01),(-2,-.2,1)]])
    write_strip('review',[frame(ROLL@ry(math.radians(a))@rx(math.radians(b))@VIEW) for a,b in [(0,0),(-4,-2),(-2,-4),(2,-4),(4,-2),(0,0)]])
def main():
    global P,IDLE_MULTIPLIER
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=['idle','standard','cardinals','row9','row10'])
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--idle-profile',choices=['published','approved-draft'],default='published')
    args=parser.parse_args()
    P=args.output.resolve();IDLE_MULTIPLIER=3 if args.idle_profile=='approved-draft' else 1
    for name in ['decoded','references','qa']:(P/name).mkdir(parents=True,exist_ok=True)
    if args.stage=='idle': idle()
    elif args.stage=='standard': standard()
    elif args.stage=='cardinals': write_strip('look-cardinals',[frame(aimed(a,20)) for a in [0,90,180,270]])
    elif args.stage=='row9': write_strip('look-row-9',[frame(aimed(a,20)) for a in np.arange(0,180,22.5)])
    else: write_strip('look-row-10',[frame(aimed(a,20)) for a in np.arange(180,360,22.5)])
    report={'ok':True,'mesh_sha256':EXPECTED,'vertices':32,'faces':60,'edges':90,'edge_length':2,
            'max_edge_error':max(x['edge_max_error'] for x in reports),'geometry_deformed':False,
            'projection':'fixed orthographic','source':'Approved source/render.py rasterizer adapted for native alpha and rigid state transforms',
            'manual_technique':'Explicit user request; sprite-sheet-contract.md manual-technique exception', 'frames':reports}
    (P/'qa').mkdir(exist_ok=True); (P/'qa'/f'render-{args.stage}.json').write_text(json.dumps(report,indent=2)); print(json.dumps({k:v for k,v in report.items() if k!='frames'}))
if __name__=='__main__': main()
