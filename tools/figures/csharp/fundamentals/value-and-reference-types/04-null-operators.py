"""Анатомія виразу name?.Length ?? 0: де обривається ланцюжок і які типи мають частини (null-ops.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, RED, box, canvas, save  # noqa: E402

WIDTH = 15
fig, ax = canvas(WIDTH, 6.6)
AX_W = ax.get_position().width * WIDTH
CHAR = 0.602 * 20 / 72 / AX_W * 100
MUTED = "#475569"

tokens = [("name", BLUE, "string?:\nможе бути null"), ("?.", RED, "name — null:\nLength не читається,\nрезультат — null"),
          ("Length", GREEN, "int"), ("??", AMBER, "зліва null:\nбереться праве"), ("0", GREY, "запасне\nзначення")]
x = 6
centers = []
Y = 58
for text, color, label in tokens:
    w = max(len(text) * CHAR + 5, 11)
    box(ax, x, Y, w, 11, text, fc=color, mono=True, size=20)
    cx = x + w / 2
    centers.append((x, x + w))
    ax.plot([cx, cx], [Y - 1.5, Y - 6], color=MUTED, lw=1.1)
    ax.text(cx, Y - 7, label, ha="center", va="top", fontsize=12, color=MUTED, linespacing=1.3)
    x += w + 8

# дужки типів над виразом
left, right = centers[0][0], centers[2][1]
ax.plot([left, left, right, right], [74, 77, 77, 74], color="#2563EB", lw=1.6)
ax.text((left + right) / 2, 79, "name?.Length — тип int? (число або null)", ha="center", fontsize=13, color="#2563EB")
left2, right2 = centers[0][0], centers[4][1]
ax.plot([left2, left2, right2, right2], [86, 89, 89, 86], color="#16A34A", lw=1.6)
ax.text((left2 + right2) / 2, 91, "увесь вираз — тип int: null замінено на 0", ha="center", fontsize=13, color="#16A34A")

ax.text(6, 22, 'name = "Київ"  →  4          name = null  →  0', fontsize=13.5, fontfamily="DejaVu Sans Mono")
save(fig, __file__)
