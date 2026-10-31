#!/usr/bin/env python3
"""
Порівняння потоку градієнтів: RNN vs LSTM
Показує, як LSTM зберігає градієнти на довгих послідовностях
"""
import matplotlib.pyplot as plt
import numpy as np

timesteps = np.arange(0, 50)

# RNN: експоненціальне зникнення
gamma_rnn = 0.82
T = 49
grad_norm_rnn = gamma_rnn ** (T - timesteps)

# Додамо шум
np.random.seed(42)
noise_rnn = np.random.normal(0, 0.05, len(timesteps))
grad_norm_rnn_noisy = grad_norm_rnn * (1 + noise_rnn)
grad_norm_rnn_noisy = np.clip(grad_norm_rnn_noisy, 1e-12, None)

# LSTM: градієнти зберігаються набагато краще
# Симуляція: невелике затухання, але не експоненціальне
grad_norm_lstm = np.ones(len(timesteps)) * 0.5  # базовий рівень
# Додамо трохи затухання в ранніх кроках
for i in range(len(timesteps)):
    decay = max(0.3, 1 - (T - i) * 0.008)  # повільне затухання
    grad_norm_lstm[i] = grad_norm_lstm[i] * decay

noise_lstm = np.random.normal(0, 0.08, len(timesteps))
grad_norm_lstm_noisy = grad_norm_lstm * (1 + noise_lstm)
grad_norm_lstm_noisy = np.clip(grad_norm_lstm_noisy, 0.05, 1)

# Візуалізація
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ========== RNN ==========
ax = axes[0]
ax.semilogy(timesteps, grad_norm_rnn_noisy, 'o-', color='#ef4444', 
            linewidth=2.5, markersize=5, alpha=0.9, label='RNN')
ax.semilogy(timesteps, grad_norm_rnn, '--', color='#991b1b', 
            linewidth=2, alpha=0.6, label=f'Теоретична: $\\gamma^{{(T-t)}}$')

ax.axhspan(1e-8, 1e-4, alpha=0.15, color='red', label='Критична зона')
ax.axhspan(0.1, 1, alpha=0.15, color='green', label='Нормальна зона')

ax.annotate('Градієнти майже зникли\nна початку послідовності', 
            xy=(5, grad_norm_rnn_noisy[5]), xytext=(15, 1e-6),
            arrowprops=dict(arrowstyle='->', color='#ef4444', lw=2),
            fontsize=10, color='#ef4444', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', alpha=0.95))

ax.set_xlabel('Крок часу t', fontsize=12, fontweight='bold')
ax.set_ylabel('Норма градієнта $||\\partial L / \\partial h_t||$', fontsize=11, fontweight='bold')
ax.set_title('RNN: Експоненціальне зникнення', fontsize=13, fontweight='bold', color='#ef4444')
ax.legend(fontsize=9, loc='upper left')
ax.grid(True, alpha=0.3, which='both', linestyle='--')
ax.set_ylim([1e-10, 2])

# ========== LSTM ==========
ax = axes[1]
ax.plot(timesteps, grad_norm_lstm_noisy, 'o-', color='#3b82f6', 
        linewidth=2.5, markersize=5, alpha=0.9, label='LSTM')
ax.plot(timesteps, grad_norm_lstm, '--', color='#1e40af', 
        linewidth=2, alpha=0.6, label='Середнє значення')

ax.axhspan(0.2, 0.8, alpha=0.15, color='green', label='Стабільна зона')

ax.annotate('Градієнти зберігаються!\nНавчання працює на всіх кроках', 
            xy=(5, grad_norm_lstm_noisy[5]), xytext=(15, 0.15),
            arrowprops=dict(arrowstyle='->', color='#3b82f6', lw=2),
            fontsize=10, color='#3b82f6', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#dbeafe', alpha=0.95))

ax.set_xlabel('Крок часу t', fontsize=12, fontweight='bold')
ax.set_ylabel('Норма градієнта $||\\partial L / \\partial h_t||$', fontsize=11, fontweight='bold')
ax.set_title('LSTM: Стабільний потік градієнтів', fontsize=13, fontweight='bold', color='#3b82f6')
ax.legend(fontsize=9, loc='upper left')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim([0, 1])

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/13.lstm-gru/gradient-flow.png', 
            dpi=150, bbox_inches='tight')
print("✓ Збережено: gradient-flow.png")
