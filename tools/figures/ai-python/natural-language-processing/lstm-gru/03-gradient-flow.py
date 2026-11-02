"""Норма градієнта до кроку t при T = 50: RNN, GRU, LSTM. Реальні виміри на 30 випадкових послідовностях (h = 64).
LSTM: градієнт по cell state cₜ; варіант з bias забувального вентиля = 1."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *
import torch, torch.nn as nn

torch.manual_seed(0)
T, H, D = 50, 64, 64

def measure(kind, fb=None, wrt="h"):
    cell = {"rnn": nn.RNNCell, "lstm": nn.LSTMCell, "gru": nn.GRUCell}[kind](D, H)
    if fb is not None:
        with torch.no_grad():
            cell.bias_hh[H:2 * H] = fb; cell.bias_ih[H:2 * H] = 0
    acc = torch.zeros(T)
    for _ in range(30):
        x = torch.randn(T, 1, D); h = torch.zeros(1, H); c = torch.zeros(1, H); hs = []; cs = []
        for t in range(T):
            if kind == "lstm":
                h, c = cell(x[t], (h, c)); c.retain_grad(); cs.append(c)
            else:
                h = cell(x[t], h)
            h.retain_grad(); hs.append(h)
        hs[-1].sum().backward()
        acc += torch.tensor([v.grad.norm().item() for v in (cs if wrt == "c" else hs)])
    return (acc / 30).numpy()

series = [("RNN", measure("rnn"), "#DC2626", "-"),
          ("GRU", measure("gru"), "#D97706", "-"),
          ("LSTM (cell state)", measure("lstm", wrt="c"), "#2563EB", "-"),
          ("LSTM, bias forget = 1", measure("lstm", fb=1.0, wrt="c"), "#16A34A", "-")]
dist = list(range(T - 1, -1, -1))
fig, ax = plt.subplots(figsize=(9.5, 4.8))
for name, g, col, ls in series:
    ax.semilogy(dist, g, color=col, lw=2.4, ls=ls, label=name)
    ax.annotate(f"{g[0]:.0e}", (T - 1, g[0]), textcoords="offset points", xytext=(6, -3), fontsize=11, color=col)
ax.set_xlabel("на скільки кроків назад від кінця послідовності")
ax.set_ylabel("норма градієнта (лог. шкала)")
ax.grid(True, alpha=0.3); ax.legend(frameon=False, loc="lower left")
ax.set_xlim(-1, 56)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, __file__)
