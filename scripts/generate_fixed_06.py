import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['text.color'] = '#0f172a'
plt.rcParams['axes.labelcolor'] = '#1e293b'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

out_path = "public/images/ai-python/neural-networks-basics/perceptron-to-mlp/06.png"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.2), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax1.set_facecolor('#ffffff')
ax2.set_facecolor('#ffffff')

# -------------------------------------------------------------
# Subplot 1: Input Space (x1, x2)
# -------------------------------------------------------------
ax1.scatter([0, 1], [0, 1], color='#ef4444', s=190, edgecolors='#0f172a', linewidths=2.0, zorder=6, label='Клас 0: (0,0), (1,1)')
ax1.scatter([0, 1], [1, 0], color='#3b82f6', s=190, edgecolors='#0f172a', linewidths=2.0, zorder=6, label='Клас 1: (0,1), (1,0)')

# Two separating lines from hidden neurons
x_vals = np.linspace(-0.35, 1.35, 200)
line_or = 0.5 - x_vals
line_and = 1.5 - x_vals

ax1.plot(x_vals, line_or, color='#d97706', linewidth=2.5, linestyle='--', label=r'Межа $h_1$ (OR): $x_1 + x_2 = 0.5$')
ax1.plot(x_vals, line_and, color='#7c3aed', linewidth=2.5, linestyle='--', label=r'Межа $h_2$ (AND): $x_1 + x_2 = 1.5$')

# Fill corridor between lines
ax1.fill_between(x_vals, line_or, line_and, color='#eff6ff', alpha=0.6, zorder=1)
ax1.fill_between(x_vals, -0.6, line_or, color='#fef2f2', alpha=0.4, zorder=1)
ax1.fill_between(x_vals, line_and, 1.8, color='#fef2f2', alpha=0.4, zorder=1)

ax1.annotate(r"Область активації $h_1$ (OR)" + "\n" + r"$x_1 + x_2 \geq 0.5$", xy=(0.2, 0.3), xytext=(-0.25, 0.65),
             fontsize=9.5, fontweight='bold', color='#b45309',
             arrowprops=dict(arrowstyle="->", color='#b45309', lw=1.5))

ax1.annotate(r"Область активації $h_2$ (AND)" + "\n" + r"$x_1 + x_2 \geq 1.5$", xy=(0.8, 0.7), xytext=(0.35, 1.15),
             fontsize=9.5, fontweight='bold', color='#6d28d9',
             arrowprops=dict(arrowstyle="->", color='#6d28d9', lw=1.5))

ax1.text(0.5, 0.5, "Смуга XOR\n(OR = 1, AND = 0)", fontsize=10, fontweight='bold', color='#1d4ed8',
         ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#93c5fd", alpha=0.9))

# Point labels in Subplot 1
ax1.text(-0.06, -0.08, "(0,0)", fontsize=10, fontweight='bold', color='#dc2626', ha='right')
ax1.text(1.06, 1.08, "(1,1)", fontsize=10, fontweight='bold', color='#dc2626', ha='left')
ax1.text(-0.06, 1.08, "(0,1)", fontsize=10, fontweight='bold', color='#1d4ed8', ha='right')
ax1.text(1.06, -0.08, "(1,0)", fontsize=10, fontweight='bold', color='#1d4ed8', ha='left')

ax1.set_title("1. Вхідний простір $(x_1, x_2)$\nКласи лінійно НЕРОЗДІЛЬНІ (потрібні 2 лінії)", fontsize=12, fontweight='bold', pad=14)
ax1.set_xlabel(r"Вхід $x_1$", fontsize=11, fontweight='bold')
ax1.set_ylabel(r"Вхід $x_2$", fontsize=11, fontweight='bold')
ax1.set_xlim(-0.45, 1.35)
ax1.set_ylim(-0.45, 1.4)
ax1.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
ax1.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.0)

# -------------------------------------------------------------
# Subplot 2: Hidden Space (h1, h2)
# -------------------------------------------------------------
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

# Hidden layer transformation with scaling
# W1 = [[6, 6], [6, 6]], b1 = [-3, -9]
pt_00 = (sigmoid(-3.0), sigmoid(-9.0))         # ~ (0.05, 0.00)
pt_01 = (sigmoid(3.0), sigmoid(-3.0))          # ~ (0.95, 0.05)
pt_10 = (sigmoid(3.0), sigmoid(-3.0))          # ~ (0.95, 0.05)
pt_11 = (sigmoid(9.0), sigmoid(3.0))          # ~ (1.00, 0.95)

# Grid for background decision shading in hidden space
h1_grid, h2_grid = np.meshgrid(np.linspace(-0.15, 1.2, 300), np.linspace(-0.25, 1.2, 300))
# Decision formula: z_out = 8*h1 - 16*h2 - 4
z_out_grid = 8.0 * h1_grid - 16.0 * h2_grid - 4.0

ax2.contourf(h1_grid, h2_grid, z_out_grid, levels=[-100, 0, 100], colors=['#fef2f2', '#eff6ff'], alpha=0.6, zorder=1)

# Plot decision boundary line: 8*h1 - 16*h2 - 4 = 0 => h2 = 0.5*h1 - 0.25
h1_line = np.linspace(-0.15, 1.2, 200)
h2_boundary = 0.5 * h1_line - 0.25
ax2.plot(h1_line, h2_boundary, color='#059669', linewidth=2.8, linestyle='-', zorder=4,
         label=r'Роздільна пряма: $8h_1 - 16h_2 - 4 = 0$')

# Scatter points in hidden space
ax2.scatter([pt_00[0]], [pt_00[1]], color='#ef4444', s=200, edgecolors='#0f172a', linewidths=2.0, zorder=6, label='Клас 0: (0,0)')
ax2.scatter([pt_11[0]], [pt_11[1]], color='#ef4444', s=200, edgecolors='#0f172a', linewidths=2.0, zorder=6, label='Клас 0: (1,1)')
ax2.scatter([pt_01[0]], [pt_01[1]], color='#3b82f6', s=220, edgecolors='#0f172a', linewidths=2.0, zorder=6, label='Клас 1: (0,1) та (1,0)')

# Annotate points with coordinates and classification
ax2.annotate(f"(0,0) → ({pt_00[0]:.2f}, {pt_00[1]:.2f})\nКлас 0 (над прямою)",
             pt_00, textcoords="offset points", xytext=(15, 15),
             fontsize=9.5, fontweight='bold', color='#dc2626')

ax2.annotate(f"(1,1) → ({pt_11[0]:.2f}, {pt_11[1]:.2f})\nКлас 0 (над прямою)",
             pt_11, textcoords="offset points", xytext=(-130, -25),
             fontsize=9.5, fontweight='bold', color='#dc2626')

ax2.annotate(f"(0,1) & (1,0) → ({pt_01[0]:.2f}, {pt_01[1]:.2f})\nКлас 1 (під прямою)",
             pt_01, textcoords="offset points", xytext=(12, -45),
             fontsize=9.5, fontweight='bold', color='#1d4ed8', ha='center',
             arrowprops=dict(arrowstyle="->", color='#3b82f6', lw=1.5))

# Clarifying annotations on zones
ax2.text(0.40, 0.72, "Червона зона (Клас 0, ŷ < 0.5)\nОбидві точки (0,0) і (1,1) тут,\nбо над прямою: 8h₁ - 16h₂ - 4 < 0", 
         fontsize=9.5, fontweight='bold', color='#b91c1c',
         ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#fca5a5", alpha=0.95))

ax2.text(0.52, -0.15, "Синя зона (Клас 1, ŷ > 0.5)\nТочки (0,1) і (1,0) тут,\nбо під прямою: 8h₁ - 16h₂ - 4 > 0", 
         fontsize=9.5, fontweight='bold', color='#1d4ed8',
         ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#93c5fd", alpha=0.95))

ax2.set_title("2. Прихований простір $(h_1, h_2)$\nТепер класи ІДЕАЛЬНО РОЗДІЛЕНІ однією прямою!", fontsize=12, fontweight='bold', pad=14)
ax2.set_xlabel(r"Активація нейрона $h_1$ (OR-ознака)", fontsize=11, fontweight='bold')
ax2.set_ylabel(r"Активація нейрона $h_2$ (AND-ознака)", fontsize=11, fontweight='bold')
ax2.set_xlim(-0.08, 1.15)
ax2.set_ylim(-0.22, 1.15)
ax2.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
ax2.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.0)

plt.tight_layout()
plt.savefig(out_path, dpi=300)
plt.close()
print(f"Generated: {out_path}")
