"""Лінійка вбудованих типів: розмір у байтах і діапазон (значення з ranges.cs і real-types.cs, .NET 10, 64-біт)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

PINK = "#FCE7F3"
# (ключове слово, тип .NET, байти, діапазон, колір)
ROWS = [
    ("bool", "Boolean", 1, "true / false", GREY),
    ("sbyte", "SByte", 1, "−128 … 127", BLUE),
    ("byte", "Byte", 1, "0 … 255", GREEN),
    ("short", "Int16", 2, "−32 768 … 32 767", BLUE),
    ("ushort", "UInt16", 2, "0 … 65 535", GREEN),
    ("char", "Char", 2, "U+0000 … U+FFFF (код UTF-16)", GREY),
    ("int", "Int32", 4, "−2 147 483 648 … 2 147 483 647", BLUE),
    ("uint", "UInt32", 4, "0 … 4 294 967 295", GREEN),
    ("float", "Single", 4, "±3.4·10³⁸, 6–9 значущих цифр", AMBER),
    ("long", "Int64", 8, "≈ ±9.2·10¹⁸", BLUE),
    ("ulong", "UInt64", 8, "0 … ≈ 1.8·10¹⁹", GREEN),
    ("nint", "IntPtr", 8, "як long (на 32-біт ОС — як int)", BLUE),
    ("double", "Double", 8, "±1.8·10³⁰⁸, 15–17 значущих цифр", AMBER),
    ("decimal", "Decimal", 16, "±7.9·10²⁸, 28–29 значущих цифр", PINK),
    ("Int128", "Int128", 16, "≈ ±1.7·10³⁸ (не ключове слово)", BLUE),
]

fig, ax = canvas(15, 10)
TOP, STEP = 90, 5.6
CELL = 2.55
X0 = 25
MUTED = "#475569"

ax.text(1, TOP + 6, "C#", fontsize=12, color=MUTED, fontweight="bold")
ax.text(9.5, TOP + 6, "System.*", fontsize=12, color=MUTED, fontweight="bold")
ax.text(X0 - 1, TOP + 6, "байти:", ha="right", fontsize=11, color=MUTED)
for b in (1, 2, 4, 8, 16):
    ax.text(X0 + (b - 0.5) * CELL, TOP + 6, str(b), ha="center", fontsize=11.5, color=MUTED, fontweight="bold")
ax.text(X0 + 16 * CELL + 2, TOP + 6, "діапазон", fontsize=12, color=MUTED, fontweight="bold")

for k, (kw, net, size, rng, color) in enumerate(ROWS):
    y = TOP - k * STEP
    ax.text(1, y, kw, va="center", fontsize=13, fontfamily="DejaVu Sans Mono", fontweight="bold")
    ax.text(9.5, y, net, va="center", fontsize=11.5, fontfamily="DejaVu Sans Mono", color=MUTED)
    for c in range(16):
        filled = c < size
        ax.add_patch(FancyBboxPatch((X0 + c * CELL + 0.15, y - 2.0), CELL - 0.3, 4.0,
                                    boxstyle="round,pad=0,rounding_size=0.4",
                                    fc=color if filled else "white", ec=INK if filled else "#E2E8F0",
                                    lw=0.9 if filled else 0.6))
    ax.text(X0 + 16 * CELL + 2, y, rng, va="center", fontsize=12.5)

ax.text(1, TOP - len(ROWS) * STEP - 1, "Блакитні — цілі зі знаком, зелені — без знаку, жовті — двійкові дробові (IEEE 754), "
        "рожевий — десятковий дріб. Одна клітинка — один байт.", fontsize=11.5, color=MUTED)
save(fig, __file__)
