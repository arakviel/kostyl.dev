"""
Shared training code for the lesson 09 (CNN for MNIST). The model/loader/train code mirrors what the article shows,
so every number in the article is reproduced exactly (CPU, fixed seeds).
Cache with trained weights and metrics: temp/cnn_mnist_cache.pt
"""
import os, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

DATA_ROOT = "temp/mnist_data"
CACHE = "temp/cnn_mnist_cache.pt"
EPOCHS = 10
SNAP_STEPS = [0, 1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200, 300, 500, 800, 1200, 2000, 3000, 4500, 6500, 9380]

transform = transforms.ToTensor()
train_set = datasets.MNIST(DATA_ROOT, train=True, download=True, transform=transform)
test_set = datasets.MNIST(DATA_ROOT, train=False, download=True, transform=transform)
X_TEST = torch.stack([test_set[i][0] for i in range(len(test_set))])      # [10000, 1, 28, 28]
Y_TEST = test_set.targets

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Flatten(), nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
    def forward(self, x): return self.net(x)

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(16 * 7 * 7, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        return self.fc(x.flatten(1))

def accuracy(model, xs, ys):
    model.eval()
    with torch.no_grad(): return (model(xs).argmax(1) == ys).float().mean().item()

def train(cls, seed, epochs=EPOCHS, snap=False, verbose=False):
    torch.manual_seed(seed); model = cls()
    loader = DataLoader(train_set, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    hist, snaps, step, recent = [], [], 0, []
    def take():
        snaps.append(dict(step=step, w=model.conv1.weight.detach().clone().numpy()[:, 0] if hasattr(model, "conv1") else None,
                          loss=float(np.mean(recent[-100:])) if recent else float("nan"), acc=accuracy(model, X_TEST, Y_TEST)))
    if snap: take()
    for ep in range(epochs):
        model.train(); tot = n = 0
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step()
            tot += loss.item() * len(y); n += len(y); step += 1; recent.append(loss.item())
            if snap and step in SNAP_STEPS: take()
        acc = accuracy(model, X_TEST, Y_TEST); hist.append((tot / n, acc))
        if verbose: print(f"Епоха {ep + 1:>2}: втрата {tot / n:.4f}, точність на тесті {acc:.2%}")
    return model, hist, snaps

def shift_images(x, s):
    y = torch.roll(x, s, dims=3)
    if s > 0: y[..., :s] = 0
    return y

def build_cache():
    out = {"seeds": {}}
    for seed in (0, 1, 2):
        for name, cls in (("MLP", MLP), ("CNN", CNN)):
            t0 = time.time(); model, hist, snaps = train(cls, seed, snap=(seed == 0 and name == "CNN"))
            out["seeds"].setdefault(seed, {})[name] = dict(state=model.state_dict(), hist=hist, secs=time.time() - t0)
            if snaps: out["snaps"] = snaps
            print(name, seed, f"{hist[-1][1]:.4f}", f"{time.time() - t0:.0f}s", flush=True)
    torch.save(out, CACHE)
    return out

def load_cache():
    if os.path.exists(CACHE): return torch.load(CACHE, weights_only=False)
    return build_cache()

if __name__ == "__main__":
    build_cache()
