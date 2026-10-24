"""
Media for content/16.ai-python/15.cnn-image-classification/10.cnn-cifar10.md  (needs temp/cifar_cache.pt, see cifar_core.py)
Images -> public/images/ai-python/cnn-image-classification/cnn-cifar10/
  01 samples by class  02 variability: cats vs sevens  03 architecture of the wide CNN  04 model comparison
  05 overfitting curves (Wide)  06 Wide vs Wide+Dropout  07 three seeds  08 confusion matrix  09 per-class accuracy
  10 learned color kernels  11 feature maps of a photo  12 misclassified photos
Videos -> public/videos/ai-python/cnn-image-classification/cnn-cifar10/
  anim-01-overfitting, anim-02-dropout-effect, anim-03-predictions
"""
import os, sys
sys.path.insert(0, "scripts")
import numpy as np
import torch, torch.nn.functional as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LogNorm
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from cifar_core import *

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/cnn-cifar10"
VID = "public/videos/ai-python/cnn-image-classification/cnn-cifar10"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110
C = load_cache()
EP = np.arange(1, EPOCHS + 1)
def H(name, seed=0, key="test_acc"): return np.array([h[key] for h in C[name][seed]["hist"]])
def get_model(name, seed=0):
    m = MODELS[name](); m.load_state_dict(C[name][seed]["state"]); m.eval(); return m
BEST = get_model("WideDrop")
with torch.no_grad(): P = BEST(X_TEST).softmax(1)
PRED = P.argmax(1); ERR = torch.nonzero(PRED != Y_TEST).flatten().tolist()
CM = np.zeros((10, 10), int)
for t, p in zip(Y_TEST.numpy(), PRED.numpy()): CM[t, p] += 1

def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def title(ax, t, color=INK, fs=12): ax.set_title(t, fontsize=fs, fontweight="bold", color=color, pad=6)
def photo(ax, x, t=None, tc=INK, fs=10.5):
    ax.imshow(x.permute(1, 2, 0).numpy(), interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    if t: title(ax, t, tc, fs)
def clean(ax): [ax.spines[s].set_visible(False) for s in ("top", "right")]

def summary():
    print("== SUMMARY ==")
    for name in C:
        for s, d in C[name].items():
            h = d["hist"]; print(name, s, f"params {sum(p.numel() for p in MODELS[name]().parameters())}", f"train_acc {h[-1]['train_acc']:.4f} test_acc {h[-1]['test_acc']:.4f} test_loss {h[-1]['test_loss']:.3f} train_loss {h[-1]['train_loss']:.3f} secs/ep {np.mean([x['secs'] for x in h]):.0f}")
    for name in ("Wide", "WideDrop"):
        te = H(name, 0, "test_loss"); print(name, "min test loss epoch", int(te.argmin()) + 1, f"{te.min():.3f}", "| best test acc epoch", int(H(name, 0).argmax()) + 1, f"{H(name, 0).max():.4f}")
    for name in ("Wide", "WideDrop"):
        f = [C[name][s]["hist"][-1]["test_acc"] for s in (0, 1, 2)]; g = [C[name][s]["hist"][-1]["train_acc"] - C[name][s]["hist"][-1]["test_acc"] for s in (0, 1, 2)]
        print(name, "final test", [f"{a:.4f}" for a in f], f"mean {np.mean(f):.4f}", "gap", [f"{a:.3f}" for a in g])
    print("errors", len(ERR), "per class acc", [f"{CM[i, i] / CM[i].sum():.3f}" for i in range(10)])
    off = sorted([(CM[i, j], i, j) for i in range(10) for j in range(10) if i != j], reverse=True)[:6]; print("top confusions", [(int(c), CLASSES[i], CLASSES[j]) for c, i, j in off])
    print("first errors", ERR[:12])

# --- images -----------------------------------------------------------------------
def img01():
    fig, axs = plt.subplots(3, 10, figsize=(17, 5.6)); tg = np.array(train_set.targets)
    for c in range(10):
        idx = np.where(tg == c)[0][:3]
        for r in range(3):
            photo(axs[r, c], train_set[idx[r]][0], CLASSES[c] if r == 0 else None, INK, 12)
    fig.suptitle("CIFAR-10: 10 класів, 50 000 навчальних і 10 000 тестових фото 32×32×3", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "01.png")

def img02():
    tg = np.array(train_set.targets); cats = np.where(tg == 3)[0][:8]; mn = np.load("temp/mnist.npz"); sev = np.where(mn["y_train"] == 7)[0][:8]
    fig = plt.figure(figsize=(15, 4.6)); gs = fig.add_gridspec(2, 9, wspace=0.08, hspace=0.08, width_ratios=[1, 1, 1, 1, 0.4, 1, 1, 1, 1])
    for k in range(8):
        r, c = divmod(k, 4); ax = fig.add_subplot(gs[r, c]); photo(ax, train_set[cats[k]][0])
        ax = fig.add_subplot(gs[r, 5 + c]); ax.imshow(mn["x_train"][sev[k]], cmap="gray", interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    fig.text(0.28, 0.97, "8 «котів» з CIFAR-10", ha="center", fontsize=13, fontweight="bold", color=INK); fig.text(0.74, 0.97, "8 «сімок» з MNIST", ha="center", fontsize=13, fontweight="bold", color=INK)
    fig.suptitle("Один клас: цифри схожі між собою, а коти різняться позою, фоном, освітленням і ракурсом", fontsize=13.5, fontweight="bold", color=INK, y=1.07)
    save_png(fig, "02.png")

def img03():
    st = [("Вхід", "[3, 32, 32]", 3, 32, "", "#64748B"), ("Conv2d(3, 32, 3, pad=1)\n+ ReLU", "[32, 32, 32]", 32, 32, "896", CYAN), ("MaxPool2d(2)", "[32, 16, 16]", 32, 16, "0", GREEN),
          ("Conv2d(32, 64, 3, pad=1)\n+ ReLU", "[64, 16, 16]", 64, 16, "18 496", CYAN), ("MaxPool2d(2)", "[64, 8, 8]", 64, 8, "0", GREEN),
          ("Conv2d(64, 128, 3, pad=1)\n+ ReLU", "[128, 8, 8]", 128, 8, "73 856", CYAN), ("MaxPool2d(2)", "[128, 4, 4]", 128, 4, "0", GREEN)]
    fig, ax = plt.subplots(figsize=(24, 6.6)); ax.set_xlim(0, 24); ax.set_ylim(0.4, 7.2); ax.axis("off"); x = 0.3
    for name, shape, ch, size, par, c in st:
        w = 0.2 + size / 32 * 1.9; n = min(max(1, ch // 20 + 1), 6)
        for q in range(n - 1, -1, -1): ax.add_patch(patches.Rectangle((x + q * .09, 2.5 + q * .09), w, w, facecolor="white", edgecolor=c, lw=2))
        ax.text(x + w / 2, 2.05, shape, ha="center", fontsize=10, color=MUTED, fontweight="bold"); ax.text(x + w / 2 + .2, 2.5 + .09 * (n - 1) + w + .3, name, ha="center", va="bottom", fontsize=10, color=INK, fontweight="bold")
        if par: ax.text(x + w / 2, 1.55, f"{par} парам.", ha="center", fontsize=10, color=c, fontweight="bold")
        ax.annotate("", xy=(x + w + 0.6, 3.5), xytext=(x + w + 0.12, 3.5), arrowprops=dict(arrowstyle="->", lw=2.3, color=MUTED)); x += w + 0.95
    ax.add_patch(patches.Rectangle((x, 2.5), 0.3, 2.4, facecolor="#FEF3C7", edgecolor=AMBER, lw=2)); ax.text(x + .15, 2.05, "[2048]", ha="center", fontsize=10, color=MUTED, fontweight="bold"); ax.text(x + .15, 5.1, "Flatten", ha="center", fontsize=10, color=INK, fontweight="bold")
    ax.annotate("", xy=(x + 1.3, 3.7), xytext=(x + .5, 3.7), arrowprops=dict(arrowstyle="->", lw=2.3, color=MUTED)); x += 1.7
    ax.add_patch(patches.Rectangle((x, 2.9), 0.3, 1.6, facecolor="#E0E7FF", edgecolor=PURPLE, lw=2)); ax.text(x + .15, 2.05, "[128]", ha="center", fontsize=10, color=MUTED, fontweight="bold")
    ax.text(x + .15, 5.9, "Linear(2048, 128)\n+ ReLU (+ Dropout)", ha="center", fontsize=10, color=INK, fontweight="bold"); ax.text(x + .15, 1.55, "262 272\nпарам.", ha="center", fontsize=10, color=PURPLE, fontweight="bold")
    ax.annotate("", xy=(x + 1.4, 3.7), xytext=(x + .5, 3.7), arrowprops=dict(arrowstyle="->", lw=2.3, color=MUTED)); x += 2.0
    for q in range(10): ax.add_patch(patches.Rectangle((x, 2.6 + q * 0.24), 0.4, 0.2, facecolor="#D1FAE5", edgecolor=GREEN, lw=1.3))
    ax.text(x + .2, 5.1, "Linear(128, 10)", ha="center", fontsize=10, color=INK, fontweight="bold"); ax.text(x + .2, 1.55, "1290\nпарам.", ha="center", fontsize=10, color=GREEN, fontweight="bold")
    fig.suptitle("Ширша CNN для CIFAR-10: 356 810 параметрів, понад 70% із них у повнозв'язному шарі", fontsize=14, fontweight="bold", color=INK, y=0.99)
    save_png(fig, "03.png")

def img04():
    names = [("MLP", "MLP", RED), ("Small", "Мала CNN\n(як для MNIST)", AMBER), ("Wide", "Широка CNN", CYAN), ("WideDrop", "Широка CNN\n+ Dropout", GREEN)]
    fig, ax = plt.subplots(figsize=(11, 5.6)); vals = [H(n, 0)[-1] * 100 for n, _, _ in names]; ps = [sum(p.numel() for p in MODELS[n]().parameters()) for n, _, _ in names]
    bars = ax.bar([l for _, l, _ in names], vals, color=[c for _, _, c in names], width=.6)
    for b, v, p in zip(bars, vals, ps): ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", fontsize=15, fontweight="bold", color=INK); ax.text(b.get_x() + b.get_width() / 2, 3, f"{p:,}\nпарам.".replace(",", " "), ha="center", fontsize=10.5, color="white", fontweight="bold")
    ax.set_ylim(0, 100); ax.set_ylabel("точність на тесті після 12 епох, %", fontsize=11, color=MUTED); clean(ax)
    ax.set_title("CIFAR-10: чотири моделі (один запуск, seed 0)", fontsize=14, fontweight="bold", color=INK, pad=12)
    save_png(fig, "04.png")

def img05():
    fig, axs = plt.subplots(1, 2, figsize=(14, 5.2)); tr, te = H("Wide", 0, "train_acc") * 100, H("Wide", 0) * 100
    axs[0].plot(EP, tr, color=RED, marker="o", lw=2.6, label="навчальні (перші 10 000)"); axs[0].plot(EP, te, color=GREEN, marker="o", lw=2.6, label="тестові"); axs[0].fill_between(EP, te, tr, color=RED, alpha=.12)
    axs[0].set_title("Точність: розрив розкривається", fontsize=13, fontweight="bold", color=INK); axs[0].set_ylabel("%", color=MUTED)
    axs[1].plot(EP, H("Wide", 0, "train_loss"), color=RED, marker="o", lw=2.6, label="навчальна втрата"); axs[1].plot(EP, H("Wide", 0, "test_loss"), color=GREEN, marker="o", lw=2.6, label="тестова втрата")
    k = int(H("Wide", 0, "test_loss").argmin()); axs[1].scatter([EP[k]], [H("Wide", 0, "test_loss")[k]], s=120, color=AMBER, zorder=5); axs[1].annotate(f"мінімум на епосі {EP[k]}", (EP[k], H("Wide", 0, "test_loss")[k]), xytext=(EP[k] + 0.6, H("Wide", 0, "test_loss")[k] - 0.18), fontsize=11, color=AMBER, fontweight="bold")
    axs[1].set_title("Втрата: на тесті починає зростати", fontsize=13, fontweight="bold", color=INK)
    for a in axs: a.set_xlabel("епоха", fontsize=11, color=MUTED); a.set_xticks(EP); a.legend(frameon=False, fontsize=10.5); clean(a)
    save_png(fig, "05.png")

def img06():
    fig, axs = plt.subplots(1, 3, figsize=(18, 5.0))
    for name, c, lab in (("Wide", RED, "без Dropout"), ("WideDrop", GREEN, "Dropout 0.5")):
        axs[0].plot(EP, H(name, 0) * 100, color=c, marker="o", lw=2.5, label=lab); axs[1].plot(EP, H(name, 0, "test_loss"), color=c, marker="o", lw=2.5, label=lab)
        axs[2].plot(EP, (H(name, 0, "train_acc") - H(name, 0)) * 100, color=c, marker="o", lw=2.5, label=lab)
    for a, t in zip(axs, ("Точність на тесті, %", "Втрата на тесті", "Розрив «навчання − тест», п. п.")): a.set_title(t, fontsize=13, fontweight="bold", color=INK); a.set_xlabel("епоха", fontsize=11, color=MUTED); a.set_xticks(EP); a.legend(frameon=False, fontsize=11); clean(a)
    save_png(fig, "06.png")

def img07():
    fig, ax = plt.subplots(figsize=(8.5, 5.4))
    for k, (name, c) in enumerate((("Wide", RED), ("WideDrop", GREEN))):
        f = [C[name][s]["hist"][-1]["test_acc"] * 100 for s in (0, 1, 2)]; ax.scatter([k] * 3, f, s=90, color=c, zorder=3); ax.errorbar([k], [np.mean(f)], yerr=[np.std(f)], color=INK, capsize=9, lw=2, zorder=4)
        ax.text(k + 0.1, np.mean(f), f"{np.mean(f):.1f}%", va="center", fontsize=14, fontweight="bold", color=c)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Широка CNN", "Широка CNN + Dropout"], fontsize=12); ax.set_xlim(-.5, 1.7); ax.set_ylabel("точність на тесті, %", fontsize=11, color=MUTED); clean(ax)
    ax.set_title("Три запуски: точки, середнє ± σ", fontsize=13.5, fontweight="bold", color=INK, pad=10)
    save_png(fig, "07.png")

def img08():
    fig, ax = plt.subplots(figsize=(9.2, 8.0)); M = np.where(CM > 0, CM, np.nan); ax.imshow(M, cmap="Blues", norm=LogNorm(vmin=1, vmax=1000), interpolation="nearest")
    for i in range(10):
        for j in range(10):
            if CM[i, j] > 0: ax.text(j, i, CM[i, j], ha="center", va="center", fontsize=10.5, fontweight="bold", color="white" if CM[i, j] > 200 else INK)
    ax.set_xticks(range(10)); ax.set_yticks(range(10)); ax.set_xticklabels(CLASSES, rotation=45, ha="right"); ax.set_yticklabels(CLASSES); ax.set_xlabel("передбачено", fontsize=12, color=MUTED); ax.set_ylabel("справжній клас", fontsize=12, color=MUTED)
    ax.set_title(f"Матриця помилок: {len(ERR)} помилок із 10 000", fontsize=13.5, fontweight="bold", color=INK, pad=12)
    save_png(fig, "08.png")

def img09():
    acc = [CM[i, i] / CM[i].sum() * 100 for i in range(10)]; order = np.argsort(acc); fig, ax = plt.subplots(figsize=(10, 5.8))
    cols = [RED if acc[i] < 70 else (AMBER if acc[i] < 85 else GREEN) for i in order]; ax.barh([CLASSES[i] for i in order], [acc[i] for i in order], color=cols, height=.65)
    for y, i in enumerate(order): ax.text(acc[i] + 1, y, f"{acc[i]:.0f}%", va="center", fontsize=12, fontweight="bold", color=INK)
    ax.set_xlim(0, 105); ax.set_xlabel("точність за класом на тесті, %", fontsize=11, color=MUTED); clean(ax)
    ax.set_title("Одні класи розпізнаються легко, інші — ні", fontsize=14, fontweight="bold", color=INK, pad=10)
    save_png(fig, "09.png")

def img10():
    w = BEST.conv1.weight.detach().numpy(); fig, axs = plt.subplots(4, 8, figsize=(13, 7.2))
    for k, ax in enumerate(axs.ravel()):
        a = w[k].transpose(1, 2, 0); a = (a - a.min()) / (a.max() - a.min() + 1e-9); ax.imshow(a, interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("32 ядра першого шару 3×3×3, показані як кольорові картинки (кожне нормовано окремо)", fontsize=14, fontweight="bold", color=INK, y=0.99)
    save_png(fig, "10.png")

def img11():
    idx = 0; x = X_TEST[idx][None]
    with torch.no_grad(): a1 = BEST.pool(F.relu(BEST.conv1(x)))[0].numpy()
    fig = plt.figure(figsize=(15, 6.8)); gs = fig.add_gridspec(4, 10, hspace=0.12, wspace=0.08)
    ax = fig.add_subplot(gs[0:2, 0:2]); photo(ax, X_TEST[idx], f"вхід: {CLASSES[int(Y_TEST[idx])]}", INK, 12)
    for k in range(32):
        ax = fig.add_subplot(gs[k // 8, 2 + k % 8]); ax.imshow(a1[k], cmap="Greens", interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("32 карти ознак після першого блоку (16×16) для одного фото", fontsize=14, fontweight="bold", color=INK, y=0.98)
    save_png(fig, "11.png")

def img12():
    idx = ERR[:12]; fig, axs = plt.subplots(2, 6, figsize=(15, 6.0))
    for ax, i in zip(axs.ravel(), idx): photo(ax, X_TEST[i], f"{CLASSES[int(Y_TEST[i])]} → {CLASSES[int(PRED[i])]}\nвпевненість {P[i].max():.0%}", RED, 11)
    fig.suptitle("Перші 12 помилок моделі в порядку тестової вибірки", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "12.png")

# --- videos -----------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps); common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps)); update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_overfit():
    tr, te = H("Wide", 0, "train_acc") * 100, H("Wide", 0) * 100; trl, tel = H("Wide", 0, "train_loss"), H("Wide", 0, "test_loss")
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.6)); fig.patch.set_facecolor("white"); fig.subplots_adjust(top=0.82, wspace=0.18); head = fig.suptitle("", fontsize=15, fontweight="bold", color=INK, y=0.97)
    total = EPOCHS + 6

    def update(f):
        k = min(f, EPOCHS - 1) + 1
        for a in axs: a.clear()
        axs[0].plot(EP[:k], tr[:k], color=RED, marker="o", lw=2.6, label="навчальні"); axs[0].plot(EP[:k], te[:k], color=GREEN, marker="o", lw=2.6, label="тестові"); axs[0].fill_between(EP[:k], te[:k], tr[:k], color=RED, alpha=.12)
        axs[0].set_xlim(0.5, EPOCHS + .5); axs[0].set_ylim(40, 105); axs[0].set_title("Точність, %", fontsize=12.5, fontweight="bold", color=INK)
        axs[1].plot(EP[:k], trl[:k], color=RED, marker="o", lw=2.6, label="навчальна втрата"); axs[1].plot(EP[:k], tel[:k], color=GREEN, marker="o", lw=2.6, label="тестова втрата")
        axs[1].set_xlim(0.5, EPOCHS + .5); axs[1].set_ylim(0, 2.4); axs[1].set_title("Втрата", fontsize=12.5, fontweight="bold", color=INK)
        for a in axs: a.legend(frameon=False, fontsize=10.5, loc="lower right" if a is axs[0] else "upper right"); a.set_xlabel("епоха", color=MUTED); clean(a)
        head.set_text(f"Епоха {k}: навчальна {tr[k - 1]:.0f}%, тестова {te[k - 1]:.0f}%, розрив {tr[k - 1] - te[k - 1]:.0f} п. п.")

    save_video(fig, update, total, "anim-01-overfitting", 2, total - 1)

def vid_dropout():
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.6)); fig.patch.set_facecolor("white"); fig.subplots_adjust(top=0.82, wspace=0.18); head = fig.suptitle("", fontsize=15, fontweight="bold", color=INK, y=0.97); total = EPOCHS + 6

    def update(f):
        k = min(f, EPOCHS - 1) + 1
        for a in axs: a.clear()
        for name, c, lab in (("Wide", RED, "без Dropout"), ("WideDrop", GREEN, "Dropout 0.5")):
            axs[0].plot(EP[:k], H(name, 0, "test_loss")[:k], color=c, marker="o", lw=2.6, label=lab); axs[1].plot(EP[:k], (H(name, 0, "train_acc") - H(name, 0))[:k] * 100, color=c, marker="o", lw=2.6, label=lab)
        axs[0].set_ylim(0.6, 2.3); axs[0].set_title("Втрата на тесті", fontsize=12.5, fontweight="bold", color=INK); axs[1].set_ylim(-8, 25); axs[1].set_title("Розрив «навчання − тест», п. п.", fontsize=12.5, fontweight="bold", color=INK)
        for a in axs: a.set_xlim(0.5, EPOCHS + .5); a.legend(frameon=False, fontsize=10.5); a.set_xlabel("епоха", color=MUTED); clean(a)
        head.set_text(f"Епоха {k}: тест {H('Wide', 0)[k - 1] * 100:.1f}% (без) і {H('WideDrop', 0)[k - 1] * 100:.1f}% (Dropout)")

    save_video(fig, update, total, "anim-02-dropout-effect", 2, total - 1)

def vid_predictions():
    idx = list(range(8)); fig = plt.figure(figsize=(13, 5.6)); fig.patch.set_facecolor("white"); ax_i = fig.add_axes([0.04, 0.12, 0.28, 0.68]); ax_p = fig.add_axes([0.5, 0.12, 0.46, 0.72]); head = fig.text(0.5, 0.94, "", ha="center", fontsize=15, fontweight="bold", color=INK); per = 4; total = per * len(idx) + 2

    def update(f):
        i = idx[min(f // per, len(idx) - 1)]; p = P[i].numpy(); ok = int(p.argmax()) == int(Y_TEST[i])
        ax_i.clear(); ax_i.imshow(X_TEST[i].permute(1, 2, 0).numpy(), interpolation="nearest"); ax_i.set_xticks([]); ax_i.set_yticks([]); ax_i.set_title(f"справжній клас: {CLASSES[int(Y_TEST[i])]}", fontsize=13, fontweight="bold", color=INK)
        ax_p.clear(); order = np.argsort(-p)[:5]; ax_p.barh([CLASSES[q] for q in order][::-1], (p[order] * 100)[::-1], color=[(GREEN if ok else RED) if q == order[0] else "#CBD5E1" for q in order][::-1]); ax_p.set_xlim(0, 105); clean(ax_p)
        ax_p.set_title("Топ-5 ймовірностей, %", fontsize=12.5, fontweight="bold", color=INK)
        head.set_text(f"Відповідь моделі: {CLASSES[int(p.argmax())]} ({p.max():.0%}) — {'вірно' if ok else 'помилка'}")

    save_video(fig, update, total, "anim-03-predictions", 3, total - 1)

if __name__ == "__main__":
    summary()
    img01(); img02(); img03(); img04(); img05(); img06(); img07(); img08(); img09(); img10(); img11(); img12()
    vid_overfit(); vid_dropout(); vid_predictions()
