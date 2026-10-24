"""
Images for content/16.ai-python/15.cnn-image-classification/02.why-convolution.md
Target: public/images/ai-python/cnn-image-classification/why-convolution/
- 01.png: one neuron as a template matcher (3 patches x template -> sum)
- 02.png: whole-image neuron breaks when the line shifts by one pixel
- 03.png: the same small detector at every position: response maps for two images
- 04.png: dense vs local vs local+shared connections (1D sketch)
- 05.png: parameter counts (dense / local / shared)
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'DejaVu Sans'
OUT = "public/images/ai-python/cnn-image-classification/why-convolution"
os.makedirs(OUT, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444"

K = np.array([[-1, 1, -1]] * 3)            # vertical-stroke detector
def line_image(col):
    im = np.zeros((6, 6), dtype=int); im[:, col] = 1; return im
A, B = line_image(2), line_image(4)

def response_map(im):
    out = np.zeros((4, 4), dtype=int)
    for i in range(4):
        for j in range(4):
            out[i, j] = int((im[i:i+3, j:j+3] * K).sum())
    return out

def signed(v):
    return "0" if v == 0 else f"{v:+d}"

def grid(ax, M, cmap, vmin, vmax, fmt="{}", dark_below=None):
    ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax)
    r, c = M.shape
    for i in range(r):
        for j in range(c):
            v = M[i, j]
            mid = (vmin + vmax) / 2
            col = "white" if (cmap == "gray" and v < 0.5) else INK
            ax.text(j, i, (fmt(v) if callable(fmt) else fmt.format(v)), ha="center", va="center", fontsize=13, fontweight="bold", color=col)
    for k in range(r + 1): ax.axhline(k - .5, color="#94A3B8", lw=.8)
    for k in range(c + 1): ax.axvline(k - .5, color="#94A3B8", lw=.8)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, facecolor="white", bbox_inches="tight")
    plt.close(fig); print("saved", name)

# 01 ---------------------------------------------------------------
def gen01():
    patches_ = [
        ("Штрих посередині", np.array([[0,1,0]]*3)),
        ("Штрих збоку", np.array([[0,0,1]]*3)),
        ("Порожньо", np.zeros((3,3), dtype=int)),
    ]
    fig, axs = plt.subplots(3, 4, figsize=(11, 8), gridspec_kw={"width_ratios": [1, 1, 1, 0.9]})
    for r, (name, P) in enumerate(patches_):
        grid(axs[r, 0], P, "gray", 0, 1)
        grid(axs[r, 1], K, "RdYlGn", -2, 2)
        grid(axs[r, 2], P * K, "RdYlGn", -2, 2)
        s = int((P * K).sum())
        axs[r, 3].axis("off")
        axs[r, 3].text(0.0, 0.5, f"сума = {signed(s)}", fontsize=20, fontweight="bold", va="center",
                       color=GREEN if s > 0 else (RED if s < 0 else MUTED))
        axs[r, 0].set_ylabel(name, fontsize=12, fontweight="bold", color=INK)
        if r == 0:
            axs[r, 0].set_title("Ділянка 3×3", fontsize=12, color=INK, pad=8)
            axs[r, 1].set_title("Ваги нейрона", fontsize=12, color=INK, pad=8)
            axs[r, 2].set_title("Ділянка × ваги", fontsize=12, color=INK, pad=8)
    fig.suptitle("Нейрон як шаблон: велика сума означає «схоже на мої ваги»", fontsize=14, fontweight="bold", color=INK)
    save(fig, "01.png")

# 02 ---------------------------------------------------------------
def gen02():
    W = np.zeros((6, 6), dtype=int); W[:, 2] = 1
    fig, axs = plt.subplots(1, 5, figsize=(15, 3.8), gridspec_kw={"width_ratios": [1, 0.15, 1, 0.15, 1]}) if False else plt.subplots(1, 3, figsize=(13, 4.6))
    grid(axs[0], A, "gray", 0, 1); axs[0].set_title("Зображення A\nштрих у стовпці 2", fontsize=12, color=INK)
    grid(axs[1], W, "RdYlGn", -2, 2); axs[1].set_title("Ваги нейрона\n(шукає штрих у стовпці 2)", fontsize=12, color=INK)
    grid(axs[2], B, "gray", 0, 1); axs[2].set_title("Зображення B\nтой самий штрих, стовпець 4", fontsize=12, color=INK)
    axs[0].set_xlabel(f"відгук = {int((A*W).sum())}", fontsize=16, fontweight="bold", color=GREEN)
    axs[2].set_xlabel(f"відгук = {int((B*W).sum())}", fontsize=16, fontweight="bold", color=RED)
    fig.suptitle("Нейрон на всю картинку: штрих посунувся — нейрон «осліп»", fontsize=14, fontweight="bold", color=INK)
    save(fig, "02.png")

# 03 ---------------------------------------------------------------
def gen03():
    fig, axs = plt.subplots(2, 3, figsize=(13, 8.2), gridspec_kw={"width_ratios": [1.5, 0.35, 1]})
    for r, (name, im) in enumerate([("A: штрих у стовпці 2", A), ("B: штрих у стовпці 4", B)]):
        grid(axs[r, 0], im, "gray", 0, 1)
        axs[r, 0].set_title(f"Зображення {name}", fontsize=12, color=INK)
        axs[r, 1].axis("off")
        axs[r, 1].annotate("", xy=(1, .5), xytext=(0, .5), arrowprops=dict(arrowstyle="->", lw=2.5, color=CYAN))
        axs[r, 1].text(.5, .62, "ковзаємо\nдетектором", ha="center", fontsize=10, color=CYAN)
        R = response_map(im)
        grid(axs[r, 2], R, "RdYlGn", -3, 3, fmt=signed)
        ys, xs = np.where(R == R.max())
        for y, x in zip(ys, xs):
            axs[r, 2].add_patch(patches.Rectangle((x-.5, y-.5), 1, 1, fill=False, edgecolor=AMBER, lw=3))
        axs[r, 2].set_title("Карта відгуків 4×4", fontsize=12, color=INK)
        axs[r, 2].set_xlabel(f"максимум = {R.max()}", fontsize=14, fontweight="bold", color=INK)
    fig.suptitle("Той самий детектор у кожній позиції: пік пересунувся разом зі штрихом, а максимум не змінився",
                 fontsize=13.5, fontweight="bold", color=INK)
    save(fig, "03.png")

# 04 ---------------------------------------------------------------
def gen04():
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.2))
    xs_in, xs_out = np.arange(6), np.arange(4) + 1
    titles = ["Повні зв'язки (Dense)\n6×4 = 24 ваги", "Лише локальні зв'язки\n4×3 = 12 ваг", "Локальні + спільні ваги\n3 ваги на весь шар"]
    wcol = ["#EF4444", "#10B981", "#3B82F6"]
    for k, ax in enumerate(axs):
        for o in range(4):
            for i in range(6):
                if k == 0:
                    ax.plot([i, xs_out[o]], [0, 1], color="#94A3B8", lw=1)
                elif i in (o, o+1, o+2):
                    c = "#94A3B8" if k == 1 else wcol[i - o]
                    ax.plot([i, xs_out[o] - 0.5 + 0.5 + 0], [0, 1], color=c, lw=2.2 if k == 2 else 1.6)
        ax.scatter(xs_in, np.zeros(6), s=420, color="white", edgecolor=INK, zorder=3, lw=1.8)
        ax.scatter(xs_out, np.ones(4), s=420, color="#DBEAFE", edgecolor=INK, zorder=3, lw=1.8)
        for i in range(6): ax.text(i, 0, f"x{i+1}", ha="center", va="center", fontsize=10, zorder=4)
        for o in range(4): ax.text(xs_out[o], 1, f"y{o+1}", ha="center", va="center", fontsize=10, zorder=4)
        ax.set_title(titles[k], fontsize=13, fontweight="bold", color=INK, pad=10)
        ax.set_xlim(-.6, 5.6); ax.set_ylim(-.35, 1.35); ax.axis("off")
    axs[2].text(2.5, -.28, "червона = w₁   зелена = w₂   синя = w₃", ha="center", fontsize=11, color=INK)
    save(fig, "04.png")

# 05 ---------------------------------------------------------------
def gen05():
    labels = ["Dense\n784 → 676", "Локальні\nзв'язки", "Локальні +\nспільні ваги"]
    vals = [784 * 676, 676 * 9, 9]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    bars = ax.bar(labels, vals, color=["#EF4444", AMBER, GREEN], width=.55)
    ax.set_yscale("log"); ax.set_ylim(1, 5e6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v * 1.25, f"{v:,}".replace(",", " "), ha="center", fontsize=15, fontweight="bold", color=INK)
    ax.set_ylabel("Кількість ваг (логарифмічна шкала)", fontsize=12, color=INK)
    ax.set_title("Скільки ваг потрібно, щоб шукати штрих у 676 позиціях", fontsize=14, fontweight="bold", color=INK, pad=12)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    save(fig, "05.png")

for g in (gen01, gen02, gen03, gen04, gen05): g()
