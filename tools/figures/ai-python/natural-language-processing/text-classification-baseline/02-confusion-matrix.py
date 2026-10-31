#!/usr/bin/env python3
"""Матриця помилок із теплової картою."""
import matplotlib.pyplot as plt
import numpy as np

# Матриця з лекції
cm = np.array([[169, 31], [34, 166]])

fig, ax = plt.subplots(figsize=(9, 8), facecolor='#070b14')
ax.set_facecolor('#070b14')

# Теплова карта
im = ax.imshow(cm, cmap='Blues', aspect='auto', alpha=0.8)

# Додати текст у кожну клітинку
for i in range(2):
    for j in range(2):
        val = cm[i, j]
        # Підсвітити діагональ
        if i == j:
            color = '#10b981'
            weight = 'bold'
            size = 22
        else:
            color = '#ef4444'
            weight = 'bold'
            size = 20
        
        text = ax.text(j, i, str(val), ha='center', va='center',
                      fontsize=size, color=color, fontweight=weight)

# Мітки осей
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Negative', 'Positive'], fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_yticklabels(['Negative', 'Positive'], fontsize=13, color='#e2e8f0', fontweight='bold')

ax.set_xlabel('Передбачено', fontsize=14, color='#e2e8f0', fontweight='bold', labelpad=10)
ax.set_ylabel('Справжнє', fontsize=14, color='#e2e8f0', fontweight='bold', labelpad=10)
ax.set_title('Матриця помилок: діагональ — правильні, off-diagonal — помилки', 
             fontsize=15, color='#e2e8f0', fontweight='bold', pad=20)

ax.tick_params(colors='#e2e8f0', labelsize=12)

# Додати анотації
ax.text(0, -0.4, 'True Negative\n(правильно негативні)', ha='center', fontsize=10, 
        color='#10b981', fontweight='bold')
ax.text(1, -0.4, 'False Positive\n(помилково позитивні)', ha='center', fontsize=10, 
        color='#ef4444', fontweight='bold')
ax.text(0, 1.4, 'False Negative\n(помилково негативні)', ha='center', fontsize=10, 
        color='#ef4444', fontweight='bold')
ax.text(1, 1.4, 'True Positive\n(правильно позитивні)', ha='center', fontsize=10, 
        color='#10b981', fontweight='bold')

# Статистика
tn, fp, fn, tp = cm.ravel()
total = tn + fp + fn + tp
accuracy = (tp + tn) / total

stats_text = f'Accuracy: {accuracy:.1%}  |  Correct: {tp + tn}/{total}  |  Errors: {fp + fn}/{total}'
ax.text(0.5, -0.15, stats_text, transform=ax.transAxes,
        fontsize=11, color='#e2e8f0', ha='center',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#0f172a', edgecolor='#06b6d4', linewidth=2))

for spine in ax.spines.values():
    spine.set_color('#334155')
    spine.set_linewidth(2)

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/text-classification-baseline/02-confusion-matrix.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 02-confusion-matrix.png створено")
