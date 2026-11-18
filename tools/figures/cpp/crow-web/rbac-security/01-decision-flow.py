import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
steps = [("Запит", GREY, ""), ("Є правило\nу політиці?", BLUE, "немає →\nпотрібен вхід"), ("Публічне?", BLUE, "так →\nпропустити"), ("Є сесія?", BLUE, "ні → 401"), ("Ролі досить?", BLUE, "ні → 403"), ("CSRF-токен\nзбігається?", BLUE, "ні → 403"), ("Виконати\nобробник", GREEN, "")]
for i, (t, c, n) in enumerate(steps):
    x = 1 + i * 14.2
    box(ax, x, 46, 12, 28, t, fc=c, size=9.5)
    if i < 6: arrow(ax, x + 12.4, 60, x + 14, 60)
    if n: ax.text(x + 6, 36, n, ha="center", va="top", fontsize=8.8, linespacing=1.4, color="#DC2626" if "→ 40" in n or "→ 403" in n else INK)
ax.text(50, 8, "Перша невдала перевірка зупиняє запит; обробник виконується лише після всіх", ha="center", fontsize=11.5)
save(fig, __file__)
