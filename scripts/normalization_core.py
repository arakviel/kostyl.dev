"""
Experiments for lesson 12 (weight initialization and Batch Normalization). Mirrors the code shown in the article (CPU, fixed seeds).
A: signal through a 30-layer stack (std of activations per layer)   B: 10-layer MLP on MNIST with different inits
C: 6-conv CNN on CIFAR-10 with and without BatchNorm (activation statistics are recorded during training)
Cache: temp/normalization_cache.pt (resumable)
"""
import os, sys, time
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import DataLoader
from cnn_mnist_core import train_set as MNIST_TRAIN, X_TEST as MX_TEST, Y_TEST as MY_TEST
from cifar_core import train_set as CIFAR_TRAIN, X_TEST as CX_TEST, Y_TEST as CY_TEST, evaluate as cifar_evaluate

CACHE = "temp/normalization_cache.pt"
INITS = ["N(0,1)", "N(0,0.01)", "default", "xavier", "he"]
DEPTH_A, WIDTH_A = 30, 256
EPOCHS_C = 8
CIFAR_RUNS = [(False, 1e-3, 0), (True, 1e-3, 0), (False, 1e-2, 0), (True, 1e-2, 0), (False, 1e-3, 1), (True, 1e-3, 1), (False, 1e-3, 2), (True, 1e-3, 2)]
SNAP_STEPS = [0, 20, 100, 400, 1000, 2000, 4000, 6000]

def init_linear(layer, init):
    if init == "N(0,1)": nn.init.normal_(layer.weight, 0, 1)
    elif init == "N(0,0.01)": nn.init.normal_(layer.weight, 0, 0.01)
    elif init == "xavier": nn.init.xavier_normal_(layer.weight)
    elif init == "he": nn.init.kaiming_normal_(layer.weight, nonlinearity="relu")

def signal_through_stack(act, init, seed=0, n_hist=20000):
    torch.manual_seed(seed); layers = []
    for _ in range(DEPTH_A):
        l = nn.Linear(WIDTH_A, WIDTH_A, bias=False); init_linear(l, init); layers.append(l)
    h = torch.randn(512, WIDTH_A, generator=torch.Generator().manual_seed(1)); stds, hists = [h.std().item()], [h.flatten()[:n_hist].clone()]
    f = torch.tanh if act == "tanh" else torch.relu
    for l in layers:
        h = f(l(h)); stds.append(h.std().item()); hists.append(h.flatten()[:n_hist].clone())
    return dict(std=stds, hist=hists)

def make_mlp(depth, init):
    L = [nn.Flatten(), nn.Linear(784, 256), nn.ReLU()]
    for _ in range(depth - 2): L += [nn.Linear(256, 256), nn.ReLU()]
    m = nn.Sequential(*L, nn.Linear(256, 10))
    for l in m:
        if isinstance(l, nn.Linear):
            init_linear(l, init)
            if init != "default": nn.init.zeros_(l.bias)
    return m

def train_mlp(init, opt_name, lr, epochs=3, depth=10, seed=0):
    torch.manual_seed(seed); m = make_mlp(depth, init)
    loader = DataLoader(MNIST_TRAIN, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(m.parameters(), lr=lr) if opt_name == "adam" else torch.optim.SGD(m.parameters(), lr=lr)
    losses, accs, grad_norms = [], [], None; step = 0
    for ep in range(epochs):
        m.train()
        for x, y in loader:
            loss = F.cross_entropy(m(x), y); opt.zero_grad(); loss.backward()
            if step == 0: grad_norms = [l.weight.grad.norm().item() for l in m if isinstance(l, nn.Linear)]
            opt.step(); step += 1
            if step % 10 == 0: losses.append(loss.item())
        m.eval()
        with torch.no_grad(): accs.append((m(MX_TEST).argmax(1) == MY_TEST).float().mean().item())
    return dict(losses=losses, acc=accs, grad_norms=grad_norms)

def make_deep_cnn(bn):
    L = []
    for k, (i, o) in enumerate(((3, 32), (32, 32), (32, 64), (64, 64), (64, 128), (128, 128))):
        L.append(nn.Conv2d(i, o, 3, padding=1))
        if bn: L.append(nn.BatchNorm2d(o))
        L.append(nn.ReLU())
        if k % 2 == 1: L.append(nn.MaxPool2d(2))
    return nn.Sequential(*L, nn.Flatten(), nn.Linear(128 * 4 * 4, 128), nn.ReLU(), nn.Linear(128, 10))

def snapshot(model, bn, probe):
    # 4th conv (index 10 with BN, 7 without): raw output and the input of its ReLU; BN momentum 0 so the snapshot does not touch running stats
    conv_idx = 10 if bn else 7
    relu_idx = conv_idx + (2 if bn else 1)
    bns = [m for m in model if isinstance(m, nn.BatchNorm2d)]
    for b in bns: b.momentum = 0.0
    store = {}
    h1 = model[conv_idx].register_forward_hook(lambda m, i, o: store.__setitem__("conv", o.detach()))
    h2 = model[relu_idx].register_forward_hook(lambda m, i, o: store.__setitem__("pre_relu", i[0].detach()))
    model.train()
    with torch.no_grad(): model(probe)
    h1.remove(); h2.remove()
    for b in bns: b.momentum = 0.1
    g = torch.Generator().manual_seed(0); out = {}
    for k, v in store.items():
        flat = v.flatten(); idx = torch.randperm(len(flat), generator=g)[:8000]
        out[k] = dict(mean=v.mean().item(), std=v.std().item(), sample=flat[idx].clone())
    return out

def train_cifar(bn, lr, seed, epochs=EPOCHS_C):
    torch.manual_seed(seed); model = make_deep_cnn(bn)
    loader = DataLoader(CIFAR_TRAIN, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=lr); hist, snaps, step = [], [], 0; probe = CX_TEST[:512]
    if seed == 0: snaps.append(dict(step=0, **snapshot(model, bn, probe)))
    for ep in range(epochs):
        t0 = time.time(); model.train(); tot = 0
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(y); step += 1
            if seed == 0 and step in SNAP_STEPS: snaps.append(dict(step=step, **snapshot(model, bn, probe)))
        te_loss, te_acc = cifar_evaluate(model, CX_TEST, CY_TEST)
        hist.append(dict(train_loss=tot / len(CIFAR_TRAIN), test_loss=te_loss, test_acc=te_acc, secs=time.time() - t0))
        print(f"cifar bn={bn} lr={lr} seed={seed} ep{ep + 1}: {hist[-1]}", flush=True)
    return dict(hist=hist, snaps=snaps, state=model.state_dict())

def build_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    def save(): torch.save(out, CACHE)
    if "A" not in out:
        out["A"] = {(act, init): signal_through_stack(act, init) for act in ("tanh", "relu") for init in INITS}; save(); print("A done", flush=True)
    out.setdefault("B", {})
    for opt_name, lr in (("sgd", 0.05), ("adam", 1e-3)):
        for init in ("N(0,0.01)", "default", "he"):
            if (opt_name, init) in out["B"]: continue
            out["B"][(opt_name, init)] = train_mlp(init, opt_name, lr); save(); print("B", opt_name, init, out["B"][(opt_name, init)]["acc"], flush=True)
    out.setdefault("C", {})
    for bn, lr, seed in CIFAR_RUNS:
        if (bn, lr, seed) in out["C"]: continue
        out["C"][(bn, lr, seed)] = train_cifar(bn, lr, seed); save()
    return out

def load_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    if len(out.get("C", {})) < len(CIFAR_RUNS): out = build_cache()
    return out

if __name__ == "__main__":
    build_cache()
