#!/usr/bin/env python3
"""Таблиця метрик класифікації."""
import matplotlib.pyplot as plt
import numpy as np

# Метрики з лекції
metrics = {
    'negative': {'precision': 0.832, 'recall': 0.845, 'f1': 0.838, 'support': 200},
    'positive': {'precision': 0.843, 'recall': 0.830, 'f1': 0.836, 'support': 200},
}

fig, ax = plt.subplots(figsize=(12, 6), facecolor='#070b14')
ax.set_facecolor('#070b14')
ax.axis('off')

# Заголовок
title = ax.text(0.5, 0.95, 'Метрики класифікації тональності відгуків',
                transform=ax.transAxes, fontsize=16, color='#e2e8f0',
                fontweight='bold', ha='center', va='top')

# Дані для таблиці
classes = ['Negative', 'Positive']
precision_vals = [metrics['negative']['precision'], metrics['positive']['precision']]
recall_vals = [metrics['negative']['recall'], metrics['positive']['recall']]
f1_vals = [metrics['negative']['f1'], metrics['positive']['f1']]

# Позиції барів
y_pos = np.array([1.5, 1.0])
bar_height = 0.12
colors = ['#ef4444', '#10b981']

# Precision
for i, (cls, val, col) in enumerate(zip(classes, precision_vals, colors)):
    ax.barh(y_pos[i] + 0.25, val, bar_height, color=col, edgecolor='#334155', linewidth=1.5)
    ax.text(val + 0.02, y_pos[i] + 0.25, f'{val:.3f}', va='center', fontsize=11, color=col, fontweight='bold')

ax.text(0.05, y_pos[0] + 0.25, 'Precision', va='center', fontsize=11, color='#e2e8f0', fontweight='bold')

# Recall
for i, (cls, val, col) in enumerate(zip(classes, recall_vals, colors)):
    ax.barh(y_pos[i], val, bar_height, color=col, edgecolor='#334155', linewidth=1.5)
    ax.text(val + 0.02, y_pos[i], f'{val:.3f}', va='center', fontsize=11, color=col, fontweight='bold')

ax.text(0.05, y_pos[0], 'Recall', va='center', fontsize=11, color='#e2e8f0', fontweight='bold')

# F1
for i, (cls, val, col) in enumerate(zip(classes, f1_vals, colors)):
    ax.barh(y_pos[i] - 0.25, val, bar_height, color=col, edgecolor='#334155', linewidth=1.5)
    ax.text(val + 0.02, y_pos[i] - 0.25, f'{val:.3f}', va='center', fontsize=11, color=col, fontweight='bold')

ax.text(0.05, y_pos[0] - 0.25, 'F1-score', va='center', fontsize=11, color='#e2e8f0', fontweight='bold')

# Мітки класів
for i, (cls, col) in enumerate(zip(classes, colors)):
    ax.text(0.52, y_pos[i], cls, fontsize=12, color=col, fontweight='bold', ha='center')

# Загальна точність
acc = 0.838
ax.text(0.5, 0.2, f'Accuracy: {acc:.1%}', transform=ax.transAxes,
        fontsize=14, color='#06b6d4', fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#0f172a', edgecolor='#06b6d4', linewidth=2))

ax.set_xlim(0, 1.1)
ax.set_ylim(0.5, 2)

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/text-classification-baseline/01-metrics-table.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 01-metrics-table.png створено")
