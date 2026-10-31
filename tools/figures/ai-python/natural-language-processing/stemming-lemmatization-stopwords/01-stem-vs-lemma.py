"""Стеммер обрізає, лематизатор шукає в словнику (дані з реального запуску NLTK)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

rows = [("running", "run", "run"), ("connected", "connect", "connect"), ("studies", "studi", "study"),
        ("university", "univers", "university"), ("mice", "mice", "mouse"), ("was", "wa", "be"),
        ("better", "better", "good")]
fig, ax = canvas(11, 5.2)
heads = [("слово", 4), ("стеммер Портера", 36), ("лемматизатор WordNet", 68)]
for t, x in heads:
    ax.text(x + 14, 96, t, ha="center", fontsize=13, fontweight="bold", color=ACCENT)
for i, (w, st, lm) in enumerate(rows):
    y = 80 - i * 12.2
    box(ax, 4, y, 28, 9, w, fc=GREY, mono=True)
    ok_stem = st in (lm, w) and st == lm
    box(ax, 36, y, 28, 9, st, fc=GREEN if st == lm else (RED if st != w and st not in (lm,) else AMBER), mono=True)
    box(ax, 68, y, 28, 9, lm, fc=GREEN, mono=True)
ax.text(50, -3, "зелений — збіг із правильною початковою формою; червоний — штучний корінь; жовтий — слово не змінилося", ha="center", fontsize=10.5)
save(fig, __file__)
