"""Покрокове присвоєння: стек і купа для int, int[] і string (поведінка перевірена copy.cs і strings.cs, .NET 10)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, INK, box, save_steps  # noqa: E402
from _memory import HEAP_FC, STACK_FC, cell, obj, ref, region  # noqa: E402

CODE = [
    "int a = 5;",
    "int b = a;",
    "b = 10;",
    "int[] x = [1, 2, 3];",
    "int[] y = x;",
    "y[0] = 99;",
    "y = [7, 8, 9];",
    'string s = "Hi";',
    "string t = s;",
    't += "!";',
]
# об'єкти в купі: ключ -> (y, вміст, ширини)
HEAP_Y = {"arr1": 62, "arr2": 49, "str1": 38, "str2": 26}

# (рядок, змінні {ім'я: значення або ключ об'єкта}, об'єкти {ключ: вміст}, змінене, підпис)
STEPS = [
    (1, {"a": "5"}, {}, "a", "a = 5: значення лежить прямо в комірці змінної."),
    (2, {"a": "5", "b": "5"}, {}, "b", "b = a: у b копіюється значення 5. Тепер це дві незалежні комірки."),
    (3, {"a": "5", "b": "10"}, {}, "b", "b = 10 змінює лише b. Змінна a лишилася 5."),
    (4, {"a": "5", "b": "10", "x": "arr1"}, {"arr1": ["1", "2", "3"]}, "x",
     "Масив створюється в купі. У x лежить лише посилання на нього."),
    (5, {"a": "5", "b": "10", "x": "arr1", "y": "arr1"}, {"arr1": ["1", "2", "3"]}, "y",
     "y = x копіює посилання, а не масив: обидві змінні ведуть до одного об'єкта."),
    (6, {"a": "5", "b": "10", "x": "arr1", "y": "arr1"}, {"arr1": ["99", "2", "3"]}, "arr1",
     "y[0] = 99 змінює сам масив. x[0] теж дорівнює 99: це той самий масив."),
    (7, {"a": "5", "b": "10", "x": "arr1", "y": "arr2"}, {"arr1": ["99", "2", "3"], "arr2": ["7", "8", "9"]}, "y",
     "y = [7, 8, 9] записує в y посилання на новий масив. x веде до старого."),
    (8, {"a": "5", "b": "10", "x": "arr1", "y": "arr2", "s": "str1"},
     {"arr1": ["99", "2", "3"], "arr2": ["7", "8", "9"], "str1": ['"Hi"']}, "s",
     "Рядок теж об'єкт у купі, у s — посилання."),
    (9, {"a": "5", "b": "10", "x": "arr1", "y": "arr2", "s": "str1", "t": "str1"},
     {"arr1": ["99", "2", "3"], "arr2": ["7", "8", "9"], "str1": ['"Hi"']}, "t",
     "t = s: два посилання на один рядок."),
    (10, {"a": "5", "b": "10", "x": "arr1", "y": "arr2", "s": "str1", "t": "str2"},
     {"arr1": ["99", "2", "3"], "arr2": ["7", "8", "9"], "str1": ['"Hi"'], "str2": ['"Hi!"']}, "t",
     "Рядок незмінний: += створює новий об'єкт \"Hi!\" і записує посилання в t.\ns, як і раніше, веде до \"Hi\"."),
]


def draw(ax, step):
    line, variables, objects, changed, caption = step
    ax.text(50, 95, "Присвоєння: копія значення чи копія посилання", ha="center", fontsize=18, fontweight="bold")

    box(ax, 1.5, 22, 33, 66, "", fc="#F8FAFC", ec="#CBD5E1")
    for n, text in enumerate(CODE, start=1):
        y = 83 - (n - 1) * 6.2
        if n == line:
            ax.add_patch(Rectangle((5.5, y - 2.7), 28.5, 5.4, fc="#FDE68A", ec="none"))
            ax.plot([3.9], [y], marker=">", color="#D97706", markersize=11)
        ax.text(6.3, y, f"{n:>2}  {text}", fontsize=12, va="center", fontfamily="DejaVu Sans Mono", color=INK)

    region(ax, 37, 22, 20, 66, "Стек (кадр)", STACK_FC)
    region(ax, 60, 22, 38.5, 66, "Керована купа", HEAP_FC)

    starts = {}
    for k, (name, value) in enumerate(variables.items()):
        y = 74 - k * 8
        if value in HEAP_Y:
            starts[name] = (cell(ax, 39, y, 16, 6, name, hot=name == changed), value)
        else:
            cell(ax, 39, y, 16, 6, name, value, hot=name == changed)

    ends = {}
    for key, parts in objects.items():
        widths = [6.5] * len(parts) if len(parts) > 1 else [11]
        label = "масив" if key.startswith("arr") else "рядок"
        ends[key] = obj(ax, 63, HEAP_Y[key], parts, widths, h=6, size=12.5, hot=key == changed, label=label)

    for name, (start, key) in starts.items():
        ex, ey = ends[key]
        offset = {"x": 1.4, "y": -1.4, "s": 1.4, "t": -1.4}.get(name, 0)
        ref(ax, start, (ex, ey + offset))

    ax.text(50, 9, caption, ha="center", va="center", fontsize=14, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.2) for s in STEPS[:-1]] + [(STEPS[-1], 5.0)], draw, poster=5)
