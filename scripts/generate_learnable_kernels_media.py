"""
Media for content/16.ai-python/15.cnn-image-classification/06.learnable-kernels.md
Images -> public/images/ai-python/cnn-image-classification/learnable-kernels/
  01 conv as one shared neuron   02 convolution as matrix product (im2col)  03 kernel at training steps
  04 loss curve + maps           05 four targets: target vs learned           06 nn.Conv2d anatomy
  07 parameters Dense vs Conv2d  08 eight random kernels -> eight maps
Videos -> public/videos/ai-python/cnn-image-classification/learnable-kernels/
  anim-01-im2col, anim-02-learning-sobel, anim-03-four-kernels, anim-04-eight-kernels
Training: Adam lr=0.1, 600 steps, seed 0, 64 MNIST digits, target = conv with a known kernel (MSE)
"""
import os
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

plt.rcParams['font.family'] = 'DejaVu Sans'
IMG = "public/images/ai-python/cnn-image-classification/learnable-kernels"
VID = "public/videos/ai-python/cnn-image-classification/learnable-kernels"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110

mn = np.load("temp/mnist.npz")
X = torch.tensor(mn["x_train"][:64] / 255, dtype=torch.float32)[:, None]      # [64, 1, 28, 28]
seven_np = mn["x_train"][101] / 255; assert mn["y_train"][101] == 7
seven = torch.tensor(seven_np, dtype=torch.float32)[None, None]
TARGETS = {"Собель X": [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], "Собель Y": [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
           "Розмиття": [[1 / 9] * 3] * 3, "Загострення": [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]}
LIM = 4.0

def train(target, steps=600, lr=0.1, seed=0):
    kt = torch.tensor(target, dtype=torch.float32)[None, None]; y = F.conv2d(X, kt)
    torch.manual_seed(seed); layer = nn.Conv2d(1, 1, 3, bias=False); opt = torch.optim.Adam(layer.parameters(), lr=lr)
    ws, ls = [layer.weight.detach().numpy()[0, 0].copy()], []
    for _ in range(steps):
        loss = F.mse_loss(layer(X), y); ls.append(loss.item()); opt.zero_grad(); loss.backward(); opt.step()
        ws.append(layer.weight.detach().numpy()[0, 0].copy())
    ls.append(F.mse_loss(layer(X), y).item())
    return np.array(ws), np.array(ls)

def fmap(w):
    return F.conv2d(seven, torch.tensor(w, dtype=torch.float32)[None, None])[0, 0].numpy()

def kpanel(ax, k, title=None, tcolor=CYAN, fs=12, lim=None):
    ax.clear(); lim = lim or max(1.0, float(np.abs(k).max()))
    ax.imshow(k, cmap="RdYlGn", vmin=-lim, vmax=lim, interpolation="nearest")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{k[i, j]:.2f}".replace("-0.00", "0.00"), ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)
    for q in range(4): ax.axhline(q - .5, color="#94A3B8", lw=.8); ax.axvline(q - .5, color="#94A3B8", lw=.8)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    if title: ax.set_title(title, fontsize=12, fontweight="bold", color=tcolor, pad=6)

def mpanel(ax, m, title=None, tcolor=INK, lim=LIM):
    ax.clear(); ax.imshow(m, cmap="RdYlGn", vmin=-lim, vmax=lim, interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_edgecolor("#CBD5E1")
    if title: ax.set_title(title, fontsize=12, fontweight="bold", color=tcolor, pad=6)

def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def grid_nums(ax, M, cmap, vmin, vmax, fmt=str, fs=12, labels=None):
    ax.clear(); ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest", aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]; ax.text(j, i, fmt(v), ha="center", va="center", fontsize=fs, fontweight="bold",
                                 color="white" if (cmap == "gray" and v < (vmin + vmax) / 2) else INK)
    for k in range(M.shape[0] + 1): ax.axhline(k - .5, color="#94A3B8", lw=.8)
    for k in range(M.shape[1] + 1): ax.axvline(k - .5, color="#94A3B8", lw=.8)
    ax.set_xticks([]); ax.set_yticks(range(M.shape[0]) if labels else [])
    if labels: ax.set_yticklabels(labels, fontsize=9, color=MUTED)
    for s in ax.spines.values(): s.set_visible(False)

I5 = np.array([[0, 1, 5, 0, 0], [0, 0, 5, 1, 0], [1, 0, 4, 0, 0], [0, 0, 5, 0, 1], [0, 1, 5, 0, 0]])
K5 = np.array([[-1, 1, -1]] * 3)

# --- images -----------------------------------------------------------------------
def img01():
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.0), gridspec_kw={"width_ratios": [1.3, 0.9, 1.0]})
    grid_nums(axs[0], I5, "gray", 0, 5, fs=13)
    axs[0].add_patch(patches.Rectangle((-.5, -.5), 3, 3, fill=False, edgecolor=CYAN, lw=4))
    axs[0].add_patch(patches.Rectangle((1.5, 1.5), 3, 3, fill=False, edgecolor=AMBER, lw=4))
    axs[0].set_title("Дві різні ділянки входу", fontsize=12.5, fontweight="bold", color=INK, pad=8)
    kpanel(axs[1], K5.astype(float), "Одні й ті самі ваги\n(один нейрон, 9 чисел)", CYAN, 14, lim=2)
    out = np.full((3, 3), np.nan); out[0, 0] = -14; out[2, 2] = -15
    axs[2].clear(); axs[2].set_xlim(-.5, 2.5); axs[2].set_ylim(2.5, -.5); axs[2].set_aspect("equal")
    for i in range(3):
        for j in range(3): axs[2].add_patch(patches.Rectangle((j - .5, i - .5), 1, 1, fill=True, facecolor="white", edgecolor="#94A3B8", lw=.8))
    for (i, j, c, v) in [(0, 0, CYAN, -14), (2, 2, AMBER, -15)]:
        axs[2].add_patch(patches.Rectangle((j - .5, i - .5), 1, 1, fill=True, facecolor=c, alpha=.35, edgecolor=c, lw=3))
        axs[2].text(j, i, f"{v}", ha="center", va="center", fontsize=16, fontweight="bold", color=INK)
    axs[2].set_xticks([]); axs[2].set_yticks([])
    for s in axs[2].spines.values(): s.set_visible(False)
    axs[2].set_title("Два виходи однієї карти", fontsize=12.5, fontweight="bold", color=INK, pad=8)
    for ax_, t in [(axs[1], "→"), (axs[2], "→")]:
        ax_.text(-0.12, 0.5, t, transform=ax_.transAxes, fontsize=30, color=MUTED, ha="center", va="center", fontweight="bold")
    fig.suptitle("Згортка — це один нейрон, який дивиться на різні ділянки", fontsize=14, fontweight="bold", color=INK, y=1.04)
    save_png(fig, "01.png")

def patches_matrix():
    rows, labels = [], []
    for i in range(3):
        for j in range(3): rows.append(I5[i:i + 3, j:j + 3].flatten()); labels.append(f"({i},{j})")
    return np.array(rows), labels

def img02():
    Xm, labels = patches_matrix(); w = K5.flatten(); o = Xm @ w
    assert np.array_equal(o.reshape(3, 3), np.array([[-14, 12, -13], [-15, 13, -14], [-14, 13, -15]]))
    fig, axs = plt.subplots(1, 4, figsize=(15, 5.6), gridspec_kw={"width_ratios": [9, 1.2, 1.2, 3.2]})
    grid_nums(axs[0], Xm, "gray", 0, 5, labels=labels); axs[0].set_title("Матриця ділянок X (9 позицій × 9 пікселів)", fontsize=12, fontweight="bold", color=INK, pad=8)
    grid_nums(axs[1], w[:, None].astype(float), "RdYlGn", -2, 2, fmt=lambda v: f"{int(v)}", fs=12); axs[1].set_title("w", fontsize=13, fontweight="bold", color=CYAN, pad=8)
    grid_nums(axs[2], o[:, None].astype(float), "RdYlGn", -15, 15, fmt=lambda v: f"{int(v):+d}", fs=12); axs[2].set_title("X · w", fontsize=13, fontweight="bold", color=GREEN, pad=8)
    grid_nums(axs[3], o.reshape(3, 3).astype(float), "RdYlGn", -15, 15, fmt=lambda v: f"{int(v):+d}", fs=14); axs[3].set_title("перескладаємо 3×3", fontsize=12, fontweight="bold", color=INK, pad=8)
    for ax_, t in [(axs[1], "×"), (axs[2], "="), (axs[3], "→")]:
        ax_.text(-0.28 if ax_ is not axs[3] else -0.1, 0.5, t, transform=ax_.transAxes, fontsize=28, color=MUTED, ha="center", va="center", fontweight="bold")
    fig.suptitle("Згортка = множення матриці ділянок на вектор ваг", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "02.png")

WS = {}
def get(name):
    if name not in WS: WS[name] = train(TARGETS[name])
    return WS[name]

def img03():
    ws, ls = get("Собель X"); steps = [0, 10, 30, 100, 300, 600]
    fig, axs = plt.subplots(1, 7, figsize=(19, 3.6), gridspec_kw={"width_ratios": [1] * 6 + [1]})
    for ax, s in zip(axs, steps): kpanel(ax, ws[s], f"крок {s}\nвтрата {ls[s]:.3g}", INK, 11, lim=2)
    kpanel(axs[6], np.array(TARGETS["Собель X"], float), "ціль:\nСобель X", GREEN, 11, lim=2)
    fig.suptitle("Ядро з випадкових чисел перетворюється на ядро Собеля X", fontsize=14, fontweight="bold", color=INK, y=1.12)
    save_png(fig, "03.png")

def img04():
    ws, ls = get("Собель X"); steps = [0, 10, 30, 100, 600]
    fig = plt.figure(figsize=(16, 7.0)); gs = fig.add_gridspec(2, 6, height_ratios=[1.0, 0.9], hspace=0.22, wspace=0.12)
    for k, s in enumerate(steps):
        ax = fig.add_subplot(gs[0, k]); mpanel(ax, fmap(ws[s]), f"крок {s}")
    ax = fig.add_subplot(gs[0, 5]); mpanel(ax, fmap(np.array(TARGETS["Собель X"], float)), "ціль", GREEN)
    ax = fig.add_subplot(gs[1, :]); ax.semilogy(np.arange(len(ls)), ls, color=CYAN, lw=2.5)
    for s in steps: ax.scatter([s], [ls[s]], color=AMBER, zorder=5, s=60)
    ax.set_xlabel("крок навчання", fontsize=11, color=MUTED); ax.set_ylabel("втрата MSE (логарифмічна шкала)", fontsize=11, color=MUTED)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.set_title("Втрата падає від ≈1.2 до ≈10⁻¹⁴", fontsize=12.5, fontweight="bold", color=INK, loc="left")
    fig.suptitle("Карта ознак цифри «7» наближається до цільової разом із падінням втрати", fontsize=14, fontweight="bold", color=INK, y=0.98)
    save_png(fig, "04.png")

def img05():
    fig, axs = plt.subplots(2, 4, figsize=(14, 6.6))
    for c, name in enumerate(TARGETS):
        ws, ls = get(name)
        kpanel(axs[0, c], np.array(TARGETS[name], float), f"ціль: {name}", GREEN, 11, lim=2)
        kpanel(axs[1, c], ws[-1], f"після 600 кроків\nвтрата {ls[-1]:.0e}", CYAN, 11, lim=2)
    fig.suptitle("Той самий код навчає ядро під будь-яку ціль", fontsize=14, fontweight="bold", color=INK, y=1.0)
    save_png(fig, "05.png")

def img06():
    fig, ax = plt.subplots(figsize=(15, 5.4)); ax.set_xlim(0, 15); ax.set_ylim(0, 5.4); ax.axis("off")
    def stack(x, y, w, n, color, label, sub):
        for k in range(n - 1, -1, -1): ax.add_patch(patches.Rectangle((x + k * .12, y + k * .12), w, w, facecolor="white", edgecolor=color, lw=2))
        ax.text(x + w / 2, y - .55, label, ha="center", fontsize=12.5, fontweight="bold", color=INK); ax.text(x + w / 2, y - .98, sub, ha="center", fontsize=10.5, color=MUTED)
    stack(.6, 1.9, 2.4, 4, "#64748B", "Вхід", "[N, 1, 28, 28]")
    for k in range(8):
        r, c = divmod(k, 4)
        ax.add_patch(patches.Rectangle((6.0 + c * .85, 3.0 - r * .95), .7, .7, facecolor="#BAE6FD", edgecolor=CYAN, lw=2))
    ax.text(7.55, 1.5, "weight: [8, 1, 3, 3]", ha="center", fontsize=12.5, fontweight="bold", color=INK); ax.text(7.55, 1.05, "8 ядер 3×3 + bias [8]", ha="center", fontsize=10.5, color=MUTED)
    ax.text(7.55, 4.45, "nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3)", ha="center", fontsize=12.5, fontweight="bold", color=CYAN)
    for k in range(8):
        r, c = divmod(k, 4)
        ax.add_patch(patches.Rectangle((11.2 + c * .95, 3.0 - r * .95), .8, .8, facecolor="#D1FAE5", edgecolor=GREEN, lw=2))
    ax.text(12.95, 1.5, "Вихід", ha="center", fontsize=12.5, fontweight="bold", color=INK); ax.text(12.95, 1.05, "[N, 8, 26, 26]", ha="center", fontsize=10.5, color=MUTED)
    for x0, x1 in [(3.7, 5.8), (9.6, 11.0)]: ax.annotate("", xy=(x1, 2.8), xytext=(x0, 2.8), arrowprops=dict(arrowstyle="->", lw=3, color=MUTED))
    fig.suptitle("Що всередині шару nn.Conv2d(1, 8, 3)", fontsize=14, fontweight="bold", color=INK, y=1.0)
    save_png(fig, "06.png")

def img07():
    dense = 784 * (8 * 26 * 26) + 8 * 26 * 26; conv = 8 * 1 * 3 * 3 + 8
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    bars = ax.bar(["Dense: 784 → 5408\nвиходів", "Conv2d(1, 8, 3)\nті самі 5408 виходів"], [dense, conv], color=[RED, GREEN], width=.5)
    ax.set_yscale("log"); ax.set_ylim(1, 3e7)
    for b, v in zip(bars, [dense, conv]): ax.text(b.get_x() + b.get_width() / 2, v * 1.3, f"{v:,}".replace(",", " "), ha="center", fontsize=15, fontweight="bold", color=INK)
    ax.set_ylabel("кількість параметрів (логарифмічна шкала)", fontsize=11, color=MUTED)
    ax.set_title(f"Різниця у {dense // conv:,} разів".replace(",", " "), fontsize=14, fontweight="bold", color=INK, pad=12)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    save_png(fig, "07.png")

def rand_kernels():
    torch.manual_seed(0); layer = nn.Conv2d(1, 8, 3)
    return layer, layer.weight.detach().numpy()[:, 0], layer(seven).detach().numpy()[0]

def img08():
    layer, ks, maps = rand_kernels(); lim = float(np.abs(maps).max())
    fig, axs = plt.subplots(2, 8, figsize=(19, 5.6))
    for k in range(8):
        kpanel(axs[0, k], ks[k], f"ядро {k + 1}", CYAN, 9, lim=0.35); mpanel(axs[1, k], maps[k], None, lim=lim)
    fig.suptitle("Вісім випадкових ядер до навчання: різні відгуки, але жодне ядро ні під що не налаштоване", fontsize=14, fontweight="bold", color=INK, y=1.0)
    save_png(fig, "08.png")

# --- videos -----------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps)
    common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps))
    update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_im2col():
    Xm, labels = patches_matrix(); w = K5.flatten(); o = Xm @ w
    fig = plt.figure(figsize=(13, 5.6)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.02, 0.18, 0.22, 0.62]); ax_x = fig.add_axes([0.31, 0.12, 0.36, 0.64]); ax_w = fig.add_axes([0.71, 0.12, 0.04, 0.64]); ax_o = fig.add_axes([0.84, 0.12, 0.04, 0.64])
    fig.text(0.5, 0.92, "Кожна позиція ядра — один рядок матриці; результат — один рядок множення на вектор ваг", ha="center", fontsize=14, fontweight="bold", color=INK)
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    fig.text(0.695, 0.45, "×", fontsize=28, color=MUTED, ha="center", va="center", fontweight="bold"); fig.text(0.805, 0.45, "=", fontsize=28, color=MUTED, ha="center", va="center", fontweight="bold")
    lead, tail = 2, 10; total = lead + 9 + tail

    def update(f):
        k = min(9, max(0, f - lead + 1))
        grid_nums(ax_i, I5, "gray", 0, 5, fs=12); ax_i.set_title("Вхід", fontsize=12, fontweight="bold", color=INK, pad=6)
        M = np.full((9, 9), np.nan); M[:k] = Xm[:k]
        ax_x.clear(); m = np.ma.masked_invalid(M); cm = plt.get_cmap("gray").copy(); cm.set_bad("white")
        ax_x.imshow(m, cmap=cm, vmin=0, vmax=5, interpolation="nearest", aspect="auto")
        for r in range(k):
            for c in range(9): ax_x.text(c, r, str(int(M[r, c])), ha="center", va="center", fontsize=11, fontweight="bold", color="white" if M[r, c] < 2.5 else INK)
        for q in range(10): ax_x.axhline(q - .5, color="#94A3B8", lw=.8); ax_x.axvline(q - .5, color="#94A3B8", lw=.8)
        ax_x.set_yticks(range(9)); ax_x.set_yticklabels(labels, fontsize=9, color=MUTED); ax_x.set_xticks([])
        for s in ax_x.spines.values(): s.set_visible(False)
        ax_x.set_title("X: ділянки, розгорнуті в рядки", fontsize=12, fontweight="bold", color=INK, pad=6)
        grid_nums(ax_w, w[:, None].astype(float), "RdYlGn", -2, 2, fmt=lambda v: f"{int(v)}", fs=11); ax_w.set_title("w", fontsize=12, fontweight="bold", color=CYAN, pad=6)
        O = np.full((9, 1), np.nan); O[:k, 0] = o[:k]
        ax_o.clear(); mo = np.ma.masked_invalid(O); cm2 = plt.get_cmap("RdYlGn").copy(); cm2.set_bad("white")
        ax_o.imshow(mo, cmap=cm2, vmin=-15, vmax=15, interpolation="nearest", aspect="auto")
        for r in range(k): ax_o.text(0, r, f"{int(O[r, 0]):+d}", ha="center", va="center", fontsize=11, fontweight="bold", color=INK)
        for q in range(10): ax_o.axhline(q - .5, color="#94A3B8", lw=.8)
        ax_o.set_xticks([]); ax_o.set_yticks([])
        for s in ax_o.spines.values(): s.set_visible(False)
        ax_o.set_title("X · w", fontsize=12, fontweight="bold", color=GREEN, pad=6)
        if 1 <= k <= 9 and f < lead + 9 + 1:
            i, j = divmod(k - 1, 3); ax_i.add_patch(patches.Rectangle((j - .5, i - .5), 3, 3, fill=False, edgecolor=CYAN, lw=4))
            ax_x.add_patch(patches.Rectangle((-.5, k - 1.5), 9, 1, fill=False, edgecolor=AMBER, lw=3))
            foot.set_text(f"позиція ({i}, {j}): ділянка стає рядком {k} матриці, відгук = {int(o[k - 1]):+d}")
        elif k == 0: foot.set_text("Розгорнемо кожну ділянку 3×3 в рядок із 9 чисел")
        else: foot.set_text("Усі 9 позицій: карта ознак — це один добуток матриці на вектор")

    save_video(fig, update, total, "anim-01-im2col", 4, total - 1)

def vid_learning():
    ws, ls = get("Собель X"); steps = np.unique(np.round(np.geomspace(1, 601, 44)).astype(int) - 1)
    steps = np.concatenate([steps, [600] * 8])
    target = np.array(TARGETS["Собель X"], float); tmap = fmap(target)
    fig = plt.figure(figsize=(13, 5.8)); fig.patch.set_facecolor("white")
    ax_k = fig.add_axes([0.03, 0.30, 0.19, 0.19 * 13 / 5.8 * 0.0 + 0.40]); ax_m = fig.add_axes([0.30, 0.20, 0.22, 0.58]); ax_t = fig.add_axes([0.56, 0.20, 0.22, 0.58]); ax_l = fig.add_axes([0.83, 0.20, 0.15, 0.58])
    head = fig.text(0.5, 0.93, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.255, 0.47, "→", fontsize=28, color=MUTED, ha="center", va="center", fontweight="bold")

    def update(f):
        s = int(steps[min(f, len(steps) - 1)])
        kpanel(ax_k, ws[s], "Ядро (навчається)", CYAN, 11, lim=2)
        mpanel(ax_m, fmap(ws[s]), "Карта ознак «7»", INK); mpanel(ax_t, tmap, "Ціль: Собель X", GREEN)
        ax_l.clear(); ax_l.semilogy(np.arange(s + 1), ls[:s + 1], color=CYAN, lw=2.5); ax_l.set_xlim(0, 600); ax_l.set_ylim(1e-14, 3)
        ax_l.set_title("Втрата", fontsize=12, fontweight="bold", color=INK, pad=6); ax_l.tick_params(labelsize=8)
        for sp in ("top", "right"): ax_l.spines[sp].set_visible(False)
        head.set_text(f"Крок навчання {s}: втрата {ls[s]:.2g}")

    save_video(fig, update, len(steps), "anim-02-learning-sobel", 6, len(steps) - 1)

def vid_four():
    names = list(TARGETS); steps = np.unique(np.round(np.geomspace(1, 601, 40)).astype(int) - 1); steps = np.concatenate([steps, [600] * 8])
    fig, axs = plt.subplots(2, 4, figsize=(13, 6.0)); fig.patch.set_facecolor("white")
    fig.subplots_adjust(top=0.78, bottom=0.08, hspace=0.45, wspace=0.2)
    head = fig.suptitle("", fontsize=15, fontweight="bold", color=INK, y=0.96)

    def update(f):
        s = int(steps[min(f, len(steps) - 1)])
        for c, n in enumerate(names):
            ws, ls = get(n)
            kpanel(axs[0, c], np.array(TARGETS[n], float), f"ціль: {n}", GREEN, 10, lim=2)
            kpanel(axs[1, c], ws[s], f"навчається, втрата {ls[s]:.1g}", CYAN, 10, lim=2)
        head.set_text(f"Чотири ядра навчаються одночасно — крок {s}")

    save_video(fig, update, len(steps), "anim-03-four-kernels", 6, len(steps) - 1)

def vid_eight():
    layer, ks, maps = rand_kernels(); lim = float(np.abs(maps).max())
    fig = plt.figure(figsize=(13, 5.6)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.02, 0.18, 0.2, 0.62]); ax_k = fig.add_axes([0.27, 0.40, 0.1, 0.24])
    cells = [fig.add_axes([0.45 + (k % 4) * 0.135, 0.52 - (k // 4) * 0.36, 0.12, 0.30]) for k in range(8)]
    fig.text(0.5, 0.92, "Вісім ядер — вісім карт ознак, складених у стос [8, 26, 26]", ha="center", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.40, 0.52, "→", fontsize=30, color=MUTED, ha="center", va="center", fontweight="bold")
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    per, lead, tail = 3, 2, 10; total = lead + 8 * per + tail

    def update(f):
        k = (f - lead) // per if f >= lead else -1; k = min(k, 7)
        ax_i.clear(); ax_i.imshow(seven_np, cmap="gray", interpolation="nearest"); ax_i.set_xticks([]); ax_i.set_yticks([]); ax_i.set_title("Вхід 28×28", fontsize=12, fontweight="bold", color=INK, pad=6)
        if k >= 0: kpanel(ax_k, ks[k], f"ядро {k + 1}", CYAN, 9, lim=0.35)
        else: ax_k.clear(); ax_k.axis("off")
        for q, ax in enumerate(cells):
            ax.clear()
            if q <= k: mpanel(ax, maps[q], f"карта {q + 1}", INK, lim=lim)
            else: ax.axis("off")
        foot.set_text("Кожне ядро шукає свою ознаку" if k < 7 else "Результат: 8 карт ознак — вісім «каналів» нового зображення")

    save_video(fig, update, total, "anim-04-eight-kernels", 4, total - 1)

if __name__ == "__main__":
    for n in TARGETS: get(n)
    img01(); img02(); img03(); img04(); img05(); img06(); img07(); img08()
    vid_im2col(); vid_learning(); vid_four(); vid_eight()
