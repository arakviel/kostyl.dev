import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt
from _style import AMBER, BLUE, INK, box, canvas, save

word = "Hello"
codes = [ord(c) for c in word]  # реальні коди літер: 72 101 108 108 111
fig, ax = canvas(10, 3.6)
ax.text(50, 92, "Слово Hello в оперативній пам'яті", ha="center", fontsize=14, fontweight="bold")
x0, w, gap = 8, 15, 2.5
for i, (ch, num) in enumerate(zip(word, codes)):
    x = x0 + i * (w + gap)
    box(ax, x, 38, w, 28, f"{num}", BLUE, size=18, weight="bold")
    ax.text(x + w / 2, 24, f"адреса\n{1000 + i}", ha="center", va="center", fontsize=11)
    ax.text(x + w / 2, 78, f"«{ch}»", ha="center", va="center", fontsize=14, fontfamily="DejaVu Sans Mono")
ax.text(50, 6, "Кожна комірка — один байт зі своєю адресою. Адреси тут умовні.", ha="center", fontsize=11, color=INK)
save(fig, __file__)
