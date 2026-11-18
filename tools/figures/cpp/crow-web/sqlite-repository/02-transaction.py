import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
ax.text(25, 95, "Усе успішно", ha="center", fontsize=12.5, weight="bold")
ax.text(75, 95, "Помилка на другому записі", ha="center", fontsize=12.5, weight="bold")
for col, ok in ((0, True), (50, False)):
    steps = [("BEGIN", GREY), ("INSERT Анна", GREEN), ("INSERT Борис", GREEN if ok else RED), ("COMMIT" if ok else "ROLLBACK", GREEN if ok else AMBER)]
    for i, (t, c) in enumerate(steps):
        box(ax, col + 8, 74 - i * 19, 34, 13, t, fc=c, mono=True, size=10.5)
        if i < 3: arrow(ax, col + 25, 73.5 - i * 19, col + 25, 62 - i * 19)
ax.text(25, 2, "в таблиці 2 записи", ha="center", fontsize=11.5)
ax.text(75, 2, "в таблиці 0 записів: Анна теж скасована", ha="center", fontsize=11.5)
save(fig, __file__)
