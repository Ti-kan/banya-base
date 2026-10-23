import sys
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
src=Path(sys.argv[1]); out=Path(sys.argv[2]); page=Path(sys.argv[3])
base=set(chr(c) for c in range(0x20,0x7F))
base|=set("ЁёАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя")
base|=set(" «»—–…№₽·×©°−→←↗★☆ ")
base|=set(page.read_text(encoding="utf-8"))
text="".join(sorted(ch for ch in base if ord(ch)>=0x20))
for name,(f,(lo,hi)) in {"oswald":("Oswald.ttf",(500,700)),"onest":("Onest.ttf",(400,700))}.items():
    font=TTFont(src/f)
    font=instancer.instantiateVariableFont(font,{"wght":(lo,hi)})
    o=subset.Options(); o.flavor="woff2"; o.layout_features=["kern","liga","calt","tnum","lnum","case","ccmp","locl"]; o.name_IDs=["*"]; o.notdef_outline=True
    s=subset.Subsetter(o); s.populate(text=text); s.subset(font); font.flavor="woff2"
    p=out/f"{name}.woff2"; font.save(p); print(p.name, p.stat().st_size//1024, "KB", len(font.getGlyphOrder()), "глифов")
