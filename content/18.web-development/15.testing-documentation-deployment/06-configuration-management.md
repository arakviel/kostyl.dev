# Керування конфігурацією

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати управління налаштуваннями застосунку через `@nestjs/config` модуль.
- Навчитися організовувати конфігурацію для різних середовищ (development, staging, production).
- Освоїти валідацію environment variables через Joi schema для запобігання помилкам конфігурації.
- Зрозуміти принципи безпечного зберігання sensitive даних (паролі, API keys, secrets).
- Навчитися створювати типізовані configuration files для структурованого доступу до налаштувань.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Environment Variables:** системні змінні оточення, що зберігають конфігураційні параметри (DATABASE_URL, PORT, JWT_SECRET).
- **Configuration Management:** процес організації, валідації та доступу до налаштувань застосунку.
- **ConfigService:** NestJS сервіс для type-safe доступу до конфігураційних параметрів через Dependency Injection.
- **Joi Validation:** бібліотека для декларативної валідації даних через schema-based підхід.
- **Namespaced Configuration:** логічне групування налаштувань за функціональними доменами (database, jwt, redis).

::

::

---

## Короткий зміст

У цій лекції розглядається управління налаштуваннями застосунку для різних середовищ:

- **@nestjs/config модуль** — офіційне рішення для configuration management, wrapper над dotenv з DI підтримкою, інсталяція та реєстрація через `ConfigModule.forRoot()`
- **.env файли** — зберігання environment variables: DATABASE_URL, JWT_SECRET, PORT, NODE_ENV, формат KEY=VALUE, .env.local для локальних override, .gitignore для безпеки
- **ConfigModule.forRoot() опції** — `isGlobal: true` для доступу у всіх модулях, `envFilePath` для custom шляху до .env, `ignoreEnvFile: true` для production (використання system env vars), `load` для custom configuration files
- **ConfigService** — сервіс для доступу до конфігурації, injection через constructor, методи `get<T>(key)` з type safety, `getOrThrow()` для required variables, default values через другий параметр
- **Валідація через Joi** — schema validation для env variables, забезпечення required fields, type checking (string, number, boolean), допустимі значення через enum, приклад schema для DATABASE_URL, JWT_SECRET, PORT
- **Custom configuration files** — окремі TypeScript файли для логічного групування (database.config.ts, jwt.config.ts), factory functions що повертають configuration object, registerAs() для namespaced config
- **Different configs для середовищ** — .env.development, .env.staging, .env.production, conditional loading на основі NODE_ENV, overrides для local development
- **Best practices** — ніколи не commit .env до git, використання example файлів (.env.example), обов'язкова валідація у production, типізація через TypeScript interfaces

Розглядаються практичні приклади: налаштування database connection через ConfigService, JWT configuration, різні configs для dev/prod, валідація env variables через Joi schema.

---

## Проблема хардкоджених налаштувань

На попередніх лекціях ми розробили backend застосунок із підключенням до бази даних, JWT автентифікацією, інтеграцією зовнішніх сервісів. Проте всі налаштування були **захардкоджені** безпосередньо у коді:

```typescript
// ❌ ПОГАНА ПРАКТИКА: хардкоджені налаштування
@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',        // Захардкоджено
      port: 5432,
      username: 'postgres',
      password: 'mysecretpass', // НЕБЕЗПЕЧНО: пароль у коді!
      database: 'blog_db',
      synchronize: true,
    }),
    JwtModule.register({
      secret: 'super-secret-key-12345', // НЕБЕЗПЕЧНО: секрет у коді!
      signOptions: { expiresIn: '1h' },
    }),
  ],
})
export class AppModule {}
```

Такий підхід створює низку критичних проблем:

**1. Небезпека витоку credentials.** Паролі до БД, API keys, JWT secrets зберігаються у коді, який комітиться у Git репозиторій. Навіть якщо репозиторій приватний, це порушує принцип **least privilege** — розробники, що не мають доступу до production БД, бачать production паролі у коді.

**2. Неможливість змінити налаштування без зміни коду.** Щоб змінити порт БД або URL зовнішнього API, потрібно редагувати код, пересобирати застосунок та деплоїти. Це ускладнює операційну підтримку.

**3. Відсутність різних налаштувань для середовищ.** У development ви використовуєте локальну PostgreSQL на `localhost:5432`, у staging — cloud БД на `staging-db.example.com:5432`, у production — кластер на `prod-db.example.com:5432`. З хардкодженими налаштуваннями доведеться підтримувати кілька гілок коду або використовувати умовну логіку.

**4. Складність тестування.** E2E тести мають підключатися до тестової БД, а не production. З хардкодженими налаштуваннями це вимагає модифікації коду перед запуском тестів.

**Рішення — винесення конфігурації у environment variables.** Замість хардкоджених значень ви зберігаєте налаштування у змінних оточення, які **не потрапляють у Git** та можуть змінюватися без зміни коду:

```typescript
// ✅ ХОРОША ПРАКТИКА: конфігурація через environment variables
@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      useFactory: (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get('DATABASE_HOST'),
        port: configService.get('DATABASE_PORT'),
        username: configService.get('DATABASE_USER'),
        password: configService.get('DATABASE_PASSWORD'),
        database: configService.get('DATABASE_NAME'),
        synchronize: configService.get('NODE_ENV') === 'development',
      }),
      inject: [ConfigService],
    }),
  ],
})
export class AppModule {}
```

Значення змінних зберігаються у `.env` файлі, який **додається до `.gitignore`** та не комітиться у репозиторій.

::plant-uml{alt="Управління конфігурацією через environment variables"}

```plantuml
@startuml
skinparam style plain
skinparam backgroundColor #FFFFFF

rectangle "Environment Variables" as Env #FEF3C7 {
  card ".env файл" as EnvFile
  card "System env vars" as SysEnv
}

rectangle "@nestjs/config" as Config #DCFCE7 {
  card "ConfigModule" as CM
  card "ConfigService" as CS
  card "Joi Validation" as Joi
}

rectangle "Application Code" as App #DBEAFE {
  card "Services" as Services
  card "Modules" as Modules
  card "Controllers" as Controllers
}

EnvFile --> CM : "Завантаження"
SysEnv --> CM : "Завантаження"
CM --> Joi : "Валідація"
Joi --> CS : "Надання доступу"
CS --> Services : "Injection"
CS --> Modules : "Injection"
CS --> Controllers : "Injection"

@enduml
```

::

---

## Інтеграція @nestjs/config

NestJS надає офіційну бібліотеку `@nestjs/config` — wrapper над популярною бібліотекою `dotenv` з інтеграцією у Dependency Injection систему.

### Встановлення

```bash
npm install --save @nestjs/config
```

Опціонально, для валідації змінних:

```bash
npm install --save joi
```

### Базова конфігурація

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true, // Робить ConfigService доступним у всіх модулях
      envFilePath: '.env', // Шлях до .env файлу
    }),
    // Інші модулі
  ],
})
export class AppModule {}
```

**`ConfigModule.forRoot()`** ініціалізує configuration management систему. Параметри:

- **`isGlobal: true`** — ConfigService стає global module та доступний у всіх модулях без повторного імпорту ConfigModule.
- **`envFilePath`** — шлях до `.env` файлу (або масив шляхів для кількох файлів). За замовчуванням `.env` у корені проєкту.
- **`ignoreEnvFile`** — ігнорувати `.env` файл та використовувати лише system environment variables (корисно у production, де env vars встановлюються через Docker/Kubernetes).
- **`load`** — масив функцій для завантаження custom configuration files.
- **`validationSchema`** — Joi schema для валідації змінних при старті застосунку.

### Створення .env файлу

Створіть файл `.env` у корені проєкту:

```bash
# .env
NODE_ENV=development

# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=mysecretpassword
DATABASE_NAME=blog_db

# JWT
JWT_SECRET=super-secret-jwt-key-change-in-production
JWT_EXPIRATION=7d

# Server
PORT=3000
API_PREFIX=api

# External Services
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Формат:** `KEY=VALUE` (без пробілів навколо `=`). Коментарі починаються з `#`.

### .gitignore — обов'язково!

**Критично важливо** додати `.env` до `.gitignore`, щоб не закомітити паролі у Git:

```gitignore
# .gitignore
.env
.env.local
.env.*.local
```

Натомість створіть `.env.example` з шаблоном змінних (без реальних значень):

```bash
# .env.example
NODE_ENV=development

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=

JWT_SECRET=
JWT_EXPIRATION=7d

PORT=3000
```

Закомітьте `.env.example` у Git як документацію для нових розробників: які змінні потрібно налаштувати.

---

## Використання ConfigService

Після налаштування `ConfigModule` використовуйте `ConfigService` для доступу до environment variables через Dependency Injection.

### Injection у сервіси

```typescript
// auth/auth.service.ts
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
  ) {}

  async generateToken(userId: string): Promise<string> {
    const payload = { sub: userId };
    
    // Отримання JWT_SECRET з конфігурації
    const secret = this.configService.get<string>('JWT_SECRET');
    const expiresIn = this.configService.get<string>('JWT_EXPIRATION', '1h');

    return this.jwtService.sign(payload, { secret, expiresIn });
  }

  getEnvironment(): string {
    return this.configService.get<string>('NODE_ENV', 'development');
  }
}
```

### Методи ConfigService

**`get<T>(key: string, defaultValue?: T): T`** — отримує значення змінної за ключем. Якщо змінна не існує, повертає `defaultValue` або `undefined`.

```typescript
const port = this.configService.get<number>('PORT', 3000);
const isProduction = this.configService.get<string>('NODE_ENV') === 'production';
```

**`getOrThrow<T>(key: string): T`** — отримує значення або **викидає виняток**, якщо змінна не визначена. Корисно для обов'язкових змінних:

```typescript
// Якщо JWT_SECRET відсутній, застосунок не стартує
const jwtSecret = this.configService.getOrThrow<string>('JWT_SECRET');
```

**Type safety:** Використовуйте generic `<T>` для типізації, проте пам'ятайте: ConfigService повертає **рядки** з `.env` файлу. Якщо потрібен number, конвертуйте вручну:

```typescript
const port = parseInt(this.configService.get<string>('PORT', '3000'), 10);
// Або через Number()
const port = Number(this.configService.get<string>('PORT', '3000'));
```

### Injection у модулі

Для динамічної конфігурації модулів використовуйте `forRootAsync()` або `forFeatureAsync()`:

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    
    // Динамічна конфігурація TypeORM через ConfigService
    TypeOrmModule.forRootAsync({
      useFactory: (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get('DATABASE_HOST'),
        port: configService.get<number>('DATABASE_PORT'),
        username: configService.get('DATABASE_USER'),
        password: configService.get('DATABASE_PASSWORD'),
        database: configService.get('DATABASE_NAME'),
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
        synchronize: configService.get('NODE_ENV') === 'development',
        logging: configService.get('NODE_ENV') === 'development',
      }),
      inject: [ConfigService],
    }),

    // Динамічна конфігурація JWT
    JwtModule.registerAsync({
      useFactory: (configService: ConfigService) => ({
        secret: configService.getOrThrow('JWT_SECRET'),
        signOptions: {
          expiresIn: configService.get('JWT_EXPIRATION', '7d'),
        },
      }),
      inject: [ConfigService],
    }),
  ],
})
export class AppModule {}
```

::tip
**`forRootAsync()` vs `forRoot()`:** Асинхронна версія дозволяє використовувати Dependency Injection для отримання залежностей (наприклад, `ConfigService`) під час ініціалізації модуля. Використовуйте `forRootAsync()` для динамічної конфігурації на основі environment variables.
::

### Використання у main.ts

У файлі `main.ts` ConfigService недоступний через DI, оскільки застосунок ще не створений. Натомість використовуйте `app.get()` після створення:

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { ConfigService } from '@nestjs/config';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Отримання ConfigService після створення app
  const configService = app.get(ConfigService);

  const port = configService.get<number>('PORT', 3000);
  const apiPrefix = configService.get<string>('API_PREFIX', 'api');

  app.setGlobalPrefix(apiPrefix);

  await app.listen(port);
  console.log(`🚀 Server running on http://localhost:${port}/${apiPrefix}`);
}

bootstrap();
```

---

## Валідація environment variables через Joi

Однією з найпоширеніших причин збоїв у production є **відсутність або некоректні environment variables**. Застосунок стартує, але падає при спробі підключитися до БД, оскільки `DATABASE_PASSWORD` не встановлений.

**Joi** дозволяє декларативно описати schema для environment variables та **валідувати їх при старті** застосунку. Якщо валідація провалюється, застосунок не запуститься та виведе зрозуміле повідомлення про помилку.

### Встановлення Joi

```bash
npm install --save joi
```

### Створення validation schema

```typescript
// config/validation.schema.ts
import * as Joi from 'joi';

export const validationSchema = Joi.object({
  // NODE_ENV має бути одним із трьох значень
  NODE_ENV: Joi.string()
    .valid('development', 'staging', 'production')
    .default('development'),

  // PORT має бути числом від 1 до 65535
  PORT: Joi.number()
    .port()
    .default(3000),

  // Database змінні обов'язкові
  DATABASE_HOST: Joi.string().required(),
  DATABASE_PORT: Joi.number().port().default(5432),
  DATABASE_USER: Joi.string().required(),
  DATABASE_PASSWORD: Joi.string().required(),
  DATABASE_NAME: Joi.string().required(),

  // JWT змінні обов'язкові та мають мінімальну довжину
  JWT_SECRET: Joi.string().min(32).required(),
  JWT_EXPIRATION: Joi.string().default('7d'),

  // Redis опціональні (можна не налаштовувати)
  REDIS_HOST: Joi.string().optional(),
  REDIS_PORT: Joi.number().port().optional(),

  // SMTP налаштування
  SMTP_HOST: Joi.string().required(),
  SMTP_PORT: Joi.number().port().required(),
  SMTP_USER: Joi.string().email().required(),
  SMTP_PASSWORD: Joi.string().required(),
});
```

### Інтеграція з ConfigModule

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { validationSchema } from './config/validation.schema';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      validationSchema, // Додаємо Joi schema
      validationOptions: {
        allowUnknown: true, // Дозволяє змінні, не описані у schema
        abortEarly: false,  // Показує всі помилки валідації, а не лише першу
      },
    }),
  ],
})
export class AppModule {}
```

Тепер при запуску застосунку, якщо будь-яка обов'язкова змінна відсутня або має некоректний формат, ви побачите детальну помилку:

::terminal-preview{title="npm start — Validation Error" :cursor="false"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">npm start</strong></div>
<div class="line"></div>
<div class="line"><span class="text-rose-400 font-bold">Error:</span> Config validation error: "DATABASE_PASSWORD" is required</div>
<div class="line"></div>
<div class="line">ValidationError: </div>
<div class="line">  - "DATABASE_PASSWORD" is required</div>
<div class="line">  - "JWT_SECRET" length must be at least 32 characters long</div>
<div class="line">  - "SMTP_USER" must be a valid email</div>
<div class="line"></div>
<div class="line"><span class="text-rose-400">Application failed to start. Fix the configuration errors above.</span></div>

::

Це запобігає «silent failures» — ситуаціям, коли застосунок стартує, але падає при першій спробі використати некоректну конфігурацію.

::warning
**Joi валідує лише формат, не безпеку!** Joi перевірить, що `JWT_SECRET` має мінімум 32 символи, але **не перевірить**, чи це криптографічно стійкий ключ. Відповідальність за генерацію безпечних secrets лежить на розробникові:

```bash
# Генерація безпечного JWT secret (32 байти у hex)
openssl rand -hex 32

# Результат: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

Додайте згенерований ключ до `.env`:

```bash
JWT_SECRET=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```
::


### Joi валідаційні методи

Основні методи для різних типів даних:

**Рядки (String):**
- `.string()` — має бути рядком.
- `.required()` — обов'язкове поле.
- `.optional()` — опціональне поле.
- `.default(value)` — значення за замовчуванням.
- `.min(n)` / `.max(n)` — мінімальна/максимальна довжина.
- `.email()` — валідний email формат.
- `.uri()` — валідний URI.
- `.valid(...values)` — одне з перелічених значень (enum).

**Числа (Number):**
- `.number()` — має бути числом.
- `.port()` — валідний порт (1-65535).
- `.min(n)` / `.max(n)` — мінімальне/максимальне значення.
- `.integer()` — ціле число.
- `.positive()` / `.negative()` — додатне/від'ємне.

**Булеві (Boolean):**
- `.boolean()` — має бути `true` або `false`.

**Приклади:**

```typescript
{
  API_RATE_LIMIT: Joi.number().integer().min(1).max(10000).default(100),
  ENABLE_SWAGGER: Joi.boolean().default(true),
  ALLOWED_ORIGINS: Joi.string().default('http://localhost:3000,http://localhost:4200'),
  LOG_LEVEL: Joi.string().valid('error', 'warn', 'info', 'debug').default('info'),
}
```

---

## Custom configuration files

Для великих застосунків зберігання всіх змінних у плоскій структурі `.env` файлу стає незручним. Натомість можна створити **окремі TypeScript файли** для логічного групування налаштувань за доменами (database, jwt, mail, redis тощо).

### Структура configuration files

```
src/
├── config/
│   ├── database.config.ts
│   ├── jwt.config.ts
│   ├── mail.config.ts
│   ├── redis.config.ts
│   └── validation.schema.ts
├── app.module.ts
└── main.ts
```

### Приклад: database.config.ts

```typescript
// config/database.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('database', () => ({
  host: process.env.DATABASE_HOST || 'localhost',
  port: parseInt(process.env.DATABASE_PORT, 10) || 5432,
  username: process.env.DATABASE_USER || 'postgres',
  password: process.env.DATABASE_PASSWORD,
  name: process.env.DATABASE_NAME || 'blog_db',
  synchronize: process.env.NODE_ENV === 'development',
  logging: process.env.NODE_ENV === 'development',
}));
```

**`registerAs(namespace, factory)`** реєструє configuration factory під певним namespace. Це дозволяє структурувати доступ до конфігурації через nested keys:

```typescript
// Замість this.configService.get('DATABASE_HOST')
// Використовуємо namespaced доступ:
this.configService.get('database.host')
this.configService.get('database.port')
```

### Приклад: jwt.config.ts

```typescript
// config/jwt.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('jwt', () => ({
  secret: process.env.JWT_SECRET,
  expiresIn: process.env.JWT_EXPIRATION || '7d',
  refreshSecret: process.env.JWT_REFRESH_SECRET,
  refreshExpiresIn: process.env.JWT_REFRESH_EXPIRATION || '30d',
}));
```

### Приклад: mail.config.ts

```typescript
// config/mail.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('mail', () => ({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT, 10) || 587,
  user: process.env.SMTP_USER,
  password: process.env.SMTP_PASSWORD,
  from: process.env.MAIL_FROM || 'noreply@example.com',
  secure: process.env.SMTP_SECURE === 'true',
}));
```

### Підключення до ConfigModule

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import databaseConfig from './config/database.config';
import jwtConfig from './config/jwt.config';
import mailConfig from './config/mail.config';
import { validationSchema } from './config/validation.schema';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [databaseConfig, jwtConfig, mailConfig], // Завантаження custom configs
      validationSchema,
    }),
  ],
})
export class AppModule {}
```

### Використання namespaced config

```typescript
// database/database.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigService } from '@nestjs/config';

@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      useFactory: (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get('database.host'),
        port: configService.get('database.port'),
        username: configService.get('database.username'),
        password: configService.get('database.password'),
        database: configService.get('database.name'),
        synchronize: configService.get('database.synchronize'),
        logging: configService.get('database.logging'),
        entities: [__dirname + '/../**/*.entity{.ts,.js}'],
      }),
      inject: [ConfigService],
    }),
  ],
})
export class DatabaseModule {}
```

**Переваги namespaced config:**

1. **Структурованість:** логічне групування налаштувань за доменами замість плоскої структури.
2. **Autocomplete:** TypeScript може надати автодоповнення для `database.host`, `jwt.secret` тощо (див. наступний розділ про типізацію).
3. **Легше тестувати:** можна замокати окремий namespace замість всієї конфігурації.
4. **Масштабованість:** додавання нових доменів (redis, elastic, stripe) не захаращує `.env` файл.

---

## Типізація конфігурації через TypeScript

Для type-safe доступу до конфігурації створіть **TypeScript interfaces**, що описують структуру кожного namespace.

### Створення типів

```typescript
// config/configuration.interface.ts

export interface DatabaseConfig {
  host: string;
  port: number;
  username: string;
  password: string;
  name: string;
  synchronize: boolean;
  logging: boolean;
}

export interface JwtConfig {
  secret: string;
  expiresIn: string;
  refreshSecret: string;
  refreshExpiresIn: string;
}

export interface MailConfig {
  host: string;
  port: number;
  user: string;
  password: string;
  from: string;
  secure: boolean;
}

// Глобальний інтерфейс конфігурації
export interface AppConfig {
  database: DatabaseConfig;
  jwt: JwtConfig;
  mail: MailConfig;
}
```

### Використання типізованих конфігів

```typescript
// auth/auth.service.ts
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtConfig } from '../config/configuration.interface';

@Injectable()
export class AuthService {
  private jwtConfig: JwtConfig;

  constructor(private readonly configService: ConfigService) {
    // Type-safe доступ до JWT config
    this.jwtConfig = this.configService.get<JwtConfig>('jwt');
  }

  async generateToken(userId: string): Promise<string> {
    // Autocomplete для jwtConfig.secret, jwtConfig.expiresIn
    return this.jwtService.sign(
      { sub: userId },
      {
        secret: this.jwtConfig.secret,
        expiresIn: this.jwtConfig.expiresIn,
      },
    );
  }

  async generateRefreshToken(userId: string): Promise<string> {
    return this.jwtService.sign(
      { sub: userId },
      {
        secret: this.jwtConfig.refreshSecret,
        expiresIn: this.jwtConfig.refreshExpiresIn,
      },
    );
  }
}
```

### Custom ConfigService wrapper (опціонально)

Для повної type safety можна створити обгортку над ConfigService:

```typescript
// config/typed-config.service.ts
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AppConfig } from './configuration.interface';

@Injectable()
export class TypedConfigService {
  constructor(private configService: ConfigService) {}

  get database() {
    return this.configService.get<AppConfig['database']>('database');
  }

  get jwt() {
    return this.configService.get<AppConfig['jwt']>('jwt');
  }

  get mail() {
    return this.configService.get<AppConfig['mail']>('mail');
  }
}
```

Використання:

```typescript
// auth/auth.service.ts
@Injectable()
export class AuthService {
  constructor(private readonly config: TypedConfigService) {}

  async generateToken(userId: string): Promise<string> {
    // Повна type safety та autocomplete
    const secret = this.config.jwt.secret;
    const expiresIn = this.config.jwt.expiresIn;

    return this.jwtService.sign({ sub: userId }, { secret, expiresIn });
  }
}
```

::tip
**TypeScript strict mode:** Увімкніть `strict: true` у `tsconfig.json` для виявлення потенційних `undefined` значень під час компіляції. Це запобіжить runtime помилкам через відсутні environment variables.
::


---

## Різні конфігурації для середовищ

У реальних проєктах застосунок деплоїться у кілька середовищ із різними налаштуваннями:

- **Development** — локальна розробка на `localhost`, детальне логування, `synchronize: true` для автоматичних міграцій БД.
- **Staging** — тестове середовище, близьке до production, але з тестовими даними та менш строгими обмеженнями.
- **Production** — продакшн середовище з реальними користувачами, максимальна безпека, мінімальне логування, `synchronize: false`.

### Структура .env файлів

Створіть окремі `.env` файли для кожного середовища:

```
.env                  # Базові змінні (закомічені як .env.example)
.env.development      # Development налаштування
.env.staging          # Staging налаштування
.env.production       # Production налаштування (НЕ комітити!)
.env.local            # Локальні override (НЕ комітити!)
```

**Пріоритет завантаження:** `.env.local` > `.env.<NODE_ENV>` > `.env`

Додайте до `.gitignore`:

```gitignore
.env
.env.local
.env.*.local
.env.production
```

### Приклад: .env.development

```bash
# .env.development
NODE_ENV=development

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=devpassword
DATABASE_NAME=blog_dev

JWT_SECRET=dev-secret-key-not-for-production-use-only-32chars
JWT_EXPIRATION=7d

PORT=3000
ENABLE_SWAGGER=true
LOG_LEVEL=debug
```

### Приклад: .env.production

```bash
# .env.production
NODE_ENV=production

DATABASE_HOST=prod-db.example.com
DATABASE_PORT=5432
DATABASE_USER=prod_user
DATABASE_PASSWORD=ultra-secure-production-password-from-secrets-manager
DATABASE_NAME=blog_prod

JWT_SECRET=production-secret-generated-by-openssl-rand-hex-32-see-docs
JWT_EXPIRATION=1h

PORT=8080
ENABLE_SWAGGER=false
LOG_LEVEL=error
```

### Завантаження відповідного .env файлу

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: [
        `.env.${process.env.NODE_ENV || 'development'}`, // .env.development або .env.production
        '.env', // Fallback до базового .env
      ],
      validationSchema,
    }),
  ],
})
export class AppModule {}
```

Тепер при запуску застосунку NODE_ENV визначає, який `.env` файл завантажується:

::terminal-preview{title="Development" :cursor="false"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">NODE_ENV=development npm run start:dev</strong></div>
<div class="line"></div>
<div class="line"><span class="text-emerald-400">✓</span> Loaded .env.development</div>
<div class="line"><span class="text-sky-400">ℹ</span> Database: localhost:5432/blog_dev</div>
<div class="line"><span class="text-sky-400">ℹ</span> Swagger enabled at http://localhost:3000/api/docs</div>
<div class="line"><span class="text-emerald-400">✓</span> Server running on http://localhost:3000</div>

::

::terminal-preview{title="Production" :cursor="false"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">NODE_ENV=production npm run start:prod</strong></div>
<div class="line"></div>
<div class="line"><span class="text-emerald-400">✓</span> Loaded .env.production</div>
<div class="line"><span class="text-sky-400">ℹ</span> Database: prod-db.example.com:5432/blog_prod</div>
<div class="line"><span class="text-amber-400">⚠</span> Swagger disabled in production</div>
<div class="line"><span class="text-emerald-400">✓</span> Server running on http://localhost:8080</div>

::

### Local overrides через .env.local

Кожен розробник може створити `.env.local` для перевизначення змінних без модифікації `.env.development`:

```bash
# .env.local (не комітити!)
DATABASE_PASSWORD=my-local-password
SMTP_HOST=localhost
SMTP_PORT=1025  # Використання локального MailHog для тестування email
```

Це дозволяє розробникам налаштовувати локальне середовище без конфліктів у Git.

---

## Production конфігурація без .env файлів

У production середовищі зазвичай **не використовують `.env` файли**, а встановлюють environment variables через:

- **Docker:** змінні у `docker-compose.yml` або Kubernetes Secrets.
- **Cloud platforms:** AWS Systems Manager Parameter Store, Azure Key Vault, Google Secret Manager.
- **CI/CD pipelines:** змінні у GitHub Actions Secrets, GitLab CI/CD Variables.

### Ігнорування .env у production

```typescript
// app.module.ts
ConfigModule.forRoot({
  isGlobal: true,
  ignoreEnvFile: process.env.NODE_ENV === 'production', // У production не використовувати .env
  validationSchema,
})
```

При `ignoreEnvFile: true` ConfigModule читає **лише system environment variables**, встановлені операційною системою або контейнеризацією.

### Приклад: Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      NODE_ENV: production
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_USER: prod_user
      DATABASE_PASSWORD: ${DATABASE_PASSWORD} # Змінна з .env (не закомічена)
      DATABASE_NAME: blog_prod
      JWT_SECRET: ${JWT_SECRET}
      JWT_EXPIRATION: 1h

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: prod_user
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_DB: blog_prod
```

Запуск:

```bash
# Встановлення змінних через .env (не закомічений)
echo "DATABASE_PASSWORD=secure-password" > .env
echo "JWT_SECRET=$(openssl rand -hex 32)" >> .env

# Запуск через Docker Compose
docker-compose up -d
```

::warning
**Ніколи не комітьте production .env у Git!** Використовуйте secrets management системи (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) для зберігання чутливих даних у production.
::

---

## Best Practices управління конфігурацією

### 1. Ніколи не комітьте .env у Git

**Додайте до .gitignore:**

```gitignore
.env
.env.local
.env.*.local
.env.production
.env.staging
```

**Натомість закомітьте .env.example:**

```bash
# .env.example
NODE_ENV=development

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=

JWT_SECRET=
JWT_EXPIRATION=7d
```

Новий розробник копіює `.env.example` → `.env` та заповнює значення.

### 2. Використовуйте Joi валідацію

**Обов'язкова валідація у production** запобігає запуску застосунку з некоректною конфігурацією:

```typescript
ConfigModule.forRoot({
  validationSchema,
  validationOptions: {
    abortEarly: false, // Показати всі помилки
  },
})
```

### 3. Генеруйте криптографічно стійкі секрети

```bash
# JWT secret (32 байти)
openssl rand -hex 32

# Database password (24 символи, alphanumeric + special chars)
openssl rand -base64 24
```

### 4. Різні конфігурації для середовищ

Використовуйте `.env.development`, `.env.staging`, `.env.production` замість умовної логіки у коді:

```typescript
// ❌ ПОГАНА ПРАКТИКА: умовна логіка
const dbHost = process.env.NODE_ENV === 'production'
  ? 'prod-db.example.com'
  : 'localhost';

// ✅ ХОРОША ПРАКТИКА: змінні у .env файлах
const dbHost = configService.get('DATABASE_HOST');
```

### 5. Використовуйте namespaced конфігурацію

Для великих застосунків групуйте налаштування за доменами:

```typescript
this.configService.get('database.host')
this.configService.get('jwt.secret')
this.configService.get('mail.from')
```

### 6. Типізуйте конфігурацію через TypeScript

Створюйте interfaces для type-safe доступу та autocomplete:

```typescript
interface JwtConfig {
  secret: string;
  expiresIn: string;
}

const jwtConfig = this.configService.get<JwtConfig>('jwt');
```

### 7. Використовуйте getOrThrow() для обов'язкових змінних

```typescript
// Якщо JWT_SECRET відсутній, застосунок не запуститься
const secret = this.configService.getOrThrow<string>('JWT_SECRET');
```

### 8. Не зберігайте secrets у .env файлах у production

Використовуйте secrets management системи:
- **AWS Secrets Manager** для AWS.
- **Azure Key Vault** для Azure.
- **Google Secret Manager** для GCP.
- **HashiCorp Vault** для on-premise.

### 9. Документуйте змінні у README.md

Створіть секцію «Environment Variables» у README:

```markdown
## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_HOST` | Yes | - | PostgreSQL host |
| `DATABASE_PORT` | No | `5432` | PostgreSQL port |
| `JWT_SECRET` | Yes | - | JWT signing key (min 32 chars) |
| `ENABLE_SWAGGER` | No | `false` | Enable Swagger docs |
```

### 10. Ротація секретів

Регулярно змінюйте production secrets (кожні 90 днів):

```bash
# Генерація нового JWT secret
openssl rand -hex 32 > new-jwt-secret.txt

# Оновлення через AWS Secrets Manager CLI
aws secretsmanager update-secret \
  --secret-id prod/jwt-secret \
  --secret-string file://new-jwt-secret.txt
```


---

## Практичний приклад: повна конфігурація застосунку

Розглянемо повний приклад налаштування конфігурації для реального застосунку.

### Структура проєкту

```
src/
├── config/
│   ├── database.config.ts
│   ├── jwt.config.ts
│   ├── mail.config.ts
│   ├── redis.config.ts
│   ├── configuration.interface.ts
│   └── validation.schema.ts
├── auth/
│   ├── auth.module.ts
│   └── auth.service.ts
├── app.module.ts
└── main.ts

.env.development
.env.production
.env.example
```

### 1. Validation Schema

```typescript
// config/validation.schema.ts
import * as Joi from 'joi';

export const validationSchema = Joi.object({
  NODE_ENV: Joi.string()
    .valid('development', 'staging', 'production')
    .default('development'),
  PORT: Joi.number().port().default(3000),

  // Database
  DATABASE_HOST: Joi.string().required(),
  DATABASE_PORT: Joi.number().port().default(5432),
  DATABASE_USER: Joi.string().required(),
  DATABASE_PASSWORD: Joi.string().required(),
  DATABASE_NAME: Joi.string().required(),

  // JWT
  JWT_SECRET: Joi.string().min(32).required(),
  JWT_EXPIRATION: Joi.string().default('1h'),
  JWT_REFRESH_SECRET: Joi.string().min(32).required(),
  JWT_REFRESH_EXPIRATION: Joi.string().default('7d'),

  // Redis
  REDIS_HOST: Joi.string().default('localhost'),
  REDIS_PORT: Joi.number().port().default(6379),
  REDIS_PASSWORD: Joi.string().optional(),

  // Mail
  SMTP_HOST: Joi.string().required(),
  SMTP_PORT: Joi.number().port().required(),
  SMTP_USER: Joi.string().email().required(),
  SMTP_PASSWORD: Joi.string().required(),
  MAIL_FROM: Joi.string().email().default('noreply@example.com'),

  // Features
  ENABLE_SWAGGER: Joi.boolean().default(false),
  LOG_LEVEL: Joi.string()
    .valid('error', 'warn', 'info', 'debug')
    .default('info'),
});
```

### 2. Configuration Files

```typescript
// config/database.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('database', () => ({
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT, 10) || 5432,
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  name: process.env.DATABASE_NAME,
  synchronize: process.env.NODE_ENV === 'development',
  logging: process.env.NODE_ENV === 'development',
}));
```

```typescript
// config/jwt.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('jwt', () => ({
  secret: process.env.JWT_SECRET,
  expiresIn: process.env.JWT_EXPIRATION || '1h',
  refreshSecret: process.env.JWT_REFRESH_SECRET,
  refreshExpiresIn: process.env.JWT_REFRESH_EXPIRATION || '7d',
}));
```

```typescript
// config/redis.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('redis', () => ({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT, 10) || 6379,
  password: process.env.REDIS_PASSWORD,
}));
```

```typescript
// config/mail.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('mail', () => ({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT, 10),
  user: process.env.SMTP_USER,
  password: process.env.SMTP_PASSWORD,
  from: process.env.MAIL_FROM || 'noreply@example.com',
  secure: parseInt(process.env.SMTP_PORT, 10) === 465,
}));
```

### 3. TypeScript Interfaces

```typescript
// config/configuration.interface.ts

export interface DatabaseConfig {
  host: string;
  port: number;
  username: string;
  password: string;
  name: string;
  synchronize: boolean;
  logging: boolean;
}

export interface JwtConfig {
  secret: string;
  expiresIn: string;
  refreshSecret: string;
  refreshExpiresIn: string;
}

export interface RedisConfig {
  host: string;
  port: number;
  password?: string;
}

export interface MailConfig {
  host: string;
  port: number;
  user: string;
  password: string;
  from: string;
  secure: boolean;
}

export interface AppConfig {
  database: DatabaseConfig;
  jwt: JwtConfig;
  redis: RedisConfig;
  mail: MailConfig;
}
```

### 4. App Module

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { JwtModule } from '@nestjs/jwt';
import databaseConfig from './config/database.config';
import jwtConfig from './config/jwt.config';
import redisConfig from './config/redis.config';
import mailConfig from './config/mail.config';
import { validationSchema } from './config/validation.schema';

@Module({
  imports: [
    // Config Module
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: [
        `.env.${process.env.NODE_ENV || 'development'}`,
        '.env',
      ],
      load: [databaseConfig, jwtConfig, redisConfig, mailConfig],
      validationSchema,
      validationOptions: {
        allowUnknown: true,
        abortEarly: false,
      },
    }),

    // Database Module
    TypeOrmModule.forRootAsync({
      useFactory: (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get('database.host'),
        port: configService.get('database.port'),
        username: configService.get('database.username'),
        password: configService.get('database.password'),
        database: configService.get('database.name'),
        synchronize: configService.get('database.synchronize'),
        logging: configService.get('database.logging'),
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
      }),
      inject: [ConfigService],
    }),

    // JWT Module
    JwtModule.registerAsync({
      global: true,
      useFactory: (configService: ConfigService) => ({
        secret: configService.getOrThrow('jwt.secret'),
        signOptions: {
          expiresIn: configService.get('jwt.expiresIn'),
        },
      }),
      inject: [ConfigService],
    }),

    // Інші модулі
  ],
})
export class AppModule {}
```

### 5. Використання у сервісах

```typescript
// auth/auth.service.ts
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import { JwtConfig } from '../config/configuration.interface';

@Injectable()
export class AuthService {
  private readonly jwtConfig: JwtConfig;

  constructor(
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
  ) {
    this.jwtConfig = this.configService.get<JwtConfig>('jwt');
  }

  async generateAccessToken(userId: string): Promise<string> {
    return this.jwtService.sign(
      { sub: userId, type: 'access' },
      {
        secret: this.jwtConfig.secret,
        expiresIn: this.jwtConfig.expiresIn,
      },
    );
  }

  async generateRefreshToken(userId: string): Promise<string> {
    return this.jwtService.sign(
      { sub: userId, type: 'refresh' },
      {
        secret: this.jwtConfig.refreshSecret,
        expiresIn: this.jwtConfig.refreshExpiresIn,
      },
    );
  }

  async verifyRefreshToken(token: string): Promise<any> {
    return this.jwtService.verify(token, {
      secret: this.jwtConfig.refreshSecret,
    });
  }
}
```

### 6. .env файли

```bash
# .env.development
NODE_ENV=development

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=devpassword
DATABASE_NAME=blog_dev

JWT_SECRET=dev-jwt-secret-32-chars-minimum-length-required-here
JWT_EXPIRATION=7d
JWT_REFRESH_SECRET=dev-refresh-secret-32-chars-minimum-length
JWT_REFRESH_EXPIRATION=30d

REDIS_HOST=localhost
REDIS_PORT=6379

SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=test@example.com
SMTP_PASSWORD=testpassword
MAIL_FROM=dev@example.com

ENABLE_SWAGGER=true
LOG_LEVEL=debug
```

```bash
# .env.production
NODE_ENV=production

DATABASE_HOST=prod-db.example.com
DATABASE_PORT=5432
DATABASE_USER=prod_user
DATABASE_PASSWORD=ultra-secure-production-password
DATABASE_NAME=blog_prod

JWT_SECRET=production-jwt-secret-generated-by-openssl-rand-hex-32
JWT_EXPIRATION=1h
JWT_REFRESH_SECRET=production-refresh-secret-generated-by-openssl
JWT_REFRESH_EXPIRATION=7d

REDIS_HOST=prod-redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=redis-secure-password

SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxxxxxxxxxxxx
MAIL_FROM=noreply@example.com

ENABLE_SWAGGER=false
LOG_LEVEL=error
```

```bash
# .env.example (закомітити у Git)
NODE_ENV=development

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=

JWT_SECRET=
JWT_EXPIRATION=1h
JWT_REFRESH_SECRET=
JWT_REFRESH_EXPIRATION=7d

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
MAIL_FROM=

ENABLE_SWAGGER=false
LOG_LEVEL=info
```

::tip
**Перший запуск для нового розробника:**

```bash
# 1. Клонування репозиторію
git clone https://github.com/your-org/blog-api.git
cd blog-api

# 2. Встановлення залежностей
npm install

# 3. Створення .env з прикладу
cp .env.example .env

# 4. Редагування .env (заповнення DATABASE_PASSWORD, JWT_SECRET тощо)
nano .env

# 5. Генерація JWT secrets
openssl rand -hex 32  # Вставити у JWT_SECRET
openssl rand -hex 32  # Вставити у JWT_REFRESH_SECRET

# 6. Запуск застосунку
npm run start:dev
```
::


---

## Висновки

::card-group

::card{title="✅ Переваги @nestjs/config" icon="i-lucide-check-circle"}

- **Безпека:** паролі та secrets виносяться з коду у environment variables, які не комітяться у Git.
- **Гнучкість:** можливість змінювати налаштування без ребілду та редеплою застосунку.
- **Середовища:** легко підтримувати різні конфігурації для development, staging, production через окремі `.env` файли.
- **Валідація:** Joi schema перевіряє наявність та коректність змінних при старті, запобігаючи runtime помилкам.
- **Type Safety:** TypeScript interfaces забезпечують автодоповнення та compile-time перевірку типів.
- **Масштабованість:** namespaced конфігурація дозволяє логічно структурувати налаштування для великих застосунків.

::

::card{title="⚠️ Поширені помилки" icon="i-lucide-alert-triangle"}

- **Комітити .env у Git** — найпоширеніша помилка, що призводить до витоку credentials.
- **Відсутність валідації** — застосунок стартує з некоректною конфігурацією та падає при першому запиті.
- **Хардкоджені fallback значення** — використання `get('KEY', 'fallback-value')` для secrets замість `getOrThrow()`.
- **Слабкі JWT secrets** — використання коротких або передбачуваних ключів (наприклад, `secret123`).
- **Відсутність .env.example** — нові розробники не знають, які змінні потрібно налаштувати.
- **Використання .env у production** — замість secrets management систем (AWS Secrets Manager, Azure Key Vault).

::

::

**Що ми розглянули:**

1. **Проблема хардкоджених налаштувань** — чому небезпечно зберігати паролі та secrets у коді.
2. **@nestjs/config модуль** — офіційне рішення для configuration management з інтеграцією у DI систему.
3. **.env файли** — формат зберігання environment variables, `.gitignore` правила, `.env.example` для документації.
4. **ConfigService** — методи `get()`, `getOrThrow()`, type-safe доступ через generics, injection у сервіси та модулі.
5. **Joi валідація** — декларативна schema для перевірки обов'язкових змінних, типів, форматів при старті застосунку.
6. **Custom configuration files** — структурування конфігурації через окремі TypeScript файли, `registerAs()` для namespaced доступу.
7. **Різні конфігурації для середовищ** — `.env.development`, `.env.production`, conditional loading на основі `NODE_ENV`.
8. **TypeScript типізація** — interfaces для type-safe доступу, autocomplete, compile-time перевірка.
9. **Production конфігурація** — використання secrets management систем замість `.env` файлів, Docker/Kubernetes integration.
10. **Best Practices** — генерація безпечних secrets, документування змінних, ротація credentials, валідація у production.

**Ключові висновки:**

- **Ніколи не комітьте .env у Git** — додайте до `.gitignore` та використовуйте `.env.example` для документації.
- **Обов'язкова валідація через Joi** — запобігає запуску застосунку з некоректною конфігурацією.
- **Використовуйте `getOrThrow()` для критичних змінних** — застосунок не стартує без обов'язкових налаштувань.
- **Генеруйте криптографічно стійкі секрети** — `openssl rand -hex 32` для JWT secrets.
- **Різні `.env` файли для середовищ** — `.env.development` для локальної розробки, `.env.production` для production (не комітити!).
- **Використовуйте secrets management у production** — AWS Secrets Manager, Azure Key Vault, HashiCorp Vault замість `.env` файлів.

Правильне управління конфігурацією — це **фундамент безпеки** backend застосунку. Витік credentials може призвести до компрометації бази даних, викрадення user даних, несанкціонованого доступу до API. Слідуйте best practices та використовуйте сучасні інструменти для захисту sensitive даних.

---

## Часті запитання (FAQ)

::accordion

::accordion-item{title="Як використовувати dotenv-expand для змінних з посиланнями?"}

**dotenv-expand** дозволяє використовувати змінні усередині інших змінних:

```bash
# .env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_URL=postgres://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_NAME}
```

Встановлення:

```bash
npm install --save dotenv-expand
```

Інтеграція з `@nestjs/config`:

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      expandVariables: true, // Увімкнення dotenv-expand
    }),
  ],
})
export class AppModule {}
```

Тепер `DATABASE_URL` автоматично розширюється до `postgres://postgres:password@localhost:5432/blog_db`.

::

::accordion-item{title="Як зберігати secrets у production без .env файлів?"}

У production **не використовуйте `.env` файли**. Натомість використовуйте secrets management системи:

**AWS Secrets Manager:**

```bash
# Створення секрету
aws secretsmanager create-secret \
  --name prod/database-password \
  --secret-string "ultra-secure-password"

# Отримання секрету у застосунку
aws secretsmanager get-secret-value \
  --secret-id prod/database-password \
  --query SecretString --output text
```

У коді:

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

async function getDatabasePassword(): Promise<string> {
  const client = new SecretsManagerClient({ region: 'us-east-1' });
  const command = new GetSecretValueCommand({
    SecretId: 'prod/database-password',
  });
  const response = await client.send(command);
  return response.SecretString;
}
```

**Azure Key Vault:**

```bash
# Створення секрету
az keyvault secret set \
  --vault-name my-key-vault \
  --name database-password \
  --value "ultra-secure-password"
```

**Docker Secrets (Docker Swarm):**

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: my-app:latest
    secrets:
      - database_password
      - jwt_secret

secrets:
  database_password:
    external: true
  jwt_secret:
    external: true
```

Секрети доступні як файли у `/run/secrets/database_password`.

::

::accordion-item{title="Як налаштувати environment variables у Docker Compose?"}

Використовуйте `environment` або `env_file`:

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_USER: ${DATABASE_USER}
      DATABASE_PASSWORD: ${DATABASE_PASSWORD}
      DATABASE_NAME: blog_prod
    env_file:
      - .env.production  # Завантаження змінних з файлу
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_DB: blog_prod
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Створіть `.env.production` (не комітити!):**

```bash
DATABASE_USER=prod_user
DATABASE_PASSWORD=secure-password
JWT_SECRET=generated-jwt-secret
```

Запуск:

```bash
docker-compose --env-file .env.production up -d
```

::

::accordion-item{title="Чи потрібно валідувати env variables у development?"}

**Так, обов'язково!** Валідація запобігає помилкам конфігурації на ранніх етапах:

```typescript
ConfigModule.forRoot({
  validationSchema, // Валідація у всіх середовищах
  validationOptions: {
    abortEarly: false, // Показати всі помилки відразу
  },
})
```

**Переваги валідації у development:**

1. **Раннє виявлення помилок** — застосунок не стартує з некоректною конфігурацією.
2. **Документація** — Joi schema описує всі необхідні змінні та їх формати.
3. **Онбордінг нових розробників** — зрозумілі помилки валідації допомагають налаштувати `.env`.

**Приклад помилки валідації:**

::terminal-preview{title="Validation Error" :cursor="false"}

<div class="line"><span class="text-rose-400">Error:</span> Config validation error</div>
<div class="line"></div>
<div class="line">ValidationError:</div>
<div class="line">  - "DATABASE_PASSWORD" is required</div>
<div class="line">  - "JWT_SECRET" length must be at least 32 characters long</div>
<div class="line">  - "SMTP_PORT" must be a number</div>
<div class="line"></div>
<div class="line">💡 Check your .env file and ensure all required variables are set</div>

::

::

::accordion-item{title="Як тестувати код, що використовує ConfigService?"}

У тестах мокайте `ConfigService` через `createMock` або власний mock:

```typescript
// auth.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { ConfigService } from '@nestjs/config';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;
  let configService: ConfigService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        {
          provide: ConfigService,
          useValue: {
            get: jest.fn((key: string) => {
              const config = {
                'jwt.secret': 'test-secret-32-characters-long-key',
                'jwt.expiresIn': '1h',
              };
              return config[key];
            }),
            getOrThrow: jest.fn((key: string) => {
              const value = {
                'jwt.secret': 'test-secret-32-characters-long-key',
              }[key];
              if (!value) throw new Error(`Missing config: ${key}`);
              return value;
            }),
          },
        },
      ],
    }).compile();

    service = module.get<AuthService>(AuthService);
    configService = module.get<ConfigService>(ConfigService);
  });

  it('should generate JWT with correct secret', async () => {
    const token = await service.generateAccessToken('user-id');
    expect(token).toBeDefined();
    expect(configService.get).toHaveBeenCalledWith('jwt.secret');
  });
});
```

**Альтернативний підхід — використання реального ConfigModule з тестовими змінними:**

```typescript
beforeEach(async () => {
  const module: TestingModule = await Test.createTestingModule({
    imports: [
      ConfigModule.forRoot({
        isGlobal: true,
        ignoreEnvFile: true, // Ігнорувати .env файл
        load: [
          () => ({
            jwt: {
              secret: 'test-secret-32-characters-long-key',
              expiresIn: '1h',
            },
          }),
        ],
      }),
    ],
    providers: [AuthService],
  }).compile();

  service = module.get<AuthService>(AuthService);
});
```

::

::accordion-item{title="Як організувати конфігурацію для мікросервісів?"}

Для мікросервісної архітектури використовуйте **централізований config server** (Spring Cloud Config, Consul) або **shared environment variables**.

**Підхід 1: Окремі .env файли для кожного сервісу**

```
services/
├── auth-service/
│   ├── .env.development
│   └── .env.production
├── user-service/
│   ├── .env.development
│   └── .env.production
└── payment-service/
    ├── .env.development
    └── .env.production
```

**Підхід 2: Shared config через Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'
services:
  auth-service:
    build: ./services/auth-service
    environment:
      NODE_ENV: production
      DATABASE_HOST: postgres
      JWT_SECRET: ${SHARED_JWT_SECRET}
      REDIS_HOST: redis

  user-service:
    build: ./services/user-service
    environment:
      NODE_ENV: production
      DATABASE_HOST: postgres
      JWT_SECRET: ${SHARED_JWT_SECRET}
      REDIS_HOST: redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}

  redis:
    image: redis:7
```

**Підхід 3: Consul для dynamic configuration**

```typescript
// Інтеграція з Consul
import * as Consul from 'consul';

const consul = new Consul({ host: 'consul-server' });

async function loadConfigFromConsul() {
  const { Value } = await consul.kv.get('config/auth-service');
  return JSON.parse(Buffer.from(Value, 'base64').toString());
}
```

::

::

**Додаткові ресурси:**

- [NestJS Configuration Documentation](https://docs.nestjs.com/techniques/configuration)
- [Joi Validation Documentation](https://joi.dev/api/)
- [12-Factor App: Config](https://12factor.net/config)
- [AWS Secrets Manager Best Practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
