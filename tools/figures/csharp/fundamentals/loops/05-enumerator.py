"""Як foreach перебирає List: GetEnumerator, потім MoveNext і Current, поки MoveNext не поверне false."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, GREEN, GREY, INK, RED, box, canvas, save  # noqa: E402

ITEMS = ["Київ", "Львів", "Одеса"]
ROWS = [
    ("e = cities.GetEnumerator()", -1, "позиція перед першим елементом", None),
    ("e.MoveNext()", 0, "true:  Current = \"Київ\"", GREEN),
    ("e.MoveNext()", 1, "true:  Current = \"Львів\"", GREEN),
    ("e.MoveNext()", 2, "true:  Current = \"Одеса\"", GREEN),
    ("e.MoveNext()", 3, "false: елементів більше немає,\nцикл завершено", RED),
]
CX, CW, GAP = 35, 10, 1.6   # перша клітинка, ширина, проміжок

fig, ax = canvas(14, 5.6)
ax.text(1, 96, "Крок", fontsize=13, fontweight="bold", va="center")
ax.text(CX, 96, "cities", fontsize=13, fontweight="bold", va="center", fontfamily="DejaVu Sans Mono")
ax.text(73, 96, "Результат", fontsize=13, fontweight="bold", va="center")
for r, (call, pos, result, color) in enumerate(ROWS):
    y = 80 - r * 17
    ax.text(1, y, call, fontsize=13, va="center", fontfamily="DejaVu Sans Mono")
    for i, item in enumerate(ITEMS):
        x = CX + i * (CW + GAP)
        fc = AMBER if i == pos else GREY
        box(ax, x, y - 4.5, CW, 9, f"\"{item}\"", fc=fc, mono=True, size=12)
    # позиція енумератора: трикутник над клітинкою, перед першою або після останньої
    if pos == -1:
        px = CX - 2.6
    elif pos == len(ITEMS):
        px = CX + len(ITEMS) * (CW + GAP) + 0.6
    else:
        px = CX + pos * (CW + GAP) + CW / 2
    ax.plot([px], [y + 7.6], marker="v", markersize=11, color="#2563EB")
    ax.text(73, y, result, fontsize=13.5, va="center", linespacing=1.3,
            color=INK if color is None else ("#16A34A" if color == GREEN else "#DC2626"))
save(fig, __file__)
