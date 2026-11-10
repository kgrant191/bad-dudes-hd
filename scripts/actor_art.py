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
    elif target==0xff001020: # boss damage flash
        grey=rgb@np.array([.299,.587,.114]);rgb[:]=grey[:,:,None]*.75+62
    elif target==0xff301638:
        rgb[:]=np.minimum(255,rgb*.55+np.array([255,126,57])*.45)
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
    for name in ['player_missing','enemy_poses','effect_poses','v4_actions','v5_actions','v6_actions']:
        poses+=json.loads((ROOT/f'metadata/{name}.json').read_text())
    sheets={};variants=defaultdict(list);stats=[];preview=[]
    palettes=defaultdict(set)
    for t,p in keys:
        if p>>24==255:palettes[t].add(p)
    for i,pose in enumerate(poses):
        rows=pose['tiles'];sp=pose['palette'];w=max(r[0] for r in rows)+8;h=max(r[1] for r in rows)+8
        original=Image.new('RGBA',(w*4,h*4));coverage=Image.new('L',original.size)
        for x,y,t,hm,vm in rows:
            im=scale(tile(t,sp))
            if hm:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if vm:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            original.alpha_composite(im,(x*4,y*4));coverage.paste(255,(x*4,y*4,(x+8)*4,(y+8)*4))
        name=pose['sheet'];j=pose['cell'];bbox=original.getchannel('A').getbbox()
        def fitted(sheet_name, cell=None):
            j=pose["cell"] if cell is None else cell
            if sheet_name not in sheets:sheets[sheet_name]=Image.open(ROOT/'art'/sheet_name).convert('RGBA')
            sheet=sheets[sheet_name];cols=pose['columns'];rs=pose['rows']
            cw,ch=sheet.width/cols,sheet.height/rs
            crop=sheet.crop((round(j%cols*cw),round(j//cols*ch),round((j%cols+1)*cw),round((j//cols+1)*ch)))
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
            painted=crop.crop(bb).resize((bbox[2]-bbox[0],bbox[3]-bbox[1]),Image.Resampling.LANCZOS)
            canvas=Image.new('RGBA',original.size);canvas.alpha_composite(painted,bbox[:2])
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
                allowed=pose.get('palettes')
                if allowed and p not in allowed and not (p==0xff0f351a and any((q&0xffffff00)==0xff0f3500 for q in allowed)):continue
                # Never turn intro/black fade palettes into visible actors.
                if p==0xff0f0f0f:continue
                if name.startswith('player_') and p not in [0xff0f2620,0xff0f2820,0xff301638]:continue
                if name in ['ninjas_a.png','ninjas_b.png','specialists.png','enemy_actions.png'] and (p&0xffffff00)!=0xff0f3500:continue
                if name in ['boss.png','boss_actions.png'] and p not in [0xff0f3606,0xff001020]:continue
                base=im2 if im2 is not None and p==0xff0f2820 else im
                painted=pickup_variant(base,p) if pose.get('pickup') or (name=='effects.png' and j in [0,1]) else palette_variant(base,sp,p)
                variant={'pose':i,'x':x,'y':y,'h':hm,'v':vm,'image':painted}
                if im2 is not None and p==0xff301638:variant['player2_image']=palette_variant(im2,sp,p)
                variants[(t,p)].append(variant)
    out=Image.new('RGB',(1280,((len(preview)+5)//6)*270),'#293541');d=ImageDraw.Draw(out)
    for j,(orig,im,i) in enumerate(preview):
        x=j%6*212;y=j//6*270;d.text((x,y),f'{i}: {poses[i]["sheet"]} {poses[i]["cell"]}',fill='white');out.paste(im,(x,y+20),im)
    out.save(ROOT/'validation/actors_review.png')
    (ROOT/'validation/actor_slicing.json').write_text(json.dumps(stats,indent=2))
    return variants,poses
