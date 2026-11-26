"""Покроково: Array.BinarySearch ділить діапазон навпіл; на невідсортованому масиві він не знаходить 42 (binary-search.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, RED, save_steps  # noqa: E402

MUTED = "#475569"
SORTED = [3, 8, 15, 21, 34, 42, 57, 66]
UNSORTED = [42, 3, 66, 15, 8, 57, 21, 34]
# стан: (масив, заголовок, lo, hi, mid, знайдено, підпис)
STEPS = [
    (SORTED, "відсортований масив, шукаємо 42", 0, 7, None, None,
     "Межі пошуку — увесь масив: lo = 0, hi = 7."),
    (SORTED, "відсортований масив, шукаємо 42", 0, 7, 3, None,
     "Середина: індекс 3, значення 21 < 42. Шукане може бути лише правіше: lo = 4."),
    (SORTED, "відсортований масив, шукаємо 42", 4, 7, 5, True,
     "Середина: індекс 5, значення 42. Знайдено за 2 порівняння: результат 5."),
    (UNSORTED, "невідсортований масив, шукаємо 42", 0, 7, None, None,
     "Ті самі числа без сортування. 42 лежить на індексі 0."),
    (UNSORTED, "невідсортований масив, шукаємо 42", 0, 7, 3, None,
     "Індекс 3: 15 < 42 — ліва половина відкидається разом з 42: lo = 4."),
    (UNSORTED, "невідсортований масив, шукаємо 42", 4, 7, 5, None,
     "Індекс 5: 57 > 42 — відкидається права частина: hi = 4."),
    (UNSORTED, "невідсортований масив, шукаємо 42", 4, 4, 4, False,
     "Індекс 4: 8 < 42, lo = 5 > hi. «Не знайдено»: результат −6,\nхоча 42 є в масиві. Помилки чи винятку немає."),
]
CW, CH, X0, Y0 = 10, 16, 10, 52


def draw(ax, state):
    values, title, lo, hi, mid, found, caption = state
    ax.text(50, 94, "Array.BinarySearch: " + title, ha="center", fontsize=17, fontweight="bold")
    for i, v in enumerate(values):
        x = X0 + i * CW
        inside = lo <= i <= hi
        fc = BLUE if inside else GREY
        if mid == i:
            fc = GREEN if found else AMBER
            if found is False:
                fc = AMBER
        alpha = 1.0 if inside or mid == i else 0.45
        ax.add_patch(Rectangle((x, Y0), CW, CH, fc=fc, ec=INK, lw=1.3, alpha=alpha))
        color = "#DC2626" if (v == 42 and values is UNSORTED and mid is not None) else INK
        ax.text(x + CW / 2, Y0 + CH / 2, str(v), ha="center", va="center", fontsize=20,
                fontfamily="DejaVu Sans Mono", color=color, alpha=1.0 if inside or color != INK else 0.5)
        ax.text(x + CW / 2, Y0 - 5, str(i), ha="center", va="center", fontsize=13, color=MUTED)
    for name, idx, dy in [("lo", lo, 26), ("hi", hi, 26)]:
        if idx <= 7:
            off = -2 if name == "lo" and lo == hi else (2 if name == "hi" and lo == hi else 0)
            ax.text(X0 + idx * CW + CW / 2 + off * 1.5, Y0 + CH + 6, name, ha="center", va="center", fontsize=14,
                    fontfamily="DejaVu Sans Mono", color="#2563EB")
    if mid is not None:
        ax.text(X0 + mid * CW + CW / 2, Y0 - 13, "mid", ha="center", va="center", fontsize=14,
                fontfamily="DejaVu Sans Mono", color="#D97706")
    ax.text(50, 12, caption, ha="center", va="center", fontsize=15, linespacing=1.5,
            bbox=dict(fc=RED if found is False else AMBER, ec="none", boxstyle="round,pad=0.6"))


steps = [(s, 3.4) for s in STEPS]
steps[2] = (STEPS[2], 4.2)
steps[-1] = (STEPS[-1], 5.5)
save_steps(__file__, steps, draw, poster=-1)
