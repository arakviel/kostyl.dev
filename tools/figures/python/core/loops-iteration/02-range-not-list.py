import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, box, canvas, save

r = range(10**12)
size = sys.getsizeof(r)
fig, ax = canvas(11, 3.6)
ax.text(24, 92, "range(10**12)", ha="center", fontsize=14, fontfamily="DejaVu Sans Mono", fontweight="bold")
box(ax, 2, 44, 14, 28, f"start\n{r.start}", BLUE, mono=True, size=12)
box(ax, 18, 44, 14, 28, f"stop\n10**12", BLUE, mono=True, size=11)
box(ax, 34, 44, 14, 28, f"step\n{r.step}", BLUE, mono=True, size=12)
ax.text(25, 28, f"об'єкт займає {size} байтів", ha="center", fontsize=12)
ax.text(75, 92, "list(range(10**12))", ha="center", fontsize=14, fontfamily="DejaVu Sans Mono", fontweight="bold")
for i in range(6):
    box(ax, 56 + i * 7.2, 52, 6, 16, "…" if i == 5 else str(i), GREY, mono=True, size=11)
ax.text(75, 36, "10**12 посилань: щонайменше 8 ТБ пам'яті", ha="center", fontsize=12)
ax.text(75, 24, "(по 8 байтів на посилання, без самих чисел)", ha="center", fontsize=11)
ax.text(50, 6, "range обчислює числа на ходу, а не зберігає їх", ha="center", fontsize=12.5, fontweight="bold")
save(fig, __file__)
