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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), dpi=200)
fig.patch.set_facecolor('#ffffff')
ax1.set_facecolor('#ffffff')
ax2.set_facecolor('#ffffff')

e = np.linspace(-3, 3, 300)

# ----------------- Subplot 1: MSE (Парабола, гладке дно) -----------------
mse = e ** 2
ax1.plot(e, mse, color='#2563eb', linewidth=3.2, label=r'$L = e^2$ (MSE)')

# Tangent line at e = 1.8
e_tangent = 1.8
slope = 2 * e_tangent
tan_x = np.linspace(e_tangent - 0.7, e_tangent + 0.7, 50)
tan_y = e_tangent**2 + slope * (tan_x - e_tangent)
ax1.plot(tan_x, tan_y, color='#dc2626', linestyle='--', linewidth=2.0, label=f'Дотична при e={e_tangent} (нахил={slope:.1f})')
ax1.scatter([e_tangent], [e_tangent**2], color='#dc2626', s=70, zorder=5)

# Tangent at minimum e = 0
tan_min_x = np.linspace(-1.0, 1.0, 50)
ax1.plot(tan_min_x, np.zeros_like(tan_min_x), color='#059669', linestyle='--', linewidth=2.2, label='Дотична в мінімумі (нахил = 0)')
ax1.scatter([0], [0], color='#059669', s=90, zorder=5)

# Steps illustration: steps naturally shrink
steps_e = [2.6, 1.8, 1.1, 0.5, 0.1, 0.0]
for i in range(len(steps_e) - 1):
    x1, y1 = steps_e[i], steps_e[i]**2
    x2, y2 = steps_e[i+1], steps_e[i+1]**2
    ax1.annotate('', xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=1.8, mutation_scale=12))

ax1.set_title('MSE: плавна парабола (гладке дно)', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('Похибка моделі e = y - ŷ', fontsize=11, labelpad=8)
ax1.set_ylabel('Значення функції втрат L', fontsize=11, labelpad=8)
ax1.set_xlim(-3.2, 3.2)
ax1.set_ylim(-0.5, 9.8)
ax1.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
ax1.legend(loc='upper center', fontsize=9.5, framealpha=0.95, facecolor='#f8fafc', edgecolor='#e2e8f0')

# ----------------- Subplot 2: MAE (V-подібна ламана, гострий кут) -----------------
mae = np.abs(e)
ax2.plot(e, mae, color='#d97706', linewidth=3.2, label=r'$L = |e|$ (MAE)')

# Left slope: constant -1
ax2.annotate('Постійний нахил = -1', xy=(-1.5, 1.5), xytext=(-2.6, 2.6),
             arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.4),
             fontsize=10, fontweight='bold', color='#b45309')

# Right slope: constant +1
ax2.annotate('Постійний нахил = +1', xy=(1.5, 1.5), xytext=(0.8, 2.6),
             arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.4),
             fontsize=10, fontweight='bold', color='#b45309')

# Point of non-differentiability at e = 0
ax2.scatter([0], [0], color='#dc2626', s=100, zorder=5, label='Злам (похідної не існує)')

# Oscillations illustration: jumps back and forth across 0
osc_e = [1.2, -0.8, 0.6, -0.4, 0.3]
for i in range(len(osc_e) - 1):
    x1, y1 = osc_e[i], abs(osc_e[i])
    x2, y2 = osc_e[i+1], abs(osc_e[i+1])
    ax2.annotate('', xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.8, mutation_scale=12,
                                 connectionstyle="arc3,rad=-0.18"))

ax2.set_title('MAE: V-подібний кут (гострий злам у нулі)', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel('Похибка моделі e = y - ŷ', fontsize=11, labelpad=8)
ax2.set_ylabel('Значення функції втрат L', fontsize=11, labelpad=8)
ax2.set_xlim(-3.2, 3.2)
ax2.set_ylim(-0.5, 3.5)
ax2.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
ax2.legend(loc='upper center', fontsize=9.5, framealpha=0.95, facecolor='#f8fafc', edgecolor='#e2e8f0')

plt.tight_layout()

out_path = 'public/images/ai-python/linear-regression-theory/gradient-descent/09-mse-vs-mae-loss-shape.png'
plt.savefig(out_path, dpi=200)
print(f"Generated successfully: {out_path}")
