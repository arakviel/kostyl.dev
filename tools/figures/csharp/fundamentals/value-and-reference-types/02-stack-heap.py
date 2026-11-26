"""Стек і купа: локальні змінні в кадрі методу, об'єкти в купі; розміри з allocations.cs (.NET 10, 64-біт)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import box, canvas, save  # noqa: E402
from _memory import HEAP_FC, MUTED, STACK_FC, cell, obj, ref, region  # noqa: E402

fig, ax = canvas(15, 7.6)
box(ax, 1.5, 60, 27, 30, 'int a = 5;\nobject boxed = a;\nint[] three = new int[3];\nstring text = "Привіт";',
    fc="#F8FAFC", mono=True, size=12, align="left")
ax.text(15, 55, "локальні змінні методу", ha="center", fontsize=11.5, color=MUTED)

region(ax, 31, 6, 21, 86, "Стек (кадр методу)", STACK_FC)
region(ax, 55, 6, 44, 86, "Керована купа", HEAP_FC)

ca = cell(ax, 33, 72, 17, 7, "a", "5")
cb = cell(ax, 33, 58, 17, 7, "boxed")
ct = cell(ax, 33, 44, 17, 7, "three")
cs = cell(ax, 33, 30, 17, 7, "text")

ob = obj(ax, 58, 66, ["заголовок", "тип: Int32", "5"], [11, 11, 6], label="boxing: копія a, 24 Б")
oa = obj(ax, 58, 44, ["заголовок", "тип: Int32[]", "довжина 3", "0", "0", "0"], [9, 10, 9, 4, 4, 4],
         label="масив int[3], 40 Б")
os_ = obj(ax, 58, 22, ["заголовок", "тип: String", "довжина 6", "Привіт"], [9, 9.5, 9, 11],
          label="рядок")
ref(ax, cb, ob)
ref(ax, ct, oa)
ref(ax, cs, os_)
ax.text(77, 11, "значення int живе там, де оголошене: змінна a — у кадрі,\n"
        "копія в boxing і елементи масиву — у купі всередині об'єктів",
        ha="center", fontsize=11, color=MUTED, linespacing=1.4)
save(fig, __file__)
