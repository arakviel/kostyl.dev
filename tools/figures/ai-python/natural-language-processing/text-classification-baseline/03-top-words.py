#!/usr/bin/env python3
"""Найвагоміші слова для кожного класу."""
import matplotlib.pyplot as plt
import numpy as np

# Дані з лекції
positive_words = [
    ('excellent', 1.687), ('wonderful', 1.435), ('perfect', 1.429), ('best', 1.414),
    ('fun', 1.380), ('great', 1.359), ('loved', 1.251), ('today', 1.198),
    ('enjoyed', 1.176), ('favorite', 1.164), ('outstanding', 1.144), ('beautifully', 1.142),
    ('superb', 1.139), ('brilliant', 1.130), ('entertaining', 1.126)
]

negative_words = [
    ('worst', -2.086), ('bad', -1.913), ('awful', -1.575), ('waste', -1.560),
    ('boring', -1.475), ('terrible', -1.417), ('poor', -1.299), ('worse', -1.286),
    ('stupid', -1.283), ('dull', -1.255), ('ridiculous', -1.226), ('annoying', -1.185),
    ('pointless', -1.145), ('unfunny', -1.113), ('lame', -1.102)
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8), facecolor='#070b14')

# Позитивні слова
ax1.set_facecolor('#070b14')
words_pos = [w for w, _ in positive_words]
coefs_pos = [c for _, c in positive_words]

bars1 = ax1.barh(range(len(words_pos)), coefs_pos, color='#10b981', edgecolor='#059669', linewidth=1.5)
ax1.set_yticks(range(len(words_pos)))
ax1.set_yticklabels(words_pos, fontsize=11, color='#e2e8f0')
ax1.set_xlabel('Коефіцієнт (вплив на клас)', fontsize=12, color='#e2e8f0', fontweight='bold')
ax1.set_title('Найвагоміші для ПОЗИТИВНОГО класу', fontsize=13, color='#10b981', fontweight='bold', pad=15)
ax1.invert_yaxis()

# Додати значення
for i, (bar, coef) in enumerate(zip(bars1, coefs_pos)):
    ax1.text(coef + 0.03, i, f'{coef:.2f}', va='center', fontsize=9, color='#10b981', fontweight='bold')

ax1.tick_params(colors='#e2e8f0', labelsize=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_color('#334155')
ax1.spines['left'].set_color('#334155')
ax1.grid(axis='x', alpha=0.2, color='#334155', linestyle='--')

# Негативні слова
ax2.set_facecolor('#070b14')
words_neg = [w for w, _ in negative_words]
coefs_neg = [c for _, c in negative_words]

bars2 = ax2.barh(range(len(words_neg)), coefs_neg, color='#ef4444', edgecolor='#dc2626', linewidth=1.5)
ax2.set_yticks(range(len(words_neg)))
ax2.set_yticklabels(words_neg, fontsize=11, color='#e2e8f0')
ax2.set_xlabel('Коефіцієнт (вплив на клас)', fontsize=12, color='#e2e8f0', fontweight='bold')
ax2.set_title('Найвагоміші для НЕГАТИВНОГО класу', fontsize=13, color='#ef4444', fontweight='bold', pad=15)
ax2.invert_yaxis()

# Додати значення
for i, (bar, coef) in enumerate(zip(bars2, coefs_neg)):
    ax2.text(coef - 0.03, i, f'{coef:.2f}', va='center', ha='right', fontsize=9, color='#ef4444', fontweight='bold')

ax2.tick_params(colors='#e2e8f0', labelsize=10)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_color('#334155')
ax2.spines['left'].set_color('#334155')
ax2.grid(axis='x', alpha=0.2, color='#334155', linestyle='--')

plt.suptitle('Коефіцієнти LogisticRegression: які слова найважливіші', 
             fontsize=15, color='#e2e8f0', fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/text-classification-baseline/03-top-words.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 03-top-words.png створено")
