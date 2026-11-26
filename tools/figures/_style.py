"""Спільний стиль для картинок лекцій: білий фон, світла палітра, DejaVu Sans."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

INK = "#1E293B"
GREY = "#E2E8F0"
BLUE = "#DBEAFE"
GREEN = "#DCFCE7"
AMBER = "#FEF3C7"
RED = "#FEE2E2"
ACCENT = "#2563EB"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "text.color": INK,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

ROOT = Path(__file__).resolve().parent


def canvas(width=10, height=3.4):
    """Порожнє полотно з координатами 0..100 по обох осях."""
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=GREY, mono=False, size=13, weight="normal", ec=INK, lw=1.4, ls="-",
        alpha=1.0, align="center"):
    """align="left" — текст (код) вирівнюється по лівому краю блока з відступом."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=2",
                                fc=fc, ec=ec, lw=lw, ls=ls, alpha=alpha))
    tx = x + w / 2 if align == "center" else x + 1.5
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=size, multialignment=align,
            fontfamily="DejaVu Sans Mono" if mono else "DejaVu Sans", fontweight=weight,
            linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, label=None, size=11, color=INK, lw=1.6, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=18,
                                 lw=lw, color=color, ls=ls, connectionstyle=f"arc3,rad={rad}"))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 4, label, ha="center", va="bottom", fontsize=size)


def save(fig, script_file):
    """tools/figures/<шлях>/NN-name.py -> public/images/<шлях>/NN-name.png"""
    script = Path(script_file).resolve()
    out = ROOT.parent.parent / "public" / "images" / script.parent.relative_to(ROOT) / f"{script.stem}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(out)


def chips(ax, x, y, tokens, fc=GREY, h=9, size=12, gap=1.2, char_w=1.55, pad=2.6, mono=True, colors=None):
    """Ряд «фішок»-токенів; повертає x правого краю."""
    for i, t in enumerate(tokens):
        w = max(5.0, len(t) * char_w + pad)
        color = colors[i] if colors else fc
        box(ax, x, y, w, h, t, fc=color, mono=mono, size=size)
        x += w + gap
    return x


def save_steps(script_file, steps, draw, size=(12, 6.75), dpi=160, poster=-1):
    """Покрокова анімація: steps — список (стан, секунди); draw(ax, стан) малює кадр на canvas.

    tools/figures/<шлях>/anim-NN-name.py -> public/videos/<шлях>/anim-NN-name.{mp4,webm,gif,png}
    Розмір кадру фіксований (без bbox_inches="tight"), щоб усі кадри мали однакові розміри.
    """
    import shutil
    import subprocess
    import tempfile

    script = Path(script_file).resolve()
    out_dir = ROOT.parent.parent / "public" / "videos" / script.parent.relative_to(ROOT)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / script.stem
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        lines = []
        for i, (state, seconds) in enumerate(steps):
            fig, ax = canvas(*size)
            fig.subplots_adjust(0, 0, 1, 1)
            draw(ax, state)
            frame = tmp / f"{i:03d}.png"
            fig.savefig(frame, dpi=dpi)
            plt.close(fig)
            lines += [f"file '{frame}'", f"duration {seconds}"]
        lines.append(f"file '{frame}'")  # concat вимагає повторити останній кадр
        (tmp / "list.txt").write_text("\n".join(lines))
        src = ["-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt")]
        even = "scale=trunc(iw/2)*2:trunc(ih/2)*2"
        ff = ["ffmpeg", "-y", "-loglevel", "error"]
        subprocess.run(ff + src + ["-vf", f"fps=25,{even},format=yuv420p", "-c:v", "libx264", "-crf", "20",
                                   "-movflags", "+faststart", f"{stem}.mp4"], check=True)
        subprocess.run(ff + src + ["-vf", f"fps=25,{even},format=yuv420p", "-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0",
                                   f"{stem}.webm"], check=True)
        subprocess.run(ff + src + ["-vf", "fps=8,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                                   f"{stem}.gif"], check=True)
        shutil.copy(tmp / f"{(poster % len(steps)):03d}.png", f"{stem}.png")
    print(f"{stem}.mp4")


def anatomy(width, height, lines, marks, notes, size=17, x0=24, y0=80, step=9.5):
    """lines — рядки коду; marks — (рядок, колонка, довжина, колір);
    notes — (рядок, колонка, текст, x підпису, y підпису, ha). Повертає (fig, ax)."""
    fig, ax = canvas(width, height)
    char = 0.602 * size / 72 / (ax.get_position().width * width) * 100
    for line, start, length, color in marks:
        y = y0 - line * step
        ax.add_patch(Rectangle((x0 + start * char - 0.2, y - step / 2 + 0.6), length * char + 0.4, step - 1.2,
                               fc=color, ec="none", zorder=1))
    for i, text in enumerate(lines):
        ax.text(x0, y0 - i * step, text, fontsize=size, fontfamily="DejaVu Sans Mono", va="center", zorder=2)
    for line, col, text, tx, ty, ha in notes:
        x = x0 + col * char
        y = y0 - line * step
        if abs(ty - y) < step / 2:          # підпис збоку — стрілка до краю символу
            target = (x, y)
        else:                               # підпис вище чи нижче — стрілка до верхнього чи нижнього краю
            target = (x, y + (step / 2 - 0.6) * (1 if ty > y else -1))
        ax.annotate(text, xy=target, xytext=(tx, ty), fontsize=12.5, ha=ha, va="center", color=INK, linespacing=1.3,
                    arrowprops=dict(arrowstyle="-", color="#475569", lw=1.1, shrinkA=4, shrinkB=2))
    return fig, ax
