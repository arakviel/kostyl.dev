import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.4)
box(ax, 1, 62, 22, 26, "HTTP-шар\nuser_api.hpp", fc=BLUE, size=11)
box(ax, 28, 62, 22, 26, "UserService\nбізнес-правила", fc=GREEN, weight="bold", size=11)
box(ax, 55, 62, 22, 26, "IUserRepository\nінтерфейс", fc=AMBER, weight="bold", size=11)
arrow(ax, 23.5, 75, 27.5, 75); arrow(ax, 50.5, 75, 54.5, 75)
for i, (n, c) in enumerate([("InMemory", GREY), ("JsonFile", GREY), ("Sqlite", GREY)]):
    box(ax, 12 + i * 25, 14, 20, 20, n, fc=c, size=11, mono=True)
    arrow(ax, 22 + i * 25, 35, 63 + (i - 1) * 5, 60)
box(ax, 80, 62, 19, 26, "Тести:\nпідміна\nреалізації", fc=RED, size=11)
arrow(ax, 79.5, 75, 77.5, 75)
ax.text(50, 3, "Сервіс залежить від інтерфейсу. Реалізацію обирає main (або тест)", ha="center", fontsize=11.5)
save(fig, __file__)
