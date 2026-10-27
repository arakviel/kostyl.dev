import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, box, canvas, save

x = 42
fig, ax = canvas(10, 3.4)
ax.text(50, 92, "Об'єкт у пам'яті Python", ha="center", fontsize=14, fontweight="bold")
box(ax, 4, 40, 26, 34, f"тип\n{type(x).__name__}", BLUE, size=15)
box(ax, 34, 40, 34, 34, f"ідентичність\nid = {id(x)}", AMBER, size=13)
box(ax, 72, 40, 24, 34, f"значення\n{x}", GREEN, size=15)
ax.text(50, 18, "Кожен об'єкт має тип, ідентичність (id) і значення. id у вас буде іншим.", ha="center", fontsize=11.5)
save(fig, __file__)
