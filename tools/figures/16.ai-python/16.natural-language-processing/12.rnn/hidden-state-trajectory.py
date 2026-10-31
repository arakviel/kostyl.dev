#!/usr/bin/env python3
"""
Візуалізація траєкторії прихованого стану RNN для речень
Показує, як h_t "рухається" в 2D просторі (PCA проєкція)
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

# Симуляція hidden states (128-dim) для двох речень
np.random.seed(42)

# Позитивний відгук: "this movie is amazing and great"
positive_sentence = ["this", "movie", "is", "amazing", "and", "great"]
# Симуляція: hidden states поступово рухаються до "позитивної" зони
hidden_pos = []
for i in range(len(positive_sentence)):
    # Тренд: збільшення по осі 0, позитивний дрейф
    base = np.random.randn(128) * 0.2
    base[0] += (i + 1) * 0.5  # рух вправо
    base[1] += (i + 1) * 0.3 + np.random.randn() * 0.1  # рух вгору
    hidden_pos.append(base)
hidden_pos = np.array(hidden_pos)

# Негативний відгук: "this movie is terrible and boring"
negative_sentence = ["this", "movie", "is", "terrible", "and", "boring"]
# Симуляція: рух до "негативної" зони
hidden_neg = []
for i in range(len(negative_sentence)):
    base = np.random.randn(128) * 0.2
    base[0] += (i + 1) * 0.3  # менший рух вправо
    base[1] -= (i + 1) * 0.4 + np.random.randn() * 0.1  # рух вниз
    hidden_neg.append(base)
hidden_neg = np.array(hidden_neg)

# PCA: проєкція в 2D
all_hidden = np.vstack([hidden_pos, hidden_neg])
pca = PCA(n_components=2)
coords_2d = pca.fit_transform(all_hidden)

pos_coords = coords_2d[:len(positive_sentence)]
neg_coords = coords_2d[len(positive_sentence):]

# Візуалізація
fig, ax = plt.subplots(figsize=(12, 8))

# Позитивна траєкторія
ax.plot(pos_coords[:, 0], pos_coords[:, 1], 'o-', color='#16a34a', 
        linewidth=3, markersize=10, label='Positive: "amazing and great"', alpha=0.9)
for i, word in enumerate(positive_sentence):
    ax.annotate(f'{i}: {word}', (pos_coords[i, 0], pos_coords[i, 1]), 
                fontsize=11, fontweight='bold', color='#16a34a',
                xytext=(8, 8), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#dcfce7', alpha=0.9))

# Негативна траєкторія
ax.plot(neg_coords[:, 0], neg_coords[:, 1], 's-', color='#dc2626', 
        linewidth=3, markersize=10, label='Negative: "terrible and boring"', alpha=0.9)
for i, word in enumerate(negative_sentence):
    ax.annotate(f'{i}: {word}', (neg_coords[i, 0], neg_coords[i, 1]), 
                fontsize=11, fontweight='bold', color='#dc2626',
                xytext=(8, -12), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#fee2e2', alpha=0.9))

# Початкова точка (h_0 = 0)
ax.scatter([0], [0], s=200, c='black', marker='X', zorder=10, label='h₀ (початок)')
ax.text(0.05, -0.15, 'START', fontsize=10, fontweight='bold', ha='left')

# Розділювальна лінія (умовна)
x_line = np.linspace(pos_coords[:, 0].min(), pos_coords[:, 0].max(), 100)
y_line = x_line * 0.1  # приблизна межа
ax.plot(x_line, y_line, '--', color='gray', linewidth=2, alpha=0.5, label='Умовна межа класів')

# Зони
ax.axhspan(0, 3, alpha=0.08, color='green')
ax.axhspan(-3, 0, alpha=0.08, color='red')
ax.text(2.5, 2.2, 'Позитивна зона', fontsize=11, style='italic', color='#16a34a', 
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.7))
ax.text(2.5, -2.2, 'Негативна зона', fontsize=11, style='italic', color='#dc2626',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.7))

# Налаштування
ax.set_xlabel('Головна компонента 1 (PC1)', fontsize=12, fontweight='bold')
ax.set_ylabel('Головна компонента 2 (PC2)', fontsize=12, fontweight='bold')
ax.set_title('Траєкторія прихованого стану RNN в 2D (PCA)', fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=10, loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim([-0.5, 3.5])
ax.set_ylim([-3, 3])

# Примітка
note = (
    "Кожна точка = прихований стан $h_t$ після обробки t-го токена.\n"
    "RNN \"рухається\" від h₀ (початок) до фінального стану, \n"
    "поступово розділяючи позитивні й негативні відгуки."
)
ax.text(0.02, 0.98, note, transform=ax.transAxes, fontsize=10,
        ha='left', va='top', style='italic',
        bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef3c7', alpha=0.95))

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/12.rnn/hidden-state-trajectory.png', dpi=150, bbox_inches='tight')
print("✓ Збережено: public/images/16.ai-python/16.natural-language-processing/12.rnn/hidden-state-trajectory.png")
