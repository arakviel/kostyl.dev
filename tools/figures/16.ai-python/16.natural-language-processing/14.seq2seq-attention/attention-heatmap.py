#!/usr/bin/env python3
"""
Теплова карта attention weights для машинного перекладу
"""
import matplotlib.pyplot as plt
import numpy as np

# Приклад перекладу: англійська → українська
src_tokens = ["The", "student", "reads", "a", "book", "at", "the", "library"]
trg_tokens = ["Студент", "читає", "книгу", "в", "бібліотеці", "<EOS>"]

# Симулюємо attention weights (реалістичні значення)
# Рядок = токен виходу, стовпець = токен входу
np.random.seed(42)

# Базова матриця (діагональ + шум)
n_trg = len(trg_tokens)
n_src = len(src_tokens)
attention = np.random.rand(n_trg, n_src) * 0.05

# "Студент" → "student" (позиція 1)
attention[0, 1] = 0.8
attention[0, 0] = 0.15  # трохи "The"

# "читає" → "reads" (позиція 2)
attention[1, 2] = 0.75
attention[1, 1] = 0.15
attention[1, 3] = 0.05

# "книгу" → "book" (позиція 4)
attention[2, 4] = 0.7
attention[2, 3] = 0.2  # "a"

# "в" → "at" (позиція 5)
attention[3, 5] = 0.65
attention[3, 6] = 0.25  # "the"

# "бібліотеці" → "library" (позиція 7)
attention[4, 7] = 0.75
attention[4, 6] = 0.15

# "<EOS>" дивиться на кінець
attention[5, 7] = 0.6
attention[5, 6] = 0.2
attention[5, 4] = 0.1

# Нормалізуємо кожен рядок до 1
attention = attention / attention.sum(axis=1, keepdims=True)

# Візуалізація
fig, ax = plt.subplots(figsize=(12, 8))
im = ax.imshow(attention, cmap='YlOrRd', vmin=0, vmax=1, aspect='auto')

# Налаштування осей
ax.set_xticks(range(n_src))
ax.set_xticklabels(src_tokens, fontsize=12, fontweight='bold', rotation=0)
ax.set_yticks(range(n_trg))
ax.set_yticklabels(trg_tokens, fontsize=12, fontweight='bold')

ax.set_xlabel('Source (English)', fontsize=13, fontweight='bold', labelpad=10)
ax.set_ylabel('Target (Ukrainian)', fontsize=13, fontweight='bold', labelpad=10)
ax.set_title('Attention Weights: English → Ukrainian Translation\n(Теплова карта: на що модель "дивиться" під час генерації)',
             fontsize=14, fontweight='bold', pad=15)

# Додаємо значення в клітинки (лише для значних weights)
for i in range(n_trg):
    for j in range(n_src):
        if attention[i, j] > 0.15:  # Показуємо лише значущі ваги
            text_color = 'white' if attention[i, j] > 0.5 else 'black'
            ax.text(j, i, f'{attention[i, j]:.2f}',
                   ha="center", va="center", color=text_color,
                   fontsize=10, fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax, pad=0.02)
cbar.set_label('Attention Weight α', fontsize=12, fontweight='bold', rotation=270, labelpad=20)
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
cbar.set_ticklabels(['0\n(не дивиться)', '0.25', '0.5', '0.75', '1.0\n(фокус)'], fontsize=10)

# Додаємо рамки навколо найсильніших зв'язків
for i in range(n_trg):
    j_max = np.argmax(attention[i])
    if attention[i, j_max] > 0.6:
        ax.add_patch(plt.Rectangle((j_max - 0.5, i - 0.5), 1, 1,
                                   fill=False, edgecolor='blue', linewidth=3))

# Примітка
note = (
    "Інтерпретація: Коли decoder генерує 'Студент', він фокусується на 'student' (α=0.80).\n"
    "Діагональний паттерн показує правильне вирівнювання між мовами."
)
fig.text(0.5, 0.02, note, ha='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef3c7', alpha=0.95))

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig('public/images/16.ai-python/16.natural-language-processing/14.seq2seq-attention/attention-heatmap.png',
            dpi=150, bbox_inches='tight')
print("✓ Збережено: attention-heatmap.png")
