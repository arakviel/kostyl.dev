"""
Matplotlib GIF animations for content/16.ai-python/15.cnn-image-classification/02.why-convolution.md
Target: public/videos/ai-python/cnn-image-classification/why-convolution/
- anim-01-neuron-sum.gif          : patch x weights, cell by cell, running sum (3 patches)
- anim-02-shift-breaks-dense.gif  : whole-image neuron: line moves, response 6 -> 0
- anim-03-detector-slides.gif     : 3x3 detector slides over the image, response map fills
- anim-04-line-moves-peak.gif     : line moves; peak of response map follows it, maximum stays 3
- anim-05-dense-to-shared.gif     : dense -> local -> shared weights (1D sketch)
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgba
from matplotlib.animation import FuncAnimation, PillowWriter

plt.rcParams['font.family'] = 'DejaVu Sans'
OUT = "public/videos/ai-python/cnn-image-classification/why-convolution"
os.makedirs(OUT, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444"
DPI = 80          # GIF fallback
VIDEO_DPI = 110   # mp4 / webm / poster
POSTER = {"anim-01-neuron-sum.gif": 8, "anim-02-shift-breaks-dense.gif": 0}   # frame used for the poster (default: last)

K = np.array([[-1, 1, -1]] * 3)
def line_image(col):
    im = np.zeros((6, 6), dtype=int); im[:, col] = 1; return im
def response_map(im):
    return np.array([[int((im[i:i + 3, j:j + 3] * K).sum()) for j in range(4)] for i in range(4)])
def signed(v):
    return "0" if v == 0 else f"{v:+d}"

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

def grid(ax, M, cmap, vmin, vmax, fmt=str, fs=14):
    """Draw matrix M; NaN cells stay blank white."""
    ax.clear()
    masked = np.ma.masked_invalid(M.astype(float))
    cm = plt.get_cmap(cmap).copy(); cm.set_bad("white")
    ax.imshow(masked, cmap=cm, vmin=vmin, vmax=vmax, interpolation="nearest")
    r, c = M.shape
    for i in range(r):
        for j in range(c):
            v = M[i, j]
            if np.isnan(v):
                continue
            col = "white" if (cmap == "gray" and v < 0.5) else INK
            ax.text(j, i, fmt(int(v)), ha="center", va="center", fontsize=fs, fontweight="bold", color=col)
    for k in range(r + 1): ax.axhline(k - .5, color="#94A3B8", lw=.8)
    for k in range(c + 1): ax.axvline(k - .5, color="#94A3B8", lw=.8)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

def mark(ax, i, j, color=AMBER, lw=3, h=1, w=1):
    ax.add_patch(patches.Rectangle((j - .5, i - .5), w, h, fill=False, edgecolor=color, lw=lw))


# 1. neuron sum -----------------------------------------------------------------
def anim_neuron_sum():
    cases = [("Штрих посередині", np.array([[0, 1, 0]] * 3)),
             ("Штрих збоку", np.array([[0, 0, 1]] * 3)),
             ("Порожньо", np.zeros((3, 3), dtype=int))]
    fig, axs = plt.subplots(1, 3, figsize=(10, 4.6))
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(top=0.78, bottom=0.2, wspace=0.15)
    head = fig.suptitle("", fontsize=16, fontweight="bold", color=INK, y=0.97)
    foot = fig.text(0.5, 0.06, "", ha="center", fontsize=16, fontweight="bold", color=INK)
    reveal, hold = 9, 6
    per = reveal + hold
    total = per * len(cases)

    def update(f):
        name, P = cases[f // per]
        k = min(f % per, reveal - 1) + 1 if f % per < reveal else reveal
        prod = np.full(9, np.nan)
        flat = (P * K).flatten()
        prod[:k] = flat[:k]
        grid(axs[0], P, "gray", 0, 1)
        grid(axs[1], K, "RdYlGn", -2, 2)
        grid(axs[2], prod.reshape(3, 3), "RdYlGn", -2, 2)
        axs[0].set_title("Ділянка 3×3", fontsize=13, color=INK, pad=6)
        axs[1].set_title("Ваги нейрона", fontsize=13, color=INK, pad=6)
        axs[2].set_title("Ділянка × ваги", fontsize=13, color=INK, pad=6)
        if k <= 9:
            i, j = divmod(k - 1, 3)
            for ax in axs: mark(ax, i, j)
        s = int(np.nansum(prod))
        color = GREEN if s > 0 else (RED if s < 0 else MUTED)
        head.set_text(name)
        foot.set_text(f"сума після {k} з 9 клітинок = {signed(s)}")
        foot.set_color(color)

    save_gif(fig, update, total, "anim-01-neuron-sum.gif", 4)


# 2. shift breaks dense -----------------------------------------------------------
def anim_shift_breaks_dense():
    W = np.zeros((6, 6), dtype=int); W[:, 2] = 1
    seq = [2] * 4 + [3] * 2 + [4] * 2 + [5] * 2 + [4] * 1 + [3] * 1 + [2] * 3
    fig = plt.figure(figsize=(11, 4.8))
    fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.18, 0.28, 0.28 * 11 / 4.8 * 0.62])
    ax_w = fig.add_axes([0.35, 0.18, 0.28, 0.28 * 11 / 4.8 * 0.62])
    ax_b = fig.add_axes([0.70, 0.22, 0.27, 0.5])
    ax_i.set_position([0.03, 0.15, 0.28, 0.28 * 11 / 4.8 * 1.0 * 0.95 if False else 0.62])
    ax_w.set_position([0.35, 0.15, 0.28, 0.62])
    ttl = fig.text(0.5, 0.94, "Нейрон на всю картинку: штрих пересувається", ha="center", fontsize=15, fontweight="bold", color=INK)
    val = fig.text(0.5, 0.04, "", ha="center", fontsize=17, fontweight="bold")

    def update(f):
        c = seq[f]
        im = line_image(c)
        grid(ax_i, im, "gray", 0, 1, fs=12)
        ax_i.set_title(f"Штрих у стовпці {c}", fontsize=13, color=INK, pad=6)
        grid(ax_w, W, "RdYlGn", -2, 2, fs=12)
        ax_w.set_title("Шаблон: стовпець 2", fontsize=13, color=INK, pad=6)
        resp = int((im * W).sum())
        ax_b.clear()
        vals = [6 if k == 2 else 0 for k in range(6)]
        bars = ax_b.bar(range(6), vals, color=["#CBD5E1"] * 6)
        bars[c].set_color(GREEN if resp else RED)
        ax_b.set_ylim(0, 7.5); ax_b.set_xticks(range(6))
        ax_b.set_xlabel("позиція штриха (стовпець)", fontsize=11, color=MUTED)
        ax_b.set_title("Відгук нейрона", fontsize=13, color=INK, pad=6)
        for s in ("top", "right"): ax_b.spines[s].set_visible(False)
        val.set_text(f"відгук = {resp}")
        val.set_color(GREEN if resp else RED)

    save_gif(fig, update, len(seq), "anim-02-shift-breaks-dense.gif", 3)


# 3. detector slides ---------------------------------------------------------------
def anim_detector_slides():
    A = line_image(2)
    R = response_map(A).astype(float)
    pos = [(i, j) for i in range(4) for j in range(4)]
    fig = plt.figure(figsize=(11, 5))
    fig.patch.set_facecolor("white")
    ax_img = fig.add_axes([0.03, 0.14, 0.38, 0.38 * 11 / 5])
    ax_img.set_position([0.03, 0.12, 0.34, 0.68])
    ax_k = fig.add_axes([0.42, 0.40, 0.14, 0.14 * 11 / 5 * 0.0 + 0.33])
    ax_r = fig.add_axes([0.64, 0.12, 0.33, 0.68])
    fig.text(0.5, 0.94, "Один детектор ковзає по всій картинці", ha="center", fontsize=15, fontweight="bold", color=INK)
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    arrow = fig.text(0.585, 0.43, "→", ha="center", va="center", fontsize=34, color=CYAN, fontweight="bold")
    pre, post = 3, 10
    total = pre + len(pos) * 2 + post

    def update(f):
        n_done = max(0, min(len(pos), (f - pre) // 2 + 1)) if f >= pre else 0
        cur = pos[min(n_done, len(pos)) - 1] if n_done else None
        grid(ax_img, A, "gray", 0, 1, fs=12)
        ax_img.set_title("Зображення 6×6", fontsize=13, color=INK, pad=6)
        grid(ax_k, K, "RdYlGn", -2, 2, fs=11)
        ax_k.set_title("Детектор 3×3", fontsize=12, color=CYAN, pad=5)
        M = np.full((4, 4), np.nan)
        for (i, j) in pos[:n_done]:
            M[i, j] = R[i, j]
        grid(ax_r, M, "RdYlGn", -3, 3, fmt=signed, fs=14)
        ax_r.set_title("Карта відгуків 4×4", fontsize=13, color=INK, pad=6)
        if cur:
            mark(ax_img, cur[0], cur[1], color=CYAN, lw=4, h=3, w=3)
            mark(ax_r, cur[0], cur[1])
            foot.set_text(f"позиція ({cur[0]}, {cur[1]}): відгук = {signed(int(R[cur]))}")
        else:
            foot.set_text("Покладемо детектор на першу ділянку…")
        if n_done == len(pos) and f >= pre + len(pos) * 2:
            for (i, j) in zip(*np.where(R == R.max())):
                mark(ax_r, i, j, color=AMBER, lw=3)
            foot.set_text("Карта готова: пік +3 вказує, де стоїть штрих")

    save_gif(fig, update, total, "anim-03-detector-slides.gif", 5)


# 4. line moves, peak follows ------------------------------------------------------
def anim_peak():
    W = np.zeros((6, 6), dtype=int); W[:, 2] = 1
    seq = [1, 2, 3, 4]   # centre columns only: a 3x3 detector cannot centre on columns 0 and 5
    per = 6
    fig = plt.figure(figsize=(12, 5.2))
    fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.02, 0.12, 0.27, 0.62])
    ax_r = fig.add_axes([0.33, 0.12, 0.27, 0.62])
    ax_k = fig.add_axes([0.70, 0.46, 0.13, 0.28])
    ax_t = fig.add_axes([0.64, 0.06, 0.34, 0.34]); ax_t.axis("off")
    fig.text(0.5, 0.93, "Штрих пересувається, а детектор його все одно знаходить", ha="center", fontsize=15, fontweight="bold", color=INK)
    total = per * len(seq) + 4

    def update(f):
        c = seq[min(f // per, len(seq) - 1)]
        im = line_image(c)
        R = response_map(im)
        grid(ax_i, im, "gray", 0, 1, fs=12)
        ax_i.set_title(f"Штрих у стовпці {c}", fontsize=13, color=INK, pad=6)
        grid(ax_r, R, "RdYlGn", -3, 3, fmt=signed, fs=14)
        ax_r.set_title("Карта відгуків детектора", fontsize=13, color=INK, pad=6)
        grid(ax_k, K, "RdYlGn", -2, 2, fs=12)
        ax_k.set_title("Ваги детектора 3×3", fontsize=12, color=CYAN, pad=6)
        for (i, j) in zip(*np.where(R == R.max())):
            mark(ax_r, i, j)
        i0, j0 = [int(v[0]) for v in np.where(R == R.max())]
        mark(ax_i, i0, j0, color=CYAN, lw=4, h=3, w=3)   # window where the detector fires
        ax_t.clear(); ax_t.axis("off")
        ax_t.text(0, 0.80, f"максимум карти = {R.max()}", fontsize=15, fontweight="bold", color=GREEN, transform=ax_t.transAxes)
        ax_t.text(0, 0.46, "Нейрон на всю картинку", fontsize=13, fontweight="bold", color=RED, transform=ax_t.transAxes)
        d = int((im * W).sum())
        ax_t.text(0, 0.24, f"відгук = {d}", fontsize=15, fontweight="bold", color=GREEN if d else RED, transform=ax_t.transAxes)
        ax_t.text(0, 0.02, "(шаблон лише для стовпця 2)", fontsize=10, color=MUTED, transform=ax_t.transAxes)

    save_gif(fig, update, total, "anim-04-line-moves-peak.gif", 5)


# 5. dense -> local -> shared -------------------------------------------------------
def anim_dense_to_shared():
    wcol = ["#EF4444", "#10B981", "#3B82F6"]
    grey = to_rgba("#94A3B8")
    xs_in, xs_out = np.arange(6), np.arange(4) + 1
    conns = []
    for o in range(4):
        for i in range(6):
            local = i in (o, o + 1, o + 2)
            conns.append((i, o, local, i - o if local else None))
    fig, ax = plt.subplots(figsize=(8, 5.4))
    fig.patch.set_facecolor("white")
    ax.set_xlim(-.6, 5.6); ax.set_ylim(-.3, 1.3); ax.axis("off")
    lines = [ax.plot([i, xs_out[o]], [0, 1], lw=1.5, zorder=1)[0] for i, o, _, _ in conns]
    ax.scatter(xs_in, np.zeros(6), s=520, color="white", edgecolor=INK, zorder=3, lw=1.8)
    ax.scatter(xs_out, np.ones(4), s=520, color="#DBEAFE", edgecolor=INK, zorder=3, lw=1.8)
    for i in range(6): ax.text(i, 0, f"x{i + 1}", ha="center", va="center", fontsize=11, zorder=4)
    for o in range(4): ax.text(xs_out[o], 1, f"y{o + 1}", ha="center", va="center", fontsize=11, zorder=4)
    title = ax.text(2.5, 1.22, "", ha="center", fontsize=16, fontweight="bold", color=INK)
    cnt = ax.text(2.5, -.2, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    hold1, fade, hold2, recol, hold3 = 8, 10, 8, 10, 12
    total = hold1 + fade + hold2 + recol + hold3

    def update(f):
        if f < hold1:
            fade_t, col_t = 0, 0
            title.set_text("Повні зв'язки (Dense)"); cnt.set_text("24 ваги", ); cnt.set_color(RED)
        elif f < hold1 + fade:
            fade_t, col_t = (f - hold1 + 1) / fade, 0
            title.set_text("Прибираємо зайві зв'язки…"); cnt.set_text("→ 12 ваг"); cnt.set_color(AMBER)
        elif f < hold1 + fade + hold2:
            fade_t, col_t = 1, 0
            title.set_text("Локальні зв'язки"); cnt.set_text("12 ваг"); cnt.set_color(AMBER)
        elif f < hold1 + fade + hold2 + recol:
            fade_t, col_t = 1, (f - hold1 - fade - hold2 + 1) / recol
            title.set_text("Робимо ваги спільними…"); cnt.set_text("→ 3 ваги"); cnt.set_color(GREEN)
        else:
            fade_t, col_t = 1, 1
            title.set_text("Локальні + спільні ваги"); cnt.set_text("3 ваги: w₁ (червона), w₂ (зелена), w₃ (синя)"); cnt.set_color(GREEN)
        for ln, (i, o, local, w) in zip(lines, conns):
            if local:
                tgt = np.array(to_rgba(wcol[w]))
                c = np.array(grey) * (1 - col_t) + tgt * col_t
                ln.set_color(c); ln.set_linewidth(1.5 + 1.2 * col_t)
            else:
                ln.set_color((*grey[:3], 1 - fade_t))

    save_gif(fig, update, total, "anim-05-dense-to-shared.gif", 6)


if __name__ == "__main__":
    anim_neuron_sum(); anim_shift_breaks_dense(); anim_detector_slides(); anim_peak(); anim_dense_to_shared()
