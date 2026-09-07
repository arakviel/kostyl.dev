# Passport.js стратегії у NestJS

## Короткий зміст

У цій лекції вивчається інтеграція бібліотеки Passport.js та реалізація стратегій автентифікації:

- **Концепція Passport.js** — модульна система стратегій автентифікації, інтеграція через `@nestjs/passport`, механізм валідації через метод `validate()`
- **Local Strategy** — автентифікація за email/паролем, створення `LocalStrategy extends PassportStrategy`, метод `validate(email, password)` для перевірки credentials, використання `AuthGuard('local')` на ендпоінті `/auth/login`
- **JWT Strategy** — захист маршрутів токеном, створення `JwtStrategy extends PassportStrategy`, конфігурація `ExtractJwt.fromAuthHeaderAsBearerToken()` для витягування токена з заголовка `Authorization: Bearer <token>`, метод `validate(payload)` для перетворення payload у `request.user`
- **AuthGuard** — декоратор `@UseGuards(AuthGuard('jwt'))` для захисту маршрутів, автоматичне додавання `request.user` після успішної валідації
- **Кастомні декоратори** — створення `@CurrentUser()` для зручного доступу до `request.user`, створення `@Public()` для позначення публічних маршрутів (без автентифікації), використання `Reflector` для читання метаданих

Розглядаються практичні приклади захисту CRUD операцій, отримання поточного користувача у контролерах, створення публічних ендпоінтів для реєстрації та логіну.

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати концепцію Passport.js як модульної системи для стратегій автентифікації різних типів.
- Навчитися створювати LocalStrategy для валідації email/пароля та JwtStrategy для верифікації токенів.
- Зрозуміти механізм роботи AuthGuard та його інтеграцію з Passport стратегіями.
- Реалізувати кастомні декоратори для елегантного доступу до даних користувача у контролерах.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Strategy (Стратегія):** клас, що інкапсулює логіку автентифікації для конкретного методу (Local, JWT, OAuth, SAML).
- **PassportStrategy:** базовий клас NestJS для створення кастомних стратегій через наслідування.
- **AuthGuard:** Guard, що активує Passport стратегію та блокує доступ при невдалій автентифікації.
- **validate() method:** метод стратегії, що викликається після успішної верифікації credentials/токена для завантаження додаткових даних.

::

::

---

## Концепція Passport.js: модульна автентифікація

Passport.js є middleware для Node.js, що надає **понад 500 готових стратегій** для автентифікації через різні методи: email/пароль, JWT токени, OAuth 2.0 (Google, Facebook, GitHub), SAML, OpenID Connect, Two-Factor Authentication та багато інших. Кожна стратегія інкапсульована у окремий npm пакет, що дозволяє підключати лише необхідні методи автентифікації.

### Філософія Passport: розділення відповідальностей

Passport дотримується принципу Single Responsibility — кожна стратегія відповідає за **один конкретний метод** верифікації облікових даних:

::mermaid

```mermaid
graph TB
    A[HTTP Request] --> B{Який AuthGuard?}
    
    B -->|AuthGuard local| C[LocalStrategy]
    B -->|AuthGuard jwt| D[JwtStrategy]
    B -->|AuthGuard google| E[GoogleOAuthStrategy]
    
    C -->|validate email/password| F[UsersService]
    D -->|verify JWT signature| D
    E -->|validate OAuth token| G[Google API]
    
    F -->|User entity| H[request.user]
    D -->|JWT payload| H
    G -->|User profile| H
    
    H --> I[Controller Handler]
    
    style A fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style C fill:#10b981,stroke:#047857,color:#ffffff
    style D fill:#8b5cf6,stroke:#6d28d9,color:#ffffff
    style E fill:#f59e0b,stroke:#b45309,color:#ffffff
    style I fill:#64748b,stroke:#334155,color:#ffffff
```

::

**Механізм роботи:**

1. Клієнт надсилає HTTP-запит з credentials (пароль або токен).
2. NestJS Guard активує відповідну Passport стратегію.
3. Стратегія витягує credentials з запиту (body, headers, cookies).
4. Стратегія викликає метод `validate()` для перевірки credentials.
5. Якщо валідація успішна, результат методу `validate()` зберігається у `request.user`.
6. Guard дозволяє виконання запиту — контролер отримує `request.user`.
7. Якщо валідація невдала, Guard кидає `UnauthorizedException` та блокує запит.

::note
**Чому не просто писати логіку автентифікації у Guards?** Passport надає стандартизований інтерфейс для різних методів автентифікації. Це дозволяє легко додавати нові стратегії (наприклад, OAuth Google) без зміни архітектури застосунку — достатньо створити нову стратегію та зареєструвати її у модулі.
::

### Інтеграція Passport у NestJS

NestJS надає обгортку `@nestjs/passport`, що інтегрує Passport middleware у систему Guards. Для використання Passport необхідно:

1. Встановити `@nestjs/passport`, `passport` та конкретні пакети стратегій (`passport-local`, `passport-jwt`).
2. Створити класи стратегій, що наслідують `PassportStrategy`.
3. Зареєструвати стратегії як провайдери у модулі.
4. Використовувати `AuthGuard('strategy-name')` для захисту маршрутів.

---

## Local Strategy: автентифікація за email/паролем

Local Strategy використовується для традиційної автентифікації через форму входу з email та паролем. Вона перехоплює POST-запит до `/auth/login`, витягує `email` та `password` з тіла запиту та викликає метод валідації.

### Встановлення залежностей

::tabs

::tabs-item{label="npm"}
```bash
npm install passport-local
npm install --save-dev @types/passport-local
```
::

::tabs-item{label="pnpm"}
```bash
pnpm add passport-local
pnpm add -D @types/passport-local
```
::

::tabs-item{label="yarn"}
```bash
yarn add passport-local
yarn add -D @types/passport-local
```
::

::

### Реалізація LocalStrategy

```typescript
// src/auth/strategies/local.strategy.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { Strategy } from 'passport-local';
import { AuthService } from '../auth.service';

@Injectable()
export class LocalStrategy extends PassportStrategy(Strategy) {
  constructor(private authService: AuthService) {
    super({
      usernameField: 'email',  // Замість дефолтного 'username' використовуємо 'email'
      passwordField: 'password', // Дефолтне поле, але явно вказуємо для читабельності
    });
  }

  /**
   * Метод validate() викликається автоматично після витягування credentials
   * 
   * @param email - Email з тіла POST-запиту
   * @param password - Пароль з тіла POST-запиту
   * @returns User entity, яка буде збережена у request.user
   * @throws UnauthorizedException якщо credentials невалідні
   */
  async validate(email: string, password: string) {
    // Делегуємо валідацію сервісному шару
    const user = await this.authService.validateUser(email, password);

    if (!user) {
      // Passport автоматично перетворить це у HTTP 401
      throw new UnauthorizedException('Invalid credentials');
    }

    // Все, що повертається з validate(), потрапляє у request.user
    return {
      userId: user.id,
      email: user.email,
      roles: user.roles,
    };
  }
}
```

**Детальний розбір параметрів конструктора:**

| Параметр | Тип | Опис |
|----------|-----|------|
| `usernameField` | string | Назва поля у тілі POST-запиту, що містить ідентифікатор користувача. За замовчуванням `'username'`, але ми змінюємо на `'email'`. |
| `passwordField` | string | Назва поля у тілі POST-запиту, що містить пароль. За замовчуванням `'password'`. |
| `passReqToCallback` | boolean | Якщо `true`, метод `validate()` отримує першим параметром `request` об'єкт. Корисно для доступу до IP-адреси або User-Agent. |

**Що відбувається під капотом:**

1. Клієнт надсилає `POST /auth/login` з body `{ email, password }`.
2. `AuthGuard('local')` активує `LocalStrategy`.
3. Passport витягує `email` та `password` з `request.body` відповідно до `usernameField` та `passwordField`.
4. Passport викликає `LocalStrategy.validate(email, password)`.
5. Метод `validate()` викликає `AuthService.validateUser()`, що:
   - Завантажує користувача з бази даних за email.
   - Порівнює хеш паролю через `bcrypt.compare()`.
   - Повертає користувача або `null`.
6. Якщо `validate()` повертає об'єкт — Passport зберігає його у `request.user`.
7. Якщо `validate()` кидає виключення — Guard блокує запит з `401 Unauthorized`.

### Створення LocalAuthGuard

```typescript
// src/auth/guards/local-auth.guard.ts
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class LocalAuthGuard extends AuthGuard('local') {}
```

Цей клас є тонкою обгорткою над `AuthGuard('local')`, що дозволяє використовувати його як декоратор `@UseGuards(LocalAuthGuard)` замість магічного рядка `'local'`.

### Використання LocalStrategy у контролері

```typescript
// src/auth/auth.controller.ts
import { Controller, Post, UseGuards, Request, Body, HttpCode, HttpStatus } from '@nestjs/common';
import { AuthService } from './auth.service';
import { LocalAuthGuard } from './guards/local-auth.guard';
import { LoginDto } from './dto/login.dto';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  /**
   * POST /auth/login
   * 
   * LocalAuthGuard активує LocalStrategy для валідації email/password
   * Після успішної валідації request.user містить дані з validate()
   */
  @Post('login')
  @UseGuards(LocalAuthGuard)
  @HttpCode(HttpStatus.OK)
  async login(@Request() req, @Body() dto: LoginDto) {
    // На цей момент LocalStrategy вже перевірила credentials
    // і user доступний через req.user

    // Генеруємо JWT токен для автентифікованого користувача
    const { accessToken, tokenType, expiresIn } = await this.authService.generateToken(req.user);

    return {
      statusCode: HttpStatus.OK,
      message: 'Login successful',
      data: {
        accessToken,
        tokenType,
        expiresIn,
        user: req.user,
      },
    };
  }
}
```

**Послідовність виконання запиту:**

1. Клієнт надсилає POST з `{ email: 'ivan@example.com', password: 'SecureP@ss123' }`.
2. `ValidationPipe` перевіряє структуру через `LoginDto` (email формат, пароль не порожній).
3. `LocalAuthGuard` активує `LocalStrategy.validate(email, password)`.
4. `LocalStrategy` викликає `AuthService.validateUser()` → порівняння bcrypt хешів.
5. Якщо успішно — `req.user` містить `{ userId, email, roles }`.
6. Метод `login()` контролера генерує JWT токен для `req.user`.
7. Клієнт отримує токен та може використовувати його для наступних запитів.

::tip
**Чому LocalStrategy потрібна лише для `/auth/login`?** Після успішного логіну клієнт отримує JWT токен, який використовується для всіх наступних запитів. LocalStrategy виконує **одноразову** валідацію email/паролю, тоді як JwtStrategy (наступна секція) **багаторазово** верифікує токен при кожному запиті до захищених маршрутів.
::

### Додавання LocalStrategy до модуля

```typescript
// src/auth/auth.module.ts
import { Module } from '@nestjs/common';
import { PassportModule } from '@nestjs/passport';
import { JwtModule } from '@nestjs/jwt';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { UsersModule } from '../users/users.module';
import { LocalStrategy } from './strategies/local.strategy';
import { JwtStrategy } from './strategies/jwt.strategy';

@Module({
  imports: [
    UsersModule,
    PassportModule,
    JwtModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get<string>('JWT_SECRET'),
        signOptions: { expiresIn: '15m' },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [
    AuthService,
    LocalStrategy,  // Реєстрація LocalStrategy як провайдера
    JwtStrategy,
  ],
  exports: [AuthService],
})
export class AuthModule {}
```

Passport автоматично реєструє стратегію під назвою `'local'` (витягнуто з назви класу `Strategy` у `passport-local`). Для використання пишемо `AuthGuard('local')`.



---

## JWT Strategy: захист маршрутів токеном

JWT Strategy використовується для **постійної** автентифікації користувача у всіх запитах після логіну. Вона витягує JWT токен з заголовка `Authorization`, верифікує підпис та декодує payload у об'єкт користувача.

### Реалізація JwtStrategy

```typescript
// src/auth/strategies/jwt.strategy.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';
import { UsersService } from '../../users/users.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    private config: ConfigService,
    private usersService: UsersService, // Опціонально: для завантаження свіжих даних
  ) {
    super({
      // Витягування токена з заголовка "Authorization: Bearer <token>"
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      
      // Чи ігнорувати exp claim (НІКОЛИ не встановлюйте true у продакшні)
      ignoreExpiration: false,
      
      // Секретний ключ для верифікації підпису
      secretOrKey: config.get<string>('JWT_SECRET'),
      
      // Опціонально: перевірка audience та issuer
      // audience: 'my-app-users',
      // issuer: 'my-app',
    });
  }

  /**
   * Метод validate() викликається ПІСЛЯ успішної верифікації токена
   * 
   * @param payload - Декодований payload токена (sub, email, roles, iat, exp)
   * @returns Об'єкт, що буде збережений у request.user
   */
  async validate(payload: any) {
    // Payload вже верифікований — підпис співпадає, exp не минув
    
    // Варіант 1: Мінімальний підхід (використання даних з токена)
    return {
      userId: payload.sub,
      email: payload.email,
      roles: payload.roles,
    };

    // Варіант 2: Завантаження свіжих даних з БД (додаткові запити)
    // const user = await this.usersService.findById(payload.sub);
    // if (!user || !user.isActive) {
    //   throw new UnauthorizedException('User is inactive or deleted');
    // }
    // return {
    //   userId: user.id,
    //   email: user.email,
    //   roles: user.roles,
    // };
  }
}
```

**Детальний розбір параметрів конструктора:**

| Параметр | Тип | Опис |
|----------|-----|------|
| `jwtFromRequest` | Function | Функція для витягування токена з запиту. `ExtractJwt.fromAuthHeaderAsBearerToken()` шукає заголовок `Authorization: Bearer <token>`. |
| `ignoreExpiration` | boolean | Якщо `true`, стратегія приймає застарілі токени (exp claim ігнорується). **Завжди `false` у продакшені!** |
| `secretOrKey` | string або Buffer | Секретний ключ для HMAC алгоритмів (HS256) або публічний ключ для RSA (RS256). |
| `secretOrKeyProvider` | Function | Асинхронна функція для динамічного завантаження ключів (для ротації ключів або JWKS). |
| `audience` | string або string[] | Перевіряє claim `aud` токена. Відхиляє токени з іншим audience. |
| `issuer` | string або string[] | Перевіряє claim `iss` токена. Відхиляє токени від інших issuer. |
| `algorithms` | string[] | Список допустимих алгоритмів підпису. За замовчуванням `['HS256']`. |

**Альтернативні способи витягування токена:**

```typescript
// З cookie замість заголовка
jwtFromRequest: ExtractJwt.fromExtractors([
  (request) => request?.cookies?.access_token,
]),

// З query parameter (?token=...)
jwtFromRequest: ExtractJwt.fromUrlQueryParameter('token'),

// Комбінація кількох джерел (fallback)
jwtFromRequest: ExtractJwt.fromExtractors([
  ExtractJwt.fromAuthHeaderAsBearerToken(), // Спочатку з заголовка
  ExtractJwt.fromUrlQueryParameter('token'), // Якщо немає — з query
]),
```

### Два підходи до методу validate()

**Підхід 1: Використання даних з токена (stateless)**

Мінімальний та найшвидший підхід — просто перетворюємо payload токена у об'єкт користувача без звернення до бази даних:

```typescript
async validate(payload: any) {
  return {
    userId: payload.sub,
    email: payload.email,
    roles: payload.roles,
  };
}
```

**Переваги:**
- ✅ Максимальна продуктивність — немає запитів до БД при кожному запиті.
- ✅ Справжній stateless підхід — сервер не зберігає стан.

**Недоліки:**
- ❌ Дані можуть бути застарілими — якщо ролі користувача змінилися у БД, токен містить старі ролі до закінчення TTL.
- ❌ Неможливо миттєво заблокувати користувача — блокування набуває чинності лише після застарівання токена.

**Підхід 2: Завантаження свіжих даних з БД (stateful)**

Завантажуємо актуальні дані користувача з бази даних при кожному запиті:

```typescript
async validate(payload: any) {
  const user = await this.usersService.findById(payload.sub);

  if (!user) {
    throw new UnauthorizedException('User not found');
  }

  if (!user.isActive) {
    throw new UnauthorizedException('User account is disabled');
  }

  return {
    userId: user.id,
    email: user.email,
    roles: user.roles,
    isActive: user.isActive,
  };
}
```

**Переваги:**
- ✅ Завжди актуальні дані — зміни ролей або блокування набувають чинності миттєво.
- ✅ Можливість додаткових перевірок (чи активний обліковий запис, чи не закінчилася підписка).

**Недоліки:**
- ❌ Додаткове навантаження на БД — запит при кожному HTTP-запиті.
- ❌ Збільшення затримок відповідей (*latency*) на 5–20 мс.
- ❌ Втрата переваги stateless автентифікації.

::tip
**Рекомендація:** для більшості застосунків використовуйте **Підхід 1** (stateless) з коротким TTL токена (15 хвилин). Для критичних систем (онлайн-банкінг, корпоративні системи з жорстким контролем доступу) використовуйте **Підхід 2** з кешуванням у Redis для зменшення навантаження на БД:

```typescript
async validate(payload: any) {
  // Спочатку перевіряємо кеш
  const cachedUser = await this.cache.get(`user:${payload.sub}`);
  if (cachedUser) {
    return cachedUser;
  }

  // Якщо немає у кеші — завантажуємо з БД
  const user = await this.usersService.findById(payload.sub);
  
  // Кешуємо на 5 хвилин
  await this.cache.set(`user:${payload.sub}`, user, 300);
  
  return user;
}
```
::

### Створення JwtAuthGuard

```typescript
// src/auth/guards/jwt-auth.guard.ts
import { Injectable, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { AuthGuard } from '@nestjs/passport';
import { IS_PUBLIC_KEY } from '../decorators/public.decorator';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  /**
   * Перевіряємо, чи маршрут позначений декоратором @Public()
   * Якщо так — пропускаємо автентифікацію
   */
  canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),  // Метод контролера
      context.getClass(),    // Клас контролера
    ]);

    if (isPublic) {
      return true; // Дозволяємо доступ без автентифікації
    }

    // Викликаємо стандартну логіку AuthGuard
    return super.canActivate(context);
  }
}
```

Цей Guard розширює базовий `AuthGuard('jwt')`, додаючи підтримку декоратора `@Public()` для позначення публічних маршрутів (детальніше у наступній секції).

### Використання JwtStrategy у контролерах

```typescript
// src/users/users.controller.ts
import { Controller, Get, UseGuards, Request, Param } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { UsersService } from './users.service';

@Controller('users')
@UseGuards(JwtAuthGuard) // Захист всього контролера
export class UsersController {
  constructor(private usersService: UsersService) {}

  /**
   * GET /users/profile
   * Отримання профілю поточного користувача
   */
  @Get('profile')
  getProfile(@Request() req) {
    // req.user встановлено JwtStrategy.validate()
    return {
      userId: req.user.userId,
      email: req.user.email,
      roles: req.user.roles,
    };
  }

  /**
   * GET /users/:id
   * Отримання профілю іншого користувача (лише для адмінів)
   */
  @Get(':id')
  async getUserById(@Param('id') id: string, @Request() req) {
    // Перевірка авторизації: чи є користувач адміністратором?
    if (!req.user.roles.includes('admin')) {
      throw new ForbiddenException('Only admins can view other users');
    }

    return this.usersService.findById(id);
  }
}
```

**Приклад запиту з JWT токеном:**

```http
GET /users/profile HTTP/1.1
Host: localhost:3000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6Iml2YW5AZXhhbXBsZS5jb20iLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTY5MzU2NDgwMCwiZXhwIjoxNjkzNTY1NzAwfQ.4Hb3LM-TqHX-2JcGKz9yP3qF8vZ5nR7wQ1xS6mE9kLo
```

**Послідовність обробки:**

1. `JwtAuthGuard` активує `JwtStrategy`.
2. `ExtractJwt.fromAuthHeaderAsBearerToken()` витягує токен з заголовка.
3. Passport верифікує підпис токена за допомогою `JWT_SECRET`.
4. Passport перевіряє `exp` claim — чи не застарів токен.
5. Passport викликає `JwtStrategy.validate(payload)`.
6. Результат `validate()` зберігається у `req.user`.
7. Контролер отримує доступ до `req.user`.

::warning
**Типова помилка:** забути додати `Bearer ` (з пробілом) перед токеном у заголовку. Правильний формат: `Authorization: Bearer <token>`. Якщо написати просто `Authorization: <token>`, `ExtractJwt.fromAuthHeaderAsBearerToken()` не знайде токен і поверне `null`, що призведе до `401 Unauthorized`.
::



---

## Кастомні декоратори: елегантний доступ до користувача

Декоратор `@Request()` дає доступ до всього об'єкта запиту, але для роботи з користувачем нам потрібен лише `req.user`. Створимо кастомний декоратор `@CurrentUser()` для витягування даних користувача безпосередньо як параметр методу.

### Декоратор @CurrentUser()

```typescript
// src/auth/decorators/current-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

/**
 * Декоратор для витягування поточного користувача з request.user
 * 
 * Використання:
 * @Get('profile')
 * getProfile(@CurrentUser() user: UserPayload) {
 *   return user;
 * }
 * 
 * Витягування конкретного поля:
 * @Get('my-posts')
 * getMyPosts(@CurrentUser('userId') userId: string) {
 *   return this.postsService.findByUserId(userId);
 * }
 */
export const CurrentUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;

    // Якщо вказано конкретне поле (наприклад, @CurrentUser('userId'))
    if (data) {
      return user?.[data];
    }

    // Якщо data не вказано — повертаємо весь об'єкт користувача
    return user;
  },
);
```

**Приклад використання:**

```typescript
// src/posts/posts.controller.ts
import { Controller, Get, Post, Body, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { CurrentUser } from '../auth/decorators/current-user.decorator';
import { PostsService } from './posts.service';
import { CreatePostDto } from './dto/create-post.dto';

interface UserPayload {
  userId: string;
  email: string;
  roles: string[];
}

@Controller('posts')
@UseGuards(JwtAuthGuard)
export class PostsController {
  constructor(private postsService: PostsService) {}

  /**
   * GET /posts/my
   * Отримання постів поточного користувача
   */
  @Get('my')
  getMyPosts(@CurrentUser() user: UserPayload) {
    // Елегантний доступ до даних користувача без req.user
    return this.postsService.findByUserId(user.userId);
  }

  /**
   * POST /posts
   * Створення нового посту від імені поточного користувача
   */
  @Post()
  createPost(
    @CurrentUser('userId') userId: string, // Витягуємо лише userId
    @Body() dto: CreatePostDto,
  ) {
    return this.postsService.create({
      ...dto,
      authorId: userId, // Автор завжди поточний користувач
    });
  }

  /**
   * GET /posts/stats
   * Статистика з доступом до всього об'єкта користувача
   */
  @Get('stats')
  getStats(@CurrentUser() user: UserPayload) {
    return {
      totalPosts: 42,
      userId: user.userId,
      userEmail: user.email,
      userRoles: user.roles,
    };
  }
}
```

**Переваги кастомного декоратора:**

- ✅ **Читабельність:** `@CurrentUser()` явно вказує, що метод працює з даними автентифікованого користувача.
- ✅ **Типізація:** можна вказати тип `UserPayload` для автодоповнення та перевірки типів.
- ✅ **Лаконічність:** не потрібно писати `req.user` у кожному методі.
- ✅ **Витягування полів:** `@CurrentUser('userId')` повертає одразу потрібне поле.

### Декоратор @Public() для публічних маршрутів

У попередніх секціях ми використовували `@UseGuards(JwtAuthGuard)` на кожному контролері або методі, що вимагає автентифікації. Проте у більшості застосунків **майже всі маршруті захищені**, а публічних лише кілька (`/auth/login`, `/auth/register`, `/health`, `/docs`). Зручніше застосувати `JwtAuthGuard` **глобально** та позначати винятки через декоратор `@Public()`.

**Створення декоратора @Public():**

```typescript
// src/auth/decorators/public.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic';

/**
 * Декоратор для позначення публічних маршрутів, що не вимагають автентифікації
 * 
 * Використання:
 * @Public()
 * @Get('health')
 * healthCheck() {
 *   return { status: 'ok' };
 * }
 */
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

**Оновлення JwtAuthGuard для підтримки @Public():**

Ми вже реалізували цю логіку у попередній секції:

```typescript
// src/auth/guards/jwt-auth.guard.ts
import { Injectable, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { AuthGuard } from '@nestjs/passport';
import { IS_PUBLIC_KEY } from '../decorators/public.decorator';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext) {
    // Читаємо метадані з декоратора @Public()
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),  // Перевіряємо метод контролера
      context.getClass(),    // Перевіряємо клас контролера
    ]);

    if (isPublic) {
      return true; // Пропускаємо автентифікацію для публічних маршрутів
    }

    // Для решти маршрутів виконуємо стандартну автентифікацію
    return super.canActivate(context);
  }
}
```

**Глобальна реєстрація JwtAuthGuard:**

```typescript
// src/app.module.ts
import { Module } from '@nestjs/common';
import { APP_GUARD } from '@nestjs/core';
import { JwtAuthGuard } from './auth/guards/jwt-auth.guard';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';

@Module({
  imports: [AuthModule, UsersModule],
  providers: [
    {
      provide: APP_GUARD,
      useClass: JwtAuthGuard, // Застосовується до ВСІХ маршрутів
    },
  ],
})
export class AppModule {}
```

**Використання @Public() у контролерах:**

```typescript
// src/auth/auth.controller.ts
import { Controller, Post, Body, HttpCode, HttpStatus } from '@nestjs/common';
import { Public } from './decorators/public.decorator';
import { AuthService } from './auth.service';
import { RegisterDto, LoginDto } from './dto';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  /**
   * Публічний ендпоінт — реєстрація доступна без токена
   */
  @Public()
  @Post('register')
  async register(@Body() dto: RegisterDto) {
    return this.authService.register(dto.email, dto.password);
  }

  /**
   * Публічний ендпоінт — вхід доступний без токена
   */
  @Public()
  @Post('login')
  @HttpCode(HttpStatus.OK)
  async login(@Body() dto: LoginDto) {
    return this.authService.login(dto.email, dto.password);
  }
}
```

```typescript
// src/health/health.controller.ts
import { Controller, Get } from '@nestjs/common';
import { Public } from '../auth/decorators/public.decorator';

@Controller()
export class HealthController {
  /**
   * Публічний health check для моніторингу
   */
  @Public()
  @Get('health')
  healthCheck() {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
    };
  }
}
```

Тепер **за замовчуванням всі маршруті захищені** `JwtAuthGuard`, а винятки (реєстрація, логін, health check) позначені декоратором `@Public()`.

::tip
**Переваги глобального Guard з @Public():**

- ✅ **Безпека за замовчуванням:** нові маршруті автоматично захищені, розробник не може забути додати `@UseGuards()`.
- ✅ **Менше коду:** не потрібно додавати декоратор на кожен захищений маршрут (яких зазвичай 90%).
- ✅ **Явність винятків:** декоратор `@Public()` чітко показує, що маршрут навмисно зроблений публічним.
- ✅ **Зручність рефакторингу:** при додаванні нового модуля він автоматично захищений.
::

---

## Декоратор @Roles() для авторизації на основі ролей

Після автентифікації через JWT часто потрібна **авторизація** — перевірка, чи має користувач необхідну роль для виконання дії. Створимо декоратор `@Roles()` та відповідний Guard.

### Створення декоратора @Roles()

```typescript
// src/auth/decorators/roles.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const ROLES_KEY = 'roles';

/**
 * Декоратор для визначення ролей, необхідних для доступу до маршруту
 * 
 * Використання:
 * @Roles('admin')
 * @Delete(':id')
 * deleteUser(@Param('id') id: string) { ... }
 * 
 * Кілька ролей (достатньо мати хоча б одну):
 * @Roles('admin', 'moderator')
 */
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);
```

### Створення RolesGuard

```typescript
// src/auth/guards/roles.guard.ts
import { Injectable, CanActivate, ExecutionContext, ForbiddenException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLES_KEY } from '../decorators/roles.decorator';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    // Читаємо ролі з метаданих декоратора @Roles()
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    // Якщо ролі не вказані — дозволяємо доступ
    if (!requiredRoles || requiredRoles.length === 0) {
      return true;
    }

    // Витягуємо дані користувача з request.user (встановлені JwtStrategy)
    const request = context.switchToHttp().getRequest();
    const user = request.user;

    if (!user) {
      throw new ForbiddenException('User not authenticated');
    }

    // Перевіряємо, чи має користувач хоча б одну з необхідних ролей
    const hasRole = requiredRoles.some((role) => user.roles?.includes(role));

    if (!hasRole) {
      throw new ForbiddenException(
        `Access denied. Required roles: [${requiredRoles.join(', ')}]`,
      );
    }

    return true;
  }
}
```

### Використання @Roles() у контролерах

```typescript
// src/users/users.controller.ts
import { Controller, Get, Delete, Param, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { CurrentUser } from '../auth/decorators/current-user.decorator';
import { UsersService } from './users.service';

@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard) // Спочатку автентифікація, потім авторизація
export class UsersController {
  constructor(private usersService: UsersService) {}

  /**
   * GET /users/profile
   * Доступно всім автентифікованим користувачам
   */
  @Get('profile')
  getProfile(@CurrentUser() user) {
    return user;
  }

  /**
   * GET /users
   * Доступно лише адміністраторам
   */
  @Get()
  @Roles('admin')
  getAllUsers() {
    return this.usersService.findAll();
  }

  /**
   * DELETE /users/:id
   * Доступно адміністраторам та модераторам
   */
  @Delete(':id')
  @Roles('admin', 'moderator')
  deleteUser(@Param('id') id: string) {
    return this.usersService.delete(id);
  }
}
```

**Порядок застосування Guards критичний:**

```typescript
@UseGuards(JwtAuthGuard, RolesGuard)
```

1. Спочатку виконується `JwtAuthGuard` — верифікація токена та встановлення `request.user`.
2. Потім виконується `RolesGuard` — перевірка ролей з `request.user.roles`.

Якщо змінити порядок, `RolesGuard` не зможе отримати дані користувача, оскільки `request.user` ще не встановлений.

::warning
**Типова помилка:** використовувати лише `RolesGuard` без `JwtAuthGuard`. У такому випадку `request.user` буде `undefined`, і Guard завжди повертатиме `403 Forbidden`. Завжди комбінуйте Guards у правильному порядку: спочатку автентифікація, потім авторизація.
::



---

## Тестування автентифікації через integration tests

Для перевірки коректності роботи стратегій та Guards критично важливо написати integration tests, що покривають повний цикл автентифікації.

### Налаштування тестового модуля

```typescript
// src/auth/auth.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../app.module';
import { UsersService } from '../users/users.service';

describe('Authentication E2E Tests', () => {
  let app: INestApplication;
  let usersService: UsersService;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();

    usersService = moduleFixture.get<UsersService>(UsersService);
  });

  afterAll(async () => {
    await app.close();
  });

  describe('POST /auth/register', () => {
    it('should register a new user', async () => {
      const response = await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'test@example.com',
          password: 'SecureP@ss123',
        })
        .expect(201);

      expect(response.body).toMatchObject({
        statusCode: 201,
        message: 'User registered successfully',
        data: {
          email: 'test@example.com',
        },
      });
      expect(response.body.data.id).toBeDefined();
    });

    it('should reject duplicate email', async () => {
      await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'duplicate@example.com',
          password: 'SecureP@ss123',
        })
        .expect(201);

      const response = await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'duplicate@example.com',
          password: 'AnotherP@ss123',
        })
        .expect(409);

      expect(response.body.message).toContain('already exists');
    });

    it('should reject weak password', async () => {
      const response = await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'weak@example.com',
          password: 'weak',
        })
        .expect(400);

      expect(response.body.message).toContain('at least 8 characters');
    });
  });

  describe('POST /auth/login', () => {
    beforeEach(async () => {
      await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'login-test@example.com',
          password: 'SecureP@ss123',
        });
    });

    it('should login with valid credentials', async () => {
      const response = await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'login-test@example.com',
          password: 'SecureP@ss123',
        })
        .expect(200);

      expect(response.body.data).toHaveProperty('accessToken');
      expect(response.body.data.tokenType).toBe('Bearer');
      expect(response.body.data.user.email).toBe('login-test@example.com');
    });

    it('should reject invalid password', async () => {
      const response = await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'login-test@example.com',
          password: 'WrongPassword123',
        })
        .expect(401);

      expect(response.body.message).toContain('Invalid credentials');
    });

    it('should reject non-existent email', async () => {
      const response = await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'nonexistent@example.com',
          password: 'SecureP@ss123',
        })
        .expect(401);

      expect(response.body.message).toContain('Invalid credentials');
    });
  });

  describe('GET /users/profile (Protected Route)', () => {
    let accessToken: string;

    beforeEach(async () => {
      await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'profile-test@example.com',
          password: 'SecureP@ss123',
        });

      const loginResponse = await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'profile-test@example.com',
          password: 'SecureP@ss123',
        });

      accessToken = loginResponse.body.data.accessToken;
    });

    it('should access protected route with valid token', async () => {
      const response = await request(app.getHttpServer())
        .get('/users/profile')
        .set('Authorization', `Bearer ${accessToken}`)
        .expect(200);

      expect(response.body.data.email).toBe('profile-test@example.com');
    });

    it('should reject request without token', async () => {
      await request(app.getHttpServer())
        .get('/users/profile')
        .expect(401);
    });

    it('should reject request with invalid token', async () => {
      await request(app.getHttpServer())
        .get('/users/profile')
        .set('Authorization', 'Bearer invalid-token-here')
        .expect(401);
    });

    it('should reject request with expired token', async () => {
      // Токен з exp у минулому (згенерований окремо)
      const expiredToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNjAwMDAwMDAwfQ.signature';

      await request(app.getHttpServer())
        .get('/users/profile')
        .set('Authorization', `Bearer ${expiredToken}`)
        .expect(401);
    });
  });
});
```

**Ключові моменти тестування:**

- **`beforeAll()`** — створення тестового застосунку один раз для всіх тестів.
- **`beforeEach()`** — підготовка даних перед кожним тестом (реєстрація тестового користувача).
- **`afterAll()`** — закриття з'єднань з БД та очищення ресурсів.
- **`expect().toMatchObject()`** — часткове співпадіння об'єкта (не перевіряємо `id`, оскільки він генерується).
- **`.set('Authorization', ...)`** — додавання JWT токена до заголовків запиту.

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Чому метод validate() викликається ПІСЛЯ верифікації токена, а не замість неї?" icon="i-lucide-help-circle"}

Passport розділяє процес автентифікації на дві фази:

**Фаза 1 (автоматична):** Passport автоматично виконує технічну верифікацію — перевіряє підпис токена, exp claim, витягує payload. Це відбувається **до** виклику `validate()`.

**Фаза 2 (кастомна):** Метод `validate()` викликається **після успішної** верифікації та отримує вже декодований payload. Тут ви можете:
- Перетворити структуру payload у зручний формат.
- Завантажити додаткові дані з БД (якщо потрібно).
- Виконати додаткові перевірки (чи активний користувач, чи не заблокований).

Якщо `validate()` кидає виключення, автентифікація вважається невдалою навіть при дійсному токені. Це корисно для сценаріїв, де токен технічно дійсний, але користувач більше не має права доступу (блокування, видалення облікового запису).

**Приклад:** токен підписаний правильно, але користувач видалений з БД. Passport перевірить підпис (фаза 1), але `validate()` викличе `UnauthorizedException` (фаза 2), що заблокує доступ.

::

::accordion-item{label="❓ Чи можна використовувати кілька стратегій одночасно на одному маршруті?" icon="i-lucide-help-circle"}

**Так, але це рідкісний сценарій.** Зазвичай один маршрут використовує одну стратегію, але можна комбінувати кілька Guard:

```typescript
@UseGuards(AuthGuard(['jwt', 'api-key']))
@Get('data')
getData() {
  // Дозволяє доступ з JWT токеном АБО API ключем
}
```

Passport спробує стратегії **послідовно**. Якщо перша (`jwt`) не проходить, спробує другу (`api-key`). Якщо хоча б одна успішна — доступ дозволено.

**Типові use cases:**

- JWT для веб-клієнтів, API Key для серверних інтеграцій.
- JWT для звичайних користувачів, OAuth для сторонніх сервісів.
- Basic Auth для legacy систем, JWT для нових клієнтів (перехідний період).

**Важливо:** порядок стратегій у масиві визначає пріоритет спроби. Рекомендується розміщувати швидші стратегії (JWT) перед повільнішими (OAuth з API викликами).

::

::accordion-item{label="❓ Що станеться, якщо забути додати LocalStrategy до providers у AuthModule?" icon="i-lucide-help-circle"}

NestJS не зможе знайти стратегію при виклику `AuthGuard('local')` і кине помилку:

```
Error: Unknown authentication strategy "local"
```

Passport шукає зареєстровані стратегії за їхніми назвами (витягнутими з імені класу `Strategy`). Якщо стратегія не додана до `providers` модуля, вона не потрапляє у Dependency Injection контейнер NestJS, і Passport не може її знайти.

**Налагодження:** якщо отримуєте цю помилку, перевірте:

1. Чи додано стратегію до `providers` масиву модуля.
2. Чи імпортовано `PassportModule` у модулі.
3. Чи правильна назва стратегії у `AuthGuard('local')` (має співпадати з назвою класу `Strategy` без префіксу/суфіксу).

**Приклад правильної конфігурації:**

```typescript
@Module({
  imports: [PassportModule, JwtModule.register(...)],
  providers: [
    AuthService,
    LocalStrategy,  // ✅ Обов'язково додати
    JwtStrategy,    // ✅ Обов'язково додати
  ],
})
export class AuthModule {}
```

::

::accordion-item{label="❓ Яка різниця між @UseGuards(JwtAuthGuard) на рівні методу vs контролера?" icon="i-lucide-help-circle"}

**На рівні методу:**
```typescript
@Controller('posts')
export class PostsController {
  @Get('public')
  getPublicPosts() { } // Публічний

  @Get('my')
  @UseGuards(JwtAuthGuard) // Захищений лише цей метод
  getMyPosts() { }
}
```

Guard застосовується **лише до одного методу**. Інші методи контролера залишаються публічними (якщо немає глобального Guard).

**На рівні контролера:**
```typescript
@Controller('posts')
@UseGuards(JwtAuthGuard) // Захищені ВСІ методи
export class PostsController {
  @Get('public')
  getPublicPosts() { } // Теж захищений!

  @Get('my')
  getMyPosts() { }
}
```

Guard застосовується до **всіх методів** контролера. Для винятків використовуйте декоратор `@Public()`:

```typescript
@Controller('posts')
@UseGuards(JwtAuthGuard)
export class PostsController {
  @Public() // Винято з автентифікації
  @Get('public')
  getPublicPosts() { }

  @Get('my')
  getMyPosts() { } // Залишається захищеним
}
```

**Рекомендація:** якщо більшість методів контролера захищені, застосовуйте Guard на рівні контролера з виключеннями через `@Public()`. Якщо більшість методів публічні — застосовуйте Guard на рівні конкретних методів.

::

::

---

## Ключові висновки

::card-group

::card{title="🔌 Модульна архітектура Passport" icon="i-lucide-puzzle"}

Passport.js надає єдиний інтерфейс для інтеграції різних методів автентифікації через стратегії. LocalStrategy для email/пароля, JwtStrategy для токенів, OAuth стратегії для сторонніх провайдерів — всі працюють через єдиний механізм `validate()`.

::

::card{title="🛡️ Guards як точки входу" icon="i-lucide-shield"}

AuthGuard активує відповідну стратегію та блокує доступ при невдалій автентифікації. Порядок Guards критичний: спочатку автентифікація (JwtAuthGuard), потім авторизація (RolesGuard). Результат валідації зберігається у request.user.

::

::card{title="🎨 Кастомні декоратори для елегантності" icon="i-lucide-wand"}

@CurrentUser() витягує дані користувача безпосередньо як параметр методу. @Public() позначає публічні маршруті при глобальному Guard. @Roles() визначає необхідні ролі для авторизації. Декоратори покращують читабельність та підтримку коду.

::

::card{title="⚡ Stateless vs Stateful validate()" icon="i-lucide-zap"}

JwtStrategy.validate() може працювати stateless (використання даних з токена) або stateful (завантаження з БД). Stateless забезпечує максимальну продуктивність, stateful — завжди актуальні дані. Для балансу використовуйте кешування у Redis.

::

::

---

## Рекомендовані ресурси для поглибленого вивчення

- **Passport.js Official Documentation:** офіційна документація з описом понад 500 стратегій автентифікації та їхньої конфігурації.

- **NestJS Authentication Documentation:** офіційний гайд NestJS з інтеграції Passport, створення кастомних стратегій та Guards.

- **passport-jwt GitHub:** документація стратегії JWT з детальним описом опцій конфігурації та витягування токенів.

- **NestJS Guards Documentation:** повний опис механізму Guards, порядку виконання та інтеграції з Reflector для метаданих.

::note
У наступній лекції ми детально розглянемо **хешування паролів через bcrypt** — вибір cost factor для балансу безпека/продуктивність, порівняння паролів через timing-safe функції, міграція існуючих користувачів з інших алгоритмів хешування (MD5, SHA-256) на bcrypt, та захист від rainbow table атак через salt.
::
