"""
Media for content/16.ai-python/15.cnn-image-classification/03.convolution-step-by-step.md
Images -> public/images/ai-python/cnn-image-classification/convolution-step-by-step/
  01.png setup (input, kernel, empty map)   02.png position (0,0)   03.png position (0,1)
  04.png full feature map                   05.png output size H-K+1  06.png receptive field
Videos -> public/videos/ai-python/cnn-image-classification/convolution-step-by-step/
  anim-01-conv-sliding   : kernel visits all 9 positions, map fills
  anim-02-output-size    : number of positions along an axis = H - K + 1
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

plt.rcParams['font.family'] = 'DejaVu Sans'
IMG = "public/images/ai-python/cnn-image-classification/convolution-step-by-step"
VID = "public/videos/ai-python/cnn-image-classification/convolution-step-by-step"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444"
DPI, VIDEO_DPI = 80, 110

I = np.array([[0, 1, 5, 0, 0], [0, 0, 5, 1, 0], [1, 0, 4, 0, 0], [0, 0, 5, 0, 1], [0, 1, 5, 0, 0]])
K = np.array([[-1, 1, -1]] * 3)

def conv(im, k):
    h, w = im.shape; kh, kw = k.shape
    return np.array([[int((im[i:i + kh, j:j + kw] * k).sum()) for j in range(w - kw + 1)] for i in range(h - kh + 1)])
O = conv(I, K)

def signed(v):
    return "0" if v == 0 else f"{v:+d}"

def grid(ax, M, cmap, vmin, vmax, fmt=str, fs=14, ticks=False):
    ax.clear()
    masked = np.ma.masked_invalid(M.astype(float))
    cm = plt.get_cmap(cmap).copy(); cm.set_bad("white")
    ax.imshow(masked, cmap=cm, vmin=vmin, vmax=vmax, interpolation="nearest")
    r, c = M.shape
    mid = (vmin + vmax) / 2
    for i in range(r):
        for j in range(c):
            v = M[i, j]
            if np.isnan(v): continue
            col = "white" if (cmap == "gray" and v < mid) else INK
            ax.text(j, i, fmt(int(v)), ha="center", va="center", fontsize=fs, fontweight="bold", color=col)
    for k in range(r + 1): ax.axhline(k - .5, color="#94A3B8", lw=.8)
    for k in range(c + 1): ax.axvline(k - .5, color="#94A3B8", lw=.8)
    if ticks:
        ax.set_xticks(range(c)); ax.set_yticks(range(r)); ax.tick_params(labelsize=10, colors=MUTED, length=0)
        ax.xaxis.tick_top()
    else:
        ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

def mark(ax, i, j, h=1, w=1, color=AMBER, lw=3):
    ax.add_patch(patches.Rectangle((j - .5, i - .5), w, h, fill=False, edgecolor=color, lw=lw))

def title(ax, t, color=INK, fs=12.5):
    ax.set_title(t, fontsize=fs, fontweight="bold", color=color, pad=8)

def save_png(fig, name):
    fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)

IM = dict(cmap="gray", vmin=0, vmax=5)

# --- images ------------------------------------------------------------------------
def img01():
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.4), gridspec_kw={"width_ratios": [1.25, 0.85, 0.85]})
    grid(axs[0], I, **IM, ticks=True); title(axs[0], "Вхід I (5×5)")
    grid(axs[1], K, "RdYlGn", -2, 2, ticks=True); title(axs[1], "Ядро K (3×3)", CYAN)
    grid(axs[2], np.full((3, 3), np.nan), "RdYlGn", -15, 15, ticks=True)
    for i in range(3):
        for j in range(3): axs[2].text(j, i, "?", ha="center", va="center", fontsize=18, color=MUTED)
    title(axs[2], "Карта ознак O (3×3)")
    fig.suptitle("Що в нас є: вхід, ядро і порожня таблиця для результату", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "01.png")

def step_fig(i, j, name):
    patch = I[i:i + 3, j:j + 3]; prod = patch * K; s = int(prod.sum())
    fig, axs = plt.subplots(1, 5, figsize=(15, 3.9), gridspec_kw={"width_ratios": [1.5, 1, 1, 1, 0.9]})
    grid(axs[0], I, **IM, fs=13, ticks=True); mark(axs[0], i, j, 3, 3, CYAN, 4); title(axs[0], f"Вхід: ядро в позиції ({i}, {j})")
    grid(axs[1], patch, **IM); title(axs[1], "Ділянка під ядром")
    grid(axs[2], K, "RdYlGn", -2, 2); title(axs[2], "Ядро K", CYAN)
    grid(axs[3], prod, "RdYlGn", -5, 5, fmt=signed); title(axs[3], "Поелементний добуток")
    axs[4].axis("off")
    axs[4].text(0.2, 0.5, f"Σ = {signed(s)}", fontsize=24, fontweight="bold", va="center", color=GREEN if s > 0 else RED)
    for ax_, t in [(axs[2], "×"), (axs[3], "="), (axs[4], "→")]:
        ax_.text(-0.14 if ax_ is not axs[4] else 0.0, 0.5, t, transform=ax_.transAxes, fontsize=30, color=MUTED,
                 ha="center", va="center", fontweight="bold")
    save_png(fig, name)

def img04():
    fig, axs = plt.subplots(1, 3, figsize=(12.5, 4.4), gridspec_kw={"width_ratios": [1.25, 0.85, 1.0]})
    grid(axs[0], I, **IM, ticks=True); title(axs[0], "Вхід I (5×5)")
    grid(axs[1], K, "RdYlGn", -2, 2, ticks=True); title(axs[1], "Ядро K (3×3)", CYAN)
    grid(axs[2], O, "RdYlGn", -15, 15, fmt=signed, ticks=True)
    for (i, j) in zip(*np.where(O == O.max())): mark(axs[2], i, j)
    title(axs[2], "Карта ознак O (3×3)", GREEN)
    fig.suptitle("Готова карта ознак: додатні значення — там, де ділянка схожа на ядро", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "04.png")

def draw_1d(ax, H, k, pos, n_done=None):
    ax.clear(); ax.set_xlim(-.7, 11.5); ax.set_ylim(-4.2, 1.6); ax.axis("off")
    for x in range(H):
        ax.add_patch(patches.Rectangle((x - .5, 0), 1, 1, facecolor="#E2E8F0", edgecolor="#64748B", lw=1.2))
        ax.text(x, .5, str(x), ha="center", va="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(-.7, 1.35, f"Вхід, ширина H = {H}", fontsize=12, color=INK, fontweight="bold")
    last = H - k
    for p in range(last + 1):
        if n_done is not None and p > n_done: break
        y = -0.9 - p * 0.9
        cur = (pos == p)
        ax.add_patch(patches.Rectangle((p - .5, y), k, 0.7, facecolor=CYAN if cur else "#BAE6FD",
                                        edgecolor=INK if cur else "#38BDF8", lw=2 if cur else 1, alpha=1 if cur else .7))
        ax.text(p + (k - 1) / 2, y + .35, f"позиція {p}", ha="center", va="center", fontsize=10.5, color=INK, fontweight="bold")

def img05():
    H, k = 5, 3
    fig, ax = plt.subplots(figsize=(11, 4.8))
    draw_1d(ax, H, k, pos=-1)
    ax.text(5.4, -0.9, f"Ліва позиція: 0\nПрава позиція: H − K = {H - k}\n\nУсього: (H − K) + 1 = {H - k + 1}", fontsize=13, color=INK, fontweight="bold", va="top")
    save_png(fig, "05.png")

def img06():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={"width_ratios": [1.3, 1]})
    grid(axs[0], I, **IM, ticks=True); mark(axs[0], 0, 1, 3, 3, CYAN, 4); title(axs[0], "Вхід: ділянка, яку «бачить» одне число")
    grid(axs[1], O, "RdYlGn", -15, 15, fmt=signed, ticks=True); mark(axs[1], 0, 1, color=CYAN, lw=4); title(axs[1], "Карта ознак: клітинка (0, 1) = +12", CYAN)
    fig.suptitle("Поле зору (receptive field) однієї клітинки карти ознак — ділянка 3×3 входу", fontsize=13.5, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "06.png")

# --- videos ------------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem)
    anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps)
    common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps))
    update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_sliding():
    pos = [(i, j) for i in range(3) for j in range(3)]
    fig = plt.figure(figsize=(12, 5.2)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.14, 0.26, 0.60]); ax_k = fig.add_axes([0.35, 0.40, 0.12, 0.277])
    ax_p = fig.add_axes([0.53, 0.40, 0.12, 0.277]); ax_o = fig.add_axes([0.74, 0.20, 0.22, 0.508])
    fig.text(0.5, 0.93, "Ядро ковзає по входу: одна позиція — одне число", ha="center", fontsize=15, fontweight="bold", color=INK)
    for x, t in [(0.50, "×"), (0.69, "→")]:
        fig.text(x, 0.54, t, fontsize=30, color=MUTED, ha="center", va="center", fontweight="bold")
    fig.text(0.59, 0.30, "", ha="center")
    foot = fig.text(0.5, 0.04, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    sumt = fig.text(0.59, 0.29, "", ha="center", fontsize=20, fontweight="bold")
    lead, per, tail = 3, 3, 10
    total = lead + per * 9 + tail

    def update(f):
        k = (f - lead) // per if f >= lead else -1
        ph = (f - lead) % per if f >= lead else 0
        k = min(k, 8)
        done = k + (1 if ph == 2 or f >= lead + per * 9 else 0)
        if f >= lead + per * 9: k, ph, done = 8, 2, 9
        grid(ax_i, I, **IM, fs=13, ticks=True); title(ax_i, "Вхід I")
        grid(ax_k, K, "RdYlGn", -2, 2, fs=11); title(ax_k, "Ядро K", CYAN, 11)
        M = np.full((3, 3), np.nan)
        for (a, b) in pos[:done]: M[a, b] = O[a, b]
        grid(ax_o, M, "RdYlGn", -15, 15, fmt=signed, fs=15, ticks=True); title(ax_o, "Карта ознак O", GREEN)
        if k < 0:
            grid(ax_p, np.full((3, 3), np.nan), "RdYlGn", -5, 5); title(ax_p, "Добуток", INK, 11)
            foot.set_text("Покладемо ядро на першу ділянку…"); sumt.set_text(""); return
        i, j = pos[k]
        mark(ax_i, i, j, 3, 3, CYAN, 4)
        prod = I[i:i + 3, j:j + 3] * K
        if ph == 0:
            grid(ax_p, np.full((3, 3), np.nan), "RdYlGn", -5, 5); sumt.set_text("")
            foot.set_text(f"Позиція ({i}, {j}): беремо ділянку 3×3 під ядром")
        else:
            grid(ax_p, prod, "RdYlGn", -5, 5, fmt=signed, fs=11)
            s = int(prod.sum()); sumt.set_text(f"Σ = {signed(s)}"); sumt.set_color(GREEN if s > 0 else RED)
            foot.set_text(f"Позиція ({i}, {j}): множимо елемент на елемент і додаємо" if ph == 1 else f"Записуємо {signed(s)} у клітинку O[{i}, {j}]")
        title(ax_p, "Добуток", INK, 11)
        if ph == 2 or f >= lead + per * 9: mark(ax_o, i, j)

    save_video(fig, update, total, "anim-01-conv-sliding", 3, lead + per * 9 - 1)

def vid_output_size():
    k = 3
    frames = []
    for H in (5, 6, 7):
        for p in range(H - k + 1):
            frames += [(H, p)] * 3
        frames += [(H, H - k)] * 5
    fig, ax = plt.subplots(figsize=(12, 5)); fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.05)
    head = fig.suptitle("", fontsize=15, fontweight="bold", color=INK)
    tx = [None]

    def update(f):
        H, p = frames[f]
        draw_1d(ax, H, k, pos=p, n_done=p)
        n = H - k + 1
        ax.text(7.6, 0.2, f"H = {H}, K = {k}\n\nпозицій: {p + 1} із {n}\n\n{H} − {k} + 1 = {n}", fontsize=14, color=INK, fontweight="bold", va="top")
        head.set_text("Скільки позицій має ядро вздовж однієї осі?")

    save_video(fig, update, len(frames), "anim-02-output-size", 3, 14)

if __name__ == "__main__":
    img01(); step_fig(0, 0, "02.png"); step_fig(0, 1, "03.png"); img04(); img05(); img06()
    vid_sliding(); vid_output_size()
