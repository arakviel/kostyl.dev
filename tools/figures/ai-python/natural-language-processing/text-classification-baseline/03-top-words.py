"""Коефіцієнти LogisticRegression: топ-15 слів кожного класу (вивід лекції 06)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

pos = [("seen",0.476),("overall",0.465),("fun",0.439),("well",0.428),("excellent",0.421),("great",0.419),("job",0.417),("until",0.413),("yet",0.396),("back",0.383),("perfectly",0.377),("husband",0.361),("terrific",0.356),("solid",0.354),("memorable",0.348)]
neg = [("bad",-0.850),("worst",-0.650),("unfortunately",-0.551),("script",-0.528),("nothing",-0.518),("plot",-0.500),("looks",-0.475),("ridiculous",-0.452),("awful",-0.446),("reason",-0.443),("women",-0.440),("only",-0.429),("waste",-0.425),("supposed",-0.415),("minute",-0.409)]
fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
for ax, data, col, title in [(axes[0], pos, "#16A34A", "підштовхують до «позитивний»"), (axes[1], neg, "#DC2626", "підштовхують до «негативний»")]:
    w, v = zip(*data); y = range(len(w))
    ax.barh(y, v, color=col); ax.set_yticks(y); ax.set_yticklabels(w, fontsize=11.5); ax.invert_yaxis(); ax.set_title(title, fontsize=13, color=col)
    for yi, vi in zip(y, v): ax.text(vi + (0.01 if vi > 0 else -0.01), yi, f"{vi:+.2f}".replace(".", ",").replace("-", "−"), va="center", ha="left" if vi > 0 else "right", fontsize=10.5)
    ax.set_xlabel("коефіцієнт моделі")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axes[0].set_xlim(0, 0.58); axes[1].set_xlim(-1.0, 0); axes[1].yaxis.tick_right()
save(fig, __file__)
