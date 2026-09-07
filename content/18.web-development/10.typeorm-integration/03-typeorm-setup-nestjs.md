# Налаштування TypeORM у NestJS проєкті

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Налаштувати повноцінну інтеграцію TypeORM у NestJS застосунок від встановлення пакетів до перевірки з'єднання.
- Освоїти синхронну та асинхронну конфігурацію DataSource через модуль `@nestjs/typeorm`.
- Навчитися безпечно керувати credentials через змінні оточення та ConfigModule.
- Підняти локальне середовище розробки з PostgreSQL у Docker Compose.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **DataSource:** центральний об'єкт TypeORM, що керує з'єднанням із базою даних та координує роботу репозиторіїв.
- **ConfigModule:** модуль NestJS для завантаження та валідації змінних оточення з `.env` файлів.
- **forRootAsync():** метод динамічної конфігурації модулів у NestJS, що дозволяє використовувати Dependency Injection.
- **Health Check:** механізм перевірки доступності сервісів (БД, API) для моніторингу стану застосунку.

::

::

---

## Встановлення необхідних пакетів

### Базові залежності для TypeORM

Перед початком роботи потрібно встановити три обов'язкові пакети: сам TypeORM, NestJS-обгортку та драйвер бази даних. Для роботи з PostgreSQL виконайте наступні команди:

::tabs

::tabs-item{label="pnpm"}

```bash
pnpm add @nestjs/typeorm typeorm pg
pnpm add -D @types/pg
```

::

::tabs-item{label="npm"}

```bash
npm install @nestjs/typeorm typeorm pg
npm install --save-dev @types/pg
```

::

::tabs-item{label="yarn"}

```bash
yarn add @nestjs/typeorm typeorm pg
yarn add --dev @types/pg
```

::

::

**Розшифровка пакетів:**

::field-group

::field{name="@nestjs/typeorm" type="package"}
Офіційна інтеграція TypeORM для NestJS. Надає декоратори (`@InjectRepository`, `@InjectDataSource`) та модулі (`TypeOrmModule`) для роботи в архітектурі NestJS із підтримкою Dependency Injection.

::

::field{name="typeorm" type="package"}
Сам ORM. Містить усю логіку роботи з базою даних: з'єднання, міграції, query builder, репозиторії. Версія 0.3.x є актуальною на момент написання лекції.

::

::field{name="pg" type="package"}
Нативний драйвер PostgreSQL для Node.js (той самий `node-postgres`, що ми вивчали у першій лекції). TypeORM використовує його під капотом для комунікації з БД.

::

::field{name="@types/pg" type="package" required="false"}
TypeScript типізація для пакету `pg`. Необхідна для коректної роботи автодоповнення IDE та перевірки типів під час компіляції.

::

::

### Версії та сумісність

При встановленні пакетів важливо переконатися, що версії сумісні між собою. На момент написання курсу рекомендовані версії:

| Пакет              | Версія    | Примітка                                      |
| ------------------ | --------- | --------------------------------------------- |
| `@nestjs/typeorm`  | `^10.0.0` | Підтримує NestJS 10.x та TypeORM 0.3.x        |
| `typeorm`          | `^0.3.20` | Стабільна версія із ESM підтримкою            |
| `pg`               | `^8.11.0` | Актуальний драйвер із підтримкою async/await  |
| `@nestjs/common`   | `^10.0.0` | Базовий пакет NestJS (має бути встановлений)  |

::warning

TypeORM 0.2.x та 0.3.x мають **несумісний API**. Якщо ви оновлюєте існуючий проєкт із 0.2.x на 0.3.x, підготуйтеся до breaking changes:

- `createConnection()` замінено на `new DataSource()`.
- `getRepository()` тепер викликається через `dataSource.getRepository()`.
- Синтаксис міграцій змінився.

Детальний гайд міграції: [TypeORM 0.3.0 Migration Guide](https://github.com/typeorm/typeorm/releases/tag/0.3.0)

::

**Перевірка встановлених версій:**

```bash
pnpm list typeorm @nestjs/typeorm pg
```

::terminal-preview{title="pnpm list" :cursor="false"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">pnpm list typeorm @nestjs/typeorm pg</strong></div>
<div class="line"></div>
<div class="line">dependencies:</div>
<div class="line"><span class="text-blue-400">@nestjs/typeorm</span> <span class="text-green-400">10.0.2</span></div>
<div class="line"><span class="text-blue-400">typeorm</span> <span class="text-green-400">0.3.20</span></div>
<div class="line"><span class="text-blue-400">pg</span> <span class="text-green-400">8.11.5</span></div>

::

---

## Конфігурація TypeOrmModule

### Імпорт `TypeOrmModule.forRoot()` у `app.module.ts`

Після встановлення пакетів потрібно зареєструвати TypeORM у кореневому модулі застосунку. NestJS використовує патерн Module для організації коду, і TypeORM має свій модуль — `TypeOrmModule`.

**Базова конфігурація (синхронна):**

```typescript [src/app.module.ts]
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'postgres',
      password: 'secret',
      database: 'myapp_dev',
      entities: [],
      synchronize: true, // ⚠️ Тільки для розробки!
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

При старті застосунку (`npm run start:dev`) TypeORM автоматично встановить з'єднання з базою даних. Якщо конфігурація коректна, у консолі з'явиться повідомлення:

::terminal-preview{title="npm run start:dev" :cursor="true"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">npm run start:dev</strong></div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">[Nest]</span> 12345  - 2026-09-05 14:30:00     <span class="text-green-400 font-bold">LOG</span> [InstanceLoader] TypeOrmModule dependencies initialized <span class="opacity-40">+42ms</span></div>
<div class="line"><span class="text-blue-400 font-bold">[Nest]</span> 12345  - 2026-09-05 14:30:00     <span class="text-green-400 font-bold">LOG</span> [TypeOrmModule] Successfully connected to database <span class="opacity-40">postgresql://localhost:5432/myapp_dev</span></div>
<div class="line"><span class="text-blue-400 font-bold">[Nest]</span> 12345  - 2026-09-05 14:30:00     <span class="text-green-400 font-bold">LOG</span> [NestApplication] Nest application successfully started <span class="opacity-40">+5ms</span></div>

::

::note

Метод `forRoot()` приймає ті самі параметри, що й конструктор `DataSource` у чистому TypeORM. Під капотом NestJS створює глобальний екземпляр DataSource та робить його доступним через Dependency Injection у всьому застосунку.

::

### Синхронна конфігурація

Синхронна конфігурація — це найпростіший спосіб налаштування TypeORM, де всі параметри передаються безпосередньо в об'єкт:

```typescript [src/app.module.ts]
TypeOrmModule.forRoot({
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'postgres',
  password: 'secret', // ⚠️ Хардкод паролю — погана практика!
  database: 'myapp_dev',
  entities: [__dirname + '/**/*.entity{.ts,.js}'],
  synchronize: true,
  logging: true,
})
```

**Недоліки синхронної конфігурації:**

- Credentials (*username*, *password*) хардкодяться у коді та потрапляють до Git.
- Неможливо використати різні налаштування для dev/staging/production.
- Немає підтримки Dependency Injection (не можна інжектити ConfigService).

::caution

**Ніколи не комітьте паролі до Git!** Навіть якщо ви видалите їх пізніше, вони залишаться в історії комітів. Для безпеки завжди використовуйте змінні оточення.

::

### Асинхронна конфігурація через `forRootAsync()`

Рекомендований підхід для production-застосунків — асинхронна конфігурація через `forRootAsync()`. Це дозволяє використовувати ConfigService для читання змінних оточення:


```typescript [src/app.module.ts]
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule, ConfigService } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true, // ConfigService доступний у всіх модулях
      envFilePath: '.env',
    }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get<string>('DB_HOST'),
        port: configService.get<number>('DB_PORT'),
        username: configService.get<string>('DB_USERNAME'),
        password: configService.get<string>('DB_PASSWORD'),
        database: configService.get<string>('DB_DATABASE'),
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
        synchronize: configService.get<boolean>('DB_SYNCHRONIZE', false),
        logging: configService.get<boolean>('DB_LOGGING', false),
      }),
      inject: [ConfigService],
    }),
  ],
})
export class AppModule {}
```

**Переваги асинхронної конфігурації:**

- **Безпека:** Credentials зберігаються у `.env` файлі, який не комітиться до Git (додайте `.env` у `.gitignore`).
- **Гнучкість:** Різні налаштування для різних середовищ (`dev`, `staging`, `production`).
- **Dependency Injection:** Можливість використовувати інші сервіси (наприклад, секрет-менеджери AWS Secrets Manager).
- **Type safety:** ConfigService типізований, що дозволяє уникнути помилок у назвах змінних.

::tip

Параметр `isGlobal: true` у ConfigModule робить ConfigService доступним у всіх модулях без необхідності імпортувати ConfigModule у кожному модулі окремо. Це зручно для великих проєктів.

::

### Dependency injection для конфігурації

Якщо вам потрібна складніша логіка конфігурації (наприклад, вибір різних параметрів залежно від оточення), ви можете створити окремий сервіс:

```typescript [src/config/database.config.ts]
import { Injectable } from '@nestjs/common';
import { TypeOrmModuleOptions, TypeOrmOptionsFactory } from '@nestjs/typeorm';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class DatabaseConfig implements TypeOrmOptionsFactory {
  constructor(private configService: ConfigService) {}

  createTypeOrmOptions(): TypeOrmModuleOptions {
    const isProduction = this.configService.get('NODE_ENV') === 'production';

    return {
      type: 'postgres',
      host: this.configService.get('DB_HOST'),
      port: this.configService.get('DB_PORT'),
      username: this.configService.get('DB_USERNAME'),
      password: this.configService.get('DB_PASSWORD'),
      database: this.configService.get('DB_DATABASE'),
      entities: [__dirname + '/../**/*.entity{.ts,.js}'],
      
      // Різні налаштування для dev і production
      synchronize: !isProduction, // FALSE у production!
      logging: !isProduction ? ['query', 'error'] : ['error'],
      
      // SSL обов'язковий у production
      ssl: isProduction ? { rejectUnauthorized: false } : false,
      
      // Connection pool налаштування
      extra: {
        max: isProduction ? 20 : 10,
        connectionTimeoutMillis: 2000,
      },
    };
  }
}
```

```typescript [src/app.module.ts]
import { DatabaseConfig } from './config/database.config';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRootAsync({
      useClass: DatabaseConfig, // Використовуємо кастомний клас
    }),
  ],
})
export class AppModule {}
```

Цей підхід дозволяє інкапсулювати всю логіку конфігурації БД в окремому класі, що спрощує тестування та підтримку коду.

---

## Параметри підключення

### `type`: тип БД

TypeORM підтримує багато типів баз даних. Найпоширеніші:

| Значення     | База даних         | Драйвер              |
| ------------ | ------------------ | -------------------- |
| `postgres`   | PostgreSQL         | `pg`                 |
| `mysql`      | MySQL / MariaDB    | `mysql2`             |
| `sqlite`     | SQLite             | `sqlite3`            |
| `mssql`      | Microsoft SQL      | `mssql`              |
| `oracle`     | Oracle Database    | `oracledb`           |
| `cockroachdb`| CockroachDB        | `pg` (сумісний з PG) |

Для нашого курсу ми використовуємо `postgres`, оскільки PostgreSQL є найпопулярнішою open-source реляційною БД для веб-застосунків.

### `host`, `port`: адреса сервера БД

**host:** IP-адреса або доменне ім'я сервера PostgreSQL.

- Локальна розробка: `localhost` або `127.0.0.1`
- Docker Compose: назва сервісу (наприклад, `postgres`)
- Production: IP або домен хмарного провайдера (AWS RDS, Google Cloud SQL)

**port:** TCP-порт, на якому слухає PostgreSQL. За замовчуванням `5432`.

```typescript
{
  host: 'localhost',       // Локально
  // або
  host: 'postgres',        // У Docker Compose (назва контейнера)
  // або
  host: 'db.example.com',  // Production сервер
  
  port: 5432,              // Стандартний порт PostgreSQL
}
```

::note

Якщо ваш NestJS застосунок працює у Docker-контейнері, використовуйте назву сервісу PostgreSQL з `docker-compose.yml` як `host`. Docker автоматично резолвить DNS-імена сервісів у внутрішню IP-адресу контейнера.

::

### `username`, `password`: credentials

Ім'я користувача та пароль для автентифікації у PostgreSQL.

**Best practices:**

1. **Ніколи не використовуйте суперкористувача `postgres` у production.** Створіть окремого користувача з обмеженими правами:

```sql
CREATE USER myapp_user WITH PASSWORD 'secure_password_here';
CREATE DATABASE myapp_production OWNER myapp_user;
GRANT ALL PRIVILEGES ON DATABASE myapp_production TO myapp_user;
```

2. **Використовуйте сильні паролі:** Мінімум 16 символів із літерами, цифрами та спецсимволами.

3. **Зберігайте паролі у змінних оточення:**

```env
DB_USERNAME=myapp_user
DB_PASSWORD=xK9$mP2@vL8#nQ5!
```

### `database`: назва бази даних

Назва конкретної бази даних, до якої підключається застосунок. Одна PostgreSQL-інстанція може містити кілька ізольованих баз даних.

**Конвенції іменування:**

```typescript
{
  // Розробка
  database: 'myapp_dev',
  
  // Тестування
  database: 'myapp_test',
  
  // Staging
  database: 'myapp_staging',
  
  // Production
  database: 'myapp_production',
}
```

::tip

Для локальної розробки зручно додавати суфікс `_dev` до назви бази, щоб випадково не підключитися до production БД при помилці у конфігурації.

::

### SSL налаштування для production

У production-середовищі всі з'єднання з БД **обов'язково** мають бути зашифрованими через SSL/TLS. Більшість хмарних провайдерів (AWS RDS, Azure SQL, Google Cloud SQL) вимагають або настійно рекомендують SSL.

**Базове SSL налаштування:**

```typescript
{
  ssl: process.env.NODE_ENV === 'production' 
    ? { rejectUnauthorized: false } 
    : false,
}
```

**Повна конфігурація із сертифікатами:**

```typescript
import * as fs from 'fs';

{
  ssl: {
    rejectUnauthorized: true, // Перевіряти валідність сертифіката
    ca: fs.readFileSync('./certs/ca-certificate.crt').toString(),
    key: fs.readFileSync('./certs/client-key.pem').toString(),
    cert: fs.readFileSync('./certs/client-cert.pem').toString(),
  },
}
```

**Для AWS RDS:**

AWS надає кореневий CA-сертифікат, який потрібно завантажити:

```bash
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

```typescript
{
  ssl: {
    ca: fs.readFileSync('./global-bundle.pem').toString(),
    rejectUnauthorized: true,
  },
}
```

::caution

Налаштування `rejectUnauthorized: false` відключає перевірку сертифіката, що робить з'єднання вразливим до MITM-атак (*man-in-the-middle*). Використовуйте це **лише для локальної розробки** або для баз даних із самопідписаними сертифікатами у контрольованому середовищі.

::

---

## Параметри поведінки TypeORM

### `synchronize`: автоматична синхронізація схеми

Коли `synchronize: true`, TypeORM автоматично створює, змінює або видаляє таблиці при старті застосунку, щоб структура БД відповідала вашим Entity класам.

```typescript
{
  synchronize: true, // TypeORM автоматично синхронізує схему
}
```

**Що відбувається при `synchronize: true`:**

1. TypeORM сканує всі Entity класи.
2. Порівнює структуру класів із реальною схемою БД.
3. Генерує та виконує DDL-команди (`CREATE TABLE`, `ALTER TABLE`, `DROP COLUMN`).

::caution

**КРИТИЧНО ВАЖЛИВО:** `synchronize: true` може призвести до **втрати даних** у production!

Приклад небезпеки:
- Ви видалили поле `age` з Entity класу `User`.
- TypeORM виконає `ALTER TABLE users DROP COLUMN age`.
- Всі дані у колонці `age` будуть безповоротно втрачені.

**Правило:** `synchronize: true` **тільки для локальної розробки**. У production завжди використовуйте міграції.

::

**Безпечна конфігурація:**

```typescript
{
  synchronize: process.env.NODE_ENV !== 'production', // TRUE тільки у dev
}
```

### `logging`: логування SQL запитів

Параметр `logging` дозволяє бачити, які SQL-запити генерує TypeORM. Це критично важливо для налагодження та оптимізації продуктивності.

**Рівні логування:**

```typescript
{
  // Логувати все
  logging: true,
  
  // Логувати тільки запити
  logging: ['query'],
  
  // Логувати тільки помилки
  logging: ['error'],
  
  // Комбінація
  logging: ['query', 'error', 'schema', 'warn', 'info'],
  
  // Відключити логування
  logging: false,
}
```

**Приклад виводу у консоль:**

::terminal-preview{title="TypeORM Query Log" :cursor="false"}

<div class="line"><span class="text-blue-400 font-bold">query:</span> SELECT "User"."id" AS "User_id", "User"."email" AS "User_email" FROM "users" "User" WHERE "User"."id" = $1</div>
<div class="line"><span class="opacity-40">parameters:</span> [1]</div>
<div class="line"></div>
<div class="line"><span class="text-green-400 font-bold">query:</span> INSERT INTO "users"("email", "name") VALUES ($1, $2) RETURNING "id"</div>
<div class="line"><span class="opacity-40">parameters:</span> ["test@example.com", "Test User"]</div>

::

**Рекомендована конфігурація:**

```typescript
{
  logging: process.env.NODE_ENV === 'development' 
    ? ['query', 'error'] 
    : ['error'], // У production логуємо тільки помилки
}
```


### `autoLoadEntities`: автоматичне завантаження entities

При використанні NestJS зручно використовувати `autoLoadEntities: true`, щоб TypeORM автоматично знаходив усі зареєстровані Entity без необхідності вказувати шляхи вручну.

```typescript
{
  autoLoadEntities: true, // TypeORM автоматично завантажує Entity
  // Замість:
  // entities: [__dirname + '/**/*.entity{.ts,.js}'],
}
```

**Як це працює:**

1. Ви реєструєте Entity у модулях через `TypeOrmModule.forFeature([User, Post])`.
2. TypeORM автоматично додає їх до глобального списку entities.
3. Не потрібно вказувати шляхи через glob-паттерни.

**Приклад використання:**

```typescript [src/users/users.module.ts]
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';
import { UsersService } from './users.service';

@Module({
  imports: [
    TypeOrmModule.forFeature([User]), // Реєстрація Entity
  ],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

::tip

`autoLoadEntities: true` працює **лише з NestJS**. Якщо ви використовуєте чистий TypeORM без фреймворку, потрібно явно вказувати масив entities або шлях через glob-паттерн.

::

### `migrations`: шлях до міграцій

Міграції — це версійовані SQL-скрипти для зміни структури БД. Вони дозволяють контролювати еволюцію схеми та відкочувати зміни у разі проблем.

```typescript
{
  migrations: [__dirname + '/migrations/**/*{.ts,.js}'],
  migrationsRun: false, // Не виконувати міграції автоматично при старті
}
```

**Структура проєкту з міграціями:**

```
src/
├── migrations/
│   ├── 1699000000000-CreateUsersTable.ts
│   ├── 1699000001000-AddAgeToUsers.ts
│   └── 1699000002000-CreatePostsTable.ts
├── entities/
│   ├── user.entity.ts
│   └── post.entity.ts
└── app.module.ts
```

**Створення міграції:**

```bash
npx typeorm migration:generate src/migrations/AddAgeToUsers -d src/data-source.ts
```

TypeORM порівняє поточний стан БД із Entity класами та згенерує SQL для синхронізації:

```typescript [src/migrations/1699000001000-AddAgeToUsers.ts]
import { MigrationInterface, QueryRunner } from 'typeorm';

export class AddAgeToUsers1699000001000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE "users" ADD "age" integer
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE "users" DROP COLUMN "age"
    `);
  }
}
```

**Виконання міграцій:**

```bash
npx typeorm migration:run -d src/data-source.ts
```

::note

У наступних лекціях ми детально розглянемо створення та застосування міграцій. На даному етапі достатньо знати, що міграції — це production-спосіб керування схемою БД замість `synchronize: true`.

::

### `entities`: шлях до entity файлів

Якщо ви не використовуєте `autoLoadEntities`, потрібно вказати, де TypeORM має шукати Entity класи:

```typescript
{
  // Glob-паттерн для пошуку всіх *.entity.ts файлів
  entities: [__dirname + '/**/*.entity{.ts,.js}'],
  
  // Або явний список
  entities: [User, Post, Comment, Category],
}
```

**Glob-паттерни:**

| Паттерн                                | Опис                                        |
| -------------------------------------- | ------------------------------------------- |
| `**/*.entity{.ts,.js}`                 | Всі файли з суфіксом `.entity.ts` або `.js` |
| `src/entities/**/*{.ts,.js}`           | Всі файли у директорії `src/entities`       |
| `src/**/entities/*{.ts,.js}`           | Entity у будь-яких піддиректоріях           |

::warning

**Проблема glob-паттернів у production:**

Коли ви збираєте NestJS застосунок (`npm run build`), TypeScript компілюється у JavaScript у папку `dist/`. Якщо glob-паттерн містить тільки `.ts`, TypeORM не знайде файли у збірці.

**Рішення:** Завжди включайте обидва розширення `{.ts,.js}` або використовуйте `autoLoadEntities: true`.

::

---

## Використання ConfigModule для credentials

### Створення `.env` файлу

Файл `.env` зберігає змінні оточення, які не повинні потрапляти до Git. Створіть цей файл у корені проєкту:

```env [.env]
# Середовище виконання
NODE_ENV=development

# База даних
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=secret_password_here
DB_DATABASE=myapp_dev
DB_SYNCHRONIZE=true
DB_LOGGING=true

# Додаткові налаштування
PORT=3000
```

**Додайте `.env` до `.gitignore`:**

```gitignore [.gitignore]
# Environment variables
.env
.env.local
.env.production

# Dependencies
node_modules/

# Build output
dist/
```

::caution

Файл `.env` містить чутливу інформацію (паролі, API ключі). **Ніколи** не комітьте його до Git! Замість цього створіть файл `.env.example` з прикладами значень (без реальних паролів) для інших розробників:

```env [.env.example]
NODE_ENV=development
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_DATABASE=myapp_dev
```

::

### Налаштування `@nestjs/config`

Встановіть пакет для роботи зі змінними оточення:

::tabs

::tabs-item{label="pnpm"}

```bash
pnpm add @nestjs/config
```

::

::tabs-item{label="npm"}

```bash
npm install @nestjs/config
```

::

::tabs-item{label="yarn"}

```bash
yarn add @nestjs/config
```

::

::

Зареєструйте ConfigModule у `app.module.ts`:

```typescript [src/app.module.ts]
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,      // Доступний у всіх модулях
      envFilePath: '.env', // Шлях до .env файлу
      cache: true,         // Кешувати змінні для продуктивності
    }),
  ],
})
export class AppModule {}
```

### Читання змінних середовища

Тепер ви можете інжектити ConfigService у будь-якому сервісі:

```typescript [src/users/users.service.ts]
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class UsersService {
  constructor(private configService: ConfigService) {
    const dbHost = this.configService.get<string>('DB_HOST');
    const dbPort = this.configService.get<number>('DB_PORT');
    
    console.log(`Database: ${dbHost}:${dbPort}`);
  }
}
```

**Методи ConfigService:**

| Метод                                  | Опис                                        |
| -------------------------------------- | ------------------------------------------- |
| `get<T>(key: string)`                  | Отримати значення змінної                   |
| `get<T>(key: string, defaultValue: T)` | Із значенням за замовчуванням               |
| `getOrThrow<T>(key: string)`           | Викинути помилку, якщо змінної немає        |

```typescript
// Без default — може повернути undefined
const host = this.configService.get<string>('DB_HOST');

// З default — гарантовано повертає значення
const port = this.configService.get<number>('DB_PORT', 5432);

// Викине помилку, якщо DB_PASSWORD не визначено
const password = this.configService.getOrThrow<string>('DB_PASSWORD');
```

### Валідація конфігурації через Joi

Щоб уникнути помилок через відсутність критичних змінних, використовуйте Joi для валідації `.env` файлу при старті застосунку:

::tabs

::tabs-item{label="pnpm"}

```bash
pnpm add joi
```

::

::tabs-item{label="npm"}

```bash
npm install joi
```

::

::tabs-item{label="yarn"}

```bash
yarn add joi
```

::

::

Створіть схему валідації:

```typescript [src/config/env.validation.ts]
import * as Joi from 'joi';

export const envValidationSchema = Joi.object({
  NODE_ENV: Joi.string()
    .valid('development', 'production', 'test', 'staging')
    .default('development'),
  
  PORT: Joi.number().default(3000),
  
  DB_HOST: Joi.string().required(),
  DB_PORT: Joi.number().default(5432),
  DB_USERNAME: Joi.string().required(),
  DB_PASSWORD: Joi.string().required(),
  DB_DATABASE: Joi.string().required(),
  DB_SYNCHRONIZE: Joi.boolean().default(false),
  DB_LOGGING: Joi.boolean().default(false),
});
```

Використайте схему у ConfigModule:

```typescript [src/app.module.ts]
import { envValidationSchema } from './config/env.validation';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      validationSchema: envValidationSchema,
      validationOptions: {
        abortEarly: true, // Зупинитися на першій помилці
        allowUnknown: true, // Дозволити невідомі змінні
      },
    }),
  ],
})
export class AppModule {}
```

Якщо при старті застосунку бракує обов'язкової змінної, ви побачите помилку:

::terminal-preview{title="Validation Error" :cursor="false"}

<div class="line"><span class="text-rose-400 font-bold">Error:</span> Config validation error: "DB_PASSWORD" is required</div>
<div class="line"></div>
<div class="line"><span class="opacity-40">at Object.&lt;anonymous&gt; (src/app.module.ts:15:3)</span></div>
<div class="line"><span class="text-rose-400 font-bold">✗</span> Application failed to start</div>

::

### Різні конфігурації для dev/staging/production

Створіть окремі `.env` файли для кожного середовища:

```
.env              # Локальна розробка (не комітити)
.env.development  # Налаштування dev (можна комітити без паролів)
.env.staging      # Staging сервер
.env.production   # Production сервер (не комітити!)
```

Використовуйте змінну `NODE_ENV` для вибору файлу:

```typescript [src/app.module.ts]
ConfigModule.forRoot({
  isGlobal: true,
  envFilePath: `.env.${process.env.NODE_ENV || 'development'}`,
  validationSchema: envValidationSchema,
})
```

Запуск із різними конфігураціями:

```bash
# Development
NODE_ENV=development npm run start:dev

# Staging
NODE_ENV=staging npm run start:prod

# Production
NODE_ENV=production npm run start:prod
```


---

## Docker Compose для локальної розробки

### Конфігурація PostgreSQL контейнера

Docker Compose дозволяє запустити PostgreSQL локально без необхідності встановлення СУБД на вашу машину. Створіть файл `docker-compose.yml` у корені проєкту:

```yaml [docker-compose.yml]
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: myapp_postgres
    restart: unless-stopped
    ports:
      - '5432:5432'
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp_dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - myapp_network
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U postgres']
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local

networks:
  myapp_network:
    driver: bridge
```

**Розшифровка параметрів:**

::field-group

::field{name="image: postgres:15-alpine" type="string"}
Використовує офіційний образ PostgreSQL версії 15 на базі Alpine Linux (легковаговий дистрибутив). Alpine-образи займають ~80MB замість ~300MB звичайного Debian-образу.

::

::field{name="container_name" type="string"}
Явна назва контейнера замість автогенерованої. Зручно для логів та debugging: `docker logs myapp_postgres`.

::

::field{name="restart: unless-stopped" type="string"}
Політика перезапуску. Контейнер автоматично перезапускається при збої, але не після ручної зупинки через `docker stop`.

::

::field{name="ports" type="array"}
Проброс портів у форматі `host:container`. PostgreSQL всередині контейнера слухає на порту 5432, і ми пробрасимо його на той самий порт хост-машини.

::

::field{name="environment" type="object"}
Змінні оточення для ініціалізації БД. `POSTGRES_USER`, `POSTGRES_PASSWORD` та `POSTGRES_DB` використовуються при першому запуску для створення користувача та бази даних.

::

::field{name="volumes" type="array"}
Named volume `postgres_data` для персистентного збереження даних БД. Без цього всі дані втратяться при видаленні контейнера.

::

::field{name="healthcheck" type="object"}
Регулярна перевірка доступності БД через команду `pg_isready`. Docker позначає контейнер як `healthy`, коли PostgreSQL готовий приймати з'єднання.

::

::

### Volume для збереження даних

Named volume гарантує, що дані БД зберігаються навіть після видалення контейнера:

```bash
# Зупинити та видалити контейнер
docker compose down

# Дані залишаються у volume
docker volume ls
# DRIVER    VOLUME NAME
# local     myapp_postgres_data

# Запустити знову — дані на місці
docker compose up -d
```

Щоб видалити дані разом із контейнером:

```bash
docker compose down -v  # -v видаляє volumes
```

### Network налаштування між NestJS та PostgreSQL

Якщо ви також запускаєте NestJS у Docker, додайте його до того самого network:

```yaml [docker-compose.yml]
version: '3.8'

services:
  postgres:
    # ... (конфігурація вище)

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: myapp_nestjs
    restart: unless-stopped
    ports:
      - '3000:3000'
    environment:
      DB_HOST: postgres  # ⚠️ Назва сервісу, а не localhost!
      DB_PORT: 5432
      DB_USERNAME: postgres
      DB_PASSWORD: secret
      DB_DATABASE: myapp_dev
    depends_on:
      postgres:
        condition: service_healthy  # Чекати, поки PostgreSQL готовий
    networks:
      - myapp_network

volumes:
  postgres_data:

networks:
  myapp_network:
```

::note

Коли NestJS працює у Docker-контейнері, використовуйте **назву сервісу PostgreSQL** (`postgres`) як `DB_HOST`, а не `localhost`. Docker автоматично резолвить DNS-імена сервісів у внутрішні IP-адреси.

::

### Environment variables у docker-compose

Замість хардкоду паролів у `docker-compose.yml`, використовуйте файл `.env`:

```env [.env]
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_DB=myapp_dev
```

```yaml [docker-compose.yml]
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
```

Docker Compose автоматично підставить значення з `.env` файлу.

### Healthcheck для БД

Healthcheck гарантує, що PostgreSQL повністю готовий приймати з'єднання перед запуском інших сервісів:

```yaml
healthcheck:
  test: ['CMD-SHELL', 'pg_isready -U postgres']
  interval: 10s     # Перевіряти кожні 10 секунд
  timeout: 5s       # Таймаут команди
  retries: 5        # 5 невдалих спроб = unhealthy
  start_period: 30s # Час на початкову ініціалізацію
```

**Використання у `depends_on`:**

```yaml
app:
  depends_on:
    postgres:
      condition: service_healthy  # Чекати healthy статусу
```

::tip

Перевірити статус здоров'я контейнера:

```bash
docker ps
# CONTAINER ID   STATUS
# abc123def456   Up 2 minutes (healthy)
```

::

**Запуск Docker Compose:**

```bash
# Запустити у фоновому режимі
docker compose up -d

# Перевірити логи
docker compose logs -f postgres

# Зупинити всі сервіси
docker compose down
```

::terminal-preview{title="docker compose up -d" :cursor="false"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">docker compose up -d</strong></div>
<div class="line"><span class="text-blue-400 font-bold">[+]</span> Running 2/2</div>
<div class="line"> <span class="text-green-400 font-bold">✔</span> Network myapp_network       Created</div>
<div class="line"> <span class="text-green-400 font-bold">✔</span> Container myapp_postgres   Started</div>
<div class="line"></div>
<div class="line"><span class="text-green-400 font-bold">SUCCESS:</span> PostgreSQL running on <strong>localhost:5432</strong></div>

::

---

## Перевірка підключення

### Тестування з'єднання при старті застосунку

Хороша практика — перевірити з'єднання з БД одразу після ініціалізації застосунку. Це дозволяє виявити проблеми з конфігурацією до того, як застосунок почне обробляти запити.

```typescript [src/app.module.ts]
import { Module, OnModuleInit } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';

@Module({
  imports: [
    // ... TypeOrmModule.forRootAsync()
  ],
})
export class AppModule implements OnModuleInit {
  constructor(private dataSource: DataSource) {}

  async onModuleInit() {
    try {
      if (this.dataSource.isInitialized) {
        console.log('✅ Database connection established successfully');
        
        // Додаткова інформація про з'єднання
        const { host, port, database } = this.dataSource.options as any;
        console.log(`📦 Connected to: ${host}:${port}/${database}`);
        
        // Перевірка версії PostgreSQL
        const result = await this.dataSource.query('SELECT version()');
        console.log(`🐘 PostgreSQL version: ${result[0].version.split(' ')[1]}`);
      }
    } catch (error) {
      console.error('❌ Database connection failed:', error.message);
      process.exit(1); // Критична помилка — зупиняємо застосунок
    }
  }
}
```

### Логування успішного підключення

При успішному підключенні ви побачите у консолі:

::terminal-preview{title="npm run start:dev" :cursor="true"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">npm run start:dev</strong></div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">[Nest]</span> 12345  - 2026-09-05 15:00:00     <span class="text-green-400 font-bold">LOG</span> [InstanceLoader] ConfigModule dependencies initialized</div>
<div class="line"><span class="text-blue-400 font-bold">[Nest]</span> 12345  - 2026-09-05 15:00:00     <span class="text-green-400 font-bold">LOG</span> [InstanceLoader] TypeOrmModule dependencies initialized <span class="opacity-40">+85ms</span></div>
<div class="line"><span class="text-green-400 font-bold">✅</span> Database connection established successfully</div>
<div class="line"><span class="text-blue-400 font-bold">📦</span> Connected to: localhost:5432/myapp_dev</div>
<div class="line"><span class="text-blue-400 font-bold">🐘</span> PostgreSQL version: 15.4</div>
<div class="line"><span class="text-blue-400 font-bold">[Nest]</span> 12345  - 2026-09-05 15:00:01     <span class="text-green-400 font-bold">LOG</span> [NestApplication] Nest application successfully started</div>

::

### Обробка помилок підключення

Типові помилки та їх причини:

**1. Connection refused (ECONNREFUSED)**

```
Error: connect ECONNREFUSED 127.0.0.1:5432
```

**Причина:** PostgreSQL не запущено або слухає на іншому порту.

**Рішення:**
- Перевірте, чи працює PostgreSQL: `docker ps` або `systemctl status postgresql`
- Переконайтеся, що порт у `.env` відповідає реальному порту БД

**2. Authentication failed (password authentication failed)**

```
Error: password authentication failed for user "postgres"
```

**Причина:** Невірний пароль у змінній `DB_PASSWORD`.

**Рішення:**
- Перевірте пароль у `.env` файлі
- Переконайтеся, що пароль не містить спецсимволів, які потребують екранування

**3. Database does not exist**

```
Error: database "myapp_dev" does not exist
```

**Причина:** База даних ще не створена.

**Рішення:**

```bash
docker exec -it myapp_postgres psql -U postgres -c "CREATE DATABASE myapp_dev;"
```

**4. Too many connections**

```
Error: sorry, too many clients already
```

**Причина:** Вичерпано ліміт одночасних з'єднань PostgreSQL.

**Рішення:**
- Зменшіть розмір пулу у конфігурації TypeORM (`max: 10`)
- Збільште `max_connections` у `postgresql.conf` (для production)

### Graceful shutdown

При зупинці застосунку коректно закривайте з'єднання з БД:

```typescript [src/main.ts]
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Graceful shutdown при отриманні SIGTERM/SIGINT
  app.enableShutdownHooks();

  await app.listen(3000);
  console.log(`🚀 Application is running on: ${await app.getUrl()}`);
}

bootstrap();
```

```typescript [src/app.module.ts]
import { Module, OnApplicationShutdown } from '@nestjs/common';
import { DataSource } from 'typeorm';

@Module({
  // ...
})
export class AppModule implements OnApplicationShutdown {
  constructor(private dataSource: DataSource) {}

  async onApplicationShutdown(signal?: string) {
    console.log(`⚠️  Received shutdown signal: ${signal}`);
    
    if (this.dataSource.isInitialized) {
      await this.dataSource.destroy();
      console.log('✅ Database connection closed');
    }
  }
}
```

::note

Метод `enableShutdownHooks()` дозволяє NestJS коректно завершити роботу при отриманні сигналів `SIGTERM` (Kubernetes/Docker) або `SIGINT` (Ctrl+C). Це критично важливо для production-систем, щоб уникнути обриву активних транзакцій.

::

---

## Підсумок

::card-group

::card{title="✅ Що ви опанували" icon="i-lucide-check-circle"}

- Встановили та налаштували TypeORM у NestJS проєкті через `@nestjs/typeorm`.
- Навчилися конфігурувати DataSource синхронно та асинхронно через `forRootAsync()`.
- Опанували роботу зі змінними оточення через ConfigModule та валідацію через Joi.
- Налаштували локальне середовище розробки з PostgreSQL у Docker Compose.
- Реалізували перевірку з'єднання, обробку помилок та graceful shutdown.

::

::card{title="🚀 Наступні кроки" icon="i-lucide-arrow-right"}

У наступній лекції ви перейдете до створення Entity класів:
- Декоратори `@Entity()`, `@Column()`, `@PrimaryGeneratedColumn()`
- Різні типи колонок: базові та складні типи даних
- Автоматичні timestamp поля (`@CreateDateColumn`, `@UpdateDateColumn`)
- Soft delete та versioning для оптимістичного блокування

::

::

::accordion

::accordion-item{label="❓ Чи можна використовувати кілька баз даних у одному NestJS застосунку?" icon="i-lucide-help-circle"}

Так, TypeORM підтримує multiple connections. Використовуйте параметр `name` для ідентифікації різних з'єднань:

```typescript
TypeOrmModule.forRoot({
  name: 'primary',
  type: 'postgres',
  // ...
}),
TypeOrmModule.forRoot({
  name: 'analytics',
  type: 'mysql',
  // ...
})
```

При інжектуванні репозиторіїв вказуйте назву з'єднання:

```typescript
@InjectRepository(User, 'primary')
private userRepository: Repository<User>
```

::

::accordion-item{label="❓ Що робити, якщо TypeORM не знаходить Entity класи?" icon="i-lucide-help-circle"}

Перевірте наступне:

1. **autoLoadEntities увімкнено:** `autoLoadEntities: true` у конфігурації
2. **Entity зареєстрована у модулі:** `TypeOrmModule.forFeature([User])`
3. **Glob-паттерн коректний:** Перевірте, що `entities: [__dirname + '/**/*.entity{.ts,.js}']` відповідає структурі вашого проєкту
4. **Декоратор @Entity() присутній:** Переконайтеся, що клас анотований декоратором

Увімкніть `logging: ['schema']` для debug інформації про завантаження Entity.

::

::accordion-item{label="❓ Чи безпечно використовувати synchronize: true у staging-середовищі?" icon="i-lucide-help-circle"}

**Категорично ні!** Навіть у staging-середовищі можуть бути важливі тестові дані, які не варто втрачати. Завжди використовуйте міграції для будь-якого середовища, окрім локальної розробки. Єдиний виняток — тимчасові тестові бази даних у CI/CD pipeline, які створюються та видаляються для кожного тесту.

::

::

::note

**Корисні ресурси:**

- [NestJS TypeORM Integration](https://docs.nestjs.com/techniques/database)
- [TypeORM DataSource Options](https://typeorm.io/data-source-options)
- [Docker Compose PostgreSQL Setup](https://hub.docker.com/_/postgres)
- [@nestjs/config Documentation](https://docs.nestjs.com/techniques/configuration)

::

---

**Вітаємо! Ви успішно налаштували TypeORM у NestJS проєкті.** Тепер у вас є повноцінне середовище розробки з PostgreSQL у Docker, безпечним керуванням credentials та перевіркою з'єднання. У наступній лекції ми перейдемо до створення Entity класів та вивчимо декоратори TypeORM детально.