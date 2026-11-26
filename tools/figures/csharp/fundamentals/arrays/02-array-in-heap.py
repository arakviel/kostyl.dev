"""Масив у пам'яті: змінна в кадрі методу містить посилання, масив з довжиною і елементами лежить у купі."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, RED, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(15, 4.6)

# кадр методу
ax.add_patch(Rectangle((2, 30), 20, 46, fc="white", ec=INK, lw=1.4))
ax.text(12, 82, "кадр методу (стек)", ha="center", fontsize=13, color=MUTED)
ax.add_patch(Rectangle((5, 46), 14, 13, fc=GREEN, ec=INK, lw=1.2))
ax.text(12, 52.5, "посилання", ha="center", va="center", fontsize=12.5)
ax.text(12, 64, "scores", ha="center", va="center", fontsize=14, fontfamily="DejaVu Sans Mono")

# масив у купі
ax.text(66, 90, "масив у купі", ha="center", fontsize=13, color=MUTED)
CW, Y, H = 6.2, 44, 16
x = 33
cells = [("заголовок", GREY, 8.5), ("тип\nint[]", GREY, 7.5), ("Length\n5", AMBER, 7.5)]
for text, fc, w in cells:
    ax.add_patch(Rectangle((x, Y), w, H, fc=fc, ec=INK, lw=1.2))
    ax.text(x + w / 2, Y + H / 2, text, ha="center", va="center", fontsize=11.5, linespacing=1.2)
    x += w
service_end = x
for i, v in enumerate([90, 0, 0, 0, 0]):
    ax.add_patch(Rectangle((x, Y), CW, H, fc=BLUE, ec=INK, lw=1.2))
    ax.text(x + CW / 2, Y + H / 2, str(v), ha="center", va="center", fontsize=14, fontfamily="DejaVu Sans Mono")
    ax.text(x + CW / 2, Y - 5, f"[{i}]", ha="center", va="center", fontsize=12, fontfamily="DejaVu Sans Mono")
    x += CW
ax.add_patch(Rectangle((x, Y), CW, H, fc="white", ec="#DC2626", lw=1.4, ls="--"))
ax.text(x + CW / 2, Y + H / 2, "?", ha="center", va="center", fontsize=14, color="#DC2626")
ax.text(x + CW / 2, Y - 5, "[5]", ha="center", va="center", fontsize=12, fontfamily="DejaVu Sans Mono",
        color="#DC2626")
ax.text(x + CW / 2, Y - 15, "IndexOutOfRangeException", ha="center", va="center", fontsize=11.5, color="#DC2626")

# дужки над частинами
ax.plot([33, 33, service_end, service_end], [Y + H + 3, Y + H + 5, Y + H + 5, Y + H + 3], color=MUTED, lw=1.2)
ax.text((33 + service_end) / 2, Y + H + 9, "службова частина", ha="center", fontsize=11.5, color=MUTED)
ax.plot([service_end, service_end, x, x], [Y + H + 3, Y + H + 5, Y + H + 5, Y + H + 3], color=MUTED, lw=1.2)
ax.text((service_end + x) / 2, Y + H + 9, "елементи int, по 4 байти підряд", ha="center", fontsize=11.5,
        color=MUTED)

ax.add_patch(FancyArrowPatch((19, 52.5), (32.6, 52.5), arrowstyle="-|>", mutation_scale=18, lw=1.6, color=INK))
ax.text(55, 14, "new int[5]: усі елементи — 0; scores[0] = 90 змінює перший", ha="center", fontsize=12.5,
        bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.5"))
ax.set_ylim(5, 96)
save(fig, __file__)
