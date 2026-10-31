#!/usr/bin/env python3
"""Зростання словника зі збільшенням розміру корпусу."""
import matplotlib.pyplot as plt
import random
from nltk.corpus import movie_reviews

random.seed(42)
fileids = movie_reviews.fileids()
random.shuffle(fileids)

sizes = [10, 25, 50, 100, 200, 500, 1000, 2000]
vocab_sizes = []

for n in sizes:
    words_n = [
        w.lower() for fid in fileids[:n] 
        for w in movie_reviews.words(fid)
        if any(c.isalpha() for c in w)
    ]
    vocab_sizes.append(len(set(words_n)))

# Створення графіка
fig, ax = plt.subplots(figsize=(11, 6), facecolor='#070b14')
ax.set_facecolor('#070b14')

ax.plot(sizes, vocab_sizes, marker='o', color='#06b6d4', linewidth=2.5, 
        markersize=8, markeredgecolor='#0e7490', markeredgewidth=1.5)

# Підсвітити першу і останню точку
ax.plot(sizes[0], vocab_sizes[0], 'o', markersize=10, color='#10b981', markeredgecolor='#059669', markeredgewidth=1.5)
ax.plot(sizes[-1], vocab_sizes[-1], 'o', markersize=10, color='#f59e0b', markeredgecolor='#d97706', markeredgewidth=1.5)

ax.set_xlabel('Кількість документів', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_ylabel('Розмір словника (унікальних слів)', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('Зростання словника сублінійне: кожен новий документ додає менше нових слів', 
             fontsize=14, color='#e2e8f0', fontweight='bold', pad=20)

# Анотації
ax.annotate(f'{sizes[0]} док.\n{vocab_sizes[0]:,} слів', 
            xy=(sizes[0], vocab_sizes[0]), xytext=(150, vocab_sizes[0] - 3000),
            fontsize=10, color='#10b981', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#10b981', lw=1.5))

ax.annotate(f'{sizes[-1]} док.\n{vocab_sizes[-1]:,} слів', 
            xy=(sizes[-1], vocab_sizes[-1]), xytext=(1700, vocab_sizes[-1] - 5000),
            fontsize=10, color='#f59e0b', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=1.5))

# Порівняння приросту
growth_first = vocab_sizes[1] - vocab_sizes[0]
growth_last = vocab_sizes[-1] - vocab_sizes[-2]

ax.text(0.03, 0.97, 
        f'Приріст 10→25 док.: +{growth_first:,} слів\nПриріст 1000→2000 док.: +{growth_last:,} слів',
        transform=ax.transAxes, fontsize=10, color='#e2e8f0', 
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#0f172a', edgecolor='#06b6d4', linewidth=2))

ax.tick_params(colors='#e2e8f0', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.grid(alpha=0.2, color='#334155', linestyle='--')

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/corpus-and-frequency/06-vocab-growth.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 06-vocab-growth.png створено")
