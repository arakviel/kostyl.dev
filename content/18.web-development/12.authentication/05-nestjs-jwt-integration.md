# Інтеграція JWT у NestJS

## Короткий зміст

У цій лекції розглядається практична реалізація JWT автентифікації у фреймворку NestJS:

- **Встановлення залежностей** — `@nestjs/jwt` та його конфігурація через `JwtModule.register()` або `JwtModule.registerAsync()` для динамічної конфігурації
- **Створення AuthModule** — структура модуля з `AuthService`, `AuthController`, імпорт `UsersModule` для доступу до репозиторію користувачів
- **AuthService** — методи `register()` (реєстрація з хешуванням пароля), `login()` (валідація credentials та генерація токена), `validateUser()` (перевірка email/password)
- **Використання JwtService** — метод `sign()` для створення токена з payload (userId, email, role), метод `verify()` для валідації токена
- **Генерація токена при логіні** — створення payload з мінімальними даними, підпис токена з TTL, повернення токена клієнту у відповіді
- **Налаштування secret key** — використання змінних оточення через `@nestjs/config`, ConfigService для безпечного зберігання JWT_SECRET

Розглядаються приклади створення ендпоінтів `/auth/register` та `/auth/login`, структура відповідей, обробка помилок при невалідних credentials.

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати повний цикл інтеграції JWT модуля у NestJS застосунок від встановлення до продакшн-конфігурації.
- Навчитися створювати AuthModule з правильною модульною архітектурою та інкапсуляцією логіки автентифікації.
- Реалізувати повноцінні ендпоінти реєстрації та входу з генерацією JWT токенів та валідацією облікових даних.
- Зрозуміти різницю між синхронною та асинхронною конфігурацією модулів для різних середовищ.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **JwtService:** сервіс NestJS, що інкапсулює бібліотеку `jsonwebtoken` для підпису та верифікації токенів.
- **Payload:** об'єкт даних, що вбудовується у JWT токен (зазвичай `{ sub, email, roles }`).
- **Dynamic Module:** модуль NestJS з методами `register()` або `registerAsync()` для конфігурації під час виконання.
- **ConfigService:** сервіс для безпечного доступу до змінних оточення через `@nestjs/config`.

::

::

---

## Архітектура модуля автентифікації

Перед початком кодування критично важливо розуміти архітектурну організацію модулів у NestJS та їхню взаємодію. Автентифікація є крос-модульною функціональністю, що залежить від модуля користувачів (*UsersModule*) для доступу до даних облікових записів.

### Структура файлів та директорій

Правильна організація файлової структури забезпечує читабельність коду, легке тестування та масштабованість застосунку. Розглянемо рекомендовану структуру для модуля автентифікації:

::code-tree

```typescript [src/auth/auth.module.ts]
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { UsersModule } from '../users/users.module';
import { JwtStrategy } from './strategies/jwt.strategy';

@Module({
  imports: [
    UsersModule,
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
  providers: [AuthService, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
```

```typescript [src/auth/auth.service.ts]
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UsersService } from '../users/users.service';
import { compare, hash } from 'bcrypt';

@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
  ) {}

  async register(email: string, password: string) {
    // Хешування паролю та створення користувача
    const passwordHash = await hash(password, 12);
    return this.usersService.create({ email, passwordHash });
  }

  async login(email: string, password: string) {
    const user = await this.validateUser(email, password);
    const payload = { sub: user.id, email: user.email, roles: user.roles };
    return { accessToken: this.jwtService.sign(payload) };
  }

  async validateUser(email: string, password: string) {
    const user = await this.usersService.findByEmail(email);
    if (!user || !(await compare(password, user.passwordHash))) {
      throw new UnauthorizedException('Invalid credentials');
    }
    return user;
  }
}
```

```typescript [src/auth/auth.controller.ts]
import { Controller, Post, Body, HttpCode, HttpStatus } from '@nestjs/common';
import { AuthService } from './auth.service';
import { RegisterDto, LoginDto } from './dto';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('register')
  async register(@Body() dto: RegisterDto) {
    const user = await this.authService.register(dto.email, dto.password);
    return { id: user.id, email: user.email };
  }

  @Post('login')
  @HttpCode(HttpStatus.OK)
  async login(@Body() dto: LoginDto) {
    return this.authService.login(dto.email, dto.password);
  }
}
```

```typescript [src/auth/dto/register.dto.ts]
import { IsEmail, IsNotEmpty, MinLength, Matches } from 'class-validator';

export class RegisterDto {
  @IsEmail({}, { message: 'Invalid email format' })
  email: string;

  @IsNotEmpty()
  @MinLength(8, { message: 'Password must be at least 8 characters' })
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase and number',
  })
  password: string;
}
```

```typescript [src/auth/dto/login.dto.ts]
import { IsEmail, IsNotEmpty } from 'class-validator';

export class LoginDto {
  @IsEmail()
  email: string;

  @IsNotEmpty()
  password: string;
}
```

```typescript [src/auth/dto/index.ts]
export * from './register.dto';
export * from './login.dto';
```

```typescript [src/auth/guards/jwt-auth.guard.ts]
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}
```

```typescript [src/auth/strategies/jwt.strategy.ts]
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private config: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: config.get<string>('JWT_SECRET'),
    });
  }

  async validate(payload: any) {
    return { userId: payload.sub, email: payload.email, roles: payload.roles };
  }
}
```

::

**Пояснення структури:**

- **`auth.module.ts`** — центральний модуль, що імпортує `JwtModule`, `UsersModule` та реєструє контролери/сервіси.
- **`auth.service.ts`** — бізнес-логіка: реєстрація, валідація credentials, генерація токенів.
- **`auth.controller.ts`** — HTTP ендпоінти `/auth/register` та `/auth/login`.
- **`dto/`** — Data Transfer Objects для валідації вхідних даних через `class-validator`.
- **`guards/`** — Guards для захисту маршрутів (JwtAuthGuard).
- **`strategies/`** — Passport стратегії для верифікації токенів (детально у наступній лекції).

### Діаграма взаємодії модулів

::mermaid

```mermaid
graph TB
    subgraph "Client"
        A[Browser/Mobile App]
    end
    
    subgraph "NestJS Application"
        B[AuthController]
        C[AuthService]
        D[JwtService]
        E[UsersService]
        F[(Database)]
        G[ConfigService]
    end
    
    A -->|POST /auth/login| B
    B --> C
    C -->|validateUser| E
    E -->|findByEmail| F
    F -->|User entity| E
    E -->|User data| C
    C -->|bcrypt.compare| C
    C -->|generate token| D
    D -->|JWT_SECRET| G
    D -->|signed token| C
    C -->|accessToken| B
    B -->|JSON response| A
    
    style A fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style B fill:#8b5cf6,stroke:#6d28d9,color:#ffffff
    style C fill:#10b981,stroke:#047857,color:#ffffff
    style D fill:#f59e0b,stroke:#b45309,color:#ffffff
    style E fill:#64748b,stroke:#334155,color:#ffffff
    style F fill:#ef4444,stroke:#b91c1c,color:#ffffff
```

::

**Потік даних при логіні:**

1. Клієнт надсилає POST-запит з `{ email, password }`.
2. `AuthController` делегує обробку `AuthService.login()`.
3. `AuthService` викликає `UsersService.findByEmail()` для завантаження користувача з бази даних.
4. Сервіс порівнює хеш паролю через `bcrypt.compare()`.
5. Якщо пароль співпадає, сервіс створює payload і викликає `JwtService.sign()`.
6. `JwtService` підписує токен, використовуючи `JWT_SECRET` з `ConfigService`.
7. Токен повертається клієнту у JSON-відповіді.

---

## Встановлення та конфігурація залежностей

Почнемо з підготовки інфраструктури — встановлення необхідних пакетів та налаштування змінних оточення.

### Встановлення npm пакетів

::tabs

::tabs-item{label="npm"}
```bash
npm install @nestjs/jwt @nestjs/passport passport passport-jwt
npm install bcrypt
npm install --save-dev @types/passport-jwt @types/bcrypt
```
::

::tabs-item{label="pnpm"}
```bash
pnpm add @nestjs/jwt @nestjs/passport passport passport-jwt
pnpm add bcrypt
pnpm add -D @types/passport-jwt @types/bcrypt
```
::

::tabs-item{label="yarn"}
```bash
yarn add @nestjs/jwt @nestjs/passport passport passport-jwt
yarn add bcrypt
yarn add -D @types/passport-jwt @types/bcrypt
```
::

::

**Опис пакетів:**

| Пакет | Призначення |
|-------|-------------|
| `@nestjs/jwt` | NestJS обгортка для `jsonwebtoken`, надає `JwtService` та `JwtModule`. |
| `@nestjs/passport` | Інтеграція Passport.js у NestJS для стратегій автентифікації. |
| `passport` | Middleware для автентифікації з підтримкою різних стратегій (JWT, OAuth, Local). |
| `passport-jwt` | Passport стратегія для верифікації JWT токенів. |
| `bcrypt` | Бібліотека для хешування паролів з підтримкою cost factor (захист від brute-force). |
| `@types/*` | TypeScript типи для автодоповнення та перевірки типів під час компіляції. |

### Конфігурація змінних оточення

Секретний ключ для підпису JWT токенів **ніколи** не має зберігатися у коді. Використовуємо `.env` файл:

```bash
# .env
JWT_SECRET=your-super-secret-key-change-in-production-min-32-chars
JWT_EXPIRATION=15m

DATABASE_URL=postgresql://user:password@localhost:5432/myapp
```

**Генерація криптографічно стійкого ключа:**

```bash
# Згенерувати 256-бітний ключ у hex форматі (64 символи)
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

::caution
**Критично важливо:** файл `.env` має бути доданий до `.gitignore` і **ніколи** не коммітитися у Git. Для різних середовищ (розробка, staging, продакшн) використовуйте окремі `.env` файли або secrets management системи (AWS Secrets Manager, Azure Key Vault, Kubernetes Secrets).
::

### Налаштування ConfigModule

Для безпечного доступу до змінних оточення встановлюємо `@nestjs/config`:

```bash
npm install @nestjs/config
```

Реєструємо `ConfigModule` глобально у `AppModule`:

```typescript
// src/app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,        // ConfigService доступний у всіх модулях
      envFilePath: '.env',   // Шлях до .env файлу
      cache: true,           // Кешування змінних для продуктивності
    }),
    AuthModule,
    UsersModule,
  ],
})
export class AppModule {}
```

Тепер `ConfigService` доступний у будь-якому сервісі через dependency injection:

```typescript
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AuthService {
  constructor(private config: ConfigService) {
    const jwtSecret = this.config.get<string>('JWT_SECRET');
    console.log('JWT Secret loaded:', jwtSecret ? '✓' : '✗');
  }
}
```



---

## Створення та конфігурація JwtModule

`JwtModule` є динамічним модулем (*Dynamic Module*), що дозволяє налаштовувати його під час виконання застосунку. Існують два підходи до конфігурації: синхронний (`register`) та асинхронний (`registerAsync`).

### Синхронна конфігурація через register()

Найпростіший спосіб — передати конфігурацію безпосередньо у `register()`:

```typescript
// src/auth/auth.module.ts
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';

@Module({
  imports: [
    JwtModule.register({
      secret: 'hardcoded-secret-not-recommended', // ❌ Небезпечно для продакшну
      signOptions: {
        expiresIn: '15m',
        algorithm: 'HS256',
      },
    }),
  ],
})
export class AuthModule {}
```

**Недоліки цього підходу:**

- ❌ Секретний ключ захардкоджений у коді та потрапить у Git репозиторій.
- ❌ Неможливо використовувати різні ключі для розробки, staging та продакшну.
- ❌ Зміна ключа вимагає ребілду та передеплою застосунку.

::warning
**Синхронна конфігурація допустима лише для локальної розробки або прототипів.** У продакшені завжди використовуйте асинхронну конфігурацію через `registerAsync()` з доступом до змінних оточення.
::

### Асинхронна конфігурація через registerAsync()

Рекомендований підхід — використання `registerAsync()` з `ConfigService` для динамічного завантаження секрету з `.env`:

```typescript
// src/auth/auth.module.ts
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { UsersModule } from '../users/users.module';

@Module({
  imports: [
    UsersModule,
    JwtModule.registerAsync({
      imports: [ConfigModule], // Імпорт ConfigModule для доступу до ConfigService
      inject: [ConfigService],  // Dependency injection ConfigService у factory
      useFactory: async (configService: ConfigService) => {
        const secret = configService.get<string>('JWT_SECRET');
        
        // Валідація наявності секрету при старті застосунку
        if (!secret) {
          throw new Error('JWT_SECRET is not defined in environment variables');
        }

        return {
          secret: secret,
          signOptions: {
            expiresIn: configService.get<string>('JWT_EXPIRATION') || '15m',
            algorithm: 'HS256',
            issuer: 'my-app-v1',      // Опціонально: ідентифікатор додатку
            audience: 'my-app-users',  // Опціонально: призначення токена
          },
        };
      },
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService],
  exports: [AuthService], // Експорт для використання в інших модулях
})
export class AuthModule {}
```

**Детальний розбір параметрів `signOptions`:**

| Параметр | Тип | Опис |
|----------|-----|------|
| `expiresIn` | string або number | Час життя токена. Формати: `'15m'`, `'1h'`, `'7d'`, `900` (секунди). |
| `algorithm` | string | Алгоритм підпису: `'HS256'`, `'HS384'`, `'HS512'`, `'RS256'`, `'ES256'`. |
| `issuer` | string | Claim `iss` — ідентифікатор сервера, що видав токен (для валідації у мікросервісах). |
| `audience` | string або string[] | Claim `aud` — призначення токена (які сервіси можуть його приймати). |
| `subject` | string | Claim `sub` — встановлюється автоматично, але можна перевизначити. |
| `notBefore` | string або number | Claim `nbf` — токен стає дійсним лише після цього часу. |
| `jwtid` | string | Claim `jti` — унікальний ідентифікатор токена (для blacklist). |

**Переваги асинхронної конфігурації:**

- ✅ Секретний ключ завантажується з безпечного джерела (`.env`, AWS Secrets Manager).
- ✅ Різні ключі для різних середовищ без зміни коду.
- ✅ Валідація конфігурації при старті застосунку — якщо `JWT_SECRET` відсутній, застосунок не запуститься.
- ✅ Можливість завантажувати конфігурацію з віддалених джерел (API, key vaults).

### Розширена конфігурація з валідацією

Для enterprise застосунків рекомендується створити окремий конфігураційний об'єкт з валідацією через `class-validator`:

```typescript
// src/config/jwt.config.ts
import { registerAs } from '@nestjs/config';
import { JwtModuleOptions } from '@nestjs/jwt';

export default registerAs(
  'jwt',
  (): JwtModuleOptions => ({
    secret: process.env.JWT_SECRET,
    signOptions: {
      expiresIn: process.env.JWT_EXPIRATION || '15m',
      algorithm: 'HS256',
      issuer: process.env.JWT_ISSUER || 'my-app',
      audience: process.env.JWT_AUDIENCE || 'my-app-users',
    },
  }),
);
```

```typescript
// src/config/validation.schema.ts
import * as Joi from 'joi';

export const validationSchema = Joi.object({
  JWT_SECRET: Joi.string().min(32).required(),
  JWT_EXPIRATION: Joi.string().default('15m'),
  JWT_ISSUER: Joi.string().default('my-app'),
  JWT_AUDIENCE: Joi.string().default('my-app-users'),
  DATABASE_URL: Joi.string().required(),
  PORT: Joi.number().default(3000),
});
```

```typescript
// src/app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import jwtConfig from './config/jwt.config';
import { validationSchema } from './config/validation.schema';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [jwtConfig],
      validationSchema: validationSchema, // Joi валідація при старті
    }),
    // ... інші модулі
  ],
})
export class AppModule {}
```

Тепер застосунок **не запуститься**, якщо `JWT_SECRET` відсутній або коротший за 32 символи:

```bash
$ npm run start:dev
Error: "JWT_SECRET" length must be at least 32 characters long
```

---

## Реалізація AuthService: логіка автентифікації

`AuthService` інкапсулює всю бізнес-логіку автентифікації — реєстрацію користувачів, валідацію облікових даних та генерацію JWT токенів.

### Повна імплементація AuthService

```typescript
// src/auth/auth.service.ts
import {
  Injectable,
  UnauthorizedException,
  ConflictException,
  BadRequestException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UsersService } from '../users/users.service';
import { hash, compare } from 'bcrypt';

interface JwtPayload {
  sub: string;      // User ID
  email: string;    // Email для відображення у UI
  roles: string[];  // Ролі для авторизації
  iat?: number;     // Issued At — встановлюється автоматично
  exp?: number;     // Expiration — встановлюється автоматично
}

@Injectable()
export class AuthService {
  private readonly BCRYPT_ROUNDS = 12; // Cost factor для bcrypt

  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
  ) {}

  /**
   * Реєстрація нового користувача
   * 
   * @throws {ConflictException} Якщо користувач з таким email вже існує
   * @throws {BadRequestException} Якщо дані невалідні
   */
  async register(email: string, password: string) {
    // Перевірка існування користувача
    const existingUser = await this.usersService.findByEmail(email);
    if (existingUser) {
      throw new ConflictException('User with this email already exists');
    }

    // Хешування паролю (cost factor 12 = 2^12 ітерацій)
    const passwordHash = await hash(password, this.BCRYPT_ROUNDS);

    // Створення користувача у базі даних
    const user = await this.usersService.create({
      email,
      passwordHash,
      roles: ['user'], // Дефолтна роль
    });

    // Повертаємо користувача без паролю
    const { passwordHash: _, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }

  /**
   * Вхід користувача та генерація JWT токена
   * 
   * @throws {UnauthorizedException} Якщо credentials невалідні
   */
  async login(email: string, password: string) {
    // Валідація облікових даних
    const user = await this.validateUser(email, password);

    // Генерація JWT токена
    const payload: JwtPayload = {
      sub: user.id,
      email: user.email,
      roles: user.roles,
    };

    const accessToken = this.jwtService.sign(payload);

    return {
      accessToken,
      tokenType: 'Bearer',
      expiresIn: 900, // 15 хвилин у секундах
      user: {
        id: user.id,
        email: user.email,
        roles: user.roles,
      },
    };
  }

  /**
   * Валідація email та паролю користувача
   * 
   * @throws {UnauthorizedException} Якщо користувач не знайдений або пароль не співпадає
   */
  async validateUser(email: string, password: string) {
    // Завантаження користувача з бази даних
    const user = await this.usersService.findByEmail(email);

    if (!user) {
      // Не розкриваємо, що користувач не існує (захист від enumeration атак)
      throw new UnauthorizedException('Invalid credentials');
    }

    // Порівняння хешу паролю
    const isPasswordValid = await compare(password, user.passwordHash);

    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    return user;
  }

  /**
   * Верифікація JWT токена (для ручної перевірки поза Passport)
   */
  async verifyToken(token: string) {
    try {
      const payload = this.jwtService.verify<JwtPayload>(token);
      return payload;
    } catch (error) {
      throw new UnauthorizedException('Invalid or expired token');
    }
  }

  /**
   * Декодування токена без верифікації (для відлагодження)
   */
  decodeToken(token: string) {
    return this.jwtService.decode(token);
  }
}
```

**Детальний розбір методів:**

**1. Метод `register()`:**

- Перевіряє, чи не існує вже користувач з таким email (запобігання дублікатів).
- Хешує пароль з cost factor 12 — баланс між безпекою та продуктивністю.
- Створює користувача з дефолтною роллю `'user'`.
- Повертає користувача без хешу паролю (безпека відповіді API).

**2. Метод `login()`:**

- Викликає `validateUser()` для перевірки credentials.
- Створює мінімальний payload з `sub` (user ID), `email` та `roles`.
- Підписує payload через `JwtService.sign()` — автоматично додаються claims `iat` та `exp`.
- Повертає структуровану відповідь з токеном та метаданими.

**3. Метод `validateUser()`:**

- Завантажує користувача з бази даних за email.
- Використовує `bcrypt.compare()` для безпечного порівняння хешів (захист від timing attacks).
- Повертає загальне повідомлення `'Invalid credentials'` для захисту від enumeration атак (зловмисник не може дізнатися, чи існує email у системі).

::tip
**Захист від timing attacks:** метод `bcrypt.compare()` завжди виконується за однаковий час, навіть якщо паролі різної довжини. Це запобігає атакам, де зловмисник вимірює час відповіді сервера для визначення правильного паролю символ за символом.
::

**4. Метод `verifyToken()`:**

- Дозволяє вручну верифікувати токен поза системою Passport (наприклад, для WebSocket автентифікації).
- `JwtService.verify()` перевіряє підпис та `exp` claim автоматично.
- Кидає виключення, якщо токен недійсний або застарів.

**5. Метод `decodeToken()`:**

- Декодує Base64URL без перевірки підпису.
- Корисний для відлагодження — можна побачити вміст токена без секретного ключа.
- **Ніколи не використовуйте для автентифікації** — лише для логування та аналізу.



---

## Створення AuthController: HTTP ендпоінти

`AuthController` відповідає за прийом HTTP-запитів, валідацію вхідних даних через DTO та делегування бізнес-логіки сервісному шару.

### Повна імплементація контролера

```typescript
// src/auth/auth.controller.ts
import {
  Controller,
  Post,
  Body,
  HttpCode,
  HttpStatus,
  UseGuards,
  Get,
  Request,
} from '@nestjs/common';
import { AuthService } from './auth.service';
import { RegisterDto } from './dto/register.dto';
import { LoginDto } from './dto/login.dto';
import { JwtAuthGuard } from './guards/jwt-auth.guard';

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  /**
   * POST /auth/register
   * Реєстрація нового користувача
   */
  @Post('register')
  async register(@Body() dto: RegisterDto) {
    const user = await this.authService.register(dto.email, dto.password);

    return {
      statusCode: HttpStatus.CREATED,
      message: 'User registered successfully',
      data: {
        id: user.id,
        email: user.email,
        createdAt: user.createdAt,
      },
    };
  }

  /**
   * POST /auth/login
   * Вхід користувача та отримання JWT токена
   * 
   * @returns {accessToken, tokenType, expiresIn, user}
   */
  @Post('login')
  @HttpCode(HttpStatus.OK) // Повертає 200 замість 201
  async login(@Body() dto: LoginDto) {
    const result = await this.authService.login(dto.email, dto.password);

    return {
      statusCode: HttpStatus.OK,
      message: 'Login successful',
      data: result,
    };
  }

  /**
   * GET /auth/profile
   * Отримання профілю поточного користувача (захищений ендпоінт)
   */
  @Get('profile')
  @UseGuards(JwtAuthGuard)
  getProfile(@Request() req) {
    // req.user встановлюється JwtStrategy після верифікації токена
    return {
      statusCode: HttpStatus.OK,
      data: req.user,
    };
  }

  /**
   * POST /auth/verify
   * Верифікація токена (для клієнтів, що хочуть перевірити токен)
   */
  @Post('verify')
  @HttpCode(HttpStatus.OK)
  async verifyToken(@Body('token') token: string) {
    const payload = await this.authService.verifyToken(token);

    return {
      statusCode: HttpStatus.OK,
      message: 'Token is valid',
      data: payload,
    };
  }
}
```

**Детальний розбір ендпоінтів:**

### Ендпоінт POST /auth/register

**Запит:**
```http
POST /auth/register HTTP/1.1
Content-Type: application/json

{
  "email": "ivan@example.com",
  "password": "SecureP@ss123"
}
```

**Успішна відповідь (201 Created):**
```json
{
  "statusCode": 201,
  "message": "User registered successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "ivan@example.com",
    "createdAt": "2026-09-06T10:30:00.000Z"
  }
}
```

**Помилка — користувач вже існує (409 Conflict):**
```json
{
  "statusCode": 409,
  "message": "User with this email already exists",
  "error": "Conflict"
}
```

**Помилка валідації (400 Bad Request):**
```json
{
  "statusCode": 400,
  "message": [
    "Password must be at least 8 characters",
    "Password must contain uppercase, lowercase and number"
  ],
  "error": "Bad Request"
}
```

### Ендпоінт POST /auth/login

**Запит:**
```http
POST /auth/login HTTP/1.1
Content-Type: application/json

{
  "email": "ivan@example.com",
  "password": "SecureP@ss123"
}
```

**Успішна відповідь (200 OK):**
```json
{
  "statusCode": 200,
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6Iml2YW5AZXhhbXBsZS5jb20iLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTY5MzU2NDgwMCwiZXhwIjoxNjkzNTY1NzAwfQ.4Hb3LM-TqHX-2JcGKz9yP3qF8vZ5nR7wQ1xS6mE9kLo",
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

**Помилка — невалідні credentials (401 Unauthorized):**
```json
{
  "statusCode": 401,
  "message": "Invalid credentials",
  "error": "Unauthorized"
}
```

### Ендпоінт GET /auth/profile (захищений)

**Запит з токеном:**
```http
GET /auth/profile HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Успішна відповідь (200 OK):**
```json
{
  "statusCode": 200,
  "data": {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "email": "ivan@example.com",
    "roles": ["user"]
  }
}
```

**Помилка — токен відсутній або недійсний (401 Unauthorized):**
```json
{
  "statusCode": 401,
  "message": "Unauthorized"
}
```

::note
**Декоратор `@HttpCode(HttpStatus.OK)`:** за замовчуванням POST-запити повертають статус `201 Created`. Для логіну семантично правильніше використовувати `200 OK`, оскільки не створюється новий ресурс, а лише генерується токен для існуючого користувача.
::

---

## Валідація вхідних даних через DTO

Data Transfer Objects (DTO) з декораторами `class-validator` забезпечують автоматичну валідацію вхідних даних до виклику контролера.

### RegisterDto: валідація реєстрації

```typescript
// src/auth/dto/register.dto.ts
import {
  IsEmail,
  IsNotEmpty,
  MinLength,
  MaxLength,
  Matches,
  IsString,
} from 'class-validator';

export class RegisterDto {
  @IsEmail({}, { message: 'Invalid email format' })
  @IsNotEmpty({ message: 'Email is required' })
  email: string;

  @IsString()
  @IsNotEmpty({ message: 'Password is required' })
  @MinLength(8, { message: 'Password must be at least 8 characters long' })
  @MaxLength(64, { message: 'Password must not exceed 64 characters' })
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]/, {
    message:
      'Password must contain at least one uppercase letter, one lowercase letter, one number and one special character',
  })
  password: string;
}
```

**Пояснення валідаторів:**

| Декоратор | Призначення |
|-----------|-------------|
| `@IsEmail()` | Перевіряє формат email через регулярний вираз (RFC 5322 compliant). |
| `@IsNotEmpty()` | Забороняє порожні рядки, `null` або `undefined`. |
| `@MinLength(8)` | Мінімальна довжина паролю 8 символів (рекомендація NIST). |
| `@MaxLength(64)` | Максимальна довжина 64 символи (захист від DoS атак через bcrypt). |
| `@Matches()` | Регулярний вираз для перевірки складності паролю. |

**Регулярний вираз для паролю:**

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]+$
```

Розбір по частинах:
- `(?=.*[a-z])` — lookahead assertion: містить хоча б одну малу літеру.
- `(?=.*[A-Z])` — містить хоча б одну велику літеру.
- `(?=.*\d)` — містить хоча б одну цифру.
- `(?=.*[@$!%*?&#])` — містить хоча б один спецсимвол із списку.
- `[A-Za-z\d@$!%*?&#]+` — дозволені символи паролю.

### LoginDto: спрощена валідація

```typescript
// src/auth/dto/login.dto.ts
import { IsEmail, IsNotEmpty, IsString } from 'class-validator';

export class LoginDto {
  @IsEmail()
  @IsNotEmpty()
  email: string;

  @IsString()
  @IsNotEmpty()
  password: string;
}
```

Для логіну не перевіряємо складність паролю, оскільки він вже збережений у базі даних у хешованому вигляді. Перевіряємо лише наявність даних.

### Активація ValidationPipe глобально

Для автоматичної валідації всіх DTO у застосунку додаємо `ValidationPipe` у `main.ts`:

```typescript
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Глобальна валідація через class-validator
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,           // Видаляє поля, не описані у DTO
      forbidNonWhitelisted: true, // Відхиляє запити з зайвими полями
      transform: true,            // Автоматично перетворює типи (string → number)
      disableErrorMessages: false, // У продакшні можна приховати деталі помилок
      validationError: {
        target: false,  // Не включає оригінальний об'єкт у помилку
        value: false,   // Не включає невалідне значення у помилку
      },
    }),
  );

  await app.listen(3000);
  console.log('🚀 Application is running on: http://localhost:3000');
}

bootstrap();
```

**Параметри ValidationPipe:**

- **`whitelist: true`** — автоматично видаляє поля, не описані у DTO. Це захищає від **mass assignment attacks**, де зловмисник додає додаткові поля (наприклад, `isAdmin: true`) у запит.

- **`forbidNonWhitelisted: true`** — замість тихого видалення зайвих полів повертає помилку `400 Bad Request`. Корисно для API, де клієнти мають бути суворо дисципліновані.

- **`transform: true`** — автоматично перетворює примітивні типи. Наприклад, query parameter `?limit=10` (string) перетворюється у number, якщо у DTO поле має тип `number`.

::tip
**У продакшені встановіть `disableErrorMessages: true`** для приховування деталей валідації від потенційних зловмисників. Натомість логуйте детальні помилки на сервері для відлагодження. Клієнт отримає загальне повідомлення `"Validation failed"` без специфіки.
::



---

## Тестування API через HTTP клієнти

Після реалізації автентифікації критично важливо протестувати всі ендпоінти для перевірки коректності роботи.

### Тестування через cURL

**Реєстрація користувача:**

```bash
curl -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecureP@ss123"
  }'
```

**Очікувана відповідь:**
```json
{
  "statusCode": 201,
  "message": "User registered successfully",
  "data": {
    "id": "uuid-here",
    "email": "test@example.com",
    "createdAt": "2026-09-06T10:30:00.000Z"
  }
}
```

**Логін користувача:**

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecureP@ss123"
  }'
```

**Збереження токена у змінну:**

```bash
TOKEN=$(curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecureP@ss123"}' \
  | jq -r '.data.accessToken')

echo "Access Token: $TOKEN"
```

**Доступ до захищеного ендпоінту:**

```bash
curl http://localhost:3000/auth/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Тестування через HTTPie (більш читабельний інтерфейс)

::tabs

::tabs-item{label="Реєстрація"}
```bash
http POST http://localhost:3000/auth/register \
  email=test@example.com \
  password=SecureP@ss123
```
::

::tabs-item{label="Логін"}
```bash
http POST http://localhost:3000/auth/login \
  email=test@example.com \
  password=SecureP@ss123
```
::

::tabs-item{label="Профіль (з токеном)"}
```bash
http GET http://localhost:3000/auth/profile \
  "Authorization: Bearer eyJhbGc..."
```
::

::

### Тестування через Postman

**Налаштування колекції:**

1. Створіть нову колекцію `Authentication API`.
2. Додайте змінну оточення `{{baseUrl}}` = `http://localhost:3000`.
3. Додайте змінну `{{accessToken}}` для автоматичного збереження токена.

**Автоматичне збереження токена після логіну:**

У вкладці **Tests** POST `/auth/login` додайте скрипт:

```javascript
// Автоматично зберігаємо токен у змінну після успішного логіну
const response = pm.response.json();
if (response.statusCode === 200 && response.data.accessToken) {
  pm.environment.set('accessToken', response.data.accessToken);
  console.log('Access token saved to environment');
}
```

**Використання токена у захищених запитах:**

У вкладці **Authorization** виберіть тип `Bearer Token` та вкажіть `{{accessToken}}`.

---

## Обробка помилок та кастомні винятки

Для покращення якості API та діагностики проблем реалізуємо кастомні винятки з детальними повідомленнями.

### Глобальний Exception Filter

```typescript
// src/common/filters/http-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Internal server error';
    let error = 'InternalServerError';

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const exceptionResponse = exception.getResponse();

      if (typeof exceptionResponse === 'object') {
        message = (exceptionResponse as any).message || exception.message;
        error = (exceptionResponse as any).error || exception.name;
      } else {
        message = exceptionResponse;
      }
    }

    // Логування помилки на сервері
    this.logger.error(
      `HTTP ${status} Error: ${message}`,
      exception instanceof Error ? exception.stack : undefined,
    );

    // Відповідь клієнту
    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      method: request.method,
      message: Array.isArray(message) ? message : [message],
      error,
    });
  }
}
```

**Реєстрація фільтра глобально:**

```typescript
// src/main.ts
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalFilters(new AllExceptionsFilter());
  app.useGlobalPipes(new ValidationPipe({ ... }));

  await app.listen(3000);
}
```

Тепер всі помилки повертаються у єдиному форматі:

```json
{
  "statusCode": 401,
  "timestamp": "2026-09-06T10:30:00.000Z",
  "path": "/auth/login",
  "method": "POST",
  "message": ["Invalid credentials"],
  "error": "Unauthorized"
}
```

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Яка різниця між JwtModule.register() та JwtModule.registerAsync()?" icon="i-lucide-help-circle"}

**`register()`** — синхронна конфігурація, де параметри передаються безпосередньо у вигляді об'єкта. Використовується, коли конфігурація статична та відома на етапі компіляції. Недолік — неможливо використовувати змінні оточення або асинхронне завантаження секретів.

**`registerAsync()`** — асинхронна конфігурація через factory function, що дозволяє dependency injection `ConfigService` або інших провайдерів. Використовується для динамічного завантаження конфігурації з `.env`, AWS Secrets Manager або API. Рекомендується для всіх продакшн застосунків.

**Приклад різниці:**

```typescript
// register() — статична конфігурація
JwtModule.register({
  secret: 'hardcoded-secret', // ❌ Небезпечно
  signOptions: { expiresIn: '15m' },
})

// registerAsync() — динамічна конфігурація
JwtModule.registerAsync({
  inject: [ConfigService],
  useFactory: (config: ConfigService) => ({
    secret: config.get('JWT_SECRET'), // ✅ Завантаження з .env
    signOptions: { expiresIn: config.get('JWT_EXPIRATION') },
  }),
})
```

::

::accordion-item{label="❓ Чому метод login() повертає об'єкт user разом з токеном?" icon="i-lucide-help-circle"}

Це покращує user experience frontend застосунків. Після успішного логіну клієнт отримує не лише токен для автентифікації наступних запитів, а й базові дані користувача (ID, email, ролі) для негайного відображення у UI без додаткового запиту `/auth/profile`. Це зменшує кількість запитів та затримки завантаження сторінки після входу.

**Альтернативний підхід:** повертати лише токен, а клієнт робить наступний запит до `/auth/profile` для завантаження даних. Цей підхід чистіший з точки зору розділення відповідальностей, але повільніший через додатковий roundtrip.

::

::accordion-item{label="❓ Чи безпечно зберігати ролі користувача у JWT payload?" icon="i-lucide-help-circle"}

**Так, якщо розумієте обмеження.** JWT токени є **підписаними, але не зашифрованими** — будь-хто може декодувати Base64URL та прочитати payload. Проте **зловмисник не може змінити ролі** без знання секретного ключа, оскільки це порушить підпис.

**Безпечно зберігати:**
- Ролі користувача (`['user', 'admin']`)
- Публічні дані (email, ім'я)
- Metadata для авторизації (subscription tier, permissions)

**Небезпечно зберігати:**
- Паролі або їхні хеші
- Номери кредитних карток
- Приватні ключі або API secrets
- Конфіденційні медичні або фінансові дані

**Важливо:** якщо ролі користувача змінюються у базі даних (адміністратор надає права модератора), вже видані токени **не оновляться автоматично** до закінчення їхнього TTL. Для критичних змін використовуйте короткий TTL (5–15 хвилин) або механізм blacklist.

::

::accordion-item{label="❓ Чому bcrypt cost factor встановлений на 12, а не 10 або 14?" icon="i-lucide-help-circle"}

**Cost factor** визначає кількість ітерацій хешування: `2^cost`. Більший cost = більша безпека, але повільніше хешування.

**Cost factor 10:** `2^10 = 1024` ітерації — мінімальний рекомендований рівень (2010-ті роки).

**Cost factor 12:** `2^12 = 4096` ітерації — оптимальний баланс для сучасних серверів (2020-ті роки). Хешування займає ~200–300 мс на сервері середньої потужності.

**Cost factor 14:** `2^14 = 16384` ітерації — дуже безпечно, але хешування займає ~1 секунду, що може створити проблеми при high-load реєстрації.

**Правило вибору:** cost factor має бути налаштований так, щоб хешування займало **100–500 мс** на вашому продакшн сервері. Це робить brute-force атаки економічно недоцільними (мільйони спроб займуть роки), але не сповільнює легітимних користувачів.

**Тест продуктивності:**

```typescript
import { hash } from 'bcrypt';

async function benchmarkBcrypt() {
  const password = 'TestPassword123';

  for (const rounds of [10, 11, 12, 13, 14]) {
    const start = Date.now();
    await hash(password, rounds);
    const duration = Date.now() - start;
    console.log(`Cost ${rounds}: ${duration}ms`);
  }
}

benchmarkBcrypt();
```

::

::

---

## Ключові висновки

::card-group

::card{title="🔧 Модульна архітектура" icon="i-lucide-boxes"}

AuthModule інкапсулює всю логіку автентифікації — сервіси, контролери, Guards та стратегії. JwtModule конфігурується асинхронно через `registerAsync()` з доступом до ConfigService для безпечного завантаження секретів.

::

::card{title="🔐 AuthService як єдине джерело істини" icon="i-lucide-shield"}

Вся бізнес-логіка автентифікації (реєстрація, валідація, генерація токенів) централізована у AuthService. Контролер лише приймає HTTP-запити та делегує обробку сервісу. Це забезпечує легке тестування та повторне використання логіки.

::

::card{title="✅ Валідація через DTO та class-validator" icon="i-lucide-check-circle"}

Data Transfer Objects з декораторами `class-validator` автоматично валідують вхідні дані до виклику контролера. ValidationPipe з `whitelist: true` захищає від mass assignment атак. Складність паролів забезпечується регулярними виразами.

::

::card{title="🛡️ Безпека через bcrypt та змінні оточення" icon="i-lucide-lock"}

Паролі хешуються з cost factor 12 через bcrypt (захист від brute-force). Секретний ключ JWT завантажується з змінних оточення та валідується при старті застосунку. Помилки автентифікації повертають загальне повідомлення без деталей для захисту від enumeration.

::

::

---

## Рекомендовані ресурси для поглибленого вивчення

- **NestJS JWT Documentation:** офіційна документація модуля `@nestjs/jwt` з прикладами конфігурації та інтеграції.

- **NestJS Passport Documentation:** гайд з інтеграції Passport.js для створення кастомних стратегій автентифікації.

- **class-validator GitHub:** повний список доступних валідаторів з прикладами для різних типів даних.

- **bcrypt npm package:** документація бібліотеки bcrypt з рекомендаціями щодо вибору cost factor та безпечного хешування.

::note
У наступній лекції ми детально розглянемо **Passport стратегії у NestJS** — створення JwtStrategy для верифікації токенів, LocalStrategy для валідації username/password, інтеграцію з Guards та кастомні декоратори для витягування даних користувача. Ви навчитеся створювати гнучкі системи автентифікації з підтримкою кількох стратегій одночасно.
::
