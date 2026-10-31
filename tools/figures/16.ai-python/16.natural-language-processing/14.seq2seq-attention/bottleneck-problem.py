#!/usr/bin/env python3
"""
Візуалізація проблеми вузького місця (bottleneck) в seq2seq
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Wedge
import numpy as np

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Bottleneck Problem у Seq2Seq', fontsize=16, fontweight='bold', pad=20)

# Довге речення (вхід)
input_text = "The conference that was originally scheduled for June but got postponed to September will be held in Kyiv"
input_tokens = input_text.split()[:12]  # Беремо перші 12 слів

# Візуалізуємо як багато інформації
encoder_y = 6
token_width = 0.8
start_x = 0.5

for i, token in enumerate(input_tokens):
    x = start_x + i * token_width
    # Токени різної "важливості" (випадкова висота для візуального ефекту)
    np.random.seed(i)
    height = 0.4 + np.random.rand() * 0.3
    
    box = FancyBboxPatch((x, encoder_y - height/2), 0.6, height,
                          boxstyle="round,pad=0.02", edgecolor='#3b82f6',
                          facecolor='#dbeafe', alpha=0.8, linewidth=1.5)
    ax.add_patch(box)

ax.text(5, encoder_y - 1.2, f'Вхід: {len(input_tokens)} токенів (велика кількість інформації)',
        ha='center', fontsize=11, fontweight='bold', color='#3b82f6')

# Стрілки, що звужуються до bottleneck
# Лівий край
ax.plot([0.5, 5], [encoder_y + 0.5, 4], 'k-', linewidth=2, alpha=0.6)
ax.plot([0.5, 5], [encoder_y - 0.5, 4], 'k-', linewidth=2, alpha=0.6)

# Правий край
ax.plot([10, 5], [encoder_y + 0.5, 4], 'k-', linewidth=2, alpha=0.6)
ax.plot([10, 5], [encoder_y - 0.5, 4], 'k-', linewidth=2, alpha=0.6)

# Bottleneck (context vector c)
bottleneck_x = 5
bottleneck_y = 3.5
bottleneck_box = FancyBboxPatch((bottleneck_x - 0.5, bottleneck_y), 1, 1,
                                boxstyle="round,pad=0.1", edgecolor='#dc2626',
                                facecolor='#fee2e2', linewidth=4)
ax.add_patch(bottleneck_box)
ax.text(bottleneck_x, bottleneck_y + 0.5, '$c$', ha='center', va='center',
        fontsize=20, fontweight='bold', color='#dc2626')

ax.text(bottleneck_x, bottleneck_y - 0.7, 'Context Vector\n(один вектор фіксованого розміру)',
        ha='center', fontsize=10, fontweight='bold', color='#dc2626',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fee2e2', alpha=0.9))

# Проблеми (стрілки з текстом)
problems = [
    (7.5, 5.5, "Забування\nпочатку послідовності"),
    (7.5, 3.5, "Втрата деталей"),
    (7.5, 1.5, "Погана якість\nна довгих текстах")
]

for x, y, text in problems:
    ax.annotate(text, xy=(5.5, 3.5), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2),
                fontsize=10, color='#dc2626', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#fee2e2', alpha=0.9),
                ha='center')

# Декодер (вихід)
decoder_y = 1
decoder_tokens = ["Конференція", "...", "Київ"]
decoder_x_pos = [1.5, 5, 8.5]

ax.plot([bottleneck_x, bottleneck_x], [2.5, 1.5], 'k-', linewidth=2, alpha=0.6)
ax.arrow(bottleneck_x, 1.5, 0, -0.3, head_width=0.2, head_length=0.1,
         fc='#10b981', ec='#10b981', linewidth=2)

for x, token in zip(decoder_x_pos, decoder_tokens):
    box = FancyBboxPatch((x - 0.4, decoder_y - 0.3), 0.8, 0.5,
                          boxstyle="round,pad=0.08", edgecolor='#10b981',
                          facecolor='#d1fae5', alpha=0.8, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, decoder_y - 0.05, token, ha='center', va='center', fontsize=10, fontweight='bold')

ax.text(5, decoder_y - 0.8, 'Вихід: decoder має працювати лише з одним вектором c',
        ha='center', fontsize=11, fontweight='bold', color='#10b981')

# Питання
ax.text(bottleneck_x, 5.2, '❓ Як зберегти ВСЮ інформацію про довгу послідовність\nв одному векторі фіксованого розміру?',
        ha='center', fontsize=11, fontweight='bold', color='#b45309',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef3c7', alpha=0.95))

# Рішення
ax.text(bottleneck_x, 9, '💡 Рішення: ATTENTION — decoder має доступ до ВСІХ h₁, h₂, ..., hₙ!',
        ha='center', fontsize=12, fontweight='bold', color='#059669',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#d1fae5', edgecolor='#059669', linewidth=2.5, alpha=0.95))

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/14.seq2seq-attention/bottleneck-problem.png',
            dpi=150, bbox_inches='tight')
print("✓ Збережено: bottleneck-problem.png")
