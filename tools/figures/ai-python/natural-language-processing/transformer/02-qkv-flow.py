"""Self-attention: від embeddings до виходу."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 4.4)
box(ax, 1, 40, 11, 20, "X\nвхідні\nвектори", fc=GREY, size=12)
for y, name, col in [(76, "Q", BLUE), (40, "K", GREEN), (4, "V", AMBER)]:
    box(ax, 22, y, 10, 14, f"×W{name.lower()}", fc="white", size=12)
    box(ax, 38, y, 8, 14, name, fc=col, size=14, weight="bold")
    arrow(ax, 12.6, 50, 21.6, y + 7)
    arrow(ax, 32.6, y + 7, 37.6, y + 7)
box(ax, 54, 56, 14, 22, "Q·Kᵀ\n÷ √d", fc=GREY, size=12)
arrow(ax, 46.6, 83, 53.6, 72); arrow(ax, 46.6, 47, 53.6, 62)
box(ax, 73, 56, 11, 22, "softmax\nA", fc=BLUE, size=12)
arrow(ax, 68.6, 67, 72.6, 67)
box(ax, 88, 30, 11, 22, "A · V\nвихід", fc=GREEN, size=12)
arrow(ax, 84.6, 62, 91, 53); arrow(ax, 46.6, 11, 87.6, 38)
ax.text(78.5, 84, "ваги уваги\n(рядки сумуються до 1)", ha="center", fontsize=10.5, color="#475569")
save(fig, __file__)
