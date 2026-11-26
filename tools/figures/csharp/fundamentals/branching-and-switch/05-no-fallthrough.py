"""switch без провалювання: C++ переходить у наступний case, C# дає CS0163; явні способи вийти з секції."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, RED, box, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(15, 6.4)
CODE = "switch (day)\n{\n    case 1:\n        Print(\"понеділок\");\n    case 2:\n        Print(\"вівторок\");\n        break;\n}"

ax.text(17, 96, "C++", ha="center", fontsize=16, fontweight="bold")
box(ax, 2, 36, 30, 50, CODE, fc=GREY, mono=True, size=11.5, align="left")
ax.text(17, 25, "компілюється; для day = 1 друкує\nпонеділок і вівторок", ha="center", va="center",
        fontsize=12, linespacing=1.4)
ax.annotate("", xy=(28, 52), xytext=(28, 69), arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.2,
                                                                connectionstyle="arc3,rad=-0.5"))
ax.text(30.5, 61, "провалювання", ha="left", va="center", fontsize=11, color="#DC2626", rotation=90)

ax.text(60, 66.5, "← CS0163", ha="center", va="center", fontsize=11.5, color="#B91C1C", fontweight="bold")
ax.text(51, 96, "C#", ha="center", fontsize=16, fontweight="bold")
box(ax, 36, 36, 30, 50, CODE, fc=RED, mono=True, size=11.5, align="left")
ax.text(51, 23, "error CS0163: Control cannot fall\nthrough from one case label\n('case 1:') to another", ha="center",
        va="center", fontsize=11, fontfamily="DejaVu Sans Mono", color="#B91C1C", linespacing=1.35)

ax.text(85, 96, "C#: як завершити секцію", ha="center", fontsize=16, fontweight="bold")
WAYS = [
    ("break;", "вийти зі switch", GREEN),
    ("return …;", "вийти з методу", GREEN),
    ("goto case 2;", "явний перехід", AMBER),
    ("case 1:\ncase 2:", "кілька міток,\nодна секція", BLUE),
]
for k, (code, note, color) in enumerate(WAYS):
    y = 78 - k * 18
    h = 12 if "\n" in code else 9
    box(ax, 70, y - h / 2 + 1, 15, h, code, fc=color, mono=True, size=11.5)
    ax.text(87, y + 1, note, ha="left", va="center", fontsize=11.5, linespacing=1.3)
save(fig, __file__)
