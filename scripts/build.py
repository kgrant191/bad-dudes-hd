from common import *
from collections import defaultdict
from PIL import ImageDraw
import json, math, hashlib, argparse
from player_art import player_art, flash
from actor_art import actor_art
from hud_art import hud_tile, panel, message_tile
from level2_art import level2_art
from level3_art import level3_art
from level4_art import level4_art
from level5_art import level5_art
parser=argparse.ArgumentParser(description='Build Bad Dudes HD from its art and captured tile mappings.')
parser.add_argument('--previews',type=Path,help='Optional directory for offline layout previews')
args=parser.parse_args()

OUT=ROOT/'pack';OUT.mkdir(exist_ok=True)
rules=[];atlas_tiles=[];tile_cache={};mapped={};special={}
blank=Image.new('RGBA',(32,32))
def briefing_glyph(t,p,default):
    # The source T/Y have one-pixel stems; the surrounding font uses two.
    # Match its 28-pixel cap width and 8-pixel stems in the original 32px cell.
    if t not in [0xd1e,0xd23]:return default
    im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im)
    color=tuple(int(c) for c in PALETTE[p&63])
    if t==0xd1e:
        shape=[(4,4),(32,4),(32,8),(22,8),(22,32),(14,32),(14,8),(4,8)]
    else:
        shape=[(4,4),(12,4),(12,11),(18,17),(24,11),(24,4),(32,4),(32,12),(22,22),(22,32),(14,32),(14,22),(4,12)]
    d.polygon([(x*4,y*4) for x,y in shape],fill=color)
    return im.resize((32,32),Image.Resampling.LANCZOS)
def add(im):
    im=im.convert('RGBA');key=hashlib.sha256(im.tobytes()).digest()
    if key not in tile_cache:
        tile_cache[key]=len(atlas_tiles);atlas_tiles.append(im)
    i=tile_cache[key];return (i%64*32,i//64*32)
def rule(t,p,im,condition=None,default=False):
    x,y=add(im)
    rules.append((f'[{condition}]' if condition else '')+f'<tile>0,{t:X},{p:08X},{x},{y},1,{"Y" if default else "N"}')
def character_rule(t,p,im,condition=None,player2=None):
    # The shared warm flash must keep the active character's identity.
    # Mirror the USA ROM palette selector at CPU $C7E4-$C80F: bit 0
    # selects the first turn; bit 1 selects the second turn when bits C0 set.
    if p == 0xff301638 and player2 is not None:
        for active in ['first_turn&second_hero_1','second_turn&second_hero_2']:
            rule(t,p,player2,active+('&'+condition if condition else ''))
    rule(t,p,im,condition)
def no_bg(im,color_index=0,t=None):
    a=np.array(im);a[pixels(t)==color_index,3]=0;return Image.fromarray(a)
keys=[]
for line in (ROOT/'metadata/capture_rules.txt').read_text().splitlines():
    if line.startswith('<tile>'):
        a=line[6:].split(',');keys.append((int(a[1],16),int(a[2],16)))
keys=list(dict.fromkeys(keys+ [tuple(k) for k in json.loads((ROOT/"metadata/additional_keys.json").read_text())]))
# Basic ninjas share pose tiles across all four uniform palettes. Cover the
# full known family rather than requiring a movie of each pose/color pair.
ninja_palettes=[0xff0f3512,0xff0f3516,0xff0f3510,0xff0f351c,0xff0f351a]
for metadata in ['enemy_poses','v4_actions']:
    for pose in json.loads((ROOT/f'metadata/{metadata}.json').read_text()):
        if pose['sheet'] in ['ninjas_a.png','ninjas_b.png'] or (pose['sheet']=='enemy_actions.png' and pose['cell']==2):
            keys.extend((row[2],p) for row in pose['tiles'] for p in ninja_palettes)
# Charge, release and dissipating punch effects alternate between the active
# hero's normal palette and the shared flash palette, even on a missed punch.
hero_palettes=[0xff0f2620,0xff0f2820,0xff301638]
for pose in json.loads((ROOT/'metadata/effect_poses.json').read_text()):
    if pose['palette'] in hero_palettes:
        keys.extend((row[2],p) for row in pose['tiles'] for p in hero_palettes)
for metadata in ['v5_actions','v6_actions','v7_actions','v8_actions']:
    for pose in json.loads((ROOT/f'metadata/{metadata}.json').read_text()):
        keys.extend((row[2],p) for row in pose['tiles'] for p in pose['palettes'])
keys=list(dict.fromkeys(keys))
panel()

# Detailed player tiles. Sprite-relative checks select the correct crop where
# the ROM reuses a tile in more than one pose; mirrored offsets are handled
# by Mesen. Every replacement remains tied to the original animation tiles.
player_variants, player_poses, _, player_stats = player_art()
player2_variants, _, _, _ = player_art(2)
player_conditions=[]
player_defaults={}
player_context=[]
for t, variants in player_variants.items():
    first=variants[0]
    player_defaults[t]=(first['image'],player2_variants[t][0]['image'])
    if len(variants)==1:continue
    signatures=[]
    for variant in variants:
        rows=player_poses[variant['pose']]['tiles']
        signatures.append({((x-variant['x'])*(-1 if variant['h'] else 1),
                            (y-variant['y'])*(-1 if variant['v'] else 1),nt)
                           for x,y,nt,h,v in rows if nt!=t})
    for j,variant in enumerate(variants[1:],1):
        # One distinguishing neighbor is enough; prefer the closest tile so
        # screen-edge clipping and native sprite-limit effects stay local.
        others=set().union(*(s for k,s in enumerate(signatures) if k!=j))
        choices=signatures[j]-others
        if not choices:continue
        dx,dy,nt=min(choices,key=lambda a:(abs(a[0])+abs(a[1]),a))
        name=f'player_{t:X}_{variant["pose"]}'
        player_conditions.append(f'<condition>{name},spriteNearby,{dx},{dy},{nt:X},FF0F2620,Y')
        player_context.append((t,name,variant['image'],player2_variants[t][j]['image']))
for t,name,im,im2 in player_context:
    rule(t,0xff0f2620,im,name)
    rule(t,0xff0f2820,im2,name)
    character_rule(t,0xff301638,flash(im),name,flash(im2))

# New actor mappings retain tile/palette identity and use local pose context.
actor_variants, actor_poses = actor_art(keys)
# Weapon layouts reuse unarmed body tiles. Include the approved unarmed
# layouts in the context search so only weapon-specific neighbors select
# the new crops, and keep the original body as the fallback.
base_pose_offset=len(actor_poses)
actor_poses+=player_poses
for (t,p), variants in actor_variants.items():
    if t not in player_variants or not any(actor_poses[v['pose']]['sheet']=='player_weapons.png' for v in variants):continue
    if p not in hero_palettes:continue
    original=[]
    for j,v in enumerate(player_variants[t]):
        q=dict(v);q['pose']+=base_pose_offset
        q['image']=player2_variants[t][j]['image'] if p==0xff0f2820 else v['image']
        if p==0xff301638:q['image']=flash(q['image']);q['player2_image']=flash(player2_variants[t][j]['image'])
        original.append(q)
    variants[:0]=original
actor_conditions=[];actor_defaults={};actor_defaults_player2={};actor_context_count=0
player_rule_count=len(rules)
for (t,p), variants in actor_variants.items():
    actor_defaults[(t,p)]=variants[0]['image']
    if 'player2_image' in variants[0]:actor_defaults_player2[(t,p)]=variants[0]['player2_image']
    if len(variants)<2:continue
    signatures=[]
    for v in variants:
        signatures.append({((x-v['x'])*(-1 if v['h'] else 1),(y-v['y'])*(-1 if v['v'] else 1),nt)
            for x,y,nt,h,vm in actor_poses[v['pose']]['tiles'] if nt!=t})
    for j,v in enumerate(variants[1:],1):
        others=set().union(*(q for k,q in enumerate(signatures) if k!=j))
        choices=signatures[j]-others
        if not choices:continue
        dx,dy,nt=min(choices,key=lambda q:(abs(q[0])+abs(q[1]),q))
        name=f'actor_{t:X}_{p:X}_{j}'
        actor_conditions.append(f'<condition>{name},spriteNearby,{dx},{dy},{nt:X},{p:08X},Y')
        character_rule(t,p,v['image'],name,v.get('player2_image'));actor_context_count+=1
rules[:]=rules[player_rule_count:]+rules[:player_rule_count]

level2_conditions=[]
for t,p,im,extra in level2_art(level2_conditions):
    rule(t,p,im,'level2&hud&stage_area'+('&'+extra if extra else ''))

for t,p,im in level3_art():
    rule(t,p,im,'level3&hud3&stage_area')

for t,p,im in level4_art():
    rule(t,p,im,'level4&hud4&stage_area')

level5_conditions=[]
for t,p,im,extra in level5_art(level5_conditions):
    rule(t,p,im,'level5&hud&stage_area'+('&'+extra if extra else ''))

# Background art retains the game's live menu, selection and dialogue layers.
for n,name in [(8,'title_intro'),(9,'title_final')]:
    im=Image.open(ROOT/'art/title.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS)
    men=Image.open(ROOT/f'art/title_men_{"intro" if n==8 else "final"}.png').convert('RGBA').resize((448,544 if n==8 else 416),Image.Resampling.LANCZOS)
    im.alpha_composite(men,(72*4,104*4))
    # Keep the original static copyright/licensing copy, accurately rendered.
    copy=render(720,0).crop((0,208,256,240));a=np.array(copy);a[np.max(a[:,:,:3],axis=2)<10,3]=0
    if n==9:im.alpha_composite(scale(Image.fromarray(a)),(0,832))
    im.save(OUT/f'{name}.png')
for name in ['select','briefing']:
    Image.open(ROOT/f'art/{name}.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS).save(OUT/f'{name}.png')
Image.open(ROOT/'art/sky.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS).save(OUT/'sky.png')

# Extract repeatable tiles from painted, aligned architectural references.
for n,name in [(3000,'street'),(3840,'truck'),(5760,'boss_area')]:
    art=Image.open(ROOT/f'art/{name}.png').convert('RGBA').resize((1024,960),Image.Resampling.LANCZOS)
    groups=defaultdict(list)
    for layer,x,y,t,p,h,v in entries(n):
        if layer==0 and t//256 in [5,6,7] and 0<=x<=248 and y<200:
            groups[(t,p)].append((x,y))
    for key,places in groups.items():
        if key in mapped:continue
        t,p=key
        # Flat blank areas are colors, not a tiny repeated fragment of a cloud.
        ix=pixels(t)
        if len(np.unique(ix))==1:continue
        x,y=sorted(places,key=lambda a:(abs(a[0]-128),a[1]))[0]
        # The recorded scroll is one pixel left of the reference's grid.
        sx=round(x/8)*32;sy=y*4
        mapped[key]=art.crop((sx,sy,sx+32,sy+32))

# Material-based fallback for architectural variants outside the reference panels.
materials=Image.open(ROOT/'art/materials.png').convert('RGB')
material_swatches=[np.array(materials.crop((c*512,r*512,(c+1)*512,(r+1)*512)).resize((64,64),Image.Resampling.LANCZOS)).astype(float) for r in range(3) for c in range(2)]
def material_tile(t,p):
    base=np.array(scale(tile(t,p))).astype(float)
    cols=[(p>>s)&255 for s in [24,16,8,0]]
    indices=np.array(Image.fromarray(pixels(t)).resize((32,32),Image.Resampling.NEAREST))
    for i,c in enumerate(cols):
        mask=indices==i
        if not mask.any():continue
        if c in [0x0f,0x0e,0x0d]:base[mask,:3]=[8,12,17];continue
        mat=0 if c in [0,0x10,0x20,0x30] else (2 if c in [0x0b,0x1b] else 1)
        tex=material_swatches[mat][(t%2)*32:(t%2+1)*32,((t//2)%2)*32:(((t//2)%2)+1)*32]
        lum=(0.40+0.20*((c>>4)&3))
        base[mask,:3]=tex[mask]*lum
    return Image.fromarray(np.clip(base,0,255).astype('uint8'))

for t,p in keys:
    sprite=p>>24==255
    bank=t//256
    src=tile(t,p)
    # Screen-specific mappings precede ordinary tile definitions.
    if bank==30 and sprite:
        rule(t,p,blank,'title_intro');rule(t,p,blank,'title_final');rule(t,p,blank,'briefing')
        special[(t,p,'title_intro')]=special[(t,p,'title_final')]=special[(t,p,'briefing')]=blank
    if bank==26 and sprite:
        rule(t,p,blank,'select');special[(t,p,'select')]=blank
    if bank==4 and not sprite:
        if 0x480<=t<=0x49f or t in [0x4c8,0x4c9,0x4ca,0x4cb]:
            a=np.array(src);a[pixels(t)==0,3]=0;im=scale(Image.fromarray(a))
        else:im=blank
        rule(t,p,im,'select');special[(t,p,'select')]=im
    if bank==13 and not sprite:
        if 0xd00<=t<0xd40:
            a=np.array(src);a[pixels(t)!=3,3]=0;im=briefing_glyph(t,p,scale(Image.fromarray(a)))
        else:im=blank
        rule(t,p,im,'briefing');special[(t,p,'briefing')]=im
    if not sprite and 0xd80<=t<=0xda7:
        hud_gate={0x0f001030:'hud3',0x0f071727:'hud4'}.get(p,'hud')
        label_gate={0x0f001030:'hud_player_label3',0x0f071727:'hud_player_label4'}.get(p,'hud_player_label')
        if t in [0xd81,0xd82]:
            rule(t,p,hud_tile(t,gold=True),hud_gate+'&hud_floor&'+label_gate)
        rule(t,p,hud_tile(t),hud_gate)
    if not sprite and t in [0x600,0x700,0x800,0x900,0xa00]:
        rule(t,p,blank,'hud_floor')
    if sprite and p==0xff001020 and 0x160c<=t<=0x1635:
        im=message_tile(t)
    elif (t,p) in actor_defaults:
        im=actor_defaults[(t,p)]
    elif not sprite and bank in [5,6,7]:
        im=mapped.get((t,p))
        if im is None:im=material_tile(t,p)
        # preserve a consistent black trailer aperture and blank areas
        if np.all(pixels(t)==0):im=Image.new('RGBA',(32,32),(7,10,15,255))
        if p==0x0f172737:
            ix=pixels(t);yy,xx=np.indices((8,8));sky=np.zeros((8,8),dtype=bool)
            if t in [0x64f,0x65f,0x670]:sky[:]=True
            elif t==0x607:sky=(yy<5)&(ix==2)
            elif t==0x608:sky=(yy<3)&(ix==2)
            elif t==0x660:sky=(ix==3)
            elif t==0x661:sky=(ix==3)
            elif t==0x665:sky=(xx<2)&(ix==2)
            elif t==0x666:sky=((xx>=4)|((yy<3)&(xx>=2)))&(ix==2)
            elif t==0x676:sky=(xx>=4)&(ix==2)
            a=np.array(im);a[np.repeat(np.repeat(sky,4,axis=0),4,axis=1),3]=0;im=Image.fromarray(a)
    elif sprite and t in player_defaults and p in [0xff0f2620,0xff0f2820,0xff301638]:
        im=player_defaults[t][1 if p==0xff0f2820 else 0]
        if p==0xff301638:im=flash(im)
    else:
        im=scale(src)
    mapped[(t,p)]=im
    second=actor_defaults_player2.get((t,p))
    if second is None and sprite and t in player_defaults and p==0xff301638:
        second=flash(player_defaults[t][1])
    character_rule(t,p,im,player2=second)

atlas=Image.new('RGBA',(2048,math.ceil(len(atlas_tiles)/64)*32))
for i,im in enumerate(atlas_tiles):atlas.paste(im,(i%64*32,i//64*32))
atlas.save(OUT/'tiles.png',optimize=True)
header=['# Bad Dudes HD v0.8.2 - Stable locomotive panels, boss chain and complete defeated pose', '<ver>109','<scale>4','<supportedRom>26E184E350F50BFA06038379A84F3B685B7509B8','<overscan>0,0,0,0','<img>tiles.png',
 '<condition>first_turn,memoryCheckConstant,23F,!=,C0,C0',
 '<condition>second_turn,memoryCheckConstant,23F,==,C0,C0',
 '<condition>second_hero_1,memoryCheckConstant,23F,==,1,1',
 '<condition>second_hero_2,memoryCheckConstant,23F,==,2,2',
 '<condition>title_intro,tileAtPosition,0,0,FD,0F263220,Y',
 '<condition>title_final,tileAtPosition,0,0,1FD,0F263220,Y',
 '<condition>select,tileAtPosition,0,0,400,0F172737,N',
 '<condition>briefing,tileAtPosition,0,0,DF1,0F0B181B,Y',
 '<condition>gameplay,memoryCheckConstant,2C0,==,0',
 '<condition>level2,memoryCheckConstant,2C0,==,1',
 '<condition>level3,memoryCheckConstant,2C0,==,2',
 '<condition>level4,memoryCheckConstant,2C0,==,3',
 '<condition>level5,memoryCheckConstant,2C0,==,4',
 '<condition>hud4,tileAtPosition,24,208,D9A,0F071727,N',
 '<condition>hud_player_label4,tileNearby,8,0,D9A,0F071727,N',
 '<condition>hud,tileAtPosition,24,208,D9A,0F001020,N',
 '<condition>hud_player_label,tileNearby,8,0,D9A,0F001020,N',
 '<condition>hud3,tileAtPosition,24,208,D9A,0F001030,N',
 '<condition>hud_player_label3,tileNearby,8,0,D9A,0F001030,N',
 '<condition>hud_floor,positionCheckY,>=,200',
 '<condition>stage_area,positionCheckY,<,200',
 '[gameplay&hud]<background>sky.png,1,0,0,10',
 '[gameplay&hud]<background>hud.png,1,0,0,11',
 '[level2&hud]<background>hud.png,1,0,0,11',
 '[level3&hud3]<background>hud.png,1,0,0,11',
 '[level4&hud4]<background>hud.png,1,0,0,11',
 '[level5&hud]<background>hud.png,1,0,0,11',
 '[level5&hud]<background>level2_sky.png,1,0,0,10',
 '[level2&hud]<background>level2_sky.png,1,0,0,10',
 '[title_intro]<background>title_intro.png,1,0,0,20',
 '[title_final]<background>title_final.png,1,0,0,20',
 '[select]<background>select.png,1,0,0,10',
 '[briefing]<background>briefing.png,1,0,0,10']
(OUT/'hires.txt').write_text('\n'.join(header+player_conditions+actor_conditions+level2_conditions+level5_conditions+rules)+'\n')
(ROOT/'build_stats.json').write_text(json.dumps({'source_keys':len(keys),'tile_rules':len(rules),'unique_atlas_tiles':len(atlas_tiles),'scale':4,'player_tiles':len(player_defaults),'player_poses_per_character':len(player_poses)+6+15+1,'player_characters':2,'player_context_rules':len(player_context)*5,'new_actor_poses':base_pose_offset,'new_actor_keys':len(actor_defaults),'actor_context_rules':actor_context_count},indent=2))

# Offline previews are only for fast layout iteration; Mesen playback is final QA.
if args.previews:args.previews.mkdir(parents=True,exist_ok=True)
for n,scene in ([(720,'title_final'),(840,'select'),(1800,'briefing'),(3000,None),(3840,None),(5760,None),(6240,None),(8160,None)] if args.previews else []):
    if scene:im=Image.open(OUT/f'{scene}.png').convert('RGBA')
    else:im=Image.open(OUT/'sky.png').convert('RGBA')
    for layer,x,y,t,p,h,v in entries(n):
        if scene=='title_final' and layer==0:continue
        sub=special.get((t,p,scene),mapped.get((t,p),scale(tile(t,p))))
        if h:sub=sub.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if v:sub=sub.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        im.alpha_composite(sub,(x*4,y*4))
    im.save(args.previews/f'preview_{n}.png')
print((ROOT/'build_stats.json').read_text())
