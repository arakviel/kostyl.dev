"""Попереднє навчання і донавчання."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _style import *

fig, ax = canvas(12, 3.8)
box(ax, 1, 58, 20, 28, "величезний\nкорпус тексту\n(мільярди слів)", fc=GREY, size=12)
box(ax, 30, 58, 20, 28, "pre-training\nпередбачати\nпропущене слово", fc=BLUE, size=12)
box(ax, 59, 58, 18, 28, "готова модель\nBERT /\nDistilBERT", fc=AMBER, size=12)
box(ax, 59, 8, 18, 28, "2000 відгуків\nIMDB з мітками", fc=GREEN, size=12)
box(ax, 83, 33, 16, 28, "fine-tuning\n→ класифікатор", fc=RED, size=12)
arrow(ax, 21.7, 72, 29.6, 72); arrow(ax, 50.7, 72, 58.6, 72)
arrow(ax, 77.7, 72, 84, 58); arrow(ax, 77.7, 22, 84, 36)
ax.text(40, 46, "один раз, на кластері GPU\n(дні або тижні)", ha="center", va="top", fontsize=11, color="#475569")
ax.text(56, 22, "ваш крок:\nхвилини на одному\nкомп'ютері", ha="right", va="center", fontsize=11, color="#475569")
save(fig, __file__)
