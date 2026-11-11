"""Keep detailed scenery and live lettering through native palette fades."""
from common import *
import json

HUD_PALETTES=[0x0f001020,0x0f001020,0x0f001030,0x0f071727,0x0f001020,0x0f1c2c3b,0x0f1b2a20]

def faded_palette(p,steps):
    values=[(p>>s)&255 for s in [24,16,8,0]]
    return sum((v if i==0 else (v-16*steps if v>=16*steps else 15))<<s for i,(v,s) in enumerate(zip(values,[24,16,8,0])))

def luminance(p):
    return max(float(PALETTE[(p>>s)&63,:3].max()) for s in [16,8,0])

def transition_rules(lines,headers):
    path=ROOT/'metadata/regression_scene_keys.json'
    if not path.exists():return []
    normal=json.loads(path.read_text())
    conditions={}
    for line in headers:
        if line.startswith('<condition>'):
            parts=line[11:].split(',');conditions[parts[0]]=parts
    stages=['gameplay']+[f'level{i}' for i in range(2,8)]
    generated=[];added=set()
    for scene,source_keys in normal.items():
        scene=int(scene);stage=stages[scene];hud=HUD_PALETTES[scene]
        source_keys={tuple(k) for k in source_keys}
        for step in range(1,5):
            pal=faded_palette(hud,step);gate=f'fade_hud_{scene}_{step}'
            headers.append(f'<condition>{gate},tileAtPosition,24,208,D9A,{pal:08X},N')
            bright=luminance(pal)/max(1,luminance(hud))
            # Only native HUD-bearing frames select these backgrounds.
            headers.append(f'[{stage}&{gate}]<background>hud.png,{bright:.6f},0,0,11')
            if scene in [0,1,4]:
                name='sky.png' if scene==0 else 'level2_sky.png'
                headers.append(f'[{stage}&{gate}]<background>{name},{bright:.6f},0,0,10')
            for line in lines:
                if '<tile>' not in line:continue
                prefix,body=line.split('<tile>');a=body.split(',');t,p=int(a[1],16),int(a[2],16)
                if p>>24==255 or (t,p) not in source_keys:continue
                names=prefix.strip('[]').split('&') if prefix else []
                if any(n in stages and n!=stage for n in names):continue
                if any(n in ['title_intro','title_final','select','briefing','ending_office','ending_credits'] for n in names):continue
                target=faded_palette(p,step)
                # A fully dark native palette must never resurrect art.
                factor=luminance(target)/max(1,luminance(p))
                new_names=[stage,gate]
                for name in names:
                    if name in stages or name in ['hud','hud3','hud4','hud6','hud7']:continue
                    condition=conditions.get(name)
                    if condition and condition[1] in ['tileNearby','spriteNearby','tileAtPosition','spriteAtPosition']:
                        clone=f'fade_{name}_{step}'
                        if clone not in added:
                            c=condition.copy();c[0]=clone;c[5]=f'{faded_palette(int(c[5],16),step):08X}'
                            headers.append('<condition>'+','.join(c));added.add(clone)
                        new_names.append(clone)
                    else:new_names.append(name)
                a[2]=f'{target:08X}';a[5]=f'{float(a[5])*factor:.6f}'
                generated.append('['+'&'.join(dict.fromkeys(new_names))+']<tile>'+','.join(a))
    return list(dict.fromkeys(generated))
