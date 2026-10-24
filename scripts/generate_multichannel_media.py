"""
Media for content/16.ai-python/15.cnn-image-classification/08.multichannel-convolution.md
Images -> public/images/ai-python/cnn-image-classification/multichannel-convolution/
  01 kernel cube at position (0,0): per-channel products and total   02 per-channel maps add up to one map
  03 cube sliding through the stack (schematic)   04 out_channels x in_channels (8 cubes -> 8 maps)
  05 photo through a hand-made Conv2d(3,2,3)       06 1x1 convolution = grayscale
  07 parameters of conv layers
Videos -> public/videos/ai-python/cnn-image-classification/multichannel-convolution/
  anim-01-cube-slide, anim-02-orange-sweep, anim-03-channels-flow
Data: sklearn flower.jpg (patch photo[222:226, 444:448])
"""
import os
import numpy as np
import torch, torch.nn as nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from sklearn.datasets import load_sample_image

plt.rcParams['font.family'] = 'DejaVu Sans'
IMG = "public/images/ai-python/cnn-image-classification/multichannel-convolution"
VID = "public/videos/ai-python/cnn-image-classification/multichannel-convolution"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
CR, CG, CB = "#DC2626", "#16A34A", "#2563EB"; CH = [CR, CG, CB]; CMAPS = ["Reds", "Greens", "Blues"]; NAMES = ["R (червоний)", "G (зелений)", "B (синій)"]
DPI, VIDEO_DPI = 80, 110

photo = load_sample_image("flower.jpg")
patch = photo[222:226, 444:448].astype(int)          # (4, 4, 3)
X = patch.transpose(2, 0, 1)                         # (3, 4, 4)
KC = np.zeros((3, 3, 3), int); KC[0] = 1; KC[2] = -1  # R:+1, G:0, B:-1
def cube(x, k):
    kh = k.shape[1]; out = np.zeros((x.shape[1] - kh + 1, x.shape[2] - kh + 1), int)
    for i in range(out.shape[0]):
        for j in range(out.shape[1]): out[i, j] = (x[:, i:i + kh, j:j + kh] * k).sum()
    return out
O = cube(X, KC); PART = [cube(X[c:c + 1], KC[c:c + 1]) for c in range(3)]
assert np.array_equal(O, sum(PART))
def signed(v): return "0" if v == 0 else f"{int(v):+d}"

def num_grid(ax, M, cmap, vmin, vmax, fmt=lambda v: f"{int(v)}", fs=12, nancolor="white"):
    ax.clear(); mm = np.ma.masked_invalid(M.astype(float)); cm = plt.get_cmap(cmap).copy(); cm.set_bad(nancolor)
    ax.imshow(mm, cmap=cm, vmin=vmin, vmax=vmax, interpolation="nearest")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            if not np.isnan(v):
                lum = (v - vmin) / (vmax - vmin + 1e-9)
                ax.text(j, i, fmt(v), ha="center", va="center", fontsize=fs, fontweight="bold", color="white" if (cmap in CMAPS and lum > 0.62) else INK)
    for k in range(M.shape[0] + 1): ax.axhline(k - .5, color="#94A3B8", lw=.8)
    for k in range(M.shape[1] + 1): ax.axvline(k - .5, color="#94A3B8", lw=.8)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

def mark(ax, i, j, h=1, w=1, color=AMBER, lw=3, ls="-"): ax.add_patch(patches.Rectangle((j - .5, i - .5), w, h, fill=False, edgecolor=color, lw=lw, ls=ls, zorder=5))
def title(ax, t, color=INK, fs=12): ax.set_title(t, fontsize=fs, fontweight="bold", color=color, pad=6)
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)

# --- images -----------------------------------------------------------------------
def img01():
    p = X[:, 0:3, 0:3]
    fig, axs = plt.subplots(3, 4, figsize=(15, 9.4), gridspec_kw={"width_ratios": [1, 1, 1, 1.5], "hspace": 0.28, "wspace": 0.25})
    for c in range(3):
        num_grid(axs[c, 0], p[c], CMAPS[c], 0, 255, fs=12); num_grid(axs[c, 1], KC[c], "RdYlGn", -2, 2, fmt=signed, fs=14)
        num_grid(axs[c, 2], p[c] * KC[c], "RdYlGn", -300, 300, fmt=signed, fs=11)
        axs[c, 3].axis("off"); s = int((p[c] * KC[c]).sum())
        axs[c, 3].text(0.0, 0.5, f"Σ = {signed(s)}", fontsize=22, fontweight="bold", va="center", color=CH[c] if s != 0 else MUTED)
        axs[c, 0].set_ylabel(NAMES[c], fontsize=12, fontweight="bold", color=CH[c])
        if c == 0:
            title(axs[0, 0], "Ділянка 3×3 каналу"); title(axs[0, 1], "Шар ядра-куба", CYAN); title(axs[0, 2], "Добуток"); title(axs[0, 3], "Сума шару")
    fig.suptitle(f"Позиція (0, 0): сума по всіх трьох каналах = {int(PART[0][0,0])} + {int(PART[1][0,0])} − {abs(int(PART[2][0,0]))} = {signed(O[0, 0])}", fontsize=14, fontweight="bold", color=INK, y=0.96)
    save_png(fig, "01.png")

def img02():
    fig, axs = plt.subplots(1, 6, figsize=(19, 4.4), gridspec_kw={"width_ratios": [1.2, 0.9, 0.9, 0.9, 0.9, 0.9]})
    axs[0].imshow(patch.astype(np.uint8), interpolation="nearest"); axs[0].set_xticks([]); axs[0].set_yticks([]); title(axs[0], "Ділянка 4×4 (3 канали)")
    for c in range(3):
        num_grid(axs[1 + c], PART[c], "RdYlGn", -1600, 1600, fmt=signed, fs=12); title(axs[1 + c], f"тільки канал {'RGB'[c]}", CH[c])
    num_grid(axs[4], O, "RdYlGn", -1600, 1600, fmt=signed, fs=16); title(axs[4], "Сума каналів", GREEN)
    axs[5].axis("off"); axs[5].text(0, 0.5, "Один вихід\nна всі канали", fontsize=14, fontweight="bold", color=INK, va="center")
    for ax_, t in [(axs[1], "→"), (axs[4], "=")]: ax_.text(-0.12, 0.5, t, transform=ax_.transAxes, fontsize=28, color=MUTED, ha="center", va="center", fontweight="bold")
    fig.suptitle("Кожен канал дає свою карту, а ядро-куб складає їх в одну", fontsize=14, fontweight="bold", color=INK, y=1.06)
    save_png(fig, "02.png")

def layer(ax, x, y, w, h, color, alpha=.35, lw=2, ec=None):
    ax.add_patch(patches.Rectangle((x, y), w, h, facecolor=color, alpha=alpha, edgecolor=ec or color, lw=lw))
    ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="none", edgecolor=ec or color, lw=lw))

def stack(ax, x, y, w, h, colors, d=0.55):
    for k in range(len(colors) - 1, -1, -1): layer(ax, x + k * d, y + k * d, w, h, colors[k])

def img03():
    fig, ax = plt.subplots(figsize=(15, 6.4)); ax.set_xlim(0, 15); ax.set_ylim(0, 6.4); ax.axis("off")
    d = 0.55; ix, iy, iw, ih = 0.8, 1.5, 4.2, 3.4
    stack(ax, ix, iy, iw, ih, CH, d)
    wx, wy, ww, wh = 1.7, 2.3, 1.2, 1.0         # window position inside the front layer
    for k in range(3): ax.add_patch(patches.Rectangle((wx + k * d, wy + k * d), ww, wh, fill=False, edgecolor=AMBER, lw=3, zorder=6))
    for (cx, cy) in [(wx, wy), (wx + ww, wy), (wx, wy + wh), (wx + ww, wy + wh)]: ax.plot([cx, cx + 2 * d], [cy, cy + 2 * d], color=AMBER, lw=2, zorder=6)
    ax.text(ix + iw / 2 + d, iy - 0.5, "Вхід [3, H, W]", ha="center", fontsize=13, fontweight="bold", color=INK)
    ax.text(ix + iw / 2 + d, iy - 1.1, "золотий каркас — ядро-куб [3, K, K]", ha="center", fontsize=12.5, fontweight="bold", color=AMBER)
    ox = 9.4; layer(ax, ox, iy + d, 3.5, 2.8, GREEN, .28, 2)
    cxo, cyo = ox + 1.2, iy + d + 1.2
    ax.add_patch(patches.Rectangle((cxo, cyo), .55, .5, facecolor=AMBER, alpha=.8, edgecolor=AMBER, lw=3))
    ax.text(ox + 1.75, iy - 0.5, "Вихід [1, H′, W′]", ha="center", fontsize=13, fontweight="bold", color=INK)
    ax.annotate("", xy=(cxo - 0.05, cyo + 0.28), xytext=(wx + ww + 2 * d + 0.1, wy + wh / 2 + 2 * d), arrowprops=dict(arrowstyle="->", lw=3, color=MUTED))
    ax.text(7.4, 4.5, "множимо весь «куб»\nі додаємо все\nв одне число", fontsize=12.5, ha="center", color=INK, fontweight="bold")
    for k, (nm, c) in enumerate(zip("RGB", CH)): ax.text(ix - .15 + k * d, iy + ih + k * d + .12, nm, color=c, fontsize=12, fontweight="bold")
    fig.suptitle("Ядро з трьох шарів проходить крізь усі канали одразу й дає одне число", fontsize=14, fontweight="bold", color=INK, y=0.98)
    save_png(fig, "03.png")

def img04():
    fig, ax = plt.subplots(figsize=(17, 6.6)); ax.set_xlim(0, 17); ax.set_ylim(0, 6.6); ax.axis("off"); d = 0.35
    stack(ax, 0.6, 1.8, 2.8, 2.5, CH, d)
    ax.text(2.2, 1.0, "Вхід", ha="center", fontsize=13, fontweight="bold", color=INK); ax.text(2.2, 0.55, "[N, 3, H, W]", ha="center", fontsize=11, color=MUTED)
    for k in range(8):
        r, c = divmod(k, 4); x0 = 6.2 + c * 1.6; y0 = 3.9 - r * 1.8
        stack(ax, x0, y0, .85, .85, CH, .17); ax.text(x0 + .55, y0 - .3, f"ядро {k + 1}", ha="center", fontsize=9.5, color=INK)
    ax.text(8.8, 6.1, "8 ядер-кубів, кожне [3, 3, 3]", ha="center", fontsize=12.5, fontweight="bold", color=CYAN)
    ax.text(8.8, 0.7, "weight [8, 3, 3, 3]  +  bias [8]", ha="center", fontsize=12, fontweight="bold", color=INK); ax.text(8.8, 0.25, "8 · 27 + 8 = 224 параметри", ha="center", fontsize=11, color=MUTED)
    stack(ax, 13.6, 1.8, 2.0, 1.8, ["#10B981"] * 6, .2)
    ax.text(14.6, 1.0, "Вихід", ha="center", fontsize=13, fontweight="bold", color=INK); ax.text(14.6, 0.55, "[N, 8, H′, W′]", ha="center", fontsize=11, color=MUTED)
    for x0, x1 in [(4.0, 5.9), (12.7, 13.4)]: ax.annotate("", xy=(x1, 3.2), xytext=(x0, 3.2), arrowprops=dict(arrowstyle="->", lw=3, color=MUTED))
    fig.suptitle("nn.Conv2d(3, 8, 3): кожен вихідний канал має власний куб із ваг", fontsize=14, fontweight="bold", color=INK, y=0.98)
    save_png(fig, "04.png")

IMGT = torch.tensor(photo.astype(np.float32) / 255).permute(2, 0, 1)[None]
def hand_layer():
    w = torch.zeros(2, 3, 3, 3); w[0, 0] = 1; w[0, 2] = -1; w[0] /= 9
    sx = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=torch.float32); w[1, :] = sx / 3
    l = nn.Conv2d(3, 2, 3, bias=False)
    with torch.no_grad(): l.weight[:] = w
    return l
OUT = hand_layer()(IMGT).detach()[0].numpy()

def img05():
    fig, axs = plt.subplots(1, 3, figsize=(18, 4.6))
    axs[0].imshow(photo); axs[0].set_xticks([]); axs[0].set_yticks([]); title(axs[0], "Кольорове фото (3 канали)")
    im = axs[1].imshow(OUT[0], cmap="RdYlGn", vmin=-0.9, vmax=0.9); axs[1].set_xticks([]); axs[1].set_yticks([]); title(axs[1], "Канал 1: R − B (зелене — «більш оранжеве»)", GREEN)
    axs[2].imshow(OUT[1], cmap="RdYlGn", vmin=-3, vmax=3); axs[2].set_xticks([]); axs[2].set_yticks([]); title(axs[2], "Канал 2: вертикальні краї (Собель X)", AMBER)
    fig.suptitle("Один шар Conv2d(3, 2, 3) із двома ядрами-кубами дає дві різні карти", fontsize=14, fontweight="bold", color=INK, y=1.04)
    save_png(fig, "05.png")

def img06():
    g = np.array([0.299, 0.587, 0.114]); ph = photo.astype(float) / 255; gray = (ph * g).sum(axis=2)
    fig, axs = plt.subplots(1, 4, figsize=(19, 4.6))
    for c in range(3):
        t = np.zeros_like(ph); t[:, :, c] = ph[:, :, c]; axs[c].imshow(t); axs[c].set_xticks([]); axs[c].set_yticks([])
        title(axs[c], f"канал {'RGB'[c]}  ×  {g[c]:.3f}", CH[c], 13)
    axs[3].imshow(gray, cmap="gray"); axs[3].set_xticks([]); axs[3].set_yticks([]); title(axs[3], "Σ = сіре зображення (1 канал)", INK, 13)
    for ax_, t in [(axs[1], "+"), (axs[2], "+"), (axs[3], "=")]: ax_.text(-0.07, 0.5, t, transform=ax_.transAxes, fontsize=30, color=MUTED, ha="center", va="center", fontweight="bold")
    fig.suptitle("Згортка 1×1: на кожному пікселі змішуємо канали з вагами — отримуємо сіре фото", fontsize=14, fontweight="bold", color=INK, y=1.05)
    save_png(fig, "06.png")

def img07():
    layers = [("Conv2d(1, 8, 3)", 1, 8, 3), ("Conv2d(3, 8, 3)", 3, 8, 3), ("Conv2d(8, 8, 3)", 8, 8, 3), ("Conv2d(8, 16, 3)", 8, 16, 3), ("Conv2d(16, 32, 3)", 16, 32, 3), ("Conv2d(3, 16, 5)", 3, 16, 5)]
    vals = [o * i * k * k + o for _, i, o, k in layers]
    fig, ax = plt.subplots(figsize=(11, 5.6)); y = np.arange(len(layers))[::-1]
    bars = ax.barh(y, vals, color=CYAN, height=.6)
    for yy, (n, i, o, k), v in zip(y, layers, vals): ax.text(v + 60, yy, f"{o}·{i}·{k}·{k} + {o} = {v:,}".replace(",", " "), va="center", fontsize=11, color=INK, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels([l[0] for l in layers], fontsize=11); ax.set_xlim(0, max(vals) * 1.45); ax.set_xlabel("кількість параметрів", fontsize=11, color=MUTED)
    ax.set_title("Параметри = вихідні канали · вхідні канали · K · K + вихідні канали", fontsize=13.5, fontweight="bold", color=INK, pad=12)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    save_png(fig, "07.png")

# --- videos -----------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps)
    common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps))
    update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_cube():
    pos = [(0, 0), (0, 1), (1, 0), (1, 1)]
    fig = plt.figure(figsize=(13, 5.6)); fig.patch.set_facecolor("white")
    axc = [fig.add_axes([0.02 + c * 0.17, 0.12, 0.15, 0.62]) for c in range(3)]; ax_t = fig.add_axes([0.54, 0.14, 0.2, 0.6]); ax_t.axis("off"); ax_o = fig.add_axes([0.80, 0.22, 0.17, 0.46])
    fig.text(0.5, 0.92, "Ядро-куб проходить усі три канали й дає одне число на позицію", ha="center", fontsize=15, fontweight="bold", color=INK)
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    fig.text(0.765, 0.45, "→", fontsize=30, color=MUTED, ha="center", va="center", fontweight="bold")
    per, lead, tail = 4, 2, 10; total = lead + per * 4 + tail

    def update(f):
        k = (f - lead) // per if f >= lead else -1; k = min(k, 3); ph = (f - lead) % per if f >= lead and f < lead + per * 4 else per - 1
        done = (k + 1 if ph >= 2 else k) if f < lead + per * 4 else 4; done = max(done, 0)
        for c in range(3):
            num_grid(axc[c], X[c], CMAPS[c], 0, 255, fs=10); title(axc[c], f"канал {'RGB'[c]}", CH[c])
            if k >= 0 and f < lead + per * 4: mark(axc[c], pos[k][0], pos[k][1], 3, 3, AMBER, 3.5)
        ax_t.clear(); ax_t.axis("off")
        if k >= 0 and f < lead + per * 4 and ph >= 1:
            i, j = pos[k]
            for c in range(3):
                s = int((X[c, i:i + 3, j:j + 3] * KC[c]).sum())
                ax_t.text(0.0, 0.85 - c * 0.2, f"{'RGB'[c]}:  {signed(s):>6}", fontsize=15, fontweight="bold", color=CH[c], family="monospace", transform=ax_t.transAxes)
            ax_t.text(0.0, 0.18, f"Σ = {signed(O[i, j])}", fontsize=19, fontweight="bold", color=GREEN, transform=ax_t.transAxes)
        Mo = np.full((2, 2), np.nan)
        for q in range(done): Mo[pos[q]] = O[pos[q]]
        num_grid(ax_o, Mo, "RdYlGn", -1000, 1000, fmt=signed, fs=14); title(ax_o, "Карта ознак 2×2", GREEN)
        for q in range(done): mark(ax_o, *pos[q], color=AMBER, lw=3)
        if k >= 0 and f < lead + per * 4: foot.set_text(f"позиція {pos[k]}: три частинні суми додаються в одне число")
        elif f >= lead + per * 4: foot.set_text("Три канали на вході — одна карта на виході")
        else: foot.set_text("Ядро має три шари: по одному на кожен канал (R: +1, G: 0, B: −1)")

    save_video(fig, update, total, "anim-01-cube-slide", 4, total - 1)

def vid_orange():
    h, w = OUT[0].shape; steps = 36; per = int(np.ceil(w / steps))
    fig = plt.figure(figsize=(13, 5.0)); fig.patch.set_facecolor("white")
    ax_p = fig.add_axes([0.02, 0.14, 0.46, 0.68]); ax_m = fig.add_axes([0.52, 0.14, 0.46, 0.68])
    fig.text(0.5, 0.93, "Ядро-куб (R − B) «знаходить» оранжеві пелюстки на кольоровому фото", ha="center", fontsize=15, fontweight="bold", color=INK)
    total = steps + 8

    def update(f):
        x = min(w, (f + 1) * per)
        ax_p.clear(); ax_p.imshow(photo); ax_p.axvline(x, color=AMBER, lw=3); ax_p.set_xticks([]); ax_p.set_yticks([]); title(ax_p, "Вхід: кольорове фото", INK, 13)
        m = np.full((h, w), np.nan); m[:, :x] = OUT[0][:, :x]
        ax_m.clear(); mm = np.ma.masked_invalid(m); cm = plt.get_cmap("RdYlGn").copy(); cm.set_bad("white")
        ax_m.imshow(mm, cmap=cm, vmin=-0.9, vmax=0.9); ax_m.set_xticks([]); ax_m.set_yticks([]); title(ax_m, "Карта «оранжевості»: зелене — так, червоне — ні", GREEN, 13)

    save_video(fig, update, total, "anim-02-orange-sweep", 6, total - 1)

def vid_flow():
    stages = [("Вхід", "[1, 28, 28]", 1, 28, "", "#64748B"), ("Conv2d(1, 8, 3)", "[8, 26, 26]", 8, 26, "80 параметрів", CYAN), ("MaxPool2d(2)", "[8, 13, 13]", 8, 13, "0 параметрів", GREEN),
              ("Conv2d(8, 16, 3)", "[16, 11, 11]", 16, 11, "1168 параметрів", CYAN), ("MaxPool2d(2)", "[16, 5, 5]", 16, 5, "0 параметрів", GREEN)]
    fig, ax = plt.subplots(figsize=(15, 5.8)); fig.patch.set_facecolor("white")
    per = 5; total = per * len(stages) + 8

    def update(f):
        k = min(f // per, len(stages) - 1)
        ax.clear(); ax.set_xlim(0, 15); ax.set_ylim(0, 5.8); ax.axis("off"); x = 0.3
        for q in range(k + 1):
            name, shape, ch, size, par, c = stages[q]; w = 0.25 + size / 28 * 1.9; n = min(ch, 8)
            for s in range(n - 1, -1, -1): ax.add_patch(patches.Rectangle((x + s * .08, 1.9 + s * .08), w, w, facecolor="white", edgecolor=c, lw=2))
            ax.text(x + w / 2 + .3, 1.5, shape, ha="center", fontsize=11, color=MUTED, fontweight="bold")
            ax.text(x + w / 2 + .3, 1.1, f"{ch} кан." if q else "1 кан.", ha="center", fontsize=11, color=c, fontweight="bold")
            ax.text(x + w / 2 + .3, 4.55 + (0.35 if q % 2 else 0), name, ha="center", fontsize=11, color=INK, fontweight="bold")
            if par: ax.text(x + w / 2 + .3, 0.55, par, ha="center", fontsize=10.5, color=INK)
            if q < k: ax.annotate("", xy=(x + w + 0.55, 3.0), xytext=(x + w + 0.15, 3.0), arrowprops=dict(arrowstyle="->", lw=2.5, color=MUTED))
            x += w + 1.15
        ax.text(7.5, 5.45, "Каналів дедалі більше, картинка дедалі менша", ha="center", fontsize=15, fontweight="bold", color=INK)

    save_video(fig, update, total, "anim-03-channels-flow", 5, total - 1)

if __name__ == "__main__":
    img01(); img02(); img03(); img04(); img05(); img06(); img07(); vid_cube(); vid_orange(); vid_flow()
