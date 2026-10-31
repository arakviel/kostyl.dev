#!/usr/bin/env python3
"""Закон Ципфа на логарифмічній шкалі."""
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

# Ідеальна лінія Ципфа
C = frequencies[0]
ideal = [C / r for r in ranks]

# Створення графіка
fig, ax = plt.subplots(figsize=(11, 6), facecolor='#070b14')
ax.set_facecolor('#070b14')

ax.loglog(ranks, frequencies, marker='o', markersize=5, color='#06b6d4', 
          linewidth=2, label='Реальні дані', markeredgecolor='#0e7490', markeredgewidth=0.8)
ax.loglog(ranks, ideal, linestyle='--', color='#f59e0b', linewidth=3, 
          label='Ідеальний Ципф (нахил –1)')

ax.set_xlabel('Ранг слова (log)', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_ylabel('Частота (log)', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('Закон Ципфа: частота обернено пропорційна рангу', 
             fontsize=15, color='#e2e8f0', fontweight='bold', pad=20)

legend = ax.legend(fontsize=11, loc='upper right', framealpha=0.9)
legend.get_frame().set_facecolor('#0f172a')
legend.get_frame().set_edgecolor('#334155')
for text in legend.get_texts():
    text.set_color('#e2e8f0')

ax.tick_params(colors='#e2e8f0', labelsize=10, which='both')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.grid(alpha=0.2, color='#334155', linestyle='--', which='both')

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/corpus-and-frequency/04-zipf-loglog.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 04-zipf-loglog.png створено")
