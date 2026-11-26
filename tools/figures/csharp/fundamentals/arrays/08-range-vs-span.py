"""a[1..^1] копіює елементи в новий масив, a.AsSpan(1, 3) — вікно в той самий масив (index-range.cs, span.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

MUTED = "#475569"
CW, CH = 8, 12
fig, ax = canvas(15, 5.2)


def row(x, y, values, fc=BLUE, labels=True, color_range=None):
    for i, v in enumerate(values):
        c = fc
        if color_range and color_range[0] <= i <= color_range[1]:
            c = AMBER
        ax.add_patch(Rectangle((x + i * CW, y), CW, CH, fc=c, ec=INK, lw=1.2))
        ax.text(x + i * CW + CW / 2, y + CH / 2, str(v), ha="center", va="center", fontsize=15,
                fontfamily="DejaVu Sans Mono")
        if labels:
            ax.text(x + i * CW + CW / 2, y - 4.5, str(i), ha="center", va="center", fontsize=11, color=MUTED)


# масив a посередині
AX, AY = 30, 50
ax.text(AX - 2, AY + CH / 2, "a", ha="right", va="center", fontsize=16, fontfamily="DejaVu Sans Mono")
row(AX, AY, [10, 20, 30, 40, 50], color_range=(1, 3))

# Range: копія
ax.text(4, 22, "int[] middle = a[1..^1];", fontsize=13.5, fontfamily="DejaVu Sans Mono", va="center")
row(AX + CW, 4, [20, 30, 40], fc=GREEN, labels=False)
ax.add_patch(FancyArrowPatch((AX + 2.5 * CW, AY - 7), (AX + 2.5 * CW, 17.5), arrowstyle="-|>", mutation_scale=16,
                             lw=1.4, color=INK, ls="--"))
ax.text(AX + 4 * CW + 3, 10, "новий масив: елементи скопійовано,\nзміна middle не зачіпає a", fontsize=12.5,
        va="center", linespacing=1.35)

# Span: вікно
ax.text(4, 92, "Span<int> window = a.AsSpan(1, 3);", fontsize=13.5, fontfamily="DejaVu Sans Mono", va="center")
x1, x2 = AX + CW, AX + 4 * CW
ax.plot([x1, x1, x2, x2], [AY + CH + 12, AY + CH + 15, AY + CH + 15, AY + CH + 12], color="#D97706", lw=2.2)
ax.text(x2 + 3, AY + CH + 14, "вікно: Length 3, ті самі комірки;\nwindow[0] = 999 змінює a[1]", fontsize=12.5,
        va="center", linespacing=1.35)
ax.set_ylim(0, 100)
save(fig, __file__)
