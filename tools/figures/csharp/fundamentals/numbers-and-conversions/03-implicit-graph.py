"""Неявні числові перетворення C#: суцільна стрілка — без втрат, пунктир — можлива втрата точності."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, arrow, box, canvas, save  # noqa: E402

PINK = "#FCE7F3"
fig, ax = canvas(15, 7.6)
W, H = 11, 8
POS = {
    "sbyte": (4, 74, BLUE), "short": (22, 74, BLUE), "int": (40, 74, BLUE), "long": (58, 74, BLUE),
    "byte": (4, 46, GREEN), "ushort": (22, 46, GREEN), "uint": (40, 46, GREEN), "ulong": (58, 46, GREEN),
    "char": (22, 18, GREY),
    "float": (84, 88, AMBER), "double": (84, 58, AMBER), "decimal": (84, 30, PINK),
}
for name, (x, y, fc) in POS.items():
    box(ax, x, y, W, H, name, fc=fc, mono=True, size=14, weight="bold")


def link(a, b, lossy=False, side="h"):
    xa, ya, _ = POS[a]
    xb, yb, _ = POS[b]
    if side == "h":
        start, end = (xa + W + 0.8, ya + H / 2), (xb - 0.8, yb + H / 2)
    elif side == "up":
        start, end = (xa + W + 0.5, ya + H + 0.5), (xb - 0.5, yb - 0.5)
    else:  # вертикально вгору
        start, end = (xa + W / 2, ya + H + 0.8), (xb + W / 2, yb - 0.8)
    arrow(ax, *start, *end, color="#DC2626" if lossy else "#1E293B", ls="--" if lossy else "-", lw=1.8)


for a, b in [("sbyte", "short"), ("short", "int"), ("int", "long"), ("byte", "ushort"), ("ushort", "uint"),
             ("uint", "ulong")]:
    link(a, b)
for a, b in [("byte", "short"), ("ushort", "int"), ("uint", "long")]:
    link(a, b, side="up")
link("char", "ushort", side="v")
arrow(ax, 89.5, 87.2, 89.5, 66.8, lw=1.8)                    # float -> double
arrow(ax, 51.8, 82, 83.2, 91, color="#DC2626", ls="--", lw=1.8)      # int -> float
arrow(ax, 51.8, 75.2, 83.2, 62.5, lw=1.8)                   # int -> double
arrow(ax, 69.8, 76.5, 83.2, 61, color="#DC2626", ls="--", lw=1.8)     # long -> double
arrow(ax, 69.8, 49, 83.2, 59.5, color="#DC2626", ls="--", lw=1.8)     # ulong -> double
arrow(ax, 69.8, 74.6, 83.2, 36, lw=1.8)                     # long -> decimal
arrow(ax, 69.8, 47.5, 83.2, 33.5, lw=1.8)                   # ulong -> decimal

ax.text(4, 86, "зі знаком", fontsize=12, color="#475569")
ax.text(4, 62, "без знаку", fontsize=12, color="#475569")
ax.text(1, 6, "Стрілки поєднуються: sbyte → long, char → int, int → decimal теж неявні. Пунктир — можлива втрата точності\n"
        "(так само uint, long, ulong → float). Зворотний напрямок, будь-що → char і double/float ↔ decimal — лише явне приведення.",
        fontsize=11.5, color="#475569", linespacing=1.5)
save(fig, __file__)
