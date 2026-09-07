# Entity класи та декоратори TypeORM

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати створення Entity класів — основних будівельних блоків TypeORM для відображення таблиць БД.
- Вивчити декоратори TypeORM для визначення структури даних: від простих колонок до складних типів.
- Навчитися правильно типізувати поля Entity для забезпечення type safety у всьому застосунку.
- Освоїти автоматичні механізми TypeORM: timestamp поля, soft delete, версіонування.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Entity:** TypeScript клас, анотований декоратором `@Entity()`, що представляє таблицю у реляційній базі даних.
- **Decorator:** спеціальна анотація TypeScript, що додає метадані до класів, методів або властивостей для використання у runtime.
- **Primary Key:** унікальний ідентифікатор рядка у таблиці, який не може повторюватися та не може бути NULL.
- **Soft Delete:** механізм логічного видалення записів через встановлення timestamp замість фізичного видалення з таблиці.

::

::

---

## Створення Entity класів

### Що таке Entity в TypeORM

**Entity** — це TypeScript клас, який представляє таблицю у базі даних. Кожна властивість класу відображається на колонку таблиці, а екземпляр класу представляє один рядок даних. TypeORM використовує декоратори для опису структури Entity та генерації SQL-схеми.

**Фундаментальна концепція відображення:**

::mermaid

```mermaid
graph LR
    A[TypeScript Class] -->|@Entity| B[Database Table]
    C[Class Property] -->|@Column| D[Table Column]
    E[Class Instance] -->|save| F[Table Row]
    
    style A fill:#DBEAFE,stroke:#1d4ed8,color:#1e293b
    style B fill:#DCFCE7,stroke:#16a34a,color:#1e293b
    style C fill:#FEF3C7,stroke:#b45309,color:#1e293b
    style D fill:#FDE68A,stroke:#b45309,color:#1e293b
    style E fill:#E0E7FF,stroke:#4f46e5,color:#1e293b
    style F fill:#D1FAE5,stroke:#16a34a,color:#1e293b
```

::

Entity класи виконують кілька критичних функцій:

1. **Схема даних:** Визначають структуру таблиці (назви колонок, типи, обмеження).
2. **Типізація:** Забезпечують type safety у TypeScript коді.
3. **Валідація:** Можуть містити валідаційні декоратори (через `class-validator`).
4. **Бізнес-логіка:** Можуть інкапсулювати методи доменної моделі.

::note

У попередніх лекціях ми налаштували DataSource та з'єднання з БД. Тепер ми навчимося створювати структури даних, які TypeORM автоматично перетворить на SQL-таблиці.

::

### Декоратор `@Entity()` та назва таблиці

Щоб позначити клас як Entity, використовуйте декоратор `@Entity()`. Цей декоратор приймає необов'язковий параметр — назву таблиці у базі даних.

**Найпростіший Entity:**

```typescript [src/entities/user.entity.ts]
import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity() // Назва таблиці буде "user" (у нижньому регістрі)
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  email: string;

  @Column()
  name: string;
}
```

**Явне вказання назви таблиці:**

```typescript
@Entity('users') // Таблиця називатиметься "users"
export class User {
  // ...
}
```

**Вказання схеми PostgreSQL:**

```typescript
@Entity('users', { schema: 'public' })
export class User {
  // ...
}

// Або для окремої схеми
@Entity('users', { schema: 'auth' })
export class AuthUser {
  // ...
}
```

Це згенерує SQL:

```sql
CREATE TABLE "public"."users" (
  "id" SERIAL PRIMARY KEY,
  "email" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL
);
```

::tip

**Конвенція іменування:** TypeORM автоматично конвертує `PascalCase` назву класу у `snake_case` назву таблиці. Клас `UserProfile` стане таблицею `user_profile`. Якщо ви хочете інше іменування, вкажіть явно: `@Entity('user_profiles')`.

::

### Базова структура Entity класу

Типовий Entity клас має таку структуру:

```typescript [src/users/entities/user.entity.ts]
import { 
  Entity, 
  PrimaryGeneratedColumn, 
  Column, 
  CreateDateColumn,
  UpdateDateColumn 
} from 'typeorm';

@Entity('users')
export class User {
  // Первинний ключ (auto-increment)
  @PrimaryGeneratedColumn()
  id: number;

  // Обов'язкові поля
  @Column({ unique: true })
  email: string;

  @Column()
  name: string;

  // Опціональні поля
  @Column({ nullable: true })
  phone?: string;

  // Автоматичні timestamp
  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;

  // Бізнес-методи (не зберігаються у БД)
  getDisplayName(): string {
    return this.name || this.email.split('@')[0];
  }
}
```

**Ключові елементи структури:**

::field-group

::field{name="@PrimaryGeneratedColumn()" type="decorator"}
Визначає первинний ключ із автоматичною генерацією значень (SERIAL у PostgreSQL). Кожна Entity **обов'язково** повинна мати хоча б один primary key.

::

::field{name="@Column()" type="decorator"}
Позначає звичайну колонку таблиці. Приймає об'єкт опцій для налаштування типу, обмежень та поведінки.

::

::field{name="@CreateDateColumn()" type="decorator"}
Спеціальна колонка, яка автоматично встановлюється на момент створення рядка. TypeORM викликає `NOW()` у SQL.

::

::field{name="@UpdateDateColumn()" type="decorator"}
Автоматично оновлюється при кожній зміні рядка через `save()` або `update()`.

::

::

### Конвенції іменування

TypeORM підтримує різні стратегії іменування (*naming strategies*). За замовчуванням використовується наступна логіка:

| Елемент TypeScript    | Назва у PostgreSQL   | Приклад                        |
| --------------------- | -------------------- | ------------------------------ |
| Клас `User`           | `user`               | `CREATE TABLE "user"`          |
| Клас `UserProfile`    | `user_profile`       | `CREATE TABLE "user_profile"`  |
| Поле `firstName`      | `firstName`          | `"firstName" VARCHAR`          |
| Поле `created_at`     | `created_at`         | `"created_at" TIMESTAMP`       |

**Кастомна стратегія іменування:**

Якщо ви хочете, щоб усі поля автоматично конвертувалися у `snake_case`:

```typescript [src/config/snake-naming.strategy.ts]
import { DefaultNamingStrategy, NamingStrategyInterface } from 'typeorm';
import { snakeCase } from 'typeorm/util/StringUtils';

export class SnakeNamingStrategy extends DefaultNamingStrategy implements NamingStrategyInterface {
  columnName(propertyName: string, customName: string): string {
    return customName || snakeCase(propertyName);
  }
}
```

```typescript [src/app.module.ts]
TypeOrmModule.forRoot({
  // ...
  namingStrategy: new SnakeNamingStrategy(),
})
```

Тепер поле `firstName` автоматично стане колонкою `first_name`.

::warning

Зміна naming strategy у існуючому проєкті призведе до невідповідності між Entity та реальною схемою БД. Якщо ви вирішите змінити стратегію, обов'язково створіть міграцію для перейменування колонок.

::

---

## Primary Keys

### `@PrimaryGeneratedColumn()` для auto-increment

Найпоширеніший тип первинного ключа — auto-increment integer. PostgreSQL використовує тип `SERIAL` або `BIGSERIAL`.

```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number; // INTEGER AUTO_INCREMENT
}
```

Згенерований SQL:

```sql
CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY
);
```

**Типи auto-increment:**

```typescript
// INTEGER (до 2,147,483,647)
@PrimaryGeneratedColumn()
id: number;

// BIGINT (до 9,223,372,036,854,775,807)
@PrimaryGeneratedColumn('increment')
id: number;
```

::note

У PostgreSQL тип `SERIAL` — це псевдонім для `INTEGER` із автоматичним створенням sequence. При вставці нового рядка PostgreSQL автоматично викликає `nextval('user_id_seq')` для отримання наступного значення.

::

### `@PrimaryGeneratedColumn('uuid')` для UUID

UUID (*Universally Unique Identifier*) — 128-бітний ідентифікатор, який генерується випадковим чином та має надзвичайно низьку ймовірність колізії.

```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string; // UUID v4: "550e8400-e29b-41d4-a716-446655440000"
}
```

Згенерований SQL (PostgreSQL):

```sql
CREATE TABLE "user" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4()
);
```

**Переваги UUID:**

- **Розподілені системи:** Можна генерувати ID на клієнті без координації з БД.
- **Безпека:** Неможливо передбачити наступний ID (на відміну від auto-increment).
- **Масштабування:** Немає проблем при злитті даних з різних баз.

**Недоліки UUID:**

- **Розмір індексів:** UUID займає 16 байт проти 4 байт для INTEGER.
- **Продуктивність:** B-tree індекси на UUID можуть бути повільнішими через відсутність послідовності.
- **Читабельність:** Важче працювати вручну (`id=42` проти `id=550e8400-e29b-41d4-a716-446655440000`).

::tip

Для production-систем із high-traffic рекомендується використовувати **UUID v7** (time-ordered UUID), який зберігає timestamp у перших байтах, що значно покращує продуктивність індексів. TypeORM не підтримує UUID v7 нативно, але ви можете використати бібліотеку `uuid` для ручної генерації.

::

### `@PrimaryColumn()` для власних ID

Якщо вам потрібен власний формат ID (наприклад, `USER_001`, `ORD_20240905_1234`), використовуйте `@PrimaryColumn()`:

```typescript
@Entity()
export class Order {
  @PrimaryColumn()
  id: string; // Ви самостійно генеруєте значення

  @Column()
  total: number;
}

// Використання
const order = new Order();
order.id = `ORD_${Date.now()}_${Math.random().toString(36).substring(7)}`;
order.total = 99.99;
await orderRepository.save(order);
```

::caution

При використанні `@PrimaryColumn()` **ви відповідаєте за унікальність** значень. TypeORM не перевіряє колізії автоматично — якщо спробуєте вставити дублікат, отримаєте помилку БД `unique_violation`.

::

### Composite primary keys

PostgreSQL підтримує складені первинні ключі (*composite keys*) — комбінацію кількох колонок як унікальний ідентифікатор.

```typescript
@Entity()
export class UserRole {
  @PrimaryColumn()
  user_id: number;

  @PrimaryColumn()
  role_id: number;

  @Column()
  assigned_at: Date;
}
```

Згенерований SQL:

```sql
CREATE TABLE "user_role" (
  "user_id" INTEGER NOT NULL,
  "role_id" INTEGER NOT NULL,
  "assigned_at" TIMESTAMP NOT NULL,
  PRIMARY KEY ("user_id", "role_id")
);
```

**Пошук за composite key:**

```typescript
const userRole = await userRoleRepository.findOneBy({
  user_id: 1,
  role_id: 2,
});
```

::note

Composite keys корисні для **проміжних таблиць** (*junction tables*) у many-to-many зв'язках. Проте для більшості Entity рекомендується використовувати один синтетичний ключ (auto-increment або UUID) для простоти.

::

---

## Колонки: базові типи

### `@Column()` для звичайних полів

Декоратор `@Column()` перетворює властивість TypeScript на колонку таблиці. TypeORM автоматично визначає тип PostgreSQL на основі TypeScript типу, але ви можете вказати його явно.

**Автоматичне визначення типу:**

```typescript
@Entity()
export class Product {
  @Column()
  name: string; // VARCHAR

  @Column()
  price: number; // DOUBLE PRECISION

  @Column()
  inStock: boolean; // BOOLEAN
}
```

### Типи: `string`, `number`, `boolean`

TypeORM мапить TypeScript типи на SQL типи наступним чином:


| TypeScript Тип | PostgreSQL Тип (за замовчуванням) | Альтернативи                    |
| -------------- | --------------------------------- | ------------------------------- |
| `string`       | `VARCHAR`                         | `TEXT`, `CHAR(n)`               |
| `number`       | `DOUBLE PRECISION`                | `INTEGER`, `BIGINT`, `DECIMAL`  |
| `boolean`      | `BOOLEAN`                         | —                               |
| `Date`         | `TIMESTAMP`                       | `DATE`, `TIME`, `TIMESTAMPTZ`   |

**Приклади явного вказання типу:**

```typescript
@Entity()
export class Product {
  @Column('varchar', { length: 255 })
  name: string;

  @Column('decimal', { precision: 10, scale: 2 })
  price: number; // Зберігає 12345678.90

  @Column('boolean', { default: true })
  inStock: boolean;
}
```

### `varchar` vs `text`

**VARCHAR(n):** Рядок змінної довжини з максимальним обмеженням.

```typescript
@Column('varchar', { length: 100 })
email: string; // До 100 символів
```

**TEXT:** Необмежений текст (до 1GB у PostgreSQL).

```typescript
@Column('text')
bio: string; // Будь-яка довжина
```

**Коли використовувати:**

- **VARCHAR:** Для полів із передбачуваною максимальною довжиною (email, телефон, ім'я).
- **TEXT:** Для довгих текстів невизначеної довжини (описи, коментарі, статті).

::note

**Міф про продуктивність:** У PostgreSQL `TEXT` та `VARCHAR` мають однакову внутрішню реалізацію (*varlena*). Різниця лише у перевірці довжини на рівні SQL. Для коротких рядків (<100 байт) немає різниці у продуктивності.

::

### `int`, `bigint`, `float`, `decimal`

**INTEGER:** 32-бітне ціле число (−2,147,483,648 до 2,147,483,647).

```typescript
@Column('int')
age: number;

@Column('int', { default: 0 })
views_count: number;
```

**BIGINT:** 64-бітне ціле число (до 9 квінтильйонів).

```typescript
@Column('bigint')
file_size_bytes: number; // Для файлів > 2GB
```

**FLOAT / DOUBLE PRECISION:** Число з плаваючою крапкою (не точне для грошей!).

```typescript
@Column('float')
temperature: number; // 23.456

@Column('double precision')
latitude: number; // 50.450100
```

**DECIMAL / NUMERIC:** Точне число з фіксованою кількістю знаків після коми.

```typescript
@Column('decimal', { precision: 10, scale: 2 })
price: number; // 99999999.99
```

**Параметри DECIMAL:**

- **precision:** Загальна кількість цифр (ліворуч + праворуч від коми).
- **scale:** Кількість цифр після коми.

```typescript
// precision=10, scale=2 дозволяє:
// Мінімум: -99999999.99
// Максимум: +99999999.99
```

::caution

**Ніколи не використовуйте FLOAT для грошей!** Числа з плаваючою крапкою мають проблеми точності через бінарне представлення:

```typescript
// ❌ ПОГАНО
@Column('float')
balance: number; // Може стати 99.99999999999999

// ✅ ДОБРЕ
@Column('decimal', { precision: 12, scale: 2 })
balance: number; // Завжди точно 99.99
```

::

---

## Колонки: складні типи

### `enum` для переліків

PostgreSQL підтримує нативні ENUM типи. TypeORM дозволяє мапити TypeScript enum на PostgreSQL enum:

```typescript [src/users/enums/user-role.enum.ts]
export enum UserRole {
  ADMIN = 'admin',
  MODERATOR = 'moderator',
  USER = 'user',
  GUEST = 'guest',
}
```

```typescript [src/users/entities/user.entity.ts]
import { UserRole } from '../enums/user-role.enum';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.USER,
  })
  role: UserRole;
}
```

Згенерований SQL:

```sql
CREATE TYPE "user_role_enum" AS ENUM('admin', 'moderator', 'user', 'guest');

CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY,
  "role" "user_role_enum" NOT NULL DEFAULT 'user'
);
```

**Type-safe використання:**

```typescript
const user = new User();
user.role = UserRole.ADMIN; // ✅ OK
user.role = 'superadmin';   // ❌ Compile error
```

::tip

Enum типи забезпечують **валідацію на рівні БД**. Якщо хтось спробує вставити невалідне значення напряму через SQL, PostgreSQL відхилить операцію:

```sql
INSERT INTO "user" (role) VALUES ('hacker'); 
-- ERROR: invalid input value for enum user_role_enum: "hacker"
```

::

### `date`, `timestamp` для дат

PostgreSQL має кілька типів для роботи з датами та часом:

| SQL Тип           | TypeScript | Зберігає                         | Приклад                      |
| ----------------- | ---------- | -------------------------------- | ---------------------------- |
| `DATE`            | `Date`     | Тільки дату (без часу)           | `2024-09-05`                 |
| `TIME`            | `string`   | Тільки час (без дати)            | `14:30:00`                   |
| `TIMESTAMP`       | `Date`     | Дата + час (без timezone)        | `2024-09-05 14:30:00`        |
| `TIMESTAMPTZ`     | `Date`     | Дата + час (з timezone)          | `2024-09-05 14:30:00+02:00`  |

**Приклади:**

```typescript
@Entity()
export class Event {
  @Column('date')
  event_date: Date; // Тільки дата

  @Column('time')
  event_time: string; // "14:30:00"

  @Column('timestamp')
  scheduled_at: Date; // Дата + час

  @Column('timestamptz')
  created_at: Date; // З timezone (рекомендовано для production)
}
```

::warning

**TIMESTAMP vs TIMESTAMPTZ:**

- `TIMESTAMP` зберігає «наївний» час без інформації про timezone. Якщо ви вставите `2024-09-05 14:30:00 UTC`, а потім прочитаєте у timezone `America/New_York`, ви отримаєте ту саму дату, ігноруючи різницю в часових поясах.
  
- `TIMESTAMPTZ` зберігає час у UTC всередині та автоматично конвертує при читанні/записі відповідно до timezone сесії PostgreSQL.

**Рекомендація:** Для глобальних застосунків завжди використовуйте `TIMESTAMPTZ`.

::

### `json` та `jsonb` для JSON даних

PostgreSQL підтримує два JSON типи:

- **JSON:** Текстове збереження JSON (повільніше, але зберігає порядок ключів).
- **JSONB:** Бінарне збереження JSON (швидше, підтримує індексацію, рекомендовано).

```typescript
@Entity()
export class User {
  @Column('jsonb', { nullable: true })
  metadata: {
    preferences: {
      theme: 'dark' | 'light';
      language: string;
    };
    settings: Record<string, any>;
  };

  @Column('jsonb', { array: false, default: {} })
  tags: string[];
}
```

**Використання:**

```typescript
const user = new User();
user.metadata = {
  preferences: {
    theme: 'dark',
    language: 'uk',
  },
  settings: {
    notifications: true,
  },
};

await userRepository.save(user);
```

**Запити до JSONB:**

```typescript
// Пошук за вкладеним полем
const darkThemeUsers = await userRepository
  .createQueryBuilder('user')
  .where("user.metadata->>'preferences'->>'theme' = :theme", { theme: 'dark' })
  .getMany();
```

::tip

JSONB підтримує **GIN індекси** для швидкого пошуку:

```sql
CREATE INDEX idx_user_metadata_gin ON "user" USING GIN (metadata);
```

Це дозволяє ефективно шукати за будь-яким ключем всередині JSON без повного сканування таблиці.

::

### `array` для масивів

PostgreSQL нативно підтримує масиви примітивних типів:

```typescript
@Entity()
export class Post {
  @Column('text', { array: true })
  tags: string[]; // text[]

  @Column('int', { array: true, default: [] })
  related_post_ids: number[]; // integer[]
}
```

Згенерований SQL:

```sql
CREATE TABLE "post" (
  "tags" TEXT[] NOT NULL,
  "related_post_ids" INTEGER[] DEFAULT '{}'
);
```

**Використання:**

```typescript
const post = new Post();
post.tags = ['typescript', 'nodejs', 'typeorm'];
post.related_post_ids = [42, 99, 123];

await postRepository.save(post);
```

**Запити до масивів:**

```typescript
// Пошук постів, що містять тег 'typescript'
const posts = await postRepository
  .createQueryBuilder('post')
  .where(':tag = ANY(post.tags)', { tag: 'typescript' })
  .getMany();
```

### `simple-array` та `simple-json`

TypeORM надає два спрощені типи для зберігання масивів та об'єктів у звичайних текстових колонках (без використання PostgreSQL типів):

**simple-array:** Масив рядків, збережений як CSV.

```typescript
@Column('simple-array')
hobbies: string[]; // Зберігається як "reading,coding,gaming"
```

**simple-json:** Об'єкт, збережений як JSON-рядок.

```typescript
@Column('simple-json')
settings: { theme: string; language: string }; // Зберігається як '{"theme":"dark","language":"uk"}'
```

::caution

**Не використовуйте `simple-array` та `simple-json` для PostgreSQL!** Ці типи призначені для БД, які не підтримують нативні JSON та масиви (MySQL, SQLite). Для PostgreSQL завжди використовуйте `jsonb` та `array`.

::

---

## Опції колонок

### `nullable`: дозвіл NULL значень

За замовчуванням усі колонки є `NOT NULL`. Щоб дозволити NULL:

```typescript
@Entity()
export class User {
  @Column()
  email: string; // NOT NULL

  @Column({ nullable: true })
  phone?: string; // NULL дозволено

  @Column({ nullable: true })
  middle_name?: string;
}
```

**Типізація TypeScript:**

Використовуйте `?` для опціональних полів, щоб TypeScript перевіряв наявність значення:

```typescript
const user = new User();
user.email = 'test@example.com'; // Обов'язково
// user.phone не потрібно задавати

console.log(user.phone?.toUpperCase()); // ✅ Safe navigation
console.log(user.email.toUpperCase());  // ✅ Гарантовано не undefined
```

### `default`: значення за замовчуванням

Встановлює значення за замовчуванням на рівні БД:

```typescript
@Entity()
export class Post {
  @Column({ default: 0 })
  views_count: number;

  @Column({ default: true })
  is_published: boolean;

  @Column({ default: () => 'NOW()' })
  created_at: Date;

  @Column({ default: 'draft' })
  status: string;
}
```

**Функції PostgreSQL як default:**

```typescript
@Column({ default: () => "uuid_generate_v4()" })
id: string;

@Column({ default: () => "CURRENT_TIMESTAMP" })
timestamp: Date;

@Column({ default: () => "'[]'::jsonb" })
metadata: any;
```

::note

Значення за замовчуванням встановлюються **на рівні БД**, а не на рівні TypeScript. Якщо ви створите екземпляр Entity без явного присвоєння, TypeScript-властивість буде `undefined` до моменту збереження у БД.

::

### `unique`: унікальність значень

Створює UNIQUE обмеження на рівні БД:

```typescript
@Entity()
export class User {
  @Column({ unique: true })
  email: string; // Два користувачі не можуть мати однаковий email

  @Column({ unique: true })
  username: string;
}
```

**Composite unique constraint:**

```typescript
@Entity()
@Unique(['first_name', 'last_name'])
export class Person {
  @Column()
  first_name: string;

  @Column()
  last_name: string;
}
```

Тепер комбінація `first_name + last_name` має бути унікальною.

### `length`: максимальна довжина

Для VARCHAR колонок:

```typescript
@Column({ length: 100 })
email: string; // VARCHAR(100)

@Column({ length: 20 })
phone: string; // VARCHAR(20)
```

::tip

Обмеження довжини на рівні БД — це додаткова валідація, але вона **не замінює** валідацію на рівні застосунку. Використовуйте `class-validator` для перевірки даних перед збереженням.

::

### `comment`: коментар для документації

Додає SQL коментар до колонки (видимий у `\d table_name` у psql):

```typescript
@Column({ comment: 'User primary email address for authentication' })
email: string;

@Column({ type: 'decimal', precision: 10, scale: 2, comment: 'Price in USD' })
price: number;
```

### `select`: виключення з SELECT за замовчуванням

Корисно для чутливих полів (паролі, токени):

```typescript
@Entity()
export class User {
  @Column()
  email: string;

  @Column({ select: false })
  password: string; // Не включається у SELECT *
}
```

**Поведінка:**

```typescript
// Пароль НЕ завантажиться
const user = await userRepository.findOneBy({ email: 'test@example.com' });
console.log(user.password); // undefined

// Явне завантаження пароля
const userWithPassword = await userRepository
  .createQueryBuilder('user')
  .addSelect('user.password') // Явно включаємо
  .where('user.email = :email', { email: 'test@example.com' })
  .getOne();

console.log(userWithPassword.password); // Тепер доступно
```


---

## Автоматичні timestamp поля

### `@CreateDateColumn()`: дата створення

Автоматично встановлює дату та час створення рядка. TypeORM викликає `NOW()` у PostgreSQL при INSERT.

```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  email: string;

  @CreateDateColumn()
  created_at: Date; // Автоматично заповнюється при save()
}
```

**Використання:**

```typescript
const user = new User();
user.email = 'test@example.com';
// created_at не потрібно задавати!

await userRepository.save(user);

console.log(user.created_at); // 2024-09-05T14:30:00.000Z
```

Згенерований SQL:

```sql
INSERT INTO "user" ("email", "created_at") 
VALUES ('test@example.com', NOW()) 
RETURNING "id", "created_at";
```

### `@UpdateDateColumn()`: дата оновлення

Автоматично оновлюється при кожній зміні рядка через `save()` або `update()`:

```typescript
@Entity()
export class Post {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date; // Оновлюється при кожному save()
}
```

**Поведінка:**

```typescript
// Створення
const post = new Post();
post.title = 'First Post';
await postRepository.save(post);

console.log(post.created_at); // 2024-09-05 14:30:00
console.log(post.updated_at); // 2024-09-05 14:30:00 (однакові)

// Оновлення через 5 хвилин
post.title = 'Updated Title';
await postRepository.save(post);

console.log(post.created_at); // 2024-09-05 14:30:00 (не змінилась)
console.log(post.updated_at); // 2024-09-05 14:35:00 (оновилась!)
```

::note

`@UpdateDateColumn()` **не** оновлюється при використанні `update()` або `query()` напряму:

```typescript
// ❌ updated_at НЕ оновиться
await postRepository.update({ id: 1 }, { title: 'New Title' });

// ✅ updated_at оновиться
const post = await postRepository.findOneBy({ id: 1 });
post.title = 'New Title';
await postRepository.save(post);
```

::

### Автоматичне заповнення TypeORM

TypeORM автоматично заповнює ці поля при виконанні операцій через репозиторії. Якщо ви використовуєте raw SQL, ви відповідаєте за встановлення timestamp вручну.

**Внутрішній механізм:**

1. При `save()` TypeORM перевіряє, чи Entity має `@CreateDateColumn()` або `@UpdateDateColumn()`.
2. Генерує SQL із `NOW()` або `CURRENT_TIMESTAMP` для цих полів.
3. Після INSERT/UPDATE зчитує повернені значення та оновлює об'єкт Entity.

### Timezone considerations

За замовчуванням PostgreSQL зберігає timestamp у **UTC** та конвертує їх відповідно до timezone сесії.

**Налаштування timezone у PostgreSQL:**

```sql
-- Перевірити поточний timezone
SHOW timezone;

-- Встановити для сесії
SET timezone = 'Europe/Kyiv';

-- Встановити глобально (у postgresql.conf)
timezone = 'UTC'
```

**Налаштування timezone у TypeORM:**

```typescript
TypeOrmModule.forRoot({
  type: 'postgres',
  // ...
  extra: {
    timezone: 'UTC', // Рекомендовано для production
  },
})
```

::tip

**Best practice для глобальних застосунків:**

1. Зберігайте всі timestamp у **UTC** (налаштуйте timezone сервера та БД на UTC).
2. Конвертуйте у локальний timezone **на клієнті** (frontend).
3. Використовуйте бібліотеки типу `dayjs` або `date-fns-tz` для роботи з timezone.

Це запобігає плутанині при роботі з користувачами з різних країн.

::

---

## Soft Delete та Versioning

### `@DeleteDateColumn()`: м'яке видалення

**Soft delete** — це механізм логічного видалення, коли замість фізичного видалення рядка з БД ми встановлюємо timestamp у спеціальну колонку `deleted_at`. Це дозволяє «відновити» видалені дані або аналізувати їх пізніше.

```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  email: string;

  @CreateDateColumn()
  created_at: Date;

  @DeleteDateColumn()
  deleted_at?: Date; // NULL = не видалено, NOT NULL = видалено
}
```

**Використання:**

```typescript
// Звичайне видалення (hard delete) — фізичне видалення
await userRepository.delete({ id: 1 });

// М'яке видалення (soft delete) — встановлює deleted_at
await userRepository.softDelete({ id: 1 });

// Або через метод екземпляра
const user = await userRepository.findOneBy({ id: 1 });
await userRepository.softRemove(user);
```

### Робота з видаленими записами

Після soft delete рядок **автоматично ховається** з усіх запитів:

```typescript
// Повертає тільки не видалених користувачів
const users = await userRepository.find();

// Видалений користувач не знайдеться
const deletedUser = await userRepository.findOneBy({ id: 1 }); // null
```

**Відновлення видалених записів:**

```typescript
await userRepository.restore({ id: 1 }); // Встановлює deleted_at = NULL
```

**Пошук разом із видаленими:**

```typescript
const allUsers = await userRepository.find({
  withDeleted: true, // Включає видалених
});

// Або тільки видалені
const deletedUsers = await userRepository
  .createQueryBuilder('user')
  .where('user.deleted_at IS NOT NULL')
  .withDeleted()
  .getMany();
```

::tip

**Use cases для soft delete:**

- **Юридичні вимоги:** GDPR дозволяє «право на забуття», але деякі країни вимагають зберігати дані протягом певного періоду.
- **Аудит:** Можливість переглянути історію видалень.
- **Захист від помилок:** Користувач може випадково видалити важливі дані.
- **Архівування:** Старі записи приховуються, але доступні для аналітики.

::

### `@VersionColumn()`: оптимістичне блокування

**Versioning** — це механізм запобігання **lost update problem** у конкурентних системах. При кожному оновленні рядка TypeORM автоматично інкрементує версію та перевіряє, чи не змінили інші процеси цей рядок одночасно.

```typescript
@Entity()
export class BankAccount {
  @PrimaryGeneratedColumn()
  id: number;

  @Column('decimal', { precision: 12, scale: 2 })
  balance: number;

  @VersionColumn()
  version: number; // Автоматично інкрементується при кожному update
}
```

**Сценарій без versioning (проблема):**

```typescript
// Процес A: читає баланс = 1000
const accountA = await repository.findOneBy({ id: 1 });
// balance = 1000, version = 1

// Процес B: читає баланс = 1000
const accountB = await repository.findOneBy({ id: 1 });
// balance = 1000, version = 1

// Процес A: знімає 100
accountA.balance -= 100; // 900
await repository.save(accountA);
// UPDATE ... SET balance = 900, version = 2 WHERE id = 1

// Процес B: знімає 200
accountB.balance -= 200; // 800
await repository.save(accountB);
// UPDATE ... SET balance = 800, version = 2 WHERE id = 1 AND version = 1
// ❌ OptimisticLockVersionMismatchError!
```

**Як це працює:**

1. TypeORM генерує SQL із перевіркою версії: `WHERE id = 1 AND version = 1`
2. Якщо версія змінилася (інший процес оновив рядок), `rowCount = 0`.
3. TypeORM викидає `OptimisticLockVersionMismatchError`.
4. Застосунок має перечитати дані та повторити операцію.

**Обробка помилки версії:**

```typescript
import { OptimisticLockVersionMismatchError } from 'typeorm';

async function withdrawMoney(accountId: number, amount: number, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const account = await repository.findOneBy({ id: accountId });
      
      if (account.balance < amount) {
        throw new Error('Insufficient funds');
      }
      
      account.balance -= amount;
      await repository.save(account); // Може викинути OptimisticLockVersionMismatchError
      
      return account; // Успіх
      
    } catch (error) {
      if (error instanceof OptimisticLockVersionMismatchError) {
        console.log(`Conflict detected, retry ${attempt + 1}/${maxRetries}`);
        await new Promise(resolve => setTimeout(resolve, 100)); // Затримка
        continue; // Повторна спроба
      }
      throw error; // Інша помилка
    }
  }
  
  throw new Error('Max retries reached due to concurrent updates');
}
```

### Use cases для versioning

**Коли використовувати `@VersionColumn()`:**

- **Фінансові операції:** Рахунки, транзакції, баланси.
- **Інвентаризація:** Кількість товарів на складі.
- **Конкурентні оновлення:** Кілька користувачів редагують один документ.
- **Distributed systems:** Запобігання race conditions у мікросервісах.

**Коли НЕ потрібен:**

- Read-heavy застосунки без конкурентних записів.
- Дані, що оновлюються лише одним процесом.
- Логи та аудит (append-only дані).

---

## Практичні приклади

### Entity для User

Повноцінний Entity класу користувача із усіма вивченими декораторами:

```typescript [src/users/entities/user.entity.ts]
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  DeleteDateColumn,
  Index,
} from 'typeorm';

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest',
}

@Entity('users')
@Index(['email']) // Індекс для швидкого пошуку
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true, length: 255 })
  email: string;

  @Column({ select: false })
  password: string; // Хеш пароля, не завантажується за замовчуванням

  @Column({ length: 100 })
  first_name: string;

  @Column({ length: 100 })
  last_name: string;

  @Column({ nullable: true, length: 20 })
  phone?: string;

  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.USER,
  })
  role: UserRole;

  @Column({ default: true })
  is_active: boolean;

  @Column({ default: false })
  is_email_verified: boolean;

  @Column('text', { nullable: true })
  bio?: string;

  @Column('jsonb', { default: {} })
  preferences: {
    theme?: 'light' | 'dark';
    language?: string;
    notifications?: boolean;
  };

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;

  @DeleteDateColumn()
  deleted_at?: Date;

  // Бізнес-методи
  getFullName(): string {
    return `${this.first_name} ${this.last_name}`;
  }

  isAdmin(): boolean {
    return this.role === UserRole.ADMIN;
  }
}
```

### Entity для Post

Приклад блогового поста зі зв'язком до User (буде детально у наступних лекціях):

```typescript [src/posts/entities/post.entity.ts]
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  Index,
  VersionColumn,
} from 'typeorm';

export enum PostStatus {
  DRAFT = 'draft',
  PUBLISHED = 'published',
  ARCHIVED = 'archived',
}

@Entity('posts')
@Index(['slug'], { unique: true })
@Index(['status', 'published_at'])
export class Post {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 255 })
  title: string;

  @Column({ unique: true, length: 255 })
  slug: string; // URL-friendly назва

  @Column('text')
  content: string;

  @Column('text', { nullable: true })
  excerpt?: string; // Короткий опис

  @Column({
    type: 'enum',
    enum: PostStatus,
    default: PostStatus.DRAFT,
  })
  status: PostStatus;

  @Column('text', { array: true, default: [] })
  tags: string[];

  @Column({ default: 0 })
  views_count: number;

  @Column({ default: 0 })
  likes_count: number;

  @Column('timestamptz', { nullable: true })
  published_at?: Date;

  @Column('jsonb', { nullable: true })
  seo_metadata?: {
    title?: string;
    description?: string;
    keywords?: string[];
  };

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;

  @VersionColumn()
  version: number; // Захист від одночасного редагування

  // Методи
  isPublished(): boolean {
    return this.status === PostStatus.PUBLISHED && !!this.published_at;
  }

  incrementViews(): void {
    this.views_count += 1;
  }
}
```

### Entity для Product з різними типами полів

Приклад e-commerce продукту:

```typescript [src/products/entities/product.entity.ts]
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  Index,
} from 'typeorm';

@Entity('products')
@Index(['sku'], { unique: true })
@Index(['category', 'is_available'])
export class Product {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true, length: 50 })
  sku: string; // Stock Keeping Unit

  @Column({ length: 255 })
  name: string;

  @Column('text')
  description: string;

  @Column('decimal', { precision: 10, scale: 2 })
  price: number; // Ціна у USD

  @Column('decimal', { precision: 5, scale: 2, nullable: true })
  discount_percent?: number; // 0.00 - 100.00

  @Column({ length: 100 })
  category: string;

  @Column({ length: 100, nullable: true })
  brand?: string;

  @Column('int', { default: 0 })
  stock_quantity: number;

  @Column({ default: true })
  is_available: boolean;

  @Column('decimal', { precision: 8, scale: 2, nullable: true })
  weight_kg?: number;

  @Column('jsonb', { nullable: true })
  dimensions?: {
    length: number;
    width: number;
    height: number;
    unit: 'cm' | 'inch';
  };

  @Column('jsonb', { default: {} })
  specifications: Record<string, any>; // Довільні характеристики

  @Column('text', { array: true, default: [] })
  image_urls: string[];

  @Column('text', { array: true, default: [] })
  tags: string[];

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;

  // Обчислювані поля (не зберігаються у БД)
  getFinalPrice(): number {
    if (this.discount_percent) {
      return this.price * (1 - this.discount_percent / 100);
    }
    return this.price;
  }

  isInStock(): boolean {
    return this.is_available && this.stock_quantity > 0;
  }
}
```

---

## Підсумок

::card-group

::card{title="✅ Що ви опанували" icon="i-lucide-check-circle"}

- Створили Entity класи з декораторами TypeORM для відображення таблиць БД на TypeScript класи.
- Вивчили різні типи primary keys: auto-increment, UUID, власні ID та composite keys.
- Опанували базові та складні типи колонок: від простих string/number до JSONB та масивів.
- Навчилися налаштовувати опції колонок: nullable, default, unique, length, select.
- Освоїли автоматичні timestamp поля (`@CreateDateColumn`, `@UpdateDateColumn`).
- Реалізували soft delete через `@DeleteDateColumn` та оптимістичне блокування через `@VersionColumn`.
- Створили повноцінні Entity для User, Post та Product із best practices.

::

::card{title="🚀 Наступні кроки" icon="i-lucide-arrow-right"}

У наступній лекції ви перейдете до роботи з даними через Repository Pattern:
- CRUD операції: create, find, update, delete
- Методи репозиторіїв: `save()`, `findOne()`, `findBy()`, `update()`, `remove()`
- Транзакції та bulk операції
- Custom репозиторії для складної бізнес-логіки

::

::

::accordion

::accordion-item{label="❓ Чи можна змінити тип колонки після створення Entity?" icon="i-lucide-help-circle"}

Так, але це потребує міграції. Якщо ви змінили `@Column('int')` на `@Column('bigint')`, TypeORM не змінить схему автоматично (якщо `synchronize: false`). Вам потрібно створити міграцію:

```typescript
await queryRunner.query(`ALTER TABLE "users" ALTER COLUMN "age" TYPE BIGINT`);
```

Важливо: деякі зміни типів можуть призвести до втрати даних (наприклад, `TEXT` → `VARCHAR(10)`).

::

::accordion-item{label="❓ Чому TypeORM не генерує колонку для методу класу?" icon="i-lucide-help-circle"}

TypeORM створює колонки **лише для властивостей** із декораторами `@Column()`, `@PrimaryColumn()` тощо. Методи класу (функції) не зберігаються у БД — вони призначені для бізнес-логіки.

Якщо вам потрібне обчислюване поле, використовуйте геттер:

```typescript
get fullName(): string {
  return `${this.first_name} ${this.last_name}`;
}
```

Або створіть віртуальну колонку (generated column у PostgreSQL 12+).

::

::accordion-item{label="❓ Як додати індекс на кілька колонок?" icon="i-lucide-help-circle"}

Використовуйте декоратор `@Index()` на рівні класу:

```typescript
@Entity()
@Index(['category', 'is_available']) // Composite index
@Index(['email'], { unique: true })  // Unique index
export class Product {
  @Column()
  category: string;

  @Column()
  is_available: boolean;

  @Column()
  email: string;
}
```

Або через міграції для складних індексів (GIN, GiST, partial indexes).

::

::

::note

**Корисні ресурси:**

- [TypeORM Entities Documentation](https://typeorm.io/entities)
- [TypeORM Column Types](https://typeorm.io/entities#column-types)
- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [TypeORM Decorators Reference](https://typeorm.io/decorator-reference)

::

---

**Вітаємо! Ви опанували Entity класи та декоратори TypeORM.** Тепер ви можете створювати типізовані структури даних, які TypeORM автоматично перетворює на PostgreSQL таблиці. У наступній лекції ми перейдемо до практичної роботи з даними через Repository Pattern та виконаємо CRUD операції.