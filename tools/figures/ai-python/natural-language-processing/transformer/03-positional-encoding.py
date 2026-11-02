"""Синусоїдальне позиційне кодування: 50 позицій × 64 виміри."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

import numpy as np
L, d = 50, 64
p = np.arange(L)[:, None]; i = np.arange(0, d, 2)
P = np.zeros((L, d)); P[:, 0::2] = np.sin(p / 10000 ** (i / d)); P[:, 1::2] = np.cos(p / 10000 ** (i / d))
fig, ax = plt.subplots(figsize=(9, 4.6))
im = ax.imshow(P, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_xlabel("вимір вектора (швидкі хвилі — зліва, повільні — справа)"); ax.set_ylabel("позиція слова")
fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
save(fig, __file__)
