# Документація: Робота з зображеннями для статей

Цей документ описує процес пошуку, завантаження та вставки якісних зображень у markdown статті за допомогою автоматизованих скриптів.

---

## Огляд системи

Система складається з двох основних скриптів:

1. **`fetch_images.py`** — пошук та завантаження якісних зображень з DuckDuckGo
2. **`insert_images.py`** — автоматична вставка завантажених зображень у markdown файли

### Ключові можливості

- ✅ Автоматична фільтрація зображень за якістю (розмір, формат, джерело)
- ✅ Інтелектуальна оцінка зображень (пріоритет SVG > PNG > JPG)
- ✅ Автоматична нумерація зображень в межах статті (01.png, 02.png, ...)
- ✅ Інтерактивний режим вибору зображень
- ✅ Автоматична вставка зображень за маркерами у markdown

---

## Скрипт 1: `fetch_images.py`

### Призначення

Шукає технічні зображення (діаграми, архітектури, схеми) через DuckDuckGo, аналізує їх якість та завантажує найкращі варіанти з автоматичною нумерацією.

### Алгоритм оцінки якості

Кожне зображення оцінюється за наступними критеріями:

1. **Формат** (максимум 100 балів):
   - SVG: 100 балів (векторна графіка, ідеально для діаграм)
   - PNG: 80 балів (без втрат, добре для схем)
   - WebP: 70 балів (сучасний формат)
   - JPG/JPEG: 60 балів (з втратами, гірше для тексту)
   - GIF: 40 балів (застарілий)

2. **Розмір зображення** (максимум 50 балів):
   - 1000-2000px ширина: 50 балів (оптимально)
   - 800-1000px: 40 балів (прийнятно)
   - 2000-3000px: 35 балів (занадто велике)
   - < 800px: 10 балів (занадто мале)

3. **Джерело** (максимум 30 балів):
   - Пріоритетні домени: +30 балів
     - Офіційні документації: kubernetes.io, docker.com, github.com, gitlab.com
     - Хмарні провайдери: microsoft.com, azure.com, google.com, aws.amazon.com, cloud.google.com
     - Технічні блоги: medium.com, dev.to, digitalocean.com, redhat.com, ibm.com, nginx.com, apache.org, mozilla.org, cloudflare.com
     - Освітні платформи: freecodecamp.org, codecademy.com, udemy.com, pluralsight.com
     - Технічні видання: infoq.com, dzone.com, hackernoon.com, towards.dev
     - Спеціалізовані ресурси: spacelift.io, k21academy.com, phoenixnap.com, ionos.com, simform.com, nops.io, rancher.com, cncf.io
     - Блоги компаній: atlassian.com, jetbrains.com, stackoverflow.com, stackexchange.com
   - Інші джерела: 0 балів

4. **Розмір файлу** (максимум 10 балів):
   - > 100KB: +10 балів (більше деталей)

**Максимальна оцінка:** 190 балів

### Використання

#### Базове використання (автоматичний режим)

```bash
# Завантажити топ-3 зображення за запитом
python scripts/fetch_images.py "kubernetes architecture" \
  --md content/07.tools/02.kubernetes/01.why-kubernetes.md

# Завантажити 5 зображень
python scripts/fetch_images.py "docker compose diagram" \
  --md content/docker/compose.md -l 5

# Встановити мінімальну ширину 1200px
python scripts/fetch_images.py "kubernetes cluster" \
  --md content/k8s.md --min-width 1200
```

#### Інтерактивний режим

```bash
# Показати топ-10 зображень та дозволити вибрати вручну
python scripts/fetch_images.py "kubernetes rolling update" \
  --md content/k8s.md -l 10 -i
```

У інтерактивному режимі скрипт покаже список зображень з оцінками:

```
🎯 ТОП ЗОБРАЖЕНЬ (відсортовано за якістю):
======================================================================
1. Оцінка: 160 | 1440x1181 | PNG
   URL: https://example.com/k8s-architecture.png
   Назва: Kubernetes Architecture Diagram

2. Оцінка: 150 | 1200x800 | SVG
   URL: https://kubernetes.io/images/architecture.svg
   Назва: Official K8s Architecture

Введіть номери для завантаження (через кому, наприклад: 1,2,3) або Enter для топ-3:
```

### Параметри

| Параметр | Опис | Типово |
|----------|------|--------|
| `query` | Пошуковий запит (обов'язковий) | - |
| `--md` | Шлях до markdown файлу для автоматичного визначення папки | - |
| `-l, --limit` | Кількість зображень для завантаження | 3 |
| `-o, --output` | Папка для збереження (якщо немає --md) | - |
| `-i, --interactive` | Інтерактивний режим вибору | false |
| `--min-width` | Мінімальна ширина зображення в пікселях | 800 |

### Структура папок

Скрипт автоматично визначає папку для зображень на основі шляху до markdown файлу:

```
content/07.tools/02.kubernetes/01.why-kubernetes.md
    ↓
public/images/tools/kubernetes/why-kubernetes/
```

Правила:
- Видаляються числові префікси (`07.tools` → `tools`)
- Видаляється розширення `.md`
- Зображення нумеруються: `01.png`, `02.svg`, `03.jpg`, ...

### Приклад виводу

```bash
$ python scripts/fetch_images.py "kubernetes architecture" --md content/k8s.md

📁 Шлях визначено автоматично за md-файлом: public/images/tools/kubernetes/why-kubernetes
🔍 Шукаємо зображення за запитом: 'kubernetes architecture' (ліміт: 3)...
✅ Знайдено 6 зображень. Аналізую якість...
  [1/6] Аналізую: https://example.com/k8s.png...
    ✓ 1440x1181 PNG | Оцінка: 160
  [2/6] Аналізую: https://kubernetes.io/arch.svg...
    ✓ 9999x9999 SVG | Оцінка: 190

📥 Завантажую 3 зображень...
  [1/3] Завантаження: https://kubernetes.io/arch.svg...
    ✅ Збережено: 01.svg
  [2/3] Завантаження: https://example.com/k8s.png...
    ✅ Збережено: 02.png

======================================================================
📋 ГОТОВІ ВСТАВКИ ДЛЯ MARKDOWN:
======================================================================
![kubernetes architecture](/images/tools/kubernetes/why-kubernetes/01.svg){.diagram-img}
![kubernetes architecture](/images/tools/kubernetes/why-kubernetes/02.png){.diagram-img}
======================================================================
```

---

## Скрипт 2: `insert_images.py`

### Призначення

Автоматично вставляє завантажені зображення у markdown файли за спеціальними маркерами.

### Як це працює

1. Додайте маркери у ваш markdown файл:

```markdown
## Архітектура Kubernetes

<!-- IMAGE: kubernetes architecture -->

Kubernetes складається з control plane та worker nodes...
```

2. Завантажте зображення:

```bash
python scripts/fetch_images.py "kubernetes architecture" --md content/k8s.md
```

3. Вставте зображення у файл:

```bash
python scripts/insert_images.py content/k8s.md
```

4. Результат:

```markdown
## Архітектура Kubernetes

![kubernetes architecture](/images/tools/kubernetes/why-kubernetes/01.png){.diagram-img}

Kubernetes складається з control plane та worker nodes...
```

### Використання

#### Базове використання

```bash
# Вставити зображення у файл
python scripts/insert_images.py content/07.tools/02.kubernetes/01.why-kubernetes.md
```

#### Режим перегляду (dry-run)

```bash
# Показати план без застосування змін
python scripts/insert_images.py content/k8s.md --dry-run
```

### Параметри

| Параметр | Опис | Типово |
|----------|------|--------|
| `markdown_file` | Шлях до markdown файлу (обов'язковий) | - |
| `--dry-run` | Показати план без застосування змін | false |

### Формат маркерів

```markdown
<!-- IMAGE: опис зображення -->
```

- Маркер має бути на окремому рядку
- Текст після `IMAGE:` використовується як alt-текст для зображення
- Зображення вставляються у порядку маркерів, починаючи з `01.png`, `02.png`, ...

### Приклад виводу

```bash
$ python scripts/insert_images.py content/k8s.md --dry-run

📄 Файл: content/07.tools/02.kubernetes/01.why-kubernetes.md
🔍 Знайдено 3 маркерів IMAGE
📁 Папка зображень: public/images/tools/kubernetes/why-kubernetes
🖼️  Доступно 5 зображень: 01.png, 02.svg, 03.png, 04.jpg, 05.png

======================================================================
📋 ПЛАН ВСТАВКИ:
======================================================================
1. Маркер: <!-- IMAGE: kubernetes architecture -->
   Зображення: 01.png
   Вставка: ![kubernetes architecture](/images/tools/kubernetes/why-kubernetes/01.png){.diagram-img}

2. Маркер: <!-- IMAGE: kubernetes self-healing -->
   Зображення: 02.svg
   Вставка: ![kubernetes self-healing](/images/tools/kubernetes/why-kubernetes/02.svg){.diagram-img}

3. Маркер: <!-- IMAGE: kubernetes rolling update -->
   Зображення: 03.png
   Вставка: ![kubernetes rolling update](/images/tools/kubernetes/why-kubernetes/03.png){.diagram-img}

🔍 Режим перегляду (dry-run). Зміни не застосовано.
```

---

## Повний робочий процес

### Крок 1: Підготовка статті

Додайте маркери у ваш markdown файл у місцях, де потрібні зображення:

```markdown
---
title: Kubernetes — коли Docker Compose більше не вистачає
---

# Kubernetes — коли Docker Compose більше не вистачає

## Що таке Kubernetes?

Kubernetes — це система оркестрації контейнерів...

<!-- IMAGE: kubernetes architecture -->

### Компоненти Kubernetes

Control plane складається з...

<!-- IMAGE: kubernetes control plane -->

## Self-healing

Kubernetes автоматично відновлює контейнери...

<!-- IMAGE: kubernetes self-healing -->
```

### Крок 2: Завантаження зображень

Завантажте зображення для кожного маркера:

```bash
# Зображення 1: kubernetes architecture
python scripts/fetch_images.py "kubernetes architecture diagram" \
  --md content/07.tools/02.kubernetes/01.why-kubernetes.md -l 1

# Зображення 2: kubernetes control plane
python scripts/fetch_images.py "kubernetes control plane components" \
  --md content/07.tools/02.kubernetes/01.why-kubernetes.md -l 1

# Зображення 3: kubernetes self-healing
python scripts/fetch_images.py "kubernetes self-healing pods" \
  --md content/07.tools/02.kubernetes/01.why-kubernetes.md -l 1
```

Або завантажте всі зображення одразу з більшим лімітом:

```bash
python scripts/fetch_images.py "kubernetes architecture" \
  --md content/07.tools/02.kubernetes/01.why-kubernetes.md -l 10 -i
```

### Крок 3: Перевірка (опціонально)

Перегляньте план вставки без застосування змін:

```bash
python scripts/insert_images.py content/07.tools/02.kubernetes/01.why-kubernetes.md --dry-run
```

### Крок 4: Вставка зображень

Застосуйте зміни:

```bash
python scripts/insert_images.py content/07.tools/02.kubernetes/01.why-kubernetes.md
```

### Крок 5: Перевірка результату

Відкрийте файл та перевірте, що зображення вставлені правильно:

```markdown
## Що таке Kubernetes?

Kubernetes — це система оркестрації контейнерів...

![kubernetes architecture](/images/tools/kubernetes/why-kubernetes/01.png){.diagram-img}

### Компоненти Kubernetes
```

---

## Поради та рекомендації

### Як отримати якісні зображення

1. **Використовуйте конкретні запити:**
   - ✅ Добре: `"kubernetes architecture diagram"`
   - ❌ Погано: `"kubernetes"`

2. **Додавайте ключові слова:**
   - `"diagram"`, `"architecture"`, `"schema"`, `"flow"`, `"structure"`

3. **Використовуйте інтерактивний режим:**
   - Дозволяє вибрати найкращі зображення вручну
   - Корисно для критично важливих діаграм

4. **Встановлюйте мінімальну ширину:**
   - Для великих діаграм: `--min-width 1200`
   - Для іконок та логотипів: `--min-width 500`

### Організація маркерів

1. **Один маркер = одне зображення:**
   ```markdown
   <!-- IMAGE: kubernetes architecture -->
   ```

2. **Описові назви:**
   ```markdown
   <!-- IMAGE: kubernetes rolling update process -->
   <!-- IMAGE: docker compose vs kubernetes comparison -->
   ```

3. **Порядок має значення:**
   - Маркери обробляються зверху вниз
   - Зображення вставляються у порядку: 01.png, 02.png, 03.png, ...

### Управління зображеннями

1. **Видалення зображень:**
   ```bash
   rm -rf public/images/tools/kubernetes/why-kubernetes/
   ```

2. **Перезавантаження зображень:**
   ```bash
   # Видалити старі
   rm -rf public/images/tools/kubernetes/why-kubernetes/
   
   # Завантажити нові
   python scripts/fetch_images.py "kubernetes architecture" \
     --md content/k8s.md -l 5
   ```

3. **Додавання нових зображень:**
   - Скрипт автоматично визначає наступний номер
   - Якщо є 01.png, 02.png, наступне буде 03.png

---

## Вимоги

### Python бібліотеки

```bash
pip install ddgs requests pillow
```

- **ddgs** — пошук зображень через DuckDuckGo
- **requests** — завантаження зображень
- **pillow** — аналіз розміру та формату зображень

### Структура проєкту

```
project/
├── content/
│   └── 07.tools/
│       └── 02.kubernetes/
│           └── 01.why-kubernetes.md
├── public/
│   └── images/
│       └── tools/
│           └── kubernetes/
│               └── why-kubernetes/
│                   ├── 01.png
│                   ├── 02.svg
│                   └── 03.jpg
└── scripts/
    ├── fetch_images.py
    └── insert_images.py
```

---

## Troubleshooting

### Проблема: "Зображень не знайдено"

**Рішення:**
- Спробуйте інший пошуковий запит
- Збільште ліміт: `-l 10`
- Зменште мінімальну ширину: `--min-width 600`

### Проблема: "Недостатньо зображень для всіх маркерів"

**Рішення:**
- Завантажте більше зображень: `-l 10`
- Або видаліть зайві маркери з markdown файлу

### Проблема: "Не вдалося завантажити зображення"

**Рішення:**
- Перевірте інтернет-з'єднання
- Спробуйте пізніше (можливо, сайт тимчасово недоступний)
- Використайте інтерактивний режим та виберіть інше зображення

### Проблема: Rate limiting від DuckDuckGo

**Рішення:**
- Зачекайте 1-2 хвилини між запитами
- Використовуйте VPN
- Завантажуйте зображення невеликими порціями

---

## Приклади використання

### Приклад 1: Стаття про Docker

```bash
# 1. Додати маркери у статтю
# content/docker/basics.md:
# <!-- IMAGE: docker architecture -->
# <!-- IMAGE: docker container lifecycle -->

# 2. Завантажити зображення
python scripts/fetch_images.py "docker architecture diagram" \
  --md content/docker/basics.md -l 1

python scripts/fetch_images.py "docker container lifecycle" \
  --md content/docker/basics.md -l 1

# 3. Вставити зображення
python scripts/insert_images.py content/docker/basics.md
```

### Приклад 2: Стаття про Kubernetes (інтерактивний режим)

```bash
# 1. Завантажити багато варіантів
python scripts/fetch_images.py "kubernetes architecture" \
  --md content/k8s/architecture.md -l 10 -i

# Вибрати найкращі 3 зображення вручну

# 2. Вставити зображення
python scripts/insert_images.py content/k8s/architecture.md
```

### Приклад 3: Масове завантаження для кількох статей

```bash
# Завантажити зображення для всіх статей про Kubernetes
python scripts/fetch_images.py "kubernetes architecture" \
  --md content/k8s/01.intro.md -l 3

python scripts/fetch_images.py "kubernetes pods" \
  --md content/k8s/02.pods.md -l 3

python scripts/fetch_images.py "kubernetes services" \
  --md content/k8s/03.services.md -l 3

# Вставити зображення у всі статті
python scripts/insert_images.py content/k8s/01.intro.md
python scripts/insert_images.py content/k8s/02.pods.md
python scripts/insert_images.py content/k8s/03.services.md
```

---

## Висновок

Ця система автоматизує процес пошуку, фільтрації та вставки якісних зображень у markdown статті. Основні переваги:

- ✅ Автоматична оцінка якості зображень
- ✅ Інтелектуальна нумерація
- ✅ Інтерактивний вибір
- ✅ Автоматична вставка за маркерами
- ✅ Підтримка різних форматів (SVG, PNG, JPG, WebP)
- ✅ Пріоритет офіційним джерелам

Використовуйте ці скрипти для швидкого наповнення статей якісними технічними діаграмами та схемами!
