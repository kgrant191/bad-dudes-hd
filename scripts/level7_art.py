"""Final factory, helicopter, moving machinery and live ending text."""
from common import *
from collections import defaultdict
from level2_art import fit_reference
from hud_art import hud_tile,FONT
from PIL import ImageDraw,ImageFont
import json


def registered_refs():
    return [(900,fit_reference('level7_factory.png',[0,407/1214,471/1214,812/1214,1010/1214,1],[0,320,368,640,800,960])),
            (3300,fit_reference('level7_dragon.png',[0,624/1214,979/1214,1],[0,520,800,960])),
            (7230,fit_reference('level7_shafts.png',[0,451/1214,519/1214,831/1214,953/1214,1],[0,392,440,712,800,960])),
            (12000,fit_reference('level7_catwalks.png',[0,72/1214,128/1214,513/1214,575/1214,887/1214,927/1214,1],[0,72,112,456,496,776,800,960])),
            (9720,fit_reference('level7_controls.png',[0,460/1214,520/1214,847/1214,972/1214,1],[0,392,440,712,800,960]))]


def painted_material(t,p,source,sprite=False):
    """Retain rare edge/door contours, with the painted material under them."""
    a=np.array(scale(tile(t,p)));ix=np.repeat(np.repeat(pixels(t),4,0),4,1)
    tex=np.array(source.resize((32,32),Image.Resampling.LANCZOS)).astype(float)
    for i in range(1,4):
        m=ix==i;a[m,:3]=np.clip(tex[m,:3]*(.32+.25*i),0,255)
    if sprite:a[ix==0]=0
    else:a[ix==0]=[0,0,0,255]
    return Image.fromarray(a)


def level7_art():
    refs=registered_refs();mapped={};positions={}
    for f,art in refs:
        groups=defaultdict(list)
        for line in (ROOT/f'metadata/level7_{f}.tiles').read_text().splitlines():
            l,x,y,t,p,h,v=map(int,line.split(','))
            if l==0 and t//256==12 and 0<=x<=248 and 0<=y<200:groups[t,p].append((x,y))
        for key,places in groups.items():
            if key in mapped:continue
            x,y=min(places,key=lambda a:(abs(a[0]-128),a[1]))
            mapped[key]=art.crop((x*4,y*4,x*4+32,y*4+32));positions[key]=(x,y)
    # The helicopter is a scrolling background, including the skids and doors.
    layout=json.loads((ROOT/'metadata/helicopter_layout.json').read_text());w,h=layout['size']
    heli=Image.open(ROOT/'art/level7_helicopter.png').convert('RGBA').resize((w*4,h*4),Image.Resampling.LANCZOS)
    groups=defaultdict(list)
    for x,y,t,p,hm,vm in layout['tiles']:groups[t,p].append((x,y))
    for key,places in groups.items():
        x,y=min(places,key=lambda a:(abs(a[0]-160),a[1]));mapped[key]=heli.crop((x*4,y*4,x*4+32,y*4+32))
    patterns={}
    for (t,p),im in mapped.items():patterns.setdefault((pixels(t).tobytes(),p),im)
    by_tile=defaultdict(list)
    for (t,p),im in mapped.items():by_tile[t].append((p,im))
    rotors=set(json.loads((ROOT/'metadata/level7_rotor_keys.json').read_text()))
    rotor_material=Image.open(ROOT/'art/level7_helicopter.png').convert('RGBA').crop((1000,18,1032,30))
    material=[];palette_states=[];out=[]
    for t,p in json.loads((ROOT/'metadata/level7_background_keys.json').read_text()):
        ix=pixels(t);im=mapped.get((t,p),patterns.get((ix.tobytes(),p)))
        if not ix.any():im=Image.new('RGBA',(32,32),(0,0,0,255))
        if im is None and by_tile[t]:
            # Factory palette fades and the original bright/dark green swap
            # preserve the same registered geometry and painted surfaces.
            sp,base=by_tile[t][0];im=base.copy()
            if p not in [0x0f0b1b2b,0x0f1b2a20,0x0f382a20,0x0f001020]:
                source=np.array(tile(t,sp))[:,:,:3].max();dest=np.array(tile(t,p))[:,:,:3].max()
                a=np.array(im);a[:,:,:3]=(a[:,:,:3]*min(1,dest/max(1,source))).astype('uint8');im=Image.fromarray(a)
            palette_states.append([t,p])
        if im is None:
            swatch=refs[0][1].crop((480,450,512,482)) if t//256==12 else heli.crop((580,180,612,212))
            im=painted_material(t,p,swatch);material.append([t,p])
        if t in rotors:im=painted_material(t,p,rotor_material)
        if 0xec0<=t<=0xecd:
            a=np.array(im);mask=np.repeat(np.repeat(ix==0,4,0),4,1);a[mask]=[0,0,0,255];im=Image.fromarray(a)
        if p==0x0f0f0f0f:im=Image.new('RGBA',(32,32),(0,0,0,255))
        out.append((t,p,im))
    (ROOT/'validation/level7_background_mapping.json').write_text(json.dumps({'reference_cells':len(mapped),'palette_states':palette_states,'painted_edge_cells':material,'unmapped':[]},indent=2)+'\n')
    return out


def level7_sprite_art():
    """Moving steel doors and rotor phases retain native per-pixel coverage."""
    art=registered_refs()[2][1];steel=art.crop((780,220,812,252))
    heli=Image.open(ROOT/'art/level7_helicopter.png').convert('RGBA');rotor=heli.crop((800,14,832,46))
    out=[]
    for t,p in json.loads((ROOT/'metadata/level7_movie_keys.json').read_text()):
        if p==0xff300010 and 0x1bc0<=t<=0x1bff:out.append((t,p,painted_material(t,p,steel,True)))
        elif t//256==0x1b and p in [0xff172737,0xff001030]:out.append((t,p,painted_material(t,p,rotor,True)))
    (ROOT/'validation/level7_machinery_mapping.json').write_text(json.dumps({'keys':[[t,p] for t,p,_ in out]},indent=2)+'\n')
    return out


def ending_glyph(char):
    im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im);font=ImageFont.truetype(FONT,106)
    bb=d.textbbox((0,0),char,font=font)
    top=88 if char in ['.',','] else 8
    d.text(((128-(bb[2]-bb[0]))/2-bb[0],top-bb[1]),char,font=font,fill=(255,221,160,255),stroke_width=2,stroke_fill=(40,25,20,255))
    return im.resize((32,32),Image.Resampling.LANCZOS)


def ending_art(headers):
    """Illustrated ending plates under the game's unchanged live text."""
    for name in ['ending_office','ending_credits']:
        Image.open(ROOT/f'art/{name}.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS).save(ROOT/f'pack/{name}.png')
    headers.extend(['<condition>ending_office,memoryCheckConstant,2C0,==,B',
                    '<condition>ending_credits,memoryCheckConstant,2C0,==,C',
                    '[ending_office]<background>ending_office.png,1,0,0,10',
                    '[ending_credits]<background>ending_credits.png,1,0,0,10'])
    blank=Image.new('RGBA',(32,32));out=[]
    for t,p in json.loads((ROOT/'metadata/level7_movie_keys.json').read_text()):
        sprite=p>>24==255;bank=t//256
        if not sprite and bank==2:
            char=chr(65+t-0x28b) if 0x28b<=t<=0x2a4 else {0x2a8:'!',0x2a9:'.',0x2aa:',',0x2ab:"'"}.get(t)
            im=ending_glyph(char) if char and p==0x0f172636 else blank
            out.append((t,p,im,'ending_office'))
        if sprite and bank in [0x1d,0x1f]:out.append((t,p,blank,'ending_office'))
        if (not sprite and bank==3) or (sprite and bank==0x1f):out.append((t,p,blank,'ending_credits'))
        if not sprite and bank==13 and p==0x0f222630:
            char=chr(65+t-0xd0b) if 0xd0b<=t<=0xd24 else {0xd29:'.',0xd2a:',',0xd2b:"'"}.get(t)
            out.append((t,p,ending_glyph(char) if char else blank,'ending_credits'))
    return out
