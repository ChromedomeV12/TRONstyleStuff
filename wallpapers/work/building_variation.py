from pathlib import Path
import colorsys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageCms

root=Path(__file__).resolve().parent.parent
im=Image.open(root/'outputs/shanghai-tron-uprising-refined.png').convert('RGB')
W,H=im.size
assert (W,H)==(4704,3136)
sx,sy=W/1920,H/1280
# Facade masks traced on the original photo, with an associated reflection
# footprint. These only select pixels for color correction.
zones=[
 ('west riverfront',207,[(43,997),(54,907),(126,905),(145,998)],85,55),
 ('west blue tower',218,[(141,996),(164,821),(229,826),(232,766),(279,750),(294,999)],215,67),
 ('west turquoise tower',178,[(288,998),(300,846),(323,819),(393,826),(412,997)],351,52),
 ('west dark tower',208,[(377,997),(394,753),(442,730),(470,748),(468,998)],428,34),
 ('cyan square tower',184,[(468,998),(469,774),(535,780),(541,997)],507,36),
 ('slender blue tower',215,[(535,997),(537,801),(553,770),(576,802),(581,997)],555,25),
 ('left central tower',194,[(580,997),(604,756),(622,711),(667,720),(673,997)],629,37),
 ('blue stepped tower',218,[(671,996),(670,755),(683,707),(704,745),(722,803),(728,996)],696,27),
 ('domed cyan tower',182,[(720,996),(721,757),(739,735),(743,716),(760,704),(780,720),(793,743),(803,996)],758,34),
 ('rear blue tower',211,[(859,996),(855,729),(867,704),(910,704),(918,997)],886,35),
 ('Pearl Tower turquoise',174,[(728,982),(786,868),(773,836),(786,797),(809,785),(809,542),(785,507),(784,477),(802,453),(821,443),(824,330),(824,269),(831,180),(838,273),(839,329),(848,383),(838,405),(842,445),(858,462),(872,486),(867,510),(849,536),(849,783),(871,803),(876,831),(866,860),(899,980),(866,980),(832,896),(760,985)],832,79),
 ('waterfront glass domes',181,[(946,998),(960,904),(987,879),(1022,867),(1053,890),(1058,997)],1006,44),
 ('central cyan skyscraper',188,[(1060,897),(1078,568),(1148,563),(1155,638),(1180,892)],1125,48),
 ('Shanghai tower blue',205,[(1265,892),(1262,435),(1285,422),(1308,469),(1332,892)],1296,28),
 ('striped blue tower',218,[(1199,895),(1206,672),(1221,660),(1271,657),(1295,895)],1245,38),
 ('gold roof recolored blue',211,[(1236,981),(1236,807),(1247,784),(1271,775),(1297,798),(1322,980)],1277,27),
 ('right turquoise tower',175,[(1328,980),(1323,779),(1382,763),(1381,740),(1402,726),(1432,760),(1440,982)],1384,44),
 ('right blue facade',213,[(1427,986),(1416,819),(1478,818),(1501,984)],1459,34),
 ('right cyan tower',185,[(1493,986),(1480,734),(1542,725),(1566,733),(1588,987)],1531,40),
 ('right deep blue tower',218,[(1581,988),(1579,824),(1623,800),(1661,819),(1672,987)],1625,35),
 ('Aurora turquoise',176,[(1666,991),(1657,759),(1664,729),(1726,724),(1737,758),(1737,815),(1756,991)],1707,47),
 ('east blue facade',210,[(1751,992),(1757,875),(1787,873),(1815,987)],1782,32),
]
a=np.asarray(im,dtype=np.float32)/255
hsv=np.asarray(im.convert('HSV'),dtype=np.float32)/255
y=a@np.array([.2126,.7152,.0722],dtype=np.float32)
def smooth(v):
    t=np.clip(v,0,1)
    return t*t*(3-2*t)

def colorize(hue):
    # Retain existing highlight brightness (HSV value), with more chroma
    # in midtones than the very brightest, nearly white light sources.
    sat=.72-.26*smooth((y-.22)/.62)
    pure=np.array(colorsys.hsv_to_rgb(hue/360,1,1),dtype=np.float32)
    return hsv[:,:,2,None]*(1-sat[:,:,None]+sat[:,:,None]*pure)

result=a.copy()
# Color facade pixels without modifying their geometry, texture or sky.
for name,hue,points,center,width in zones:
    mask=Image.new('L',(W,H))
    ImageDraw.Draw(mask).polygon([(round(x*sx),round(yy*sy)) for x,yy in points],fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(1.5*sx))
    m=np.asarray(mask,dtype=np.float32)/255
    m*=smooth((y-.008)/.055)
    # Process bounding region only for color allocation.
    left,top,right,bottom=mask.getbbox()
    sl=np.s_[top:bottom,left:right]
    sat=.72-.26*smooth((y[sl]-.22)/.62)
    pure=np.array(colorsys.hsv_to_rgb(hue/360,1,1),dtype=np.float32)
    target=hsv[sl][:,:,2,None]*(1-sat[:,:,None]+sat[:,:,None]*pure)
    result[sl]=result[sl]*(1-m[sl][:,:,None])+target*m[sl][:,:,None]

# Give existing water reflections the same building palette. Nearby
# footprints mix softly, widening slightly away from the shoreline.
water_top=round(1013*sy)
xx=np.arange(W,dtype=np.float32)/sx
for row in range(water_top,H):
    depth=(row-water_top)/(H-water_top)
    total=np.zeros(W,dtype=np.float32)
    hue_total=np.zeros(W,dtype=np.float32)
    for name,hue,points,center,width in zones:
        weight=np.exp(-.5*((xx-center)/(width*(.57+.11*depth)))**2)
        total+=weight
        hue_total+=weight*hue
    hues=hue_total/np.maximum(total,1e-30)
    # All palette hues are between 174 and 218 degrees, within HSV sectors
    # 2 and 3. Vectorized conversion from hue to saturated RGB.
    sector=hues/60
    pure=np.zeros((W,3),dtype=np.float32)
    pure[:,1]=np.where(sector<3,1,4-sector)
    pure[:,2]=np.where(sector<3,sector-2,1)
    sat=.70-.24*smooth((y[row]-.22)/.62)
    target=hsv[row,:,2,None]*(1-sat[:,None]+sat[:,None]*pure)
    strength=smooth((row-water_top)/(8*sy))*smooth((y[row]-.007)/.060)*smooth(total/.12)
    result[row]=a[row]*(1-strength[:,None])+target*strength[:,None]

out=np.rint(np.clip(result,0,1)*255).astype(np.uint8)
path=root/'outputs/shanghai-tron-building-colors.png'
Image.fromarray(out).save(path,icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
saved=Image.open(path)
assert saved.size==(4704,3136) and saved.info.get('icc_profile')
assert np.array_equal(np.asarray(saved),out)
preview=saved.copy(); preview.thumbnail((1500,1000)); preview.save(root/'work/building-colors-preview.png')
# Save palette assignments and verification for an auditable color edit.
report={'size':[W,H],'profile':'sRGB','operation':'Facade masks and matching reflection footprints; color-only edits; no generation, geometry changes, water synthesis or image resampling.',
 'building_hues_degrees':{z[0]:z[1] for z in zones},
 'reflection_method':'Same building hue assignments projected beneath each building, softly blended where neighboring reflected light overlaps. Original ripples and brightness texture retained.',
 'highlight_check':'Original softened maximum RGB intensity preserved or reduced; blue facades have naturally lower luminance than equally intense cyan facades.',
 'max_channel_increase_0_255':int(np.max(out.max(axis=2).astype(int)-np.asarray(im).max(axis=2).astype(int))),
 'saved_pixel_verification':True}
(root/'outputs/building-colors-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
