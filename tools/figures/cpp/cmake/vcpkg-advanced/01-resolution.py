import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(11, 4.4)
box(ax, 1, 62, 26, 28, "vcpkg.json\n\n\"fmt\"\nbuiltin-baseline", fc=BLUE, mono=True, size=10.5)
box(ax, 37, 62, 26, 28, "каталог vcpkg\nна цьому комміті\n\nfmt → 12.1.0", fc=GREY, size=11)
box(ax, 73, 62, 26, 28, "порт fmt\nportfile.cmake\nvcpkg.json", fc=AMBER, size=11)
arrow(ax, 27, 76, 37, 76, "baseline", 10)
arrow(ax, 63, 76, 73, 76, "порт", 10)
box(ax, 73, 10, 26, 28, "ключ ABI:\nкомпілятор + triplet\n+ версія порту", fc=GREY, size=10.5)
box(ax, 37, 10, 26, 28, "кеш збігся?\nтак → розпакувати\nні → зібрати", fc=GREEN, size=10.5)
box(ax, 1, 10, 26, 28, "build/vcpkg_installed\nготові .a / .lib\nі заголовки", fc=BLUE, mono=False, size=10.5)
arrow(ax, 86, 62, 86, 38)
arrow(ax, 73, 24, 63, 24)
arrow(ax, 37, 24, 27, 24)
save(fig, __file__)
