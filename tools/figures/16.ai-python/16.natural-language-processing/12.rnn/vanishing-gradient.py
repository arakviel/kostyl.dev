#!/usr/bin/env python3
"""
Візуалізація проблеми зникнення градієнта в RNN
Показує, як норма градієнта ||∂L/∂h_t|| зменшується з часом
"""
import matplotlib.pyplot as plt
import numpy as np

# Послідовність з 40 кроків
timesteps = np.arange(0, 40)

# Симуляція: градієнт зменшується експоненціально
# ||∂L/∂h_t|| ≈ γ^(T-t), де γ < 1
gamma = 0.85  # типове значення для tanh RNN
T = 39  # останній крок

# Норма градієнта (логарифмічна шкала для наочності)
grad_norm = gamma ** (T - timesteps)

# Додамо трохи шуму для реалізму
np.random.seed(42)
noise = np.random.normal(0, 0.05, len(timesteps))
grad_norm_noisy = grad_norm * (1 + noise)
grad_norm_noisy = np.clip(grad_norm_noisy, 1e-10, None)  # уникаємо від'ємних

fig, ax = plt.subplots(figsize=(12, 6))

# Основний графік
ax.semilogy(timesteps, grad_norm_noisy, 'o-', color='#dc2626', linewidth=2.5, 
            markersize=6, label='Виміряна норма градієнта', alpha=0.9)

# Теоретична лінія
ax.semilogy(timesteps, grad_norm, '--', color='#2563eb', linewidth=2, 
            label=f'Теоретична: $\\gamma^{{(T-t)}}$, $\\gamma={gamma}$', alpha=0.7)

# Зони
ax.axhspan(1e-6, 1e-3, alpha=0.15, color='red', label='Критична зона (≈0)')
ax.axhspan(0.1, 1, alpha=0.15, color='green', label='Нормальна зона')

# Анотації
ax.annotate('Градієнти майже зникли!\n(важко навчатися на ранніх токенах)', 
            xy=(5, grad_norm_noisy[5]), xytext=(12, 1e-5),
            arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2),
            fontsize=11, color='#dc2626', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#fee2e2', alpha=0.95))

ax.annotate('Останні кроки:\nградієнти сильні', 
            xy=(35, grad_norm_noisy[35]), xytext=(27, 0.3),
            arrowprops=dict(arrowstyle='->', color='#059669', lw=2),
            fontsize=11, color='#059669', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#d1fae5', alpha=0.95))

# Налаштування
ax.set_xlabel('Крок часу t (0 = початок послідовності, 39 = кінець)', fontsize=12, fontweight='bold')
ax.set_ylabel('Норма градієнта $||\\partial L / \\partial h_t||$', fontsize=12, fontweight='bold')
ax.set_title('Проблема зникнення градієнта в RNN', fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=10, loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3, which='both', linestyle='--')
ax.set_ylim([1e-8, 2])

# Додаткова інформація
info_text = (
    "Для послідовності з 40 токенів градієнт на початку\n"
    f"майже в {gamma**(-39):.0f}× менший, ніж в кінці!"
)
ax.text(0.98, 0.05, info_text, transform=ax.transAxes, fontsize=10,
        ha='right', va='bottom', style='italic',
        bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef3c7', alpha=0.9))

plt.tight_layout()
plt.savefig('public/images/16.ai-python/16.natural-language-processing/12.rnn/vanishing-gradient.png', dpi=150, bbox_inches='tight')
print("✓ Збережено: public/images/16.ai-python/16.natural-language-processing/12.rnn/vanishing-gradient.png")
