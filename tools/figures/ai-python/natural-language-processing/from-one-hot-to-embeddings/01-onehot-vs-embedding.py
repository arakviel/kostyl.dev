#!/usr/bin/env python3
"""Порівняння one-hot і embedding векторів."""
import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), facecolor='#070b14')

# One-hot вектор (словник 100 слів, індекс 42)
ax1.set_facecolor('#070b14')
vocab_size = 100
onehot = np.zeros(vocab_size)
onehot[42] = 1

# Показати лише перші 50 для читабельності
display_size = 50
x = range(display_size)
colors = ['#10b981' if i == 42 else '#1e293b' for i in x]

bars1 = ax1.bar(x, onehot[:display_size], color=colors, edgecolor='none', width=1.0)
bars1[42].set_edgecolor('#059669')
bars1[42].set_linewidth(2)

ax1.set_title('One-hot вектор: розмір = vocab_size (100), лише одна 1', 
              fontsize=13, color='#e2e8f0', fontweight='bold', pad=15)
ax1.set_ylabel('Значення', fontsize=11, color='#e2e8f0')
ax1.set_ylim(0, 1.3)
ax1.set_xlim(-1, display_size)

# Анотація
ax1.annotate('Індекс 42 = 1', xy=(42, 1), xytext=(42, 1.15),
            fontsize=10, color='#10b981', ha='center', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#10b981', lw=1.5))

ax1.text(0.98, 0.85, f'Розмір: {vocab_size}\nНенульових: 1 ({1/vocab_size*100:.1f}%)',
        transform=ax1.transAxes, fontsize=10, color='#e2e8f0',
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#334155', linewidth=1.5))

ax1.tick_params(colors='#e2e8f0', labelsize=9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_color('#334155')
ax1.spines['left'].set_color('#334155')

# Embedding вектор (розмір 10, щільний)
ax2.set_facecolor('#070b14')
embedding_dim = 10
np.random.seed(42)
embedding = np.random.randn(embedding_dim) * 0.5

x_emb = range(embedding_dim)
colors_emb = ['#06b6d4' if v > 0 else '#ef4444' for v in embedding]

bars2 = ax2.bar(x_emb, embedding, color=colors_emb, edgecolor='#0e7490', linewidth=1.5, width=0.6)

ax2.set_title('Embedding вектор: розмір = d (10), усі значення ненульові', 
              fontsize=13, color='#e2e8f0', fontweight='bold', pad=15)
ax2.set_ylabel('Значення', fontsize=11, color='#e2e8f0')
ax2.set_xlabel('Індекс у векторі', fontsize=11, color='#e2e8f0')
ax2.set_ylim(-0.8, 0.8)
ax2.set_xlim(-0.5, embedding_dim - 0.5)
ax2.axhline(0, color='#334155', linewidth=1, linestyle='--')

# Додати значення
for i, (bar, val) in enumerate(zip(bars2, embedding)):
    ax2.text(i, val + (0.06 if val > 0 else -0.06), f'{val:.2f}', 
            ha='center', va='bottom' if val > 0 else 'top', 
            fontsize=9, color='#e2e8f0', fontweight='bold')

non_zero_pct = 100.0
ax2.text(0.98, 0.85, f'Розмір: {embedding_dim}\nНенульових: {embedding_dim} ({non_zero_pct:.0f}%)',
        transform=ax2.transAxes, fontsize=10, color='#e2e8f0',
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#334155', linewidth=1.5))

ax2.tick_params(colors='#e2e8f0', labelsize=9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_color('#334155')
ax2.spines['left'].set_color('#334155')
ax2.grid(axis='y', alpha=0.2, color='#334155', linestyle='--')

plt.suptitle('One-hot vs Embedding: розріджений проти щільного', 
             fontsize=15, color='#e2e8f0', fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/from-one-hot-to-embeddings/01-onehot-vs-embedding.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 01-onehot-vs-embedding.png створено")
