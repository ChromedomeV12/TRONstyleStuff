from PIL import Image, ImageCms
import numpy as np
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
ref_path = root/'inputs/legacy-reference.gif'
src_path = root/'inputs/source.jpg'
weights = np.array([.2126,.7152,.0722])
def sample(im):
    im = im.convert('RGB')
    im.thumbnail((800,800))
    return np.asarray(im).reshape(-1,3).astype(np.float32)/255
def stats(a):
    y = a @ weights
    bright = a[y > np.quantile(y,.95)]
    return {'brightness_percentiles_0_255': dict(zip(['1','10','25','50','75','90','95','99','99.9'],np.round(np.quantile(y,[.01,.1,.25,.5,.75,.9,.95,.99,.999])*255,2).tolist())), 'mean_brightness_0_255': round(float(y.mean()*255),2), 'highlight_mean_rgb':np.round(bright.mean(axis=0)*255,2).tolist()}
ref=Image.open(ref_path)
indexes=np.unique(np.linspace(0,ref.n_frames-1,min(16,ref.n_frames)).astype(int))
samples=[]
for idx in indexes:
    ref.seek(int(idx))
    samples.append(sample(ref))
r=np.concatenate(samples)
np.save(root/'work/reference_pixels.npy',r)
src=Image.open(src_path)
grade=Image.open(root/'outputs/shanghai-tron-color-grade.png')
report={'reference_frames':ref.n_frames,'sampled_frames':indexes.tolist(),'source_size':src.size,'source_metadata_keys':list(src.info.keys()),'reference':stats(r),'current_grade':stats(sample(grade))}
print(json.dumps(report,indent=2))
(root/'work/initial-color-check.json').write_text(json.dumps(report,indent=2))
