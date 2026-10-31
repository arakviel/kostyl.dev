#!/usr/bin/env python3
"""Частота від рангу на лінійній шкалі."""
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import movie_reviews

# Завантажити всі слова
all_words = [
    w.lower() for fid in movie_reviews.fileids()
    for w in movie_reviews.words(fid)
    if any(c.isalpha() for c in w)
]

freq = Counter(all_words)
top100 = freq.most_common(100)
ranks = list(range(1, len(top100) + 1))
frequencies = [count for _, count in top100]

# Створення графіка
fig, ax = plt.subplots(figsize=(11, 6), facecolor='#070b14')
ax.set_facecolor('#070b14')

ax.plot(ranks, frequencies, marker='o', markersize=4, color='#06b6d4', 
        linewidth=2, markeredgecolor='#0e7490', markeredgewidth=0.8)

ax.set_xlabel('Ранг слова', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_ylabel('Частота', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('Частота від рангу (лінійна шкала)', 
             fontsize=15, color='#e2e8f0', fontweight='bold', pad=20)

# Виділити першу і останню точку
ax.plot(ranks[0], frequencies[0], 'o', markersize=8, color='#10b981', markeredgecolor='#059669', markeredgewidth=1.5)
ax.plot(ranks[-1], frequencies[-1], 'o', markersize=8, color='#f59e0b', markeredgecolor='#d97706', markeredgewidth=1.5)

ax.annotate(f'Ранг 1: {frequencies[0]:,}', xy=(ranks[0], frequencies[0]), 
            xytext=(10, frequencies[0] - 8000), fontsize=10, color='#10b981', fontweight='bold')
ax.annotate(f'Ранг 100: {frequencies[-1]:,}', xy=(ranks[-1], frequencies[-1]), 
            xytext=(70, frequencies[-1] + 3000), fontsize=10, color='#f59e0b', fontweight='bold')

ax.tick_params(colors='#e2e8f0', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.grid(alpha=0.2, color='#334155', linestyle='--')

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/corpus-and-frequency/03-zipf-linear.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 03-zipf-linear.png створено")
