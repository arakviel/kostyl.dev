#!/usr/bin/env python3
"""Діаграма 20 найчастіших слів у корпусі Movie Reviews."""
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
top20 = freq.most_common(20)
words, counts = zip(*top20)

# Створення графіка
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#070b14')
ax.set_facecolor('#070b14')

bars = ax.bar(range(len(words)), counts, color='#06b6d4', edgecolor='#0e7490', linewidth=1.5)

ax.set_xticks(range(len(words)))
ax.set_xticklabels(words, rotation=45, ha='right', fontsize=11, color='#e2e8f0')
ax.set_ylabel('Частота', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_xlabel('Слово', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('20 найчастіших слів у корпусі Movie Reviews', 
             fontsize=15, color='#e2e8f0', fontweight='bold', pad=20)

# Додати значення на стовпчиках
for i, (bar, count) in enumerate(zip(bars, counts)):
    if i < 5:  # Тільки для перших 5
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1500,
                f'{count:,}', ha='center', va='bottom', fontsize=9, color='#06b6d4')

ax.tick_params(colors='#e2e8f0', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.grid(axis='y', alpha=0.2, color='#334155', linestyle='--')

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/corpus-and-frequency/01-top-words.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 01-top-words.png створено")
