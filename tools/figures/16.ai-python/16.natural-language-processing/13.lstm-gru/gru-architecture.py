#!/usr/bin/env python3
"""
Схема GRU архітектури з reset і update gates
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('GRU Architecture (один крок часу)', fontsize=16, fontweight='bold', pad=20)

# Кольори
color_reset = '#f97316'
color_update = '#06b6d4'
color_hidden = '#8b5cf6'

# Вхід x_t (знизу)
ax.arrow(3, 1, 0, 1.3, head_width=0.25, head_length=0.2, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(3, 0.5, '$x_t$', fontsize=14, fontweight='bold', ha='center')

ax.arrow(6, 1, 0, 1.3, head_width=0.25, head_length=0.2, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(6, 0.5, '$x_t$', fontsize=14, fontweight='bold', ha='center')

ax.arrow(9, 1, 0, 1.3, head_width=0.25, head_length=0.2, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(9, 0.5, '$x_t$', fontsize=14, fontweight='bold', ha='center')

# h_{t-1} (зліва)
ax.arrow(1, 4, 1.3, 0, head_width=0.2, head_length=0.15, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(0.5, 4, '$h_{t-1}$', fontsize=14, fontweight='bold', ha='right', va='center')

# Горизонтальна лінія h_{t-1}
ax.plot([2.5, 10.5], [4, 4], 'k--', linewidth=2, alpha=0.4)

# ========== RESET GATE ==========
# Сигмоїда блок
reset_box = FancyBboxPatch((2.5, 3.3), 1, 1, boxstyle="round,pad=0.1", 
                           edgecolor=color_reset, facecolor='#fed7aa', linewidth=2.5)
ax.add_patch(reset_box)
ax.text(3, 3.8, 'σ', ha='center', va='center', fontsize=18, fontweight='bold', color=color_reset)

# Множення
circle_mult_reset = Circle((3, 5.5), 0.35, edgecolor=color_reset, facecolor='white', linewidth=2.5)
ax.add_patch(circle_mult_reset)
ax.text(3, 5.5, '⊗', ha='center', va='center', fontsize=20, fontweight='bold')
ax.text(2.2, 5.5, '$r_t$', fontsize=12, fontweight='bold', ha='right', va='center', color=color_reset)

# Стрілки
ax.arrow(3, 4.35, 0, 0.75, head_width=0.15, head_length=0.12, fc=color_reset, ec=color_reset, linewidth=2)
ax.arrow(3, 4, 0, -0.5, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=1.5)

# ========== UPDATE GATE ==========
# Сигмоїда блок
update_box = FancyBboxPatch((5.5, 3.3), 1, 1, boxstyle="round,pad=0.1", 
                            edgecolor=color_update, facecolor='#cffafe', linewidth=2.5)
ax.add_patch(update_box)
ax.text(6, 3.8, 'σ', ha='center', va='center', fontsize=18, fontweight='bold', color=color_update)

ax.arrow(6, 4, 0, -0.5, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=1.5)

# ========== CANDIDATE ==========
# tanh блок
candidate_box = FancyBboxPatch((8.5, 5), 1, 1, boxstyle="round,pad=0.1", 
                               edgecolor=color_hidden, facecolor='#ede9fe', linewidth=2.5)
ax.add_patch(candidate_box)
ax.text(9, 5.5, 'tanh', ha='center', va='center', fontsize=14, fontweight='bold', color=color_hidden)

# Стрілка від reset*h_{t-1}
ax.arrow(3.35, 5.5, 5, 0, head_width=0.15, head_length=0.15, fc='black', ec='black', linewidth=2)
ax.arrow(9, 4, 0, 0.85, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=1.5)

ax.text(6, 5.5, '$r_t \\odot h_{t-1}$', fontsize=11, ha='center', va='bottom', style='italic')
ax.text(9, 6.2, '$\\tilde{h}_t$', fontsize=13, fontweight='bold', ha='center', color=color_hidden)

# ========== FINAL h_t ==========
# (1 - z_t)
circle_one_minus = Circle((6, 7), 0.35, edgecolor=color_update, facecolor='white', linewidth=2.5)
ax.add_patch(circle_one_minus)
ax.text(6, 7, '1−', ha='center', va='center', fontsize=14, fontweight='bold')

# Стрілка від z_t
ax.arrow(6, 4.35, 0, 2.3, head_width=0.15, head_length=0.12, fc=color_update, ec=color_update, linewidth=2)

# Множення (1-z_t) * h_{t-1}
circle_mult1 = Circle((4.5, 7), 0.35, edgecolor='black', facecolor='white', linewidth=2.5)
ax.add_patch(circle_mult1)
ax.text(4.5, 7, '⊗', ha='center', va='center', fontsize=20, fontweight='bold')

ax.arrow(4.5, 4, 0, 2.6, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=1.5, linestyle='--')
ax.arrow(5.65, 7, -0.95, 0, head_width=0.15, head_length=0.12, fc=color_update, ec=color_update, linewidth=2)

# Множення z_t * h_tilde
circle_mult2 = Circle((9, 7), 0.35, edgecolor='black', facecolor='white', linewidth=2.5)
ax.add_patch(circle_mult2)
ax.text(9, 7, '⊗', ha='center', va='center', fontsize=20, fontweight='bold')

ax.arrow(9, 6.05, 0, 0.6, head_width=0.15, head_length=0.12, fc=color_hidden, ec=color_hidden, linewidth=2)
ax.arrow(6.35, 7, 2.3, 0, head_width=0.15, head_length=0.12, fc=color_update, ec=color_update, linewidth=2)

ax.text(7.5, 7, '$z_t$', fontsize=12, fontweight='bold', ha='center', va='bottom', color=color_update)

# Додавання
circle_add = Circle((6.75, 8.3), 0.35, edgecolor='black', facecolor='#dcfce7', linewidth=2.5)
ax.add_patch(circle_add)
ax.text(6.75, 8.3, '+', ha='center', va='center', fontsize=24, fontweight='bold')

ax.arrow(4.5, 7.35, 2, 0.85, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=2)
ax.arrow(9, 7.35, -2, 0.85, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=2)

# h_t вихід
ax.arrow(6.75, 8.7, 0, 0.8, head_width=0.25, head_length=0.2, fc=color_hidden, ec=color_hidden, linewidth=2.5)
ax.text(6.75, 9.7, '$h_t$', fontsize=14, fontweight='bold', ha='center', color=color_hidden)

# Підписи формул
ax.text(3, 2.8, '$r_t$', fontsize=12, fontweight='bold', ha='center', color=color_reset)
ax.text(6, 2.8, '$z_t$', fontsize=12, fontweight='bold', ha='center', color=color_update)

# Формули внизу
formulas = [
    "$r_t = \\sigma(W_r [h_{t-1}, x_t])$",
    "$z_t = \\sigma(W_z [h_{t-1}, x_t])$",
    "$\\tilde{h}_t = \\tanh(W_h [r_t \\odot h_{t-1}, x_t])$",
    "$h_t = (1 - z_t) \\odot h_{t-1} + z_t \\odot \\tilde{h}_t$"
]

formula_text = '\n'.join(formulas)
ax.text(6, 0.2, formula_text, ha='center', va='bottom', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef3c7', alpha=0.95))

# Легенда
ax.add_patch(mpatches.Rectangle((9.5, 8.5), 0.4, 0.4, facecolor=color_reset, alpha=0.5))
ax.text(10.2, 8.7, 'Reset gate ($r_t$)', fontsize=10, va='center')

ax.add_patch(mpatches.Rectangle((9.5, 8), 0.4, 0.4, facecolor=color_update, alpha=0.5))
ax.text(10.2, 8.2, 'Update gate ($z_t$)', fontsize=10, va='center')

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/13.lstm-gru/gru-architecture.png', 
            dpi=150, bbox_inches='tight')
print("✓ Збережено: gru-architecture.png")
