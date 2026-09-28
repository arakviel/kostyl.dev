import matplotlib.pyplot as plt
import numpy as np

# Styling configuration matching project aesthetics
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#1e293b'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)
fig.patch.set_facecolor('#ffffff')
ax1.set_facecolor('#ffffff')
ax2.set_facecolor('#ffffff')

x = np.linspace(0, 10, 100)

# Subplot 1: Impact of weight w (with fixed b = 5)
ax1.plot(x, 0.5 * x + 5, color='#2a9d8f', linewidth=2.8, label='w = 0.5 (пологий)')
ax1.plot(x, 1.0 * x + 5, color='#2b7bc6', linewidth=2.8, label='w = 1.0 (помірний)')
ax1.plot(x, 2.0 * x + 5, color='#e76f51', linewidth=2.8, label='w = 2.0 (крутий)')

ax1.set_title('Вплив ваги w (при фіксованому b = 5)', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('X (площа квартири, м²)', fontsize=11, labelpad=8)
ax1.set_ylabel('Y (ціна, тис. $)', fontsize=11, labelpad=8)
ax1.set_xlim(-0.3, 10.5)
ax1.set_ylim(4, 25.5)
ax1.set_xticks(np.arange(0, 11, 2))
ax1.set_yticks(np.arange(5, 26, 2.5))
ax1.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
ax1.legend(loc='upper left', fontsize=10, framealpha=0.9, facecolor='#f8fafc', edgecolor='#e2e8f0')

# Subplot 2: Impact of bias b (with fixed w = 1.0)
ax2.plot(x, 1.0 * x + 0, color='#334155', linewidth=2.8, label='b = 0')
ax2.plot(x, 1.0 * x + 5, color='#2b7bc6', linewidth=2.8, label='b = 5')
ax2.plot(x, 1.0 * x + 10, color='#7c3aed', linewidth=2.8, label='b = 10')

ax2.set_title('Вплив зсуву b (при фіксованому w = 1.0)', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel('X (площа квартири, м²)', fontsize=11, labelpad=8)
ax2.set_ylabel('Y (ціна, тис. $)', fontsize=11, labelpad=8)
ax2.set_xlim(-0.3, 10.5)
ax2.set_ylim(-0.5, 20.5)
ax2.set_xticks(np.arange(0, 11, 2))
ax2.set_yticks(np.arange(0, 21, 2.5))
ax2.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
ax2.legend(loc='upper left', fontsize=10, framealpha=0.9, facecolor='#f8fafc', edgecolor='#e2e8f0')

plt.tight_layout()

out_path = 'public/images/ai-python/linear-regression-theory/regression-task/06-weights-bias-impact.png'
plt.savefig(out_path, dpi=200, bbox_inches='tight')
print(f"Generated successfully: {out_path}")
