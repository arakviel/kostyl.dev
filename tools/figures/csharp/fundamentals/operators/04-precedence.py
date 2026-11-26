"""Пріоритет операторів C# (від вищого до нижчого) і асоціативність; .., switch і with — у пізніших лекціях."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

PINK = "#FCE7F3"
LEVELS = [
    ("первинні", "x.y  f(x)  a[i]  x?.y  x++  x--  new  typeof  nameof  …", GREY, "→"),
    ("унарні", "+x   -x   !x   ~x   ++x   --x   (T)x", GREY, "→"),
    ("мультиплікативні", "*   /   %", GREEN, "→"),
    ("адитивні", "+   -", GREEN, "→"),
    ("зсуви", "<<   >>   >>>", GREEN, "→"),
    ("відношення, тип", "<   >   <=   >=   is   as", BLUE, "→"),
    ("рівність", "==   !=", BLUE, "→"),
    ("бітове І", "&", AMBER, "→"),
    ("бітове виключне АБО", "^", AMBER, "→"),
    ("бітове АБО", "|", AMBER, "→"),
    ("логічне І", "&&", AMBER, "→"),
    ("логічне АБО", "||", AMBER, "→"),
    ("null-coalescing", "??", PINK, "←"),
    ("умовний", "?:", PINK, "←"),
    ("присвоєння", "=  +=  -=  *=  /=  %=  &=  |=  ^=  <<=  >>=  >>>=  ??=", PINK, "←"),
]
MUTED = "#475569"
fig, ax = canvas(15, 10)
TOP, STEP = 92, 5.9
ax.text(2, TOP + 5, "вищий пріоритет", fontsize=12, color=MUTED, fontweight="bold")
ax.text(97, TOP + 5, "асоціативність", fontsize=12, color=MUTED, fontweight="bold", ha="right")
for k, (name, ops, color, assoc) in enumerate(LEVELS):
    y = TOP - k * STEP
    ax.add_patch(FancyBboxPatch((1, y - 2.5), 98, 5, boxstyle="round,pad=0,rounding_size=0.8", fc=color, ec="none",
                                alpha=0.85))
    ax.text(3, y, f"{k + 1:>2}", va="center", fontsize=11.5, color=MUTED, fontfamily="DejaVu Sans Mono")
    ax.text(7, y, name, va="center", fontsize=12.5)
    ax.text(29, y, ops, va="center", fontsize=12.5, fontfamily="DejaVu Sans Mono", fontweight="bold")
    ax.text(96.5, y, assoc, va="center", ha="center", fontsize=15, color="#DC2626" if assoc == "←" else INK)
ax.text(2, TOP - len(LEVELS) * STEP + 1, "нижчий пріоритет", fontsize=12, color=MUTED, fontweight="bold")
ax.text(98, TOP - len(LEVELS) * STEP + 1, "→ зліва направо, ← справа наліво", fontsize=11.5, color=MUTED, ha="right")
save(fig, __file__)
