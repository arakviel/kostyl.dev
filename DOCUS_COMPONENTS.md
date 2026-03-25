# Docus Components Reference (v4)

Повний довідник компонентів Docus для MDC (Markdown Dynamic Components) синтаксису. Ця документація призначена для точного написання компонентів — без вигадок, тільки робочий синтаксис.

---

## Зміст

1. [Callouts (Акценти)](#callouts-акценти)
2. [Cards (Картки)](#cards-картки)
3. [Code Components (Код)](#code-components-код)
4. [Accordion (Акордеон)](#accordion-акордеон)
5. [Tabs (Вкладки)](#tabs-вкладки)
6. [Steps (Кроки)](#steps-кроки)
7. [Field (Поля)](#field-поля)
8. [Collapsible (Згортання)](#collapsible-згортання)
9. [Badge (Бейджі)](#badge-бейджі)
10. [Icon (Іконки)](#icon-іконки)
11. [Kbd (Клавіші)](#kbd-клавіші)
12. [Custom: Mermaid](#custom-mermaid)
13. [Custom: PlantUML](#custom-plantuml)
14. [Custom: Educational Components (Освітні компоненти)](#custom-educational-components-освітні-компоненти)
15. [Code Block Features (MDC Magic)](#code-block-features-mdc-magic)

---

## ⚠️ Важливо: Автоформатування

При використанні автоформатерів (Prettier, тощо) закриваючі теги `::` можуть отримувати зайві пробіли на початку (2-4 пробіли). Це ламає синтаксис MDC. Як правило, воно відбувається при списках.

```markdown
::tip
**Переваги extraArgument:**

- Легше тестувати (можна передати mock api)
- Централізована конфігурація API (headers, базовий URL)
- Можна передати кілька сервісів: `thunk.withExtraArgument({ api, analytics, logger })`

::← Форматер додав пробіли! це завжди так, перед списками!
```

**Проблема:**

```markdown
::card-group

::card{title="Заголовок"}
Контент
:: ← Форматер додав пробіли!

:: ← Форматер додав пробіли!
```

**Рішення:** Додавайте порожній рядок **перед** закриваючим тегом:

```markdown
::card-group

::card{title="Заголовок"}
Контент

::

::
```

> **Правило:** Закриваючий `::` завжди має починатися з початку рядка, без будь-яких пробілів.

---

## Callouts (Акценти)

Компоненти для виділення важливої інформації. Доступні типи: `note`, `tip`, `warning`, `caution`, `callout`.

### ::note

Додатковий контекст або нейтральна інформація.

```markdown
::note
Тут розміщується додаткова інформація або примітка.
::
```

### ::tip

Корисні поради, best practices.

```markdown
::tip
Використовуйте `readonly` для незмінних полів, які ініціалізуються лише один раз.
::
```

### ::warning

Застереження, потенційні проблеми.

```markdown
::warning
Будьте обережні з цією дією — вона може мати непередбачувані наслідки.
::
```

### ::caution

Критичні застереження, небезпечні дії.

```markdown
::caution
Цю дію неможливо скасувати.
::
```

### ::callout (розширений)

Загальний компонент із підтримкою кастомних іконок та кольорів.

```markdown
::callout{icon="i-lucide-info" color="primary"}
Lorem velit voluptate ex reprehenderit ullamco et culpa.
::
```

**Атрибути:**

| Атрибут | Тип    | Опис                                        |
| ------- | ------ | ------------------------------------------- |
| `icon`  | string | Іконка (iconify формат: `i-lucide-*`)       |
| `color` | string | Колір: `primary`, `neutral`, `error`, тощо. |

---

## Cards (Картки)

### ::card-group + ::card

Картки для навігації, групування концепцій або резюме.

**✅ Рекомендований синтаксис (Frontmatter у YAML):**

```markdown
::card-group

::card{title="✅ Заголовок 1" icon="i-heroicons-magnifying-glass"}

- Пункт 1
- Пункт 2

::

::card{title="🔒 Заголовок 2" icon="i-heroicons-shield-check"}

- Пункт A
- Пункт B

::

::
```

**Атрибути ::card:**

| Атрибут  | Тип    | Опис                               |
| -------- | ------ | ---------------------------------- |
| `title`  | string | Заголовок картки                   |
| `icon`   | string | Іконка (iconify формат)            |
| `to`     | string | URL для посилання                  |
| `target` | string | Target атрибут (`_blank`, `_self`) |
| `color`  | string | Колір картки                       |

---

## Code Components (Код)

### ::code-group

Групування блоків коду у вкладки. Ідеально для порівняння синтаксису або показу команд для різних платформ.

````markdown
::code-group

```bash [pnpm]
pnpm add @nuxt/ui-pro@next
```

```bash [yarn]
yarn add @nuxt/ui-pro@next
```

```bash [npm]
npm install @nuxt/ui-pro@next
```

::
````

### ::code-tree

Візуалізація структури файлів та директорій з можливістю перегляду вмісту файлів.

````markdown
::code-tree

    ```csharp [GlobalUsings.cs]
    global using System;
    global using System.Linq;
    ```

    ```csharp [Services/UserService.cs]
    namespace MyApp.Services;
    public class UserService { }
    ```

::
````

**Особливості:**

- Шлях файлу у `[папка/файл.ext]` формує дерево директорій автоматично.
- Підтримка синтаксису підсвічування для будь-якої мови.

### ::code-collapse

Довгий код, який за замовчуванням згорнутий.

````markdown
::code-collapse

```css [main.css]
@import 'tailwindcss';
@theme {
    --font-sans: 'Public Sans', sans-serif;
    --color-green-50: #effdf5;
}
```

::
````

### ::code-preview

Демонстрація результату виконання коду (живий приклад). Лише для HTML/Vue компонентів.

```markdown
::code-preview
<button class="btn">Click me</button>
::
```

---

## Accordion (Акордеон)

Інтерактивний компонент для FAQ, деталей, що розгортаються.

```markdown
::accordion
::accordion-item{label="Що таке Docus?" icon="i-lucide-circle-help"}
Docus — це тема документації для Nuxt, побудована на Nuxt UI Pro.
::
::accordion-item{label="Як почати?" icon="i-lucide-circle-help"}
Створіть папку `content/` і почніть писати Markdown файли.
::
::
```

**Атрибути ::accordion-item:**

| Атрибут | Тип    | Опис               |
| ------- | ------ | ------------------ |
| `label` | string | Заголовок елемента |
| `icon`  | string | Іконка (iconify)   |

---

## Tabs (Вкладки)

Для групування контенту за вкладками (різні підходи, платформи).

```markdown
::tabs
::tabs-item{label="Windows"}
Встановіть через Chocolatey: `choco install dotnet`
::
::tabs-item{label="macOS"}
Встановіть через Homebrew: `brew install dotnet`
::
::tabs-item{label="Linux"}
Встановіть через APT: `sudo apt install dotnet-sdk-8.0`
::
::
```

**Атрибути ::tabs-item:**

| Атрибут | Тип    | Опис             |
| ------- | ------ | ---------------- |
| `label` | string | Назва вкладки    |
| `icon`  | string | Іконка (iconify) |

**З іконками:**

```markdown
::tabs{.w-full}
::tabs-item{icon="i-lucide-code" label="Code"}
Тут код
::
::tabs-item{icon="i-lucide-eye" label="Preview"}
Тут результат
::
::
```

---

## Steps (Кроки)

Для алгоритмів, інструкцій або логічних послідовностей.

```markdown
::steps

### Крок 1: Встановлення

Виконайте команду встановлення.

### Крок 2: Налаштування

Створіть файл конфігурації.

### Крок 3: Запуск

Запустіть проєкт.
::
```

> **Важливо:** Кожен крок починається з `###` заголовка.

---

## Field (Поля)

Для документації параметрів, властивостей API або конфігурацій.

```markdown
::field-group
::field{name="analytics" type="boolean"}
Default to `false` — Enables analytics for your project.
::
::field{name="database" type="boolean"}
Default to `false` — Enables SQL database.
::
::
```

**Атрибути ::field:**

| Атрибут    | Тип    | Опис                            |
| ---------- | ------ | ------------------------------- |
| `name`     | string | Назва параметра                 |
| `type`     | string | Тип (`boolean`, `string`, тощо) |
| `required` | bool   | Чи обов'язковий                 |
| `default`  | string | Значення за замовчуванням       |

---

## Collapsible (Згортання)

Для великих шматків коду або додаткової інформації, яку можна згорнути.

````markdown
::collapsible{title="Показати повний код"}

```typescript
// Довгий код тут
interface ComplexInterface {
    // багато властивостей
}
```

::
````

**Атрибути:**

| Атрибут | Тип    | Опис              |
| ------- | ------ | ----------------- |
| `title` | string | Заголовок кнопки  |
| `open`  | bool   | Відкрито за замовчуванням |

---

## Badge (Бейджі)

Для версій, тегів або статусів.

```markdown
::badge{color="green"}
v1.0.0
::
```

**Inline синтаксис:**

```markdown
Стаття :badge[Draft]{color="amber"}
```

**Атрибути:**

| Атрибут | Тип    | Опис                                       |
| ------- | ------ | ------------------------------------------ |
| `color` | string | `green`, `amber`, `red`, `blue`, `neutral` |

---

## Icon (Іконки)

Вбудовані іконки з Iconify.

```markdown
:icon{name="i-heroicons-check-circle" class="text-green-500"}
```

**Атрибути:**

| Атрибут | Тип    | Опис                   |
| ------- | ------ | ---------------------- |
| `name`  | string | Назва іконки (iconify) |
| `class` | string | CSS класи              |

**Формат назви іконок:**

- Heroicons: `i-heroicons-*`
- Lucide: `i-lucide-*`
- Simple Icons: `i-simple-icons-*`

---

## Kbd (Клавіші)

Відображення клавіатурних скорочень.

```markdown
Натисніть :kbd{value="Ctrl"} + :kbd{value="C"} для копіювання.
```

---

## Custom: Mermaid

Кастомний компонент для діаграм Mermaid. Рендериться клієнтською бібліотекою mermaid.js з темною темою.

**Синтаксис:**

````markdown
::mermaid

```mermaid
graph TD
    A[Start] --> B{Decision}
    B -- Yes --> C[Process]
    B -- No --> D[End]
    style A fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style B fill:#f59e0b,stroke:#b45309,color:#ffffff
    style C fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style D fill:#64748b,stroke:#334155,color:#ffffff
```

::
````

**Підтримувані типи діаграм:**

| Тип                | Використання               |
| ------------------ | -------------------------- |
| `graph`/`flowchart`| Блок-схеми, потоки даних   |
| `sequenceDiagram`  | Взаємодія між актором       |
| `classDiagram`     | UML класи                  |
| `stateDiagram-v2`  | Стани та переходи          |
| `erDiagram`        | Entity Relationship        |
| `gantt`            | Діаграми Ганта             |
| `pie`              | Кругові діаграми           |
| `timeline`         | Часові лінії               |
| `mindmap`          | Ментальні карти            |
| `gitGraph`         | Git-гілки                  |

**Рекомендована кольорова схема:**

-   Primary: `#3b82f6` (Blue)
-   Secondary: `#64748b` (Slate)
-   Accent: `#f59e0b` (Amber) — для важливих нодів
-   Text: `#ffffff` (White)

---

## Custom: PlantUML

Кастомний компонент для PlantUML діаграм. Використовує PlantUML сервер для рендерингу.

**Синтаксис (рекомендовано plain стиль):**

````markdown
::plant-uml

```plantuml
@startuml
skinparam style plain

class User {
    - id: Long
    - name: String
    + getId(): Long
    + getName(): String
}

class Order {
    - orderId: Long
    - total: BigDecimal
}

User "1" -- "*" Order : places

@enduml
```

::
````

**Атрибути:**

| Атрибут  | Тип    | За замовчуванням            | Опис                    |
| -------- | ------ | --------------------------- | ----------------------- |
| `server` | string | `https://www.plantuml.com/plantuml` | PlantUML сервер  |
| `format` | string | `svg`                       | `svg`, `png`, `txt`     |
| `alt`    | string | `PlantUML Diagram`          | Alt текст зображення    |

**Підтримувані типи діаграм:**

| Тип                | Використання                     |
| ------------------ | -------------------------------- |
| `@startuml`        | UML діаграми (class, sequence)   |
| `@startmindmap`    | Ментальні карти                  |
| `@startwbs`        | Work Breakdown Structure         |
| `@startgantt`      | Діаграми Ганта                   |
| `@startsalt`       | Wireframes                       |
| `@startjson`       | JSON візуалізація                |
| `@startyaml`       | YAML візуалізація                |

---

## Mermaid vs PlantUML: Коли що використовувати

```
┌─────────────────────────────┬───────────────────────────────────────────────┐
│         MERMAID             │              PLANTUML                         │
├─────────────────────────────┼───────────────────────────────────────────────┤
│ ✅ Flowcharts               │ ✅ Complex Class Diagrams                     │
│ ✅ Sequence (simple)        │ ✅ Detailed Sequence Diagrams                 │
│ ✅ Quick sketches           │ ✅ Database ER Diagrams                       │
│ ✅ State machines           │ ✅ Component/Deployment Diagrams              │
│ ✅ Git graphs               │ ✅ Wireframes (Salt)                          │
│ ✅ Browser-native           │ ✅ Enterprise-grade UML                       │
│                             │ ✅ Mind maps with complex layouts             │
├─────────────────────────────┼───────────────────────────────────────────────┤
│ ❌ Limited UML support      │ ❌ Requires server                            │
│ ❌ Less layout control      │ ❌ More verbose syntax                        │
│ ❌ Basic styling            │ ❌ Slower rendering                           │
└─────────────────────────────┴───────────────────────────────────────────────┘
```

### Рекомендації:

| Сценарій                        | Вибір    |
| ------------------------------- | -------- |
| Швидка блок-схема алгоритму     | Mermaid  |
| Детальна UML-діаграма класів    | PlantUML |
| Sequence diagram (до 5 акторів) | Mermaid  |
| Sequence diagram (5+ акторів)   | PlantUML |
| ER-діаграма бази даних          | PlantUML |
| Стан-машина (state diagram)     | Обидва   |
| Mind map з групуванням          | PlantUML |
| Простий таймлайн                | Mermaid  |
| Діаграма компонентів системи    | PlantUML |
| Git flow візуалізація           | Mermaid  |

---

## Custom: Educational Components (Освітні компоненти)

Ця серія компонентів розроблена спеціально для проєкту `kostyl.dev` для візуалізації концепцій програмування, низькорівневих структур та результатів виконання коду. Всі компоненти підтримують macOS-стилістику та адаптивні до світлої/темної тем.

### ::terminal-preview

Компонент для демонстрації **роботи** з консольними програмами (CLI) або виводу коду в стилі macOS Terminal.

> [!IMPORTANT]
> На відміну від стандартних блоків коду, `terminal-preview` орієнтований на показ **результатів виконання** та взаємодії користувача з терміналом.

**Синтаксис (CLI Usage):**

```markdown
::terminal-preview{title="dotnet run" :cursor="true"}
<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">dotnet run</strong></div>
<div class="line"><span class="text-green-400 font-bold">SUCCESS:</span> Build completed in 1.8s.</div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">Hello, kostyl.dev!</span></div>
<div class="line">Execution finished with <span class="text-green-400 font-bold">exit code 0</span>.</div>
::
```

**Атрибути:**

| Атрибут       | Тип     | За замовчуванням | Опис                                                                 |
| ------------- | ------- | ---------------- | ------------------------------------------------ |
| `title`       | string  | `bash`           | Заголовок вікна                                  |
| `showButtons` | boolean | `true`           | Показувати кнопки macOS                          |
| `cursor`      | boolean | `false`          | Додає блимаючий курсор у кінці                   |
| `expandable`  | boolean | `false`          | Додає можливість розгортання довгого виводу      |
| `maxHeight`   | string  | `320px`          | Максимальна висота у згорнутому стані            |

**Стилізація контенту:**

Для досягнення "преміального" вигляду використовуйте наступні паттерни всередині слота:

1.  **Рядки**: Огортайте кожен рядок у `<div class="line">...</div>` для чіткого вертикального розділення.
2.  **Промпт (Запит)**: Використовуйте `<span class="opacity-40">$</span>` для імітації системного символу. Опційно додайте `mr-2`.
3.  **Кольори**: Використовуйте Tailwind класи:
    -   `text-green-400` — успіх, позитивні статуси.
    -   `text-blue-400` — інформаційні повідомлення, акценти.
    -   `text-yellow-400` — попередження.
    -   `text-rose-400` — помилки.
    -   `text-gray-400` або `opacity-40` — другорядний текст (шляхи, дати).
4.  **Жирний текст**: 
    -   Використовуйте клас `font-bold`.
    -   Альтернативно: теги `<strong>` або `<b>`.
    -   > [!WARNING]
    -   > Майте на увазі, що Markdown-символи (наприклад, `**брудний**`) можуть **не розпізнаватися** всередині сирих HTML-тегів на кшталт `<div>`. У таких випадках використовуйте HTML-теги або MDC-синтаксис (`:strong[текст]`).

---

### ::html-preview

Візуалізація результату рендерингу HTML/CSS у стилі вікна браузера macOS Chrome.

**Синтаксис:**

````markdown
::html-preview
```html
<div class="p-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-3xl text-white shadow-xl">
  <h1 class="text-3xl font-black mb-4">Привіт, Tailwind v4!</h1>
  <button class="mt-4 px-6 py-2 bg-white text-indigo-600 font-bold rounded-full">
    Натисни мене
  </button>
</div>
```
::
````

**Особливості:**
- Автоматично рендерить перший знайдений блок коду всередині.
- Декоративний інтерфейс Chrome: адресний рядок `localhost:3000`, вкладка з фавіконкою `kostyl.dev` та кнопки macOS.

---

### ::premium-alert

Високоякісний компонент для виділення важливих думок, порад або застережень. На відміну від стандартних callouts, має ефекти глибокої прозорості (glassmorphism), текстуру шуму та мікро-анімації.

**Синтаксис:**

```markdown
::premium-alert{type="tip" title="Best Practice"}
Використовуйте `MemoryView` для візуального пояснення вказівників (pointers).
::
```

**Атрибути:**

| Атрибут | Тип    | За замовчуванням | Опис                                             |
| ------- | ------ | ---------------- | ------------------------------------------------ |
| `type`  | string | `info`           | Тип: `tip`, `info`, `warning`, `danger`          |
| `title` | string | `undefined`      | Заголовок акценту                                |

**Поведінка**: При наведенні іконка повертається і масштабується, а фоновий "glow" ефект стає яскравішим.

---

### ::debugger-view

Візуалізація стану програми (змінних, регістрів) у стилі дебаг-панелі сучасних IDE (Xcode, VS Code).

**Синтаксис:**

```markdown
::debugger-view{title="Local Variables" :variables='[{"name": "pAddress", "type": "uintptr_t", "value": "0x00007FF7BFEFF5A0"}, {"name": "status", "type": "char", "value": "K"}]'}
::
```

**Атрибути:**

| Атрибут     | Тип   | Опис                                                |
| ----------- | ----- | --------------------------------------------------- |
| `title`     | string| Заголовок секції (наприклад, "Registers" або "Watch")|
| `variables` | array | Список об'єктів `{name, type, value}`               |

---

### ::memory-view

Елемент для візуалізації сирих даних у пам'яті (Hex Dump). Ідеально для пояснення адресації, структур даних та вказівників у низькорівневих мовах.

**Синтаксис:**

```markdown
::memory-view{title="Stack Memory" startAddress="0x004014A0" :data='[72, 137, 92, 36, 8, 107, 111, 115, 116, 121, 108]' :highlight="[0, 1, 2, 5, 6, 7]"}
::
```

**Атрибути:**

| Атрибут        | Тип    | Опис                                                 |
| -------------- | ------ | ---------------------------------------------------- |
| `title`        | string | Заголовок вікна                                      |
| `startAddress` | string | Початкова адреса в HEX (н-д: `0x00401000`)           |
| `data`         | array  | Масив байтів (числа 0-255 або HEX рядки)              |
| `highlight`    | array  | Індекси байтів, які потрібно підсвітити (акцентом)   |
| `rowSize`      | number | Кількість байтів у одному рядку (default: 16)        |

**Особливості**: Використовує CSS Grid для ідеального вирівнювання ASCII-колонки. Підтримує підсвітку важливих зон пам'яті.

---

## Code Block Features (MDC Magic)

### Line Numbers

Додавання нумерації рядків:

````markdown
```typescript showLineNumbers
const x = 1
const y = 2
```
````

### Highlighting (підсвічування рядків)

**Через атрибут:**

```markdown
```typescript {1,3-5}
const highlighted = true;
const normal = false;
const alsoHighlighted = true;
```

**Через коментар:**

```typescript
const normal = false;
const highlighted = true; // [!code highlight]
```

### Diffs (показ змін)

```typescript
const old = true; // [!code --]
const new = false; // [!code ++]
```

### Focus (фокус уваги)

```typescript
const normal = 1
const focused = 2 // [!code focus]
const normal2 = 3
```

### Filename (назва файлу)

````markdown
```typescript [app.config.ts]
export default defineAppConfig({})
```
````

---

## Загальний синтаксис MDC

### Inline компоненти

```markdown
:component-name[слот]{атрибут="значення"}
```

Приклади:

---

## Custom: Docker Desktop GUI (Освітні компоненти)

Спеціальний набір компонентів, що імітує інтерфейс Docker Desktop. Ідеально підходить для візуальних інструкцій та гайдів.

### ::docker-desktop
Головний контейнер (вікно додатка), що містить сайдбар та хедер.

**Атрибути:**
| Атрибут | Тип | За замовчуванням | Опис |
| --- | --- | --- | --- |
| `activeTab` | string | `containers` | Активний пункт меню (`containers`, `images`, `volumes`, `builds`, `dev-envs`, `extensions`) |
| `os` | string | `mac` | Стиль вікна (`mac` або `windows`) |

### ::docker-list та ::docker-list-item
Компоненти для імітації таблиці зі списком контейнерів або образів.

**Синтаксис:**
```markdown
::docker-desktop{activeTab="containers"}
  ::docker-list{title="Containers" :showActions="true"}
    ::docker-list-item{name="kostyl-web" image="node:20" status="running" ports="3000:3000"}
    ::
    ::docker-list-item{name="kostyl-db" image="postgres:15" status="exited" highlight="play"}
    ::
  ::
::
```

**Атрибути `::docker-list-item`:**
| Атрибут | Тип | Опис |
| --- | --- | --- |
| `name` | string | Назва контейнера |
| `image` | string | Назва образу |
| `status` | string | Статус (`running`, `exited`, `error`) |
| `ports` | string | Рядок з портами (напр. `8080:80`) |
| `highlight` | string | Опціональна підсвітка кнопок: `play` або `delete` |

### ::docker-settings
Компонент для імітації сторінки налаштувань Docker Desktop (зокрема для пояснення WSL Integration або Docker Engine).

**Синтаксис:**
```markdown
::docker-desktop{activeTab="settings"}
  ::docker-settings{activeSection="docker-engine"}
    Тут контент налаштувань, наприклад JSON редактор або чекбокси.
  ::
::
```

**Атрибути `::docker-settings`:**
| Атрибут | Тип | Опис |
| --- | --- | --- |
| `activeSection` | string | Відкритий розділ (`general`, `resources`, `docker-engine`, `builder`, `kubernetes`) |

```markdown
:badge[v1.0]{color="green"}
:icon{name="i-heroicons-star"}
:kbd[Ctrl]
```

### Block компоненти

```markdown
::component-name{атрибут="значення"}
Контент (default slot)
::
```

### Вкладені компоненти (кількість `:` має збільшуватись)

```markdown
::parent
:::child
Content
:::
::
```

### YAML Frontmatter атрибути

```markdown
## ::component

title: Заголовок
icon: i-heroicons-star
to: /link

---

Контент
::
```

---

## Перелік усіх компонентів

| Компонент        | Тип    | Призначення                        |
| ---------------- | ------ | ---------------------------------- |
| `accordion`      | block  | Розгортаємий FAQ                   |
| `accordion-item` | nested | Елемент акордеону                  |
| `badge`          | inline | Версії, теги, статуси              |
| `callout`        | block  | Загальний callout з налаштуваннями |
| `card`           | block  | Картка контенту                    |
| `card-group`     | block  | Група карток                       |
| `caution`        | block  | Критичне застереження              |
| `code-collapse`  | block  | Згорнутий блок коду                |
| `code-group`     | block  | Вкладки з кодом                    |
| `code-icon`      | inline | Іконка поруч з кодом               |
| `code-preview`   | block  | Preview результату                 |
| `code-tree`      | block  | Дерево файлів з кодом              |
| `collapsible`    | block  | Згортаємий контент                 |
| `field`          | block  | Документація параметра             |
| `field-group`    | block  | Група полів                        |
| `icon`           | inline | Іконка Iconify                     |
| `kbd`            | inline | Клавіатурна клавіша                |
| `note`           | block  | Примітка                           |
| `steps`          | block  | Покрокова інструкція               |
| `tabs`           | block  | Вкладки контенту                   |
| `tabs-item`      | nested | Елемент вкладки                    |
| `tip`            | block  | Корисна порада                     |
| `warning`        | block  | Застереження                       |
| `mermaid`        | custom | Mermaid діаграми                   |
| `plant-uml`      | custom | PlantUML діаграми                  |
| **Освітні**      |        |                                    |
| `terminal-preview`| block  | CLI/Terminal macOS вікно           |
| `html-preview`   | block  | Браузерне вікно macOS Chrome       |
| `premium-alert`  | block  | Glassmorphism акценти з текстурою  |
| `debugger-view`  | block  | Стан змінних (IDE style)           |
| `memory-view`    | block  | Hex Dump / Memory visualizer       |

---

> **Останнє оновлення:** Березень 2026
