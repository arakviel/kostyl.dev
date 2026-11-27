"""Порівняння підтвердження email при реєстрації та зміни email."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import AMBER, BLUE, GREEN, GREY, INK, arrow, box, canvas, save

fig, ax = canvas(11, 4.5)

# Заголовки колонок
box(ax, 3, 83, 44, 12, "ConfirmEmailAsync (реєстрація)", fc=BLUE, size=13, weight="bold")
box(ax, 53, 83, 44, 12, "ChangeEmailAsync (зміна адреси)", fc=AMBER, size=13, weight="bold")

# Ліва колонка
box(ax, 5, 62, 40, 14, "1. Email вже записано в БД\nEmailConfirmed = false", fc=GREY, size=11)
arrow(ax, 25, 61, 25, 51)
box(ax, 5, 36, 40, 14, "2. Токен містить:\nuserId + purpose + SecurityStamp", fc=GREY, size=11)
arrow(ax, 25, 35, 25, 25)
box(ax, 5, 7, 40, 17, "3. Результат:\nEmailConfirmed = true\nСесія не потребує оновлення", fc=GREEN, size=11)

# Права колонка
box(ax, 55, 62, 40, 14, "1. Старий Email активний\nНовий ще не записано в БД", fc=GREY, size=11)
arrow(ax, 75, 61, 75, 51)
box(ax, 55, 36, 40, 14, "2. Токен додатково містить\nnewEmail (захист від підміни)", fc=GREY, size=11)
arrow(ax, 75, 35, 75, 25)
box(ax, 55, 7, 40, 17, "3. Результат: новий Email,\nUserName і SecurityStamp\nПотрібен RefreshSignInAsync()", fc=GREEN, size=11)

save(fig, __file__)
