# React + TypeScript: Повна навчальна програма

::card-group

::card{title="🎯 Мета курсу" icon="i-lucide-target"}

- Опанувати бібліотеку React із TypeScript від перших компонентів до повноцінного продакшн-стеку.
- Побудувати впевнене розуміння декларативного підходу до побудови інтерфейсів, управління станом та роботи з побічними ефектами.
- Освоїти екосистему: React Router, Redux Toolkit, RTK Query, React Hook Form, Zod, Axios, Vitest, Framer Motion, i18next.

::

::card{title="🔑 Передумови" icon="i-lucide-key"}

- Впевнене володіння HTML, CSS та JavaScript (ES6+).
- Базове розуміння TypeScript: типи, інтерфейси, дженерики, модулі.
- Встановлені Node.js (≥ 18) та пакетний менеджер npm або pnpm.

::

::card{title="📚 Структура курсу" icon="i-lucide-book-open"}

- **Вступ.** Створення проєкту (01) — еволюція від CDN HTML до Vite + React + TS.
- **Частина I.** Основи React (02–11) — філософія, JSX/TSX, компоненти, CSS Modules, пропси, списки, чистота компонентів, UI як дерево.
- **Частина II.** Додавання інтерактивності (12–18) — події, `useState`, рендер і коміт, знімки стану, черга оновлень, мутації об'єктів та масивів.
- **Частина III.** Управління станом (19–24) — декларативний UI, структура стану, підйом стану, збереження та скидання, `useReducer`, Context API.
- **Частина IV.** Запасні виходи (25–32) — рефи для значень і DOM, життєвий цикл ефектів, оптимізація синхронізації, кастомні хуки.
- **Частина V.** Екосистема React (33–42) — Router, Axios, Redux Classic & Toolkit, Zustand, TanStack Query / RTK Query, RHF + Zod / Yup, Framer Motion, Vitest, i18next.
- **Частина VI.** Оптимізація продуктивності (43–44) — `useMemo`, `useCallback`, `React.memo`.

::

::

---

## 📌 Методичні вимоги та інтеграція референсів react.dev

Кожна тема навчального курсу спирається на офіційну документацію **React.dev** як на **первинний концептуальний референс**:

1. **🔗 Референсна прив'язка:** До кожного матеріалу ядра React додано пряме посилання на відповідний розділ `uk.react.dev/learn` як базовий референс.
2. **📦 Обов'язкове витягування ВСІХ інтерактивних Sandbox-прикладів:**
   - Усі живі пісочниці (*Sandpack / CodeSandbox*) з офіційної документації **мусять бути повністю витягнуті** у навчальний матеріал.
   - Усі приклади коду з чистого JavaScript мають бути адаптовані під **строгий TypeScript (TSX)** із чітким визначенням інтерфейсів (`interface`), типізацією пропсів, подій та дженериків.
   - Багатофайлові sandbox-проєкти оформлюються через компонент Docus `::code-group` (з окремими вкладками для компонентів, типів та стилів) із розгорнутим текстовим коментарем до ключових рядків.
3. **🎯 Обов'язкове витягування ВСІХ практичних завдань (Challenges):**
   - У кінці кожної статті react.dev міститься блок тренувальних челенджів (*«Спробуйте виконати завдання»*).
   - Усі без винятку практичні завдання **повинні бути витягнуті** у відповідний матеріал нашого курсу.
   - Оформлення завдань здійснюється строго через компонент Docus `::::accordion`:
     - `:::accordion-item{label="📋 Завдання: [Назва]" icon="i-lucide-clipboard-list"}` — постановка задачі, вихідний код із помилкою або прогалиною та критерії успішного виконання.
     - `:::accordion-item{label="✅ Розв'язок та покроковий аналіз" icon="i-lucide-check-circle"}` — повністю робочий типізований код розв'язку та покрокове інженерне пояснення логіки розв'язання.

---

---

# 📁 Каталог практичних навчальних проєктів курсу (Hands-on Projects)

Усі практичні проєкти курсу систематизовані, протестовані та розміщені у відповідних модульних папках із чіткою наскрізною нумерацією від `01` до `X`. Кожен проєкт є завершеним, готовим до запуску застосунком із власною архітектурою та методичною метою.

| № | Модуль / Тема | Назва проєкту | Стек технологій | Основний фокус та ключові можливості |
|---|---|---|---|---|
| 01 | **04-context-api** | [01-shopping-cart](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/04-context-api/01-shopping-cart) | React 19, Vite, Context API | Кошик інтернет-магазину: CartContext, CartProvider, розрахунок суми, додавання/видалення товарів |
| 02 | **04-context-api** | [02-ticket-booking-system](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/04-context-api/02-ticket-booking-system) | React 19, Vite, Multi-Context | Багатокрокове бронювання квитків: вибір події, місць у залі (SeatSelection), оформлення замовлення |
| 03 | **06-effects-and-lifecycle** | [01-react-effects-sample](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/06-effects-and-lifecycle/01-react-effects-sample) | React 19, Vite | Анатомія `useEffect`: залежності, очищення підписок/таймерів, асинхронні ефекти, попередні значення |
| 04 | **06-effects-and-lifecycle** | [02-react-lifecycle-and-effects](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/06-effects-and-lifecycle/02-react-lifecycle-and-effects) | React 19, Vite, CSS Modules | Практичні кейси ефектів: секундомір, таймер, Dropdown (клік поза межами), OnlineStatus, оптимізація пошуку |
| 05 | **08-portals** | [01-react-portals](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/08-portals/01-react-portals) | React 19, ReactDOM, Vite | Портали: `createPortal`, модальні вікна, випадаючі списки без overflow, контекстне меню, Toast-сповіщення |
| 06 | **09-forms-and-validation** | [01-react-form-validation](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/09-forms-and-validation/01-react-form-validation) | React 19, Vite, RHF, Yup | Форми з валідацією: `react-hook-form`, валідаційні схеми Yup, контрольовані поля, модальне підтвердження |
| 07 | **11-react-router-v7** | [01-react-router-sample](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/11-react-router-v7/01-react-router-sample) | React 19, Vite, React Router v7 | Повноцінне SPA: Layout, динамічні `/products/:id`, пошукові URL-параметри, ProtectedRoute, Dashboard, ErrorBoundary |
| 08 | **11-react-router-v7** | [02-react-router-sample-clean](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/11-react-router-v7/02-react-router-sample-clean) | React 19, Vite 7, React Router 7.9 | Чистий шаблон React Router v7 без сторонніх компіляторних плагінів для студентської практики |
| 09 | **12-redux** | [01-redux-vanilla-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/01-redux-vanilla-counter) | Redux 4 (Vanilla JS), HTML5 | Redux з нуля в одному HTML/JS файлі: `createStore`, `getState`, `dispatch`, `subscribe` без фреймворків |
| 10 | **12-redux** | [02-redux-vanilla-todo](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/02-redux-vanilla-todo) | Redux 4 (Vanilla JS), HTML5 | Модульний чистий Redux: actionTypes, actions, редюсер списку задач, маніпуляція DOM через subscribe |
| 11 | **12-redux** | [03-redux-react-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/03-redux-react-counter) | React 19, Redux, react-redux | Перша інтеграція з React: `<Provider store={store}>`, хуки `useSelector` та `useDispatch` |
| 12 | **12-redux** | [04-redux-react-todo](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/04-redux-react-todo) | React 19, Redux, react-redux | React TodoList на класичному Redux: структуровані action creators, редюсер, локальний стан + глобальний стор |
| 13 | **12-redux** | [05-redux-classic-bookstore-thunk](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/05-redux-classic-bookstore-thunk) | React 19, Redux, redux-thunk | Книгарня на класичному Redux: фільтрація, статистика, порівняння HOC `connect()` з хуками, thunk middleware |
| 14 | **12-redux** | [06-rtk-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/06-rtk-counter) | React 19, Redux Toolkit, Vite | Сучасний Redux Toolkit (RTK): `createSlice`, `configureStore`, автоматичні екшени, Immer під капотом |
| 15 | **12-redux** | [07-rtk-bookstore-async](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/07-rtk-bookstore-async) | React 19, RTK, Axios, json-server | Повноцінний RTK BookStore: асинхронні санки `createAsyncThunk`, REST API, обробка pending/fulfilled/rejected |
| 16 | **13-zustand** | [01-zustand-todo-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/13-zustand/01-zustand-todo-counter) | React 19, Zustand, Vite | Основи Zustand: створення сторів `create()`, селектори, мутація через `set()`, робота без провайдерів |
| 17 | **13-zustand** | [02-zustand-bookstore](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/13-zustand/02-zustand-bookstore) | React 19, Zustand, json-server | Книгарня на Zustand: асинхронні дії прямо у сторі, фільтрація, обчислювана статистика, інтеграція з API |
| 18 | **14-tanstack-query** | [01-tanstack-query-starter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/14-tanstack-query/01-tanstack-query-starter) | React 19, Vite | Стартовий шаблон для виконання практичних завдань із підключення TanStack Query з нуля |
| 19 | **14-tanstack-query** | [02-tanstack-query-demo](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/14-tanstack-query/02-tanstack-query-demo) | Next.js, TanStack Query v5, shadcn/ui | Професійний додаток: QueryClient, useQuery, useMutation, інвалідація кешу, пагінація, нескінченний скрол |

---

# Вступ. Створення проєкту

## 01. Від одного HTML-файлу до повноцінного проєкту

> 🔗 **Офіційний референс:** [Побудова React-застосунку з нуля (Build a React App from Scratch)](https://uk.react.dev/learn/build-a-react-app-from-scratch) та [Встановлення (Installation)](https://uk.react.dev/learn/installation)
> 📥 **Вимога до наповнення статті:** Витягнути всі інтерактивні sandbox-приклади з CDN/Babel та практичні завдання з налаштування оточення.

Перш ніж занурюватися в компоненти та хуки, важливо зрозуміти, **як саме React-код потрапляє до браузера**. Ми пройдемо цей шлях еволюційно — від найпростішого способу до продакшн-готового інструментарію.

### Етап перший: один HTML-файл із Babel у браузері

Найшвидший спосіб почати експериментувати з React — це один HTML-файл, де бібліотека Babel компілює JSX прямо у браузері. Жодних інструментів збірки, жодного терміналу — достатньо текстового редактора та браузера:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8" />
  <title>React без збірки</title>
</head>
<body>
  <div id="root"></div>

  <!-- Підключаємо React із CDN -->
  <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>

  <!-- Babel компілює JSX прямо в браузері -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <script type="text/babel">
    function Greeting() {
      return <h1>Привіт, React без жодної збірки!</h1>;
    }

    const root = ReactDOM.createRoot(document.getElementById("root"));
    root.render(<Greeting />);
  </script>
</body>
</html>
```

Відкривши цей файл у браузері, ви побачите заголовок «Привіт, React без жодної збірки!». Магія полягає у тегу `<script type="text/babel">` — бібліотека Babel перехоплює такі блоки, парсить JSX-синтаксис та перетворює його на звичайні виклики `React.createElement()`, які браузер уже вміє виконувати.

::warning
Цей підхід підходить **виключно для експериментів та навчання**. Babel у браузері компілює код при кожному завантаженні сторінки, що робить старт повільним — кожен раз парсер обробляє весь код з нуля. Крім того, ви не отримуєте перевірку типів TypeScript, модульну систему, мініфікацію та інші переваги інструментів збірки. У реальних проєктах так ніхто не працює.
::

### Етап другий: компіляція заздалегідь і простий Node.js-сервер

Наступний крок еволюції — перенести компіляцію з браузера на етап розробки. Ідея проста: ми компілюємо JSX у звичайний JavaScript **до** того, як браузер отримає файл, і віддаємо браузеру вже готовий код.

Встановимо Babel як інструмент командного рядка:

```bash
mkdir my-react-experiment && cd my-react-experiment
npm init -y
npm install @babel/core @babel/cli @babel/preset-react
```

Створимо файл `src/app.jsx`:

```jsx
// src/app.jsx — цей файл містить JSX, який браузер не розуміє
function Greeting() {
  const name = "React";
  return <h1>Привіт від {name} з попередньою компіляцією!</h1>;
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Greeting />);
```

Скомпілюємо JSX у звичайний JavaScript:

```bash
npx babel src/app.jsx --presets=@babel/preset-react --out-file dist/app.js
```

Результат у `dist/app.js` — чистий JavaScript без JSX:

```js
// dist/app.js — браузер розуміє цей код без жодного Babel
function Greeting() {
  const name = "React";
  return React.createElement("h1", null, "Привіт від ", name, " з попередньою компіляцією!");
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(React.createElement(Greeting, null));
```

Тепер створимо найпростіший Node.js-сервер, який віддаватиме наші файли (цей приклад демонструє принцип, а не використовується у продакшні):

```js
// server.js — простий сервер для розробки (~20 рядків)
const http = require("http");
const fs = require("fs");
const path = require("path");

const MIME_TYPES = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
};

const server = http.createServer((req, res) => {
  const filePath = req.url === "/" ? "/index.html" : req.url;
  const fullPath = path.join(__dirname, "dist", filePath);
  const ext = path.extname(fullPath);

  fs.readFile(fullPath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end("Not Found");
      return;
    }
    res.writeHead(200, { "Content-Type": MIME_TYPES[ext] || "text/plain" });
    res.end(data);
  });
});

server.listen(3000, () => {
  console.log("Сервер працює на http://localhost:3000");
});
```

А файл `dist/index.html` підключає вже скомпільований JavaScript:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8" />
  <title>React з попередньою компіляцією</title>
</head>
<body>
  <div id="root"></div>
  <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
  <!-- Тепер тут звичайний JS, а не text/babel! -->
  <script src="/app.js"></script>
</body>
</html>
```

Запускаємо `node server.js` — сторінка відкривається миттєво, без затримки на компіляцію у браузері.

::note
Зверніть увагу на ключову різницю: у першому підході `<script type="text/babel">` змушував Babel парсити та компілювати JSX при кожному завантаженні сторінки. Тепер компіляція відбувається один раз (`npx babel ...`), а браузер отримує готовий JavaScript. Це принципово швидше, але все ще незручно — доводиться вручну запускати `babel` після кожної зміни, немає модульної системи, немає TypeScript.
::

### Етап третій: Vite + React + TypeScript

Усі ці проблеми вирішують сучасні інструменти збірки. **Vite** — збирач нового покоління, що поєднує блискавичний dev-сервер із гарячим перезавантаженням (*Hot Module Replacement*, HMR), модульну систему ES-модулів, підтримку TypeScript, автоматичну компіляцію JSX/TSX та оптимізацію для продакшну — все в одному інструменті.

::tabs
::tabs-item{label="npm"}
```bash
npm create vite@latest my-react-app -- --template react-ts
cd my-react-app
npm install
npm run dev
```
::
::tabs-item{label="pnpm"}
```bash
pnpm create vite my-react-app --template react-ts
cd my-react-app
pnpm install
pnpm dev
```
::
::

Після запуску dev-сервера у терміналі з'явиться локальна адреса (зазвичай `http://localhost:5173`), а у браузері — стартова сторінка з логотипами React та Vite. Прапор `--template react-ts` вказує Vite створити проєкт із підтримкою TypeScript «з коробки» — конфігурація `tsconfig.json`, розширення файлів `.tsx` та типи React вже налаштовані.

::code-tree

```text [my-react-app/]
├── index.html          # Точка входу HTML
├── package.json        # Залежності та скрипти
├── tsconfig.json       # Конфігурація TypeScript
├── vite.config.ts      # Конфігурація Vite
├── src/
│   ├── main.tsx        # Точка входу React
│   ├── App.tsx         # Кореневий компонент
│   ├── App.css         # Стилі компонента App
│   └── vite-env.d.ts   # Типи середовища Vite
└── public/             # Статичні файли
```

::

Саме цей підхід — **Vite + React + TypeScript** — ми будемо використовувати протягом усього курсу.

::tip
Тепер ви розумієте повну картину: JSX/TSX **завжди** компілюється у виклики `React.createElement()` (або у сучасному JSX Transform — у `_jsx()`). Різниця лише в тому, **коли** це відбувається: у браузері на льоту (Babel standalone), заздалегідь вручну (Babel CLI) чи автоматично при збереженні файлу (Vite dev-сервер). Vite обирає останній варіант, додаючи TypeScript, модулі, HMR та оптимізацію продакшн-бандлу.
::

---

# Частина I. Основи React

## 02. Що таке React

> 🔗 **Офіційний референс:** [Швидкий старт (Quick Start)](https://uk.react.dev/learn) та [Мислення в стилі React (Thinking in React)](https://uk.react.dev/learn/thinking-in-react)
> 📥 **Вимога до наповнення статті:** Витягнути всі sandbox-ілюстрації декларативного підходу та челенджі на декомпозицію інтерфейсу на компоненти.

**React** — це JavaScript-бібліотека для побудови користувацьких інтерфейсів, створена командою Meta (Facebook) у 2013 році. Ключове слово тут — саме **бібліотека**, а не фреймворк: React не нав'язує структуру проєкту, систему маршрутизації чи підхід до роботи з даними. Він зосереджений на одній задачі — декларативному описі UI як функції від даних.

Фундаментальна ідея React полягає у тому, що інтерфейс — це **проєкція стану додатку**. Замість того щоб імперативно маніпулювати DOM-елементами (`document.querySelector(...).innerHTML = ...`), розробник описує, **як повинен виглядати** інтерфейс для заданого набору даних, а React бере на себе оновлення реального DOM.

Ця декларативність досягається через дві ключові абстракції:

- **React Element** — легковажний JavaScript-об'єкт, що описує вузол інтерфейсу: його тип (HTML-тег або компонент), пропси та дочірні елементи. React Element — це не DOM-елемент, а лише його «план» або «креслення».
- **Virtual DOM** — дерево React Elements, яке React порівнює з попередньою версією (процес, що називається *reconciliation*), обчислює мінімальний набір змін і застосовує їх до реального DOM.

```tsx
// Це React Element — звичайний JavaScript-об'єкт
const element = {
  type: "h1",
  props: {
    className: "title",
    children: "Привіт, React!",
  },
};
```

Звісно, створювати такі об'єкти вручну було б незручно. Саме тому існує JSX.

## 03. JSX та TSX: синтаксичний цукор, а не магія React

> 🔗 **Офіційний референс:** [Написання розмітки з JSX (Writing Markup with JSX)](https://uk.react.dev/learn/writing-markup-with-jsx)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці трансформації JSX у createElement та всі практичні завдання (Challenges) щодо виправлення синтаксичних помилок JSX у форматі акордеонів.

**JSX** (*JavaScript XML*) — це синтаксичне розширення JavaScript, яке дозволяє писати структуру UI безпосередньо у коді, використовуючи синтаксис, візуально схожий на HTML. **TSX** — це той самий JSX, але у файлах TypeScript (`.tsx`), де додатково працює система типів.

::warning
Критично важливо зрозуміти: **JSX не є частиною React**. JSX — це незалежна специфікація синтаксичного розширення, яку може використовувати будь-яка бібліотека чи фреймворк. React просто популяризував JSX, але він також використовується у Preact, SolidJS, Inferno та інших бібліотеках. Теоретично можна написати власний рендерер, що інтерпретує JSX для побудови PDF-документів або термінальних інтерфейсів.
::

### Як JSX перетворюється на JavaScript

Браузер **не розуміє** JSX — це не валідний JavaScript. Тому компілятор (Babel, TypeScript, SWC або esbuild) **завжди** перетворює JSX на звичайні виклики функцій:

::code-group

```tsx [Те, що ви пишете (JSX/TSX)]
const element = (
  <div className="card">
    <h2>Заголовок</h2>
    <p>Опис картки</p>
  </div>
);
```

```js [Те, що отримує браузер (класичний JSX Transform)]
const element = React.createElement(
  "div",
  { className: "card" },
  React.createElement("h2", null, "Заголовок"),
  React.createElement("p", null, "Опис картки")
);
```

```js [Те, що отримує браузер (сучасний JSX Transform)]
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";

const element = _jsxs("div", {
  className: "card",
  children: [
    _jsx("h2", { children: "Заголовок" }),
    _jsx("p", { children: "Опис картки" }),
  ],
});
```

::

Результат виклику `React.createElement()` (або `_jsx()`) — це звичайний JavaScript-об'єкт, який називається **React Element**:

```tsx
// React.createElement("h1", { className: "title" }, "Привіт!")
// повертає ось такий об'єкт:
{
  type: "h1",
  props: {
    className: "title",
    children: "Привіт!",
  },
  key: null,
  ref: null,
  // ...внутрішні поля React
}
```

React Element — це **незмінний опис** (*immutable description*) того, що повинно бути на екрані. Він не є DOM-елементом і не «рендериться» сам по собі — React читає ці об'єкти та створює або оновлює реальний DOM відповідно до них.

### Можна писати React без JSX

Оскільки JSX — лише синтаксичний цукор, React-додатки можна писати і без нього. Це не практичний підхід, але розуміння цього факту допомагає усвідомити, що JSX — не магія:

```tsx
import { createElement } from "react";

// Без JSX — через createElement напряму
function GreetingWithoutJSX() {
  return createElement(
    "div",
    null,
    createElement("h1", null, "Привіт!"),
    createElement("p", { className: "subtitle" }, "Це React без JSX")
  );
}

// Той самий компонент із JSX — значно читабельніше
function GreetingWithJSX() {
  return (
    <div>
      <h1>Привіт!</h1>
      <p className="subtitle">Це React із JSX</p>
    </div>
  );
}
```

::note
Сучасний **JSX Transform** (доступний з React 17+) не вимагає імпорту `React` у кожному файлі. Компілятор автоматично додає необхідний імпорт з `react/jsx-runtime`. У старіших проєктах ви могли бачити `import React from "react"` на початку кожного файлу — це було потрібно саме тому, що JSX компілювався у `React.createElement()`, і без імпорту `React` у scope виникала помилка.
::

## 04. Компоненти: будівельні блоки інтерфейсу

> 🔗 **Офіційний референс:** [Ваш перший компонент (Your First Component)](https://uk.react.dev/learn/your-first-component) та [Імпорт та експорт компонентів (Importing and Exporting Components)](https://uk.react.dev/learn/importing-and-exporting-components)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади базових компонентів (галереї, профілі) та всі практичні завдання (Challenges) з експорту/імпорту компонентів.

React-застосунок складається з **компонентів** (*components*) — самостійних, повторно використовуваних фрагментів інтерфейсу. Компонент — це звичайна TypeScript-функція, яка повертає React Elements (тобто JSX-розмітку). На відміну від HTML-тегів, які починаються з малої літери (`<div>`, `<button>`), імена React-компонентів **завжди** починаються з великої літери (`<App>`, `<UserProfile>`). Це не лише конвенція — React використовує регістр першої літери, щоб відрізнити власні компоненти від вбудованих HTML-елементів.

Розглянемо найпростіший компонент:

```tsx
function Greeting() {
  return <h1>Привіт, React із TypeScript!</h1>;
}
```

Коли React зустрічає `<Greeting />`, він **викликає функцію** `Greeting()`, отримує React Element (об'єкт, що описує `<h1>`) і рендерить відповідний DOM-елемент. Компонент — це по суті фабрика React Elements.

::tip
Тип повернення функціонального компонента — `React.JSX.Element` (або `React.ReactNode` для більш загальних випадків). TypeScript здатний вивести цей тип автоматично, тому далі у курсі ми будемо опускати явну анотацію для лаконічності. У проєктах із суворою типізацією його можна зазначати явно: `function Greeting(): React.JSX.Element { ... }`.
::

## 05. JSX: розмітка всередині TypeScript

> 🔗 **Офіційний референс:** [JavaScript у JSX із фігурними дужками (JavaScript in JSX with Curly Braces)](https://uk.react.dev/learn/javascript-in-jsx-with-curly-braces) та [Використання TypeScript (Using TypeScript)](https://uk.react.dev/learn/typescript)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці з виразами JS/TS у розмітці та практичні завдання щодо динамічного формування атрибутів і стилів.

JSX виглядає схоже на HTML, але має суттєві відмінності, про які важливо знати від самого початку.

**Правило єдиного кореневого елемента.** Компонент може повертати лише один кореневий елемент. Якщо потрібно повернути кілька елементів без зайвої обгортки у DOM, використовують *фрагмент* (*Fragment*) — порожні кутові дужки `<>...</>`:

```tsx
function UserInfo() {
  return (
    <>
      <h2>Олена Коваленко</h2>
      <p>Frontend-розробниця</p>
    </>
  );
}
```

**Фігурні дужки — вікно у TypeScript.** Усередині JSX фігурні дужки `{}` дозволяють вставляти будь-який TypeScript-вираз: змінні, виклики функцій, тернарні оператори, обчислення:

```tsx
function DateDisplay() {
  const today: Date = new Date();
  const formattedDate: string = today.toLocaleDateString("uk-UA", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return <p>Сьогодні: {formattedDate}</p>;
}
```

**Атрибути HTML перейменовані у camelCase.** Оскільки JSX — це TypeScript, а не HTML, деякі атрибути мають інші імена: `class` стає `className`, `for` стає `htmlFor`, обробники подій пишуться у camelCase (`onClick`, `onChange`, `onSubmit`). Це пов'язано з тим, що `class` та `for` є зарезервованими словами у JavaScript.

```tsx
function StyledButton() {
  return (
    <button className="btn btn-primary" onClick={() => console.log("Клік!")}>
      Натисни мене
    </button>
  );
}
```

**Інлайнові стилі — це об'єкт.** На відміну від HTML, де `style` приймає рядок, у JSX `style` приймає об'єкт з CSS-властивостями у camelCase:

```tsx
function ColorBox() {
  const boxStyle: React.CSSProperties = {
    backgroundColor: "#3b82f6",
    padding: "1rem",
    borderRadius: "0.5rem",
    color: "white",
  };

  return <div style={boxStyle}>Стилізований блок</div>;
}
```

::tip
Тип `React.CSSProperties` забезпечує автодоповнення та перевірку типів для всіх CSS-властивостей. Використовуйте його завжди, коли оголошуєте об'єкт стилів окремою змінною.
::

## 06. CSS Modules: локальна інкапсуляція стилів

> 🔗 **Офіційний референс:** [Специфікація CSS Modules (GitHub Repository)](https://github.com/css-modules/css-modules)
> 📥 **Вимога до наповнення статті:** Витягнути приклади конфігурації з Vite, типізації стилів через TypeScript-плагіни (typed-css-modules) та практичне завдання на ізоляцію стилів.

CSS Modules вирішують проблему глобальних CSS-селекторів — кожен клас автоматично отримує унікальний суфікс під час збірки, що гарантує ізоляцію стилів між компонентами. Vite підтримує CSS Modules «з коробки» — достатньо назвати файл із суфіксом `.module.css`.

```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.primary:hover {
  background-color: #2563eb;
}

.secondary {
  background-color: #e2e8f0;
  color: #0f172a;
}

.secondary:hover {
  background-color: #cbd5e1;
}

.fullWidth {
  width: 100%;
}
```

```tsx
import styles from "./Button.module.css";

interface ButtonProps {
  variant?: "primary" | "secondary";
  fullWidth?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({
  variant = "primary",
  fullWidth = false,
  children,
  onClick,
}: ButtonProps) {
  const classNames = [
    styles.button,
    styles[variant],
    fullWidth ? styles.fullWidth : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button className={classNames} onClick={onClick}>
      {children}
    </button>
  );
}
```

::tip
Для проєктів із великою кількістю динамічних класів рекомендується використовувати бібліотеку `clsx` або `classnames`, що спрощує умовну генерацію рядків класів: `className={clsx(styles.button, styles[variant], { [styles.fullWidth]: fullWidth })}`.
::

---

## 07. Пропси: параметри компонентів

> 🔗 **Офіційний референс:** [Передача пропсів до компонента (Passing Props to a Component)](https://uk.react.dev/learn/passing-props-to-a-component)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ інтерактивні sandbox-приклади передачі пропсів (включаючи children) та ВСІ практичні завдання (Challenges) з рефакторингу пропсів.

Компоненти стають по-справжньому корисними, коли вони приймають **пропси** (*props*, скорочення від *properties*) — вхідні параметри, які батьківський компонент передає дочірньому. Пропси роблять компоненти конфігурованими та повторно використовуваними: замість того щоб створювати окремий компонент для кожної кнопки чи картки, ми створюємо один узагальнений компонент і налаштовуємо його через пропси.

У TypeScript пропси описуються інтерфейсом або типом, що забезпечує перевірку на етапі компіляції — якщо батьківський компонент забуде передати обов'язковий проп або передасть значення неправильного типу, TypeScript повідомить про помилку ще до запуску коду.

```tsx
interface ProfileCardProps {
  name: string;
  role: string;
  avatarUrl: string;
  isOnline?: boolean; // необов'язковий проп
}

function ProfileCard({ name, role, avatarUrl, isOnline = false }: ProfileCardProps) {
  return (
    <div className="profile-card">
      <img src={avatarUrl} alt={`Аватар ${name}`} />
      <h3>{name}</h3>
      <p>{role}</p>
      {isOnline && <span className="status-online">В мережі</span>}
    </div>
  );
}
```

У цьому прикладі варто звернути увагу на кілька ключових деталей. Деструктуризація `{ name, role, avatarUrl, isOnline = false }` витягує значення пропсів безпосередньо у параметрах функції — це ідіоматичний спосіб роботи з пропсами у React. Знак питання `?` в інтерфейсі позначає необов'язковий проп, а конструкція `= false` встановлює значення за замовчуванням (*default value*), яке буде використане, якщо батьківський компонент не передасть цей проп.

Використання компонента:

```tsx
function App() {
  return (
    <div>
      <ProfileCard
        name="Олена Коваленко"
        role="Frontend-розробниця"
        avatarUrl="/avatars/olena.jpg"
        isOnline={true}
      />
      <ProfileCard
        name="Андрій Мельник"
        role="Backend-розробник"
        avatarUrl="/avatars/andriy.jpg"
        // isOnline не вказано — буде false за замовчуванням
      />
    </div>
  );
}
```

::warning
Пропси є **незмінними** (*immutable*) — компонент не повинен модифікувати отримані пропси. Якщо вам потрібно змінити значення, отримане через проп, створіть локальну змінну або використовуйте стан (*state*). Спроба змінити проп напряму призведе до непередбачуваної поведінки та порушить односпрямований потік даних (*one-way data flow*) — фундаментальний принцип React.
::

### Дочірні елементи через `children`

Існує особливий проп `children` — він містить усе, що розміщено між відкриваючим та закриваючим тегами компонента. Це дозволяє створювати компоненти-обгортки (*wrapper components*), які не знають заздалегідь, який вміст вони оточуватимуть:

```tsx
interface CardProps {
  title: string;
  children: React.ReactNode;
}

function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      <div className="card-header">
        <h3>{title}</h3>
      </div>
      <div className="card-body">{children}</div>
    </div>
  );
}

// Використання
function App() {
  return (
    <Card title="Профіль користувача">
      <p>Ім'я: Олена Коваленко</p>
      <p>Роль: Frontend-розробниця</p>
      <button>Редагувати</button>
    </Card>
  );
}
```

Тип `React.ReactNode` є найбільш загальним типом для дочірніх елементів — він охоплює рядки, числа, JSX-елементи, масиви елементів, фрагменти, `null` та `undefined`.

## 08. Умовний рендеринг

> 🔗 **Офіційний референс:** [Умовний рендеринг (Conditional Rendering)](https://uk.react.dev/learn/conditional-rendering)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади розгалуження UI (if/else, тернарний оператор, &&) та ВСІ практичні завдання (Challenges) із прихованими розв'язками в акордеонах.

Інтерфейси рідко бувають статичними — компоненти повинні показувати різний вміст залежно від даних, стану користувача чи результатів мережевих запитів. React не має спеціального синтаксису для умов — замість цього використовуються стандартні конструкції TypeScript.

**Тернарний оператор** — найпоширеніший спосіб обрати між двома варіантами розмітки:

```tsx
interface StatusBadgeProps {
  isActive: boolean;
}

function StatusBadge({ isActive }: StatusBadgeProps) {
  return (
    <span className={isActive ? "badge-active" : "badge-inactive"}>
      {isActive ? "Активний" : "Неактивний"}
    </span>
  );
}
```

**Логічне «І» (`&&`)** — зручний патерн, коли потрібно показати елемент лише за певної умови, а інакше — нічого не рендерити:

```tsx
interface NotificationProps {
  count: number;
}

function NotificationBadge({ count }: NotificationProps) {
  return (
    <div>
      <span>Сповіщення</span>
      {count > 0 && <span className="badge">{count}</span>}
    </div>
  );
}
```

::caution
Будьте обережні з `&&`, коли ліва частина може бути числом `0`. Вираз `{count && <span>{count}</span>}` при `count = 0` відрендерить `0` у DOM, а не порожній вміст, оскільки `0` є *falsy*, але React рендерить його як текстовий вузол. Завжди перетворюйте на булевий вираз: `{count > 0 && ...}`.
::

**Ранній повернення** — якщо умова стосується всього компонента цілком, доцільно використовувати `if` та ранній `return`:

```tsx
interface UserGreetingProps {
  user: { name: string; email: string } | null;
}

function UserGreeting({ user }: UserGreetingProps) {
  if (!user) {
    return <p>Будь ласка, увійдіть до системи.</p>;
  }

  return (
    <div>
      <h2>Вітаємо, {user.name}!</h2>
      <p>{user.email}</p>
    </div>
  );
}
```

## 09. Рендеринг списків

> 🔗 **Офіційний референс:** [Рендеринг списків (Rendering Lists)](https://uk.react.dev/learn/rendering-lists)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці з .map() та фільтрацією, демонстрацію багів з індексами масиву як key, та ВСІ практичні завдання (Challenges) щодо унікальних ключів.

Майже кожен реальний інтерфейс містить списки — переліки товарів, повідомлення у чаті, рядки таблиці. У React для рендерингу списків використовується метод масивів `.map()`, який перетворює кожен елемент даних на відповідний JSX-елемент. Це не спеціальний API React, а звичайний JavaScript-метод, який ідеально вписується у декларативний підхід.

```tsx
interface Task {
  id: number;
  title: string;
  completed: boolean;
}

const tasks: Task[] = [
  { id: 1, title: "Вивчити JSX", completed: true },
  { id: 2, title: "Опанувати пропси", completed: true },
  { id: 3, title: "Зрозуміти стан", completed: false },
];

function TaskList() {
  return (
    <ul>
      {tasks.map((task) => (
        <li key={task.id} className={task.completed ? "done" : ""}>
          {task.title}
        </li>
      ))}
    </ul>
  );
}
```

Проп `key` — це спеціальний атрибут, який React вимагає для кожного елемента у списку. Ключі допомагають React визначити, які елементи змінилися, були додані або видалені. Без ключів React не зможе ефективно оновлювати DOM і змушений буде перемальовувати весь список при кожній зміні.

::warning
**Ніколи не використовуйте індекс масиву як `key`**, якщо порядок елементів може змінюватися (сортування, видалення, вставка). Це призводить до непередбачуваних багів: React «плутає» елементи, і стан одного компонента може «перетекти» до іншого. Використовуйте стабільний унікальний ідентифікатор — `id` з бази даних, UUID або інший незмінний ідентифікатор.
::

### Фільтрація та трансформація списків

Оскільки `.map()` — звичайний метод масиву, його можна комбінувати з `.filter()`, `.sort()` та іншими методами для створення складних трансформацій:

```tsx
function ActiveTaskList() {
  const activeTasks = tasks
    .filter((task) => !task.completed)
    .sort((a, b) => a.title.localeCompare(b.title, "uk"));

  return (
    <ul>
      {activeTasks.map((task) => (
        <li key={task.id}>{task.title}</li>
      ))}
    </ul>
  );
}
```

::note
Зверніть увагу, що фільтрація та сортування відбуваються **до** JSX-розмітки. Це зберігає JSX чистим та читабельним. Уникайте складної логіки всередині `{}` у JSX — краще винести обчислення у змінну перед `return`.
::

## 10. Чистота компонентів: математична передбачуваність UI

> 🔗 **Офіційний референс:** [Чистота компонентів (Keeping Components Pure)](https://uk.react.dev/learn/keeping-components-pure)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ інтерактивні пісочниці (годинник, чайний сервіз, кубок), демонстрацію помилок мутації та ВСІ практичні завдання (Challenges) з виправлення нечистих компонентів.

У комп'ютерних науках і функційному програмуванні **чиста функція** (*pure function*) — це функція, яка володіє двома суворими математичними властивостями:

1. **Займається виключно своїми справами (*Mind its own business*):** вона не змінює жодних об'єктів, змінних або структур даних, які існували до моменту її виклику.
2. **Однакові вхідні дані — однаковий результат (*Same inputs, same output*):** при повторному виклику з ідентичними аргументами чиста функція завжди повертає абсолютно однаковий результат.

Фундаментальна філософія React побудована навколо цієї концепції. React виходить із припущення, що **кожен написаний вами компонент є чистою функцією**. Це означає, що компонент повинен приймати пропси й стан та повертати виключно JSX-розмітку, не спричиняючи жодних побічних дій під час рендерингу.

### Побічні ефекти під час рендерингу: типова помилка

Розглянемо приклад, який порушує принцип чистоти: компонент модифікує зовнішню змінну, що знаходиться за межами його області видимості:

```tsx
// ❌ ПОМИЛКА: зовнішня змінна мутується під час рендерингу
let guestCounter = 0;

interface CupProps {
  drink: string;
}

function Cup({ drink }: CupProps) {
  // Побічний ефект: зміна глобального стану під час рендерингу
  guestCounter = guestCounter + 1;

  return (
    <p>
      Гість #{guestCounter}: чашка з напоєм «{drink}»
    </p>
  );
}

export function TeaParty() {
  return (
    <div>
      <Cup drink="Зелений чай" />
      <Cup drink="Чорний чай" />
      <Cup drink="М'ятний чай" />
    </div>
  );
}
```

Якщо викликати цей компонент двічі або перерендерити один із нащадків, значення `guestCounter` буде непередбачувано зростати (`4, 5, 6...`). Порядок рендерингу компонентів стає критичним, а передбачуваність інтерфейсу повністю руйнується.

Правильний підхід полягає у передачі всіх змінних даних **явно через пропси**:

```tsx
// ✅ ПРАВИЛЬНО: компонент чистий і залежить виключно від пропсів
interface CupProps {
  guestNumber: number;
  drink: string;
}

function Cup({ guestNumber, drink }: CupProps) {
  return (
    <p>
      Гість #{guestNumber}: чашка з напоєм «{drink}»
    </p>
  );
}

export function TeaParty() {
  return (
    <div>
      <Cup guestNumber={1} drink="Зелений чай" />
      <Cup guestNumber={2} drink="Чорний чай" />
      <Cup guestNumber={3} drink="М'ятний чай" />
    </div>
  );
}
```

Тепер компонент `Cup` математично чистий: передавши `guestNumber={1}` та `drink="Зелений чай"`, ви гарантовано отримаєте однаковий HTML незалежно від того, скільки разів і в якому порядку викликається компонент.

### Локальна мутація: що дозволено всередині рендеру

Чистота не забороняє будь-які зміни взагалі. Вона забороняє мутувати те, що існувало **до початку виконання функції**. Зміна об'єктів, створених безпосередньо під час поточного виклику, називається **локальною мутацією** (*local mutation*) і є абсолютно безпечною:

```tsx
interface OrderSummaryProps {
  items: string[];
}

function OrderSummary({ items }: OrderSummaryProps) {
  // ✅ Локальна мутація: масив створено всередині цього виклику функції
  const formattedItems: string[] = [];

  for (let i = 0; i < items.length; i++) {
    formattedItems.push(`${i + 1}. ${items[i].trim()}`);
  }

  return (
    <ul>
      {formattedItems.map((item, index) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  );
}
```

Оскільки масив `formattedItems` створюється наново при кожному виклику і не виходить за межі функції, жоден інший компонент не може побачити проміжний стан цієї мутації.

### Де дозволені побічні ефекти

Реальні вебзастосунки повинні взаємодіяти із зовнішнім світом: відправляти мережеві HTTP-запити, змінювати заголовок сторінки у браузері, зберігати дані у `localStorage` чи запускати таймери. Усі ці дії є **побічними ефектами** (*side effects*).

У філософії React діє непохитне правило: **побічні ефекти ніколи не повинні виконуватися під час фази рендерингу**. Для них передбачені два чітко ізольовані місця:

1. **Обробники подій (*Event Handlers*):** функції, що реагують на дії користувача (`onClick`, `onSubmit`, `onChange`). Оскільки обробники подій спрацьовують після завершення рендерингу, вони не впливають на чистоту самого відображення.
2. **Хук `useEffect`:** якщо ефект повинен виконатися у відповідь на сам факт появи компонента на екрані (наприклад, початкове завантаження даних), його розміщують усередині хука `useEffect`, який викликається React лише після того, як зміни застосовані до реального DOM.

::note
**Чому чистота критична для React?**
- **Рендеринг на сервері (SSR):** чистий компонент повертає однаковий результат як на Node.js-сервері, так і у браузері клієнта.
- **Оптимізація та кешування:** React може автоматично пропустити рендеринг компонента, чиї пропси не змінилися (`React.memo`, React Compiler).
- **Конкурентний режим (*Concurrent Mode*):** React здатний призупинити тривалий рендер у фоні або почати його наново при надходженні більш пріоритетної події, не залишаючи напівзруйнованого стану.
::

### StrictMode: виявлення нечистих функцій у розробці

Щоб допомогти розробникам вчасно помітити випадкові побічні ефекти, React надає режим **`<React.StrictMode>`**. У середовищі розробки (*development*) StrictMode **навмисно викликає функцію кожного компонента двічі**:

1. Перший виклик виконує плановий рендер.
2. Другий виклик негайно повторює рендер із тими самими пропсами, щоб перевірити, чи не змінився внутрішній результат або зовнішні змінні.

Якщо ваш компонент чистий, подвійне виконання абсолютно непомітне (`f(x) === f(x)`). Проте якщо компонент містить несанкціоновану мутацію (як у прикладі з `guestCounter`), значення миттєво підскочить удвічі, оголюючи баг ще на етапі локального тестування. У production-збірці подвійний виклик автоматично відключається.

---

## 11. Інтерфейс користувача як дерево: дерева рендерингу та модульних залежностей

> 🔗 **Офіційний референс:** [Ваш UI як дерево (Understanding Your UI as a Tree)](https://uk.react.dev/learn/understanding-your-ui-as-a-tree)
> 📥 **Вимога до наповнення статті:** Витягнути діаграми дерева рендерингу та дерева залежностей модулів, sandbox-приклади умовних гілок та аналітичні завдання щодо структури дерев.

У вебвекторній графіці та браузерному оточенні зв'язки між елементами традиційно моделюються у вигляді дерев: наприклад, HTML утворює **DOM** (*Document Object Model*), а стилі — **CSSOM** (*CSS Object Model*). React так само спирається на деревоподібні структури для організації взаємозв'язків між компонентами та файлами.

Для глибокого інженерного розуміння роботи React-застосунку необхідно розрізняти два абсолютно різних дерева:
- **Дерево рендерингу (*Render Tree*)**
- **Дерево залежностей модулів (*Module Dependency Tree*)**

### Дерево рендерингу (Render Tree)

**Дерево рендерингу** відображає ієрархічні відносини між батьківськими та дочірніми компонентами, які фактично відображаються на екрані у даний момент часу.

- **Кореневий вузол (*Root Node*):** верхня точка застосунку, зазвичай це компонент `<App />` або провайдер контексту.
- **Проміжні вузли (*Branch Nodes*):** компоненти-обгортки, що інкапсулюють структуру та логіку (`<DashboardLayout>`, `<Navigation>`, `<ProductGrid>`).
- **Листові вузли (*Leaf Nodes*):** компоненти нижнього рівня дерева, які не рендерять інші кастомні React-компоненти, а складаються виключно з базових DOM-тегів (`<button>`, `<span>`, `<input>`) або не повертають нащадків.

Дерево рендерингу є **динамічним**: воно описує лише поточний стан інтерфейсу. Якщо певний блок приховано через умовний рендеринг, він взагалі відсутній у поточному дереві рендерингу:

```tsx
interface HeaderProps {
  isLoggedIn: boolean;
  username?: string;
}

export function Header({ isLoggedIn, username }: HeaderProps) {
  return (
    <header className="header">
      <Logo />
      {isLoggedIn ? <UserMenu username={username!} /> : <LoginButton />}
    </header>
  );
}
```

Якщо `isLoggedIn === false`, у дереві рендерингу існує гілка `Header -> LoginButton`. Компонент `UserMenu` не монтується, його код не виконується, а пов'язані з ним хуки не ініціалізуються.

::tip
**Чому форма дерева рендерингу важлива?**
Листові вузли зазвичай перемальовуються частіше за кореневі. Якщо важкий стан розміщено близько до вершини дерева (у кореневому вузлі), кожна його зміна викликатиме каскадний рендеринг великого піддерева. Проєктування компонента таким чином, щоб стан локалізувався ближче до листових вузлів, є головним прийомом оптимізації продуктивності.
::

### Дерево залежностей модулів (Module Dependency Tree)

На відміну від дерева рендерингу, **дерево залежностей модулів** представляє статичні зв'язки між окремими файлами у кодовій базі через директиви `import` та `export`.

У цьому дереві:
- Коренем є вхідна точка збірки (наприклад, `src/main.tsx`).
- Кожен окремий файл (`.ts`, `.tsx`, `.css`, `.svg`) є вузлом.
- Кожен оператор `import` формує спрямоване ребро від одного модуля до іншого.

Дерево залежностей модулів є **статичним**: воно будується компілятором або інструментом збірки (Vite, Rollup, webpack) **до** запуску програми й не залежить від того, які значення мають змінні чи який компонент відображено на екрані.

### Порівняння дерев та практичне значення

| Характеристика | Дерево рендерингу (Render Tree) | Дерево залежностей модулів (Dependency Tree) |
| :--- | :--- | :--- |
| **Елементи вузлів** | Екземпляри React-компонентів | Окремі файли та модулі на диску |
| **Природа** | Динамічна (змінюється залежно від стану та пропсів) | Статична (визначається операторами `import`/`export`) |
| **Хто аналізує** | Середовище виконання React (*Runtime Virtual DOM*) | Інструмент збірки (*Bundler*: Vite, esbuild, Rollup) |
| **Головне призначення** | Оптимальне оновлення реального браузерного DOM | Мінімізація розміру файлів, Tree Shaking, Code Splitting |

Дерево залежностей модулів критично важливе для розуміння розміру підсумкового клієнтського бандла:

1. **Tree Shaking:** збирач аналізує дерево залежностей і повністю видаляє модулі та функції, які ніде не імпортуються.
2. **Розділення коду (*Code Splitting*):** за допомогою динамічного імпорту `React.lazy(() => import("./HeavyChart"))` ми розриваємо синхронну гілку в дереві залежностей модулів. Компонент завантажується по мережі лише тоді, коли він дійсно потрібен у дереві рендерингу.

Розуміння різниці між двома деревами дозволяє проєктувати компонентну архітектуру, де великі бібліотеки чи рідко використовувані екрани не сповільнюють стартове завантаження додатку.

---

# Частина II. Додавання інтерактивності

## 12. Обробка подій

> 🔗 **Офіційний референс:** [Реагування на події (Responding to Events)](https://uk.react.dev/learn/responding-to-events)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади синтетичних подій, спливання (propagation) і preventDefault, та ВСІ практичні завдання (Challenges) щодо обробників подій.

React використовує синтетичну систему подій (*Synthetic Events*), яка нормалізує відмінності між браузерами та надає єдиний API. Обробники подій передаються як пропси у camelCase: `onClick`, `onChange`, `onSubmit`, `onKeyDown` тощо.

У TypeScript кожна подія має відповідний тип, що забезпечує автодоповнення та перевірку:

```tsx
function SearchInput() {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    console.log("Введене значення:", event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    console.log("Форму надіслано!");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Пошук..."
        onChange={handleChange}
      />
      <button type="submit">Шукати</button>
    </form>
  );
}
```

Тип `React.ChangeEvent<HTMLInputElement>` — це дженерик, параметризований типом HTML-елемента, на якому відбувається подія. Це дозволяє TypeScript знати, що `event.target` є `HTMLInputElement` і має властивість `value`. Для інших елементів використовуйте відповідні типи: `HTMLTextAreaElement`, `HTMLSelectElement`, `HTMLButtonElement`.

### Передавання аргументів у обробники подій

Часто обробник повинен знати, з яким саме елементом списку пов'язана подія. Для цього використовують стрілкову функцію-обгортку або замикання:

```tsx
interface ButtonGroupProps {
  labels: string[];
  onSelect: (label: string) => void;
}

function ButtonGroup({ labels, onSelect }: ButtonGroupProps) {
  return (
    <div>
      {labels.map((label) => (
        <button key={label} onClick={() => onSelect(label)}>
          {label}
        </button>
      ))}
    </div>
  );
}
```

::note
Конструкція `onClick={() => onSelect(label)}` створює нову функцію при кожному рендері. Для більшості випадків це не є проблемою продуктивності, але у критичних місцях (списки з тисячами елементів) можна оптимізувати за допомогою `useCallback` — хука, який ми розглянемо пізніше.
::

## 13. Стан компонента: `useState`

> 🔗 **Офіційний референс:** [Стан: пам'ять компонента (State: A Component's Memory)](https://uk.react.dev/learn/state-a-components-memory)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади useState (галерея скульптур, лічильники) та ВСІ практичні завдання (Challenges) щодо виправлення помилок оновлення стану.

До цього моменту наші компоненти були статичними — вони отримували пропси та рендерили відповідну розмітку, але не могли змінюватися у відповідь на дії користувача. **Стан** (*state*) — це пам'ять компонента, що дозволяє йому «запам'ятовувати» інформацію між рендерами та реагувати на взаємодію користувача.

Хук `useState` — це основний механізм додавання стану до функціонального компонента. Він приймає початкове значення та повертає масив із двох елементів: поточне значення стану та функцію для його оновлення.

```tsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState<number>(0);

  return (
    <div>
      <p>Лічильник: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(count - 1)}>-1</button>
      <button onClick={() => setCount(0)}>Скинути</button>
    </div>
  );
}
```

Розглянемо, що відбувається при натисканні кнопки «+1». Виклик `setCount(count + 1)` повідомляє React, що стан компонента змінився. React запланує повторний рендер — повторний виклик функції `Counter`. Під час наступного рендеру `useState` поверне оновлене значення `count`, і розмітка відобразить нове число. Важливо усвідомити: `setCount` **не змінює** поточне значення `count` миттєво — вона лише планує оновлення для наступного рендеру.

::tip
Дженерик `useState<number>(0)` у цьому прикладі є необов'язковим — TypeScript виводить тип із початкового значення `0`. Проте явна типізація стає необхідною, коли початкове значення не розкриває повний тип, наприклад: `useState<string | null>(null)` або `useState<Task[]>([])`.
::

## 14. Рендер і коміт: анатомія життєвого циклу оновлення

> 🔗 **Офіційний референс:** [Рендер і коміт (Render and Commit)](https://uk.react.dev/learn/render-and-commit)
> 📥 **Вимога до наповнення статті:** Витягнути всі ілюстративні пісочниці тригерів, рекурсивного рендерингу та точкових комітів у DOM, а також концептуальні запитання на самоперевірку.

Перш ніж компоненти з'являться на екрані, вони проходять суворий багатоетапний конвеєр обробки React. Помилково вважати, що зміна стану компонента безпосередньо маніпулює браузерним DOM. Насправді процес перетворення коду на видимі пікселі складається з **трьох фундаментальних кроків**:

1. **Запуск рендерингу (*Triggering a render*)**
2. **Рендеринг компонентів (*Rendering the component*)**
3. **Фіксація змін у DOM (*Committing to the DOM*)**

Для легкості розуміння уявіть аналогію з рестораном: компонент — це шеф-кухар на кухні, який формує страву з інгредієнтів (пропсів і стану), React — це уважний офіціант, який приймає замовлення і несе готові страви, а браузерний DOM — це стіл клієнта.

### Крок 1. Запуск рендерингу (Trigger)

Рендеринг запускається лише у двох ситуаціях:
- **Початковий рендер застосунку:** коли програма стартує, викликається метод `createRoot` із кореневим компонентом:
  ```tsx
  import { createRoot } from "react-dom/client";
  import App from "./App";

  const root = createRoot(document.getElementById("root")!);
  root.render(<App />);
  ```
- **Оновлення стану компонента чи його предків:** коли стан компонента оновлюється за допомогою функції `setState`, React автоматично планує наступний рендер у черзі завдань.

### Крок 2. Рендеринг компонентів (Render)

На етапі рендерингу React **викликає ваші функції-компоненти**:
- **Під час початкового рендеру** React викликає кореневий компонент `<App />`.
- **Під час повторного рендеру** React викликає компонент, чий стан спровокував оновлення, а також рекурсивно перерендерить усіх його дочірніх нащадків.

::important
Рендеринг у React — це **виключно розрахунок**. Це виклик функції вашого компонента для отримання опису JSX (дерева React Elements). На цьому етапі React **жодним чином не торкається реального DOM**. Рендеринг має залишатися абсолютно чистим процесом без побічних дій.
::

### Крок 3. Фіксація змін у DOM (Commit)

Після завершення обчислення нового дерева елементів React переходить до фіксації:
- **Для початкового рендеру:** React використовує браузерні системні виклики `node.appendChild()` для створення всіх вузлів у DOM вперше.
- **Для повторних рендерів:** React виконує алгоритм узгодження (*Reconciliation / Diffing*). Він порівнює щойно обчислене дерево з попереднім і застосовує **мінімально необхідні зміни** до реального DOM.

Якщо під час рендерингу результат обчислення компонента збігається з попереднім (наприклад, повернуто ту саму розмітку), React **не здійснює жодних операцій із DOM**.

```tsx
// React оновить у DOM лише текст усередині <span>!
// Теги <h1> та <section> залишаться незмінними в браузерному дереві.
function Clock({ time }: { time: string }) {
  return (
    <section className="clock-card">
      <h1>Поточний час сервера:</h1>
      <span className="time-value">{time}</span>
    </section>
  );
}
```

### Фінальний етап: Відображення браузером (Browser Paint)

Коли React завершив коміт і оновив DOM, керування повертається браузерному рушію. Браузер перераховує геометричні параметри елементів (*Layout/Reflow*) і перемальовує пікселі на екрані (*Painting*). Цей етап часто називають браузерним рендерингом, і важливо не плутати його з внутрішнім рендерингом React.

---

## 15. Стан як знімок: модель рендерингу React

> 🔗 **Офіційний референс:** [Стан як снепшот (State as a Snapshot)](https://uk.react.dev/learn/state-as-a-snapshot)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ інтерактивні sandbox-приклади (поведінка асинхронних лічильників, чернетки повідомлень у таймерах) та ВСІ практичні завдання (Challenges) щодо моделі знімків.

Щоб ефективно працювати зі станом, необхідно зрозуміти ключову ментальну модель React: **кожен рендер — це знімок** (*snapshot*) інтерфейсу на певний момент часу. Коли React викликає функцію вашого компонента, він «фотографує» поточне значення всіх змінних стану та створює відповідну розмітку. Виклик `setState` не змінює стан «на місці» — він просить React виконати новий рендер з оновленим значенням.

Ця концепція пояснює поведінку, яка часто здивовує початківців:

```tsx
function BatchExample() {
  const [count, setCount] = useState(0);

  const handleClick = (): void => {
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1);
    // Результат: count стане 1, а не 3!
  };

  return <button onClick={handleClick}>Клік ({count})</button>;
}
```

Чому три виклики `setCount(count + 1)` збільшують лічильник лише на 1? Тому що всередині обробника подій `count` — це «заморожене» значення знімка поточного рендеру (наприклад, `0`). Всі три виклики обчислюються як `setCount(0 + 1)`, а React батчить (*batches*) оновлення та виконує лише один повторний рендер.

Для коректного послідовного оновлення використовуйте **функціональну форму** (*updater function*):

```tsx
const handleClick = (): void => {
  setCount((prev) => prev + 1);
  setCount((prev) => prev + 1);
  setCount((prev) => prev + 1);
  // Результат: count стане 3
};
```

Функціональна форма `(prev) => prev + 1` отримує **актуальне** значення стану з черги оновлень, а не «заморожене» значення зі знімка рендеру.

## 16. Черга оновлень стану та автоматичний батчинг

> 🔗 **Офіційний референс:** [Додавання до черги низки оновлень стану (Queueing a Series of State Updates)](https://uk.react.dev/learn/queueing-a-series-of-state-updates)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади пакетного оновлення (батчингу), функції оновлення (n => n + 1) та ВСІ завдання (Challenges) з розрахунку черги оновлень.

Уявіть, що ви прийшли до ресторану і диктуєте замовлення офіціантові. Ви не відправляєте офіціанта на кухню після кожного окремого слова: «Принесіть воду». (Офіціант біжить). «А також пасту». (Знову біжить). Ви називаєте всі страви разом, і лише після завершення замовлення офіціант іде на кухню.

Саме так діє **автоматичний батчинг** (*Automatic Batching*) у React: React чекає завершення роботи всього коду всередині обробника події перед тим, як оновити стан і запустити рендеринг. Це дозволяє уникнути кількох повторних рендерів для однієї взаємодії користувача.

### Проблема послідовної заміни стану

Розглянемо випадок, коли обробник намагається збільшити лічильник тричі поспіль:

```tsx
function Counter() {
  const [number, setNumber] = useState<number>(0);

  const handleClick = (): void => {
    setNumber(number + 1);
    setNumber(number + 1);
    setNumber(number + 1);
  };

  return <button onClick={handleClick}>Додати 3 (поточне: {number})</button>;
}
```

Після кліку значення `number` стане `1`, а не `3`. 

**Чому так відбувається?**
У кожному виклику `number` береться зі знімка (*snapshot*) поточного рендеру, де `number === 0`. Код фактично виконує:
1. `setNumber(0 + 1)` — React готує заміну на `1`.
2. `setNumber(0 + 1)` — React перезаписує чергу новою заміною на `1`.
3. `setNumber(0 + 1)` — React знову призначає `1`.

### Функції оновлення (Updater Functions)

Якщо вам потрібно оновити стан кілька разів у межах однієї події або обчислити наступний стан на основі найсвіжішого значення, передавайте у `setState` **функцію оновлення** (*updater function*):

```tsx
function CounterFixed() {
  const [number, setNumber] = useState<number>(0);

  const handleClick = (): void => {
    setNumber((prev) => prev + 1);
    setNumber((prev) => prev + 1);
    setNumber((prev) => prev + 1);
  };

  return <button onClick={handleClick}>Додати 3 (поточне: {number})</button>;
}
```

Тут `prev => prev + 1` не замінює значення негайно, а додає функцію до внутрішньої черги React: «обчисли наступне значення від актуального проміжного результату».

### Як React обробляє чергу оновлень

Розглянемо складніший сценарій змішування заміни значення та функцій оновлення:

```tsx
setNumber(number + 5);        // 1. Заміна на 0 + 5 = 5
setNumber((prev) => prev + 1); // 2. Оновлення: 5 + 1 = 6
setNumber(42);                 // 3. Пряма заміна на 42
```

| Черга оновлення | Аргумент виклику | Обчислене значення стану |
| :--- | :--- | :--- |
| 1 | `0 + 5` (значення) | `5` |
| 2 | `prev => prev + 1` (функція) | `5 => 5 + 1 = 6` |
| 3 | `42` (значення) | `42` |

Фінальним значенням `number` після обробки черги буде `42`.

::tip
**Правило іменування аргументів:**
Прийнято називати параметр функції оновлення або словом `prev` (від *previous*), або першими літерами відповідної змінної стану:
```tsx
setEnabled((e) => !e);
setLastName((ln) => ln.toUpperCase());
setUsers((prevUsers) => [...prevUsers, newUser]);
```
::

---

## 17. Оновлення об'єктів у стані

> 🔗 **Офіційний референс:** [Оновлення об'єктів у стані (Updating Objects in State)](https://uk.react.dev/learn/updating-objects-in-state)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці імутабельного оновлення (переміщення курсора, вкладені об'єкти профілю, Immer) та ВСІ практичні завдання (Challenges) щодо усунення мутацій.

React визначає, чи потрібен повторний рендер, порівнюючи попередній та новий стан за **посиланням** (*reference equality*). Якщо ви мутуєте об'єкт напряму, його посилання не змінюється, і React не помітить зміну — інтерфейс не оновиться. Тому стан у React завжди оновлюється **імутабельно** (*immutably*) — створенням нового об'єкта замість зміни існуючого.

```tsx
interface UserProfile {
  name: string;
  email: string;
  age: number;
}

function ProfileEditor() {
  const [profile, setProfile] = useState<UserProfile>({
    name: "Олена",
    email: "olena@example.com",
    age: 25,
  });

  // ❌ Неправильно: мутація існуючого об'єкта
  const handleWrong = (): void => {
    profile.name = "Андрій"; // React не побачить зміну!
    setProfile(profile);     // Те саме посилання — рендер не відбудеться
  };

  // ✅ Правильно: створення нового об'єкта через spread-оператор
  const handleCorrect = (): void => {
    setProfile({ ...profile, name: "Андрій" });
  };

  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const { name, value } = event.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <form>
      <input name="name" value={profile.name} onChange={handleInputChange} />
      <input name="email" value={profile.email} onChange={handleInputChange} />
      <p>Профіль: {profile.name}, {profile.email}</p>
    </form>
  );
}
```

### Оновлення вкладених об'єктів

Коли об'єкт має вкладені структури, spread-оператор створює лише **поверхневу копію** (*shallow copy*). Для зміни вкладених полів потрібен вкладений spread:

```tsx
interface Address {
  city: string;
  street: string;
  zip: string;
}

interface Employee {
  name: string;
  address: Address;
}

function EmployeeEditor() {
  const [employee, setEmployee] = useState<Employee>({
    name: "Марія",
    address: { city: "Київ", street: "Хрещатик", zip: "01001" },
  });

  const handleCityChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    setEmployee((prev) => ({
      ...prev,
      address: { ...prev.address, city: event.target.value },
    }));
  };

  return (
    <div>
      <p>Місто: {employee.address.city}</p>
      <input value={employee.address.city} onChange={handleCityChange} />
    </div>
  );
}
```

## 18. Оновлення масивів у стані

> 🔗 **Офіційний референс:** [Оновлення масивів у стані (Updating Arrays in State)](https://uk.react.dev/learn/updating-arrays-in-state)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади операцій з масивами (списки справ, додавання, видалення, сортування, трансформація) та ВСІ практичні завдання (Challenges) з розв'язками.

Масиви підпорядковуються тим самим правилам імутабельності, що й об'єкти. Замість мутуючих методів (`push`, `splice`, `sort` на місці) використовуються методи, що повертають нові масиви: `map`, `filter`, `concat`, спред-оператор `[...arr]`, та `toSorted()`.

```tsx
interface TodoItem {
  id: number;
  text: string;
  done: boolean;
}

function TodoList() {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [nextId, setNextId] = useState(1);
  const [inputText, setInputText] = useState("");

  // Додавання елемента
  const handleAdd = (): void => {
    if (!inputText.trim()) return;
    setTodos((prev) => [...prev, { id: nextId, text: inputText, done: false }]);
    setNextId((prev) => prev + 1);
    setInputText("");
  };

  // Перемикання стану виконання
  const handleToggle = (id: number): void => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, done: !todo.done } : todo
      )
    );
  };

  // Видалення елемента
  const handleDelete = (id: number): void => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  return (
    <div>
      <input
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Нова задача..."
      />
      <button onClick={handleAdd}>Додати</button>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => handleToggle(todo.id)}
            />
            <span style={{ textDecoration: todo.done ? "line-through" : "none" }}>
              {todo.text}
            </span>
            <button onClick={() => handleDelete(todo.id)}>✕</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

::note
Цей приклад демонструє три основні операції з масивами у стані: додавання (`[...prev, newItem]`), оновлення (`prev.map(...)`) та видалення (`prev.filter(...)`). Запам'ятайте цю трійку — вона покриває переважну більшість сценаріїв роботи зі списками у React.
::

---

# Частина III. Управління станом

## 19. Реагування станом на введення: від імперативного до декларативного UI

> 🔗 **Офіційний референс:** [Реагування станом на введення (Reacting to Input with State)](https://uk.react.dev/learn/reacting-to-input-with-state)
> 📥 **Вимога до наповнення статті:** Витягнути інтерактивне порівняння імперативної форми та декларативної React-форми, а також ВСІ практичні завдання (Challenges) з моделювання станів компонентів.

При імперативному підході до розробки (наприклад, із чистим JavaScript або jQuery) розробник пише прямі інструкції для маніпуляції кожним UI-елементом окремо:
- «Якщо користувач натиснув кнопку, увімкни спінер».
- «Заблокуй поле введення».
- «Якщо виникла помилка, покажи блок із червоним текстом і вимкни спінер».

Зі збільшенням складності форми кількість переходів між станами зростає лавиноподібно. Легко забути сховати помилку або вимкнути індикатор завантаження, що призводить до розсинхронізації інтерфейсу.

**Декларативний підхід React** пропонує іншу парадигму: ви описуєте, **як повинен виглядати інтерфейс для кожного можливого стану**, а потім змінюєте лише стан.

### 5 кроків декларативного проєктування форми

1. **Визначте всі візуальні стани компонента:**
   - Порожня форма (*Empty*): кнопка «Надіслати» заблокована.
   - Введення тексту (*Typing*): кнопка розблокована.
   - Відправка (*Submitting*): форма заблокована, активний індикатор завантаження.
   - Успіх (*Success*): форма зникає, з'являється повідомлення про успіх.
   - Помилка (*Error*): показується повідомлення про помилку, поля знову активні.
2. **Визначте тригери переходу між станами:**
   - Дії людини: введення символу, клік по кнопці.
   - Дії комп'ютера: успішна відповідь HTTP-сервера, мережевий таймаут.
3. **Змоделюйте стан у пам'яті за допомогою `useState`.**
4. **Усуньте несуттєві та взаємовиключні змінні стану.**
5. **Підключіть обробники подій для встановлення стану.**

### Приклад: Типобезпечна форма відгуку на TypeScript

Замість набору незалежних булевих прапорців (`isSubmitting`, `isSuccess`, `isError`), які можуть увійти в суперечливий стан (`isSubmitting === true && isSuccess === true`), використовуйте **дискримінований союз статусів**:

```tsx
type FormStatus = "typing" | "submitting" | "success" | "error";

interface FeedbackFormProps {
  onSubmitFeedback: (message: string) => Promise<void>;
}

export function FeedbackForm({ onSubmitFeedback }: FeedbackFormProps) {
  const [text, setText] = useState<string>("");
  const [status, setStatus] = useState<FormStatus>("typing");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (status === "success") {
    return <h3 className="success-banner">Дякуємо за ваш відгук!</h3>;
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStatus("submitting");
    setErrorMessage(null);

    try {
      await onSubmitFeedback(text);
      setStatus("success");
    } catch (err) {
      setStatus("error");
      setErrorMessage(err instanceof Error ? err.message : "Сталася помилка");
    }
  };

  const isSubmitting = status === "submitting";
  const isEmpty = text.trim().length === 0;

  return (
    <form onSubmit={handleSubmit} className="feedback-form">
      <h2>Залиште відгук</h2>
      <textarea
        value={text}
        disabled={isSubmitting}
        onChange={(e) => setText(e.target.value)}
        placeholder="Опишіть ваші враження..."
        rows={4}
      />

      {status === "error" && errorMessage && (
        <p className="error-alert">{errorMessage}</p>
      )}

      <button type="submit" disabled={isEmpty || isSubmitting}>
        {isSubmitting ? "Надсилання..." : "Надіслати"}
      </button>
    </form>
  );
}
```

---

## 20. Вибір структури стану: принципи проєктування та нормалізація

> 🔗 **Офіційний референс:** [Вибір структури стану (Choosing the State Structure)](https://uk.react.dev/learn/choosing-the-state-structure)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади надлишкового, суперечливого та нормалізованого стану, а також ВСІ практичні завдання (Challenges) з рефакторингу структури стану.

Структурування стану — це проєктування моделі даних вашого клієнтського застосунку. Невдало обрана структура призводить до багів синхронізації та надмірної складності оновлення.

### 5 правил структурування стану

1. **Групуйте пов'язані змінні:**
   Якщо дві або більше змінних стану завжди оновлюються одночасно, об'єднайте їх в один об'єкт.
   ```tsx
   // ❌ Погано: два окремих виклики для координат
   const [x, setX] = useState(0);
   const [y, setY] = useState(0);

   // ✅ Добре: єдиний об'єкт точки
   const [position, setPosition] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
   ```

2. **Уникайте суперечностей у стані:**
   Коли структура стану дозволяє одночасне існування двох взаємовиключних фактів, застосунок неминуче отримає баг. Використовуйте рядкові union-типи статусів замість незалежних boolean-полів.

3. **Уникайте надлишкового стану (*Redundant State*):**
   Якщо значення можна обчислити під час рендерингу з наявних пропсів або стану, **не зберігайте його у стані**:
   ```tsx
   // ❌ Погано: надлишковий стан fullName
   const [firstName, setFirstName] = useState("");
   const [lastName, setLastName] = useState("");
   const [fullName, setFullName] = useState(""); // Доводиться синхронізувати вручну!

   // ✅ Добре: виведення під час рендерингу
   const fullName = `${firstName} ${lastName}`.trim();
   ```

4. **Уникайте дублювання даних:**
   Зберігання одного й того самого об'єкта у кількох місцях призводить до ситуацій, коли одна частина інтерфейсу показує оновлені дані, а інша — застарілі.
   ```tsx
   // ❌ Погано: повне копіювання вибраного елемента
   const [items, setItems] = useState<Item[]>(initialItems);
   const [selectedItem, setSelectedItem] = useState<Item | null>(null);

   // ✅ Добре: зберігання лише унікального ID
   const [selectedId, setSelectedId] = useState<string | null>(null);
   const selectedItem = items.find((item) => item.id === selectedId) ?? null;
   ```

5. **Уникайте глибокої вкладеності (Нормалізація):**
   Глибоко вкладені об'єкти вимагають складного копіювання при імутабельному оновленні. Нормалізуйте складні структури даних за зразком реляційних баз даних: зберігайте сутності у вигляді пласких об'єктів-словників `Record<string, Entity>`, а порядок — масивом ідентифікаторів `string[]`.

---

## 21. Підйом стану (Lifting State Up)

> 🔗 **Офіційний референс:** [Поширення стану між компонентами (Sharing State Between Components)](https://uk.react.dev/learn/sharing-state-between-components)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці синхронізації стану (панелі акордеона, фільтровані списки) та ВСІ практичні завдання (Challenges) щодо підйому стану до спільного предка.

Коли кілька компонентів повинні відображати одні й ті самі дані або реагувати на зміни один одного, виникає потреба у спільному стані. React вирішує цю задачу через патерн **підйому стану** (*lifting state up*): стан переміщується до найближчого спільного батьківського компонента, який передає значення та функції оновлення дочірнім компонентам через пропси.

Розглянемо приклад конвертера температури, де два поля введення (Цельсій та Фаренгейт) синхронізуються між собою:

```tsx
function toCelsius(fahrenheit: number): number {
  return ((fahrenheit - 32) * 5) / 9;
}

function toFahrenheit(celsius: number): number {
  return (celsius * 9) / 5 + 32;
}

interface TemperatureInputProps {
  scale: "c" | "f";
  temperature: string;
  onTemperatureChange: (value: string) => void;
}

function TemperatureInput({
  scale,
  temperature,
  onTemperatureChange,
}: TemperatureInputProps) {
  const scaleLabel = scale === "c" ? "Цельсія" : "Фаренгейта";

  return (
    <fieldset>
      <legend>Введіть температуру в градусах {scaleLabel}:</legend>
      <input
        value={temperature}
        onChange={(e) => onTemperatureChange(e.target.value)}
      />
    </fieldset>
  );
}

function TemperatureCalculator() {
  const [temperature, setTemperature] = useState("");
  const [scale, setScale] = useState<"c" | "f">("c");

  const handleCelsiusChange = (value: string): void => {
    setScale("c");
    setTemperature(value);
  };

  const handleFahrenheitChange = (value: string): void => {
    setScale("f");
    setTemperature(value);
  };

  const numericTemp = parseFloat(temperature);
  const celsius = scale === "f" && !isNaN(numericTemp)
    ? toCelsius(numericTemp).toFixed(2)
    : temperature;
  const fahrenheit = scale === "c" && !isNaN(numericTemp)
    ? toFahrenheit(numericTemp).toFixed(2)
    : temperature;

  return (
    <div>
      <TemperatureInput
        scale="c"
        temperature={celsius}
        onTemperatureChange={handleCelsiusChange}
      />
      <TemperatureInput
        scale="f"
        temperature={fahrenheit}
        onTemperatureChange={handleFahrenheitChange}
      />
    </div>
  );
}
```

У цьому прикладі стан `temperature` та `scale` «живе» у батьківському `TemperatureCalculator`, а не у кожному `TemperatureInput` окремо. Батько обчислює похідні значення (конвертовані температури) та передає їх дочірнім компонентам. Такий підхід гарантує, що обидва поля завжди синхронізовані — **єдине джерело правди** (*single source of truth*).

## 22. Збереження та скидання стану: позиція в дереві та ключі

> 🔗 **Офіційний референс:** [Збереження та скидання стану (Preserving and Resetting State)](https://uk.react.dev/learn/preserving-and-resetting-state)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади поведінки стану при зміні дерева, скидання стану через унікальний key, та ВСІ практичні завдання (Challenges) з ізоляції стану.

Стан не живе всередині самої функції-компонента. У момент виклику функції React бере актуальний стан із внутрішнього сховища та зіставляє його з компонентом. **Стан прив'язаний до позиції компонента у дереві рендерингу (*Render Tree*)**.

### Стан зберігається, поки зберігається позиція в дереві

Поки компонент залишається на тій самій позиції в дереві рендерингу між рендерами, React **зберігає його стан**, навіть якщо значення пропсів кардинально змінилися:

```tsx
export function App() {
  const [isFancy, setIsFancy] = useState(false);

  return (
    <div>
      {/* Обидва вирази рендерять <Counter /> на одній і тій самій позиції (перший нащадок div) */}
      {isFancy ? (
        <Counter isFancy={true} />
      ) : (
        <Counter isFancy={false} />
      )}
      <button onClick={() => setIsFancy(!isFancy)}>Змінити стиль</button>
    </div>
  );
}
```

При перемиканні `isFancy` лічильник `Counter` не скидається на `0`, тому що для React це **той самий компонент на тій самій позиції**.

### Стан скидається при зміні структури дерева

Якщо на тій самій позиції з'являється інший тип компонента або змінюється структура контейнера, React повністю видаляє старе дерево разом з його станом:

```tsx
// Стан Counter буде знищено при перемиканні, оскільки позиції різні:
// В одній гілці батьком є <div>, у другій — <section>!
{isFancy ? (
  <div>
    <Counter />
  </div>
) : (
  <section>
    <Counter />
  </section>
)}
```

### Примусове скидання стану за допомогою ключа (`key`)

Найбільш елегантний та декларативний спосіб скинути стан компонента при зміні контексту — використання спеціального атрибута **`key`**.

Коли React бачить, що значення `key` у компонента змінилося, він розглядає його як **абсолютно новий компонент**. Старий екземпляр повністю демонтується, його стан знищується, а новий монтується з початковим станом:

```tsx
interface ChatProps {
  recipientId: string;
}

export function Messenger({ recipientId }: ChatProps) {
  // Завдяки key={recipientId} при виборі іншого співрозмовника
  // внутрішній стан чернетки тексту в <ChatBox /> гарантовано очиститься!
  return <ChatBox key={recipientId} recipientId={recipientId} />;
}
```

::note
Використання `key` для скидання стану усуває потребу у громіздких синхронізаціях через `useEffect`, гарантуючи чистий і надійний життєвий цикл компонентів.
::

---

## 23. Хук `useReducer`: структуроване управління складним станом

> 🔗 **Офіційний референс:** [Винесення логіки стану в редюсер (Extracting State Logic into a Reducer)](https://uk.react.dev/learn/extracting-state-logic-into-a-reducer)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці рефакторингу useState у useReducer (список завдань, месенджер) та ВСІ практичні завдання (Challenges) з написання чистих редюсерів.

Коли стан компонента стає складним — містить кілька взаємопов'язаних полів, підтримує багато різних операцій або має складну логіку переходів — `useState` стає незручним. Хук `useReducer` пропонує альтернативний підхід, натхненний патерном Redux: весь стан зосереджено в одному об'єкті, а зміни описуються **діями** (*actions*) та обробляються єдиною **функцією-редюсером** (*reducer function*).

```tsx
import { useReducer } from "react";

// Типи стану та дій
interface TaskState {
  tasks: TodoItem[];
  nextId: number;
  filter: "all" | "active" | "completed";
}

type TaskAction =
  | { type: "ADD_TASK"; payload: string }
  | { type: "TOGGLE_TASK"; payload: number }
  | { type: "DELETE_TASK"; payload: number }
  | { type: "SET_FILTER"; payload: "all" | "active" | "completed" };

// Початковий стан
const initialState: TaskState = {
  tasks: [],
  nextId: 1,
  filter: "all",
};

// Редюсер — чиста функція, що обчислює новий стан
function taskReducer(state: TaskState, action: TaskAction): TaskState {
  switch (action.type) {
    case "ADD_TASK":
      return {
        ...state,
        tasks: [
          ...state.tasks,
          { id: state.nextId, text: action.payload, done: false },
        ],
        nextId: state.nextId + 1,
      };
    case "TOGGLE_TASK":
      return {
        ...state,
        tasks: state.tasks.map((task) =>
          task.id === action.payload ? { ...task, done: !task.done } : task
        ),
      };
    case "DELETE_TASK":
      return {
        ...state,
        tasks: state.tasks.filter((task) => task.id !== action.payload),
      };
    case "SET_FILTER":
      return { ...state, filter: action.payload };
    default:
      return state;
  }
}

function TaskManager() {
  const [state, dispatch] = useReducer(taskReducer, initialState);
  const [inputText, setInputText] = useState("");

  const filteredTasks = state.tasks.filter((task) => {
    if (state.filter === "active") return !task.done;
    if (state.filter === "completed") return task.done;
    return true;
  });

  const handleAdd = (): void => {
    if (!inputText.trim()) return;
    dispatch({ type: "ADD_TASK", payload: inputText });
    setInputText("");
  };

  return (
    <div>
      <input
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleAdd()}
      />
      <button onClick={handleAdd}>Додати</button>

      <div>
        {(["all", "active", "completed"] as const).map((f) => (
          <button
            key={f}
            onClick={() => dispatch({ type: "SET_FILTER", payload: f })}
            style={{ fontWeight: state.filter === f ? "bold" : "normal" }}
          >
            {f === "all" ? "Усі" : f === "active" ? "Активні" : "Виконані"}
          </button>
        ))}
      </div>

      <ul>
        {filteredTasks.map((task) => (
          <li key={task.id}>
            <input
              type="checkbox"
              checked={task.done}
              onChange={() => dispatch({ type: "TOGGLE_TASK", payload: task.id })}
            />
            <span>{task.text}</span>
            <button onClick={() => dispatch({ type: "DELETE_TASK", payload: task.id })}>
              ✕
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

Ключова перевага `useReducer` — **типобезпечний дискримінований union** для дій. TypeScript гарантує, що ви не забудете обробити жоден тип дії, а всередині кожного `case` блоку `action.payload` автоматично звужується до правильного типу. Редюсер є чистою функцією — його легко тестувати окремо від React, передаючи стан та дію і перевіряючи результат.

## 24. Context API: передавання даних без «пропс-дрілінгу»

> 🔗 **Офіційний референс:** [Глибока передача даних через контекст (Passing Data Deeply with Context)](https://uk.react.dev/learn/passing-data-deeply-with-context) та [Масштабування з контекстом і редюсером](https://uk.react.dev/learn/scaling-up-with-reducer-and-context)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ інтерактивні sandbox-приклади контексту (рівні заголовків, тема, масштабний Todo-застосунок) та ВСІ практичні завдання (Challenges).
> 📁 **Практичні навчальні проєкти модуля:**
> - [01-shopping-cart](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/04-context-api/01-shopping-cart) — кошик покупок на Context API. Реалізація глобального стану через `CartContext` і `CartProvider`. Додавання товарів у кошик, зміна кількості, розрахунок загальної вартості замовлення та очищення кошика без «пропс-дрілінгу».
> - [02-ticket-booking-system](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/04-context-api/02-ticket-booking-system) — комплексна система бронювання квитків із багатоетапним контекстом. Керування вибором подій (`EventList`), схемою зали та вибором місць (`SeatSelection`), кошиком та підтвердженням замовлення (`BookingConfirmation`).

У великих застосунках часто виникає ситуація, коли дані потрібні глибоко вкладеним компонентам, але проміжні компоненти ієрархії не використовують ці дані — лише транзитно передають їх далі. Цю проблему називають **пропс-дрілінгом** (*prop drilling*), і вона робить код крихким та важкопідтримуваним. **Context API** дозволяє «телепортувати» дані безпосередньо до компонентів, які їх потребують, обминаючи проміжні рівні.

```tsx
import { createContext, useContext, useReducer } from "react";

// Типи
interface ThemeContextType {
  theme: "light" | "dark";
  toggleTheme: () => void;
}

// Створення контексту з початковим значенням
const ThemeContext = createContext<ThemeContextType | null>(null);

// Кастомний хук для безпечного доступу до контексту
function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}

// Компонент-провайдер
function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  const toggleTheme = (): void => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Глибоко вкладений компонент — отримує тему без пропс-дрілінгу
function ThemedButton() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      style={{
        backgroundColor: theme === "dark" ? "#1e293b" : "#f8fafc",
        color: theme === "dark" ? "#e2e8f0" : "#0f172a",
        border: "1px solid",
        padding: "0.5rem 1rem",
        borderRadius: "0.375rem",
      }}
    >
      Поточна тема: {theme === "dark" ? "Темна" : "Світла"}
    </button>
  );
}

// Використання
function App() {
  return (
    <ThemeProvider>
      <div>
        <h1>Додаток із темізацією</h1>
        <ThemedButton />
      </div>
    </ThemeProvider>
  );
}
```

::warning
Зверніть увагу на патерн `createContext<ThemeContextType | null>(null)` із кастомним хуком `useTheme()`, який кидає помилку, якщо контекст використовується за межами провайдера. Це є рекомендованим підходом у TypeScript-проєктах — він усуває необхідність у перевірці `null` кожного разу, коли ви викликаєте `useContext`, та одразу повідомляє розробника про помилку конфігурації.
::

### Комбінування `useReducer` та Context

Найпотужнішим патерном локального управління станом є комбінація `useReducer` для логіки стану та Context для його поширення. Цей підхід фактично відтворює архітектуру Redux на рівні окремого піддерева компонентів:

```tsx
interface AppState {
  user: { name: string; email: string } | null;
  notifications: string[];
}

type AppAction =
  | { type: "LOGIN"; payload: { name: string; email: string } }
  | { type: "LOGOUT" }
  | { type: "ADD_NOTIFICATION"; payload: string }
  | { type: "CLEAR_NOTIFICATIONS" };

const AppStateContext = createContext<AppState | null>(null);
const AppDispatchContext = createContext<React.Dispatch<AppAction> | null>(null);

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case "LOGIN":
      return { ...state, user: action.payload };
    case "LOGOUT":
      return { ...state, user: null };
    case "ADD_NOTIFICATION":
      return { ...state, notifications: [...state.notifications, action.payload] };
    case "CLEAR_NOTIFICATIONS":
      return { ...state, notifications: [] };
    default:
      return state;
  }
}

function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, {
    user: null,
    notifications: [],
  });

  return (
    <AppStateContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>
        {children}
      </AppDispatchContext.Provider>
    </AppStateContext.Provider>
  );
}

function useAppState(): AppState {
  const context = useContext(AppStateContext);
  if (!context) throw new Error("useAppState must be used within AppProvider");
  return context;
}

function useAppDispatch(): React.Dispatch<AppAction> {
  const context = useContext(AppDispatchContext);
  if (!context) throw new Error("useAppDispatch must be used within AppProvider");
  return context;
}
```

::tip
Розділення стану та диспатчу на два окремих контексти — важлива оптимізація. Компоненти, які лише диспатчать дії (наприклад, кнопка «Вийти»), не будуть перерендерюватися при зміні стану, адже вони підписані лише на `AppDispatchContext`, значення якого не змінюється між рендерами.
::

---

# Частина IV. Запасні виходи (Escape Hatches)

## 25. Збереження значень за допомогою рефів: хук `useRef`

> 🔗 **Офіційний референс:** [Збереження значень за допомогою рефів (Referencing Values with Refs)](https://uk.react.dev/learn/referencing-values-with-refs)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади (секундоміри, фіксація попередніх значень, лічильники кліків без рендеру) та ВСІ практичні завдання (Challenges) щодо useRef.

Іноді компоненту потрібно зберігати певну інформацію між рендерами, але зміна цієї інформації **не повинна викликати новий рендер**. Для таких задач у React передбачено хук `useRef`.

Хук `useRef` повертає звичайний JavaScript-об'єкт із єдиною мутабельною властивістю: `{ current: initialValue }`.

```tsx
import { useRef, useState, useEffect } from "react";

export function StopWatch() {
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  
  // Зберігаємо ID таймера у рефі, оскільки зміна таймера не змінює UI напряму
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const handleStart = (): void => {
    if (isRunning) return;
    setIsRunning(true);
    intervalRef.current = setInterval(() => {
      setElapsedTime((prev) => prev + 10);
    }, 10);
  };

  const handleStop = (): void => {
    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setIsRunning(false);
  };

  const handleReset = (): void => {
    handleStop();
    setElapsedTime(0);
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current !== null) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const formatTime = (ms: number): string => {
    const seconds = Math.floor((ms % 60000) / 1000);
    const centiseconds = Math.floor((ms % 1000) / 10);
    return `${seconds}.${String(centiseconds).padStart(2, "0")}s`;
  };

  return (
    <div className="stopwatch">
      <h2>Секундомір: {formatTime(elapsedTime)}</h2>
      <button onClick={handleStart} disabled={isRunning}>Старт</button>
      <button onClick={handleStop} disabled={!isRunning}>Стоп</button>
      <button onClick={handleReset}>Скидання</button>
    </div>
  );
}
```

### Відмінності між `useRef` та `useState`

| Характеристика | `useRef(initialValue)` | `useState(initialValue)` |
| :--- | :--- | :--- |
| **Що повертає** | Об'єкт `{ current: initialValue }` | Кортеж `[value, setValue]` |
| **Зміна викликає рендер?** | **Ні** (мутація `.current` тиха) | **Так** (планує повторний рендер) |
| **Мутабельність** | Мутабельний (можна читати й писати `.current`) | Імутабельний (оновлення тільки через `set`) |
| **Коли читати/писати** | У подіях та ефектах (не під час рендеру!) | У будь-який момент під час рендеру |

::warning
**Суворе правило чистоти:** Ніколи не записуйте і не читайте `ref.current` безпосередньо під час виконання функції-рендерингу. Якщо значення потрібне для відображення в JSX — використовуйте `useState`.
::

---

## 26. Маніпулювання DOM за допомогою рефів: фокус, скрол та кастомні компоненти

> 🔗 **Офіційний референс:** [Маніпулювання DOM за допомогою рефів (Manipulating the DOM with Refs)](https://uk.react.dev/learn/manipulating-the-dom-with-refs)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці взаємодії з DOM (фокус, скрол до коментаря, відтворення медіа, callback refs) та ВСІ практичні завдання (Challenges) щодо DOM-рефів.

Найпоширенішим практичним використанням рефів є безпосередня взаємодія з елементами браузерного DOM: встановлення фокусу, прокручування контейнера, вимірювання розмірів (`getBoundingClientRect`) чи керування медіаплеєром (`play()`, `pause()`).

### Доступ до DOM-елемента у TypeScript

Щоб зв'язати реф із DOM-вузлом, передайте його в атрибут `ref` відповідного JSX-тегу. Початковим значенням завжди передається `null`:

```tsx
import { useRef } from "react";

export function SearchField() {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFocus = () => {
    // Оператор optional chaining перевіряє наявність DOM-вузла
    inputRef.current?.focus();
  };

  return (
    <div className="search-box">
      <input ref={inputRef} type="text" placeholder="Почніть вводити назву..." />
      <button onClick={handleFocus}>Встановити фокус</button>
    </div>
  );
}
```

### Передача рефу до власного компонента (React 19 vs forwardRef)

За замовчуванням React не дозволяє компонентам отримувати доступ до DOM-вузлів інших компонентів. У класичному React для цього використовувалася функція `forwardRef`, проте починаючи з **React 19**, `ref` є звичайним пропсом:

```tsx
interface CustomInputProps {
  label: string;
  placeholder?: string;
  ref?: React.Ref<HTMLInputElement>;
}

// У сучасному React 19 проп ref передається напряму:
export function CustomInput({ label, placeholder, ref }: CustomInputProps) {
  return (
    <label className="input-group">
      <span>{label}</span>
      <input ref={ref} placeholder={placeholder} />
    </label>
  );
}
```

### Керування списком рефів (Callback Refs)

Якщо кількість DOM-елементів динамічна (наприклад, перелік повідомлень у чаті), не можна викликати `useRef` усередині циклу. Для цього використовується **колбек-реф** (*callback ref*):

```tsx
import { useRef } from "react";

interface CommentItem {
  id: number;
  text: string;
}

export function CommentList({ comments }: { comments: CommentItem[] }) {
  // Зберігаємо мапу DOM-вузлів у єдиному рефі
  const itemsRef = useRef<Map<number, HTMLLIElement>>(new Map());

  const scrollToComment = (id: number) => {
    const node = itemsRef.current.get(id);
    node?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  };

  return (
    <div>
      <button onClick={() => scrollToComment(comments[comments.length - 1].id)}>
        До останнього коментаря
      </button>
      <ul>
        {comments.map((comment) => (
          <li
            key={comment.id}
            ref={(node) => {
              if (node) {
                itemsRef.current.set(comment.id, node);
              } else {
                itemsRef.current.delete(comment.id);
              }
            }}
          >
            {comment.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Портали в React: рендеринг за межі DOM-ієрархії (`createPortal`)

Коли потрібно відрендерити дочірній елемент (модальне вікно, спливаючу підказку, контекстне меню або сповіщення) у DOM-вузол, розташований за межами кореневої структури батьківського компонента (наприклад, прямо в `document.body` для уникнення проблем із `z-index` чи `overflow: hidden`), використовується API `ReactDOM.createPortal`. При цьому React зберігає повну віртуальну ієрархію: спливання подій (Event Bubbling) та Context API продовжують працювати крізь портал.

> 📁 **Практичний навчальний проєкт модуля:**
> - [01-react-portals](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/08-portals/01-react-portals) — повна практична енциклопедія використання `createPortal`: модальні вікна із затемненням та блокуванням скролу (`Modal`, `ModalExample`), випадаючі списки (`Dropdown`), контекстні меню за координатами кліку (`ContextMenu`) та тост-сповіщення (`Toast`, `ToastExample`).

---

## 27. Синхронізація з ефектами: хук `useEffect` та функції очищення

> 🔗 **Офіційний референс:** [Синхронізація з ефектами (Synchronizing with Effects)](https://uk.react.dev/learn/synchronizing-with-effects)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади підключення до сторонніх систем (чат-сервери, анімації, події вікна, очищення) та ВСІ практичні завдання (Challenges) щодо useEffect.
> 📁 **Практичні навчальні проєкти модуля:**
> - [01-react-effects-sample](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/06-effects-and-lifecycle/01-react-effects-sample) — фундаментальний анатомічний довідник патернів `useEffect`: рендер без масиву залежностей (`EffectOnEveryRender`), одноразовий запуск монтування (`EffectOnce`), ефект із залежностями (`EffectWithDeps`), функція очищення таймерів/слухачів (`EffectCleanup`), асинхронні запити (`AsyncEffect`) та збереження попереднього значення (`PreviousValueEffect`).
> - [02-react-lifecycle-and-effects](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/06-effects-and-lifecycle/02-react-lifecycle-and-effects) — практичні UI-кейси життєвого циклу компонентів: цифрові таймери та секундоміри (`Timer`, `Stopwatch`, `IntervalDemo`), відстеження кліків поза межами для випадаючого меню (`Dropdown`), синхронізація з `document.title`, моніторинг інтернет-з'єднання (`OnlineStatus`) та оптимізація вхідних даних пошуку (`SearchComponent`).

Компоненти React зосереджені на обчисленні розмітки. Але вебдодаток повинен синхронізуватися із зовнішніми системами: сторонніми JS-бібліотеками, мережевими підключеннями, сокетами, системними таймерами браузера. Для цього призначений хук `useEffect`.

```tsx
import { useState, useEffect } from "react";

interface ChatConnection {
  connect: () => void;
  disconnect: () => void;
}

function createConnection(roomId: string): ChatConnection {
  return {
    connect: () => console.log(`Підключено до кімнати: ${roomId}`),
    disconnect: () => console.log(`Відключено від кімнати: ${roomId}`),
  };
}

export function ChatRoom({ roomId }: { roomId: string }) {
  const [serverUrl, setServerUrl] = useState("https://api.chat.dev");

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();

    // Функція очищення (cleanup function)
    return () => {
      connection.disconnect();
    };
  }, [roomId]); // Ефект перезапускається щоразу при зміні roomId

  return <h3>Кімната чату: {roomId}</h3>;
}
```

### Життєвий цикл функції очищення (Cleanup)

Функція очищення, яку повертає `useEffect`, гарантує відсутність витоків пам'яті та завислих з'єднань:
1. Вона викликається **перед кожним повторним виконанням ефекту** (із попередніми значеннями).
2. Вона викликається **під час остаточного розмонтування компонента** (видалення з DOM).

::note
**Чому ефекти запускаються двічі у режимі розробки?**
У `<React.StrictMode>` React навмисно монтує компонент, негайно розмонтовує його і монтує знову (`mount -> cleanup -> mount`). Це перевіряє, чи правильно ваша функція очищення нейтралізує побічну дію (скидає таймери, закриває сокети або скасовує мережеві запити через `AbortController`).
::

---

## 28. Можливо, вам не потрібен ефект: антипатерни та правильні альтернативи

> 🔗 **Офіційний референс:** [Можливо, вам не потрібен ефект (You Might Not Need an Effect)](https://uk.react.dev/learn/you-might-not-need-an-effect)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ практичні кейси усунення зайвих ефектів (фільтрація, кешування, скидання форм через key, ланцюжки оновлень) та ВСІ челенджі з рефакторингу.

Одна з найпоширеніших помилок розробників — надмірне використання `useEffect`. Ефекти є «запасним виходом» з парадигми React, і коли їх використовують для звичайної синхронізації стану всередині програми, код стає повільним, складним і крихким.

### 4 типові антипатерни та їхні правильні рішення

#### 1. Трансформація даних для відображення
- ❌ **Погано:** Зберігати список у стані, потім у `useEffect` фільтрувати його і класти у другий стан.
- ✅ **Правильно:** Обчислюйте відфільтровані дані прямо під час рендерингу (або через `useMemo`, якщо фільтрація важка):
```tsx
// ✅ Відфільтрований список обчислюється на льоту під час рендеру!
const visibleTodos = useMemo(() => {
  return todos.filter((todo) => !todo.completed);
}, [todos]);
```

#### 2. Скидання форми при зміні вибору користувача
- ❌ **Погано:** Писати `useEffect(() => { setDraft(''); }, [userId])`, що викликає каскадний рендер зі застарілими даними на одну мить.
- ✅ **Правильно:** Розділити компоненти за допомогою ключа `key`:
```tsx
// ✅ Зміна key повністю перестворює внутрішній стан форми без жодного useEffect!
<ProfileForm key={selectedUserId} userId={selectedUserId} />
```

#### 3. Обробка дій користувача
- ❌ **Погано:** Встановлювати прапорець `setBought(true)` в обробнику кнопки, а в `useEffect` відправляти запит на сервер при зміні прапорця.
- ✅ **Правильно:** Відправляти мережевий запит безпосередньо у функції обробника події `handleBuyClick`.

#### 4. Сповіщення батьківського компонента про зміну стану
- ❌ **Погано:** Викликати `useEffect(() => { onChange(value); }, [value, onChange])`.
- ✅ **Правильно:** Викликати `onChange` безпосередньо в обробнику події введення всередині дочірнього компонента.

---

## 29. Життєвий цикл реактивних ефектів: мислення процесами синхронізації

> 🔗 **Офіційний референс:** [Життєвий цикл реактивних ефектів (Lifecycle of Reactive Effects)](https://uk.react.dev/learn/lifecycle-of-reactive-effects)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці повторної синхронізації (перемикання кімнат чату, анімації), роботу лінтера exhaustive-deps та ВСІ практичні завдання (Challenges).

Компоненти мають життєвий цикл: вони монтуються, оновлюються пропсами або станом, і розмонтовуються. Проте **ефекти мають зовсім інший життєвий цикл**.

### Ментальна модель: Початок і кінець синхронізації

Ефект не думає категоріями «перший рендер чи п'ятий рендер». Ефект вміє лише дві речі:
- **Почати синхронізацію (*Start synchronizing*)** із зовнішньою системою.
- **Припинити синхронізацію (*Stop synchronizing*)**, викликавши функцію очищення.

Якщо значення залежностей змінилися, React спочатку **зупиняє** попередню синхронізацію (викликає `cleanup`), а потім **починає** нову з актуальними даними.

### Реактивні значення та правило вичерпних залежностей

Усі змінні, оголошені всередині тіла компонента (включаючи `props`, `state` та похідні змінні), є **реактивними**, оскільки вони беруть участь у потоці рендерингу і можуть змінюватися:

```tsx
function Chat({ roomId, theme }: { roomId: string; theme: string }) {
  useEffect(() => {
    const server = connectToServer(roomId);
    server.on("message", (msg) => {
      showNotification(msg, theme);
    });

    return () => server.disconnect();
  }, [roomId, theme]); // Обидві змінні реактивні і зобов'язані бути вказані!
}
```

::important
Правило лінтера `react-hooks/exhaustive-deps` вимагає, щоб **кожне реактивне значення**, прочитане всередині ефекту, обов'язково було присутнє у масиві залежностей. Якщо значення не повинно перезапускати ефект, його потрібно або винести за межі компонента, або скористатися техніками розділення подій та ефектів.
::

---

## 30. Розділення подій та ефектів: реактивна проти нереактивної логіки

> 🔗 **Офіційний референс:** [Розділення подій та ефектів (Separating Events from Effects)](https://uk.react.dev/learn/separating-events-from-effects)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-ілюстрації розмежування логіки взаємодії користувача та синхронізації ефектів, патерни useEffectEvent/рефів та всі челенджі.

У реальних застосунках часто виникає дилема: певний фрагмент коду повинен прочитати свіже значення стану, але зміна цього стану **не повинна перезапускати весь ефект синхронізації**.

- **Обробники подій (*Event Handlers*):** запускаються виключно у відповідь на конкретну взаємодію користувача. Вони не є реактивними щодо змін пропсів.
- **Ефекти (*Effects*):** запускаються щоразу, коли змінюються реактивні залежності, для збереження актуальності зв'язку.

### Проблема змішування реактивних залежностей

Уявіть, що при зміні `roomId` ми повинні підключитися до чату і вивести сповіщення кольором поточної теми (`theme`). Якщо ми просто додамо `theme` у залежності, чат буде **розривати та відновлювати сокет-з'єднання щоразу, коли користувач просто перемикає світлу/темну тему**:

```tsx
// ❌ Погано: перемикання theme перезапускає мережеве підключення!
useEffect(() => {
  const socket = connect(roomId);
  socket.on("connect", () => {
    notify(`Підключено!`, theme); // theme потрібна, але не для перепідключення
  });
  return () => socket.close();
}, [roomId, theme]);
```

### Патерн збереження нереактивної логіки через рефи

Щоб прочитати найсвіжіше значення `theme` без включення його до залежностей, використовують патерн збереження колбека у `useRef`:

```tsx
export function ChatWithTheme({ roomId, theme }: { roomId: string; theme: string }) {
  // Зберігаємо актуальну тему у рефі
  const themeRef = useRef(theme);
  themeRef.current = theme;

  useEffect(() => {
    const socket = connect(roomId);
    socket.on("connect", () => {
      // Читаємо актуальне значення без реактивної прив'язки
      notify("Підключено!", themeRef.current);
    });

    return () => socket.close();
  }, [roomId]); // Тепер ефект залежить виключно від roomId!
}
```

Цей підхід дозволяє чітко розмежовувати: що саме є **тригером повторної синхронізації** (`roomId`), а що є **допоміжними даними** під час виконання (`theme`).

---

## 31. Видалення зайвих залежностей ефектів та оптимізація синхронізації

> 🔗 **Офіційний референс:** [Видалення залежностей ефектів (Removing Effect Dependencies)](https://uk.react.dev/learn/removing-effect-dependencies)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці усунення непотрібних залежностей (винесення функцій, переміщення всередину ефекту, функціональні оновлення) та ВСІ завдання (Challenges).

Коли лінтер повідомляє про пропущену залежність в `useEffect`, розробники-початківці часто просто додають директиву `// eslint-disable-next-line`. Це небезпечний антипатерн, який призводить до застарілих замикань (*stale closures*) та прихованих багів. Залежності потрібно усувати грамотно.

### 4 стратегії видалення залежностей

#### 1. Перемістіть статичний код за межі компонента
Якщо функція або об'єкт не використовують пропси чи стан, винесіть їх за межі компонента. Вони перестануть бути реактивними:
```tsx
// Поза компонентом: посилання стабільне, залежність не потрібна
const options = { serverUrl: "https://api.example.com", timeout: 5000 };

function DataViewer() {
  useEffect(() => {
    fetchData(options);
  }, []); // options не є залежністю!
}
```

#### 2. Перенесіть створення об'єкта або функції всередину ефекту
Якщо об'єкт потрібен лише цьому ефекту, створіть його всередині:
```tsx
useEffect(() => {
  const options = { roomId: id };
  const conn = createConn(options);
  return () => conn.close();
}, [id]); // Замість залежності від об'єкта options — залежність від простого рядка id
```

#### 3. Використовуйте функціональне оновлення стану
Якщо ефект читає стан лише для того, щоб обчислити наступне значення, позбудьтеся читання за допомогою `setCount(prev => prev + 1)`:
```tsx
// ❌ Потребує count у залежностях:
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, [count]);

// ✅ Не потребує count у залежностях:
useEffect(() => {
  const id = setInterval(() => setCount((prev) => prev + 1), 1000);
  return () => clearInterval(id);
}, []); // Таймер створюється один раз!
```

#### 4. Розділіть один ефект на кілька незалежних
Якщо один ефект одночасно синхронізує аналітику та завантажує дані користувача, розділіть його на два окремих хуки `useEffect`, кожен зі своїми точковими залежностями.

---

## 32. Кастомні хуки: повторне використання та композиція реактивної логіки

> 🔗 **Офіційний референс:** [Повторне використання логіки з кастомними хуками (Reusing Logic with Custom Hooks)](https://uk.react.dev/learn/reusing-logic-with-custom-hooks)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ інтерактивні sandbox-приклади кастомних хуків (useOnlineStatus, useChatRoom, анімаційні хуки) та ВСІ практичні завдання (Challenges) з розв'язками.

Кастомні хуки дозволяють виносити повторювану реактивну логіку (поєднання стану, рефів та ефектів) в окремі функції. Якщо компоненти відповідають за перевикористання UI-структури, то **кастомні хуки відповідають за перевикористання поведінки**.

### Правила побудови кастомних хуків

1. Назва функції завжди починається з префікса `use` (`useFetch`, `useOnlineStatus`, `useWindowSize`).
2. Усередині можна вільно викликати будь-які стандартні або інші кастомні хуки React.
3. Кожен виклик кастомного хука має **власний незалежний стан** — хук ділиться логікою зі станом, а не самим екземпляром стану!

### Приклад 1. Хук відстеження мережевого з'єднання `useOnlineStatus`

```tsx
import { useState, useEffect } from "react";

export function useOnlineStatus(): boolean {
  const [isOnline, setIsOnline] = useState<boolean>(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return isOnline;
}
```

### Приклад 2. Типізований хук отримання даних `useFetch` з AbortController

```tsx
export function useFetch<T>(url: string): {
  data: T | null;
  isLoading: boolean;
  error: string | null;
} {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData(): Promise<void> {
      try {
        setIsLoading(true);
        setError(null);
        const response = await fetch(url, { signal: controller.signal });

        if (!response.ok) {
          throw new Error(`HTTP помилка: ${response.status}`);
        }

        const result: T = await response.json();
        setData(result);
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err.message);
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
    return () => controller.abort();
  }, [url]);

  return { data, isLoading, error };
}
```

### Композиція хуків у компонентах

```tsx
export function Dashboard() {
  const isOnline = useOnlineStatus();
  const { data: metrics, isLoading } = useFetch<{ cpu: number; memory: number }>(
    "/api/v1/system/metrics"
  );

  if (!isOnline) {
    return <div className="offline-banner">З'єднання з мережею втрачено...</div>;
  }

  if (isLoading) return <p>Оновлення метрик...</p>;

  return (
    <div className="metrics-card">
      <p>CPU: {metrics?.cpu}%</p>
      <p>Пам'ять: {metrics?.memory}%</p>
    </div>
  );
}
```

::tip
Кастомні хуки приховують складні деталі роботи з DOM, браузерними подіями та таймерами, роблячи код компонентів чистим, декларативним і легко читабельним.
::

---
---

# Частина V. Екосистема React

## 33. React Router: маршрутизація в SPA

> 🔗 **Офіційний референс:** [Офіційна документація React Router (React Router Docs)](https://reactrouter.com/en/main)
> 📥 **Вимога до наповнення статті:** Витягнути повноцінний інтерактивний sandbox-приклад SPA-маршрутизації (вкладені маршрути, loader-функції, параметри URL) та практичні завдання на налаштування роутингу.
> 📁 **Практичні навчальні проєкти модуля:**
> - [01-react-router-sample](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/11-react-router-v7/01-react-router-sample) — повнофункціональний еталонний проєкт на React Router v7: глобальна розмітка (`Layout` + `Outlet`), навігація через `NavLink`, динамічні маршрути (`/products/:id`), пошукові параметри (`useSearchParams`), захищені маршрути авторизації (`ProtectedRoute`, `useAuth`, `Login`), вкладена панель керування `Dashboard`, обробка винятків `ErrorBoundary` та сторінка 404.
> - [02-react-router-sample-clean](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/11-react-router-v7/02-react-router-sample-clean) — очищений та мінімалістичний шаблон React Router v7 (Vite 7, React Router 7.9) для швидкого старту та виконання самостійних завдань.

Односторінкові застосунки (*Single Page Applications*, SPA) відображають різний вміст залежно від URL-адреси, але без повного перезавантаження сторінки. **React Router** — це стандартна бібліотека маршрутизації для React, яка відображає URL на компоненти та надає API для навігації.

::tabs
::tabs-item{label="npm"}
```bash
npm install react-router-dom
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add react-router-dom
```
::
::

### Базова конфігурація маршрутів

```tsx
import { BrowserRouter, Routes, Route, Link, NavLink, Outlet } from "react-router-dom";

// Layout — спільний каркас з навігацією
function Layout() {
  return (
    <div>
      <nav>
        <NavLink
          to="/"
          className={({ isActive }) => (isActive ? "nav-active" : "")}
        >
          Головна
        </NavLink>
        <NavLink
          to="/about"
          className={({ isActive }) => (isActive ? "nav-active" : "")}
        >
          Про нас
        </NavLink>
        <NavLink
          to="/users"
          className={({ isActive }) => (isActive ? "nav-active" : "")}
        >
          Користувачі
        </NavLink>
      </nav>

      {/* Outlet рендерить дочірній маршрут */}
      <main>
        <Outlet />
      </main>
    </div>
  );
}

function HomePage() {
  return <h1>Головна сторінка</h1>;
}

function AboutPage() {
  return <h1>Про нас</h1>;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="users" element={<UsersPage />} />
          <Route path="users/:userId" element={<UserDetailPage />} />
          <Route path="*" element={<h1>404 — Сторінку не знайдено</h1>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### Параметри маршруту та програмна навігація

Хук `useParams` дозволяє отримати динамічні сегменти URL, а `useNavigate` — програмно переходити між сторінками:

```tsx
import { useParams, useNavigate, useSearchParams } from "react-router-dom";

function UserDetailPage() {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const { data: user, isLoading } = useFetch<{ id: number; name: string; email: string }>(
    `https://jsonplaceholder.typicode.com/users/${userId}`
  );

  if (isLoading) return <p>Завантаження...</p>;
  if (!user) return <p>Користувача не знайдено</p>;

  return (
    <div>
      <button onClick={() => navigate(-1)}>← Назад</button>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      <button onClick={() => navigate("/users")}>До списку</button>
    </div>
  );
}
```

### Пошукові параметри (Query Parameters)

```tsx
function UsersPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get("q") ?? "";

  const { data: users } = useFetch<{ id: number; name: string }[]>(
    "https://jsonplaceholder.typicode.com/users"
  );

  const filteredUsers = users?.filter((user) =>
    user.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setSearchParams({ q: e.target.value })}
        placeholder="Пошук користувача..."
      />
      <ul>
        {filteredUsers?.map((user) => (
          <li key={user.id}>
            <Link to={`/users/${user.id}`}>{user.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

::note
Компонент `NavLink` відрізняється від `Link` тим, що автоматично додає CSS-клас або стиль для активного маршруту. Проп `className` приймає функцію з об'єктом `{ isActive, isPending }`, що дозволяє стилізувати поточний пункт навігації.
::

---

## 34. Axios: HTTP-клієнт із розширеними можливостями

> 🔗 **Офіційний референс:** [Офіційна документація Axios (Axios HTTP Docs)](https://axios-http.com/docs/intro)
> 📥 **Вимога до наповнення статті:** Витягнути sandbox-приклади створення типізованого інстансу з interceptors (перехоплювачами токенів та помилок), кастомний хук useAxios та практичні вправи.

Хоча вбудований `fetch` API цілком придатний для простих запитів, у виробничих проєктах часто обирають **Axios** — HTTP-клієнт, що надає автоматичну серіалізацію/десеріалізацію JSON, перехоплювачі запитів (*interceptors*), налаштування таймаутів, скасування запитів та зручнішу обробку помилок.

::tabs
::tabs-item{label="npm"}
```bash
npm install axios
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add axios
```
::
::

### Створення типізованого Axios-інстансу

```tsx
import axios, { AxiosInstance, AxiosError } from "axios";

// Типи для API
interface ApiError {
  message: string;
  statusCode: number;
}

interface User {
  id: number;
  name: string;
  email: string;
  phone: string;
}

interface CreateUserDTO {
  name: string;
  email: string;
  phone: string;
}

// Створюємо інстанс із базовими налаштуваннями
const api: AxiosInstance = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Перехоплювач запитів — додає токен авторизації
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Перехоплювач відповідей — централізована обробка помилок
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("authToken");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Типізовані функції для API
const usersApi = {
  getAll: () => api.get<User[]>("/users"),
  getById: (id: number) => api.get<User>(`/users/${id}`),
  create: (data: CreateUserDTO) => api.post<User>("/users", data),
  update: (id: number, data: Partial<CreateUserDTO>) =>
    api.patch<User>(`/users/${id}`, data),
  delete: (id: number) => api.delete(`/users/${id}`),
};
```

### Використання Axios із хуком

```tsx
function useAxiosFetch<T>(fetcher: () => Promise<{ data: T }>) {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function load(): Promise<void> {
      try {
        setIsLoading(true);
        const response = await fetcher();
        setData(response.data);
      } catch (err) {
        if (axios.isAxiosError(err)) {
          setError(err.response?.data?.message ?? err.message);
        } else if (err instanceof Error) {
          setError(err.message);
        }
      } finally {
        setIsLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, []);

  return { data, isLoading, error };
}

// Використання
function UserListWithAxios() {
  const { data: users, isLoading, error } = useAxiosFetch(() => usersApi.getAll());

  if (isLoading) return <p>Завантаження...</p>;
  if (error) return <p>Помилка: {error}</p>;

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name} — {user.email}</li>
      ))}
    </ul>
  );
}
```

::note
Функція `axios.isAxiosError(err)` — це типовий гард (*type guard*), який звужує тип помилки до `AxiosError`. Це дозволяє безпечно звернутися до `err.response`, `err.config` та інших специфічних полів Axios.
::

## 35. Redux: класичний підхід до глобального стану

> 🔗 **Офіційний референс:** [Класична документація Redux (Redux Core Documentation)](https://redux.js.org/introduction/getting-started)
> 📥 **Вимога до наповнення статті:** Витягнути sandbox-приклади еволюції Redux: від одного HTML-файлу на ванільному JS з підпискою через store.subscribe до зв'язки з React через react-redux (Provider, useSelector, useDispatch) та суворою типізацією TSX.
> 📁 **Практичні навчальні проєкти модуля (Еволюція класичного Redux):**
> - [01-redux-vanilla-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/01-redux-vanilla-counter) — Redux без React та бандлерів в одному HTML/JS файлі: створення сховища `createStore`, чиста функція редюсера, диспетчеризація дій `dispatch()`, читання стану `getState()` та підписка `subscribe()`.
> - [02-redux-vanilla-todo](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/02-redux-vanilla-todo) — модульна архітектура чистого Redux: константи дій (`actionTypes`), фабрики дій (`todoActions`), ізольований редюсер списку задач (`todoReducer`) та ручне оновлення DOM через підписку на стор.
> - [03-redux-react-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/03-redux-react-counter) — інтеграція Redux у React-застосунок: обгортка `<Provider store={store}>` з бібліотеки `react-redux`, хуки `useSelector` та `useDispatch`.
> - [04-redux-react-todo](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/04-redux-react-todo) — повноцінний React-додаток TodoList на класичному Redux: структурування стану списку завдань, поєднання форми з локальним станом та глобального стору.
> - [05-redux-classic-bookstore-thunk](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/05-redux-classic-bookstore-thunk) — комплексний класичний застосунок «Книжковий магазин»: фільтрація, статистика, порівняння застарілого HOC `connect()` (файл `BookListConnect.example.jsx`) із хуками, підключення middleware `redux-thunk` для сайд-ефектів.

Більшість розробників знайомляться з Redux у контексті React, через що виникає хибне враження, ніби Redux — це частина React або бібліотека, створена виключно для нього. Насправді **Redux не має жодної прямої прив'язки до React**. Це абсолютно самостійна бібліотека з крихітним розміром (близько 2 Кб), яка реалізує патерн передбачуваного контейнера стану (*predictable state container*) для будь-якого JavaScript-оточення: браузера, Node.js, Angular, Vue або звичайного скрипта.

Щоб по-справжньому зрозуміти Redux і не заплутатися в надбудовах, ми пройдемо еволюційний шлях: почнемо з одного HTML-файлу на чистому JavaScript, розберемо кожну концепцію крок за кроком і лише потім інтегруємо сховище в React.

### Етап 1: Redux без React — один HTML-файл на чистому JavaScript

Створимо найпростіший лічильник, підключивши Redux із CDN у звичайний HTML-файл. Жодного React, жодного Vite чи терміналу:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8" />
  <title>Redux у чистому HTML</title>
</head>
<body>
  <div>
    <h1>Лічильник: <span id="value">0</span></h1>
    <button id="increment">+1</button>
    <button id="decrement">-1</button>
    <button id="incrementIfOdd">Додати, якщо непарне</button>
  </div>

  <!-- Підключаємо Redux напряму з CDN -->
  <script src="https://unpkg.com/redux@4.2.1/dist/redux.min.js"></script>

  <script>
    // 1. РЕДЮСЕР: чиста функція, що описує зміну стану
    function counterReducer(state = 0, action) {
      switch (action.type) {
        case "INCREMENT":
          return state + 1;
        case "DECREMENT":
          return state - 1;
        default:
          return state;
      }
    }

    // 2. СХОВИЩЕ (STORE): створення єдиного контейнера стану
    const store = Redux.createStore(counterReducer);

    const valueEl = document.getElementById("value");

    // 3. ПІДПИСКА (SUBSCRIBE): оновлення DOM щоразу, коли стан змінюється
    function render() {
      valueEl.innerText = store.getState().toString();
    }

    render(); // Початкове відображення
    store.subscribe(render); // Реєструємо слухача змін

    // 4. ДІСПАТЧ (DISPATCH): відправка екшенів у відповідь на дії користувача
    document.getElementById("increment").addEventListener("click", () => {
      store.dispatch({ type: "INCREMENT" });
    });

    document.getElementById("decrement").addEventListener("click", () => {
      store.dispatch({ type: "DECREMENT" });
    });

    document.getElementById("incrementIfOdd").addEventListener("click", () => {
      if (store.getState() % 2 !== 0) {
        store.dispatch({ type: "INCREMENT" });
      }
    });
  </script>
</body>
</html>
```

Зверніть увагу: інтерфейс оновлюється автоматично завдяки `store.subscribe(render)`. Увесь потік даних суворо односпрямований:

::math-formula
\text{Подія DOM (Event)} \longrightarrow \text{dispatch(Action)} \longrightarrow \text{Reducer(state, action)} \longrightarrow \text{Новий State} \longrightarrow \text{subscribe(render)}
::

### Етап 2: Анатомія концепцій Redux у природному порядку

Архітектура Redux спирається на **три непорушні принципи**:
1. **Єдине джерело правди (*Single source of truth*):** увесь стан застосунку зберігається в єдиному дереві об'єктів всередині одного сховища (*Store*).
2. **Стан доступний лише для читання (*State is read-only*):** єдиний спосіб змінити стан — відправити дію (*Action*), що описує подію.
3. **Зміни здійснюються чистими функціями (*Changes are made with pure functions*):** для визначення того, як дія перетворює дерево стану, пишуться чисті функції — редюсери (*Reducers*).

#### 1. Дія (Action)
**Дія** — це звичайний JavaScript-об'єкт, що описує факт події. Єдина обов'язкова вимога до дії — наявність рядкового поля `type`. Додаткові дані традиційно передаються у полі `payload`:
```ts
const addMessageAction = {
  type: "messages/add",
  payload: { id: "m1", text: "Привіт, Redux!" },
};
```

#### 2. Створювачі дій (Action Creators)
Писати об'єкти дій вручну у кожному місці програми незручно і небезпечно (можна помилитися у назві типу). **Створювач дії** — це функція, яка повертає об'єкт дії:
```ts
function addMessage(text: string) {
  return {
    type: "messages/add" as const,
    payload: { id: crypto.randomUUID(), text },
  };
}
```

#### 3. Редюсер (Reducer)
**Редюсер** — це чиста функція, яка приймає поточний стан і дію, та повертає новий стан: `(prevState, action) => newState`.
- Редюсер **ніколи не мутує** попередній стан (`state.value++` — суворе табу!).
- Редюсер не виконує асинхронних операцій, випадкових чисел (`Math.random()`) або запитів до мережі.
- Якщо передано невідому дію, редюсер зобов'язаний повернути поточний `state` без змін.

#### 4. Сховище (Store) та його API
Сховище створюється функцією `createStore(reducer)` і має лише 4 методи:
- `store.getState()`: повертає актуальне дерево стану.
- `store.dispatch(action)`: відправляє дію в редюсер, викликаючи перерахунок стану.
- `store.subscribe(listener)`: підписує функцію на кожну зміну стану (повертає функцію `unsubscribe`).
- `store.replaceReducer(nextReducer)`: використовується для динамічного завантаження коду (Code Splitting).

#### 5. Комбінування редюсерів (`combineReducers`)
У реальних системах стан розбивають на незалежні домени (наприклад, `auth`, `cart`, `products`). Функція `combineReducers` об'єднує незалежні редюсери в один кореневий:
```ts
const rootReducer = Redux.combineReducers({
  auth: authReducer,
  cart: cartReducer,
});
```

#### 6. Проміжне програмне забезпечення (Middleware) та Thunk
Звичайний `store.dispatch` синхронний. Щоб виконати мережевий запит перед оновленням стану, використовується **Middleware** — ланцюжок функцій-перехоплювачів між `dispatch` та `reducer`:
- **`redux-thunk`**: дозволяє передавати в `dispatch` не об'єкт, а функцію `(dispatch, getState) => { ... }`, усередині якої можна виконати `await fetch()` і після завершення відправити фінальний синхронний екшен.

### Етап 3: Перехід до React — чому виникла бібліотека `react-redux`

Якби ми підключали чистий Redux до React вручну, довелося б писати такий код у кожному компоненті:
```tsx
// ❌ Наївне ручне підключення: неефективне та схильне до витоків пам'яті
function BadCounter() {
  const [, forceUpdate] = useState(0);

  useEffect(() => {
    // Підписуємося на весь стор: компонент ререндериться на БУДЬ-ЯКУ зміну у сторі!
    const unsubscribe = store.subscribe(() => forceUpdate((c) => c + 1));
    return unsubscribe;
  }, []);

  return <div>{store.getState().counter}</div>;
}
```

Цей підхід має критичні недоліки:
1. Компонент ререндериться навіть тоді, коли змінилася абсолютно чужа частина глобального стану.
2. Немає селекторів та мемоїзації.
3. Потрібно імпортувати глобальний `store` у кожен файл, руйнуючи модульність і ускладнюючи тестування.

Саме для вирішення цих проблем існує офіційна бібліотека зв'язки **`react-redux`**:

::tabs
::tabs-item{label="npm"}
```bash
npm install redux react-redux
npm install -D @types/react-redux
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add redux react-redux
pnpm add -D @types/react-redux
```
::
::

### Етап 4: Повна типізація класичного Redux + React у TypeScript

Поєднаємо всі концепції у повноцінному типізованому React-застосунку:

```tsx
import React from "react";
import { createStore, combineReducers } from "redux";
import { Provider, useSelector, useDispatch, TypedUseSelectorHook } from "react-redux";

// --- 1. Модель стану ---
interface CartItem {
  id: string;
  name: string;
  price: number;
}

interface CartState {
  items: CartItem[];
  total: number;
}

// --- 2. Дії та Створювачі дій (Action Creators) ---
type CartAction =
  | { type: "cart/addItem"; payload: CartItem }
  | { type: "cart/removeItem"; payload: string }
  | { type: "cart/clear" };

export const addItem = (item: CartItem): CartAction => ({
  type: "cart/addItem",
  payload: item,
});

export const removeItem = (id: string): CartAction => ({
  type: "cart/removeItem",
  payload: id,
});

export const clearCart = (): CartAction => ({
  type: "cart/clear",
});

// --- 3. Чистий редюсер ---
const initialCartState: CartState = {
  items: [],
  total: 0,
};

function cartReducer(
  state: CartState = initialCartState,
  action: CartAction
): CartState {
  switch (action.type) {
    case "cart/addItem":
      return {
        ...state,
        items: [...state.items, action.payload],
        total: state.total + action.payload.price,
      };
    case "cart/removeItem": {
      const filtered = state.items.filter((item) => item.id !== action.payload);
      return {
        ...state,
        items: filtered,
        total: filtered.reduce((acc, item) => acc + item.price, 0),
      };
    }
    case "cart/clear":
      return initialCartState;
    default:
      return state;
  }
}

// --- 4. Сховище та виведення глобальних типів ---
const rootReducer = combineReducers({
  cart: cartReducer,
});

export const store = createStore(rootReducer);

// Виведення типів кореневого стану та відправника
export type RootState = ReturnType<typeof rootReducer>;
export type AppDispatch = typeof store.dispatch;

// Типізовані хуки для використання у компонентах
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
export const useAppDispatch = () => useDispatch<AppDispatch>();

// --- 5. Компонент кошика ---
function ShoppingCart() {
  // Селектор підписується лише на зміну гілки cart
  const { items, total } = useAppSelector((state) => state.cart);
  const dispatch = useAppDispatch();

  const handleAddSample = () => {
    dispatch(
      addItem({
        id: crypto.randomUUID(),
        name: "React + TypeScript Книга",
        price: 450,
      })
    );
  };

  return (
    <div className="cart-container">
      <h2>Кошик покупок (Сума: {total} грн)</h2>
      <button onClick={handleAddSample}>Додати товар</button>
      <button onClick={() => dispatch(clearCart())} disabled={items.length === 0}>
        Очистити
      </button>

      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.name} — {item.price} грн
            <button onClick={() => dispatch(removeItem(item.id))}>✕</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

// --- 6. Провайдер у корені застосунку ---
export function App() {
  return (
    <Provider store={store}>
      <ShoppingCart />
    </Provider>
  );
}
```

::warning
**Ціна класичного бойлерплейту Redux:**
Проаналізуйте обсяг коду вище: для простого кошика нам довелося створити константи/літерали типів, дискримінований союз дій, окремі функції-криейтори, ручні `switch/case` з постійним спредингом об'єктів для імутабельності, ручний виклик `combineReducers` та конфігурацію типізованих хуків.

Коли проєкт налічує десятки сутностей, такий підхід призводить до сотень рядків шаблонного коду (*boilerplate*) та частих випадкових помилок мутації стану. Саме щоб усунути весь цей бойлерплейт, команда Redux створила офіційний стандарт — **Redux Toolkit (RTK)**, до якого ми переходимо в наступній статті.
::

## 36. Redux Toolkit: сучасний стандарт Redux

> 🔗 **Офіційний референс:** [Офіційна документація Redux Toolkit (RTK Docs)](https://redux-toolkit.js.org/introduction/getting-started)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-приклади слайсів через createSlice, асинхронних операцій createAsyncThunk, типізованих хуків useAppDispatch/useAppSelector та челенджі.
> 📁 **Практичні навчальні проєкти модуля (Redux Toolkit):**
> - [06-rtk-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/06-rtk-counter) — базовий перехід на RTK: створення зрізу стану за допомогою `createSlice`, усунення шаблонного коду (boilerplate), безпечна мутація стану завдяки Immer, підключення через `configureStore`.
> - [07-rtk-bookstore-async](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/12-redux/07-rtk-bookstore-async) — повноцінний продакшн-орієнтований проєкт книгарні на RTK: асинхронні операції `createAsyncThunk` для взаємодії з REST API (Axios + JSON-Server), обробка станів `pending`/`fulfilled`/`rejected` в `extraReducers`, фільтрація та агрегована статистика.

**Redux Toolkit** (RTK) — це офіційний, рекомендований спосіб написання логіки Redux. Він усуває бойлерплейт класичного Redux, інтегрує Immer для «мутабельного» синтаксису оновлень та надає утиліти для асинхронних операцій.

::tabs
::tabs-item{label="npm"}
```bash
npm install @reduxjs/toolkit react-redux
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add @reduxjs/toolkit react-redux
```
::
::

### `createSlice`: слайси замість ручних редюсерів

```tsx
import { createSlice, configureStore, PayloadAction } from "@reduxjs/toolkit";
import { TypedUseSelectorHook, useDispatch, useSelector, Provider } from "react-redux";

// --- Слайс ---
interface CounterState {
  value: number;
}

const counterSlice = createSlice({
  name: "counter",
  initialState: { value: 0 } as CounterState,
  reducers: {
    increment(state) {
      state.value += 1; // Immer дозволяє «мутабельний» синтаксис!
    },
    decrement(state) {
      state.value -= 1;
    },
    incrementByAmount(state, action: PayloadAction<number>) {
      state.value += action.payload;
    },
    reset(state) {
      state.value = 0;
    },
  },
});

// Екшен-криейтори генеруються автоматично
export const { increment, decrement, incrementByAmount, reset } = counterSlice.actions;

// --- Стор ---
const store = configureStore({
  reducer: {
    counter: counterSlice.reducer,
  },
});

// Типізовані хуки — створюються один раз для всього додатку
type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;

const useAppDispatch: () => AppDispatch = useDispatch;
const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// --- Компонент ---
function RTKCounter() {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();

  return (
    <div>
      <p>Лічильник: {count}</p>
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(decrement())}>-1</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
      <button onClick={() => dispatch(reset())}>Скинути</button>
    </div>
  );
}
```

Порівняйте із класичним Redux: `createSlice` автоматично генерує екшен-криейтори та типи екшенів із назв редюсерів. Завдяки бібліотеці Immer, вбудованій у RTK, ви можете писати `state.value += 1` замість `return { ...state, value: state.value + 1 }` — Immer перехоплює мутації та створює незмінну копію під капотом.

### Асинхронні операції: `createAsyncThunk`

Для мережевих запитів та інших асинхронних операцій RTK надає `createAsyncThunk` — утиліту, що автоматично генерує три екшени: `pending`, `fulfilled` та `rejected`:

```tsx
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import axios from "axios";

interface User {
  id: number;
  name: string;
  email: string;
}

interface UsersState {
  items: User[];
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
}

// Асинхронний thunk
export const fetchUsers = createAsyncThunk<User[], void, { rejectValue: string }>(
  "users/fetchAll",
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get<User[]>(
        "https://jsonplaceholder.typicode.com/users"
      );
      return response.data;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return rejectWithValue(err.message);
      }
      return rejectWithValue("Невідома помилка");
    }
  }
);

const usersSlice = createSlice({
  name: "users",
  initialState: {
    items: [],
    status: "idle",
    error: null,
  } as UsersState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action: PayloadAction<User[]>) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload ?? "Помилка завантаження";
      });
  },
});

// Компонент
function UserListRTK() {
  const dispatch = useAppDispatch();
  const { items: users, status, error } = useAppSelector((state) => state.users);

  useEffect(() => {
    if (status === "idle") {
      dispatch(fetchUsers());
    }
  }, [dispatch, status]);

  if (status === "loading") return <p>Завантаження...</p>;
  if (status === "failed") return <p>Помилка: {error}</p>;

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```



---

## 37. Zustand: сучасний легковажний підхід до глобального стану

> 🔗 **Офіційний референс:** [Документація Zustand (Zustand GitHub Docs)](https://github.com/pmndrs/zustand)
> 📥 **Вимога до наповнення статті:** Витягнути приклади створення атомарних сторів без провайдерів, асинхронних дій та оптимізації ререндерів через селектори.

**Zustand** — це одна з найпопулярніших сучасних бібліотек керування глобальним клієнтським станом у React. На відміну від Redux або Context API, Zustand **не потребує огортання застосунку в Provider**, практично не містить бойлерплейту, підтримує асинхронні дії прямо у тілі стору та оптимізує ререндери компонентів завдяки суворим селекторам.

> 📁 **Практичні навчальні проєкти модуля (Zustand):**
> - [01-zustand-todo-counter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/13-zustand/01-zustand-todo-counter) — базовий практикум на Zustand: створення сторів `useCounterStore` та `useTodoStore` за допомогою `create()`, мутація стану через `set()`, точкові селектори стану для запобігання зайвим ререндерам та фільтрація списку задач.
> - [02-zustand-bookstore](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/13-zustand/02-zustand-bookstore) — комплексний проєкт книгарні на Zustand: асинхронні дії прямо всередині стору (fetch/post/delete без складних thunk/saga), комбінована фільтрація книг, обчислювана статистика (derived state) та взаємодія з mock REST API.

```tsx
import { create } from "zustand";

interface CounterState {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

## 38. Серверний стан: RTK Query та TanStack Query (React Query)

> 🔗 **Офіційний референс:** [Документація TanStack Query v5](https://tanstack.com/query/latest) та [RTK Query Overview](https://redux-toolkit.js.org/rtk-query/overview)
> 📥 **Вимога до наповнення статті:** Витягнути інтерактивні sandbox-приклади кешування, фонової інвалідації, пагінації та оптимістичних оновлень.
> 📁 **Практичні навчальні проєкти модуля (TanStack Query):**
> - [01-tanstack-query-starter](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/14-tanstack-query/01-tanstack-query-starter) — базовий тренувальний шаблон Vite + React для покрокового встановлення та підключення `QueryClient` і `QueryClientProvider` з нуля.
> - [02-tanstack-query-demo](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/14-tanstack-query/02-tanstack-query-demo) — професійний повнофункціональний застосунок на Next.js та TanStack Query v5 з UI-компонентами shadcn/ui: налаштування `QueryClient`, кастомні хуки `useBooks`, автоматична фонова інвалідація запитів (`queryClient.invalidateQueries`), пагінація таблиць, нескінченний скрол (`useInfiniteQuery`) та оптимістичні оновлення (optimistic updates).

> 🔗 **Офіційний референс:** [Документація RTK Query (RTK Query Overview)](https://redux-toolkit.js.org/rtk-query/overview)
> 📥 **Вимога до наповнення статті:** Витягнути повноцінний sandbox-приклад CRUD API (createApi, endpoints, auto-generated hooks, інвалідація тегів tagTypes) та практичне завдання на кешування.

**RTK Query** — це потужний інструмент для отримання та кешування даних, вбудований у Redux Toolkit. Він повністю усуває потребу в ручному написанні `useEffect` + `useState` для мережевих запитів, автоматично обробляє стани завантаження, помилки, кешування, інвалідацію кешу та перегони запитів.

### Визначення API

```tsx
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

interface User {
  id: number;
  name: string;
  email: string;
  phone: string;
}

interface CreateUserDTO {
  name: string;
  email: string;
  phone: string;
}

export const usersApi = createApi({
  reducerPath: "usersApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "https://jsonplaceholder.typicode.com",
    prepareHeaders: (headers) => {
      const token = localStorage.getItem("authToken");
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ["User"],
  endpoints: (builder) => ({
    // GET /users
    getUsers: builder.query<User[], void>({
      query: () => "/users",
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "User" as const, id })),
              { type: "User", id: "LIST" },
            ]
          : [{ type: "User", id: "LIST" }],
    }),

    // GET /users/:id
    getUserById: builder.query<User, number>({
      query: (id) => `/users/${id}`,
      providesTags: (result, error, id) => [{ type: "User", id }],
    }),

    // POST /users
    createUser: builder.mutation<User, CreateUserDTO>({
      query: (body) => ({
        url: "/users",
        method: "POST",
        body,
      }),
      invalidatesTags: [{ type: "User", id: "LIST" }],
    }),

    // PATCH /users/:id
    updateUser: builder.mutation<User, { id: number; data: Partial<CreateUserDTO> }>({
      query: ({ id, data }) => ({
        url: `/users/${id}`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "User", id }],
    }),

    // DELETE /users/:id
    deleteUser: builder.mutation<void, number>({
      query: (id) => ({
        url: `/users/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: (result, error, id) => [
        { type: "User", id },
        { type: "User", id: "LIST" },
      ],
    }),
  }),
});

// Автоматично згенеровані хуки
export const {
  useGetUsersQuery,
  useGetUserByIdQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = usersApi;
```

### Підключення до стору

```tsx
import { configureStore } from "@reduxjs/toolkit";
import { usersApi } from "./services/usersApi";

const store = configureStore({
  reducer: {
    [usersApi.reducerPath]: usersApi.reducer,
    // ...інші слайси
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(usersApi.middleware),
});
```

### Використання у компонентах

```tsx
function UserListRTKQuery() {
  const { data: users, isLoading, isError, error, refetch } = useGetUsersQuery();
  const [deleteUser] = useDeleteUserMutation();

  if (isLoading) return <p>Завантаження...</p>;
  if (isError) return <p>Помилка: {JSON.stringify(error)}</p>;

  return (
    <div>
      <button onClick={refetch}>Оновити</button>
      <ul>
        {users?.map((user) => (
          <li key={user.id}>
            {user.name} — {user.email}
            <button onClick={() => deleteUser(user.id)}>Видалити</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function UserDetail({ userId }: { userId: number }) {
  const { data: user, isLoading } = useGetUserByIdQuery(userId);
  const [updateUser, { isLoading: isUpdating }] = useUpdateUserMutation();

  if (isLoading) return <p>Завантаження...</p>;
  if (!user) return <p>Не знайдено</p>;

  const handleRename = async (): Promise<void> => {
    await updateUser({ id: userId, data: { name: "Нове ім'я" } });
    // Кеш автоматично інвалідується завдяки тегам!
  };

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={handleRename} disabled={isUpdating}>
        {isUpdating ? "Оновлення..." : "Перейменувати"}
      </button>
    </div>
  );
}
```

::note
RTK Query автоматично кешує результати, дедуплікує однакові запити та оновлює кеш при мутаціях завдяки системі тегів (`providesTags` / `invalidatesTags`). Коли мутація `deleteUser` інвалідує тег `{ type: "User", id: "LIST" }`, RTK Query автоматично перезавантажить список користувачів у всіх компонентах, що використовують `useGetUsersQuery`.
::

## 39. React Hook Form + Zod: типобезпечна валідація форм

> 🔗 **Офіційний референс:** [Документація React Hook Form (RHF Docs)](https://react-hook-form.com/get-started) та [Zod Documentation](https://zod.dev/)
> 📥 **Вимога до наповнення статті:** Витягнути sandbox-проєкт складної форми з динамічними полями (useFieldArray), валідацією схем через zodResolver та завдання на обробку помилок валідації.
> 📁 **Практичний навчальний проєкт модуля:**
> - [01-react-form-validation](file:///Users/arakviel/Work/IT%20Academy/12_React_Angular/react/_new/09-forms-and-validation/01-react-form-validation) — форма реєстрації з декларативною валідацією на `react-hook-form` та схемі Yup (`@hookform/resolvers/yup`): валідація складності пароля, підтвердження пароля, обов'язкових полів, виведення помилок у реальному часі та модальне вікно успішного сабміту.

Обробка форм — одна з найчастіших задач у фронтенд-розробці, і водночас одна з найскладніших: валідація полів, відображення помилок, керування фокусом, повторне надсилання та інтеграція з бекенд-валідацією. **React Hook Form** — це бібліотека, що мінімізує ререндери та надає зручний API для роботи з формами, а **Zod** — бібліотека для оголошення та валідації схем даних, яка ідеально інтегрується з TypeScript.

::tabs
::tabs-item{label="npm"}
```bash
npm install react-hook-form zod @hookform/resolvers
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add react-hook-form zod @hookform/resolvers
```
::
::

### Визначення схеми валідації

```tsx
import { z } from "zod";

// Zod-схема — єдине джерело правди для валідації та типів
const registrationSchema = z
  .object({
    name: z
      .string()
      .min(2, "Ім'я має містити щонайменше 2 символи")
      .max(50, "Ім'я не може перевищувати 50 символів"),
    email: z
      .string()
      .email("Введіть коректну електронну адресу"),
    age: z
      .number({ invalid_type_error: "Вік має бути числом" })
      .min(16, "Мінімальний вік — 16 років")
      .max(120, "Введіть коректний вік"),
    password: z
      .string()
      .min(8, "Пароль має містити щонайменше 8 символів")
      .regex(/[A-Z]/, "Пароль має містити хоча б одну велику літеру")
      .regex(/[0-9]/, "Пароль має містити хоча б одну цифру"),
    confirmPassword: z.string(),
    acceptTerms: z.literal(true, {
      errorMap: () => ({ message: "Необхідно прийняти умови використання" }),
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Паролі не збігаються",
    path: ["confirmPassword"],
  });

// TypeScript-тип автоматично виводиться зі схеми
type RegistrationFormData = z.infer<typeof registrationSchema>;
```

### Інтеграція з React Hook Form

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

function RegistrationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
    defaultValues: {
      name: "",
      email: "",
      age: undefined,
      password: "",
      confirmPassword: "",
      acceptTerms: false as unknown as true,
    },
  });

  const onSubmit = async (data: RegistrationFormData): Promise<void> => {
    // Дані вже валідовані та типізовані!
    console.log("Валідні дані:", data);
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Імітація API
    reset();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div>
        <label htmlFor="name">Ім'я</label>
        <input id="name" {...register("name")} />
        {errors.name && <span className="error">{errors.name.message}</span>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register("email")} />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="age">Вік</label>
        <input
          id="age"
          type="number"
          {...register("age", { valueAsNumber: true })}
        />
        {errors.age && <span className="error">{errors.age.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Пароль</label>
        <input id="password" type="password" {...register("password")} />
        {errors.password && (
          <span className="error">{errors.password.message}</span>
        )}
      </div>

      <div>
        <label htmlFor="confirmPassword">Підтвердження паролю</label>
        <input
          id="confirmPassword"
          type="password"
          {...register("confirmPassword")}
        />
        {errors.confirmPassword && (
          <span className="error">{errors.confirmPassword.message}</span>
        )}
      </div>

      <div>
        <label>
          <input type="checkbox" {...register("acceptTerms")} />
          Я приймаю умови використання
        </label>
        {errors.acceptTerms && (
          <span className="error">{errors.acceptTerms.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Надсилання..." : "Зареєструватися"}
      </button>
    </form>
  );
}
```

::tip
Конструкція `z.infer<typeof registrationSchema>` автоматично створює TypeScript-тип із Zod-схеми. Це усуває дублювання — ви описуєте структуру даних **один раз** у Zod-схемі, а TypeScript-тип та валідація генеруються автоматично. Зміна схеми одразу відобразиться і в типах, і в валідації.
::

### Кастомні компоненти поля з `Controller`

Для кастомних UI-компонентів, які не підтримують стандартний API `ref`, використовуйте `Controller`:

```tsx
import { Controller, useForm } from "react-hook-form";

interface SelectOption {
  value: string;
  label: string;
}

interface CustomSelectProps {
  options: SelectOption[];
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

function CustomSelect({ options, value, onChange, error }: CustomSelectProps) {
  return (
    <div>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">Оберіть...</option>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <span className="error">{error}</span>}
    </div>
  );
}

const formSchema = z.object({
  country: z.string().min(1, "Оберіть країну"),
});

type FormData = z.infer<typeof formSchema>;

function FormWithController() {
  const { control, handleSubmit } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <Controller
        name="country"
        control={control}
        render={({ field, fieldState }) => (
          <CustomSelect
            options={[
              { value: "ua", label: "Україна" },
              { value: "pl", label: "Польща" },
              { value: "de", label: "Німеччина" },
            ]}
            value={field.value}
            onChange={field.onChange}
            error={fieldState.error?.message}
          />
        )}
      />
      <button type="submit">Надіслати</button>
    </form>
  );
}
```

## 40. Framer Motion: декларативні анімації

> 🔗 **Офіційний референс:** [Документація Framer Motion (Motion for React Docs)](https://motion.dev/docs/react-quick-start)
> 📥 **Вимога до наповнення статті:** Витягнути живі інтерактивні sandbox-приклади анімацій (motion.div, AnimatePresence, переходи сторінок, анімації списків) та творчі челенджі.

**Framer Motion** — провідна бібліотека анімацій для React, що дозволяє створювати плавні, фізично реалістичні анімації декларативним способом. Замість ручного маніпулювання CSS-анімаціями чи `requestAnimationFrame`, ви описуєте початковий та кінцевий стан, а Motion обчислює всі проміжні кадри.

::tabs
::tabs-item{label="npm"}
```bash
npm install framer-motion
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add framer-motion
```
::
::

### Базові анімації

```tsx
import { motion } from "framer-motion";

function AnimatedCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      whileHover={{ scale: 1.05, boxShadow: "0 10px 30px rgba(0,0,0,0.15)" }}
      whileTap={{ scale: 0.95 }}
      style={{
        padding: "1.5rem",
        borderRadius: "0.75rem",
        backgroundColor: "#f8fafc",
        cursor: "pointer",
      }}
    >
      <h3>Анімована картка</h3>
      <p>Наведіть курсор або натисніть</p>
    </motion.div>
  );
}
```

### Анімація списків з `AnimatePresence`

`AnimatePresence` дозволяє анімувати компоненти, які входять та виходять з DOM — функціональність, яку неможливо реалізувати стандартними CSS-переходами:

```tsx
import { motion, AnimatePresence } from "framer-motion";

interface Notification {
  id: number;
  message: string;
  type: "success" | "error" | "info";
}

function NotificationList({
  notifications,
  onDismiss,
}: {
  notifications: Notification[];
  onDismiss: (id: number) => void;
}) {
  return (
    <div style={{ position: "fixed", top: "1rem", right: "1rem" }}>
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 100 }}
            transition={{ type: "spring", damping: 20, stiffness: 300 }}
            style={{
              padding: "1rem",
              marginBottom: "0.5rem",
              borderRadius: "0.5rem",
              backgroundColor:
                notification.type === "success"
                  ? "#dcfce7"
                  : notification.type === "error"
                    ? "#fee2e2"
                    : "#dbeafe",
              cursor: "pointer",
            }}
            onClick={() => onDismiss(notification.id)}
          >
            {notification.message}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
```

### Анімація переходів між сторінками

```tsx
import { motion } from "framer-motion";

const pageVariants = {
  initial: { opacity: 0, x: -20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 },
};

function PageWrapper({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

::note
Проп `transition={{ type: "spring", damping: 20, stiffness: 300 }}` задає фізичну пружинну модель замість лінійної інтерполяції. Пружинні анімації виглядають більш природно, бо імітують реальну фізику — елемент може трохи «проскочити» цільову позицію та повернутися, як справжня пружина.
::

## 41. React Testing Library + Vitest: тестування компонентів

> 🔗 **Офіційний референс:** [React Testing Library Docs](https://testing-library.com/docs/react-testing-library/intro) та [Vitest Guide](https://vitest.dev/)
> 📥 **Вимога до наповнення статті:** Витягнути повні лістинги тестів поведінки компонентів (render, screen, userEvent, тестування асинхронних форм та моків) та практичні завдання на покриття тестами.

Тестування — невід'ємна частина професійної розробки. **Vitest** — це блискавичний тестовий фреймворк, сумісний з Vite, а **React Testing Library** — бібліотека для тестування React-компонентів, що фокусується на поведінці з точки зору користувача, а не на внутрішній реалізації.

::tabs
::tabs-item{label="npm"}
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```
::
::

### Конфігурація Vitest

```tsx
// vite.config.ts
/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
    css: true,
  },
});
```

```tsx
// src/test/setup.ts
import "@testing-library/jest-dom";
```

### Написання тестів

```tsx
// Counter.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import Counter from "./Counter";

describe("Counter", () => {
  it("відображає початкове значення 0", () => {
    render(<Counter />);
    expect(screen.getByText("Лічильник: 0")).toBeInTheDocument();
  });

  it("збільшує лічильник при натисканні +1", async () => {
    const user = userEvent.setup();
    render(<Counter />);

    await user.click(screen.getByRole("button", { name: "+1" }));
    expect(screen.getByText("Лічильник: 1")).toBeInTheDocument();
  });

  it("зменшує лічильник при натисканні -1", async () => {
    const user = userEvent.setup();
    render(<Counter />);

    await user.click(screen.getByRole("button", { name: "-1" }));
    expect(screen.getByText("Лічильник: -1")).toBeInTheDocument();
  });

  it("скидає лічильник до 0", async () => {
    const user = userEvent.setup();
    render(<Counter />);

    await user.click(screen.getByRole("button", { name: "+1" }));
    await user.click(screen.getByRole("button", { name: "+1" }));
    await user.click(screen.getByRole("button", { name: "Скинути" }));

    expect(screen.getByText("Лічильник: 0")).toBeInTheDocument();
  });
});
```

### Тестування форм

```tsx
// RegistrationForm.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import RegistrationForm from "./RegistrationForm";

describe("RegistrationForm", () => {
  it("показує помилки валідації для порожніх полів", async () => {
    const user = userEvent.setup();
    render(<RegistrationForm />);

    await user.click(screen.getByRole("button", { name: "Зареєструватися" }));

    await waitFor(() => {
      expect(
        screen.getByText("Ім'я має містити щонайменше 2 символи")
      ).toBeInTheDocument();
      expect(
        screen.getByText("Введіть коректну електронну адресу")
      ).toBeInTheDocument();
    });
  });

  it("надсилає форму з валідними даними", async () => {
    const user = userEvent.setup();
    const consoleSpy = vi.spyOn(console, "log");
    render(<RegistrationForm />);

    await user.type(screen.getByLabelText("Ім'я"), "Олена");
    await user.type(screen.getByLabelText("Email"), "olena@test.com");
    await user.type(screen.getByLabelText("Вік"), "25");
    await user.type(screen.getByLabelText("Пароль"), "SecurePass1");
    await user.type(screen.getByLabelText("Підтвердження паролю"), "SecurePass1");
    await user.click(screen.getByLabelText(/умови використання/));
    await user.click(screen.getByRole("button", { name: "Зареєструватися" }));

    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith("Валідні дані:", expect.any(Object));
    });
  });
});
```

::warning
React Testing Library навмисно **не надає** методів для прямого доступу до стану компонента чи його пропсів. Тести повинні взаємодіяти з компонентом так, як це робить реальний користувач — через видимий текст, ролі елементів, мітки полів. Це гарантує, що тести залишаються стабільними при рефакторингу внутрішньої реалізації.
::

## 42. i18next: інтернаціоналізація React-застосунків

> 🔗 **Офіційний референс:** [Документація react-i18next](https://react.i18next.com/)
> 📥 **Вимога до наповнення статті:** Витягнути sandbox-приклад мультимовного інтерфейсу (конфігурація i18n, JSON-переклади, хук useTranslation, інтерполяція) та практичне завдання на локалізацію.

**i18next** — найпопулярніша бібліотека для інтернаціоналізації (*internationalization*, скорочено i18n), що дозволяє перекладати інтерфейс на кілька мов, форматувати дати, числа та валюту відповідно до локалі, та обробляти плюралізацію (*pluralization*).

::tabs
::tabs-item{label="npm"}
```bash
npm install i18next react-i18next i18next-browser-languagedetector
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add i18next react-i18next i18next-browser-languagedetector
```
::
::

### Налаштування

```tsx
// src/i18n/index.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

const resources = {
  uk: {
    translation: {
      nav: {
        home: "Головна",
        about: "Про нас",
        users: "Користувачі",
      },
      greeting: "Привіт, {{name}}!",
      itemCount_one: "{{count}} елемент",
      itemCount_few: "{{count}} елементи",
      itemCount_many: "{{count}} елементів",
      buttons: {
        save: "Зберегти",
        cancel: "Скасувати",
        delete: "Видалити",
      },
    },
  },
  en: {
    translation: {
      nav: {
        home: "Home",
        about: "About",
        users: "Users",
      },
      greeting: "Hello, {{name}}!",
      itemCount_one: "{{count}} item",
      itemCount_other: "{{count}} items",
      buttons: {
        save: "Save",
        cancel: "Cancel",
        delete: "Delete",
      },
    },
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: "uk",
    interpolation: {
      escapeValue: false, // React вже екранує значення
    },
  });

export default i18n;
```

### Використання у компонентах

```tsx
import { useTranslation } from "react-i18next";

function Navigation() {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng: string): void => {
    i18n.changeLanguage(lng);
  };

  return (
    <nav>
      <a href="/">{t("nav.home")}</a>
      <a href="/about">{t("nav.about")}</a>
      <a href="/users">{t("nav.users")}</a>

      <div>
        <button onClick={() => changeLanguage("uk")}>🇺🇦 UA</button>
        <button onClick={() => changeLanguage("en")}>🇬🇧 EN</button>
      </div>
    </nav>
  );
}

function WelcomePage({ userName }: { userName: string }) {
  const { t } = useTranslation();
  const itemCount = 5;

  return (
    <div>
      {/* Інтерполяція змінних */}
      <h1>{t("greeting", { name: userName })}</h1>

      {/* Плюралізація */}
      <p>{t("itemCount", { count: itemCount })}</p>

      {/* Вкладені ключі */}
      <button>{t("buttons.save")}</button>
      <button>{t("buttons.cancel")}</button>
    </div>
  );
}
```

::note
Плюралізація в i18next автоматично обирає правильну форму залежно від числа та мови. Для української мови потрібні три форми: `_one` (1 елемент), `_few` (2–4 елементи), `_many` (5+ елементів). Для англійської достатньо двох: `_one` та `_other`.
::

---

# Частина VI. Оптимізація продуктивності

## 43. `useMemo`: мемоїзація обчислень

> 🔗 **Офіційний референс:** [Довідник React: useMemo (React Reference: useMemo)](https://uk.react.dev/reference/react/useMemo)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ пісочниці замірів продуктивності (важка фільтрація списків, порівняння з консольним таймером) та ВСІ практичні завдання (Challenges) щодо useMemo.

Хук `useMemo` кешує результат обчислення та повторно обчислює його лише коли змінюються залежності. Використовуйте його для ресурсоємних операцій (фільтрація/сортування великих масивів, складні розрахунки), а не для тривіальних обчислень — сам `useMemo` має накладні витрати.

```tsx
import { useMemo, useState } from "react";

interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
}

function ProductList({ products }: { products: Product[] }) {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"name" | "price">("name");

  const filteredAndSorted = useMemo(() => {
    console.log("Перерахунок списку..."); // Виводиться лише при зміні залежностей
    return products
      .filter((p) =>
        p.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
      .sort((a, b) =>
        sortBy === "name"
          ? a.name.localeCompare(b.name, "uk")
          : a.price - b.price
      );
  }, [products, searchQuery, sortBy]);

  return (
    <div>
      <input
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Пошук..."
      />
      <select
        value={sortBy}
        onChange={(e) => setSortBy(e.target.value as "name" | "price")}
      >
        <option value="name">За назвою</option>
        <option value="price">За ціною</option>
      </select>
      <ul>
        {filteredAndSorted.map((product) => (
          <li key={product.id}>
            {product.name} — {product.price} грн
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## 44. `useCallback` та `React.memo`: запобігання зайвим ререндерам

> 🔗 **Офіційний референс:** [Довідник React: useCallback](https://uk.react.dev/reference/react/useCallback) та [Довідник React: memo](https://uk.react.dev/reference/react/memo)
> 📥 **Вимога до наповнення статті:** Витягнути ВСІ sandbox-ілюстрації оптимізації передачі колбеків у мемоїзовані списки, профайлер React DevTools та ВСІ практичні завдання (Challenges) з розв'язками.

`React.memo` обгортає компонент і перерендерює його лише коли пропси змінилися. `useCallback` мемоїзує функцію, щоб її посилання залишалося стабільним між рендерами — це критично при передачі колбеків у мемоїзовані дочірні компоненти.

```tsx
import { memo, useCallback, useState } from "react";

interface TodoItemProps {
  id: number;
  text: string;
  done: boolean;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
}

// memo запобігає ререндеру, якщо пропси не змінилися
const TodoItem = memo(function TodoItem({
  id,
  text,
  done,
  onToggle,
  onDelete,
}: TodoItemProps) {
  console.log(`Рендер TodoItem #${id}`);

  return (
    <li>
      <input
        type="checkbox"
        checked={done}
        onChange={() => onToggle(id)}
      />
      <span style={{ textDecoration: done ? "line-through" : "none" }}>
        {text}
      </span>
      <button onClick={() => onDelete(id)}>✕</button>
    </li>
  );
});

function TodoApp() {
  const [todos, setTodos] = useState<{ id: number; text: string; done: boolean }[]>([
    { id: 1, text: "Вивчити useMemo", done: false },
    { id: 2, text: "Вивчити useCallback", done: false },
  ]);

  // useCallback стабілізує посилання на функцію
  const handleToggle = useCallback((id: number): void => {
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t))
    );
  }, []);

  const handleDelete = useCallback((id: number): void => {
    setTodos((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          id={todo.id}
          text={todo.text}
          done={todo.done}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </ul>
  );
}
```

::caution
Не обгортайте кожен компонент у `React.memo` — це **передчасна оптимізація**, яка ускладнює код. Мемоїзація доцільна лише коли: (1) компонент рендерить складну розмітку, (2) батьківський компонент часто перерендерюється, (3) пропси дочірнього компонента рідко змінюються. Завжди вимірюйте продуктивність перед оптимізацією за допомогою React DevTools Profiler.
::

---

# Підсумок

Ця навчальна програма охопила повний шлях від базових концепцій React до професійного стеку технологій:

::card-group

::card{title="📦 Ядро React" icon="i-lucide-box"}

- Компоненти, JSX, пропси з TypeScript
- Стан (`useState`), знімки, імутабельність
- Обробка подій із типізацією
- Умовний рендеринг, списки, ключі

::

::card{title="🏗️ Архітектура стану" icon="i-lucide-layers"}

- Підйом стану (Lifting State Up)
- `useReducer` з дискримінованими union-типами
- Context API та кастомні хуки
- Еволюція: Redux → Redux Toolkit → RTK Query

::

::card{title="🔌 Побічні ефекти" icon="i-lucide-plug"}

- `useEffect` та масив залежностей
- Рефи (`useRef`) для DOM та збереження значень
- Кастомні хуки (`useFetch`, `useLocalStorage`)
- Axios з перехоплювачами та типізацією

::

::card{title="🧰 Екосистема" icon="i-lucide-wrench"}

- React Router (маршрути, параметри, навігація)
- CSS Modules (локальна інкапсуляція стилів)
- React Hook Form + Zod (форми та валідація)
- Framer Motion, Vitest, i18next

::

::card{title="⚡ Оптимізація" icon="i-lucide-zap"}

- `useMemo` для мемоїзації обчислень
- `useCallback` + `React.memo` для ререндерів
- RTK Query кешування та інвалідація
- React DevTools Profiler

::

::

