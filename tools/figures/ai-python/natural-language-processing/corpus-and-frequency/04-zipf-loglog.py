"""Закон Ципфа в подвійному логарифмі: реальні дані проти ідеальної лінії C/r."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
import numpy as np
from _data import freq, all_words, vocab_growth

top = freq.most_common(100)
f = np.array([c for _, c in top]); r = np.arange(1, 101)
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.loglog(r, f, "o-", color="#2563EB", ms=4, lw=1.8, label="реальні дані")
ax.loglog(r, f[0] / r, "--", color="#D97706", lw=2.2, label="ідеальний Ципф: C / r (нахил −1)")
ax.set_xlabel("ранг (лог. шкала)"); ax.set_ylabel("частота (лог. шкала)"); ax.grid(alpha=0.3, which="both"); ax.legend(frameon=False)
slope = np.polyfit(np.log(r), np.log(f), 1)[0]
ax.text(1.3, 1300, f"нахил реальних даних ≈ {slope:.2f}".replace(".", ",").replace("-", "−"), fontsize=12, color="#2563EB")
print("slope", slope)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
