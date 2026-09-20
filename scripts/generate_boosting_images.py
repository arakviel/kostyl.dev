import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("public/images/ai-python/gradient-boosting/gradient-boosting-xgboost", exist_ok=True)
out_dir = "public/images/ai-python/gradient-boosting/gradient-boosting-xgboost"

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8

def plot_rf_bias():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    
    labels = ["$0–150k\n(дешеве житло)", "$150–300k\n(середній сегмент)", "$300–450k\n(дорогий сегмент)", "$450k+\n(елітна нерухомість)"]
    errors = [12.3, -8.5, -45.2, -123.4]
    colors = ["#22C55E" if e > 0 else "#EF4444" for e in errors]
    
    bars = ax.bar(labels, errors, color=colors, width=0.55, edgecolor="#0F172A", linewidth=1.2, alpha=0.85)
    ax.axhline(0, color="#0F172A", linestyle="-", linewidth=1.2)
    
    for bar, err in zip(bars, errors):
        height = bar.get_height()
        va = "bottom" if err >= 0 else "top"
        y_pos = height + (3 if err >= 0 else -6)
        text_label = f"+${abs(err):.1f}k\n(переоцінка)" if err > 0 else f"-${abs(err):.1f}k\n(недооцінка)"
        ax.text(bar.get_x() + bar.get_width() / 2, y_pos, text_label, ha="center", va=va, fontsize=10, fontweight="bold", color="#1E293B")
        
    ax.set_ylabel("Середня похибка прогнозу ($y_{pred} - y_{true}$), тис. $", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_title("Систематичне зміщення (Bias) Random Forest за вартістю квартир", fontsize=13, fontweight="bold", pad=15, color="#0F172A")
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="#94A3B8")
    ax.set_axisbelow(True)
    ax.set_ylim(-155, 35)
    
    # Text annotation describing the problem
    ax.text(0.98, 0.93, "⚠️ Random Forest усереднює дерева,\nтому занижує пікові екстремуми.\nBoosting покликаний виправити саме це!", 
            transform=ax.transAxes, ha="right", va="top", fontsize=9.5,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF3C7", edgecolor="#F59E0B", alpha=0.9))
    
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "01.png"), dpi=300)
    plt.close(fig)
    print("Saved 01.png")

def plot_feature_importance_comparison():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    features = [
        "MedInc (медіанний дохід)",
        "Latitude (географічна широта)",
        "Longitude (географічна довгота)",
        "AveOccup (середня заселеність)",
        "HouseAge (вік будинку)",
        "AveRooms (кількість кімнат)",
        "Population (населення)",
        "AveBedrms (кількість спалень)"
    ][::-1]
    
    rf_imp = [0.5234, 0.1456, 0.1234, 0.0107, 0.0445, 0.0823, 0.0512, 0.0189][::-1]
    xgb_imp = [0.5567, 0.1389, 0.1156, 0.0678, 0.0534, 0.0389, 0.0189, 0.0098][::-1]
    
    y = np.arange(len(features))
    height = 0.38
    
    bars1 = ax.barh(y - height/2, rf_imp, height, label="Random Forest (100 дерев)", color="#3B82F6", edgecolor="#1D4ED8", alpha=0.85)
    bars2 = ax.barh(y + height/2, xgb_imp, height, label="XGBoost (300 дерев, lr=0.05)", color="#10B981", edgecolor="#047857", alpha=0.85)
    
    ax.set_yticks(y)
    ax.set_yticklabels(features, fontsize=10, color="#1E293B")
    ax.set_xlabel("Важливість ознаки (Gini / Gain Importance)", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_title("Порівняння важливості ознак: Random Forest vs XGBoost", fontsize=13, fontweight="bold", pad=15, color="#0F172A")
    ax.legend(loc="lower right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=10)
    ax.grid(axis="x", linestyle="--", alpha=0.3, color="#94A3B8")
    ax.set_axisbelow(True)
    ax.set_xlim(0, 0.65)
    
    # Values labels on bars
    for bar in bars1:
        w = bar.get_width()
        if w > 0.03:
            ax.text(w + 0.008, bar.get_y() + bar.get_height()/2, f"{w*100:.1f}%", va="center", ha="left", fontsize=8.5, color="#1D4ED8", fontweight="bold")
    for bar in bars2:
        w = bar.get_width()
        if w > 0.03:
            ax.text(w + 0.008, bar.get_y() + bar.get_height()/2, f"{w*100:.1f}%", va="center", ha="left", fontsize=8.5, color="#047857", fontweight="bold")
            
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "02.png"), dpi=300)
    plt.close(fig)
    print("Saved 02.png")

if __name__ == "__main__":
    plot_rf_bias()
    plot_feature_importance_comparison()
