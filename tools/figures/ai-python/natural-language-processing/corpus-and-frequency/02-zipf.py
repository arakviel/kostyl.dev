"""Закон Ципфа: частота обернено пропорційна рангу."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _style import *
from _data import counts

f = np.array(sorted(counts.values(), reverse=True))
r = np.arange(1, len(f) + 1)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
a1.bar(r[:60], f[:60], color="#2563EB", edgecolor=INK, lw=0.4)
a1.set_title("Звичайна шкала: перші 60 слів", fontweight="bold")
a1.set_xlabel("ранг слова")
a1.set_ylabel("частота")
a2.loglog(r, f, color="#2563EB", lw=2.2, label="реальні дані")
a2.loglog(r, f[0] / r, color="#DC2626", lw=1.6, ls="--", label="f = C / ранг")
a2.set_title("Логарифмічна шкала: всі слова", fontweight="bold")
a2.set_xlabel("ранг слова")
a2.legend(frameon=False)
for ax in (a1, a2):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, __file__)
