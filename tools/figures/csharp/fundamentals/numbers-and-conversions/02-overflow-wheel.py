"""Переповнення по колу: 8-бітні значення як sbyte (всередині) і byte (зовні)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import canvas, save  # noqa: E402
from _wheel import BLUE, MUTED, wheel  # noqa: E402

fig, ax = canvas(9, 9)
ax.set_aspect("equal")
wheel(ax, 50, 50, 33)
ax.text(50, 54, "+1 — крок", ha="center", fontsize=12, color=MUTED)
ax.text(50, 49, "за годинниковою", ha="center", fontsize=12, color=MUTED)
ax.text(50, 44, "стрілкою", ha="center", fontsize=12, color=MUTED)
ax.text(3, 3, "синє — sbyte", fontsize=12, color=BLUE)
ax.text(97, 3, "сіре — byte", fontsize=12, color=MUTED, ha="right")
save(fig, __file__)
