from common import *
for n in [480,600,720]:
 out=Image.new('RGBA',(256,240))
 for l,x,y,t,p,h,v in entries(n):
  if l==0:
   if not (0<=t//256<=1 and t%256<128 and t%256 not in [0x2c,0x3c,0x2d,0x3d,0x2e,0x3e] and 96<=x<160 and 120<=y<208):continue
  else:
   if not (t//256==0x1e and 80<=x<180 and y>=112):continue
  im=tile(t,p)
  if h:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  out.alpha_composite(im,(x,y))
 out.crop((72,104,184,216)).resize((448,448),Image.Resampling.NEAREST).save(ROOT/f'../work/title_men_{n}.png')
