"""Спільна функція: таблиця «так / ні / частково» з кольоровими клітинками."""
from matplotlib.patches import FancyBboxPatch

FILL = {"так": "#DCFCE7", "ні": "#FEE2E2", "частково": "#FEF3C7"}
INK = "#1E293B"


def matrix(ax, rows, cols, cells, x0=34, y0=86, col_w=21, row_h=11, head_size=12.5, size=12):
    for j, col in enumerate(cols):
        ax.text(x0 + j * col_w + col_w / 2, y0 + 5, col, ha="center", va="bottom", fontsize=head_size,
                fontweight="bold", linespacing=1.3)
    for i, row in enumerate(rows):
        y = y0 - i * row_h
        ax.text(1, y - row_h / 2, row, va="center", fontsize=size)
        for j in range(len(cols)):
            value, note = cells[i][j] if isinstance(cells[i][j], tuple) else (cells[i][j], "")
            ax.add_patch(FancyBboxPatch((x0 + j * col_w + 0.6, y - row_h + 0.8), col_w - 1.2, row_h - 1.6,
                                        boxstyle="round,pad=0.2,rounding_size=1", fc=FILL[value], ec="none"))
            label = value if not note else f"{value}\n{note}"
            ax.text(x0 + j * col_w + col_w / 2, y - row_h / 2, label, ha="center", va="center",
                    fontsize=size if not note else size - 1.5, color=INK, linespacing=1.2)
