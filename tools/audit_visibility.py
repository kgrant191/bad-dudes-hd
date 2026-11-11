"""Audit recorded actor cells against selected pack rules, not just key presence."""
import csv,json,re,collections,sys,os
from pathlib import Path
import numpy as np
from PIL import Image
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--rom',required=True,type=Path)
parser.add_argument('--capture-dir',required=True,type=Path)
parser.add_argument('--pack',required=True,type=Path)
parser.add_argument('--output',required=True,type=Path)
args=parser.parse_args()
base=args.capture_dir
states={int(a[0]):(int(a[1]),int(a[2])) for a in csv.reader(open(base/'state.csv'))}
atlas=Image.open(args.pack/'tiles.png').convert('RGBA');conditions={};rules=collections.defaultdict(list);areas={}
for line in (args.pack/'hires.txt').read_text().splitlines():
 if line.startswith('<condition>'):
  a=line[11:].split(',');conditions[a[0]]=a[1:]
 elif '<tile>' in line:
  pre,body=line.split('<tile>');a=body.split(',');t,p=int(a[1],16),int(a[2],16)
  if p>>24!=255:continue
  xy=(int(a[3]),int(a[4]))
  if xy not in areas:areas[xy]=int((np.array(atlas.crop((xy[0],xy[1],xy[0]+32,xy[1]+32)))[:,:,3]>32).sum())
  rules[t,p].append((pre.strip('[]').split('&') if pre else [],areas[xy]))
rom=args.rom.read_bytes();chrrom=rom[16+rom[4]*16384:]
nonempty={t:any(chrrom[t*16:t*16+16]) for t in range(len(chrrom)//16)}
def compare(a,op,b):return {'==':a==b,'!=':a!=b,'<':a<b,'>':a>b,'<=':a<=b,'>=':a>=b}[op]
frames=0;clusters=0;suspects=[]
def process(rows):
 global frames,clusters
 if not rows:return
 f=rows[0][0];scene,hero=states.get(f,(-1,0))
 if not 0<=scene<=6:return
 sprites=[r for r in rows if r[1]==1 and 0<=r[2]<256 and 0<=r[3]<200 and 0x1200<=r[4]<0x1e00 and r[5]!=0xff0f0f0f and nonempty[r[4]]]
 if not sprites:return
 frames+=1;points=collections.defaultdict(list)
 for r in rows:
  if r[1]==1:points[r[2],r[3]].append(r)
 def match(name,row):
  a=conditions.get(name)
  if not a:return False
  typ=a[0];_,_,x,y,t,p,h,v=row
  if typ=='memoryCheckConstant':
   addr=int(a[1],16);value={0x2c0:scene,0x23f:hero}.get(addr,0);mask=int(a[4],16) if len(a)>4 else 255
   return compare(value&mask,a[2],int(a[3],16))
  if typ=='spriteNearby':
   dx,dy=int(a[1])*(-1 if h else 1),int(a[2])*(-1 if v else 1);nt,npal=int(a[3],16),int(a[4],16)
   return any(q[4]==nt and (a[5]=='Y' or q[5]==npal) for q in points[x+dx,y+dy])
  if typ in ['positionCheckY','originPositionCheckY']:return compare(y,a[1],int(a[2]))
  if typ in ['positionCheckX','originPositionCheckX']:return compare(x,a[1],int(a[2]))
  return False
 visible=[]
 for row in sprites:
  area=1
  for names,alpha in rules[row[4],row[5]]:
   if all(match(name,row) for name in names):area=alpha;break
  visible.append(area)
 # Adjacent native cells form a pose. Only flag full multi-cell components,
 # so a transparent corner or an intentional detached effect is not an error.
 index=collections.defaultdict(list)
 for i,r in enumerate(sprites):index[r[2],r[3],r[5]].append(i)
 remaining=set(range(len(sprites)))
 while remaining:
  first=remaining.pop();component=[first];queue=[first]
  while queue:
   i=queue.pop();r=sprites[i]
   for dx in [-8,0,8]:
    for dy in [-8,0,8]:
     for j in index[r[2]+dx,r[3]+dy,r[5]]:
      if j in remaining:remaining.remove(j);component.append(j);queue.append(j)
  if len(component)<6:continue
  clusters+=1
  if not any(visible[i] for i in component):
   suspects.append({'frame':f,'palette':hex(sprites[first][5]),'cells':[[sprites[i][2],sprites[i][3],hex(sprites[i][4])] for i in component]})
old=-1;rows=[]
for row in csv.reader(open(base/'tiles.csv')):
 if len(row)!=8:continue
 r=tuple(map(int,row))
 if r[0]!=old:process(rows);rows=[];old=r[0]
 rows.append(r)
process(rows)
out={'actor_frames':frames,'connected_actor_components':clusters,'fully_transparent_components':suspects,
     'method':'Native on-screen enemy/boss cells, exact tile/palette rule order, local sprite-neighbor and scene/hero conditions; components contain at least six nonempty native cells.'}
args.output.write_text(json.dumps(out,indent=2))
print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in out.items()}))
