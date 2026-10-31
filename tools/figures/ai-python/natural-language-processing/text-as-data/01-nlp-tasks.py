"""Чотири типи задач NLP: що на вході, що на виході."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 5.2)
rows = [
    ("Класифікація", "«Чудовий товар!»", "позитивний відгук", BLUE),
    ("Пошук сутностей", "«Іван живе у Львові»", "Іван — особа,\nЛьвів — місто", GREEN),
    ("Переклад", "«Я люблю каву»", "«I love coffee»", AMBER),
    ("Відповідь на\nзапитання", "«Столиця України?»\n+ текст статті", "«Київ»", GREY),
]
for i, (name, inp, out, fc) in enumerate(rows):
    y = 76 - i * 24
    box(ax, 1, y, 22, 17, name, fc=fc, weight="bold", size=12)
    box(ax, 31, y, 30, 17, inp, fc="white", size=12)
    box(ax, 70, y, 29, 17, out, fc="white", size=12)
    arrow(ax, 24, y + 8.5, 30, y + 8.5)
    arrow(ax, 62, y + 8.5, 69, y + 8.5)
ax.text(46, 99, "вхід (текст)", ha="center", fontsize=12, color=ACCENT, fontweight="bold")
ax.text(84, 99, "вихід", ha="center", fontsize=12, color=ACCENT, fontweight="bold")
save(fig, __file__)
