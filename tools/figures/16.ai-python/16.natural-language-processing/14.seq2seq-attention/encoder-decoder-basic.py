#!/usr/bin/env python3
"""
Базова схема Encoder-Decoder архітектури (без attention)
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Encoder-Decoder Architecture (базова, без attention)', fontsize=16, fontweight='bold', pad=20)

# Кольори
color_encoder = '#3b82f6'
color_decoder = '#10b981'
color_context = '#f59e0b'

# ========== ENCODER ==========
encoder_y = 3
encoder_tokens = ["I", "am", "student"]
encoder_x_positions = [1.5, 2.5, 3.5]

# Вхідні токени
for i, (x, token) in enumerate(zip(encoder_x_positions, encoder_tokens)):
    ax.text(x, encoder_y - 0.7, token, ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#e0f2fe', alpha=0.9))

# LSTM блоки encoder
for i, x in enumerate(encoder_x_positions):
    box = FancyBboxPatch((x - 0.3, encoder_y), 0.6, 0.8, boxstyle="round,pad=0.08",
                          edgecolor=color_encoder, facecolor='#dbeafe', linewidth=2.5)
    ax.add_patch(box)
    ax.text(x, encoder_y + 0.4, 'LSTM', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Стрілка від токена до LSTM
    ax.arrow(x, encoder_y - 0.3, 0, 0.2, head_width=0.1, head_length=0.08,
             fc='gray', ec='gray', linewidth=1.5)
    
    # Стрілки між LSTM (h_t)
    if i < len(encoder_x_positions) - 1:
        ax.arrow(x + 0.35, encoder_y + 0.4, 0.6, 0, head_width=0.1, head_length=0.1,
                 fc=color_encoder, ec=color_encoder, linewidth=2.5)
        ax.text(x + 0.65, encoder_y + 0.7, f'$h_{{{i+1}}}$', fontsize=10, color=color_encoder, fontweight='bold')

ax.text(2.5, encoder_y - 1.3, 'ENCODER', ha='center', fontsize=14, fontweight='bold',
        color=color_encoder, bbox=dict(boxstyle='round,pad=0.5', facecolor='#dbeafe', alpha=0.8))

# ========== CONTEXT VECTOR ==========
context_x = 5.5
context_y = encoder_y + 0.4

# Стрілка від останнього h_n до context
ax.arrow(encoder_x_positions[-1] + 0.35, encoder_y + 0.4, 1.3, 0,
         head_width=0.15, head_length=0.15, fc=color_context, ec=color_context, linewidth=3)

# Context вектор
context_box = FancyBboxPatch((context_x - 0.4, context_y - 0.35), 0.8, 0.7,
                             boxstyle="round,pad=0.1", edgecolor=color_context,
                             facecolor='#fef3c7', linewidth=3)
ax.add_patch(context_box)
ax.text(context_x, context_y, '$c$', ha='center', va='center', fontsize=16, fontweight='bold', color=color_context)

ax.text(context_x, context_y + 1, 'Context\nVector', ha='center', fontsize=10, fontweight='bold',
        color=color_context, style='italic')

# Примітка про bottleneck
ax.text(context_x, context_y - 1.2, 'Вся інформація про вхід\nстиснута в один вектор!',
        ha='center', fontsize=9, style='italic', color='#dc2626',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fee2e2', alpha=0.9))

# ========== DECODER ==========
decoder_y = 7
decoder_tokens = ["<SOS>", "Я", "студент"]
decoder_out = ["Я", "студент", "<EOS>"]
decoder_x_positions = [8, 9.5, 11]

# Стрілка від context до decoder (початковий стан)
ax.arrow(context_x, context_y + 0.4, 1.8, 2.6, head_width=0.15, head_length=0.15,
         fc=color_context, ec=color_context, linewidth=3, linestyle='--')
ax.text(6.5, 5.5, '$s_0 = c$', fontsize=11, fontweight='bold', color=color_context)

# LSTM блоки decoder
for i, x in enumerate(decoder_x_positions):
    # Вхідний токен
    ax.text(x, decoder_y - 0.7, decoder_tokens[i], ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#d1fae5', alpha=0.9))
    
    # LSTM
    box = FancyBboxPatch((x - 0.35, decoder_y), 0.7, 0.8, boxstyle="round,pad=0.08",
                          edgecolor=color_decoder, facecolor='#dcfce7', linewidth=2.5)
    ax.add_patch(box)
    ax.text(x, decoder_y + 0.4, 'LSTM', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Стрілка від токена до LSTM
    ax.arrow(x, decoder_y - 0.3, 0, 0.2, head_width=0.1, head_length=0.08,
             fc='gray', ec='gray', linewidth=1.5)
    
    # Вихідний токен
    ax.arrow(x, decoder_y + 0.85, 0, 0.5, head_width=0.1, head_length=0.08,
             fc=color_decoder, ec=color_decoder, linewidth=2)
    ax.text(x, decoder_y + 1.6, decoder_out[i], ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#d1fae5', alpha=0.9))
    
    # Стрілки між LSTM (s_t)
    if i < len(decoder_x_positions) - 1:
        ax.arrow(x + 0.4, decoder_y + 0.4, 0.85, 0, head_width=0.1, head_length=0.1,
                 fc=color_decoder, ec=color_decoder, linewidth=2.5)
        ax.text(x + 0.82, decoder_y + 0.7, f'$s_{{{i+1}}}$', fontsize=10, color=color_decoder, fontweight='bold')

ax.text(9.5, decoder_y - 1.3, 'DECODER', ha='center', fontsize=14, fontweight='bold',
        color=color_decoder, bbox=dict(boxstyle='round,pad=0.5', facecolor='#dcfce7', alpha=0.8))

# Примітка про teacher forcing
ax.text(9.5, decoder_y + 2.5, 'Teacher forcing: на вхід подаємо справжні токени',
        ha='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fef3c7', alpha=0.9))

# Загальна примітка
note = "Encoder обробляє вхід → Context vector c → Decoder генерує вихід крок за кроком"
ax.text(7, 0.5, note, ha='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#f3f4f6', alpha=0.95))

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/14.seq2seq-attention/encoder-decoder-basic.png',
            dpi=150, bbox_inches='tight')
print("✓ Збережено: encoder-decoder-basic.png")
