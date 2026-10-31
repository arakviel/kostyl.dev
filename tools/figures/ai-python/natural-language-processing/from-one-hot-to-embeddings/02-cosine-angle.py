#!/usr/bin/env python3
"""Косинусна подібність як кут між векторами."""
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#070b14')

# Три приклади: кут 0°, 90°, 180°
examples = [
    ([1, 1], [2, 2], 0, '#10b981', 'Кут 0°\nкосинус = 1\n(однаковий напрямок)'),
    ([1, 0], [0, 1], 90, '#06b6d4', 'Кут 90°\nкосинус = 0\n(перпендикулярні)'),
    ([1, 1], [-1, -1], 180, '#ef4444', 'Кут 180°\nкосинус = –1\n(протилежні)')
]

for ax, (v1, v2, angle, color, title) in zip(axes, examples):
    ax.set_facecolor('#070b14')
    
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    # Вектори
    ax.arrow(0, 0, v1[0], v1[1], head_width=0.15, head_length=0.15, 
             fc=color, ec=color, linewidth=2.5, length_includes_head=True, zorder=3)
    ax.arrow(0, 0, v2[0], v2[1], head_width=0.15, head_length=0.15, 
             fc='#f59e0b', ec='#f59e0b', linewidth=2.5, length_includes_head=True, zorder=3)
    
    # Кут
    if angle == 0:
        # Вектори накладаються, показати окремо
        ax.text(v1[0] + 0.3, v1[1] + 0.3, 'u', fontsize=12, color=color, fontweight='bold')
        ax.text(v2[0] - 0.3, v2[1] - 0.3, 'v', fontsize=12, color='#f59e0b', fontweight='bold')
    elif angle == 90:
        ax.text(v1[0] + 0.2, v1[1], 'u', fontsize=12, color=color, fontweight='bold')
        ax.text(v2[0], v2[1] + 0.2, 'v', fontsize=12, color='#f59e0b', fontweight='bold')
        # Показати прямий кут
        square_size = 0.2
        square = plt.Rectangle((0, 0), square_size, square_size, 
                               fill=False, edgecolor='#64748b', linewidth=1.5)
        ax.add_patch(square)
    else:  # 180
        ax.text(v1[0] + 0.3, v1[1] + 0.3, 'u', fontsize=12, color=color, fontweight='bold')
        ax.text(v2[0] - 0.3, v2[1] - 0.3, 'v', fontsize=12, color='#f59e0b', fontweight='bold')
    
    # Налаштування осей
    lim = 2.5
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color='#334155', linewidth=1, linestyle='--')
    ax.axvline(0, color='#334155', linewidth=1, linestyle='--')
    ax.set_aspect('equal')
    ax.grid(alpha=0.15, color='#334155')
    
    ax.set_title(title, fontsize=11, color='#e2e8f0', fontweight='bold', pad=10)
    
    ax.tick_params(colors='#e2e8f0', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#334155')

plt.suptitle('Косинусна подібність: чим менший кут, тим більший косинус', 
             fontsize=15, color='#e2e8f0', fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/from-one-hot-to-embeddings/02-cosine-angle.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 02-cosine-angle.png створено")
