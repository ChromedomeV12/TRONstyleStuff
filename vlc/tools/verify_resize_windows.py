import ctypes as c
from ctypes import wintypes as w
import argparse,os,subprocess,time,sys,statistics,tempfile
from pathlib import Path

if sys.platform!='win32':
    raise SystemExit('This integration check requires Windows and VLC with Skins2.')
parser=argparse.ArgumentParser(description='Check real VLC skin resizing with Win32 mouse messages, without changing saved preferences.')
parser.add_argument('skin',nargs='?',type=Path,default=Path(__file__).resolve().parent.parent/'dist/TRON.vlt')
parser.add_argument('--vlc',type=Path,default=Path(os.environ.get('ProgramFiles','C:/Program Files'))/'VideoLAN/VLC/vlc.exe')
parser.add_argument('--media',type=Path,help='Optional video to check resizing during playback; audio is disabled.')
parser.add_argument('--benchmark',action='store_true',help='Measure a short right-edge drag instead of the full resize checks.')
args=parser.parse_args()
if args.media and not args.media.is_file():
    parser.error('The supplied video file does not exist.')
u=c.WinDLL('user32',use_last_error=True)
u.SetProcessDPIAware()
u.SendMessageW.argtypes=[w.HWND,w.UINT,w.WPARAM,w.LPARAM]
u.SendMessageW.restype=w.LPARAM
u.GetClientRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
u.GetWindowRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
def size(h):
    r=w.RECT();u.GetClientRect(h,c.byref(r));return r.right,r.bottom
resize_times=[]
def send(h,msg,x,y,flags=0):
    start=time.perf_counter()
    u.SendMessageW(h,msg,flags,((y&65535)<<16)|(x&65535))
    if msg==0x200 and flags==1:resize_times.append((time.perf_counter()-start)*1000)
def drag(h,x,y,dx,dy):
    before=size(h)
    send(h,0x200,x,y)
    send(h,0x201,x,y,1)
    for step in range(1,5):
        send(h,0x200,x+dx*step//4,y+dy*step//4,1);time.sleep(.08)
    send(h,0x202,x+dx,y+dy)
    time.sleep(.25)
    return before,size(h)
si=subprocess.STARTUPINFO();si.dwFlags=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
skin=args.skin.resolve()
test_profile=tempfile.TemporaryDirectory(prefix='vlc-tron-test-')
command=[str(args.vlc),'--no-one-instance','--ignore-config','--config='+str(Path(test_profile.name)/'vlcrc'),'--no-media-library','--intf=skins2','--skins2-last='+str(skin),'--no-qt-privacy-ask','--no-qt-updates-notif','--no-audio']
if args.media:command+=['--input-repeat=10',str(args.media.resolve())]
p=subprocess.Popen(command,startupinfo=si)
def windows():
    found=[]
    @c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
    def cb(h,l):
        pid=w.DWORD();u.GetWindowThreadProcessId(h,c.byref(pid))
        if pid.value==p.pid:
            cls=c.create_unicode_buffer(200);u.GetClassNameW(h,cls,200)
            if cls.value=='SkinWindowClass' and u.IsWindowVisible(h) and size(h)[0]>=300:found.append(h)
        return True
    u.EnumWindows(cb,0);return found
try:
    h=None
    for _ in range(150):
        candidates=windows()
        h=next((x for x in candidates if size(x)==(960,644)),None)
        if h:break
        time.sleep(.1)
    assert h,'Skin main window not found'
    time.sleep(.5)
    if args.benchmark:
        for delta in (160,-160):
            width,height=size(h)
            before,after=drag(h,width-3,height//2,delta,0)
            assert after==(before[0]+delta,before[1]),(before,after)
        print(f'Resize mouse-message processing: median {statistics.median(resize_times):.1f} ms, max {max(resize_times):.1f} ms ({len(resize_times)} moves).',flush=True)
        raise SystemExit(0)
    original=size(h)
    for _ in range(2):
        send(h,0x200,650,24);send(h,0x203,650,24);time.sleep(.4)
        if _==0:assert size(h)!=original,'Title-bar double-click did not maximize'
    assert size(h)==original,'Title-bar double-click did not restore the original size'
    print('PASS: title-bar maximize/restore round trip.',flush=True)
    def verify(window,name,minimum):
        for label,dx,dy in [('right',80,0),('bottom',0,60),('corner',80,60),('corner',-80,-60),('bottom',0,-60),('right',-80,0),('corner',-500,-500)]:
            width,height=size(window)
            x,y={'right':(width-3,height//2),'bottom':(width//2,height-3),'corner':(width-10,height-10)}[label]
            before,after=drag(window,x,y,dx,dy)
            expected=(max(minimum[0],before[0]+dx),max(minimum[1],before[1]+dy))
            assert after==expected,(name,label,before,after,expected)
            print(name,label,before,'->',after,flush=True)
    verify(h,'player',(800,470))
    # Restore the known layout before opening the matching playlist.
    width,height=size(h);drag(h,width-10,height-10,960-width,644-height)
    for msg,flags in [(0x200,0),(0x201,1),(0x202,0)]:send(h,msg,394,594,flags)
    queue=None
    for _ in range(30):
        queue=next((x for x in windows() if x!=h and size(x)==(440,480)),None)
        if queue:break
        time.sleep(.1)
    assert queue,'Playlist window did not open'
    verify(queue,'playlist',(320,280))
    print('PASS: both windows grow, shrink, and respect minimum dimensions.',flush=True)
finally:
    p.terminate();p.wait(timeout=5)
    test_profile.cleanup()
