"""
Media for content/16.ai-python/15.cnn-image-classification/07.pooling.md
Images -> public/images/ai-python/cnn-image-classification/pooling/
  01 max/avg pooling on a 4x4 table  02 pooling of a real feature map (26x26 -> 13x13)
  03 pooling and a 1-pixel shift     04 receptive field boxes on the digit
  05 receptive field growth chart    06 Conv-ReLU-Pool tensor shapes
Videos -> public/videos/ai-python/cnn-image-classification/pooling/
  anim-01-pool-slide, anim-02-pool-feature-map, anim-03-shift-robustness, anim-04-receptive-field
Data: temp/mnist.npz (x_train[101] == 7)
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
IMG = "public/images/ai-python/cnn-image-classification/pooling"
VID = "public/videos/ai-python/cnn-image-classification/pooling"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110

mn = np.load("temp/mnist.npz"); assert mn["y_train"][101] == 7
seven = mn["x_train"][101] / 255
SX = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
def fmap(im): return np.maximum(correlate2d(im, SX, mode="valid"), 0)
def maxpool(m, k=2): h, w = m.shape; return m[:h // k * k, :w // k * k].reshape(h // k, k, w // k, k).max(axis=(1, 3))
def avgpool(m, k=2): h, w = m.shape; return m[:h // k * k, :w // k * k].reshape(h // k, k, w // k, k).mean(axis=(1, 3))
M4 = np.array([[1, 3, 2, 1], [4, 6, 5, 2], [7, 2, 9, 4], [1, 0, 3, 8]])
A = fmap(seven); PA = maxpool(A)
VMAX = 4.0

def num_grid(ax, M, cmap, vmin, vmax, fmt=lambda v: f"{v:g}", fs=15):
    ax.clear(); ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]): ax.text(j, i, fmt(M[i, j]), ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)
    for k in range(M.shape[0] + 1): ax.axhline(k - .5, color="#94A3B8", lw=.8)
    for k in range(M.shape[1] + 1): ax.axvline(k - .5, color="#94A3B8", lw=.8)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

def mimg(ax, m, title=None, tcolor=INK, vmax=VMAX, cmap="Greens"):
    ax.clear(); ax.imshow(m, cmap=cmap, vmin=0, vmax=vmax, interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_edgecolor("#CBD5E1")
    if title: ax.set_title(title, fontsize=12, fontweight="bold", color=tcolor, pad=6)

def mark(ax, i, j, h=1, w=1, color=AMBER, lw=3, ls="-"):
    ax.add_patch(patches.Rectangle((j - .5, i - .5), w, h, fill=False, edgecolor=color, lw=lw, ls=ls, zorder=5))

def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def title(ax, t, color=INK, fs=12.5): ax.set_title(t, fontsize=fs, fontweight="bold", color=color, pad=8)

# --- images -----------------------------------------------------------------------
def img01():
    cols = [CYAN, AMBER, PURPLE, GREEN]; mp, ap = maxpool(M4), avgpool(M4)
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.0), gridspec_kw={"width_ratios": [1.3, 0.9, 0.9]})
    num_grid(axs[0], M4, "Blues", 0, 14)
    for q, c in enumerate(cols): mark(axs[0], (q // 2) * 2, (q % 2) * 2, 2, 2, c, 4)
    title(axs[0], "Карта ознак 4×4: чотири вікна 2×2")
    num_grid(axs[1], mp, "Blues", 0, 14, fs=18)
    for q, c in enumerate(cols): mark(axs[1], q // 2, q % 2, color=c, lw=4)
    title(axs[1], "Max: найбільше", GREEN)
    num_grid(axs[2], ap, "Blues", 0, 14, fmt=lambda v: f"{v:.1f}", fs=18)
    for q, c in enumerate(cols): mark(axs[2], q // 2, q % 2, color=c, lw=4)
    title(axs[2], "Average: середнє", AMBER)
    for ax_ in (axs[1], axs[2]): ax_.text(-0.1, 0.5, "→", transform=ax_.transAxes, fontsize=28, color=MUTED, ha="center", va="center", fontweight="bold")
    fig.suptitle("Пулінг: із кожного вікна 2×2 лишаємо одне число", fontsize=14, fontweight="bold", color=INK, y=1.03)
    save_png(fig, "01.png")

def img02():
    fig, axs = plt.subplots(1, 3, figsize=(16, 5.6), gridspec_kw={"width_ratios": [2, 1, 1]})
    mimg(axs[0], A, f"Карта ознак Собеля X після ReLU: {A.shape[0]}×{A.shape[1]}")
    mimg(axs[1], PA, f"Max-пулінг 2×2: {PA.shape[0]}×{PA.shape[1]}", GREEN)
    mimg(axs[2], avgpool(A), f"Average-пулінг 2×2: {PA.shape[0]}×{PA.shape[1]}", AMBER)
    fig.suptitle("Те саме зображення вдвічі менше: max зберігає яскравість країв, average розмиває", fontsize=14, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "02.png")

def rel(x, y): return float(np.abs(x - y).sum() / np.abs(x).sum())
def corr(x, y): return float(np.corrcoef(x.ravel(), y.ravel())[0, 1])

def img03():
    sh = np.roll(seven, 1, axis=1); b = fmap(sh); pb = maxpool(b)
    fig = plt.figure(figsize=(14, 10.5)); gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.12, height_ratios=[1, 1, 1])
    ax = fig.add_subplot(gs[0, 0]); ax.imshow(seven, cmap="gray"); ax.set_xticks([]); ax.set_yticks([]); title(ax, "Оригінал")
    ax = fig.add_subplot(gs[0, 1]); ax.imshow(sh, cmap="gray"); ax.set_xticks([]); ax.set_yticks([]); title(ax, "Зсув на 1 піксель вправо")
    ax = fig.add_subplot(gs[0, 2]); ax.axis("off")
    ax.text(0, 0.7, f"кореляція карт:", fontsize=13, color=MUTED, fontweight="bold"); ax.text(0, 0.45, f"без пулінгу   {corr(A, b):.2f}", fontsize=15, color=RED, fontweight="bold")
    ax.text(0, 0.2, f"після пулінгу {corr(PA, pb):.2f}", fontsize=15, color=GREEN, fontweight="bold")
    for r, (x, y, name, c) in enumerate([(A, b, "Карта ознак 26×26", RED), (PA, pb, "Після max-пулінгу 13×13", GREEN)]):
        ax = fig.add_subplot(gs[r + 1, 0]); mimg(ax, x, f"{name}: оригінал")
        ax = fig.add_subplot(gs[r + 1, 1]); mimg(ax, y, f"{name}: зсунуте")
        ax = fig.add_subplot(gs[r + 1, 2]); mimg(ax, np.abs(x - y), f"|різниця| = {rel(x, y):.2f} від суми", c)
    fig.suptitle("Пулінг пом'якшує вплив зсуву на 1 піксель, але не прибирає його", fontsize=14, fontweight="bold", color=INK, y=0.96)
    save_png(fig, "03.png")

RF_STAGES = [("Conv 3×3", 3), ("MaxPool 2×2", 4), ("Conv 3×3", 8), ("MaxPool 2×2", 10), ("Conv 3×3", 18)]

def img04():
    fig, axs = plt.subplots(1, 5, figsize=(19, 4.6))
    for ax, (name, r) in zip(axs, RF_STAGES):
        ax.imshow(seven, cmap="gray"); ax.set_xticks([]); ax.set_yticks([])
        ax.add_patch(patches.Rectangle((13.5 - r / 2, 13.5 - r / 2), r, r, fill=True, facecolor=CYAN, alpha=.22, edgecolor=CYAN, lw=3))
        title(ax, f"після шару «{name}»\nполе зору {r}×{r}", INK, 11.5)
    fig.suptitle("Одне число дивиться на дедалі більшу ділянку входу (малюнок умовно по центру)", fontsize=14, fontweight="bold", color=INK, y=1.08)
    save_png(fig, "04.png")

def img05():
    with_pool = [3, 4, 8, 10, 18, 22]; plain = [3, 5, 7, 9, 11, 13]; x = np.arange(1, 7)
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.plot(x, with_pool, marker="o", lw=2.8, color=GREEN, ms=8); ax.plot(x, plain, marker="o", lw=2.8, color=RED, ms=8)
    ax.axhline(28, color=MUTED, ls="--", lw=1.5); ax.text(1.05, 28.6, "розмір цифри MNIST: 28", color=MUTED, fontsize=11)
    ax.text(6.12, 22, "Conv, Pool, Conv, Pool, …", color=GREEN, fontsize=11, fontweight="bold", va="center")
    ax.text(6.12, 13, "лише Conv 3×3", color=RED, fontsize=11, fontweight="bold", va="center")
    labels = ["Conv", "Pool", "Conv", "Pool", "Conv", "Pool"]
    ax.set_xticks(x); ax.set_xticklabels([f"{i}\n{l}" for i, l in zip(x, labels)])
    ax.set_xlim(0.6, 8.6); ax.set_ylim(0, 31); ax.set_xlabel("кількість шарів поспіль (підписи під віссю — для зеленої лінії)", fontsize=11, color=MUTED); ax.set_ylabel("поле зору (пікселів)", fontsize=11, color=MUTED)
    ax.set_title("Пулінг прискорює зростання поля зору", fontsize=14, fontweight="bold", color=INK, pad=12)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    save_png(fig, "05.png")

def img06():
    stages = [("Вхід", "[N, 1, 28, 28]", 28, "#64748B"), ("Conv2d(1, 8, 3, pad=1)\n+ ReLU", "[N, 8, 28, 28]", 28, CYAN), ("MaxPool2d(2)", "[N, 8, 14, 14]", 14, GREEN),
              ("Conv2d(8, 8, 3, pad=1)\n+ ReLU", "[N, 8, 14, 14]", 14, CYAN), ("MaxPool2d(2)", "[N, 8, 7, 7]", 7, GREEN)]
    fig, ax = plt.subplots(figsize=(17, 4.9)); ax.set_xlim(0, 17); ax.set_ylim(1.5, 6.3); ax.axis("off")
    x = 0.4
    for k, (name, shape, size, c) in enumerate(stages):
        w = 0.1 + size / 28 * 2.3; n = 1 if k == 0 else 4
        for q in range(n - 1, -1, -1): ax.add_patch(patches.Rectangle((x + q * .1, 2.4 + q * .1), w, w, facecolor="white", edgecolor=c, lw=2.2))
        ax.text(x + w / 2, 2.0, shape, ha="center", fontsize=11, color=MUTED, fontweight="bold")
        ax.text(x + w / 2 + 0.15, 2.4 + 0.1 * (n - 1) + w + 0.35, name, ha="center", va="bottom", fontsize=11.5, color=INK, fontweight="bold")
        if k < len(stages) - 1: ax.annotate("", xy=(x + w + 0.65, 3.4), xytext=(x + w + 0.1, 3.4), arrowprops=dict(arrowstyle="->", lw=2.5, color=MUTED))
        x += w + 1.0
    fig.suptitle("Типовий блок «Conv → ReLU → Pool»: розмір вдвічі менший, каналів більше", fontsize=14, fontweight="bold", color=INK, y=0.98)
    save_png(fig, "06.png")

# --- videos -----------------------------------------------------------------------
def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps)
    common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps))
    update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_slide():
    cols = [CYAN, AMBER, PURPLE, GREEN]; mp, ap = maxpool(M4), avgpool(M4)
    fig = plt.figure(figsize=(12, 5.4)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.12, 0.32, 0.32 * 12 / 5.4 * 0.0 + 0.66]); ax_m = fig.add_axes([0.46, 0.14, 0.2, 0.2 * 12 / 5.4 * 0.0 + 0.5]); ax_a = fig.add_axes([0.74, 0.14, 0.2, 0.5])
    fig.text(0.5, 0.92, "Вікно 2×2 стрибає з кроком 2 і лишає одне число", ha="center", fontsize=15, fontweight="bold", color=INK)
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)
    fig.text(0.40, 0.40, "→", fontsize=32, color=MUTED, ha="center", va="center", fontweight="bold")
    per, lead, tail = 4, 2, 10; total = lead + per * 4 + tail

    def update(f):
        k = (f - lead) // per if f >= lead else -1; k = min(k, 3); ph = (f - lead) % per if f >= lead and f < lead + per * 4 else per - 1
        done = (k + 1 if ph >= 2 else k) if f < lead + per * 4 else 4; done = max(done, 0)
        num_grid(ax_i, M4, "Blues", 0, 14); title(ax_i, "Карта ознак 4×4")
        for q in range(done): mark(ax_i, (q // 2) * 2, (q % 2) * 2, 2, 2, cols[q], 2, "--")
        Mm = np.full((2, 2), np.nan); Ma = np.full((2, 2), np.nan)
        for q in range(done): Mm[q // 2, q % 2] = mp[q // 2, q % 2]; Ma[q // 2, q % 2] = ap[q // 2, q % 2]
        for ax_, data, t, c, fm in [(ax_m, Mm, "Max", GREEN, lambda v: f"{v:g}"), (ax_a, Ma, "Average", AMBER, lambda v: f"{v:.1f}")]:
            ax_.clear(); mm = np.ma.masked_invalid(data); cm = plt.get_cmap("Blues").copy(); cm.set_bad("white")
            ax_.imshow(mm, cmap=cm, vmin=0, vmax=14, interpolation="nearest")
            for i in range(2):
                for j in range(2):
                    if not np.isnan(data[i, j]): ax_.text(j, i, fm(data[i, j]), ha="center", va="center", fontsize=18, fontweight="bold", color=INK)
            for q in range(3): ax_.axhline(q - .5, color="#94A3B8", lw=.8); ax_.axvline(q - .5, color="#94A3B8", lw=.8)
            ax_.set_xticks([]); ax_.set_yticks([]); title(ax_, t + "-пулінг 2×2", c)
            for s in ax_.spines.values(): s.set_visible(False)
        for q in range(done): mark(ax_m, q // 2, q % 2, color=cols[q], lw=3.5); mark(ax_a, q // 2, q % 2, color=cols[q], lw=3.5)
        if k >= 0 and f < lead + per * 4:
            mark(ax_i, (k // 2) * 2, (k % 2) * 2, 2, 2, cols[k], 4)
            win = M4[(k // 2) * 2:(k // 2) * 2 + 2, (k % 2) * 2:(k % 2) * 2 + 2]
            foot.set_text(f"вікно {k + 1}: числа {', '.join(str(int(v)) for v in win.flatten())} → max = {int(win.max())}, середнє = {win.mean():.1f}")
        elif f >= lead + per * 4: foot.set_text("Розмір 4×4 → 2×2; у пулінгу немає жодної ваги, що навчається")
        else: foot.set_text("Беремо вікна 2×2 без перекриття")

    save_video(fig, update, total, "anim-01-pool-slide", 4, total - 1)

def vid_map():
    n = PA.size; per = 7; total = int(np.ceil(n / per)) + 8
    fig = plt.figure(figsize=(12, 5.8)); fig.patch.set_facecolor("white")
    ax_i = fig.add_axes([0.03, 0.12, 0.42, 0.62]); ax_o = fig.add_axes([0.56, 0.12, 0.42, 0.62])
    fig.text(0.5, 0.92, "Max-пулінг проходить усю карту ознак і зменшує її вдвічі", ha="center", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.505, 0.43, "→", fontsize=32, color=MUTED, ha="center", va="center", fontweight="bold")
    foot = fig.text(0.5, 0.03, "", ha="center", fontsize=14, fontweight="bold", color=INK)

    def update(f):
        k = min(n, (f + 1) * per)
        flat = np.full(n, np.nan); flat[:k] = PA.flatten()[:k]
        mimg(ax_i, A, "Вхід: карта ознак 26×26")
        i, j = divmod(k - 1, 13); mark(ax_i, 2 * i, 2 * j, 2, 2, CYAN, 3)
        ax_o.clear(); mm = np.ma.masked_invalid(flat.reshape(13, 13)); cm = plt.get_cmap("Greens").copy(); cm.set_bad("white")
        ax_o.imshow(mm, cmap=cm, vmin=0, vmax=VMAX, interpolation="nearest"); ax_o.set_xticks([]); ax_o.set_yticks([])
        title(ax_o, "Після пулінгу 13×13", GREEN)
        foot.set_text(f"вікон оброблено: {k} із {n}" if k < n else "Готово: контури цифри збережено, чисел у 4 рази менше (676 → 169)")

    save_video(fig, update, total, "anim-02-pool-feature-map", 6, total - 1)

def vid_shift():
    shifts = [0, 1, 2, 3]
    fig = plt.figure(figsize=(13, 5.8)); fig.patch.set_facecolor("white")
    ax_d = fig.add_axes([0.02, 0.18, 0.2, 0.2 * 13 / 5.8 * 0.0 + 0.58]); ax_r = fig.add_axes([0.28, 0.18, 0.22, 0.58]); ax_p = fig.add_axes([0.56, 0.18, 0.22, 0.58]); ax_t = fig.add_axes([0.80, 0.2, 0.19, 0.55]); ax_t.axis("off")
    head = fig.text(0.5, 0.93, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    per = 5; total = per * len(shifts) + 6

    def update(f):
        s = shifts[min(f // per, len(shifts) - 1)]
        im = np.roll(seven, s, axis=1); b = fmap(im); pb = maxpool(b)
        ax_d.clear(); ax_d.imshow(im, cmap="gray"); ax_d.set_xticks([]); ax_d.set_yticks([]); title(ax_d, "Вхід")
        mimg(ax_r, b, "Карта ознак 26×26"); mimg(ax_p, pb, "Після пулінгу 13×13", GREEN)
        ax_t.clear(); ax_t.axis("off")
        ax_t.text(0, 0.85, "кореляція з оригіналом", fontsize=11.5, color=MUTED, fontweight="bold")
        ax_t.text(0, 0.62, f"карта: {corr(A, b):.2f}", fontsize=16, color=RED, fontweight="bold")
        ax_t.text(0, 0.40, f"пулінг: {corr(PA, pb):.2f}", fontsize=16, color=GREEN, fontweight="bold")
        head.set_text("Без зсуву" if s == 0 else f"Цифра зсунута на {s} пікс. вправо")

    save_video(fig, update, total, "anim-03-shift-robustness", 4, total - 1)

def vid_rf():
    fig = plt.figure(figsize=(12, 5.6)); fig.patch.set_facecolor("white")
    ax_d = fig.add_axes([0.04, 0.12, 0.38, 0.66]); ax_t = fig.add_axes([0.50, 0.10, 0.46, 0.72]); ax_t.axis("off")
    fig.text(0.5, 0.93, "Поле зору одного числа росте від шару до шару", ha="center", fontsize=15, fontweight="bold", color=INK)
    names = [("Вхід", 1)] + RF_STAGES; per = 5; total = per * len(names) + 6

    def update(f):
        k = min(f // per, len(names) - 1); r = names[k][1]
        ax_d.clear(); ax_d.imshow(seven, cmap="gray"); ax_d.set_xticks([]); ax_d.set_yticks([])
        ax_d.add_patch(patches.Rectangle((13.5 - r / 2, 13.5 - r / 2), r, r, fill=True, facecolor=CYAN, alpha=.25, edgecolor=CYAN, lw=3))
        title(ax_d, f"Ділянка входу {r}×{r}", INK, 13)
        ax_t.clear(); ax_t.axis("off")
        for q, (nm, rr) in enumerate(names):
            y = 0.92 - q * 0.16; active = q == k
            ax_t.text(0.0, y, f"{'▶ ' if active else '   '}{nm}", fontsize=14, fontweight="bold" if active else "normal", color=CYAN if active else (INK if q < k else MUTED), transform=ax_t.transAxes)
            ax_t.text(0.78, y, f"{rr}×{rr}", fontsize=14, fontweight="bold" if active else "normal", color=CYAN if active else (INK if q < k else MUTED), transform=ax_t.transAxes)
        ax_t.text(0.0, 0.0, "Пулінг додає до поля зору більше, ніж ще одна Conv", fontsize=11, color=MUTED, transform=ax_t.transAxes)

    save_video(fig, update, total, "anim-04-receptive-field", 5, total - 1)

if __name__ == "__main__":
    img01(); img02(); img03(); img04(); img05(); img06(); vid_slide(); vid_map(); vid_shift(); vid_rf()
