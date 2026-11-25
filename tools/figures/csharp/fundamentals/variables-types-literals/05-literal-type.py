"""Тип цілого літерала без суфікса: перший тип, у який влізе значення (перевірено int-literals.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, INK, RED, arrow, box, canvas, save  # noqa: E402

fig, ax = canvas(15, 8.6)
MUTED = "#475569"
STEPS = [
    ("влізе в int?", "int", "2_147_483_647"),
    ("влізе в uint?", "uint", "2_147_483_648"),
    ("влізе в long?", "long", "4_294_967_296"),
    ("влізе в ulong?", "ulong", "9_223_372_036_854_775_808"),
]
box(ax, 1, 84, 24, 9, "ціле число\nбез суфікса", fc=AMBER, size=13.5, weight="bold")
TOP, STEP = 70, 15.5
for k, (question, type_name, example) in enumerate(STEPS):
    y = TOP - k * STEP
    x = 4 + k * 5
    box(ax, x, y, 21, 8, question, fc=BLUE, size=13)
    arrow(ax, x + 21.8, y + 4, 44, y + 4)
    ax.text((x + 21.8 + 44) / 2, y + 5.2, "так", ha="center", fontsize=12)
    box(ax, 45, y, 11, 8, type_name, fc=GREEN, mono=True, size=15, weight="bold")
    ax.text(59, y + 4, example, va="center", fontsize=13, fontfamily="DejaVu Sans Mono")
    src_y = 84 if k == 0 else y + STEP
    src_x = 13 if k == 0 else x - 5 + 10.5
    arrow(ax, src_x, src_y - 0.8, x + 10.5, y + 8.8)
    if k > 0:
        ax.text(src_x - 1.5, y + STEP - 5.6, "ні", fontsize=12, ha="right")

y = TOP - len(STEPS) * STEP
box(ax, 24, y, 21, 8, "помилка CS1021", fc=RED, size=13)
arrow(ax, 4 + 3 * 5 + 10.5, y + STEP - 0.8, 34.5, y + 8.8)
ax.text(4 + 3 * 5 + 9, y + STEP - 5.6, "ні", fontsize=12, ha="right")
ax.text(48, y + 4, "Integral constant is too large", va="center", fontsize=12.5, color="#DC2626",
        fontfamily="DejaVu Sans Mono")

ax.text(59, 81, "приклад", fontsize=12, color=MUTED, fontweight="bold")
ax.text(30, 88.5, "Суфікси звужують вибір: U — uint або ulong, L — long або ulong, UL — тільки ulong", fontsize=12.5, color=MUTED, va="center")
save(fig, __file__)
