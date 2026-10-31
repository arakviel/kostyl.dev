#!/usr/bin/env python3
"""Embedding як lookup-таблиця: індекс → вектор."""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(12, 8), facecolor='#070b14')
ax.set_facecolor('#070b14')
ax.axis('off')

# Параметри
vocab_size = 8
embedding_dim = 5
np.random.seed(42)
embedding_matrix = np.random.randn(vocab_size, embedding_dim) * 0.5

# Малювання матриці
cell_height = 0.8
cell_width = 1.2
start_x = 2
start_y = 8

# Заголовок
ax.text(start_x + cell_width * embedding_dim / 2, start_y + 1.5, 
        'Embedding Matrix (V × d)', fontsize=14, color='#e2e8f0', 
        fontweight='bold', ha='center')

ax.text(start_x - 1.5, start_y + 0.5, 'Словник\n(індекси)', 
        fontsize=11, color='#64748b', ha='center', va='center', fontweight='bold')

# Матриця
for i in range(vocab_size):
    for j in range(embedding_dim):
        val = embedding_matrix[i, j]
        color = '#0f172a'
        if i == 3:  # Підсвітити рядок 3
            color = '#1e3a5f'
        
        rect = plt.Rectangle((start_x + j * cell_width, start_y - i * cell_height), 
                            cell_width * 0.95, cell_height * 0.95, 
                            facecolor=color, edgecolor='#334155', linewidth=1)
        ax.add_patch(rect)
        
        text_color = '#06b6d4' if i == 3 else '#64748b'
        ax.text(start_x + j * cell_width + cell_width/2, 
               start_y - i * cell_height + cell_height/2,
               f'{val:.2f}', ha='center', va='center', 
               fontsize=9, color=text_color, fontweight='bold' if i == 3 else 'normal')
    
    # Індекс рядка
    idx_color = '#10b981' if i == 3 else '#e2e8f0'
    ax.text(start_x - 0.5, start_y - i * cell_height + cell_height/2, 
           str(i), ha='center', va='center', 
           fontsize=11, color=idx_color, fontweight='bold')

# Стрілка: індекс → рядок
arrow_start_y = start_y + 2.5
ax.annotate('', xy=(start_x - 0.5, start_y - 3 * cell_height + cell_height/2),
           xytext=(start_x - 0.5, arrow_start_y),
           arrowprops=dict(arrowstyle='->', color='#10b981', lw=3))
ax.text(start_x - 0.5, arrow_start_y + 0.3, 'індекс = 3', 
       ha='center', fontsize=12, color='#10b981', fontweight='bold')

# Стрілка: рядок → вектор
vector_y = start_y - 3 * cell_height + cell_height/2
arrow_end_x = start_x + embedding_dim * cell_width + 1.5
ax.annotate('', xy=(arrow_end_x, vector_y),
           xytext=(start_x + embedding_dim * cell_width, vector_y),
           arrowprops=dict(arrowstyle='->', color='#06b6d4', lw=3))

# Вектор справа
vector = embedding_matrix[3]
ax.text(arrow_end_x + 0.5, vector_y + 1, 'Вектор слова 3:', 
       fontsize=11, color='#06b6d4', fontweight='bold')
vector_str = '[' + ', '.join([f'{v:.2f}' for v in vector]) + ']'
ax.text(arrow_end_x + 0.5, vector_y, vector_str, 
       fontsize=10, color='#06b6d4', ha='left', va='center',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#06b6d4', linewidth=2))

# Пояснення
explanation = 'nn.Embedding — це просто lookup-таблиця:\nіндекс слова → рядок матриці → вектор'
ax.text(start_x + cell_width * embedding_dim / 2, start_y - vocab_size * cell_height - 1, 
       explanation, fontsize=11, color='#e2e8f0', ha='center',
       bbox=dict(boxstyle='round,pad=0.7', facecolor='#0f172a', edgecolor='#334155', linewidth=2))

ax.set_xlim(0, 12)
ax.set_ylim(-2, 11)

plt.tight_layout()
plt.savefig('public/images/ai-python/natural-language-processing/from-one-hot-to-embeddings/03-embedding-lookup.png',
            dpi=150, facecolor='#070b14', edgecolor='none')
print("✓ 03-embedding-lookup.png створено")
