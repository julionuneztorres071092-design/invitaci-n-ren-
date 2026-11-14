# Vectoriza el logo original por color -> logo.js + logo.svg
import sys, json, numpy as np, potrace
from PIL import Image
from scipy import ndimage as ndi
src, outdir = sys.argv[1], sys.argv[2]
S = 8
im = Image.open(src).convert('RGB'); im = im.resize((im.width*S, im.height*S), Image.LANCZOS)
a = np.asarray(im).astype(int); r,g,b = a[...,0],a[...,1],a[...,2]
dist=np.sqrt(((a-255)**2).sum(-1))
dist_s=ndi.gaussian_filter(dist,sigma=5)
F=dist_s>140
lab0,n0=ndi.label(F)
comp_class={}
for i in range(1,n0+1):
    c=lab0==i
    if c.sum()<400: continue
    core=c&(dist>230)
    px=a[core] if core.sum()>20 else a[c]
    mr,mg,mb=np.median(px,axis=0)
    if mr>170 and mg<120: k='red'
    elif abs(mr-mg)<25 and abs(mg-mb)<25: k='gray'
    elif mg>100: k='light'
    else: k='navy'
    comp_class[i]=k
masks={}
def trace(mask):
    bm = potrace.Bitmap(~mask)
    pl = bm.trace(turdsize=40, alphamax=1.1, opticurve=True, opttolerance=1.2)
    d=[]
    for c in pl:
        s=c.start_point; d.append(f'M{s.x/S:.2f} {s.y/S:.2f}')
        for sg in c.segments:
            if sg.is_corner: d.append(f'L{sg.c.x/S:.2f} {sg.c.y/S:.2f}L{sg.end_point.x/S:.2f} {sg.end_point.y/S:.2f}')
            else: d.append(f'C{sg.c1.x/S:.2f} {sg.c1.y/S:.2f} {sg.c2.x/S:.2f} {sg.c2.y/S:.2f} {sg.end_point.x/S:.2f} {sg.end_point.y/S:.2f}')
        d.append('Z')
    return ''.join(d)
parts=[]
for i,name in comp_class.items():
    comp=ndi.binary_fill_holes(lab0==i) if False else (lab0==i)
    ys,xs=np.where(comp)
    parts.append(dict(kind=name,x0=xs.min()/S,x1=xs.max()/S,y0=ys.min()/S,y1=ys.max()/S,d=trace(comp)))
cols={'red':'#E4202D','navy':'#0E4988','light':'#2475BA','gray':'#5a5a5a'}
parts.sort(key=lambda p:(p['kind']!='red' and p['kind']!='navy', p['x0']))
json.dump(dict(w=im.width/S,h=im.height/S,parts=parts,cols=cols), open(outdir+'/logo.json','w'))
open(outdir+'/logo.js','w').write('const LOGO_DATA='+json.dumps(dict(w=im.width/S,h=im.height/S,parts=parts,cols=cols))+';')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {im.width/S} {im.height/S}"><rect width="100%" height="100%" fill="#fff"/>'+''.join(f'<path d="{p["d"]}" fill="{cols[p["kind"]]}" fill-rule="evenodd"/>' for p in parts)+'</svg>'
open(outdir+'/logo.svg','w').write(svg)
for p in parts: print(p['kind'],round(p['x0']),round(p['x1']),round(p['y0']),round(p['y1']))
