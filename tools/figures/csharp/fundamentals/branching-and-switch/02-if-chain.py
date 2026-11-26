"""Ланцюжок if / else if / else для score = 74 (вивід if-else.cs): перевірки згори вниз, виконується перша істинна гілка."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import GREEN, GREY, INK, RED, arrow, box, canvas, save  # noqa: E402

MUTED = "#475569"
fig, ax = canvas(12, 7.5)
ax.text(50, 97, "score = 74", ha="center", fontsize=16, fontweight="bold", fontfamily="DejaVu Sans Mono")

ROWS = [
    ("score >= 90", "\"відмінно\"", "ні"),
    ("score >= 75", "\"добре\"", "ні"),
    ("score >= 60", "\"задовільно\"", "так"),
    ("else", "\"незадовільно\"", None),
]
TOP, STEP, H = 78, 22, 11
for k, (cond, result, verdict) in enumerate(ROWS):
    y = TOP - k * STEP
    if verdict == "ні":
        cfc, rfc, rls, ralpha = RED, "white", "--", 0.6
    elif verdict == "так":
        cfc, rfc, rls, ralpha = GREEN, GREEN, "-", 1.0
    else:
        cfc, rfc, rls, ralpha = "white", "white", "--", 0.6
    box(ax, 18, y, 26, H, cond, fc=cfc, mono=True, size=15, ls="--" if verdict is None else "-",
        alpha=1.0 if verdict else 0.6)
    box(ax, 60, y, 30, H, f"grade = {result}", fc=rfc, mono=True, size=13, ls=rls, alpha=ralpha)
    if verdict == "так":
        arrow(ax, 44.8, y + H / 2, 59.2, y + H / 2, color="#16A34A", lw=2.4)
        ax.text(52, y + H / 2 + 2, "так", ha="center", va="bottom", fontsize=13, color="#16A34A", fontweight="bold")
    if k < 2:
        arrow(ax, 31, y - 0.6, 31, y - STEP + H + 0.6, color="#DC2626", lw=2.2)
        ax.text(32.5, y - (STEP - H) / 2, "ні", ha="left", va="center", fontsize=13, color="#DC2626",
                fontweight="bold")
    if k == 2:
        ax.text(9, y - STEP + H / 2, "далі не\nперевіряється", ha="center", va="center", fontsize=11.5,
                color=MUTED)

ax.text(9, TOP + H / 2, "перевірки\nзгори вниз", ha="center", va="center", fontsize=11.5, color=MUTED)
arrow(ax, 9, TOP - 2, 9, TOP - 2 * STEP + 6, color=MUTED, lw=1.4)
ax.text(53, 3, "Виконується лише перша гілка, умова якої істинна; пунктир — гілки, які не виконуються.",
        ha="center", va="center", fontsize=12.5, color=INK)
save(fig, __file__)
