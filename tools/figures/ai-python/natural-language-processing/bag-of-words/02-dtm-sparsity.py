#!/usr/bin/env python3
"""Візуалізація матриці документ-слово та її розрідженості."""
import matplotlib.pyplot as plt
import numpy as np

# Симуляція розрідженої матриці
np.random.seed(42)
n_docs = 100
n_words = 200

# Створити розріджену матрицю (98.9% нулів)
sparsity = 0.989
matrix = np.zeros((n_docs, n_words))
n_nonzero = int(n_docs * n_words * (1 - sparsity))

# Випадково розмістити ненульові елементи
nonzero_positions = np.random.choice(n_docs * n_words, size=n_nonzero, replace=False)
for pos in nonzero_positions:
    i, j = divmod(pos, n_words)
    matrix[i, j] = np.random.randint(1, 5)

# Створення графіка
fig = plt.figure(figsize=(14, 8), facecolor='#070b14')
gs = fig.add_gridspec(2, 2, height_ratios=[3, 1], width_ratios=[3, 1], 
                       hspace=0.3, wspace=0.15)

# Основна теплова карта
ax_main = fig.add_subplot(gs[0, 0])
ax_main.set_facecolor('#070b14')

im = ax_main.imshow(matrix, aspect='auto', cmap='viridis', interpolation='nearest')
ax_main.set_xlabel('Індекс слова у словнику', fontsize=12, color='#e2e8f0', fontweight='bold')
ax_main.set_ylabel('Номер документа', fontsize=12, color='#e2e8f0', fontweight='bold')
ax_main.set_title('Матриця документ–слово: ненульові елементи яскраві', 
                  fontsize=13, color='#e2e8f0', fontweight='bold', pad=15)

ax_main.tick_params(colors='#e2e8f0', labelsize=10)
for spine in ax_main.spines.values():
    spine.set_color('#334155')

# Colorbar
cbar = plt.colorbar(im, ax=ax_main, pad=0.02)
cbar.set_label('Частота слова', color='#e2e8f0', fontsize=10, fontweight='bold')
cbar.ax.tick_params(colors='#e2e8f0', labelsize=9)
cbar.outline.set_edgecolor('#334155')

# Гістограма ненульових на документ
ax_hist_y = fig.add_subplot(gs[0, 1])
ax_hist_y.set_facecolor('#070b14')

nonzero_per_doc = (matrix > 0).sum(axis=1)
ax_hist_y.barh(range(n_docs), nonzero_per_doc, color='#06b6d4', edgecolor='#0e7490', linewidth=0.5)
ax_hist_y.set_xlabel('Ненульових\nслів', fontsize=10, color='#e2e8f0')
ax_hist_y.set_ylim(ax_main.get_ylim())
ax_hist_y.tick_params(colors='#e2e8f0', labelsize=9)
ax_hist_y.invert_xaxis()

for spine in ax_hist_y.spines.values():
    spine.set_color('#334155')
ax_hist_y.spines['top'].set_visible(False)
ax_hist_y.spines['right'].set_visible(False)

# Статистика внизу
ax_stats = fig.add_subplot(gs[1, :])
ax_stats.axis('off')

stats_text = f"""
Розмір матриці: {n_docs} документів × {n_words} слів = {n_docs * n_words:,} елементів
Ненульових: {n_nonzero:,} ({(1-sparsity)*100:.2f}%)  |  Нульових: {n_docs * n_words - n_nonzero:,} ({sparsity*100:.2f}%)
Пам'ять (щільна float64): {n_docs * n_words * 8 / 1024:.1f} КБ  |  Пам'ять (розріджена): {(n_nonzero * (8 + 4 + 4)) / 1024:.1f} КБ
"""

ax_stats.text(0.5, 0.5, stats_text.strip(), transform=ax_stats.transAxes,
              fontsize=11, color='#e2e8f0', ha='center', va='center',
              bbox=dict(boxstyle='round,pad=1', facecolor='#0f172a', edgecolor='#06b6d4', linewidth=2))

plt.suptitle('Розрідженість матриці документ–слово: 98,9% нулів', 
             fontsize=15, color='#e2e8f0', fontweight='bold', y=0.98)

plt.savefig('public/images/ai-python/natural-language-processing/bag-of-words/02-dtm-sparsity.png',
            dpi=150, facecolor='#070b14', edgecolor='none', bbox_inches='tight')
print("✓ 02-dtm-sparsity.png створено")
