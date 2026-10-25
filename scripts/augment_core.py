"""
Experiments for lesson 14 (data augmentation on CIFAR-10). Model = the WideCNN from lesson 10 (356 810 parameters), Adam 1e-3, batch 64,
EPOCHS epochs, CPU, fixed seeds. Test/eval images are never augmented. Cache: temp/augment_cache.pt (resumable)
"""
import os, sys, time
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms as T
from cifar_core import WideCNN, DATA_ROOT, X_TEST, Y_TEST, X_TR10, Y_TR10, evaluate

CACHE = "temp/augment_cache.pt"
EPOCHS = 25
CONFIGS = {
    "none":  [],
    "flip":  [T.RandomHorizontalFlip()],
    "crop":  [T.RandomCrop(32, padding=4)],
    "flip_crop": [T.RandomCrop(32, padding=4), T.RandomHorizontalFlip()],
    "flip_crop_erase": [T.RandomCrop(32, padding=4), T.RandomHorizontalFlip(), "ERASE"],
    "bad":   [T.RandomVerticalFlip(), T.RandomRotation(90)],
}
RUNS = [(c, s) for s in (0, 1, 2) for c in ("none", "flip", "crop", "flip_crop", "flip_crop_erase")] 
RUNS = [r for r in RUNS if r[1] == 0] + [("bad", 0)] + [r for r in RUNS if r[1] != 0]

def make_transform(name):
    ops = []
    for op in CONFIGS[name]:
        if op == "ERASE": continue
        ops.append(op)
    ops.append(T.ToTensor())
    if "ERASE" in CONFIGS[name]: ops.append(T.RandomErasing(p=0.5))
    return T.Compose(ops)

def train_aug(name, seed, epochs=EPOCHS):
    ds = datasets.CIFAR10(DATA_ROOT, train=True, download=False, transform=make_transform(name))
    torch.manual_seed(seed); model = WideCNN(0.0)
    loader = DataLoader(ds, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3); hist = []
    for ep in range(epochs):
        t0 = time.time(); model.train(); tot = 0
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(y)
        _, tr_acc = evaluate(model, X_TR10, Y_TR10); te_loss, te_acc = evaluate(model, X_TEST, Y_TEST)
        hist.append(dict(train_loss=tot / len(ds), train_acc=tr_acc, test_loss=te_loss, test_acc=te_acc, secs=time.time() - t0))
        print(f"{name} s{seed} ep{ep + 1}: tr {tr_acc:.4f} te {te_acc:.4f} loss {te_loss:.3f} {hist[-1]['secs']:.0f}s", flush=True)
    return dict(hist=hist, state=model.state_dict() if seed == 0 else None)

def build_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    for name, seed in RUNS:
        if (name, seed) in out: continue
        out[(name, seed)] = train_aug(name, seed); torch.save(out, CACHE); print("DONE", name, seed, out[(name, seed)]["hist"][-1]["test_acc"], flush=True)
    return out

def load_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    return out if len(out) >= len(RUNS) else build_cache()

if __name__ == "__main__":
    build_cache()
