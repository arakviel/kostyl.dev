"""
Experiments for lesson 11 (mini-batch, batch size vs learning rate, LR schedulers) on the MNIST CNN from lesson 09.
Everything here mirrors the code shown in the article (CPU, fixed seeds). Results cached in temp/minibatch_cache.pt
(re-run resumes: finished parts are kept).
"""
import os, sys, time
sys.path.insert(0, "scripts")
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from cnn_mnist_core import CNN, train_set, test_set

CACHE = "temp/minibatch_cache.pt"
BATCHES = [8, 32, 128, 512, 2048]
LRS = [2.5e-4, 1e-3, 4e-3, 1.6e-2, 6.4e-2]
NOISE_BATCHES = [1, 8, 32, 128, 512, 2048]
SCHEDS = ["const-1e-3", "const-1e-2", "step", "cosine", "warmup-cosine"]
SCHED_EPOCHS, SCHED_SEEDS = 10, (0, 1, 2)
test_loader = DataLoader(test_set, batch_size=1000)

def evaluate(model):
    model.eval(); correct = 0
    with torch.no_grad():
        for x, y in test_loader: correct += (model(x).argmax(1) == y).sum().item()
    return correct / len(test_set)

def run_grid_cell(B, lr, epochs=3, seed=0):
    torch.manual_seed(seed); model = CNN()
    loader = DataLoader(train_set, batch_size=B, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=lr); t0 = time.time(); accs, secs = [], []
    for _ in range(epochs):
        model.train()
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step()
        accs.append(evaluate(model)); secs.append(time.time() - t0)
    return dict(acc=accs, secs=secs, steps_per_epoch=len(loader))

def make_scheduler(kind, opt, n, epochs):
    S = torch.optim.lr_scheduler
    if kind.startswith("const"): return None
    if kind == "step": return S.StepLR(opt, step_size=3 * n, gamma=0.3)
    if kind == "cosine": return S.CosineAnnealingLR(opt, T_max=n * epochs)
    if kind == "warmup-cosine":
        return S.SequentialLR(opt, [S.LinearLR(opt, 0.01, 1.0, total_iters=n), S.CosineAnnealingLR(opt, T_max=n * (epochs - 1))], [n])

def run_sched(kind, seed, epochs=SCHED_EPOCHS):
    lr0 = 1e-3 if kind == "const-1e-3" else 1e-2
    torch.manual_seed(seed); model = CNN()
    loader = DataLoader(train_set, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=lr0); sch = make_scheduler(kind, opt, len(loader), epochs)
    accs, losses, lrs = [], [], []
    for _ in range(epochs):
        model.train(); tot = 0
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step()
            if sch: sch.step()
            tot += loss.item() * len(y); lrs.append(opt.param_groups[0]["lr"])
        accs.append(evaluate(model)); losses.append(tot / len(train_set))
    return dict(acc=accs, loss=losses, lr=lrs)

def flat_grad(model):
    return torch.cat([p.grad.flatten() for p in model.parameters()])

def gradient_noise(n_draws=100, seed=0):
    # a CNN after one epoch of ordinary training, then: exact full-data gradient and gradients of random mini-batches
    torch.manual_seed(seed); model = CNN()
    loader = DataLoader(train_set, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for x, y in loader:
        loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step()
    model.zero_grad(); acc = torch.zeros(sum(p.numel() for p in model.parameters()))
    for x, y in DataLoader(train_set, batch_size=2000):
        model.zero_grad(); F.cross_entropy(model(x), y, reduction="sum").backward(); acc += flat_grad(model)
    full = acc / len(train_set); out = {"full_norm": full.norm().item(), "cos": {}, "rel": {}}
    g = torch.Generator().manual_seed(123)
    for B in NOISE_BATCHES:
        cs, rs = [], []
        for _ in range(n_draws):
            idx = torch.randperm(len(train_set), generator=g)[:B]
            x = torch.stack([train_set[i][0] for i in idx]); y = train_set.targets[idx]
            model.zero_grad(); F.cross_entropy(model(x), y).backward(); gb = flat_grad(model)
            cs.append(F.cosine_similarity(gb, full, dim=0).item()); rs.append(((gb - full).norm() / full.norm()).item())
        out["cos"][B], out["rel"][B] = cs, rs
        print("noise B", B, f"cos {np.mean(cs):.3f} rel {np.mean(rs):.2f}", flush=True)
    return out

def build_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    def save(): torch.save(out, CACHE)
    if "noise" not in out: out["noise"] = gradient_noise(); save()
    out.setdefault("grid", {})
    for B in BATCHES:
        for lr in LRS:
            if (B, lr) in out["grid"]: continue
            out["grid"][(B, lr)] = run_grid_cell(B, lr); save(); print("grid", B, lr, [f"{a:.4f}" for a in out["grid"][(B, lr)]["acc"]], flush=True)
    out.setdefault("sched", {})
    for kind in SCHEDS:
        for seed in SCHED_SEEDS:
            if (kind, seed) in out["sched"]: continue
            out["sched"][(kind, seed)] = run_sched(kind, seed); save()
            print("sched", kind, seed, f"{out['sched'][(kind, seed)]['acc'][-1]:.4f}", flush=True)
    return out

def load_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    if "sched" not in out or len(out["sched"]) < len(SCHEDS) * len(SCHED_SEEDS): out = build_cache()
    return out

if __name__ == "__main__":
    build_cache()
