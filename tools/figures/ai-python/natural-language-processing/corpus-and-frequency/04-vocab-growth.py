"""Зростання словника зі збільшенням корпусу."""
import sys
import random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
from nltk.corpus import movie_reviews

random.seed(0)
ids = movie_reviews.fileids()
random.shuffle(ids)
seen, n, pts = set(), 0, []
for i, fid in enumerate(ids, 1):
    for w in movie_reviews.words(fid):
        if w.isalpha():
            n += 1
            seen.add(w)
    if i in (10, 25, 50, 100, 250, 500, 1000, 1500, 2000):
        pts.append((n, len(seen)))
xs, ys = zip(*pts)
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.plot(xs, ys, "o-", color="#2563EB", lw=2.2, ms=7)
for x, y in pts[::2]:
    ax.annotate(f"{y:,}".replace(",", " "), (x, y), textcoords="offset points", xytext=(-6, 9), ha="right", fontsize=10)
ax.set_xlabel("слів у корпусі (токенів)")
ax.set_ylabel("різних слів (типів)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", " ")))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", " ")))
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
save(fig, __file__)
