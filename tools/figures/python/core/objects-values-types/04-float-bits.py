import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, box, canvas, save

bits = "".join(f"{c:08b}" for c in struct.pack(">d", 0.1))
sign, exp, mant = bits[0], bits[1:12], bits[12:]
fig, ax = canvas(11, 3.6)
ax.text(50, 92, "0.1 у форматі IEEE 754 (64 біти)", ha="center", fontsize=14, fontweight="bold")
box(ax, 2, 45, 6, 28, sign, AMBER, mono=True, size=13)
box(ax, 10, 45, 24, 28, exp, BLUE, mono=True, size=11)
box(ax, 36, 45, 62, 28, mant, GREEN, mono=True, size=10)
ax.text(5, 32, "знак\n1 біт", ha="center", fontsize=11)
ax.text(22, 32, "експонента\n11 біт", ha="center", fontsize=11)
ax.text(67, 32, "мантиса\n52 біти", ha="center", fontsize=11)
ax.text(50, 8, "Точне значення, яке зберігається: " + f"{0.1:.30f}"[:24] + "…", ha="center", fontsize=12, fontfamily="DejaVu Sans Mono")
save(fig, __file__)
