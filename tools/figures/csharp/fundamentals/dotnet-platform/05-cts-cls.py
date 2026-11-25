"""CTS, CLS і мови: CLS — спільна частина, кожна мова бере з CTS трохи більше."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse  # noqa: E402
from _style import INK, save  # noqa: E402

fig, ax = plt.subplots(figsize=(12, 7.4))
ax.set_xlim(0, 120)
ax.set_ylim(-6, 74)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(Ellipse((60, 37), 112, 70, fc="#EEF2FF", ec="#4F46E5", lw=2))
ax.text(60, 68, "CTS — усе, що вміє описати платформа", ha="center", fontsize=14, fontweight="bold", color="#3730A3")

langs = [
    ((46, 41), 50, 36, 25, "#DBEAFE", "#2563EB", "C#", (28, 52)),
    ((74, 41), 50, 36, -25, "#DCFCE7", "#16A34A", "F#", (92, 52)),
    ((60, 26), 58, 40, 0, "#FEF3C7", "#D97706", "Visual Basic", (60, 15)),
]
for center, w, h, angle, fc, ec, name, label_at in langs:
    ax.add_patch(Ellipse(center, w, h, angle=angle, fc=fc, ec=ec, lw=2, alpha=0.55))
    ax.text(*label_at, name, ha="center", fontsize=14, fontweight="bold", color=ec)

ax.add_patch(Ellipse((60, 33.5), 22, 12, fc="#FDF4FF", ec="#A21CAF", lw=2.2))
ax.text(60, 36.3, "CLS", ha="center", va="center", fontsize=15, fontweight="bold", color="#86198F")
ax.text(60, 31.8, "int, string, double,\nкласи, методи", ha="center", va="center", fontsize=9.5, linespacing=1.15)

notes = [
    ((27, 38), "Count і count\nяк різні члени"),
    ((60, 45), "uint, ulong, sbyte: є в усіх\nтрьох мовах, але не в CLS"),
    ((60, 10), "XML-літерали"),
    ((94, 40), "одиниці виміру\n(units of measure)"),
]
for (x, y), text in notes:
    ax.text(x, y, text, ha="center", va="center", fontsize=10.5, color=INK, linespacing=1.2,
            bbox=dict(fc="white", ec="none", alpha=0.75, pad=2))

ax.text(60, -4, "Публічний API бібліотеки в межах CLS можна викликати з будь-якої мови .NET.",
        ha="center", fontsize=11.5, style="italic")
save(fig, __file__)
