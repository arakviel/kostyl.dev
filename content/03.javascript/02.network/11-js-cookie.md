# js-cookie: Керування Cookies без Болю

У попередніх розділах ми дослідили нативний інтерфейс `document.cookie`. Ви напевно помітили, наскільки він архаїчний та незручний. Робота з ним нагадує спробу написати SMS, використовуючи азбуку Морзе — це можливо, але навіщо так страждати у 21-му столітті?

Сьогодні ми познайомимось із **js-cookie** — бібліотекою, яка перетворює роботу з куками з "каторги" на елегантний та зрозумілий процес. Це **Industry Standard** для клієнтської роботи з cookies.

::note
**Чому саме js-cookie?**
Це легка (< 800 байт gzip), надійна бібліотека без залежностей, яка підтримує всі сучасні браузери та стандарти RFC 6265. Вона автоматично обробляє кодування спеціальних символів, що часто стає причиною багів при ручній роботі.
::

---

## 1. Проблема Нативного API

Перш ніж пірнати в рішення, згадаймо проблему. Чому розробники тікають від `document.cookie`?

Уявіть, що ви хочете просто прочитати куку `user_id`. Нативний спосіб виглядає як регулярний вираз або цикл з розбиттям рядка:

```javascript
// Native Way (The "Painful" Way)
const getCookie = (name) => {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop().split(';').shift()
}
```

Це багато коду для такої простої дії. А як щодо запису?

```javascript
// Запис складної куки
document.cookie = 'user=John%20Doe; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT; Secure; SameSite=Strict'
```

Тут легко помилитися в форматі дати, забути `encodeURIComponent`, або переплутати порядок.

**js-cookie** вирішує це радикально просто:

```javascript
Cookies.get('user_id') // Просто і гарно
```

---

## 2. Встановлення та Налаштування

Оскільки ми використовуємо **Vite** як наш сучасний збирач проєктів, встановлення відбудеться через NPM.

### Крок 1: Інсталяція пакету

Відкрийте термінал у вашому проєкті та виконайте команду:

::tabs
::tabs-item{label="npm"}

```bash
npm install js-cookie
```

::
::tabs-item{label="yarn"}

```bash
yarn add js-cookie
```

::
::tabs-item{label="pnpm"}

```bash
pnpm add js-cookie
```

::
::

### Крок 2: Типізація (TypeScript)

Якщо ви використовуєте TypeScript (а ви, як професіонал, маєте прагнути до цього), обов'язково встановіть типи. Бібліотека написана на JS, тому типи поставляються окремо:

```bash
npm install --save-dev @types/js-cookie
```

### Крок 3: Імпорт

У вашому JavaScript/TypeScript файлі:

```javascript [src/main.js]
import Cookies from 'js-cookie'

console.log(Cookies.get()) // Перевірка роботи
```

---

## 3. Базовий API: CRUD Операції

Бібліотека надає інтуїтивний API, який нагадує роботу з `localStorage`.

### 3.1. Запис Cookies (Create / Update)

Метод `Cookies.set(name, value, [options])` використовується для створення або оновлення куки.

```javascript
// Найпростіший випадок
// Створює сесійну куку для всього сайту
Cookies.set('theme', 'dark')
```

**Анатомія виклику:**

1.  `'theme'`: Назва куки (кей).
2.  `'dark'`: Значення. Воно автоматично енкодиться (URL-encoded).

> [!TIP]
> js-cookie автоматично перетворить `space` на `%20` та інші спецсимволи. Вам не потрібно викликати `encodeURIComponent`.

### 3.2. Читання Cookies (Read)

Метод `Cookies.get([name])` дозволяє отримати значення.

```javascript
// Отримання конкретної куки
const currentTheme = Cookies.get('theme') // => 'dark'

// Отримання неіснуючої куки
const token = Cookies.get('auth_token') // => undefined

// Отримання ВСІХ доступних кук (повертає об'єкт)
const allCookies = Cookies.get()
// => { theme: 'dark', _ga: 'GA1.2.345...' }
```

**Важливий момент:** При читанні бібліотека автоматично декодує значення (`decodeURIComponent`).

### 3.3. Видалення Cookies (Delete)

Метод `Cookies.remove(name, [options])` видаляє куку.

```javascript
Cookies.remove('theme')
```

::warning
**Підводний камінь:**
Якщо ви встановлювали куку з певними параметрами `path` або `domain`, ви **МУСИТЕ** передати ті самі параметри при видаленні!

```javascript
// Встановлення
Cookies.set('id', '123', { path: '/dashboard' })

// Не спрацює! (шукає в path: '/')
Cookies.remove('id')

// Спрацює
Cookies.remove('id', { path: '/dashboard' })
```

::

---

## 4. Робота з JSON

Одна з найпотужніших фіч js-cookie — прозора робота з JSON об'єктами. Нативний API приймає лише рядки. Якщо вам треба зберегти налаштування користувача, вам доводиться робити `JSON.stringify`. `js-cookie` бере це на себе.

### Запис об'єкта

```javascript
const userSettings = {
    theme: 'dark',
    notifications: false,
    sidebar: 'collapsed',
}

// Автоматичний JSON.stringify під капотом
Cookies.set('settings', userSettings)
```

У браузері це буде збережено як закодований JSON рядок.

### Читання об'єкта

```javascript
// Автоматичний JSON.parse
const settings = Cookies.getJSON('settings')
// або в нових версіях просто get, якщо бібліотека детектує JSON,
// але краще явно контролювати це.
```

_Примітка: У версії 3.x метод `getJSON` був видалений для спрощення API. Тепер розробник має сам дбати про парсинг, або використовувати конвертери (про це далі)._

Давайте подивимось, як це робити правильно у **v3+** (поточний стандарт):

```javascript
// v3 Pattern
const value = Cookies.get('settings')
if (value) {
    try {
        const settings = JSON.parse(value)
        console.log(settings.theme) // 'dark'
    } catch (e) {
        console.error('Cookie parsing failed', e)
    }
}
```

Чекайте, це ж знову незручно! Саме тому в v3 з'явилися **Converters** (Конвертери), які дозволяють повернути магію.

---

## 5. Конвертери (Converters)

Конвертери дозволяють змінити поведінку читання та запису за замовчуванням. Ми можемо створити свій екземпляр API, який автоматично працює з JSON.

```javascript
import Cookies from 'js-cookie'

const JsonCookies = Cookies.withConverter({
    read: function (value, name) {
        // Якщо значення починається з 'j:', це наш маркер JSON (опціонально)
        // Або просто пробуємо парсити все
        try {
            return JSON.parse(value)
        } catch (e) {
            // Якщо не вийшло, повертаємо як рядок
            return value
        }
    },
    write: function (value, name) {
        // Якщо це об'єкт, стрінгіфаємо його
        if (typeof value === 'object') {
            return JSON.stringify(value)
        }
        return value
    },
})

// Використання
JsonCookies.set('config', { color: 'red' })
const config = JsonCookies.get('config') // => { color: 'red' }
```

Це демонструє архітектурну гнучкість бібліотеки. Ви не прив'язані до дефолтної поведінки.

---

## 6. Атрибути Кук: Тонке Налаштування

Cookies — це не просто ключ-значення. Це механізм з купою налаштувань безпеки та життєвого циклу. Всі вони передаються третім аргументом.

### 6.1. Expires (Час життя)

За замовчуванням кука є **Session Cookie** (зникає при закритті браузера). Щоб зробити її постійною, треба вказати `expires`.

`js-cookie` приймає **кількість днів** як число (на відміну від нативного API, де треба передавати об'єкт `Date` у форматі UTC String).

```javascript
// Живе 7 днів
Cookies.set('token', 'xyz', { expires: 7 })

// Живе півдня (0.5 дня = 12 годин)
Cookies.set('short_lived', 'value', { expires: 0.5 })

// Живе 100 років (фактично вічна)
Cookies.set('forever', 'value', { expires: 36500 })
```

Якщо вам все ж потрібна точність до секунди, ви можете передати об'єкт `Date`:

```javascript
const date = new Date()
date.setTime(date.getTime() + 15 * 60 * 1000) // +15 хвилин
Cookies.set('session', 'active', { expires: date })
```

### 6.2. Path (Шлях)

Визначає, на яких URL доступна кука.

-   За замовчуванням: `'/'` (доступна на всьому сайті).
-   Можна обмежити видимість:

```javascript
// Доступна тільки на /store і вкладених (/store/cart)
Cookies.set('cart_id', '555', { path: '/store' })
```

### 6.3. Domain (Домен)

Дозволяє шарити куки між піддоменами.

Уявіть, що у вас є `app.example.com` і `blog.example.com`.
За замовчуванням кука з `app.` не видна на `blog.`.

```javascript
// Робимо куку доступною для *.example.com
Cookies.set('sso_token', 'token_val', { domain: '.example.com' })
```

### 6.4. Secure (Тільки HTTPS)

Критично для безпеки. Браузер не віддасть цю куку, якщо з'єднання не захищене (HTTP).

```javascript
Cookies.set('secret', 'top_secret', { secure: true })
```

> [!IMPORTANT]
> Завжди використовуйте `secure: true` для авторизаційних токенів та чутливих даних у продакшн середовищі. На `localhost` (крім Chrome) це може працювати і без HTTPS, але в Інтернеті — обов'язково.

### 6.5. SameSite (СTRF Захист)

Атрибут, який контролює, коли куки відправляються при крос-сайтових запитах.

-   `'Strict'`: Кука відправляється тільки якщо ви на тому ж сайті. Ніяких лінків з пошти.
-   `'Lax'`: (Дефолт у сучасних браузерах) Дозволяє безпечні переходи (GET) з інших сайтів.
-   `'None'`: Відправляється завжди (потрібен `Secure: true`).

```javascript
Cookies.set('auth', 'token', { sameSite: 'Strict', secure: true })
```

### Групове налаштування (defaults)

Якщо ви хочете, щоб усі ваші куки мали певні атрибути (наприклад, `SameSite: Strict`), не треба писати це щоразу. Використовуйте `withAttributes`:

```javascript
const SecureCookies = Cookies.withAttributes({
    path: '/',
    secure: true,
    parse: 'Strict',
})

SecureCookies.set('a', '1') // вже має secure і path
SecureCookies.set('b', '2')
```

---

## 7. Практичний Кейс: "Запам'ятати Мене"

Давайте реалізуємо класичний функціонал "Remember Me" на сторінці логіну.

**Задача:** Користувач вводить логін. Якщо він ставить галочку "Запам'ятати", ми зберігаємо його email на 30 днів.

```html [index.html]
<form id="loginForm">
    <input type="email" id="email" placeholder="Email" />
    <label> <input type="checkbox" id="remember" /> Запам'ятати мене </label>
    <button type="submit">Увійти</button>
</form>
```

```javascript [login.js]
import Cookies from 'js-cookie'

const emailInput = document.getElementById('email')
const rememberCheckbox = document.getElementById('remember')
const form = document.getElementById('loginForm')

// 1. При завантаженні перевіряємо куку
const savedEmail = Cookies.get('remember_email')
if (savedEmail) {
    emailInput.value = savedEmail
    rememberCheckbox.checked = true
}

// 2. Обробка сабміту
form.addEventListener('submit', (e) => {
    e.preventDefault()

    const email = emailInput.value
    const shouldRemember = rememberCheckbox.checked

    if (shouldRemember) {
        // Зберігаємо на 30 днів
        Cookies.set('remember_email', email, { expires: 30, sameSite: 'Lax' })
    } else {
        // Якщо галочку зняли — видаляємо куку
        Cookies.remove('remember_email')
    }

    // ... далі логіка авторизації
    console.log('Logging in...')
})
```

**Розбір Коду:**

1.  **Ініціалізація**: Ми перевіряємо, чи є вже збережений email. Це покращує UX — користувачу не треба вводити його знову.
2.  **User Intent**: Ми поважаємо вибір користувача. Якщо він знімає галочку `.remove()`, ми чистимо "хвости".
3.  **Безпека**: Ми не зберігаємо тут пароль! Тільки email. Паролі в куках (у відкритому вигляді) — це табу.

---

---

## 8. Deep Dive: Під Капотом (Under the Hood)

Щоб використовувати інструмент професійно, треба розуміти, як він працює всередині. `js-cookie` — це не просто обгортка над `document.cookie`, це розумний механізм, який вирішує проблеми сумісності та стандартів.

### 8.1. RFC 6265 та Кодування

Згідно зі стандартом RFC 6265, значення куки може містити обмежений набір символів. Пробіли, коми, крапки з комою та Non-ASCII символи заборонені або можуть інтерпретуватися неправильно різними браузерами.

**Як це робить `js-cookie`:**
Коли ви викликаєте `Cookies.set('key', 'val ue')`, бібліотека автоматично застосовує `encodeURIComponent` до значення (але не до всіх символів!).

Вона використовує **м'яке кодування**:

1.  Символи, дозволені RFC 6265, залишаються як є: `! # $ & ' ( ) * + - . / : < = > ? @ [ ] ^ _ { } | ~`.
2.  Замінюються лише "небезпечні" символи: `%` (процент), `;` (сепаратор), `,` (кома у старих браузерах), `\` (бексліш) та контрольні символи.

Це робить куки максимально читабельними для сервера, на відміну від повного `encodeURIComponent`, який перетворив би все на кашу з відсотків.

```javascript
// js-cookie
Cookies.set('a', '{b:c}')
// Результат в браузері: a=%7Bb%3Ac%7D
// (фігурні дужки кодуються, двокрапка - ні, якщо це дозволено)
```

### 8.2. Читання та Декодування

При читанні `Cookies.get('key')`, бібліотека бере сирий рядок `document.cookie`, розбиває його по `; ` і шукає потрібну пару.

**Алгоритм пошуку:**

1.  Перебір всіх пар ключ=значення.
2.  Декодування ключа.
3.  Якщо ключ співпав — декодування значення (`decodeURIComponent`).
4.  Повернення результату.

Зверніть увагу: якщо значення куки було змінено іншим скриптом або сервером без правильного кодування, `js-cookie` може не розпізнати його або повернути raw value (залежить від конвертера).

---

## 9. Advanced Patterns: Архітектурні Рішення

Використовувати глобальний об'єкт `Cookies` напряму у великому проєкті — це моветон. Краще створити шар абстракції (Wrapper).

### 9.1. Типізований Сервіс (TypeScript)

Створимо сервіс, який гарантує, що ми використовуємо правильні ключі.

```typescript [src/services/cookie.service.ts]
import Cookies from 'js-cookie'

// 1. Визначаємо дозволені ключі
type CookieKeys = 'auth_token' | 'user_theme' | 'gdpr_consent'

// 2. Створюємо типізовані опції
interface CookieOptions {
    expires?: number | Date
    path?: string
    domain?: string
    secure?: boolean
    sameSite?: 'Strict' | 'Lax' | 'None'
}

export const CookieService = {
    // Обгортка над set
    set(key: CookieKeys, value: string, options?: CookieOptions) {
        Cookies.set(key, value, {
            path: '/',
            secure: location.protocol === 'https:', // автоматично secure для https
            ...options,
        })
    },

    // Обгортка над get
    get(key: CookieKeys): string | undefined {
        return Cookies.get(key)
    },

    // Обгортка над remove
    remove(key: CookieKeys, options?: CookieOptions) {
        Cookies.remove(key, { path: '/', ...options })
    },
}

// Використання
CookieService.set('user_theme', 'dark') // OK
// CookieService.set('wrong_key', 'val'); // Error: Argument of type '"wrong_key"' is not assignable...
```

**Переваги:**

-   **Type Safety**: Ви не помилитеся в назві ключа (typo).
-   **Centralized Config**: Дефолтні параметри (наприклад, `path: '/'`) задаються в одному місці.
-   **Refactoring**: Легко змінити бібліотеку під капотом, не змінюючи код у всьому проєкті.

### 9.2. Namespace Pattern (Простір імен)

Якщо на одному домені живе кілька додатків (наприклад, `admin` і `shop`), корисно додавати префікси до кук, щоб уникнути колізій.

Можна реалізувати це через кастомний конвертер, але простіше через обгортку:

```javascript
const APP_PREFIX = 'myapp_'

const AppCookies = {
    set: (key, val, opts) => Cookies.set(APP_PREFIX + key, val, opts),
    get: (key) => Cookies.get(APP_PREFIX + key),
    remove: (key, opts) => Cookies.remove(APP_PREFIX + key, opts),
}

AppCookies.set('token', '123')
// Браузер: myapp_token=123
```

---

## 10. Безпека: Що Варто Знати

Робота з куками на клієнті має свої обмеження безпеки.

### 10.1. HttpOnly Cookies

Ви **НЕ МОЖЕТЕ** прочитати `HttpOnly` куки через `js-cookie` (або будь-який JS). Це зроблено навмисно.

-   **HttpOnly**: Кука доступна _тільки_ серверу. Браузер автоматично додає її до запитів, але JS її "не бачить".
-   **Use Case**: Найбезпечніше місце для зберігання **Refresh Token**. Якщо хакер виконає XSS (впровадить свій скрипт), він не зможе вкрасти токен, бо `document.cookie` його не покаже.

::caution
Якщо ваш API віддає токен авторизації як `HttpOnly` куку, `Cookies.get('token')` поверне `undefined`. Це норма!
::

### 10.2. XSS (Cross-Site Scripting)

Будь-яка кука, доступна через JS (`HttpOnly: false`), може бути вкрадена, якщо на вашому сайті є XSS вразливість.

**Рекомендації:**

1.  **Не зберігайте чутливі дані** (паролі, дані карток, PII) у звичайних куках.
2.  Використовуйте `Secure: true` для всіх важливих кук.
3.  Використовуйте `SameSite: Strict` або `Lax` для захисту від CSRF.

---

## 11. Практичний Кейс: GDPR Consent Banner

Давайте створимо повноцінний компонент логіки для банера згоду на використання кук. Це вимога закону в ЄС та багатьох інших регіонах.

**Логіка:**

1.  При старті перевіряємо, чи є кука `cookie_consent`.
2.  Якщо немає — показуємо банер.
3.  Якщо користувач тисне "OK", ставимо куку на 1 рік і ховаємо банер.

```javascript [utils/consent.js]
import Cookies from 'js-cookie'

const CONSENT_COOKIE = 'cookie_consent_status'

export class ConsentManager {
    constructor(bannerElement) {
        this.banner = bannerElement
        this.btnAccept = this.banner.querySelector('#acceptCookies')
        this.btnReject = this.banner.querySelector('#rejectCookies')

        this.init()
    }

    init() {
        // Перевіряємо статус
        const status = Cookies.get(CONSENT_COOKIE)

        if (!status) {
            this.showBanner()
        } else {
            console.log(`Consent status: ${status}`)
            this.applyConsent(status)
        }

        // Біндимо події
        this.btnAccept?.addEventListener('click', () => this.handleConsent('granted'))
        this.btnReject?.addEventListener('click', () => this.handleConsent('denied'))
    }

    showBanner() {
        this.banner.classList.remove('hidden')
    }

    hideBanner() {
        this.banner.classList.add('hidden')
    }

    handleConsent(status) {
        // Зберігаємо вибір на 365 днів
        Cookies.set(CONSENT_COOKIE, status, {
            expires: 365,
            sameSite: 'Lax',
            secure: true,
        })

        this.hideBanner()
        this.applyConsent(status)
    }

    applyConsent(status) {
        if (status === 'granted') {
            this.enableAnalytics()
        } else {
            this.disableAnalytics()
        }
    }

    enableAnalytics() {
        console.log('Google Analytics/Pixel loaded...')
        // Тут код завантаження скриптів аналітики
    }

    disableAnalytics() {
        console.log('Analytics disabled respecting user choice.')
        // Видаляємо аналітичні куки, якщо вони були
        Cookies.remove('_ga')
        Cookies.remove('_gid')
    }
}
```

Цей клас капсулює всю логіку і робить ваш код чистим.

---

---

## 12. Інтеграція з Фреймворками (React & Vue)

`js-cookie` — це ванільна JS бібліотека, але в екосистемі компонентів ми хочемо реактивність. Давайте напишемо обгортки (Wrappers).

### 12.1. React Hook: `useCookie`

Ми хочемо хук, який не просто читає куку, а й оновлює компонент при її зміні.

**Застереження**: `js-cookie` не має івентів зміни кук. Ми можемо реагувати лише на зміни, зроблені через наш хук, або використовувати `setInterval` (що погано). Найкращий паттерн — це єдине джерело правди.

```typescript [src/hooks/useCookie.ts]
import { useState, useCallback } from 'react'
import Cookies from 'js-cookie'

export default function useCookie(name: string, defaultValue: string) {
    const [value, setValue] = useState<string>(() => {
        const cookie = Cookies.get(name)
        return cookie || defaultValue
    })

    const updateCookie = useCallback(
        (newValue: string, options?: Cookies.CookieAttributes) => {
            Cookies.set(name, newValue, options)
            setValue(newValue)
        },
        [name],
    )

    const deleteCookie = useCallback(() => {
        Cookies.remove(name)
        setValue('') // або null, залежить від вашої логіки
    }, [name])

    return [value, updateCookie, deleteCookie] as const
}
```

**Використання в компоненті:**

```tsx [src/components/ThemeToggler.tsx]
import React from 'react'
import useCookie from '../hooks/useCookie'

const ThemeToggler = () => {
    const [theme, setTheme, removeTheme] = useCookie('theme', 'light')

    return (
        <div>
            <p>Current Theme: {theme}</p>
            <button onClick={() => setTheme('light')}>Light</button>
            <button onClick={() => setTheme('dark')}>Dark</button>
            <button onClick={removeTheme}>Reset</button>
        </div>
    )
}
```

### 12.2. Vue Composable: `useCookie`

В Vue 3 Composition API це виглядає ще елегантніше завдяки `ref` та `watch`.

```typescript [src/composables/useCookie.ts]
import { ref, watch } from 'vue'
import Cookies from 'js-cookie'

export function useCookie(name: string, defaultValue: string = '') {
    // Ініціалізація
    const cookieValue = Cookies.get(name) || defaultValue
    const cookieRef = ref(cookieValue)

    // Слідкуємо за змінами змінної і пишемо в куки
    watch(cookieRef, (newValue) => {
        if (newValue === null || newValue === undefined) {
            Cookies.remove(name)
        } else {
            Cookies.set(name, newValue)
        }
    })

    return cookieRef
}
```

**Використання:**

```vue [src/components/LanguageSwitcher.vue]
<script setup lang="ts">
    import { useCookie } from '../composables/useCookie'

    const lang = useCookie('app_lang', 'en')
</script>

<template>
    <select v-model="lang">
        <option value="en">English</option>
        <option value="uk">Ukrainian</option>
    </select>
</template>
```

---

## 13. Тестування (Unit Testing)

Як тестувати код, що залежить від `js-cookie`, у Jest або Vitest? Ми не хочемо, щоб тести залежали від реального браузерного середовища або забруднювали його.

### Підхід 1: Мокання (Mocking)

Найпростіший спосіб — замокати всю бібліотеку.

```javascript [src/services/__tests__/auth.test.js]
import { AuthService } from '../auth'
import Cookies from 'js-cookie'

// Автоматичний мок всіх методів бібліотеки
vi.mock('js-cookie')

describe('AuthService', () => {
    it('should save token to cookies on login', () => {
        const token = 'fake-jwt-token'
        AuthService.login(token)

        // Перевіряємо, чи був викликаний метод set
        expect(Cookies.set).toHaveBeenCalledWith('auth_token', token, expect.any(Object))
    })

    it('should read token from cookies', () => {
        // Налаштовуємо мок на повернення значення
        Cookies.get.mockReturnValue('stored-token')

        const token = AuthService.getToken()
        expect(token).toBe('stored-token')
    })
})
```

### Підхід 2: Реальна імплементація з JSDOM

Якщо ви використовуєте `jsdom` (дефолт для Vitest/Jest для фронтенду), `document.cookie` там працює! `js-cookie` буде працювати "як справжній".

Але тут є ризик: тести можуть впливати один на одного (shared state). Треба чистити куки після кожного тесту.

```javascript
afterEach(() => {
    // Очистка всіх кук
    Object.keys(Cookies.get()).forEach((cookieName) => {
        Cookies.remove(cookieName)
    })
})
```

---

## 14. SSR (Server-Side Rendering) та Hydration

Якщо ви використовуєте Next.js, Nuxt або Remix, ви зіткнетесь із проблемою: `js-cookie` працює з `document`, якого **не існує на сервері**.

### Проблема "Window is not defined"

Якщо ви спробуєте імпортувати і використати `js-cookie` в коді, який виконується під час серверного рендерингу (наприклад, у верхній частині компонента), ви отримаєте помилку.

**Правильне використання в SSR:**

1.  **Виконувати тільки в ефектах (Effects/Mounted):** `useEffect` (React) або `onMounted` (Vue) гарантовано запускаються тільки в браузері.
2.  **Перевірка середовища:**

```javascript
const isBrowser = typeof window !== 'undefined'

if (isBrowser) {
    Cookies.set('foo', 'bar')
}
```

### Синхронізація (Hydration Mismatch)

Якщо ви рендерите HTML на сервері на основі куки (наприклад, "Темна тема"), а на клієнті `js-cookie` ще не встиг прочитати куку, ви отримаєте миготіння (Flash of Incorrect Content) або помилку гідратації.

**Рішення для Next.js:** Використовуйте спеціалізовані бібліотеки (`nookies` або `cookies-next`), які вміють читати куки з `Server Request Headers` і передавати їх у пропси.

Для суто клієнтських задач (наприклад, збереження стану закритого банера) `js-cookie` в `useEffect` — ідеальний варіант.

---

## 15. Практичний Кейс: A/B Тестування

Маркетологи часто просять провести A/B тест. Покажемо 50% користувачів червону кнопку, а 50% — зелену, і збережемо вибір, щоб він не змінювався при оновленні сторінки.

```javascript [utils/ab-test.js]
import Cookies from 'js-cookie'

const TEST_NAME = 'ab_button_color'
const VARIANTS = ['red', 'green']

export function getVariant() {
    // 1. Пробуємо отримати вже призначений варіант
    let variant = Cookies.get(TEST_NAME)

    // 2. Якщо вже є і він валідний — повертаємо
    if (variant && VARIANTS.includes(variant)) {
        return variant
    }

    // 3. Якщо немає — жеребкування (50/50)
    variant = Math.random() < 0.5 ? 'red' : 'green'

    // 4. Зберігаємо результат "навічно" (наприклад, 30 днів)
    // Важливо: використовуємо SameSite Lax, щоб не губити тест при зовнішніх переходах
    Cookies.set(TEST_NAME, variant, { expires: 30, sameSite: 'Lax', path: '/' })

    // 5. Логуємо подію аналітики (псевдокод)
    console.log(`[Analytics] Assigned A/B variant: ${variant}`)

    return variant
}
```

**Використання:**

```javascript
/* main.js */
import { getVariant } from './utils/ab-test'

const color = getVariant()
document.querySelector('.buy-button').style.backgroundColor = color
```

Цей код гарантує **Consistency** (постійність). Користувач не побачить, як кнопка змінить колір при наступному візиті.

---

## 16. FAQ: Часті Питання та Ліміти

### Який максимальний розмір куки?

Згідно RFC, мінімально гарантований розмір — **4096 байт (4KB)**. Це включає назву, значення та атрибути. Якщо ви спробуєте записати більше, кука просто не збережеться (тихо відпаде).

### Скільки кук можна створити?

Ліміти різняться, але "безпечна" цифра — **20 кук на домен**. Chrome дозволяє до 180, але не варто на це покладатися.

### Чи можна зберігати масиви?

Нативно — ні, це просто рядок. Але з `js-cookie` ви можете передати масив `['a', 'b']`, і він автоматично конвертується в JSON-рядок.

```javascript
Cookies.set('ids', [1, 2, 3])
const ids = Cookies.getJSON('ids') // [1, 2, 3]
```

### Чому кука не зберігається в Chrome на localhost?

Chrome має суворі політики щодо `Secure` cookies. Якщо ви тестуєте на `http://localhost` і ставите `secure: true`, кука може не зберегтися.
У нових версіях `localhost` вважається "безпечним контекстом", тому це мало б працювати, але якщо виникають проблеми — спробуйте прибрати `secure` для дев-режиму.

---

## 17. Troubleshooting (Вирішення Проблем)

Типові ситуації, коли щось йде не так.

### Проблема 1: Кука не встановлюється

-   **Причина:** Ви намагаєтесь поставити `Secure` куку на `http://` (не localhost).
-   **Рішення:** Використовуйте HTTPS або тестуйте на `localhost`.
-   **Причина 2:** Розмір куки перевищує 4KB.
-   **Рішення:** Куки не для великих даних. Використовуйте `localStorage` або `IndexedDB`.

### Проблема 2: Кука не видаляється

-   **Причина:** Неспівпадіння `path` або `domain`.
-   **Рішення:** Перевірте DevTools -> Application -> Cookies. Подивіться на стовпчики Path/Domain. Виклик `remove()` має точно їх дублювати.

### Проблема 3: JSON повертає рядок

-   **Причина:** Ви записали куку не через `js-cookie` (наприклад, сервер PHP/Node), і формат не відповідає очікуваному (зайві символи, інше кодування).
-   **Рішення:** Використовуйте кастомний конвертер або парсіть вручну через `try/catch`.

---

## 18. js-cookie vs Native API: Фінальне Порівняння

| Критерій        | Native `document.cookie`         | `js-cookie`                       |
| :-------------- | :------------------------------- | :-------------------------------- |
| **Читання**     | Складний парсинг рядка, Regex    | `Cookies.get('name')`             |
| **Запис**       | Ручне формування рядка           | `Cookies.set('name', 'val')`      |
| **Кодування**   | Ручне `encodeURIComponent`       | Автоматичне                       |
| **Типи даних**  | Тільки String                    | Підтримка JSON (через конвертери) |
| **Видалення**   | Встановлення дати в минуле (хак) | `Cookies.remove('name')`          |
| **Розмір коду** | Багато бойлерплейту              | 1 рядок                           |

`js-cookie` — це той випадок, коли маленька бібліотека економить години налагодження і кілометри нервів.

---

---

## 19. Словник Термінів

Щоб говорити однією мовою з колегами, запам'ятайте ці визначення:

-   **Cookie (Кука)**: Невеликий фрагмент даних (< 4KB), який сервер надсилає браузеру для збереження. Браузер повертає його при кожному наступному запиті до того ж сервера.
-   **Session Cookie**: Тимчасова кука, яка живе лише до закриття вкладки або браузера. Не має атрибута `Expires` або `Max-Age`.
-   **Persistent Cookie**: "Вічна" кука, яка зберігається на диску користувача до вказаної дати (`Expires`). Цінна для "Remember Me".
-   **HttpOnly**: Прапор безпеки. Така кука недоступна через JavaScript (`document.cookie`), що захищає її від крадіжки через XSS.
-   **Secure**: Прапор, що дозволяє передачу куки лише через шифроване з'єднання (HTTPS).
-   **SameSite**: Атрибут, що контролює передачу кук при запитах з інших сайтів (Cross-Site). Головний захист від CSRF атак.
-   **Domain**: Визначає область видимості куки. Кука, встановлена для `.google.com`, буде доступна і для `mail.google.com`.
-   **Path**: Обмежує видимість куки певною директорією URL (наприклад, `/admin`).
-   **Third-party Cookie**: Кука, встановлена доменом, відмінним від того, на якому зараз знаходиться користувач (наприклад, Facebook Pixel на сайті новин).

---

## Перевірка знань

Закріпіть отримані знання про `js-cookie`:

::tally-embed{id="w7Xj0y" title="js-cookie Quiz"}
::
