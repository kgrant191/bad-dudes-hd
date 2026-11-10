"""Forest scenery registered to the original scrolling tile and palette keys."""
from common import *
from collections import defaultdict
import json
from level2_art import fit_reference


def level4_art():
    refs=[(300,'level4_forest.png'),(4620,'level4_ferns.png'),
          (30,'level4_tall_tree.png'),(4980,'level4_lower_forest.png'),
          (750,'level4_cliff_edge.png'),(6660,'level4_broken_stump.png')]
    mapped={}
    for f,name in refs:
        art=Image.open(ROOT/'art'/name).convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS)
        if f==4980:
            art=fit_reference(name,[0,470/1214,777/1214,860/1214,980/1214,1],[0,384,640,704,800,960])
        if f==6660:
            art=fit_reference(name,[0,474/1214,784/1214,870/1214,990/1214,1],[0,384,640,704,800,960])
        groups=defaultdict(list)
        for line in (ROOT/f'metadata/level4_{f}.tiles').read_text().splitlines():
            l,x,y,t,p,h,v=map(int,line.split(','))
            if l==0 and t//256==9 and 0<=x<=248 and 0<=y<200:groups[t,p].append((x,y))
        for key,places in groups.items():
            if key in mapped:continue
            x,y=min(places,key=lambda a:(abs(a[0]-128),a[1]))
            mapped[key]=art.crop((x*4,y*4,x*4+32,y*4+32))
    patterns={(pixels(t).tobytes(),p):im for (t,p),im in mapped.items()}
    source=Image.open(ROOT/'art/level4_forest.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS)
    stone=source.crop((180,440,212,472));bark=source.crop((100,160,132,192));leaf=source.crop((300,30,332,62))
    unseen=[];out=[]
    for t,p in json.loads((ROOT/'metadata/level4_background_keys.json').read_text()):
        ix=pixels(t);im=mapped.get((t,p),patterns.get((ix.tobytes(),p)))
        if im is None:
            unseen.append([t,p])
            # Rare boundary and cut-trunk cells keep the native shape with
            # detailed material sampled from the matching painted scenery.
            im=scale(tile(t,p));a=np.array(im);idx=np.repeat(np.repeat(ix,4,axis=0),4,axis=1)
            cols=[(p>>s)&255 for s in [24,16,8,0]]
            for j,c in enumerate(cols):
                m=idx==j
                if c in [0xf,0xe,0xd]:a[m]=[0,0,0,255]
                else:
                    swatch=stone if c in [7,0x17,0x27] else bark if c in [8,0x18,0x28] else leaf
                    tex=np.array(swatch).astype(float);tex[:,:,:3]*=.45+.27*((c>>4)&3);a[m]=np.clip(tex,0,255).astype('uint8')[m]
            im=Image.fromarray(a)
        if not ix.any():im=Image.new('RGBA',(32,32),(0,0,0,255))
        out.append((t,p,im))
    (ROOT/'validation/level4_background_mapping.json').write_text(json.dumps({'reference_cells':len(mapped),'material_fallback':unseen},indent=2)+'\n')
    return out
