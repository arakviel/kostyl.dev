"""Один крок уваги: запит декодера, ваги над станами енкодера, контекст."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 5.2)
words = ["I", "am", "a", "student"]; w = [0.16, 0.21, 0.18, 0.45]
box(ax, 2, 70, 18, 14, "стан декодера\nsₜ (запит)", fc=GREEN, size=12)
for i, (wd, a) in enumerate(zip(words, w)):
    x = 14 + i * 20
    box(ax, x, 6, 14, 12, f"h{'₁₂₃₄'[i]}", fc=BLUE, size=13)
    ax.text(x + 7, 0, wd, ha="center", va="top", fontsize=12, fontfamily="DejaVu Sans Mono")
    ax.add_patch(FancyBboxPatch((x + 2, 36), 10, 9, boxstyle="round,pad=0.3,rounding_size=1.5", fc=AMBER, ec=INK, lw=1.3))
    ax.text(x + 7, 40.5, f"{a:.2f}", ha="center", va="center", fontsize=12.5, fontweight="bold" if a > 0.4 else "normal")
    ax.plot([x + 7, x + 7], [18.5, 35.5], color=INK, lw=0.8 + 6 * a, solid_capstyle="butt", alpha=0.85)
    ax.plot([x + 7, x + 7], [46, 55], color=INK, lw=0.8 + 6 * a, solid_capstyle="butt", alpha=0.85)
ax.plot([21, 81], [55, 55], color=INK, lw=1.2)
arrow(ax, 51, 55, 51, 61)
box(ax, 38, 62, 26, 14, "контекст c = Σ αᵢ·hᵢ", fc=AMBER, size=12)
arrow(ax, 20.7, 77, 37.5, 69, "")
ax.text(25, 85, "порівняти sₜ з кожним hᵢ → softmax", fontsize=11, color="#475569", ha="left")
ax.text(91, 40.5, "α — ваги\nуваги\n(сума = 1)", fontsize=11.5, color="#475569", va="center")
save(fig, __file__)
