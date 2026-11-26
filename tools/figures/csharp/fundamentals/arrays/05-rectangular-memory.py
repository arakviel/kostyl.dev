"""int[,] у пам'яті: таблиця 2 × 3 лежить одним блоком, рядок за рядком; [i, j] — позиція i · 3 + j."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

MUTED = "#475569"
ROW_FC = [BLUE, GREEN]
fig, ax = canvas(15, 4.6)

# логічна таблиця
ax.text(17, 95, "як записано в коді", ha="center", fontsize=13, color=MUTED)
CW, CH = 8, 12
gx, gy = 5, 58
for i in range(2):
    for j in range(3):
        x, y = gx + j * CW, gy + (1 - i) * CH
        ax.add_patch(Rectangle((x, y), CW, CH, fc=ROW_FC[i], ec=INK, lw=1.2))
        ax.text(x + CW / 2, y + CH / 2 + 1.5, str(i * 3 + j + 1), ha="center", va="center", fontsize=15,
                fontfamily="DejaVu Sans Mono")
        ax.text(x + CW / 2, y + 2.6, f"[{i},{j}]", ha="center", va="center", fontsize=9.5, color=MUTED,
                fontfamily="DejaVu Sans Mono")
    ax.text(gx - 1.2, gy + (1 - i) * CH + CH / 2, f"рядок {i}", ha="right", va="center", fontsize=11.5)

# пам'ять
ax.text(66, 95, "як лежить у купі: один об'єкт", ha="center", fontsize=13, color=MUTED)
mx, my, MW, MH = 40, 62, 7.4, 14
ax.add_patch(Rectangle((mx, my), 13, MH, fc=GREY, ec=INK, lw=1.2))
ax.text(mx + 6.5, my + MH / 2, "службова\nчастина", ha="center", va="center", fontsize=11, linespacing=1.2)
x = mx + 13
for k in range(6):
    i = k // 3
    ax.add_patch(Rectangle((x, my), MW, MH, fc=ROW_FC[i], ec=INK, lw=1.2))
    ax.text(x + MW / 2, my + MH / 2 + 1.5, str(k + 1), ha="center", va="center", fontsize=15,
            fontfamily="DejaVu Sans Mono")
    ax.text(x + MW / 2, my + 2.6, str(k), ha="center", va="center", fontsize=9.5, color=MUTED)
    x += MW
ax.text(mx + 13 + 1.5 * MW, my - 5, "рядок 0", ha="center", fontsize=11.5)
ax.text(mx + 13 + 4.5 * MW, my - 5, "рядок 1", ha="center", fontsize=11.5)
ax.add_patch(FancyArrowPatch((gx + 3 * CW + 1.5, gy + CH), (mx - 1, my + MH / 2), arrowstyle="-|>",
                             mutation_scale=16, lw=1.4, color=INK))

ax.text(50, 38, "елемент [i, j] лежить на позиції  i · 3 + j  (3 — кількість стовпців)", ha="center", fontsize=13.5,
        bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.5"))
ax.text(50, 26, "[1, 2] → 1 · 3 + 2 = 5: шостий елемент блока", ha="center", fontsize=13,
        fontfamily="DejaVu Sans Mono")
ax.set_ylim(18, 100)
save(fig, __file__)
