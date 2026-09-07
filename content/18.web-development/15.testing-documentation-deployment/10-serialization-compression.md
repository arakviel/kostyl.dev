# Серіалізація та компресія

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати `ClassSerializerInterceptor` для автоматичної трансформації entities у JSON responses.
- Навчитися використовувати `@Exclude()` та `@Expose()` декоратори для контролю serialization.
- Освоїти transformation groups для різних контекстів (admin, user, public).
- Зрозуміти compression middleware для зменшення розміру HTTP responses.
- Ознайомитися з концепціями payment integration (Stripe, LiqPay, Fondy).

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Serialization:** перетворення JavaScript об'єктів у JSON для HTTP response.
- **Class Transformer:** бібліотека для декларативної трансформації об'єктів через decorators.
- **Compression:** стиснення HTTP responses (gzip, deflate) для зменшення bandwidth.
- **Transformation Groups:** умовна serialization на основі контексту (admin vs user).
- **Idempotency Key:** унікальний ідентифікатор для запобігання duplicate payments.

::

::

---

## Короткий зміст

У цій лекції вивчається оптимізація HTTP відповідей через трансформацію даних та стиснення:

- **ClassSerializerInterceptor** — автоматична трансформація entities у JSON, використання class-transformer декораторів, глобальна реєстрація через `app.useGlobalInterceptors()`, працює з Plain-to-Class transformation
- **@Exclude() декоратор** — виключення полів з response (password, internal fields), захист sensitive data, застосування на рівні класу або property, можливість exclude за умовою
- **@Expose() декоратор** — явне включення полів у response, whitelist підхід для максимальної безпеки, computed properties через @Expose() getter methods
- **Transformation groups** — різні серіалізації для різних контекстів, groups: 'admin', 'user', 'public', декоратор `@SerializeOptions({ groups: ['admin'] })` на контролері, conditional exposure через groups
- **Type transformation** — автоматичне перетворення типів (Date → ISO string, BigInt → string), custom transformers через @Transform() декоратор, nested object transformation
- **Compression middleware** — стиснення HTTP responses через compression package, підтримка gzip та deflate, автоматичне визначення Accept-Encoding, threshold для мінімального розміру response
- **Response interceptors** — custom interceptors для трансформації структури response, wrapping data у {success, data, metadata}, error normalization, pagination metadata injection
- **Огляд платіжних інтеграцій** — Stripe для міжнародних платежів (webhooks, subscription billing), LiqPay для України (checkout widget, callback handling), Fondy для СНД (tokenization, recurring payments), загальні концепції: idempotency keys, webhook verification, PCI compliance

Розглядаються практичні приклади: налаштування ClassSerializerInterceptor, hiding password field, groups для admin/user responses, compression для великих payloads, integration з payment providers.

---

## Проблема неконтрольованої serialization

Базовий NestJS контролер повертає entities «як є»:

```typescript
@Get(':id')
async findOne(@Param('id') id: string) {
  return this.usersService.findOne(id);
}
```

**Response містить ВСЕ поля entity:**

```json
{
  "id": "user-123",
  "email": "user@example.com",
  "password": "$2b$10$N9qo8uLOickgx2...", // ❌ Небезпечно!
  "isAdmin": true,
  "createdAt": "2024-01-15T14:23:45.123Z",
  "updatedAt": "2024-01-15T14:23:45.123Z",
  "_internalFlag": true // ❌ Не має бути у публічному API
}
```

**Проблеми:**

1. **Security риски** — password hash потрапляє у response.
2. **Відсутність контролю** — немає різниці між admin та user responses.
3. **Зайві дані** — клієнт отримує internal fields.
4. **Великі payloads** — неоптимізовані responses споживають bandwidth.

**Рішення:**

1. **ClassSerializerInterceptor** — автоматична трансформація через decorators.
2. **Compression middleware** — стиснення responses для зменшення розміру.

---

## ClassSerializerInterceptor

`ClassSerializerInterceptor` автоматично трансформує entities у JSON, дотримуючись `class-transformer` decorators.

### Встановлення

```bash
npm install --save class-transformer class-validator
```

### Глобальна реєстрація

```typescript
// main.ts
import { ClassSerializerInterceptor, ValidationPipe } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));
  
  await app.listen(3000);
}
```

### @Exclude() — Приховування полів

```typescript
// entities/user.entity.ts
import { Exclude } from 'class-transformer';

export class User {
  id: string;
  email: string;
  
  @Exclude() // ❌ Не включається у response
  password: string;
  
  @Exclude()
  _internalFlag: boolean;
  
  isAdmin: boolean;
  createdAt: Date;
}
```

**Response тепер безпечний:**

```json
{
  "id": "user-123",
  "email": "user@example.com",
  "isAdmin": true,
  "createdAt": "2024-01-15T14:23:45.123Z"
}
```

### @Expose() — Whitelist підхід

Для максимальної безпеки використовуйте `@Expose()` з `excludeExtraneousValues`:

```typescript
import { Expose, Exclude } from 'class-transformer';

@Exclude() // За замовчуванням exclude всі поля
export class User {
  @Expose() // ✅ Явно expose
  id: string;
  
  @Expose()
  email: string;
  
  // password НЕ має @Expose() → автоматично excluded
  password: string;
  
  @Expose()
  isAdmin: boolean;
}
```

### Computed properties

```typescript
export class User {
  @Expose()
  id: string;
  
  firstName: string;
  lastName: string;
  
  @Expose()
  get fullName(): string {
    return `${this.firstName} ${this.lastName}`;
  }
}
```

**Response:**

```json
{
  "id": "user-123",
  "fullName": "John Doe"
}
```

---

## Transformation Groups

Різні serialization для різних ролей/контекстів.

### Entity з groups

```typescript
// entities/user.entity.ts
import { Expose, Exclude } from 'class-transformer';

export class User {
  @Expose({ groups: ['user', 'admin'] })
  id: string;
  
  @Expose({ groups: ['user', 'admin'] })
  email: string;
  
  @Exclude()
  password: string;
  
  @Expose({ groups: ['admin'] }) // Лише для admin
  isAdmin: boolean;
  
  @Expose({ groups: ['admin'] })
  lastLoginIp: string;
  
  @Expose({ groups: ['user', 'admin'] })
  createdAt: Date;
}
```

### Controller з @SerializeOptions

```typescript
// users/users.controller.ts
import { Controller, Get, UseInterceptors, ClassSerializerInterceptor } from '@nestjs/common';
import { SerializeOptions } from '@nestjs/common';

@Controller('users')
@UseInterceptors(ClassSerializerInterceptor)
export class UsersController {
  
  @Get('me')
  @SerializeOptions({ groups: ['user'] }) // User context
  async getProfile(@CurrentUser() user: User) {
    return user;
  }
  
  @Get('admin')
  @SerializeOptions({ groups: ['admin'] }) // Admin context
  async getAllUsers() {
    return this.usersService.findAll();
  }
}
```

**Response для GET /users/me (user):**

```json
{
  "id": "user-123",
  "email": "user@example.com",
  "createdAt": "2024-01-15T14:23:45.123Z"
}
```

**Response для GET /users/admin (admin):**

```json
{
  "id": "user-123",
  "email": "user@example.com",
  "isAdmin": true,
  "lastLoginIp": "192.168.1.100",
  "createdAt": "2024-01-15T14:23:45.123Z"
}
```

---

## Compression Middleware

Стиснення HTTP responses для зменшення bandwidth.

### Встановлення

```bash
npm install --save compression
npm install --save-dev @types/compression
```

### Інтеграція

```typescript
// main.ts
import * as compression from 'compression';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.use(compression({
    filter: (req, res) => {
      if (req.headers['x-no-compression']) {
        return false; // Skip compression
      }
      return compression.filter(req, res);
    },
    threshold: 1024, // Compress якщо response > 1KB
    level: 6, // Compression level (0-9)
  }));
  
  await app.listen(3000);
}
```

**Ефект:**

- Response 50KB → 5KB (gzip)
- Зменшення bandwidth на 90%
- Швидший завантаження для клієнтів

---

## Висновки

::card-group

::card{title="✅ Переваги Serialization" icon="i-lucide-check-circle"}

- **Security:** автоматичне приховування sensitive fields (password, tokens).
- **Flexibility:** різні responses для різних контекстів (admin vs user).
- **Type safety:** computed properties з TypeScript.
- **Performance:** compression зменшує bandwidth на 80-90%.

::

::card{title="⚠️ Поширені помилки" icon="i-lucide-alert-triangle"}

- **Забути @Exclude() для password** — security incident.
- **Відсутність groups** — admin fields доступні для users.
- **No compression** — великі payloads споживають bandwidth.

::

::

**Ключові висновки:**

- **Завжди exclude password** — використовуйте `@Exclude()`.
- **Groups для різних roles** — admin бачить більше, ніж user.
- **Compression обов'язковий** — зменшення response size на 90%.

---

## Часті запитання (FAQ)

::accordion

::accordion-item{title="Як працює compression з different Accept-Encoding?"}

Compression middleware автоматично визначає `Accept-Encoding` header:

- `gzip` — найпопулярніший (підтримка всіх браузерів)
- `deflate` — альтернатива
- `br` (Brotli) — новий, ефективніший (потребує окремий package)

::

::accordion-item{title="Чи впливає compression на performance?"}

**CPU overhead:** мінімальний для рівня 6 (default).

**Trade-off:**
- Витрати CPU на compression: +5-10ms
- Економія bandwidth: 80-90%
- Швидше завантаження: -200-500ms (залежить від connection speed)

**Рекомендація:** compression вимкнено для responses < 1KB (overhead > benefit).

::

::

**Додаткові ресурси:**

- [class-transformer Documentation](https://github.com/typestack/class-transformer)
- [Compression Best Practices](https://expressjs.com/en/advanced/best-practice-performance.html#use-gzip-compression)
