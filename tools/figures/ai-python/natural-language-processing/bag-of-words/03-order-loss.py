#!/usr/bin/env python3
"""Втрата порядку слів: речення з різним змістом мають однаковий вектор."""
import matplotlib.pyplot as plt
import numpy as np

# Дві пари речень
pairs = [
    ("dog bites man", "man bites dog"),
    ("not good but not bad", "not bad but not good")
]

vocab1 = ["dog", "bites", "man"]
vocab2 = ["not", "good", "but", "bad"]

# Створення графіка
fig, axes = plt.subplots(2, 2, figsize=(14, 8), facecolor='#070b14')

# Пара 1
for col, (text, vocab) in enumerate([(pairs[0][0], vocab1), (pairs[0][1], vocab1)]):
    ax = axes[0, col]
    ax.set_facecolor('#070b14')
    
    # Підрахунок
    words = text.split()
    counts = [words.count(w) for w in vocab]
    
    colors = ['#10b981' if c > 0 else '#1e293b' for c in counts]
    bars = ax.bar(range(len(vocab)), counts, color=colors, edgecolor='#059669', linewidth=2, width=0.6)
    
    ax.set_xticks(range(len(vocab)))
    ax.set_xticklabels(vocab, fontsize=11, color='#e2e8f0', fontweight='bold')
    ax.set_ylabel('Частота', fontsize=11, color='#e2e8f0')
    ax.set_ylim(0, 1.5)
    ax.set_title(f'"{text}"', fontsize=12, color='#e2e8f0', pad=10, fontweight='bold')
    
    # Додати значення на барах
    for bar, count in zip(bars, counts):
        if count > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                   str(count), ha='center', fontsize=10, color='#10b981', fontweight='bold')
    
    ax.tick_params(colors='#e2e8f0', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#334155')
    ax.spines['left'].set_color('#334155')
    ax.grid(axis='y', alpha=0.2, color='#334155', linestyle='--')

# Стрілка між ними
arrow_props = dict(arrowstyle='<->', color='#f59e0b', lw=3)
fig.text(0.5, 0.73, '= ІДЕНТИЧНІ ВЕКТОРИ =', ha='center', fontsize=12, 
         color='#f59e0b', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#f59e0b', linewidth=2))

# Пара 2
for col, (text, vocab) in enumerate([(pairs[1][0], vocab2), (pairs[1][1], vocab2)]):
    ax = axes[1, col]
    ax.set_facecolor('#070b14')
    
    words = text.split()
    counts = [words.count(w) for w in vocab]
    
    colors = ['#06b6d4' if c > 0 else '#1e293b' for c in counts]
    bars = ax.bar(range(len(vocab)), counts, color=colors, edgecolor='#0e7490', linewidth=2, width=0.6)
    
    ax.set_xticks(range(len(vocab)))
    ax.set_xticklabels(vocab, fontsize=11, color='#e2e8f0', fontweight='bold')
    ax.set_ylabel('Частота', fontsize=11, color='#e2e8f0')
    ax.set_ylim(0, 2.5)
    ax.set_title(f'"{text}"', fontsize=12, color='#e2e8f0', pad=10, fontweight='bold')
    
    for bar, count in zip(bars, counts):
        if count > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08,
                   str(count), ha='center', fontsize=10, color='#06b6d4', fontweight='bold')
    
    ax.tick_params(colors='#e2e8f0', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#334155')
    ax.spines['left'].set_color('#334155')
    ax.grid(axis='y', alpha=0.2, color='#334155', linestyle='--')

fig.text(0.5, 0.27, '= ІДЕНТИЧНІ ВЕКТОРИ =', ha='center', fontsize=12, 
         color='#f59e0b', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#f59e0b', linewidth=2))

plt.suptitle('Втрата порядку: різний зміст, однаковий мішок слів', 
             fontsize=15, color='#e2e8f0', fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('public/images/ai-python/natural-language-processing/bag-of-words/03-order-loss.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 03-order-loss.png створено")
