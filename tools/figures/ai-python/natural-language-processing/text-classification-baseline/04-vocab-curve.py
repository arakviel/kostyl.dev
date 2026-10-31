#!/usr/bin/env python3
"""Крива якості від розміру словника."""
import matplotlib.pyplot as plt
import numpy as np

# Дані з лекції
sizes = [500, 1000, 2000, 5000, 10000, 20000]
f1_train = [0.891, 0.927, 0.957, 0.987, 0.995, 0.998]
f1_test = [0.805, 0.826, 0.833, 0.836, 0.839, 0.838]

fig, ax = plt.subplots(figsize=(12, 7), facecolor='#070b14')
ax.set_facecolor('#070b14')

# Лінії
ax.plot(sizes, f1_train, marker='o', markersize=8, color='#06b6d4', linewidth=3, 
        label='Навчання', markeredgecolor='#0e7490', markeredgewidth=1.5)
ax.plot(sizes, f1_test, marker='s', markersize=8, color='#10b981', linewidth=3, 
        label='Тест', markeredgecolor='#059669', markeredgewidth=1.5)

# Виділити оптимум (5000)
optimal_idx = 3
ax.plot(sizes[optimal_idx], f1_test[optimal_idx], 'o', markersize=14, 
        color='#f59e0b', markeredgecolor='#d97706', markeredgewidth=2, zorder=5)
ax.annotate('Оптимум:\n5000 слів', xy=(sizes[optimal_idx], f1_test[optimal_idx]), 
            xytext=(sizes[optimal_idx] + 3000, f1_test[optimal_idx] - 0.03),
            fontsize=11, color='#f59e0b', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2))

# Зона перенавчання
ax.axvspan(10000, 20000, alpha=0.15, color='#ef4444')
ax.text(15000, 0.96, 'Зона\nперенавчання', fontsize=11, color='#ef4444', 
        fontweight='bold', ha='center', va='center')

ax.set_xlabel('Розмір словника (max_features)', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_ylabel('F1-score', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('Вплив розміру словника на якість класифікації', 
             fontsize=15, color='#e2e8f0', fontweight='bold', pad=20)

ax.set_xscale('log')
ax.set_xticks(sizes)
ax.set_xticklabels([str(s) for s in sizes], fontsize=10, color='#e2e8f0')
ax.set_ylim(0.78, 1.01)

legend = ax.legend(fontsize=12, loc='lower right', framealpha=0.95)
legend.get_frame().set_facecolor('#0f172a')
legend.get_frame().set_edgecolor('#334155')
for text in legend.get_texts():
    text.set_color('#e2e8f0')

ax.tick_params(colors='#e2e8f0', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.grid(alpha=0.2, color='#334155', linestyle='--')

# Анотація
ax.text(0.03, 0.97, 'Тест насичується на 5000 слів\nНавчання зростає → перенавчання',
        transform=ax.transAxes, fontsize=10, color='#e2e8f0',
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#0f172a', edgecolor='#06b6d4', linewidth=2))

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/text-classification-baseline/04-vocab-curve.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 04-vocab-curve.png створено")
