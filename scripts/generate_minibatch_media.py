"""
Media for content/16.ai-python/15.cnn-image-classification/11.mini-batch-learning-rate.md  (needs temp/minibatch_cache.pt)
Images -> public/images/ai-python/cnn-image-classification/mini-batch-learning-rate/
  01 toy paths (GD / mini-batch / SGD)  02 anatomy of an epoch  03 gradient noise vs batch size  04 batch x lr grid
  05 time per epoch  06 lr schedules  07 scheduler results
Videos -> public/videos/ai-python/cnn-image-classification/mini-batch-learning-rate/
  anim-01-toy-paths, anim-02-schedules
"""
import os, sys
sys.path.insert(0, "scripts")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from minibatch_core import BATCHES, LRS, NOISE_BATCHES, SCHEDS, SCHED_SEEDS, load_cache

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/mini-batch-learning-rate"
VID = "public/videos/ai-python/cnn-image-classification/mini-batch-learning-rate"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def despine(ax): [ax.spines[s].set_visible(False) for s in ("top", "right")]

# --- toy problem from Module 3: y = w*x + b, MSE; three ways to take steps ---------------------------------
rng = np.random.default_rng(0)
TX = rng.uniform(-3, 3, 200); TY = 2.0 * TX + 1.0 + rng.normal(0, 1.5, 200)
W_OPT, B_OPT = np.polyfit(TX, TY, 1)
def mse(w, b): return np.mean((w * TX + b - TY) ** 2)
TOY_LR, TOY_EPOCHS, START = 0.05, 4, np.array([-2.0, -3.0])
def toy_path(batch, seed=0):
    r = np.random.default_rng(seed); p = START.copy(); path = [p.copy()]
    for _ in range(TOY_EPOCHS):
        order = r.permutation(len(TX))
        for s in range(0, len(TX), batch):
            i = order[s:s + batch]; e = p[0] * TX[i] + p[1] - TY[i]
            p = p - TOY_LR * np.array([2 * np.mean(e * TX[i]), 2 * np.mean(e)]); path.append(p.copy())
    return np.array(path)
MODES = [("Весь датасет (B = 200)", 200, RED), ("Міні-батч (B = 20)", 20, GREEN), ("По одному (B = 1)", 1, PURPLE)]
PATHS = {B: toy_path(B) for _, B, _ in MODES}
GW, GB = np.meshgrid(np.linspace(-3, 3.2, 160), np.linspace(-4, 4, 160))
GZ = np.mean((GW[..., None] * TX + GB[..., None] - TY) ** 2, axis=-1)
def contour(ax):
    ax.contourf(GW, GB, GZ, levels=np.geomspace(GZ.min() + 0.05, GZ.max(), 22), cmap="Blues_r", alpha=.85)
    ax.plot(W_OPT, B_OPT, marker="*", ms=17, color=AMBER, mec=INK, mew=1, zorder=6); ax.set_xlabel("w", fontsize=11, color=MUTED); ax.set_ylabel("b", fontsize=11, color=MUTED)
    ax.set_xlim(-3, 3.2); ax.set_ylim(-4, 4)

def summary(C):
    print("== SUMMARY ==")
    for _, B, _ in MODES: p = PATHS[B]; print("toy B", B, "steps", len(p) - 1, "final", p[-1].round(3), "loss", round(mse(*p[-1]), 3))
    print("opt", W_OPT.round(3), B_OPT.round(3), "loss", round(mse(W_OPT, B_OPT), 3))
    for B in NOISE_BATCHES: print("noise", B, "cos", f"{np.mean(C['noise']['cos'][B]):.3f}", "rel", f"{np.mean(C['noise']['rel'][B]):.2f}")
    for B in BATCHES: print("grid", B, [f"{C['grid'][(B, lr)]['acc'][-1]:.4f}" for lr in LRS], "steps/epoch", C["grid"][(B, 1e-3)]["steps_per_epoch"], "sec/3ep", [round(C["grid"][(B, lr)]["secs"][-1]) for lr in LRS])
    for k in SCHEDS:
        fin = [C["sched"][(k, s)]["acc"][-1] for s in SCHED_SEEDS]; print("sched", k, [f"{a:.4f}" for a in fin], f"mean {np.mean(fin):.4f}")

def img01():
    fig, axs = plt.subplots(1, 3, figsize=(16, 5.3), sharey=True)
    for ax, (name, B, c) in zip(axs, MODES):
        contour(ax); p = PATHS[B]; ax.plot(p[:, 0], p[:, 1], "-", color=c, lw=1.6 if B > 1 else 1.0, alpha=.95, zorder=4); ax.plot(*p[0], "o", color=INK, ms=8, zorder=5); ax.plot(*p[-1], "o", color=c, ms=8, mec="white", zorder=5)
        ax.set_title(f"{name}\n{len(p) - 1} кроків за {TOY_EPOCHS} епохи", fontsize=12.5, fontweight="bold", color=c)
    fig.suptitle("Одна й та сама лінійна регресія й та сама швидкість навчання: різна кількість кроків і різний «шум»", fontsize=13.5, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "01.png")

def img02():
    fig, ax = plt.subplots(figsize=(15.5, 4.7)); ax.set_xlim(0, 31); ax.set_ylim(0, 9.4); ax.axis("off")
    ax.add_patch(patches.FancyBboxPatch((0.3, 2.2), 4.6, 4.2, boxstyle="round,pad=0.1", fc="#E0F2FE", ec=CYAN, lw=2.5))
    ax.text(2.6, 5.35, "Датасет", ha="center", fontsize=14, fontweight="bold", color=INK); ax.text(2.6, 4.2, "60 000\nцифр", ha="center", fontsize=13, color=INK)
    ax.text(2.6, 2.75, "shuffle=True →\nперемішали", ha="center", fontsize=10.5, color=MUTED)
    ax.annotate("", xy=(6.7, 4.3), xytext=(5.2, 4.3), arrowprops=dict(arrowstyle="->", lw=2.5, color=MUTED))
    for k in range(5):
        x = 7.0 + k * 3.55
        ax.add_patch(patches.FancyBboxPatch((x, 2.9), 2.9, 2.8, boxstyle="round,pad=0.05", fc="#D1FAE5", ec=GREEN, lw=2)); ax.text(x + 1.45, 4.55, f"батч {k + 1}", ha="center", fontsize=12, fontweight="bold", color=INK); ax.text(x + 1.45, 3.7, "64 цифри", ha="center", fontsize=10.5, color=INK)
        ax.text(x + 1.45, 2.3, "forward → loss\n→ backward → step", ha="center", va="top", fontsize=9, color=MUTED)
    ax.text(25.0, 4.3, "…", fontsize=26, ha="center", va="center", color=MUTED)
    ax.add_patch(patches.FancyBboxPatch((26.3, 2.9), 4.2, 2.8, boxstyle="round,pad=0.05", fc="#FEF3C7", ec=AMBER, lw=2)); ax.text(28.4, 4.55, "батч 938", ha="center", fontsize=12, fontweight="bold", color=INK); ax.text(28.4, 3.7, "32 цифри (залишок)", ha="center", fontsize=10.5, color=INK)
    ax.text(15.5, 7.9, "Одна епоха = 938 кроків оптимізатора (⌈60 000 / 64⌉)", ha="center", fontsize=15, fontweight="bold", color=INK)
    ax.text(15.5, 0.55, "після останнього батча епоха закінчується, датасет знову перемішується, і починається наступна", ha="center", fontsize=11.5, color=MUTED)
    save_png(fig, "02.png")

def img03(C):
    cos, rel = C["noise"]["cos"], C["noise"]["rel"]; fig, axs = plt.subplots(1, 2, figsize=(14.5, 5.2)); pos = np.arange(len(NOISE_BATCHES))
    for ax, d, ttl, ylab in ((axs[0], cos, "Косинус кута між градієнтом батча й повним градієнтом", "1 = той самий напрямок"), (axs[1], rel, "Відносна помилка ‖g_B − g‖ / ‖g‖", "0 = точний градієнт")):
        bp = ax.boxplot([d[B] for B in NOISE_BATCHES], positions=pos, widths=.55, patch_artist=True, showfliers=False, medianprops=dict(color=INK, lw=2))
        for b in bp["boxes"]: b.set(facecolor="#BAE6FD", edgecolor=CYAN, lw=1.8)
        for w in bp["whiskers"] + bp["caps"]: w.set(color=CYAN, lw=1.5)
        ax.set_xticks(pos); ax.set_xticklabels([str(B) for B in NOISE_BATCHES], fontsize=11.5); ax.set_xlabel("розмір батча B", fontsize=11.5, color=MUTED); ax.set_ylabel(ylab, fontsize=11, color=MUTED)
        ax.set_title(ttl, fontsize=12, fontweight="bold", color=INK); despine(ax)
    xs = np.array(NOISE_BATCHES, float)
    for ax, d in ((axs[0], cos), (axs[1], rel)): ax.plot(pos, [np.mean(d[B]) for B in NOISE_BATCHES], "D", color=RED, ms=8, zorder=5, label="середнє")
    axs[1].plot(pos, np.mean(rel[NOISE_BATCHES[-1]]) * np.sqrt(xs[-1] / xs), "--", color=AMBER, lw=2.2, label="~ 1/√B (через B = 2048)"); axs[1].legend(frameon=False, fontsize=10.5); axs[0].legend(frameon=False, fontsize=10.5, loc="lower right")
    save_png(fig, "03.png")

def img04(C):
    A = np.array([[C["grid"][(B, lr)]["acc"][-1] * 100 for lr in LRS] for B in BATCHES]); fig, ax = plt.subplots(figsize=(10.5, 5.7))
    im = ax.imshow(A, cmap="YlGn", vmin=85, vmax=99, aspect="auto")
    for i in range(len(BATCHES)):
        for j in range(len(LRS)):
            ax.text(j, i, f"{A[i, j]:.1f}", ha="center", va="center", fontsize=13, fontweight="bold", color="white" if A[i, j] > 96 else INK)
        j = int(A[i].argmax()); ax.add_patch(patches.Rectangle((j - .5, i - .5), 1, 1, fill=False, ec=RED, lw=3))
    ax.set_xticks(range(len(LRS))); ax.set_xticklabels([f"{lr:g}" for lr in LRS], fontsize=11.5); ax.set_yticks(range(len(BATCHES))); ax.set_yticklabels(BATCHES, fontsize=11.5)
    ax.set_xlabel("швидкість навчання lr (Adam)", fontsize=12, color=MUTED); ax.set_ylabel("розмір батча B", fontsize=12, color=MUTED)
    ax.set_title("Точність на тесті після 3 епох, %  (червона рамка — найкращий lr для цього B)", fontsize=12.5, fontweight="bold", color=INK, pad=10)
    save_png(fig, "04.png")

def img05(C):
    fig, axs = plt.subplots(1, 2, figsize=(14, 4.9))
    steps = [C["grid"][(B, 1e-3)]["steps_per_epoch"] for B in BATCHES]; secs = [np.mean([C["grid"][(B, lr)]["secs"][-1] / 3 for lr in LRS]) for B in BATCHES]
    b = axs[0].bar([str(B) for B in BATCHES], steps, color=CYAN, width=.6); axs[0].set_yscale("log"); axs[0].set_title("Кроків оптимізатора за епоху (логарифмічна шкала)", fontsize=12, fontweight="bold", color=INK)
    for r, v in zip(b, steps): axs[0].text(r.get_x() + r.get_width() / 2, v * 1.15, f"{v}", ha="center", fontsize=12, fontweight="bold", color=INK)
    axs[0].set_ylim(10, 20000)
    b = axs[1].bar([str(B) for B in BATCHES], secs, color=AMBER, width=.6); axs[1].set_title("Секунд на епоху (CPU, середнє за 5 значень lr)", fontsize=12, fontweight="bold", color=INK); axs[1].set_ylim(0, max(secs) * 1.3)
    for r, v in zip(b, secs): axs[1].text(r.get_x() + r.get_width() / 2, v + 0.3, f"{v:.1f}", ha="center", fontsize=12, fontweight="bold", color=INK)
    for a in axs: a.set_xlabel("розмір батча B", fontsize=11.5, color=MUTED); despine(a)
    save_png(fig, "05.png")

SCHED_STYLE = {"const-1e-3": ("постійний 1e-3", MUTED), "const-1e-2": ("постійний 1e-2", RED), "step": ("StepLR від 1e-2", AMBER), "cosine": ("Cosine від 1e-2", CYAN), "warmup-cosine": ("warmup + Cosine від 1e-2", GREEN)}
def img06(C):
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    for k in SCHEDS:
        lr = np.array(C["sched"][(k, 0)]["lr"]); n = len(lr) / 10; ax.plot(np.arange(1, len(lr) + 1) / n, lr, color=SCHED_STYLE[k][1], lw=2.8, label=SCHED_STYLE[k][0])
    ax.set_xlabel("епоха", fontsize=12, color=MUTED); ax.set_ylabel("lr", fontsize=12, color=MUTED); ax.set_yscale("log"); ax.legend(frameon=False, fontsize=11, loc="lower left"); despine(ax); ax.set_xticks(range(0, 11))
    ax.set_title("Як змінюється швидкість навчання впродовж 10 епох", fontsize=13.5, fontweight="bold", color=INK); save_png(fig, "06.png")

def img07(C):
    fig, axs = plt.subplots(1, 2, figsize=(15.5, 5.3), gridspec_kw={"width_ratios": [1.3, 1]}); ep = np.arange(1, 11)
    for k in SCHEDS:
        m = np.mean([np.array(C["sched"][(k, s)]["acc"]) for s in SCHED_SEEDS], axis=0) * 100; axs[0].plot(ep, m, marker="o", lw=2.6, color=SCHED_STYLE[k][1], label=SCHED_STYLE[k][0])
    axs[0].set_ylim(96.0, 99.4); axs[0].set_xticks(ep); axs[0].set_xlabel("епоха", fontsize=11.5, color=MUTED); axs[0].legend(frameon=False, fontsize=10.5, loc="lower right"); despine(axs[0])
    axs[0].set_title("Точність на тесті, % (середнє за 3 запуски)", fontsize=12.5, fontweight="bold", color=INK)
    for j, k in enumerate(SCHEDS):
        fin = [C["sched"][(k, s)]["acc"][-1] * 100 for s in SCHED_SEEDS]; axs[1].scatter([j] * 3, fin, color=SCHED_STYLE[k][1], s=60, zorder=3); axs[1].errorbar([j], [np.mean(fin)], yerr=[np.std(fin)], color=INK, capsize=7, lw=2, zorder=4)
        axs[1].text(j + 0.16, np.mean(fin), f"{np.mean(fin):.2f}", ha="left", va="center", fontsize=11.5, fontweight="bold", color=INK)
    axs[1].set_xticks(range(len(SCHEDS))); axs[1].set_xticklabels(["const\n1e-3", "const\n1e-2", "Step", "Cosine", "warmup\n+Cosine"], fontsize=10.5); axs[1].set_ylim(96.8, 99.6); axs[1].set_xlim(-0.5, 4.8); despine(axs[1])
    axs[1].set_title("Після 10-ї епохи, %", fontsize=12.5, fontweight="bold", color=INK); save_png(fig, "07.png")

def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps); common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps)); update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_toy():
    # the three optimisers walk in "time" = number of data passes (epochs), so the video shows steps per epoch visually
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.4), sharey=True); fig.patch.set_facecolor("white"); FR = 90
    head = fig.text(0.5, 0.97, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    def upto(B, f):
        n = len(PATHS[B]) - 1; return int(round(n * min(1.0, f / (FR - 12))))
    def update(f):
        for ax, (name, B, c) in zip(axs, MODES):
            ax.clear(); contour(ax); k = upto(B, f); p = PATHS[B][:k + 1]
            ax.plot(p[:, 0], p[:, 1], "-", color=c, lw=1.6 if B > 1 else 0.9, zorder=4); ax.plot(*p[0], "o", color=INK, ms=8, zorder=5); ax.plot(*p[-1], "o", color=c, ms=9, mec="white", zorder=5)
            ax.set_title(f"{name}\nкрок {k} із {len(PATHS[B]) - 1}, втрата {mse(*p[-1]):.2f}", fontsize=12, fontweight="bold", color=c)
        head.set_text(f"Епоха {min(TOY_EPOCHS, 1 + int(min(f, FR - 12) / (FR - 12) * TOY_EPOCHS - 1e-9))} із {TOY_EPOCHS}: усі троє бачать дані однакову кількість разів")
    save_video(fig, update, FR, "anim-01-toy-paths", 12, FR - 1)

def vid_sched(C):
    fig, axs = plt.subplots(1, 2, figsize=(14, 5.4)); fig.patch.set_facecolor("white"); n = len(C["sched"][("cosine", 0)]["lr"]); per = n // 10; FR = 70
    head = fig.text(0.5, 0.97, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    def update(f):
        t = int(n * min(1.0, f / (FR - 10))); e = t / per
        for a in axs: a.clear()
        for k in SCHEDS:
            lab, c = SCHED_STYLE[k]; lr = np.array(C["sched"][(k, 0)]["lr"])
            axs[0].plot(np.arange(1, t + 1) / per, lr[:t], color=c, lw=2.6, label=lab)
            ep = int(e); axs[1].plot(range(1, ep + 1), np.array(C["sched"][(k, 0)]["acc"][:ep]) * 100, marker="o", color=c, lw=2.4)
        axs[0].set_yscale("log"); axs[0].set_xlim(0, 10); axs[0].set_ylim(5e-6, 2e-2); axs[0].set_title("Швидкість навчання lr", fontsize=12.5, fontweight="bold", color=INK); axs[0].set_xlabel("епоха", color=MUTED)
        axs[1].set_xlim(0.5, 10.5); axs[1].set_ylim(96.5, 99.4); axs[1].set_title("Точність на тесті, % (зерно 0)", fontsize=12.5, fontweight="bold", color=INK); axs[1].set_xlabel("епоха", color=MUTED)
        axs[0].legend(frameon=False, fontsize=9.5, loc="lower left"); [despine(a) for a in axs]; head.set_text(f"Епоха {min(10, int(e) + 1)} із 10")
    save_video(fig, update, FR, "anim-02-schedules", 12, FR - 1)

if __name__ == "__main__":
    C = load_cache(); summary(C)
    img01(); img02(); img03(C); img04(C); img05(C); img06(C); img07(C); vid_toy(); vid_sched(C)
