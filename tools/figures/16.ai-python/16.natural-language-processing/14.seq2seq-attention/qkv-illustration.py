#!/usr/bin/env python3
"""
Візуалізація концепції Query-Key-Value (Q/K/V) в attention
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# ========== ЛІВОРУЧ: Аналогія з словником ==========
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Аналогія: Attention як пошук у словнику', fontsize=13, fontweight='bold', pad=15)

# Query (запит)
query_box = FancyBboxPatch((1, 7.5), 2, 1, boxstyle="round,pad=0.1",
                           edgecolor='#8b5cf6', facecolor='#ede9fe', linewidth=2.5)
ax.add_patch(query_box)
ax.text(2, 8, 'Query\n"apple"', ha='center', va='center', fontsize=11, fontweight='bold', color='#8b5cf6')

# Keys (ключі словника)
keys = ["apple", "book", "cat"]
key_y_positions = [5.5, 4, 2.5]

for i, (key, y) in enumerate(zip(keys, key_y_positions)):
    # Key
    key_box = FancyBboxPatch((0.5, y), 1.5, 0.8, boxstyle="round,pad=0.08",
                             edgecolor='#3b82f6', facecolor='#dbeafe', linewidth=2)
    ax.add_patch(key_box)
    ax.text(1.25, y + 0.4, f'Key: "{key}"', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#3b82f6')
    
    # Value
    value_box = FancyBboxPatch((2.5, y), 1.5, 0.8, boxstyle="round,pad=0.08",
                               edgecolor='#10b981', facecolor='#d1fae5', linewidth=2)
    ax.add_patch(value_box)
    
    values_uk = ["яблуко", "книга", "кіт"]
    ax.text(3.25, y + 0.4, f'Value: "{values_uk[i]}"', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#10b981')
    
    # Стрілка від Query до Key (схожість)
    if i == 0:  # "apple" == "apple" — висока схожість
        alpha_val = 1.0
        lw = 3
    else:
        alpha_val = 0.2
        lw = 1
    
    ax.plot([2, 1.25], [7.5, y + 0.8], color='#f59e0b', linewidth=lw, alpha=alpha_val)
    
    if i == 0:
        ax.text(1.6, 6.7, 'Висока\nсхожість!', fontsize=9, color='#f59e0b',
                fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef3c7', alpha=0.9))

# Результат
result_box = FancyBboxPatch((5.5, 3.5), 3, 1.5, boxstyle="round,pad=0.15",
                            edgecolor='#10b981', facecolor='#d1fae5', linewidth=3)
ax.add_patch(result_box)
ax.text(7, 4.6, 'Результат:', ha='center', fontsize=11, fontweight='bold', color='#10b981')
ax.text(7, 4, '"яблуко"', ha='center', fontsize=13, fontweight='bold', color='#10b981')

ax.arrow(4.2, 5.5, 1.1, -1.2, head_width=0.2, head_length=0.15,
         fc='#10b981', ec='#10b981', linewidth=2.5)

# Пояснення
ax.text(5, 1.2, 'Query порівнюється з Keys → найсхожіший Key → повертає Value',
        ha='center', fontsize=10, style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f3f4f6', alpha=0.9))

# ========== ПРАВОРУЧ: Attention механізм ==========
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Attention: Q порівнюється з усіма K', fontsize=13, fontweight='bold', pad=15)

# Query
q_box = FancyBboxPatch((1, 7.5), 1.5, 1, boxstyle="round,pad=0.1",
                       edgecolor='#8b5cf6', facecolor='#ede9fe', linewidth=2.5)
ax.add_patch(q_box)
ax.text(1.75, 8, 'Q', ha='center', va='center', fontsize=14, fontweight='bold', color='#8b5cf6')
ax.text(1.75, 7.2, '(decoder\nstate)', ha='center', fontsize=8, style='italic')

# Keys + Values
n_kv = 4
kv_x_positions = np.linspace(4, 8, n_kv)
kv_y = 7.5

for i, x in enumerate(kv_x_positions):
    # Key
    k_box = FancyBboxPatch((x - 0.3, kv_y + 0.7), 0.6, 0.5, boxstyle="round,pad=0.05",
                           edgecolor='#3b82f6', facecolor='#dbeafe', linewidth=2)
    ax.add_patch(k_box)
    ax.text(x, kv_y + 0.95, f'$k_{{{i+1}}}$', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#3b82f6')
    
    # Value
    v_box = FancyBboxPatch((x - 0.3, kv_y), 0.6, 0.5, boxstyle="round,pad=0.05",
                           edgecolor='#10b981', facecolor='#d1fae5', linewidth=2)
    ax.add_patch(v_box)
    ax.text(x, kv_y + 0.25, f'$v_{{{i+1}}}$', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#10b981')
    
    # Стрілка від Q до K (обчислення схожості)
    ax.plot([2.6, x], [8, kv_y + 1.3], color='#f59e0b', linewidth=1.5,
            linestyle='--', alpha=0.6)

# Scores
ax.text(6, 6.5, 'Scores: $e_i = Q^T K_i$', ha='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fef3c7', alpha=0.9))

# Softmax
ax.arrow(6, 6.2, 0, -0.5, head_width=0.3, head_length=0.1,
         fc='#f59e0b', ec='#f59e0b', linewidth=2)
ax.text(6, 5.5, 'softmax', ha='center', fontsize=10, fontweight='bold', color='#f59e0b')

# Attention weights
alpha_values = [0.1, 0.6, 0.2, 0.1]
for i, (x, alpha) in enumerate(zip(kv_x_positions, alpha_values)):
    circle_size = 0.3 + alpha * 0.8
    circle = plt.Circle((x, 4.5), circle_size * 0.3, color='#f59e0b', alpha=0.7)
    ax.add_patch(circle)
    ax.text(x, 4.5, f'{alpha:.1f}', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')
    ax.text(x, 3.7, f'$\\alpha_{{{i+1}}}$', ha='center', fontsize=9, color='#f59e0b', fontweight='bold')

# Зважена сума
ax.arrow(6, 3.4, 0, -0.4, head_width=0.3, head_length=0.1,
         fc='#10b981', ec='#10b981', linewidth=2)

result_box2 = FancyBboxPatch((4.5, 1.5), 3, 1.2, boxstyle="round,pad=0.1",
                             edgecolor='#10b981', facecolor='#d1fae5', linewidth=3)
ax.add_patch(result_box2)
ax.text(6, 2.3, 'Вихід:', ha='center', fontsize=10, fontweight='bold', color='#10b981')
ax.text(6, 1.85, '$\\sum \\alpha_i v_i$', ha='center', fontsize=12, fontweight='bold', color='#10b981')

# Формула
formula = '$\\text{Attention}(Q, K, V) = \\text{softmax}(Q K^T) V$'
fig.text(0.5, 0.02, formula, ha='center', fontsize=13, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef3c7', edgecolor='#f59e0b', linewidth=2, alpha=0.95))

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig('public/images/16.ai-python/16.natural-language-processing/14.seq2seq-attention/qkv-illustration.png',
            dpi=150, bbox_inches='tight')
print("✓ Збережено: qkv-illustration.png")
