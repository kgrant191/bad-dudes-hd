"""Painted Level 2 tile references, scoped to the live second-stage scene."""
from common import *
from collections import defaultdict
import json


def fit_reference(name, source_y, target_y):
    source=Image.open(ROOT/'art'/name).convert('RGBA')
    # Register the painted horizontal bands to their original game heights.
    out=Image.new('RGBA',(1024,960))
    for sy0,sy1,ty0,ty1 in zip(source_y,source_y[1:],target_y,target_y[1:]):
        crop=source.crop((0,round(sy0*source.height),source.width,round(sy1*source.height)))
        out.paste(crop.resize((1024,ty1-ty0),Image.Resampling.LANCZOS),(0,ty0))
    return out


def level2_art():
    Image.open(ROOT/'art/level2_sky.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS).save(ROOT/'pack/level2_sky.png')
    refs=[(600,fit_reference('level2_truck.png',
        [0,451/1214,519/1214,617/1214,688/1214,773/1214,940/1214,978/1214,1],
        [0,388,440,512,576,640,768,800,960])),
        (7500,fit_reference('level2_cab.png',
        [0,432/1214,607/1214,920/1214,958/1214,1],
        [0,388,512,768,800,960]))]
    out={}
    for f,art in refs:
        groups=defaultdict(list)
        for line in (ROOT/f'metadata/level2_{f}.tiles').read_text().splitlines():
            l,x,y,t,p,h,v=map(int,line.split(','))
            if l==0 and t//256 in [5,6,7] and 0<=x<=248 and y<200:
                groups[(t,p)].append((x,y))
        for key,places in groups.items():
            if key in out:continue
            t,p=key
            x,y=min(places,key=lambda q:(abs(q[0]-128),q[1]))
            out[key]=art.crop((x*4,y*4,x*4+32,y*4+32))
    # The game swaps identical CHR cells between banks 5 and 7 while
    # scrolling. Reuse their exact painted counterparts, including tires.
    by_pixels={}
    for (t,p),im in out.items():by_pixels.setdefault((pixels(t).tobytes(),p),im)
    # The horizontal office-window cell must not sample a nearby cornice.
    if (0x772,0x0f001038) in out:out[(0x753,0x0f001038)]=out[(0x772,0x0f001038)]
    road=Image.open(ROOT/'art/level2_cab.png').convert('RGBA')
    road=road.crop((int(road.width*.62),int(road.height*.56),int(road.width*.67),int(road.height*.61))).resize((32,32),Image.Resampling.LANCZOS)
    sky=Image.new('RGBA',(32,32))
    keys=[tuple(k) for k in json.loads((ROOT/'metadata/level2_background_keys.json').read_text())]
    variants=[]
    for t,p in keys:
        ix=pixels(t)
        im=out.get((t,p))
        if im is None:im=by_pixels.get((ix.tobytes(),p))
        if t in [0x503,0x783] and p==0x0f001020:
            im=refs[0][1].crop((0,388,32,420))
        if im is None:
            # Unseen edge cells retain original geometry, with stage-specific colors.
            src=np.array(scale(tile(t,p)));cols=[(p>>s)&255 for s in [24,16,8,0]]
            colors={0x0f:[7,13,19],0x00:[78,88,98],0x10:[156,172,183],0x20:[228,235,235],
                    0x38:[226,202,148],0x09:[13,57,38],0x19:[25,115,67],0x1c:[17,95,124],0x2c:[62,157,193]}
            idx=np.repeat(np.repeat(ix,4,axis=0),4,axis=1)
            for j,c in enumerate(cols):
                if c in colors:src[idx==j,:3]=colors[c]
            im=Image.fromarray(src)
        if p==0x0f1c2c20:
            # Sky colored pixels (source index 2) are one cohesive blue;
            # avoid copying tiny disconnected cloud fragments into every tile.
            mask=np.repeat(np.repeat(ix==2,4,axis=0),4,axis=1)
            a=np.array(im);a[mask]=[65,157,222,255];im=Image.fromarray(a)
            if t in [0x704,0x707,0x708,0x709,0x716,0x717,0x718,0x719]:im=sky
            elif t in [0x705,0x706,0x714,0x715,0x724,0x725]:
                a=np.array(im);a[mask,3]=0;im=Image.fromarray(a)
            # Native dotted roadway and the narrow gaps between trailers.
            if t==0x523 or any(np.array_equal(ix,pixels(u)) for u in [0x70d,0x71d,0x7a3]):im=road
        if t in [0x502,0x512,0x522,0x506,0x516,0x782,0x792,0x7a2,0x786,0x796] and p in [0x0f001020,0x0f091910]:
            a=np.array(im);rgb=a[:,:,:3].astype(float)
            cyan=(rgb[:,:,2]>rgb[:,:,0]*1.35)&(rgb[:,:,1]>rgb[:,:,0]*1.25)&(rgb[:,:,2]>=rgb[:,:,1]*.95)&(rgb[:,:,0]<180)
            a[cyan]=np.array(road)[cyan];im=Image.fromarray(a)
        if np.all(ix==0):im=Image.new('RGBA',(32,32),(7,13,19,255))
        variants.append((t,p,im,None))
    return variants
