#!/usr/bin/env python3
"""Generate simplified, editable SVG diagrams for Unit 03: Covalent Bonding.

All artwork is authored from SVG vector primitives; no raster/image generation is used.
Run from the repository root: python scripts/generate_covalent_diagrams.py
"""
from pathlib import Path
from html import escape

OUT = Path("diagrams/covalent")
OUT.mkdir(parents=True, exist_ok=True)
INK = "#1f2937"
MUTED = "#64748b"
BLUE = "#2563eb"
RED = "#dc2626"
GREEN = "#15803d"
PURPLE = "#7c3aed"
PALE = "#f8fafc"

def text(x, y, s, size=22, weight=400, fill=INK, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(str(s))}</text>'

def line(x1, y1, x2, y2, width=4, color=INK, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{extra}/>'

def circle(x, y, r, label="", fill="#ffffff", stroke=INK, size=24):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>' + (text(x,y+size*.34,label,size,700) if label else "")

def frame(title, body, width=900, height=360, subtitle=""):
    head = text(width/2, 38, title, 26, 700)
    if subtitle:
        head += text(width/2, 66, subtitle, 15, 400, MUTED)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<title>{escape(title)}</title><rect width="100%" height="100%" rx="18" fill="#ffffff"/>
{head}{body}</svg>'''

def save(name, content):
    (OUT / name).write_text(content + "\n", encoding="utf-8")

# Methane: compare a simplified ball-and-stick model with a Lewis-style sketch.
b = ""
for x,y in [(245,155),(145,220),(345,220),(195,95),(295,95)]:
    b += line(245,175,x,y,5,"#94a3b8")
b += circle(245,175,34,"C","#dbeafe",BLUE,26)
for x,y in [(245,110),(110,240),(380,240),(170,70),(320,70)]:
    b += circle(x,y,23,"H","#f8fafc","#94a3b8",20)
b += text(245,292,"Ball-and-stick",20,700)
# Lewis sketch: four shared pairs around carbon
b += text(650,112,"H",25,700)+text(650,260,"H",25,700)+text(570,186,"H",25,700)+text(730,186,"H",25,700)
b += text(650,190,"C",30,700)
for x1,y1,x2,y2 in [(650,128,650,150),(650,225,650,244),(595,184,620,184),(680,184,705,184)]:
    b += line(x1,y1,x2,y2,3,BLUE)
b += text(650,292,"Lewis bond sketch",20,700)
save("methane-models.svg", frame("Methane, CH₄: two models", b, subtitle="Models emphasize different features; neither is the molecule itself."))

# Lewis structures for F2, O2, N2: show bond order and valence electron pairs.
b = ""
molecules = [
    (155,"F₂","F","F",1,"Each F has 3 lone pairs"),
    (450,"O₂","O","O",2,"Each O has 2 lone pairs"),
    (745,"N₂","N","N",3,"Each N has 1 lone pair"),
]
for x, formula, a1, a2, order, note in molecules:
    b += text(x,105,formula,24,700)
    b += text(x-54,175,a1,31,700)+text(x+54,175,a2,31,700)
    for k in range(order):
        yy=166+(k-(order-1)/2)*9
        b += line(x-28,yy,x+28,yy,2.8,BLUE)
    if order == 1:
        pairs=[(x-76,143),(x-76,205),(x+76,143),(x+76,205),(x-54,130),(x+54,130)]
    elif order == 2:
        pairs=[(x-76,145),(x-76,199),(x+76,145),(x+76,199)]
    else:
        pairs=[(x-54,132),(x+54,132)]
    for px,py in pairs:
        b += circle(px,py,2.8,"",BLUE,BLUE)
        b += circle(px+8,py,2.8,"",BLUE,BLUE)
    b += text(x,250,["single bond","double bond","triple bond"][order-1],18,700)
    b += text(x,282,note,14,400,MUTED)
save("diatomic-lewis.svg", frame("Lewis bonding in F₂, O₂, and N₂", b, height=320, subtitle="Shared electron pairs are shown as blue bond lines; lone pairs are blue dots."))

# CH3Cl: central carbon with three H and one Cl, plus chlorine lone pairs.
b = text(450,155,"C",32,700)
for label,x,y in [("H",450,100),("H",365,170),("H",450,225),("Cl",545,170)]:
    b += line(450,170,x,y,3,BLUE)
    b += text(x,y+8,label,27,700, GREEN if label=="Cl" else INK)
for x,y in [(575,143),(588,143),(575,165),(588,165),(575,187),(588,187)]:
    b += circle(x,y,3,"",BLUE,BLUE)
b += text(450,275,"14 valence electrons total",18,700)
b += text(450,302,"4 C + 3 H + 7 Cl",16,400,MUTED)
save("lewis-ch3cl.svg", frame("Worked Lewis-structure sketch: CH₃Cl", b, height=335, subtitle="Carbon forms four single bonds; chlorine has three lone pairs."))

# Bond order comparison
b = ""
for x, label, order, length, energy in [(175,"C—C",1,"154 pm","346 kJ/mol"),(450,"C=C",2,"134 pm","612 kJ/mol"),(725,"C≡C",3,"120 pm","835 kJ/mol")]:
    b += text(x,105,label,30,700)
    for k in range(order):
        b += line(x-52,155+(k-(order-1)/2)*10,x+52,155+(k-(order-1)/2)*10,3,BLUE)
    b += text(x,215,"Length: "+length,18,700)
    b += text(x,247,"Energy: "+energy,18,700)
b += text(450,300,"Higher bond order → shorter bond and greater bond energy (in this comparison)",16,400,MUTED)
save("bond-order-length-energy.svg", frame("Bond order, length, and dissociation energy", b, height=330))

# Electronegativity trends
b = ""
b += '<rect x="245" y="110" width="400" height="150" rx="10" fill="#eff6ff" stroke="#93c5fd" stroke-width="2"/>'
for i in range(5):
    for j in range(3):
        b += f'<rect x="{270+i*72}" y="{130+j*37}" width="55" height="26" rx="3" fill="#dbeafe" stroke="#93c5fd"/>'
b += line(300,285,610,285,4,GREEN)+f'<polygon points="610,285 594,276 594,294" fill="{GREEN}"/>'
b += text(455,315,"Across a period: electronegativity generally increases →",17,700,GREEN)
b += line(680,230,680,125,4,PURPLE)+f'<polygon points="680,125 671,141 689,141" fill="{PURPLE}"/>'
b += text(760,166,"Down a group:",16,700,PURPLE)+text(760,190,"generally",15,400,PURPLE)+text(760,211,"decreases ↓",16,700,PURPLE)
b += text(450,95,"Schematic periodic-table trend",18,700)
save("electronegativity-trends.svg", frame("Periodic trend in electronegativity", b, height=350, subtitle="General trends shown in the slides; individual elements can vary."))

# Polar bond: unequal sharing, delta charges, and dipole arrow.
b = circle(300,170,43,"H","#f8fafc","#64748b",30)
b += circle(570,170,49,"Cl","#dcfce7",GREEN,27)
b += line(350,170,515,170,3,"#94a3b8")
b += text(365,145,"shared pair",15,400,MUTED)
b += text(300,112,"δ+",20,700,RED)+text(570,105,"δ−",20,700,BLUE)
b += line(370,225,505,225,4,BLUE)+f'<polygon points="505,225 488,215 488,235" fill="{BLUE}"/>'
b += text(438,258,"bond dipole points toward the more electronegative atom",16,400)
save("polar-covalent-bond.svg", frame("Polar covalent bond: H—Cl", b, height=310, subtitle="The shared electrons are attracted more strongly toward chlorine."))

# Coordinate covalent formation of ammonium.
b = text(225,140,"NH₃",34,700)+text(450,140,"+",26,700)+text(565,140,"H⁺",34,700)
b += line(315,150,385,150,3,INK)+f'<polygon points="385,150 371,142 371,158" fill="{INK}"/>'
b += text(450,195,"lone pair donated by N",17,400,MUTED)
b += line(625,150,695,150,3,INK)+f'<polygon points="695,150 681,142 681,158" fill="{INK}"/>'
b += text(770,140,"NH₄⁺",31,700)
b += text(450,245,"Both electrons in the new N—H bond come from nitrogen.",18,700)
save("coordinate-covalent-bond.svg", frame("Coordinate covalent bond: ammonium", b, height=290, subtitle="A simplified formation sketch based on the slide's explanation."))

# Ozone resonance structures
b = ""
for x, labels in [(230,("O","O","O")),(670,("O","O","O"))]:
    b += text(x-75,160,labels[0],31,700)+text(x,160,labels[1],31,700)+text(x+75,160,labels[2],31,700)
b += line(165,145,195,145,3,BLUE)+line(165,153,195,153,3,BLUE)+line(265,149,295,149,3,INK)
b += line(605,149,635,149,3,INK)+line(705,145,735,145,3,BLUE)+line(705,153,735,153,3,BLUE)
b += text(230,205,"O=O—O",18,700)+text(670,205,"O—O=O",18,700)
b += text(450,158,"↔",36,700,PURPLE)
b += text(450,255,"The actual structure is described as a resonance hybrid—not as rapid switching.",17,400,MUTED)
save("ozone-resonance.svg", frame("Resonance in ozone, O₃", b, height=300, subtitle="Two valid Lewis contributors differ in the placement of the double bond."))

# Benzene resonance: two hexagons, alternating bonds and ring representation.
def hexagon(cx,cy,r,offset=0):
    pts=[]
    import math
    for i in range(6):
        a=math.radians(60*i-30+offset)
        pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    s=""
    for i in range(6):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%6]
        s += line(round(x1,1),round(y1,1),round(x2,1),round(y2,1),3,INK)
        if i%2==0:
            mx=(x1+x2)/2; my=(y1+y2)/2
            s += line(round(cx+(mx-cx)*.72),round(cy+(my-cy)*.72),round(cx+(mx-cx)*.9),round(cy+(my-cy)*.9),2.5,BLUE)
    return s
b = hexagon(240,165,75)+text(240,270,"alternating bonds",17,700)
b += text(450,175,"↔",36,700,PURPLE)
b += '<polygon points="590,105 645,137 645,193 590,225 535,193 535,137" fill="none" stroke="#1f2937" stroke-width="3"/>'
b += '<circle cx="590" cy="165" r="38" fill="none" stroke="#2563eb" stroke-width="3"/>'
b += text(590,270,"ring shorthand",17,700)
save("benzene-resonance.svg", frame("Resonance in benzene, C₆H₆", b, height=310, subtitle="The ring shorthand represents delocalized inner electrons."))

# VSEPR geometry gallery: all major atom arrangements shown in the slide tables.
b = ""
import math
def atom(x,y,label="",fill="#dbeafe"):
    return circle(x,y,10,label,fill,BLUE,12)
def bond(x1,y1,x2,y2):
    return line(x1,y1,x2,y2,2.5,"#94a3b8")
def geometry(cx,cy,kind,title):
    if kind == "linear":
        pts=[(cx-43,cy),(cx+43,cy)]
    elif kind == "trigonal planar":
        pts=[(cx-35,cy+22),(cx+35,cy+22),(cx,cy-40)]
    elif kind == "bent":
        pts=[(cx-32,cy+23),(cx+32,cy+23)]
    elif kind == "tetrahedral":
        pts=[(cx-35,cy+20),(cx+35,cy+20),(cx-18,cy-35),(cx+18,cy-35)]
    elif kind == "trigonal pyramidal":
        pts=[(cx-35,cy+20),(cx+35,cy+20),(cx,cy-38)]
    elif kind == "trigonal bipyramidal":
        pts=[(cx-36,cy+15),(cx+36,cy+15),(cx,cy-25),(cx,cy-48),(cx,cy+48)]
    elif kind == "seesaw":
        pts=[(cx-40,cy),(cx+40,cy),(cx-15,cy-35),(cx+15,cy+35)]
    elif kind == "T-shaped":
        pts=[(cx,cy-43),(cx,cy+43),(cx+38,cy)]
    elif kind == "octahedral":
        pts=[(cx-42,cy),(cx+42,cy),(cx,cy-42),(cx,cy+42),(cx-28,cy-28),(cx+28,cy+28)]
    elif kind == "square pyramidal":
        pts=[(cx-28,cy-22),(cx+28,cy-22),(cx-28,cy+22),(cx+28,cy+22),(cx,cy-48)]
    elif kind == "square planar":
        pts=[(cx-30,cy-30),(cx+30,cy-30),(cx-30,cy+30),(cx+30,cy+30)]
    elif kind in ("pentagonal bipyramidal","pentagonal pyramidal"):
        pts=[]
        radius=39
        count=5
        for i in range(count):
            a=math.radians(72*i-90)
            pts.append((cx+radius*math.cos(a),cy+radius*math.sin(a)))
        if kind == "pentagonal bipyramidal":
            pts.extend([(cx,cy-50),(cx,cy+50)])
        else:
            pts.append((cx,cy-50))
    s=""
    for x,y in pts:
        s+=bond(cx,cy,x,y)
    s+=atom(cx,cy,"A","#bfdbfe")
    for x,y in pts:
        s+=atom(x,y,"X")
    s+=text(cx,cy+70,title,14,700)
    return s
items=[
 (125,135,"linear","Linear"),
 (375,135,"trigonal planar","Trigonal planar"),
 (625,135,"bent","Bent"),
 (875,135,"tetrahedral","Tetrahedral"),
 (125,315,"trigonal pyramidal","Trigonal pyramidal"),
 (375,315,"trigonal bipyramidal","Trigonal bipyramidal"),
 (625,315,"seesaw","Seesaw"),
 (875,315,"T-shaped","T-shaped"),
 (125,495,"octahedral","Octahedral"),
 (375,495,"square pyramidal","Square pyramidal"),
 (625,495,"square planar","Square planar"),
 (875,495,"pentagonal bipyramidal","Pentagonal bipyramidal"),
 (500,655,"pentagonal pyramidal","Pentagonal pyramidal")
]
for cx,cy,k,t in items:
    b+=geometry(cx,cy,k,t)
save("vsepr-geometries.svg", frame("VSEPR: molecular geometries in the slide tables", b, width=1000, height=750, subtitle="Simplified atom-only sketches; lone pairs and perspective depth are omitted."))

# Atomic-radius trends: smaller across a period, larger down a group.
b = text(450,100,"Across a period",20,700)
for i,r in enumerate([31,27,23,19,15]):
    x=280+i*78
    b+=circle(x,160,r,"", "#dbeafe", BLUE)
b+=line(245,215,650,215,3,GREEN)+f'<polygon points="650,215 634,207 634,223" fill="{GREEN}"/>'
b+=text(450,245,"Atomic radius generally decreases →",16,700,GREEN)
b+=text(450,310,"Down a group",20,700)
for i,r in enumerate([16,22,28,34]):
    y=355+i*55
    b+=circle(355,y,r,"", "#dbeafe", BLUE)
b+=line(430,345,430,540,3,PURPLE)+f'<polygon points="430,540 422,524 438,524" fill="{PURPLE}"/>'
b+=text(570,440,"Atomic radius generally",16,700,PURPLE)+text(570,465,"increases ↓",16,700,PURPLE)
save("atomic-radius-trends.svg", frame("Atomic radius: periodic trends", b, height=590, subtitle="Schematic trend diagrams, not measured atom sizes."))

# Inverse-square idea: increasing distance weakens attraction.
b = circle(220,180,34,"+","#fee2e2",RED,28)
b+=text(220,235,"nucleus",16,700)
b+=circle(350,180,13,"−","#dbeafe",BLUE,16)
b+=line(260,180,330,180,3,INK)
b+=text(295,155,"r",18,700)
b+=text(470,180,"Closer electron",18,700)
b+=text(470,210,"stronger attraction",16,400,GREEN)
b+=circle(650,180,34,"+","#fee2e2",RED,28)
b+=circle(805,180,13,"−","#dbeafe",BLUE,16)
b+=line(690,180,785,180,3,INK)
b+=text(738,155,"2r",18,700)
b+=text(730,235,"Twice the distance",18,700)
b+=text(730,262,"one-quarter the force",16,400,RED)
save("inverse-square-distance.svg", frame("Distance and electrostatic attraction", b, height=320, subtitle="The inverse-square relationship is F ∝ 1/r²; the sketch is conceptual."))

# CO2: polar bonds cancel because the molecule is linear.
b = text(240,150,"O",34,700,BLUE)+text(450,150,"C",34,700)+text(660,150,"O",34,700,BLUE)
b += line(285,150,405,150,3,INK)+line(285,158,405,158,3,INK)
b += line(495,150,615,150,3,INK)+line(495,158,615,158,3,INK)
b += line(355,105,405,105,3,RED)+f'<polygon points="355,105 370,97 370,113" fill="{RED}"/>'
b += line(545,105,495,105,3,RED)+f'<polygon points="545,105 530,97 530,113" fill="{RED}"/>'
b += text(450,215,"← bond dipole      bond dipole →",18,700,RED)
b += text(450,260,"Equal and opposite bond dipoles cancel: net molecular dipole = 0",18,700,GREEN)
save("co2-dipole-cancellation.svg", frame("Polar bonds, nonpolar molecule: CO₂", b, height=300, subtitle="Linear geometry places the two C=O bond dipoles in opposite directions."))

print(f"Generated {len(list(OUT.glob('*.svg')))} SVG diagrams in {OUT}")
