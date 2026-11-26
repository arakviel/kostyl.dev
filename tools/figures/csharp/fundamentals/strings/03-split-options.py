"""Split(',') з опціями і без (slicing.cs); пробіли показано крапками."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cells import MUTED, cells  # noqa: E402
from _style import AMBER, BLUE, GREEN, RED, box, canvas, save  # noqa: E402

TEXT = " Київ, Львів ,,Одеса "
fig, ax = canvas(15, 5.6)
W = 3.6
X0 = 20
ax.text(X0 - 2, 86, "messy", ha="right", va="center", fontsize=14, fontfamily="DejaVu Sans Mono")
commas = {i: AMBER for i, ch in enumerate(TEXT) if ch == ","}
cells(ax, X0, 81, TEXT, w=W, h=10, highlight=commas, index=False, size=14, show_space=True)
ax.text(X0 + len(TEXT) * W + 2, 86, "пробіли показано як ·", va="center", fontsize=11.5, color=MUTED)


def parts(y, items, label, fc):
    ax.text(X0 - 2, y + 5, label, ha="right", va="center", fontsize=13, fontfamily="DejaVu Sans Mono")
    x = X0
    for item in items:
        shown = item.replace(" ", "·")
        w = max(len(shown) * 2.5 + 5, 6)
        box(ax, x, y, w, 10, f"\"{shown}\"", fc=fc if item else RED, mono=True, size=13)
        x += w + 3
    return x


x = parts(52, [" Київ", " Львів ", "", "Одеса "], "Split(',')", BLUE)
ax.text(x + 1, 57, "4 частини: пробіли лишилися,\nміж ,, — порожній рядок", va="center", fontsize=12,
        linespacing=1.35)
x = parts(18, ["Київ", "Львів", "Одеса"], "з опціями", GREEN)
ax.text(x + 1, 23, "3 частини", va="center", fontsize=12)
ax.text(X0, 6, "опції: StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries", fontsize=12.5,
        fontfamily="DejaVu Sans Mono", va="center")
ax.set_ylim(0, 96)
save(fig, __file__)
