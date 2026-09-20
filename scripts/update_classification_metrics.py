import re

file_path = "content/16.ai-python/11.logistic-regression-classification/02.classification-metrics.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Clean up outline draft (lines 6-430)
outline_start = "### 1. Hook: Accuracy = 99%, але модель — катастрофа!"
outline_end = "**Наступний модуль:** Основи нейронних мереж — персептрон, багатошаровий персептрон, PyTorch."

start_pos = content.find(outline_start)
end_pos = content.find(outline_end) + len(outline_end)

assert start_pos != -1 and end_pos != -1, "Outline boundaries not found"
# Slice out outline draft, preserving header and moving straight to full lecture
content = content[:start_pos].rstrip() + "\n\n" + content[end_pos:].lstrip()

# 2. Output: Initial Confusion matrix + 01.png
old_cm_1 = """Confusion Matrix:
[[40  0]
 [20 40]]

True Positive (TP): 40
False Positive (FP): 0
False Negative (FN): 20
True Negative (TN): 40

![Heatmap з чотирма квадратами: TN=40, FP=0, FN=20, TP=40]"""

new_cm_1 = """| | Передбачено: Позитив (1) | Передбачено: Негатив (0) | Всього факт |
| :--- | :---: | :---: | :---: |
| **Реально: Позитив (1)** | **TP = 40** (Вірно виявлені) | **FN = 20** (Пропущена загроза) | 60 |
| **Реально: Негатив (0)** | **FP = 0** (Хибна тривога) | **TN = 40** (Вірно відхилені) | 40 |
| **Всього прогноз** | 40 | 60 | **100** |

![Матриця помилок (Confusion Matrix): розподіл правильно та помилково класифікованих об'єктів для бінарної класифікації](/images/ai-python/logistic-regression-classification/classification-metrics/01.png){.diagram-img}"""

assert old_cm_1 in content, "old_cm_1 not found"
content = content.replace(old_cm_1, new_cm_1, 1)

# 3. Output: Precision
old_prec = """Precision: 90.00%

Інтерпретація:
З 100 листів, позначених як 'спам', 90 реально спам.
10 важливих листів потрапили до спаму (FP) — проблема!"""

new_prec = """::card-group
::card{title="🎯 Метрика Precision" icon="i-lucide-crosshair"}
**90.00%** (точність позитивних передбачень моделі)
::
::card{title="✉️ Інтерпретація на пошті" icon="i-lucide-mail"}
З **100** позначених як спам: **90** — справжній спам, а **10** — важливі листи, втрачені в спамі (FP).
::
::"""

assert old_prec in content, "old_prec not found"
content = content.replace(old_prec, new_prec, 1)

# 4. Output: Recall
old_rec = """Recall: 90.00%

Інтерпретація:
З 50 реально хворих пацієнтів модель знайшла 45.
Пропустила 5 хворих (FN) — це КРИТИЧНО! 💀

У медицині Recall важливіший за Precision!"""

new_rec = """::card-group
::card{title="🔍 Метрика Recall" icon="i-lucide-search"}
**90.00%** (повнота охоплення цільового класу)
::
::card{title="🏥 Медичний наслідок" icon="i-lucide-activity"}
З **50** хворих виявлено **45**. Пропущено **5** недіагностованих пацієнтів (FN) — критична загроза!
::
::"""

assert old_rec in content, "old_rec not found"
content = content.replace(old_rec, new_rec, 1)

# 5. Output: Trade-off curve + 02.png
old_tradeoff = """![Графік: Precision зростає зі збільшенням порогу, Recall спадає]"""

new_tradeoff = """![Компроміс між точністю та повнотою (Precision vs Recall Trade-off) залежно від обраного порогу класифікації](/images/ai-python/logistic-regression-classification/classification-metrics/02.png){.diagram-img}"""

assert old_tradeoff in content, "old_tradeoff not found"
content = content.replace(old_tradeoff, new_tradeoff, 1)

# 6. Output: Threshold table
old_th_table = """|   | Поріг | TP  | FP  | FN  | TN  | Precision | Recall |
|---|-------|-----|-----|-----|-----|-----------|--------|
| 0 | 0.3   | 85  | 35  | 5   | 175 | 0.708     | 0.944  |
| 1 | 0.5   | 78  | 15  | 12  | 195 | 0.839     | 0.867  |
| 2 | 0.7   | 65  | 5   | 25  | 205 | 0.929     | 0.722  |"""

new_th_table = """| Поріг ($T$) | TP | FP | FN | TN | Precision | Recall | Характеристика режиму |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0.3** | 85 | 35 | 5 | 175 | **0.708** ($70.8\%$) | **0.944** ($94.4\%$) | 🛡️ Агресивний пошук (мінімум пропусків FN) |
| **0.5** | 78 | 15 | 12 | 195 | **0.839** ($83.9\%$) | **0.867** ($86.7\%$) | ⚖️ Збалансований стандартний режим |
| **0.7** | 65 | 5 | 25 | 205 | **0.929** ($92.9\%$) | **0.722** ($72.2\%$) | 🎯 Консервативний відбір (висока впевненість FP↓) |"""

assert old_th_table in content, "old_th_table not found"
content = content.replace(old_th_table, new_th_table, 1)

# 7. Output: F1 harmonic mean table
old_f1_table = """|   | Precision | Recall | Arithmetic Mean | F1 (Harmonic Mean) |
|---|-----------|--------|-----------------|-------------------|
| 0 | 1.0       | 1.0    | 1.000           | 1.000             |
| 1 | 0.9       | 0.9    | 0.900           | 0.900             |
| 2 | 1.0       | 0.5    | 0.750           | 0.667             |
| 3 | 1.0       | 0.1    | 0.550           | 0.182             |
| 4 | 0.5       | 0.5    | 0.500           | 0.500             |"""

new_f1_table = """| Precision | Recall | Арифметичне середнє | F1-score (Гармонійне середнє) | Інтерпретація чутливості |
| :---: | :---: | :---: | :---: | :--- |
| **1.00** | **1.00** | 1.000 | **1.000** | Ідеальна якість обох метрик |
| **0.90** | **0.90** | 0.900 | **0.900** | Гармонійний збалансований класифікатор |
| **1.00** | **0.50** | 0.750 | **0.667** | Помірний штраф за падіння Recall |
| **1.00** | **0.10** | 0.550 | **0.182** | ⚠️ Жорсткий штраф за дисбаланс метрик |
| **0.50** | **0.50** | 0.500 | **0.500** | Середня якість за симетричних значень |"""

assert old_f1_table in content, "old_f1_table not found"
content = content.replace(old_f1_table, new_f1_table, 1)

# 8. Output: Classification report table
old_report = """```
              precision    recall  f1-score   support

    Злоякісна       0.94      0.91      0.93        43
  Доброякісна       0.96      0.97      0.96        71

     accuracy                           0.95       114
    macro avg       0.95      0.94      0.95       114
 weighted avg       0.95      0.95      0.95       114
```"""

new_report = """| Клас / Метрика | Precision | Recall | F1-Score | Кількість (Support) |
| :--- | :---: | :---: | :---: | :---: |
| **Злоякісна (Malignant)** | **0.94** | **0.91** | **0.93** | 43 |
| **Доброякісна (Benign)** | **0.96** | **0.97** | **0.96** | 71 |
| **Accuracy (Загальна точність)** | — | — | **0.95** | 114 |
| **Macro Avg (Просте середнє)** | 0.95 | 0.94 | 0.95 | 114 |
| **Weighted Avg (Зважене середнє)** | 0.95 | 0.95 | 0.95 | 114 |"""

assert old_report in content, "old_report not found"
content = content.replace(old_report, new_report, 1)

# 9. Output: ROC curve 1 + 03.png
old_roc_1 = """![ROC крива — S-подібна лінія, що проходить значно вище діагоналі]"""

new_roc_1 = """![ROC-крива: Оцінка роздільної здатності логістичної регресії та площі під кривою (AUC = 0.998)](/images/ai-python/logistic-regression-classification/classification-metrics/03.png){.diagram-img}"""

assert old_roc_1 in content, "old_roc_1 not found"
content = content.replace(old_roc_1, new_roc_1, 1)

# 10. Output: Practical dataset stats
old_ds_stats = """📊 Датасет: 569 зразків, 30 ознак
⚖️ Баланс класів: Злоякісна=212, Доброякісна=357

📈 Метрики класифікації:
  Accuracy:  0.965
  Precision: 0.958
  Recall:    0.972
  F1-score:  0.965
  ROC-AUC:   0.993"""

new_ds_stats = """::card-group
::card{title="📊 Параметри вибірки" icon="i-lucide-database"}
**569 зразків**, **30 ознак**. Злоякісних: 212 ($37.3\%$), Доброякісних: 357 ($62.7\%$).
::
::card{title="🎯 Комплексні метрики" icon="i-lucide-activity"}
- **Accuracy:** `0.965` ($96.5\%$)
- **Precision:** `0.958` ($95.8\%$)
- **Recall:** `0.972` ($97.2\%$)
- **F1-score:** `0.965`
- **ROC-AUC:** `0.993`
::
::"""

assert old_ds_stats in content, "old_ds_stats not found"
content = content.replace(old_ds_stats, new_ds_stats, 1)

# 11. Output: Confusion Matrix Breast Cancer + 04.png
old_cm_bc = """![Confusion Matrix: TN=41, FP=2, FN=2, TP=69]

🔍 Детальний аналіз помилок:
  True Positive (TP): 69 — правильно виявлена доброякісна пухлина
  True Negative (TN): 41 — правильно виявлена злоякісна пухлина
  False Positive (FP): 2 — злоякісну назвали доброякісною (КРИТИЧНО! 💀)
  False Negative (FN): 2 — доброякісну назвали злоякісною (неприємно, але менш критично)"""

new_cm_bc = """| | Передбачено: Доброякісна (1) | Передбачено: Злоякісна (0) | Всього факт |
| :--- | :---: | :---: | :---: |
| **Фактично: Доброякісна (1)** | **TP = 69** (Вірно виявлена) | **FN = 2** (Хибна підозра) | 71 |
| **Фактично: Злоякісна (0)** | **FP = 2** (⚠️ Пропуск пухлини!) | **TN = 41** (Вірно виявлена) | 43 |
| **Всього прогноз** | 71 | 43 | **114** |

![Матриця помилок (Confusion Matrix) для діагностики раку молочної залози](/images/ai-python/logistic-regression-classification/classification-metrics/04.png){.diagram-img}"""

assert old_cm_bc in content, "old_cm_bc not found"
content = content.replace(old_cm_bc, new_cm_bc, 1)

# 12. Output: ROC curve Breast Cancer + 05.png
old_roc_bc = """![ROC крива з AUC = 0.993]"""

new_roc_bc = """![ROC-крива для моделі діагностики раку молочної залози (AUC = 0.993)](/images/ai-python/logistic-regression-classification/classification-metrics/05.png){.diagram-img}"""

assert old_roc_bc in content, "old_roc_bc not found"
content = content.replace(old_roc_bc, new_roc_bc, 1)

# 13. Output: Top-5 thresholds
old_top_th = """🎯 Оптимальний поріг: 0.45
📊 Найкращий F1-score: 0.972

Топ-5 порогів за F1-score:
    Threshold  Precision  Recall  F1-score
12       0.45      0.958   0.986     0.972
11       0.40      0.945   0.986     0.965
13       0.50      0.958   0.972     0.965
14       0.55      0.972   0.972     0.972
10       0.35      0.932   0.986     0.958"""

new_top_th = """::card-group
::card{title="🎯 Оптимальний поріг ($T^*$)" icon="i-lucide-sliders"}
**0.45** (зсув у бік вищої чутливості Recall)
::
::card{title="📊 Максимальний F1-score" icon="i-lucide-trending-up"}
**0.972** (приріст порівняно зі стандартним порогом 0.5)
::
::

| Ранг | Поріг (Threshold) | Precision | Recall | F1-Score | Ефект для клініки |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 🥇 | **0.45** | `0.958` | `0.986` | **0.972** | **Оптимум:** знайдено 98.6% пухлин при 95.8% точності |
| 🥈 | **0.55** | `0.972` | `0.972` | **0.972** | Повна симетрія Precision та Recall |
| 🥉 | **0.50** | `0.958` | `0.972` | **0.965** | Стандартний нескоригований поріг за замовчуванням |
| 4 | **0.40** | `0.945` | `0.986` | **0.965** | Більш консервативний до Recall, але втрата в точності |
| 5 | **0.35** | `0.932` | `0.986` | **0.958** | Надмірна кількість хибних тривог (FP) |"""

assert old_top_th in content, "old_top_th not found"
content = content.replace(old_top_th, new_top_th, 1)

# 14. Output: Model comparison table
old_comp = """|   | Модель               | Accuracy | Precision | Recall | F1-score | ROC-AUC | Час навчання (с) |
|---|----------------------|----------|-----------|--------|----------|---------|------------------|
| 0 | Logistic Regression  | 0.965    | 0.958     | 0.972  | 0.965    | 0.993   | 0.045            |
| 1 | Decision Tree        | 0.939    | 0.932     | 0.944  | 0.938    | 0.931   | 0.012            |
| 2 | Random Forest        | 0.974    | 0.972     | 0.972  | 0.972    | 0.996   | 0.285            |"""

new_comp = """| Алгоритм (Модель) | Accuracy | Precision | Recall | F1-score | ROC-AUC | Час навчання (с) | Вердикт та застосування |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 🌲 **Random Forest** | **0.974** | **0.972** | **0.972** | **0.972** | **0.996** | 0.285 с | 🏆 **Лідер за точністю** (рекомендовано для клініки) |
| 📈 **Logistic Regression** | 0.965 | 0.958 | 0.972 | 0.965 | 0.993 | **0.045 с** | ⚡ **Швидка та повністю інтерпретабельна** |
| 🌳 **Decision Tree** | 0.939 | 0.932 | 0.944 | 0.938 | 0.931 | 0.012 с | 📉 Схильна до перенавчання на малих вибірках |"""

assert old_comp in content, "old_comp not found"
content = content.replace(old_comp, new_comp, 1)

# 15. Fix broken word wrap
content = content.replace(
    "навіть якщо навчання три\n\nвале довше.",
    "навіть якщо навчання триває довше."
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated 02.classification-metrics.md!")
