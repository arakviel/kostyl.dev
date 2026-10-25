"""
Experiments for lesson 16 (pneumonia on chest X-rays). 128x128 grayscale, CPU, fixed seeds. Cache: temp/xray_cache.pt (resumable)
Hold-out for choosing thresholds is taken from train BY PATIENT (the official val has only 16 images).
"""
import os, sys, time, re
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
import torchvision.models as M
from torchvision import transforms as T
from torch.utils.data import DataLoader, Dataset
from xray_data import load, CLASSES

CACHE = "temp/xray_cache.pt"
DATA = load(128)
XTR, YTR, NTR = DATA["train"]; XTE, YTE, NTE = DATA["test"]

def group_of(name):
    if name.startswith("person"): return name.split("_")[0]
    return re.sub(r"^NORMAL2-", "", name)[:7]            # IM-0115

def split_holdout(frac=0.15, seed=0):
    groups = sorted({group_of(n) for n in NTR}); rng = np.random.RandomState(seed); rng.shuffle(groups)
    hold = set(groups[:int(len(groups) * frac)])
    mask = torch.tensor([group_of(n) in hold for n in NTR])
    return (~mask).nonzero().flatten(), mask.nonzero().flatten()
TR_IDX, HO_IDX = split_holdout()

AUG = T.Compose([T.RandomAffine(degrees=8, translate=(0.05, 0.05), scale=(0.92, 1.08)), T.RandomAutocontrast(0.3)])
class DS(Dataset):
    def __init__(self, x, y, aug): self.x, self.y, self.aug = x, y, aug
    def __len__(self): return len(self.x)
    def __getitem__(self, i):
        x = self.x[i].unsqueeze(0)
        if self.aug: x = AUG(x)
        return x.float() / 255, self.y[i]

class SmallCNN(nn.Module):
    def __init__(self):
        super().__init__()
        def blk(i, o): return nn.Sequential(nn.Conv2d(i, o, 3, padding=1, bias=False), nn.BatchNorm2d(o), nn.ReLU(), nn.MaxPool2d(2))
        self.f = nn.Sequential(blk(1, 16), blk(16, 32), blk(32, 64), blk(64, 64))
        self.fc = nn.Linear(64, 2)
    def forward(self, x): return self.fc(F.adaptive_avg_pool2d(self.f(x), 1).flatten(1))

class Pre(nn.Module):
    """ResNet-18 trained on ImageNet; a grayscale image is repeated into 3 channels and normalised like ImageNet."""
    def __init__(self, pretrained=True):
        super().__init__()
        self.net = M.resnet18(weights=M.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None); self.net.fc = nn.Linear(512, 2)
        self.register_buffer("mean", torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)); self.register_buffer("std", torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))
    def prep(self, x): return (x.repeat(1, 3, 1, 1) - self.mean) / self.std
    def forward(self, x): return self.net(self.prep(x))
    def features(self, x):
        n = self.net; x = self.prep(x); x = n.maxpool(n.relu(n.bn1(n.conv1(x))))
        return F.adaptive_avg_pool2d(n.layer4(n.layer3(n.layer2(n.layer1(x)))), 1).flatten(1)

def probs(model, x, bs=128):
    model.eval(); out = []
    with torch.no_grad():
        for i in range(0, len(x), bs): out.append(F.softmax(model(x[i:i + bs].unsqueeze(1).float() / 255), 1)[:, 1])
    return torch.cat(out)

def metrics(p, y, thr=0.5):
    pred = (p >= thr).long(); tp = int(((pred == 1) & (y == 1)).sum()); fn = int(((pred == 0) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum()); tn = int(((pred == 0) & (y == 0)).sum())
    return dict(tp=tp, fn=fn, fp=fp, tn=tn, acc=(tp + tn) / len(y), recall=tp / max(tp + fn, 1), precision=tp / max(tp + fp, 1), spec=tn / max(tn + fp, 1))

def train(kind, seed, epochs, lr, weighted=False, verbose=True):
    torch.manual_seed(seed)
    model = SmallCNN() if kind == "scratch" else Pre(True)
    ds = DS(XTR[TR_IDX], YTR[TR_IDX], True)
    loader = DataLoader(ds, batch_size=32, shuffle=True, generator=torch.Generator().manual_seed(seed))
    cnt = torch.bincount(YTR[TR_IDX]).float(); w = (cnt.sum() / (2 * cnt)) if weighted else None
    opt = torch.optim.Adam(model.parameters(), lr=lr); hist = []
    xh, yh = XTR[HO_IDX], YTR[HO_IDX]
    for ep in range(epochs):
        t0 = time.time(); model.train(); tot = 0
        for x, y in loader:
            loss = F.cross_entropy(model(x), y, weight=w); opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(y)
        ph = probs(model, xh); pt = probs(model, XTE); mh = metrics(ph, yh); mt = metrics(pt, YTE)
        hist.append(dict(train_loss=tot / len(ds), hold=mh, test=mt, secs=time.time() - t0))
        if verbose: print(f"{kind} w={weighted} s{seed} ep{ep + 1}: loss {tot / len(ds):.3f} hold acc {mh['acc']:.3f} rec {mh['recall']:.3f} | test acc {mt['acc']:.3f} rec {mt['recall']:.3f} spec {mt['spec']:.3f} {hist[-1]['secs']:.0f}s", flush=True)
    return dict(hist=hist, ph=ph, pt=pt, state=model.state_dict())

def frozen(seed, epochs=60):
    torch.manual_seed(seed); m = Pre(True).eval()
    def feats(x):
        with torch.no_grad(): return torch.cat([m.features(x[i:i + 128].unsqueeze(1).float() / 255) for i in range(0, len(x), 128)])
    ftr, fho, fte = feats(XTR[TR_IDX]), feats(XTR[HO_IDX]), feats(XTE)
    fc = nn.Linear(512, 2); opt = torch.optim.Adam(fc.parameters(), 1e-3); y = YTR[TR_IDX]
    g = torch.Generator().manual_seed(seed)
    for ep in range(epochs):
        perm = torch.randperm(len(ftr), generator=g)
        for i in range(0, len(perm), 64):
            b = perm[i:i + 64]; loss = F.cross_entropy(fc(ftr[b]), y[b]); opt.zero_grad(); loss.backward(); opt.step()
    ph = F.softmax(fc(fho), 1)[:, 1].detach(); pt = F.softmax(fc(fte), 1)[:, 1].detach()
    return dict(hist=[dict(hold=metrics(ph, YTR[HO_IDX]), test=metrics(pt, YTE))], ph=ph, pt=pt)

RUNS = [("scratch", s, 10, 1e-3, False) for s in (0, 1, 2)] + [("finetune", s, 4, 1e-4, False) for s in (0, 1, 2)] + [("finetune", s, 4, 1e-4, True) for s in (0, 1, 2)]

def build_cache():
    out = torch.load(CACHE, weights_only=False) if os.path.exists(CACHE) else {}
    for s in (0, 1, 2):
        k = ("frozen", s, False)
        if k not in out: out[k] = frozen(s); torch.save(out, CACHE); print("DONE", k, out[k]["hist"][0]["test"]["acc"], flush=True)
    for kind, s, ep, lr, w in RUNS:
        k = (kind, s, w)
        if k in out: continue
        out[k] = train(kind, s, ep, lr, w); torch.save(out, CACHE); print("DONE", k, out[k]["hist"][-1]["test"]["acc"], flush=True)
    return out

def load_cache(): return build_cache() if not os.path.exists(CACHE) else torch.load(CACHE, weights_only=False)

if __name__ == "__main__":
    print("train", len(TR_IDX), "holdout", len(HO_IDX), "hold pneu", int(YTR[HO_IDX].sum()), flush=True)
    build_cache()
