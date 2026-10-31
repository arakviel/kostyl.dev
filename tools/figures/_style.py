"""Спільний стиль для картинок лекцій: білий фон, світла палітра, DejaVu Sans."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK = "#1E293B"
GREY = "#E2E8F0"
BLUE = "#DBEAFE"
GREEN = "#DCFCE7"
AMBER = "#FEF3C7"
RED = "#FEE2E2"
ACCENT = "#2563EB"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "text.color": INK,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

ROOT = Path(__file__).resolve().parent


def canvas(width=10, height=3.4):
    """Порожнє полотно з координатами 0..100 по обох осях."""
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=GREY, mono=False, size=13, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=2",
                                fc=fc, ec=INK, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            fontfamily="DejaVu Sans Mono" if mono else "DejaVu Sans", fontweight=weight,
            linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, label=None, size=11):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=18,
                                 lw=1.6, color=INK))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 4, label, ha="center", va="bottom", fontsize=size)


def save(fig, script_file):
    """tools/figures/<шлях>/NN-name.py -> public/images/<шлях>/NN-name.png"""
    script = Path(script_file).resolve()
    out = ROOT.parent.parent / "public" / "images" / script.parent.relative_to(ROOT) / f"{script.stem}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(out)


def chips(ax, x, y, tokens, fc=GREY, h=9, size=12, gap=1.2, char_w=1.55, pad=2.6, mono=True, colors=None):
    """Ряд «фішок»-токенів; повертає x правого краю."""
    for i, t in enumerate(tokens):
        w = max(5.0, len(t) * char_w + pad)
        color = colors[i] if colors else fc
        box(ax, x, y, w, h, t, fc=color, mono=mono, size=size)
        x += w + gap
    return x
