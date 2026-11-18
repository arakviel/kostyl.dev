import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 3.8)
box(ax, 2, 40, 26, 40, "Модель\nдані й правила\n(kUsers, репозиторій)", fc=GREEN, size=11)
box(ax, 37, 40, 26, 40, "Контролер\nобробник маршруту\n(лямбда)", fc=BLUE, size=11)
box(ax, 72, 40, 26, 40, "Вигляд\nшаблон Mustache\n(.html)", fc=AMBER, size=11)
arrow(ax, 37, 66, 29, 66, "")
arrow(ax, 29, 52, 36, 52)
arrow(ax, 64, 60, 71, 60)
ax.text(32.5, 72, "дані", ha="center", fontsize=10.5)
ax.text(67.5, 66, "контекст", ha="center", fontsize=10.5)
ax.text(50, 20, "Браузер надсилає запит контролеру і отримує готовий HTML від вигляду", ha="center", fontsize=11.5)
save(fig, __file__)
