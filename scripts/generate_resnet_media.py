"""
Media for content/16.ai-python/15.cnn-image-classification/15.deep-networks-resnet.md  (needs temp/resnet_cache.pt)
Images -> public/images/ai-python/cnn-image-classification/resnet-skip-connections/
  01 degradation (plain 8/20/32)  02 plain vs residual  03 block scheme  04 gradient norm per block  05 final accuracies  06 ResNet-20 + augmentation  07 model family
"""
import os, sys
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn.functional as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import torchvision.models as M
from resnet_core import Net, load_cache, X_TEST, Y_TEST

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/resnet-skip-connections"
os.makedirs(IMG, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DEPTH = {1: 8, 3: 20, 5: 32}; DCOL = {1: CYAN, 3: AMBER, 5: RED}
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def despine(ax): [ax.spines[s].set_visible(False) for s in ("top", "right")]
def title(ax, t): ax.set_title(t, fontsize=12.5, fontweight="bold", color=INK)

def img01(C):
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.6)); ep = np.arange(1, 11)
    for n in (1, 3, 5):
        h = C[(n, False, False)]["hist"]; lab = f"{DEPTH[n]} шарів"
        axs[0].plot(ep, [e["train_loss"] for e in h], color=DCOL[n], lw=3, label=lab)
        axs[1].plot(ep, [e["train_acc"] * 100 for e in h], color=DCOL[n], lw=3, label=lab)
        axs[2].plot(ep, [e["test_acc"] * 100 for e in h], color=DCOL[n], lw=3, label=lab)
    title(axs[0], "Втрата на навчанні (звичайні мережі)"); title(axs[1], "Точність на навчальних зображеннях, %"); title(axs[2], "Точність на тесті, %")
    axs[1].legend(frameon=False, fontsize=10.5, loc="lower right")
    for a in axs: a.set_xlabel("епоха", color=MUTED); despine(a)
    save_png(fig, "01.png")

def img02(C):
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.6), sharey=True); ep = np.arange(1, 11)
    for a, n in zip(axs, (1, 3, 5)):
        for res, c, lab in ((False, MUTED, "звичайна"), (True, GREEN, "із пропускними з'єднаннями")):
            h = C[(n, res, False)]["hist"]
            a.plot(ep, [e["train_acc"] * 100 for e in h], color=c, lw=3, label=f"{lab}: навчання")
            a.plot(ep, [e["test_acc"] * 100 for e in h], color=c, lw=2, ls="--", label=f"{lab}: тест")
        title(a, f"{DEPTH[n]} шарів"); a.set_xlabel("епоха", color=MUTED); despine(a)
    axs[0].set_ylabel("точність, %", color=MUTED); axs[0].legend(frameon=False, fontsize=9, loc="lower right")
    save_png(fig, "02.png")

def box(ax, x, y, w, h, text, fc, ec=INK, fs=10.5, tc=INK):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.6))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold")
def arrow(ax, p, q, c=INK, lw=2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=c, lw=lw, connectionstyle=f"arc3,rad={rad}"))

def img03():
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 6.2))
    for a, res in zip(axs, (False, True)):
        a.set_xlim(-2, 2.6); a.set_ylim(-0.4, 7.6); a.axis("off")
        a.set_title("Звичайний блок" if not res else "Залишковий блок (residual block)", fontsize=13, fontweight="bold", color=INK)
        ys = [6.8, 5.5, 4.4, 3.3, 2.2]
        box(a, 0, 6.8, 1.6, .6, "вхід x", "#F1F5F9")
        box(a, 0, 5.6, 2.0, .6, "Conv 3×3 + BN", "#E0F2FE"); box(a, 0, 4.6, 2.0, .5, "ReLU", "#FEF3C7")
        box(a, 0, 3.6, 2.0, .6, "Conv 3×3 + BN", "#E0F2FE")
        arrow(a, (0, 6.5), (0, 5.9)); arrow(a, (0, 5.3), (0, 4.85)); arrow(a, (0, 4.35), (0, 3.9))
        if res:
            a.add_patch(Circle((0, 2.5), .32, fc="white", ec=GREEN, lw=2.2)); a.text(0, 2.5, "+", ha="center", va="center", fontsize=18, color=GREEN, fontweight="bold")
            arrow(a, (0, 3.3), (0, 2.82)); a.plot([0.8, 1.55], [6.8, 6.8], color=GREEN, lw=2.4)
            a.plot([1.55, 1.55], [6.8, 2.5], color=GREEN, lw=2.4); arrow(a, (1.55, 2.5), (.34, 2.5), GREEN, 2.4)
            a.text(1.7, 4.6, "shortcut\n(пропускне\nз'єднання)", fontsize=10.5, color=GREEN, fontweight="bold", va="center")
            box(a, 0, 1.4, 1.6, .5, "ReLU", "#FEF3C7"); arrow(a, (0, 2.18), (0, 1.67)); box(a, 0, .3, 2.6, .6, "F(x) + x", "#DCFCE7", GREEN)
            arrow(a, (0, 1.12), (0, .62))
        else:
            box(a, 0, 2.5, 1.6, .5, "ReLU", "#FEF3C7"); arrow(a, (0, 3.3), (0, 2.77)); box(a, 0, 1.2, 2.6, .6, "F(x)", "#F1F5F9"); arrow(a, (0, 2.22), (0, 1.52))
    save_png(fig, "03.png")

def grads(res):
    torch.manual_seed(0); m = Net(5, res); m.train()
    F.cross_entropy(m(X_TEST[:256]), Y_TEST[:256]).backward()
    return [b.conv1.weight.grad.norm().item() for b in m.blocks]

def img04():
    gp, gr = grads(False), grads(True); x = np.arange(1, 16)
    fig, ax = plt.subplots(figsize=(10, 4.8)); w = .38
    ax.bar(x - w / 2, gp, w, color=MUTED, label="звичайна"); ax.bar(x + w / 2, gr, w, color=GREEN, label="із пропускними з'єднаннями")
    ax.set_xticks(x); ax.set_xlabel("номер блоку (1 — біля входу, 15 — біля виходу)", color=MUTED); ax.set_ylabel("норма градієнта ваг conv1 блоку", color=MUTED)
    title(ax, "Градієнти у 32-шаровій мережі до навчання (1 пакет, 256 зображень)"); ax.legend(frameon=False, fontsize=11); despine(ax)
    save_png(fig, "04.png"); print("grad plain", [round(v, 3) for v in gp], "res", [round(v, 3) for v in gr])

def img05(C):
    fig, ax = plt.subplots(figsize=(10, 5)); w = .36; x = np.arange(3)
    for k, (res, c, lab) in enumerate(((False, MUTED, "звичайна"), (True, GREEN, "із пропускними з'єднаннями"))):
        v = [C[(n, res, False)]["hist"][-1]["test_acc"] * 100 for n in (1, 3, 5)]
        ax.bar(x + (k - .5) * w, v, w, color=c, label=lab)
        for xi, vi in zip(x + (k - .5) * w, v): ax.text(xi, vi + .4, f"{vi:.1f}", ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_xticks(x); ax.set_xticklabels([f"{DEPTH[n]} шарів" for n in (1, 3, 5)], fontsize=11.5); ax.set_ylim(60, 88); ax.set_ylabel("точність на тесті, %", color=MUTED)
    title(ax, "CIFAR-10, 10 епох, без аугментації"); ax.legend(frameon=False, fontsize=11, loc="upper left"); despine(ax)
    save_png(fig, "05.png")

def img06(C):
    h = C[(3, True, True)]["hist"]; h0 = C[(3, True, False)]["hist"]; ep = np.arange(1, 21)
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.6))
    axs[0].plot(ep, [e["train_acc"] * 100 for e in h], color=CYAN, lw=3, label="навчання"); axs[0].plot(ep, [e["test_acc"] * 100 for e in h], color=GREEN, lw=3, label="тест")
    axs[0].plot(ep[:10], [e["test_acc"] * 100 for e in h0], color=MUTED, lw=2, ls="--", label="тест, без аугментації (10 еп.)")
    title(axs[0], "ResNet-20 + відображення і зсув"); axs[0].set_ylabel("точність, %", color=MUTED); axs[0].legend(frameon=False, fontsize=10, loc="lower right")
    axs[1].plot(ep, [e["train_loss"] for e in h], color=CYAN, lw=3, label="навчання"); axs[1].plot(ep, [e["test_loss"] for e in h], color=GREEN, lw=3, label="тест")
    title(axs[1], "Втрата"); axs[1].legend(frameon=False, fontsize=10)
    for a in axs: a.set_xlabel("епоха", color=MUTED); despine(a)
    save_png(fig, "06.png")

def img07():
    names = ["LeNet-5\n1998", "AlexNet\n2012", "VGG-16\n2014", "ResNet-18\n2015", "ResNet-50\n2015", "ResNet-152\n2015"]
    p = [61706, sum(x.numel() for x in M.alexnet().parameters()), sum(x.numel() for x in M.vgg16().parameters()), sum(x.numel() for x in M.resnet18().parameters()),
         sum(x.numel() for x in M.resnet50().parameters()), sum(x.numel() for x in M.resnet152().parameters())]
    cols = [MUTED, AMBER, PURPLE, GREEN, GREEN, GREEN]
    fig, ax = plt.subplots(figsize=(11, 4.8)); ax.bar(range(6), p, color=cols); ax.set_yscale("log")
    for i, v in enumerate(p): ax.text(i, v * 1.15, f"{v / 1e6:.2f} млн" if v > 1e6 else f"{v:,}".replace(",", " "), ha="center", fontsize=10.5, fontweight="bold", color=INK)
    ax.set_xticks(range(6)); ax.set_xticklabels(names, fontsize=10.5); ax.set_ylim(2e4, 5e8); ax.set_ylabel("кількість параметрів (логарифмічна шкала)", color=MUTED)
    title(ax, "Відомі архітектури: параметри"); despine(ax); save_png(fig, "07.png"); print("params", p)

if __name__ == "__main__":
    C = load_cache()
    img01(C); img02(C); img03(); img04(); img05(C); img06(C); img07()
