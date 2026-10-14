"""
Script for generating 300 DPI high-resolution figures for Neural Networks Basics:
Perceptron to Multi-Layer Perceptron (16.ai-python/12.neural-networks-basics/01.perceptron-to-mlp.md).

Output directory:
public/images/ai-python/neural-networks-basics/perceptron-to-mlp/

Figures:
01.png: Linear Decision Boundaries for Perceptron (OR & AND gates)
02.png: XOR Non-linear Separability Problem
03.png: Feature Space Transformation by MLP (Input space -> Hidden space)
04.png: Activation Functions Comparison (Sigmoid, Tanh, ReLU, Leaky ReLU)
05.png: Activation Function Derivatives & Vanishing Gradient Dynamics
06.png: Forward Pass Tensor Dimension & Matrix Multiplication Pipeline
07.png: Backpropagation Computational Graph & Chain Rule Gradient Flow
08.png: Optimizer Trajectories on Loss Surface (Batch GD, SGD, Momentum, Adam)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configure global aesthetics
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['text.color'] = '#0f172a'
plt.rcParams['axes.labelcolor'] = '#1e293b'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

out_dir = "public/images/ai-python/neural-networks-basics/perceptron-to-mlp"
os.makedirs(out_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 01.png: Linear Decision Boundaries for Perceptron (OR & AND gates)
# -----------------------------------------------------------------------------
def make_fig_01():
    out_path = os.path.join(out_dir, "01.png")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # Grid for contour background
    xx, yy = np.meshgrid(np.linspace(-0.3, 1.3, 200), np.linspace(-0.3, 1.3, 200))

    # --- Subplot 1: OR Gate (w1=1, w2=1, b=-0.5) ---
    z_or = 1.0 * xx + 1.0 * yy - 0.5
    ax1.contourf(xx, yy, z_or >= 0, levels=[-0.5, 0.5, 1.5], colors=['#fee2e2', '#dbeafe'], alpha=0.55)
    ax1.contour(xx, yy, z_or, levels=[0], colors=['#2563eb'], linewidths=2.5, linestyles='--')

    # Points for OR
    or_pts = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    or_labels = np.array([0, 1, 1, 1])
    
    # Class 0 (0,0)
    ax1.scatter([0], [0], color='#ef4444', s=160, edgecolors='#1e293b', linewidths=1.8, zorder=5, label='Клас 0: (0,0) → 0')
    # Class 1 (0,1), (1,0), (1,1)
    ax1.scatter([0, 1, 1], [1, 0, 1], color='#3b82f6', s=160, edgecolors='#1e293b', linewidths=1.8, zorder=5, label='Клас 1: (0,1), (1,0), (1,1) → 1')

    # Boundary annotation
    ax1.annotate(r'Межа розділення: $x_1 + x_2 - 0.5 = 0$', xy=(0.6, -0.1), xytext=(0.2, -0.22),
                 fontsize=10, fontweight='bold', color='#1d4ed8',
                 arrowprops=dict(arrowstyle="->", color='#1d4ed8', lw=1.5),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#f8fafc", ec="#93c5fd", lw=1))

    ax1.set_title("1. Персептрон для логічного OR (АБО)\n" + r"$z = 1.0 \cdot x_1 + 1.0 \cdot x_2 - 0.5$", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel(r"Вхід $x_1$", fontsize=11, fontweight='bold')
    ax1.set_ylabel(r"Вхід $x_2$", fontsize=11, fontweight='bold')
    ax1.set_xlim(-0.3, 1.3)
    ax1.set_ylim(-0.3, 1.3)
    ax1.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax1.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    # --- Subplot 2: AND Gate (w1=1, w2=1, b=-1.5) ---
    z_and = 1.0 * xx + 1.0 * yy - 1.5
    ax2.contourf(xx, yy, z_and >= 0, levels=[-0.5, 0.5, 1.5], colors=['#fee2e2', '#dbeafe'], alpha=0.55)
    ax2.contour(xx, yy, z_and, levels=[0], colors=['#059669'], linewidths=2.5, linestyles='--')

    # Points for AND
    ax2.scatter([0, 0, 1], [0, 1, 0], color='#ef4444', s=160, edgecolors='#1e293b', linewidths=1.8, zorder=5, label='Клас 0: (0,0), (0,1), (1,0) → 0')
    ax2.scatter([1], [1], color='#3b82f6', s=160, edgecolors='#1e293b', linewidths=1.8, zorder=5, label='Клас 1: (1,1) → 1')

    # Boundary annotation
    ax2.annotate(r'Межа розділення: $x_1 + x_2 - 1.5 = 0$', xy=(0.8, 0.7), xytext=(0.1, 0.95),
                 fontsize=10, fontweight='bold', color='#047857',
                 arrowprops=dict(arrowstyle="->", color='#047857', lw=1.5),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#f8fafc", ec="#6ee7b7", lw=1))

    ax2.set_title("2. Персептрон для логічного AND (І)\n" + r"$z = 1.0 \cdot x_1 + 1.0 \cdot x_2 - 1.5$", fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel(r"Вхід $x_1$", fontsize=11, fontweight='bold')
    ax2.set_ylabel(r"Вхід $x_2$", fontsize=11, fontweight='bold')
    ax2.set_xlim(-0.3, 1.3)
    ax2.set_ylim(-0.3, 1.3)
    ax2.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax2.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 02.png: XOR Non-linear Separability Problem
# -----------------------------------------------------------------------------
def make_fig_02():
    out_path = os.path.join(out_dir, "02.png")
    fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Points for XOR
    # Class 0: (0,0) and (1,1)
    ax.scatter([0, 1], [0, 1], color='#ef4444', s=200, edgecolors='#0f172a', linewidths=2.0, zorder=5, label='Клас 0: однакові входи (0,0), (1,1)')
    # Class 1: (0,1) and (1,0)
    ax.scatter([0, 1], [1, 0], color='#3b82f6', s=200, edgecolors='#0f172a', linewidths=2.0, zorder=5, label='Клас 1: різні входи (0,1), (1,0)')

    # Labels near points
    labels = {
        (0, 0): "(0, 0)\ny = 0",
        (1, 1): "(1, 1)\ny = 0",
        (0, 1): "(0, 1)\ny = 1",
        (1, 0): "(1, 0)\ny = 1"
    }
    for (x, y), txt in labels.items():
        offset_y = 12 if y == 0 else -25
        offset_x = 12 if x == 0 else -40
        ax.annotate(txt, (x, y), textcoords="offset points", xytext=(offset_x, offset_y),
                    fontsize=10, fontweight='bold', color='#1e293b',
                    bbox=dict(boxstyle="round,pad=0.25", fc="#f1f5f9", ec="#cbd5e1", lw=0.8))

    # Candidate decision lines that all FAIL
    x_vals = np.linspace(-0.3, 1.3, 100)
    ax.plot(x_vals, 0.5 - 0.5 * x_vals, color='#dc2626', linestyle='--', linewidth=1.8, alpha=0.7, label='Спроба прямої 1 (помилка на (0,1))')
    ax.plot(x_vals, 1.2 - x_vals, color='#d97706', linestyle=':', linewidth=2.0, alpha=0.8, label='Спроба прямої 2 (помилка на (1,1))')
    ax.plot(x_vals, 0.4 + 0.4 * x_vals, color='#7c3aed', linestyle='-.', linewidth=1.8, alpha=0.7, label='Спроба прямої 3 (помилка на (1,0))')

    # Shaded curve or zone showing non-linear separation is needed
    theta = np.linspace(0, 2*np.pi, 200)
    r = 0.55
    cx, cy = 0.5, 0.5
    # Draw an ellipse/curve indicating non-linear boundary
    ax.plot(cx + r*np.cos(theta), cy + 0.35*np.sin(theta), color='#059669', linewidth=2.5, label='Необхідна крива (нелінійна межа)')

    ax.annotate("Жодна пряма лінія не здатна\nвідокремити червоні точки від синіх!",
                xy=(0.5, 0.5), xytext=(0.1, 0.82),
                fontsize=10.5, fontweight='bold', color='#b91c1c',
                arrowprops=dict(arrowstyle="->", color='#b91c1c', lw=1.5),
                bbox=dict(boxstyle="round,pad=0.4", fc="#fef2f2", ec="#f87171", lw=1.2))

    ax.set_title("Проблема XOR (Виключне АБО): фундаментальна межа лінійності\nОдношаровий персептрон математично нездатний провести нелінійну криву", fontsize=12, fontweight='bold', pad=14)
    ax.set_xlabel(r"Вхід $x_1$", fontsize=11, fontweight='bold')
    ax.set_ylabel(r"Вхід $x_2$", fontsize=11, fontweight='bold')
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(-0.35, 1.35)
    ax.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 03.png: Feature Space Transformation by MLP (Input space -> Hidden space)
# -----------------------------------------------------------------------------
def make_fig_03():
    out_path = os.path.join(out_dir, "03.png")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # Subplot 1: Input space (x1, x2)
    ax1.scatter([0, 1], [0, 1], color='#ef4444', s=160, edgecolors='#0f172a', linewidths=1.8, zorder=5, label='Клас 0: (0,0), (1,1)')
    ax1.scatter([0, 1], [1, 0], color='#3b82f6', s=160, edgecolors='#0f172a', linewidths=1.8, zorder=5, label='Клас 1: (0,1), (1,0)')

    # Draw the two separating hyperplanes from hidden neurons h1 and h2
    # h1 (OR): x1 + x2 = 0.5
    x_line = np.linspace(-0.2, 1.2, 100)
    ax1.plot(x_line, 0.5 - x_line, color='#d97706', linewidth=2.2, linestyle='--', label=r'Межа $h_1$ (OR-подібна): $x_1 + x_2 = 0.5$')
    # h2 (AND): x1 + x2 = 1.5
    ax1.plot(x_line, 1.5 - x_line, color='#7c3aed', linewidth=2.2, linestyle='--', label=r'Межа $h_2$ (AND-подібна): $x_1 + x_2 = 1.5$')

    ax1.annotate("Область активації $h_1$\n(x1 + x2 ≥ 0.5)", xy=(0.2, 0.3), xytext=(-0.15, 0.55),
                 fontsize=9, fontweight='bold', color='#b45309',
                 arrowprops=dict(arrowstyle="->", color='#b45309', lw=1.2))
    ax1.annotate("Область активації $h_2$\n(x1 + x2 ≥ 1.5)", xy=(0.8, 0.7), xytext=(0.45, 0.95),
                 fontsize=9, fontweight='bold', color='#6d28d9',
                 arrowprops=dict(arrowstyle="->", color='#6d28d9', lw=1.2))

    ax1.set_title("1. Вхідний простір $(x_1, x_2)$\nКласи лінійно НЕРОЗДІЛЬНІ (потрібні 2 лінії)", fontsize=11.5, fontweight='bold', pad=12)
    ax1.set_xlabel(r"Вхід $x_1$", fontsize=10.5, fontweight='bold')
    ax1.set_ylabel(r"Вхід $x_2$", fontsize=10.5, fontweight='bold')
    ax1.set_xlim(-0.25, 1.25)
    ax1.set_ylim(-0.25, 1.25)
    ax1.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax1.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    # Subplot 2: Hidden space (h1, h2) after sigmoid transformation
    sigmoid = lambda z: 1.0 / (1.0 + np.exp(-z))
    # W1 = [[1, 1], [1, 1]], b1 = [-0.5, -1.5]
    # For (0,0): z1 = -0.5 -> h1=0.378; z2 = -1.5 -> h2=0.182
    # For (0,1): z1 = 0.5 -> h1=0.622; z2 = -0.5 -> h2=0.378
    # For (1,0): z1 = 0.5 -> h1=0.622; z2 = -0.5 -> h2=0.378
    # For (1,1): z1 = 1.5 -> h1=0.818; z2 = 0.5 -> h2=0.622
    h_coords = {
        '(0,0) Клас 0': (sigmoid(-0.5), sigmoid(-1.5)),
        '(1,1) Клас 0': (sigmoid(1.5), sigmoid(0.5)),
        '(0,1)/(1,0) Клас 1': (sigmoid(0.5), sigmoid(-0.5))
    }

    # Plot points in hidden space
    ax2.scatter([h_coords['(0,0) Клас 0'][0]], [h_coords['(0,0) Клас 0'][1]], color='#ef4444', s=160, edgecolors='#0f172a', linewidths=1.8, zorder=5, label='Клас 0: (0,0)')
    ax2.scatter([h_coords['(1,1) Клас 0'][0]], [h_coords['(1,1) Клас 0'][1]], color='#ef4444', s=160, edgecolors='#0f172a', linewidths=1.8, zorder=5, label='Клас 0: (1,1)')
    ax2.scatter([h_coords['(0,1)/(1,0) Клас 1'][0]], [h_coords['(0,1)/(1,0) Клас 1'][1]], color='#3b82f6', s=180, edgecolors='#0f172a', linewidths=1.8, zorder=5, label='Клас 1: (0,1) та (1,0) злилися!')

    # Single linear decision boundary from output neuron: y = h1 - 2*h2 = 0 => h2 = 0.5 * h1
    h1_vals = np.linspace(0.2, 0.95, 100)
    h2_bound = 0.5 * h1_vals
    ax2.plot(h1_vals, h2_bound, color='#059669', linewidth=2.5, linestyle='-', label=r'Межа вихідного шару: $h_1 - 2h_2 = 0$')

    # Annotate points
    ax2.annotate(f"(0,0)\n({h_coords['(0,0) Клас 0'][0]:.2f}, {h_coords['(0,0) Клас 0'][1]:.2f})",
                 h_coords['(0,0) Клас 0'], textcoords="offset points", xytext=(12, -15),
                 fontsize=9, fontweight='bold', color='#dc2626')
    ax2.annotate(f"(1,1)\n({h_coords['(1,1) Клас 0'][0]:.2f}, {h_coords['(1,1) Клас 0'][1]:.2f})",
                 h_coords['(1,1) Клас 0'], textcoords="offset points", xytext=(-45, 10),
                 fontsize=9, fontweight='bold', color='#dc2626')
    ax2.annotate(f"(0,1) & (1,0)\n({h_coords['(0,1)/(1,0) Клас 1'][0]:.2f}, {h_coords['(0,1)/(1,0) Клас 1'][1]:.2f})",
                 h_coords['(0,1)/(1,0) Клас 1'], textcoords="offset points", xytext=(15, 10),
                 fontsize=9, fontweight='bold', color='#2563eb')

    ax2.set_title("2. Прихований простір $(h_1, h_2)$\nТепер точки ЛІНІЙНО РОЗДІЛЬНІ однією прямою!", fontsize=11.5, fontweight='bold', pad=12)
    ax2.set_xlabel(r"Активація нейрона $h_1$ (OR-фіча)", fontsize=10.5, fontweight='bold')
    ax2.set_ylabel(r"Активація нейрона $h_2$ (AND-фіча)", fontsize=10.5, fontweight='bold')
    ax2.set_xlim(0.25, 0.95)
    ax2.set_ylim(0.1, 0.75)
    ax2.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax2.legend(loc='lower right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 04.png: Activation Functions Comparison (Sigmoid, Tanh, ReLU, Leaky ReLU)
# -----------------------------------------------------------------------------
def make_fig_04():
    out_path = os.path.join(out_dir, "04.png")
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    z = np.linspace(-5, 5, 400)

    # 1. Sigmoid
    ax = axes[0, 0]
    ax.set_facecolor('#ffffff')
    sig = 1.0 / (1.0 + np.exp(-z))
    ax.plot(z, sig, color='#2563eb', linewidth=2.5, label=r'$\sigma(z) = \frac{1}{1 + e^{-z}}$')
    ax.axhline(0, color='#94a3b8', linestyle=':', linewidth=1)
    ax.axhline(1, color='#94a3b8', linestyle=':', linewidth=1)
    ax.axvline(0, color='#cbd5e1', linestyle='--', linewidth=1)
    ax.scatter([0], [0.5], color='#dc2626', s=60, zorder=5)
    ax.annotate("(0, 0.5)", (0, 0.5), textcoords="offset points", xytext=(10, -5), fontsize=9, fontweight='bold', color='#dc2626')
    ax.set_title("Sigmoid (Логістична)", fontsize=11.5, fontweight='bold')
    ax.set_ylabel("Вихід $\sigma(z)$", fontsize=10)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    # 2. Tanh
    ax = axes[0, 1]
    ax.set_facecolor('#ffffff')
    tanh_v = np.tanh(z)
    ax.plot(z, tanh_v, color='#059669', linewidth=2.5, label=r'$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$')
    ax.axhline(0, color='#94a3b8', linestyle=':', linewidth=1)
    ax.axhline(-1, color='#94a3b8', linestyle=':', linewidth=1)
    ax.axhline(1, color='#94a3b8', linestyle=':', linewidth=1)
    ax.axvline(0, color='#cbd5e1', linestyle='--', linewidth=1)
    ax.scatter([0], [0], color='#dc2626', s=60, zorder=5)
    ax.annotate("(0, 0) Центрована навколо 0", (0, 0), textcoords="offset points", xytext=(10, -15), fontsize=9, fontweight='bold', color='#dc2626')
    ax.set_title("Tanh (Гіперболічний тангенс)", fontsize=11.5, fontweight='bold')
    ax.set_ylabel("Вихід $\\tanh(z)$", fontsize=10)
    ax.set_ylim(-1.2, 1.2)
    ax.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    # 3. ReLU
    ax = axes[1, 0]
    ax.set_facecolor('#ffffff')
    relu_v = np.maximum(0, z)
    ax.plot(z, relu_v, color='#d97706', linewidth=2.5, label=r'$\text{ReLU}(z) = \max(0, z)$')
    ax.axhline(0, color='#94a3b8', linestyle=':', linewidth=1)
    ax.axvline(0, color='#cbd5e1', linestyle='--', linewidth=1)
    ax.annotate("«Мертва зона» (z < 0)\nВихід = 0, градієнт = 0", xy=(-2.5, 0), xytext=(-4.5, 1.8),
                fontsize=9, fontweight='bold', color='#b45309',
                arrowprops=dict(arrowstyle="->", color='#b45309', lw=1.2),
                bbox=dict(boxstyle="round,pad=0.25", fc="#fffbeb", ec="#fcd34d", lw=0.8))
    ax.set_title("ReLU (Rectified Linear Unit)", fontsize=11.5, fontweight='bold')
    ax.set_xlabel("Зважена сума $z$", fontsize=10)
    ax.set_ylabel("Вихід $\\text{ReLU}(z)$", fontsize=10)
    ax.set_ylim(-0.5, 5.2)
    ax.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    # 4. Leaky ReLU
    ax = axes[1, 1]
    ax.set_facecolor('#ffffff')
    alpha = 0.1  # slightly exaggerated for visual clarity
    leaky_v = np.where(z > 0, z, alpha * z)
    ax.plot(z, leaky_v, color='#7c3aed', linewidth=2.5, label=r'$\text{Leaky ReLU}(z) = \max(\alpha z, z), \alpha=0.1$')
    ax.axhline(0, color='#94a3b8', linestyle=':', linewidth=1)
    ax.axvline(0, color='#cbd5e1', linestyle='--', linewidth=1)
    ax.annotate("Малий нахил $\\alpha=0.1$\nЗапобігає «смерті» нейронів", xy=(-3.0, -0.3), xytext=(-4.5, 1.8),
                fontsize=9, fontweight='bold', color='#6d28d9',
                arrowprops=dict(arrowstyle="->", color='#6d28d9', lw=1.2),
                bbox=dict(boxstyle="round,pad=0.25", fc="#f5f3ff", ec="#c4b5fd", lw=0.8))
    ax.set_title("Leaky ReLU", fontsize=11.5, fontweight='bold')
    ax.set_xlabel("Зважена сума $z$", fontsize=10)
    ax.set_ylabel("Вихід $\\text{Leaky ReLU}(z)$", fontsize=10)
    ax.set_ylim(-0.8, 5.2)
    ax.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 05.png: Activation Function Derivatives & Vanishing Gradient Dynamics
# -----------------------------------------------------------------------------
def make_fig_05():
    out_path = os.path.join(out_dir, "05.png")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    z = np.linspace(-6, 6, 400)

    # Derivatives
    # Sigmoid derivative: s * (1 - s)
    sig = 1.0 / (1.0 + np.exp(-z))
    d_sig = sig * (1.0 - sig)
    # Tanh derivative: 1 - tanh^2
    d_tanh = 1.0 - np.tanh(z)**2
    # ReLU derivative: 1 if z > 0 else 0
    d_relu = np.where(z > 0, 1.0, 0.0)

    ax1.plot(z, d_sig, color='#2563eb', linewidth=2.5, label=r"Sigmoid: $\sigma'(z) \leq 0.25$")
    ax1.plot(z, d_tanh, color='#059669', linewidth=2.2, label=r"Tanh: $\tanh'(z) \leq 1.0$")
    ax1.plot(z, d_relu, color='#d97706', linewidth=2.2, linestyle='--', label=r"ReLU: $\text{ReLU}'(z) = 1$ при $z > 0$")

    ax1.scatter([0], [0.25], color='#2563eb', s=70, zorder=5)
    ax1.annotate(r"Максимум $\sigma'(0) = 0.25$", (0, 0.25), textcoords="offset points", xytext=(-50, 15),
                 fontsize=9.5, fontweight='bold', color='#1d4ed8',
                 arrowprops=dict(arrowstyle="->", color='#1d4ed8', lw=1.2))

    ax1.scatter([0], [1.0], color='#059669', s=70, zorder=5)
    ax1.annotate(r"Максимум $\tanh'(0) = 1.0$", (0, 1.0), textcoords="offset points", xytext=(-60, -22),
                 fontsize=9.5, fontweight='bold', color='#047857',
                 arrowprops=dict(arrowstyle="->", color='#047857', lw=1.2))

    ax1.set_title("1. Похідні функцій активації $\sigma'(z)$\nСигмоїда стискає градієнт щонайменше в 4 рази на кожному шарі!", fontsize=11.5, fontweight='bold', pad=12)
    ax1.set_xlabel("Зважена сума $z$", fontsize=10.5, fontweight='bold')
    ax1.set_ylabel("Значення похідної", fontsize=10.5, fontweight='bold')
    ax1.set_ylim(-0.05, 1.15)
    ax1.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax1.legend(loc='upper right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    # Subplot 2: Vanishing gradient across layers L = 1 to 10
    layers = np.arange(1, 11)
    grad_sigmoid = 0.25 ** layers
    grad_tanh = 0.7 ** layers  # typical average tanh derivative in non-saturated zone
    grad_relu = 1.0 ** layers

    ax2.plot(layers, grad_sigmoid, 'o-', color='#2563eb', linewidth=2.2, markersize=6, label=r'Sigmoid $(\times 0.25^L)$ — миттєве зникнення')
    ax2.plot(layers, grad_tanh, 's-', color='#059669', linewidth=2.0, markersize=6, label=r'Tanh $(\approx 0.7^L)$ — помірне згасання')
    ax2.plot(layers, grad_relu, '^-', color='#d97706', linewidth=2.2, markersize=6, label=r'ReLU $(\times 1.0^L)$ — градієнт зберігається!')

    ax2.annotate(r"Шар 10: градієнт $\approx 10^{-6}$" + "\nВаги не навчаються!",
                 (10, grad_sigmoid[-1]), textcoords="offset points", xytext=(-110, 25),
                 fontsize=9.5, fontweight='bold', color='#dc2626',
                 arrowprops=dict(arrowstyle="->", color='#dc2626', lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fef2f2", ec="#fca5a5", lw=1))

    ax2.set_yscale('log')
    ax2.set_title("2. Проблема зникаючого градієнта (Vanishing Gradient)\nЗгасання величини сигналу помилки при проходженні 10 шарів", fontsize=11.5, fontweight='bold', pad=12)
    ax2.set_xlabel("Кількість шарів мережі ($L$)", fontsize=10.5, fontweight='bold')
    ax2.set_ylabel("Масштаб градієнта (логарифмічна шкала)", fontsize=10.5, fontweight='bold')
    ax2.set_xticks(layers)
    ax2.grid(True, linestyle='--', alpha=0.35, color='#cbd5e1')
    ax2.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 06.png: Forward Pass Tensor Dimension & Matrix Multiplication Pipeline
# -----------------------------------------------------------------------------
def make_fig_06():
    out_path = os.path.join(out_dir, "06.png")
    fig, ax = plt.subplots(figsize=(14, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.axis('off')

    # Draw diagram blocks for network 3 -> 4 -> 2 -> 1
    blocks = [
        {"name": "Вхідні дані\nx", "shape": "(3, 1)", "color": "#dbeafe", "border": "#3b82f6", "x": 0.05, "w": 0.12},
        {"name": "Шар 1 (Linear)\nW₁·x + b₁", "shape": "W₁: (4, 3)\nb₁: (4, 1)", "color": "#fef3c7", "border": "#f59e0b", "x": 0.24, "w": 0.16},
        {"name": "Активація 1\na₁ = ReLU(z₁)", "shape": "a₁: (4, 1)", "color": "#fef9c3", "border": "#eab308", "x": 0.44, "w": 0.13},
        {"name": "Шар 2 (Linear)\nW₂·a₁ + b₂", "shape": "W₂: (2, 4)\nb₂: (2, 1)", "color": "#fce7f3", "border": "#ec4899", "x": 0.61, "w": 0.16},
        {"name": "Вихідний шар\nŷ = σ(z₃)", "shape": "W₃: (1, 2)\nŷ: (1, 1)", "color": "#dcfce7", "border": "#10b981", "x": 0.81, "w": 0.14},
    ]

    for b in blocks:
        # Outer box
        rect = patches.FancyBboxPatch((b["x"], 0.25), b["w"], 0.5,
                                      boxstyle="round,pad=0.03,rounding_size=0.04",
                                      facecolor=b["color"], edgecolor=b["border"], linewidth=2.0)
        ax.add_patch(rect)
        # Text inside
        ax.text(b["x"] + b["w"]/2, 0.58, b["name"], ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="#0f172a")
        # Shape badge
        ax.text(b["x"] + b["w"]/2, 0.38, f"Розмірність:\n{b['shape']}", ha="center", va="center",
                fontsize=9, fontfamily="monospace", fontweight="bold", color="#334155")

    # Connectors / Arrows
    arrows = [
        (0.175, 0.235, "x"),
        (0.405, 0.435, "z₁"),
        (0.575, 0.605, "a₁"),
        (0.775, 0.805, "a₂")
    ]
    for x_start, x_end, lbl in arrows:
        ax.annotate("", xy=(x_end, 0.5), xytext=(x_start, 0.5),
                    arrowprops=dict(arrowstyle="-|>", color="#475569", lw=2.2, mutation_scale=15))
        ax.text((x_start + x_end)/2, 0.54, lbl, ha="center", va="bottom",
                fontsize=9.5, fontfamily="monospace", fontweight="bold", color="#2563eb")

    # Matrix multiplication rule box at the bottom
    rule_rect = patches.FancyBboxPatch((0.15, 0.05), 0.7, 0.14,
                                       boxstyle="round,pad=0.02,rounding_size=0.03",
                                       facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2)
    ax.add_patch(rule_rect)
    ax.text(0.5, 0.12, r"Золоте правило узгодження розмірностей: $(n_{\text{out}} \times n_{\text{in}}) \cdot (n_{\text{in}} \times 1) + (n_{\text{out}} \times 1) = (n_{\text{out}} \times 1)$",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0f172a")

    ax.set_title("Потік обчислень та узгодження розмірностей тензорів (Мережа 3 → 4 → 2 → 1)\nКожен шар перетворює розмірність вхідного вектора за формулою $z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}$",
                 fontsize=12, fontweight="bold", pad=15)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.88)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 07.png: Backpropagation Computational Graph & Chain Rule Gradient Flow
# -----------------------------------------------------------------------------
def make_fig_07():
    out_path = os.path.join(out_dir, "07.png")
    fig, ax = plt.subplots(figsize=(14.5, 6.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.axis('off')

    nodes = [
        {"id": "x", "label": "Вхід\nx", "x": 0.08, "y": 0.58, "color": "#dbeafe", "border": "#3b82f6"},
        {"id": "w", "label": "Вага\nw", "x": 0.08, "y": 0.28, "color": "#fef3c7", "border": "#f59e0b"},
        {"id": "z", "label": "Зважена сума\nz = w·x + b", "x": 0.35, "y": 0.45, "color": "#f1f5f9", "border": "#64748b"},
        {"id": "y_hat", "label": "Активація\nŷ = σ(z)", "x": 0.62, "y": 0.45, "color": "#dcfce7", "border": "#10b981"},
        {"id": "loss", "label": "Втрати\nL(ŷ, y)", "x": 0.88, "y": 0.45, "color": "#fee2e2", "border": "#ef4444"}
    ]

    for n in nodes:
        rect = patches.FancyBboxPatch((n["x"] - 0.06, n["y"] - 0.1), 0.12, 0.2,
                                      boxstyle="round,pad=0.02,rounding_size=0.03",
                                      facecolor=n["color"], edgecolor=n["border"], linewidth=2.0)
        ax.add_patch(rect)
        ax.text(n["x"], n["y"], n["label"], ha="center", va="center",
                fontsize=10, fontweight="bold", color="#0f172a")

    # Forward arrows (Top, Blue)
    fwd_edges = [
        ((0.14, 0.60), (0.29, 0.49), "× w"),
        ((0.14, 0.32), (0.29, 0.41), "+ b"),
        ((0.41, 0.50), (0.56, 0.50), "σ(z)"),
        ((0.68, 0.50), (0.82, 0.50), "MSE/BCE")
    ]
    for start, end, lbl in fwd_edges:
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=2.2, mutation_scale=14))

    ax.text(0.5, 0.72, "ПРЯМИЙ ПРОХІД (FORWARD PASS) ───►\nОбчислення активацій та функції втрат",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#1d4ed8",
            bbox=dict(boxstyle="round,pad=0.3", fc="#eff6ff", ec="#bfdbfe", lw=1))

    # Backward arrows (Bottom, Red)
    bwd_edges = [
        ((0.82, 0.40), (0.68, 0.40), r"$\frac{\partial L}{\partial \hat{y}}$"),
        ((0.56, 0.40), (0.41, 0.40), r"$\frac{\partial L}{\partial z} = \frac{\partial L}{\partial \hat{y}} \cdot \sigma'(z)$"),
        ((0.29, 0.38), (0.14, 0.25), r"$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot x$")
    ]
    for start, end, lbl in bwd_edges:
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="-|>", color="#dc2626", lw=2.2, linestyle="--", mutation_scale=14))
        # Label below arrow
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2 - 0.08
        ax.text(mid_x, mid_y, lbl, ha="center", va="top",
                fontsize=9.5, fontweight="bold", color="#b91c1c",
                bbox=dict(boxstyle="round,pad=0.2", fc="#fff5f5", ec="#fecaca", lw=0.8))

    ax.text(0.5, 0.12, "◄─── ЗВОРОТНИЙ ПРОХІД (BACKPROPAGATION)\nЛанцюгове правило: градієнт ваги є добутком локальних похідних!",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#b91c1c",
            bbox=dict(boxstyle="round,pad=0.3", fc="#fef2f2", ec="#fecaca", lw=1))

    ax.set_title("Граф обчислень (Computational Graph) та ланцюгове правило (Chain Rule)\nВід функції втрат $L$ назад до ваг $w$ через множення часткових похідних",
                 fontsize=12, fontweight="bold", pad=15)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.02, 0.85)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 08.png: Optimizer Trajectories on Loss Surface (Batch GD, SGD, Momentum, Adam)
# -----------------------------------------------------------------------------
def make_fig_08():
    out_path = os.path.join(out_dir, "08.png")
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Anisotropic quadratic loss surface: f(x, y) = 0.08*x^2 + 1.2*y^2 (elongated valley)
    x = np.linspace(-5.5, 5.5, 300)
    y = np.linspace(-2.5, 2.5, 300)
    X, Y = np.meshgrid(x, y)
    Z = 0.08 * X**2 + 1.2 * Y**2

    # Plot loss contours
    levels = np.logspace(-1, 1.8, 18)
    cs = ax.contour(X, Y, Z, levels=levels, cmap='Greys', alpha=0.45, linewidths=1.0)

    # 1. Batch GD (steady but slow perpendicular to contours)
    gd_x = [-4.5]
    gd_y = [2.0]
    lr = 0.15
    for _ in range(25):
        gx = 2 * 0.08 * gd_x[-1]
        gy = 2 * 1.2 * gd_y[-1]
        gd_x.append(gd_x[-1] - lr * gx)
        gd_y.append(gd_y[-1] - lr * gy)
    ax.plot(gd_x, gd_y, 'o-', color='#64748b', linewidth=2.0, markersize=4, label='Batch Gradient Descent (повільна збіжність)')

    # 2. SGD (noisy oscillations across the valley)
    np.random.seed(42)
    sgd_x = [-4.5]
    sgd_y = [2.0]
    for _ in range(30):
        noise_x = np.random.normal(0, 0.4)
        noise_y = np.random.normal(0, 0.6)
        gx = 2 * 0.08 * sgd_x[-1] + noise_x
        gy = 2 * 1.2 * sgd_y[-1] + noise_y
        sgd_x.append(sgd_x[-1] - 0.12 * gx)
        sgd_y.append(sgd_y[-1] - 0.12 * gy)
    ax.plot(sgd_x, sgd_y, 'x--', color='#ef4444', linewidth=1.5, markersize=5, alpha=0.75, label='SGD (високий шум, зигзаги)')

    # 3. Momentum (smooth acceleration along the valley, dampening oscillations)
    mom_x = [-4.5]
    mom_y = [2.0]
    vx, vy = 0.0, 0.0
    beta = 0.75
    lr_mom = 0.14
    for _ in range(25):
        gx = 2 * 0.08 * mom_x[-1]
        gy = 2 * 1.2 * mom_y[-1]
        vx = beta * vx + (1 - beta) * gx
        vy = beta * vy + (1 - beta) * gy
        mom_x.append(mom_x[-1] - lr_mom * vx * 3.5)
        mom_y.append(mom_y[-1] - lr_mom * vy * 3.5)
    ax.plot(mom_x, mom_y, 's-', color='#d97706', linewidth=2.2, markersize=4, label='SGD + Momentum (розгін у долині)')

    # 4. Adam (adaptive per-parameter learning rate, fast direct path)
    adam_x = [-4.5]
    adam_y = [2.0]
    m_x, m_y = 0.0, 0.0
    v_x, v_y = 0.0, 0.0
    b1, b2 = 0.9, 0.999
    lr_adam = 0.35
    for t in range(1, 26):
        gx = 2 * 0.08 * adam_x[-1]
        gy = 2 * 1.2 * adam_y[-1]
        m_x = b1 * m_x + (1 - b1) * gx
        m_y = b1 * m_y + (1 - b1) * gy
        v_x = b2 * v_x + (1 - b2) * (gx**2)
        v_y = b2 * v_y + (1 - b2) * (gy**2)
        m_x_hat = m_x / (1 - b1**t)
        m_y_hat = m_y / (1 - b1**t)
        v_x_hat = v_x / (1 - b2**t)
        v_y_hat = v_y / (1 - b2**t)
        adam_x.append(adam_x[-1] - lr_adam * m_x_hat / (np.sqrt(v_x_hat) + 1e-8))
        adam_y.append(adam_y[-1] - lr_adam * m_y_hat / (np.sqrt(v_y_hat) + 1e-8))
    ax.plot(adam_x, adam_y, '*-', color='#2563eb', linewidth=2.6, markersize=6, label='Adam (адаптивний крок, оптимальна траєкторія)')

    # Starting & Optimum points
    ax.scatter([-4.5], [2.0], color='#0f172a', s=130, zorder=6, label='Старт')
    ax.scatter([0.0], [0.0], color='#10b981', s=200, marker='*', zorder=6, label='Глобальний мінімум (0, 0)')

    ax.annotate("Точка старту\n(-4.5, 2.0)", xy=(-4.5, 2.0), xytext=(-5.3, 1.2),
                fontsize=9.5, fontweight='bold', color='#0f172a',
                arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))

    ax.annotate("Глобальний оптимум\nLoss = 0", xy=(0.0, 0.0), xytext=(0.4, 0.6),
                fontsize=9.5, fontweight='bold', color='#047857',
                arrowprops=dict(arrowstyle="->", color='#047857', lw=1.4),
                bbox=dict(boxstyle="round,pad=0.25", fc="#ecfdf5", ec="#6ee7b7", lw=1))

    ax.set_title("Порівняння оптимізаторів на рельєфі функції втрат (Яружна долина)\nAdam та Momentum значно швидше долають ділянки зі слабкою кривизною", fontsize=12, fontweight='bold', pad=14)
    ax.set_xlabel("Параметр $w_1$ (полога вісь)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Параметр $w_2$ (крута вісь)", fontsize=11, fontweight='bold')
    ax.set_xlim(-5.6, 5.6)
    ax.set_ylim(-2.6, 2.6)
    ax.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    make_fig_01()
    make_fig_02()
    make_fig_03()
    make_fig_04()
    make_fig_05()
    make_fig_06()
    make_fig_07()
    make_fig_08()
    print("All 8 figures successfully generated!")
