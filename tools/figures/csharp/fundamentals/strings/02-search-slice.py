"""Пошук і вирізання в рядку "2026-11-26" (slicing.cs, search.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cells import MUTED, cells  # noqa: E402
from _style import AMBER, BLUE, GREEN, GREY, box, canvas, save  # noqa: E402

fig, ax = canvas(14, 4.8)
W = 6.5
X0, Y0 = 22, 58
ax.text(X0 - 2, Y0 + 5.5, "date", ha="right", va="center", fontsize=15, fontfamily="DejaVu Sans Mono")
cells(ax, X0, Y0, "2026-11-26", w=W, h=11, highlight={4: AMBER, 7: AMBER, 5: GREEN, 6: GREEN}, size=17)


def bracket_above(i0, i1, text, y):
    x1, x2 = X0 + i0 * W, X0 + (i1 + 1) * W
    ax.plot([x1, x1, x2, x2], [y - 2, y, y, y - 2], color=MUTED, lw=1.2)
    ax.text((x1 + x2) / 2, y + 4, text, ha="center", fontsize=12.5, fontfamily="DejaVu Sans Mono")


bracket_above(0, 3, "Substring(0, 4)", 74)
bracket_above(5, 6, "Substring(5, 2)", 74)
bracket_above(8, 9, "Substring(8)", 74)
ax.text(X0 + 4.5 * W, 92, "IndexOf('-') = 4", ha="center", fontsize=12.5, fontfamily="DejaVu Sans Mono",
        color="#B45309")
ax.text(X0 + 7.5 * W, 92, "LastIndexOf('-') = 7", ha="left", fontsize=12.5, fontfamily="DejaVu Sans Mono",
        color="#B45309")

ax.text(X0 - 2, 24, "Split('-')", ha="right", va="center", fontsize=14, fontfamily="DejaVu Sans Mono")
x = X0
for part in ["2026", "11", "26"]:
    w = len(part) * 3.6 + 6
    box(ax, x, 19, w, 10, f"\"{part}\"", fc=BLUE, mono=True, size=14)
    x += w + 3
ax.text(x + 2, 24, "новий масив string[] з 3 рядків;\nроздільник у результат не потрапляє", va="center",
        fontsize=12.5, linespacing=1.35)
ax.set_ylim(10, 100)
save(fig, __file__)
