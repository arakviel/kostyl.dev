"""
Media for content/16.ai-python/15.cnn-image-classification/09.cnn-mnist.md  (needs temp/cnn_mnist_cache.pt, see cnn_mnist_core.py)
Images -> public/images/ai-python/cnn-image-classification/cnn-mnist/
  01 sample digits  02 architecture  03 training curves  04 MLP vs CNN over 3 seeds  05 confusion matrix
  06 misclassified digits  07 learned conv1 kernels  08 feature maps of one digit  09 shift robustness  10 probabilities
Videos -> public/videos/ai-python/cnn-image-classification/cnn-mnist/
  anim-01-training, anim-02-forward-pass, anim-03-shift-test
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
from cnn_mnist_core import *

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/cnn-mnist"
VID = "public/videos/ai-python/cnn-image-classification/cnn-mnist"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110

C = load_cache()
def get_model(cls, name, seed=0):
    m = cls(); m.load_state_dict(C["seeds"][seed][name]["state"]); m.eval(); return m
CNN0, MLP0 = get_model(CNN, "CNN"), get_model(MLP, "MLP")
with torch.no_grad():
    P_CNN, P_MLP = CNN0(X_TEST).softmax(1), MLP0(X_TEST).softmax(1)
PRED_CNN, PRED_MLP = P_CNN.argmax(1), P_MLP.argmax(1)
ERR = torch.nonzero(PRED_CNN != Y_TEST).flatten().tolist()
CM = np.zeros((10, 10), int)
for t, p in zip(Y_TEST.numpy(), PRED_CNN.numpy()): CM[t, p] += 1
SHIFTS = list(range(7))
ACC_SHIFT = {n: [accuracy(m, shift_images(X_TEST, s), Y_TEST) for s in SHIFTS] for n, m in (("MLP", MLP0), ("CNN", CNN0))}

def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def title(ax, t, color=INK, fs=12): ax.set_title(t, fontsize=fs, fontweight="bold", color=color, pad=6)
def show_digit(ax, x, t=None, tc=INK, fs=11):
    arr = x.numpy() if torch.is_tensor(x) else x
    arr = arr[0] if arr.ndim == 3 else arr
    ax.imshow(arr, cmap="gray", vmin=0, vmax=1, interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    if t: title(ax, t, tc, fs)

def summary():
    print("== SUMMARY ==")
    for s in (0, 1, 2):
        for n in ("MLP", "CNN"): print(n, s, [f"{a:.4f}" for _, a in C["seeds"][s][n]["hist"]][-1], f"{C['seeds'][s][n]['secs']:.0f}s")
    for n in ("MLP", "CNN"):
        fin = [C["seeds"][s][n]["hist"][-1][1] for s in (0, 1, 2)]; print(n, "mean", f"{np.mean(fin):.4f}", "std", f"{np.std(fin):.4f}")
    print("CNN errors", len(ERR), "MLP errors", int((PRED_MLP != Y_TEST).sum()))
    off = [(CM[i, j], i, j) for i in range(10) for j in range(10) if i != j]; off.sort(reverse=True); print("top confusions (count, true, pred):", off[:6])
    print("shift acc", {n: [round(a, 4) for a in v] for n, v in ACC_SHIFT.items()})
    print("first errors", ERR[:12])

# --- images -----------------------------------------------------------------------
def img01():
    fig, axs = plt.subplots(2, 10, figsize=(16, 3.9))
    for k, ax in enumerate(axs.ravel()): show_digit(ax, train_set.data[k].float() / 255, f"мітка {int(train_set.targets[k])}", INK, 11)
    fig.suptitle("Перші 20 цифр навчальної вибірки MNIST (60 000 зображень 28×28)", fontsize=14, fontweight="bold", color=INK, y=1.06)
    save_png(fig, "01.png")

def img02():
    st = [("Вхід", "[N, 1, 28, 28]", 1, 28, "", "#64748B"), ("Conv2d(1, 8, 3, pad=1)\n+ ReLU", "[N, 8, 28, 28]", 8, 28, "80", CYAN), ("MaxPool2d(2)", "[N, 8, 14, 14]", 8, 14, "0", GREEN),
          ("Conv2d(8, 16, 3, pad=1)\n+ ReLU", "[N, 16, 14, 14]", 16, 14, "1168", CYAN), ("MaxPool2d(2)", "[N, 16, 7, 7]", 16, 7, "0", GREEN)]
    fig, ax = plt.subplots(figsize=(19, 5.6)); ax.set_xlim(0, 19); ax.set_ylim(0.6, 6.4); ax.axis("off"); x = 0.3
    for k, (name, shape, ch, size, par, c) in enumerate(st):
        w = 0.2 + size / 28 * 2.1; n = min(ch, 6)
        for q in range(n - 1, -1, -1): ax.add_patch(patches.Rectangle((x + q * .09, 2.4 + q * .09), w, w, facecolor="white", edgecolor=c, lw=2))
        ax.text(x + w / 2, 2.0, shape, ha="center", fontsize=10.5, color=MUTED, fontweight="bold"); ax.text(x + w / 2 + 0.2, 2.4 + 0.09 * (n - 1) + w + 0.3, name, ha="center", va="bottom", fontsize=10.5, color=INK, fontweight="bold")
        if par: ax.text(x + w / 2, 1.55, f"{par} парам.", ha="center", fontsize=10.5, color=c, fontweight="bold")
        ax.annotate("", xy=(x + w + 0.65, 3.5), xytext=(x + w + 0.15, 3.5), arrowprops=dict(arrowstyle="->", lw=2.5, color=MUTED)); x += w + 1.0
    ax.add_patch(patches.Rectangle((x, 2.4), 0.35, 2.4, facecolor="#FEF3C7", edgecolor=AMBER, lw=2))
    ax.text(x + 0.17, 2.0, "[N, 784]", ha="center", fontsize=10.5, color=MUTED, fontweight="bold"); ax.text(x + 0.17, 5.0, "Flatten", ha="center", fontsize=10.5, color=INK, fontweight="bold")
    ax.annotate("", xy=(x + 1.2, 3.6), xytext=(x + 0.6, 3.6), arrowprops=dict(arrowstyle="->", lw=2.5, color=MUTED)); x += 1.4
    for q in range(10):
        ax.add_patch(patches.Rectangle((x, 2.2 + q * 0.26), 0.45, 0.22, facecolor="#D1FAE5", edgecolor=GREEN, lw=1.5)); ax.text(x + 0.62, 2.31 + q * 0.26, str(q), va="center", fontsize=8.5, color=INK)
    ax.text(x + 0.3, 1.55, "Linear(784, 10)\n7850 парам.", ha="center", fontsize=10.5, color=GREEN, fontweight="bold"); ax.text(x + 0.3, 5.0, "10 логітів", ha="center", fontsize=10.5, color=INK, fontweight="bold")
    fig.suptitle("Архітектура CNN для MNIST: усього 9 098 параметрів", fontsize=14, fontweight="bold", color=INK, y=0.99)
    save_png(fig, "02.png")

def img03():
    fig, axs = plt.subplots(1, 2, figsize=(14, 5.0)); ep = np.arange(1, EPOCHS + 1)
    for n, c in (("MLP", RED), ("CNN", GREEN)):
        h = C["seeds"][0][n]["hist"]; axs[0].plot(ep, [a for a, _ in h], marker="o", color=c, lw=2.5, label=n); axs[1].plot(ep, [b * 100 for _, b in h], marker="o", color=c, lw=2.5, label=n)
    axs[0].set_title("Втрата на навчальній вибірці", fontsize=13, fontweight="bold", color=INK); axs[1].set_title("Точність на тестовій вибірці, %", fontsize=13, fontweight="bold", color=INK)
    for a in axs: a.set_xlabel("епоха", fontsize=11, color=MUTED); a.legend(frameon=False, fontsize=11); a.set_xticks(ep); [a.spines[s].set_visible(False) for s in ("top", "right")]
    save_png(fig, "03.png")

def img04():
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.0), gridspec_kw={"width_ratios": [1, 1.1]})
    nparam = {"MLP": sum(p.numel() for p in MLP().parameters()), "CNN": sum(p.numel() for p in CNN().parameters())}
    bars = axs[0].bar(["MLP", "CNN"], [nparam["MLP"], nparam["CNN"]], color=[RED, GREEN], width=.55); axs[0].set_yscale("log"); axs[0].set_ylim(1000, 400000)
    for b, v in zip(bars, nparam.values()): axs[0].text(b.get_x() + b.get_width() / 2, v * 1.2, f"{v:,}".replace(",", " "), ha="center", fontsize=14, fontweight="bold", color=INK)
    axs[0].set_title("Параметрів (логарифмічна шкала)", fontsize=13, fontweight="bold", color=INK)
    for k, (n, c) in enumerate((("MLP", RED), ("CNN", GREEN))):
        fin = [C["seeds"][s][n]["hist"][-1][1] * 100 for s in (0, 1, 2)]
        axs[1].scatter([k] * 3, fin, color=c, s=70, zorder=3); axs[1].errorbar([k], [np.mean(fin)], yerr=[np.std(fin)], color=INK, capsize=8, lw=2, zorder=4)
        axs[1].text(k + 0.12, np.mean(fin), f"{np.mean(fin):.2f}%", va="center", fontsize=13, fontweight="bold", color=c)
    axs[1].set_xticks([0, 1]); axs[1].set_xticklabels(["MLP", "CNN"], fontsize=12); axs[1].set_xlim(-.5, 1.7); axs[1].set_ylim(96.5, 99.5)
    axs[1].set_title("Точність на тесті (3 запуски)", fontsize=13, fontweight="bold", color=INK)
    for a in axs: [a.spines[s].set_visible(False) for s in ("top", "right")]
    save_png(fig, "04.png")

def img05():
    fig, ax = plt.subplots(figsize=(8.4, 7.2)); M = np.where(CM > 0, CM, np.nan)
    ax.imshow(M, cmap="Blues", norm=LogNorm(vmin=1, vmax=1200), interpolation="nearest")
    for i in range(10):
        for j in range(10):
            if CM[i, j] > 0: ax.text(j, i, CM[i, j], ha="center", va="center", fontsize=11, fontweight="bold", color="white" if CM[i, j] > 60 else INK)
    ax.set_xticks(range(10)); ax.set_yticks(range(10)); ax.set_xlabel("передбачено", fontsize=12, color=MUTED); ax.set_ylabel("справжня цифра", fontsize=12, color=MUTED)
    ax.set_title(f"Матриця помилок CNN: {len(ERR)} помилок із 10 000", fontsize=13.5, fontweight="bold", color=INK, pad=12)
    save_png(fig, "05.png")

def img06():
    idx = ERR[:12]; fig, axs = plt.subplots(2, 6, figsize=(15, 5.6))
    for ax, i in zip(axs.ravel(), idx):
        show_digit(ax, X_TEST[i], f"істина {int(Y_TEST[i])} → {int(PRED_CNN[i])}\nвпевненість {P_CNN[i].max():.0%}", RED, 11)
    fig.suptitle("Перші 12 помилок CNN у порядку тестової вибірки", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "06.png")

def img07():
    w = CNN0.conv1.weight.detach().numpy()[:, 0]; b = CNN0.conv1.bias.detach().numpy(); lim = float(np.abs(w).max())
    fig, axs = plt.subplots(2, 4, figsize=(13, 6.8))
    for k, ax in enumerate(axs.ravel()):
        ax.imshow(w[k], cmap="RdYlGn", vmin=-lim, vmax=lim, interpolation="nearest")
        for i in range(3):
            for j in range(3): ax.text(j, i, f"{w[k, i, j]:.2f}", ha="center", va="center", fontsize=11, fontweight="bold", color=INK)
        for q in range(4): ax.axhline(q - .5, color="#94A3B8", lw=.8); ax.axvline(q - .5, color="#94A3B8", lw=.8)
        ax.set_xticks([]); ax.set_yticks([]); title(ax, f"ядро {k + 1}, зсув {b[k]:+.2f}", CYAN, 11)
    fig.suptitle("Вісім ядер першого шару після навчання: мережа знайшла їх сама", fontsize=14, fontweight="bold", color=INK, y=0.99)
    save_png(fig, "07.png")

def stages(model, x):
    with torch.no_grad():
        a1 = F.relu(model.conv1(x)); p1 = model.pool(a1); a2 = F.relu(model.conv2(p1)); p2 = model.pool(a2)
        probs = model.fc(p2.flatten(1)).softmax(1)
    return dict(a1=a1[0].numpy(), p1=p1[0].numpy(), a2=a2[0].numpy(), p2=p2[0].numpy(), probs=probs[0].numpy())

def img08():
    S = stages(CNN0, X_TEST[:1]); fig = plt.figure(figsize=(17, 9.6))
    gs = fig.add_gridspec(6, 8, height_ratios=[1.0, 0.18, 1.0, 0.18, 1.0, 1.0], hspace=0.5, wspace=0.08)
    ax = fig.add_subplot(gs[0, 0]); show_digit(ax, X_TEST[0], f"вхід: цифра {int(Y_TEST[0])}")
    for row, txt in ((1, "після блоку 1: 8 карт 14×14"), (3, "після блоку 2: 16 карт 7×7")):
        ax = fig.add_subplot(gs[row, :]); ax.axis("off"); ax.text(0, 0.1, txt, fontsize=13, fontweight="bold", color=CYAN, va="bottom")
    for k in range(8):
        ax = fig.add_subplot(gs[2, k]); ax.imshow(S["p1"][k], cmap="Greens", interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([]); title(ax, f"карта {k + 1}", INK, 10)
    for k in range(16):
        ax = fig.add_subplot(gs[4 + k // 8, k % 8]); ax.imshow(S["p2"][k], cmap="Greens", interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([]); title(ax, f"карта {k + 1}", INK, 10)
    fig.suptitle("Як одна цифра перетворюється шарами: каналів більше, карти менші й абстрактніші", fontsize=14, fontweight="bold", color=INK, y=0.95)
    save_png(fig, "08.png")

def img09():
    fig = plt.figure(figsize=(14, 7.2)); gs = fig.add_gridspec(2, 7, height_ratios=[1, 1.6], hspace=0.35)
    for k, s in enumerate(SHIFTS):
        ax = fig.add_subplot(gs[0, k]); xs = shift_images(X_TEST[:1], s); show_digit(ax, xs[0], f"зсув {s}\nCNN: {int(CNN0(xs).argmax())}  MLP: {int(MLP0(xs).argmax())}", INK, 10)
    ax = fig.add_subplot(gs[1, :])
    for n, c in (("MLP", RED), ("CNN", GREEN)):
        v = np.array(ACC_SHIFT[n]) * 100; ax.plot(SHIFTS, v, marker="o", lw=2.8, color=c, ms=8)
        for s, a in zip(SHIFTS, v): ax.text(s, a + (3 if n == "CNN" else -7), f"{a:.0f}", ha="center", fontsize=10.5, color=c, fontweight="bold")
        ax.text(6.12, v[-1], n, color=c, fontsize=13, fontweight="bold", va="center")
    ax.set_xlim(-0.3, 6.8); ax.set_ylim(0, 108); ax.set_xticks(SHIFTS); ax.set_xlabel("зсув тестових цифр вправо, пікселів", fontsize=11, color=MUTED); ax.set_ylabel("точність, %", fontsize=11, color=MUTED)
    ax.set_title("Обидві мережі навчені без зсунутих прикладів; CNN втрачає точність повільніше", fontsize=13, fontweight="bold", color=INK, loc="left"); [ax.spines[s].set_visible(False) for s in ("top", "right")]
    save_png(fig, "09.png")

def img10():
    idx = [0, ERR[0]]; fig, axs = plt.subplots(1, 4, figsize=(16, 4.4), gridspec_kw={"width_ratios": [0.7, 1.5, 0.7, 1.5]})
    for k, i in enumerate(idx):
        show_digit(axs[2 * k], X_TEST[i], f"тест №{i}: істина {int(Y_TEST[i])}", INK, 12); p = P_CNN[i].numpy()
        cols = [GREEN if q == int(p.argmax()) else "#CBD5E1" for q in range(10)]; axs[2 * k + 1].bar(range(10), p * 100, color=cols); axs[2 * k + 1].set_xticks(range(10)); axs[2 * k + 1].set_ylim(0, 105)
        axs[2 * k + 1].set_title(f"softmax, ймовірності у %: передбачено {int(p.argmax())} ({p.max():.1%})", fontsize=12, fontweight="bold", color=GREEN if int(p.argmax()) == int(Y_TEST[i]) else RED)
        [axs[2 * k + 1].spines[s].set_visible(False) for s in ("top", "right")]
    save_png(fig, "10.png")

# --- videos -----------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps); common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps)); update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_training():
    sn = C["snaps"]; steps = [s["step"] for s in sn]; allw = np.array([s["w"] for s in sn]); lim = float(np.abs(allw).max())
    fig = plt.figure(figsize=(13, 6.0)); fig.patch.set_facecolor("white")
    kax = [fig.add_axes([0.03 + (k % 4) * 0.115, 0.50 - (k // 4) * 0.34, 0.1, 0.1 * 13 / 6.0 * 0.0 + 0.26]) for k in range(8)]
    ax_l = fig.add_axes([0.55, 0.16, 0.19, 0.62]); ax_a = fig.add_axes([0.80, 0.16, 0.18, 0.62])
    head = fig.text(0.5, 0.93, "", ha="center", fontsize=15, fontweight="bold", color=INK); fig.text(0.24, 0.84, "Ядра першого шару", ha="center", fontsize=12.5, fontweight="bold", color=CYAN)
    total = len(sn) + 8

    def update(f):
        q = min(f, len(sn) - 1); s = sn[q]
        for k, ax in enumerate(kax):
            ax.clear(); ax.imshow(s["w"][k], cmap="RdYlGn", vmin=-lim, vmax=lim, interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values(): sp.set_edgecolor("#CBD5E1")
        ax_l.clear(); ax_l.plot(steps[1:q + 1], [x["loss"] for x in sn[1:q + 1]], color=AMBER, lw=2.5, marker="o", ms=4); ax_l.set_xscale("log"); ax_l.set_xlim(1, 12000); ax_l.set_ylim(0, 2.4)
        ax_l.set_title("Втрата (по 100 кроках)", fontsize=11.5, fontweight="bold", color=INK, pad=6); ax_l.tick_params(labelsize=8); [ax_l.spines[sp].set_visible(False) for sp in ("top", "right")]
        ax_a.clear(); ax_a.plot(steps[:q + 1], [x["acc"] * 100 for x in sn[:q + 1]], color=GREEN, lw=2.5, marker="o", ms=4); ax_a.set_xscale("symlog", linthresh=1); ax_a.set_xlim(0, 12000); ax_a.set_ylim(0, 100)
        ax_a.set_title("Точність на тесті, %", fontsize=11.5, fontweight="bold", color=INK, pad=6); ax_a.tick_params(labelsize=8); [ax_a.spines[sp].set_visible(False) for sp in ("top", "right")]
        head.set_text(f"Крок навчання {s['step']}: точність на тесті {s['acc']:.1%}")

    save_video(fig, update, total, "anim-01-training", 4, total - 1)

def vid_forward():
    S = stages(CNN0, X_TEST[:1]); probs = S["probs"]
    fig = plt.figure(figsize=(14, 5.8)); fig.patch.set_facecolor("white"); ax_i = fig.add_axes([0.02, 0.2, 0.14, 0.14 * 14 / 5.8 * 0.0 + 0.5])
    g1 = [fig.add_axes([0.2 + (k % 4) * 0.06, 0.6 - (k // 4) * 0.28, 0.052, 0.24]) for k in range(8)]
    g2 = [fig.add_axes([0.46 + (k % 8) * 0.036, 0.6 - (k // 8) * 0.28, 0.03, 0.24]) for k in range(16)]; ax_p = fig.add_axes([0.80, 0.2, 0.18, 0.55])
    head = fig.text(0.5, 0.93, "", ha="center", fontsize=15, fontweight="bold", color=INK); cap1 = fig.text(0.31, 0.14, "", ha="center", fontsize=11, fontweight="bold", color=CYAN); cap2 = fig.text(0.62, 0.14, "", ha="center", fontsize=11, fontweight="bold", color=CYAN)
    per = 5; total = per * 5 + 8

    def update(f):
        k = min(f // per, 4); txt = ["Вхід: цифра із тестової вибірки", "Блок 1: 8 карт ознак (Conv + ReLU + Pool)", "Блок 1 готовий", "Блок 2: 16 карт 7×7 (Conv + ReLU + Pool)", "Flatten → Linear → softmax: ймовірності цифр"][k]
        head.set_text(txt); ax_i.clear(); ax_i.imshow(X_TEST[0, 0].numpy(), cmap="gray", interpolation="nearest"); ax_i.set_xticks([]); ax_i.set_yticks([]); ax_i.set_title("Вхід", fontsize=12, fontweight="bold", color=INK)
        for q, ax in enumerate(g1):
            ax.clear(); ax.axis("off")
            if k >= 1: ax.imshow(S["p1"][q], cmap="Greens", interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([]); ax.axis("on")
        for q, ax in enumerate(g2):
            ax.clear(); ax.axis("off")
            if k >= 3: ax.imshow(S["p2"][q], cmap="Greens", interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([]); ax.axis("on")
        cap1.set_text("8 карт 14×14" if k >= 1 else ""); cap2.set_text("16 карт 7×7" if k >= 3 else "")
        ax_p.clear()
        if k >= 4:
            ax_p.barh(range(10), probs * 100, color=[GREEN if q == int(probs.argmax()) else "#CBD5E1" for q in range(10)]); ax_p.set_yticks(range(10)); ax_p.invert_yaxis(); ax_p.set_xlim(0, 105)
            ax_p.set_title(f"Відповідь: {int(probs.argmax())} ({probs.max():.1%})", fontsize=12, fontweight="bold", color=GREEN); [ax_p.spines[sp].set_visible(False) for sp in ("top", "right")]
        else: ax_p.axis("off")

    save_video(fig, update, total, "anim-02-forward-pass", 5, total - 1)

def vid_shift():
    fig = plt.figure(figsize=(13, 5.6)); fig.patch.set_facecolor("white"); ax_d = fig.add_axes([0.03, 0.15, 0.25, 0.25 * 13 / 5.6 * 0.0 + 0.65]); ax_c = fig.add_axes([0.40, 0.15, 0.25, 0.6]); ax_m = fig.add_axes([0.72, 0.15, 0.25, 0.6])
    head = fig.text(0.5, 0.93, "", ha="center", fontsize=15, fontweight="bold", color=INK); per = 5; total = per * len(SHIFTS) + 6

    def update(f):
        s = SHIFTS[min(f // per, len(SHIFTS) - 1)]; x = shift_images(X_TEST[:1], s)
        with torch.no_grad(): pc, pm = CNN0(x).softmax(1)[0].numpy(), MLP0(x).softmax(1)[0].numpy()
        ax_d.clear(); ax_d.imshow(x[0, 0].numpy(), cmap="gray", interpolation="nearest"); ax_d.set_xticks([]); ax_d.set_yticks([]); ax_d.set_title(f"Цифра {int(Y_TEST[0])}, зсув {s} пікс.", fontsize=12, fontweight="bold", color=INK)
        for ax, p, name in ((ax_c, pc, "CNN"), (ax_m, pm, "MLP")):
            ax.clear(); ok = int(p.argmax()) == int(Y_TEST[0]); ax.barh(range(10), p * 100, color=[(GREEN if ok else RED) if q == int(p.argmax()) else "#CBD5E1" for q in range(10)]); ax.set_yticks(range(10)); ax.invert_yaxis(); ax.set_xlim(0, 105)
            ax.set_title(f"{name}: {int(p.argmax())} ({p.max():.0%})", fontsize=12.5, fontweight="bold", color=GREEN if ok else RED); [ax.spines[sp].set_visible(False) for sp in ("top", "right")]
        head.set_text("Мережі навчені без зсунутих цифр: хто тримається довше?")

    save_video(fig, update, total, "anim-03-shift-test", 4, total - 1)

if __name__ == "__main__":
    summary()
    img01(); img02(); img03(); img04(); img05(); img06(); img07(); img08(); img09(); img10()
    vid_training(); vid_forward(); vid_shift()
