from pathlib import Path
import sys, math, shutil
BASE=Path(__file__).parent
sys.path.insert(0,str(BASE/'.tools'))
from PIL import Image, ImageDraw, ImageFont
ASSETS=BASE/'dist'/'assets'
KIT=BASE.parent/'Seferihisar-Taksi-724-Teslim'
ASSETS.mkdir(parents=True,exist_ok=True)
KIT.mkdir(exist_ok=True)
YELLOW='#f4d348'; DARK='#09131c'; WHITE='#f3f2e9'
FONT=Path('C:/Windows/Fonts')
def font(size,bold=False):
 return ImageFont.truetype(str(FONT/('arialbd.ttf' if bold else 'arial.ttf')),size)
def text(d,xy,s,size,fill=WHITE,bold=False):d.text(xy,s,font=font(size,bold),fill=fill)
mark='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="25" fill="#f4d348"/><path d="M67 25H42c-12 0-19 7-19 17s8 16 19 16h15c6 0 9 3 9 7s-3 7-9 7H31" fill="none" stroke="#09131c" stroke-width="10" stroke-linecap="square"/><path d="M61 18h20v20M80 19 58 41" fill="none" stroke="#09131c" stroke-width="7"/><path d="M22 83h8m6 0h8m6 0h8m6 0h8" stroke="#09131c" stroke-width="4"/></svg>'''
(ASSETS/'logo-mark.svg').write_text(mark,encoding='utf-8')
logo='''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="280" viewBox="0 0 1000 280"><rect width="1000" height="280" rx="30" fill="#09131c"/><svg x="45" y="45" width="190" height="190" viewBox="0 0 100 100">'''+mark.split('>',1)[1].rsplit('</svg>',1)[0]+'''</svg><text x="275" y="112" font-family="Arial,sans-serif" font-weight="bold" font-size="43" fill="#f3f2e9" letter-spacing="3">SEFERİHİSAR</text><text x="275" y="196" font-family="Arial,sans-serif" font-weight="bold" font-size="85" fill="#f3f2e9">TAKSİ</text><rect x="582" y="139" width="180" height="64" rx="32" fill="#f4d348"/><text x="611" y="184" font-family="Arial,sans-serif" font-weight="bold" font-size="43" fill="#09131c">7/24</text></svg>'''
(KIT/'logo.svg').write_text(logo,encoding='utf-8')
shutil.copy2(ASSETS/'logo-mark.svg',KIT/'logo-simge.svg')
def raster_mark(size):
 im=Image.new('RGB',(512,512),DARK);d=ImageDraw.Draw(im)
 d.rounded_rectangle((20,20,492,492),radius=120,fill=YELLOW)
 d.line([(330,141),(230,141),(166,161),(146,206),(170,245),(283,265),(328,302),(315,351),(265,370),(155,370)],fill=DARK,width=44,joint='curve')
 d.line([(300,96),(416,96),(416,209)],fill=DARK,width=33)
 d.line([(411,101),(300,212)],fill=DARK,width=33)
 for x in range(115,385,56):d.rectangle((x,424,x+29,435),fill=DARK)
 return im.resize((size,size),Image.Resampling.LANCZOS)
for size in [192,512]:raster_mark(size).save(ASSETS/f'icon-{size}.png')
raster_mark(512).save(KIT/'logo-profil-512.png')
im=Image.new('RGB',(1600,450),DARK);d=ImageDraw.Draw(im);im.paste(raster_mark(270),(65,90))
text(d,(400,92),'SEFERİHİSAR',71,bold=True);text(d,(396,174),'TAKSİ',132,bold=True)
d.rounded_rectangle((810,202,1080,300),radius=45,fill=YELLOW);text(d,(846,212),'7/24',75,DARK,True)
im.save(KIT/'logo-yatay.png')
social=Image.new('RGB',(1200,630),DARK);d=ImageDraw.Draw(social)
for r in [240,330,420]:d.ellipse((920-r,295-r,920+r,295+r),outline='#26333b',width=2)
social.paste(raster_mark(100),(70,55));text(d,(198,70),'SEFERİHİSAR TAKSİ 7/24',30,bold=True)
text(d,(70,220),'Şehir sakin.',78,bold=True);text(d,(70,310),'Senin yolun açık.',78,YELLOW,True)
d.line((70,463,1130,463),fill='#34414a',width=2)
text(d,(70,505),'0551 218 22 44',45,YELLOW,True);text(d,(700,520),'MERKEZ · SAHİL · HAVALİMANI',20)
social.save(ASSETS/'social.png',optimize=True);social.save(KIT/'sosyal-paylasim-1200x630.png')
# Short, one-shot animation: avoids perpetual flashing and respects reduced motion via <picture>.
frames=[]
for i in range(32):
 im=Image.new('RGB',(960,180),DARK);d=ImageDraw.Draw(im)
 d.rounded_rectangle((1,1,958,178),radius=22,outline='#3b4341',width=2)
 d.rounded_rectangle((18,18,145,162),radius=16,fill=YELLOW)
 text(d,(39,43),'7/24',37,DARK,True);text(d,(40,96),'TAKSİ',23,DARK,True)
 text(d,(171,25),'SEFERİHİSAR’DA TAKSİ ÇAĞIRMAK',29,bold=True)
 text(d,(171,64),'İÇİN TIKLAYINIZ',33,YELLOW,True)
 text(d,(174,119),'0551 218 22 44  ·  GECE / GÜNDÜZ',22)
 shift=int(10*math.sin(i/31*math.pi*2)) if i<28 else 0
 d.rounded_rectangle((837,35,930,145),radius=18,fill=YELLOW)
 # Draw the arrow geometrically: Arial on some Windows systems lacks this glyph.
 d.line([(859+shift,119),(905+shift,69)],fill=DARK,width=8)
 d.line([(865+shift,69),(905+shift,69),(905+shift,109)],fill=DARK,width=8)
 x=173+int(616*min(1,i/26));d.rounded_rectangle((173,158,x+1,162),radius=2,fill=YELLOW)
 frames.append(im)
frames[0].save(ASSETS/'taksi-cagir.png',optimize=True)
palette=frames[0].quantize(colors=48)
indexed=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
indexed[0].save(ASSETS/'taksi-cagir.gif',save_all=True,append_images=indexed[1:],duration=75,disposal=1,optimize=True)
shutil.copy2(ASSETS/'taksi-cagir.gif',KIT/'mobil-taksi-cagir-960x180.gif')
shutil.copy2(ASSETS/'taksi-cagir.png',KIT/'mobil-taksi-cagir-sabit.png')
print('Logo, PNG sosyal görsel, uygulama ikonları ve 960x180 animasyonlu GIF oluşturuldu.')
