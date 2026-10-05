from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math
O=Path("diagrams/electrons"); O.mkdir(parents=True,exist_ok=True)
W,H=1800,1000
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F=lambda n:ImageFont.truetype(FONT,n)
B=lambda n:ImageFont.truetype(BOLD,n)
class ContrastDraw:
    """Pillow drawing wrapper that keeps dark text readable on light and dark themes."""
    def __init__(self, draw):
        self._draw = draw

    def text(self, xy, text, *args, **kwargs):
        kwargs.setdefault("stroke_width", 6)
        kwargs.setdefault("stroke_fill", (248, 248, 248, 245))
        return self._draw.text(xy, text, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._draw, name)

def base(t):
    im=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ContrastDraw(ImageDraw.Draw(im))
    d.text((70,45),t,font=B(52),fill=(20,25,35,255))
    return im,d
def save(im,n): im.save(O/n,"PNG",optimize=True)

im,d=base("Electron Energy Levels")
for i,n in enumerate([1,2,3,4],1):
    y=820-(i-1)*170
    d.line((350,y,1450,y),fill=(35,90,180,255),width=8)
    d.text((150,y-28),f"n = {n}",font=B(42),fill=(20,25,35,255))
d.ellipse((875,830,925,880),fill=(210,55,55,255))
d.text((780,900),"nucleus",font=F(34),fill=(20,25,35,255))
save(im,"electron-energy-levels.png")

im,d=base("s and p Orbitals")
cx,cy=360,560
d.ellipse((cx-150,cy-150,cx+150,cy+150),fill=(75,140,220,180),outline=(30,80,150,255),width=5)
d.text((cx-20,760),"s",font=B(46),fill=(20,25,35,255))
for cx,cy,label,vertical in [(900,560,"pₓ",False),(1180,560,"pᵧ",True),(1460,560,"p_z",True)]:
    if vertical:
        d.ellipse((cx-70,cy-210,cx+70,cy),fill=(75,170,90,180),outline=(35,110,55,255),width=5)
        d.ellipse((cx-70,cy,cx+70,cy+210),fill=(75,170,90,180),outline=(35,110,55,255),width=5)
    else:
        d.ellipse((cx-210,cy-70,cx,cy+70),fill=(75,170,90,180),outline=(35,110,55,255),width=5)
        d.ellipse((cx,cy-70,cx+210,cy+70),fill=(75,170,90,180),outline=(35,110,55,255),width=5)
    d.ellipse((cx-8,cy-8,cx+8,cy+8),fill=(25,25,25,255))
    d.text((cx-35,820),label,font=B(42),fill=(20,25,35,255))
save(im,"s-and-p-orbitals.png")

im,d=base("Periodic Table Blocks")
x0,y0,cell=180,270,42
for r in range(7):
    for c in range(2):
        d.rectangle((x0+c*cell,y0+r*cell,x0+(c+1)*cell,y0+(r+1)*cell),outline=(210,70,70,255),width=3)
d.text((x0,y0-55),"s-block",font=B(40),fill=(190,45,45,255))
xd=500
for r in range(4):
    for c in range(10):
        d.rectangle((xd+c*cell,y0+2*cell+r*cell,xd+(c+1)*cell,y0+2*cell+(r+1)*cell),outline=(45,105,200,255),width=3)
d.text((xd,y0+2*cell-55),"d-block",font=B(40),fill=(35,85,180,255))
xp=960
for r in range(6):
    for c in range(6):
        d.rectangle((xp+c*cell,y0+r*cell,xp+(c+1)*cell,y0+(r+1)*cell),outline=(60,150,75,255),width=3)
d.text((xp,y0-55),"p-block",font=B(40),fill=(45,130,60,255))
xf,yf=650,700
for r in range(2):
    for c in range(14):
        d.rectangle((xf+c*cell,yf+r*cell,xf+(c+1)*cell,yf+(r+1)*cell),outline=(125,75,190,255),width=3)
d.text((xf,yf-55),"f-block",font=B(40),fill=(105,60,170,255))
for y,t in [(350,"s: Groups 1–2"),(420,"p: Groups 13–18"),(490,"d: transition metals"),(560,"f: lanthanides + actinides")]:
    d.text((1250,y),t,font=F(36),fill=(20,25,35,255))
save(im,"periodic-table-blocks.png")

im,d=base("Aufbau / Madelung Filling Order")
levels=["1s","2s","2p","3s","3p","4s","3d","4p","5s","4d","5p","6s","4f","5d","6p","7s","5f","6d","7p"]
C={}
for i,s in enumerate(levels):
    col,row=i//6,i%6
    x,y=170+col*500,170+row*110
    C[s]=(x,y)
    d.rounded_rectangle((x,y,x+150,y+70),12,fill=(245,245,250,255),outline=(60,90,150,255),width=4)
    d.text((x+48,y+13),s,font=B(34),fill=(20,25,35,255))
for a,b in zip(levels,levels[1:]):
    x,y=C[a]; xx,yy=C[b]
    d.line((x+150,y+35,xx,yy+35),fill=(220,80,50,255),width=5)
d.text((1050,850),"1s → 2s → 2p → 3s → 3p → 4s → 3d → 4p → …",font=F(34),fill=(20,25,35,255))
save(im,"aufbau-madelung.png")

im,d=base("Orbital Notation")
els=[("C","1s² 2s² 2p²",["↑↓","↑","↑"]),("N","1s² 2s² 2p³",["↑","↑","↑"]),("O","1s² 2s² 2p⁴",["↑↓","↑","↑"]),("F","1s² 2s² 2p⁵",["↑↓","↑↓","↑"]),("Ne","1s² 2s² 2p⁶",["↑↓","↑↓","↑↓"])]
for j,(el,conf,boxes) in enumerate(els):
    x=80+j*340
    d.text((x,180),el,font=B(42),fill=(20,25,35,255))
    d.text((x-15,235),conf,font=F(28),fill=(20,25,35,255))
    d.text((x,330),"2p",font=B(30),fill=(20,25,35,255))
    for k,bx in enumerate(boxes):
        xx=x+k*85
        d.rectangle((xx,390,xx+65,455),outline=(35,75,130,255),width=4)
        d.text((xx+18,395),bx,font=B(30),fill=(20,25,35,255))
d.text((100,720),"Each orbital holds at most 2 electrons; Hund’s rule fills degenerate orbitals singly before pairing.",font=F(31),fill=(20,25,35,255))
save(im,"orbital-notation.png")

im,d=base("Lewis Dot Notation")
pos=[(180,40),(220,90),(180,145),(140,90),(140,40),(220,40),(220,145),(140,145)]
for i,n in enumerate(range(1,9)):
    x,y=140+(i%4)*410,220+(i//4)*350
    d.text((x+105,y-20),f"{n} valence e⁻",font=B(32),fill=(20,25,35,255))
    d.text((x+180,y+70),"X",font=B(62),fill=(20,25,35,255))
    for k in range(n):
        px,py=pos[k]
        d.ellipse((x+px-7,y+py-7,x+px+7,y+py+7),fill=(30,30,30,255))
save(im,"lewis-dot-notation.png")

im,d=base("Period 2 Lewis Dot Notation")
els=[("Li",1),("Be",2),("B",3),("C",4),("N",5),("O",6),("F",7),("Ne",8)]
for i,(el,n) in enumerate(els):
    x,y=110+i*210,300
    d.text((x+45,y),el,font=B(42),fill=(20,25,35,255))
    for px,py in pos[:n]:
        d.ellipse((x+px-6,y+py-6,x+px+6,y+py+6),fill=(25,25,25,255))
d.text((520,650),"Valence electrons increase from 1 → 8 across Period 2.",font=F(36),fill=(20,25,35,255))
save(im,"period-2-lewis-dots.png")

im,d=base("Electromagnetic Wave")
x0,x1,mid,amp=150,1650,560,180
pts=[(x0+(x1-x0)*i/600,mid-amp*math.sin(2*math.pi*3*i/600)) for i in range(601)]
d.line(pts,fill=(55,95,190,255),width=8)
d.line((x0,mid,x1,mid),fill=(80,80,80,180),width=3)
d.text((120,260),"amplitude",font=B(34),fill=(20,25,35,255))
d.line((100,mid-amp,100,mid),fill=(220,80,50,255),width=5)
d.line((250,820,650,820),fill=(220,80,50,255),width=5)
d.text((375,840),"wavelength λ",font=F(32),fill=(20,25,35,255))
save(im,"electromagnetic-wave.png")

im,d=base("Wavelength and Frequency")
for label,cyc,y in [("low frequency / long wavelength",2,350),("high frequency / short wavelength",8,700)]:
    pts=[(150+1450*i/500,y-90*math.sin(2*math.pi*cyc*i/500)) for i in range(501)]
    d.line(pts,fill=(55,95,190,255),width=7)
    d.text((160,y-170),label,font=B(34),fill=(20,25,35,255))
d.text((540,880),"At constant speed:  c = νλ",font=B(42),fill=(20,25,35,255))
save(im,"wavelength-frequency.png")

im,d=base("Electron Transitions")
ys={1:800,2:610,3:420,4:230}
for n,y in ys.items():
    d.line((300,y,1250,y),fill=(50,75,120,255),width=6)
    d.text((180,y-25),f"n = {n}",font=B(36),fill=(20,25,35,255))
d.line((700,790,700,240),fill=(50,130,210,255),width=8)
d.text((760,430),"absorption",font=B(36),fill=(40,105,180,255))
d.line((1000,240,1000,790),fill=(225,90,55,255),width=8)
d.text((1060,500),"emission",font=B(36),fill=(190,65,40,255))
d.text((520,880),"ΔE = hν",font=B(42),fill=(20,25,35,255))
save(im,"electron-transitions.png")

im,d=base("Hydrogen Emission Spectrum — Balmer Series")
d.text((100,180),"visible region",font=B(34),fill=(20,25,35,255))
d.rectangle((100,300,1700,500),fill=(230,230,240,255))
for nm,c in [(410,(130,60,190,255)),(434,(50,140,220,255)),(486,(30,170,210,255)),(656,(190,40,50,255))]:
    x=100+(nm-400)/(700-400)*1600
    d.rectangle((x-6,300,x+6,500),fill=c)
    d.text((x-45,540),f"{nm} nm",font=B(28),fill=(20,25,35,255))
d.text((100,700),"Balmer lines correspond to transitions ending at n = 2.",font=F(36),fill=(20,25,35,255))
save(im,"hydrogen-emission-spectrum.png")

im,d=base("Absorption Spectrum")
seg=[(210,60,70),(235,80,55),(250,170,45),(220,205,50),(70,160,80),(60,120,200),(100,80,180)]
x=100
d.text((100,200),"continuous spectrum",font=B(34),fill=(20,25,35,255))
for c in seg:
    d.rectangle((x,280,x+230,480),fill=(*c,255)); x+=230
d.text((100,570),"absorption spectrum",font=B(34),fill=(20,25,35,255))
x=100
for c in seg:
    d.rectangle((x,650,x+230,850),fill=(*c,255)); x+=230
for xx in [520,875,1330]:
    d.rectangle((xx,650,xx+12,850),fill=(20,20,30,255))
d.text((100,900),"Dark lines mark wavelengths absorbed by the material.",font=F(30),fill=(20,25,35,255))
save(im,"absorption-spectrum.png")
