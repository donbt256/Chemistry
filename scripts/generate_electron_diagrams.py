from pathlib import Path
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Ellipse
import numpy as np

OUT=Path("diagrams/electrons"); OUT.mkdir(parents=True,exist_ok=True)
TEXT_COLOR="#888888"
# Trigger regeneration after orbital-notation spacing correction.

def figure(title):
    fig,ax=plt.subplots(figsize=(12,6.67)); fig.patch.set_alpha(0)
    ax.set_facecolor("none"); ax.set_xlim(0,12); ax.set_ylim(0,6.67); ax.axis("off")
    ax.text(.25,6.25,title,color=TEXT_COLOR,fontsize=22,fontweight="bold",va="center")
    return fig,ax
def label(ax,x,y,s,size=14,**kw):
    kw.setdefault("color",TEXT_COLOR); kw.setdefault("ha","center"); kw.setdefault("va","center")
    ax.text(x,y,s,fontsize=size,**kw)
def save(fig,name):
    p=OUT/name; fig.savefig(p,format="svg",transparent=True,bbox_inches="tight",pad_inches=.05); plt.close(fig)

fig,ax=figure(r"Electron energy levels")
for i,n in enumerate([1,2,3,4]):
    y=1+i*1.05; ax.plot([2.4,10.5],[y,y],lw=3,color="#355f9e"); label(ax,1.4,y,r"$n=%d$"%n,18)
ax.add_patch(Circle((6.45,.48),.13,color="#b73737")); label(ax,6.45,.12,r"$\mathrm{nucleus}$",13)
save(fig,"electron-energy-levels.svg")

fig,ax=figure(r"$s$ and $p$ orbitals")
# s orbital: spherical electron-density region centered on the nucleus.
ax.add_patch(Circle((1.9,3.2),1.18,facecolor="#78aee8",alpha=.55,edgecolor="#315f9a",lw=2))
ax.add_patch(Circle((1.9,3.2),.07,color="#222222"))
label(ax,1.9,1.45,r"$s$",20)
label(ax,1.9,5.0,r"$\text{spherical}$",12)

# p orbitals: each is a two-lobed dumbbell with a node at the nucleus.
# The three panels show the mutually perpendicular x, y, and z orientations.
p_specs=[
    (5.0,r"$p_x$","x"),
    (7.8,r"$p_y$","y"),
    (10.6,r"$p_z$","z"),
]
for x,name,orient in p_specs:
    if orient=="x":
        ax.add_patch(Ellipse((x-.55,3.2),1.55,.9,facecolor="#78aee8",alpha=.55,edgecolor="#315f9a",lw=2))
        ax.add_patch(Ellipse((x+.55,3.2),1.55,.9,facecolor="#79b37f",alpha=.55,edgecolor="#3c7b42",lw=2))
    elif orient=="y":
        ax.add_patch(Ellipse((x,3.2-.55),.9,1.55,facecolor="#78aee8",alpha=.55,edgecolor="#315f9a",lw=2))
        ax.add_patch(Ellipse((x,3.2+.55),.9,1.55,facecolor="#79b37f",alpha=.55,edgecolor="#3c7b42",lw=2))
    else:
        # Perspective view of the z-oriented dumbbell: the lobes are tilted
        # toward and away from the viewer rather than incorrectly repeating p_y.
        ax.add_patch(Ellipse((x-.45,3.2),1.45,.78,angle=35,facecolor="#78aee8",alpha=.55,edgecolor="#315f9a",lw=2))
        ax.add_patch(Ellipse((x+.45,3.2),1.45,.78,angle=35,facecolor="#79b37f",alpha=.55,edgecolor="#3c7b42",lw=2))
    ax.add_patch(Circle((x,3.2),.07,color="#222222"))
    label(ax,x,1.45,name,20)
label(ax,6.25,.55,r"$\text{Each }p\text{ orbital has two lobes separated by a nodal plane.}$",12)
save(fig,"s-and-p-orbitals.svg")

fig,ax=figure(r"Periodic table blocks")
for r in range(7):
    for c in range(2): ax.add_patch(Rectangle((.7+c*.38,1.25+r*.38),.38,.38,fill=False,edgecolor="#c04a4a",lw=1.5))
for r in range(4):
    for c in range(10): ax.add_patch(Rectangle((3+c*.38,2.01+r*.38),.38,.38,fill=False,edgecolor="#3d70bd",lw=1.5))
for r in range(6):
    for c in range(6): ax.add_patch(Rectangle((7+c*.38,1.25+r*.38),.38,.38,fill=False,edgecolor="#4f9c58",lw=1.5))
for r in range(2):
    for c in range(14): ax.add_patch(Rectangle((4.1+c*.38,.35+r*.38),.38,.38,fill=False,edgecolor="#8057ad",lw=1.5))
label(ax,1.1,4.15,r"$s$-block",17); label(ax,4.7,4.15,r"$d$-block",17); label(ax,8,4.15,r"$p$-block",17); label(ax,6.75,.05,r"$f$-block",17)
label(ax,9.9,2.95,r"$s$: Groups 1--2",12,ha="left"); label(ax,9.9,2.45,r"$p$: Groups 13--18",12,ha="left"); label(ax,9.9,1.95,r"$d$: transition metals",12,ha="left"); label(ax,9.9,1.45,r"$f$: lanthanides + actinides",12,ha="left")
save(fig,"periodic-table-blocks.svg")

fig,ax=figure(r"Aufbau / Madelung filling order")
levels=["1s","2s","2p","3s","3p","4s","3d","4p","5s","4d","5p","6s","4f","5d","6p","7s","5f","6d","7p"]; coords={}
for i,s in enumerate(levels):
    col,row=divmod(i,6); x,y=1+col*3.35,5.45-row*.78; coords[s]=(x,y)
    ax.add_patch(Rectangle((x-.55,y-.25),1.1,.5,facecolor="#f2f3f7",edgecolor="#4b6794",lw=1.5)); label(ax,x,y,"$"+s+"$",14)
for a,b in zip(levels,levels[1:]):
    x,y=coords[a]; xx,yy=coords[b]; ax.add_patch(FancyArrowPatch((x+.55,y),(xx-.55,yy),arrowstyle="->",mutation_scale=12,lw=1.5,color="#c85b3d"))
label(ax,6,.55,r"$1s\rightarrow2s\rightarrow2p\rightarrow3s\rightarrow3p\rightarrow4s\rightarrow3d\rightarrow4p\rightarrow\cdots$",15)
save(fig,"aufbau-madelung.svg")

fig,ax=figure(r"Orbital notation")
examples=[(r"$\mathrm{C}$",r"$1s^2\;2s^2\;2p^2$",[r"$\uparrow\downarrow$",r"$\uparrow$",r"$\uparrow$"]),(r"$\mathrm{N}$",r"$1s^2\;2s^2\;2p^3$",[r"$\uparrow$",r"$\uparrow$",r"$\uparrow$"]),(r"$\mathrm{O}$",r"$1s^2\;2s^2\;2p^4$",[r"$\uparrow\downarrow$",r"$\uparrow$",r"$\uparrow$"]),(r"$\mathrm{F}$",r"$1s^2\;2s^2\;2p^5$",[r"$\uparrow\downarrow$",r"$\uparrow\downarrow$",r"$\uparrow$"]),(r"$\mathrm{Ne}$",r"$1s^2\;2s^2\;2p^6$",[r"$\uparrow\downarrow$",r"$\uparrow\downarrow$",r"$\uparrow\downarrow$"])]
for j,(el,conf,arrows) in enumerate(examples):
    x=1+j*2.2; label(ax,x,5.25,el,19); label(ax,x,4.7,conf,11)
    for k,a in enumerate(arrows):
        xx=x-.42+k*.42; ax.add_patch(Rectangle((xx,3.55),.42,.55,fill=False,edgecolor="#355f9e",lw=1.5)); label(ax,xx+.21,3.82,a,15)
label(ax,6,1.15,r"$\text{Each orbital holds at most 2 electrons; Hund's rule fills degenerate orbitals singly before pairing.}$",11)
save(fig,"orbital-notation.svg")

fig,ax=figure(r"Lewis dot notation")
positions=[(0,.42),(.42,0),(0,-.42),(-.42,0),(.42,.42),(-.42,.42),(.42,-.42),(-.42,-.42)]
for i,n in enumerate(range(1,9)):
    x=1.2+(i%4)*2.75; y=4.65-(i//4)*2.35; label(ax,x,y,r"$X$",26)
    for k in range(n): dx,dy=positions[k]; label(ax,x+dx,y+dy,r"$\bullet$",15)
    label(ax,x,y-.78,r"$%d\;\mathrm{valence\ electrons}$"%n,11)
save(fig,"lewis-dot-notation.svg")

fig,ax=figure(r"Period 2 Lewis dot notation")
els=[("Li",1),("Be",2),("B",3),("C",4),("N",5),("O",6),("F",7),("Ne",8)]
for i,(el,n) in enumerate(els):
    x=.9+i*1.45; y=3.65; label(ax,x,y,"$\\mathrm{%s}$"%el,17)
    for k in range(n): dx,dy=positions[k]; label(ax,x+dx*.72,y+dy*.72,r"$\bullet$",11)
label(ax,6,1,r"$\text{Valence electrons increase from 1 to 8 across Period 2.}$",13); save(fig,"period-2-lewis-dots.svg")

fig,ax=figure(r"Electromagnetic wave")
x=np.linspace(.7,11.3,700); y=3.2+1.15*np.sin(2*np.pi*3*(x-.7)/10.6); ax.plot(x,y,color="#355f9e",lw=3); ax.plot([.7,11.3],[3.2,3.2],color="#777777",lw=1)
ax.annotate("",xy=(1,4.35),xytext=(1,3.2),arrowprops=dict(arrowstyle="<->",color="#c85b3d",lw=2)); label(ax,1.45,3.85,r"$\text{amplitude}$",12,ha="left")
ax.annotate("",xy=(4.25,1),xytext=(6,1),arrowprops=dict(arrowstyle="<->",color="#c85b3d",lw=2)); label(ax,5.12,.62,r"$\text{wavelength }\lambda$",12); save(fig,"electromagnetic-wave.svg")

fig,ax=figure(r"Wavelength and frequency")
for y,cycles,txt in [(4.35,2,r"$\text{low frequency / long wavelength}$"),(2,8,r"$\text{high frequency / short wavelength}$")]:
    xx=np.linspace(.9,11.1,700); yy=y+.55*np.sin(2*np.pi*cycles*(xx-.9)/10.2); ax.plot(xx,yy,color="#355f9e",lw=2.5); label(ax,1.1,y+.9,txt,12,ha="left")
label(ax,6,.55,r"$c=\nu\lambda$",21); save(fig,"wavelength-frequency.svg")

fig,ax=figure(r"Electron transitions")
ys={1:1,2:2.15,3:3.3,4:4.45}
for n,y in ys.items(): ax.plot([2,9.8],[y,y],color="#355f9e",lw=2.5); label(ax,1.35,y,r"$n=%d$"%n,14)
ax.add_patch(FancyArrowPatch((5,1),(5,4.35),arrowstyle="->",mutation_scale=16,lw=2.5,color="#3d78bd")); label(ax,6.1,2.75,r"$\text{absorption}$",13,ha="left")
ax.add_patch(FancyArrowPatch((8,4.45),(8,1.1),arrowstyle="->",mutation_scale=16,lw=2.5,color="#c85b3d")); label(ax,8.55,2.75,r"$\text{emission}$",13,ha="left"); label(ax,6,.35,r"$\Delta E=h\nu$",20); save(fig,"electron-transitions.svg")

fig,ax=figure(r"Hydrogen emission spectrum — Balmer series")
ax.add_patch(Rectangle((1,2.65),10,1.4,facecolor="#e8e8ef",edgecolor="none"))
for nm,color in [(410,"#8238a6"),(434,"#3d83d4"),(486,"#31a9c4"),(656,"#bf3038")]:
    xx=1+(nm-400)/300*10; ax.plot([xx,xx],[2.65,4.05],color=color,lw=5); label(ax,xx,2.15,r"$%d\;\mathrm{nm}$"%nm,11)
label(ax,1,4.55,r"$\text{visible region}$",13,ha="left"); label(ax,6,.9,r"$\text{Balmer lines correspond to transitions ending at }n=2.$",12); save(fig,"hydrogen-emission-spectrum.svg")

fig,ax=figure(r"Absorption spectrum")
colors=["#d23c46","#d98739","#d7bc3e","#72a84e","#3e9f88","#3f76bd","#7950a6"]
for i,color in enumerate(colors):
    ax.add_patch(Rectangle((1+i*1.4,3.55),1.4,1.25,facecolor=color,edgecolor="none")); ax.add_patch(Rectangle((1+i*1.4,1),1.4,1.25,facecolor=color,edgecolor="none"))
for xx in [3.45,5.2,8]: ax.add_patch(Rectangle((xx,1),.08,1.25,facecolor="#1f1f2a",edgecolor="none"))
label(ax,1,5.15,r"$\text{continuous spectrum}$",13,ha="left"); label(ax,1,.55,r"$\text{absorption spectrum}$",13,ha="left"); label(ax,9,1.5,r"$\text{dark lines = absorbed wavelengths}$",11,ha="left"); save(fig,"absorption-spectrum.svg")

