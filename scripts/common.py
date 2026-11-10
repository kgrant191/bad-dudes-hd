from pathlib import Path
import numpy as np,re,ctypes,os
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
rom_path=Path(os.environ.get('BAD_DUDES_ROM',str(ROOT.parent/'work/Bad Dudes (USA).nes')))
rom_data=rom_path.read_bytes()
if rom_data[:4]!=b'NES\x1a':raise ValueError('Supply the original NES ROM via BAD_DUDES_ROM')
chr_offset=16+(512 if rom_data[6]&4 else 0)+rom_data[4]*16384
ROM=rom_data[chr_offset:]
PALETTE=np.array([[int(x,16)>>16&255,int(x,16)>>8&255,int(x,16)&255,255] for x in re.findall('0x([A-Fa-f0-9]+)',(ROOT/'scripts/palette.inc').read_text())],dtype='uint8')
lib=ctypes.CDLL(os.environ.get('BAD_DUDES_XBRZ_LIBRARY',str(ROOT.parent/'tools/scale.so')))
lib.scale4.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
def pixels(t):
 a=np.unpackbits(np.frombuffer(ROM[t*16:t*16+16],dtype='uint8')).reshape(16,8);return a[:8]+a[8:]*2

def tile(t,p):
 ix=pixels(t);cols=np.array([(p>>24)&255,(p>>16)&255,(p>>8)&255,p&255]);out=PALETTE[cols&63][ix].copy()
 if cols[0]==255:out[ix==0]=0
 return Image.fromarray(out)

def scale(im):
 a=np.array(im.convert('RGBA'))[:,:,[2,1,0,3]].copy();h,w=a.shape[:2];b=np.zeros((h*4,w*4,4),dtype='uint8');lib.scale4(a.ctypes.data,b.ctypes.data,w,h);return Image.fromarray(b[:,:,[2,1,0,3]])

def entries(n):return [tuple(map(int,l.split(','))) for l in (ROOT/f'metadata/{n:05d}.tiles').read_text().splitlines()]
def render(n,layer):
 out=Image.new('RGBA',(256,240))
 for l,x,y,t,p,h,v in entries(n):
  if l!=layer:continue
  im=tile(t,p)
  if h:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  out.alpha_composite(im,(x,y))
 return out
if __name__=='__main__':
 for n in [3840,4320,5760]:render(n,0).save(ROOT/f'../work/bg_{n}.png')
