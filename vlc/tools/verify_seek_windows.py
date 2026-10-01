"""Check the rendered fill/handle join in an isolated Windows VLC instance."""
import argparse
import ctypes as c
from ctypes import wintypes as w
import os
from pathlib import Path
import subprocess
import sys
import time
import tempfile
from PIL import Image

if sys.platform != 'win32':
    raise SystemExit('This integration check requires Windows and VLC.')
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--skin',type=Path,default=Path(__file__).resolve().parent.parent/'dist/TRON.vlt')
parser.add_argument('--vlc',type=Path,default=Path(os.environ.get('ProgramFiles','C:/Program Files'))/'VideoLAN/VLC/vlc.exe')
parser.add_argument('--media',type=Path,required=True,help='A seekable test video, ideally at least 30 seconds long.')
parser.add_argument('--captures',type=Path,help='Optional folder for rendered screenshots.')
args=parser.parse_args()
if not args.media.is_file():parser.error('Test video does not exist.')
if args.captures:args.captures.mkdir(parents=True,exist_ok=True)
u=c.WinDLL('user32');g=c.WinDLL('gdi32')
u.SetProcessDPIAware()
u.SendMessageW.argtypes=[w.HWND,w.UINT,w.WPARAM,w.LPARAM];u.SendMessageW.restype=w.LPARAM
u.GetWindowDC.argtypes=[w.HWND];u.GetWindowDC.restype=w.HDC
u.GetClientRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
u.PrintWindow.argtypes=[w.HWND,w.HDC,w.UINT]
u.ReleaseDC.argtypes=[w.HWND,w.HDC]
g.CreateCompatibleDC.argtypes=[w.HDC];g.CreateCompatibleDC.restype=w.HDC
g.CreateCompatibleBitmap.argtypes=[w.HDC,c.c_int,c.c_int];g.CreateCompatibleBitmap.restype=w.HBITMAP
g.SelectObject.argtypes=[w.HDC,w.HGDIOBJ];g.SelectObject.restype=w.HGDIOBJ
g.GetDIBits.argtypes=[w.HDC,w.HBITMAP,w.UINT,w.UINT,c.c_void_p,c.c_void_p,w.UINT]
g.DeleteObject.argtypes=[w.HGDIOBJ];g.DeleteDC.argtypes=[w.HDC]
class BI(c.Structure):
    _fields_=[('size',w.DWORD),('width',w.LONG),('height',w.LONG),('planes',w.WORD),('bits',w.WORD),('compression',w.DWORD),('imageSize',w.DWORD),('xp',w.LONG),('yp',w.LONG),('used',w.DWORD),('important',w.DWORD)]
def size(h):
    r=w.RECT();u.GetClientRect(h,c.byref(r));return r.right,r.bottom
def send(h,msg,x,y,flags=0):u.SendMessageW(h,msg,flags,((y&65535)<<16)|(x&65535))
def capture(h):
    width,height=size(h)
    dc=u.GetWindowDC(h);mem=g.CreateCompatibleDC(dc);bmp=g.CreateCompatibleBitmap(dc,width,height);old=g.SelectObject(mem,bmp)
    try:
        assert u.PrintWindow(h,mem,2),'PrintWindow failed'
        bi=BI();bi.size=c.sizeof(BI);bi.width=width;bi.height=-height;bi.planes=1;bi.bits=32
        buf=c.create_string_buffer(width*height*4)
        g.SelectObject(mem,old)
        assert g.GetDIBits(mem,bmp,0,height,buf,c.byref(bi),0),'GetDIBits failed'
        return Image.frombytes('RGB',(width,height),buf.raw,'raw','BGRX')
    finally:
        g.DeleteObject(bmp);g.DeleteDC(mem);u.ReleaseDC(h,dc)
def blue(pixel):
    r,g,b=pixel
    return b>180 and g>90 and b-r>55 and b-g>15
si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
test_profile=tempfile.TemporaryDirectory(prefix='vlc-tron-test-')
p=subprocess.Popen([str(args.vlc),'--no-one-instance','--ignore-config','--config='+str(Path(test_profile.name)/'vlcrc'),'--no-media-library',
                    '--intf=skins2','--skins2-last='+str(args.skin.resolve()),'--no-qt-privacy-ask',
                    '--no-qt-updates-notif','--no-audio',str(args.media.resolve())],startupinfo=si)
try:
    found=[]
    @c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
    def cb(h,param):
        pid=w.DWORD();u.GetWindowThreadProcessId(h,c.byref(pid))
        cls=c.create_unicode_buffer(200);u.GetClassNameW(h,cls,200)
        if pid.value==p.pid and cls.value=='SkinWindowClass' and size(h)==(960,644):found.append(h)
        return True
    for _ in range(150):
        u.EnumWindows(cb,0)
        if found:break
        time.sleep(.1)
    assert found,'Player window not found'
    h=found[0]
    # A window can appear before the input has loaded and becomes seekable.
    for _ in range(100):
        im=capture(h)
        if any(blue(im.getpixel((x,546))) for x in range(25,935)):break
        time.sleep(.1)
    else:raise AssertionError('Media did not become seekable')
    send(h,0x200,102,594);send(h,0x201,102,594,1);send(h,0x202,102,594)
    time.sleep(.2)
    gaps=[]
    for target in (960,1440,1920):
        width,height=size(h)
        if target!=width:
            x,y=width-3,height//2
            send(h,0x200,x,y);send(h,0x201,x,y,1)
            send(h,0x200,x+target-width,y,1);time.sleep(.3)
            send(h,0x202,x+target-width,y);time.sleep(.2)
        width,height=size(h);assert width==target,(width,target)
        for fraction,offset in ((.129,-10),(.509,0),(.899,10)):
            y=height-95;x=35+round((width-70)*fraction)
            send(h,0x200,x,y+offset);send(h,0x201,x,y+offset,1);send(h,0x202,x,y+offset)
            send(h,0x200,650,24);time.sleep(.25)
            im=capture(h)
            if args.captures:im.save(args.captures/f'seek-{width}-{fraction:.3f}.png')
            # Only the circular handle has blue pixels three rows above the line.
            knob=[xx for xx in range(25,width-25) if blue(im.getpixel((xx,y-3)))]
            assert knob,'Seek handle was not rendered'
            center=(min(knob)+max(knob))/2
            assert abs(center-x)<width*.012,('Click/seek did not reach requested position',center,x)
            line_start=next((xx for xx in range(30,55) if blue(im.getpixel((xx,y)))),None)
            assert line_start is not None,'Filled track was not rendered'
            line_end=line_start
            for xx in range(line_start,int(center)+1):
                if blue(im.getpixel((xx,y))):line_end=xx
                else:break
            gap=max(0,center-5-line_end)
            gaps.append(gap)
            print(f'{width}px at {fraction:.1%}: visible fill/handle gap {gap:.1f}px',flush=True)
    assert max(gaps)<=2,f'Visible fill/handle gap: {max(gaps):.1f}px'
    print('PASS: fill stays joined to the handle across seek positions and window widths.',flush=True)
finally:
    p.terminate();p.wait(timeout=5)
    test_profile.cleanup()
