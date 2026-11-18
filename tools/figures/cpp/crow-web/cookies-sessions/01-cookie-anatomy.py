import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.2)
ax.text(2, 92, "Set-Cookie:", fontsize=12, family="DejaVu Sans Mono", weight="bold")
parts = [("sid=e584…ff84", "ім'я і значення\n(випадковий ідентифікатор)", BLUE, 2, 24), ("Path=/", "діє для\nвсього сайту", GREY, 28, 10), ("Max-Age=3600", "живе 1 годину;\n0 = видалити", AMBER, 40, 17), ("HttpOnly", "недоступний\nJavaScript", GREEN, 59, 14), ("SameSite=Lax", "не надсилається з\nчужих сайтів (POST)", GREEN, 75, 23)]
for t, n, c, x, w in parts:
    box(ax, x, 60, w, 18, t, fc=c, mono=True, size=9.8)
    ax.text(x + w / 2, 40, n, ha="center", va="center", fontsize=10, linespacing=1.4)
ax.text(50, 12, "Ще один атрибут: Secure — cookie передається лише через HTTPS", ha="center", fontsize=11.5)
save(fig, __file__)
