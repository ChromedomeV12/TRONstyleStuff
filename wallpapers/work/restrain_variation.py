from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageCms

root=Path(__file__).resolve().parent.parent
base=Image.open(root/'outputs/shanghai-tron-uprising-refined.png').convert('RGB')
strong=Image.open(root/'outputs/shanghai-tron-building-colors.png').convert('RGB')
assert base.size==strong.size==(4704,3136)
a=np.asarray(base,dtype=np.float32)
b=np.asarray(strong,dtype=np.float32)
# Reduce the previous selective correction to 28% strength, identically
# for facades and their reflection footprints. This restores the reference-
# based grade's dominant palette and keeps only a subdued color separation.
strength=.28
out=np.rint(a+strength*(b-a)).clip(0,255).astype(np.uint8)
path=root/'outputs/shanghai-tron-uprising-subtle.png'
Image.fromarray(out).save(path,icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
saved=Image.open(path)
assert saved.size==base.size
assert saved.info.get('icc_profile')
assert np.array_equal(np.asarray(saved),out)
assert np.max(out.max(axis=2).astype(int)-a.max(axis=2))<=1
preview=saved.copy()
preview.thumbnail((1500,1000))
preview.save(root/'work/uprising-subtle-preview.png')
report={
 'dimensions':list(saved.size),
 'profile':'sRGB IEC61966-2.1',
 'selective_color_strength_percent':28,
 'method':'Previous building and reflection color adjustments reduced together over the reference-based, softened-light grade.',
 'preserved':'Photo geometry, original water ripples, full source dimensions, softened highlights.',
 'verification':'PNG reopened; dimensions, profile, saved RGB values and no highlight increase verified.'
}
(root/'outputs/uprising-subtle-color-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
