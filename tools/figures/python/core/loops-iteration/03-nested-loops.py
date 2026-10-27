import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, box, canvas, save

fig, ax = canvas(10, 3.8)
ax.text(2, 94, "for i in range(1, 4):   # зовнішній (повільний)", fontsize=12, fontfamily="DejaVu Sans Mono")
ax.text(2, 84, "    for j in range(1, 4):   # внутрішній (швидкий)", fontsize=12, fontfamily="DejaVu Sans Mono")
for j in range(1, 4):
    box(ax, 22 + (j - 1) * 14, 62, 12, 10, f"j = {j}", BLUE, mono=True, size=11)
for i in range(1, 4):
    y = 44 - (i - 1) * 16
    box(ax, 6, y, 12, 12, f"i = {i}", AMBER, mono=True, size=11)
    for j in range(1, 4):
        box(ax, 22 + (j - 1) * 14, y, 12, 12, str(i * j), GREEN, mono=True, size=13)
ax.text(76, 40, "кожен i запускає\nвесь внутрішній цикл\nщоразу заново:\n3 × 3 = 9 ітерацій", fontsize=12, va="center")
save(fig, __file__)
