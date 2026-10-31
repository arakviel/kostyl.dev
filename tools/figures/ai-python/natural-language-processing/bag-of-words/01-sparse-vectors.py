#!/usr/bin/env python3
"""Візуалізація розріджених векторів: три речення перетворені на вектори з більшістю нулів."""
import matplotlib.pyplot as plt
import numpy as np

# Приклади векторів (спрощені для демонстрації)
texts = [
    "this movie is excellent",
    "bad movie bad acting",
    "the film was not good but not terrible either"
]

# Симуляція векторів (5000 елементів, показуємо перші 100)
np.random.seed(42)
vocab_size = 100  # Для візуалізації
vectors = []

# Вектор 1: 4 ненульових
v1 = np.zeros(vocab_size)
v1[[9, 14, 5, 38]] = [1, 1, 1, 1]
vectors.append(v1)

# Вектор 2: 3 ненульових (bad двічі)
v2 = np.zeros(vocab_size)
v2[[14, 22, 22]] = [1, 2, 1]  # bad movie acting
v2[22] = 2  # bad appears twice
v2[14] = 1  # movie
v2[67] = 1  # acting
vectors.append(v2)

# Вектор 3: 7 ненульових
v3 = np.zeros(vocab_size)
v3[[0, 19, 33, 41, 52, 64, 78]] = [1, 1, 1, 2, 1, 1, 1]
v3[41] = 2  # not appears twice
vectors.append(v3)

# Створення графіка
fig, axes = plt.subplots(3, 1, figsize=(14, 8), facecolor='#070b14')

for i, (ax, vec, text) in enumerate(zip(axes, vectors, texts)):
    ax.set_facecolor('#070b14')
    
    # Показати вектор як bar plot
    colors = ['#06b6d4' if v > 0 else '#1e293b' for v in vec]
    bars = ax.bar(range(vocab_size), vec, color=colors, edgecolor='none', width=1.0)
    
    # Підсвітити ненульові
    for j, v in enumerate(vec):
        if v > 0:
            bars[j].set_edgecolor('#0e7490')
            bars[j].set_linewidth(1.5)
    
    non_zero = np.count_nonzero(vec)
    percentage = non_zero / vocab_size * 100
    
    ax.set_title(f'Текст: "{text}"  |  Ненульових: {non_zero}/{vocab_size} ({percentage:.1f}%)', 
                 fontsize=11, color='#e2e8f0', pad=10, fontweight='bold')
    ax.set_ylabel('Частота', fontsize=10, color='#e2e8f0')
    ax.set_ylim(0, 2.5)
    
    ax.tick_params(colors='#e2e8f0', labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#334155')
    ax.spines['left'].set_color('#334155')
    
    # Додати анотацію
    ax.text(0.98, 0.85, f'Решта {vocab_size - non_zero}\nпозицій нульові',
            transform=ax.transAxes, fontsize=10, color='#64748b',
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#334155', linewidth=1))

axes[-1].set_xlabel('Індекс у словнику (0–99)', fontsize=11, color='#e2e8f0', fontweight='bold')

plt.suptitle('Розріджені вектори: більшість позицій нульові', 
             fontsize=14, color='#e2e8f0', fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/bag-of-words/01-sparse-vectors.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 01-sparse-vectors.png створено")
