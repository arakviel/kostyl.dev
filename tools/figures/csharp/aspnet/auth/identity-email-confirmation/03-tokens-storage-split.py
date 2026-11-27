"""Порівняння DataProtectionTokenProvider і таблиці AspNetUserTokens."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _style import AMBER, BLUE, GREEN, GREY, box, canvas, save

fig, ax = canvas(12, 4.6)

box(ax, 2, 81, 46, 14, "DataProtectionTokenProvider\n(за замовчуванням)", fc=BLUE, size=11.5, weight="bold")
box(ax, 52, 81, 46, 14, "Таблиця AspNetUserTokens\nу базі даних", fc=AMBER, size=11.5, weight="bold")

box(ax, 2, 52, 46, 24,
    "Призначення:\nEmailConfirmation, PasswordReset,\nChangeEmail\nЗберігання в БД: НЕ записується",
    fc=GREY, size=10.5, align="left")
box(ax, 2, 24, 46, 23,
    "Як перевіряється:\nРозшифрування ключем Data Protection +\nперевірка SecurityStamp та TTL (1 день)",
    fc=GREY, size=10.5, align="left")
box(ax, 2, 4, 46, 15,
    "Масштабування: stateless,\nпрацює без запису в БД",
    fc=GREEN, size=10.5)

box(ax, 52, 52, 46, 24,
    "Призначення:\n2FA AuthenticatorKey, зовнішні токени,\nвласні провайдери (ShortCode)",
    fc=GREY, size=10.5, align="left")
box(ax, 52, 24, 46, 23,
    "Первинний ключ:\n(UserId, LoginProvider, Name) -> Value\nНовий запис перезаписує старий",
    fc=GREY, size=10.5, align="left")
box(ax, 52, 4, 46, 15,
    "Контроль: можна явно видалити\nабо відкликати запис у БД",
    fc=GREEN, size=10.5)

save(fig, __file__)
