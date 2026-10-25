"""
Experiments for lesson 15 (deep nets, degradation, skip connections). CIFAR-style ResNet: 3 stages (16/32/64 channels), n blocks per stage,
depth = 6n + 2; 'plain' = same convs without skip connections. Adam 1e-3, batch 64, CPU, fixed seeds. Cache: temp/resnet_cache.pt (resumable)
"""
import os, sys, time
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms as T
from cifar_core import DATA_ROOT, X_TEST, Y_TEST, X_TR10, Y_TR10, evaluate

CACHE = "temp/resnet_cache.pt"
EPOCHS = 10
NS = [1, 3, 5]                            # depth 8, 20, 32
RUNS = [(n, res, False, EPOCHS) for n in (3, 5, 1) for res in (False, True)] + [(3, True, True, 20)]    # last: ResNet-20 with augmentation, 20 epochs

class Block(nn.Module):
    def __init__(self, c_in, c_out, stride, residual):
        super().__init__()
        self.conv1 = nn.Conv2d(c_in, c_out, 3, stride, 1, bias=False); self.bn1 = nn.BatchNorm2d(c_out)
        self.conv2 = nn.Conv2d(c_out, c_out, 3, 1, 1, bias=False); self.bn2 = nn.BatchNorm2d(c_out)
        self.residual = residual
        self.shortcut = nn.Identity()
        if residual and (stride != 1 or c_in != c_out):
            self.shortcut = nn.Sequential(nn.Conv2d(c_in, c_out, 1, stride, bias=False), nn.BatchNorm2d(c_out))
    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        if self.residual: out = out + self.shortcut(x)
        return F.relu(out)

class Net(nn.Module):
    def __init__(self, n, residual):
        super().__init__()
        self.stem = nn.Sequential(nn.Conv2d(3, 16, 3, padding=1, bias=False), nn.BatchNorm2d(16), nn.ReLU())
        layers, c_in = [], 16
        for c_out, stride in ((16, 1), (32, 2), (64, 2)):
            for i in range(n):
                layers.append(Block(c_in, c_out, stride if i == 0 else 1, residual)); c_in = c_out
        self.blocks = nn.Sequential(*layers)
        self.fc = nn.Linear(64, 10)
    def forward(self, x):
        x = self.blocks(self.stem(x))
        return self.fc(F.adaptive_avg_pool2d(x, 1).flatten(1))

def train_net(n, residual, seed=0, epochs=EPOCHS, augment=False):
    tf = T.Compose(([T.RandomCrop(32, padding=4), T.RandomHorizontalFlip()] if augment else []) + [T.ToTensor()])
    ds = datasets.CIFAR10(DATA_ROOT, train=True, download=False, transform=tf)
    torch.manual_seed(seed); model = Net(n, residual)
    loader = DataLoader(ds, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3); hist = []
    for ep in range(epochs):
        t0 = time.time(); model.train(); tot = 0
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(y)
        _, tr_acc = evaluate(model, X_TR10, Y_TR10); te_loss, te_acc = evaluate(model, X_TEST, Y_TEST)
        hist.append(dict(train_loss=tot / len(ds), train_acc=tr_acc, test_loss=te_loss, test_acc=te_acc, secs=time.time() - t0))
        print(f"n={n} res={residual} aug={augment} s{seed} ep{ep + 1}: loss {hist[-1]['train_loss']:.3f} tr {tr_acc:.4f} te {te_acc:.4f} {hist[-1]['secs']:.0f}s", flush=True)
    return dict(hist=hist, state=model.state_dict())

def build_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    for n, res, aug, ep in RUNS:
        k = (n, res, aug)
        if k in out: continue
        out[k] = train_net(n, res, 0, ep, aug); torch.save(out, CACHE); print("DONE", k, out[k]["hist"][-1]["test_acc"], flush=True)
    return out

def load_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    return out if len(out) >= len(RUNS) else build_cache()

if __name__ == "__main__":
    build_cache()
