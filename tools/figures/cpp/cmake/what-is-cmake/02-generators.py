import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.6)
box(ax, 33, 80, 34, 16, "CMakeLists.txt\n(один опис проєкту)", fc=BLUE, mono=True, size=11)
box(ax, 40, 52, 20, 14, "CMake", fc=GREEN, size=13, weight="bold")
arrow(ax, 50, 80, 50, 66)
gens = [(2, "Makefile\nLinux"), (27, "Visual Studio\n.sln"), (52, "Xcode\nmacOS"), (77, "Ninja\nшвидка збірка")]
for x, t in gens:
    box(ax, x, 24, 21, 16, t, fc=AMBER, size=11)
    arrow(ax, 50, 52, x + 10.5, 40)
    arrow(ax, x + 10.5, 24, 50, 12)
box(ax, 28, 0, 44, 11, "Скомпільована програма", fc=GREY, size=12, weight="bold")
save(fig, __file__)
