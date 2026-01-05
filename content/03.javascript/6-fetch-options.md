---
title: Fetch API - Повний довідник опцій
description: Вичерпний довідник усіх опцій Fetch API - referrer, mode, credentials, cache, redirect, integrity та keepalive з практичними прикладами
---

# Fetch API - Повний довідник опцій

## Вступ та Контекст

На цей момент ми вже детально розглянули основи Fetch API: базові запити, FormData, відстеження прогресу, переривання та CORS. Але Fetch API має набагато більше можливостей через додаткові опції конфігурації.

**Важливо:** Більшість цих опцій використовуються рідко і потрібні лише для спеціалізованих сценаріїв. Ви можете успішно працювати з fetch, знаючи лише базові опції. Цей розділ — довідник для особливих випадків.

::note
**Коли повертатися до цього розділу?**

-   Потрібно контролювати кешування
-   Треба налаштувати Referer header
-   Важлива валідація цілісності файлів (integrity)
-   Потрібні аналітичні запити, які "переживають" закриття сторінки
    ::

## Повний синтаксис Fetch

Ось всі можливі опції з їх значеннями за замовчуванням:

```javascript
const response = await fetch(url, {
    // Основні опції (розглянуті раніше)
    method: 'GET', // POST, PUT, DELETE, PATCH
    headers: {}, // об'єкт або Headers
    body: undefined, // string, FormData, Blob, URLSearchParams
    signal: undefined, // AbortController.signal

    // Безпека та CORS
    mode: 'cors', // 'same-origin', 'no-cors'
    credentials: 'same-origin', // 'omit', 'include'

    // Referer
    referrer: 'about:client', // '' (не відправляти) або URL
    referrerPolicy: 'strict-origin-when-cross-origin',

    // Кешування
    cache: 'default', // 'no-store', 'reload', 'no-cache', etc.

    // Переадресація
    redirect: 'follow', // 'error', 'manual'

    // Валідація цілісності
    integrity: '', // наприклад, 'sha256-abc123...'

    // Keepalive
    keepalive: false, // true для аналітики

    // Застарілі/рідковживані
    window: window, // null
})
```

::field-group
::field{name="method" type="string"}
HTTP метод: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
::

::field{name="headers" type="object | Headers"}
Об'єкт з HTTP headers або екземпляр `Headers`
::

::field{name="body" type="any"}
Тіло запиту: `string`, `FormData`, `Blob`, `URLSearchParams`
::

::field{name="signal" type="AbortSignal"}
Сигнал від `AbortController` для переривання
::
::

## Referrer та Referrer Policy

### Що таке Referer?

**Referer** (так, з помилкою в назві) — HTTP header, який містить URL сторінки, з якої був зроблений запит.

```http
GET /api/data HTTP/1.1
Host: api.example.com
Referer: https://mysite.com/admin/dashboard
```

**Навіщо?** Сервер бачить, звідки прийшов запит (для аналітики, безпеки).

**Проблема:** Може розкривати чутливу інформацію з URL (наприклад, `/admin/secret-page`).

### Опція `referrer`

Дозволяє встановити або приховати Referer:

```javascript
// Не відправляти Referer взагалі
fetch('/api/data', {
    referrer: '',
})

// Встановити власне значення (в межах того самого origin)
fetch('/api/data', {
    referrer: 'https://mysite.com/public-page',
})
```

::caution
**Обмеження referrer**

Ви можете встановити `referrer` тільки на URL **вашого власного origin**. Неможливо підробити Referer на чужий домен.

```javascript
// ✅ Можна (той самий origin)
fetch('/api', { referrer: 'https://mysite.com/page' })

// ❌ Буде ігноровано (інший origin)
fetch('/api', { referrer: 'https://evil.com' })
```

::

### Опція `referrerPolicy`

Встановлює загальні правила для Referer header:

| Policy                               | Same-Origin | Cross-Origin | HTTPS→HTTP  |
| :----------------------------------- | :---------- | :----------- | :---------- |
| `no-referrer`                        | —           | —            | —           |
| `no-referrer-when-downgrade`         | Full URL    | Full URL     | —           |
| `origin`                             | Origin only | Origin only  | Origin only |
| `origin-when-cross-origin`           | Full URL    | Origin only  | Origin only |
| `same-origin`                        | Full URL    | —            | —           |
| `strict-origin`                      | Origin only | Origin only  | —           |
| `strict-origin-when-cross-origin` ⭐ | Full URL    | Origin only  | —           |
| `unsafe-url`                         | Full URL    | Full URL     | Full URL    |

⭐ Значення за замовчуванням

**Пояснення значень:**

-   **Full URL**: `https://site.com/admin/dashboard`
-   **Origin only**: `https://site.com`
-   **—**: не відправляти Referer

**Приклад: приховування шляху від зовнішніх сайтів**

```javascript
// Для cross-origin відправляємо лише origin, без шляху
fetch('https://external-api.com/data', {
    referrerPolicy: 'origin-when-cross-origin',
})

// Referer буде: https://mysite.com (без /admin/secret)
```

**Приклад: повна приватність**

```javascript
// Ніколи не відправляти Referer
fetch('/api/data', {
    referrerPolicy: 'no-referrer',
})
```

## Mode - Контроль CORS

Опція `mode` контролює, чи дозволені cross-origin запити:

```javascript
fetch(url, {
    mode: 'cors' | 'same-origin' | 'no-cors',
})
```

### Значення

**`'cors'` (за замовчуванням)**

Дозволяє cross-origin запити з CORS headers:

```javascript
fetch('https://api.github.com/users/octocat', {
    mode: 'cors', // дозволено
})
```

**`'same-origin'`**

Заборонює будь-які cross-origin запити:

```javascript
fetch('https://external-api.com/data', {
    mode: 'same-origin',
})
// ❌ TypeError: Failed to fetch
```

**`'no-cors'`**

Дозволяє лише "безпечні" cross-origin запити БЕЗ доступу до відповіді:

```javascript
const response = await fetch('https://example.com/image.jpg', {
    mode: 'no-cors',
})

console.log(response.status) // 0
console.log(await response.text()) // Помилка - доступ заборонено!
```

::warning
**`no-cors` - не те, що ви думаєте**

Багато розробників помилково використовують `mode: 'no-cors'`, думаючи, що це "вимкне CORS". Насправді це робить відповідь **opaque** (непрозорою) — ви не можете прочитати дані!

✅ **Використовуйте `no-cors` лише для:**

-   Завантаження ресурсів без читання (наприклад, зображення для кешування)
-   Logging/Analytics запитів, де відповідь не важлива

❌ **НЕ використовуйте для:**

-   Отримання даних API
-   Будь-яких запитів, де потрібна відповідь
    ::

## Credentials - Cookies та Authentication

Контролює відправку cookies та HTTP Authentication:

```javascript
fetch(url, {
    credentials: 'same-origin' | 'include' | 'omit',
})
```

### Значення

**`'same-origin'` (за замовчуванням)**

Cookies відправляються лише для same-origin запитів:

```javascript
// ✅ Cookies відправляються
fetch('/api/profile')

// ❌ Cookies НЕ відправляються
fetch('https://external-api.com/data')
```

**`'include'`**

Завжди відправляти cookies (навіть cross-origin):

```javascript
fetch('https://api.mybackend.com/profile', {
    credentials: 'include',
})
```

Сервер має відповісти:

```http
Access-Control-Allow-Origin: https://mysite.com
Access-Control-Allow-Credentials: true
```

**`'omit'`**

Ніколи не відправляти cookies (навіть same-origin):

```javascript
fetch('/api/public-data', {
    credentials: 'omit', // Без cookies
})
```

### Приклад: Авторизований API запит

```javascript
async function getUUserProfile() {
    const response = await fetch('https://api.myapp.com/user/profile', {
        credentials: 'include', // Відправити session cookie
        headers: {
            Accept: 'application/json',
        },
    })

    if (!response.ok) {
        throw new Error('Not authenticated')
    }

    return response.json()
}
```

## Cache - Контроль HTTP кешування

Керує взаємодією з HTTP-кешем браузера:

```javascript
fetch(url, {
    cache: 'default' | 'no-store' | 'reload' | 'no-cache' | 'force-cache' | 'only-if-cached',
})
```

### Значення

| Режим            | Опис                                | Коли використовувати  |
| :--------------- | :---------------------------------- | :-------------------- |
| `default`        | Стандартне HTTP кешування           | 99% випадків          |
| `no-store`       | Не кешувати запит і відповідь       | Чутливі дані          |
| `reload`         | Ігнорувати кеш, але оновити його    | "Примусове оновлення" |
| `no-cache`       | Валідувати кеш, потім використати   | Актуальні дані        |
| `force-cache`    | Використати кеш (навіть застарілий) | Офлайн режим          |
| `only-if-cached` | Тільки кеш, помилка якщо немає      | Повний офлайн         |

### Приклади

**Завжди свіжі дані (без кешу)**

```javascript
fetch('/api/stock-prices', {
    cache: 'no-store', // Ніколи не кешувати
})
```

**Примусове оновлення (hard reload)**

```javascript
fetch('/api/config', {
    cache: 'reload', // Ігнорувати кеш, оновити його
})
```

**Офлайн-режим (використовувати кеш)**

```javascript
fetch('/api/articles', {
    cache: 'force-cache', // Використати кеш, навіть якщо застарілий
}).catch(() => {
    console.log('Немає інтернету, використано кеш')
})
```

## Redirect - Processing Переадресацій

Контролює обробку HTTP redirects (301, 302, 307, 308):

```javascript
fetch(url, {
    redirect: 'follow' | 'error' | 'manual',
})
```

### Значення

**`'follow'` (за замовчуванням)**

Автоматично слідувати redirects:

```javascript
fetch('http://example.com/old-url', {
    redirect: 'follow',
})
// Автоматично перейде на новий URL
```

**`'error'`**

Генерувати помилку при redirect:

```javascript
fetch('http://example.com/old-url', {
    redirect: 'error',
})
// TypeError: Failed to fetch (якщо є redirect)
```

**`'manual'`**

Дозволяє обробляти redirects вручну:

```javascript
const response = await fetch('http://example.com/old-url', {
    redirect: 'manual',
})

if (response.type === 'opaqueredirect') {
    console.log('Redirect виявлено, але не обробленосправжнього статусу немає')
    // response.status === 0
    // response.url === ''
}
```

::note
**Коли використовувати `manual`?**

Рідко потрібно. Може бути корисно для:

-   Відстеження ланцюжків redirects
-   Спеціальної логіки переадресацій
-   Debugging redirect loops
    ::

## Integrity - Перевірка цілісності

Валідує, що завантажений ресурс відповідає очікуваній контрольній сумі (hash):

```javascript
fetch(url, {
    integrity: 'sha256-{hash}' | 'sha384-{hash}' | 'sha512-{hash}',
})
```

### Як це працює

1. Ви знаєте заздалегідь hash файлу
2. Передаєте його у `integrity`
3. Браузер завантажує файл та обчислює hash
4. Якщо hash не збігається → помилка

### Приклад: Завантаження CDN скрипта

```javascript
// Завантажуємо jQuery з CDN з перевіркою integrity
fetch('https://code.jquery.com/jquery-3.7.1.min.js', {
    integrity: 'sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=',
})
    .then((r) => r.text())
    .then((code) => {
        console.log('jQuery завантажено та перевірено!')
        eval(code) // Безпечно, бо перевірили hash
    })
    .catch((error) => {
        console.error('Hash не збігається! Можлива модифікація файлу.')
    })
```

### Генерація hash

**Онлайн:**
Використовуйте [SRI Hash Generator](https://www.srihash.org/)

**Командний рядок:**

```bash
# Для файлу
curl https://code.jquery.com/jquery-3.7.1.min.js | openssl dgst -sha256 -binary | openssl base64 -A

# Результат: sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=
```

::tip
**Subresource Integrity (SRI)**

`integrity` — це реалізація SRI специфікації. Це особливо важливо для:

-   Завантаження скриптів з CDN
-   Гарантування, що файли не змінені
-   Захисту від компрометації CDN
    ::

## Keepalive - Запити після закриття сторінки

Дозволяє запиту "пережити" закриття сторінки:

```javascript
fetch(url, {
    keepalive: true,
})
```

### Проблема

Коли користувач закриває вкладку, браузер **скасовує всі активні запити**:

```javascript
window.addEventListener('unload', () => {
    fetch('/analytics', {
        method: 'POST',
        body: JSON.stringify({ event: 'page_close' }),
    })
    // ❌ Запит буде скасовано!
})
```

### Рішення: keepalive

```javascript
window.addEventListener('unload', () => {
    fetch('/analytics', {
        method: 'POST',
        body: JSON.stringify({ event: 'page_close' }),
        keepalive: true, // ✅ Запит завершиться навіть після закриття
    })
})
```

### Обмеження

1. **Розмір:** Максимум 64KB для тіла запиту
2. **Множинні запити:** Загальний ліміт 64KB для всіх keepalive зараз
3. **Відповідь:** Ви не можете прочитати відповідь (сторінка вже закрита)

### Приклад: Аналітика відвідувань

```javascript
class Analytics {
    constructor() {
        this.events = []

        // Відправляти при закритті сторінки
        window.addEventListener('beforeunload', () => {
            this.flush()
        })

        // Або кожні 30 секунд
        setInterval(() => this.flush(), 30000)
    }

    track(eventName, data) {
        this.events.push({
            event: eventName,
            data,
            timestamp: Date.now(),
        })

        // Якщо багато подій, відправити зараз
        if (this.events.length >= 10) {
            this.flush()
        }
    }

    flush() {
        if (this.events.length === 0) return

        const payload = JSON.stringify(this.events)

        // Перевірка ліміту 64KB
        if (new Blob([payload]).size > 64 * 1024) {
            console.warn('Payload занадто великий для keepalive')
            return
        }

        fetch('/api/analytics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: payload,
            keepalive: true,
        })

        this.events = []
    }
}

// Використання
const analytics = new Analytics()

analytics.track('page_view', { url: location.href })
analytics.track('button_click', { button: 'signup' })
```

::warning
**Альтернатива: navigator.sendBeacon()**

Для аналітичних запитів часто краще використовувати `navigator.sendBeacon()`:

```javascript
window.addEventListener('beforeunload', () => {
    const data = JSON.stringify({ event: 'page_close' })
    navigator.sendBeacon('/analytics', data)
})
```

**Переваги sendBeacon:**

-   Спеціально розроблений для аналітики
-   Автоматично keepalive
-   Простіший API
-   Кращесь гарантії доставки
    ::

## Підсумки

Fetch API має багато опцій для тонкого налаштування:

::card-group
::card{title="Referrer Control" icon="i-lucide-link"}

```javascript
{
  referrer: '',  // Приховати
  referrerPolicy: 'no-referrer'
}
```

✅ Для приватності та безпеки
✅ Приховання внутрішньої структури URL

::

::card{title="Security & CORS" icon="i-lucide-shield"}

```javascript
{
  mode: 'same-origin',
  credentials: 'include'
}
```

✅ Контроль cross-origin запитів
✅ Керування cookies
::

::card{title="Caching" icon="i-lucide-database"}

```javascript
{
  cache: 'no-store', // no cache
  cache: 'reload',   // обійти кеш
  cache: 'force-cache' // offline
}
```

✅ Контроль свіжості даних
✅ Офлайн режим
::

::card{title="Integrity & Keepalive" icon="i-lucide-check-circle"}

```javascript
{
  integrity: 'sha256-abc...',
  keepalive: true
}
```

✅ Валідація файлів з CDN
✅ Аналітика при закритті

::
::

### Швидка довідка опцій

| Опція            | Значення за замовчуванням           | Основні альтернативи                   |
| :--------------- | :---------------------------------- | :------------------------------------- |
| `method`         | `'GET'`                             | `POST`, `PUT`, `DELETE`, `PATCH`       |
| `headers`        | `{}`                                | Об'єкт або `Headers` instance          |
| `body`           | `undefined`                         | `string`, `FormData`, `Blob`           |
| `mode`           | `'cors'`                            | `'same-origin'`, `'no-cors'`           |
| `credentials`    | `'same-origin'`                     | `'include'`, `'omit'`                  |
| `cache`          | `'default'`                         | `'no-store'`, `'reload'`, `'no-cache'` |
| `redirect`       | `'follow'`                          | `'error'`, `'manual'`                  |
| `referrer`       | `'about:client'`                    | `''` (не відправляти), URL             |
| `referrerPolicy` | `'strict-origin-when-cross-origin'` | `'no-referrer'`, `'origin'`            |
| `integrity`      | `''`                                | `'sha256-...'`, `'sha384-...'`         |
| `keepalive`      | `false`                             | `true`                                 |
| `signal`         | `undefined`                         | `AbortController.signal`               |

### Коли використовувати рідкісні опції

✅ **`referrerPolicy`:**

-   Захист приватних URL від витоку
-   Безпека admin-панелей

✅ **`cache: 'no-store'`:**

-   Фінансові дані
-   Персональна інформація
-   Реал-тайм pricing

✅ **`integrity`:**

-   Завантаження з CDN
-   Критичні безпекові скрипти

✅ **`keepalive`:**

-   Аналітика відвідувань
-   Логування помилок при закритті
-   A/B тестування metrics

❌ **Не використовувати без потреби:**

-   `mode: 'no-cors'` (майже ніколи не потрібен)
-   `redirect: 'manual'` (складна обробка)
-   Надто агресивний кешинг (`force-cache`)

Більшість проектів чудово працюють з базовими опціями (`method`, `headers`, `body`, `signal`). Використовуйте розширені опції лише коли є конкретна потреба, а не "на всяк випадок".

## Додаткові ресурси

-   [MDN: Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) — повна документація
-   [Fetch Standard](https://fetch.spec.whatwg.org/) — офіційна специфікація
-   [MDN: Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) — інтерфейс Request
-   [Referrer Policy Spec](https://w3c.github.io/webappsec-referrer-policy/) — специфікація Referrer Policy
-   [Subresource Integrity](https://w3c.github.io/webappsec-subresource-integrity/) — SRI специфікація
