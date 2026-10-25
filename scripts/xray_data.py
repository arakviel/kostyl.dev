"""Chest X-Ray (Kaggle): loading into uint8 tensors, cache temp/xray_<size>.pt"""
import os
import numpy as np, torch
from PIL import Image

ROOT = "temp/chest_xray"
CLASSES = ["NORMAL", "PNEUMONIA"]

def _load_split(split, size):
    xs, ys, names = [], [], []
    for y, c in enumerate(CLASSES):
        d = os.path.join(ROOT, split, c)
        for f in sorted(os.listdir(d)):
            if not f.lower().endswith((".jpeg", ".jpg", ".png")): continue
            xs.append(np.asarray(Image.open(os.path.join(d, f)).convert("L").resize((size, size), Image.BILINEAR))); ys.append(y); names.append(f)
    return torch.from_numpy(np.stack(xs)), torch.tensor(ys), names

def load(size=128):
    path = f"temp/xray_{size}.pt"
    if os.path.exists(path): return torch.load(path, weights_only=False)
    data = {s: _load_split(s, size) for s in ("train", "val", "test")}
    torch.save(data, path); return data

if __name__ == "__main__":
    d = load(128)
    for s, (x, y, _) in d.items(): print(s, tuple(x.shape), "normal", int((y == 0).sum()), "pneumonia", int((y == 1).sum()))
