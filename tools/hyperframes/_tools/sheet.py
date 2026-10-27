# usage: sheet.py <project-dir> <out.png>  -> contact sheet (2 columns) of the newest `hyperframes snapshot` run, to read all frames in one look
import sys,glob,os
from PIL import Image
d=sorted(glob.glob(sys.argv[1]+"/.hyperframes/artifacts/snapshots/*"),key=os.path.getmtime)[-1]
fs=sorted(glob.glob(d+"/*.png"),key=lambda f:int(os.path.basename(f).split("-")[1]))
n=len(fs); cols=2; rows=(n+1)//2
S=Image.new("RGB",(cols*960,rows*540),"#222")
for i,f in enumerate(fs): S.paste(Image.open(f).convert("RGB").resize((960,540)),((i%cols)*960,(i//cols)*540))
S.save(sys.argv[2]); print(n,[os.path.basename(f) for f in fs])
