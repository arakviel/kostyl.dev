#!/usr/bin/env python3
"""
Схема Seq2Seq з attention mechanism
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 11)
ax.axis('off')
ax.set_title('Seq2Seq з Attention Mechanism', fontsize=16, fontweight='bold', pad=20)

# Кольори
color_encoder = '#3b82f6'
color_decoder = '#10b981'
color_attention = '#f59e0b'

# ========== ENCODER ==========
encoder_y = 3
encoder_tokens = ["I", "am", "student"]
encoder_x_positions = [1.5, 3, 4.5]

for i, (x, token) in enumerate(zip(encoder_x_positions, encoder_tokens)):
    # Токен
    ax.text(x, encoder_y - 0.7, token, ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#e0f2fe', alpha=0.9))
    
    # LSTM
    box = FancyBboxPatch((x - 0.25, encoder_y), 0.5, 0.7, boxstyle="round,pad=0.06",
                          edgecolor=color_encoder, facecolor='#dbeafe', linewidth=2)
    ax.add_patch(box)
    ax.text(x, encoder_y + 0.35, 'LSTM', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Стрілка вгору (h_i)
    ax.arrow(x, encoder_y + 0.75, 0, 1.8, head_width=0.12, head_length=0.1,
             fc=color_encoder, ec=color_encoder, linewidth=2)
    ax.text(x + 0.35, encoder_y + 1.5, f'$h_{{{i+1}}}$', fontsize=10, color=color_encoder, fontweight='bold')
    
    # Стрілки між LSTM
    if i < len(encoder_x_positions) - 1:
        ax.arrow(x + 0.3, encoder_y + 0.35, 0.9, 0, head_width=0.08, head_length=0.08,
                 fc=color_encoder, ec=color_encoder, linewidth=1.8)

ax.text(3, encoder_y - 1.3, 'ENCODER', ha='center', fontsize=13, fontweight='bold',
        color=color_encoder, bbox=dict(boxstyle='round,pad=0.4', facecolor='#dbeafe', alpha=0.8))

# Горизонтальна лінія h_i (всі виходи encoder доступні)
ax.plot([1, 5.5], [5.5, 5.5], color=color_encoder, linewidth=3, linestyle='--', alpha=0.6)
ax.text(6.2, 5.5, 'Всі $h_i$ доступні decoder!', va='center', fontsize=10,
        fontweight='bold', color=color_encoder, style='italic')

# ========== ATTENTION LAYER ==========
attention_y = 7
attention_x_positions = [8, 10, 12]

for step_idx, x in enumerate(attention_x_positions):
    # Attention механізм (кружок)
    circle = Circle((x, attention_y), 0.35, edgecolor=color_attention,
                    facecolor='#fef3c7', linewidth=2.5)
    ax.add_patch(circle)
    ax.text(x, attention_y, 'Attn', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Стрілки від encoder h_i до attention
    for enc_x in encoder_x_positions:
        # Показуємо лише кілька стрілок для наочності
        if step_idx == 0:
            alpha_val = 0.3
        else:
            alpha_val = 0.15
        
        ax.plot([enc_x, x], [5.5, attention_y - 0.4], color=color_attention,
                linewidth=1.5, alpha=alpha_val, linestyle=':')
    
    # Context vector c_t
    ax.arrow(x, attention_y - 0.4, 0, -0.6, head_width=0.12, head_length=0.08,
             fc=color_attention, ec=color_attention, linewidth=2)
    ax.text(x + 0.5, attention_y - 0.7, f'$c_{{{step_idx}}}$', fontsize=10,
            color=color_attention, fontweight='bold')

# ========== DECODER ==========
decoder_y = 5
decoder_tokens = ["<SOS>", "Я", "студент"]
decoder_out = ["Я", "студент", "<EOS>"]

for i, x in enumerate(attention_x_positions):
    # Вхідний токен
    ax.text(x, decoder_y - 0.7, decoder_tokens[i], ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#d1fae5', alpha=0.9))
    
    # LSTM
    box = FancyBboxPatch((x - 0.3, decoder_y), 0.6, 0.7, boxstyle="round,pad=0.06",
                          edgecolor=color_decoder, facecolor='#dcfce7', linewidth=2)
    ax.add_patch(box)
    ax.text(x, decoder_y + 0.35, 'LSTM', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # s_t до attention
    ax.arrow(x, decoder_y + 0.75, 0, 0.8, head_width=0.12, head_length=0.08,
             fc=color_decoder, ec=color_decoder, linewidth=2)
    ax.text(x - 0.45, decoder_y + 1.1, f'$s_{{{i}}}$', fontsize=10, color=color_decoder, fontweight='bold')
    
    # Комбінування c_t + s_t
    combine_y = 8.5
    ax.arrow(x, attention_y + 0.4, 0, 0.6, head_width=0.12, head_length=0.08,
             fc='black', ec='black', linewidth=1.5, linestyle='--')
    
    # Вихід
    ax.arrow(x, combine_y + 0.3, 0, 0.5, head_width=0.12, head_length=0.08,
             fc=color_decoder, ec=color_decoder, linewidth=2)
    ax.text(x, combine_y + 1.1, decoder_out[i], ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#d1fae5', alpha=0.9))
    
    # Стрілки між decoder кроками
    if i < len(attention_x_positions) - 1:
        ax.arrow(x + 0.35, decoder_y + 0.35, 1.15, 0, head_width=0.08, head_length=0.08,
                 fc=color_decoder, ec=color_decoder, linewidth=1.8)

ax.text(10, decoder_y - 1.3, 'DECODER', ha='center', fontsize=13, fontweight='bold',
        color=color_decoder, bbox=dict(boxstyle='round,pad=0.4', facecolor='#dcfce7', alpha=0.8))

# Легенда
legend_y = 10
ax.text(1, legend_y, 'На кожному кроці t:', fontsize=11, fontweight='bold')
ax.text(1, legend_y - 0.5, '1. Attention обчислює $c_t$ як зважену суму всіх $h_i$', fontsize=10)
ax.text(1, legend_y - 1, '2. Decoder використовує $c_t$ та $s_t$ для генерації $y_t$', fontsize=10)

# Формула attention
formula = r'$c_t = \sum_{i=1}^{n} \alpha_{t,i} \cdot h_i$'
ax.text(7, 0.7, formula, ha='center', fontsize=13, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef3c7', alpha=0.95))

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/14.seq2seq-attention/attention-architecture.png',
            dpi=150, bbox_inches='tight')
print("✓ Збережено: attention-architecture.png")
