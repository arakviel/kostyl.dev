"""Шлях тексту до моделі: карта модуля."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 4.6)
steps = [("Сирий текст", "«Не люблю каву!»", GREY, "01"), ("Очищення\nі токени", "[не, люблю, каву]", BLUE, "02–04"),
         ("Числа", "вектор слів", GREEN, "05–10"), ("Модель", "RNN · LSTM ·\nTransformer", AMBER, "11–16"), ("Результат", "негативний", RED, "")]
for i, (t, sub, fc, lec) in enumerate(steps):
    x = 1 + i * 20
    box(ax, x, 40, 17, 28, t, fc=fc, weight="bold", size=12)
    ax.text(x + 8.5, 28, sub, ha="center", va="top", fontsize=11, fontfamily="DejaVu Sans Mono")
    if lec:
        ax.text(x + 8.5, 78, f"лекції {lec}", ha="center", fontsize=11, color=ACCENT)
    if i < 4:
        arrow(ax, x + 17.6, 54, x + 19.6, 54)
save(fig, __file__)
