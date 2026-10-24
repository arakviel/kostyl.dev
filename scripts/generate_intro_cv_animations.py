"""
Matplotlib GIF animations for content/16.ai-python/15.cnn-image-classification/01.intro-computer-vision.md
Target: public/videos/ai-python/cnn-image-classification/intro-computer-vision/
- anim-01-zoom-into-pixels.gif : MNIST "7" -> zoom -> raw pixel numbers
- anim-02-rgb-channels.gif     : 4x4 photo patch splits into R, G, B matrices and merges back
- anim-03-flatten.gif          : 28x28 digit unrolled row by row; vertical neighbours end up 28 apart
- anim-04-shift-digit.gif      : digit "3" shifts 0..5 px; flattened vector and overlap counter
Sources: temp/mnist.npz, sklearn flower.jpg
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

plt.rcParams['font.family'] = 'DejaVu Sans'
OUT = "public/videos/ai-python/cnn-image-classification/intro-computer-vision"
os.makedirs(OUT, exist_ok=True)
INK, MUTED, AMBER = "#0F172A", "#475569", "#F59E0B"
DPI = 80          # GIF fallback
VIDEO_DPI = 110   # mp4 / webm / poster
POSTER = {"anim-02-rgb-channels.gif": 30}   # frame used for the poster (default: last)

mn = np.load("temp/mnist.npz")


def save_gif(fig, update, n, name, fps):
    """Writes <stem>.mp4, <stem>.webm, <stem>.gif (fallback) and <stem>-poster.png."""
    from matplotlib.animation import FFMpegWriter
    stem = os.path.join(OUT, name[:-4])
    anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps)
    common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(stem + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(
        fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(stem + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(
        fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(stem + ".gif", dpi=DPI, writer=PillowWriter(fps=fps))
    update(POSTER.get(name, n - 1))
    fig.savefig(stem + "-poster.png", dpi=VIDEO_DPI, facecolor="white")
    plt.close(fig)
    print("saved", name[:-4], f"mp4 {os.path.getsize(stem + '.mp4') // 1024} KB, webm {os.path.getsize(stem + '.webm') // 1024} KB")


def ease(t):
    return t * t * (3 - 2 * t)


# 1. zoom into pixels ---------------------------------------------------------
def anim_zoom():
    img = mn["x_train"][101]
    r0, c0, size = 6, 10, 10
    fig, ax = plt.subplots(figsize=(7, 7.4))
    fig.patch.set_facecolor("white")
    ax.imshow(img, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    box = patches.Rectangle((c0 - .5, r0 - .5), size, size, fill=False, edgecolor=AMBER, linewidth=3)
    ax.add_patch(box)
    texts = []
    for r in range(r0, r0 + size):
        for c in range(c0, c0 + size):
            v = int(img[r, c])
            texts.append(ax.text(c, r, str(v), ha="center", va="center", fontsize=11, fontweight="bold",
                                 color="white" if v < 128 else INK, alpha=0))
    title = ax.set_title("", fontsize=15, fontweight="bold", color=INK, pad=12)
    hold0, zoom, fade, hold1 = 8, 22, 8, 14
    total = hold0 + zoom + fade + hold1
    x_full, x_crop = (-.5, 27.5), (c0 - .5, c0 + size - .5)
    y_full, y_crop = (27.5, -.5), (r0 + size - .5, r0 - .5)

    def update(f):
        if f < hold0:
            t, a, msg = 0, 0, "Цифра «7»: 784 пікселі"
        elif f < hold0 + zoom:
            t, a, msg = ease((f - hold0) / (zoom - 1)), 0, "Наближаємо…"
        else:
            t = 1
            a = min(1, (f - hold0 - zoom) / fade)
            msg = "Кожен піксель — число від 0 до 255"
        ax.set_xlim(x_full[0] + (x_crop[0] - x_full[0]) * t, x_full[1] + (x_crop[1] - x_full[1]) * t)
        ax.set_ylim(y_full[0] + (y_crop[0] - y_full[0]) * t, y_full[1] + (y_crop[1] - y_full[1]) * t)
        box.set_alpha(1 - t)
        for tx in texts:
            tx.set_alpha(a)
        title.set_text(msg)

    save_gif(fig, update, total, "anim-01-zoom-into-pixels.gif", 12)


# 2. RGB channels -------------------------------------------------------------
def anim_rgb():
    from sklearn.datasets import load_sample_image
    photo = load_sample_image("flower.jpg")
    patch = photo[222:226, 444:448]
    n = 4
    fig = plt.figure(figsize=(10, 4.6))
    fig.patch.set_facecolor("white")
    W, H, Y = 0.28, 0.28 * 10 / 4.6, 0.17
    centre = 0.36
    targets = [0.04, 0.36, 0.68]
    comp_ax = fig.add_axes([centre, Y, W, H])
    comp = comp_ax.imshow(patch, interpolation="nearest")
    comp_ax.set_xticks([]); comp_ax.set_yticks([])
    chans, ch_axes, ch_titles, ch_texts = [], [], [], []
    names = [("R: червоний", "#DC2626"), ("G: зелений", "#16A34A"), ("B: синій", "#2563EB")]
    for k in range(3):
        ax = fig.add_axes([centre, Y, W, H])
        tint = np.zeros((n, n, 3), dtype=np.uint8)
        tint[:, :, k] = patch[:, :, k]
        chans.append(ax.imshow(tint, interpolation="nearest", alpha=0))
        ax.set_xticks([]); ax.set_yticks([])
        ax.patch.set_alpha(0)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ch_axes.append(ax)
        ch_titles.append(ax.set_title(names[k][0], fontsize=13, fontweight="bold", color=names[k][1], alpha=0, pad=8))
        tl = []
        for r in range(n):
            for c in range(n):
                v = int(patch[r, c, k])
                tl.append(ax.text(c, r, str(v), ha="center", va="center", fontsize=11, fontweight="bold",
                                  color="white" if v > 128 else "#E2E8F0", alpha=0))
        ch_texts.append(tl)
    comp_title = comp_ax.set_title("Піксель = три числа [R, G, B]", fontsize=13, fontweight="bold", color=INK, pad=8)
    cap = fig.text(0.5, 0.05, "", ha="center", fontsize=13, color=MUTED, fontweight="bold")
    hold0, split, hold1, merge, hold2 = 8, 14, 14, 14, 4
    total = hold0 + split + hold1 + merge + hold2

    def update(f):
        if f < hold0:
            t, num, msg = 0, 0, "Ділянка 4×4 пікселі з фото жоржини: (4, 4, 3) — 48 чисел"
        elif f < hold0 + split:
            t, num, msg = ease((f - hold0) / (split - 1)), 0, "Розкладаємо на три канали…"
        elif f < hold0 + split + hold1:
            t = 1
            num = min(1, (f - hold0 - split) / 5)
            msg = "Три таблиці 4×4: по одному числу з кожного пікселя"
        elif f < hold0 + split + hold1 + merge:
            t = 1 - ease((f - hold0 - split - hold1) / (merge - 1))
            num, msg = 0, "Складаємо назад…"
        else:
            t, num, msg = 0, 0, "Кольорове фото = стос із трьох таблиць"
        a = min(1, t * 3)
        comp.set_alpha(1 - a)
        comp_title.set_alpha(1 - a)
        for k in range(3):
            ch_axes[k].set_position([centre + (targets[k] - centre) * t, Y, W, H])
            chans[k].set_alpha(a)
            ch_titles[k].set_alpha(1.0 if num > 0 else 0.0)
            for tx in ch_texts[k]:
                tx.set_alpha(num)
        cap.set_text(msg)

    save_gif(fig, update, total, "anim-02-rgb-channels.gif", 10)


# 3. flatten ------------------------------------------------------------------
def anim_flatten():
    img = mn["x_train"][12]
    vec = img.flatten().astype(float)
    fig = plt.figure(figsize=(8, 7))
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.25, 0.36, 0.5, 0.5 * 8 / 7])
    ax.imshow(img, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Картинка 28×28", fontsize=14, fontweight="bold", color=INK, pad=8)
    row_box = patches.Rectangle((-.5, -.5), 28, 1, fill=False, edgecolor=AMBER, linewidth=3)
    ax.add_patch(row_box)
    pair = [patches.Rectangle((14 - .5, 13 - .5), 1, 1, fill=False, edgecolor="#EF4444", linewidth=3, alpha=0),
            patches.Rectangle((14 - .5, 14 - .5), 1, 1, fill=False, edgecolor="#0EA5E9", linewidth=3, alpha=0)]
    for p_ in pair:
        ax.add_patch(p_)
    sx = fig.add_axes([0.04, 0.17, 0.92, 0.07])
    cmap = plt.get_cmap("gray").copy()
    cmap.set_bad("#F1F5F9")
    strip = sx.imshow(np.full((1, 784), np.nan), cmap=cmap, aspect="auto", vmin=0, vmax=255, interpolation="nearest")
    sx.set_yticks([]); sx.set_xticks([0, 783]); sx.set_xticklabels(["0", "783"], fontsize=10)
    sx.set_xlim(-.5, 783.5)
    sx.set_title("Вектор із 784 чисел (рядок за рядком)", fontsize=12, color=MUTED, pad=4)
    m1 = sx.axvline(13 * 28 + 14, color="#EF4444", linewidth=3, alpha=0)
    m2 = sx.axvline(14 * 28 + 14, color="#0EA5E9", linewidth=3, alpha=0)
    note = fig.text(0.5, 0.06, "", ha="center", fontsize=13, fontweight="bold", color=INK)
    hold = 16
    total = 28 + hold + 2

    def update(f):
        k = min(f, 27)
        row_box.set_xy((-.5, k - .5))
        shown = np.full(784, np.nan)
        shown[:(k + 1) * 28] = vec[:(k + 1) * 28]
        strip.set_data(shown.reshape(1, -1))
        if f < 28:
            note.set_text(f"Беремо рядок {k + 1} із 28 і дописуємо його в кінець вектора")
            for p_ in pair: p_.set_alpha(0)
            m1.set_alpha(0); m2.set_alpha(0)
        else:
            row_box.set_alpha(0)
            for p_ in pair: p_.set_alpha(1)
            m1.set_alpha(1); m2.set_alpha(1)
            note.set_text("Сусіди по вертикалі в картинці — на позиціях 378 і 406: між ними 28 чисел")

    save_gif(fig, update, total, "anim-03-flatten.gif", 8)


# 4. shift digit ----------------------------------------------------------------
def anim_shift():
    img = mn["x_train"][12]
    steps = list(range(6))
    fig = plt.figure(figsize=(10, 6.4))
    fig.patch.set_facecolor("white")
    axA = fig.add_axes([0.04, 0.38, 0.30, 0.30 * 10 / 6.4])
    axB = fig.add_axes([0.36, 0.38, 0.30, 0.30 * 10 / 6.4])
    axC = fig.add_axes([0.68, 0.38, 0.30, 0.30 * 10 / 6.4])
    for ax_, t in [(axA, "Оригінал"), (axB, "Зсунута цифра"), (axC, "Збіг яскравих пікселів")]:
        ax_.set_xticks([]); ax_.set_yticks([])
        ax_.set_title(t, fontsize=13, fontweight="bold", color=INK, pad=6)
    axA.imshow(img, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    imB = axB.imshow(img, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    imC = axC.imshow(np.zeros(img.shape + (3,)), interpolation="nearest")
    v0 = img.flatten()
    stripA = fig.add_axes([0.20, 0.17, 0.76, 0.05])
    stripB = fig.add_axes([0.20, 0.07, 0.76, 0.05])
    for s_, t in [(stripA, "Вектор\nоригіналу"), (stripB, "Вектор\nзсунутої")]:
        s_.set_yticks([]); s_.set_xticks([])
        s_.set_ylabel(t, rotation=0, ha="right", va="center", fontsize=10, color=MUTED)
    stripA.imshow(v0.reshape(1, -1), cmap="gray", aspect="auto", vmin=0, vmax=255, interpolation="nearest")
    imSB = stripB.imshow(v0.reshape(1, -1), cmap="gray", aspect="auto", vmin=0, vmax=255, interpolation="nearest")
    head = fig.text(0.5, 0.95, "", ha="center", fontsize=16, fontweight="bold", color=INK)
    stat = fig.text(0.5, 0.28, "", ha="center", fontsize=13, fontweight="bold", color="#B91C1C")
    per = 4
    total = per * len(steps) + 10

    def update(f):
        s = steps[min(f // per, len(steps) - 1)]
        sh = np.roll(img, s, axis=1)
        a, b = img > 128, sh > 128
        both, oa, ob = a & b, a & ~b, ~a & b
        ov = np.zeros(img.shape + (3,))
        ov[oa] = (0.23, 0.51, 0.96); ov[ob] = (0.98, 0.45, 0.09); ov[both] = (0.06, 0.73, 0.51)
        imB.set_data(sh); imC.set_data(ov); imSB.set_data(sh.flatten().reshape(1, -1))
        ch = int((v0 != sh.flatten()).sum())
        head.set_text(f"Зсув на {s} пікс." if s else "Без зсуву")
        stat.set_text(f"збіг яскравих: {int(both.sum())} із {int(a.sum())}  |  змінено позицій вектора: {ch} із 784")

    save_gif(fig, update, total, "anim-04-shift-digit.gif", 4)


if __name__ == "__main__":
    anim_zoom(); anim_rgb(); anim_flatten(); anim_shift()
