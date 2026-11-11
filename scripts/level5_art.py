"""Train/canyon art with identical moving-bank aliases and palette variants."""
from common import *
from collections import defaultdict
import json
from level2_art import fit_reference


def level5_art(conditions):
    refs=[(300,fit_reference('level5_train.png',
           [0,490/1214,575/1214,880/1214,980/1214,1008/1214,1],
           [0,384,448,696,772,800,960])),
          (13410,fit_reference('level5_engine.png',
           [0,442/1214,520/1214,840/1214,945/1214,973/1214,1],
           [0,384,448,696,772,800,960])),
          (10860,fit_reference('level5_freight.png',
           [0,450/1214,527/1214,612/1214,700/1214,840/1214,945/1214,973/1214,1],
           [0,384,448,512,576,696,772,800,960]))]
    # One continuous sky sits behind the moving mountains and mesas. Native
    # tiny cloud cells become transparent instead of repeating painted scraps.
    # Reuse the existing sky image without shipping a duplicate PNG.
    # Register the freight door columns as well as their row boundaries.
    freight=refs[2][1];registered=Image.new('RGBA',(1024,960))
    sx=[0,289/1295*1024,370/1295*1024,840/1295*1024,1094/1295*1024,1024]
    tx=[0,232,300,680,880,1024]
    for x0,x1,u0,u1 in zip(sx,sx[1:],tx,tx[1:]):
        registered.paste(freight.crop((round(x0),0,round(x1),960)).resize((u1-u0,960),Image.Resampling.LANCZOS),(u0,0))
    refs[2]=(10860,registered)
    mapped={};places_by_key={}
    for f,art in refs:
        groups=defaultdict(list)
        for line in (ROOT/f'metadata/level5_{f}.tiles').read_text().splitlines():
            l,x,y,t,p,h,v=map(int,line.split(','))
            if l==0 and t//256 in [5,10] and 0<=x<=248 and 0<=y<200:groups[t,p].append((x,y))
        for key,places in groups.items():
            if key in mapped:continue
            x,y=min(places,key=lambda a:(abs(a[0]-128),a[1]))
            mapped[key]=art.crop((x*4,y*4,x*4+32,y*4+32));places_by_key[key]=(x,y)
    # The engine's 580-5FF bank alternates with A00-A7F every two frames.
    # Several identical native patterns occupy different painted panel rows.
    # Resolve the explicit bank counterpart before generic pattern matching,
    # otherwise an unchanged native panel can select a different HD row.
    engine_bank_art={}
    for t in range(0x580,0x600):
        p=0x0f0b1b2b;u=t+0x480
        if (t,p) in mapped and np.array_equal(pixels(t),pixels(u)):
            engine_bank_art[u,p]=mapped[t,p]
    patterns={};any_palette=defaultdict(list)
    for (t,p),im in mapped.items():
        pat=pixels(t).tobytes();patterns.setdefault((pat,p),im)
        any_palette[pat].append((p,im))
    train_palettes=[0x0f001020,0x0f081828,0x0f0a1a2a,0x0f061626,0x0f0b1b2b]
    colors={0x0f001020:[.8,.88,.95],0x0f081828:[.95,.68,.13],
            0x0f0a1a2a:[.06,.62,.23],0x0f061626:[.88,.16,.09],0x0f0b1b2b:[.06,.57,.26]}
    def recolor(im,p):
        a=np.array(im).astype(float);lum=a[:,:,:3]@np.array([.299,.587,.114]);target=np.array(colors[p])
        a[:,:,:3]=np.minimum(255,lum[:,:,None]*target/np.dot(target,[.299,.587,.114]));return Image.fromarray(a.astype('uint8'))
    fallback=[];out=[]
    for t,p in json.loads((ROOT/'metadata/level5_background_keys.json').read_text()):
        ix=pixels(t);pat=ix.tobytes();im=engine_bank_art.get((t,p),mapped.get((t,p),patterns.get((pat,p))))
        # Palette changes must recolor one registered freight-car surface,
        # not splice in differently aligned rib/door art from another view.
        # The engine palette keeps its own painted panel/vent surfaces.
        steel=patterns.get((pat,0x0f001020))
        if steel is not None and p in train_palettes[:-1] and (0x500<=t<0x600 or 0xa00<=t<0xa80):
            im=steel if p==0x0f001020 else recolor(steel,p)
        if im is None and p in train_palettes and any_palette[pat]:
            choices=any_palette[pat];src,im=next(((sp,im) for sp,im in choices if sp==0x0f001020),choices[0])
            im=recolor(im,p)
        if im is None and p==0x0f312c20 and t in [0xa01,0xa02,0x581,0x582]:
            im=Image.new('RGBA',(32,32))
        if im is None:
            fallback.append([t,p]);im=scale(tile(t,p))
            # Keep rare transition-edge shapes, using actual painted metal or
            # rock rather than flat NES fills.
            swatch=refs[0][1].crop((180,250,212,282)) if p==0x0f081828 and 0xa00<=t<0xa80 else refs[0][1].crop((300,520,332,552))
            if p in colors:swatch=recolor(swatch,p)
            a=np.array(im);tex=np.array(swatch).astype(float);idx=np.repeat(np.repeat(ix,4,axis=0),4,axis=1)
            for i in range(4):
                m=idx==i;a[m]=np.clip(tex*(.45+.22*i),0,255).astype('uint8')[m]
            a[idx==0]=[2,8,10,255];im=Image.fromarray(a)
        if p==0x0f312c20:
            # Index 2 is sky; upper tiny-cloud tiles reveal the single backdrop.
            coords=places_by_key.get((t,p));a=np.array(im)
            if (coords and coords[1]<32) or t in [0xa01,0xa02,0x581,0x582]:im=Image.new('RGBA',(32,32))
            else:
                mask=np.repeat(np.repeat(ix==2,4,axis=0),4,axis=1);a[mask,3]=0;im=Image.fromarray(a)
        if not ix.any():im=Image.new('RGBA',(32,32),(0,0,0,255))
        out.append((t,p,im,None))
    lookup={(t,p):im for t,p,im,_ in out};extra=[]
    context=json.loads((ROOT/'metadata/level5_train_contexts.json').read_text())
    for j,(kind,t,p,y,nt,npal) in enumerate(context['train']):
        row=f'level5_row_{y}'
        declaration=f'<condition>{row},originPositionCheckY,==,{y}'
        if declaration not in conditions:conditions.append(declaration)
        near=f'level5_train_{j}'
        conditions.append(f'<condition>{near},tileNearby,0,{112-y},{nt:X},{npal:08X},N')
        if kind=='wall':
            im=lookup.get((t,npal))
            if im is None:im=recolor(lookup[t,p],npal)
        else:
            # A freight-car body directly below distinguishes its roof from
            # the locomotive vents, including native scrolling bank swaps.
            im=refs[0][1].crop((384,y*4,416,y*4+32))
            if y==104:im=recolor(im,npal)
        extra.append((t,p,im,row+'&'+near))
    for j,(t,p,y,dx,dy,nt,npal) in enumerate(context['canyon_blanks']):
        row=f'level5_shadow_row_{y}'
        declaration=f'<condition>{row},originPositionCheckY,==,{y}'
        if declaration not in conditions:conditions.append(declaration)
        near=f'level5_shadow_{j}'
        conditions.append(f'<condition>{near},tileNearby,{dx},{dy},{nt:X},{npal:08X},N')
        shadow=refs[0][1].crop((320,300,352,332));a=np.array(shadow);a[:,:,:3]=(a[:,:,:3]*.55).astype('uint8')
        extra.append((t,p,Image.fromarray(a),row+'&'+near))
    out=extra+out
    (ROOT/'validation/level5_background_mapping.json').write_text(json.dumps({'reference_cells':len(mapped),'material_fallback':fallback,'train_context_rules':len(context['train']),'canyon_shadow_rules':len(context['canyon_blanks']),'engine_bank_aliases':len(engine_bank_art)},indent=2)+'\n')
    return out
