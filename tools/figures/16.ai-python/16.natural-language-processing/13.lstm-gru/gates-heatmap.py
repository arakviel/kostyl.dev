#!/usr/bin/env python3
"""
Візуалізація активації вентилів LSTM (forget, input, output) для речення
"""
import matplotlib.pyplot as plt
import numpy as np

# Симулюємо активації вентилів для речення "The movie was not good"
np.random.seed(42)

tokens = ["The", "movie", "was", "not", "good"]
seq_len = len(tokens)
hidden_dim = 8  # показуємо лише 8 нейронів для наочності

# Forget gate: на "not" частково закривається (забути попередню позитивну інформацію)
forget_gates = np.random.rand(seq_len, hidden_dim) * 0.7 + 0.2
forget_gates[3, :] *= 0.4  # "not" — зменшуємо активацію

# Input gate: на "not" і "good" відкривається (додати важливу інформацію)
input_gates = np.random.rand(seq_len, hidden_dim) * 0.5 + 0.3
input_gates[3, :] *= 1.5  # "not"
input_gates[4, :] *= 1.4  # "good"
input_gates = np.clip(input_gates, 0, 1)

# Output gate: контролює вихід
output_gates = np.random.rand(seq_len, hidden_dim) * 0.6 + 0.3

# Візуалізація
fig, axes = plt.subplots(3, 1, figsize=(10, 9))

gates = [
    (forget_gates, "Forget Gate $f_t$", '#ef4444'),
    (input_gates, "Input Gate $i_t$", '#3b82f6'),
    (output_gates, "Output Gate $o_t$", '#8b5cf6')
]

for idx, (gate, name, color) in enumerate(gates):
    ax = axes[idx]
    im = ax.imshow(gate.T, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto', interpolation='nearest')
    
    ax.set_yticks(range(hidden_dim))
    ax.set_yticklabels([f'$h_{{{i}}}$' for i in range(hidden_dim)], fontsize=10)
    ax.set_xticks(range(seq_len))
    ax.set_xticklabels(tokens, fontsize=12, fontweight='bold')
    ax.set_title(name, fontweight='bold', fontsize=13, pad=10, color=color)
    ax.set_xlabel('Токен', fontsize=11, fontweight='bold')
    ax.set_ylabel('Нейрон', fontsize=11, fontweight='bold')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label('Активація', fontsize=10, fontweight='bold')
    cbar.set_ticks([0, 0.5, 1])
    cbar.set_ticklabels(['0\n(закрито)', '0.5\n(частково)', '1\n(відкрито)'], fontsize=9)
    
    # Додамо рамки навколо важливих клітинок
    if idx == 0:  # Forget gate
        # "not" має низьку активацію
        for h in range(hidden_dim):
            ax.add_patch(plt.Rectangle((2.5, h-0.5), 1, 1, fill=False, 
                                      edgecolor='red', linewidth=2.5))
    elif idx == 1:  # Input gate
        # "not" і "good" мають високу активацію
        for h in range(hidden_dim):
            ax.add_patch(plt.Rectangle((2.5, h-0.5), 1, 1, fill=False, 
                                      edgecolor='blue', linewidth=2.5))
            ax.add_patch(plt.Rectangle((3.5, h-0.5), 1, 1, fill=False, 
                                      edgecolor='blue', linewidth=2.5))

# Загальна інтерпретація
interpretation = (
    "Інтерпретація (умовна, для демонстрації):\n"
    "• Forget Gate: На токені 'not' частково закривається (темний) — забути попередню позитивну інформацію\n"
    "• Input Gate: На 'not' і 'good' відкривається (світлий) — додати нову важливу інформацію про негативний відгук\n"
    "• Output Gate: Контролює, що з cell state потрапляє в hidden state h_t"
)

fig.text(0.5, 0.01, interpretation, ha='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef3c7', alpha=0.95),
         verticalalignment='bottom')

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig('public/images/16.ai-python/16.natural-language-processing/13.lstm-gru/gates-heatmap.png', 
            dpi=150, bbox_inches='tight')
print("✓ Збережено: gates-heatmap.png")
