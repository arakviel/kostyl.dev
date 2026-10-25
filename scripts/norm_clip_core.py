"""
Experiments for lesson 13 (LayerNorm and gradient clipping). Mirrors the code in the article (CPU, fixed seeds).
D: MNIST CNN with different normalization (none / BatchNorm / LayerNorm=GroupNorm(1)) and batch size   (eval-mode test accuracy)
F: 10-layer MLP with default PyTorch init (the one that was stuck in lesson 12) + BatchNorm / LayerNorm, SGD lr 0.05
G: 10-layer He MLP, SGD, lr grid x clipping (max_norm) -> divergence / grad norm history
Cache: temp/normclip_cache.pt (resumable)
"""
import os, sys, time
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import DataLoader
from cnn_mnist_core import train_set, X_TEST, Y_TEST

CACHE = "temp/normclip_cache.pt"
D_NORMS = ["none", "bn", "ln"]; D_BATCHES = [2, 8, 32, 128]; D_SEEDS = [0, 1, 2]; D_EPOCHS = 2
G_LRS = [0.05, 0.2, 0.5, 1.0, 2.0]; G_CLIPS = [None, 1.0]; G_SEEDS = [0, 1, 2]

def norm_layer(kind, c):
    if kind == "bn": return nn.BatchNorm2d(c)
    if kind == "ln": return nn.GroupNorm(1, c)       # one group = normalize over (C, H, W) of every image = LayerNorm for conv maps
    return nn.Identity()

def make_cnn(kind):
    return nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), norm_layer(kind, 16), nn.ReLU(), nn.MaxPool2d(2),
                         nn.Conv2d(16, 32, 3, padding=1), norm_layer(kind, 32), nn.ReLU(), nn.MaxPool2d(2),
                         nn.Flatten(), nn.Linear(32 * 7 * 7, 10))

def test_acc(model):
    model.eval()
    with torch.no_grad(): return (model(X_TEST).argmax(1) == Y_TEST).float().mean().item()

def train_cnn(kind, batch, seed, epochs=D_EPOCHS, lr=1e-3):
    torch.manual_seed(seed); model = make_cnn(kind)
    loader = DataLoader(train_set, batch_size=batch, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=lr); accs = []; t0 = time.time()
    for _ in range(epochs):
        model.train()
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step()
        accs.append(test_acc(model))
    return dict(acc=accs, secs=time.time() - t0)

def make_mlp(norm, depth=10):
    L = [nn.Flatten(), nn.Linear(784, 256)]
    L += [nn.BatchNorm1d(256) if norm == "bn" else nn.LayerNorm(256)] if norm in ("bn", "ln") else []
    L += [nn.ReLU()]
    for _ in range(depth - 2):
        L += [nn.Linear(256, 256)] + ([nn.BatchNorm1d(256) if norm == "bn" else nn.LayerNorm(256)] if norm in ("bn", "ln") else []) + [nn.ReLU()]
    return nn.Sequential(*L, nn.Linear(256, 10))          # PyTorch default init

def train_mlp_norm(norm, seed=0, epochs=3, lr=0.05):
    torch.manual_seed(seed); model = make_mlp(norm)
    loader = DataLoader(train_set, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.SGD(model.parameters(), lr=lr); accs = []
    for _ in range(epochs):
        model.train()
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step()
        accs.append(test_acc(model))
    return dict(acc=accs)

def make_he_mlp(depth=10):
    L = [nn.Flatten(), nn.Linear(784, 256), nn.ReLU()]
    for _ in range(depth - 2): L += [nn.Linear(256, 256), nn.ReLU()]
    m = nn.Sequential(*L, nn.Linear(256, 10))
    for l in m:
        if isinstance(l, nn.Linear): nn.init.kaiming_normal_(l.weight, nonlinearity="relu"); nn.init.zeros_(l.bias)
    return m

def train_clip(lr, clip, seed, epochs=1):
    torch.manual_seed(seed); model = make_he_mlp()
    loader = DataLoader(train_set, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.SGD(model.parameters(), lr=lr); norms, losses = [], []
    for _ in range(epochs):
        model.train()
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward()
            n = torch.nn.utils.clip_grad_norm_(model.parameters(), clip if clip else float("inf"))
            norms.append(n.item()); losses.append(loss.item()); opt.step()
    return dict(norms=norms, losses=losses, acc=test_acc(model))

def build_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    def save(): torch.save(out, CACHE)
    out.setdefault("D", {}); out.setdefault("F", {}); out.setdefault("G", {})
    for norm in ["none", "bn", "ln"]:
        if norm in out["F"]: continue
        out["F"][norm] = train_mlp_norm(norm); save(); print("F", norm, out["F"][norm]["acc"], flush=True)
    for lr in G_LRS:
        for clip in G_CLIPS:
            for seed in G_SEEDS:
                k = (lr, clip, seed)
                if k in out["G"]: continue
                out["G"][k] = train_clip(lr, clip, seed); save(); print("G", k, out["G"][k]["acc"], flush=True)
    for batch in D_BATCHES:
        for norm in D_NORMS:
            for seed in D_SEEDS:
                k = (norm, batch, seed)
                if k in out["D"]: continue
                out["D"][k] = train_cnn(norm, batch, seed); save(); print("D", k, out["D"][k], flush=True)
    return out

def load_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    if len(out.get("D", {})) < len(D_NORMS) * len(D_BATCHES) * len(D_SEEDS) or len(out.get("G", {})) < len(G_LRS) * len(G_CLIPS) * len(G_SEEDS): out = build_cache()
    return out

if __name__ == "__main__":
    build_cache()
