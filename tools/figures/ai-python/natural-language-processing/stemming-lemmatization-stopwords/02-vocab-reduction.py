"""Скільки різних слів у 2000 відгуках після кожного кроку (NLTK movie_reviews)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

labels = ["без змін", "лемматизація\n(іменники)", "лемматизація\n(іменники + дієслова)", "стеммінг\n(Портер)"]
vals = [39341, 34942, 29570, 25832]
cols = ["#94A3B8", "#93C5FD", "#60A5FA", "#2563EB"]
fig, ax = plt.subplots(figsize=(10, 4.8))
b = ax.bar(labels, vals, color=cols, edgecolor=INK, lw=1.2)
for r, v in zip(b, vals):
    ax.text(r.get_x() + r.get_width() / 2, v + 600, f"{v:,}".replace(",", " "), ha="center", fontweight="bold")
    ax.text(r.get_x() + r.get_width() / 2, v / 2, f"−{round(100 * (1 - v / vals[0]))}%" if v != vals[0] else "100%", ha="center", color="white", fontsize=14, fontweight="bold")
ax.set_ylabel("унікальних слів (типів)")
ax.set_ylim(0, 45000)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", " ")))
save(fig, __file__)
