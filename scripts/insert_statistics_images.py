#!/usr/bin/env python3
"""
Скрипт для вставки посилань на згенеровані діаграми у відповідні лекції.
"""

import os
import re

updates = [
    # 01.random-variables.md
    {
        "file": "content/16.ai-python/04.statistics-basics/01.random-variables.md",
        "plot_idx": 1,
        "img_path": "/images/ai-python/statistics-basics/random-variables/02.png",
        "alt": "Порівняння дискретної та неперервної випадкових величин (кубик vs температура)"
    },
    # 02.central-tendency.md
    {
        "file": "content/16.ai-python/04.statistics-basics/02.central-tendency.md",
        "plot_idx": 1,
        "img_path": "/images/ai-python/statistics-basics/central-tendency/01.png",
        "alt": "Симетричний та асиметричний розподіли: вплив форми на середнє та медіану"
    },
    # 04.distributions.md
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 1,
        "img_path": "/images/ai-python/statistics-basics/distributions/01.png",
        "alt": "Гістограма розподілу споживання молока з лініями середнього та ±1σ"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 2,
        "img_path": "/images/ai-python/statistics-basics/distributions/02.png",
        "alt": "Порівняння PMF (дискретна величина) та PDF (неперервна величина)"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 3,
        "img_path": "/images/ai-python/statistics-basics/distributions/03.png",
        "alt": "Дискретний рівномірний розподіл: 1000 кидків кубика"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 4,
        "img_path": "/images/ai-python/statistics-basics/distributions/04.png",
        "alt": "Неперервний рівномірний розподіл Uniform(0, 10)"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 5,
        "img_path": "/images/ai-python/statistics-basics/distributions/05.png",
        "alt": "Параметри нормального розподілу: вплив середнього μ та стандартного відхилення σ"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 6,
        "img_path": "/images/ai-python/statistics-basics/distributions/06.png",
        "alt": "Правило трьох сигм (емпіричне правило 68-95-99.7%)"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 7,
        "img_path": "/images/ai-python/statistics-basics/distributions/07.png",
        "alt": "Біноміальний розподіл: кількість конверсій з різною ймовірністю успіху"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/04.distributions.md",
        "plot_idx": 8,
        "img_path": "/images/ai-python/statistics-basics/distributions/08.png",
        "alt": "Розподіл Пуассона: кількість подій за фіксований проміжок часу"
    },
    # 05.correlation.md
    {
        "file": "content/16.ai-python/04.statistics-basics/05.correlation.md",
        "plot_idx": 1,
        "img_path": "/images/ai-python/statistics-basics/correlation/01.png",
        "alt": "Діаграма розсіювання (Scatter plot): зв'язок між зростом і вагою"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/05.correlation.md",
        "plot_idx": 2,
        "img_path": "/images/ai-python/statistics-basics/correlation/02.png",
        "alt": "8 патернів кореляції: від повної прямої до від'ємної та нелінійної"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/05.correlation.md",
        "plot_idx": 3,
        "img_path": "/images/ai-python/statistics-basics/correlation/03.png",
        "alt": "Теплова карта (Heatmap) матриці кореляцій фінансових показників"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/05.correlation.md",
        "plot_idx": 4,
        "img_path": "/images/ai-python/statistics-basics/correlation/04.png",
        "alt": "Квартет Анскомба: чотири різні датасети з однаковими статистичними показниками"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/05.correlation.md",
        "plot_idx": 5,
        "img_path": "/images/ai-python/statistics-basics/correlation/05.png",
        "alt": "Хибна кореляція (Spurious correlation): спільний часовий тренд без причинного зв'язку"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/05.correlation.md",
        "plot_idx": 6,
        "img_path": "/images/ai-python/statistics-basics/correlation/06.png",
        "alt": "Матриця кореляцій для виявлення мультиколінеарності"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/05.correlation.md",
        "plot_idx": 7,
        "img_path": "/images/ai-python/statistics-basics/correlation/07.png",
        "alt": "Нелінійний монотонний зв'язок: порівняння коефіцієнтів Пірсона та Спірмена"
    },
    # 06.outliers.md
    {
        "file": "content/16.ai-python/04.statistics-basics/06.outliers.md",
        "plot_idx": 1,
        "img_path": "/images/ai-python/statistics-basics/outliers/01.png",
        "alt": "Вплив викиду (зарплата CEO) на середнє значення та розподіл"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/06.outliers.md",
        "plot_idx": 2,
        "img_path": "/images/ai-python/statistics-basics/outliers/02.png",
        "alt": "Виявлення викидів за допомогою методу міжквартильного розмаху (IQR)"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/06.outliers.md",
        "plot_idx": 3,
        "img_path": "/images/ai-python/statistics-basics/outliers/03.png",
        "alt": "Анатомія коробкового графіка (Box plot) та виявлення аномалій"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/06.outliers.md",
        "plot_idx": 4,
        "img_path": "/images/ai-python/statistics-basics/outliers/04.png",
        "alt": "Виявлення викидів за допомогою Z-оцінки (|Z| > 3)"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/06.outliers.md",
        "plot_idx": 5,
        "img_path": "/images/ai-python/statistics-basics/outliers/05.png",
        "alt": "Логарифмічна трансформація скошеного розподілу з викидами"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/06.outliers.md",
        "plot_idx": 6,
        "img_path": "/images/ai-python/statistics-basics/outliers/06.png",
        "alt": "Порівняння методів обробки викидів: видалення, вінзоризація, робастні метрики"
    },
    {
        "file": "content/16.ai-python/04.statistics-basics/06.outliers.md",
        "plot_idx": 7,
        "img_path": "/images/ai-python/statistics-basics/outliers/07.png",
        "alt": "Стійкість моделей до викидів: лінійна регресія проти дерева рішень"
    },
    # 07.linear-regression-theory/05.practice.md
    {
        "file": "content/16.ai-python/07.linear-regression-theory/05.practice.md",
        "plot_idx": 1,
        "img_path": "/images/ai-python/linear-regression-theory/practice-gd.png",
        "alt": "Крива навчання градієнтного спуску та навчена модель лінійної регресії"
    }
]

# Групуємо оновлення по файлах
by_file = {}
for u in updates:
    by_file.setdefault(u["file"], []).append(u)

for filepath, file_updates in by_file.items():
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Створюємо мапу plot_idx -> update
    updates_map = {u["plot_idx"]: u for u in file_updates}

    new_lines = []
    in_code = False
    cur_code = []
    plot_counter = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("```python"):
            in_code = True
            cur_code = []
            new_lines.append(line)
        elif line.startswith("```") and in_code:
            in_code = False
            code_text = "".join(cur_code)
            new_lines.append(line)

            if "plt.show()" in code_text:
                plot_counter += 1
                if plot_counter in updates_map:
                    upd = updates_map[plot_counter]
                    img_markdown = f"![{upd['alt']}]({upd['img_path']}){{.diagram-img}}\n"

                    # Перевіряємо наступні рядки
                    # Шукаємо #output або наступні рядки
                    # Дивимось, що йде далі
                    j = i + 1
                    found_output = False
                    while j < min(i + 5, len(lines)):
                        if lines[j].strip() == "#output":
                            found_output = True
                            # Копіюємо порожні рядки до #output
                            for k in range(i + 1, j + 1):
                                new_lines.append(lines[k])
                            # Вставляємо картинку одразу після #output
                            # Перевіряємо чи картинки там вже немає
                            if j + 1 < len(lines) and upd["img_path"] in lines[j + 1]:
                                pass # Вже вставлена
                            else:
                                new_lines.append(img_markdown + "\n")
                            i = j
                            break
                        j += 1

                    if not found_output:
                        # Якщо #output немає (наприклад, у 05.practice.md)
                        new_lines.append("\n" + img_markdown)
        else:
            if in_code:
                cur_code.append(line)
            new_lines.append(line)
        i += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Updated: {filepath} with {len(file_updates)} images")

print("All markdown files successfully updated!")
