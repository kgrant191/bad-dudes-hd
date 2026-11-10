"""Sewer artwork registered to the native scrolling tile layout."""
from common import *
from collections import defaultdict
import json
from level2_art import fit_reference


def level3_art():
    refs=[(300,'level3_sewer.png'),(2280,'level3_drains.png'),(5880,'level3_broken_wall.png'),(3630,'level3_lower_drains.png')]
    mapped={}
    for f,name in refs:
        art=Image.open(ROOT/'art'/name).convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS)
        if f==5880:
            art=fit_reference(name,[0,486/1214,858/1214,1016/1214,1],[0,392,684,800,960])
        if f==3630:
            original=art.copy()
            source_x=[0,92*4,140*4,184*4,256*4]
            target_x=[0,100*4,140*4,190*4,256*4]
            for sx0,sx1,tx0,tx1 in zip(source_x,source_x[1:],target_x,target_x[1:]):
                art.paste(original.crop((sx0,0,sx1,960)).resize((tx1-tx0,960),Image.Resampling.LANCZOS),(tx0,0))
        groups=defaultdict(list)
        for line in (ROOT/f'metadata/level3_{f}.tiles').read_text().splitlines():
            l,x,y,t,p,h,v=map(int,line.split(','))
            if l==0 and t//256==8 and 0<=x<=248 and 0<=y<200:groups[t,p].append((x,y))
        for key,places in groups.items():
            if key in mapped:continue
            x,y=min(places,key=lambda a:(abs(a[0]-128),a[1]))
            mapped[key]=art.crop((x*4,y*4,x*4+32,y*4+32))
    # Exact CHR-pattern duplicates retain the same material crop.
    patterns={(pixels(t).tobytes(),p):im for (t,p),im in mapped.items()}
    source=Image.open(ROOT/'art/level3_sewer.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS)
    stone=source.crop((104,422,168,486)).resize((32,32),Image.Resampling.LANCZOS)
    brick=source.crop((272,128,336,192)).resize((32,32),Image.Resampling.LANCZOS)
    plaster=source.crop((280,280,344,344)).resize((32,32),Image.Resampling.LANCZOS)
    unseen=[];out=[]
    for t,p in json.loads((ROOT/'metadata/level3_background_keys.json').read_text()):
        ix=pixels(t);im=mapped.get((t,p),patterns.get((ix.tobytes(),p)))
        if im is None:
            unseen.append([t,p])
            # Preserve the source mask for rare partial cells and alternate
            # drain phases, with colors and materials from the painted set.
            im=scale(tile(t,p));a=np.array(im);idx=np.repeat(np.repeat(ix,4,axis=0),4,axis=1)
            cols=[(p>>s)&255 for s in [24,16,8,0]]
            for j,c in enumerate(cols):
                m=idx==j
                if c in [0xf,0xe,0xd]:a[m]=[4,8,7,255]
                elif c in [0xb,0x1b,0x2b]:
                    tex=np.array(stone).astype(float);tex[:,:,:3]*={0xb:.35,0x1b:.7,0x2b:1.0}[c];a[m]=tex.astype('uint8')[m]
                elif c in [8,0x18]:a[m]=np.array(brick)[m]
                elif c in [0,0x10]:
                    tex=np.array(plaster).astype(float);tex[:,:,:3]*=.6 if c==0 else 1;a[m]=tex.astype('uint8')[m]
            im=Image.fromarray(a)
        if not ix.any():im=Image.new('RGBA',(32,32),(3,7,6,255))
        out.append((t,p,im))
    (ROOT/'validation/level3_background_mapping.json').write_text(json.dumps({'reference_cells':len(mapped),'material_fallback':unseen},indent=2)+'\n')
    return out
