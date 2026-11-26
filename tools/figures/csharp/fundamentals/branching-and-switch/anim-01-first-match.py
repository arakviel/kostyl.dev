"""Покроково: switch expression з relational.cs для t = 18 — гілки згори вниз, перша, що підійшла, дає результат."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, GREEN, INK, RED, box, save_steps  # noqa: E402

MUTED = "#475569"
W = 12
SIZE = 19
HEAD = "string kind = t switch"
ARMS = [
    ("< 0", "\"мороз\"", "18 < 0 — ні"),
    ("< 10", "\"холодно\"", "18 < 10 — ні"),
    (">= 10 and < 25", "\"тепло\"", "18 >= 10 і 18 < 25 — так"),
    (">= 25", "\"спека\"", None),
    ("_", "\"немає даних\"", None),
]
# стан: (номер поточної гілки або None, чи знайдено результат, підпис)
STEPS = [
    (None, False, "t = 18. Гілки перевіряються згори вниз."),
    (0, False, "Шаблон < 0 не підходить: переходимо до наступної гілки."),
    (1, False, "Шаблон < 10 теж не підходить."),
    (2, False, "Шаблон >= 10 and < 25 підходить: результат гілки — \"тепло\"."),
    (2, True, "Решта гілок не перевіряється: kind = \"тепло\".\nПорядок гілок важливий — виграє перша, що підійшла."),
]


def draw(ax, state):
    current, done, caption = state
    pos = ax.get_position()
    char = 0.602 * SIZE / 72 / (pos.width * W) * 100
    x0, y0, line = 16, 86, 9.2
    ax.text(50, 96.5, "switch expression: перша гілка, що підійшла", ha="center", fontsize=17, fontweight="bold")
    ax.text(x0, y0, HEAD, fontsize=SIZE, fontfamily="DejaVu Sans Mono", va="center")
    ax.text(x0, y0 - line, "{", fontsize=SIZE, fontfamily="DejaVu Sans Mono", va="center")
    for i, (pattern, result, check) in enumerate(ARMS):
        y = y0 - (i + 2) * line
        text = f"    {pattern} => {result},"
        if current is not None:
            if i < current or (i == current and not done and i != 2):
                fc = RED
            elif i == current:
                fc = GREEN
            else:
                fc = None
            if i == 2 and current == 2:
                fc = GREEN
            if fc:
                ax.add_patch(Rectangle((x0 + 4 * char - 0.5, y - line / 2 + 0.7), (len(text) - 4) * char + 1,
                                       line - 1.4, fc=fc, ec="none", zorder=1))
            if i <= current and check:
                ax.text(x0 + 33 * char, y, check, fontsize=14, va="center",
                        color="#16A34A" if "так" in check else "#DC2626")
        alpha = 0.35 if done and i > current else 1.0
        ax.text(x0, y, text, fontsize=SIZE, fontfamily="DejaVu Sans Mono", va="center", alpha=alpha, zorder=2)
        if done and i > current:
            ax.text(x0 + 33 * char, y, "не перевіряється", fontsize=14, va="center", color=MUTED)
    ax.text(x0, y0 - 7 * line, "};", fontsize=SIZE, fontfamily="DejaVu Sans Mono", va="center")
    box(ax, 72, 70, 22, 12, "kind = \"тепло\"" if done else "kind = ?", fc=GREEN if done else "white", mono=True,
        size=16)
    ax.text(50, 9, caption, ha="center", va="center", fontsize=15, linespacing=1.5,
            bbox=dict(fc=AMBER, ec="none", boxstyle="round,pad=0.6"))


save_steps(__file__, [(s, 3.2) for s in STEPS[:-1]] + [(STEPS[-1], 5.0)], draw, poster=-1)
