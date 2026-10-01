"""Generate shader-free projectM presets for VLC's legacy projectM plugin."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'visualizations'
OUT.mkdir(exist_ok=True)

BASE = '''[preset00]
fRating=3.000000
fGammaAdj=1.000000
fDecay=0.000000
fVideoEchoAlpha=0.000000
fVideoEchoZoom=1.000000
nVideoEchoOrientation=0
nWaveMode=0
bAdditiveWaves=0
bWaveDots=0
bWaveThick=1
bModWaveAlphaByVolume=0
bMaximizeWaveColor=0
bTexWrap=0
bDarkenCenter=0
bRedBlueStereo=0
bBrighten=0
bDarken=0
bSolarize=0
bInvert=0
fWaveAlpha=0.000000
fWaveScale=4.000000
fWaveSmoothing=0.750000
fWarpAnimSpeed=0.000000
fWarpScale=1.000000
fZoomExponent=1.000000
zoom=1.000000
rot=0.000000
cx=0.500000
cy=0.500000
dx=0.000000
dy=0.000000
warp=0.000000
sx=1.000000
sy=1.000000
ob_size=0.000000
ob_a=0.000000
ib_size=0.000000
ib_a=0.000000
mv_a=0.000000
shapecode_0_enabled=1
shapecode_0_sides=4
shapecode_0_additive=1
shapecode_0_thickOutline=0
shapecode_0_textured=0
shapecode_0_x=0.500000
shapecode_0_y=0.500000
shapecode_0_rad=100.000000
shapecode_0_ang=0.000000
shapecode_0_r=0.019608
shapecode_0_g=0.054902
shapecode_0_b=0.078431
shapecode_0_a=1.000000
shapecode_0_r2=0.019608
shapecode_0_g2=0.054902
shapecode_0_b2=0.078431
shapecode_0_a2=1.000000
shapecode_0_border_a=0.000000
'''

# With zero feedback, the additive background paints exact #050e14 onto black.
# During preset transitions projectM scales both shapes' alpha: adding their
# contributions preserves the color, whereas normal alpha blending darkens it.
# The oversized quad also covers extreme aspect ratios after native resizing.
# Native preset equations smooth audio energy between incoming PCM blocks.
# Drawing raw PCM directly made the image hold still between audio updates.
# Keep the curve bounded at 256 points; no textures, shaders or companion app.
# Global fields must precede shape fields in the legacy preset parser.
SMOOTH = '''per_frame_init_1=q1=0;q2=0;
per_frame_1=q1=q1*0.85+min(2,max(0,bass))*0.15;
per_frame_2=q2=q2*0.85+min(2,max(0,treb))*0.15;
per_frame_3=q3=time;
'''
CURVE = '''wavecode_0_enabled=1
wavecode_0_samples=256
wavecode_0_bSpectrum=0
wavecode_0_bUseDots=0
wavecode_0_bDrawThick=1
wavecode_0_bAdditive=0
wavecode_0_scaling=1
wavecode_0_smoothing=0
wavecode_0_r={r:.6f}
wavecode_0_g={g:.6f}
wavecode_0_b={b:.6f}
wavecode_0_a=1
'''
def preset(color, equations):
    base = BASE.replace('shapecode_0_enabled=1',SMOOTH+'shapecode_0_enabled=1')
    return base + CURVE.format(**dict(zip(('r','g','b'),(c/255 for c in color)))) + equations

waves = preset((111,195,223), '''wave_0_per_point1=x=sample;
wave_0_per_point2=y=0.5+(0.012+q1*0.035)*sin(sample*18.849556-q3*2.4)+(0.004+q2*0.012)*sin(sample*37.699112+q3*1.7);
''')
# Inline the radius expression: this legacy renderer held intermediate t-variable
# point expressions still after startup in the sustained-animation check.
orbit = preset((120,221,255), '''wave_0_per_point1=x=0.5+(0.20+q1*0.035+(0.007+q2*0.009)*sin(sample*31.415925-q3*1.8))*0.48*cos(sample*6.283185);
wave_0_per_point2=y=0.5+(0.20+q1*0.035+(0.007+q2*0.009)*sin(sample*31.415925-q3*1.8))*sin(sample*6.283185);
''')
for name,data in [('Waves',waves),('Orbit',orbit)]:
    (OUT/f'TRON - {name}.milk').write_text(data,encoding='ascii')
    folder=OUT/name.lower()
    folder.mkdir(exist_ok=True)
    (folder/f'TRON - {name}.milk').write_text(data,encoding='ascii')
print('Built TRON Waves and Orbit projectM presets.')
