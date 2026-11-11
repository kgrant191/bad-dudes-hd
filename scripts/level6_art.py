"""Cave artwork registered to the original scene's scrolling tile geometry."""
from common import *
from collections import defaultdict
import json
from level2_art import fit_reference


def level6_art():
    refs=[(300,fit_reference('level6_cave.png',
        [0,488/1214,902/1214,1014/1214,1],[0,384,704,800,960])),
        (1950,fit_reference('level6_pillar.png',
        [0,474/1214,881/1214,995/1214,1],[0,384,704,800,960])),
        (9960,fit_reference('level6_depths.png',
        [0,850/1214,966/1214,1],[0,704,800,960])),
        (7890,fit_reference('level6_ceiling.png',
        [0,904/1214,956/1214,1],[0,768,800,960])),
        (420,fit_reference('level6_rock_wall.png',
        [0,466/1214,865/1214,978/1214,1],[0,384,704,800,960]))]
    mapped={}
    for f,art in refs:
        groups=defaultdict(list)
        for line in (ROOT/f'metadata/level6_{f}.tiles').read_text().splitlines():
            l,x,y,t,p,h,v=map(int,line.split(','))
            if l==0 and t//256==0xb and 0<=x<=248 and 0<=y<200:
                groups[t,p].append((x,y))
        for key,places in groups.items():
            if key in mapped:continue
            x,y=min(places,key=lambda a:(abs(a[0]-128),a[1]))
            mapped[key]=art.crop((x*4,y*4,x*4+32,y*4+32))
    patterns={}
    for (t,p),im in mapped.items():patterns.setdefault((pixels(t).tobytes(),p),im)
    missing=[];edge_material=[];out=[]
    for t,p in json.loads((ROOT/'metadata/level6_background_keys.json').read_text()):
        ix=pixels(t);im=mapped.get((t,p),patterns.get((ix.tobytes(),p)))
        if not ix.any():im=Image.new('RGBA',(32,32),(0,0,0,255))
        if im is None and t in [0xb24,0xb34] and p==0x0f1c2c3b:
            # Two one-column right-screen cliff boundaries never appear in a
            # full source view. Keep their native contour and use the adjacent
            # painted limestone surface, not the original cyan fallback.
            texture=np.array(refs[0][1].crop((512,480,544,512)))
            mask=np.array(scale(tile(t,p)))[:,:,:3].max(axis=2)>12
            a=np.zeros((32,32,4),dtype='uint8');a[:,:,3]=255;a[mask]=texture[mask]
            im=Image.fromarray(a);edge_material.append([t,p])
        if im is None:
            missing.append([t,p]);im=scale(tile(t,p))
        out.append((t,p,im))
    (ROOT/'validation/level6_background_mapping.json').write_text(json.dumps(
        {'reference_cells':len(mapped),'edge_material':edge_material,'unmapped':missing},indent=2)+'\n')
    return out
