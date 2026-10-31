#!/usr/bin/env python3
"""
Візуалізація RNN: згорнута форма (з петлею) і розгорнута в часі
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# ========== ЛІВОРУЧ: Згорнута форма ==========
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('Згорнута форма (Folded)', fontsize=14, fontweight='bold', pad=20)

# RNN блок
rnn_box = FancyBboxPatch((4, 4), 2, 2, boxstyle="round,pad=0.1", 
                          edgecolor='#2563eb', facecolor='#dbeafe', linewidth=2.5)
ax1.add_patch(rnn_box)
ax1.text(5, 5, 'RNN', ha='center', va='center', fontsize=16, fontweight='bold')

# Вхід x_t (знизу)
ax1.arrow(5, 2.5, 0, 1.3, head_width=0.2, head_length=0.15, fc='#059669', ec='#059669', linewidth=2)
ax1.text(5, 1.8, r'$x_t$', ha='center', va='center', fontsize=14, color='#059669', fontweight='bold')

# Вихід h_t (вгору)
ax1.arrow(5, 6.2, 0, 1.3, head_width=0.2, head_length=0.15, fc='#dc2626', ec='#dc2626', linewidth=2)
ax1.text(5, 8.2, r'$h_t$', ha='center', va='center', fontsize=14, color='#dc2626', fontweight='bold')

# Петля (h_{t-1} → RNN)
# Стрілка вправо-вгору-вліво
arc = Arc((6.5, 5), 2, 2, angle=0, theta1=45, theta2=315, color='#7c3aed', linewidth=2.5)
ax1.add_patch(arc)
# Стрілка назад
ax1.arrow(5.4, 6.4, -0.35, -0.35, head_width=0.15, head_length=0.1, fc='#7c3aed', ec='#7c3aed', linewidth=2)
ax1.text(7.5, 5.8, r'$h_{t-1}$', ha='center', va='center', fontsize=13, color='#7c3aed', fontweight='bold')

# ========== ПРАВОРУЧ: Розгорнута форма ==========
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('Розгорнута в часі (Unfolded)', fontsize=14, fontweight='bold', pad=20)

# 4 RNN блоки
num_steps = 4
x_positions = [2 + i*3 for i in range(num_steps)]
box_size = 1.4

for i, x_pos in enumerate(x_positions):
    # RNN блок
    box = FancyBboxPatch((x_pos - box_size/2, 4.5), box_size, box_size, 
                          boxstyle="round,pad=0.08", 
                          edgecolor='#2563eb', facecolor='#dbeafe', linewidth=2)
    ax2.add_patch(box)
    ax2.text(x_pos, 5.2, 'RNN', ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Вхід x_t знизу
    ax2.arrow(x_pos, 2.8, 0, 1.5, head_width=0.15, head_length=0.12, 
              fc='#059669', ec='#059669', linewidth=1.8)
    ax2.text(x_pos, 2.0, f'$x_{{{i}}}$', ha='center', va='center', 
             fontsize=12, color='#059669', fontweight='bold')
    
    # Вихід h_t вгору
    ax2.arrow(x_pos, 6.0, 0, 1.2, head_width=0.15, head_length=0.12, 
              fc='#dc2626', ec='#dc2626', linewidth=1.8)
    ax2.text(x_pos, 7.8, f'$h_{{{i}}}$', ha='center', va='center', 
             fontsize=12, color='#dc2626', fontweight='bold')
    
    # Горизонтальна стрілка до наступного блоку
    if i < num_steps - 1:
        ax2.arrow(x_pos + box_size/2 + 0.1, 5.2, 3 - box_size - 0.4, 0, 
                  head_width=0.15, head_length=0.12, 
                  fc='#7c3aed', ec='#7c3aed', linewidth=2)

# Підписи часу
ax2.text(1, 0.8, 't = 0', ha='center', fontsize=11, style='italic', color='#6b7280')
ax2.text(13, 0.8, 't = 3', ha='center', fontsize=11, style='italic', color='#6b7280')
ax2.plot([1.5, 12.5], [1.2, 1.2], 'k--', alpha=0.3, linewidth=1)
ax2.text(7, 0.3, 'Час →', ha='center', fontsize=10, color='#6b7280', style='italic')

# Примітка
ax2.text(7, 9.2, 'Одні й ті ж ваги $W_h, W_x, b$ на всіх кроках', 
         ha='center', fontsize=10, style='italic', 
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef3c7', alpha=0.8))

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/12.rnn/rnn-unfolding.png', dpi=150, bbox_inches='tight')
print("✓ Збережено: public/images/16.ai-python/16.natural-language-processing/12.rnn/rnn-unfolding.png")
