# Нотатки до презентації: State Managers в React додатках. Redux

Детальні пояснення для кожного слайду з термінологією та прикладами.

---

## Слайд 1: Титульний

**Що говорити:**
Вітаю всіх! Сьогодні ми з вами детально розглянемо одну з найпопулярніших бібліотек для управління станом у React додатках - Redux. Ця презентація буде дуже практичною, ми розглянемо не тільки теорію, але й багато прикладів коду. Наприкінці ви зможете самостійно використовувати Redux у своїх проектах.

**Ключові моменти:**

-   Redux - це не просто бібліотека, це цілий екосистема і підхід до архітектури додатків
-   Ми розглянемо як класичний Redux, так і сучасний Redux Toolkit
-   Будуть практичні приклади від простих до складних

---

## Слайд 2: План презентації

**Що говорити:**
Давайте подивимося на структуру нашої презентації. Ми почнемо з базових концепцій - що таке управління станом і навіщо воно потрібне. Потім детально розглянемо Redux, його принципи та основні поняття. Після цього перейдемо до сучасного Redux Toolkit, який значно спрощує роботу. І завершимо best practices та порадами з оптимізації.

**Термінологія:**

-   **State Management** - управління станом додатку
-   **Redux Toolkit (RTK)** - сучасна обгортка над Redux, яка спрощує розробку
-   **Async Operations** - асинхронні операції, такі як запити до API
-   **Best Practices** - найкращі практики, перевірені підходи до розробки

---

## Слайд 3: Що таке State Management?

**Що говорити:**
Почнемо з основ. State, або стан - це дані, які можуть змінюватися під час роботи додатку. Наприклад, список завдань у todo додатку, інформація про авторизованого користувача, вміст кошика в інтернет-магазині - все це стан.

State Management - це підхід до того, як ми організовуємо, зберігаємо та змінюємо ці дані. У React є кілька типів стану:

**Local State** - це стан окремого компонента. Наприклад, значення в input полі, чи відкрите меню. Для цього ми використовуємо useState або useReducer хуки.

**Global State** - це стан, який потрібен багатьом компонентам одночасно. Наприклад, інформація про користувача може знадобитися в Header, у профілі, у налаштуваннях.

**Server State** - це дані, які ми отримуємо з сервера через API. Списки продуктів, пости в соцмережі тощо.

**URL State** - параметри, які зберігаються в адресній стрічці браузера. Наприклад, фільтри, пагінація.

**Термінологія:**

-   **useState** - React хук для створення локального стану
-   **useReducer** - React хук для складнішої логіки стану
-   **API** - Application Programming Interface, інтерфейс для спілкування з сервером

---

## Слайд 4: Проблеми без State Manager

**Що говорити:**
Тепер розглянемо конкретну проблему. Уявіть, що у вас є інформація про користувача, яка потрібна десь глибоко в дереві компонентів. Без state manager доведеться передавати props через всі проміжні компоненти.

Дивіться на код: компонент App передає user і setUser в Layout, Layout передає їх далі в Header, Header - в UserMenu, і тільки там ми можемо їх використати. При цьому Layout і Header взагалі не використовують ці дані, вони просто транспортують їх далі!

Ця проблема називається **Prop Drilling** - коли props "пробуриваються" через багато рівнів компонентів. Це призводить до:

-   Багато зайвого коду
-   Складності підтримки - якщо потрібно додати ще один prop, доведеться змінювати всі проміжні компоненти
-   Важко відстежувати, звідки беруться дані

**Термінологія:**

-   **Props** - properties, властивості, які передаються від батьківського компонента до дочірнього
-   **Prop Drilling** - передача props через багато рівнів вкладеності
-   **Дерево компонентів** - ієрархічна структура React компонентів

---

## Слайд 5: Навіщо потрібен State Manager?

**Що говорити:**
State Manager вирішує проблему Prop Drilling та надає багато інших переваг.

**Централізоване сховище** - весь важливий стан зберігається в одному місці. Це називається Single Source of Truth - єдине джерело правди. Це означає, що немає суперечливих даних в різних частинах додатку.

**Уникнення Prop Drilling** - будь-який компонент може отримати доступ до потрібних даних напряму зі сховища, без передачі через проміжні компоненти.

**Передбачуваність** - є чіткі правила, як можна змінювати стан. Не можна просто взяти і змінити дані як завгодно - потрібно відправити action, він пройде через reducer, і тільки тоді стан зміниться. Це робить код більш передбачуваним і зменшує кількість помилок.

**Дебаг** - з Redux DevTools ви можете бачити всі зміни стану в реальному часі, відстежувати, яка дія призвела до якої зміни.

**Time Travel Debugging** - можна "перемотати" час назад, подивитися, як виглядав стан 5 хвилин тому, і навіть повернутися до того стану!

**Тестування** - коли логіка відокремлена від компонентів, її набагато легше тестувати.

**Термінологія:**

-   **Single Source of Truth** - принцип, коли всі дані зберігаються в одному місці
-   **Action** - дія, подія, яка описує, що сталося в додатку
-   **Reducer** - функція, яка змінює стан
-   **Redux DevTools** - інструмент для відлагодження Redux додатків

---

## Слайд 6: Що таке Redux?

**Що говорити:**
Redux - це бібліотека для управління станом JavaScript додатків. Важливо розуміти, що Redux не прив'язаний до React - його можна використовувати з Angular, Vue, або навіть з чистим JavaScript. Але найчастіше його використовують саме з React.

Основна ідея Redux дуже проста:

1. Весь стан додатку зберігається в одному великому JavaScript об'єкті, який називається Store
2. Цей стан доступний тільки для читання - ви не можете просто взяти і змінити його
3. Щоб змінити стан, потрібно відправити action
4. Action обробляється reducer'ом - чистою функцією, яка приймає старий стан і action, і повертає новий стан

Redux створили Dan Abramov та Andrew Clark у 2015 році. Dan Abramov - це той самий чувак, який працює в команді React і створив React DevTools. Redux був натхненний архітектурою Flux від Facebook і концепціями функціонального програмування, особливо з мови Elm.

**Термінологія:**

-   **Store** - сховище, об'єкт, який містить весь стан додатку
-   **Flux** - архітектурний патерн від Facebook для управління даними
-   **Чиста функція (Pure Function)** - функція, яка завжди повертає той самий результат для тих самих аргументів і не має побічних ефектів

---

## Слайд 7: Три принципи Redux

**Що говорити:**
Redux побудований на трьох фундаментальних принципах. Дотримання цих принципів робить додаток передбачуваним і легким для відлагодження.

**Перший принцип: Single Source of Truth**
Весь стан вашого додатку зберігається в одному Store. Це один великий JavaScript об'єкт. Наприклад:

```
{
  user: { name: 'Іван', email: 'ivan@example.com' },
  todos: [{ id: 1, text: 'Вивчити Redux' }],
  settings: { theme: 'dark' }
}
```

**Другий принцип: State is Read-Only**
Ви не можете просто взяти і змінити стан напряму. Єдиний спосіб змінити стан - це відправити (dispatch) action. Action - це звичайний JavaScript об'єкт, який описує, ЩО сталося. Наприклад:

```
{ type: 'TODO_ADDED', payload: { text: 'Новий todo' } }
```

**Третій принцип: Changes are Made with Pure Functions**
Щоб описати, як action змінює стан, ми пишемо чисті функції - reducer'и. Чиста функція - це функція, яка:

-   Не змінює свої аргументи (іммутабельність)
-   Не має побічних ефектів (не робить API запити, не змінює глобальні змінні)
-   Завжди повертає той самий результат для тих самих аргументів

**Термінологія:**

-   **Dispatch** - відправити, запустити дію
-   **Payload** - корисне навантаження, дані, які несе action
-   **Іммутабельність (Immutability)** - незмінність, принцип, коли замість зміни даних ми створюємо нові

---

## Слайд 8: Redux Data Flow

**Що говорити:**
Тепер розглянемо, як працює потік даних в Redux. Це однонаправлений потік, що робить додаток передбачуваним.

**Крок 1: Користувач взаємодіє з UI**
Наприклад, натискає кнопку "Додати todo". Компонент викликає dispatch і відправляє action:

```
dispatch({ type: 'ADD_TODO', payload: { text: 'Нове завдання' } })
```

**Крок 2: Action**
Action - це простий об'єкт, який описує, що сталося. У ньому обов'язково має бути поле type (тип дії), і опціонально payload (дані). Наприклад:

```
{ type: 'ADD_TODO', payload: { id: 1, text: 'Нове завдання', completed: false } }
```

**Крок 3: Reducer**
Redux передає цей action у reducer. Reducer - це функція, яка приймає поточний стан і action, і повертає новий стан. Важливо: reducer НЕ ЗМІНЮЄ старий стан, а створює новий!

**Крок 4: Store**
Новий стан зберігається в Store. Store - це об'єкт, який:

-   Зберігає стан
-   Дозволяє читати стан через getState()
-   Дозволяє відправляти actions через dispatch()
-   Дозволяє підписуватися на зміни

**Крок 5: UI Re-render**
Коли стан змінюється, всі підписані компоненти отримують оновлення і перерендеруються з новими даними.

І цикл повторюється! Це однонаправлений потік даних - дані рухаються тільки в одному напрямку, що робить додаток передбачуваним.

**Термінологія:**

-   **Однонаправлений потік даних (Unidirectional Data Flow)** - дані рухаються в одному напрямку
-   **Re-render** - повторний рендеринг, оновлення UI компонента
-   **Subscribe** - підписатися, слухати зміни

---

## Слайд 9: Core Concepts: Actions

**Що говорити:**
Розглянемо детальніше перше ключове поняття - Actions (дії).

Action - це найпростіша річ у Redux. Це звичайний JavaScript об'єкт з обов'язковим полем type. Наприклад:

```
{ type: 'ADD_TODO' }
```

Якщо action несе якісь дані, їх зазвичай поміщають у поле payload:

```
{
  type: 'ADD_TODO',
  payload: {
    id: 1,
    text: 'Вивчити Redux',
    completed: false
  }
}
```

Але постійно писати такі об'єкти незручно, тому використовують **Action Creators** - функції, які створюють actions. Подивіться на приклад:

```javascript
function addTodo(text) {
    return {
        type: 'ADD_TODO',
        payload: {
            id: Date.now(), // простий спосіб згенерувати унікальний ID
            text,
            completed: false,
        },
    }
}
```

Тепер замість того, щоб писати весь об'єкт, можна просто викликати:

```
dispatch(addTodo('Вивчити Redux'))
```

Це зручніше, менше шансів зробити помилку, і якщо потрібно змінити структуру action, змінюємо в одному місці.

**Термінологія:**

-   **Action Creator** - функція, яка створює і повертає action
-   **Date.now()** - JavaScript функція, яка повертає поточний час в мілісекундах (часто використовується для генерації простих ID)

---

## Слайд 10: Action Types: Best Practices

**Що говорити:**
Тепер поговоримо про найкращі практики роботи з типами actions.

**Погана практика:**
Використовувати рядки напряму - легко зробити друкарську помилку, IDE не підкаже, і якщо помилитеся, помилки не буде, action просто не спрацює:

```javascript
dispatch({ type: 'add_todo' }) // Хтось написав маленькими літерами
dispatch({ type: 'ADD_TODO' }) // А хтось великими - це вже інший action!
```

**Добра практика:**
Винести типи в константи:

```javascript
const ADD_TODO = 'ADD_TODO'
const TOGGLE_TODO = 'TOGGLE_TODO'

dispatch({ type: ADD_TODO }) // Якщо помилитеся в назві константи, IDE підкаже
```

**Ще краще:**
Використовувати namespace pattern - додавати префікс з назвою фічі:

```javascript
const ADD_TODO = 'todos/add'
const TOGGLE_TODO = 'todos/toggle'
const DELETE_TODO = 'todos/delete'
```

Це допомагає уникнути конфліктів - якщо у вас є todos і posts, обидва можуть мати action ADD, але 'todos/add' і 'posts/add' - різні.

**Найкраще для TypeScript:**
Використовувати enum:

```typescript
enum TodoActionTypes {
    ADD = 'todos/add',
    TOGGLE = 'todos/toggle',
    DELETE = 'todos/delete',
}
```

З TypeScript отримуєте автодоповнення, перевірку типів, і якщо помилитеся - помилку на етапі компіляції, а не в runtime.

**Термінологія:**

-   **Namespace** - простір імен, префікс для групування
-   **Enum** - enumeration, перерахування, тип даних в TypeScript
-   **IDE** - Integrated Development Environment, середовище розробки (VS Code, WebStorm)
-   **Runtime** - час виконання програми

---

## Слайд 11: Core Concepts: Reducers

**Що говорити:**
Переходимо до другого ключового поняття - Reducers.

Reducer - це чиста функція, яка описує, ЯК стан змінюється у відповідь на action. Вона приймає два аргументи:

1. Поточний стан (state)
2. Action, який відправили

І повертає новий стан.

Важливий момент: перший параметр має значення за замовчуванням - initialState. Це потрібно, тому що коли Redux тільки ініціалізується, він викликає reducer з undefined як стан, і reducer повертає початковий стан.

Подивіться на приклад. У нас є початковий стан з порожнім масивом todos і фільтром 'all'.

Коли приходить action 'ADD_TODO', ми повертаємо НОВИЙ об'єкт. Важливо: ми використовуємо spread оператор `...state` щоб скопіювати всі поля, а потім перезаписуємо тільки todos. Для todos також створюємо новий масив: `[...state.todos, action.payload]` - копіюємо старі todos і додаємо новий.

Для 'TOGGLE_TODO' використовуємо метод map. Map створює новий масив, проходить по кожному todo. Якщо id співпадає - створюємо новий об'єкт todo з перемкнутим completed, якщо ні - повертаємо старий todo без змін.

І обов'язково має бути default case, який повертає стан без змін. Це важливо, тому що через reducer проходять ВСІ actions, навіть ті, які не стосуються цього reducer'а.

**Термінологія:**

-   **Spread оператор (...)** - оператор розгортання, копіює властивості об'єкта або елементи масиву
-   **map** - метод масиву, який створює новий масив, застосовуючи функцію до кожного елемента
-   **default case** - випадок за замовчуванням у switch statement

---

## Слайд 12: Правила Reducers

**Що говорити:**
Дуже важливо розуміти правила, яких має дотримуватися reducer. Reducer ОБОВ'ЯЗКОВО має бути чистою функцією.

**Що дозволено:**

-   Робити обчислення на основі state та action
-   Створювати нові об'єкти та масиви

**Що ЗАБОРОНЕНО:**

-   Мутувати (змінювати) state. Це найчастіша помилка початківців!
-   Виконувати side effects (побічні ефекти) - API запити, setTimeout, Math.random(), Date.now()
-   Викликати недетерміновані функції - функції, які можуть повертати різні значення для тих самих аргументів

Подивіться на приклади:

**Погано - мутація:**

```javascript
function reducer(state, action) {
    state.count++ // МИ ЗМІНЮЄМО state! Це порушує іммутабельність
    return state
}
```

Проблема: Redux не зрозуміє, що стан змінився, тому що це той самий об'єкт (посилання не змінилося). Компоненти не оновляться!

**Добре - іммутабельність:**

```javascript
function reducer(state, action) {
    return { ...state, count: state.count + 1 } // Створюємо НОВИЙ об'єкт
}
```

Тут ми створюємо новий об'єкт, копіюємо всі властивості старого, і змінюємо тільки count. Redux бачить, що це новий об'єкт, і запускає оновлення компонентів.

**Термінологія:**

-   **Мутація (Mutation)** - зміна існуючого об'єкта/масиву
-   **Side effects** - побічні ефекти, дії, які впливають на щось поза функцією
-   **Детермінована функція** - функція, яка завжди повертає той самий результат для тих самих аргументів
-   **Посилання (Reference)** - адреса об'єкта в пам'яті

---

## Слайд 13: Immutability Patterns

**Що говорити:**
Оскільки іммутабельність - це основа Redux, розглянемо типові патерни роботи з іммутабельними оновленнями.

**Оновлення об'єкта:**
Використовуємо spread оператор для копіювання. Якщо потрібно оновити вкладений об'єкт, копіюємо кожен рівень:

```javascript
const newState = {
    ...state, // копіюємо всі властивості першого рівня
    user: { ...state.user, name: 'Новий Name' }, // копіюємо об'єкт user і змінюємо name
}
```

**Додавання до масиву:**
Створюємо новий масив зі старих елементів плюс новий:

```javascript
const newTodos = [...state.todos, newTodo]
```

**Видалення з масиву:**
Використовуємо filter, який створює новий масив без елемента:

```javascript
const filtered = state.todos.filter((todo) => todo.id !== todoId)
```

**Оновлення елемента масиву:**
Використовуємо map для створення нового масиву з оновленим елементом:

```javascript
const updated = state.todos.map((todo) => (todo.id === todoId ? { ...todo, completed: true } : todo))
```

**Глибоко вкладені об'єкти:**
Тут складніше - потрібно копіювати кожен рівень вкладеності:

```javascript
const newState = {
    ...state,
    user: {
        ...state.user,
        profile: {
            ...state.user.profile,
            email: 'new@email.com',
        },
    },
}
```

Саме тому з'явився Redux Toolkit - він використовує бібліотеку Immer, яка дозволяє писати код, який виглядає як мутація, але насправді створює нові об'єкти.

**Термінологія:**

-   **filter** - метод масиву, створює новий масив з елементами, які пройшли перевірку
-   **Вкладеність (Nesting)** - структура об'єктів всередині об'єктів
-   **Immer** - бібліотека, яка спрощує роботу з іммутабельними оновленнями

---

## Слайд 14: Core Concepts: Store

**Що говорити:**
Переходимо до третього ключового поняття - Store.

Store - це об'єкт, який об'єднує все разом. Він зберігає весь стан додатку і надає методи для роботи з ним.

Створюємо Store за допомогою функції createStore, передаючи туди reducer:

```javascript
const store = createStore(todosReducer)
```

Store надає три основні методи:

**1. getState()** - повертає поточний стан:

```javascript
const currentState = store.getState()
console.log(currentState) // { todos: [], filter: 'all' }
```

**2. dispatch(action)** - відправляє action для зміни стану:

```javascript
store.dispatch({
    type: 'ADD_TODO',
    payload: { text: 'Learn Redux' },
})
```

**3. subscribe(listener)** - підписується на зміни стану. Повертає функцію для відписки:

```javascript
const unsubscribe = store.subscribe(() => {
    console.log('Стан змінився:', store.getState())
})

// Коли підписка більше не потрібна
unsubscribe()
```

Зверніть увагу: в реальних React додатках ви майже ніколи не викликаєте ці методи напряму. Бібліотека react-redux робить це за вас через хуки useSelector та useDispatch. Але важливо розуміти, як це працює під капотом.

**Термінологія:**

-   **Listener** - слухач, функція, яка викликається при певній події
-   **Subscribe/Unsubscribe** - підписатися/відписатися від подій
-   **Під капотом (Under the hood)** - внутрішня реалізація, як щось працює насправді

---

## Слайд 15: Комбінування Reducers

**Що говорити:**
У реальних додатках стан може бути дуже великим і складним. Було б незручно мати один величезний reducer на весь додаток. Тому Redux дозволяє розбити логіку на декілька маленьких reducers, а потім об'єднати їх.

Подивіться на приклад. У нас є два окремих reducer'и:

**todosReducer** - відповідає тільки за список todos. Він приймає не весь стан, а тільки масив todos:

```javascript
function todosReducer(state = [], action) {
    switch (action.type) {
        case 'ADD_TODO':
            return [...state, action.payload]
        default:
            return state
    }
}
```

**filterReducer** - відповідає тільки за фільтр:

```javascript
function filterReducer(state = 'all', action) {
    switch (action.type) {
        case 'SET_FILTER':
            return action.payload
        default:
            return state
    }
}
```

А потім використовуємо функцію combineReducers для їх об'єднання:

```javascript
const rootReducer = combineReducers({
    todos: todosReducer,
    filter: filterReducer,
})
```

Результат: структура стану буде виглядати так:

```javascript
{
  todos: [...],  // цим керує todosReducer
  filter: 'all'  // цим керує filterReducer
}
```

Коли ви dispatch'ите action, Redux автоматично передасть його в ОБА reducer'и. Кожен reducer подивиться на action.type і або оновить свою частину стану, або поверне її без змін.

Це називається **composition** - складання великої системи з маленьких, незалежних частин. Це робить код більш модульним і легким для підтримки.

**Термінологія:**

-   **combineReducers** - функція Redux для об'єднання кількох reducers
-   **Root Reducer** - кореневий reducer, який об'єднує всі інші
-   **Composition** - композиція, складання складної логіки з простих частин
-   **Модульність** - принцип розбиття коду на незалежні модулі

---

## Слайд 16: React + Redux: Підключення

**Що говорити:**
Тепер розглянемо, як підключити Redux до React додатку.

Спочатку створюємо Store. Зазвичай це робиться в окремому файлі store.js:

```javascript
import { createStore } from 'redux'
import rootReducer from './reducers'

const store = createStore(rootReducer)
export default store
```

Тут ми імпортуємо rootReducer (який ми створили за допомогою combineReducers), передаємо його в createStore, і експортуємо готовий store.

Потім у файлі index.js, де ми рендеримо весь додаток, обгортаємо його в компонент Provider:

```javascript
import { Provider } from 'react-redux'
import store from './store'

ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root'),
)
```

**Provider** - це спеціальний компонент з бібліотеки react-redux. Він:

-   Приймає prop store (наш Redux store)
-   Використовує React Context під капотом
-   Робить store доступним для всіх дочірніх компонентів

Після цього будь-який компонент всередині App може отримати доступ до Redux store через хуки useSelector та useDispatch, про які ми зараз поговоримо.

**Термінологія:**

-   **Provider** - постачальник, компонент, який надає доступ до даних
-   **React Context** - механізм React для передачі даних через дерево компонентів без props
-   **react-redux** - офіційна бібліотека для інтеграції Redux з React

---

## Слайд 17: React + Redux: useSelector

**Що говорити:**
Хук useSelector використовується для читання даних зі Store.

Він приймає функцію-селектор, яка отримує весь стан і повертає тільки потрібну частину:

```javascript
const todos = useSelector((state) => state.todos)
```

Тут state - це весь стан Redux store. Ми витягуємо з нього тільки todos. Компонент автоматично підпишеться на зміни цієї частини стану і перерендериться, коли вона зміниться.

Можна витягувати кілька частин стану:

```javascript
const todos = useSelector((state) => state.todos)
const filter = useSelector((state) => state.filter)
```

Також можна робити обчислення прямо в селекторі:

```javascript
const filteredTodos = useSelector((state) => {
    const { todos, filter } = state
    if (filter === 'active') {
        return todos.filter((t) => !t.completed)
    }
    if (filter === 'completed') {
        return todos.filter((t) => t.completed)
    }
    return todos
})
```

Тут ми фільтруємо todos на основі filter. Це зручно, але є підводний камінь: ця функція виконується при кожному рендері. Якщо обчислення складні, це може сповільнити додаток. Для складних обчислень використовують мемоізацію з createSelector, про що поговоримо пізніше.

**Важливо:** useSelector порівнює попередній результат з новим за допомогою строгої рівності (===). Якщо ви повертаєте новий об'єкт або масив, компонент буде рендеритися навіть якщо дані не змінилися!

**Термінологія:**

-   **Selector** - селектор, функція для витягування даних зі стану
-   **Hook** - хук, спеціальна функція React (useState, useEffect, useSelector)
-   **Мемоізація (Memoization)** - збереження результату обчислення для повторного використання
-   **Строга рівність (===)** - порівняння посилань, чи це той самий об'єкт в пам'яті

---

## Слайд 18: React + Redux: useDispatch

**Що говорити:**
Хук useDispatch використовується для відправки actions.

Він повертає функцію dispatch, за допомогою якої можна відправляти actions:

```javascript
const dispatch = useDispatch()
```

Це та сама функція store.dispatch, яку ми бачили раніше. react-redux просто надає зручний спосіб отримати до неї доступ.

Подивіться на приклад компонента форми для додавання todo:

```javascript
function AddTodoForm() {
    const dispatch = useDispatch()
    const [text, setText] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault() // Запобігаємо перезавантаженню сторінки

        dispatch({
            type: 'ADD_TODO',
            payload: {
                id: Date.now(),
                text,
                completed: false,
            },
        })

        setText('') // Очищаємо поле після додавання
    }

    return (
        <form onSubmit={handleSubmit}>
            <input value={text} onChange={(e) => setText(e.target.value)} />
            <button type="submit">Додати</button>
        </form>
    )
}
```

Що тут відбувається:

1. Отримуємо dispatch через useDispatch
2. Створюємо локальний стан для тексту в input (це нормально - не весь стан має бути в Redux!)
3. При submit форми відправляємо action ADD_TODO з текстом
4. Очищаємо поле вводу

Зверніть увагу: ми відправляємо action об'єкт напряму. У великих проектах краще використовувати action creators для уникнення дублювання коду.

**Термінологія:**

-   **e.preventDefault()** - метод, який запобігає стандартній поведінці браузера
-   **handleSubmit** - обробник події submit форми
-   **onSubmit** - подія, яка спрацьовує при відправці форми

---

## Слайд 19: Повний приклад: Counter App

**Що говорити:**
Тепер розглянемо повний приклад простого додатку Counter. Почнемо з actions.

**actions.js:**
Спочатку визначаємо константи для типів actions:

```javascript
export const INCREMENT = 'counter/increment'
export const DECREMENT = 'counter/decrement'
export const INCREMENT_BY_AMOUNT = 'counter/incrementByAmount'
```

Зверніть увагу на префікс 'counter/' - це namespace pattern, про який ми говорили.

Потім створюємо action creators:

```javascript
export const increment = () => ({ type: INCREMENT })
export const decrement = () => ({ type: DECREMENT })
export const incrementByAmount = (amount) => ({
    type: INCREMENT_BY_AMOUNT,
    payload: amount,
})
```

Перші два action creators не приймають аргументів, третій приймає amount.

**reducer.js:**

```javascript
const initialState = { value: 0 }

export function counterReducer(state = initialState, action) {
    switch (action.type) {
        case INCREMENT:
            return { value: state.value + 1 }
        case DECREMENT:
            return { value: state.value - 1 }
        case INCREMENT_BY_AMOUNT:
            return { value: state.value + action.payload }
        default:
            return state
    }
}
```

Reducer дуже простий: для кожного action повертаємо новий об'єкт з оновленим value. Не забуваємо default case!

**Термінологія:**

-   **Counter** - лічильник, додаток для збільшення/зменшення числа
-   **amount** - кількість, на яку збільшуємо/зменшуємо

---

## Слайд 20: Counter App: Component

**Що говорити:**
Тепер подивимося на компонент, який використовує наш counter:

```javascript
import { useSelector, useDispatch } from 'react-redux'
import { increment, decrement, incrementByAmount } from './actions'

function Counter() {
    const count = useSelector((state) => state.counter.value)
    const dispatch = useDispatch()

    return (
        <div>
            <h1>Count: {count}</h1>
            <button onClick={() => dispatch(increment())}>+1</button>
            <button onClick={() => dispatch(decrement())}>-1</button>
            <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
        </div>
    )
}
```

Розберемо по частинах:

1. **Читаємо стан:**

```javascript
const count = useSelector((state) => state.counter.value)
```

Витягуємо значення counter з Redux store. Компонент автоматично підпишеться на зміни.

2. **Отримуємо dispatch:**

```javascript
const dispatch = useDispatch()
```

3. **Відображаємо UI:**
   Показуємо поточне значення та кнопки для зміни.

4. **Обробляємо кліки:**

```javascript
onClick={() => dispatch(increment())}
```

При кліку викликаємо action creator і відразу відправляємо результат через dispatch.

Важливо: ми передаємо стрілкову функцію в onClick, а не просто `dispatch(increment())`. Якщо написати `onClick={dispatch(increment())}`, action відправиться одразу при рендері, а не при кліку!

**Термінологія:**

-   **onClick** - обробник події кліку
-   **Стрілкова функція (Arrow function)** - () => {}

---

## Слайд 21: Redux Toolkit (RTK)

**Що говорити:**
Тепер переходимо до сучасного способу роботи з Redux - Redux Toolkit, скорочено RTK.

Класичний Redux, який ми розглядали до цього, має кілька проблем:

**❌ Проблеми класичного Redux:**

1. **Багато boilerplate коду** - для простої фічі потрібно створити файл з constants, action creators, reducer, це багато повторюваного коду

2. **Складна настройка Store** - потрібно підключати middleware, DevTools, все налаштовувати вручну

3. **Іммутабельні оновлення складні** - весь цей код з spread операторами легко зробити помилку

4. **Для async операцій потрібні додаткові бібліотеки** - redux-thunk або redux-saga

**✅ Redux Toolkit вирішує ці проблеми:**

1. **Менше коду** - автоматична генерація action creators, менше boilerplate

2. **Вбудований Immer** - можна писати код, який виглядає як мутація: `state.value++`, а Immer під капотом зробить іммутабельне оновлення

3. **createSlice** - одна функція замість action types + action creators + reducer

4. **Вбудована підтримка async** - createAsyncThunk для асинхронних операцій

5. **Redux DevTools включені автоматично** - не потрібно нічого налаштовувати

6. **TypeScript friendly** - відмінна підтримка TypeScript

Redux Toolkit - це НЕ нова бібліотека, це обгортка над Redux, яка включає найкращі практики.

**Термінологія:**

-   **Boilerplate** - шаблонний код, який потрібно писати знову і знову
-   **Middleware** - проміжне ПЗ, обробляє actions між dispatch і reducer
-   **TypeScript** - типізована надбудова над JavaScript

---

## Слайд 22: Redux Toolkit: Встановлення

**Що говорити:**
Встановлення Redux Toolkit дуже просте.

Якщо створюєте новий проект, є готовий шаблон:

```bash
npx create-react-app my-app --template redux
```

Це створить React додаток з уже налаштованим Redux Toolkit, структурою папок, прикладами коду.

Якщо додаєте до існуючого проекту:

```bash
npm install @reduxjs/toolkit react-redux
```

або якщо використовуєте Yarn:

```bash
yarn add @reduxjs/toolkit react-redux
```

Зверніть увагу: встановлюємо дві бібліотеки:

-   **@reduxjs/toolkit** - сам Redux Toolkit, який включає Redux, Immer, Thunk, DevTools Extension
-   **react-redux** - офіційні React bindings (Provider, useSelector, useDispatch)

Після встановлення доступні основні API:

-   **configureStore()** - замість createStore, автоматично налаштовує middleware і DevTools
-   **createSlice()** - створює reducer і action creators за один раз
-   **createAsyncThunk()** - для асинхронних операцій
-   **createSelector()** - для мемоізованих селекторів (з бібліотеки Reselect)
-   **createEntityAdapter()** - для нормалізації даних

**Термінологія:**

-   **npm/yarn** - пакетні менеджери для JavaScript
-   **create-react-app** - офіційний інструмент для створення React додатків
-   **template** - шаблон проекту зі всіма налаштуваннями
-   **Bindings** - зв'язки, інтеграція між бібліотеками

---

## Слайд 23: createSlice: Основи

**Що говорити:**
createSlice - це основна функція Redux Toolkit, яка значно спрощує код.

Раніше нам потрібно було створювати окремо action types, action creators, і reducer. З createSlice все це створюється автоматично!

Подивіться на приклад:

```javascript
const counterSlice = createSlice({
    name: 'counter',
    initialState: { value: 0 },
    reducers: {
        increment: (state) => {
            state.value += 1 // Виглядає як мутація!
        },
        decrement: (state) => {
            state.value -= 1
        },
        incrementByAmount: (state, action) => {
            state.value += action.payload
        },
    },
})
```

Розберемо параметри:

**name: 'counter'** - назва slice, використовується як префікс для action types

**initialState: { value: 0 }** - початковий стан

**reducers** - об'єкт з reducer функціями. Ключі - це назви actions, значення - reducer функції.

**Важлива особливість:** можна писати код, який виглядає як мутація: `state.value += 1`. Це працює завдяки бібліотеці Immer! Під капотом Immer відстежує всі зміни і створює новий іммутабельний стан.

Можна і далі повертати новий стан явно, якщо хочете:

```javascript
increment: (state) => {
    return { value: state.value + 1 }
}
```

Обидва підходи працюють, але перший простіший і більш читабельний.

**Експорт:**

```javascript
export const { increment, decrement, incrementByAmount } = counterSlice.actions
```

Action creators створюються автоматично! Назви беруться з ключів reducers.

```javascript
export default counterSlice.reducer
```

Експортуємо reducer для підключення до store.

**Термінологія:**

-   **Slice** - шматок, частина стану (counter, todos, user)
-   **Immer** - бібліотека, яка дозволяє писати іммутабельний код у мутабельному стилі

---

## Слайд 24: configureStore: Створення Store

**Що говорити:**
Тепер розглянемо, як створити Store за допомогою configureStore.

У класичному Redux використовували createStore і вручну налаштовували middleware, DevTools. З Redux Toolkit все набагато простіше:

```javascript
import { configureStore } from '@reduxjs/toolkit'
import counterReducer from './features/counter/counterSlice'
import todosReducer from './features/todos/todosSlice'
import userReducer from './features/user/userSlice'

const store = configureStore({
    reducer: {
        counter: counterReducer,
        todos: todosReducer,
        user: userReducer,
    },
})
```

Це все! configureStore автоматично:

-   Викликає combineReducers для об'єднання reducer'ів
-   Додає redux-thunk middleware для async операцій
-   Підключає Redux DevTools Extension
-   Додає перевірки в development режимі (перевіряє мутації, недетерміновані функції)

**Структура стану** буде така:

```javascript
{
  counter: { value: 0 },
  todos: { items: [], filter: 'all' },
  user: { data: null, loading: false }
}
```

**Для TypeScript** можна експортувати типи:

```typescript
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
```

**RootState** - тип всього стану додатку
**AppDispatch** - тип функції dispatch (потрібно для async thunks)

Ці типи потім використовуються для створення типізованих версій useSelector і useDispatch.

**Термінологія:**

-   **ReturnType** - TypeScript utility type, витягує тип результату функції
-   **typeof** - оператор TypeScript для отримання типу значення
-   **Development режим** - режим розробки з додатковими перевірками

---

## Слайд 25: RTK: Повний приклад Todos

**Що говорити:**
Розглянемо повний приклад Todos додатку з Redux Toolkit.

```javascript
const todosSlice = createSlice({
    name: 'todos',
    initialState: {
        items: [],
        filter: 'all',
    },
    reducers: {
        addTodo: (state, action) => {
            state.items.push({
                id: Date.now(),
                text: action.payload,
                completed: false,
            })
        },
        toggleTodo: (state, action) => {
            const todo = state.items.find((t) => t.id === action.payload)
            if (todo) {
                todo.completed = !todo.completed
            }
        },
        deleteTodo: (state, action) => {
            state.items = state.items.filter((t) => t.id !== action.payload)
        },
        setFilter: (state, action) => {
            state.filter = action.payload
        },
    },
})
```

Зверніть увагу на код - він виглядає дуже просто!

**addTodo:**

```javascript
state.items.push({ ... });
```

Ми просто пушимо в масив! В класичному Redux це було б помилкою, але з Immer це працює.

**toggleTodo:**

```javascript
const todo = state.items.find((t) => t.id === action.payload)
if (todo) {
    todo.completed = !todo.completed
}
```

Знаходимо todo і прямо змінюємо його поле! Immer бачить цю зміну і створює новий іммутабельний стан.

**deleteTodo:**

```javascript
state.items = state.items.filter((t) => t.id !== action.payload)
```

Присвоюємо новий масив. Це також працює.

**setFilter:**

```javascript
state.filter = action.payload
```

Змінюємо примітивне значення.

Весь цей код набагато коротший і читабельніший, ніж з класичним Redux!

Не забуваємо експортувати actions і reducer:

```javascript
export const { addTodo, toggleTodo, deleteTodo, setFilter } = todosSlice.actions
export default todosSlice.reducer
```

**Термінологія:**

-   **push** - метод масиву для додавання елемента в кінець
-   **find** - метод масиву для пошуку елемента
-   **Примітивне значення** - прості типи даних (string, number, boolean)

---

## Слайд 26: RTK: Todos Component

**Що говорити:**
Тепер подивимося, як використовувати наш todos slice в React компоненті.

Компонент виглядає майже так само, як з класичним Redux, але тепер action creators створюються автоматично:

```javascript
import { useSelector, useDispatch } from 'react-redux'
import { addTodo, toggleTodo, deleteTodo } from './todosSlice'

function TodoList() {
    const todos = useSelector((state) => state.todos.items)
    const dispatch = useDispatch()
    const [text, setText] = useState('')

    const handleAdd = () => {
        dispatch(addTodo(text)) // Просто передаємо текст
        setText('')
    }

    return (
        <div>
            <input value={text} onChange={(e) => setText(e.target.value)} />
            <button onClick={handleAdd}>Додати</button>

            <ul>
                {todos.map((todo) => (
                    <li key={todo.id}>
                        <input
                            type="checkbox"
                            checked={todo.completed}
                            onChange={() => dispatch(toggleTodo(todo.id))}
                        />
                        <span
                            style={{
                                textDecoration: todo.completed ? 'line-through' : 'none',
                            }}
                        >
                            {todo.text}
                        </span>
                        <button onClick={() => dispatch(deleteTodo(todo.id))}>Видалити</button>
                    </li>
                ))}
            </ul>
        </div>
    )
}
```

Що відбувається:

1. Читаємо todos зі стану через useSelector
2. При додаванні викликаємо `dispatch(addTodo(text))` - передаємо тільки текст, payload створюється автоматично
3. При перемиканні відправляємо id: `dispatch(toggleTodo(todo.id))`
4. При видаленні теж відправляємо id: `dispatch(deleteTodo(todo.id))`

Зверніть увагу на стилі: якщо todo completed, додаємо line-through для перекресленого тексту.

**Термінологія:**

-   **checkbox** - прапорець, елемент форми
-   **line-through** - CSS властивість для перекресленого тексту
-   **ul/li** - HTML теги для списків (unordered list / list item)

---

## Слайд 27: Middleware в Redux

**Що говорити:**
Middleware - це важлива концепція в Redux. Це функції, які "сидять" між dispatch і reducer і можуть:

-   Логувати actions
-   Відправляти звіти про помилки
-   Робити асинхронні запити
-   Модифікувати або зупиняти actions

Подивіться на схему потоку даних з middleware:

```
Action → Middleware 1 → Middleware 2 → Reducer → Store
```

Коли ви викликаєте dispatch(action), action спочатку проходить через всі middleware по черзі, і тільки потім потрапляє до reducer.

Простий приклад logger middleware:

```javascript
const loggerMiddleware = (store) => (next) => (action) => {
    console.log('Dispatching:', action)
    const result = next(action) // Передаємо далі
    console.log('Next state:', store.getState())
    return result
}
```

Це складна конструкція - функція, яка повертає функцію, яка повертає функцію (currying). Розберемо:

-   **store** - доступ до Redux store (getState, dispatch)
-   **next** - наступний middleware або reducer
-   **action** - action, який dispatch'или
-   **next(action)** - передати action далі по ланцюгу

Підключення middleware:

```javascript
const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(loggerMiddleware),
})
```

**getDefaultMiddleware()** повертає стандартні middleware (thunk, серіалізація, іммутабельність перевірки). Ми додаємо свій через concat.

**Термінологія:**

-   **Middleware** - проміжне програмне забезпечення
-   **Currying** - техніка перетворення функції з багатьма аргументами на послідовність функцій
-   **Logging** - запис подій для відлагодження
-   **Crash reporting** - відправка інформації про помилки на сервер

---

## Слайд 28: Async Operations: Проблема

**Що говорити:**
Тепер поговоримо про одну з найскладніших частин Redux - асинхронні операції.

Пригадаємо правила reducer'ів: вони мають бути чистими функціями без побічних ефектів. Це означає, що **НЕМОЖНА робити async операції в reducer!**

Подивіться на цей неправильний приклад:

```javascript
function todosReducer(state, action) {
    switch (action.type) {
        case 'FETCH_TODOS':
            // ❌ ПОМИЛКА! Async код в reducer!
            fetch('/api/todos')
                .then((res) => res.json())
                .then((data) => {
                    // Як тут dispatch нового action?
                })
            return state
    }
}
```

Проблеми:

1. Reducer не може робити async операції
2. Reducer не має доступу до dispatch для відправки нового action з даними
3. Це порушує принцип чистої функції

Також не можна просто dispatch'ити Promise:

```javascript
dispatch(fetch('/api/todos')) // НЕ ПРАЦЮЄ!
```

Redux очікує, що action буде звичайним об'єктом з полем type. Promise - це не об'єкт з type!

**Рішення:**
Потрібен спосіб виконувати async код ДО того, як action потрапить до reducer. Для цього використовують:

1. **Redux Thunk** - middleware, який дозволяє dispatch'ити функції замість об'єктів
2. **createAsyncThunk** з Redux Toolkit - високорівнева абстракція над thunk

**Термінологія:**

-   **Async/асинхронний** - код, який виконується не одразу (setTimeout, fetch, Promise)
-   **Sync/синхронний** - код, який виконується послідовно, рядок за рядком
-   **Promise** - об'єкт для роботи з асинхронним кодом
-   **fetch** - API для HTTP запитів

---

## Слайд 29: Redux Thunk

**Що говорити:**
Redux Thunk - це middleware, який вирішує проблему асинхронних операцій.

Спочатку розберемо, що таке thunk. **Thunk** - це функція, яка повертає іншу функцію. Назва походить з функціонального програмування і означає "відкладене обчислення".

**Звичайний action creator** повертає об'єкт:

```javascript
const addTodo = (text) => ({ type: 'ADD_TODO', payload: text })
```

**Thunk action creator** повертає функцію:

```javascript
const fetchTodos = () => {
    return async (dispatch, getState) => {
        // async логіка тут
    }
}
```

Ця функція отримує два аргументи:

-   **dispatch** - функція для відправки actions
-   **getState** - функція для читання поточного стану (рідко використовується)

Подивіться на повний приклад:

```javascript
const fetchTodos = () => {
    return async (dispatch, getState) => {
        // 1. Відправляємо action про початок завантаження
        dispatch({ type: 'FETCH_TODOS_REQUEST' })

        try {
            // 2. Робимо async запит
            const response = await fetch('/api/todos')
            const todos = await response.json()

            // 3. Відправляємо action з даними
            dispatch({ type: 'FETCH_TODOS_SUCCESS', payload: todos })
        } catch (error) {
            // 4. Якщо помилка - відправляємо action з помилкою
            dispatch({ type: 'FETCH_TODOS_FAILURE', payload: error.message })
        }
    }
}
```

Використання:

```javascript
dispatch(fetchTodos())
```

Redux Thunk перехоплює цю функцію, викликає її, передаючи dispatch і getState, і функція може робити що завгодно, включно з async операціями.

**Термінологія:**

-   **Thunk** - відкладене обчислення, функція, що повертає функцію
-   **try/catch** - конструкція для обробки помилок
-   **await** - чекає на виконання Promise
-   **HTTP запит** - запит до сервера

---

## Слайд 30: createAsyncThunk: Основи

**Що говорити:**
Redux Toolkit надає createAsyncThunk - більш зручний спосіб роботи з async операціями.

createAsyncThunk автоматизує рутинні речі: створення action types для pending/fulfilled/rejected станів, обробку помилок.

Синтаксис:

```javascript
export const fetchTodos = createAsyncThunk(
    'todos/fetchTodos', // action type prefix
    async (userId, thunkAPI) => {
        // async функція
        const response = await fetch(`/api/users/${userId}/todos`)
        if (!response.ok) {
            throw new Error('Failed to fetch todos')
        }
        return response.json() // це стане action.payload
    },
)
```

Розберемо параметри:

**Перший аргумент:** 'todos/fetchTodos' - префікс для action types. createAsyncThunk автоматично створить три action types:

-   **'todos/fetchTodos/pending'** - коли запит починається
-   **'todos/fetchTodos/fulfilled'** - коли запит успішний
-   **'todos/fetchTodos/rejected'** - коли запит завершився помилкою

**Другий аргумент:** async функція, яка виконує запит. Вона отримує:

-   **userId** - аргумент, який ви передаєте при dispatch: `dispatch(fetchTodos(123))`
-   **thunkAPI** - об'єкт з корисними методами (dispatch, getState, rejectWithValue)

**Що повертає функція:**

-   Якщо успішно - повертає дані, вони стануть `action.payload` в fulfilled action
-   Якщо помилка (throw) - створюється rejected action з помилкою

Використання:

```javascript
dispatch(fetchTodos(userId))
```

**Термінологія:**

-   **pending** - очікування, запит у процесі
-   **fulfilled** - виконано успішно
-   **rejected** - відхилено, помилка
-   **thunkAPI** - API для thunk функцій

---

## Слайд 31: createAsyncThunk: Reducer

**Що говорити:**
Тепер подивимося, як обробляти ці async actions в reducer.

Для async actions, створених через createAsyncThunk, використовується спеціальний розділ **extraReducers** в createSlice:

```javascript
const todosSlice = createSlice({
    name: 'todos',
    initialState: {
        items: [],
        loading: false,
        error: null,
    },
    reducers: {
        // Тут звичайні синхронні actions
    },
    extraReducers: (builder) => {
        // Тут обробляємо async actions
    },
})
```

**Чому extraReducers?** Тому що ці actions створені ЗА МЕЖАМИ нашого slice, за допомогою createAsyncThunk.

У extraReducers використовується **builder pattern**:

```javascript
extraReducers: (builder) => {
    builder
        .addCase(fetchTodos.pending, (state) => {
            state.loading = true
            state.error = null
        })
        .addCase(fetchTodos.fulfilled, (state, action) => {
            state.loading = false
            state.items = action.payload // Дані з сервера
        })
        .addCase(fetchTodos.rejected, (state, action) => {
            state.loading = false
            state.error = action.error.message // Повідомлення про помилку
        })
}
```

Що тут відбувається:

**pending:** Коли запит починається:

-   Встановлюємо loading = true (щоб показати spinner)
-   Очищаємо попередню помилку

**fulfilled:** Коли запит успішний:

-   Встановлюємо loading = false
-   Зберігаємо дані в items
-   action.payload містить те, що повернула async функція

**rejected:** Коли сталася помилка:

-   Встановлюємо loading = false
-   Зберігаємо повідомлення про помилку

Така структура стану з loading/error дуже типова для async операцій.

**Термінологія:**

-   **extraReducers** - додаткові reducer'и для зовнішніх actions
-   **Builder pattern** - патерн проектування з методами, які повертають this для ланцюжка викликів
-   **addCase** - метод для додавання обробника конкретного action type
-   **Spinner** - індикатор завантаження (крутилка)

---

## Слайд 32: createAsyncThunk: Component

**Що говорити:**
Тепер подивимося, як використовувати все це в React компоненті.

```javascript
import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { fetchTodos } from './todosSlice'

function TodoList() {
    const dispatch = useDispatch()
    const { items, loading, error } = useSelector((state) => state.todos)

    useEffect(() => {
        dispatch(fetchTodos(123)) // userId
    }, [dispatch])

    if (loading) return <div>Завантаження...</div>
    if (error) return <div>Помилка: {error}</div>

    return (
        <ul>
            {items.map((todo) => (
                <li key={todo.id}>{todo.text}</li>
            ))}
        </ul>
    )
}
```

Розберемо покроково:

**1. Читаємо стан:**

```javascript
const { items, loading, error } = useSelector((state) => state.todos)
```

Використовуємо деструктуризацію для витягування items, loading та error.

**2. Завантаження при монтуванні:**

```javascript
useEffect(() => {
    dispatch(fetchTodos(123))
}, [dispatch])
```

useEffect з порожнім масивом залежностей (тільки dispatch) виконається один раз при монтуванні компонента. Тут ми відправляємо async action для завантаження todos.

**3. Відображаємо різні стани:**

```javascript
if (loading) return <div>Завантаження...</div>
if (error) return <div>Помилка: {error}</div>
```

Це called "early returns" - якщо loading, показуємо індикатор, якщо error - повідомлення про помилку. Тільки якщо все ОК, показуємо список.

**4. Рендеримо список:**

```javascript
<ul>
    {items.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
    ))}
</ul>
```

Важливо: завжди додавайте key при рендері списків! React використовує key для оптимізації.

**Термінологія:**

-   **useEffect** - React хук для побічних ефектів (API запити, підписки)
-   **Деструктуризація** - синтаксис для витягування властивостей з об'єкта
-   **Монтування (Mount)** - коли компонент вперше з'являється на сторінці
-   **Early return** - раннє повернення з функції
-   **key prop** - спеціальний prop для допомоги React ідентифікувати елементи списку

---

## Слайд 33: Повний приклад: User Profile з API

**Що говорити:**
Тепер розглянемо більш реалістичний приклад - профіль користувача з можливістю завантаження та оновлення.

Створимо два async thunks:

**fetchUser** - для завантаження даних користувача:

```javascript
export const fetchUser = createAsyncThunk('user/fetchUser', async (userId, { rejectWithValue }) => {
    try {
        const response = await fetch(`/api/users/${userId}`)
        if (!response.ok) throw new Error('User not found')
        return await response.json()
    } catch (error) {
        return rejectWithValue(error.message)
    }
})
```

Зверніть увагу на **rejectWithValue** - це метод з thunkAPI. Він дозволяє самостійно контролювати, що буде в action.payload при помилці. Без нього action.payload містив би серіалізований Error об'єкт, що незручно.

**updateUser** - для оновлення даних:

```javascript
export const updateUser = createAsyncThunk('user/updateUser', async ({ userId, data }) => {
    const response = await fetch(`/api/users/${userId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    return await response.json()
})
```

Тут ми приймаємо об'єкт з userId та data. Використовуємо деструктуризацію параметрів.

**PATCH** - HTTP метод для часткового оновлення ресурсу (на відміну від PUT, який замінює повністю).

**JSON.stringify** - перетворює JavaScript об'єкт у JSON рядок для відправки на сервер.

**Термінологія:**

-   **rejectWithValue** - метод для відхилення з кастомним значенням
-   **PATCH** - HTTP метод для часткового оновлення
-   **PUT** - HTTP метод для повного оновлення
-   **Content-Type** - HTTP заголовок, що вказує тип даних
-   **JSON** - JavaScript Object Notation, формат даних

---

## Слайд 34: User Slice: Reducer

**Що говорити:**
Тепер створимо slice для обробки цих async actions.

```javascript
const userSlice = createSlice({
    name: 'user',
    initialState: {
        data: null, // Дані користувача
        loading: false, // Чи завантажуються дані
        error: null, // Помилка завантаження
        updating: false, // Чи оновлюються дані
    },
    reducers: {
        clearUser: (state) => {
            state.data = null
            state.error = null
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch user
            .addCase(fetchUser.pending, (state) => {
                state.loading = true
            })
            .addCase(fetchUser.fulfilled, (state, action) => {
                state.loading = false
                state.data = action.payload
            })
            .addCase(fetchUser.rejected, (state, action) => {
                state.loading = false
                state.error = action.payload // Тут наше повідомлення з rejectWithValue
            })
            // Update user
            .addCase(updateUser.pending, (state) => {
                state.updating = true
            })
            .addCase(updateUser.fulfilled, (state, action) => {
                state.updating = false
                state.data = action.payload // Оновлені дані з сервера
            })
    },
})
```

Зверніть увагу на кілька моментів:

1. **Окремі флаги loading і updating** - це дозволяє показувати різні індикатори. Наприклад, при завантаженні показувати spinner на всю сторінку, а при оновленні - тільки disabled на кнопці "Зберегти".

2. **clearUser в reducers** - це синхронний action для очищення даних користувача (наприклад, при logout).

3. **Для updateUser немає rejected case** - це необов'язково. Можете додати обробку помилок оновлення, якщо потрібно.

4. **data: null** - використовуємо null замість undefined, щоб явно вказати "дані ще не завантажені" vs "немає даних".

**Термінологія:**

-   **Flag** - прапорець, boolean змінна для позначення стану
-   **disabled** - HTML атрибут, що робить елемент неактивним
-   **logout** - вихід з системи
-   **null vs undefined** - null = явна відсутність значення, undefined = значення не визначене

---

## Слайд 35: User Profile Component

**Що говорити:**
І нарешті, компонент для відображення та редагування профілю користувача.

```javascript
function UserProfile({ userId }) {
    const dispatch = useDispatch()
    const { data, loading, error, updating } = useSelector((state) => state.user)

    useEffect(() => {
        dispatch(fetchUser(userId))
    }, [userId, dispatch])

    const handleUpdate = (newData) => {
        dispatch(updateUser({ userId, data: newData }))
    }

    if (loading) return <Spinner />
    if (error) return <ErrorMessage error={error} />
    if (!data) return null

    return (
        <div>
            <h1>{data.name}</h1>
            <p>{data.email}</p>
            <button onClick={() => handleUpdate({ name: 'New Name' })} disabled={updating}>
                {updating ? 'Оновлення...' : 'Оновити'}
            </button>
        </div>
    )
}
```

Розберемо логіку:

**1. Завантаження даних:**

```javascript
useEffect(() => {
    dispatch(fetchUser(userId))
}, [userId, dispatch])
```

useEffect залежить від userId - якщо userId зміниться, завантажимо дані іншого користувача.

**2. Обробка станів:**

```javascript
if (loading) return <Spinner />
if (error) return <ErrorMessage error={error} />
if (!data) return null
```

Early returns для різних станів. Якщо data === null (ще не завантажені), повертаємо null (нічого не рендеримо).

**3. Кнопка оновлення:**

```javascript
<button onClick={() => handleUpdate({ name: 'New Name' })} disabled={updating}>
    {updating ? 'Оновлення...' : 'Оновити'}
</button>
```

-   **disabled={updating}** - поки йде оновлення, кнопка неактивна (користувач не може натиснути ще раз)
-   **Умовний текст** - показуємо "Оновлення..." або "Оновити" залежно від стану

У реальному додатку handleUpdate викликався б з форми, а не з хардкоднутим значенням.

**Термінологія:**

-   **Hardcoded** - захардкоджене, значення написане напряму в коді
-   **Conditional rendering** - умовний рендеринг
-   **Props** - властивості, які передаються в компонент

---

## Слайд 36: Селектори (Selectors)

**Що говорити:**
Селектори - це функції для витягування та обчислення даних зі стану. Вони роблять код більш читабельним та підтримуваним.

**Прості селектори:**

```javascript
const selectTodos = (state) => state.todos.items
const selectFilter = (state) => state.todos.filter
```

Це просто функції, які приймають весь стан і повертають його частину. Навіщо вони потрібні, якщо можна писати `state => state.todos.items` напряму?

**Переваги селекторів:**

1. **Переви використання:** Якщо структура стану зміниться, міняємо тільки селектор, а не кожен useSelector по всіх компонентах.

2. **Іменовані функції:** `selectTodos` читабельніше, ніж анонімна стрілкова функція.

3. **Можна виносити логіку:** Розглянемо selector з логікою:

```javascript
const selectFilteredTodos = (state) => {
    const todos = state.todos.items
    const filter = state.todos.filter

    if (filter === 'active') {
        return todos.filter((t) => !t.completed)
    }
    if (filter === 'completed') {
        return todos.filter((t) => t.completed)
    }
    return todos
}
```

Тепер ця логіка фільтрації в одному місці, а компоненти просто використовують:

```javascript
const filteredTodos = useSelector(selectFilteredTodos)
```

**Проблема:** Ця функція буде викликатися при кожному рендері, і filter буде виконуватися кожного разу, навіть якщо todos і filter не змінилися. Для вирішення використовують мемоізацію.

**Термінологія:**

-   **Selector** - селектор, функція для витягування даних
-   **Повторне використання (Reusability)** - можливість використовувати код в різних місцях
-   **Підтримуваність (Maintainability)** - легкість внесення змін
-   **Мемоізація (Memoization)** - збереження результату обчислень

---

## Слайд 37: createSelector: Мемоізація

**Що говорити:**
createSelector створює мемоізовані селектори - селектори, які запам'ятовують попередній результат і повертають його, якщо вхідні дані не змінилися.

```javascript
import { createSelector } from '@reduxjs/toolkit'

// Input selectors
const selectTodos = (state) => state.todos.items
const selectFilter = (state) => state.todos.filter

// Мемоізований selector
const selectFilteredTodos = createSelector(
    [selectTodos, selectFilter], // Input selectors
    (todos, filter) => {
        // Result function
        console.log('Обчислення відфільтрованих todos')

        if (filter === 'active') return todos.filter((t) => !t.completed)
        if (filter === 'completed') return todos.filter((t) => t.completed)
        return todos
    },
)
```

Як це працює:

**Input selectors:** `[selectTodos, selectFilter]`

-   createSelector викликає кожен input selector
-   Порівнює результати з попередніми (за допомогою ===)

**Result function:** `(todos, filter) => { ... }`

-   Викликається ТІЛЬКИ якщо хоч один з input селекторів повернув нове значення
-   Результат кешується

Подивіться на console.log - він виведеться тільки коли todos або filter зміняться! Якщо компонент ререндериться з іншої причини, обчислення не відбудеться, поверneться закешований результат.

**Складніший приклад - статистика:**

```javascript
const selectTodoStats = createSelector([selectTodos], (todos) => ({
    total: todos.length,
    active: todos.filter((t) => !t.completed).length,
    completed: todos.filter((t) => t.completed).length,
}))
```

Тут ми обчислюємо статистику - загальна кількість, активні, завершені. Без мемоізації це обчислювалося б при кожному рендері будь-якого компонента, який підписаний на стан.

**Важливо:** createSelector з Reselect бібліотеки, але Redux Toolkit експортує його для зручності.

**Термінологія:**

-   **Кешування (Caching)** - збереження результату для повторного використання
-   **Input selectors** - вхідні селектори, витягують дані
-   **Result function** - функція обчислення результату
-   **Reselect** - бібліотека для створення мемоізованих селекторів

---

## Слайд 38: Селектори з параметрами

**Що говорити:**
Іноді потрібен селектор, який приймає додаткові параметри. Наприклад, знайти todo за id.

**Підхід 1: Selector factory**

```javascript
const makeSelectTodoById = () =>
    createSelector([selectTodos, (state, todoId) => todoId], (todos, todoId) => todos.find((t) => t.id === todoId))
```

Це фабрика - функція, що створює selector. Використання:

```javascript
function TodoItem({ todoId }) {
    const selectTodoById = useMemo(makeSelectTodoById, [])
    const todo = useSelector((state) => selectTodoById(state, todoId))

    return <div>{todo?.text}</div>
}
```

**useMemo** тут потрібен, щоб створити selector один раз при монтуванні, а не при кожному рендері.

**Чому це потрібно?** Кожен selector має свій власний кеш. Якщо створювати новий selector при кожному рендері, мемоізація не працюватиме.

**Підхід 2: Простіший (але без мемоізації):**

```javascript
const selectTodoById = (state, todoId) => state.todos.items.find((t) => t.id === todoId)

function TodoItem({ todoId }) {
    const todo = useSelector((state) => selectTodoById(state, todoId))
    return <div>{todo?.text}</div>
}
```

Цей підхід простіший, але find буде викликатися при кожному рендері будь-якого компонента, підписаного на todos. Для великих списків це може бути повільно.

**Optional chaining (?.)**:

```javascript
{
    todo?.text
}
```

Це безпечний доступ до властивості. Якщо todo === null або undefined, не буде помилки, просто поверне undefined.

**Термінологія:**

-   **Factory** - фабрика, функція, що створює інші функції/об'єкти
-   **useMemo** - React хук для мемоізації значень
-   **Optional chaining (?.)** - безпечний доступ до властивостей
-   **find** - метод масиву для пошуку елемента

---

## Слайд 39: Redux DevTools

**Що говорити:**
Redux DevTools - це надпотужний інструмент для відлагодження Redux додатків. Це браузерне розширення, яке дозволяє:

**1. Перегляд всіх actions та state:**
Бачите всі actions, які були відправлені, і як вони змінили стан. Можна клікнути на будь-який action і подивитися:

-   Action type і payload
-   Стан ДО цього action
-   Стан ПІСЛЯ цього action
-   Diff - що саме змінилося

**2. Time Travel - подорож в часі:**
Можна "перемотати" стан назад до будь-якого попереднього action! Це ДУЖЕ корисно для відлагодження. Наприклад, ви зробили 50 дій, і щось пішло не так на 30-й. Просто перемотуєте до 30-ї і дивитеся, що сталося.

**3. Snapshot testing:**
Можна зберегти поточний стан і пізніше порівняти з ним.

**4. Action/State charts:**
Візуалізація того, як часто викликаються різні actions.

**5. Import/Export стану:**
Можна експортувати стан і історію actions, відправити колезі, і вони зможуть імпортувати і побачити точно те саме, що бачили ви.

**Налаштування з Redux Toolkit:**

```javascript
const store = configureStore({
    reducer: rootReducer,
    devTools: process.env.NODE_ENV !== 'production',
})
```

У Redux Toolkit DevTools включені автоматично в development режимі і вимкнені в production. Це важливо - не хочете, щоб користувачі бачили всю внутрішню кухню!

**Встановлення:**
Шукайте "Redux DevTools" в магазині розширень Chrome або Firefox.

**Термінологія:**

-   **DevTools** - інструменти розробника
-   **Browser extension** - розширення браузера
-   **Diff** - різниця між двома версіями
-   **Time Travel Debugging** - відлагодження з можливістю повернутися в часі
-   **Snapshot** - знімок, збережений стан в певний момент часу

---

## Слайд 40: Best Practices: Структура проєкту

**Що говорити:**
Правильна структура проєкту дуже важлива для підтримуваності. Redux офіційно рекомендує **feature-based structure** - організацію за функціональністю.

Подивіться на структуру:

```
src/
├── app/
│   ├── store.js              # Налаштування store
│   └── hooks.js              # Типізовані hooks (TS)
├── features/
│   ├── todos/
│   │   ├── todosSlice.js     # Slice + reducers + actions
│   │   ├── TodoList.jsx      # Компоненти
│   │   ├── TodoItem.jsx
│   │   └── todosAPI.js       # API calls
│   ├── user/
│   │   ├── userSlice.js
│   │   └── UserProfile.jsx
│   └── counter/
│       ├── counterSlice.js
│       └── Counter.jsx
└── index.js
```

**Ключові моменти:**

**app/** - загальні налаштування додатку

-   store.js - створення і експорт store
-   hooks.js - типізовані useAppDispatch і useAppSelector для TypeScript

**features/** - кожна фіча в окремій папці

-   Все, що стосується todos, знаходиться в features/todos/
-   slice, компоненти, API calls - все разом
-   Легко знайти, легко видалити фічу цілком

**Альтернативний підхід (НЕ рекомендується):**

```
src/
├── actions/
│   ├── todoActions.js
│   ├── userActions.js
├── reducers/
│   ├── todoReducer.js
│   ├── userReducer.js
├── components/
│   ├── TodoList.jsx
│   ├── UserProfile.jsx
```

Проблема: щоб працювати з однією фічею, потрібно відкривати файли в різних папках. Важко видалити фічу - треба знайти всі пов'язані файли.

**Feature-based structure** краща, бо всі файли однієї фічі разом.

**Термінологія:**

-   **Feature-based structure** - структура на основі функціональності
-   **Maintainability** - підтримуваність, легкість внесення змін
-   **Colocation** - розміщення пов'язаних речей разом
-   **TypeScript** - типізована надбудова над JavaScript

---

**[ЧАСТИНА 2 НОТАТОК]**

## Слайд 41: Best Practices: Коли використовувати Redux

**Що говорити:**
Дуже важливе питання - коли варто використовувати Redux, а коли ні. Redux - потужний інструмент, але він додає складності. Не варто використовувати його "просто тому що".

**✅ Використовуйте Redux коли:**

**1. Великий додаток з багатьма компонентами**
Якщо у вас десятки або сотні компонентів, і багато хто з них потребують доступу до спільного стану.

**2. Стан потрібен в багатьох місцях**
Наприклад, інформація про користувача використовується в Header, Sidebar, Profile, Settings - по всьому додатку.

**3. Складна логіка зміни стану**
Коли зміна одного значення тригерить багато інших змін. Redux робить цю логіку передбачуваною.

**4. Потрібен Time Travel debugging**
Для складних бізнес-додатків можливість "відмотати" стан назад дуже цінна.

**5. Велика команда**
Redux вводить чіткі правила, як працювати зі станом. Це допомагає в команді - всі пишуть код однаково.

**❌ НЕ використовуйте Redux коли:**

**1. Малий додаток**
Якщо у вас 5-10 компонентів, Context API цілком достатньо. Redux буде overhead'ом.

**2. Стан локальний для компонента**
Якщо стан використовується тільки в одному компоненті і його дітях - використовуйте useState або Context.

**3. Простий CRUD без складної логіки**
Для простих форм, списків з базовим CRUD не потрібна вся потужність Redux.

**4. Learning curve важливіший**
Якщо команда не знайома з Redux і проект потрібно зробити швидко, навчання займе час.

**Золоте правило:** Починайте з простіших рішень (useState, Context), і переходьте на Redux, коли відчуєте, що це справді потрібно.

**Термінологія:**

-   **Overhead** - надлишкова складність, зайві витрати
-   **CRUD** - Create, Read, Update, Delete - базові операції з даними
-   **Learning curve** - крива навчання, час потрібний для освоєння
-   **Context API** - вбудований механізм React для глобального стану

---

## Слайд 42: Best Practices: Нормалізація даних

**Що говорити:**
Нормалізація даних - це важлива техніка організації стану в Redux, особливо для складних вкладених структур.

**Проблема вкладеної структури:**

```javascript
{
    posts: [
        {
            id: 1,
            title: 'Post 1',
            author: { id: 5, name: 'John' },
            comments: [{ id: 10, text: 'Great!', author: { id: 5, name: 'John' } }],
        },
    ]
}
```

Проблеми:

1. **Дублювання даних** - author John з'являється двічі. Якщо змінимо його ім'я, потрібно оновити в багатьох місцях.
2. **Складність оновлення** - щоб змінити текст коментаря, потрібно знайти post, потім comment, потім оновити з іммутабельністю - це складно.
3. **Важко знайти дані** - щоб знайти всі пости автора, треба пройтись по всіх постах і перевірити author.id.

**Нормалізована структура:**

```javascript
{
  posts: {
    byId: {
      1: { id: 1, title: 'Post 1', authorId: 5, commentIds: [10] }
    },
    allIds: [1]
  },
  users: {
    byId: {
      5: { id: 5, name: 'John' }
    },
    allIds: [5]
  },
  comments: {
    byId: {
      10: { id: 10, text: 'Great!', authorId: 5, postId: 1 }
    },
    allIds: [10]
  }
}
```

Це схоже на реляційну базу даних! Кожна сутність в окремій "таблиці".

**Переваги:**

1. **Немає дублювання** - user з id 5 зберігається один раз
2. **Легко оновлювати** - щоб змінити ім'я John, змінюємо `state.users.byId[5].name`
3. **Швидкий доступ** - отримати post за id: `state.posts.byId[1]` - O(1)
4. **Зручно додавати/видаляти** - просто додаємо/видаляємо з byId і allIds

**byId + allIds pattern:**

-   **byId** - об'єкт для швидкого доступу за id
-   **allIds** - масив для збереження порядку та ітерації

Redux Toolkit має **createEntityAdapter** для автоматизації цього!

**Термінологія:**

-   **Нормалізація** - процес організації даних для усунення дублювання
-   **Реляційна БД** - база даних з таблицями та зв'язками
-   **O(1)** - константна складність, дуже швидко
-   **Сутність (Entity)** - об'єкт предметної області (user, post, comment)

---

## Слайд 61: RTK Query - Введення

**Що говорити:**
Тепер переходимо до однієї з найпотужніших можливостей Redux Toolkit - RTK Query. Це революційний підхід до роботи з даними від сервера.

**Проблема без RTK Query:**

До появи RTK Query, для кожного API запиту нам потрібно було:

1. Створювати async thunk за допомогою createAsyncThunk
2. Вручну обробляти три стани: pending, fulfilled, rejected
3. Додавати в initialState поля loading, error, data
4. Писати extraReducers для обробки всіх трьох станів
5. І робити це для КОЖНОГО endpoint!

Уявіть, у вас 20 API endpoints - це величезна кількість boilerplate коду!

❌ **Також немає:**

-   Автоматичного кешування - кожного разу робимо запит заново
-   Автоматичного re-fetching - якщо дані застаріли, не знаємо про це
-   Дедуплікації - якщо два компоненти запитують ті самі дані одночасно, робимо два запити

**RTK Query вирішує все це:**

✅ **Автоматичне управління станом** - loading, error, success створюються автоматично
✅ **Кешування** - запит виконується один раз, результат зберігається
✅ **Автоматичний re-fetching** - дані оновлюються коли потрібно
✅ **Інвалідація кешу** - після мутації автоматично оновлюємо пов'язані дані
✅ **Генерація hooks** - для кожного endpoint автоматично створюється хук
✅ **Polling** - автоматичне періодичне оновлення даних
✅ **Prefetching** - передзавантаження даних до того, як вони знадобляться

RTK Query натхненний такими бібліотеками як React Query та Apollo Client, але інтегрований безпосередньо в Redux Toolkit.

**Термінологія:**

-   **Boilerplate** - шаблонний код, який доводиться писати знову і знову
-   **Кешування (Caching)** - збереження результатів запитів для повторного використання
-   **Re-fetching** - повторне завантаження даних
-   **Дедуплікація (Deduplication)** - усунення дублікатів, об'єднання однакових запитів
-   **Інвалідація кешу** - позначення даних як застарілих, що потребують оновлення
-   **Polling** - періодичне опитування сервера для оновлення даних

---

## Слайд 62: RTK Query: Основні концепції

**Що говорити:**
RTK Query побудований навколо кількох ключових концепцій. Розберемо кожну.

**API Slice - центральна частина:**

Це не звичайний slice з createSlice. Це спеціальний slice, створений за допомогою **createApi**:

```javascript
export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['Todo', 'User'],
  endpoints: (builder) => ({ ... })
});
```

Розберемо параметри:

**reducerPath: 'api'**
Це ключ, під яким API slice буде зберігатися в Redux store. Стан буде доступний як `state.api`.

**baseQuery: fetchBaseQuery({ baseUrl: '/api' })**
fetchBaseQuery - це обгортка над fetch API. Ви вказуєте базову URL, і всі запити будуть робитися відносно неї.

Наприклад, якщо endpoint `'todos'`, повний URL буде `/api/todos`.

Можна використовувати свій baseQuery, наприклад, для axios:

```javascript
const axiosBaseQuery =
    ({ baseUrl }) =>
    async ({ url, method, data }) => {
        const result = await axios({ url: baseUrl + url, method, data })
        return { data: result.data }
    }
```

**tagTypes: ['Todo', 'User']**
Типи тегів для системи кешування та інвалідації. Про це детально на наступних слайдах. Коротко: це "мітки", які дозволяють групувати дані і автоматично оновлювати їх.

**endpoints: (builder) => ({ ... })**
Тут визначаємо всі наші API endpoints. builder надає методи:

-   **builder.query** - для читання даних (GET)
-   **builder.mutation** - для зміни даних (POST, PUT, DELETE, PATCH)

**Два типи endpoints:**

**Query** - для отримання даних:

-   Виконується автоматично при монтуванні компонента
-   Результати кешуються
-   Можна налаштувати polling, re-fetching

**Mutation** - для зміни даних:

-   Виконується вручну при виклику
-   Може інвалідувати кеш для оновлення пов'язаних queries
-   Повертає promise з результатом

**Термінологія:**

-   **API Slice** - спеціальний slice для роботи з API
-   **fetchBaseQuery** - вбудована функція для HTTP запитів
-   **baseUrl** - базова URL для всіх запитів
-   **endpoint** - точка доступу API, конкретний URL
-   **builder** - об'єкт з методами для створення endpoints
-   **GET/POST/PUT/DELETE/PATCH** - HTTP методи

---

## Слайд 63: RTK Query: Query Endpoints

**Що говорити:**
Розглянемо детально, як створювати **query endpoints** для отримання даних.

**Простий query:**

```javascript
getTodos: builder.query({
    query: () => 'todos',
})
```

Тут `query` - це функція, яка повертає URL (або об'єкт з конфігурацією). Цей query зробить GET запит до `/api/todos`.

**Query з параметрами:**

```javascript
getTodoById: builder.query({
    query: (id) => `todos/${id}`,
})
```

Параметр `id` передається при виклику: `useGetTodoByIdQuery(5)` → запит до `/api/todos/5`.

**Query з кількома параметрами:**

```javascript
getTodosByUser: builder.query({
    query: ({ userId, completed }) => ({
        url: 'todos',
        params: { userId, completed },
    }),
})
```

Тут ми повертаємо об'єкт замість рядка. `params` стануть query parameters:

-   `useGetTodosByUserQuery({ userId: 5, completed: true })`
-   Запит: `/api/todos?userId=5&completed=true`

**Query з custom headers:**

```javascript
getProtectedData: builder.query({
    query: () => ({
        url: 'protected',
        headers: {
            authorization: `Bearer ${getToken()}`,
        },
    }),
})
```

Можна додати свої заголовки, наприклад, токен авторизації. Хоча краще використовувати `prepareHeaders` в baseQuery для глобального додавання заголовків.

**Автоматично згенеровані hooks:**

RTK Query автоматично створює хуки на основі назв endpoints:

-   `getTodos` → `useGetTodosQuery`
-   `getTodoById` → `useGetTodoByIdQuery`
-   `getTodosByUser` → `useGetTodosByUserQuery`

Шаблон: `use[EndpointName][Query/Mutation]`

Ці хуки можна використовувати в компонентах:

```javascript
const { data, isLoading, error } = useGetTodosQuery()
```

**Термінологія:**

-   **Query parameters** - параметри запиту в URL після `?`
-   **Headers** - заголовки HTTP запиту
-   **Bearer token** - тип токену авторизації
-   **Auto-generated hooks** - автоматично згенеровані хуки
-   **Naming convention** - угода про іменування

---

## Слайд 64: RTK Query: Mutation Endpoints

**Що говорити:**
Тепер розглянемо **mutation endpoints** для зміни даних на сервері.

**POST - створення нового ресурсу:**

```javascript
addTodo: builder.mutation({
    query: (todo) => ({
        url: 'todos',
        method: 'POST',
        body: todo,
    }),
})
```

Тут ми створюємо новий todo. Параметр `todo` - це об'єкт, який буде відправлений в тілі запиту.

Використання:

```javascript
const [addTodo] = useAddTodoMutation()
await addTodo({ text: 'Нове завдання', completed: false })
```

**PUT - повне оновлення:**

```javascript
updateTodo: builder.mutation({
    query: ({ id, ...todo }) => ({
        url: `todos/${id}`,
        method: 'PUT',
        body: todo,
    }),
})
```

PUT замінює ресурс повністю. Використовуємо деструктуризацію: витягуємо `id` окремо, решту полів збираємо в `todo`.

**PATCH - часткове оновлення:**

```javascript
patchTodo: builder.mutation({
    query: ({ id, ...patch }) => ({
        url: `todos/${id}`,
        method: 'PATCH',
        body: patch,
    }),
})
```

PATCH оновлює тільки передані поля. Наприклад, можна змінити тільки `completed`:

```javascript
patchTodo({ id: 5, completed: true })
```

**DELETE - видалення:**

```javascript
deleteTodo: builder.mutation({
    query: (id) => ({
        url: `todos/${id}`,
        method: 'DELETE',
    }),
})
```

DELETE зазвичай приймає тільки id ресурсу.

**Різниця PUT vs PATCH:**

-   **PUT** - "замінити ресурс повністю". Треба передати всі поля.
-   **PATCH** - "оновити частково". Передаємо тільки ті поля, що змінюються.

**Автоматично згенеровані hooks:**

-   `addTodo` → `useAddTodoMutation`
-   `updateTodo` → `useUpdateTodoMutation`
-   `patchTodo` → `usePatchTodoMutation`
-   `deleteTodo` → `useDeleteTodoMutation`

Шаблон такий же: `use[EndpointName]Mutation`

**Термінологія:**

-   **POST** - HTTP метод для створення ресурсу
-   **PUT** - HTTP метод для повного оновлення
-   **PATCH** - HTTP метод для часткового оновлення
-   **DELETE** - HTTP метод для видалення
-   **Тіло запиту (body)** - дані, що відправляються на сервер
-   **Деструктуризація** - витягування значень з об'єкта
-   **Rest параметри (...)** - збір решти властивостей в об'єкт

---

## Слайд 65: RTK Query: Використання Query Hooks

**Що говорити:**
Тепер подивимося, як використовувати згенеровані query hooks в компонентах.

**Базове використання:**

```javascript
const { data: todos, isLoading, isSuccess, isError, error, refetch } = useGetTodosQuery()
```

Хук повертає об'єкт з багатьма корисними полями:

**data** - дані з сервера (undefined поки завантажується)
**isLoading** - true якщо це перший запит і дані ще завантажуються
**isFetching** - true якщо йде будь-який запит (включно з re-fetching)
**isSuccess** - true якщо запит успішний
**isError** - true якщо була помилка
**error** - об'єкт помилки
**refetch** - функція для ручного перезавантаження даних

**Query з параметрами:**

```javascript
const { data: todo } = useGetTodoByIdQuery(5)
```

Параметр передається прямо в хук. RTK Query відстежує зміни параметра - якщо він зміниться, зробить новий запит.

**Skip - пропустити запит:**

```javascript
const { data } = useGetTodosQuery(undefined, {
    skip: !isAuthenticated,
})
```

Якщо `skip: true`, запит не виконається. Корисно коли запит потрібен тільки за певної умови. Наприклад, завантажувати дані користувача тільки якщо він авторизований.

**Polling - автоматичне оновлення:**

```javascript
const { data } = useGetTodosQuery(undefined, {
    pollingInterval: 5000,
})
```

`pollingInterval: 5000` означає "оновлювати дані кожні 5 секунд". Корисно для даних, які часто змінюються - чат, дашборд тощо.

**Refetch on focus/reconnect:**

```javascript
const { data } = useGetTodosQuery(undefined, {
    refetchOnFocus: true,
    refetchOnReconnect: true,
})
```

**refetchOnFocus** - оновити дані коли користувач повертається на вкладку
**refetchOnReconnect** - оновити дані при відновленні інтернет-з'єднання

Це забезпечує актуальність даних!

**Ручне оновлення:**

```javascript
<button onClick={refetch}>Оновити</button>
```

Функція `refetch` дозволяє користувачу вручну оновити дані.

**Термінологія:**

-   **Refetch** - повторне завантаження даних
-   **Polling** - періодичне опитування, регулярне оновлення
-   **Focus** - фокус, коли вікно/вкладка активне
-   **Reconnect** - відновлення з'єднання після втрати
-   **Skip** - пропустити, не виконувати
-   **undefined** - коли query не приймає параметрів, передаємо undefined

---

## Слайд 66: RTK Query: Використання Mutation Hooks

**Що говорити:**
Mutation hooks працюють інакше ніж query hooks. Вони не виконуються автоматично, а повертають функцію trigger для ручного виклику.

**Базове використання:**

```javascript
const [addTodo, { isLoading, isSuccess, error }] = useAddTodoMutation()
```

Mutation hook повертає **масив з двох елементів:**

1. **Trigger функція** - функція для виклику mutation
2. **Об'єкт стану** - isLoading, isSuccess, isError, error, data

Це схоже на useState - також повертає масив!

**Виклик mutation:**

```javascript
const handleAdd = async () => {
    try {
        const newTodo = await addTodo({ text: 'Нове завдання' }).unwrap()
        console.log('Створено:', newTodo)
    } catch (err) {
        console.error('Помилка:', err)
    }
}
```

**unwrap()** - важливий метод! Trigger функція повертає promise, але не звичайний. Він НІКОЛИ не reject'иться. Замість цього результат в полях isSuccess/isError.

**unwrap()** перетворює цей promise на звичайний:

-   Якщо успішно - resolve з даними
-   Якщо помилка - reject з помилкою

Це дозволяє використовувати try/catch для обробки помилок.

**Кілька mutations в одному компоненті:**

```javascript
const [addTodo, { isLoading: isAdding }] = useAddTodoMutation()
const [updateTodo, { isLoading: isUpdating }] = useUpdateTodoMutation()
const [deleteTodo] = useDeleteTodoMutation()
```

Використовуємо деструктуризацію з перейменуванням `{ isLoading: isAdding }`, бо всі мають isLoading.

**Підтвердження перед видаленням:**

```javascript
const handleDelete = async (id) => {
    if (window.confirm('Видалити?')) {
        await deleteTodo(id).unwrap()
    }
}
```

Хороша практика - питати підтвердження перед деструктивними операціями.

**Відображення статусу:**

```javascript
{
    isSuccess && <div>✅ Успішно додано!</div>
}
{
    error && <div>❌ Помилка: {error.message}</div>
}
```

Можна показувати повідомлення про успіх або помилку на основі стану.

**Термінологія:**

-   **Trigger функція** - функція-тригер для запуску mutation
-   **unwrap()** - метод для перетворення RTK Query promise на звичайний
-   **resolve/reject** - успішне виконання / помилка promise
-   **try/catch** - конструкція для обробки помилок
-   **Деструктивна операція** - операція, яка незворотньо змінює/видаляє дані
-   **window.confirm()** - браузерне модальне вікно для підтвердження

---

## Слайд 67: RTK Query: Tags і Cache Invalidation

**Що говорити:**
Тепер найважливіша частина RTK Query - система тегів для управління кешем. Це те, що робить RTK Query по-справжньому потужним!

**Проблема:**
Уявіть: користувач дивиться список todos. Список закешований. Потім він додає новий todo через форму. Як оновити список? Можна викликати refetch вручну, але це незручно.

**Рішення: Tags**

Теги дозволяють автоматично інвалідувати (позначити застарілим) кеш коли дані змінюються.

**Визначення типів тегів:**

```javascript
tagTypes: ['Todo', 'User']
```

Це просто список рядків - назви типів сутностей.

**Query надає теги (providesTags):**

```javascript
getTodos: builder.query({
    query: () => 'todos',
    providesTags: ['Todo'],
})
```

Це означає: "Цей запит надає дані типу Todo". Тобто результат цього запиту - це Todo'шки.

**Специфічні теги:**

```javascript
getTodoById: builder.query({
    query: (id) => `todos/${id}`,
    providesTags: (result, error, id) => [{ type: 'Todo', id }],
})
```

Тут ми надаємо не просто 'Todo', а специфічний тег `{ type: 'Todo', id: 5 }`. Це дозволяє інвалідувати конкретний todo, а не всі.

`providesTags` може бути функцією, яка отримує:

-   **result** - дані з сервера
-   **error** - помилка (якщо була)
-   **id** - аргумент, переданий в query

**Mutation інвалідує теги (invalidatesTags):**

```javascript
addTodo: builder.mutation({
  query: (todo) => ({ ... }),
  invalidatesTags: ['Todo']
})
```

Після успішного виконання цієї mutation, RTK Query автоматично:

1. Знайде всі активні queries з тегом 'Todo'
2. Позначить їх кеш як застарілий
3. Якщо компонент з useGetTodosQuery() на екрані - перезавантажить дані

**Інвалідація конкретного ресурсу:**

```javascript
updateTodo: builder.mutation({
  query: ({ id, ...patch }) => ({ ... }),
  invalidatesTags: (result, error, { id }) => [{ type: 'Todo', id }]
})
```

Тут ми інвалідуємо тільки конкретний todo з цим id. getTodos також оновиться (бо має загальний тег 'Todo'), але getTodoById з іншим id - ні.

**Як це працює:**

1. Користувач відкриває список todos → `useGetTodosQuery()` → запит → кеш ['Todo']
2. Користувач натискає "Додати" → `addTodo()` → створення → invalidatesTags: ['Todo']
3. RTK Query бачить: "Todo інвалідовано" → автоматично перезавантажує useGetTodosQuery()
4. Список оновлюється автоматично!

Це магія! Не потрібно ніяких refetch, підписок, глобальних подій. Просто вказуєте зв'язки через теги.

**Термінологія:**

-   **Cache invalidation** - інвалідація кешу, позначення даних застарілими
-   **providesTags** - надає теги, вказує які дані повертає query
-   **invalidatesTags** - інвалідує теги, позначає які дані застаріли
-   **Active query** - активний запит, підписка на яку є у компоненті на екрані
-   **Tag** - мітка, тег для групування даних
-   **Type + id** - тип сутності + її унікальний ідентифікатор

---

## Слайд 68: RTK Query: Optimistic Updates

**Що говорити:**
Optimistic Updates - це просунута техніка для покращення user experience. Ідея: оновлюємо UI миттєво, не чекаючи відповіді сервера.

**Проблема:**
Користувач клікає checkbox "Виконано" біля todo. З звичайним підходом:

1. Відправляємо запит
2. Чекаємо відповідь (може 200-500мс)
3. Тільки тоді оновлюємо UI

Відчувається затримка, інтерфейс "лагає".

**Optimistic Update:**

1. Одразу оновлюємо UI (оптимістично припускаємо, що запит вдасться)
2. Відправляємо запит в фоні
3. Якщо запит успішний - все ОК
4. Якщо помилка - відкатуємо зміни назад

**Реалізація:**

```javascript
toggleTodo: builder.mutation({
  query: ({ id, completed }) => ({ ... }),

  async onQueryStarted({ id, completed }, { dispatch, queryFulfilled }) {
    // 1. Оптимістично оновлюємо кеш
    const patchResult = dispatch(
      api.util.updateQueryData('getTodos', undefined, (draft) => {
        const todo = draft.find(t => t.id === id);
        if (todo) {
          todo.completed = completed;
        }
      })
    );

    try {
      // 2. Чекаємо відповідь сервера
      await queryFulfilled;
      // Якщо ОК - нічого не робимо, зміни вже застосовані
    } catch {
      // 3. Якщо помилка - відкатуємо
      patchResult.undo();
    }
  }
})
```

**onQueryStarted** - lifecycle метод, який викликається коли mutation починається.

Параметри:

-   **arg** - аргумент, переданий в mutation ({ id, completed })
-   **{ dispatch, queryFulfilled }** - об'єкт з корисними методами

**api.util.updateQueryData** - метод для ручного оновлення кешу query.

Параметри:

-   **'getTodos'** - назва query для оновлення
-   **undefined** - аргументи цього query (наш getTodos без аргументів)
-   **(draft) => { ... }** - функція для модифікації даних (Immer draft)

Всередині функції ми можемо "мутувати" draft (завдяки Immer):

```javascript
const todo = draft.find((t) => t.id === id)
todo.completed = completed
```

**updateQueryData повертає patchResult** з методом **undo()** для відкату.

**queryFulfilled** - це promise, який resolve'иться коли запит завершиться успішно, або reject'иться при помилці.

**Результат:**
Користувач клікає checkbox → UI миттєво оновлюється → через 200мс приходить відповідь сервера → якщо ОК, все залишається як є → якщо помилка, checkbox повертається назад + показується помилка.

Інтерфейс відчувається блискавично швидким!

**Термінологія:**

-   **Optimistic Update** - оптимістичне оновлення, зміна UI до підтвердження сервером
-   **User Experience (UX)** - досвід користувача
-   **Lifecycle метод** - метод життєвого циклу, викликається на певних етапах
-   **onQueryStarted** - викликається коли mutation починається
-   **queryFulfilled** - promise що resolve'иться при успіху
-   **undo()** - відкотити зміни
-   **draft** - чернетка, об'єкт Immer для мутацій

---

## Слайд 69: RTK Query: Transforming Responses

**Що говорити:**
Іноді дані з сервера потребують обробки перед використанням. **transformResponse** дозволяє перетворювати дані перед збереженням в кеш.

**Приклад 1: Сортування**

```javascript
getTodos: builder.query({
    query: () => 'todos',
    transformResponse: (response) => {
        return response.sort((a, b) => b.id - a.id)
    },
})
```

Сервер повертає todos в невідомому порядку. Ми сортуємо за id в зворотньому порядку (нові першими).

**Важливо:** transformResponse викликається ОДИН РАЗ при отриманні даних, результат кешується. Не викликається при кожному рендері.

**Приклад 2: Додавання обчислених полів**

```javascript
getUser: builder.query({
    query: (id) => `users/${id}`,
    transformResponse: (response) => {
        return {
            ...response,
            fullName: `${response.firstName} ${response.lastName}`,
            avatar: response.avatar || '/default-avatar.png',
        }
    },
})
```

Сервер повертає firstName і lastName окремо. Ми додаємо fullName для зручності. Також додаємо дефолтний avatar якщо його немає.

Тепер в компоненті можна просто:

```javascript
<h1>{user.fullName}</h1>
<img src={user.avatar} />
```

**Приклад 3: Нормалізація даних**

```javascript
getPosts: builder.query({
    query: () => 'posts',
    transformResponse: (response) => {
        const byId = {}
        const allIds = []

        response.forEach((post) => {
            byId[post.id] = post
            allIds.push(post.id)
        })

        return { byId, allIds }
    },
})
```

Сервер повертає масив. Ми перетворюємо в нормалізовану структуру byId + allIds для швидкого доступу.

Використання:

```javascript
const { data } = useGetPostsQuery()
const post = data?.byId[postId] // O(1) доступ!
```

**Коли використовувати:**

-   Сортування/фільтрація даних
-   Перетворення формату дат
-   Додавання обчислених полів
-   Нормалізація структури
-   Видалення непотрібних полів

**Важливо:** transformResponse працює з оригінальними даними з сервера, ДО збереження в кеш. Не плутайте з селекторами (працюють з даними З кешу).

**Термінологія:**

-   **Transform** - перетворення, трансформація
-   **Response** - відповідь сервера
-   **Computed property** - обчислена властивість, створена на основі інших
-   **Default value** - значення за замовчуванням
-   **Нормалізація** - перетворення в плоску структуру
-   **Кешування** - збереження результату
-   **O(1)** - константна складність, миттєвий доступ

---

## Слайд 70: RTK Query: Error Handling

**Що говорити:**
Правильна обробка помилок критична для хорошого UX. RTK Query надає гнучкі способи роботи з помилками.

**prepareHeaders - глобальні налаштування:**

```javascript
baseQuery: fetchBaseQuery({
    baseUrl: '/api',
    prepareHeaders: (headers, { getState }) => {
        const token = getState().auth.token
        if (token) {
            headers.set('authorization', `Bearer ${token}`)
        }
        return headers
    },
})
```

**prepareHeaders** викликається перед КОЖНИМ запитом. Параметри:

-   **headers** - об'єкт Headers для модифікації
-   **{ getState, endpoint, type, ... }** - корисні методи

Тут ми додаємо токен авторизації до кожного запиту. Отримуємо його зі стану Redux через getState().

**transformErrorResponse - обробка помилок:**

```javascript
getProtectedData: builder.query({
    query: () => 'protected',
    transformErrorResponse: (response, meta, arg) => {
        if (response.status === 401) {
            return 'Не авторизовано'
        }
        if (response.status === 403) {
            return 'Доступ заборонено'
        }
        return response.data?.message || 'Невідома помилка'
    },
})
```

**transformErrorResponse** дозволяє перетворити помилку з сервера в зручний формат.

Параметри:

-   **response** - відповідь сервера (включно з status, data)
-   **meta** - метадані запиту
-   **arg** - аргументи, передані в query

Ми перевіряємо HTTP статус і повертаємо користувацьке повідомлення. Це зручніше ніж обробляти статуси в кожному компоненті.

**Використання в компоненті:**

```javascript
const { data, error, isError } = useGetProtectedDataQuery()

if (isError) {
    return <div className="error">{error}</div>
}
```

**error** тепер містить наш текст "Не авторизовано" замість складного об'єкта помилки.

**Глобальна обробка помилок:**

Можна створити custom baseQuery для глобальної обробки:

```javascript
const baseQueryWithReauth = async (args, api, extraOptions) => {
    let result = await fetchBaseQuery({ baseUrl: '/api' })(args, api, extraOptions)

    if (result.error && result.error.status === 401) {
        // Спробувати оновити токен
        const refreshResult = await fetchBaseQuery({ baseUrl: '/api' })(
            { url: '/auth/refresh', method: 'POST' },
            api,
            extraOptions,
        )

        if (refreshResult.data) {
            // Зберегти новий токен
            api.dispatch(setToken(refreshResult.data.token))
            // Повторити оригінальний запит
            result = await fetchBaseQuery({ baseUrl: '/api' })(args, api, extraOptions)
        } else {
            // Refresh не вдався - вийти з акаунта
            api.dispatch(logout())
        }
    }

    return result
}
```

Цей паттерн автоматично оновлює токен при 401 помилці.

**Термінологія:**

-   **prepareHeaders** - функція для налаштування заголовків перед запитом
-   **transformErrorResponse** - функція для перетворення помилки
-   **HTTP status** - код статусу HTTP (200, 401, 403, 404, 500 тощо)
-   **401 Unauthorized** - не авторизовано, потрібен login
-   **403 Forbidden** - доступ заборонений, навіть з авторизацією
-   **Token refresh** - оновлення токену авторизації
-   **Reauth** - повторна автентифікація

---

## Слайд 71: RTK Query: Conditional Fetching

**Що говорити:**
Іноді потрібно контролювати, коли саме виконувати запити. Conditional fetching дозволяє це робити.

**skip - пропустити запит:**

```javascript
const { data, isLoading } = useGetTodoByIdQuery(todoId, {
    skip: !isOpen,
})
```

Якщо `skip: true`, запит не виконається ВЗАГАЛІ. Не буде HTTP запиту, не буде isLoading.

Приклад: модальне вікно з деталями todo. Якщо модалка закрита (`isOpen: false`), навіщо завантажувати дані?

**skip автоматично відслідковується:** Якщо skip зміниться з true на false, запит автоматично виконається.

**Складні умови:**

```javascript
const shouldFetch = isAuthenticated && hasPermission && userId
const { data } = useGetProtectedDataQuery(undefined, {
    skip: !shouldFetch,
})
```

Завантажувати дані тільки якщо:

-   Користувач авторизований
-   Має права доступу
-   userId визначений

**useLazyQuery - ручне управління:**

Звичайні query хуки виконуються автоматично. Іноді потрібно повний ручний контроль - useLazy...Query:

```javascript
function ManualFetch() {
    const [trigger, result] = useLazyGetTodosQuery()

    return (
        <div>
            <button onClick={() => trigger()}>Завантажити дані</button>
            {result.isLoading && <Spinner />}
            {result.data && <TodoList todos={result.data} />}
        </div>
    )
}
```

**useLazy...Query** повертає масив:

1. **trigger** - функція для запуску запиту
2. **result** - об'єкт зі станом (isLoading, data, error, ...)

Запит НЕ виконається при монтуванні, тільки при виклику `trigger()`.

Можна викликати trigger кілька разів:

```javascript
<button onClick={() => trigger()}>Перезавантажити</button>
```

**Lazy queries з параметрами:**

```javascript
const [getTodoById, result] = useLazyGetTodoByIdQuery();

<button onClick={() => getTodoById(5)}>Завантажити todo 5</button>
<button onClick={() => getTodoById(10)}>Завантажити todo 10</button>
```

**Коли використовувати:**

-   **skip** - коли запит потрібен за умови (авторизація, права, стан UI)
-   **useLazy** - коли запит запускається користувачем (пошук, завантаження за кнопкою)

**Термінологія:**

-   **Conditional** - умовний, залежний від умови
-   **skip** - пропустити, не виконувати
-   **Lazy loading** - лінива завантаження, за запитом
-   **Trigger** - тригер, запуск
-   **Manual control** - ручне управління
-   **Auto-tracking** - автоматичне відстеження змін

---

## Слайд 72: RTK Query: Prefetching

**Що говорити:**
**Prefetching** - це техніка передзавантаження даних ДО того, як користувач їх запросив. Покращує сприйнятий performance.

**Prefetch при hover:**

```javascript
function TodoListItem({ todo }) {
    const dispatch = useDispatch()

    const handleMouseEnter = () => {
        dispatch(
            api.util.prefetch('getTodoById', todo.id, {
                force: false,
            }),
        )
    }

    return (
        <div onMouseEnter={handleMouseEnter}>
            <Link to={`/todos/${todo.id}`}>{todo.text}</Link>
        </div>
    )
}
```

Що тут відбувається:

1. Користувач наводить мишку на todo
2. Спрацьовує onMouseEnter
3. Ми dispatch'имо prefetch для getTodoById
4. Дані завантажуються в фон і кешуються
5. Коли користувач клікає на Link, дані вже є!

**force: false** означає "завантажувати тільки якщо немає в кеші". Якщо дані вже є - не робимо зайвий запит.

**api.util.prefetch** - метод для ручного prefetching.

Параметри:

-   **'getTodoById'** - назва endpoint
-   **todo.id** - аргументи для цього endpoint
-   **{ force, ifOlderThan }** - опції

**Prefetch при завантаженні додатка:**

```javascript
function App() {
    const dispatch = useDispatch()

    useEffect(() => {
        // Prefetch критичних даних
        dispatch(api.util.prefetch('getUser', 'me'))
        dispatch(api.util.prefetch('getSettings', undefined))
    }, [dispatch])

    return <Routes />
}
```

При завантаженні додатка одразу завантажуємо дані користувача і налаштування. Коли користувач перейде на сторінку Profile, дані вже будуть готові.

**ifOlderThan:**

```javascript
api.util.prefetch('getTodos', undefined, {
    ifOlderThan: 10, // секунди
})
```

Завантажувати тільки якщо дані старіші 10 секунд. Якщо свіжіші - використати кеш.

**Коли використовувати:**

-   Навігація - prefetch даних сторінки при hover на Link
-   Пагінація - prefetch наступної сторінки
-   Tabs - prefetch даних неактивних табів
-   Критичні дані - prefetch при завантаженні додатка

**Важливо:** Не зловживайте! Кожен prefetch - це запит до сервера. Prefetch'іть тільки те, що користувач ЙМОВІРНО запросить.

**Термінологія:**

-   **Prefetching** - передзавантаження, завантаження наперед
-   **Perceived performance** - сприйнятий performance, як швидко додаток відчувається
-   **Hover** - наведення миші
-   **Critical data** - критичні дані, необхідні одразу
-   **force** - примусово, ігнорувати кеш
-   **ifOlderThan** - якщо старіше ніж (вік кешу)

---

## Слайд 73: RTK Query: Підключення до Store

**Що говорити:**
Щоб RTK Query працював, потрібно правильно підключити його до Redux store.

**Додавання reducer:**

```javascript
reducer: {
  [api.reducerPath]: api.reducer,
  todos: todosReducer
}
```

**[api.reducerPath]** - це computed property name. api.reducerPath = 'api' (ми визначили в createApi).

Еквівалентно:

```javascript
reducer: {
  api: api.reducer,
  todos: todosReducer
}
```

Тепер в стані буде `state.api` з усіма даними RTK Query.

**Додавання middleware:**

```javascript
middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(api.middleware)
```

**getDefaultMiddleware()** повертає дефолтні middleware Redux Toolkit (thunk, immutability check, serialization check).

**.concat(api.middleware)** додає RTK Query middleware до них.

**Чому потрібен middleware?**

RTK Query middleware відповідає за:

1. **Кешування** - зберігає результати запитів
2. **Інвалідацію** - автоматично оновлює дані за тегами
3. **Polling** - періодичне оновлення
4. **Refetching** - оновлення при focus/reconnect
5. **Очищення кешу** - видаляє старі дані
6. **Deduplication** - об'єднує однакові запити

Без middleware RTK Query НЕ ПРАЦЮВАТИМЕ!

**Підключення Provider:**

```javascript
ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root'),
)
```

Це звичайний Provider з react-redux, нічого специфічного для RTK Query.

**Структура стану:**

```javascript
{
  api: {
    queries: {
      'getTodos(undefined)': { status: 'fulfilled', data: [...] },
      'getTodoById(5)': { status: 'fulfilled', data: {...} }
    },
    mutations: {
      'addTodo(42)': { status: 'fulfilled' }
    },
    subscriptions: { ... },
    config: { ... }
  },
  todos: { ... },
  user: { ... }
}
```

**api.queries** - кеш усіх query запитів
**api.mutations** - стан мутацій
**api.subscriptions** - активні підписки (компоненти, що використовують дані)

**Термінологія:**

-   **Computed property name** - обчислена назва властивості [key]
-   **middleware** - проміжне ПЗ
-   **getDefaultMiddleware** - отримати дефолтні middleware
-   **.concat()** - з'єднати, додати до масиву
-   **Provider** - компонент-постачальник для React Context
-   **Deduplication** - дедуплікація, усунення дублікатів

---

## Слайд 74: RTK Query: Повний приклад - Blog App

**Що говорити:**
Тепер подивимося на повний реалістичний приклад - блог додаток з постами, коментарями, CRUD операціями.

**Створення API slice:**

```javascript
export const blogApi = createApi({
  reducerPath: 'blogApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['Post', 'Comment'],
  endpoints: (builder) => ({ ... })
});
```

Зверніть увагу: використовуємо окремий reducerPath 'blogApi'. Це дозволяє мати кілька API slices в одному додатку.

Наприклад:

-   blogApi - для блогу
-   authApi - для автентифікації
-   analyticsApi - для аналітики

Теги ['Post', 'Comment'] для автоматичної інвалідації.

**Query endpoints:**

```javascript
getPosts: builder.query({
    query: () => 'posts',
    providesTags: ['Post'],
})
```

Завантажує всі пости, надає тег 'Post'.

```javascript
getPostById: builder.query({
    query: (id) => `posts/${id}`,
    providesTags: (result, error, id) => [{ type: 'Post', id }],
})
```

Завантажує конкретний пост, надає специфічний тег.

**Mutation endpoints:**

**createPost:**

```javascript
createPost: builder.mutation({
    query: (post) => ({
        url: 'posts',
        method: 'POST',
        body: post,
    }),
    invalidatesTags: ['Post'],
})
```

Після створення поста інвалідується тег 'Post' → getPosts автоматично перезавантажиться → новий пост з'явиться в списку.

**updatePost:**

```javascript
updatePost: builder.mutation({
    query: ({ id, ...patch }) => ({
        url: `posts/${id}`,
        method: 'PATCH',
        body: patch,
    }),
    invalidatesTags: (result, error, { id }) => [{ type: 'Post', id }],
})
```

Інвалідується тільки конкретний пост. Якщо відкрита сторінка цього поста - оновиться. Список постів теж оновиться (загальний тег 'Post').

**deletePost:**

```javascript
deletePost: builder.mutation({
    query: (id) => ({
        url: `posts/${id}`,
        method: 'DELETE',
    }),
    invalidatesTags: ['Post'],
})
```

Після видалення список оновлюється, видалений пост зникає.

**Експорт hooks:**

```javascript
export const {
    useGetPostsQuery,
    useGetPostByIdQuery,
    useCreatePostMutation,
    useUpdatePostMutation,
    useDeletePostMutation,
} = blogApi
```

Тепер ці хуки можна використовувати в компонентах!

**Термінологія:**

-   **Blog** - блог, платформа для публікацій
-   **CRUD** - Create, Read, Update, Delete
-   **reducerPath** - шлях reducer в store
-   **Multiple API slices** - кілька API slices
-   **Specific tag** - специфічний тег з id
-   **Automatic refetch** - автоматичне перезавантаження

---

## Слайд 75: RTK Query: Blog App - Components

**Що говорити:**
Тепер подивимося, як використовувати ці hooks в React компонентах.

**PostsList - список постів:**

```javascript
function PostsList() {
    const { data: posts, isLoading, isError, error } = useGetPostsQuery()

    if (isLoading) return <Spinner />
    if (isError) return <ErrorMessage error={error} />

    return (
        <div>
            <h1>Blog Posts</h1>
            {posts?.map((post) => (
                <PostCard key={post.id} post={post} />
            ))}
        </div>
    )
}
```

Дуже просто! Немає useEffect, немає useState для loading/error, немає ручного fetch. Все автоматично.

**Optional chaining (?.):**

```javascript
posts?.map(...)
```

Якщо posts ще undefined (завантажується), не буде помилки. Коли дані завантажаться, компонент автоматично перерендериться.

**PostEditor - форма створення/редагування:**

```javascript
function PostEditor({ post }) {
    const [createPost, { isLoading: isCreating }] = useCreatePostMutation()
    const [updatePost, { isLoading: isUpdating }] = useUpdatePostMutation()

    const [title, setTitle] = useState(post?.title || '')
    const [content, setContent] = useState(post?.content || '')

    const handleSubmit = async (e) => {
        e.preventDefault()

        try {
            if (post) {
                await updatePost({ id: post.id, title, content }).unwrap()
                toast.success('Пост оновлено!')
            } else {
                await createPost({ title, content }).unwrap()
                toast.success('Пост створено!')
            }
        } catch (err) {
            toast.error(`Помилка: ${err.message}`)
        }
    }

    const isLoading = isCreating || isUpdating

    return (
        <form onSubmit={handleSubmit}>
            <input value={title} onChange={(e) => setTitle(e.target.value)} required />
            <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
            <button type="submit" disabled={isLoading}>
                {isLoading ? 'Збереження...' : post ? 'Оновити' : 'Створити'}
            </button>
        </form>
    )
}
```

**Універсальна форма:** Якщо передано prop `post` - режим редагування, якщо ні - режим створення.

**Локальний стан для форми:** Використовуємо useState для title і content. Це нормально - не весь стан має бути в Redux! Поля форми - локальний UI стан.

**unwrap() + try/catch:** Для обробки помилок і показу toast повідомлень.

**isLoading комбіноване:** `isCreating || isUpdating` - кнопка disabled в обох випадках.

**Умовний текст кнопки:**

```javascript
{
    isLoading ? 'Збереження...' : post ? 'Оновити' : 'Створити'
}
```

Три варіанти: завантаження / редагування / створення.

**toast.success/error:** Використовуємо бібліотеку для toast повідомлень (наприклад, react-toastify). Не обов'язково, можна показувати по-іншому.

**Після успішної мутації:**
Не потрібно вручну оновлювати список постів! RTK Query автоматично інвалідує тег 'Post', і PostsList оновиться.

**Термінологія:**

-   **Optional chaining (?.)** - безпечний доступ до властивостей
-   **Spinner** - індикатор завантаження (крутилка)
-   **ErrorMessage** - компонент для показу помилки
-   **PostCard** - компонент картки поста
-   **Toast** - спливаюче повідомлення
-   **e.preventDefault()** - запобігти стандартній дії форми
-   **required** - HTML атрибут, поле обов'язкове

---

## Слайд 76: RTK Query vs createAsyncThunk

**Що говорити:**
Тепер важливе питання: коли використовувати RTK Query, а коли createAsyncThunk?

**Використовуйте RTK Query коли:**

✅ **CRUD операції з REST API**
Якщо ваш backend - звичайний REST API з GET/POST/PUT/DELETE, RTK Query ідеально підходить.

✅ **Потрібне автоматичне кешування**
RTK Query автоматично кешує результати. Якщо три компоненти запитують ті самі дані, запит буде один.

✅ **Множинні запити до однієї API**
Якщо у вас 20+ endpoints, RTK Query значно скоротить код порівняно з 20 async thunks.

✅ **Потрібен automatic re-fetching**
Дані застарівають, потрібно періодично оновлювати. RTK Query це вміє з коробки.

✅ **Polling або prefetching**
RTK Query має вбудовані рішення для цього.

**Використовуйте createAsyncThunk коли:**

✅ **Складна бізнес-логіка**
Якщо перед/після запиту потрібно виконати складні обчислення, валідацію, трансформації - thunk дає повний контроль.

✅ **Не REST API**
WebSocket, GraphQL, Firebase - це не REST. RTK Query оптимізований саме для REST.

Хоча можна написати custom baseQuery для будь-чого, але це складно.

✅ **Потрібен повний контроль над станом**
З thunk ви самі керуєте структурою стану, логікою reducers.

✅ **Один-два запити**
Якщо у вас один login endpoint, можливо RTK Query - overkill. Простий thunk буде достатньо.

✅ **Специфічна обробка помилок**
Якщо кожен endpoint має унікальну логіку обробки помилок, складні retry стратегії - thunk гнучкіший.

**Можна комбінувати!**

RTK Query і createAsyncThunk можна використовувати разом:

```javascript
// RTK Query для API
const { data: user } = useGetUserQuery(userId)

// createAsyncThunk для бізнес-логіки
const dispatch = useDispatch()
dispatch(processComplexWorkflow(user))
```

**Рекомендація:** Починайте з RTK Query для API запитів. Якщо з якимось endpoint виникають складнощі - використайте thunk для нього.

**Термінологія:**

-   **REST API** - архітектурний стиль для API (GET /users, POST /users тощо)
-   **CRUD** - Create, Read, Update, Delete
-   **WebSocket** - протокол двостороннього зв'язку
-   **GraphQL** - мова запитів для API
-   **Overkill** - надлишковий, занадто складний для задачі
-   **Retry strategy** - стратегія повторних спроб при помилках

---

_Цей файл містить детальні нотатки для озвучування презентації з поясненням всієї термінології та концепцій Redux і RTK Query._
