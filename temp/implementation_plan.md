# План модуля CSS (content/12.html-css)

Існуючі 8 статей (01–08) покривають HTML. Наступні 10 статей покривають CSS — від базових концепцій до сучасних технік. Кожна стаття ~800–1200 рядків, дотримується структури `prompt.md` і активно використовує компоненти Docus.

---

## Proposed Changes

### Модуль CSS — 10 нових файлів

---

#### [NEW] [09.css-intro-selectors.md](file:///y:/Work/kostyl.dev/content/12.html-css/09.css-intro-selectors.md)

**Вступ до CSS. Селектори**

**Hook**: Чому одна веб-сторінка виглядає як шедевр дизайну, а інша — як текстовий файл 1992 року?

**Ключові теми:**

- Що таке CSS і каскадність (Cascading)
- Три способи підключення CSS: inline, `<style>`, зовнішній файл — переваги та недоліки кожного
- Синтаксис правила CSS: селектор, властивість, значення
- Типи селекторів: тегові, класи (`.`), ідентифікатори (`#`), атрибутні (`[attr]`)
- Комбінатори: нащадок (` `), дочірній (`>`), сусід (`+`), загальний сусід (`~`)
- Pseudo-класи: `:hover`, `:focus`, `:nth-child()`, `:not()`, `:first-child`, `:last-child`
- Pseudo-елементи: `::before`, `::after`, `::first-line`, `::placeholder`
- Специфічність (Specificity): розрахунок ваги (інлайн / id / клас / тег)
- Каскад: порядок, специфічність, `!important` (і чому його слід уникати)

**Docus компоненти:**

- `::mermaid` — діаграма ваг специфічності (0,0,0,0)
- `::tabs` — порівняння трьох способів підключення CSS
- `::card-group` — картки типів селекторів
- `::steps` — покроковий алгоритм визначення специфічності
- `::warning` — `!important` як анти-патерн

---

#### [NEW] [10.css-box-model.md](file:///y:/Work/kostyl.dev/content/12.html-css/10.css-box-model.md)

**Блокова модель CSS. Відступи. Box Sizing**

**Hook**: Чому елемент шириною `width: 200px` займає 240px у browser inspection?

**Ключові теми:**

- Блокова модель (Box Model): content, padding, border, margin
- `width` та `height` — що насправді вимірюється
- `box-sizing: content-box` vs `box-sizing: border-box` — революційна різниця
- `margin: auto` та центрування блоків
- Колапс марджинів (Margin Collapse) — один з найбільших сюрпризів CSS
- `display: block`, `inline`, `inline-block` — коли що використовувати
- `overflow`: `hidden`, `scroll`, `auto`, `clip`
- `visibility` vs `display: none` — різниця в поведінці та доступності

**Docus компоненти:**

- Схема блокової моделі як `::mermaid` або `::plant-uml`
- `::tabs` — `content-box` vs `border-box` з live прикладами
- `::note` — пояснення margin collapse
- `::caution` — поширена помилка з `width: 100% + padding`
- Завдання 3 рівнів складності

---

#### [NEW] [11.css-typography.md](file:///y:/Work/kostyl.dev/content/12.html-css/11.css-typography.md)

**Типографіка в CSS. Шрифти. Текст**

**Hook**: Чому деякі сайти читаються легко, а інші — немов через матове скло?

**Ключові теми:**

- `font-family` та стек шрифтів (font stack): системні, веб-безпечні, Google Fonts
- `@font-face` та підключення власних шрифтів
- `font-size`: px, em, rem — різниця та коли що використовувати
- `font-weight`, `font-style`, `font-variant`
- Скорочення `font`
- `line-height` — оптимальне значення для читабельності
- `letter-spacing`, `word-spacing`
- `text-align`, `text-decoration`, `text-transform`
- `text-overflow: ellipsis` — обрізання тексту
- Одиниці виміру: `px`, `em`, `rem`, `%`, `vw`, `vh`, `ch`
- CSS змінні (`--custom-properties`) для системи типографіки

**Docus компоненти:**

- `::tabs` — em vs rem з інтерактивним прикладом наслідування
- `::card-group` — Google Fonts vs system fonts vs `@font-face`
- `::tip` — правило золотого перетину для `line-height`
- `::mermaid` — дерево наслідування `em` в DOM
- `::accordion` — детальний розбір всіх одиниць виміру

---

#### [NEW] [12.css-colors-backgrounds.md](file:///y:/Work/kostyl.dev/content/12.html-css/12.css-colors-backgrounds.md)

**Кольори та фони в CSS**

**Hook**: Чому кольори в CSS задають п'ятьма різними способами — і який з них правильний?

**Ключові теми:**

- Колірні моделі: `hex`, `rgb()`, `rgba()`, `hsl()`, `hsla()`, `oklch()`
- CSS Custom Properties (змінні) для кольорової теми
- `background-color`, `background-image`, `background-size`, `background-position`
- Градієнти: `linear-gradient`, `radial-gradient`, `conic-gradient`
- `background-repeat`, `background-attachment` (parallax effect)
- Скорочення `background`
- Кілька фонів (`multiple backgrounds`)
- `opacity` і `rgba` — різниця між прозорістю елемента та кольору
- CSS-змінні для темної/світлої теми (`prefers-color-scheme`)

**Docus компоненти:**

- `::tabs` — hex/rgb/hsl/oklch порівняння з візуальними прикладами
- `::mermaid` — схема HSL кола кольорів
- `::tip` — коли використовувати `oklch` для доступності
- `::code-group` — приклади градієнтів (linear, radial, conic)
- `::warning` — `opacity: 0` впливає на дочірні елементи; `rgba` — ні

---

#### [NEW] [13.css-layout-flexbox.md](file:///y:/Work/kostyl.dev/content/12.html-css/13.css-layout-flexbox.md)

**CSS Flexbox. Гнучкий макет**

**Hook**: Як горизонтально та вертикально відцентрувати елемент — те, що роками займало 5 рядків CSS-хаків, тепер вирішується двома.

**Ключові теми:**

- Проблема до Flexbox: `float`, `inline-block`, `table-cell` — чому це хаки?
- `display: flex` — контейнер та елементи
- Головна вісь та поперечна вісь (main axis / cross axis)
- `flex-direction`: `row`, `column`, `row-reverse`, `column-reverse`
- `justify-content`: `flex-start`, `center`, `space-between`, `space-around`, `space-evenly`
- `align-items` та `align-self`
- `flex-wrap` та `align-content`
- `flex-grow`, `flex-shrink`, `flex-basis` — деталі скорочення `flex`
- `order` та `gap`
- Практика: navigation bar, card grid, sticky footer, centering

**Docus компоненти:**

- `::mermaid` — схема осей Flexbox
- `::tabs` — justify-content vs align-items (з візуальними прикладами)
- `::card-group` — головні властивості контейнера і елементів
- `::steps` — побудова навігаційного меню крок за кроком
- `::tip` — `gap` замість margin-хаків

---

#### [NEW] [14.css-layout-grid.md](file:///Users/arakviel/Work/kostyl.dev/content/12.html-css/14.css-layout-grid.md) ✅ Створено (1052 рядки)

**CSS Grid. Двовимірний макет. Частина 1**

**Hook**: Flexbox вміє розкладати елементи в один рядок або стовпець. Що робити, коли потрібна справжня двовимірна сітка?

---

#### [NEW] [14b.css-layout-grid-advanced.md](file:///Users/arakviel/Work/kostyl.dev/content/12.html-css/14b.css-layout-grid-advanced.md) ✅ Створено (1143 рядки)

**CSS Grid. Двовимірний макет. Частина 2 (Named Areas, вирівнювання, практика)**

**Ключові теми:**

- `display: grid` — контейнер та grid-елементи
- `grid-template-columns`, `grid-template-rows`
- Одиниця `fr` (fractional unit)
- `repeat()`, `minmax()`, `auto-fill`, `auto-fit`
- Розміщення елементів: `grid-column`, `grid-row`, `span`
- `grid-area` та `grid-template-areas` (named areas)
- `gap` (row-gap, column-gap)
- Явна та неявна сітки (`grid-auto-rows`, `grid-auto-flow`)
- `place-items`, `place-content`, `place-self`
- Flexbox vs Grid: коли що обирати
- Практика: класичний page layout, card masonry

**Docus компоненти:**

- `::plant-uml` або `::mermaid` — схема Grid з named areas
- `::tabs` — Flexbox vs Grid (порівняння)
- `::card-group` — explicit grid vs implicit grid
- `::code-group` — `auto-fill` vs `auto-fit`
- `::steps` — побудова повноцінного page layout

---

#### [NEW] [15.css-positioning.md](file:///y:/Work/kostyl.dev/content/12.html-css/15.css-positioning.md)

**Позиціонування в CSS. Z-index. Stacking Context**

**Hook**: Чому `z-index: 9999` інколи не допомагає підняти елемент поверх іншого? Відповідь — в stacking context.

**Ключові теми:**

- `position: static` (за замовчуванням)
- `position: relative` — зміщення без виходу з потоку
- `position: absolute` — абсолютне позиціонування відносно позиціонованого предка
- `position: fixed` — відносно viewport
- `position: sticky` — hybrid між relative і fixed
- Властивості `top`, `right`, `bottom`, `left`
- `z-index` та stacking context (контекст накладання)
- Що створює новий stacking context: `transform`, `opacity < 1`, `filter`, `isolation: isolate`
- Практика: tooltip, modal overlay, sticky header, dropdown menu

**Docus компоненти:**

- `::mermaid` — схема stacking context (дерево контекстів)
- `::tabs` — `absolute` vs `fixed` vs `sticky`
- `::warning` — `z-index` без `position` не працює
- `::caution` — `transform` скидає `position: fixed` відносно viewport
- `::accordion` — типові кейси для кожного `position`

---

#### [NEW] [16.css-responsive-media-queries.md](file:///y:/Work/kostyl.dev/content/12.html-css/16.css-responsive-media-queries.md)

**Адаптивний дизайн. Media Queries**

**Hook**: У 2024 році понад 60% веб-трафіку — мобільні пристрої. Як зробити один сайт для всіх екранів?

**Ключові теми:**

- Що таке адаптивний дизайн (Responsive Web Design)
- `<meta name="viewport">` — чому без нього мобільний вигляд зламаний
- `@media` — синтаксис та типи: `screen`, `print`, `prefers-color-scheme`, `prefers-reduced-motion`
- Media features: `min-width`, `max-width`, `orientation`, `resolution`
- Mobile-first vs Desktop-first підхід
- Breakpoints: стандартні значення (320, 480, 768, 1024, 1280, 1920)
- Responsive images: `max-width: 100%`, `<picture>`, `srcset`
- Fluid typography: `clamp()`, `vw`-based fonts
- Container Queries (новинка): `@container`

**Docus компоненти:**

- `::mermaid` — timeline еволюції підходів (fixed → fluid → responsive → container)
- `::tabs` — Mobile-first vs Desktop-first з прикладами коду
- `::card-group` — breakpoints та їх призначення
- `::tip` — `clamp()` як замінник медіа-запитів для типографіки
- `::steps` — конвертація desktop-макету в responsive

---

#### [NEW] [17.css-animations-transitions.md](file:///y:/Work/kostyl.dev/content/12.html-css/17.css-animations-transitions.md)

**CSS Анімації та Переходи**

**Hook**: Що відрізняє хороший UX від чудового? Часто — це 200мс плавного переходу, яких ви майже не помічаєте, але їх відсутність вас дратує.

**Ключові теми:**

- `transition`: властивість, тривалість, функція часу, затримка
- Функції часу: `ease`, `linear`, `ease-in`, `ease-out`, `ease-in-out`, `cubic-bezier()`
- Що можна анімувати: `transform`, `opacity`, `color` (GPU-accelerated vs layout-affecting)
- `transform`: `translate()`, `rotate()`, `scale()`, `skew()`, `matrix()`
- `@keyframes` та `animation`
- Властивості `animation`: `name`, `duration`, `timing-function`, `delay`, `iteration-count`, `direction`, `fill-mode`, `play-state`
- `will-change` — підказка браузеру для оптимізації
- `prefers-reduced-motion` — доступність анімацій
- Практика: hover effects, loading spinner, fade-in, slide-in

**Docus компоненти:**

- `::tabs` — `transition` vs `@keyframes animation`
- `::mermaid` — порівняння GPU-accelerated vs layout-affecting властивостей
- `::tip` — `transform` і `opacity` — найбезпечніші для анімації
- `::warning` — `animation: all` — чому погано
- `::caution` — завжди додавати `prefers-reduced-motion`

---

#### [NEW] [18.css-variables-methodologies.md](file:///y:/Work/kostyl.dev/content/12.html-css/18.css-variables-methodologies.md)

**CSS Custom Properties. Методології. Сучасний CSS**

**Hook**: Як великі команди пишуть CSS без хаосу? Як Dark Mode вмикається одним рядком? Відповідь — CSS Custom Properties та чіткі методології.

**Ключові теми:**

- CSS Custom Properties (змінні): `--variable`, `var()`, `fallback`
- Область видимості (scope): `:root` vs локальні змінні
- Динамічна зміна змінних через JavaScript
- CSS Препроцесори: огляд Sass/SCSS — навіщо існували і чи потрібні зараз?
- Методології іменування CSS: BEM, SMACSS, OOCSS — принципи та приклади
- BEM детально: Block, Element, Modifier (синтаксис і практика)
- Utility-First CSS: принцип Tailwind CSS (без самого Tailwind)
- Сучасний CSS 2024: `@layer`, `@scope`, `nesting` (нативний CSS Nesting)
- CSS Reset vs Normalize vs Modern CSS Reset

**Docus компоненти:**

- `::tabs` — BEM vs Utility-first vs Component-based
- `::mermaid` — схема BEM структури блоків
- `::card-group` — порівняння методологій (BEM / SMACSS / OOCSS)
- `::code-group` — `@layer` оголошення
- `::tip` — CSS Custom Properties повністю замінюють Sass змінні

---

## Загальні принципи написання

Кожна стаття:

- Починається з **Hook** (проблема або реальний сценарій)
- Містить мінімум **2 діаграми** (Mermaid або PlantUML)
- Використовує **Docus компоненти** для інтерактивності
- Завершується **3 рівнями завдань** (базовий / логіка / архітектура)
- Написана **українською мовою** з англійськими термінами в дужках при першому вжитку
- Обсяг: **800–1400 рядків**

## Verification Plan

### Manual Verification

Після написання кожної статті:

1. Відкрити файл у VS Code та перевірити MDC-синтаксис (закриваючі `::` без пробілів)
2. Запустити dev-сервер Docus (`npm run dev`) та перевірити відображення компонентів у браузері
3. Перевірити, що всі `::mermaid` і `::plant-uml` діаграми рендеряться коректно
4. Перевірити, що `::tabs`, `::accordion`, `::steps` працюють інтерактивно
5. Переконатись у наявності завдань трьох рівнів у кожній статті
