"""
Media for content/16.ai-python/15.cnn-image-classification/04.filters-what-kernel-sees.md
Images -> public/images/ai-python/cnn-image-classification/filters-what-kernel-sees/
  01.png old stroke kernel on real MNIST 7 (fails)   02.png Sobel X: reading the map (+/-/0, ReLU)
  03.png row profile: brightness vs Sobel X response 04.png six classic filters on the 7
  05.png Sobel X, Sobel Y, gradient magnitude         06.png the same ideas on a real photo (grayscale)
Videos -> public/videos/ai-python/cnn-image-classification/filters-what-kernel-sees/
  anim-01-sobel-scan, anim-02-filter-gallery
Data: temp/mnist.npz (x_train[101] == 7), sklearn flower.jpg
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from scipy.signal import correlate2d
from sklearn.datasets import load_sample_image

plt.rcParams['font.family'] = 'DejaVu Sans'
IMG = "public/images/ai-python/cnn-image-classification/filters-what-kernel-sees"
VID = "public/videos/ai-python/cnn-image-classification/filters-what-kernel-sees"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444"
DPI, VIDEO_DPI = 80, 110

mn = np.load("temp/mnist.npz")
assert mn["y_train"][101] == 7
seven = mn["x_train"][101].astype(float) / 255
photo = load_sample_image("flower.jpg").astype(float).mean(axis=2) / 255

def conv(im, k): return correlate2d(im, k, mode="valid")
K_STROKE = np.array([[-1, 1, -1]] * 3)
K_ID = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float)
K_BLUR = np.ones((3, 3)) / 9
K_SHARP = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=float)
SX = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
SY = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
LIM = 4.0

def kernel_panel(ax, k, title=None, fs=13, frac=False):
    ax.clear()
    ax.imshow(k, cmap="RdYlGn", vmin=-2.2, vmax=2.2, interpolation="nearest")
    for i in range(3):
        for j in range(3):
            t = ("1/9" if frac else (f"{int(k[i, j])}" if float(k[i, j]).is_integer() else f"{k[i, j]:.2f}"))
            ax.text(j, i, t, ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)
    for q in range(4):
        ax.axhline(q - .5, color="#94A3B8", lw=.8); ax.axvline(q - .5, color="#94A3B8", lw=.8)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    if title: ax.set_title(title, fontsize=12, fontweight="bold", color=CYAN, pad=6)

def show(ax, data, kind, title, tcolor=INK, fs=12):
    ax.clear()
    if kind == "gray": im = ax.imshow(data, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
    elif kind == "div": im = ax.imshow(data, cmap="RdYlGn", vmin=-LIM, vmax=LIM, interpolation="nearest")
    elif kind == "pos": im = ax.imshow(data, cmap="Greens", vmin=0, vmax=LIM, interpolation="nearest")
    elif kind == "mag": im = ax.imshow(data, cmap="gray", vmin=0, vmax=LIM, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_edgecolor("#CBD5E1")
    ax.set_title(title, fontsize=fs, fontweight="bold", color=tcolor, pad=8)
    return im

def save_png(fig, name):
    fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)

def colorbar(fig, im, ax, label):
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04); cb.set_label(label, fontsize=10, color=MUTED); cb.ax.tick_params(labelsize=9)

# --- images -----------------------------------------------------------------------
def img01():
    o = conv(seven, K_STROKE)
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.8), gridspec_kw={"width_ratios": [1, 0.55, 1]})
    show(axs[0], seven, "gray", "Вхід: цифра «7»")
    kernel_panel(axs[1], K_STROKE, "Ядро з минулих лекцій")
    im = show(axs[2], o, "div", f"Карта ознак: максимум {o.max():.2f}", RED)
    colorbar(fig, im, axs[2], "відгук")
    fig.suptitle("Ядро «тонка вертикальна риска» на справжній цифрі: майже всюди мінус", fontsize=14, fontweight="bold", color=INK, y=1.03)
    save_png(fig, "01.png")

def img02():
    o = conv(seven, SX)
    fig, axs = plt.subplots(1, 4, figsize=(17, 4.6), gridspec_kw={"width_ratios": [1, 0.5, 1, 1]})
    show(axs[0], seven, "gray", "Вхід: цифра «7»")
    kernel_panel(axs[1], SX, "Ядро Собеля (X)")
    im = show(axs[2], o, "div", "Карта ознак", INK); colorbar(fig, im, axs[2], "червоне — мінус, зелене — плюс")
    im2 = show(axs[3], np.maximum(o, 0), "pos", "Після ReLU: лише «знайдено»", GREEN); colorbar(fig, im2, axs[3], "відгук ≥ 0")
    fig.suptitle("Читаємо карту ознак: плюс, мінус і нуль", fontsize=14, fontweight="bold", color=INK, y=1.03)
    save_png(fig, "02.png")

def img03():
    r = 12
    o = conv(seven, SX)[r - 1]
    xs = np.arange(28); xo = np.arange(26) + 1
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 6.2), sharex=True, gridspec_kw={"height_ratios": [1, 1]})
    a1.fill_between(xs, seven[r], color="#94A3B8", alpha=.5, step="mid"); a1.step(xs, seven[r], where="mid", color=INK, lw=2)
    a1.set_ylabel("яскравість", fontsize=11, color=MUTED); a1.set_title(f"Рядок {r} цифри «7»", fontsize=12.5, fontweight="bold", color=INK, loc="left")
    cols = [GREEN if v > 0 else RED for v in o]
    a2.bar(xo, o, color=cols, width=.8); a2.axhline(0, color=INK, lw=1)
    a2.set_ylabel("відгук Собеля (X)", fontsize=11, color=MUTED); a2.set_xlabel("номер стовпця", fontsize=11, color=MUTED)
    a2.set_title("Плюс — яскравість зростає зліва направо, мінус — спадає", fontsize=12.5, fontweight="bold", color=INK, loc="left")
    up = int(np.argmax(o)); dn = int(np.argmin(o))
    a2.annotate("темне → світле", xy=(xo[up], o[up]), xytext=(xo[up] - 6, o[up] - .2), fontsize=11, color=GREEN, fontweight="bold", arrowprops=dict(arrowstyle="->", color=GREEN))
    a2.annotate("світле → темне", xy=(xo[dn], o[dn]), xytext=(xo[dn] + 1.5, o[dn] + .6), fontsize=11, color=RED, fontweight="bold", arrowprops=dict(arrowstyle="->", color=RED))
    for a in (a1, a2):
        for s in ("top", "right"): a.spines[s].set_visible(False)
    save_png(fig, "03.png")

FILTERS = [("Тотожність", K_ID, "gray", False), ("Розмиття", K_BLUR, "gray", True), ("Загострення", K_SHARP, "gray", False),
           ("Собель X", SX, "div", False), ("Собель Y", SY, "div", False)]

def img04():
    fig, axs = plt.subplots(2, 5, figsize=(17, 6.6))
    for c, (name, k, kind, frac) in enumerate(FILTERS):
        kernel_panel(axs[0, c], k, f"{name}\nΣ ваг = {k.sum():.0f}", frac=frac)
        show(axs[1, c], conv(seven, k) if kind == "div" else np.clip(conv(seven, k), 0, 1), kind, "")
    fig.suptitle("П'ять класичних ядер на одній і тій самій цифрі", fontsize=14, fontweight="bold", color=INK, y=1.0)
    save_png(fig, "04.png")

def img05():
    gx, gy = conv(seven, SX), conv(seven, SY); mag = np.hypot(gx, gy)
    fig, axs = plt.subplots(1, 4, figsize=(17, 4.6))
    show(axs[0], seven, "gray", "Вхід")
    show(axs[1], gx, "div", "Собель X: вертикальні краї")
    show(axs[2], gy, "div", "Собель Y: горизонтальні краї")
    show(axs[3], mag, "mag", "Сила краю √(X² + Y²)", AMBER)
    fig.suptitle("Два ядра разом дають контур цифри", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "05.png")

def img06():
    gx, gy = conv(photo, SX), conv(photo, SY); mag = np.hypot(gx, gy)
    items = [("Сірий знімок", photo[1:-1, 1:-1], "gray"), ("Собель X", gx, "div"), ("Собель Y", gy, "div"),
             ("Сила краю", mag, "mag"), ("Розмиття", conv(photo, K_BLUR), "gray"), ("Загострення", np.clip(conv(photo, K_SHARP), 0, 1), "gray")]
    global LIM
    old = LIM; LIM = 1.5
    fig, axs = plt.subplots(2, 3, figsize=(15, 7.4))
    for ax, (t, d, kind) in zip(axs.ravel(), items): show(ax, d, kind, t)
    LIM = old
    fig.suptitle("Ті самі ядра на справжньому фото", fontsize=14, fontweight="bold", color=INK, y=0.98)
    save_png(fig, "06.png")

# --- videos -----------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem)
    anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps)
    common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps))
    update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_scan():
    full = conv(seven, SX); n = full.size; per = 13
    fig = plt.figure(figsize=(12, 6)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.12, 0.30, 0.60]); ax_k = fig.add_axes([0.385, 0.34, 0.11, 0.22]); ax_o = fig.add_axes([0.58, 0.12, 0.33, 0.66])
    fig.text(0.5, 0.92, "Ядро Собеля проходить усю цифру і малює карту країв", ha="center", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.54, 0.45, "→", ha="center", va="center", fontsize=34, color=MUTED, fontweight="bold")
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    sm = plt.cm.ScalarMappable(cmap="RdYlGn", norm=plt.Normalize(-LIM, LIM)); cax = fig.add_axes([0.93, 0.12, 0.012, 0.66])
    cb = fig.colorbar(sm, cax=cax); cb.ax.tick_params(labelsize=9)
    total = n // per + 8

    def update(f):
        k = min(n, (f + 1) * per)
        flat = np.full(n, np.nan); flat[:k] = full.flatten()[:k]
        show(ax_i, seven, "gray", "Вхід")
        i, j = divmod(k - 1, 26)
        ax_i.add_patch(patches.Rectangle((j - .5, i - .5), 3, 3, fill=False, edgecolor=CYAN, lw=2.5))
        kernel_panel(ax_k, SX, "Ядро", fs=11)
        ax_o.clear(); m = np.ma.masked_invalid(flat.reshape(26, 26))
        cm = plt.get_cmap("RdYlGn").copy(); cm.set_bad("white")
        ax_o.imshow(m, cmap=cm, vmin=-LIM, vmax=LIM, interpolation="nearest"); ax_o.set_xticks([]); ax_o.set_yticks([])
        ax_o.set_title("Карта ознак 26×26", fontsize=12, fontweight="bold", color=GREEN, pad=8)
        foot.set_text(f"позицій пораховано: {k} із {n}" if k < n else "Готово: зелене — темне→світле, червоне — світле→темне")

    save_video(fig, update, total, "anim-01-sobel-scan", 8, total - 1)

def vid_gallery():
    stages = [(nm, k, kind, fr, conv(seven, k) if kind == "div" else np.clip(conv(seven, k), 0, 1)) for nm, k, kind, fr in FILTERS]
    gx, gy = conv(seven, SX), conv(seven, SY)
    stages.append(("Сила краю (Собель X + Y)", None, "mag", False, np.hypot(gx, gy)))
    hold = 10
    fig = plt.figure(figsize=(12, 5.6)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.12, 0.28, 0.60 * 0.95]); ax_k = fig.add_axes([0.37, 0.36, 0.12, 0.26]); ax_o = fig.add_axes([0.58, 0.12, 0.32, 0.72])
    head = fig.text(0.5, 0.92, "", ha="center", fontsize=16, fontweight="bold", color=INK)
    sumt = fig.text(0.43, 0.24, "", ha="center", fontsize=15, fontweight="bold", color=AMBER)
    fig.text(0.535, 0.49, "→", ha="center", va="center", fontsize=34, color=MUTED, fontweight="bold")

    def update(f):
        nm, k, kind, fr, res = stages[min(f // hold, len(stages) - 1)]
        show(ax_i, seven, "gray", "Вхід")
        ax_k.clear()
        if k is not None:
            kernel_panel(ax_k, k, "Ядро", fs=11, frac=fr); sumt.set_text(f"Σ ваг = {k.sum():.0f}")
        else:
            ax_k.axis("off"); ax_k.text(0.5, 0.5, "√(X² + Y²)", ha="center", va="center", fontsize=14, fontweight="bold", color=INK); sumt.set_text("")
        show(ax_o, res, kind, "Результат"); head.set_text(nm)

    save_video(fig, update, hold * len(stages), "anim-02-filter-gallery", 4, hold * 4 + 3)

if __name__ == "__main__":
    img01(); img02(); img03(); img04(); img05(); img06(); vid_scan(); vid_gallery()
