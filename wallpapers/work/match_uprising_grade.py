from pathlib import Path
from io import BytesIO
import json
import numpy as np
from PIL import Image, ImageCms, PngImagePlugin

root=Path(__file__).resolve().parent.parent
source=root/'inputs/source.jpg'
reference=root/'inputs/uprising-reference.jpg'
w=np.array([.2126,.7152,.0722],dtype=np.float32)
srgb=ImageCms.createProfile('sRGB')
im=Image.open(source)
source_profile='untagged; assumed sRGB'
if im.info.get('icc_profile'):
    profile=ImageCms.ImageCmsProfile(BytesIO(im.info['icc_profile']))
    source_profile=ImageCms.getProfileDescription(profile).strip()
    im=ImageCms.profileToProfile(im,profile,srgb,outputMode='RGB')
else:
    im=im.convert('RGB')

# Reference histogram and conditional RGB averages across every animation
# frame, weighted by display duration. No resizing for measurement.
bins=4096
hist=np.zeros(bins,dtype=np.float64)
sums=np.zeros((bins,3),dtype=np.float64)
gif=Image.open(reference)
durations=[]
for i in range(getattr(gif, 'n_frames', 1)):
    gif.seek(i)
    duration=gif.info.get('duration',100) or 100
    durations.append(duration)
    a=np.asarray(gif.convert('RGB'),dtype=np.float32)/255
    y=a@w
    index=np.minimum((y*(bins-1)).astype(np.int32),bins-1).ravel()
    hist+=np.bincount(index,minlength=bins)*duration
    for c in range(3):
        sums[:,c]+=np.bincount(index,weights=a[:,:,c].ravel(),minlength=bins)*duration
levels=np.linspace(0,1,bins)
cdf=np.cumsum(hist)/hist.sum()
valid=hist>0
colors=np.column_stack([np.interp(levels,levels[valid],sums[valid,c]/hist[valid]) for c in range(3)])
# Smooth palette fluctuations from reference JPEG quantization, keep only cool colors.
kernel=np.ones(25)/25
for c in range(3):
    colors[:,c]=np.convolve(np.pad(colors[:,c],(12,12),mode='edge'),kernel,mode='valid')
colors[:,1]=np.maximum(colors[:,1],colors[:,0])
colors[:,2]=np.maximum(colors[:,2],colors[:,1])
colors*=levels[:,None]/np.maximum(colors@w,1e-7)[:,None]
colors=np.clip(colors,0,1)

a=np.asarray(im,dtype=np.float32)/255
# Source tone includes a small peak-channel component so saturated signs
# remain luminous after their hue is changed. Every operation is pointwise.
tone=.8*(a@w)+.2*a.max(axis=2)
source_hist=np.histogram(tone,bins=bins,range=(0,1))[0]
source_cdf=(np.cumsum(source_hist)-source_hist*.5)/source_hist.sum()
target_tone=np.interp(source_cdf,cdf,levels)
del a
out=np.empty((im.height,im.width,3),dtype=np.uint8)
for c in range(3):
    lut=np.interp(target_tone,levels,colors[:,c])
    out[:,:,c]=np.rint(np.clip(np.interp(tone,levels,lut),0,1)*255).astype(np.uint8)
result=Image.fromarray(out)
output=root/'outputs/shanghai-tron-uprising-color-grade.png'
result.save(output,icc_profile=ImageCms.ImageCmsProfile(srgb).tobytes())
preview=result.copy()
preview.thumbnail((1500,1000))
preview.save(root/'work/uprising-preview.png')

def measurements_from_hist(h):
    c=np.cumsum(h)/h.sum()
    return {str(p):round(float(np.interp(p/100,c,levels)*255),2) for p in [10,25,50,75,90,95,99,99.9]}
out_y=(out.astype(np.float32)/255)@w
out_hist=np.histogram(out_y,bins=bins,range=(0,1))[0]
ref_rgb=sums.sum(axis=0)/hist.sum()*255
out_rgb=out.mean(axis=(0,1))
readback=Image.open(output)
assert readback.size==im.size==(4704,3136)
assert np.array_equal(np.asarray(readback),out)
assert readback.info.get('icc_profile')
report={
 'output':str(output),'dimensions':list(readback.size),
 'method':'Deterministic pointwise color and tone mapping from original photo; no generative editing, geometric transforms, blur, compositing, or added objects.',
 'source_profile':source_profile,'output_profile':'sRGB IEC61966-2.1',
 'reference_frames_checked':getattr(gif, 'n_frames', 1),'reference_duration_ms':sum(durations),
 'reference_assumption':'Reference JPEG interpreted as sRGB. Source mastering gamma cannot be inferred from a screenshot; the output uses the standard sRGB transfer function.',
 'tone_check':'Reference screenshot brightness distribution, measured as Rec.709-weighted encoded RGB luma, matched with a monotonic tone curve. Not a claim of original film colorimetry.',
 'reference_luma_percentiles_0_255':measurements_from_hist(hist),
 'output_luma_percentiles_0_255':measurements_from_hist(out_hist),
 'reference_mean_rgb_0_255':np.round(ref_rgb,2).tolist(),
 'output_mean_rgb_0_255':np.round(out_rgb,2).tolist(),
 'reference_mean_luma_0_255':round(float(ref_rgb@w),2),
 'output_mean_luma_0_255':round(float(out_rgb@w),2),
 'warm_pixels':int(np.count_nonzero((out[:,:,0]>out[:,:,1])|(out[:,:,1]>out[:,:,2]))),
 'verification':'Full-resolution PNG reopened; dimensions, embedded sRGB profile, and all RGB pixel values verified.'
}
(root/'outputs/uprising-color-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
