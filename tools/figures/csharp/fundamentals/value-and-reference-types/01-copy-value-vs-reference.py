"""Присвоєння: значущий тип копіює значення, посилальний — посилання (copy.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import box, canvas, save  # noqa: E402
from _memory import HEAP_FC, MUTED, STACK_FC, cell, obj, ref, region  # noqa: E402

fig, ax = canvas(15, 7.4)

# ліва половина: int
ax.text(23, 96, "Значущий тип: копіюється значення", ha="center", fontsize=14, fontweight="bold")
box(ax, 2, 62, 40, 22, "int a = 5;\nint b = a;\nb = 10;", fc="#F8FAFC", mono=True, size=13, align="left")
region(ax, 8, 8, 28, 46, "Стек (кадр методу)", STACK_FC)
cell(ax, 11, 32, 22, 7, "a", "5")
cell(ax, 11, 20, 22, 7, "b", "10", hot=True)
ax.text(22, 12, "дві незалежні комірки", ha="center", fontsize=11.5, color=MUTED)

ax.plot([49, 49], [4, 92], color="#CBD5E1", lw=1.2)

# права половина: int[]
ax.text(76, 96, "Посилальний тип: копіюється посилання", ha="center", fontsize=14, fontweight="bold")
box(ax, 53, 62, 44, 22, "int[] x = [1, 2, 3];\nint[] y = x;\ny[0] = 99;", fc="#F8FAFC", mono=True, size=13, align="left")
region(ax, 52, 8, 18, 46, "Стек", STACK_FC)
region(ax, 72, 8, 27, 46, "Керована купа", HEAP_FC)
px = cell(ax, 54, 32, 14, 7, "x")
py = cell(ax, 54, 20, 14, 7, "y")
target = obj(ax, 74, 26, ["99", "2", "3"], [7, 7, 7], h=7, size=13, label="масив int[3]")
ref(ax, px, (target[0], target[1] + 1.5))
ref(ax, py, (target[0], target[1] - 1.5))
ax.text(85.5, 12, "один масив, два посилання:\nзміну видно через x і через y", ha="center", fontsize=11.5, color=MUTED)
save(fig, __file__)
