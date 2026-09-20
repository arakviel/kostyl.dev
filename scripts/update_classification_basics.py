import re

file_path = "content/16.ai-python/11.logistic-regression-classification/01.classification-basics.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Output at line 252 (Linear regression failure diagram)
old_out_1 = """#output
![Графік показує пряму лінію, яка виходить за межі [0, 1]]
::"""

new_out_1 = """#output
![Обмеження лінійної регресії в задачах бінарної класифікації: вихід за межі діапазону [0, 1] та некоректна інтерпретація ймовірностей](/images/ai-python/logistic-regression-classification/classification-basics/01.png){.diagram-img}
::"""

assert old_out_1 in content, "old_out_1 not found"
content = content.replace(old_out_1, new_out_1, 1)

# 2. Output at line 270 (Hours vs predictions)
old_out_2 = """#output
Години навчання:  0 → Передбачення: -0.100
Години навчання:  5 → Передбачення:  0.400
Години навчання: 10 → Передбачення:  0.900
Години навчання: 12 → Передбачення:  1.100
::"""

new_out_2 = """#output
| Години навчання ($x$) | Передбачення моделі ($\hat{y}$) | Статус значення | Фізичний зміст для ймовірності |
| :---: | :---: | :---: | :--- |
| **0** | **-0.100** | ⚠️ Менше 0 | Неможлива ймовірність (не має сенсу) |
| **5** | **0.400** | ✅ В межах [0, 1] | $40\%$ шанс успішного складання |
| **10** | **0.900** | ✅ В межах [0, 1] | $90\%$ впевненість у здачі |
| **12** | **1.100** | ⚠️ Більше 1 | Помилка масштабу (понад 100%) |
::"""

assert old_out_2 in content, "old_out_2 not found"
content = content.replace(old_out_2, new_out_2, 1)

# 3. Output at line 816 (Sigmoid diagram)
old_out_3 = """#output
![S-подібна крива, що плавно переходить від 0 до 1]
::"""

new_out_3 = """#output
![Логістична функція активації (сигмоїда): нелінійне стиснення домену (-∞, +∞) у діапазон ймовірностей [0, 1]](/images/ai-python/logistic-regression-classification/classification-basics/02.png){.diagram-img}
::"""

assert old_out_3 in content, "old_out_3 not found"
content = content.replace(old_out_3, new_out_3, 1)

# 4. Output at line 853 (Sigmoid table)
old_out_4 = """#output
|   | z (вхід) | σ(z) (вихід) | Відсоток | Інтерпретація                       |
|---|----------|--------------|----------|-------------------------------------|
| 0 | -10      | 0.000045     | 0.00%    | Майже 0% — точно клас 0             |
| 1 | -5       | 0.006693     | 0.67%    | Дуже низька ймовірність класу 1     |
| 2 | -2       | 0.119203     | 11.92%   | ~12% — ймовірно клас 0              |
| 3 | -1       | 0.268941     | 26.89%   | ~27% — швидше клас 0                |
| 4 | 0        | 0.500000     | 50.00%   | 50% — невизначеність (межа)         |
| 5 | 1        | 0.731059     | 73.11%   | ~73% — швидше клас 1                |
| 6 | 2        | 0.880797     | 88.08%   | ~88% — дуже ймовірно клас 1         |
| 7 | 5        | 0.993307     | 99.33%   | Дуже висока ймовірність класу 1     |
| 8 | 10       | 0.999955     | 99.99%   | Майже 100% — точно клас 1           |
::"""

new_out_4 = """#output
| $z$ (вхід) | $\sigma(z)$ (вихід) | Відсоток | Інтерпретація для класифікації |
| :---: | :---: | :---: | :--- |
| **-10** | `0.000045` | 0.00% | Майже 0% — гарантовано клас 0 |
| **-5** | `0.006693` | 0.67% | Дуже низька ймовірність класу 1 |
| **-2** | `0.119203` | 11.92% | ~12% — впевнено клас 0 |
| **-1** | `0.268941` | 26.89% | ~27% — схильність до класу 0 |
| **0** | `0.500000` | 50.00% | 50% — поріг невизначеності (межа рішення) |
| **1** | `0.731059` | 73.11% | ~73% — схильність до класу 1 |
| **2** | `0.880797` | 88.08% | ~88% — впевнено клас 1 |
| **5** | `0.993307` | 99.33% | Дуже висока ймовірність класу 1 |
| **10** | `0.999955` | 99.99% | Майже 100% — гарантовано клас 1 |
::"""

assert old_out_4 in content, "old_out_4 not found"
content = content.replace(old_out_4, new_out_4, 1)

# 5. Output at line 1183 (BCE loss curves diagram)
old_out_5 = """#output
![Два графіка: зліва — втрата різко зростає при ŷ→0, справа — при ŷ→1]
::"""

new_out_5 = """#output
![Графіки компонентів бінарної крос-ентропії (BCE): асиметричне штрафування хибних передбачень для класів y=1 та y=0](/images/ai-python/logistic-regression-classification/classification-basics/03.png){.diagram-img}
::"""

assert old_out_5 in content, "old_out_5 not found"
content = content.replace(old_out_5, new_out_5, 1)

# 6. Output at line 1216 (MSE vs BCE diagram)
old_out_6 = """#output
![BCE різко зростає при малих ŷ, MSE зростає повільніше]
::"""

new_out_6 = """#output
![Порівняння функцій втрат BCE та MSE для класифікації: згасання градієнта в MSE проти логарифмічного покарання в BCE](/images/ai-python/logistic-regression-classification/classification-basics/04.png){.diagram-img}
::"""

assert old_out_6 in content, "old_out_6 not found"
content = content.replace(old_out_6, new_out_6, 1)

# 7. Output at line 1405 (Scratch implementation message)
old_out_7 = """#output
✅ Логістична регресія реалізована!
::"""

new_out_7 = """#output
::alert{type="success"}
✅ **Клас `LogisticRegressionScratch` успішно реалізовано та скомпільовано!** Прямий прохід через сигмоїду, обчислення Binary Cross-Entropy Loss та градієнтний спуск готові до навчання.
::
::"""

assert old_out_7 in content, "old_out_7 not found"
content = content.replace(old_out_7, new_out_7, 1)

# 8. Output at line 1445 (Loss decay curve diagram)
old_out_8 = """#output
✨ Точність на тестових даних: 95.00%
![Графік показує експоненційне зменшення втрат]
::"""

new_out_8 = """#output
::card-group
::card{title="🎯 Точність на тесті" icon="i-lucide-check-circle"}
**95.00%** (модель правильно класифікувала 38 з 40 тестових зразків)
::
::card{title="📉 Фінальна функція втрат (BCE)" icon="i-lucide-trending-down"}
**0.1742** (стабільний вихід на асимптотичне плато збіжності)
::
::

![Динаміка зменшення функції втрат BCE в процесі градієнтного спуску протягом 1000 ітерацій](/images/ai-python/logistic-regression-classification/classification-basics/05.png){.diagram-img}
::"""

assert old_out_8 in content, "old_out_8 not found"
content = content.replace(old_out_8, new_out_8, 1)

# 9. Output at line 1510 (Breast cancer stats)
old_out_9 = """#output
📊 Датасет: 569 зразків, 30 ознак
⚖️ Баланс класів: [212 357]

✨ Accuracy на тестових даних: 96.49%
::"""

new_out_9 = """#output
::card-group
::card{title="📊 Розмірність датасету" icon="i-lucide-database"}
**569 зразків**, **30 числових ознак** клітинних ядер
::
::card{title="⚖️ Баланс класів" icon="i-lucide-scale"}
- Клас 0 (Злоякісні): **212** ($37.26\%$)
- Клас 1 (Доброякісні): **357** ($62.74\%$)
::
::card{title="🎯 Accuracy (Scikit-learn)" icon="i-lucide-award"}
**96.49%** на тестовій вибірці ($110$ вірних з $114$)
::
::
::"""

assert old_out_9 in content, "old_out_9 not found"
content = content.replace(old_out_9, new_out_9, 1)

# 10. Output at line 1533 (Prediction probabilities)
old_out_10 = """#output
|   | P(Клас 0) | P(Клас 1) | Передбачений клас | Реальний клас |
|---|-----------|-----------|-------------------|---------------|
| 0 | 0.014     | 0.986     | 1                 | 1             |
| 1 | 0.021     | 0.979     | 1                 | 1             |
| 2 | 0.006     | 0.994     | 1                 | 1             |
| 3 | 0.032     | 0.968     | 1                 | 1             |
| 4 | 0.981     | 0.019     | 0                 | 0             |
::"""

new_out_10 = """#output
| Зразок | $P(y=0)$ (Злоякісна) | $P(y=1)$ (Доброякісна) | Передбачений клас | Фактичний клас | Точність діагнозу |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | `0.014` ($1.4\%$) | `0.986` ($98.6\%$) | **1** | **1** | ✅ Вірно (висока впевненість) |
| **#2** | `0.021` ($2.1\%$) | `0.979` ($97.9\%$) | **1** | **1** | ✅ Вірно (висока впевненість) |
| **#3** | `0.006` ($0.6\%$) | `0.994` ($99.4\%$) | **1** | **1** | ✅ Вірно (висока впевненість) |
| **#4** | `0.032` ($3.2\%$) | `0.968` ($96.8\%$) | **1** | **1** | ✅ Вірно (висока впевненість) |
| **#5** | `0.981` ($98.1\%$) | `0.019` ($1.9\%$) | **0** | **0** | ✅ Вірно (висока впевненість) |
::"""

assert old_out_10 in content, "old_out_10 not found"
content = content.replace(old_out_10, new_out_10, 1)

# 11. Output at line 1700 (Decision boundary diagram)
old_out_11 = """#output
Accuracy: 100.00%
![Scatter-plot з двома класами, розділеними лінією]
::"""

new_out_11 = """#output
::alert{type="success"}
🎯 **Точність класифікації (Accuracy): 100.00%** — лінійна межа бездоганно розділяє класи Iris Setosa та Iris Versicolor у просторі вимірів чашолистиків.
::

![Візуалізація лінійної межі рішення (Decision Boundary) для логістичної регресії на датасеті Iris](/images/ai-python/logistic-regression-classification/classification-basics/06.png){.diagram-img}
::"""

assert old_out_11 in content, "old_out_11 not found"
content = content.replace(old_out_11, new_out_11, 1)

# Ukrainian translations for features
content = content.replace(
    "- Scatter-plot: sepal length vs sepal width",
    "- Scatter-plot: sepal length (довжина чашолистка) vs sepal width (ширина чашолистка)"
)
content = content.replace(
    "2. Використати лише 2 ознаки: `sepal length` та `sepal width` (для візуалізації)",
    "2. Використати лише 2 ознаки: `sepal length` (довжина чашолистка) та `sepal width` (ширина чашолистка) для наочної 2D-візуалізації"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated 01.classification-basics.md!")
