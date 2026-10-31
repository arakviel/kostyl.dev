#!/usr/bin/env python3
"""
Схема LSTM архітектури з вентилями (forget, input, output) і cell state
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 12)
ax.axis('off')
ax.set_title('LSTM Architecture (один крок часу)', fontsize=16, fontweight='bold', pad=20)

# Кольори
color_forget = '#ef4444'
color_input = '#3b82f6'
color_output = '#8b5cf6'
color_cell = '#10b981'
color_hidden = '#f59e0b'

# Cell state (горизонтальна лінія вгорі)
ax.plot([1, 13], [9, 9], 'k-', linewidth=4, alpha=0.6)
ax.text(0.5, 9, '$C_{t-1}$', fontsize=14, fontweight='bold', ha='right', va='center')
ax.text(13.5, 9, '$C_t$', fontsize=14, fontweight='bold', ha='left', va='center')

# Вхід x_t (знизу)
ax.arrow(3, 1, 0, 1.3, head_width=0.25, head_length=0.2, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(3, 0.5, '$x_t$', fontsize=14, fontweight='bold', ha='center')

ax.arrow(7, 1, 0, 1.3, head_width=0.25, head_length=0.2, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(7, 0.5, '$x_t$', fontsize=14, fontweight='bold', ha='center')

ax.arrow(11, 1, 0, 1.3, head_width=0.25, head_length=0.2, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(11, 0.5, '$x_t$', fontsize=14, fontweight='bold', ha='center')

# h_{t-1} (знизу зліва)
ax.arrow(1, 3, 1.5, 0, head_width=0.2, head_length=0.15, fc='#6b7280', ec='#6b7280', linewidth=2.5)
ax.text(0.5, 3, '$h_{t-1}$', fontsize=14, fontweight='bold', ha='right', va='center')

# ========== FORGET GATE ==========
# Сигмоїда блок
forget_box = FancyBboxPatch((2.5, 3), 1, 1, boxstyle="round,pad=0.1", 
                            edgecolor=color_forget, facecolor='#fee2e2', linewidth=2.5)
ax.add_patch(forget_box)
ax.text(3, 3.5, 'σ', ha='center', va='center', fontsize=18, fontweight='bold', color=color_forget)

# Стрілка до cell state
ax.arrow(3, 4.1, 0, 1.5, head_width=0.2, head_length=0.15, fc=color_forget, ec=color_forget, linewidth=2.5)

# Множення з C_{t-1}
circle_mult1 = Circle((3, 7), 0.35, edgecolor=color_forget, facecolor='white', linewidth=2.5)
ax.add_patch(circle_mult1)
ax.text(3, 7, '⊗', ha='center', va='center', fontsize=20, fontweight='bold')
ax.text(3, 6.2, '$f_t$', fontsize=12, fontweight='bold', ha='center', color=color_forget)

# Стрілка від C_{t-1} до множення
ax.arrow(2, 9, 0.7, -1.7, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=2)

# Стрілка від множення далі
ax.arrow(3.4, 7, 2, 0, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=2)

# ========== INPUT GATE ==========
# Сигмоїда блок
input_box_sig = FancyBboxPatch((6.5, 3), 1, 1, boxstyle="round,pad=0.1", 
                               edgecolor=color_input, facecolor='#dbeafe', linewidth=2.5)
ax.add_patch(input_box_sig)
ax.text(7, 3.5, 'σ', ha='center', va='center', fontsize=18, fontweight='bold', color=color_input)

# tanh блок
input_box_tanh = FancyBboxPatch((8.5, 3), 1, 1, boxstyle="round,pad=0.1", 
                                edgecolor=color_input, facecolor='#dbeafe', linewidth=2.5)
ax.add_patch(input_box_tanh)
ax.text(9, 3.5, 'tanh', ha='center', va='center', fontsize=14, fontweight='bold', color=color_input)

# Стрілки до cell state
ax.arrow(7, 4.1, 0, 1.2, head_width=0.2, head_length=0.15, fc=color_input, ec=color_input, linewidth=2.5)
ax.arrow(9, 4.1, 0, 1.2, head_width=0.2, head_length=0.15, fc=color_input, ec=color_input, linewidth=2.5)

# Множення
circle_mult2 = Circle((7.5, 6), 0.35, edgecolor=color_input, facecolor='white', linewidth=2.5)
ax.add_patch(circle_mult2)
ax.text(7.5, 6, '⊗', ha='center', va='center', fontsize=20, fontweight='bold')
ax.text(7.5, 5.2, '$i_t \\odot \\tilde{C}_t$', fontsize=11, fontweight='bold', ha='center', color=color_input)

# Додавання до cell state
circle_add = Circle((7.5, 8), 0.35, edgecolor=color_cell, facecolor='white', linewidth=2.5)
ax.add_patch(circle_add)
ax.text(7.5, 8, '+', ha='center', va='center', fontsize=24, fontweight='bold', color=color_cell)

ax.arrow(5.6, 7, 1.6, 0.9, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=2)
ax.arrow(7.5, 6.4, 0, 1.2, head_width=0.15, head_length=0.12, fc=color_input, ec=color_input, linewidth=2)

# Cell state далі
ax.arrow(7.9, 8, 1, 0.9, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=2)

# ========== OUTPUT GATE ==========
# Сигмоїда блок
output_box = FancyBboxPatch((10.5, 3), 1, 1, boxstyle="round,pad=0.1", 
                            edgecolor=color_output, facecolor='#ede9fe', linewidth=2.5)
ax.add_patch(output_box)
ax.text(11, 3.5, 'σ', ha='center', va='center', fontsize=18, fontweight='bold', color=color_output)

# tanh від C_t
tanh_box = FancyBboxPatch((10.5, 7.5), 1, 1, boxstyle="round,pad=0.1", 
                          edgecolor=color_cell, facecolor='#d1fae5', linewidth=2.5)
ax.add_patch(tanh_box)
ax.text(11, 8, 'tanh', ha='center', va='center', fontsize=14, fontweight='bold', color=color_cell)

# Стрілка від C_t до tanh
ax.arrow(9.5, 9, 1.3, -0.7, head_width=0.15, head_length=0.12, fc='black', ec='black', linewidth=2)

# Множення
circle_mult3 = Circle((11, 5.5), 0.35, edgecolor=color_output, facecolor='white', linewidth=2.5)
ax.add_patch(circle_mult3)
ax.text(11, 5.5, '⊗', ha='center', va='center', fontsize=20, fontweight='bold')

# Стрілки
ax.arrow(11, 4.1, 0, 0.95, head_width=0.15, head_length=0.12, fc=color_output, ec=color_output, linewidth=2)
ax.arrow(11, 7.4, 0, -1.5, head_width=0.15, head_length=0.12, fc=color_cell, ec=color_cell, linewidth=2)

# h_t вихід
ax.arrow(11, 5.1, 0, -1.5, head_width=0.2, head_length=0.15, fc=color_hidden, ec=color_hidden, linewidth=2.5)
ax.text(11, 2.8, '$h_t$', fontsize=14, fontweight='bold', ha='center', color=color_hidden)
ax.text(11.5, 5.5, '$o_t$', fontsize=12, fontweight='bold', ha='left', va='center', color=color_output)

# Легенда
legend_y = 11
ax.text(1, legend_y, 'Вентилі:', fontsize=12, fontweight='bold')
ax.add_patch(mpatches.Rectangle((2.5, legend_y-0.2), 0.4, 0.4, facecolor=color_forget, alpha=0.5))
ax.text(3.2, legend_y, 'Forget gate ($f_t$)', fontsize=11, va='center')

ax.add_patch(mpatches.Rectangle((6, legend_y-0.2), 0.4, 0.4, facecolor=color_input, alpha=0.5))
ax.text(6.7, legend_y, 'Input gate ($i_t$)', fontsize=11, va='center')

ax.add_patch(mpatches.Rectangle((9.5, legend_y-0.2), 0.4, 0.4, facecolor=color_output, alpha=0.5))
ax.text(10.2, legend_y, 'Output gate ($o_t$)', fontsize=11, va='center')

# Формули внизу
formulas = [
    "$f_t = \\sigma(W_f [h_{t-1}, x_t] + b_f)$",
    "$i_t = \\sigma(W_i [h_{t-1}, x_t] + b_i)$",
    "$\\tilde{C}_t = \\tanh(W_C [h_{t-1}, x_t] + b_C)$",
    "$C_t = f_t \\odot C_{t-1} + i_t \\odot \\tilde{C}_t$",
    "$o_t = \\sigma(W_o [h_{t-1}, x_t] + b_o)$",
    "$h_t = o_t \\odot \\tanh(C_t)$"
]

formula_box = ax.text(7, 0.3, '  |  '.join(formulas), 
                      ha='center', va='bottom', fontsize=9,
                      bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef3c7', alpha=0.95))

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/13.lstm-gru/lstm-architecture.png', 
            dpi=150, bbox_inches='tight')
print("✓ Збережено: lstm-architecture.png")
