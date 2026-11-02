"""Токенізація підслів BERT (WordPiece): реальний вивід bert-base-uncased."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.8)
rows = [("unhappiness", ["un", "##ha", "##pp", "##iness"]),
        ("tokenization", ["token", "##ization"]),
        ("transformers", ["transformers"]),
        ("ChatGPT", ["chat", "##gp", "##t"]),
        ("антитіло", list("а") + ["##н", "##т", "##и", "##т", "##і", "##л", "##о"])]
for k, (word, toks) in enumerate(rows):
    y = 84 - k * 19
    ax.text(1, y + 4.5, word, fontsize=13, va="center", fontfamily="DejaVu Sans Mono", fontweight="bold")
    arrow(ax, 26, y + 4.5, 30, y + 4.5)
    colors = [GREEN if not t.startswith("##") else BLUE for t in toks]
    chips(ax, 31, y, toks, h=9, size=12, colors=colors, char_w=1.3, pad=2.2)
ax.text(31, 98, "початок слова", fontsize=11, color="#16A34A"); ax.text(52, 98, "продовження (##)", fontsize=11, color="#2563EB")
save(fig, __file__)
