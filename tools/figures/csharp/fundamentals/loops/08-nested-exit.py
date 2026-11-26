"""Пошук a і b (1..9) з a * b == 24 і a + b == 10: які пари перевіряє лише break, а які — прапорець, goto чи return."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import BLUE, GREEN, INK, canvas, save  # noqa: E402


def checked_break_only():
    cells, found = set(), []
    for a in range(1, 10):
        for b in range(1, 10):
            cells.add((a, b))
            if a * b == 24 and a + b == 10:
                found.append((a, b))
                break
    return cells, found


def checked_full_exit():
    cells = set()
    for a in range(1, 10):
        for b in range(1, 10):
            cells.add((a, b))
            if a * b == 24 and a + b == 10:
                return cells, [(a, b)]
    return cells, []


C = 4.3   # розмір клітинки


def grid(ax, x0, title, cells, found):
    ax.text(x0 + 4.5 * C, 98, title, ha="center", va="center", fontsize=14, fontweight="bold")
    ax.text(x0 + 4.5 * C, 91, "b →", ha="center", va="center", fontsize=12.5, color="#475569")
    ax.text(x0 - 4.2, 86 - 4.5 * C * 1.05, "a\n↓", ha="center", va="center", fontsize=12.5, color="#475569")
    for a in range(1, 10):
        for b in range(1, 10):
            x = x0 + (b - 1) * C
            y = 86 - a * C * 1.05
            fc = GREEN if (a, b) in found else (BLUE if (a, b) in cells else "white")
            hit = (a, b) in found
            ax.add_patch(Rectangle((x, y), C, C * 1.05, fc=fc, ec="#16A34A" if hit else "#94A3B8",
                                   lw=2.2 if hit else 0.8, zorder=3 if hit else 1))
            if (a, b) in found:
                ax.text(x + C / 2, y + C * 0.52, f"{a}×{b}", ha="center", va="center", fontsize=9.5,
                        fontweight="bold", zorder=4)
        ax.text(x0 - 1.2, 86 - a * C * 1.05 + C * 0.52, str(a), ha="right", va="center", fontsize=11)
    for b in range(1, 10):
        ax.text(x0 + (b - 0.5) * C, 87.5, str(b), ha="center", va="center", fontsize=11)
    ax.text(x0 + 4.5 * C, 37, f"перевірок: {len(cells)}", ha="center", va="center", fontsize=14,
            fontfamily="DejaVu Sans Mono")


fig, ax = canvas(15, 6.6)
cells, found = checked_break_only()
grid(ax, 6, "лише break", cells, found)
cells, found = checked_full_exit()
grid(ax, 57, "прапорець, goto або return", cells, found)
ax.add_patch(Rectangle((20, 24), 2.6, 4, fc=BLUE, ec="#94A3B8"))
ax.text(23.6, 26, "пару перевірено", va="center", fontsize=12.5)
ax.add_patch(Rectangle((45, 24), 2.6, 4, fc=GREEN, ec="#94A3B8"))
ax.text(48.6, 26, "умову виконано", va="center", fontsize=12.5)
ax.add_patch(Rectangle((68, 24), 2.6, 4, fc="white", ec="#94A3B8"))
ax.text(71.6, 26, "не перевірялася", va="center", fontsize=12.5)
ax.set_ylim(20, 100)
save(fig, __file__)
