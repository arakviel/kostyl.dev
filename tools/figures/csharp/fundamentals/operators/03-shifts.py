"""Зсуви вправо для -16: >> заповнює знаковим бітом, >>> — нулями (вивід shifts.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, INK, canvas, save  # noqa: E402

def bits32(v):
    return format(v & 0xFFFF_FFFF, "032b")

ROWS = [("-16", -16, None, None), ("-16 >> 2", -16 >> 2, 2, "1"), ("-16 >>> 2", (-16 & 0xFFFF_FFFF) >> 2, 2, "0")]
VALUES = {"-16": "-16", "-16 >> 2": "-4", "-16 >>> 2": "1073741820"}
MUTED = "#475569"
RED = "#FEE2E2"
fig, ax = canvas(16, 4.6)
X0, CELL, TOP, STEP = 15, 2.35, 78, 26

for k, (name, value, filled, fill_bit) in enumerate(ROWS):
    y = TOP - k * STEP
    ax.text(X0 - 1.5, y, name, ha="right", va="center", fontsize=13.5, fontfamily="DejaVu Sans Mono")
    s = bits32(value)
    for i, ch in enumerate(s):
        new = filled is not None and i < filled
        lost = False
        fc = (AMBER if new else (BLUE if ch == "1" else "white"))
        ax.add_patch(FancyBboxPatch((X0 + i * CELL + 0.1, y - 5), CELL - 0.2, 10, boxstyle="round,pad=0,rounding_size=0.3",
                                    fc=fc, ec=INK, lw=0.8 if not new else 1.6))
        ax.text(X0 + i * CELL + CELL / 2, y, ch, ha="center", va="center", fontsize=11, fontfamily="DejaVu Sans Mono")
    ax.text(X0 + 32 * CELL + 1.5, y, f"= {VALUES[name]}", va="center", fontsize=13, fontfamily="DejaVu Sans Mono")
    if filled:
        note = "нові біти = знаковий біт (1)" if fill_bit == "1" else "нові біти = 0"
        ax.text(X0, y - 8.5, note, fontsize=11, color="#B45309")

ax.text(X0 + 16 * CELL, 3, "Два молодші біти виходять за межі й зникають; зліва з'являються два нові (жовті).",
        ha="center", fontsize=11.5, color=MUTED)
save(fig, __file__)
