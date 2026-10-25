"""
Media for content/16.ai-python/15.cnn-image-classification/13.layernorm-gradient-clipping.md  (needs temp/normclip_cache.pt)
Images -> public/images/ai-python/cnn-image-classification/layernorm-clipping/
  01 normalization axes BN vs LN  02 batch size x normalization  03 rescue of the 10-layer default-init MLP
  04 gradient norm history lr=1.0 without / with clipping  05 lr x clipping grid  06 clip by norm vs by value
"""
import os, sys
sys.path.insert(0, "scripts")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from norm_clip_core import D_NORMS, D_BATCHES, D_SEEDS, G_LRS, G_SEEDS, load_cache

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/layernorm-clipping"
os.makedirs(IMG, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
NORM_STYLE = {"none": ("без нормалізації", MUTED), "bn": ("BatchNorm", GREEN), "ln": ("LayerNorm", PURPLE)}
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def despine(ax): [ax.spines[s].set_visible(False) for s in ("top", "right")]

def img01():
    fig, axs = plt.subplots(1, 2, figsize=(15, 5.2)); rows, cols = 6, 6
    for ax, mode, title, col in ((axs[0], "bn", "BatchNorm: статистика по стовпцю (по прикладах батча)", AMBER), (axs[1], "ln", "LayerNorm: статистика по рядку (по ознаках одного прикладу)", PURPLE)):
        ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off"); ax.set_title(title, fontsize=12.5, fontweight="bold", color=INK)
        for i in range(rows):
            for j in range(cols):
                hl = (j == 2) if mode == "bn" else (i == 2)
                ax.add_patch(patches.Rectangle((1.3 + j * 1.1, 1.4 + (rows - 1 - i) * 0.9), 1.0, 0.8, fc=("#FEF3C7" if mode == "bn" else "#EDE9FE") if hl else "#F1F5F9", ec=col if hl else "#CBD5E1", lw=2 if hl else 1))
        ax.text(1.3 + cols * 0.55, 0.7, "ознаки (C)", ha="center", fontsize=11, color=MUTED); ax.text(0.9, 1.4 + rows * 0.45, "приклади (N)", rotation=90, va="center", ha="center", fontsize=11, color=MUTED)
    axs[0].text(5.0, 7.3, "залежить від інших прикладів у батчі", ha="center", fontsize=11, color=AMBER, fontweight="bold")
    axs[1].text(5.0, 7.3, "кожен приклад нормалізується сам, без батча", ha="center", fontsize=11, color=PURPLE, fontweight="bold")
    save_png(fig, "01.png")

def img02(C):
    fig, ax = plt.subplots(figsize=(10.5, 5.2)); x = np.arange(len(D_BATCHES))
    for n in D_NORMS:
        lab, c = NORM_STYLE[n]; runs = np.array([[C["D"][(n, b, s)]["acc"][-1] for s in D_SEEDS] for b in D_BATCHES]) * 100
        for k in range(len(D_SEEDS)): ax.plot(x, runs[:, k], "o", color=c, alpha=.3, ms=6)
        ax.plot(x, runs.mean(1), "-o", color=c, lw=3, ms=8, label=lab)
    ax.set_xticks(x); ax.set_xticklabels([f"B = {b}" for b in D_BATCHES]); ax.set_ylabel("точність на тесті після 2 епох, %", color=MUTED); ax.legend(frameon=False, fontsize=11); despine(ax)
    ax.set_title("CNN на MNIST (Adam, lr = 0,001): розмір батча й нормалізація (великі точки — середнє, блідо — зерна)", fontsize=12, fontweight="bold", color=INK)
    save_png(fig, "02.png")

def img03(C):
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    for n in ("none", "bn", "ln"):
        lab, c = NORM_STYLE[n]; a = np.array(C["F"][n]["acc"]) * 100; ax.plot([1, 2, 3], a, "-o", color=c, lw=3, ms=9, label=f"{lab}: {a[-1]:.2f}%")
    ax.set_xticks([1, 2, 3]); ax.set_xlabel("епоха", color=MUTED); ax.set_ylabel("точність на тесті, %", color=MUTED); ax.legend(frameon=False, fontsize=11, loc="center right"); despine(ax)
    ax.set_title("10 шарів, ваги за замовчуванням, SGD lr = 0,05 (та сама мережа, що застрягла в лекції 12)", fontsize=11.5, fontweight="bold", color=INK)
    save_png(fig, "03.png")

def img04(C):
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.8))
    r = C["G"][(1.0, None, 0)]; n = np.array(r["norms"]); k = int(np.argmax(np.isnan(r["losses"])))
    fin = [i for i in range(k) if np.isfinite(n[i])]; axs[0].semilogy(fin, n[fin], color=RED, lw=2.5, marker="o"); axs[0].set_title(f"Без обрізання: норма градієнта, кроки 0–{k - 1}\nкрок {k - 1}: inf, а на кроці {k} втрата стає nan", fontsize=12, fontweight="bold", color=RED)
    for i in fin: axs[0].annotate(f"{n[i]:.3g}", (i, n[i]), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=10, color=INK)
    axs[0].set_xlabel("крок", color=MUTED); axs[0].set_xticks(range(k)); axs[0].set_xlim(-.3, k - .7); axs[0].set_ylim(1, 1e6)
    rc = C["G"][(1.0, 1.0, 0)]; nc = np.array(rc["norms"])
    axs[1].semilogy(nc, color=GREEN, lw=0.9); axs[1].axhline(1.0, color=INK, ls="--", lw=1.2); axs[1].text(len(nc) * .98, 0.62, "max_norm = 1", ha="right", fontsize=10.5, color=INK, bbox=dict(fc="white", ec="none", pad=1))
    axs[1].set_title("З обрізанням: норма градієнта\nдо обрізання (оптимізатор бачить ≤ 1)", fontsize=12, fontweight="bold", color=GREEN); axs[1].set_xlabel("крок (1 епоха = 938)", color=MUTED)
    ls = np.array(rc["losses"]); w = 20; sm = np.convolve(ls, np.ones(w) / w, mode="valid")
    axs[2].plot(ls, color=GREEN, lw=0.6, alpha=.4); axs[2].plot(np.arange(len(sm)) + w // 2, sm, color=GREEN, lw=2.5); axs[2].set_title("З обрізанням: втрата на навчанні\n(точність на тесті 94,71%)", fontsize=12, fontweight="bold", color=GREEN); axs[2].set_xlabel("крок", color=MUTED)
    for a in axs: despine(a)
    fig.suptitle("10-шарова мережа з ініціалізацією He, SGD з lr = 1,0 (зерно 0)", fontsize=13.5, fontweight="bold", color=INK, y=1.04); save_png(fig, "04.png")

def img05(C):
    fig, ax = plt.subplots(figsize=(11, 5.2)); x = np.arange(len(G_LRS)); w = 0.38
    for off, clip, lab, c in ((-w / 2, None, "без обрізання", RED), (w / 2, 1.0, "clip_grad_norm_(max_norm = 1)", GREEN)):
        for i, lr in enumerate(G_LRS):
            a = np.array([C["G"][(lr, clip, s)]["acc"] for s in G_SEEDS]) * 100
            ax.bar(i + off, a.mean(), w * .92, color=c, alpha=.9, label=lab if i == 0 else None)
            ax.plot([i + off] * len(a), a, "o", color=INK, ms=4, alpha=.7)
            div = int(np.sum([np.isnan(C["G"][(lr, clip, s)]["losses"]).any() for s in G_SEEDS]))
            ax.text(i + off, a.mean() + 2, f"{a.mean():.0f}" + (f"\nnan: {div}/3" if div else ""), ha="center", fontsize=9.5, color=INK, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels([f"lr = {lr}" for lr in G_LRS]); ax.set_ylabel("точність на тесті після 1 епохи, %", color=MUTED); ax.set_ylim(0, 112); ax.legend(frameon=False, fontsize=11, loc="lower left"); despine(ax)
    ax.set_title("10-шаровий MLP (He, SGD): швидкість навчання проти обрізання (стовпчик — середнє з 3 зерен, крапки — зерна)", fontsize=11.5, fontweight="bold", color=INK)
    save_png(fig, "05.png")

def img06():
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 5.6), sharey=True); g = np.array([3., 4.])
    for ax, (t, new, c, note) in zip(axs, (("clip_grad_norm_: масштабуємо весь вектор", g / 5, GREEN, "напрямок збережено, довжина 5 → 1"), ("clip_grad_value_: обрізаємо кожну компоненту", np.clip(g, -1, 1), RED, "напрямок змінився: (3; 4) → (1; 1)"))):
        ax.annotate("", xy=g, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=3)); ax.text(3.1, 4.1, "g = (3; 4), ‖g‖ = 5", fontsize=11, color=MUTED)
        ax.annotate("", xy=new, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=4)); ax.text(new[0] + .15, new[1] - .45, f"({new[0]:.1f}; {new[1]:.1f})", fontsize=11.5, color=c, fontweight="bold")
        ax.add_patch(patches.Circle((0, 0), 1, fill=False, ec=INK, ls="--", lw=1)) if c == GREEN else ax.add_patch(patches.Rectangle((-1, -1), 2, 2, fill=False, ec=INK, ls="--", lw=1))
        ax.set_xlim(-1.5, 5); ax.set_ylim(-1.5, 5); ax.set_aspect("equal"); ax.set_title(f"{t}\n{note}", fontsize=11.5, fontweight="bold", color=c); ax.axhline(0, color="#CBD5E1", lw=.8); ax.axvline(0, color="#CBD5E1", lw=.8); despine(ax)
    save_png(fig, "06.png")

if __name__ == "__main__":
    C = load_cache(); img01(); img02(C); img03(C); img04(C); img05(C); img06()
