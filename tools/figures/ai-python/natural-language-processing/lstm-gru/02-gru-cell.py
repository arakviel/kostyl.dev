"""Один крок GRU: два вентилі, один стан."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 5)
box(ax, 2, 34, 16, 16, "hₜ₋₁\nxₜ", fc=GREY, size=13)
box(ax, 30, 62, 16, 14, "σ  r\nreset", fc=GREEN, size=12)
box(ax, 30, 8, 16, 14, "σ  z\nupdate", fc=BLUE, size=12)
box(ax, 56, 34, 18, 16, "tanh\nкандидат h̃", fc=AMBER, size=12)
box(ax, 80, 34, 18, 16, "змішування\nhₜ", fc=RED, size=12)
arrow(ax, 18.5, 47, 29.5, 64)
arrow(ax, 18.5, 37, 29.5, 20)
arrow(ax, 18.5, 42, 55.5, 42)
arrow(ax, 46.5, 66, 61, 51)
ax.text(57, 62, "r ⊙ hₜ₋₁", fontsize=11, ha="left")
arrow(ax, 46.5, 16, 85, 33)
ax.text(58, 8, "z: скільки нового взяти", fontsize=11, ha="left")
arrow(ax, 74.5, 42, 79.5, 42)
ax.plot([10, 10], [51, 90], color=INK, lw=1.6); ax.plot([10, 89], [90, 90], color=INK, lw=1.6)
arrow(ax, 89, 90, 89, 51.5)
ax.text(50, 94, "старий стан hₜ₋₁ проходить напряму, якщо z ≈ 0", ha="center", fontsize=11.5, color="#475569")
arrow(ax, 98.5, 42, 100, 42) if False else None
save(fig, __file__)
