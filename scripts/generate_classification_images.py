import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.datasets import make_classification, load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8

dir1 = "public/images/ai-python/logistic-regression-classification/classification-basics"
dir2 = "public/images/ai-python/logistic-regression-classification/classification-metrics"
os.makedirs(dir1, exist_ok=True)
os.makedirs(dir2, exist_ok=True)

# -------------------------------------------------------------
# Classification Basics Images (1 - 6)
# -------------------------------------------------------------

def make_basics_01():
    # 01.png: Linear regression failing on classification
    hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
    passed = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])
    model = LinearRegression()
    model.fit(hours, passed)

    hours_range = np.linspace(0, 12, 200).reshape(-1, 1)
    predictions = model.predict(hours_range)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.scatter(hours, passed, color='#2563eb', s=90, label='Реальні дані (0 = не здав, 1 = здав)', zorder=3, edgecolor='#0F172A', linewidth=1.2)
    ax.plot(hours_range, predictions, color='#DC2626', linewidth=2.5, label='Лінія лінійної регресії')
    ax.axhline(y=0.5, color='#16A34A', linestyle='--', linewidth=2, label='Поріг класифікації (0.5)')
    ax.axhline(y=0, color='#64748B', linestyle='-', linewidth=1, alpha=0.5)
    ax.axhline(y=1, color='#64748B', linestyle='-', linewidth=1, alpha=0.5)
    
    # Annotate invalid regions
    ax.fill_between(hours_range.flatten(), 1, 1.4, where=(predictions.flatten() > 1), color='#FEE2E2', alpha=0.6, label='Некоректна зона: ŷ > 1')
    ax.fill_between(hours_range.flatten(), -0.3, 0, where=(predictions.flatten() < 0), color='#FEF3C7', alpha=0.6, label='Некоректна зона: ŷ < 0')

    ax.set_xlabel('Години підготовки до іспиту (год)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Факт складання іспиту / Прогноз ŷ', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Чому лінійна регресія не підходить для бінарної класифікації', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.legend(fontsize=9.5, loc='upper left', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax.set_ylim(-0.3, 1.4)
    ax.set_xlim(-0.5, 12.5)

    plt.tight_layout()
    fig.savefig(os.path.join(dir1, "01.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-basics/01.png")

def make_basics_02():
    # 02.png: Sigmoid curve
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    z = np.linspace(-10, 10, 300)
    sigma_z = sigmoid(z)

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.plot(z, sigma_z, linewidth=3, label=r'$\sigma(z) = 1 / (1 + e^{-z})$', color='#2563EB')
    ax.axhline(y=0.5, color='#16A34A', linestyle='--', linewidth=1.8, label=r'Поріг рішення $\sigma(z) = 0.5$ ($z=0$)', alpha=0.8)
    ax.axvline(x=0, color='#64748B', linestyle='--', linewidth=1.2, alpha=0.6)
    ax.axhline(y=1.0, color='#94A3B8', linestyle=':', linewidth=1.2, label='Горизонтальні асимптоти (0 та 1)')
    ax.axhline(y=0.0, color='#94A3B8', linestyle=':', linewidth=1.2)

    key_points_z = [-5, -2, 0, 2, 5]
    key_points_sigma = [sigmoid(zv) for zv in key_points_z]
    ax.scatter(key_points_z, key_points_sigma, color='#DC2626', s=80, zorder=5, edgecolor='#0F172A', linewidth=1.2)

    for zv, sv in zip(key_points_z, key_points_sigma):
        offset_y = 0.08 if zv <= 0 else -0.1
        ax.annotate(f'σ({zv}) = {sv:.3f}',
                    xy=(zv, sv), xytext=(zv, sv + offset_y),
                    fontsize=9, ha='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF3C7', edgecolor='#F59E0B', alpha=0.9))

    ax.fill_between(z, 0.5, 1.0, where=(z >= 0), color='#DCFCE7', alpha=0.35, label='Область Класу 1 (P ≥ 0.5)')
    ax.fill_between(z, 0.0, 0.5, where=(z < 0), color='#DBEAFE', alpha=0.35, label='Область Класу 0 (P < 0.5)')

    ax.set_xlabel('Лінійна комбінація ознак z = w^T x + b', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Ймовірність належності до класу 1: P(y=1 | x)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Функція сигмоїда (Sigmoid) — перетворення чисел у ймовірності', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax.legend(fontsize=9.5, loc='upper left', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.set_ylim(-0.08, 1.12)
    ax.set_xlim(-10.5, 10.5)

    plt.tight_layout()
    fig.savefig(os.path.join(dir1, "02.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-basics/02.png")

def make_basics_03():
    # 03.png: 2 subplots for BCE loss (y=1 and y=0)
    y_pred = np.linspace(0.001, 0.999, 1000)
    loss_y1 = -np.log(y_pred)
    loss_y0 = -np.log(1 - y_pred)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # Subplot 1: y = 1
    ax1.plot(y_pred, loss_y1, color='#2563EB', linewidth=3, label=r'$L(1, \hat{y}) = -\ln(\hat{y})$')
    ax1.set_xlabel('Передбачена ймовірність ŷ', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Функція втрат L(1, ŷ)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_title('Втрата для істинного класу y = 1', fontsize=12, fontweight='bold', pad=10, color='#0F172A')
    ax1.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax1.set_ylim(0, 5)
    ax1.set_xlim(0, 1)
    ax1.axvline(x=0.5, color='#16A34A', linestyle='--', alpha=0.7, linewidth=1.5)
    ax1.text(0.15, 3.8, 'Впевнена помилка:\nŷ → 0 ⇒ L → ∞', fontsize=9.5,
             bbox=dict(boxstyle='round', facecolor='#FEE2E2', edgecolor='#EF4444', alpha=0.9))
    ax1.text(0.85, 0.8, 'Точний прогноз:\nŷ → 1 ⇒ L → 0', fontsize=9.5, ha='center',
             bbox=dict(boxstyle='round', facecolor='#DCFCE7', edgecolor='#22C55E', alpha=0.9))
    ax1.legend(loc='upper right', fontsize=10)

    # Subplot 2: y = 0
    ax2.plot(y_pred, loss_y0, color='#DC2626', linewidth=3, label=r'$L(0, \hat{y}) = -\ln(1 - \hat{y})$')
    ax2.set_xlabel('Передбачена ймовірність ŷ', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Функція втрат L(0, ŷ)', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_title('Втрата для істинного класу y = 0', fontsize=12, fontweight='bold', pad=10, color='#0F172A')
    ax2.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax2.set_ylim(0, 5)
    ax2.set_xlim(0, 1)
    ax2.axvline(x=0.5, color='#16A34A', linestyle='--', alpha=0.7, linewidth=1.5)
    ax2.text(0.85, 3.8, 'Впевнена помилка:\nŷ → 1 ⇒ L → ∞', fontsize=9.5, ha='center',
             bbox=dict(boxstyle='round', facecolor='#FEE2E2', edgecolor='#EF4444', alpha=0.9))
    ax2.text(0.15, 0.8, 'Точний прогноз:\nŷ → 0 ⇒ L → 0', fontsize=9.5,
             bbox=dict(boxstyle='round', facecolor='#DCFCE7', edgecolor='#22C55E', alpha=0.9))
    ax2.legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    fig.savefig(os.path.join(dir1, "03.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-basics/03.png")

def make_basics_04():
    # 04.png: BCE vs MSE
    y_pred = np.linspace(0.001, 0.999, 1000)
    mse_loss = (1 - y_pred)**2
    bce_loss = -np.log(y_pred)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.plot(y_pred, mse_loss, label='MSE = (1 − ŷ)² (обмежений максимум = 1.0)', color='#F59E0B', linewidth=2.8, linestyle='--')
    ax.plot(y_pred, bce_loss, label='BCE = −ln(ŷ) (штраф зростає до ∞)', color='#2563EB', linewidth=3)
    ax.set_xlabel('Передбачена ймовірність ŷ (для випадку істинного класу y=1)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Величина втрати (Penalty)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Порівняння функцій втрат: чому Binary Cross-Entropy перевершує MSE', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.legend(fontsize=10, loc='upper right', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax.set_ylim(0, 5)
    ax.set_xlim(0, 1)

    # Critical zone highlighting
    ax.axvspan(0, 0.25, alpha=0.12, color='#EF4444', label='Критична зона впевненої помилки')
    ax.text(0.12, 4.3, 'BCE різко штрафує модель\nі формує потужний градієнт для навчання', 
            ha='center', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEE2E2', edgecolor='#EF4444', alpha=0.9))
    ax.text(0.12, 1.2, 'MSE виходить на плато,\nградієнт згасає → 0', 
            ha='center', fontsize=9, color='#B45309')

    plt.tight_layout()
    fig.savefig(os.path.join(dir1, "04.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-basics/04.png")

def make_basics_05():
    # 05.png: Loss curve during gradient descent
    class ScratchLogReg:
        def __init__(self, lr=0.1, n_iter=1000):
            self.lr = lr
            self.n_iter = n_iter
            self.losses = []
        def fit(self, X, y):
            m, n = X.shape
            w = np.zeros(n)
            b = 0
            for _ in range(self.n_iter):
                z = np.dot(X, w) + b
                y_hat = 1 / (1 + np.exp(-z))
                eps = 1e-15
                y_hat = np.clip(y_hat, eps, 1 - eps)
                loss = -np.mean(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))
                self.losses.append(loss)
                dw = np.dot(X.T, (y_hat - y)) / m
                db = np.mean(y_hat - y)
                w -= self.lr * dw
                b -= self.lr * db

    X, y = make_classification(n_samples=200, n_features=2, n_informative=2,
                              n_redundant=0, n_clusters_per_class=1, random_state=42)
    model = ScratchLogReg(lr=0.1, n_iter=1000)
    model.fit(X, y)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.plot(model.losses, linewidth=2.5, color='#2563EB', label='Binary Cross-Entropy Loss')
    ax.set_xlabel('Номер ітерації градієнтного спуску', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Значення функції втрат (Loss)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Динаміка збіжності градієнтного спуску для логістичної регресії', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax.legend(fontsize=10)
    ax.annotate(f'Початкова втрата: {model.losses[0]:.3f}', xy=(0, model.losses[0]), xytext=(70, model.losses[0]-0.05),
                arrowprops=dict(facecolor='#0F172A', arrowstyle='->'), fontsize=9, fontweight='bold')
    ax.annotate(f'Фінальна збіжність: {model.losses[-1]:.3f}', xy=(len(model.losses)-1, model.losses[-1]), xytext=(len(model.losses)-300, model.losses[-1]+0.1),
                arrowprops=dict(facecolor='#16A34A', arrowstyle='->'), fontsize=9, fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(dir1, "05.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-basics/05.png")

def make_basics_06():
    # 06.png: Iris 2D decision boundary
    iris = load_iris()
    X = iris.data[:100, :2]
    y = iris.target[:100]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 250), np.linspace(y_min, y_max, 250))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=300)
    ax.contourf(xx, yy, Z, alpha=0.25, cmap='coolwarm')
    ax.scatter(X[y==0, 0], X[y==0, 1], c='#3B82F6', label='Iris-setosa (Клас 0)', edgecolor='#0F172A', s=75, alpha=0.9)
    ax.scatter(X[y==1, 0], X[y==1, 1], c='#EF4444', label='Iris-versicolor (Клас 1)', edgecolor='#0F172A', s=75, alpha=0.9)
    ax.set_xlabel('Довжина чашолистка — Sepal Length (см)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Ширина чашолистка — Sepal Width (см)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title(f'Лінійна межа рішення (Decision Boundary) на Iris (Точність: {acc:.1%})', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.legend(fontsize=10, loc='upper left', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

    plt.tight_layout()
    fig.savefig(os.path.join(dir1, "06.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-basics/06.png")

# -------------------------------------------------------------
# Classification Metrics Images (1 - 2)
# -------------------------------------------------------------

def make_metrics_01():
    # 01.png: Confusion matrix heatmap: TN=40, FP=0, FN=20, TP=40
    cm = np.array([[40, 0], [20, 40]])
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    
    im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    
    classes = ['Клас 0\n(Негативний)', 'Клас 1\n(Позитивний)']
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(classes, fontsize=10.5, fontweight='bold', color='#1E293B')
    ax.set_yticklabels(classes, fontsize=10.5, fontweight='bold', color='#1E293B')
    ax.set_xlabel('Передбачений клас (Predicted Class)', fontsize=11, fontweight='bold', labelpad=10, color='#0F172A')
    ax.set_ylabel('Фактичний клас (Actual Class)', fontsize=11, fontweight='bold', labelpad=10, color='#0F172A')
    ax.set_title('Матриця помилок (Confusion Matrix)', fontsize=13, fontweight='bold', pad=15, color='#0F172A')
    
    labels_map = [
        [("40", "True Negative (TN)\nПравильно відхилені"), ("0", "False Positive (FP)\nХибна тривога")],
        [("20", "False Negative (FN)\nПропущена загроза (Type II)"), ("40", "True Positive (TP)\nПравильно виявлені (Hit)")]
    ]
    
    thresh = cm.max() / 2.
    for i in range(2):
        for j in range(2):
            val_str, desc = labels_map[i][j]
            color = "white" if cm[i, j] > thresh else "#0F172A"
            ax.text(j, i - 0.12, val_str, ha="center", va="center", color=color, fontsize=18, fontweight="bold")
            ax.text(j, i + 0.18, desc, ha="center", va="center", color=color, fontsize=8.5, fontweight="bold" if "⚠️" in desc else "normal")

    plt.tight_layout()
    fig.savefig(os.path.join(dir2, "01.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-metrics/01.png")

def make_metrics_02():
    # 02.png: Precision vs Recall vs Threshold curves
    thresholds = np.linspace(0.05, 0.95, 19)
    precisions = 1 / (1 + np.exp(-5 * (thresholds - 0.35))) * 0.45 + 0.52
    precisions = np.clip(precisions, 0.55, 1.0)
    recalls = 1 - (1 / (1 + np.exp(-6 * (thresholds - 0.5)))) * 0.65 - 0.15
    recalls = np.clip(recalls, 0.25, 0.98)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.plot(thresholds, precisions, label='Precision (Точність сигналів)', color='#2563EB', linewidth=2.8, marker='o', markersize=4)
    ax.plot(thresholds, recalls, label='Recall (Повнота виявлення)', color='#DC2626', linewidth=2.8, marker='s', markersize=4)
    ax.axvline(x=0.5, color='#16A34A', linestyle='--', linewidth=2, alpha=0.8, label='Стандартний поріг (T = 0.5)')

    # Equilibrium intersection
    idx_eq = np.argmin(np.abs(precisions - recalls))
    ax.scatter([thresholds[idx_eq]], [precisions[idx_eq]], color='#0F172A', s=80, zorder=5)
    ax.annotate(f'Точка балансу:\nT ≈ {thresholds[idx_eq]:.2f}, Score ≈ {precisions[idx_eq]:.2f}',
                xy=(thresholds[idx_eq], precisions[idx_eq]), xytext=(thresholds[idx_eq] + 0.05, precisions[idx_eq] + 0.08),
                fontsize=9.5, fontweight='bold',
                arrowprops=dict(facecolor='#0F172A', arrowstyle='->'),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF3C7', edgecolor='#F59E0B', alpha=0.9))

    ax.set_xlabel('Поріг класифікації (Classification Threshold)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Значення метрики якості', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Компроміс між точністю та повнотою (Precision vs Recall Trade-off)', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax.legend(fontsize=10, loc='center right', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    ax.set_ylim(0.2, 1.05)
    ax.set_xlim(0.0, 1.0)

    plt.tight_layout()
    fig.savefig(os.path.join(dir2, "02.png"), dpi=300)
    plt.close(fig)
    print("Saved classification-metrics/02.png")

if __name__ == "__main__":
    make_basics_01()
    make_basics_02()
    make_basics_03()
    make_basics_04()
    make_basics_05()
    make_basics_06()
    make_metrics_01()
    make_metrics_02()
    print("All 8 classification images successfully generated!")
