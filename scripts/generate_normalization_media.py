"""
Media for content/16.ai-python/15.cnn-image-classification/12.weight-init-batchnorm.md  (needs temp/normalization_cache.pt)
Images -> public/images/ai-python/cnn-image-classification/init-batchnorm/
  01 activation std per layer (30 layers)  02 activation histograms by layer  03 10-layer MLP: loss + gradient norms
  04 BatchNorm axes (1d / 2d)  05 4th conv output before/after BN  06 CIFAR plain vs BN  07 drift of activations during training
Videos -> public/videos/ai-python/cnn-image-classification/init-batchnorm/
  anim-01-signal-depth
"""
import os, sys
sys.path.insert(0, "scripts")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from normalization_core import INITS, DEPTH_A, CIFAR_RUNS, load_cache

plt.rcParams["font.family"] = "DejaVu Sans"
IMG = "public/images/ai-python/cnn-image-classification/init-batchnorm"
VID = "public/videos/ai-python/cnn-image-classification/init-batchnorm"
os.makedirs(IMG, exist_ok=True); os.makedirs(VID, exist_ok=True)
INK, MUTED, AMBER, CYAN, GREEN, RED, PURPLE = "#0F172A", "#64748B", "#F59E0B", "#0EA5E9", "#10B981", "#EF4444", "#8B5CF6"
DPI, VIDEO_DPI = 80, 110
INIT_STYLE = {"N(0,1)": ("N(0; 1)", RED), "N(0,0.01)": ("N(0; 0,01)", AMBER), "default": ("PyTorch за замовч.", MUTED), "xavier": ("Xavier", CYAN), "he": ("He (Kaiming)", GREEN)}
def save_png(fig, name): fig.savefig(os.path.join(IMG, name), dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig); print("saved", name)
def despine(ax): [ax.spines[s].set_visible(False) for s in ("top", "right")]

def img01(C):
    fig, axs = plt.subplots(1, 2, figsize=(15, 5.2), sharey=True)
    for ax, act, t in zip(axs, ("tanh", "relu"), ("tanh", "ReLU")):
        for init in INITS:
            lab, c = INIT_STYLE[init]; s = np.maximum(C["A"][(act, init)]["std"], 1e-38)
            ax.plot(range(DEPTH_A + 1), s, color=c, lw=3 if init == "he" or (init == "xavier" and act == "tanh") else 2, label=lab)
        ax.axhline(1, color=INK, lw=0.8, ls=":"); ax.set_yscale("log"); ax.set_ylim(1e-30, 1e34); ax.set_xlabel("номер шару", color=MUTED)
        ax.set_title(f"Активація {t}", fontsize=13, fontweight="bold", color=INK); despine(ax)
    axs[0].set_ylabel("std активацій (логарифмічна шкала)", color=MUTED); axs[0].legend(frameon=False, fontsize=10, loc="lower left")
    fig.suptitle("Що лишається від сигналу після 30 шарів по 256 нейронів (вхід: 512 випадкових векторів зі std = 1)", fontsize=13.5, fontweight="bold", color=INK, y=1.02)
    save_png(fig, "01.png")

HIST_CASES = [("tanh", "N(0,1)", "tanh, N(0; 1)"), ("relu", "N(0,0.01)", "ReLU, N(0; 0,01)"), ("relu", "he", "ReLU, He")]
def img02(C):
    layers = [1, 3, 10, 30]; fig, axs = plt.subplots(3, 4, figsize=(15, 8.2))
    for r, (act, init, name) in enumerate(HIST_CASES):
        c = INIT_STYLE[init][1]
        for k, L in enumerate(layers):
            ax = axs[r, k]; h = C["A"][(act, init)]["hist"][L].detach().numpy(); ax.hist(h, bins=np.linspace(-3, 3, 61), color=c, alpha=.9)
            ax.set_yticks([]); despine(ax); ax.set_xlim(-3, 3); s = C["A"][(act, init)]["std"][L]
            ax.set_title(f"шар {L}: std = {s:.2g}", fontsize=11.5, color=INK, fontweight="bold")
            if k == 0: ax.set_ylabel(name, fontsize=12, fontweight="bold", color=c)
    fig.suptitle("Розподіл активацій (однакова шкала по x: від −3 до 3)", fontsize=14, fontweight="bold", color=INK, y=1.0); fig.tight_layout()
    save_png(fig, "02.png")

def img03(C):
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.9)); sty = [("N(0,0.01)", "N(0; 0,01)", AMBER), ("default", "PyTorch за замовч.", MUTED), ("he", "He", GREEN)]
    for init, lab, c in sty:
        r = C["B"][("sgd", init)]; l = np.array(r["losses"]); axs[0].plot(np.arange(1, len(l) + 1) * 10, l, color=c, lw=1.4, label=lab, alpha=.9)
        axs[1].plot(range(1, 11), r["grad_norms"], marker="o", color=c, lw=2.2, label=lab)
        ra = C["B"][("adam", init)]; axs[2].plot([1, 2, 3], np.array(ra["acc"]) * 100, marker="o", color=c, lw=2.4, label=lab)
    axs[0].set_title("SGD: втрата під час навчання", fontsize=12.5, fontweight="bold", color=INK); axs[0].set_xlabel("крок"); axs[0].legend(frameon=False, fontsize=10)
    axs[1].set_yscale("log"); axs[1].set_title("Норма градієнта ваг кожного шару, крок 0", fontsize=12.5, fontweight="bold", color=INK); axs[1].set_xlabel("шар (1 — біля входу, 10 — біля виходу)")
    axs[2].set_title("Adam, lr = 0,001: точність на тесті, %", fontsize=12.5, fontweight="bold", color=INK); axs[2].set_xlabel("епоха"); axs[2].set_xticks([1, 2, 3])
    for a in axs: despine(a); a.xaxis.label.set_color(MUTED)
    save_png(fig, "03.png")

def img04():
    fig, axs = plt.subplots(1, 2, figsize=(15, 5.3))
    ax = axs[0]; ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off"); ax.set_title("BatchNorm1d: тензор (N, C) — статистика по рядках", fontsize=12.5, fontweight="bold", color=INK)
    cols = 6; rows = 6
    for i in range(rows):
        for j in range(cols):
            hl = (j == 2); ax.add_patch(patches.Rectangle((1.3 + j * 1.1, 1.4 + (rows - 1 - i) * 0.9), 1.0, 0.8, fc="#FEF3C7" if hl else "#F1F5F9", ec=AMBER if hl else "#CBD5E1", lw=2 if hl else 1))
    ax.text(1.3 + cols * 0.55, 0.7, "ознаки (C = 6)", ha="center", fontsize=11, color=MUTED); ax.text(0.9, 1.4 + rows * 0.45, "приклади у батчі (N)", rotation=90, va="center", ha="center", fontsize=11, color=MUTED)
    ax.text(1.3 + 2.5 * 1.1, 0.0, "μ₂, σ₂² — одна пара на всі N значень стовпчика", ha="center", fontsize=11, color=AMBER, fontweight="bold")
    ax = axs[1]; ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off"); ax.set_title("BatchNorm2d: тензор (N, C, H, W) — статистика по (N, H, W)", fontsize=12.5, fontweight="bold", color=INK)
    for c in range(3):
        for n in range(3):
            x0 = 0.8 + c * 3.1 + n * 0.0; y0 = 4.4 - n * 1.25
            hl = (c == 1); ax.add_patch(patches.Rectangle((x0, y0), 2.4, 1.0, fc="#CFFAFE" if hl else "#F1F5F9", ec=CYAN if hl else "#CBD5E1", lw=2 if hl else 1))
            for q in range(1, 4): ax.plot([x0 + q * 0.6] * 2, [y0, y0 + 1.0], color=CYAN if hl else "#CBD5E1", lw=0.6)
            ax.text(x0 + 1.2, y0 + .35, f"H×W", ha="center", fontsize=9, color=MUTED)
        ax.text(0.8 + c * 3.1 + 1.2, 5.9, f"канал {c + 1}", ha="center", fontsize=11, color=CYAN if c == 1 else MUTED, fontweight="bold")
    ax.text(5.0, 0.7, "одна пара (μ, σ²) на канал: усереднення по N зображеннях і по всіх H×W позиціях", ha="center", fontsize=11, color=CYAN, fontweight="bold")
    ax.text(0.2, 4.9, "N", fontsize=11, color=MUTED); save_png(fig, "04.png")

def img05(C):
    s = {s["step"]: s for s in C["C"][(True, 1e-3, 0)]["snaps"]}[1000]
    fig, axs = plt.subplots(1, 2, figsize=(14, 4.6)); bins = np.linspace(-6, 6, 90)
    for ax, (k, t, c) in zip(axs, (("conv", "Вихід згортки (до BatchNorm)", PURPLE), ("pre_relu", "Після BatchNorm (вхід ReLU)", GREEN))):
        h = s[k]["sample"].numpy(); ax.hist(h, bins=bins, color=c, alpha=.9); ax.axvline(0, color=INK, lw=0.8, ls=":")
        ax.set_title(f"{t}\nсереднє = {s[k]['mean']:.2f}, std = {s[k]['std']:.2f}", fontsize=12.5, fontweight="bold", color=c); ax.set_yticks([]); despine(ax)
    fig.suptitle("4-й згортковий шар після 1000 кроків: ті самі дані, до і після нормалізації", fontsize=13.5, fontweight="bold", color=INK, y=1.04); save_png(fig, "05.png")

def img06(C):
    fig, axs = plt.subplots(1, 2, figsize=(15, 5.2)); ep = np.arange(1, 9)
    for bn, lab, c in ((False, "без BatchNorm", RED), (True, "з BatchNorm", GREEN)):
        runs = np.array([[h["test_acc"] for h in C["C"][(bn, 1e-3, s)]["hist"]] for s in range(3)]) * 100
        for r in runs: axs[0].plot(ep, r, color=c, lw=1, alpha=.35)
        axs[0].plot(ep, runs.mean(0), color=c, lw=3, marker="o", label=f"{lab} ({runs[:, -1].mean():.1f}%)")
        r2 = np.array([h["test_acc"] for h in C["C"][(bn, 1e-2, 0)]["hist"]]) * 100; axs[1].plot(ep, r2, color=c, lw=3, marker="o", label=f"{lab} ({r2[-1]:.1f}%)")
    axs[0].set_title("lr = 0,001 (3 зерна: тонкі лінії; товста — середнє)", fontsize=12.5, fontweight="bold", color=INK)
    axs[1].set_title("lr = 0,01 (в 10 разів більший)", fontsize=12.5, fontweight="bold", color=INK)
    for a in axs: a.set_xlabel("епоха", color=MUTED); a.set_ylabel("точність на тесті, %", color=MUTED); a.legend(frameon=False, fontsize=11, loc="center right"); despine(a)
    save_png(fig, "06.png")

def img07(C):
    fig, axs = plt.subplots(1, 2, figsize=(15, 4.9))
    for bn, lab, c in ((False, "без BatchNorm", RED), (True, "з BatchNorm", GREEN)):
        sn = C["C"][(bn, 1e-3, 0)]["snaps"]; st = [max(s["step"], 1) for s in sn]
        for ax, key, ttl in ((axs[0], "mean", "Середнє"), (axs[1], "std", "Стандартне відхилення")):
            ax.plot(st, [s["pre_relu"][key] for s in sn], color=c, lw=3, marker="o", label=lab + ": вхід ReLU")
            if bn: ax.plot(st, [s["conv"][key] for s in sn], color=PURPLE, lw=2, ls="--", marker="s", label="з BatchNorm: вихід згортки (до BN)")
            ax.set_xscale("log"); ax.set_title(f"{ttl} входу 4-го ReLU (на фіксованих 512 картинках)", fontsize=12, fontweight="bold", color=INK); ax.set_xlabel("крок навчання (0 показано як 1)", color=MUTED); despine(ax)
    axs[0].legend(frameon=False, fontsize=10); save_png(fig, "07.png")

def save_video(fig, update, n, stem, fps, poster):
    base = os.path.join(VID, stem); anim = FuncAnimation(fig, update, frames=n, interval=1000 / fps); common = ["-r", "24", "-pix_fmt", "yuv420p"]
    anim.save(base + ".mp4", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libx264", extra_args=common + ["-crf", "20", "-movflags", "+faststart"]))
    anim.save(base + ".webm", dpi=VIDEO_DPI, writer=FFMpegWriter(fps=fps, codec="libvpx-vp9", extra_args=common + ["-b:v", "0", "-crf", "34"]))
    anim.save(base + ".gif", dpi=DPI, writer=PillowWriter(fps=fps)); update(poster); fig.savefig(base + "-poster.png", dpi=VIDEO_DPI, facecolor="white"); plt.close(fig)
    print("saved", stem, f"mp4 {os.path.getsize(base + '.mp4') // 1024} KB")

def vid_signal(C):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.2)); fig.patch.set_facecolor("white"); FR = DEPTH_A + 1 + 10
    head = fig.text(0.5, 0.97, "", ha="center", fontsize=15, fontweight="bold", color=INK)
    def update(f):
        L = min(f, DEPTH_A); head.set_text(f"Шар {L} із {DEPTH_A}: ReLU, три способи ініціалізації")
        for ax, (act, init, name) in zip(axs, HIST_CASES[1:2] + [("relu", "default", "PyTorch за замовч.")] + HIST_CASES[2:]):
            ax.clear(); c = INIT_STYLE[init][1]; d = C["A"][(act, init)]
            ax.hist(d["hist"][L].detach().numpy(), bins=np.linspace(-3, 3, 61), color=c, alpha=.9); ax.set_xlim(-3, 3); ax.set_yticks([]); despine(ax)
            ax.set_title(f"{name}\nstd = {d['std'][L]:.2g}", fontsize=12.5, fontweight="bold", color=c)
    save_video(fig, update, FR, "anim-01-signal-depth", 8, FR - 1)

if __name__ == "__main__":
    C = load_cache(); img01(C); img02(C); img03(C); img04(); img05(C); img06(C); img07(C); vid_signal(C)
