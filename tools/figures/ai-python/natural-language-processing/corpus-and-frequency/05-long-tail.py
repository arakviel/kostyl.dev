#!/usr/bin/env python3
"""Розподіл слів за частотою: довгий хвіст."""
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
freq_of_freq = Counter(freq.values())

# Взяти перші 50 частот
frequencies = sorted([f for f in freq_of_freq.keys() if f <= 50])
word_counts = [freq_of_freq[f] for f in frequencies]

# Створення графіка
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#070b14')
ax.set_facecolor('#070b14')

bars = ax.bar(frequencies, word_counts, color='#06b6d4', edgecolor='#0e7490', linewidth=1)

# Підсвітити частоту 1
bars[0].set_color('#10b981')

ax.set_xlabel('Частота слова (скільки разів зустрілося)', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_ylabel('Кількість слів із такою частотою', fontsize=13, color='#e2e8f0', fontweight='bold')
ax.set_title('Довгий хвіст: більшість слів рідкісні', 
             fontsize=15, color='#e2e8f0', fontweight='bold', pad=20)

# Анотація для частоти 1
ax.annotate(f'{freq_of_freq[1]:,} слів\nлише 1 раз', 
            xy=(1, freq_of_freq[1]), xytext=(8, freq_of_freq[1] + 1200),
            fontsize=11, color='#10b981', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#10b981', lw=1.5))

# Додати текстову статистику
total_words_lte5 = sum(freq_of_freq[f] for f in range(1, 6))
total_types = len(freq)
percentage = total_words_lte5 / total_types * 100

ax.text(0.98, 0.97, f'Слова з частотою ≤5:\n{total_words_lte5:,} ({percentage:.1f}% словника)',
        transform=ax.transAxes, fontsize=11, color='#f59e0b', 
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#0f172a', edgecolor='#f59e0b', linewidth=2))

ax.tick_params(colors='#e2e8f0', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.grid(axis='y', alpha=0.2, color='#334155', linestyle='--')

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/corpus-and-frequency/05-long-tail.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 05-long-tail.png створено")
