"""Спільна функція для схем лекції про рядки: ряд клітинок-символів з індексами."""
from matplotlib.patches import Rectangle

INK = "#1E293B"
MUTED = "#475569"


def cells(ax, x, y, text, w=6.0, h=11, fc="#DBEAFE", highlight=None, index=True, size=16, show_space=False):
    """highlight — словник {індекс: колір}. Повертає x правого краю."""
    for i, ch in enumerate(text):
        color = (highlight or {}).get(i, fc)
        ax.add_patch(Rectangle((x + i * w, y), w, h, fc=color, ec=INK, lw=1.1))
        shown = "·" if (show_space and ch == " ") else ch
        ax.text(x + i * w + w / 2, y + h / 2, shown, ha="center", va="center", fontsize=size,
                fontfamily="DejaVu Sans Mono", color=MUTED if shown == "·" else INK)
        if index:
            ax.text(x + i * w + w / 2, y - 3.8, str(i), ha="center", va="center", fontsize=10.5, color=MUTED)
    return x + len(text) * w
