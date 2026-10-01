from pathlib import Path
import colorsys
import json
import numpy as np
from PIL import Image, ImageCms

root=Path(__file__).resolve().parent.parent
previous=Image.open(root/'outputs/shanghai-tron-uprising-color-grade.png').convert('RGB')
original=Image.open(root/'inputs/source.jpg').convert('RGB')
assert original.size == previous.size == (4704,3136)
weights=np.array([.2126,.7152,.0722],dtype=np.float32)
output=np.empty((original.height,original.width,3),dtype=np.uint8)
old_highlights=[]
new_highlights=[]
hue_samples=[]

def smoothstep(x):
    x=np.clip(x,0,1)
    return x*x*(3-2*x)

# Harmonize original facade and reflection hues into several nearby cool
# families. Their original color boundaries provide the masks, so colored
# light and its reflection receive the same hue treatment without painting
# new shapes or adding spatial gradients across the photograph.
source_hues=np.array([0,30,60,90,120,150,180,210,240,270,300,330,360])
cool_hues=np.array([180,194,208,184,176,180,187,201,212,207,196,185,180])
pure_hue_lut=np.array([colorsys.hsv_to_rgb(h/360,1,1) for h in np.linspace(0,360,4097)],dtype=np.float32)

for top in range(0,original.height,128):
    bottom=min(top+128,original.height)
    box=(0,top,original.width,bottom)
    old=np.asarray(previous.crop(box),dtype=np.float32)/255
    source_hsv=np.asarray(original.crop(box).convert('HSV'),dtype=np.float32)/255
    base_hsv=np.asarray(previous.crop(box).convert('HSV'),dtype=np.float32)/255
    y=old@weights
    # A gentle shoulder reduces bright lights by up to 12%, leaving dark
    # building detail and the main shadow grade unchanged.
    shoulder=smoothstep((y-.30)/.65)
    target_y=y*(1-.12*shoulder)
    mapped_hue=np.interp(source_hsv[:,:,0]*360,source_hues,cool_hues)
    color_confidence=smoothstep((source_hsv[:,:,1]-.08)/.60)
    hue=base_hsv[:,:,0]*360+(mapped_hue-base_hsv[:,:,0]*360)*color_confidence*.95
    # Favor variation in illuminated surfaces; keep very dark tones stable.
    saturation=np.maximum(base_hsv[:,:,1],.16+.35*source_hsv[:,:,1])
    saturation=np.clip(saturation,0,.90)
    rgb_hue=pure_hue_lut[np.rint(hue/360*4096).astype(int)]
    rgb=1-saturation[:,:,None]+saturation[:,:,None]*rgb_hue
    rgb=rgb/np.maximum((rgb@weights)[:,:,None],1e-6)
    chroma=target_y[:,:,None]*(rgb-1)
    # Compress chroma toward equal-channel gray only when needed for gamut,
    # maintaining target luminance instead of hard clipping neon channels.
    upper=np.max(chroma,axis=2)
    lower=np.min(chroma,axis=2)
    amount=np.minimum(1,np.minimum((1-target_y)/np.maximum(upper,1e-6),target_y/np.maximum(-lower,1e-6)))
    adjusted=target_y[:,:,None]+chroma*amount[:,:,None]
    # Preserve shadow colors, using a smooth light-level mask.
    mask=smoothstep((y-.035)/.18)
    result=old*(1-mask[:,:,None])+adjusted*mask[:,:,None]
    output[top:bottom]=np.rint(np.clip(result,0,1)*255).astype(np.uint8)
    bright=y>.65
    old_highlights.extend(y[bright][::16].tolist())
    new_highlights.extend((result@weights)[bright][::16].tolist())
    hue_samples.extend(hue[(y>.20)&(y<.70)&(source_hsv[:,:,1]>.40)][::32].tolist())

path=root/'outputs/shanghai-tron-uprising-refined.png'
Image.fromarray(output).save(path,icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
check=Image.open(path)
assert check.size==original.size
assert check.info.get('icc_profile')
assert np.array_equal(np.asarray(check),output)
preview=check.copy()
preview.thumbnail((1500,1000))
preview.save(root/'work/uprising-refined-preview.png')
report={
 'dimensions':list(check.size),
 'profile':'sRGB IEC61966-2.1',
 'method':'Color and tone adjustments only, original image geometry and texture retained. Hue variations follow original colors, including their existing reflections.',
 'light_shoulder_max_reduction_percent':12,
 'bright_pixel_mean_reduction_percent':round((1-np.mean(new_highlights)/np.mean(old_highlights))*100,2),
 'colored_midtone_hue_percentiles_degrees':dict(zip(['10','50','90'],np.round(np.percentile(hue_samples,[10,50,90]),2).tolist())),
 'verification':'Saved PNG reopened and checked for exact dimensions, sRGB tagging and unchanged saved pixel values.'
}
(root/'outputs/uprising-refined-color-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
