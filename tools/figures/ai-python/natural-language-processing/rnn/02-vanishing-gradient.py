"""Норма градієнта dL/dh_t для звичайної RNN залежно від відстані до останнього кроку.
Числа з реального запуску: 30 випадкових послідовностей, T = 50, h = 64 (nn.RNNCell, початкові ваги).
Запуск: uv run --python 3.13 --with matplotlib --with torch python <цей файл>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import torch, torch.nn as nn

torch.manual_seed(0)
T, H, D = 50, 64, 64
cell = nn.RNNCell(D, H)
acc = torch.zeros(T)
for _ in range(30):
    x = torch.randn(T, 1, D); h = torch.zeros(1, H); hs = []
    for t in range(T):
        h = cell(x[t], h); h.retain_grad(); hs.append(h)
    hs[-1].sum().backward()
    acc += torch.tensor([v.grad.norm().item() for v in hs])
g = (acc / 30).numpy()
dist = list(range(T - 1, -1, -1))

fig, ax = plt.subplots(figsize=(9, 4.6))
ax.semilogy(dist, g, color="#DC2626", lw=2.4)
ax.set_xlabel("на скільки кроків назад від кінця послідовності")
ax.set_ylabel("норма градієнта (лог. шкала)")
ax.invert_xaxis() if False else None
ax.grid(True, alpha=0.3)
for d in (0, 10, 30, 49):
    ax.annotate(f"{g[T - 1 - d]:.0e}", (d, g[T - 1 - d]), textcoords="offset points", xytext=(6, 8), fontsize=12)
    ax.plot([d], [g[T - 1 - d]], "o", color="#DC2626")
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
