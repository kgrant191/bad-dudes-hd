"""Resolution-independent live HUD glyphs; scores and health remain game-driven."""
from common import *
from PIL import ImageDraw, ImageFont
FONT=str(ROOT/'tools/fonts/DejaVuSansMono-Bold.ttf')
def hud_tile(t, gold=False):
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
        numeric=char.isdigit() and not gold
        top=np.array([246,249,255] if numeric else [248,208,128]);bottom=np.array([167,196,218] if numeric else [174,123,55])
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


def message_tile(t):
    """Full 8x16 stage lettering, split across the native two sprite rows."""
    from PIL import ImageFilter
    base=t&~1
    chars={0x160c:'P',0x160e:'L',0x1610:'A',0x1612:'Y',0x1614:'E',0x1616:'R',
           0x161a:'1',0x161c:'2',0x161e:'N',0x1620:'X',0x1622:'T',0x1624:'S',
           0x1626:'G',0x1628:'C',0x162a:'3',0x162c:'4',0x162e:'5',0x1630:'6',0x1632:'O',0x1634:'7'}
    char=chars.get(base)
    if char is None:return scale(tile(t,0xff001020))
    mask=Image.new('L',(160,256));d=ImageDraw.Draw(mask)
    d.text((10,0),char,font=ImageFont.truetype(FONT,180),fill=255)
    mask=mask.crop(mask.getbbox()).resize((100,192),Image.Resampling.LANCZOS)
    m=Image.new('L',(128,256));m.paste(mask,(14,32))
    outline=m.filter(ImageFilter.MaxFilter(17))
    im=Image.new('RGBA',(128,256),(4,9,14,0));im.putalpha(outline)
    a=np.zeros((256,128,4),dtype='uint8')
    for y in range(256):a[y,:,:3]=[255,247-int(y*.13),207-int(y*.35)]
    a[:,:,3]=np.array(m);im.alpha_composite(Image.fromarray(a))
    im=im.resize((32,64),Image.Resampling.LANCZOS)
    return im.crop((0,32*(t&1),32,32*(1+(t&1))))
