import os
import numpy as np
import matplotlib.pyplot as plt

# Aesthetics
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

out_dir = "public/images/ai-python/logistic-regression-classification/classification-basics"
os.makedirs(out_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. 05-weights-impact.png: Вплив ваг (w) на нахил та орієнтацію межі
# -----------------------------------------------------------------------------
def generate_weights_impact():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)

    x = np.linspace(0, 100, 300)
    y = np.linspace(0, 100, 300)
    X, Y = np.meshgrid(x, y)

    # ------------------ Subplot 1: w = [1, 1], b = -100 ------------------
    Z1 = X + Y - 100
    
    # Fill decision regions
    ax1.contourf(X, Y, Z1 >= 0, levels=[-0.5, 0.5, 1.5], colors=['#FEE2E2', '#DCFCE7'], alpha=0.6)
    
    # Decision boundary line
    x1_line = np.linspace(0, 100, 100)
    x2_line1 = -x1_line + 100
    valid1 = (x2_line1 >= 0) & (x2_line1 <= 100)
    ax1.plot(x1_line[valid1], x2_line1[valid1], color='#2563EB', linewidth=3.2,
             label=r'Розділова межа: $x_1 + x_2 = 100$ ($k = -1$)')

    # Normal weight vector w = [1, 1] starting from (50, 50)
    ax1.annotate('', xy=(68, 68), xytext=(50, 50),
                 arrowprops=dict(facecolor='#1E3A8A', edgecolor='#1E3A8A', width=2.5, headwidth=9, headlength=10))
    ax1.text(69, 69, r'$\mathbf{w} = [1, 1]$' + '\n' + r'(вектор ваг $\perp$ межі)',
             fontsize=10.5, fontweight='bold', color='#1E3A8A', va='bottom', ha='left')

    # Illustrative points
    ax1.scatter([40, 70], [70, 40], color='#10B981', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax1.text(42, 72, r'$A(40, 70) \to \hat{y}=1$', fontsize=9.5, fontweight='bold', color='#065F46')
    ax1.text(72, 42, r'$B(70, 40) \to \hat{y}=1$', fontsize=9.5, fontweight='bold', color='#065F46')

    ax1.scatter([30], [40], color='#EF4444', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax1.text(32, 38, r'$C(30, 40) \to \hat{y}=0$', fontsize=9.5, fontweight='bold', color='#991B1B')

    # Region annotations
    ax1.text(75, 85, 'Клас 1: Прийнято\n($x_1 + x_2 > 100$)', fontsize=11, fontweight='bold',
             color='#166534', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#86EFAC', alpha=0.9))
    ax1.text(25, 20, 'Клас 0: Не прийнято\n($x_1 + x_2 < 100$)', fontsize=11, fontweight='bold',
             color='#991B1B', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#FCA5A5', alpha=0.9))

    # Explanation text box
    ax1.text(0.04, 0.05,
             "• Рівноважні ваги: $w_1 = w_2 = 1$\n• Кут нахилу: 45° ($k = -1$)\n• Внесок $x_1$ та $x_2$ однаковий\n• +10 балів за $x_1$ = +10 балів за $x_2$",
             transform=ax1.transAxes, fontsize=10, verticalalignment='bottom',
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.98))

    ax1.set_title('Приклад 1: Рівноважні ваги\n$w = [1, 1], \\quad b = -100$', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax1.set_xlabel('Іспит 1: $x_1$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Іспит 2: $x_2$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax1.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    # ------------------ Subplot 2: w = [3, 1], b = -100 ------------------
    Z2 = 3 * X + Y - 100
    
    # Fill decision regions
    ax2.contourf(X, Y, Z2 >= 0, levels=[-0.5, 0.5, 1.5], colors=['#FEE2E2', '#DCFCE7'], alpha=0.6)

    # Old boundary comparison (ghost line)
    ax2.plot(x1_line[valid1], x2_line1[valid1], color='#94A3B8', linewidth=2.0, linestyle='--',
             label=r'Стара межа ($w = [1, 1]$)')

    # New decision boundary line
    x2_line2 = -3 * x1_line + 100
    valid2 = (x2_line2 >= 0) & (x2_line2 <= 100)
    ax2.plot(x1_line[valid2], x2_line2[valid2], color='#7C3AED', linewidth=3.2,
             label=r'Нова межа: $3x_1 + x_2 = 100$ ($k = -3$)')

    # Normal weight vector w = [3, 1] starting from (25, 25)
    norm_w = np.sqrt(3**2 + 1**2)
    dx = (3 / norm_w) * 22
    dy = (1 / norm_w) * 22
    ax2.annotate('', xy=(25 + dx, 25 + dy), xytext=(25, 25),
                 arrowprops=dict(facecolor='#5B21B6', edgecolor='#5B21B6', width=2.5, headwidth=9, headlength=10))
    ax2.text(25 + dx + 2, 25 + dy, r'$\mathbf{w} = [3, 1]$' + '\n' + r'(повернутий ближче до $x_1$)',
             fontsize=10.5, fontweight='bold', color='#5B21B6', va='center', ha='left')

    # Rotation indicator curved arrow
    ax2.annotate('Поворот межі\nпри $w_1 = 3$', xy=(18, 55), xytext=(35, 75),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.25", color='#7C3AED', lw=2.2),
                 fontsize=10.5, fontweight='bold', color='#7C3AED', ha='center',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F3FF', edgecolor='#DDD6FE', alpha=0.9))

    # Illustrative points
    ax2.scatter([20], [80], color='#10B981', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax2.text(23, 82, r'$D(20, 80) \to \hat{y}=1$' + '\n(завдяки високому $x_1$)', fontsize=9, fontweight='bold', color='#065F46')

    ax2.scatter([15], [45], color='#EF4444', s=100, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax2.text(17, 41, r'$E(15, 45) \to \hat{y}=0$', fontsize=9, fontweight='bold', color='#991B1B')

    # Explanation text box (placed with high opacity so background lines don't bleed through)
    ax2.text(0.48, 0.05,
             "• $x_1$ у 3 рази важливіший за $x_2$\n• Крутіший нахил ($k = -3$)\n• Невеликий ріст $x_1$ різко змінює клас\n• Для компенсації потрібен утричі більший $x_2$",
             transform=ax2.transAxes, fontsize=10, verticalalignment='bottom', zorder=10,
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFFFFF', edgecolor='#CBD5E1', alpha=1.0))

    ax2.set_title('Приклад 2: $x_1$ важливіший за $x_2$\n$w = [3, 1], \\quad b = -100$', fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax2.set_xlabel('Іспит 1: $x_1$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Іспит 2: $x_2$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax2.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    plt.tight_layout()
    path = os.path.join(out_dir, "05-weights-impact.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)


# -----------------------------------------------------------------------------
# 2. 05-bias-impact.png: Вплив зміщення (bias b) на паралельний зсув межі
# -----------------------------------------------------------------------------
def generate_bias_impact():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)

    # ------------------ Subplot 1: 2D площина ознак ------------------
    x1 = np.linspace(0, 140, 200)

    lines_info = [
        (-80, '#10B981', 'b = -80 (м\'який поріг: x1 + x2 ≥ 80)', '--'),
        (-100, '#2563EB', 'b = -100 (базовий поріг: x1 + x2 ≥ 100)', '-'),
        (-120, '#EF4444', 'b = -120 (суворий поріг: x1 + x2 ≥ 120)', '-.')
    ]

    for b_val, col, lbl, style in lines_info:
        x2 = -x1 - b_val
        valid = (x2 >= 0) & (x2 <= 140)
        ax1.plot(x1[valid], x2[valid], color=col, linewidth=3.0, linestyle=style, label=lbl)

    # Shared normal weight vector w = [1, 1] placed in upper right area
    ax1.annotate('', xy=(100, 50), xytext=(85, 35),
                 arrowprops=dict(facecolor='#1E293B', edgecolor='#1E293B', width=2.5, headwidth=9, headlength=10))
    ax1.text(102, 52, r'$\mathbf{w} = [1, 1]$' + '\n' + r'(однаковий вектор для всіх 3-х меж)',
             fontsize=10.0, fontweight='bold', color='#1E293B', va='bottom', ha='left')

    # Parallel shift arrow annotation in lower-left area
    ax1.annotate('', xy=(50, 50), xytext=(26, 26),
                 arrowprops=dict(arrowstyle="<->", color='#475569', lw=2.4))
    ax1.text(20, 36, 'Паралельний зсув\n(кут не змінюється)', fontsize=9.0, fontweight='bold',
             color='#334155', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.95))

    # Student A at (35, 55) -> Sum = 90
    ax1.scatter([35], [55], color='#D97706', s=130, edgecolors='#0F172A', linewidths=1.8, zorder=6)
    ax1.annotate('Студент А (35, 55)\nСума = 90 балів:\n[+] b = -80  => Прийнято\n[-] b = -100 => Відхилено',
                 xy=(35, 55), xytext=(12, 85),
                 arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.8),
                 fontsize=9.0, fontweight='bold', color='#B45309',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#FEF3C7', edgecolor='#FCD34D', alpha=0.95))

    # Student B at (70, 40) -> Sum = 110
    ax1.scatter([70], [40], color='#2563EB', s=130, edgecolors='#0F172A', linewidths=1.8, zorder=6)
    ax1.annotate('Студент Б (70, 40)\nСума = 110 балів:\n[+] b = -100 => Прийнято\n[-] b = -120 => Відхилено',
                 xy=(70, 40), xytext=(85, 12),
                 arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8),
                 fontsize=9.0, fontweight='bold', color='#1D4ED8',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#EFF6FF', edgecolor='#BFDBFE', alpha=0.95))

    ax1.set_title('Паралельний зсув межі у 2D просторі ознак\n$w = [1, 1], \\quad b \\in \\{-80, -100, -120\\}$',
                  fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax1.set_xlabel('Іспит 1: $x_1$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Іспит 2: $x_2$ (бали)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_xlim(0, 135)
    ax1.set_ylim(0, 135)
    ax1.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax1.legend(loc='upper right', fontsize=9.0, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    # ------------------ Subplot 2: 1D розріз сигмоїди P(y=1) ------------------
    S = np.linspace(50, 150, 300)

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    scale = 0.1
    p_80 = sigmoid(scale * (S - 80))
    p_100 = sigmoid(scale * (S - 100))
    p_120 = sigmoid(scale * (S - 120))

    ax2.plot(S, p_80, color='#10B981', linewidth=2.8, linestyle='--', label=r'$b = -80$: поріг $S = 80$')
    ax2.plot(S, p_100, color='#2563EB', linewidth=3.2, linestyle='-', label=r'$b = -100$: поріг $S = 100$')
    ax2.plot(S, p_120, color='#EF4444', linewidth=2.8, linestyle='-.', label=r'$b = -120$: поріг $S = 120$')

    # Decision threshold P = 0.5
    ax2.axhline(0.5, color='#64748B', linestyle=':', linewidth=1.5, label='Поріг рішення P = 0.5')

    # Markers where P = 0.5
    ax2.scatter([80, 100, 120], [0.5, 0.5, 0.5], color=['#10B981', '#2563EB', '#EF4444'],
                s=110, edgecolors='#0F172A', linewidths=1.5, zorder=5)
    ax2.text(80, 0.53, '80 балів', color='#065F46', fontsize=9.5, fontweight='bold', ha='center')
    ax2.text(100, 0.53, '100 балів', color='#1D4ED8', fontsize=9.5, fontweight='bold', ha='center')
    ax2.text(120, 0.53, '120 балів', color='#991B1B', fontsize=9.5, fontweight='bold', ha='center')

    # Arrow indicating threshold shift
    ax2.annotate('', xy=(122, 0.22), xytext=(78, 0.22),
                 arrowprops=dict(arrowstyle="->", color='#1E293B', lw=2.2))
    ax2.text(100, 0.25, 'Зменшення b (суворіший відбір)\nзміщує криву праворуч',
             fontsize=9.5, fontweight='bold', color='#1E293B', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor='#CBD5E1', alpha=0.95))

    # Highlight student points on curves
    p_stu_a_80 = sigmoid(scale * (90 - 80))
    p_stu_a_100 = sigmoid(scale * (90 - 100))
    ax2.scatter([90, 90], [p_stu_a_80, p_stu_a_100], color='#D97706', s=80, zorder=6)
    ax2.plot([90, 90], [p_stu_a_100, p_stu_a_80], color='#D97706', linestyle=':', lw=2)
    ax2.annotate('Студент А (Сума S=90):\n• P = 73% при b = -80\n• P = 27% при b = -100',
                 xy=(90, p_stu_a_80), xytext=(55, 0.75),
                 arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.8),
                 fontsize=9.0, fontweight='bold', color='#B45309',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF3C7', edgecolor='#FCD34D', alpha=0.95))

    ax2.set_title('Зсув кривої ймовірності $P(y=1) = \\sigma(S + b)$\nзалежно від сумарного балу $S = x_1 + x_2$',
                  fontsize=12.5, fontweight='bold', color='#0F172A', pad=10)
    ax2.set_xlabel('Сумарний бал: $S = x_1 + x_2$', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Ймовірність зарахування $P(y=1)$', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_xlim(50, 150)
    ax2.set_ylim(-0.02, 1.05)
    ax2.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax2.legend(loc='lower right', fontsize=9.0, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    plt.tight_layout()
    path = os.path.join(out_dir, "05-bias-impact.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)


if __name__ == '__main__':
    generate_weights_impact()
    generate_bias_impact()
    print("All parameter impact plots generated cleanly!")
