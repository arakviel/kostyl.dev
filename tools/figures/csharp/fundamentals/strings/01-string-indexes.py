"""Рядок як послідовність char з індексами (basics.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cells import MUTED, cells  # noqa: E402
from _style import AMBER, GREEN, RED, canvas, save  # noqa: E402

fig, ax = canvas(14, 4.0)
W = 8
X0, Y0 = 26, 52
ax.text(X0 - 2, Y0 + 5.5, "city", ha="right", va="center", fontsize=16, fontfamily="DejaVu Sans Mono")
end = cells(ax, X0, Y0, "Чернігів", w=W, h=13, highlight={0: GREEN, 7: AMBER}, size=19)

ax.annotate("city[0] = 'Ч'", xy=(X0 + W / 2, Y0 + 13), xytext=(X0 + W / 2, 90), ha="center", fontsize=13,
            fontfamily="DejaVu Sans Mono", arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.1))
ax.annotate("city[city.Length - 1] = 'в'", xy=(end - W / 2, Y0 + 13), xytext=(end - W / 2, 90), ha="center",
            fontsize=13, fontfamily="DejaVu Sans Mono", arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.1))
ax.plot([X0, X0, end, end], [Y0 - 9, Y0 - 11, Y0 - 11, Y0 - 9], color=MUTED, lw=1.2)
ax.text((X0 + end) / 2, Y0 - 16, "city.Length = 8: індекси від 0 до 7", ha="center", fontsize=13)
ax.text(50, 12, "кожна клітинка — char (2 байти UTF-16); індексатор лише читає: city[0] = 'ч' — помилка CS0200",
        ha="center", fontsize=12.5, bbox=dict(fc=RED, ec="none", boxstyle="round,pad=0.5"))
ax.set_ylim(4, 100)
save(fig, __file__)
