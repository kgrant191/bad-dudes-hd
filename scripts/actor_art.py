"""Fit new painted actors/effects to captured cells and preserve palette variants."""
from common import *
from collections import defaultdict
import json
from PIL import ImageDraw

def palette_variant(im, source, target):
    if source == target: return im
    a=np.array(im).astype(float);rgb=a[:,:,:3]
    if target==0xff303030:
        rgb[:]=[247,255,244]
    elif target in [0xff001020,0xff300010]: # boss damage flash
        grey=rgb@np.array([.299,.587,.114]);rgb[:]=grey[:,:,None]*.75+62
    elif target==0xff301638:
        rgb[:]=np.minimum(255,rgb*.55+np.array([255,126,57])*.45)
    elif target==0xff0f1018:
        # Final-stage return of the armored Level 4 boss: olive armor.
        spread=rgb.max(axis=2)-rgb.min(axis=2);mask=spread<48
        lum=rgb.max(axis=2)/180
        rgb[mask]=np.clip(lum[mask,None]*np.array([128,123,61]),0,255)
    elif target==0xff0f1c08:
        # Returning bosses retain their detailed skin/armor; only the native
        # costume palette changes to the train encounter's olive brown.
        r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
        mask=((r>g*1.6)&(r>b*1.4)&(g<110)) if source==0xff0f3606 else ((r>g*1.15)&(b>g*1.15))
        lum=rgb.max(axis=2)/170
        rgb[mask]=np.clip(lum[mask,None]*np.array([111,95,43]),0,255)
    elif source==0xff0f3602 and (target & 0xffffff00)==0xff0f3500:
        # Small ninja aliases retain the known uniform family in later stages.
        r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
        mask=(b>g*1.2)&(b>r*.8)
        if target==0xff0f3510:
            grey=rgb@np.array([.299,.587,.114]);rgb[mask]=grey[mask,None]*np.array([.98,1.02,1.06])
        else:
            colors={0x12:[54,82,194],0x16:[190,47,35],0x1c:[24,155,156],0x1a:[39,146,38]}
            lum=rgb.max(axis=2)/190
            rgb[mask]=np.clip(lum[mask,None]*np.array(colors[target&255]),0,255)
    elif (target & 0xffffff00)==0xff0f3500 and (source & 0xffffff00)==0xff0f3500:
        # The ROM changes ninja uniform colors without changing their tiles.
        src=source&255;dst=target&255
        r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
        if src==0x12: mask=(b>r*1.12)&(b>g*1.04)
        elif src==0x10: mask=(np.max(rgb,axis=2)-np.min(rgb,axis=2)<27)
        elif src==0x1a: mask=(g>r*1.15)&(g>b*1.15)
        elif src==0x1c: mask=(g>r*1.15)&(b>r*1.1)
        else: mask=(r>g*1.35)&(r>b*1.55)&(g<120)
        colors={0x12:[54,82,194],0x16:[190,47,35],0x10:[151,157,164],0x1c:[24,155,156],0x1a:[39,146,38]}
        lum=rgb.max(axis=2)/190
        rgb[mask]=np.clip(lum[mask,None]*np.array(colors.get(dst,[151,157,164])),0,255)
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))

def pickup_variant(im, target):
    """The pickup keeps its detailed shape in both native palette phases."""
    if target != 0xff301638: return im
    a = np.array(im).astype(float)
    a[:, :, :3] = a[:, :, :3] * .65 + 255 * .35
    return Image.fromarray(a.astype('uint8'))

def actor_art(keys):
    poses=[]
    for name in ['player_missing','enemy_poses','effect_poses','v4_actions','v5_actions','v6_actions','v7_actions','v8_actions','v9_actions','v10_actions','v11_actions']:
        poses+=json.loads((ROOT/f'metadata/{name}.json').read_text())
    sheets={};variants=defaultdict(list);stats=[];preview=[]
    palettes=defaultdict(set)
    for t,p in keys:
        if p>>24==255:palettes[t].add(p)
    for i,pose in enumerate(poses):
        rows=pose['tiles'];sp=pose['palette'];w=max(r[0] for r in rows)+8;h=max(r[1] for r in rows)+8
        original=Image.new('RGBA',(w*4,h*4));coverage=Image.new('L',original.size)
        for x,y,t,hm,vm in rows:
            im=scale(tile(t,pose.get('tile_palettes',{}).get(str(t),sp)))
            if hm:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if vm:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            original.alpha_composite(im,(x*4,y*4));coverage.paste(255,(x*4,y*4,(x+8)*4,(y+8)*4))
        name=pose['sheet'];j=pose['cell'];bbox=original.getchannel('A').getbbox()
        def fitted(sheet_name, cell=None):
            j=pose["cell"] if cell is None else cell
            if sheet_name not in sheets:sheets[sheet_name]=Image.open(ROOT/'art'/sheet_name).convert('RGBA')
            sheet=sheets[sheet_name];cols=pose['columns'];rs=pose['rows']
            cw,ch=sheet.width/cols,sheet.height/rs
            crop=sheet.crop(pose.get('art_rect',(round(j%cols*cw),round(j//cols*ch),round((j%cols+1)*cw),round((j//cols+1)*ch))))
            if pose.get('flip_art'):crop=crop.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if pose.get('art_rotation'):crop=crop.rotate(pose['art_rotation'],resample=Image.Resampling.BICUBIC,expand=True)
            # Ignore tiny detached fragments from adjacent generated atlas cells.
            from scipy.ndimage import label
            ca=np.array(crop);labels,nlabels=label(ca[:,:,3]>80)
            sizes=np.bincount(labels.ravel());sizes[0]=0
            if nlabels:
                keep=sizes>=max(24,sizes.max()*.012)
                ca[~keep[labels],3]=0;crop=Image.fromarray(ca)
            bb=crop.getchannel('A').point(lambda a:255 if a>80 else 0).getbbox()
            if not bb or not bbox:raise ValueError(f'Empty actor cell: {sheet_name} {j}')
            if 'art_scale' in pose:
                # Shared sheet scale keeps a limb or head movement from
                # stretching the animal's body to a new native bounding box.
                k=pose['art_scale'];size=(round((bb[2]-bb[0])*k),round((bb[3]-bb[1])*k))
                ax,ay=pose['art_anchor'];position=(round(ax-size[0]/2),round(ay-size[1]))
            else:
                size=(bbox[2]-bbox[0],bbox[3]-bbox[1]);position=bbox[:2]
            painted=crop.crop(bb).resize(size,Image.Resampling.LANCZOS)
            canvas=Image.new('RGBA',original.size);canvas.alpha_composite(painted,position)
            return canvas
        canvas=fitted(name)
        player2_name=pose.get('player2_sheet') or {'player_sheet_missing.png':'player2_missing.png','player_hit.png':'player2_hit.png'}.get(name)
        player2=fitted(player2_name, pose.get("player2_cell")) if player2_name else None
        # Cells are the engine's drawable coverage. Clear outside them for QA.
        a=np.array(canvas);loss=int(((a[:,:,3]>32)&(np.array(coverage)==0)).sum())
        stats.append({'pose':i,'sheet':name,'cell':j,'tiles':len(rows),'clipped_pixels':loss})
        a[np.array(coverage)==0,3]=0;preview.append((original,Image.fromarray(a),i))
        for x,y,t,hm,vm in rows:
            im=canvas.crop((x*4,y*4,(x+8)*4,(y+8)*4))
            if hm:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if vm:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            im2=None
            if player2 is not None:
                im2=player2.crop((x*4,y*4,(x+8)*4,(y+8)*4))
                if hm:im2=im2.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if vm:im2=im2.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            for p in palettes[t]:
                if p in pose.get('excluded_palettes',[]):continue
                part_palette=pose.get('tile_palettes',{}).get(str(t))
                if part_palette is not None and p not in [part_palette,0xff001020]+pose.get('damage_palettes',[]):continue
                allowed=pose.get('palettes')
                if allowed and p not in allowed and not (p==0xff0f351a and any((q&0xffffff00)==0xff0f3500 for q in allowed)):continue
                # Never turn intro/black fade palettes into visible actors.
                if p==0xff0f0f0f:continue
                if name.startswith('player_') and p not in [0xff0f2620,0xff0f2820,0xff301638]:continue
                if name in ['ninjas_a.png','ninjas_b.png','specialists.png','enemy_actions.png'] and (p&0xffffff00)!=0xff0f3500:continue
                if name in ['boss.png','boss_actions.png'] and p not in [0xff0f3606,0xff001020,0xff0f1c08]:continue
                base=im2 if im2 is not None and p==0xff0f2820 else im
                painted=pickup_variant(base,p) if pose.get('pickup') or (name=='effects.png' and j in [0,1]) else palette_variant(base,part_palette if part_palette is not None else sp,p)
                variant={'pose':i,'x':x,'y':y,'h':hm,'v':vm,'image':painted}
                if im2 is not None and p==0xff301638:variant['player2_image']=palette_variant(im2,sp,p)
                variants[(t,p)].append(variant)
    # Shared native head/torso cells stay identical while the ninja's legs
    # animate. A different fitted full-body crop must not resize his head.
    for i,pose in enumerate(poses):
        source=pose.get('share_native_tiles_from')
        if not source:continue
        base=next(j for j,p in enumerate(poses) if p['sheet']==source['sheet'] and p['cell']==source['cell'])
        for variants_for_key in variants.values():
            shared=next((v for v in variants_for_key if v['pose']==base),None)
            if shared:
                for v in variants_for_key:
                    if v['pose']==i:v['image']=shared['image'].copy()
    # The airborne chain has byte-identical CHR aliases in bank 1D.
    for alias in json.loads((ROOT/'metadata/v8_sprite_aliases.json').read_text()):
        t,u,p=alias['tile'],alias['source'],alias['palette']
        assert np.array_equal(pixels(t),pixels(u))
        if (t,p) in keys and (u,p) in variants:
            variants[t,p]=[dict(variants[u,p][0])]
    # The chain extends by repeating the same native link cell. Cropping each
    # occurrence from a whole fighter painting gives that repeated cell a hand,
    # claw or different vertical alignment. Use one weapon strip for all three
    # byte-identical CHR banks, independent of body pose and chain length.
    chain_pose=next(i for i,p in enumerate(poses) if p['sheet']=='level5_boss.png' and p['cell']==9)
    weapon=sheets['level5_boss.png'].crop((1500,415,1800,550))
    bb=weapon.getchannel('A').point(lambda a:255 if a>80 else 0).getbbox()
    weapon=weapon.crop(bb).resize((128,36),Image.Resampling.LANCZOS)
    strip=Image.new('RGBA',(128,64));strip.alpha_composite(weapon,(0,28))
    for heads,rect in [([0x19ac,0x19ec,0x1d68],(32,0,64,64)),
                       ([0x19ae,0x19ee,0x1d6a],(96,0,128,64)),
                       ([0x19b2,0x19f2,0x1d6e],(96,0,128,64))]:
        part=strip.crop(rect)
        for t in heads:
            for half in [0,1]:
                cell=part.crop((0,half*32,32,(half+1)*32))
                for p in palettes[t+half]:
                    if p not in [0xff0f361c,0xff001020]:continue
                    variants[t+half,p]=[{'pose':chain_pose,'x':0,'y':half*8,'h':0,'v':0,
                        'image':palette_variant(cell,0xff0f361c,p)}]
    # Rescue victory reuses the detailed hand through an alternate CHR tile.
    assert np.array_equal(pixels(0xf6f),pixels(0xf2f))
    for p in [0xff0f2620,0xff0f2820,0xff301638]:
        if (0xf2f,p) in variants:variants[0xf6f,p]=[dict(variants[0xf2f,p][0])]
    out=Image.new('RGB',(1280,((len(preview)+5)//6)*270),'#293541');d=ImageDraw.Draw(out)
    for j,(orig,im,i) in enumerate(preview):
        x=j%6*212;y=j//6*270;d.text((x,y),f'{i}: {poses[i]["sheet"]} {poses[i]["cell"]}',fill='white');out.paste(im,(x,y+20),im)
    out.save(ROOT/'validation/actors_review.png')
    (ROOT/'validation/actor_slicing.json').write_text(json.dumps(stats,indent=2))
    return variants,poses
