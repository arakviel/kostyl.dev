# Робота з базами даних у Node.js через нативні драйвери

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати основи роботи з реляційними базами даних у середовищі Node.js через нативні драйвери.
- Зрозуміти різницю між прямим використанням SQL та абстракціями ORM (*Object-Relational Mapping*).
- Навчитися безпечно виконувати запити до PostgreSQL через пакет `pg` (*node-postgres*).
- Освоїти механізм пулів з'єднань (*connection pooling*) для підвищення продуктивності серверних застосунків.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Драйвер БД** (*database driver*): низькорівнева бібліотека для з'єднання застосунку з системою керування базою даних (СУБД).
- **Connection Pool**: механізм багаторазового використання TCP-з'єднань із базою даних для зменшення накладних витрат.
- **Prepared Statement**: попередньо скомпільований SQL-запит із плейсхолдерами (*placeholders*) для параметрів, що запобігає SQL-ін'єкціям.
- **Transaction**: атомарна послідовність операцій БД, яка або виконується цілком, або відкочується повністю.

::

::

---

## Архітектурний контекст: від TCP-сокета до запиту SQL

Перед тим як почати писати код, важливо зрозуміти, що відбувається «під капотом» при взаємодії Node.js застосунку з реляційною базою даних. На фундаментальному рівні процес виглядає наступним чином:

1. **Встановлення TCP-з'єднання**: застосунок відкриває TCP-сокет на стандартний порт PostgreSQL (за замовчуванням `5432`). Якщо база розташована на віддаленому сервері, виконується трьохкроковий хендшейк (*three-way handshake*) для створення надійного каналу передачі даних.

2. **Автентифікація**: після встановлення з'єднання клієнт надсилає credentials (ім'я користувача та пароль або сертифікат), які сервер PostgreSQL перевіряє за допомогою налаштувань `pg_hba.conf`.

3. **Обмін повідомленнями**: запити SQL передаються як текстові або бінарні повідомлення через з'єднання. Сервер БД парсить запит, виконує його та повертає результат у форматі, визначеному протоколом PostgreSQL (*Frontend/Backend Protocol*).

4. **Закриття з'єднання**: після завершення роботи сокет закривається. Проте, якщо використовується пул з'єднань, TCP-з'єднання не закривається фізично, а повертається в пул для повторного використання.

::note

У середовищі Node.js всі операції з базою даних є асинхронними за замовчуванням, що узгоджується з подійною моделлю (*event-driven model*) середовища виконання V8. Завдяки цьому застосунок може обробляти тисячі одночасних запитів до БД без блокування головного потоку.

::

::plant-uml{alt="Архітектура взаємодії Node.js із PostgreSQL"}

```plantuml
@startuml
skinparam style plain
skinparam backgroundColor #FFFFFF
autonumber

actor "Node.js застосунок" as App #DBEAFE
participant "Драйвер pg" as Driver #E2E8F0
participant "Connection Pool" as Pool #FEF3C7
database "PostgreSQL" as DB #DCFCE7

App -> Driver : import { Pool } from 'pg'
Driver -> Pool : new Pool({ host, port, user, ... })
Pool -> DB : Відкриття 5 TCP-з'єднань
note over Pool, DB #F1F5F9
  З'єднання встановлюються при ініціалізації пулу.
  Кожне з'єднання проходить автентифікацію.
end note

App -> Driver : await pool.query('SELECT * FROM users')
Driver -> Pool : Отримати вільне з'єднання
Pool --> Driver : Надати client із пулу
Driver -> DB : Відправити SQL через TCP
DB --> Driver : Повернути ResultSet (rows + metadata)
Driver --> App : Повернути Promise<QueryResult>
Driver -> Pool : Повернути client назад у пул

@enduml
```

::

---

## Нативні драйвери для PostgreSQL

### Огляд пакету `pg` (node-postgres)

Пакет **`pg`** — це найбільш широко використовуваний драйвер для з'єднання Node.js застосунків із PostgreSQL. Він надає низькорівневий API для виконання SQL-запитів, керування транзакціями та управління з'єднаннями. На відміну від ORM-бібліотек (*Object-Relational Mapping*), таких як TypeORM або Sequelize, драйвер `pg` не приховує SQL-синтаксис — ви працюєте безпосередньо з мовою запитів, що дає повний контроль над продуктивністю та оптимізацією.

**Основні переваги використання чистого драйвера:**

- **Повна прозорість:** ви бачите кожен SQL-запит, який надсилається до бази даних. Це критично важливо для профілювання та виявлення bottlenecks (*вузьких місць*) у продуктивності.
- **Мінімальні накладні витрати:** відсутність проміжних шарів абстракції означає, що немає додаткових витрат на серіалізацію об'єктів та маппінг результатів.
- **Ідеальний вибір для міграцій:** інструменти міграцій (наприклад, `node-pg-migrate` або `db-migrate`) зазвичай використовують саме драйвер `pg` для виконання DDL-команд (*Data Definition Language*: `CREATE TABLE`, `ALTER TABLE`).
- **Гнучкість у складних запитах:** для аналітичних звітів, агрегацій із кількома JOIN або рекурсивних CTE (*Common Table Expressions*) написання raw SQL часто є єдиним розумним варіантом.


::tip

Під час навчання рекомендується почати саме з драйвера `pg`, навіть якщо у промисловому проєкті ви плануєте використовувати ORM. Це дозволить зрозуміти, як працює комунікація з базою даних на найнижчому рівні, та усвідомити вартість кожної операції.

::

### Встановлення та базова конфігурація

Для початку роботи встановіть пакет `pg` та його TypeScript-типізацію у свій проєкт:

::tabs

::tabs-item{label="npm"}

```bash
npm install pg
npm install --save-dev @types/node @types/pg
```

::

::tabs-item{label="pnpm"}

```bash
pnpm add pg
pnpm add -D @types/node @types/pg
```

::

::tabs-item{label="yarn"}

```bash
yarn add pg
yarn add --dev @types/node @types/pg
```

::

::

Після встановлення переконайтеся, що у вашому `tsconfig.json` увімкнена підтримка модулів ESNext або CommonJS:

```json [tsconfig.json]
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Типи клієнтів: `Client` vs `Pool`

Драйвер `pg` надає два основні класи для роботи з базою даних:

**1. `Client` — одне з'єднання для ізольованих операцій:**

Клас `Client` представляє одне TCP-з'єднання з PostgreSQL. Він призначений для сценаріїв, коли потрібно виконати послідовність запитів у межах однієї транзакції або коли з'єднання керується вручну.

```typescript [client-example.ts]
import { Client } from 'pg';

async function singleConnectionExample() {
  const client = new Client({
    host: 'localhost',
    port: 5432,
    user: 'postgres',
    password: 'secret',
    database: 'myapp_dev',
  });

  await client.connect(); // Відкриття з'єднання
  console.log('З\'єднання встановлено');

  try {
    const result = await client.query('SELECT NOW()');
    console.log('Час на сервері БД:', result.rows[0].now);
  } finally {
    await client.end(); // Обов'язкове закриття!
  }
}

singleConnectionExample();
```

::warning

Якщо ви не викличете `client.end()`, TCP-сокет залишиться відкритим, що призведе до витоку ресурсів (*resource leak*). У промислових застосунках це може вичерпати ліміт одночасних з'єднань на стороні PostgreSQL (параметр `max_connections` у `postgresql.conf`).

::

**2. `Pool` — пул з'єднань для високонавантажених застосунків:**

Клас `Pool` керує набором з'єднань (`Client` екземплярів), які автоматично розподіляються між запитами. Це дозволяє обробляти велику кількість одночасних операцій без накладних витрат на повторне відкриття сокетів.

```typescript [pool-example.ts]
import { Pool } from 'pg';

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  user: 'postgres',
  password: 'secret',
  database: 'myapp_dev',
  max: 20, // Максимум 20 одночасних з'єднань
  idleTimeoutMillis: 30000, // Закривати неактивні з'єднання через 30 сек
  connectionTimeoutMillis: 2000, // Таймаут очікування вільного з'єднання
});

async function poolExample() {
  // Pool автоматично надає вільне з'єднання
  const result = await pool.query('SELECT COUNT(*) FROM users');
  console.log('Кількість користувачів:', result.rows[0].count);

  // З'єднання автоматично повертається в пул після завершення
}

poolExample();
```

::note

Метод `pool.query()` — це синтаксичний цукор (*syntactic sugar*), який автоматично бере з'єднання з пулу, виконує запит і повертає з'єднання назад. Для явного керування з'єднанням використовуйте `const client = await pool.connect()` та `client.release()`.

::

**Коли використовувати `Client`, а коли `Pool`?**

| Сценарій                                           | Рекомендація |
| -------------------------------------------------- | ------------ |
| Короткий скрипт для міграції або seed даних        | `Client`     |
| Веб-сервер (Express, NestJS) із сотнями запитів   | `Pool`       |
| Довга транзакція з кількома запитами               | `Pool.connect()` + `client.release()` |
| CLI-інструмент для одноразового аналізу даних      | `Client`     |
| Background workers (черги, cron-job)               | `Pool`       |

---

## Підключення до бази даних

### Connection string формат

PostgreSQL підтримує два способи передачі параметрів підключення: через окремі опції (об'єкт конфігурації) або через єдиний рядок у форматі URI (*Uniform Resource Identifier*).

**Формат connection string:**

```
postgresql://[user[:password]@][host][:port][/database][?param=value&...]
```

**Приклади:**

```typescript
// Локальна база без пароля
const connectionString1 = 'postgresql://localhost/myapp_dev';

// Віддалений сервер із автентифікацією
const connectionString2 = 'postgresql://admin:pass123@db.example.com:5432/production';

// Із додатковими параметрами (SSL, таймаути)
const connectionString3 = 'postgresql://user:pass@host:5432/db?sslmode=require&connect_timeout=10';
```

Використання connection string у коді:

```typescript [connection-string.ts]
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});
```

::tip

У production-середовищі завжди зберігайте connection string у змінних оточення (`.env` файл або secrets manager). Ніколи не хардкодьте credentials безпосередньо у коді, який потрапляє до системи контролю версій.

::

### Параметри підключення

Якщо ви віддаєте перевагу явній конфігурації, використовуйте об'єкт із наступними ключами:


```typescript [config-object.ts]
import { PoolConfig } from 'pg';

const config: PoolConfig = {
  host: 'localhost',           // Адреса сервера БД
  port: 5432,                  // Порт PostgreSQL (за замовчуванням 5432)
  user: 'app_user',            // Ім'я користувача БД
  password: 'secure_password', // Пароль
  database: 'myapp_production', // Назва бази даних
  
  // Налаштування пулу
  max: 20,                     // Макс. кількість з'єднань у пулі
  min: 5,                      // Мін. кількість підтримуваних з'єднань
  idleTimeoutMillis: 30000,    // Закривати неактивні з'єднання через 30 сек
  connectionTimeoutMillis: 2000, // Таймаут очікування доступного з'єднання
  
  // SSL (для production)
  ssl: {
    rejectUnauthorized: false, // Для самопідписаних сертифікатів
  },
};
```

::field-group

::field{name="host" type="string"}
Адреса сервера PostgreSQL. Може бути IP-адресою (`192.168.1.100`) або доменним ім'ям (`db.example.com`). Для локальної розробки використовуйте `localhost` або `127.0.0.1`.

::

::field{name="port" type="number"}
TCP-порт, на якому слухає PostgreSQL. За замовчуванням `5432`. Якщо ви використовуєте Docker, переконайтеся, що порт прокинутий (`-p 5432:5432`).

::

::field{name="user" type="string"}
Ім'я користувача бази даних. У production-системах **ніколи** не використовуйте суперкористувача `postgres` — створіть окремого користувача з обмеженими правами через `CREATE ROLE`.

::

::field{name="password" type="string"}
Пароль користувача. У найпростіших випадках це текстовий рядок, але для Enterprise-систем рекомендується інтеграція з системами керування секретами (AWS Secrets Manager, HashiCorp Vault).

::

::field{name="database" type="string"}
Назва бази даних, до якої підключається застосунок. Одна PostgreSQL-інстанція може містити кілька баз даних, ізольованих одна від одної.

::

::field{name="max" type="number"}
Максимальна кількість одночасних з'єднань у пулі. Якщо всі з'єднання зайняті, новий запит чекатиме або викине помилку після `connectionTimeoutMillis`. Типові значення: 10–50 залежно від навантаження.

::

::field{name="idleTimeoutMillis" type="number"}
Час у мілісекундах, після якого неактивне з'єднання закривається. Це запобігає накопиченню «мертвих» з'єднань, якщо навантаження різко впало.

::

::field{name="connectionTimeoutMillis" type="number"}
Максимальний час очікування, поки з'явиться вільне з'єднання у пулі. Якщо за цей час з'єднання не звільнилося, викидається помилка `TimeoutError`.

::

::

### Налаштування SSL для безпечного з'єднання

У production-середовищі всі з'єднання з базою даних мають бути зашифрованими через SSL/TLS (*Transport Layer Security*). Це особливо критично, якщо база даних розташована у віддаленому дата-центрі або хмарному середовищі (AWS RDS, Google Cloud SQL, Azure Database).

**Рівні SSL-режимів у PostgreSQL:**

| Режим               | Опис                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------- |
| `disable`           | SSL не використовується. З'єднання передається відкритим текстом.                     |
| `allow`             | Спочатку спроба без SSL, якщо не вдається — спроба з SSL.                             |
| `prefer`            | Спочатку спроба з SSL, якщо не вдається — без SSL (за замовчуванням).                 |
| `require`           | Обов'язковий SSL. Якщо сервер не підтримує — з'єднання відхиляється.                  |
| `verify-ca`         | SSL + перевірка, що сертифікат підписаний довіреним центром сертифікації (*CA*).      |
| `verify-full`       | SSL + перевірка CA + перевірка, що hostname у сертифікаті відповідає серверу.         |

**Приклад конфігурації із самопідписаним сертифікатом:**

```typescript [ssl-config.ts]
import { Pool } from 'pg';
import * as fs from 'fs';

const pool = new Pool({
  host: 'db.example.com',
  port: 5432,
  user: 'app_user',
  password: process.env.DB_PASSWORD,
  database: 'production_db',
  ssl: {
    rejectUnauthorized: true, // Вимагати валідний сертифікат
    ca: fs.readFileSync('./certs/ca-certificate.crt').toString(), // Кореневий CA
    key: fs.readFileSync('./certs/client-key.pem').toString(),    // Приватний ключ клієнта
    cert: fs.readFileSync('./certs/client-cert.pem').toString(),  // Сертифікат клієнта
  },
});
```

::caution

Налаштування `rejectUnauthorized: false` відключає перевірку сертифіката, що робить з'єднання вразливим до атак типу *man-in-the-middle* (*MITM*). Використовуйте це налаштування лише у контрольованому локальному середовищі або для тестування!

::

### Обробка помилок підключення

При спробі з'єднання можуть виникнути різні помилки: мережевий таймаут, невірні credentials, недоступність сервера БД. Важливо перехоплювати ці помилки та надавати зрозумілі повідомлення розробнику або логувати їх для подальшого аналізу.

```typescript [error-handling.ts]
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

async function testConnection() {
  try {
    const client = await pool.connect();
    console.log('✅ З\'єднання успішно встановлено');
    
    const result = await client.query('SELECT current_database(), version()');
    console.log('Поточна база:', result.rows[0].current_database);
    console.log('Версія PostgreSQL:', result.rows[0].version);
    
    client.release(); // Повертаємо з'єднання у пул
  } catch (error) {
    if (error instanceof Error) {
      console.error('❌ Помилка підключення:', error.message);
      
      // Аналіз типу помилки
      if (error.message.includes('ENOTFOUND')) {
        console.error('Сервер БД недоступний. Перевірте host та DNS.');
      } else if (error.message.includes('authentication failed')) {
        console.error('Невірні credentials (user/password).');
      } else if (error.message.includes('ECONNREFUSED')) {
        console.error('PostgreSQL не запущено або не слухає на вказаному порту.');
      }
    }
    process.exit(1); // Зупиняємо процес при критичній помилці
  }
}

testConnection();
```

::accordion

::accordion-item{label="❓ Чому важливо викликати client.release() після використання з'єднання?" icon="i-lucide-help-circle"}

Метод `release()` повертає з'єднання назад у пул, роблячи його доступним для інших запитів. Якщо ви забудете викликати `release()`, з'єднання залишиться «заблокованим» (*checked out*), і коли кількість таких з'єднань досягне параметра `max`, нові запити почнуть чекати або падати з таймаутом. Це класичний приклад витоку ресурсів (*resource leak*) у Node.js застосунках.

::

::accordion-item{label="❓ Як перевірити, скільки з'єднань зараз активно у пулі?" icon="i-lucide-help-circle"}

Об'єкт `Pool` має публічні властивості для моніторингу стану:

```typescript
console.log('Всього з\'єднань:', pool.totalCount);
console.log('Активних (зайнятих):', pool.totalCount - pool.idleCount);
console.log('Вільних (idle):', pool.idleCount);
console.log('Очікують у черзі:', pool.waitingCount);
```

Ці метрики корисні для налаштування розміру пулу та діагностики bottleneck'ів.

::

::

---

## Виконання SQL запитів

### Метод `query()` для виконання запитів


Основний метод для виконання SQL-команд — це `query()`, який приймає текст запиту та опціональні параметри. Цей метод повертає `Promise`, що резолвиться в об'єкт `QueryResult` із полями `rows` (масив результатів) та `rowCount` (кількість оброблених рядків).

**Базовий приклад SELECT-запиту:**

```typescript [simple-query.ts]
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function getAllUsers() {
  const result = await pool.query('SELECT id, email, created_at FROM users');
  
  console.log('Знайдено користувачів:', result.rowCount);
  
  result.rows.forEach(user => {
    console.log(`ID: ${user.id}, Email: ${user.email}`);
  });
}

getAllUsers();
```

**Структура об'єкта `QueryResult`:**

```typescript
interface QueryResult<T = any> {
  rows: T[];           // Масив рядків результату
  rowCount: number;    // Кількість рядків (для INSERT/UPDATE/DELETE)
  command: string;     // Тип команди: SELECT, INSERT, UPDATE тощо
  oid: number;         // Object ID (для INSERT у таблиці з OID)
  fields: FieldDef[];  // Метадані колонок (назва, тип, розмір)
}
```

### Параметризовані запити (Prepared Statements)

**Найважливіше правило безпеки: ніколи не конкатенуйте користувацький ввід безпосередньо у SQL-рядок!** Це призводить до вразливості SQL-ін'єкції (*SQL injection*), яка дозволяє зловмиснику виконати довільні команди у вашій базі даних.

::warning

**Небезпечний код (вразливий до SQL injection):**

```typescript
// ❌ НІКОЛИ ТАК НЕ РОБІТЬ!
const email = userInput; // Наприклад: "admin@test.com' OR '1'='1"
const query = `SELECT * FROM users WHERE email = '${email}'`;
await pool.query(query);
```

Якщо зловмисник передасть `email = "' OR '1'='1"`, запит перетвориться на:

```sql
SELECT * FROM users WHERE email = '' OR '1'='1'
```

Умова `'1'='1'` завжди істинна, тому буде повернуто всі рядки таблиці.

::

**Правильний підхід — параметризовані запити:**

Драйвер `pg` підтримує плейсхолдери у форматі `$1`, `$2`, `$3` тощо, куди підставляються значення з масиву параметрів. PostgreSQL автоматично екранує (*escapes*) спеціальні символи, запобігаючи ін'єкціям.

```typescript [parameterized-query.ts]
async function getUserByEmail(email: string) {
  const query = 'SELECT id, email, created_at FROM users WHERE email = $1';
  const values = [email];
  
  const result = await pool.query(query, values);
  
  if (result.rowCount === 0) {
    console.log('Користувача не знайдено');
    return null;
  }
  
  return result.rows[0];
}

// Використання:
const user = await getUserByEmail('test@example.com');
```

**Кілька параметрів:**

```typescript [multiple-params.ts]
async function createUser(email: string, name: string, age: number) {
  const query = `
    INSERT INTO users (email, name, age, created_at)
    VALUES ($1, $2, $3, NOW())
    RETURNING id, email, created_at
  `;
  const values = [email, name, age];
  
  const result = await pool.query(query, values);
  return result.rows[0]; // Повертає вставлений рядок
}

const newUser = await createUser('john@example.com', 'John Doe', 28);
console.log('Створено користувача з ID:', newUser.id);
```

::tip

Ключове слово `RETURNING` у PostgreSQL дозволяє отримати значення вставленого/оновленого рядка одразу після операції, без необхідності виконувати додатковий SELECT-запит. Це значно зменшує кількість round-trip'ів до БД.

::

### Захист від SQL injection: додаткові міркування

Навіть при використанні параметризованих запитів існують сценарії, коли розробники можуть допустити помилку:

1. **Динамічні назви таблиць або колонок:** Плейсхолдери `$1` працюють лише для **значень**, а не для ідентифікаторів (назв таблиць, колонок). Якщо вам потрібно динамічно підставити назву таблиці, використовуйте білий список (*whitelist*) дозволених значень.

```typescript
// ❌ Небезпечно
const tableName = userInput; // Може бути "users; DROP TABLE users; --"
await pool.query(`SELECT * FROM ${tableName}`);

// ✅ Безпечно
const allowedTables = ['users', 'posts', 'comments'];
if (!allowedTables.includes(userInput)) {
  throw new Error('Invalid table name');
}
await pool.query(`SELECT * FROM ${userInput}`);
```

2. **ORDER BY та LIMIT:** Ці конструкції також не можуть використовувати параметри напряму. Застосуйте валідацію або бібліотеки query builder (наприклад, `slonik` або `knex`).

### Обробка результатів запиту

Результат запиту `SELECT` — це завжди масив об'єктів, де ключами є назви колонок. PostgreSQL повертає типи у форматі JavaScript (числа, рядки, дати, JSON).

```typescript [result-processing.ts]
interface User {
  id: number;
  email: string;
  created_at: Date;
  metadata: { role: string; verified: boolean };
}

async function getUsersWithMetadata(): Promise<User[]> {
  const result = await pool.query<User>(`
    SELECT id, email, created_at, metadata
    FROM users
    WHERE metadata->>'role' = 'admin'
  `);
  
  return result.rows;
}

const admins = await getUsersWithMetadata();
admins.forEach(admin => {
  console.log(`Admin: ${admin.email}, Verified: ${admin.metadata.verified}`);
});
```

::note

PostgreSQL підтримує нативні JSON-типи (`json` та `jsonb`). Оператор `->` дозволяє отримати значення за ключем, а `->>` повертає текстове представлення. У TypeScript ви можете типізувати структуру JSON-поля через інтерфейс.

::

---

## Connection Pooling: глибинний розбір

### Що таке connection pool і навіщо він потрібен

Встановлення нового TCP-з'єднання з базою даних — це дорога операція, яка включає:

1. Відкриття сокета та TCP handshake (3 пакети).
2. Автентифікацію користувача (обчислення хешу пароля, перевірка у `pg_authid`).
3. Ініціалізацію сесії (завантаження налаштувань, перевірка привілеїв).

У високонавантаженому веб-застосунку, де обробляється 1000 запитів на секунду, відкриття нового з'єднання для кожного запиту призвело б до колосальних накладних витрат. Саме тому використовується **пул з'єднань** — механізм багаторазового використання вже відкритих сокетів.

**Принцип роботи:**

1. При ініціалізації `Pool` відкривається мінімальна кількість з'єднань (параметр `min`).
2. Коли надходить запит, пул надає вільне з'єднання. Якщо всі зайняті, відкривається нове (до досягнення `max`).
3. Після завершення запиту з'єднання не закривається, а повертається у пул та переходить у стан `idle` (*очікування*).
4. Якщо з'єднання залишається неактивним протягом `idleTimeoutMillis`, воно закривається для економії ресурсів.

::plant-uml{alt="Життєвий цикл з'єднання у пулі"}

```plantuml
@startuml
skinparam style plain
skinparam backgroundColor #FFFFFF

[*] --> Closed : Pool створено
Closed --> Connecting : pool.connect()
Connecting --> Idle : Успішна автентифікація
Idle --> Active : Запит query()
Active --> Idle : Запит завершено, client.release()
Idle --> Idle : Очікування нових запитів
Idle --> Closed : Таймаут (idleTimeout)
Active --> Closed : Помилка з'єднання (network error)
Closed --> [*]

note right of Idle #FEF3C7
  З'єднання залишається відкритим
  та готовим до миттєвого використання
end note

@enduml
```

::

### Конфігурація пулу з'єднань


Правильна конфігурація пулу критично впливає на продуктивність та стабільність застосунку. Розглянемо ключові параметри та їх вплив:

```typescript [pool-config-advanced.ts]
import { Pool, PoolConfig } from 'pg';

const config: PoolConfig = {
  // Базові параметри
  connectionString: process.env.DATABASE_URL,
  
  // === Розмір пулу ===
  min: 5,  // Мінімум підтримуваних з'єднань (завжди відкриті)
  max: 20, // Максимум одночасних з'єднань
  
  // === Таймаути ===
  connectionTimeoutMillis: 5000,  // Макс. час очікування вільного з'єднання
  idleTimeoutMillis: 30000,       // Закривати idle з'єднання через 30 сек
  
  // === Обробка помилок ===
  // Функція, що викликається при помилці на idle-з'єднанні
  on: {
    error: (err, client) => {
      console.error('Несподівана помилка на idle-з\'єднанні:', err.message);
      // Пул автоматично видалить проблемне з'єднання
    },
  },
  
  // === Розширені налаштування ===
  application_name: 'myapp_api', // Ім'я застосунку (видно у pg_stat_activity)
  statement_timeout: 10000,       // Скасувати запит, якщо виконується > 10 сек
  query_timeout: 5000,            // Таймаут для client.query()
};

const pool = new Pool(config);
```

**Вибір розміру пулу: формула Хікарі (*HikariCP formula*):**

Існує емпірична формула для розрахунку оптимального розміру пулу:

::math-formula

\text{pool size} = \frac{\text{available cores} \times 2}{1}  + \text{effective spindle count}

::

Для типового веб-сервера з 4 ядрами CPU та SSD-диском (ефективно необмежена кількість «шпинделів»):

::math-formula

\text{pool size} = 4 \times 2 + 1 = 9

::

Проте у реальності розмір залежить від природи запитів:

- Якщо більшість запитів — прості SELECT на індексах (*read-heavy workload*): `max = 10–20`.
- Якщо багато складних JOIN або агрегацій (*CPU-bound*): `max = 5–10`.
- Якщо запити блокуються на записі (*write-heavy with locks*): збільшуйте пул обережно, щоб уникнути конкуренції за блокування (*lock contention*).

::tip

Використовуйте моніторинг `pg_stat_activity` для аналізу кількості активних з'єднань:

```sql
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
```

Якщо ви бачите багато з'єднань у стані `idle in transaction`, це сигнал про витік ресурсів — десь забули завершити транзакцію.

::

### Управління життєвим циклом з'єднань

Для явного керування з'єднанням використовуйте метод `pool.connect()`, який повертає `PoolClient` — обгортку над фізичним з'єднанням.

```typescript [manual-client.ts]
import { Pool, PoolClient } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function performComplexOperation() {
  const client: PoolClient = await pool.connect();
  
  try {
    // Тепер ми володіємо ексклюзивним з'єднанням
    await client.query('BEGIN'); // Початок транзакції
    
    const result1 = await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [100, 1]
    );
    
    const result2 = await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [100, 2]
    );
    
    await client.query('COMMIT'); // Фіксація змін
    console.log('Транзакція успішно завершена');
    
  } catch (error) {
    await client.query('ROLLBACK'); // Відкат при помилці
    console.error('Помилка транзакції, виконано rollback:', error);
    throw error;
    
  } finally {
    client.release(); // КРИТИЧНО: повертаємо з'єднання у пул!
  }
}

performComplexOperation();
```

::warning

Якщо ви забудете викликати `client.release()` у блоці `finally`, з'єднання назавжди залишиться «захопленим», і через деякий час пул вичерпається. Це призведе до помилки `TimeoutError: ResourceRequest timed out`.

::

### Best practices для production

**1. Graceful shutdown:** При зупинці застосунку коректно закривайте пул, щоб уникнути обриву активних запитів.

```typescript [graceful-shutdown.ts]
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// Обробка сигналів завершення
process.on('SIGTERM', async () => {
  console.log('Отримано SIGTERM, закриваємо пул з\'єднань...');
  await pool.end(); // Чекає завершення всіх активних запитів
  console.log('Пул закрито, вихід.');
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('Отримано SIGINT (Ctrl+C), закриваємо пул...');
  await pool.end();
  process.exit(0);
});
```

**2. Моніторинг метрик пулу:** Інтегруйте метрики у систему спостереження (Prometheus, Datadog).

```typescript [metrics.ts]
function logPoolMetrics(pool: Pool) {
  setInterval(() => {
    console.log({
      totalCount: pool.totalCount,     // Всього з'єднань у пулі
      idleCount: pool.idleCount,       // Вільних (idle)
      waitingCount: pool.waitingCount, // Очікують у черзі
    });
  }, 10000); // Кожні 10 секунд
}

logPoolMetrics(pool);
```

**3. Connection health checks:** Періодично перевіряйте, що з'єднання не «протухли» (*stale*).

```typescript [health-check.ts]
async function checkDatabaseHealth(pool: Pool): Promise<boolean> {
  try {
    const result = await pool.query('SELECT 1 AS alive');
    return result.rows[0].alive === 1;
  } catch (error) {
    console.error('Database health check failed:', error);
    return false;
  }
}

// Використання у Kubernetes liveness probe
app.get('/health', async (req, res) => {
  const isHealthy = await checkDatabaseHealth(pool);
  res.status(isHealthy ? 200 : 503).json({ database: isHealthy });
});
```

---

## CRUD операції через raw SQL

Тепер, коли ми розібралися з підключенням та пулами, перейдемо до практичних прикладів основних операцій з даними: створення (*Create*), читання (*Read*), оновлення (*Update*) та видалення (*Delete*).

### CREATE: INSERT запити

Операція `INSERT` додає нові рядки у таблицю. PostgreSQL підтримує два синтаксиси: вставка одного рядка та масова вставка (*bulk insert*).

**Вставка одного рядка:**

```typescript [insert-single.ts]
interface User {
  id: number;
  email: string;
  name: string;
  created_at: Date;
}

async function createUser(email: string, name: string): Promise<User> {
  const query = `
    INSERT INTO users (email, name, created_at)
    VALUES ($1, $2, NOW())
    RETURNING id, email, name, created_at
  `;
  
  const result = await pool.query<User>(query, [email, name]);
  return result.rows[0];
}

const user = await createUser('alice@example.com', 'Alice Smith');
console.log('Створено:', user);
```

**Масова вставка (bulk insert):**

Для вставки кількох рядків одним запитом використовуйте синтаксис `VALUES (...), (...), (...)`. Це значно швидше, ніж виконання окремих `INSERT` у циклі.

```typescript [bulk-insert.ts]
async function createMultipleUsers(users: Array<{ email: string; name: string }>) {
  // Генеруємо плейсхолдери: ($1, $2), ($3, $4), ($5, $6)
  const values: any[] = [];
  const placeholders = users.map((user, index) => {
    values.push(user.email, user.name);
    const offset = index * 2;
    return `($${offset + 1}, $${offset + 2}, NOW())`;
  }).join(', ');
  
  const query = `
    INSERT INTO users (email, name, created_at)
    VALUES ${placeholders}
    RETURNING id, email, name
  `;
  
  const result = await pool.query(query, values);
  return result.rows;
}

const newUsers = await createMultipleUsers([
  { email: 'bob@example.com', name: 'Bob Johnson' },
  { email: 'charlie@example.com', name: 'Charlie Brown' },
]);

console.log('Створено користувачів:', newUsers.length);
```

::tip

Для дуже великих масових вставок (>1000 рядків) розгляньте використання команди `COPY` PostgreSQL, яка працює швидше за `INSERT`. Драйвер `pg` підтримує це через метод `copyFrom()`.

::

### READ: SELECT з фільтрацією та JOIN

Запити `SELECT` можуть варіюватися від простих вибірок до складних агрегацій із кількома JOIN.


**Проста фільтрація:**

```typescript [select-filter.ts]
async function getUsersByDomain(domain: string) {
  const query = `
    SELECT id, email, name, created_at
    FROM users
    WHERE email LIKE $1
    ORDER BY created_at DESC
  `;
  
  const result = await pool.query(query, [`%@${domain}`]);
  return result.rows;
}

const gmailUsers = await getUsersByDomain('gmail.com');
console.log('Користувачів з Gmail:', gmailUsers.length);
```

**JOIN між таблицями:**

Припустимо, у нас є дві таблиці: `users` та `posts`. Одному користувачу може належати багато постів (*one-to-many*).

```typescript [select-join.ts]
interface UserWithPosts {
  user_id: number;
  user_email: string;
  post_id: number | null;
  post_title: string | null;
  post_created_at: Date | null;
}

async function getUsersWithPosts(): Promise<UserWithPosts[]> {
  const query = `
    SELECT 
      u.id AS user_id,
      u.email AS user_email,
      p.id AS post_id,
      p.title AS post_title,
      p.created_at AS post_created_at
    FROM users u
    LEFT JOIN posts p ON p.user_id = u.id
    ORDER BY u.id, p.created_at DESC
  `;
  
  const result = await pool.query<UserWithPosts>(query);
  return result.rows;
}
```

::note

Використання `LEFT JOIN` гарантує, що користувачі без постів також будуть включені у результат (із `NULL` у полях посту). Якщо вам потрібні лише користувачі, які мають пости, використовуйте `INNER JOIN`.

::

### UPDATE: оновлення записів

Операція `UPDATE` змінює існуючі рядки. Критично важливо завжди використовувати умову `WHERE`, щоб не оновити всі рядки таблиці випадково.

```typescript [update.ts]
async function updateUserEmail(userId: number, newEmail: string): Promise<void> {
  const query = `
    UPDATE users
    SET email = $1, updated_at = NOW()
    WHERE id = $2
  `;
  
  const result = await pool.query(query, [newEmail, userId]);
  
  if (result.rowCount === 0) {
    throw new Error(`Користувача з ID ${userId} не знайдено`);
  }
  
  console.log(`Оновлено email для користувача ${userId}`);
}

await updateUserEmail(42, 'newemail@example.com');
```

**Умовне оновлення з перевіркою версії (Optimistic Locking):**

Для запобігання race condition (*стану гонки*) при одночасному оновленні можна використовувати поле версії:

```typescript [optimistic-lock.ts]
async function updateWithVersion(userId: number, newName: string, expectedVersion: number) {
  const query = `
    UPDATE users
    SET name = $1, version = version + 1, updated_at = NOW()
    WHERE id = $2 AND version = $3
    RETURNING version
  `;
  
  const result = await pool.query(query, [newName, userId, expectedVersion]);
  
  if (result.rowCount === 0) {
    throw new Error('Conflict: запис було змінено іншим процесом');
  }
  
  return result.rows[0].version;
}
```

### DELETE: видалення записів

Операція `DELETE` видаляє рядки з таблиці. Як і у випадку з `UPDATE`, завжди використовуйте `WHERE`, якщо не хочете видалити всю таблицю.

```typescript [delete.ts]
async function deleteUser(userId: number): Promise<boolean> {
  const query = 'DELETE FROM users WHERE id = $1';
  const result = await pool.query(query, [userId]);
  
  return result.rowCount > 0; // true, якщо щось було видалено
}

const deleted = await deleteUser(99);
console.log(deleted ? 'Користувача видалено' : 'Користувача не знайдено');
```

**Каскадне видалення через FK:**

Якщо у вас налаштовані зовнішні ключі (*foreign keys*) з опцією `ON DELETE CASCADE`, видалення батьківського рядка автоматично видалить пов'язані дочірні рядки.

```sql
-- Визначення FK із каскадним видаленням
ALTER TABLE posts
ADD CONSTRAINT fk_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

Тепер при `DELETE FROM users WHERE id = 42` усі пости цього користувача також будуть видалені автоматично.

### Транзакції через `BEGIN`, `COMMIT`, `ROLLBACK`

Транзакція — це послідовність операцій, які або виконуються повністю, або відкочуються цілком у разі помилки. Це фундаментальна властивість ACID (*Atomicity, Consistency, Isolation, Durability*).

**Базовий приклад транзакції:**

```typescript [transaction.ts]
async function transferMoney(fromUserId: number, toUserId: number, amount: number) {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    
    // Зняти гроші з рахунку відправника
    const debitResult = await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE user_id = $2 RETURNING balance',
      [amount, fromUserId]
    );
    
    if (debitResult.rows[0].balance < 0) {
      throw new Error('Insufficient funds');
    }
    
    // Додати гроші на рахунок отримувача
    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE user_id = $2',
      [amount, toUserId]
    );
    
    await client.query('COMMIT');
    console.log(`Переказано ${amount} від ${fromUserId} до ${toUserId}`);
    
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Помилка транзакції, виконано rollback:', error);
    throw error;
    
  } finally {
    client.release();
  }
}

await transferMoney(1, 2, 500);
```

::caution

Транзакція блокує (*lock*) рядки, які вона змінює, до моменту `COMMIT` або `ROLLBACK`. Якщо ви виконуєте довгу транзакцію (наприклад, із зовнішніми HTTP-запитами всередині), інші запити можуть чекати на звільнення блокувань. Це призводить до проблем продуктивності (*lock contention*).

::

**Рівні ізоляції транзакцій:**

PostgreSQL підтримує 4 рівні ізоляції згідно зі стандартом SQL:

| Рівень               | Опис                                                                                      | Коли використовувати                 |
| -------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------ |
| `READ UNCOMMITTED`   | Не підтримується у PostgreSQL (еквівалент `READ COMMITTED`)                               | —                                    |
| `READ COMMITTED`     | За замовчуванням. Читає тільки зафіксовані дані.                                          | Більшість веб-застосунків            |
| `REPEATABLE READ`    | Гарантує, що повторні SELECT у межах транзакції повертають ті самі рядки.                 | Фінансові операції, звіти            |
| `SERIALIZABLE`       | Найсуворіший рівень. Емулює послідовне виконання транзакцій.                              | Критичні операції (рідко використовується) |

**Встановлення рівня ізоляції:**

```typescript
await client.query('BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ');
```

::accordion

::accordion-item{label="❓ Що станеться, якщо мережа впаде під час транзакції?" icon="i-lucide-help-circle"}

Якщо TCP-з'єднання обривається до того, як клієнт встиг надіслати `COMMIT`, PostgreSQL автоматично виконує `ROLLBACK` для всіх незафіксованих змін. Це гарантується протоколом БД. Проте важливо правильно обробляти мережеві помилки на стороні застосунку, щоб уникнути «напіввідкритих» транзакцій (*half-open transactions*).

::

::accordion-item{label="❓ Чи можна вкладати транзакції одна в одну?" icon="i-lucide-help-circle"}

PostgreSQL не підтримує справжні вкладені транзакції (*nested transactions*), але надає механізм **savepoint** (*точок збереження*) для часткового відкату:

```typescript
await client.query('BEGIN');
await client.query('SAVEPOINT my_savepoint');
// ... операції
await client.query('ROLLBACK TO SAVEPOINT my_savepoint'); // Частковий відкат
await client.query('COMMIT');
```

Це корисно для складних бізнес-логік, де потрібно відкотити частину операцій без скасування всієї транзакції.

::

::

---

## Обробка помилок

### Try-catch блоки для асинхронних запитів

Будь-яка операція з базою даних може завершитися помилкою: мережевий збій, порушення обмежень (*constraint violation*), таймаут. Критично важливо обробляти ці помилки, щоб уникнути падіння застосунку.

```typescript [error-handling-advanced.ts]
import { DatabaseError } from 'pg';

async function createUserSafely(email: string, name: string) {
  try {
    const query = 'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id';
    const result = await pool.query(query, [email, name]);
    return result.rows[0];
    
  } catch (error) {
    if (error instanceof DatabaseError) {
      // Обробка специфічних помилок PostgreSQL
      switch (error.code) {
        case '23505': // unique_violation
          throw new Error(`Email ${email} вже зареєстрований`);
          
        case '23502': // not_null_violation
          throw new Error(`Пропущено обов'язкове поле: ${error.column}`);
          
        case '23503': // foreign_key_violation
          throw new Error(`Порушення FK: ${error.detail}`);
          
        default:
          console.error('Database error:', error.code, error.message);
          throw error;
      }
    }
    
    // Мережеві або інші помилки
    console.error('Unexpected error:', error);
    throw error;
  }
}
```

### Типи помилок PostgreSQL

PostgreSQL повертає коди помилок у форматі `SQLSTATE` (5-символьний код). Найпоширеніші:


| Код    | Назва                         | Опис                                             |
| ------ | ----------------------------- | ------------------------------------------------ |
| `23505`| `unique_violation`            | Порушення обмеження унікальності (UNIQUE)        |
| `23502`| `not_null_violation`          | Спроба вставити NULL у NOT NULL колонку          |
| `23503`| `foreign_key_violation`       | Порушення зовнішнього ключа (FK)                 |
| `42P01`| `undefined_table`             | Таблиця не існує                                 |
| `42703`| `undefined_column`            | Колонка не існує                                 |
| `57014`| `query_canceled`              | Запит було скасовано (таймаут або `pg_cancel_backend`) |
| `08006`| `connection_failure`          | Обрив з'єднання з БД                             |
| `53300`| `too_many_connections`        | Вичерпано ліміт одночасних з'єднань              |

::tip

Повний список кодів помилок доступний у офіційній документації PostgreSQL: [Appendix A. PostgreSQL Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html).

::

### Graceful shutdown та закриття з'єднань

При зупинці застосунку важливо коректно завершити всі активні з'єднання, щоб уникнути втрати даних або пошкодження стану БД. Розглянемо повний приклад із обробкою сигналів завершення:

```typescript [shutdown.ts]
import { Pool } from 'pg';
import * as http from 'http';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const server = http.createServer(async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ time: result.rows[0].now }));
  } catch (error) {
    res.writeHead(500);
    res.end('Database error');
  }
});

server.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});

// Graceful shutdown
async function shutdown(signal: string) {
  console.log(`\nОтримано сигнал ${signal}, починаємо graceful shutdown...`);
  
  // 1. Зупиняємо прийом нових HTTP-запитів
  server.close(() => {
    console.log('HTTP-сервер зупинено');
  });
  
  // 2. Чекаємо завершення активних запитів до БД та закриваємо пул
  try {
    await pool.end();
    console.log('Пул з\'єднань закрито');
  } catch (error) {
    console.error('Помилка при закритті пулу:', error);
  }
  
  process.exit(0);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
```

::note

У Kubernetes або Docker-середовищах сигнал `SIGTERM` надсилається перед force-kill (`SIGKILL`). Якщо ваш застосунок не встигає завершити graceful shutdown за 30 секунд (за замовчуванням), контейнер буде примусово зупинено. Налаштуйте `terminationGracePeriodSeconds` у Pod-специфікації, якщо потрібен більший таймаут.

::

---

## Практичні приклади

### Створення простого CRUD сервісу

Зведемо всі набуті знання у повноцінний модуль для керування користувачами:

```typescript [user-service.ts]
import { Pool, PoolClient } from 'pg';

interface User {
  id: number;
  email: string;
  name: string;
  created_at: Date;
  updated_at: Date;
}

interface CreateUserDto {
  email: string;
  name: string;
}

interface UpdateUserDto {
  name?: string;
  email?: string;
}

export class UserService {
  constructor(private pool: Pool) {}

  async create(dto: CreateUserDto): Promise<User> {
    const query = `
      INSERT INTO users (email, name, created_at, updated_at)
      VALUES ($1, $2, NOW(), NOW())
      RETURNING id, email, name, created_at, updated_at
    `;
    
    const result = await this.pool.query<User>(query, [dto.email, dto.name]);
    return result.rows[0];
  }

  async findById(id: number): Promise<User | null> {
    const query = 'SELECT * FROM users WHERE id = $1';
    const result = await this.pool.query<User>(query, [id]);
    return result.rows[0] || null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const query = 'SELECT * FROM users WHERE email = $1';
    const result = await this.pool.query<User>(query, [email]);
    return result.rows[0] || null;
  }

  async findAll(limit = 100, offset = 0): Promise<User[]> {
    const query = `
      SELECT * FROM users
      ORDER BY created_at DESC
      LIMIT $1 OFFSET $2
    `;
    const result = await this.pool.query<User>(query, [limit, offset]);
    return result.rows;
  }

  async update(id: number, dto: UpdateUserDto): Promise<User | null> {
    const fields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    if (dto.name !== undefined) {
      fields.push(`name = $${paramIndex++}`);
      values.push(dto.name);
    }

    if (dto.email !== undefined) {
      fields.push(`email = $${paramIndex++}`);
      values.push(dto.email);
    }

    if (fields.length === 0) {
      return this.findById(id); // Нічого не змінено
    }

    fields.push(`updated_at = NOW()`);
    values.push(id);

    const query = `
      UPDATE users
      SET ${fields.join(', ')}
      WHERE id = $${paramIndex}
      RETURNING id, email, name, created_at, updated_at
    `;

    const result = await this.pool.query<User>(query, values);
    return result.rows[0] || null;
  }

  async delete(id: number): Promise<boolean> {
    const query = 'DELETE FROM users WHERE id = $1';
    const result = await this.pool.query(query, [id]);
    return result.rowCount > 0;
  }

  // Приклад транзакції: переміщення користувача в архів
  async archive(id: number): Promise<void> {
    const client: PoolClient = await this.pool.connect();

    try {
      await client.query('BEGIN');

      // Копіюємо користувача в архівну таблицю
      await client.query(`
        INSERT INTO users_archive (id, email, name, created_at, archived_at)
        SELECT id, email, name, created_at, NOW()
        FROM users
        WHERE id = $1
      `, [id]);

      // Видаляємо з основної таблиці
      await client.query('DELETE FROM users WHERE id = $1', [id]);

      await client.query('COMMIT');
      console.log(`Користувача ${id} переміщено в архів`);

    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Помилка архівування:', error);
      throw error;

    } finally {
      client.release();
    }
  }
}

// Використання:
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const userService = new UserService(pool);

(async () => {
  const user = await userService.create({
    email: 'test@example.com',
    name: 'Test User',
  });

  console.log('Створено:', user);

  const found = await userService.findById(user.id);
  console.log('Знайдено:', found);

  await userService.update(user.id, { name: 'Updated Name' });
  console.log('Оновлено');

  await userService.archive(user.id);
  console.log('Заархівовано');
})();
```

### Використання у NestJS без ORM

У NestJS можна використовувати драйвер `pg` напряму, без TypeORM. Це корисно, коли вам потрібен повний контроль над SQL або коли проєкт має специфічні вимоги до продуктивності.

**Крок 1: Створення Database Module**

```typescript [database.module.ts]
import { Module, Global } from '@nestjs/common';
import { Pool } from 'pg';

export const PG_CONNECTION = 'PG_CONNECTION';

@Global()
@Module({
  providers: [
    {
      provide: PG_CONNECTION,
      useFactory: () => {
        const pool = new Pool({
          connectionString: process.env.DATABASE_URL,
          max: 20,
          idleTimeoutMillis: 30000,
        });

        pool.on('error', (err) => {
          console.error('Unexpected error on idle client', err);
        });

        return pool;
      },
    },
  ],
  exports: [PG_CONNECTION],
})
export class DatabaseModule {}
```

**Крок 2: Інжекція пулу у сервіс**

```typescript [users.service.ts]
import { Injectable, Inject } from '@nestjs/common';
import { Pool } from 'pg';
import { PG_CONNECTION } from './database.module';

@Injectable()
export class UsersService {
  constructor(@Inject(PG_CONNECTION) private pool: Pool) {}

  async findAll() {
    const result = await this.pool.query('SELECT * FROM users');
    return result.rows;
  }

  async create(email: string, name: string) {
    const query = 'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *';
    const result = await this.pool.query(query, [email, name]);
    return result.rows[0];
  }
}
```

**Крок 3: Використання у контролері**

```typescript [users.controller.ts]
import { Controller, Get, Post, Body } from '@nestjs/common';
import { UsersService } from './users.service';

@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  async findAll() {
    return this.usersService.findAll();
  }

  @Post()
  async create(@Body() body: { email: string; name: string }) {
    return this.usersService.create(body.email, body.name);
  }
}
```

### Коли raw SQL кращий за ORM

Хоча ORM-бібліотеки значно спрощують роботу з даними, існують сценарії, коли використання чистого SQL є кращим вибором:

**1. Складні аналітичні запити:**

```typescript
// Приклад: агрегація з віконними функціями (Window Functions)
const query = `
  SELECT
    user_id,
    email,
    total_orders,
    RANK() OVER (ORDER BY total_orders DESC) as rank
  FROM (
    SELECT
      u.id as user_id,
      u.email,
      COUNT(o.id) as total_orders
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.email
  ) subquery
  WHERE total_orders > 0
  ORDER BY rank
  LIMIT 10
`;
```

Такий запит важко виразити через методи ORM без втрати читабельності або продуктивності.

**2. Масові оновлення з підзапитами:**

```typescript
const query = `
  UPDATE products
  SET discount = 0.15
  WHERE category_id IN (
    SELECT id FROM categories WHERE seasonal = true
  )
`;
```

**3. Використання специфічних можливостей PostgreSQL:**

- Повнотекстовий пошук (`tsvector`, `tsquery`)
- JSON-оператори (`jsonb_path_query`)
- Рекурсивні запити (Recursive CTE)
- Геопросторові запити через PostGIS

```typescript
// Повнотекстовий пошук
const query = `
  SELECT id, title, ts_rank(search_vector, query) as rank
  FROM articles, plainto_tsquery('english', $1) query
  WHERE search_vector @@ query
  ORDER BY rank DESC
  LIMIT 20
`;

const results = await pool.query(query, ['machine learning']);
```

::tip

Загальне правило: використовуйте ORM для стандартних CRUD-операцій та простих JOIN, але переходьте на raw SQL для оптимізації критичних шляхів (*hot paths*) або коли потрібні специфічні можливості БД.

::

---

## Підсумок

У цій лекції ми детально розглянули роботу з реляційними базами даних у Node.js через нативний драйвер `pg`. Ви дізналися:


::card-group

::card{title="✅ Що ви опанували" icon="i-lucide-check-circle"}

- Архітектуру взаємодії Node.js із PostgreSQL через TCP-сокети та протокол Frontend/Backend.
- Різницю між `Client` (одне з'єднання) та `Pool` (пул з'єднань) у контексті високонавантажених застосунків.
- Безпечне виконання SQL-запитів через параметризовані плейсхолдери для запобігання SQL-ін'єкціям.
- Конфігурацію пулів з'єднань: розмір, таймаути, SSL-налаштування для production.
- Реалізацію транзакцій (`BEGIN`, `COMMIT`, `ROLLBACK`) для атомарності операцій.
- Обробку помилок PostgreSQL через коди `SQLSTATE` та graceful shutdown застосунку.

::

::card{title="🚀 Наступні кроки" icon="i-lucide-arrow-right"}

- У наступній лекції ми перейдемо до вивчення ORM (*Object-Relational Mapping*) та познайомимося з TypeORM — потужною бібліотекою для роботи з базами даних через класи та декоратори.
- Ви дізнаєтеся, як TypeORM автоматизує багато рутинних операцій, які ми виконували вручну у цій лекції.
- Проте знання чистого SQL та драйверів залишається критично важливим для розуміння того, що відбувається «під капотом» ORM.

::

::

::accordion

::accordion-item{label="❓ Чи можна використовувати `pg` разом із TypeORM у одному проєкті?" icon="i-lucide-help-circle"}

Так, це розповсюджена практика. TypeORM використовує драйвер `pg` під капотом, але ви можете створити окремий `Pool` для виконання специфічних raw SQL запитів, які важко виразити через QueryBuilder або Entity репозиторії. У цьому випадку переконайтеся, що обидва пули використовують різні ідентифікатори з'єднань або координуються через один пул.

::

::accordion-item{label="❓ Як налаштувати логування всіх SQL-запитів для дебагу?" icon="i-lucide-help-circle"}

Драйвер `pg` не має вбудованого логування запитів, але ви можете створити обгортку (*wrapper*) над методом `query`:

```typescript
const originalQuery = pool.query.bind(pool);
pool.query = (...args: any[]) => {
  console.log('SQL:', args[0]);
  console.log('Params:', args[1]);
  return originalQuery(...args);
};
```

Альтернативно, використовуйте бібліотеку `pg-monitor` для структурованого логування.

::

::accordion-item{label="❓ Що робити, якщо база даних тимчасово недоступна?" icon="i-lucide-help-circle"}

Реалізуйте механізм повторних спроб (*retry logic*) з експоненційною затримкою (*exponential backoff*):

```typescript
async function queryWithRetry(query: string, values: any[], maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await pool.query(query, values);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
      console.log(`Retry ${i + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

Для промислових систем розгляньте використання бібліотек на кшталт `p-retry` або `async-retry`.

::

::

::note

**Корисні ресурси для поглибленого вивчення:**

- [Офіційна документація node-postgres](https://node-postgres.com/)
- [PostgreSQL Documentation: Frontend/Backend Protocol](https://www.postgresql.org/docs/current/protocol.html)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Connection Pooling Best Practices](https://github.com/brianc/node-postgres/wiki/pg.Pool)

::

---

**Ви успішно завершили першу лекцію модуля TypeORM Integration!** Тепер у вас є міцна основа для розуміння роботи з реляційними базами даних на низькому рівні. У наступній лекції ми перейдемо до абстракцій ORM та дізнаємося, як TypeORM спрощує багато операцій, які ви тільки що виконували вручну.