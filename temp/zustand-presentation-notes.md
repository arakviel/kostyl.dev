# Нотатки до презентації: State Management в React додатках. Zustand

Детальні пояснення для кожного слайду з термінологією та прикладами.

---

## Слайд 1: Титульний

**Що говорити:**
Вітаю всіх! Сьогодні ми з вами розглянемо Zustand - надзвичайно простий і елегантний інструмент для управління станом у React додатках. Якщо ви працювали з Redux і думали "це занадто складно для мого додатку" - Zustand саме для вас! Це мінімалістична бібліотека, яка надає все необхідне без зайвого коду.

**Ключові моменти:**

-   Zustand перекладається з німецької як "стан" - дуже символічна назва
-   Це одна з найлегших бібліотек для state management - менше 1KB!
-   Незважаючи на простоту, вона дуже потужна і підходить навіть для великих проектів
-   Ми побачимо, наскільки простіше може бути code порівняно з Redux

**Термінологія:**

-   **Zustand** - німецьке слово, що означає "стан"
-   **State Management** - управління станом додатку
-   **Мінімалістична** - максимально проста, без зайвих функцій

---

## Слайд 2: План презентації

**Що говорити:**
Давайте подивимося на структуру презентації. Ми почнемо з того, що таке Zustand і чому він може бути кращим вибором ніж Redux для багатьох проектів. Потім детально розглянемо основні концепції - як створювати store, як працювати з асинхронними операціями. Після цього вивчимо більш просунуті теми - middleware, DevTools, persist. І завершимо реальними прикладами та найкращими практиками.

**Структура:**

-   Основи - що таке Zustand, порівняння з Redux
-   Core API - create, set, get
-   Async операції - як працювати з API запитами
-   Розширені можливості - middleware, DevTools, persist
-   Практика - реальні приклади додатків
-   Best practices - як писати якісний код

**Особливість Zustand:** На відміну від Redux, тут немає concepts як actions, reducers, dispatch - все набагато простіше!

---

## Слайд 3: Що таке Zustand?

**Що говорити:**
Zustand - це бібліотека для управління станом, створена командою Poimandres (раніше відомі як React Spring team). Вони створили багато популярних бібліотек для React екосистеми.

**Ключові особливості:**

**Легка** - менше 1KB у стисненому вигляді (gzipped). Для порівняння: Redux з React-Redux та Redux Toolkit - це близько 13KB. Це означає швидше завантаження додатку і менший bundle size.

**Проста** - мінімальне API. Вам потрібно вивчити буквально одну функцію `create()` щоб почати працювати. Немає actions, reducers, dispatch, providers - просто пишете звичайний JavaScript код.

**Швидка** - не використовує React Context, тому немає проблеми з надмірними rerenders. Компоненти оновлюються тільки коли змінюються дані, які вони використовують.

**Гнучка** - не нав'язує жодної архітектури. Можете організувати код як вам зручно - один великий store, багато маленьких stores, чи комбінацію.

**Без залежностей** - не потребує Context Provider, не залежить від React Context API. Це робить її легкою для інтеграції в існуючі проекти.

**Хуки** - природна інтеграція з React через hooks. Якщо ви знаєте useState, useEffect - ви легко зрозумієте Zustand.

**Історія:**
Zustand створена у 2019 році. Вона швидко набула популярності завдяки своїй простоті. Багато developers, які були втомлені від складності Redux, перейшли на Zustand.

**Термінологія:**

-   **Bundle size** - розмір JavaScript файлів, які завантажує браузер
-   **Gzipped** - стиснутий алгоритмом gzip
-   **API** - набір функцій для роботи з бібліотекою
-   **Boilerplate** - повторюваний шаблонний код
-   **React Context** - механізм React для передачі даних через дерево компонентів

---

## Слайд 4: Чому Zustand?

**Що говорити:**
Розглянемо конкретні переваги Zustand більш детально.

**Простота:**

Немає boilerplate коду. У Redux ви створюєте константи для action types, action creators, reducers. У Zustand ви просто пишете функції:

```javascript
// Redux RTK
const counterSlice = createSlice({
    name: 'counter',
    initialState: { value: 0 },
    reducers: {
        increment: (state) => {
            state.value += 1
        },
    },
})

// Zustand
const useStore = create((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
}))
```

Код виглядає більш природньо, менше магії, простіше читати.

**Продуктивність:**

Zustand не використовує Context API, тому немає проблеми Context rerenders. У Redux з Context, коли стан змінюється, всі компоненти під Provider можуть ререндеритись. Zustand оптимізує це автоматично - компонент ререндериться тільки якщо змінюються дані, які він використовує.

**Гнучкість:**

Можна використовувати Zustand навіть поза React компонентами! Наприклад, в utility функціях, в event handlers поза компонентами. Це дуже зручно для деяких сценаріїв.

Легко інтегрується з існуючим кодом - не потрібно обгортати весь додаток в Provider, можна поступово додавати Zustand до окремих частин.

**Термінологія:**

-   **Rerender** - повторний рендеринг компонента
-   **Context rerenders** - проблема, коли багато компонентів ререндеряться через зміну Context
-   **Utility функції** - допоміжні функції, які не є компонентами
-   **Provider** - компонент, який надає доступ до даних дочірнім компонентам

---

## Слайд 5: Порівняння з Redux

**Що говорити:**
Давайте порівняємо Zustand з Redux по ключових характеристиках.

**Розмір:**
Redux з усіма залежностями - близько 3KB (тільки сам Redux), але з React-Redux та Redux Toolkit виходить ~13KB. Zustand - всього 1KB. Це дуже важливо для продуктивності, особливо на мобільних пристроях з повільним інтернетом.

**Boilerplate:**
Redux вимагає створення actions, action types, reducers, store configuration. Zustand - просто створюєте store з функцією create(). Різниця - десятки рядків коду проти кількох.

**Provider:**
Redux вимагає обгортати додаток в `<Provider store={store}>`. Zustand не потребує Provider взагалі - просто імпортуйте hook і використовуйте.

**Actions і Reducers:**
У Redux вони обов'язкові - структура, яку потрібно дотримуватись. У Zustand це опціонально - можете створити схожу структуру якщо хочете, але не обов'язково.

**DevTools:**
Обидві бібліотеки підтримують Redux DevTools для debugging. У Redux це вбудовано, у Zustand додається через middleware.

**Async:**
Redux вимагає додаткових інструментів - Redux Thunk або Redux Saga. У Zustand просто пишете async функції - працює нативно.

**Learning Curve:**
Redux має круту криву навчання - багато концепцій, принципи, best practices. Zustand можна вивчити за годину.

**Ecosystem:**
Redux має величезну екосистему - RTK Query, Redux Saga, Redux Observable, безліч middleware. Zustand має меншу, але зростаючу екосистему.

**Для яких проектів:**
Redux - може бути overkill для малих додатків, але відмінний для великих корпоративних проектів з великою командою.
Zustand - ідеальний для малих і середніх проектів, але також добре працює на великих.

**Висновок:**
Якщо ви не впевнені що вам потрібна вся потужність Redux - почніть з Zustand. Завжди можете перейти на Redux якщо проект виросте.

**Термінологія:**

-   **Learning curve** - крива навчання, наскільки складно вивчити
-   **Overkill** - занадто складне рішення для простої задачі
-   **Ecosystem** - екосистема, набір інструментів навколо бібліотеки
-   **Native** - вбудована підтримка, без додаткових інструментів

---

## Слайд 6: Встановлення

**Що говорити:**
Встановлення Zustand надзвичайно просте - одна команда і все готово.

```bash
npm install zustand
```

Після встановлення не потрібно:

-   Налаштовувати store
-   Створювати Provider
-   Підключати middleware
-   Налаштовувати DevTools

Все працює out of the box! Просто імпортуйте `create` і починайте використовувати.

Zustand не має peer dependencies (залежностей, які повинні бути встановлені окремо). Це контрастує з Redux, де потрібно встановлювати react-redux окремо.

**Розмір:**
Після встановлення ваш bundle збільшиться всього на ~1KB. Для порівняння - додавання будь-якої іконки з react-icons може бути більше!

**Сумісність:**
Zustand працює з:

-   React 16.8+ (будь-яка версія з hooks)
-   React Native
-   Next.js (включаючи SSR)
-   Preact
-   Навіть Vanilla JavaScript (без React)

**Термінологія:**

-   **Peer dependencies** - залежності, які мають бути встановлені окремо
-   **Out of the box** - працює одразу, без налаштувань
-   **SSR** - Server-Side Rendering, рендеринг на сервері
-   **Vanilla JavaScript** - чистий JavaScript без фреймворків

---

## Слайд 7: Базовий приклад: Counter

**Що говорити:**
Розглянемо найпростіший можливий приклад - Counter. Це класичний приклад для демонстрації state management.

**Створення store:**

```javascript
const useCounterStore = create((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
    reset: () => set({ count: 0 }),
}))
```

Розберемо що тут відбувається:

**create()** - єдина функція, яка потрібна для створення store. Вона приймає функцію, яка отримує `set` як аргумент.

**set** - функція для оновлення стану. Вона може приймати об'єкт або функцію.

**Стан і actions в одному місці:** `count: 0` - це стан, `increment`, `decrement`, `reset` - це actions (функції для зміни стану).

**Використання в компоненті:**

```javascript
const count = useCounterStore((state) => state.count)
const increment = useCounterStore((state) => state.increment)
```

Це selector функції - ви вибираєте тільки те, що потрібно компоненту. Компонент підпишеться тільки на count і increment, якщо щось інше в store зміниться - компонент не ререндериться.

**Порівняння з useState:**
Якби це було локальним станом:

```javascript
const [count, setCount] = useState(0)
```

Але з Zustand цей стан доступний БУДЬ-ЯКОМУ компоненту в додатку без передачі props!

**Важливо:**
Зверніть увагу, що `useCounterStore` - це хук. Назва починається з `use` як всі React hooks. Його можна викликати тільки в React компонентах або кастомних хуках.

**Термінологія:**

-   **create** - функція для створення store
-   **set** - функція для оновлення стану
-   **selector** - функція для вибору даних зі store
-   **hook** - спеціальна функція React, яка починається з `use`

---

## Слайд 8: Створення Store

**Що говорити:**
Розглянемо детальніше, як працює функція `create()` і які параметри вона надає.

**create()** приймає функцію, яка отримує два аргументи:

**set** - функція для оновлення стану
**get** - функція для читання поточного стану

Подивіться на приклад:

```javascript
const useStore = create((set, get) => ({
    bears: 0,
    fish: 0,

    addBear: () => set((state) => ({ bears: state.bears + 1 })),
    removeAllBears: () => set({ bears: 0 }),

    eatFish: () => {
        const currentFish = get().fish
        if (currentFish > 0) {
            set({ fish: currentFish - 1 })
        }
    },
}))
```

**set()** має два способи використання:

1. **З функцією:** `set((state) => ({ bears: state.bears + 1 }))`

    - Використовуйте коли потрібно обчислити новий стан на основі попереднього
    - state - це поточний стан
    - Повертаєте об'єкт з полями, які хочете змінити

2. **З об'єктом:** `set({ bears: 0 })`
    - Використовуйте коли новий стан не залежить від попереднього
    - Просто передаєте об'єкт з новими значеннями

**get()** використовується коли потрібно прочитати поточний стан всередині action:

```javascript
eatFish: () => {
    const currentFish = get().fish // Читаємо поточне значення
    if (currentFish > 0) {
        set({ fish: currentFish - 1 })
    }
}
```

Це корисно для умовної логіки або коли потрібно використати кілька полів стану.

**Важливо:**

-   `set()` робить shallow merge - об'єднує новий стан зі старим
-   Не потрібно повертати весь стан, тільки поля, які змінюються
-   `get()` завжди повертає актуальний стан на момент виклику

**Термінологія:**

-   **Shallow merge** - поверхневе об'єднання, змішує тільки верхній рівень об'єкта
-   **Conditional logic** - умовна логіка (if/else)
-   **Current state** - поточний стан на момент виклику

---

## Слайд 9: set() функція

**Що говорити:**
Давайте детальніше розглянемо функцію `set()`, бо це ключова функція для оновлення стану.

**1. Об'єкт (merge):**

```javascript
set({ count: 5 })
```

Це найпростіший спосіб. Ви передаєте об'єкт з полями, які хочете змінити. Zustand автоматично об'єднає їх зі існуючим станом. Наприклад, якщо у вас був стан `{ count: 0, user: 'John' }`, після `set({ count: 5 })` стан буде `{ count: 5, user: 'John' }`. Поле user залишилось без змін!

**2. Функція (на основі попереднього стану):**

```javascript
set((state) => ({ count: state.count + 1 }))
```

Використовуйте цей спосіб коли новий стан залежить від попереднього. Це важливо для асинхронних операцій! Якщо два оновлення відбудуться швидко одне за одним, функціональний підхід гарантує, що обидва використають актуальний стан.

**Приклад проблеми без функції:**

```javascript
// ❌ Може бути race condition
increment: () => {
    const current = get().count;
    setTimeout(() => {
        set({ count: current + 1 }); // current може бути застарілим!
    }, 1000);
}

// ✅ Завжди безпечно
increment: () => {
    setTimeout(() => {
        set((state) => ({ count: state.count + 1 })); // state завжди актуальний
    }, 1000);
}
```

**3. Replace mode:**

```javascript
set({ count: 5 }, true) // true = replace замість merge
```

Другий параметр - булеве значення. Якщо true, новий стан ПОВНІСТЮ заміняє старий, а не об'єднується. Використовується рідко, здебільшого для скидання стану.

**Приклад:**

```javascript
// Стан: { count: 5, user: 'John', theme: 'dark' }
set({ count: 0 }) // Результат: { count: 0, user: 'John', theme: 'dark' }
set({ count: 0 }, true) // Результат: { count: 0 } - все інше видалено!
```

**Shallow merge:**
За замовчуванням set() робить shallow merge - об'єднує тільки верхній рівень. Для вкладених об'єктів потрібно бути обережним:

```javascript
// Стан: { user: { name: 'John', age: 25 } }
set({ user: { name: 'Jane' } }) // user стане { name: 'Jane' } - age зникне!

// Правильно:
set((state) => ({
    user: { ...state.user, name: 'Jane' },
}))
```

**Термінологія:**

-   **Race condition** - ситуація, коли результат залежить від порядку виконання операцій
-   **Replace** - заміна, повна зміна стану
-   **Merge** - об'єднання, змішування нового і старого
-   **Shallow** - поверхневий, тільки перший рівень
-   **Deep** - глибокий, всі рівні вкладеності

---

## Слайд 10: Використання в компонентах

**Що говорити:**
Тепер розглянемо як правильно використовувати store в React компонентах. Це критично важливо для продуктивності!

**❌ Погано: підписка на весь store:**

```javascript
function UserProfile() {
    const store = useStore() // Підписка на ВСЕ!
    return <div>{store.user.name}</div>
}
```

Проблема: компонент підпишеться на весь store і буде ререндеритись при БУДЬ-ЯКІЙ зміні стану, навіть якщо змінюються поля, які він не використовує. Якщо в store є 100 полів і змінюється одне - компонент все одно ререндериться.

**✅ Добре: підписка тільки на user:**

```javascript
function UserProfile() {
    const user = useStore((state) => state.user)
    return <div>{user.name}</div>
}
```

Тепер компонент ререндериться тільки коли змінюється поле `user`. Якщо змінюється `todos` або інше поле - компонент не ререндериться.

**✅ Ще краще: підписка на конкретне поле:**

```javascript
function UserName() {
    const name = useStore((state) => state.user.name)
    return <div>{name}</div>
}
```

Компонент ререндериться тільки коли змінюється `user.name`. Навіть якщо змінюється `user.age` - компонент не ререндериться!

**Як це працює:**
Zustand порівнює результат selector функції з попереднім результатом за допомогою strict equality (===). Якщо результат той самий - ререндера немає.

**Приклад з кількома полями:**

```javascript
function TodoCounter() {
    // Витягуємо тільки довжину масиву, не сам масив
    const count = useStore((state) => state.todos.length)
    return <div>Всього todos: {count}</div>
}
```

Цей компонент ререндериться тільки коли змінюється кількість todos, а не при кожній зміні todo (наприклад, toggle completed).

**Принцип оптимізації:**
"Підписуйтесь тільки на те, що використовуєте!" - це золоте правило для продуктивності.

**Термінологія:**

-   **Підписка (subscription)** - слухання змін стану
-   **Rerender** - повторний рендеринг компонента
-   **Selector function** - функція для вибору даних
-   **Strict equality (===)** - строге порівняння за посиланням
-   **Performance** - продуктивність

---

## Слайд 11: Вибір кількох полів

**Що говорити:**
Що робити, якщо компоненту потрібно кілька полів зі store? Є кілька підходів, і не всі вони однаково ефективні.

**❌ Погано: повертає новий об'єкт кожного разу:**

```javascript
const { count, user } = useStore((state) => ({
    count: state.count,
    user: state.user,
}))
```

Проблема: selector функція створює НОВИЙ об'єкт при кожному виклику. Zustand порівнює об'єкти за посиланням (===), а нові об'єкти ніколи не рівні:

```javascript
{ count: 5, user: 'John' } === { count: 5, user: 'John' } // false!
```

Результат: компонент ререндериться при кожній зміні store, навіть якщо count і user не змінилися!

**✅ Добре: окремі селектори:**

```javascript
const count = useStore((state) => state.count)
const user = useStore((state) => state.user)
```

Це найпростіше рішення. Кожен селектор підписується на своє поле. Компонент ререндериться тільки якщо count ЧИ user змінюється.

**✅ Добре: shallow порівняння:**

```javascript
import { shallow } from 'zustand/shallow'

const { count, user } = useStore(
    (state) => ({ count: state.count, user: state.user }),
    shallow, // Порівнює ПОЛЯ об'єкта, а не посилання
)
```

`shallow` - це функція порівняння, яка перевіряє чи змінились поля об'єкта, а не посилання на об'єкт. Якщо count і user ті самі - ререндера не буде.

**✅ Добре: useShallow hook (Zustand 4.5+):**

```javascript
import { useShallow } from 'zustand/react/shallow'

const { count, user } = useStore(useShallow((state) => ({ count: state.count, user: state.user })))
```

Це новіший спосіб з версії 4.5. useShallow - це хук-обгортка для shallow порівняння. Синтаксис трохи чистіший.

**Як працює shallow:**

```javascript
// Без shallow
{ count: 5, user: 'John' } === { count: 5, user: 'John' } // false (різні посилання)

// З shallow
shallow(
  { count: 5, user: 'John' },
  { count: 5, user: 'John' }
) // true (поля однакові)
```

**Коли що використовувати:**

-   **1-2 поля:** окремі селектори (найпростіше)
-   **3+ полів:** useShallow або shallow
-   **Складні обчислення:** винесіть в окремий selector поза компонентом

**Термінологія:**

-   **Reference** - посилання, адреса об'єкта в пам'яті
-   **Shallow comparison** - поверхневе порівняння, перевіряє тільки верхній рівень
-   **Deep comparison** - глибоке порівняння, перевіряє всі рівні вкладеності
-   **Equality function** - функція порівняння

---

## Слайд 12: Actions: Оновлення стану

**Що говорити:**
Розглянемо типові операції зі станом на прикладі todo списку.

**Додавання до масиву:**

```javascript
addTodo: (text) =>
    set((state) => ({
        todos: [...state.todos, { id: Date.now(), text, completed: false }],
    }))
```

Створюємо НОВИЙ масив: беремо всі старі todos (`...state.todos`) і додаємо новий todo в кінець. Це іммутабельне оновлення - ми не змінюємо старий масив, а створюємо новий.

**Оновлення елемента в масиві:**

```javascript
toggleTodo: (id) =>
    set((state) => ({
        todos: state.todos.map((todo) => (todo.id === id ? { ...todo, completed: !todo.completed } : todo)),
    }))
```

Використовуємо `map` для створення нового масиву. Для кожного todo:

-   Якщо id співпадає - створюємо новий об'єкт з перемкнутим completed
-   Якщо ні - повертаємо старий todo без змін

**Видалення з масиву:**

```javascript
deleteTodo: (id) =>
    set((state) => ({
        todos: state.todos.filter((todo) => todo.id !== id),
    }))
```

`filter` створює новий масив, що містить тільки todos з id відмінним від того, що ми видаляємо.

**Очищення:**

```javascript
clearTodos: () => set({ todos: [] })
```

Найпростіший варіант - встановлюємо порожній масив. Оскільки не потрібен попередній стан, передаємо об'єкт напряму.

**Важливість іммутабельності:**

```javascript
// ❌ НЕПРАВИЛЬНО - мутація!
addTodo: (text) => set((state) => {
    state.todos.push({ text }); // Змінюємо масив!
    return { todos: state.todos };
})

// ✅ ПРАВИЛЬНО - іммутабельність
addTodo: (text) => set((state) => ({
    todos: [...state.todos, { text }] // Новий масив
}))
```

Чому це важливо? Zustand порівнює посилання для оптимізації. Якщо ви мутуєте масив, посилання залишається тим самим, і Zustand може не помітити зміни!

**Альтернатива - Immer:**
Якщо іммутабельні оновлення здаються складними, використовуйте Immer middleware - він дозволяє писати код який виглядає як мутація, але насправді створює іммутабельні копії.

**Термінологія:**

-   **Іммутабельність (Immutability)** - незмінність, створення нових об'єктів замість зміни існуючих
-   **Мутація (Mutation)** - зміна існуючого об'єкта/масиву
-   **Spread оператор (...)** - розгортання, копіювання елементів
-   **map** - метод масиву, створює новий масив застосовуючи функцію до кожного елемента
-   **filter** - метод масиву, створює новий масив з елементами, що пройшли перевірку

---

## Слайд 13: get() - Читання поточного стану

**Що говорити:**
Функція `get()` використовується для читання стану всередині actions. Розглянемо практичні приклади.

**Базове використання:**

```javascript
getTotal: () => {
    const { count, multiplier } = get();
    return count * multiplier;
}
```

Ця функція не змінює стан, а тільки читає і обчислює значення на основі кількох полів стану.

**Action на основі поточного стану:**

```javascript
doubleCount: () => {
    const currentCount = get().count;
    set({ count: currentCount * 2 });
}
```

Тут ми читаємо поточне значення, виконуємо обчислення, і встановлюємо новий стан.

**Умовна логіка:**

```javascript
incrementIfLessThan10: () => {
    const current = get().count;
    if (current < 10) {
        set({ count: current + 1 });
    }
}
```

Дуже корисно для валідації або умовних оновлень. Оновлюємо стан тільки якщо виконується умова.

**Комбінування даних:**

```javascript
addWithBonus: () => {
    const { count, multiplier } = get();
    set({ count: count + multiplier });
}
```

Коли потрібно використати кілька полів стану для обчислення нового значення.

**get() vs set з функцією:**

```javascript
// З get()
increment: () => {
    const current = get().count;
    set({ count: current + 1 });
}

// Без get(), через set з функцією
increment: () => {
    set((state) => ({ count: state.count + 1 }));
}
```

Обидва підходи працюють, але другий більш іціоматичний для Zustand і безпечніший для async операцій.

**Коли використовувати get():**

-   Коли потрібно прочитати стан, але не змінювати його
-   Для складної логіки з кількома if/else
-   Для обчислень на основі кількох полів
-   У функціях, які повертають значення (не actions)

**Коли НЕ використовувати get():**

-   Для простих оновлень - краще `set((state) => ...)`
-   В async функціях між await - стан може змінитися
-   Якщо можна використати state parameter в set()

**Термінологія:**

-   **Conditional logic** - умовна логіка
-   **Validation** - перевірка, валідація даних
-   **Idiomatic** - ідіоматичний, типовий для даної бібліотеки
-   **Async-safe** - безпечний для асинхронного коду

---

## Слайд 14: Async Actions

**Що говорити:**
Одна з найбільших переваг Zustand - async операції працюють нативно, без додаткових інструментів!

У Redux вам потрібен Redux Thunk або Redux Saga. У Zustand просто пишете async функції як звичайно.

**Базовий приклад завантаження даних:**

```javascript
fetchUsers: async () => {
    set({ loading: true, error: null });

    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        set({ users, loading: false });
    } catch (error) {
        set({ error: error.message, loading: false });
    }
}
```

Розберемо покроково:

1. **Встановлюємо loading: true** - щоб показати spinner в UI
2. **Очищаємо попередню помилку** - error: null
3. **Робимо запит** - await fetch(...)
4. **При успіху** - зберігаємо дані і встановлюємо loading: false
5. **При помилці** - зберігаємо повідомлення про помилку і встановлюємо loading: false

**Створення даних:**

```javascript
createUser: async (userData) => {
    set({ loading: true });

    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        const newUser = await response.json();

        set((state) => ({
            users: [...state.users, newUser],
            loading: false
        }));
    } catch (error) {
        set({ error: error.message, loading: false });
    }
}
```

Зверніть увагу: ми використовуємо `set((state) => ...)` щоб додати нового користувача до існуючого масиву. Це важливо - не можна просто `set({ users: [newUser] })`, бо це замінить весь масив!

**Типова структура стану для async операцій:**

```javascript
{
    data: null,      // Дані з сервера
    loading: false,  // Чи виконується запит
    error: null      // Повідомлення про помилку
}
```

Цей паттерн повторюється в більшості async операцій.

**Переваги перед Redux:**

```javascript
// Redux Thunk
const fetchUsers = () => async (dispatch) => {
    dispatch({ type: 'FETCH_USERS_REQUEST' });
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        dispatch({ type: 'FETCH_USERS_SUCCESS', payload: users });
    } catch (error) {
        dispatch({ type: 'FETCH_USERS_FAILURE', payload: error.message });
    }
};

// Zustand
const fetchUsers = async () => {
    set({ loading: true });
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        set({ users, loading: false });
    } catch (error) {
        set({ error: error.message, loading: false });
    }
};
```

Код Zustand коротший, читабельніший, і не потрібні додаткові інструменти!

**Термінологія:**

-   **Native** - вбудована підтримка, без додаткових інструментів
-   **Async/await** - синтаксис для роботи з асинхронним кодом
-   **try/catch** - обробка помилок
-   **fetch** - API для HTTP запитів
-   **Spinner** - індикатор завантаження
-   **Pattern** - паттерн, повторюваний підхід

---

## Слайд 15: Async: Використання в компонентах

**Що говорити:**
Тепер подивимося як використовувати async actions в React компонентах.

**Компонент списку:**

```javascript
function UserList() {
    const { users, loading, error, fetchUsers } = useStore()

    useEffect(() => {
        fetchUsers()
    }, [fetchUsers])

    if (loading) return <Spinner />
    if (error) return <ErrorMessage error={error} />

    return (
        <ul>
            {users.map((user) => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    )
}
```

Розберемо компонент:

**1. Витягуємо дані і функції:**

```javascript
const { users, loading, error, fetchUsers } = useStore()
```

Використовуємо деструктуризацію для витягування всього, що потрібно. Якщо витягуєте кілька полів - не забудьте про shallow!

**2. Завантаження при монтуванні:**

```javascript
useEffect(() => {
    fetchUsers()
}, [fetchUsers])
```

useEffect з fetchUsers в dependencies виконається один раз при монтуванні (якщо fetchUsers не міняється, а в Zustand функції стабільні).

**3. Обробка різних станів:**

```javascript
if (loading) return <Spinner />
if (error) return <ErrorMessage error={error} />
```

Early returns для різних станів. Це зручний паттерн - код далі виконується тільки якщо дані завантажені успішно.

**Компонент форми:**

```javascript
function CreateUserForm() {
    const createUser = useStore((state) => state.createUser)
    const [name, setName] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        await createUser({ name })
        setName('')
    }

    return (
        <form onSubmit={handleSubmit}>
            <input value={name} onChange={(e) => setName(e.target.value)} />
            <button type="submit">Додати</button>
        </form>
    )
}
```

**Важливі моменти:**

1. **await createUser()** - чекаємо завершення запиту перед очищенням форми
2. **Локальний стан** - name зберігається локально в useState, не в Zustand. Це правильно - не весь стан має бути глобальним!
3. **e.preventDefault()** - запобігаємо перезавантаженню сторінки

**Обробка loading в формі:**

```javascript
function CreateUserForm() {
    const { createUser, loading } = useStore()
    const [name, setName] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        await createUser({ name })
        setName('')
    }

    return (
        <form onSubmit={handleSubmit}>
            <input value={name} onChange={(e) => setName(e.target.value)} disabled={loading} />
            <button type="submit" disabled={loading}>
                {loading ? 'Додавання...' : 'Додати'}
            </button>
        </form>
    )
}
```

Тепер форма disabled під час завантаження, і кнопка показує стан.

**Термінологія:**

-   **useEffect** - React hook для побічних ефектів
-   **Dependencies** - залежності useEffect
-   **Early return** - раннє повернення з функції
-   **e.preventDefault()** - запобігання стандартній поведінці браузера
-   **disabled** - заблокований, неактивний

---

## Слайд 16: Селектори (Selectors)

**Що говорити:**
Селектори - це функції для витягування та обчислення даних зі store. Вони роблять код більш організованим і підтримуваним.

**Базові селектори:**

```javascript
const selectTodos = (state) => state.todos
const selectFilter = (state) => state.filter
```

Це найпростіші селектори - просто повертають поле зі стану. Але навіщо їх створювати? Чому не писати `(state) => state.todos` напряму?

**Переваги:**

1. **Переви використання** - якщо структура стану зміниться, міняємо тільки селектор
2. **Іменовані функції** - `selectTodos` читабельніше
3. **Легко тестувати** - можна тестувати селектори окремо
4. **Один раз визначили** - використовуємо скрізь

**Обчислений селектор:**

```javascript
const selectFilteredTodos = (state) => {
    const { todos, filter } = state
    if (filter === 'active') return todos.filter((t) => !t.completed)
    if (filter === 'completed') return todos.filter((t) => t.completed)
    return todos
}
```

Цей селектор робить обчислення - фільтрує todos на основі filter. Логіка інкапсульована в селекторі, компонент просто використовує результат:

```javascript
function TodoList() {
    const filteredTodos = useStore(selectFilteredTodos)
    return (
        <ul>
            {filteredTodos.map((todo) => (
                <li key={todo.id}>{todo.text}</li>
            ))}
        </ul>
    )
}
```

Компонент не знає ЯК фільтруються todos - він просто отримує відфільтрований список. Це називається separation of concerns - розділення відповідальностей.

**Де визначати селектори:**

```javascript
// store.js
const useStore = create((set) => ({
    todos: [],
    filter: 'all',
    // ...
}))

// Селектори поруч зі store
export const selectTodos = (state) => state.todos
export const selectFilteredTodos = (state) => {
    const { todos, filter } = state
    if (filter === 'active') return todos.filter((t) => !t.completed)
    if (filter === 'completed') return todos.filter((t) => t.completed)
    return todos
}
```

Експортуйте селектори разом зі store - так їх легко імпортувати і використовувати.

**Композиція селекторів:**

```javascript
const selectTodos = (state) => state.todos
const selectActiveTodos = (state) => selectTodos(state).filter((t) => !t.completed)
const selectCompletedTodos = (state) => selectTodos(state).filter((t) => t.completed)
const selectTodoCount = (state) => selectTodos(state).length
```

Можна будувати складні селектори на основі простих.

**Термінологія:**

-   **Selector** - селектор, функція для вибору даних
-   **Computed value** - обчислене значення
-   **Separation of concerns** - розділення відповідальностей
-   **Encapsulation** - інкапсуляція, приховування деталей реалізації
-   **Composition** - композиція, побудова складного з простого

---

## Слайд 17: Мемоізовані Селектори

**Що говорити:**
Якщо селектор робить складні обчислення, варто використовувати мемоізацію для оптимізації продуктивності.

**Проблема без мемоізації:**

```javascript
const selectFilteredTodos = (state) => {
    console.log('Computing filtered todos')
    const { todos, filter } = state
    if (filter === 'active') return todos.filter((t) => !t.completed)
    if (filter === 'completed') return todos.filter((t) => t.completed)
    return todos
}

function TodoList() {
    const filteredTodos = useStore(selectFilteredTodos)
    // ...
}
```

Console.log буде спрацьовувати при кожному рендері компонента, навіть якщо todos і filter не змінилися! Це може бути проблемою для дорогих обчислень.

**Рішення: Reselect:**

```javascript
import { createSelector } from 'reselect'

const selectFilteredTodos = createSelector(
    [(state) => state.todos, (state) => state.filter],
    (todos, filter) => {
        console.log('Computing filtered todos') // Викликається тільки при зміні!
        if (filter === 'active') return todos.filter((t) => !t.completed)
        if (filter === 'completed') return todos.filter((t) => t.completed)
        return todos
    },
)
```

**Як це працює:**

1. **Input selectors:** `[(state) => state.todos, (state) => state.filter]`

    - createSelector викликає кожен input selector
    - Порівнює результати з попередніми за допомогою ===

2. **Result function:** `(todos, filter) => { ... }`
    - Викликається ТІЛЬКИ якщо хоч один з inputs змінився
    - Результат кешується

**Переваги:**

-   Обчислення виконуються тільки коли потрібно
-   Результат кешується і переви використовується
-   Компоненти не ререндеряться без потреби

**Альтернатива: zustand/traditional:**

```javascript
import { createWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/shallow'

const useStore = createWithEqualityFn(
    (set) => ({
        /* ... */
    }),
    shallow,
)
```

Це дозволяє використовувати shallow порівняння за замовчуванням для всього store.

**Коли використовувати мемоізацію:**

-   Складні обчислення (фільтрація, сортування великих масивів)
-   Обчислення на основі кількох полів стану
-   Створення нових об'єктів/масивів в селекторі

**Коли НЕ потрібна мемоізація:**

-   Прості селектори - просто повертають поле
-   Обчислення дуже швидкі (< 1ms)
-   Дані змінюються при кожному рендері

**Термінологія:**

-   **Memoization** - мемоізація, кешування результату обчислень
-   **Caching** - кешування, збереження для повторного використання
-   **Expensive computation** - дороге обчислення, яке займає багато часу
-   **Reselect** - бібліотека для створення мемоізованих селекторів
-   **Input selectors** - вхідні селектори, витягують дані для обчислень

---

## Слайд 18: Доступ поза React компонентами

**Що говорити:**
Одна з унікальних можливостей Zustand - можна використовувати store поза React компонентами! Це дуже корисно для utility функцій, WebSocket handlers, event listeners.

**Читання стану:**

```javascript
const currentCount = useStore.getState().count
console.log(currentCount) // 0
```

`getState()` - метод, який повертає поточний стан. Це синхронна функція, результат актуальний на момент виклику.

**Виклик action:**

```javascript
useStore.getState().increment()
console.log(useStore.getState().count) // 1
```

Actions також доступні через getState(). Можете викликати їх де завгодно.

**Підписка на зміни:**

```javascript
const unsubscribe = useStore.subscribe(
    (state) => console.log('State changed:', state.count),
    (state) => state.count, // Selector - слухати тільки count
)

// Коли підписка більше не потрібна
unsubscribe()
```

`subscribe()` дозволяє підписатися на зміни стану. Перший аргумент - callback, другий - опціональний selector.

**Зміна стану напряму:**

```javascript
useStore.setState({ count: 100 })
```

`setState()` - аналог функції `set()` всередині create, але доступний ззовні.

**Скидання стану:**

```javascript
useStore.setState(useStore.getInitialState())
```

`getInitialState()` повертає початковий стан, з яким store був створений.

**Приклади використання:**

**1. WebSocket handler:**

```javascript
const socket = new WebSocket('ws://localhost:3000')

socket.onmessage = (event) => {
    const message = JSON.parse(event.data)
    useStore.setState({ messages: [...useStore.getState().messages, message] })
}
```

**2. Event listener:**

```javascript
window.addEventListener('online', () => {
    useStore.setState({ isOnline: true })
})

window.addEventListener('offline', () => {
    useStore.setState({ isOnline: false })
})
```

**3. Utility функція:**

```javascript
export function logCurrentUser() {
    const user = useStore.getState().user
    console.log('Current user:', user)
}

// Можна викликати де завгодно
logCurrentUser()
```

**4. API client:**

```javascript
export async function apiCall(endpoint) {
    const token = useStore.getState().token

    const response = await fetch(endpoint, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })

    return response.json()
}
```

**Важливо:**
Поза React компонентами немає автоматичних rerenders! Якщо ви читаєте стан через getState(), ви отримуєте значення на момент виклику, але не підписуєтесь на зміни.

**Термінологія:**

-   **getState()** - метод для отримання поточного стану
-   **setState()** - метод для зміни стану ззовні
-   **subscribe()** - метод для підписки на зміни
-   **unsubscribe()** - функція для відписки
-   **WebSocket** - технологія для двостороннього зв'язку з сервером
-   **Event listener** - слухач подій

---

## Слайд 19: Middleware: Logging

**Що говорити:**
Middleware в Zustand - це функції, які обгортають store для додавання додаткової функціональності. Це схоже на middleware в Redux, але синтаксис трохи інший.

**Власний logger middleware:**

```javascript
const logger = (config) => (set, get, api) =>
    config(
        (...args) => {
            console.log('Previous state:', get())
            set(...args)
            console.log('New state:', get())
        },
        get,
        api,
    )

const useStore = create(
    logger((set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 })),
    })),
)
```

Це виглядає складно! Розберемо що тут відбувається.

**Структура middleware:**

```javascript
const middleware = (config) => (set, get, api) => config(modifiedSet, get, api)
```

Middleware - це функція, яка:

1. Приймає **config** (функцію створення store)
2. Повертає функцію, яка приймає **(set, get, api)**
3. Ця функція викликає config з модифікованими параметрами

У нашому logger middleware ми обгортаємо `set`:

```javascript
(...args) => {
    console.log('Previous state:', get())
    set(...args) // Викликаємо оригінальний set
    console.log('New state:', get())
}
```

Тепер при кожній зміні стану ми побачимо в консолі попередній і новий стан!

**Вбудований devtools middleware:**

```javascript
import { devtools } from 'zustand/middleware'

const useStore = create(
    devtools((set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 })),
    })),
)
```

Devtools middleware інтегрує store з Redux DevTools Extension. Це дозволяє:

-   Бачити всі зміни стану
-   Time travel debugging
-   Export/import стану
-   Performance monitoring

**Використання devtools з назвами actions:**

```javascript
const useStore = create(
    devtools((set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 }), false, 'increment'),
        decrement: () => set((state) => ({ count: state.count - 1 }), false, 'decrement'),
    })),
)
```

Третій параметр `set()` - назва action в DevTools. Це допомагає відстежувати що саме змінило стан.

**Опції devtools:**

```javascript
const useStore = create(
    devtools(
        (set) => ({
            /* ... */
        }),
        {
            name: 'CounterStore', // Назва в DevTools
            enabled: process.env.NODE_ENV === 'development', // Тільки в dev режимі
        },
    ),
)
```

**name** - як store буде називатися в DevTools (корисно якщо у вас кілька stores)
**enabled** - чи увімкнений DevTools (зазвичай тільки в development)

**Термінологія:**

-   **Middleware** - проміжне ПЗ, обгортка для додавання функціональності
-   **Logger** - інструмент для логування, запису подій
-   **DevTools** - інструменти для розробників
-   **Time travel debugging** - відлагодження з можливістю повернутися до попереднього стану
-   **Wrapping** - обгортання функції для зміни її поведінки

---

## Слайд 20: DevTools

**Що говорити:**
Redux DevTools - це потужний інструмент для debugging, і Zustand може його використовувати через devtools middleware.

**Базове підключення:**

```javascript
import { devtools } from 'zustand/middleware'

const useStore = create(
    devtools((set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 }), false, 'increment'),
    })),
)
```

Після цього встановіть Redux DevTools Extension в браузері (Chrome/Firefox), і ваш Zustand store буде видимий там!

**Параметри set() з DevTools:**

```javascript
set(newState, replace, actionName)
```

-   **newState** - новий стан (об'єкт або функція)
-   **replace** - true для повної заміни, false для merge
-   **actionName** - назва дії для відображення в DevTools

**Приклад з назвами:**

```javascript
const useTodoStore = create(
    devtools((set) => ({
        todos: [],
        addTodo: (text) =>
            set((state) => ({ todos: [...state.todos, { id: Date.now(), text }] }), false, 'todos/add'),
        toggleTodo: (id) =>
            set(
                (state) => ({
                    todos: state.todos.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t)),
                }),
                false,
                'todos/toggle',
            ),
        deleteTodo: (id) =>
            set((state) => ({ todos: state.todos.filter((t) => t.id !== id) }), false, 'todos/delete'),
    })),
)
```

Тепер в DevTools ви бачитимете назви actions: "todos/add", "todos/toggle", "todos/delete". Це допомагає зрозуміти що саме відбувається в додатку.

**Опції devtools:**

```javascript
const useStore = create(
    devtools(
        (set) => ({
            /* store */
        }),
        {
            name: 'TodoStore', // Назва в DevTools
            enabled: process.env.NODE_ENV === 'development', // Увімкнено тільки в dev
            anonymousActionType: 'unknown', // Назва для actions без імені
            trace: true, // Stack trace для actions
        },
    ),
)
```

**Можливості DevTools:**

1. **Список actions** - бачите всі зміни стану в хронологічному порядку
2. **State diff** - різниця між попереднім і новим станом
3. **Time travel** - можете "повернутися" до будь-якого попереднього стану
4. **Export/Import** - збережіть стан і завантажте пізніше для тестування
5. **Action filtering** - фільтруйте actions по назві
6. **State charts** - візуалізація змін стану

**Поради:**

-   Завжди давайте назви actions - це робить debugging набагато легшим
-   Використовуйте namespace pattern: 'todos/add', 'user/login'
-   Вимикайте DevTools в production через enabled: false
-   Якщо забули назву action, побачите "unknown" в DevTools

**Термінологія:**

-   **Redux DevTools** - розширення браузера для відлагодження Redux (і Zustand!)
-   **Action name** - назва дії для відображення в DevTools
-   **State diff** - різниця між станами
-   **Time travel** - можливість повернутися до попереднього стану
-   **Stack trace** - стек викликів, послідовність функцій

---

## Слайд 21: Persist: Збереження в localStorage

**Що говорити:**
Persist middleware автоматично зберігає стан в localStorage (або sessionStorage) і відновлює його при перезавантаженні сторінки. Це дуже корисно для збереження налаштувань, auth токенів, кошика покупок.

**Базове використання:**

```javascript
import { persist, createJSONStorage } from 'zustand/middleware'

const useStore = create(
    persist(
        (set) => ({
            user: null,
            token: null,
            setUser: (user) => set({ user }),
            setToken: (token) => set({ token }),
            logout: () => set({ user: null, token: null }),
        }),
        {
            name: 'auth-storage', // Ключ в localStorage
            storage: createJSONStorage(() => localStorage),
        },
    ),
)
```

Після цього:

1. Коли стан змінюється - автоматично зберігається в `localStorage['auth-storage']`
2. При завантаженні сторінки - стан автоматично відновлюється

Відкрийте DevTools → Application → Local Storage і побачите збережений стан!

**localStorage vs sessionStorage:**

```javascript
// localStorage - зберігається навіть після закриття браузера
storage: createJSONStorage(() => localStorage)

// sessionStorage - очищається при закритті вкладки
storage: createJSONStorage(() => sessionStorage)
```

**Часткове збереження (partialize):**

```javascript
persist(
    (set) => ({
        user: { name: 'John', preferences: { theme: 'dark' } },
        token: 'abc123',
        temporaryData: 'не зберігати',
        /* ... */
    }),
    {
        name: 'auth-storage',
        partialize: (state) => ({
            token: state.token,
            theme: state.user.preferences.theme,
            // НЕ зберігаємо user і temporaryData
        }),
    },
)
```

`partialize` дозволяє вибрати ЩО саме зберігати. Це корисно:

-   Для зменшення розміру в localStorage (обмеження ~5-10MB)
-   Щоб не зберігати тимчасові дані
-   Для безпеки - не зберігати чутливі дані

**Чому корисно:**

1. **Auth токени** - користувач залишається залогіненим після перезавантаження
2. **Налаштування** - тема, мова, layout preferences
3. **Кошик покупок** - товари не зникають при перезавантаженні
4. **Форми** - draft posts, незбережені зміни
5. **UI стан** - відкриті панелі, позиція скролу

**Обмеження localStorage:**

-   Розмір: ~5-10MB (залежить від браузера)
-   Синхронний API - може гальмувати при великих даних
-   Тільки strings - об'єкти серіалізуються в JSON
-   Доступний з JavaScript - не зберігайте паролі!

**Термінологія:**

-   **localStorage** - сховище браузера, зберігається назавжди
-   **sessionStorage** - сховище сесії, очищається при закритті вкладки
-   **Persist** - збереження, зберігання даних між сесіями
-   **Hydration** - відновлення стану з сховища
-   **Serialization** - перетворення об'єкта в string (JSON)
-   **Partialize** - часткове збереження, вибір полів для збереження

---

## Слайд 22: Persist: Опції

**Що говорити:**
Persist middleware має багато опцій для налаштування поведінки збереження.

**Базові опції:**

```javascript
persist(
    (set) => ({
        /* store */
    }),
    {
        name: 'my-storage', // ОБОВ'ЯЗКОВО: ключ в localStorage
        storage: createJSONStorage(() => localStorage), // Де зберігати
        partialize: (state) => ({ count: state.count }), // Що зберігати
    },
)
```

**Версіонування та міграції:**

```javascript
persist(
    (set) => ({
        /* store */
    }),
    {
        name: 'my-storage',
        version: 2, // Версія структури стану
        migrate: (persistedState, version) => {
            // Міграція при зміні версії
            if (version === 0) {
                // Була версія 0, оновлюємо до версії 1
                persistedState.newField = 'default value'
            }
            if (version === 1) {
                // Була версія 1, оновлюємо до версії 2
                persistedState.renamedField = persistedState.oldField
                delete persistedState.oldField
            }
            return persistedState
        },
    },
)
```

Це дуже корисно! Уявіть, ви змінили структуру стану в новій версії додатку:

```javascript
// Стара версія
{ user: 'John' }

// Нова версія
{ user: { name: 'John', role: 'admin' } }
```

Без міграції користувачі, які мають стару версію в localStorage, отримають помилки. З міграцією ви конвертуєте старий формат в новий.

**Callbacks:**

```javascript
persist(
    (set) => ({
        /* store */
    }),
    {
        name: 'my-storage',
        onRehydrateStorage: () => (state, error) => {
            // Викликається ПІСЛЯ відновлення стану
            if (error) {
                console.log('Error during hydration:', error)
            } else {
                console.log('Hydration finished')
                console.log('Restored state:', state)
            }
        },
    },
)
```

`onRehydrateStorage` корисний для:

-   Логування успішного відновлення
-   Обробки помилок (corrupted data)
-   Виконання додаткової логіки після відновлення
-   Показу splash screen під час завантаження

**Skip hydration:**

```javascript
persist(
    (set) => ({
        /* store */
    }),
    {
        name: 'my-storage',
        skipHydration: true, // Не відновлювати автоматично
    },
)

// Потім вручну:
useStore.persist.rehydrate()
```

Це корисно коли потрібен контроль над моментом відновлення стану. Наприклад, спочатку показати splash screen, завантажити critical data, і тільки потім відновити стан.

**Custom storage:**

```javascript
persist(
    (set) => ({
        /* store */
    }),
    {
        name: 'my-storage',
        storage: {
            getItem: async (name) => {
                // Завантажити з IndexedDB, AsyncStorage, etc
                return await myDB.get(name)
            },
            setItem: async (name, value) => {
                await myDB.set(name, value)
            },
            removeItem: async (name) => {
                await myDB.delete(name)
            },
        },
    },
)
```

Можна зберігати де завгодно:

-   IndexedDB - для великих даних
-   AsyncStorage - для React Native
-   Custom backend - зберігання на сервері
-   In-memory cache

**Термінологія:**

-   **Version** - версія структури даних
-   **Migration** - міграція, конвертація старого формату в новий
-   **Hydration** - відновлення стану з сховища
-   **Rehydrate** - повторне відновлення
-   **Corrupted data** - пошкоджені дані
-   **IndexedDB** - база даних браузера для великих об'ємів даних
-   **AsyncStorage** - асинхронне сховище в React Native

---

## Слайд 23: Immer: Мутабельний синтаксис

**Що говорити:**
Immer middleware дозволяє писати код, який виглядає як мутація, але насправді створює іммутабельні копії. Це робить код набагато простішим, особливо для складних вкладених структур.

**Без Immer:**

```javascript
// ❌ Складний іммутабельний код
addTodo: (text) =>
    set((state) => ({
        todos: [...state.todos, { id: Date.now(), text, completed: false }],
    }))

toggleTodo: (id) =>
    set((state) => ({
        todos: state.todos.map((todo) => (todo.id === id ? { ...todo, completed: !todo.completed } : todo)),
    }))
```

**З Immer:**

```javascript
import { immer } from 'zustand/middleware/immer'

const useStore = create(
    immer((set) => ({
        todos: [],

        // ✨ Можна "мутувати"!
        addTodo: (text) =>
            set((state) => {
                state.todos.push({ id: Date.now(), text, completed: false })
            }),

        toggleTodo: (id) =>
            set((state) => {
                const todo = state.todos.find((t) => t.id === id)
                if (todo) {
                    todo.completed = !todo.completed
                }
            }),

        deleteTodo: (id) =>
            set((state) => {
                const index = state.todos.findIndex((t) => t.id === id)
                if (index !== -1) {
                    state.todos.splice(index, 1)
                }
            }),
    })),
)
```

Код виглядає як звичайні мутації: `push`, `todo.completed = !todo.completed`, `splice`. Але Immer під капотом створює нові іммутабельні об'єкти!

**Як це працює:**

Immer використовує Proxy для відстеження всіх змін. Коли ви "змінюєте" стан, Immer записує ці зміни і створює новий іммутабельний стан на їх основі.

**Переваги Immer:**

1. **Простіший код** - не потрібно пам'ятати про spread operators
2. **Менше помилок** - важко випадково змутувати стан
3. **Читабельність** - код виглядає як звичайний JavaScript
4. **Вкладені оновлення** - легко оновлювати deep nested objects

**Приклад складного оновлення:**

```javascript
// Без Immer - ЖАХЛИВО
updateUserEmail: (newEmail) => set(state => ({
    user: {
        ...state.user,
        profile: {
            ...state.user.profile,
            contacts: {
                ...state.user.profile.contacts,
                email: newEmail
            }
        }
    }
}))

// З Immer - ПРОСТО
updateUserEmail: (newEmail) => set(state => {
    state.user.profile.contacts.email = newEmail;
})
```

Різниця драматична! З Immer код читабельний і зрозумілий.

**Комбінування з іншими middleware:**

```javascript
import { immer } from 'zustand/middleware/immer'
import { devtools, persist } from 'zustand/middleware'

const useStore = create(
    devtools(
        persist(
            immer((set) => ({
                // store
            })),
            { name: 'storage' },
        ),
    ),
)
```

**Коли використовувати Immer:**

-   ✅ Складні вкладені структури
-   ✅ Багато оновлень масивів
-   ✅ Команда не звикла до іммутабельності
-   ✅ Код стає занадто складним з spread operators

**Коли НЕ потрібен Immer:**

-   ❌ Прості flat структури
-   ❌ Критична продуктивність (Immer трохи повільніший)
-   ❌ Bundle size важливий (Immer ~15KB)

**Термінологія:**

-   **Immer** - бібліотека для іммутабельних оновлень через мутабельний синтаксис
-   **Proxy** - JavaScript об'єкт для перехоплення операцій
-   **Deep nested** - глибоко вкладені структури
-   **Flat** - плоска структура без вкладеності
-   **Spread operator (...)** - оператор розгортання

---

## Слайд 24: Комбінування Middleware

**Що говорити:**
Middleware можна комбінувати для отримання всіх необхідних можливостей. Але порядок має значення!

**Правильний порядок:**

```javascript
const useStore = create(
    devtools(
        // Найзовнішній - devtools бачить все
        persist(
            // Середній - persist зберігає результат після immer
            immer((set) => ({
                // Найвнутрішній - immer працює з кодом напряму
                user: null,
                todos: [],

                setUser: (user) =>
                    set((state) => {
                        state.user = user
                    }),

                addTodo: (text) =>
                    set((state) => {
                        state.todos.push({ id: Date.now(), text, completed: false })
                    }),
            })),
            { name: 'app-storage' }, // Опції для persist
        ),
        { name: 'AppStore' }, // Опції для devtools
    ),
)
```

**Чому порядок важливий:**

1. **Immer** - найвнутрішній, бо він перетворює мутабельний код в іммутабельний. Інші middleware працюють з результатом.

2. **Persist** - середній, зберігає стан після того, як Immer створив іммутабельну копію. Якщо persist буде всередині, може зберегти неправильний стан.

3. **DevTools** - найзовнішній, щоб бачити всі зміни після всіх трансформацій. Він показує фінальний стан.

**Загальне правило:**

```
devtools → persist → immer → [інші middleware] → store code
```

**Приклад з кількома middleware:**

```javascript
import { create } from 'zustand'
import { devtools, persist, subscribeWithSelector } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

const useStore = create(
    devtools(
        persist(
            subscribeWithSelector(
                immer((set) => ({
                    // store
                })),
            ),
            { name: 'storage' },
        ),
        { name: 'Store' },
    ),
)
```

`subscribeWithSelector` - middleware, який дозволяє підписуватися на зміни конкретних полів поза React.

**Типові комбінації:**

```javascript
// Auth store - persist + devtools
create(devtools(persist(store, { name: 'auth' }), { name: 'Auth' }))

// Todo store - всі три
create(devtools(persist(immer(store), { name: 'todos' }), { name: 'Todos' }))

// Settings store - тільки persist
create(persist(store, { name: 'settings' }))

// Dev store - тільки devtools
create(devtools(store, { name: 'Dev' }))
```

**Проблеми порядку:**

```javascript
// ❌ НЕПРАВИЛЬНО - persist всередині immer
create(immer(persist(store, { name: 'storage' })))
// Persist може зберегти проміжний стан!

// ✅ ПРАВИЛЬНО
create(persist(immer(store), { name: 'storage' }))
```

**TypeScript типізація:**

```typescript
const useStore = create<State>()(
    // Додаткові дужки для TypeScript!
    devtools(persist(immer(store), { name: 'storage' }), { name: 'Store' }),
)
```

Зверніть увагу на `create<State>()()` - подвійні дужки потрібні для правильної типізації з middleware.

**Термінологія:**

-   **Middleware composition** - композиція middleware, комбінування
-   **Order matters** - порядок має значення
-   **Wrapping** - обгортання одного в інше
-   **Outer/Inner** - зовнішній/внутрішній middleware
-   **subscribeWithSelector** - middleware для підписки на частину стану

---

## Слайд 25: Slices Pattern

**Що говорити:**
Для великих додатків рекомендується розбивати store на slices - логічні частини, які відповідають за окремі domain areas.

**Проблема великого store:**

```javascript
// ❌ Один великий файл - важко підтримувати
const useStore = create((set) => ({
    // User state
    user: null,
    setUser: (user) => set({ user }),
    logout: () => set({ user: null }),

    // Todos state
    todos: [],
    addTodo: (text) => set((state) => ({ todos: [...state.todos, { text }] })),
    deleteTodo: (id) => set((state) => ({ todos: state.todos.filter((t) => t.id !== id) })),

    // Settings state
    theme: 'light',
    setTheme: (theme) => set({ theme }),
    // ... ще 100 рядків коду
}))
```

**Рішення - Slices Pattern:**

```javascript
// slices/userSlice.js
export const createUserSlice = (set, get) => ({
    user: null,
    setUser: (user) => set({ user }),
    logout: () => set({ user: null }),
    isAuthenticated: () => {
        return get().user !== null
    },
})

// slices/todosSlice.js
export const createTodosSlice = (set, get) => ({
    todos: [],
    addTodo: (text) =>
        set((state) => ({
            todos: [...state.todos, { id: Date.now(), text, completed: false }],
        })),
    getTodoCount: () => {
        return get().todos.length
    },
})

// store.js
import { create } from 'zustand'
import { createUserSlice } from './slices/userSlice'
import { createTodosSlice } from './slices/todosSlice'

const useStore = create((...a) => ({
    ...createUserSlice(...a),
    ...createTodosSlice(...a),
}))

export default useStore
```

**Що тут відбувається:**

1. **Кожен slice** - окрема функція, яка повертає частину стану
2. **`(...a)`** - передаємо всі аргументи (set, get, api) в кожен slice
3. **Spread operator** - об'єднуємо всі slices в один store

**Переваги:**

-   ✅ **Організація** - кожен domain в окремому файлі
-   ✅ **Переви використання** - slices можна використовувати в різних stores
-   ✅ **Команда** - різні розробники працюють над різними slices
-   ✅ **Тестування** - кожен slice тестується окремо
-   ✅ **Code splitting** - можна lazy load slices

**Взаємодія між slices:**

```javascript
// todosSlice може використовувати user slice
export const createTodosSlice = (set, get) => ({
    todos: [],
    addTodo: (text) => {
        const user = get().user // Доступ до іншого slice!
        if (!user) {
            console.error('User not authenticated')
            return
        }
        set((state) => ({
            todos: [...state.todos, { id: Date.now(), text, userId: user.id }],
        }))
    },
})
```

Slices можуть читати стан інших slices через `get()`.

**Структура проекту:**

```
src/
├── store/
│   ├── slices/
│   │   ├── userSlice.js
│   │   ├── todosSlice.js
│   │   ├── settingsSlice.js
│   │   └── cartSlice.js
│   ├── index.js          # Комбінований store
│   └── types.ts          # TypeScript types
├── components/
└── ...
```

**Коли використовувати slices:**

-   ✅ Додаток має кілька доменів (user, todos, cart, etc)
-   ✅ Store файл > 200-300 рядків
-   ✅ Різні розробники працюють над різними частинами
-   ✅ Потрібна повторне використання логіки

**Коли НЕ потрібні slices:**

-   ❌ Малий додаток (< 100 рядків store коду)
-   ❌ Всі дані тісно пов'язані
-   ❌ Працюєте один

**Термінологія:**

-   **Slice** - частина, шматок store
-   **Domain** - домен, логічна область (user, todos, cart)
-   **Code splitting** - розділення коду на частини
-   **Reusability** - можливість повторного використання
-   **Spread operator** - оператор розгортання

---

## Слайд 26: Slices з TypeScript

**Що говорити:**
TypeScript з slices pattern вимагає трохи більше типізації, але результат дуже потужний - повна type safety!

**Визначаємо типи для кожного slice:**

```typescript
// User Slice
interface User {
    id: number
    name: string
    email: string
}

interface UserSlice {
    user: User | null
    setUser: (user: User) => void
    logout: () => void
}

const createUserSlice: StateCreator<UserSlice & TodosSlice, [], [], UserSlice> = (set) => ({
    user: null,
    setUser: (user) => set({ user }),
    logout: () => set({ user: null }),
})
```

**Розберемо StateCreator:**

```typescript
StateCreator<Store, Middlewares, InnerMiddlewares, Slice>
```

-   **Store** - повний тип store (всі slices разом)
-   **Middlewares** - які middleware використовуються
-   **InnerMiddlewares** - внутрішні middleware
-   **Slice** - тип цього конкретного slice

**Комбінування slices:**

```typescript
// Todos Slice
interface Todo {
    id: number
    text: string
    completed: boolean
}

interface TodosSlice {
    todos: Todo[]
    addTodo: (text: string) => void
    toggleTodo: (id: number) => void
}

const createTodosSlice: StateCreator<UserSlice & TodosSlice, [], [], TodosSlice> = (set) => ({
    todos: [],
    addTodo: (text) => set((state) => ({ todos: [...state.todos, { id: Date.now(), text, completed: false }] })),
    toggleTodo: (id) =>
        set((state) => ({
            todos: state.todos.map((todo) => (todo.id === id ? { ...todo, completed: !todo.completed } : todo)),
        })),
})
```

**Створюємо store:**

```typescript
type StoreState = UserSlice & TodosSlice

const useStore = create<StoreState>()((...a) => ({
    ...createUserSlice(...a),
    ...createTodosSlice(...a),
}))
```

Зверніть увагу: `create<StoreState>()()` - подвійні дужки!

**Використання в компонентах:**

```typescript
function UserProfile() {
    // TypeScript знає всі доступні поля і методи!
    const { user, logout } = useStore()

    if (!user) return <div>Please login</div>

    return (
        <div>
            <h1>{user.name}</h1> {/* TypeScript перевірить що name існує */}
            <button onClick={logout}>Logout</button>
        </div>
    )
}
```

**З middleware:**

```typescript
import { immer } from 'zustand/middleware/immer'

const createTodosSlice: StateCreator<UserSlice & TodosSlice, [['zustand/immer', never]], [], TodosSlice> = (set) => ({
    todos: [],
    addTodo: (text) =>
        set((state) => {
            state.todos.push({ id: Date.now(), text, completed: false })
        }),
})
```

Другий generic параметр `[['zustand/immer', never]]` вказує що використовується Immer middleware.

**Переваги TypeScript з slices:**

-   ✅ **Автодоповнення** - IDE підказує всі доступні методи
-   ✅ **Type safety** - помилки на етапі компіляції
-   ✅ **Refactoring** - легко перейменовувати поля
-   ✅ **Documentation** - типи - це документація

**Складність:**
Так, типізація виглядає складно. Але:

-   Пишете один раз
-   Копіюєте pattern для нових slices
-   Отримуєте type safety везде

**Термінологія:**

-   **StateCreator** - тип для функцій створення slices
-   **Generic** - узагальнений параметр типу
-   **Type safety** - безпека типів, перевірка на етапі компіляції
-   **Autocomplete** - автодоповнення коду
-   **Refactoring** - рефакторинг, зміна структури коду

---

## Слайд 27: TypeScript: Базовий приклад

**Що говорити:**
Zustand має відмінну підтримку TypeScript. Розглянемо базовий типізований store.

**Визначаємо interface стану:**

```typescript
interface CounterState {
    count: number
    increment: () => void
    decrement: () => void
    incrementByAmount: (amount: number) => void
    reset: () => void
}
```

Тут ми описуємо:

-   **Поля стану** - count: number
-   **Actions** - функції для зміни стану з їх сигнатурами

**Створюємо store:**

```typescript
const useCounterStore = create<CounterState>()((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
    incrementByAmount: (amount) => set((state) => ({ count: state.count + amount })),
    reset: () => set({ count: 0 }),
}))
```

**Важливо:** `create<CounterState>()()` - подвійні дужки!

Чому подвійні дужки? Це особливість TypeScript типізації. Перші дужки для типу, другі для функції.

**Використання в компонентах:**

```typescript
function Counter() {
    // TypeScript знає типи!
    const { count, increment, decrement } = useCounterStore()

    return (
        <div>
            <h1>Count: {count}</h1>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
        </div>
    )
}
```

TypeScript автоматично:

-   Підказує доступні поля (count, increment, decrement, ...)
-   Перевіряє типи (count - це number, increment - це function)
-   Показує помилки якщо ви помилилися в назві

**Переваги:**

```typescript
// ❌ TypeScript покаже помилку
const counter = useCounterStore((state) => state.countr) // Typo!

// ❌ TypeScript покаже помилку
useCounterStore().increment(5) // increment не приймає аргументи!

// ✅ Все правильно
const count = useCounterStore((state) => state.count)
useCounterStore().incrementByAmount(5)
```

**Типізація селекторів:**

```typescript
// TypeScript автоматично визначає тип
const count = useCounterStore((state) => state.count) // count: number

// Можна явно вказати тип результату
const count = useCounterStore((state: CounterState) => state.count)
```

**Best practice:**

```typescript
// ✅ Добре - interface для стану
interface CounterState {
    count: number
    increment: () => void
}

// ❌ Не треба - type для actions окремо
type CounterActions = {
    increment: () => void
}
```

Краще все в одному interface - простіше і зручніше.

**Термінологія:**

-   **Interface** - інтерфейс, опис структури об'єкта
-   **Type** - тип даних
-   **Generic** - узагальнений тип `<T>`
-   **Type inference** - автоматичне визначення типу
-   **Signature** - сигнатура функції (параметри і тип результату)

---

## Слайд 28: TypeScript з Middleware

**Що говорити:**
При використанні middleware з TypeScript потрібна додаткова типізація, але це забезпечує повну type safety.

**Базовий store з типами:**

```typescript
interface Todo {
    id: number
    text: string
    completed: boolean
}

interface TodoState {
    todos: Todo[]
    addTodo: (text: string) => void
    toggleTodo: (id: number) => void
}
```

**З Immer:**

```typescript
import { immer } from 'zustand/middleware/immer'

const useTodoStore = create<TodoState>()(
    immer((set) => ({
        todos: [],
        addTodo: (text) =>
            set((state) => {
                // TypeScript знає що state.todos - це Todo[]
                state.todos.push({ id: Date.now(), text, completed: false })
            }),
        toggleTodo: (id) =>
            set((state) => {
                const todo = state.todos.find((t) => t.id === id)
                if (todo) {
                    todo.completed = !todo.completed
                }
            }),
    })),
)
```

**З DevTools і Persist:**

```typescript
const useTodoStore = create<TodoState>()(
    devtools(
        persist(
            immer((set) => ({
                todos: [],
                addTodo: (text) =>
                    set((state) => {
                        state.todos.push({ id: Date.now(), text, completed: false })
                    }),
            })),
            { name: 'todos' }, // Опції persist
        ),
        { name: 'TodoStore' }, // Опції devtools
    ),
)
```

**Важливо:** Зверніть увагу на `create<TodoState>()()` - подвійні дужки обов'язкові при використанні middleware!

**Чому подвійні дужки:**

```typescript
// Без middleware - одинарні
const useStore = create<State>((set) => ({
    /* ... */
}))

// З middleware - подвійні
const useStore = create<State>()(
    middleware((set) => ({
        /* ... */
    })),
)
```

Це особливість TypeScript inference з middleware.

**Типізація persist partialize:**

```typescript
interface AuthState {
    user: User | null
    token: string | null
    temporaryData: string
    login: (credentials: Credentials) => Promise<void>
}

const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            /* ... */
        }),
        {
            name: 'auth',
            // TypeScript перевірить що поля існують
            partialize: (state) => ({
                token: state.token,
                // user: state.usr  // ❌ Помилка - usr не існує
            }),
        },
    ),
)
```

**Async actions з типами:**

```typescript
interface UserState {
    users: User[]
    loading: boolean
    error: string | null
    fetchUsers: () => Promise<void>
}

const useUserStore = create<UserState>()((set) => ({
    users: [],
    loading: false,
    error: null,

    fetchUsers: async () => {
        set({ loading: true, error: null })
        try {
            const response = await fetch('/api/users')
            const users: User[] = await response.json()
            set({ users, loading: false })
        } catch (error) {
            set({ error: (error as Error).message, loading: false })
        }
    },
}))
```

TypeScript перевіряє:

-   Типи полів (users: User[], loading: boolean)
-   Типи параметрів actions
-   Типи результатів async операцій

**Custom middleware типізація:**

```typescript
import { StateCreator, StoreMutatorIdentifier } from 'zustand'

type Logger = <
  T,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = []
>(
  config: StateCreator<T, Mps, Mcs>
) => StateCreator<T, Mps, Mcs>

const logger: Logger = (config) => (set, get, api) =>
    config(
        (...args) => {
            console.log('Previous:', get())
            set(...args)
            console.log('New:', get())
        },
        get,
        api
    )
```

Це складна типізація, але дає повну type safety для кастомних middleware.

**Переваги TypeScript з middleware:**

-   ✅ Type safety для всіх операцій
-   ✅ Автодоповнення працює скрізь
-   ✅ Помилки на етапі компіляції
-   ✅ Безпечний refactoring

**Термінологія:**

-   **Type inference** - автоматичне визначення типу
-   **StoreMutatorIdentifier** - тип для ідентифікації middleware
-   **StateCreator** - тип для функції створення store
-   **Generic** - узагальнений тип
-   **Type assertion** - явне вказування типу `as Type`

---

(Продовження нотаток у наступній частині...)
