"""Виконання IL методу SumTo(3) крок за кроком: стек обчислень, локальні змінні, переходи.

IL — реальний вивід `ilspycmd -il` для sum-loop.cs (Release, .NET 10.0.15).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, box, save_steps  # noqa: E402

IL = [
    ("IL_0000", "ldc.i4.0"), ("IL_0001", "stloc.0"), ("IL_0002", "ldc.i4.1"), ("IL_0003", "stloc.1"),
    ("IL_0004", "br.s IL_000e"),
    ("IL_0006", "ldloc.0"), ("IL_0007", "ldloc.1"), ("IL_0008", "add"), ("IL_0009", "stloc.0"),
    ("IL_000a", "ldloc.1"), ("IL_000b", "ldc.i4.1"), ("IL_000c", "add"), ("IL_000d", "stloc.1"),
    ("IL_000e", "ldloc.1"), ("IL_000f", "ldarg.0"), ("IL_0010", "ble.s IL_0006"),
    ("IL_0012", "ldloc.0"), ("IL_0013", "ret"),
]
LABEL = {label: i for i, (label, _) in enumerate(IL)}
CS = ["int sum = 0;", "for (int i = 1;", "     i <= n;", "     i++)", "    sum += i;", "return sum;"]
CS_OF = {0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 4, 6: 4, 7: 4, 8: 4, 9: 3, 10: 3, 11: 3, 12: 3, 13: 2, 14: 2, 15: 2,
         16: 5, 17: 5}


def explain(op, stack_before, jumped):
    if op.startswith("ldc.i4."):
        return f"{op}: покласти на стек константу {op[-1]}."
    if op.startswith("stloc."):
        return f"{op}: зняти значення зі стеку і записати в локальну змінну [{op[-1]}]."
    if op.startswith("ldloc."):
        return f"{op}: покласти на стек значення локальної змінної [{op[-1]}]."
    if op == "ldarg.0":
        return "ldarg.0: покласти на стек аргумент n."
    if op == "add":
        return f"add: зняти {stack_before[-2]} і {stack_before[-1]}, покласти суму {stack_before[-2] + stack_before[-1]}."
    if op.startswith("br.s"):
        return "br.s: безумовний перехід до перевірки умови циклу."
    if op.startswith("ble.s"):
        a, b = stack_before[-2], stack_before[-1]
        return (f"ble.s: {a} <= {b} — так, перехід на початок тіла циклу." if jumped
                else f"ble.s: {a} <= {b} — ні, цикл завершено, виконання йде далі.")
    if op == "ret":
        return f"ret: повернути {stack_before[-1]} — результат SumTo(3)."
    return op


def simulate():
    pc, stack, loc, n = 0, [], [None, None], 3
    states = [(None, [], [None, None], "Початок методу SumTo(3): локальні змінні sum і i — слоти [0] і [1].")]
    while True:
        label, op = IL[pc]
        before = list(stack)
        jumped = False
        if op.startswith("ldc.i4."):
            stack.append(int(op[-1]))
        elif op.startswith("stloc."):
            loc[int(op[-1])] = stack.pop()
        elif op.startswith("ldloc."):
            stack.append(loc[int(op[-1])])
        elif op == "ldarg.0":
            stack.append(n)
        elif op == "add":
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif op.startswith("br.s"):
            jumped = True
        elif op.startswith("ble.s"):
            b, a = stack.pop(), stack.pop()
            jumped = a <= b
        elif op == "ret":
            stack.pop()
        states.append((pc, list(stack), list(loc), explain(op, before, jumped)))
        if op == "ret":
            states[-1] = (pc, [before[-1]], list(loc), states[-1][3])
            return states
        pc = LABEL[op.split()[-1]] if jumped else pc + 1


def draw(ax, state):
    pc, stack, loc, caption = state
    ax.text(50, 96, "IL циклу: SumTo(3) крок за кроком", ha="center", fontsize=18, fontweight="bold")

    # IL
    for i, (label, op) in enumerate(IL):
        y = 88 - i * 4.15
        if i == pc:
            ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
                (2.5, y - 1.9), 33, 3.8, fc=AMBER, ec="#D97706", lw=1.5))
        in_loop = 5 <= i <= 15
        ax.text(3.2, y, f"{label}: {op}", fontsize=11.5, va="center", fontfamily="DejaVu Sans Mono",
                color=INK if (pc is None or i == pc or True) else "#94A3B8")
    ax.plot([37, 38, 38, 37], [88 - 5 * 4.15 + 2, 88 - 5 * 4.15 + 2, 88 - 15 * 4.15 - 2, 88 - 15 * 4.15 - 2],
            color="#2563EB", lw=1.6)
    ax.text(39, 88 - 10 * 4.15, "цикл", rotation=90, va="center", fontsize=11, color="#2563EB")

    # C#
    ax.text(44, 88, "C#", fontsize=13, fontweight="bold")
    for i, line in enumerate(CS):
        y = 82 - i * 5
        hot = pc is not None and CS_OF[pc] == i
        if hot:
            ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
                (43.5, y - 2.1), 24, 4.2, fc=AMBER, ec="none"))
        ax.text(44, y, line, fontsize=11.5, va="center", fontfamily="DejaVu Sans Mono")

    # стек
    ax.text(57, 47, "Стек обчислень", ha="center", fontsize=13, fontweight="bold")
    ax.plot([48, 48, 66, 66], [42, 18, 18, 42], color=INK, lw=2)
    for i, v in enumerate(stack):
        box(ax, 49.3, 19.3 + i * 7.5, 15.4, 6, str(v), fc=BLUE, mono=True, size=15, weight="bold")
    if not stack:
        ax.text(57, 30, "порожній", ha="center", fontsize=12, color="#94A3B8", style="italic")

    # локальні змінні й аргумент
    ax.text(84, 88, "Локальні змінні", ha="center", fontsize=13, fontweight="bold")
    for i, (name, val) in enumerate([("[0] sum", loc[0]), ("[1] i", loc[1])]):
        txt = f"{name} = {'—' if val is None else val}"
        box(ax, 72, 74 - i * 11, 24, 8, txt, fc=GREEN if val is not None else GREY, mono=True, size=13)
    ax.text(84, 48, "Аргумент", ha="center", fontsize=13, fontweight="bold")
    box(ax, 72, 36, 24, 8, "n = 3", fc=GREY, mono=True, size=13)

    ax.text(66, 7, caption, ha="center", va="center", fontsize=13, linespacing=1.4,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


states = simulate()
durations = []
for k, s in enumerate(states):
    if k == 0:
        durations.append(3.0)
    elif k <= 16:          # підготовка і перша ітерація — повільно
        durations.append(2.4)
    elif k >= len(states) - 5:  # вихід з циклу і ret
        durations.append(2.6)
    else:
        durations.append(0.9)
save_steps(__file__, list(zip(states, durations)), draw, poster=13)
print(len(states), "кроків", round(sum(durations), 1), "с")
