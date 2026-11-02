"""Loss за епоху (різниця накопичених значень gensim). Накопичені значення — з виводу лекції."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import numpy as np

cum = [4163257, 7458082, 10312332, 13003633, 15687613, 18294990, 20840348, 23379856, 25921468, 28468028,
       31022754, 33554528, 34905832, 36233112, 37555140, 38860508, 40142336, 41431184, 42709352, 43967696]
per = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, len(cum))]
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.plot(range(1, 21), [p / 1e6 for p in per], "o-", color="#2563EB", lw=2.4)
ax.axvline(12.5, color="#DC2626", ls="--", lw=1.4)
ax.text(12.8, 3.6, "накопичене значення перетнуло\n2²⁵ ≈ 33,5 млн: точність float32\nзменшилась, прирости стали меншими",
        color="#DC2626", fontsize=11, va="top")
ax.text(2.3, 4.0, "швидке навчання", color="#D97706", fontsize=12, fontweight="bold")
ax.set_xlabel("епоха"); ax.set_ylabel("loss за епоху, млн"); ax.set_xticks(range(1, 21)); ax.grid(alpha=0.3)
ax.set_ylim(0, 4.6)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
