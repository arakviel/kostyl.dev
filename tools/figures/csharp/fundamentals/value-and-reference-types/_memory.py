"""Спільні елементи схем пам'яті: комірка змінної в кадрі стеку, об'єкт у купі, стрілка-посилання."""
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK = "#1E293B"
MUTED = "#475569"
STACK_FC = "#DBEAFE"
HEAP_FC = "#DCFCE7"
OBJ_FC = "#FFFFFF"
HOT = "#FEF3C7"
ARROW = "#2563EB"


def region(ax, x, y, w, h, title, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.5", fc=fc, ec="none", alpha=0.55))
    ax.text(x + w / 2, y + h - 3.2, title, ha="center", va="center", fontsize=13, fontweight="bold", color=INK)


def cell(ax, x, y, w, h, name, value=None, hot=False, size=12.5):
    """Комірка змінної: ім'я ліворуч, значення праворуч. value=None — посилання (крапка), повертає точку виходу стрілки."""
    split = x + w * 0.48
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                fc=HOT if hot else OBJ_FC, ec=INK, lw=1.2))
    ax.plot([split, split], [y, y + h], color=INK, lw=0.8)
    ax.text(x + 1.2, y + h / 2, name, va="center", fontsize=size, fontfamily="DejaVu Sans Mono")
    if value is None:
        cx = (split + x + w) / 2
        ax.plot([cx], [y + h / 2], marker="o", color=ARROW, markersize=6)
        return cx, y + h / 2
    ax.text((split + x + w) / 2, y + h / 2, value, ha="center", va="center", fontsize=size,
            fontfamily="DejaVu Sans Mono", fontweight="bold")
    return None


def obj(ax, x, y, parts, widths, h=6, hot=False, size=12, label=None):
    """Об'єкт у купі: ряд клітинок (заголовок, тип, дані). Повертає точку входу стрілки (лівий край)."""
    cx = x
    for text, w in zip(parts, widths):
        muted = text in ("заголовок", "тип") or text.startswith("тип:") or text.startswith("довжина")
        ax.add_patch(FancyBboxPatch((cx, y), w, h, boxstyle="round,pad=0,rounding_size=0.5",
                                    fc="#F1F5F9" if muted else (HOT if hot else OBJ_FC), ec=INK, lw=1.0))
        ax.text(cx + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size - (2 if muted else 0),
                color=MUTED if muted else INK, fontfamily="DejaVu Sans" if muted else "DejaVu Sans Mono")
        cx += w
    if label:
        ax.text(x, y + h + 1.2, label, fontsize=10.5, color=MUTED, va="bottom")
    return x, y + h / 2


def ref(ax, start, end, rad=0.0, color=ARROW):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15, lw=1.6, color=color,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
