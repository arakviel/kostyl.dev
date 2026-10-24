"""
Shared training code for lesson 10 (CNN for CIFAR-10). Model/loader/train code mirrors the article, so the numbers are reproducible
(CPU, fixed seeds). Cache with weights and per-epoch metrics: temp/cifar_cache.pt
"""
import os, time, warnings
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
warnings.filterwarnings("ignore")

DATA_ROOT = "temp/cifar_data"
CACHE = "temp/cifar_cache.pt"
EPOCHS = 12
CLASSES = ["літак", "авто", "птах", "кіт", "олень", "собака", "жаба", "кінь", "корабель", "вантажівка"]

transform = transforms.ToTensor()
train_set = datasets.CIFAR10(DATA_ROOT, train=True, download=True, transform=transform)
test_set = datasets.CIFAR10(DATA_ROOT, train=False, download=True, transform=transform)
X_TEST = torch.stack([test_set[i][0] for i in range(len(test_set))]); Y_TEST = torch.tensor(test_set.targets)
X_TR10 = torch.stack([train_set[i][0] for i in range(10000)]); Y_TR10 = torch.tensor(train_set.targets[:10000])

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Flatten(), nn.Linear(3072, 256), nn.ReLU(), nn.Linear(256, 10))
    def forward(self, x): return self.net(x)

class SmallCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(32 * 8 * 8, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        return self.fc(x.flatten(1))

class WideCNN(nn.Module):
    def __init__(self, dropout=0.0):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(128 * 4 * 4, 128)
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(128, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.dropout(F.relu(self.fc1(x.flatten(1))))
        return self.fc2(x)

MODELS = {"MLP": MLP, "Small": SmallCNN, "Wide": lambda: WideCNN(0.0), "WideDrop": lambda: WideCNN(0.5)}

def evaluate(model, x, y, bs=1000):
    model.eval(); loss = correct = 0
    with torch.no_grad():
        for i in range(0, len(x), bs):
            out = model(x[i:i + bs]); loss += F.cross_entropy(out, y[i:i + bs], reduction="sum").item(); correct += (out.argmax(1) == y[i:i + bs]).sum().item()
    return loss / len(x), correct / len(x)

def train(name, seed, epochs=EPOCHS, verbose=False):
    torch.manual_seed(seed); model = MODELS[name]()
    loader = DataLoader(train_set, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3); hist = []
    for ep in range(epochs):
        t0 = time.time(); model.train(); tot = 0
        for x, y in loader:
            loss = F.cross_entropy(model(x), y); opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(y)
        _, tr_acc = evaluate(model, X_TR10, Y_TR10); te_loss, te_acc = evaluate(model, X_TEST, Y_TEST)
        hist.append(dict(train_loss=tot / len(train_set), train_acc=tr_acc, test_loss=te_loss, test_acc=te_acc, secs=time.time() - t0))
        if verbose: print(f"{name} s{seed} ep{ep + 1}: {hist[-1]}", flush=True)
    return model, hist

PLAN = [(0, "MLP"), (0, "Small"), (0, "Wide"), (0, "WideDrop"), (1, "Wide"), (1, "WideDrop"), (2, "Wide"), (2, "WideDrop")]

def build_cache():
    out = {}
    for seed, name in PLAN:
        model, hist = train(name, seed, verbose=True)
        out.setdefault(name, {})[seed] = dict(state=model.state_dict(), hist=hist)
        torch.save(out, CACHE + ".partial")
        print("DONE", name, seed, f"{hist[-1]['test_acc']:.4f}", flush=True)
    torch.save(out, CACHE)
    return out

def load_cache():
    if os.path.exists(CACHE): return torch.load(CACHE, weights_only=False)
    return build_cache()

if __name__ == "__main__":
    build_cache()
