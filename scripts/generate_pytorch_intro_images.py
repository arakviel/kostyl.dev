"""
Script for generating 300 DPI high-resolution figures for PyTorch Intro module (13.pytorch-intro).
Files:
- public/images/ai-python/pytorch-intro/tensors-and-autograd/01.png
- public/images/ai-python/pytorch-intro/building-and-training/01.png
- public/images/ai-python/pytorch-intro/data-and-regularization/01.png
- public/images/ai-python/pytorch-intro/advanced-topics/01.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Styling settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#94a3b8'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#1e293b'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

# 1. Tensors and Autograd (01.png)
def make_fig_autograd():
    out_path = "public/images/ai-python/pytorch-intro/tensors-and-autograd/01.png"
    ensure_dir(out_path)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # Subplot 1: Polynomial f(x) and its autograd derivative
    x = np.linspace(-1.0, 3.5, 300)
    f = lambda v: v**3 - 4*v**2 + 6*v - 2
    df = lambda v: 3*v**2 - 8*v + 6
    
    y = f(x)
    dy = df(x)

    ax1.plot(x, y, color='#2563eb', linewidth=2.5, label=r'Функція $f(x) = x^3 - 4x^2 + 6x - 2$')
    ax1.plot(x, dy, color='#059669', linewidth=2, linestyle='--', label=r'Градієнт $f^\prime(x) = 3x^2 - 8x + 6$')
    
    # Highlight points x=0, x=1, x=2
    eval_points = [0.0, 1.0, 2.0]
    point_colors = ['#dc2626', '#d97706', '#7c3aed']
    for pt, col in zip(eval_points, point_colors):
        y_pt = f(pt)
        grad_pt = df(pt)
        ax1.scatter([pt], [y_pt], color=col, s=70, zorder=5)
        # Draw small tangent line
        tan_x = np.linspace(pt - 0.4, pt + 0.4, 20)
        tan_y = y_pt + grad_pt * (tan_x - pt)
        ax1.plot(tan_x, tan_y, color=col, linewidth=1.5, alpha=0.8)
        ax1.annotate(f"x={pt:.0f}, f'(x)={grad_pt:.1f}",
                     (pt, y_pt),
                     textcoords="offset points",
                     xytext=(10, 10 if pt != 2 else -15),
                     fontsize=9,
                     fontweight='bold',
                     color=col,
                     bbox=dict(boxstyle="round,pad=0.3", fc="#f8fafc", ec=col, lw=1))

    ax1.set_title("Автоматичне диференціювання в PyTorch (Autograd)", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Значення x", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Значення f(x) / f'(x)", fontsize=10, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax1.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    # Subplot 2: Gradient Descent Steps
    x_grid = np.linspace(-2.5, 4.5, 300)
    loss_fn = lambda v: (v - 3.0)**2
    ax2.plot(x_grid, loss_fn(x_grid), color='#64748b', linewidth=2, label=r'Функція втрат: $Loss = (x - 3)^2$')

    # Simulate steps
    cur_x = -2.0
    lr = 0.1
    steps_x = [cur_x]
    steps_y = [loss_fn(cur_x)]
    for _ in range(35):
        grad = 2 * (cur_x - 3.0)
        cur_x = cur_x - lr * grad
        steps_x.append(cur_x)
        steps_y.append(loss_fn(cur_x))

    ax2.plot(steps_x, steps_y, 'o-', color='#dc2626', markersize=4, linewidth=1.2, alpha=0.7, label='Кроки градієнтного спуску (lr=0.1)')
    ax2.scatter([steps_x[0]], [steps_y[0]], color='#dc2626', s=100, zorder=6, label=f'Старт ($x_0=-2.0$)')
    ax2.scatter([3.0], [0.0], color='#059669', s=130, marker='*', zorder=6, label=r'Оптимум ($x^*=3.0$, Loss=0)')

    ax2.annotate("Старт: x=-2.0\nLoss=25.0", (-2.0, 25.0),
                 textcoords="offset points", xytext=(-70, -25),
                 fontsize=9, fontweight='bold', color='#dc2626',
                 arrowprops=dict(arrowstyle="->", color='#dc2626', lw=1.2))

    ax2.annotate("Збіжність до мінімуму\nx ≈ 2.95 (Ітерація 40)", (steps_x[20], steps_y[20]),
                 textcoords="offset points", xytext=(20, 20),
                 fontsize=9, fontweight='bold', color='#059669',
                 arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2))

    ax2.set_title("Траєкторія градієнтного спуску (Gradient Descent)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel("Параметр x", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Функція втрат Loss", fontsize=10, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax2.legend(loc='upper right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated:", out_path)

# 2. Building and Training (01.png)
def make_fig_training():
    out_path = "public/images/ai-python/pytorch-intro/building-and-training/01.png"
    ensure_dir(out_path)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    epochs = np.arange(1, 36)
    
    # Train loss steadily drops
    train_loss = 0.52 * np.exp(-epochs / 9.0) + 0.05
    # Val loss drops until epoch 24, then fluctuates slightly upward
    val_loss = 0.48 * np.exp(-epochs / 11.0) + 0.09
    for i in range(24, len(epochs)):
        val_loss[i] = val_loss[23] + 0.0035 * (epochs[i] - 24)**1.3

    best_idx = 23 # epoch 24
    best_epoch = epochs[best_idx]
    best_loss = val_loss[best_idx]
    stop_idx = 26 # epoch 27 (patience=3)
    stop_epoch = epochs[stop_idx]

    # Panel 1: Loss curves + Early stopping
    ax1.plot(epochs[:stop_idx+1], train_loss[:stop_idx+1], color='#2563eb', linewidth=2.5, label='Train Loss (навчання)')
    ax1.plot(epochs[:stop_idx+1], val_loss[:stop_idx+1], color='#f59e0b', linewidth=2.5, label='Validation Loss (валідація)')
    # Show ghost remaining if continued
    ax1.plot(epochs[stop_idx:], train_loss[stop_idx:], color='#93c5fd', linewidth=1.5, linestyle=':')
    ax1.plot(epochs[stop_idx:], val_loss[stop_idx:], color='#fde68a', linewidth=1.5, linestyle=':')

    # Highlight patience window
    ax1.axvspan(best_epoch, stop_epoch, color='#fee2e2', alpha=0.6, label='Patience вікно (3 епохи)')
    ax1.axvline(stop_epoch, color='#dc2626', linestyle='--', linewidth=1.8, label=f'Early Stopping (епоха {stop_epoch})')

    # Best model checkpoint star
    ax1.scatter([best_epoch], [best_loss], color='#059669', s=150, marker='*', zorder=6,
                label=f'Найкращий чекпоінт ({best_loss:.4f})')

    ax1.annotate(f"Збереження best_model.pt\nЕпоха {best_epoch}: Val Loss = {best_loss:.4f}",
                 (best_epoch, best_loss),
                 textcoords="offset points", xytext=(-60, 25),
                 fontsize=9, fontweight='bold', color='#059669',
                 arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec='#059669', lw=1))

    ax1.annotate(f"Зупинка тренування!\nPatience вичерпано (3/3)",
                 (stop_epoch, val_loss[stop_idx]),
                 textcoords="offset points", xytext=(15, 30),
                 fontsize=9, fontweight='bold', color='#dc2626',
                 arrowprops=dict(arrowstyle="->", color='#dc2626', lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fef2f2", ec='#dc2626', lw=1))

    ax1.set_title("Динаміка втрат (Loss) та Early Stopping", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Номер епохи (Epoch)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Функція втрат (CrossEntropy / BCE)", fontsize=10, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax1.legend(loc='upper right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=8.5)

    # Panel 2: Accuracy curves
    train_acc = 75.0 + 24.0 * (1 - np.exp(-epochs / 7.0))
    val_acc = 73.0 + 21.0 * (1 - np.exp(-epochs / 8.5))
    for i in range(24, len(epochs)):
        val_acc[i] = val_acc[23] - 0.25 * (epochs[i] - 24)

    ax2.plot(epochs[:stop_idx+1], train_acc[:stop_idx+1], color='#2563eb', linewidth=2.5, label='Train Accuracy %')
    ax2.plot(epochs[:stop_idx+1], val_acc[:stop_idx+1], color='#10b981', linewidth=2.5, label='Validation Accuracy %')
    ax2.scatter([best_epoch], [val_acc[best_idx]], color='#059669', s=150, marker='*', zorder=6,
                label=f'Пікова точність: {val_acc[best_idx]:.1f}%')

    ax2.axvline(stop_epoch, color='#dc2626', linestyle='--', linewidth=1.8, label=f'Early Stopping')

    ax2.annotate(f"Макс. валідаційна точність: {val_acc[best_idx]:.1f}%\nна епосі {best_epoch}",
                 (best_epoch, val_acc[best_idx]),
                 textcoords="offset points", xytext=(-90, -40),
                 fontsize=9, fontweight='bold', color='#059669',
                 arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec='#059669', lw=1))

    ax2.set_title("Динаміка метрики точності (Accuracy)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel("Номер епохи (Epoch)", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Точність класифікації (%)", fontsize=10, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax2.legend(loc='lower right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated:", out_path)

# 3. Data and Regularization (01.png)
def make_fig_regularization():
    out_path = "public/images/ai-python/pytorch-intro/data-and-regularization/01.png"
    ensure_dir(out_path)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    epochs = np.arange(1, 51)
    
    # 1. Overfitting baseline (from overfitting_demo.ipynb)
    train_loss_overfit = np.array([1.0 - i * 0.019 for i in epochs])
    val_loss_overfit = np.array([1.0 - i * 0.018 if i < 15 else 0.73 + (i - 15) * 0.01 for i in epochs])

    ax1.plot(epochs, train_loss_overfit, color='#2563eb', linewidth=2.5, label='Train Loss (навчання)')
    ax1.plot(epochs, val_loss_overfit, color='#dc2626', linewidth=2.5, label='Val Loss (валідація)')

    # Shading the overfitting gap
    ax1.fill_between(epochs[14:], train_loss_overfit[14:], val_loss_overfit[14:], color='#fee2e2', alpha=0.6,
                     label='Зона перенавчання (Gap)')
    ax1.axvline(15, color='#94a3b8', linestyle='--', linewidth=1.5)
    ax1.annotate("Початок перенавчання\n(епоха 15, Val=0.730)", (15, 0.730),
                 textcoords="offset points", xytext=(15, 20),
                 fontsize=9, fontweight='bold', color='#dc2626',
                 arrowprops=dict(arrowstyle="->", color='#dc2626', lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fef2f2", ec='#dc2626', lw=1))

    ax1.annotate(f"Епоха 50: розрив суттєвий!\nTrain = {train_loss_overfit[-1]:.3f} vs Val = {val_loss_overfit[-1]:.3f}",
                 (50, val_loss_overfit[-1]),
                 textcoords="offset points", xytext=(-180, -25),
                 fontsize=9, fontweight='bold', color='#991b1b',
                 arrowprops=dict(arrowstyle="->", color='#991b1b', lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fff1f2", ec='#991b1b', lw=1))

    ax1.set_title("Без регуляризації: Ефект перенавчання (Overfitting)", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Номер епохи (Epoch)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Функція втрат Loss", fontsize=10, fontweight='bold')
    ax1.set_ylim(-0.05, 1.2)
    ax1.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax1.legend(loc='upper right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    # 2. Regularized (Dropout + Weight Decay)
    train_loss_reg = 0.9 * np.exp(-epochs / 16.0) + 0.15
    val_loss_reg = 0.92 * np.exp(-epochs / 16.5) + 0.18 + 0.01 * np.sin(epochs / 3.0)

    ax2.plot(epochs, train_loss_reg, color='#2563eb', linewidth=2.5, label='Train Loss (Dropout + WD)')
    ax2.plot(epochs, val_loss_reg, color='#059669', linewidth=2.5, label='Val Loss (Dropout + WD)')
    ax2.fill_between(epochs, train_loss_reg, val_loss_reg, color='#ecfdf5', alpha=0.6,
                     label='Стабільне узагальнення')

    ax2.annotate("Стійка збіжність:\nVal Loss не зростає!",
                 (35, val_loss_reg[34]),
                 textcoords="offset points", xytext=(-40, 30),
                 fontsize=9, fontweight='bold', color='#059669',
                 arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec='#059669', lw=1))

    ax2.set_title("З регуляризацією (Dropout p=0.3 + Weight Decay 1e-4)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel("Номер епохи (Epoch)", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Функція втрат Loss", fontsize=10, fontweight='bold')
    ax2.set_ylim(-0.05, 1.2)
    ax2.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax2.legend(loc='upper right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated:", out_path)

# 4. Advanced Topics (01.png)
def make_fig_advanced():
    out_path = "public/images/ai-python/pytorch-intro/advanced-topics/01.png"
    ensure_dir(out_path)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # Panel 1: CPU vs GPU speedup
    sizes = np.array([512, 1024, 2048, 4096])
    cpu_times = np.array([4.2, 32.5, 245.0, 1920.0]) # ms
    gpu_times = np.array([1.2, 2.1, 7.8, 28.5])      # ms

    width = 0.35
    x_indices = np.arange(len(sizes))

    ax1.bar(x_indices - width/2, cpu_times, width, label='CPU (Intel Core / AMD)', color='#64748b')
    ax1.bar(x_indices + width/2, gpu_times, width, label='GPU (CUDA / MPS)', color='#2563eb')

    # Add speedup annotations on top of GPU bars
    for i in range(len(sizes)):
        speedup = cpu_times[i] / gpu_times[i]
        ax1.annotate(f"{speedup:.1f}x швидше",
                     (x_indices[i] + width/2, gpu_times[i]),
                     textcoords="offset points", xytext=(0, 6),
                     ha='center', fontsize=8.5, fontweight='bold', color='#1e40af')

    ax1.set_yscale('log')
    ax1.set_title("Час обчислення множення матриць N x N (CPU vs GPU)", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels([f"{s}x{s}" for s in sizes], fontsize=9)
    ax1.set_xlabel("Розмір квадратної матриці (Matrix Size)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Час виконання (мілісекунди, логарифмічна шкала)", fontsize=10, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1', which='both')
    ax1.legend(loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    # Panel 2: FP32 vs Mixed Precision (FP16 / AMP)
    metrics = ['VRAM Пам\'ять (GB)\n(менше = краще)', 'Швидкість тренування\n(зразків/сек, більше = краще)']
    fp32_vals = [9.4, 320]
    amp_vals = [4.8, 675]

    # Normalize to 100% baseline for visual comparison
    fp32_norm = [100.0, 100.0]
    amp_norm = [(4.8 / 9.4) * 100.0, (675 / 320) * 100.0]

    y_indices = np.arange(len(metrics))
    bar_height = 0.32

    ax2.barh(y_indices + bar_height/2, fp32_norm, bar_height, label='Стандартний FP32 (Full Precision)', color='#94a3b8')
    ax2.barh(y_indices - bar_height/2, amp_norm, bar_height, label='PyTorch AMP (Mixed Precision FP16)', color='#10b981')

    # Annotate absolute values
    ax2.annotate(f"9.4 GB (100%)", (102, y_indices[0] + bar_height/2 - 0.05), fontsize=9, fontweight='bold', color='#475569')
    ax2.annotate(f"4.8 GB (-49% пам'яті)", (amp_norm[0] + 2, y_indices[0] - bar_height/2 - 0.05), fontsize=9, fontweight='bold', color='#047857')

    ax2.annotate(f"320 зр/с (100%)", (102, y_indices[1] + bar_height/2 - 0.05), fontsize=9, fontweight='bold', color='#475569')
    ax2.annotate(f"675 зр/с (+111% прискорення)", (amp_norm[1] + 2, y_indices[1] - bar_height/2 - 0.05), fontsize=9, fontweight='bold', color='#047857')

    ax2.set_yticks(y_indices)
    ax2.set_yticklabels(metrics, fontsize=9.5, fontweight='bold')
    ax2.set_xlim(0, 260)
    ax2.set_title("Переваги Automatic Mixed Precision (AMP)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel("Відносне значення до базового рівня FP32 (%)", fontsize=10, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
    ax2.legend(loc='lower right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated:", out_path)

if __name__ == '__main__':
    make_fig_autograd()
    make_fig_training()
    make_fig_regularization()
    make_fig_advanced()
    print("All 4 diagrams generated successfully.")
