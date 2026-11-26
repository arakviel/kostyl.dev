"""Поглиблено: дерево рішень, у яке Roslyn скомпілював switch expression Range (IL з switch-il.cs, Release)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import AMBER, BLUE, GREEN, GREY, INK, RED, box, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(15, 7.4)

# ліворуч — вихідний код
CODE = "score switch\n{\n    < 0 => \"помилка\",\n    < 60 => \"F\",\n    < 75 => \"C\",\n    < 90 => \"B\",\n    <= 100 => \"A\",\n    _ => \"помилка\",\n}"
ax.text(13, 95, "вихідний код", ha="center", fontsize=13, fontweight="bold")
box(ax, 0.5, 30, 25, 58, CODE, fc=GREY, mono=True, size=12, align="left")
ax.text(13, 22, "у тексті — 5 перевірок\nпідряд", ha="center", va="center", fontsize=12, color=MUTED, linespacing=1.35)

ax.text(64, 95, "що в IL (Release): дерево рішень", ha="center", fontsize=13, fontweight="bold")
NODES = {
    "r": (64, 80, "score >= 90", BLUE),
    "a": (84, 58, "score <= 100", BLUE),
    "b": (46, 58, "score >= 60", BLUE),
    "c": (60, 36, "score < 75", BLUE),
    "d": (34, 36, "score < 0", BLUE),
}
LEAVES = {
    "A": (92, 36, "\"A\"", GREEN), "err1": (78, 36, "\"помилка\"", RED),
    "C": (66, 14, "\"C\"", GREEN), "B": (54, 14, "\"B\"", GREEN),
    "err2": (28, 14, "\"помилка\"", RED), "F": (40, 14, "\"F\"", GREEN),
}
EDGES = [("r", "a", "так"), ("r", "b", "ні"), ("a", "A", "так"), ("a", "err1", "ні"), ("b", "c", "так"),
         ("b", "d", "ні"), ("c", "C", "так"), ("c", "B", "ні"), ("d", "err2", "так"), ("d", "F", "ні")]
ALL = {**NODES, **LEAVES}
for p, c, label in EDGES:
    x1, y1 = ALL[p][:2]
    x2, y2 = ALL[c][:2]
    ax.plot([x1, x2], [y1 - 4, y2 + 4], color=INK, lw=1.3, zorder=1)
    ax.text((x1 + x2) / 2 + (1.2 if x2 > x1 else -1.2), (y1 + y2) / 2, label, fontsize=11,
            ha="left" if x2 > x1 else "right", va="center", color="#16A34A" if label == "так" else "#DC2626")
for key, (x, y, text, color) in NODES.items():
    box(ax, x - 7.5, y - 4, 15, 8, text, fc=color, mono=True, size=12)
for key, (x, y, text, color) in LEAVES.items():
    w = 11 if len(text) > 4 else 6
    box(ax, x - w / 2, y - 4, w, 8, text, fc=color, mono=True, size=12)
ax.text(64, 3, "будь-яке значення — щонайбільше 3 порівняння; результат той самий, що й при перевірці згори вниз",
        ha="center", va="center", fontsize=12, color=MUTED)
save(fig, __file__)
