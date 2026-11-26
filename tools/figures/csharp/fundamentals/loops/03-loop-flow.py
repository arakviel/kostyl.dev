"""Порядок виконання while, do-while і for: де перевіряється умова і куди повертається цикл."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import FancyArrowPatch  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, RED, box, canvas, save  # noqa: E402

W, H = 8.0, 3.2   # пів-ширина і пів-висота блока
GREEN_LINE, RED_LINE = "#16A34A", "#DC2626"


def block(ax, cx, cy, text, fc, mono=True):
    box(ax, cx - W, cy - H, 2 * W, 2 * H, text, fc=fc, mono=mono, size=12.5)


def path(ax, points, color=INK, label=None, at=None):
    """Ламана зі стрілкою на останньому відрізку; label ставиться в точці at."""
    xs, ys = zip(*points)
    ax.plot(xs[:-1], ys[:-1], color=color, lw=1.6, solid_capstyle="round")
    ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>", mutation_scale=16, lw=1.6, color=color))
    if label:
        ax.text(*at, label, fontsize=12, color=color, ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=1))


fig, ax = canvas(15, 7.2)
EXIT_Y = 6

# while
x = 16
ax.text(x, 97, "while", fontsize=16, fontweight="bold", ha="center", fontfamily="DejaVu Sans Mono")
ax.text(x, 91.5, "умова перед тілом", fontsize=12.5, ha="center", color="#475569")
block(ax, x, 74, "умова?", AMBER, mono=False)
block(ax, x, 48, "тіло", GREY, mono=False)
block(ax, x, EXIT_Y, "після циклу", BLUE, mono=False)
path(ax, [(x, 88), (x, 74 + H + 0.6)])
path(ax, [(x, 74 - H - 0.6), (x, 48 + H + 0.6)], GREEN_LINE, "true", (x + 4, 62))
path(ax, [(x - W - 0.6, 48), (x - W - 5, 48), (x - W - 5, 74), (x - W - 0.6, 74)])
path(ax, [(x + W + 0.6, 74), (x + W + 5, 74), (x + W + 5, EXIT_Y), (x + W + 0.6, EXIT_Y)], RED_LINE, "false",
      (x + W + 5, 40))

# do-while
x = 50
ax.text(x, 97, "do-while", fontsize=16, fontweight="bold", ha="center", fontfamily="DejaVu Sans Mono")
ax.text(x, 91.5, "тіло хоча б раз, умова після", fontsize=12.5, ha="center", color="#475569")
block(ax, x, 74, "тіло", GREY, mono=False)
block(ax, x, 48, "умова?", AMBER, mono=False)
block(ax, x, EXIT_Y, "після циклу", BLUE, mono=False)
path(ax, [(x, 88), (x, 74 + H + 0.6)])
path(ax, [(x, 74 - H - 0.6), (x, 48 + H + 0.6)])
path(ax, [(x - W - 0.6, 48), (x - W - 5, 48), (x - W - 5, 74), (x - W - 0.6, 74)], GREEN_LINE, "true",
      (x - W - 5, 61))
path(ax, [(x, 48 - H - 0.6), (x, EXIT_Y + H + 0.6)], RED_LINE, "false", (x + 4.5, 28))

# for
x = 84
ax.text(x, 97, "for", fontsize=16, fontweight="bold", ha="center", fontfamily="DejaVu Sans Mono")
ax.text(x, 91.5, "while з ініціалізатором і ітератором", fontsize=12.5, ha="center", color="#475569")
block(ax, x, 76, "int i = 0", BLUE)
block(ax, x, 59.5, "i < 5 ?", AMBER)
block(ax, x, 43, "тіло", GREY, mono=False)
block(ax, x, 26.5, "i++", RED)
block(ax, x, EXIT_Y, "після циклу", BLUE, mono=False)
path(ax, [(x, 88), (x, 76 + H + 0.6)])
path(ax, [(x, 76 - H - 0.6), (x, 59.5 + H + 0.6)])
path(ax, [(x, 59.5 - H - 0.6), (x, 43 + H + 0.6)], GREEN_LINE, "true", (x + 4, 51.2))
path(ax, [(x, 43 - H - 0.6), (x, 26.5 + H + 0.6)])
path(ax, [(x - W - 0.6, 26.5), (x - W - 5, 26.5), (x - W - 5, 59.5), (x - W - 0.6, 59.5)])
path(ax, [(x + W + 0.6, 59.5), (x + W + 4.5, 59.5), (x + W + 4.5, EXIT_Y), (x + W + 0.6, EXIT_Y)], RED_LINE, "false",
      (x + W + 4.5, 34))

ax.set_ylim(0, 100)
save(fig, __file__)
