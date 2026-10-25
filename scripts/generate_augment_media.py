"""
Media for content/16.ai-python/15.cnn-image-classification/14.data-augmentation.md  (needs temp/augment_cache.pt)
Images -> public/images/ai-python/cnn-image-classification/data-augmentation/
  01 augmentation gallery  02 curves none vs flip+crop  03 ablation  04 per-class accuracy  05 what bad augmentation does
Videos -> public/videos/ai-python/cnn-image-classification/data-augmentation/   anim-01-one-cat-many-views
"""
import os, sys
sys.path.insert(0, "scripts")
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from torchvision import datasets, transforms as T
from cifar_core import WideCNN, DATA_ROOT, CLASSES, X_TEST, Y_TEST
from augment_core import CONFIGS, make_transform, load_cache

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/data-augmentation"
VID = "public/videos/ai-python/cnn-image-classification/data-augmentation"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110
NAMES = {"none": ("без аугментації", MUTED), "flip": ("відображення", CYAN), "crop": ("зсув (crop)", AMBER), "flip_crop": ("відображення + зсув", GREEN), "flip_crop_erase": ("+ вирізання (erasing)", PURPLE), "bad": ("погана: догори дриґом + поворот 90°", RED)}
RAW = datasets.CIFAR10(DATA_ROOT, train=True, download=False)
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def despine(ax): [ax.spines[s].set_visible(False) for s in ("top", "right")]
def show(ax, t): ax.imshow(t.permute(1, 2, 0).clamp(0, 1).numpy(), interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])

def img01():
    idx = [i for i in range(60) if RAW.targets[i] in (3, 1, 8, 4)][:6]   # cat, car, ship, deer ...
    rows = ["none", "flip", "crop", "flip_crop_erase", "bad"]; titles = ["оригінал", "відображення", "зсув (padding 4)", "зсув + відображення + вирізання", "погана: догори дриґом + поворот"]
    fig, axs = plt.subplots(len(rows), len(idx), figsize=(10.5, 9.2))
    for r, name in enumerate(rows):
        tf = make_transform(name)
        for c, i in enumerate(idx):
            torch.manual_seed(100 + 7 * c + r); show(axs[r, c], tf(RAW[i][0]))
            if r == 0: axs[r, c].set_title(CLASSES[RAW.targets[i]], fontsize=11, color=INK, fontweight="bold")
        axs[r, 0].set_ylabel(titles[r], fontsize=9.5, color=RED if name == "bad" else INK, fontweight="bold", rotation=0, ha="right", va="center", labelpad=8)
    save_png(fig, "01.png")

def img02(C):
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.8)); ep = np.arange(1, 26)
    for name in ("none", "flip_crop"):
        lab, c = NAMES[name]; H = [C[k]["hist"] for k in C if k[0] == name]
        m = lambda key: np.mean([[h[key] for h in run] for run in H], axis=0)
        axs[0].plot(ep, m("test_acc") * 100, color=c, lw=3, label=f"{lab}: тест"); axs[0].plot(ep, m("train_acc") * 100, color=c, lw=2, ls="--", label=f"{lab}: навчання")
        axs[1].plot(ep, m("test_loss"), color=c, lw=3, label=lab); axs[2].plot(ep, (m("train_acc") - m("test_acc")) * 100, color=c, lw=3, label=lab)
    axs[0].set_title("Точність, % (середнє з 3 зерен)", fontsize=12.5, fontweight="bold", color=INK); axs[0].legend(frameon=False, fontsize=9.5, loc="lower right")
    axs[1].set_title("Втрата на тесті", fontsize=12.5, fontweight="bold", color=INK); axs[1].legend(frameon=False, fontsize=10)
    axs[2].set_title("Розрив: точність на навчанні − на тесті, п. п.", fontsize=12.5, fontweight="bold", color=INK)
    for a in axs: a.set_xlabel("епоха", color=MUTED); despine(a)
    save_png(fig, "02.png")

def img03(C):
    order = ["none", "flip", "crop", "flip_crop", "flip_crop_erase"]; fig, axs = plt.subplots(1, 2, figsize=(15, 5.0), gridspec_kw=dict(width_ratios=[1.5, 1]))
    for i, name in enumerate(order):
        lab, c = NAMES[name]; a = np.array([C[k]["hist"][-1]["test_acc"] for k in C if k[0] == name]) * 100
        axs[0].bar(i, a.mean(), .7, color=c); axs[0].plot([i] * len(a), a, "o", color=INK, ms=5, alpha=.7); axs[0].text(i, a.mean() + .6, f"{a.mean():.1f}", ha="center", fontsize=11.5, fontweight="bold", color=INK)
    axs[0].set_xticks(range(5)); axs[0].set_xticklabels(["без", "відобр.", "зсув", "відобр.\n+ зсув", "+ вирізання"], fontsize=10.5); axs[0].set_ylim(65, 83); axs[0].set_ylabel("точність на тесті, 25-та епоха, %", color=MUTED)
    axs[0].set_title("Скільки дає кожна аугментація (3 зерна)", fontsize=12.5, fontweight="bold", color=INK)
    for i, name in enumerate(order):
        lab, c = NAMES[name]; g = np.array([C[k]["hist"][-1]["train_acc"] - C[k]["hist"][-1]["test_acc"] for k in C if k[0] == name]) * 100
        axs[1].barh(i, g.mean(), .7, color=c); axs[1].text(g.mean() + .4, i, f"{g.mean():.1f}", va="center", fontsize=11, fontweight="bold", color=INK)
    axs[1].set_yticks(range(5)); axs[1].set_yticklabels(["без", "відобр.", "зсув", "відобр.+зсув", "+ вирізання"]); axs[1].invert_yaxis(); axs[1].set_xlim(0, 28); axs[1].set_title("Розрив навчання − тест, п. п.", fontsize=12.5, fontweight="bold", color=INK)
    for a in axs: despine(a)
    save_png(fig, "03.png")

def per_class(state):
    m = WideCNN(0.0); m.load_state_dict(state); m.eval()
    with torch.no_grad(): p = m(X_TEST).argmax(1)
    return np.array([(p[Y_TEST == k] == k).float().mean().item() for k in range(10)]) * 100

def img04(C):
    a, b = per_class(C[("none", 0)]["state"]), per_class(C[("flip_crop", 0)]["state"]); y = np.arange(10)
    fig, ax = plt.subplots(figsize=(10, 5.6)); ax.barh(y - .2, a, .38, color=MUTED, label="без аугментації"); ax.barh(y + .2, b, .38, color=GREEN, label="відображення + зсув")
    for i in range(10): ax.text(max(a[i], b[i]) + 1, i, f"{b[i] - a[i]:+.1f}", va="center", fontsize=10.5, fontweight="bold", color=GREEN if b[i] >= a[i] else RED)
    ax.set_yticks(y); ax.set_yticklabels(CLASSES); ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xlabel("точність за класом, % (зерно 0)", color=MUTED); ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2); despine(ax)
    ax.set_title("Де саме допомогла аугментація (цифри — зміна, п. п.)", fontsize=12.5, fontweight="bold", color=INK); save_png(fig, "04.png")
    return a, b

def img05(C):
    fig, ax = plt.subplots(figsize=(9.5, 4.8)); ep = np.arange(1, 26)
    for name in ("none", "flip_crop", "bad"):
        lab, c = NAMES[name]; run = C[(name, 0)]["hist"]; ax.plot(ep, [h["test_acc"] * 100 for h in run], color=c, lw=3, label=f"{lab}: {run[-1]['test_acc'] * 100:.1f}%")
    ax.set_xlabel("епоха", color=MUTED); ax.set_ylabel("точність на тесті, %", color=MUTED); ax.legend(frameon=False, fontsize=10.5, loc="lower right"); despine(ax)
    ax.set_title("Аугментація має зберігати мітку (зерно 0)", fontsize=12.5, fontweight="bold", color=INK); save_png(fig, "05.png")

def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps); common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps)); update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_views():
    cat = next(i for i in range(200) if RAW.targets[i] == 3); tf = make_transform("flip_crop_erase"); orig = T.ToTensor()(RAW[cat][0])
    views = []
    for k in range(24): torch.manual_seed(500 + k); views.append(tf(RAW[cat][0]))
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 4.6)); fig.patch.set_facecolor("white"); head = fig.text(0.5, 0.96, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    def update(f):
        k = min(f // 2, 23)
        for a in axs: a.clear()
        show(axs[0], orig); axs[0].set_title("Оригінал: один раз і назавжди", fontsize=11.5, color=MUTED, fontweight="bold")
        show(axs[1], views[k]); axs[1].set_title(f"Нова версія №{k + 1} (мітка та сама: «кіт»)", fontsize=11.5, color=GREEN, fontweight="bold")
        head.set_text("Кожну епоху мережа бачить інший варіант того самого фото")
    save_video(fig, update, 48, "anim-01-one-cat-many-views", 6, 47)

if __name__ == "__main__":
    C = load_cache(); img01(); img02(C); img03(C); a, b = img04(C); print("per class none", a.round(1), "aug", b.round(1)); img05(C); vid_views()
