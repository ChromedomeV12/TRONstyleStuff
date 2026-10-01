from pathlib import Path
import argparse, os, tarfile, zipfile
from PIL import Image, ImageDraw, ImageFont
from lxml import etree as E

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
SKIN = ROOT / 'skin'
SKIN.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
C = dict(bg='#050E14', panel='#08141C', raised='#102936', line='#163645', fg='#C4D4D8', muted='#829FAA', blue='#6FC3DF', orange='#FF8C1A', cyan='#78DDFF', red='#FF6B4A', edge='#2EAAC9', inner='#174653')
S = 3
parser = argparse.ArgumentParser(description='Generate the TRON VLC skin and distribution bundle.')
parser.add_argument('--font', type=Path, help='TTF font for rasterized menu labels; Windows defaults to Segoe UI.')
parser.add_argument('--vlc-dir', type=Path, help='VLC install/share directory for optional skin.dtd validation.')
args = parser.parse_args()
font_candidates = [args.font] if args.font else [
    Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/segoeui.ttf',
    Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
    Path('/usr/share/fonts/TTF/DejaVuSans.ttf'),
]
FONT_PATH = next((p for p in font_candidates if p.is_file()), None)
if FONT_PATH is None:
    parser.error('No menu-label font found. Pass --font /path/to/font.ttf.')
assets = {}
def canvas(w,h,bg=(0,0,0,0)):
    im=Image.new('RGBA',(w*S,h*S),bg); return im,ImageDraw.Draw(im)
def rect(d,box,fill,r=0,outline=None,width=1):
    d.rounded_rectangle(tuple(int(v*S) for v in box),radius=r*S,fill=fill,outline=outline,width=width*S)
def line(d,pts,fill,width=2):
    d.line([(int(x*S),int(y*S)) for x,y in pts], fill=fill,width=width*S,joint='curve')
def polygon(d,pts,fill): d.polygon([(int(x*S),int(y*S)) for x,y in pts],fill=fill)
def txt(d,xy,text,size,color,anchor=None):
    f=ImageFont.truetype(str(FONT_PATH),size*S)
    d.text((xy[0]*S,xy[1]*S),text,font=f,fill=color,anchor=anchor)
def save(name,im):
    im=im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS)
    im.save(SKIN/(name+'.png')); assets[name]=im; return name
# VLC mosaics Images by default, issuing a native draw for every tile.
# Large solid tiles avoid hundreds of thousands of 2x2 blits per resize.
for name,col,w,h in [('bg',C['bg'],1024,1024),('panel',C['panel'],1024,144),
                     ('line',C['line'],2048,2),('edge',C['edge'],2048,2),
                     ('inner',C['inner'],2048,2),('rail',C['edge'],2,2048),
                     ('rail_inner',C['inner'],2,2048),('raised',C['raised'],40,40)]:
    im,d=canvas(w,h,col); save(name,im)
im,d=canvas(155,48,C['panel'])
save('brand',im)
im,d=canvas(952,452,C['bg'])
# Plain idle background, hidden automatically during video playback.
save('idle',im)

def icon(name,state):
    im,d=canvas(40,40,C['panel'])
    active=name.endswith('_on'); kind=name.removesuffix('_on')
    primary=kind in ('play','pause')
    fill=C['blue'] if primary else (C['raised'] if state!='up' or active else C['panel'])
    if state=='down': fill=C['orange'] if primary else C['line']
    if state=='over' and primary: fill=C['cyan']
    rect(d,(2,2,38,38),fill,7, C['cyan'] if primary or state=='over' else (C['orange'] if active else C['inner']),1)
    col=C['bg'] if primary else (C['orange'] if active else (C['fg'] if state!='up' else C['muted']))
    if kind=='play': polygon(d,[(16,12),(16,28),(28,20)],col)
    elif kind=='pause':
        rect(d,(14,12,18,28),col,1); rect(d,(23,12,27,28),col,1)
    elif kind in ('previous','next'):
        if kind=='previous': polygon(d,[(26,12),(26,28),(15,20)],col); line(d,[(12,12),(12,28)],col)
        else: polygon(d,[(14,12),(14,28),(25,20)],col); line(d,[(28,12),(28,28)],col)
    elif kind=='stop': rect(d,(13,13,27,27),col,2)
    elif kind=='open':
        line(d,[(10,27),(10,13),(18,13),(21,16),(29,16),(29,19)],col)
        polygon(d,[(10,27),(14,19),(32,19),(28,27)],col)
    elif kind=='playlist':
        for y in (13,20,27):
            rect(d,(10,y-1,12,y+1),col); line(d,[(16,y),(30,y)],col)
    elif kind in ('volume','mute'):
        polygon(d,[(10,17),(15,17),(21,12),(21,28),(15,23),(10,23)],col)
        if kind=='mute':
            line(d,[(26,16),(32,24)],C['red']); line(d,[(32,16),(26,24)],C['red'])
        else:
            d.arc((18*S,11*S,31*S,29*S),-65,65,fill=col,width=2*S)
    elif kind=='fullscreen':
        for pts in [[(11,17),(11,11),(17,11)],[(23,11),(29,11),(29,17)],[(11,23),(11,29),(17,29)],[(23,29),(29,29),(29,23)]]: line(d,pts,col)
    elif kind=='shuffle':
        line(d,[(10,13),(14,13),(26,27),(30,27)],col)
        line(d,[(10,27),(14,27),(26,13),(30,13)],col)
        line(d,[(27,10),(30,13),(27,16)],col); line(d,[(27,24),(30,27),(27,30)],col)
    elif kind=='repeat':
        line(d,[(12,21),(12,14),(29,14),(26,11)],col)
        line(d,[(28,19),(28,26),(11,26),(14,29)],col)
    elif kind=='close':
        col=C['red'] if state!='up' else col
        line(d,[(14,14),(26,26)],col); line(d,[(26,14),(14,26)],col)
    elif kind=='minimize': line(d,[(13,24),(27,24)],col)
    elif kind=='maximize': rect(d,(13,13,27,27),None,1,col)
    elif kind=='restore':
        line(d,[(17,13),(28,13),(28,24),(25,24)],col)
        rect(d,(12,17,24,29),None,1,col)
    elif kind=='menu':
        for x in (13,20,27): d.ellipse(((x-1)*S,19*S,(x+1)*S,21*S),fill=col)
    elif kind=='add':
        line(d,[(12,20),(28,20)],col);line(d,[(20,12),(20,28)],col)
    elif kind=='remove': line(d,[(12,20),(28,20)],col)
    elif kind=='save':
        rect(d,(12,11,28,29),None,2,col); rect(d,(16,11,24,17),col); rect(d,(16,23,24,29),None,0,col)
    return save(name+'_'+state,im)

for name in ['play','pause','previous','next','stop','open','playlist','playlist_on','volume','mute','fullscreen','shuffle','shuffle_on','repeat','repeat_on','close','minimize','maximize','restore','menu','add','remove','save']:
    for state in ('up','over','down'): icon(name,state)
MENUS = [('Media',62,'media_menu.show()'), ('Playback',84,'playback_menu.show()'),
         ('Audio',60,'audio_menu.show()'), ('Video',60,'video_menu.show()'),
         ('Subtitles',78,'dialogs.popup()'), ('Tools',58,'tools_menu.show()'),
         ('View',56,'view_menu.show()'), ('Help',56,'help_window.show()')]
for label,w,action in MENUS:
    for state in ('up','over','down'):
        im,d=canvas(w,40,C['panel'])
        if state!='up': rect(d,(2,3,w-2,37),C['raised'] if state=='over' else C['line'],5)
        txt(d,(w/2,20),label,13,C['cyan'] if state=='over' else C['fg'],'mm')
        save('nav_'+label.lower()+'_'+state,im)
for name,col in [('knob',C['blue']),('knob_over',C['cyan']),('vol_knob',C['blue'])]:
    im,d=canvas(14,14); d.ellipse((2*S,2*S,12*S,12*S),fill=col);save(name,im)
for name,label in [('eq_disabled','Enable'),('eq_enabled','Disable')]:
    for state in ('up','over','down'):
        im,d=canvas(104,32,C['panel'])
        rect(d,(1,1,103,31),C['raised'] if state=='up' else C['line'],5)
        txt(d,(52,16),label,13,C['fg'],'mm')
        save(name+'_'+state,im)
im,d=canvas(12,34);rect(d,(3,0,9,33),C['muted'],3);save('scroll',im)
im,d=canvas(28,28,C['panel'])
for n in (10,16,22): line(d,[(n,24),(24,n)],C['blue'],1)
line(d,[(26,0),(26,26),(0,26)],C['edge'],1)
line(d,[(22,0),(22,22),(0,22)],C['inner'],1)
save('resize',im)
# Use dense, three-pixel-high track frames. The previous 101-frame atlas
# rounded progress down to whole percentages, visibly trailing the handle.
# A separate interactive slider keeps a generous hit area and fixed-size knob
# without stretching tall, mostly transparent atlases on every window resize.
SEEK_FRAMES = 2001
VOLUME_FRAMES = 257
for name,width,frames,col in [('seek',891,SEEK_FRAMES,C['blue']),
                              ('volume_track',103,VOLUME_FRAMES,C['blue'])]:
    im=Image.new('RGBA',(width,3*frames),C['panel'])
    d=ImageDraw.Draw(im)
    for i in range(frames):
        y=3*i+1
        d.line((0,y,width-1,y),fill=C['line'],width=1)
        if i:
            endpoint=round((width-1)*i/(frames-1))
            d.line((0,y,endpoint,y),fill=col,width=1)
    im.save(SKIN/(name+'.png'));assets[name]=im
im,d=canvas(1,1)
save('invisible',im)

theme=E.Element('Theme',version='2.0',magnet='12')
def el(parent,tag,**kw): return E.SubElement(parent,tag,**{k:str(v) for k,v in kw.items()})
el(theme,'ThemeInfo',name='TRON',author='Custom skin for VLC')
for name in assets: el(theme,'Bitmap',id=name,file=name+'.png',alphacolor='#ff00ff')
def popup(name,items):
    menu=el(theme,'PopupMenu',id=name)
    for item in items:
        if item is None: el(menu,'MenuSeparator')
        else: el(menu,'MenuItem',label=item[0],action=item[1])
popup('media_menu',[
    ('Open File...','dialogs.fileSimple()'), ('Open Multiple Files...','dialogs.file()'),
    ('Open Folder...','dialogs.directory()'), ('Open Disc...','dialogs.disc()'),
    ('Open Network Stream...','dialogs.net()'), None,
    ('Save Playlist...','playlist.save()'), None, ('Quit','vlc.quit()')])
popup('playback_menu',[
    ('Play','vlc.play()'), ('Pause','vlc.pause()'), ('Stop','vlc.stop()'), None,
    ('Previous','playlist.previous()'), ('Next','playlist.next()'), None,
    ('Faster','vlc.faster()'), ('Slower','vlc.slower()'), ('Next Frame','vlc.nextFrame()'),
    None, ('Navigation and Playback Options...','dialogs.miscPopup()')])
popup('audio_menu',[
    ('Equalizer / Bass Boost...','eq.show()'),
    ('Audio Options...','dialogs.audioPopup()'), None,
    ('Mute / Unmute','vlc.mute()'), ('Increase Volume','vlc.volumeUp()'),
    ('Decrease Volume','vlc.volumeDown()')])
popup('video_menu',[
    ('Fullscreen','vlc.fullscreen()'), ('Always on Top','vlc.onTop()'),
    ('Take Snapshot','vlc.snapshot()'), None,
    ('Video Settings...','dialogs.videoPopup()')])
popup('tools_menu',[
    ('Equalizer...','eq.show()'),
    ('Media Information...','dialogs.fileInfo()'), ('Messages...','dialogs.messages()'),
    None, ('Preferences...','dialogs.prefs()'), ('Change Skin...','dialogs.changeSkin()')])
popup('view_menu',[
    ('Show Playlist','queue.show()'), ('Hide Playlist','queue.hide()'), None,
    ('Maximize','main.maximize()'), ('Restore','main.unmaximize()'), None,
    ('All VLC Options...','dialogs.popup()')])
def image(parent,name,x,y,w=None,h=None,lt='lefttop',rb=None,**kw):
    args=dict(image=name,x=x,y=y,lefttop=lt,rightbottom=rb or lt,**kw)
    if w is not None: args['width']=w
    if h is not None: args['height']=h
    return el(parent,'Image',**args)
def text(parent,value,x,y,w,col='fg',lt='lefttop',rb=None,**kw):
    return el(parent,'Text',text=value,x=x,y=y,width=w,font='defaultfont',color=C[col],lefttop=lt,rightbottom=rb or lt,focus='false',**kw)
def button(parent,name,x,y,action,tip,lt='lefttop',**kw):
    return el(parent,'Button',x=x,y=y,up=name+'_up',over=name+'_over',down=name+'_down',action=action,tooltiptext=tip,lefttop=lt,rightbottom=lt,**kw)
def check(parent,a,b,x,y,state,act1,act2,tip1,tip2,lt='lefttop'):
    return el(parent,'Checkbox',x=x,y=y,state=state,up1=a+'_up',over1=a+'_over',down1=a+'_down',up2=b+'_up',over2=b+'_over',down2=b+'_down',action1=act1,action2=act2,tooltiptext1=tip1,tooltiptext2=tip2,lefttop=lt,rightbottom=lt)
def resize_handles(parent,width,height):
    # Skins2 exposes east, south, and southeast resize actions. Keep these
    # opaque hit areas outside native video controls, which receive mouse
    # input before skin controls. Add last so other skin controls cannot mask them.
    image(parent,'panel',width-8,48,8,height-76,lt='righttop',rb='rightbottom',
          action='resizeE',help='Drag right edge to resize width')
    image(parent,'panel',0,height-8,width-28,8,lt='leftbottom',rb='rightbottom',
          action='resizeS',help='Drag bottom edge to resize height')
    image(parent,'resize',width-28,height-28,lt='rightbottom',
          action='resizeSE',help='Drag corner to resize width and height')
def shell_frame(parent,width,height,resizable=False):
    # Long strips retain the large-tile resize fix. Edge strips also preserve
    # the existing east/south hit targets instead of covering them with dead areas.
    for inset,horizontal,vertical in ((1,'edge','rail'),(5,'inner','rail_inner')):
        image(parent,horizontal,inset,inset,width-2*inset,1,rb='righttop',action='move')
        image(parent,horizontal,inset,height-inset-1,width-inset-28 if resizable else width-2*inset,1,
              lt='leftbottom',rb='rightbottom',action='resizeS' if resizable else 'move')
        image(parent,vertical,inset,inset,1,height-2*inset,rb='leftbottom',action='move')
        image(parent,vertical,width-inset-1,inset,1,height-inset-28 if resizable else height-2*inset,
              lt='righttop',rb='rightbottom',action='resizeE' if resizable else 'move')
    if height>144:
        image(parent,'edge',8,47,width-16,1,rb='righttop')

def progress_slider(parent,value,x,y,length,track,frames,knob,tooltip,
                    lt='leftbottom',rb='rightbottom',visible='true'):
    shared=dict(value=value,lefttop=lt,rightbottom=rb,visible=visible)
    # Both curves have the same width (length + 1), so VLC applies the same
    # horizontal resize factor to the fill and the handle. Track y=1 and
    # handle y=0 keep both centers at the supplied absolute y coordinate.
    background=el(parent,'Slider',x=x,y=y-1,points=f'(0,1),({length},1)',
                  up='invisible',**shared)
    el(background,'SliderBackground',image=track,nbvert=frames)
    el(parent,'Slider',x=x,y=y,points=f'(0,0),({length},0)',up=knob,
       over='knob_over',down='knob_over',thickness=18,
       tooltiptext=tooltip,**shared)
def controls(p,y):
    image(p,'panel',0,y,960,144,lt='leftbottom',rb='rightbottom',action='move')
    image(p,'edge',8,y,944,1,lt='leftbottom',rb='rightbottom')
    image(p,'inner',8,y+4,944,1,lt='leftbottom',rb='rightbottom')
    text(p,'$T',28,y+16,100,'muted','leftbottom')
    text(p,'$D',820,y+16,112,'muted','rightbottom',alignment='right')
    progress_slider(p,'time',35,y+49,890,'seek',SEEK_FRAMES,'knob',
                    'Seek: $T / $D',visible='vlc.isSeekable')
    image(p,'line',35,y+48,890,2,lt='leftbottom',rb='rightbottom',visible='not vlc.isSeekable')
    cy=y+74
    button(p,'open',22,cy,'dialogs.fileSimple()','Open media','leftbottom')
    check(p,'play','pause',82,cy,'vlc.isPlaying','vlc.play()','vlc.pause()','Play','Pause','leftbottom')
    button(p,'previous',134,cy,'playlist.previous()','Previous','leftbottom')
    button(p,'next',178,cy,'playlist.next()','Next','leftbottom')
    button(p,'stop',222,cy,'vlc.stop()','Stop','leftbottom')
    check(p,'shuffle','shuffle_on',286,cy,'playlist.isRandom','playlist.setRandom(true)','playlist.setRandom(false)','Enable shuffle','Disable shuffle','leftbottom')
    check(p,'repeat','repeat_on',330,cy,'playlist.isLoop','playlist.setLoop(true)','playlist.setLoop(false)','Loop playlist','Disable loop','leftbottom')
    check(p,'playlist','playlist_on',374,cy,'queue.isVisible','queue.show()','queue.hide()','Show playlist','Hide playlist','leftbottom')
    check(p,'volume','mute',694,cy,'vlc.isMute','vlc.mute()','vlc.mute()','Mute','Unmute','rightbottom')
    progress_slider(p,'volume',749,cy+20,102,'volume_track',VOLUME_FRAMES,
                    'vol_knob','Volume: $V%',lt='rightbottom')
    button(p,'fullscreen',884,cy,'vlc.fullscreen()','Fullscreen (F / Esc)','rightbottom')

win=el(theme,'Window',id='main',x=160,y=100,dragdrop='true',playondrop='true')
layout=el(win,'Layout',id='mainLayout',width=960,height=644,minwidth=800,minheight=470,maxwidth=7680,maxheight=4320)
image(layout,'bg',0,0,960,644,rb='rightbottom')
# The opaque background already supplies the plain idle video area.
# Keep the native video host available for projectM's direct OpenGL surface,
# which does not set vlc.hasVout like a decoded video does.
el(layout,'Video',x=8,y=48,width=944,height=452,rightbottom='rightbottom',autoresize='false',visible='not vlc.isStopped')
image(layout,'panel',0,0,960,48,rb='righttop',action='move',action2='main.maximize()',visible='not main.isMaximized')
image(layout,'panel',0,0,960,48,rb='righttop',action='move',action2='main.unmaximize()',visible='main.isMaximized')
image(layout,'brand',0,0)
x=12
for label,w,action in MENUS:
    tip='VLC menu > Subtitle (load a video first)' if label=='Subtitles' else label
    button(layout,'nav_'+label.lower(),x,4,action,tip)
    x+=w
button(layout,'menu',792,4,'dialogs.popup()','VLC menu','righttop')
button(layout,'minimize',834,4,'vlc.minimize()','Minimize','righttop')
check(layout,'maximize','restore',876,4,'main.isMaximized','main.maximize()','main.unmaximize()','Maximize','Restore','righttop')
button(layout,'close',918,4,'vlc.quit()','Close','righttop')
controls(layout,500)
resize_handles(layout,960,644)
shell_frame(layout,960,644,True)

win=el(theme,'Window',id='queue',x=1135,y=100,visible='false')
p=el(win,'Layout',id='queueLayout',width=440,height=480,minwidth=320,minheight=280,maxwidth=1600,maxheight=2000)
image(p,'bg',0,0,440,480,rb='rightbottom')
image(p,'panel',0,0,440,48,rb='righttop',action='move')
text(p,'PLAYLIST',20,17,250,'cyan')
button(p,'close',396,4,'queue.hide()','Hide playlist','righttop')
tree=el(p,'Playtree',id='tracks',x=16,y=64,width=386,height=340,font='defaultfont',fgcolor=C['fg'],playcolor=C['blue'],bgcolor1=C['bg'],bgcolor2=C['bg'],selcolor=C['raised'],flat='true',rightbottom='rightbottom')
el(tree,'Slider',x=407,y=64,points='(0,322),(0,0)',up='scroll',lefttop='righttop',rightbottom='rightbottom')
image(p,'panel',0,420,440,60,lt='leftbottom',rb='rightbottom',action='move')
button(p,'add',16,430,'playlist.add()','Add media','leftbottom')
button(p,'remove',60,430,'playlist.del()','Remove selected','leftbottom')
button(p,'save',104,430,'playlist.save()','Save playlist','leftbottom')
text(p,'Double-click to play',164,444,150,'muted','leftbottom')
resize_handles(p,440,480)
shell_frame(p,440,480,True)

win=el(theme,'Window',id='fullscreenController',position='South',ymargin=24,visible='false')
p=el(win,'Layout',id='fullscreenLayout',width=960,height=144)
controls(p,0)
shell_frame(p,960,144)

win=el(theme,'Window',id='eq',x=260,y=180,visible='false')
p=el(win,'Layout',id='eqLayout',width=640,height=324)
image(p,'bg',0,0,640,324)
image(p,'panel',0,0,640,48,action='move')
text(p,'EQUALIZER',20,17,170,'fg')
text(p,'On',200,17,80,'blue',visible='equalizer.isEnabled')
text(p,'Off',200,17,80,'muted',visible='not equalizer.isEnabled')
check(p,'eq_disabled','eq_enabled',476,8,'equalizer.isEnabled','equalizer.enable()','equalizer.disable()','Enable equalizer','Disable equalizer')
button(p,'close',596,4,'eq.hide()','Close equalizer')
for label,y in [('+20',91),('0 dB',161),('-20',231)]:text(p,label,12,y,42,'muted')
for i,label in enumerate(['Preamp','60','170','310','600','1k','3k','6k','12k','14k','16k']):
    x=74 if i==0 else 142+(i-1)*47
    image(p,'rail_inner',x,94,2,140)
    image(p,'line',x-5,164,12,2)
    value='equalizer.preamp' if i==0 else f'equalizer.band({i-1})'
    el(p,'Slider',x=x,y=94,points='(0,140),(0,0)',up='vol_knob' if i==0 else 'knob',over='knob_over',value=value,thickness=14,tooltiptext=label+' (-20 to +20 dB)')
    text(p,label,x-24,250,48,'muted',alignment='center')
text(p,'Bass: raise 60 / 170 Hz. Lower Preamp if the sound distorts.',24,292,590,'muted')

shell_frame(p,640,324)

win=el(theme,'Window',id='help_window',x=260,y=180,visible='false')
p=el(win,'Layout',id='helpLayout',width=440,height=320)
image(p,'bg',0,0,440,320)
image(p,'panel',0,0,440,48,action='move')
text(p,'KEYBOARD SHORTCUTS',20,17,320,'fg')
button(p,'close',396,4,'help_window.hide()','Close help')
for i,(key,description) in enumerate([
    ('Space','Play / pause'), ('F / Esc','Enter / leave fullscreen'),
    ('Ctrl + O','Open a media file'), ('Ctrl + P','Preferences'),
    ('M','Mute / unmute'), ('I / middle click','Fullscreen controller'),
    ('Right-click','All VLC options')]):
    text(p,key,24,72+i*30,142,'blue')
    text(p,description,174,72+i*30,248,'fg')

shell_frame(p,440,320)

xml=E.tostring(theme,pretty_print=True,encoding='UTF-8',xml_declaration=True,doctype='<!DOCTYPE Theme PUBLIC "-//VideoLAN//DTD VLC Skins V2.0//EN" "skin.dtd">')
(SKIN/'theme.xml').write_bytes(xml)
vlc_dirs = ([args.vlc_dir] if args.vlc_dir else [
    Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'VideoLAN/VLC',
    Path(os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)')) / 'VideoLAN/VLC',
    Path('/usr/share/vlc'), Path('/usr/local/share/vlc'),
])
dtd_path = next((base/sub for base in vlc_dirs for sub in ('skins/skin.dtd','skins2/skin.dtd','skin.dtd')
                 if (base/sub).is_file()), None)
if dtd_path:
    dtd=E.DTD(str(dtd_path))
    assert dtd.validate(theme),str(dtd.error_log)
    print('Validated against VLC DTD:', dtd_path)
else:
    print('VLC skin.dtd unavailable; DTD validation skipped. Use --vlc-dir to supply it.')
ids={e.get('id') for e in theme.iter() if e.get('id')}
for e in theme.iter():
    for key in ('image','up','over','down','up1','up2','over1','over2','down1','down2'):
        if e.get(key): assert e.get(key) in ids,(e.tag,key,e.get(key))
for path in SKIN.glob('*.png'):
    with Image.open(path) as im: im.verify()
with tarfile.open(OUT/'TRON.vlt','w:gz') as archive:
    for path in sorted([SKIN/'theme.xml'] + [SKIN/(name+'.png') for name in assets]):
        archive.add(path,arcname=path.name)
print('All bitmap references and PNG files valid.')
print(OUT/'TRON.vlt')

with zipfile.ZipFile(OUT/'TRON-VLC.zip','w',zipfile.ZIP_DEFLATED) as bundle:
    for filename in ('TRON.vlt','Try-TRON.cmd','Try-TRON-Music.cmd','README.txt'):
        bundle.write(OUT/filename,filename)
    bundle.write(ROOT/'docs/preview.png','TRON-Preview.png')
    for path in sorted((ROOT/'visualizations').rglob('*.milk')):
        bundle.write(path,path.relative_to(ROOT).as_posix())
    for filename in ('audio.md','equalizer.png','visualization-waves.png','visualization-orbit.png'):
        bundle.write(ROOT/'docs'/filename,'docs/'+filename)
    bundle.write(ROOT/'tools/make_timed_playlist.py','tools/make_timed_playlist.py')
print(OUT/'TRON-VLC.zip')
