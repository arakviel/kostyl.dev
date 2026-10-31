#!/usr/bin/env python3
"""
Порівняння RNN, LSTM і GRU на IMDB: accuracy і кількість параметрів
"""
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 11)

# Симуляція реалістичних результатів для IMDB
# RNN
rnn_train_acc = 60 + 32 * (1 - np.exp(-0.3 * epochs))
rnn_val_acc = 58 + 30 * (1 - np.exp(-0.28 * epochs))

# LSTM (краща точність, повільніша збіжність)
lstm_train_acc = 62 + 35 * (1 - np.exp(-0.28 * epochs))
lstm_val_acc = 60 + 32 * (1 - np.exp(-0.26 * epochs))

# GRU (між RNN і LSTM)
gru_train_acc = 61 + 34 * (1 - np.exp(-0.29 * epochs))
gru_val_acc = 59 + 31 * (1 - np.exp(-0.27 * epochs))

# Графік accuracy
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ========== ACCURACY ==========
ax = axes[0]
ax.plot(epochs, rnn_train_acc, 'o-', color='#ef4444', linewidth=2.5, markersize=7, 
        label='RNN (train)', alpha=0.9)
ax.plot(epochs, rnn_val_acc, 's--', color='#ef4444', linewidth=2, markersize=6, 
        label='RNN (val)', alpha=0.7)

ax.plot(epochs, lstm_train_acc, 'o-', color='#3b82f6', linewidth=2.5, markersize=7, 
        label='LSTM (train)', alpha=0.9)
ax.plot(epochs, lstm_val_acc, 's--', color='#3b82f6', linewidth=2, markersize=6, 
        label='LSTM (val)', alpha=0.7)

ax.plot(epochs, gru_train_acc, 'o-', color='#8b5cf6', linewidth=2.5, markersize=7, 
        label='GRU (train)', alpha=0.9)
ax.plot(epochs, gru_val_acc, 's--', color='#8b5cf6', linewidth=2, markersize=6, 
        label='GRU (val)', alpha=0.7)

# Фінальні значення
ax.axhline(y=87.6, color='#ef4444', linestyle=':', alpha=0.5, linewidth=2)
ax.text(0.5, 88.3, '87.6%', fontsize=10, color='#ef4444', fontweight='bold')

ax.axhline(y=89.8, color='#3b82f6', linestyle=':', alpha=0.5, linewidth=2)
ax.text(0.5, 90.5, '89.8%', fontsize=10, color='#3b82f6', fontweight='bold')

ax.axhline(y=89.5, color='#8b5cf6', linestyle=':', alpha=0.5, linewidth=2)
ax.text(0.5, 90.2, '89.5%', fontsize=10, color='#8b5cf6', fontweight='bold')

ax.set_xlabel('Епоха', fontsize=12, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax.set_title('Accuracy на IMDB', fontsize=13, fontweight='bold', pad=15)
ax.legend(fontsize=9, framealpha=0.95, loc='lower right', ncol=2)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim([55, 98])

# Анотації
ax.annotate('LSTM: найкраща точність', 
            xy=(9, lstm_val_acc[-2]), xytext=(5, 75),
            arrowprops=dict(arrowstyle='->', color='#3b82f6', lw=1.5),
            fontsize=10, color='#3b82f6', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#dbeafe', alpha=0.9))

# ========== ПАРАМЕТРИ ТА ЧАС ==========
ax = axes[1]

models = ['RNN', 'LSTM', 'GRU']
params = [1.2, 3.8, 2.9]  # млн параметрів
times = [45, 72, 58]  # секунди на епоху

x_pos = np.arange(len(models))
width = 0.35

bars1 = ax.bar(x_pos - width/2, params, width, label='Параметри (M)', 
               color=['#ef4444', '#3b82f6', '#8b5cf6'], alpha=0.7)
ax2 = ax.twinx()
bars2 = ax2.bar(x_pos + width/2, times, width, label='Час епоха (сек)', 
                color=['#fca5a5', '#93c5fd', '#c4b5fd'], alpha=0.7)

# Підписи значень
for i, (p, t) in enumerate(zip(params, times)):
    ax.text(i - width/2, p + 0.1, f'{p}M', ha='center', fontsize=10, fontweight='bold')
    ax2.text(i + width/2, t + 1, f'{t}с', ha='center', fontsize=10, fontweight='bold')

ax.set_ylabel('Параметри (млн)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Час на епоху (сек, GPU)', fontsize=11, fontweight='bold')
ax.set_xlabel('Модель', fontsize=12, fontweight='bold')
ax.set_title('Ресурси: Параметри та Швидкість', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x_pos)
ax.set_xticklabels(models, fontsize=11, fontweight='bold')
ax.set_ylim([0, 5])
ax2.set_ylim([0, 90])

# Легенда
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10, framealpha=0.95)

ax.grid(True, alpha=0.3, axis='y', linestyle='--')

# Примітка
note = (
    "LSTM має найкращу accuracy (+2.2% проти RNN),\n"
    "але потребує ×3 більше параметрів і працює повільніше.\n"
    "GRU — компроміс між точністю та швидкістю."
)
fig.text(0.5, 0.02, note, ha='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef3c7', alpha=0.95))

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig('public/images/16.ai-python/16.natural-language-processing/13.lstm-gru/comparison-accuracy.png', 
            dpi=150, bbox_inches='tight')
print("✓ Збережено: comparison-accuracy.png")
