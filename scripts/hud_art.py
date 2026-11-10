"""Resolution-independent live HUD glyphs; scores and health remain game-driven."""
from common import *
from PIL import ImageDraw, ImageFont
FONT=str(ROOT/'tools/fonts/DejaVuSansMono-Bold.ttf')
def hud_tile(t):
    im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im)
    if t==0xd80:return im.resize((32,32))
    if 0xd81<=t<=0xda4:
        char='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'[t-0xd81]
        font=ImageFont.truetype(FONT,112);bb=d.textbbox((0,0),char,font=font)
        mask=Image.new('L',(128,128));md=ImageDraw.Draw(mask)
        md.text(((128-(bb[2]-bb[0]))/2-bb[0],6-bb[1]),char,font=font,fill=255)
        # Fit all glyphs within their original 8-pixel cell.
        bb=mask.getbbox();mask=mask.crop(bb).resize((100,104),Image.Resampling.LANCZOS)
        glyph=Image.new('RGBA',(100,104));a=np.zeros((104,100,4),dtype='uint8')
        top=np.array([246,249,255] if char.isdigit() else [248,208,128]);bottom=np.array([167,196,218] if char.isdigit() else [174,123,55])
        for y in range(104):a[y,:,:3]=top+(bottom-top)*y/103
        a[:,:,3]=np.array(mask);im.alpha_composite(Image.fromarray(a),(12,8))
    elif t==0xda7:
        d.rounded_rectangle((18,88,42,112),radius=3,fill=(246,249,255,255))
    elif t in [0xda5,0xda6]:
        for x in ([12,76] if t==0xda5 else [12]):
            d.rounded_rectangle((x,8,x+36,111),radius=7,fill=(36,205,164,255),outline=(141,255,222,255),width=5)
            d.line((x+10,18,x+10,94),fill=(213,255,236,255),width=5)
    return im.resize((32,32),Image.Resampling.LANCZOS)

def panel():
    im=Image.new('RGBA',(1024,960));d=ImageDraw.Draw(im)
    for y in range(800,960):
        c=int(22-(y-800)*.06);d.line((0,y,1023,y),fill=(c,c+7,c+15,255))
    d.line((0,802,1023,802),fill=(201,153,73,255),width=3)
    d.line((0,807,1023,807),fill=(61,74,87,255),width=2)
    im.save(ROOT/'pack/hud.png')
