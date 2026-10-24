"""
Media for content/16.ai-python/15.cnn-image-classification/05.padding-and-stride.md
Images -> public/images/ai-python/cnn-image-classification/padding-and-stride/
  01.png coverage of pixels (valid vs padding=1)     02.png zero padding 5x5 -> 7x7 -> 5x5
  03.png stroke in column 0: invisible without padding  04.png stride 2: windows and result
  05.png feature-map size through 6 layers (3 settings)
Videos -> public/videos/ai-python/cnn-image-classification/padding-and-stride/
  anim-01-padding-slide, anim-02-stride-jumps, anim-03-size-stack
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from scipy.signal import correlate2d

plt.rcParams['font.family'] = 'DejaVu Sans'
IMG = "public/images/ai-python/cnn-image-classification/padding-and-stride"
VID = "public/videos/ai-python/cnn-image-classification/padding-and-stride"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110

I = np.array([[0, 1, 5, 0, 0], [0, 0, 5, 1, 0], [1, 0, 4, 0, 0], [0, 0, 5, 0, 1], [0, 1, 5, 0, 0]])
K = np.array([[-1, 1, -1]] * 3)
def conv(im, k): return correlate2d(im, k, mode="valid")
def signed(v): return "0" if v == 0 else f"{v:+d}"
def out_size(h, k, p=0, s=1): return (h + 2 * p - k) // s + 1

def coverage(h, w, k, p=0):
    cov = np.zeros((h + 2 * p, w + 2 * p), int)
    for i in range(h + 2 * p - k + 1):
        for j in range(w + 2 * p - k + 1): cov[i:i + k, j:j + k] += 1
    return cov[p:p + h, p:p + w]

def grid(ax, M, cmap, vmin, vmax, fmt=str, fs=13, ticks=False, hatch_mask=None):
    ax.clear()
    masked = np.ma.masked_invalid(M.astype(float))
    cm = plt.get_cmap(cmap).copy(); cm.set_bad("white")
    ax.imshow(masked, cmap=cm, vmin=vmin, vmax=vmax, interpolation="nearest")
    r, c = M.shape; mid = (vmin + vmax) / 2
    for i in range(r):
        for j in range(c):
            v = M[i, j]
            if np.isnan(v): continue
            pad = hatch_mask is not None and hatch_mask[i, j]
            col = MUTED if pad else ("white" if (cmap == "gray" and v < mid) else INK)
            ax.text(j, i, fmt(int(v)), ha="center", va="center", fontsize=fs if not pad else fs - 2, fontweight="bold", color=col)
            if pad: ax.add_patch(patches.Rectangle((j - .5, i - .5), 1, 1, fill=True, facecolor="#E2E8F0", edgecolor="none", alpha=.85, zorder=1.5)); ax.text(j, i, "0", ha="center", va="center", fontsize=fs - 2, fontweight="bold", color=MUTED, zorder=3)
    for k in range(r + 1): ax.axhline(k - .5, color="#94A3B8", lw=.8)
    for k in range(c + 1): ax.axvline(k - .5, color="#94A3B8", lw=.8)
    if ticks:
        ax.set_xticks(range(c)); ax.set_yticks(range(r)); ax.tick_params(labelsize=9, colors=MUTED, length=0); ax.xaxis.tick_top()
    else: ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

def mark(ax, i, j, h=1, w=1, color=AMBER, lw=3, ls="-"):
    ax.add_patch(patches.Rectangle((j - .5, i - .5), w, h, fill=False, edgecolor=color, lw=lw, ls=ls, zorder=5))

def title(ax, t, color=INK, fs=12.5): ax.set_title(t, fontsize=fs, fontweight="bold", color=color, pad=8)
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
IM = dict(cmap="gray", vmin=0, vmax=5)

# --- images -----------------------------------------------------------------------
def img01():
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 5.6))
    grid(axs[0], coverage(7, 7, 3), "Blues", 0, 12, fs=14); title(axs[0], "Без доповнення: кут — 1 раз, центр — 9 разів")
    grid(axs[1], coverage(7, 7, 3, 1), "Blues", 0, 12, fs=14); title(axs[1], "З доповненням (padding = 1): кут — 4 рази", GREEN)
    fig.suptitle("Скільки разів піксель потрапляє під ядро 3×3 (вхід 7×7)", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "01.png")

def img02():
    padded = np.pad(I, 1); hm = np.zeros(padded.shape, bool); hm[0, :] = hm[-1, :] = hm[:, 0] = hm[:, -1] = True
    out = conv(padded, K)
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.0), gridspec_kw={"width_ratios": [1, 1.2, 1]})
    grid(axs[0], I, **IM, ticks=False); title(axs[0], "Вхід 5×5")
    grid(axs[1], padded, **IM, hatch_mask=hm); mark(axs[1], 0, 0, 3, 3, CYAN, 4); title(axs[1], "З рамкою нулів 7×7 (P = 1)")
    grid(axs[2], out, "RdYlGn", -15, 15, fmt=signed); title(axs[2], "Карта ознак 5×5", GREEN)
    for ax_, t in [(axs[1], "→"), (axs[2], "→")]:
        ax_.text(-0.09, 0.5, t, transform=ax_.transAxes, fontsize=30, color=MUTED, ha="center", va="center", fontweight="bold")
    fig.suptitle("Рамка з нулів: розмір результату збігається з розміром входу", fontsize=14, fontweight="bold", color=INK, y=1.04)
    save_png(fig, "02.png")

def img03():
    im = np.zeros((6, 6), int); im[:, 0] = 1
    a, b = conv(im, K), conv(np.pad(im, 1), K)
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.0), gridspec_kw={"width_ratios": [1.2, 0.85, 1.25]})
    grid(axs[0], im, "gray", 0, 1, fs=12); title(axs[0], "Штрих у крайньому стовпці 0")
    grid(axs[1], a, "RdYlGn", -3, 3, fmt=signed); title(axs[1], f"Без padding (4×4): максимум {a.max()}", RED)
    grid(axs[2], b, "RdYlGn", -3, 3, fmt=signed)
    for (i, j) in zip(*np.where(b == b.max())): mark(axs[2], i, j)
    title(axs[2], f"З padding = 1 (6×6): максимум {b.max()}", GREEN)
    fig.suptitle("Ядро не могло «стати» центром на крайній стовпець, а з рамкою — може", fontsize=14, fontweight="bold", color=INK, y=1.04)
    save_png(fig, "03.png")

def img04():
    full = conv(I, K); s2 = full[::2, ::2]
    cols = [CYAN, AMBER, PURPLE, GREEN]; pos = [(0, 0), (0, 2), (2, 0), (2, 2)]
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.0), gridspec_kw={"width_ratios": [1.3, 0.8, 0.9]})
    grid(axs[0], I, **IM, ticks=True)
    for (i, j), c, off in zip(pos, cols, [(-.06, -.06), (-.06, .06), (.06, -.06), (.06, .06)]):
        axs[0].add_patch(patches.Rectangle((j - .5 + off[1], i - .5 + off[0]), 3, 3, fill=False, edgecolor=c, lw=3.2))
    title(axs[0], "Вхід: ядро стрибає на 2 пікселі (stride = 2)")
    grid(axs[1], s2, "RdYlGn", -15, 15, fmt=signed, fs=15)
    for k, (c, (a, b)) in enumerate(zip(cols, [(0, 0), (0, 1), (1, 0), (1, 1)])): mark(axs[1], a, b, color=c, lw=4)
    title(axs[1], "Карта 2×2", GREEN)
    grid(axs[2], full, "RdYlGn", -15, 15, fmt=signed, fs=11)
    for (i, j), c in zip(pos, cols): mark(axs[2], i, j, color=c, lw=3)
    title(axs[2], "Для порівняння: stride = 1", MUTED)
    fig.suptitle("Stride 2 дає кожну другу клітинку карти для stride 1", fontsize=14, fontweight="bold", color=INK, y=1.04)
    save_png(fig, "04.png")

def img05():
    def seq(p, s, n=6, h=28):
        out = [h]
        for _ in range(n): h = out_size(h, 3, p, s); out.append(h)
        return out
    sets = [("без padding\nstride 1", seq(0, 1), RED), ("padding 1\nstride 1", seq(1, 1), GREEN), ("padding 1\nstride 2", seq(1, 2), AMBER)]
    fig, ax = plt.subplots(figsize=(10, 5.6)); x = np.arange(7)
    for name, v, c in sets:
        ax.plot(x, v, marker="o", lw=2.6, color=c, ms=7)
        ax.text(6.12, v[-1], f"{name}\n(підсумок {v[-1]}×{v[-1]})", color=c, fontsize=10.5, fontweight="bold", va="center")
    ax.set_xlim(-0.2, 8.3); ax.set_ylim(-1, 30); ax.set_xticks(x)
    ax.set_xlabel("кількість згорток 3×3 поспіль", fontsize=11, color=MUTED); ax.set_ylabel("розмір карти ознак (пікселів)", fontsize=11, color=MUTED)
    ax.set_title("Як змінюється розмір 28×28 після кожної згортки", fontsize=14, fontweight="bold", color=INK, pad=12)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    save_png(fig, "05.png")

# --- videos -----------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps)
    common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps))
    update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_padding():
    padded = np.pad(I, 1); hm = np.zeros(padded.shape, bool); hm[0, :] = hm[-1, :] = hm[:, 0] = hm[:, -1] = True
    full = conv(padded, K); pos = [(i, j) for i in range(5) for j in range(5)]
    fig = plt.figure(figsize=(12, 5.4)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.12, 0.33, 0.33 * 12 / 5.4 * 0.0 + 0.66]); ax_k = fig.add_axes([0.42, 0.40, 0.11, 0.24]); ax_o = fig.add_axes([0.62, 0.12, 0.34, 0.66])
    fig.text(0.5, 0.92, "Ядро проходить вхід із рамкою нулів — результат 5×5", ha="center", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.575, 0.52, "→", ha="center", va="center", fontsize=34, color=MUTED, fontweight="bold")
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    lead, tail = 3, 10; total = lead + 25 + tail

    def update(f):
        k = f - lead
        done = max(0, min(25, k + 1))
        grid(ax_i, padded, **IM, hatch_mask=hm, fs=13); title(ax_i, "Вхід + рамка нулів (7×7)")
        grid(ax_k, K, "RdYlGn", -2, 2, fs=11); title(ax_k, "Ядро", CYAN, 11)
        M = np.full((5, 5), np.nan)
        for (a, b) in pos[:done]: M[a, b] = full[a, b]
        grid(ax_o, M, "RdYlGn", -15, 15, fmt=signed, fs=13); title(ax_o, "Карта ознак 5×5", GREEN)
        if done == 0: foot.set_text("Починаємо з кутової позиції — вона накриває рамку"); return
        i, j = pos[done - 1]; mark(ax_i, i, j, 3, 3, CYAN, 4); mark(ax_o, i, j)
        touches = i == 0 or j == 0 or i == 4 or j == 4
        foot.set_text(f"позиція ({i}, {j}): відгук = {signed(int(full[i, j]))}" + ("  — ядро накриває нулі рамки" if touches else "") if done < 25 else "Готово: розмір карти збігається з розміром входу")

    save_video(fig, update, total, "anim-01-padding-slide", 5, total - 1)

def vid_stride():
    full = conv(I, K); pos = [(0, 0), (0, 2), (2, 0), (2, 2)]; cols = [CYAN, AMBER, PURPLE, GREEN]
    fig = plt.figure(figsize=(12, 5.4)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.12, 0.34, 0.66]); ax_k = fig.add_axes([0.42, 0.40, 0.11, 0.24]); ax_o = fig.add_axes([0.66, 0.22, 0.24, 0.48])
    fig.text(0.5, 0.92, "Stride = 2: ядро стрибає через піксель", ha="center", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.60, 0.46, "→", ha="center", va="center", fontsize=34, color=MUTED, fontweight="bold")
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    per, lead, tail = 5, 3, 12; total = lead + per * 4 + tail

    def update(f):
        k = (f - lead) // per if f >= lead else -1; k = min(k, 3)
        ph = (f - lead) % per if f >= lead and f < lead + per * 4 else per - 1
        done = k + 1 if (k >= 0 and ph >= 2) or f >= lead + per * 4 else max(k, 0)
        grid(ax_i, I, **IM, ticks=True, fs=13); title(ax_i, "Вхід 5×5")
        grid(ax_k, K, "RdYlGn", -2, 2, fs=11); title(ax_k, "Ядро", CYAN, 11)
        for q in range(max(0, min(done, 4) if f < lead + per * 4 else 4)):
            mark(ax_i, *pos[q], 3, 3, cols[q], 2, ls="--")
        M = np.full((2, 2), np.nan)
        for q in range(min(done, 4)): M[q // 2, q % 2] = full[pos[q]]
        grid(ax_o, M, "RdYlGn", -15, 15, fmt=signed, fs=16); title(ax_o, "Карта ознак 2×2", GREEN)
        for q in range(min(done, 4)): mark(ax_o, q // 2, q % 2, color=cols[q], lw=3.5)
        if k >= 0 and f < lead + per * 4:
            mark(ax_i, *pos[k], 3, 3, cols[k], 4)
            foot.set_text(f"позиція ({pos[k][0]}, {pos[k][1]}): відгук = {signed(int(full[pos[k]]))}")
        elif f >= lead + per * 4: foot.set_text("Результат 2×2: ядро зупинялося через одну позицію")
        else: foot.set_text("Крок зсуву — не 1, а 2 пікселі")

    save_video(fig, update, total, "anim-02-stride-jumps", 5, total - 1)

def vid_stack():
    def seq(p, s, n=6, h=28):
        out = [h]
        for _ in range(n): h = out_size(h, 3, p, s); out.append(h)
        return out
    sc = [("Без padding", seq(0, 1), RED), ("padding = 1", seq(1, 1), GREEN), ("padding = 1, stride = 2", seq(1, 2), AMBER)]
    fig = plt.figure(figsize=(12, 5.4)); fig.patch.set_facecolor("white")
    axs = [fig.add_axes([0.04 + k * 0.325, 0.15, 0.28, 0.28 * 12 / 5.4 * 0.0 + 0.62]) for k in range(3)]
    head = fig.text(0.5, 0.93, "", ha="center", fontsize=16, fontweight="bold", color=INK)
    hold = 5; total = hold * 7 + 6

    def update(f):
        layer = min(f // hold, 6)
        head.set_text("Вхід 28×28" if layer == 0 else f"Після згортки №{layer}")
        for ax, (name, v, c) in zip(axs, sc):
            ax.clear(); ax.set_xlim(0, 28); ax.set_ylim(0, 28); ax.set_aspect("equal"); ax.axis("off")
            ax.add_patch(patches.Rectangle((0, 0), 28, 28, fill=False, edgecolor="#CBD5E1", lw=1.5, ls="--"))
            s = v[layer]; o = (28 - s) / 2
            ax.add_patch(patches.Rectangle((o, o), s, s, facecolor=c, alpha=.35, edgecolor=c, lw=2.5))
            ax.text(14, 14, f"{s}×{s}", ha="center", va="center", fontsize=18, fontweight="bold", color=INK)
            ax.set_title(name, fontsize=13, fontweight="bold", color=c, pad=8)

    save_video(fig, update, total, "anim-03-size-stack", 5, total - 1)

if __name__ == "__main__":
    img01(); img02(); img03(); img04(); img05(); vid_padding(); vid_stride(); vid_stack()
