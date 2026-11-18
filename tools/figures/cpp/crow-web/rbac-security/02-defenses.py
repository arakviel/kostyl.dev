import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
ax.text(2, 94, "Загроза", fontsize=12.5, weight="bold"); ax.text(46, 94, "Захист у демо 17", fontsize=12.5, weight="bold")
rows = [("Пароль у відкритому вигляді", "argon2id із сіллю", GREEN), ("Підбір паролів", "ліміт спроб + однаковий час відповіді", GREEN), ("Крадіжка сесії через XSS", "cookie HttpOnly, заголовки CSP", GREEN), ("Підміна sid (session fixation)", "новий sid при кожному вході", GREEN), ("CSRF: чужий сайт діє від імені", "SameSite=Lax + токен X-CSRF-Token", GREEN), ("IDOR: чужі дані за id", "перевірка власника, 404 замість 403", GREEN)]
y = 82
for t, d, c in rows:
    box(ax, 1, y - 5.5, 98, 11, "", fc=c)
    ax.text(3, y, t, va="center", fontsize=10.6)
    ax.text(46, y, d, va="center", fontsize=10.6)
    y -= 13.5
save(fig, __file__)
