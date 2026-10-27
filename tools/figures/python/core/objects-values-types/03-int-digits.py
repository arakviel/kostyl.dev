import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, box, canvas, save

n = 2**100
digits = []
m = n
while m:
    digits.append(m & (2**30 - 1))
    m >>= 30
fig, ax = canvas(10, 3.6)
ax.text(50, 92, "2**100 у пам'яті: «цифри» за основою 2**30", ha="center", fontsize=14, fontweight="bold")
w, gap = 20, 3
for i, d in enumerate(digits):
    x = 4 + i * (w + gap)
    box(ax, x, 40, w, 30, f"{d}", GREEN if d else GREY, mono=True, size=14)
    ax.text(x + w / 2, 30, f"цифра {i}", ha="center", fontsize=11)
ax.text(50, 10, f"{n}  =  " + " + ".join(f"{d}·(2^30)^{i}" for i, d in enumerate(digits) if d), ha="center", fontsize=10.5, fontfamily="DejaVu Sans Mono")
save(fig, __file__)
