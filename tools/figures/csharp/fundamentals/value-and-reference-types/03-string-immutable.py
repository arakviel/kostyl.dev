"""Незмінний рядок: += створює новий об'єкт, старий не змінюється (strings.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import box, canvas, save  # noqa: E402
from _memory import HEAP_FC, STACK_FC, cell, obj, ref, region  # noqa: E402

fig, ax = canvas(15, 6.4)


def panel(ox, title, code, after):
    ax.text(ox + 24, 95, title, ha="center", fontsize=14, fontweight="bold")
    box(ax, ox + 2, 68, 44, 19, code, fc="#F8FAFC", mono=True, size=12.5, align="left")
    region(ax, ox + 1, 6, 16, 56, "Стек", STACK_FC)
    region(ax, ox + 19, 6, 29, 56, "Купа", HEAP_FC)
    p1 = cell(ax, ox + 2.5, 38, 13, 7, "s1")
    p2 = cell(ax, ox + 2.5, 22, 13, 7, "s2", hot=after)
    o1 = obj(ax, ox + 21, 38, ['"Привіт"'], [15], h=7, size=12.5)
    ref(ax, p1, o1)
    if after:
        o2 = obj(ax, ox + 21, 16, ['"Привіт!"'], [16], h=7, size=12.5, hot=True, label="новий об'єкт")
        ref(ax, p2, o2)
    else:
        ref(ax, p2, (o1[0], o1[1] - 2), rad=0.25)


panel(1, "До: два посилання на один рядок", 'string s1 = "Привіт";\nstring s2 = s1;', False)
ax.plot([50, 50], [4, 92], color="#CBD5E1", lw=1.2)
panel(51, 'Після s2 += "!"', 'string s1 = "Привіт";\nstring s2 = s1;\ns2 += "!";', True)
save(fig, __file__)
