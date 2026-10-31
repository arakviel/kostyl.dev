#!/usr/bin/env python3
"""Стовпчикова діаграма 25 найчастіших слів."""
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
top25 = freq.most_common(25)
words, counts = zip(*top25)

# Створення графіка
fig, ax = plt.subplots(figsize=(14, 6), facecolor='#070b14')
ax.set_facecolor('#070b14')

bars = ax.bar(range(len(words)), counts, color='#06b6d4', edgecolor='#0e7490', linewidth=1.2)

ax.set_xticks(range(len(words)))
ax.set_xticklabels(words, rotation=60, ha='right', fontsize=10, color='#e2e8f0')
ax.set_ylabel('Частота', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_xlabel('Слово', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('25 найчастіших слів: швидкий спад частоти', 
             fontsize=15, color='#e2e8f0', fontweight='bold', pad=20)

# Підсвітити перше і останнє
bars[0].set_color('#10b981')
bars[-1].set_color('#f59e0b')

# Додати анотації
ax.annotate(f'{counts[0]:,}', xy=(0, counts[0]), xytext=(0, counts[0] + 3000),
            ha='center', fontsize=10, color='#10b981', fontweight='bold')
ax.annotate(f'{counts[-1]:,}', xy=(24, counts[-1]), xytext=(24, counts[-1] + 2000),
            ha='center', fontsize=10, color='#f59e0b', fontweight='bold')

ax.tick_params(colors='#e2e8f0', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.grid(axis='y', alpha=0.2, color='#334155', linestyle='--')

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/corpus-and-frequency/02-top25-barplot.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 02-top25-barplot.png створено")
