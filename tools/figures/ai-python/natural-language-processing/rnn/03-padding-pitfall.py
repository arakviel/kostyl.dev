"""Пастка padding: стан береться після нулів. Точність з реального запуску (10 000 train / 5 000 test IMDB, 6 епох)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, axes = plt.subplots(1, 2, figsize=(12, 3.9), gridspec_kw=dict(width_ratios=[1.7, 1]))
ax = axes[0]; ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
toks = ["not", "good", "‹pad›", "‹pad›", "‹pad›"]
for i, t in enumerate(toks):
    pad = t == "‹pad›"
    box(ax, 3 + i * 19, 52, 14, 15, "RNN", fc=GREY if pad else BLUE, size=12)
    box(ax, 3 + i * 19, 18, 14, 13, t, fc=GREY if pad else GREEN, size=11)
    arrow(ax, 10 + i * 19, 32, 10 + i * 19, 51)
    if i < 4: arrow(ax, 17.6 + i * 19, 59.5, 21.4 + i * 19, 59.5)
ax.text(29.5, 82, "тут закінчується відгук", ha="center", fontsize=11, color="#16A34A")
arrow(ax, 29.5, 79, 29.5, 70)
ax.text(86, 82, "h_n береться тут", ha="center", fontsize=11, color="#DC2626")
arrow(ax, 86, 79, 86, 70)
ax.text(50, 3, "після нулів стан «забуває» слова", ha="center", fontsize=12)

ax = axes[1]
names = ["без\npacking", "з\npacking"]
vals = [50.0, 68.0]
bars = ax.bar(names, vals, color=["#DC2626", "#16A34A"], width=0.55)
for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v}%", ha="center", fontsize=13)
ax.axhline(50, color="#94A3B8", ls="--", lw=1); ax.text(1.33, 50.6, "випадково", fontsize=11, color="#64748B", ha="left"); ax.set_xlim(-0.5, 2.0)
ax.set_ylim(40, 75); ax.set_ylabel("accuracy на тесті, %")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
