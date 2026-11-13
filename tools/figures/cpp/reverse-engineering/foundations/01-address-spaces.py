import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
box(ax, 2, 62, 36, 30, "Процес «Гра»\nвласний адресний\nпростір", BLUE, size=13)
box(ax, 62, 62, 36, 30, "Процес «Тренер»\nвласний адресний\nпростір", GREEN, size=13)
box(ax, 30, 8, 40, 22, "Ядро ОС\nвіртуальна пам'ять,\nправа доступу", AMBER, size=13)
arrow(ax, 20, 62, 42, 31, "сторінки гри")
arrow(ax, 80, 62, 58, 31)
ax.text(86, 44, "ReadProcessMemory\nprocess_vm_readv\nmach_vm_read", ha="center", fontsize=11, fontfamily="DejaVu Sans Mono")
save(fig, __file__)
