"""Шаблони відношення як діапазони на числовій осі (вивід relational.cs)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from matplotlib.patches import Rectangle  # noqa: E402

from _style import AMBER, BLUE, GREEN, GREY, INK, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(15, 4.6)
LO, HI = -20, 40
X0, X1 = 4, 96


def X(v):
    return X0 + (v - LO) / (HI - LO) * (X1 - X0)


Y = 62
SEGMENTS = [
    (LO, 0, "#BFDBFE", "< 0", "мороз"),
    (0, 10, BLUE, "< 10", "холодно"),
    (10, 25, GREEN, ">= 10 and < 25", "тепло"),
    (25, HI, AMBER, ">= 25", "спека"),
]
for a, b, color, pattern, name in SEGMENTS:
    ax.add_patch(Rectangle((X(a), Y - 4), X(b) - X(a), 8, fc=color, ec="none"))
    mid = (X(a) + X(b)) / 2
    ax.text(mid, Y + 13, pattern, ha="center", va="center", fontsize=14, fontfamily="DejaVu Sans Mono",
            fontweight="bold")
    ax.text(mid, Y, name, ha="center", va="center", fontsize=13)
ax.annotate("", xy=(X1 + 2, Y - 4), xytext=(X0 - 1, Y - 4), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
ax.text(X(5), Y + 21, "після < 0 сюди потрапляє лише [0; 10)", ha="center", va="center", fontsize=11.5,
        color=MUTED)

for tick in range(LO, HI + 1, 5):
    ax.plot([X(tick), X(tick)], [Y - 5.5, Y - 4], color=INK, lw=1)
    ax.text(X(tick), Y - 8.5, str(tick), ha="center", va="center", fontsize=10.5, color=MUTED)

# межі: зафарбований кружок — значення належить правому діапазону
for v in (0, 10, 25):
    ax.plot([X(v)], [Y + 4], marker="o", ms=9, mfc=INK, mec=INK)

VALUES = [(-12, "мороз"), (0, "холодно"), (7.5, "холодно"), (18, "тепло"), (24.9, "тепло"), (25, "спека"),
          (33, "спека")]
for k, (v, _) in enumerate(VALUES):
    y = Y - 19 - (k % 2) * 9
    ax.plot([X(v), X(v)], [Y - 4, y + 2.5], color="#2563EB", lw=1, ls=":")
    ax.text(X(v), y, f"{v:g}", ha="center", va="center", fontsize=12, fontfamily="DejaVu Sans Mono",
            color="#1D4ED8", bbox=dict(fc="white", ec="#93C5FD", boxstyle="round,pad=0.25"))

ax.plot([X(-19)], [22], marker="o", ms=9, mfc=INK, mec=INK)
ax.text(X(-18), 22, "межа належить правому діапазону: 0 — «холодно», 10 — «тепло», 25 — «спека»", ha="left",
        va="center", fontsize=12, color=MUTED)
ax.text(50, 6, "NaN не задовольняє жоден шаблон відношення: для double потрібна гілка _ (інакше попередження CS8509)",
        ha="center", va="center", fontsize=12, bbox=dict(fc=GREY, ec="none", boxstyle="round,pad=0.5"))
save(fig, __file__)
