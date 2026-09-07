# ORM та знайомство з TypeORM

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Зрозуміти концепцію Object-Relational Mapping (*ORM*) та її роль у сучасній розробці веб-застосунків.
- Усвідомити переваги та обмеження ORM-бібліотек порівняно з безпосереднім використанням SQL.
- Познайомитися з TypeORM — провідним ORM-рішенням для TypeScript та Node.js екосистеми.
- Навчитися обирати правильний інструмент для роботи з даними залежно від архітектурних вимог проєкту.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **ORM (Object-Relational Mapping):** техніка відображення реляційних таблиць бази даних на об'єкти об'єктно-орієнтованої мови програмування.
- **Entity:** клас TypeScript, що представляє таблицю у базі даних та інкапсулює бізнес-логіку доменної моделі.
- **Repository Pattern:** архітектурний патерн для абстракції доступу до даних через спеціалізовані класи-репозиторії.
- **Active Record vs Data Mapper:** два фундаментальні підходи до організації логіки взаємодії об'єктів із базою даних.

::

::

---

## Що таке ORM: від SQL до об'єктів

### Концепція Object-Relational Mapping

У попередній лекції ми працювали з PostgreSQL через нативний драйвер `pg`, писали SQL-запити вручну та обробляли результати як масиви об'єктів JavaScript. Цей підхід дає повний контроль, але супроводжується значною кількістю повторюваного коду (*boilerplate*): конструювання запитів, валідація параметрів, маппінг результатів на типізовані структури.

**ORM (Object-Relational Mapping)** — це техніка програмування, яка створює «віртуальну об'єктну базу даних» (*virtual object database*) поверх реляційної СУБД. Замість написання SQL-запитів ви працюєте з класами та об'єктами, а ORM автоматично транслює ваші дії у відповідні SQL-команди.

**Приклад без ORM (чистий SQL):**

```typescript
// Створення користувача
const query = 'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *';
const result = await pool.query(query, ['user@example.com', 'John Doe']);
const user = result.rows[0];

// Пошук за email
const findQuery = 'SELECT * FROM users WHERE email = $1';
const findResult = await pool.query(findQuery, ['user@example.com']);
const foundUser = findResult.rows[0];
```

**Той самий код із TypeORM:**

```typescript
// Створення користувача
const user = new User();
user.email = 'user@example.com';
user.name = 'John Doe';
await userRepository.save(user);

// Пошук за email
const foundUser = await userRepository.findOne({
  where: { email: 'user@example.com' }
});
```

Різниця очевидна: код стає декларативним (*declarative*) — ви описуєте **що** потрібно зробити, а не **як** це виконати на рівні SQL.

### Відображення таблиць БД на класи

Кожна таблиця у реляційній базі даних відображається на клас TypeScript, який називається **Entity**. Колонки таблиці стають властивостями класу, а рядки — екземплярами об'єктів.

**Таблиця `users` у PostgreSQL:**

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  age INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Entity клас `User` у TypeORM:**

```typescript
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column({ length: 100 })
  name: string;

  @Column({ nullable: true })
  age?: number;

  @CreateDateColumn()
  created_at: Date;
}
```

TypeORM використовує **декоратори** (*decorators*) — спеціальні анотації, що додають метадані до класів та їх властивостей. Ці метадані зчитуються у runtime та використовуються для автоматичної генерації SQL-запитів.

::note

Декоратори — це експериментальна функція TypeScript (Stage 3 у TC39 proposal), яку потрібно увімкнути у `tsconfig.json`:

```json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

TypeORM покладається на ці налаштування для коректної роботи рефлексії типів (*type reflection*).

::

### Абстракція над SQL запитами

ORM надає кілька рівнів абстракції для роботи з даними:

**1. Репозиторії (*Repositories*):** Високорівневий API для стандартних CRUD-операцій.

```typescript
const userRepository = dataSource.getRepository(User);

// CREATE
const user = userRepository.create({ email: 'test@example.com', name: 'Test' });
await userRepository.save(user);

// READ
const users = await userRepository.find();
const oneUser = await userRepository.findOneBy({ email: 'test@example.com' });

// UPDATE
await userRepository.update({ id: 1 }, { name: 'Updated Name' });

// DELETE
await userRepository.delete({ id: 1 });
```

**2. Query Builder:** Програмний конструктор запитів для складніших сценаріїв.

```typescript
const users = await userRepository
  .createQueryBuilder('user')
  .where('user.age > :age', { age: 18 })
  .andWhere('user.email LIKE :domain', { domain: '%@gmail.com' })
  .orderBy('user.created_at', 'DESC')
  .take(10)
  .getMany();
```

**3. Raw SQL:** Можливість виконати чистий SQL, коли це необхідно.

```typescript
const result = await dataSource.query(
  'SELECT * FROM users WHERE email = $1',
  ['test@example.com']
);
```

::tip

TypeORM не забороняє використання raw SQL. Це гібридний підхід: використовуйте ORM для стандартних операцій та SQL для специфічних оптимізацій. Це найкраще з обох світів.

::

### Історія та еволюція ORM

Концепція ORM виникла у 1990-х роках разом із популяризацією об'єктно-орієнтованого програмування. Першим широковідомим ORM став **Hibernate** для Java (2001), який встановив стандарти, що використовуються досі.

**Еволюція ORM у JavaScript/TypeScript екосистемі:**

::mermaid

```mermaid
timeline
    title Еволюція ORM для Node.js
    2011 : Sequelize<br/>Перший популярний ORM для Node.js<br/>Promise-based API
    2015 : Bookshelf.js<br/>Побудований поверх Knex.js<br/>Акцент на відносини між моделями
    2016 : TypeORM (v0.1)<br/>TypeScript-first підхід<br/>Декоратори та метадані
    2019 : Prisma 2.0<br/>Schema-first генерація типів<br/>Власний Query Engine (Rust)
    2022 : Drizzle ORM<br/>Lightweight, type-safe<br/>Мінімальний runtime overhead
    2023 : TypeORM 0.3.x<br/>ESM підтримка<br/>Покращена продуктивність
```

::

TypeORM з'явився у 2016 році як відповідь на потребу у повноцінному ORM для TypeScript, що підтримує сучасні можливості мови: строгу типізацію (*strict typing*), декоратори та async/await синтаксис.


---

## Навіщо потрібен ORM

### Підвищення продуктивності розробки

Найочевидніша перевага ORM — це **значне скорочення обсягу коду**, який потрібно написати для типових операцій з даними. Замість написання окремих SQL-запитів для кожної операції, ви описуєте структуру даних один раз через Entity класи, а ORM автоматично генерує всі необхідні запити.

**Порівняння обсягу коду для CRUD операцій:**

::code-group

```typescript [Без ORM (pg драйвер)]
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// CREATE
async function createUser(email: string, name: string) {
  const query = 'INSERT INTO users (email, name, created_at) VALUES ($1, $2, NOW()) RETURNING *';
  const result = await pool.query(query, [email, name]);
  return result.rows[0];
}

// READ (один користувач)
async function getUserById(id: number) {
  const query = 'SELECT * FROM users WHERE id = $1';
  const result = await pool.query(query, [id]);
  return result.rows[0] || null;
}

// READ (з фільтрацією)
async function getUsersByDomain(domain: string) {
  const query = 'SELECT * FROM users WHERE email LIKE $1 ORDER BY created_at DESC';
  const result = await pool.query(query, [`%@${domain}`]);
  return result.rows;
}

// UPDATE
async function updateUser(id: number, name: string) {
  const query = 'UPDATE users SET name = $1, updated_at = NOW() WHERE id = $2 RETURNING *';
  const result = await pool.query(query, [name, id]);
  return result.rows[0] || null;
}

// DELETE
async function deleteUser(id: number) {
  const query = 'DELETE FROM users WHERE id = $1';
  const result = await pool.query(query, [id]);
  return result.rowCount > 0;
}

// Приблизно 40+ рядків коду
```

```typescript [З TypeORM]
import { Repository } from 'typeorm';
import { User } from './entities/User';

class UserService {
  constructor(private userRepository: Repository<User>) {}

  // CREATE
  async createUser(email: string, name: string) {
    const user = this.userRepository.create({ email, name });
    return this.userRepository.save(user);
  }

  // READ (один користувач)
  async getUserById(id: number) {
    return this.userRepository.findOneBy({ id });
  }

  // READ (з фільтрацією)
  async getUsersByDomain(domain: string) {
    return this.userRepository
      .createQueryBuilder('user')
      .where('user.email LIKE :pattern', { pattern: `%@${domain}` })
      .orderBy('user.created_at', 'DESC')
      .getMany();
  }

  // UPDATE
  async updateUser(id: number, name: string) {
    await this.userRepository.update({ id }, { name });
    return this.getUserById(id);
  }

  // DELETE
  async deleteUser(id: number) {
    const result = await this.userRepository.delete({ id });
    return result.affected > 0;
  }
}

// Приблизно 25 рядків + Entity визначення (15 рядків)
```

::

Хоча різниця може здаватися невеликою у цьому простому прикладі, вона стає критичною при роботі з:
- Складними зв'язками між таблицями (*relations*: one-to-many, many-to-many).
- Валідацією даних на рівні Entity.
- Каскадним збереженням (*cascade saves*) вкладених об'єктів.
- Автоматичною серіалізацією JSON-полів.

### Type safety у TypeScript

Одна з найсильніших переваг TypeORM — це **повна інтеграція з системою типів TypeScript**. Компілятор перевіряє коректність запитів на етапі компіляції, а не у runtime.

```typescript
const user = await userRepository.findOneBy({ id: 1 });

// ✅ TypeScript знає, що user має типи:
user?.email;      // string
user?.age;        // number | undefined
user?.created_at; // Date

// ❌ Помилка компіляції: властивість не існує
user?.nonExistentField; // Property 'nonExistentField' does not exist on type 'User'

// ✅ Автодоповнення у IDE
await userRepository.findOneBy({
  // IDE показує доступні поля: id, email, name, age, created_at
});
```

**Порівняння з чистим SQL:**

```typescript
// pg драйвер: результат має тип any
const result = await pool.query('SELECT * FROM users WHERE id = $1', [1]);
const user = result.rows[0]; // тип: any

// Немає перевірки типів!
console.log(user.eemail); // Друкарська помилка, але код скомпілюється
```

::tip

Type safety не тільки запобігає помилкам, але й значно прискорює розробку завдяки автодоповненню у сучасних IDE (VS Code, WebStorm). Ви не пам'ятаєте точну назву колонки? Просто натисніть `Ctrl+Space` — IDE покаже всі доступні властивості Entity.

::

### Автоматичне керування схемою БД (міграції)

TypeORM підтримує два підходи до синхронізації структури бази даних:

**1. Автоматична синхронізація (`synchronize: true`):**

```typescript
const dataSource = new DataSource({
  type: 'postgres',
  host: 'localhost',
  database: 'myapp',
  synchronize: true, // ⚠️ Тільки для розробки!
  entities: [User, Post, Comment],
});
```

При старті застосунку TypeORM автоматично створює, змінює або видаляє таблиці, щоб структура БД відповідала вашим Entity класам.

::caution

**Ніколи не використовуйте `synchronize: true` у production!** Це може призвести до втрати даних при зміні структури Entity (наприклад, видалення колонки). Для production завжди використовуйте міграції.

::

**2. Міграції (*Migrations*):** Контрольовані зміни схеми через версійовані SQL-скрипти.

```bash
# Генерація міграції на основі змін Entity
npx typeorm migration:generate -d src/data-source.ts -n AddAgeToUsers

# Застосування міграції
npx typeorm migration:run -d src/data-source.ts
```

TypeORM автоматично генерує SQL-код для міграції:

```typescript
import { MigrationInterface, QueryRunner } from 'typeorm';

export class AddAgeToUsers1699000000000 implements MigrationInterface {
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

Міграції зберігаються у системі контролю версій (Git) разом із кодом, що дозволяє відслідковувати всі зміни схеми БД та відкочувати їх у разі потреби.

### Спрощення роботи зі зв'язками між таблицями

У реляційних базах даних таблиці пов'язані через зовнішні ключі (*foreign keys*). Без ORM вам потрібно вручну виконувати JOIN-запити та зшивати дані з різних таблиць. TypeORM автоматизує цей процес через декоратори відносин.

**Приклад: користувач має багато постів (one-to-many):**

```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @OneToMany(() => Post, post => post.user)
  posts: Post[];
}

@Entity()
export class Post {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @ManyToOne(() => User, user => user.posts)
  user: User;
}
```

Тепер ви можете завантажити користувача разом із усіма його постами одним викликом:

```typescript
const user = await userRepository.findOne({
  where: { id: 1 },
  relations: ['posts'], // Eager loading через JOIN
});

console.log(user.name);
user.posts.forEach(post => console.log(post.title));
```

TypeORM згенерує оптимізований SQL із LEFT JOIN:

```sql
SELECT 
  user.*, 
  post.id AS post_id, 
  post.title AS post_title
FROM users user
LEFT JOIN posts post ON post.user_id = user.id
WHERE user.id = 1
```

::note

Це значно простіше, ніж писати JOIN вручну та маппити результати у вкладені об'єкти. TypeORM автоматично розпізнає структуру результату та створить об'єкти з правильними зв'язками.

::

### Кросплатформенність (підтримка різних СУБД)

TypeORM підтримує понад 10 різних систем керування базами даних. Це означає, що ви можете перемикатися між БД, змінюючи лише конфігурацію, без переписування коду запитів.

**Підтримувані СУБД:**

| База даних       | Драйвер          | Особливості                                |
| ---------------- | ---------------- | ------------------------------------------ |
| PostgreSQL       | `pg`             | Повна підтримка всіх функцій TypeORM       |
| MySQL / MariaDB  | `mysql2`         | Відмінності у синтаксисі JSON-запитів      |
| SQLite           | `sqlite3`        | Ідеально для тестування та прототипування  |
| Microsoft SQL    | `mssql`          | Підтримка Windows Authentication           |
| Oracle           | `oracledb`       | Специфічний синтаксис пагінації            |
| MongoDB          | `mongodb`        | NoSQL підтримка (обмежений функціонал ORM) |
| CockroachDB      | `pg`             | PostgreSQL-сумісний розподілений DB        |

**Приклад перемикання між БД:**

::code-group

```typescript [PostgreSQL]
const dataSource = new DataSource({
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'postgres',
  password: 'secret',
  database: 'myapp',
  entities: [User],
});
```

```typescript [MySQL]
const dataSource = new DataSource({
  type: 'mysql',
  host: 'localhost',
  port: 3306,
  username: 'root',
  password: 'secret',
  database: 'myapp',
  entities: [User],
});
```

```typescript [SQLite (для тестів)]
const dataSource = new DataSource({
  type: 'sqlite',
  database: ':memory:', // In-memory БД
  entities: [User],
  synchronize: true,
});
```

::

Це особливо корисно для:


- **Локальної розробки:** Використовуйте SQLite для швидкого прототипування.
- **Тестування:** In-memory SQLite база для юніт-тестів (надзвичайно швидко).
- **Production:** PostgreSQL або MySQL залежно від інфраструктури.
- **Міграції між провайдерами:** Перехід з on-premise MySQL на AWS RDS PostgreSQL без переписування логіки.

::warning

Хоча TypeORM намагається абстрагувати відмінності між БД, деякі специфічні функції все ж таки не є кросплатформними. Наприклад, `ARRAY` типи у PostgreSQL або `JSON_EXTRACT()` у MySQL. Якщо ви плануєте підтримувати кілька СУБД, уникайте використання специфічних функцій у запитах.

::

---

## Переваги використання ORM

### Менше boilerplate коду

У попередньому розділі ми бачили приклади скорочення коду. Але справжня перевага стає очевидною при роботі зі складними операціями.

**Приклад: каскадне збереження вкладених об'єктів**

Без ORM вам потрібно вручну керувати порядком INSERT та передавати ID між запитами:

```typescript
// Без ORM: багато ручної роботи
async function createUserWithPosts(userData, postsData) {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    
    // 1. Створюємо користувача
    const userResult = await client.query(
      'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id',
      [userData.email, userData.name]
    );
    const userId = userResult.rows[0].id;
    
    // 2. Для кожного поста створюємо запис
    for (const postData of postsData) {
      await client.query(
        'INSERT INTO posts (user_id, title, content) VALUES ($1, $2, $3)',
        [userId, postData.title, postData.content]
      );
    }
    
    await client.query('COMMIT');
    return userId;
    
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

З TypeORM це перетворюється на 5 рядків:

```typescript
// З TypeORM: просто та елегантно
const user = new User();
user.email = 'test@example.com';
user.name = 'Test User';
user.posts = [
  { title: 'Post 1', content: '...' },
  { title: 'Post 2', content: '...' },
].map(data => Object.assign(new Post(), data));

await userRepository.save(user); // Cascade збереже і користувача, і пости
```

### Автодоповнення та перевірка типів

TypeORM використовує TypeScript Generic типи для забезпечення type safety у всіх операціях:

```typescript
// Репозиторій типізований на User
const userRepository: Repository<User> = dataSource.getRepository(User);

// QueryBuilder знає структуру User
const users = await userRepository
  .createQueryBuilder('user')
  .where('user.age > :minAge', { minAge: 18 }) // ✅ Типи параметрів перевіряються
  .orderBy('user.created_at', 'DESC')           // ✅ 'ASC' | 'DESC' — enum type
  .getMany();                                   // Повертає Promise<User[]>

// Find опції також типізовані
const user = await userRepository.findOne({
  where: { 
    email: 'test@example.com', // ✅ Правильний тип
    // age: '25' // ❌ Помилка: string не присвоюється number
  },
  select: ['id', 'email'], // ✅ Тільки властивості User
  order: { created_at: 'DESC' },
});
```

**Інтеграція з VS Code:**

::terminal-preview{title="VS Code IntelliSense" :cursor="false"}

<div class="line"><span class="opacity-40">//</span> Коли ви пишете <strong>userRepository.find</strong> та натискаєте Ctrl+Space:</div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">find</span><span class="opacity-60">(options?: FindManyOptions&lt;User&gt;): Promise&lt;User[]&gt;</span></div>
<div class="line"><span class="text-blue-400 font-bold">findBy</span><span class="opacity-60">(where: FindOptionsWhere&lt;User&gt;): Promise&lt;User[]&gt;</span></div>
<div class="line"><span class="text-blue-400 font-bold">findOne</span><span class="opacity-60">(options: FindOneOptions&lt;User&gt;): Promise&lt;User | null&gt;</span></div>
<div class="line"><span class="text-blue-400 font-bold">findOneBy</span><span class="opacity-60">(where: FindOptionsWhere&lt;User&gt;): Promise&lt;User | null&gt;</span></div>
<div class="line"><span class="text-green-400 font-bold">✓</span> Автодоповнення показує всі доступні методи з документацією</div>

::

### Простіше тестування через мокування

TypeORM використовує Repository Pattern, що дозволяє легко замінити справжній репозиторій на mock у тестах:

```typescript
// users.service.ts
export class UsersService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}

  async findByEmail(email: string): Promise<User | null> {
    return this.userRepository.findOneBy({ email });
  }
}

// users.service.spec.ts
describe('UsersService', () => {
  let service: UsersService;
  let mockRepository: MockType<Repository<User>>;

  beforeEach(() => {
    mockRepository = {
      findOneBy: jest.fn(),
      save: jest.fn(),
      // ... інші методи
    };

    service = new UsersService(mockRepository as any);
  });

  it('should find user by email', async () => {
    const mockUser = { id: 1, email: 'test@example.com', name: 'Test' };
    mockRepository.findOneBy.mockResolvedValue(mockUser);

    const result = await service.findByEmail('test@example.com');

    expect(result).toEqual(mockUser);
    expect(mockRepository.findOneBy).toHaveBeenCalledWith({ 
      email: 'test@example.com' 
    });
  });
});
```

Без ORM вам довелося б мокувати весь `Pool` та його методи, що значно складніше.

### Вбудована підтримка транзакцій

TypeORM надає зручні обгортки для роботи з транзакціями:

```typescript
// Підхід 1: Метод withTransaction
await dataSource.transaction(async (transactionalEntityManager) => {
  const user = new User();
  user.email = 'test@example.com';
  await transactionalEntityManager.save(user);

  const post = new Post();
  post.title = 'First Post';
  post.user = user;
  await transactionalEntityManager.save(post);

  // Якщо виникне помилка, обидві операції відкотяться автоматично
});

// Підхід 2: QueryRunner для ручного керування
const queryRunner = dataSource.createQueryRunner();
await queryRunner.connect();
await queryRunner.startTransaction();

try {
  await queryRunner.manager.save(user);
  await queryRunner.manager.save(post);
  await queryRunner.commitTransaction();
} catch (error) {
  await queryRunner.rollbackTransaction();
  throw error;
} finally {
  await queryRunner.release();
}
```

### Захист від SQL injection за замовчуванням

TypeORM автоматично екранує всі параметри у запитах, тому SQL-ін'єкції неможливі за замовчуванням:

```typescript
// ✅ Безпечно: TypeORM автоматично екранує параметри
const email = userInput; // Може містити "'; DROP TABLE users; --"
const user = await userRepository.findOneBy({ email });

// Генерується параметризований запит:
// SELECT * FROM users WHERE email = $1
// Параметри: ["'; DROP TABLE users; --"]

// ✅ Також безпечно у QueryBuilder
const users = await userRepository
  .createQueryBuilder('user')
  .where('user.email = :email', { email: userInput })
  .getMany();
```

::caution

Захист діє лише якщо ви **не конкатенуєте** рядки вручну:

```typescript
// ❌ НЕБЕЗПЕЧНО: Ручна конкатенація
const searchTerm = userInput;
await dataSource.query(`SELECT * FROM users WHERE email LIKE '%${searchTerm}%'`);

// ✅ БЕЗПЕЧНО: Параметризований запит
await dataSource.query(
  'SELECT * FROM users WHERE email LIKE $1',
  [`%${searchTerm}%`]
);
```

::

---

## Недоліки ORM

### Performance overhead

ORM додає додатковий шар обробки між вашим кодом та базою даних. Це включає:

1. **Парсинг метаданих декораторів:** TypeORM сканує Entity класи та будує внутрішню схему при ініціалізації.
2. **Генерація SQL:** Кожен виклик методу репозиторію транслюється у SQL через внутрішній query builder.
3. **Маппінг результатів:** Рядки з БД перетворюються на екземпляри класів із усіма декораторами та методами.

**Приклад вимірювання overhead:**

```typescript
// Benchmark: отримання 10,000 записів
console.time('Raw SQL');
const rawResult = await pool.query('SELECT * FROM users LIMIT 10000');
console.timeEnd('Raw SQL'); // ~50ms

console.time('TypeORM find()');
const ormResult = await userRepository.find({ take: 10000 });
console.timeEnd('TypeORM find()'); // ~120ms

// TypeORM повільніший на ~70ms (140% overhead)
```

::note

У більшості веб-застосунків цей overhead незначний порівняно з іншими факторами (мережева затримка, обробка бізнес-логіки). Проте для високонавантажених систем із мільйонами запитів на секунду кожна мілісекунда має значення.

::

### Складність налаштування для оптимізації

Щоб TypeORM генерував оптимальні запити, потрібно розуміти:

- **Eager vs Lazy loading:** Коли завантажувати зв'язані дані.
- **N+1 problem:** Як уникнути множинних запитів у циклі.
- **Query optimization:** Які індекси потрібні для швидких запитів.

**Приклад N+1 проблеми:**

```typescript
// ❌ ПОГАНО: N+1 запитів
const users = await userRepository.find(); // 1 запит

for (const user of users) {
  const posts = await postRepository.findBy({ userId: user.id }); // N запитів!
  console.log(`${user.name} has ${posts.length} posts`);
}
// Якщо 100 користувачів — виконається 101 запит

// ✅ ДОБРЕ: 1 запит із JOIN
const users = await userRepository.find({ relations: ['posts'] });

for (const user of users) {
  console.log(`${user.name} has ${user.posts.length} posts`);
}
// Виконається лише 1 запит із LEFT JOIN
```

### Крива навчання

TypeORM має велику кількість концепцій, які потрібно вивчити:

- Декоратори Entity (`@Entity`, `@Column`, `@PrimaryGeneratedColumn`)
- Види відносин (`@OneToOne`, `@OneToMany`, `@ManyToMany`)
- Каскадні операції (`cascade: true`)
- Eager/Lazy loading
- Query Builder синтаксис
- Міграції та синхронізація схеми
- Subscribers та Listeners для життєвого циклу Entity

Для розробника, який щойно почав вивчати Node.js, це може бути overwhelming (*переповнюючим*).


### Обмеження для дуже складних запитів

Деякі SQL-конструкції важко або неможливо виразити через ORM API без використання raw SQL:

**Приклад 1: Віконні функції (Window Functions)**

```sql
-- Складний SQL із ROW_NUMBER()
SELECT 
  *,
  ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as rank
FROM products
WHERE rank <= 3;
```

У TypeORM це потребує raw query або складного QueryBuilder:

```typescript
const result = await dataSource.query(`
  SELECT 
    *,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as rank
  FROM products
`).then(rows => rows.filter(r => r.rank <= 3));
```

**Приклад 2: Рекурсивні CTE (Common Table Expressions)**

```sql
-- Ієрархічний запит для дерева категорій
WITH RECURSIVE category_tree AS (
  SELECT id, name, parent_id, 0 as level
  FROM categories
  WHERE parent_id IS NULL
  
  UNION ALL
  
  SELECT c.id, c.name, c.parent_id, ct.level + 1
  FROM categories c
  JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

TypeORM не має нативної підтримки рекурсивних CTE — потрібен raw SQL.

### "Чорна скринька" ефект

Коли ви використовуєте ORM, може виникнути ситуація, коли ви не розумієте, які саме SQL-запити генеруються. Це призводить до:

- **Неоптимальних запитів:** ORM може згенерувати запит із зайвими JOIN або без необхідних індексів.
- **Важкості діагностики:** Коли виникає performance issue, важко зрозуміти, де саме проблема.
- **Надмірної залежності:** Розробники забувають основи SQL та не можуть оптимізувати запити вручну.

::tip

Завжди вмикайте логування SQL під час розробки:

```typescript
const dataSource = new DataSource({
  type: 'postgres',
  logging: true, // Логує всі SQL-запити у консоль
  // або
  logging: ['query', 'error'], // Логує тільки запити та помилки
});
```

Це дозволить вам бачити, які запити генерує TypeORM, та виявляти неефективні паттерни.

::

---

## Коли використовувати ORM vs raw SQL

### ORM для стандартних CRUD операцій

TypeORM найкраще підходить для типових операцій з даними:

```typescript
// ✅ Ідеально для ORM
await userRepository.save(user);
await userRepository.findOneBy({ email });
await userRepository.update({ id }, { name: 'New Name' });
await userRepository.delete({ id });

// Прості зв'язки
await userRepository.find({ 
  relations: ['posts', 'profile'],
  where: { isActive: true }
});
```

### Raw SQL для складних аналітичних запитів

Коли потрібна максимальна продуктивність або специфічні функції БД:

```typescript
// ✅ Краще використовувати raw SQL
const analytics = await dataSource.query(`
  SELECT 
    DATE_TRUNC('day', created_at) as date,
    COUNT(*) as total_orders,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) as median_order
  FROM orders
  WHERE created_at >= NOW() - INTERVAL '30 days'
  GROUP BY DATE_TRUNC('day', created_at)
  ORDER BY date DESC
`);
```

### Гібридний підхід у великих проєктах

У реальних Enterprise-застосунках зазвичай використовується комбінація:

```typescript
export class OrdersService {
  constructor(
    @InjectRepository(Order) private orderRepository: Repository<Order>,
    private dataSource: DataSource,
  ) {}

  // Простий CRUD через репозиторій
  async createOrder(dto: CreateOrderDto): Promise<Order> {
    const order = this.orderRepository.create(dto);
    return this.orderRepository.save(order);
  }

  async findById(id: number): Promise<Order> {
    return this.orderRepository.findOne({
      where: { id },
      relations: ['items', 'customer'],
    });
  }

  // Складна аналітика через raw SQL
  async getDashboardStats(startDate: Date, endDate: Date) {
    return this.dataSource.query(`
      SELECT 
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(*) as total_orders,
        SUM(total_amount) as revenue,
        AVG(items_count) as avg_items_per_order
      FROM orders
      WHERE created_at BETWEEN $1 AND $2
    `, [startDate, endDate]);
  }

  // QueryBuilder для динамічних фільтрів
  async search(filters: OrderSearchDto) {
    const query = this.orderRepository.createQueryBuilder('order');

    if (filters.customerId) {
      query.andWhere('order.customer_id = :customerId', { 
        customerId: filters.customerId 
      });
    }

    if (filters.status) {
      query.andWhere('order.status IN (:...statuses)', { 
        statuses: filters.status 
      });
    }

    if (filters.minAmount) {
      query.andWhere('order.total_amount >= :minAmount', { 
        minAmount: filters.minAmount 
      });
    }

    return query
      .orderBy('order.created_at', 'DESC')
      .skip(filters.offset)
      .take(filters.limit)
      .getMany();
  }
}
```

### Критерії вибору

| Критерій                              | ORM (Repository) | QueryBuilder | Raw SQL |
| ------------------------------------- | ---------------- | ------------ | ------- |
| Прості CRUD операції                  | ✅ Так           | ⚠️ Надмірно  | ❌ Ні   |
| Складні JOIN (3+ таблиці)             | ⚠️ Можливо       | ✅ Так       | ✅ Так  |
| Агрегації та аналітика                | ❌ Обмежено      | ⚠️ Можливо   | ✅ Так  |
| Динамічні фільтри                     | ⚠️ Складно       | ✅ Так       | ⚠️ Складно |
| Type safety                           | ✅ Повна         | ✅ Часткова  | ❌ Ні   |
| Продуктивність                        | ⚠️ Overhead      | ⚠️ Середнє   | ✅ Максимальна |
| Читабельність для новачків            | ✅ Висока        | ⚠️ Середня   | ⚠️ Потребує знання SQL |

::accordion

::accordion-item{label="❓ Чи можна використовувати QueryBuilder для всіх запитів замість репозиторіїв?" icon="i-lucide-help-circle"}

Теоретично так, але це буде надмірно багатослівно (*verbose*) для простих операцій. QueryBuilder найкраще підходить для **динамічних запитів**, де умови `WHERE` залежать від вхідних параметрів. Для статичних запитів репозиторії простіші та зрозуміліші.

::

::accordion-item{label="❓ Як перевірити, який SQL генерує TypeORM для конкретного запиту?" icon="i-lucide-help-circle"}

Використовуйте метод `.getSql()` або `.printSql()` у QueryBuilder:

```typescript
const query = userRepository
  .createQueryBuilder('user')
  .where('user.age > :age', { age: 18 })
  .orderBy('user.created_at', 'DESC');

console.log(query.getSql()); // Виведе SQL без виконання
```

Або увімкніть глобальне логування у конфігурації DataSource.

::

::

---

## Огляд TypeORM

### TypeScript-first підхід

TypeORM — один із небагатьох ORM, що був розроблений спеціально для TypeScript з нуля. Це означає:

- **Нативна підтримка декораторів:** Використання `experimentalDecorators` для метаданих Entity.
- **Generic типи:** Всі методи репозиторіїв типізовані через `Repository<T>`.
- **Enum підтримка:** TypeScript enum автоматично мапяться на PostgreSQL enum типи.
- **Strict null checks:** Повна підтримка `strictNullChecks` у TypeScript.

```typescript
// Enum у TypeScript
export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest',
}

// Автоматично створюється PostgreSQL enum
@Entity()
export class User {
  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.USER,
  })
  role: UserRole;
}

// Type-safe використання
const user = new User();
user.role = UserRole.ADMIN; // ✅ OK
user.role = 'moderator';    // ❌ Error: Type '"moderator"' is not assignable
```

### Декоративний стиль (decorators)

Декоратори — це основний спосіб визначення метаданих Entity у TypeORM:

```typescript
@Entity('users', { schema: 'public' }) // Таблиця та схема БД
export class User {
  @PrimaryGeneratedColumn('uuid') // UUID як primary key
  id: string;

  @Column({ unique: true, length: 255 }) // Унікальна колонка з обмеженням
  email: string;

  @Column('text', { nullable: true }) // Nullable TEXT колонка
  bio?: string;

  @CreateDateColumn() // Автоматична дата створення
  created_at: Date;

  @UpdateDateColumn() // Автоматична дата оновлення
  updated_at: Date;

  @VersionColumn() // Для optimistic locking
  version: number;

  @OneToMany(() => Post, post => post.user, { cascade: true })
  posts: Post[];
}
```

### Підтримка Active Record та Data Mapper патернів

TypeORM підтримує два архітектурні патерни для роботи з даними:

**Active Record Pattern:** Entity сам відповідає за збереження/завантаження:

```typescript
@Entity()
export class User extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  // Методи Entity
  async archive(): Promise<void> {
    this.isArchived = true;
    await this.save(); // Метод успадкований від BaseEntity
  }
}

// Використання
const user = new User();
user.name = 'John';
await user.save(); // Active Record стиль

const foundUser = await User.findOneBy({ name: 'John' });
await foundUser.remove();
```

**Data Mapper Pattern (рекомендований):** Репозиторії відокремлені від Entity:

```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  // Entity — чиста доменна модель без методів БД
}

// Використання через репозиторій
const userRepository = dataSource.getRepository(User);

const user = new User();
user.name = 'John';
await userRepository.save(user);

const foundUser = await userRepository.findOneBy({ name: 'John' });
await userRepository.remove(foundUser);
```

::tip

**Data Mapper підхід рекомендований для великих проєктів**, оскільки він забезпечує кращу testability (легше мокувати репозиторії) та дотримується принципу Single Responsibility (Entity відповідає лише за дані, а репозиторій — за персистентність).

::

### Велика екосистема та community

TypeORM має активну спільноту та велику кількість розширень:

- **GitHub:** 33k+ зірок, 6k+ forks
- **NPM:** 2+ мільйони завантажень на тиждень
- **Підтримка фреймворків:** NestJS (офіційна інтеграція), Koa, Express, Fastify
- **Інструменти:**
  - `typeorm-extension`: Utilities для seeding та fixtures
  - `typeorm-naming-strategies`: Кастомні стратегії іменування колонок
  - `typeorm-transactional`: Декларативні транзакції через декоратори

### Офіційна інтеграція з NestJS

TypeORM є рекомендованим ORM для NestJS фреймворку:


```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'postgres',
      password: 'secret',
      database: 'myapp',
      entities: [User],
      synchronize: false,
    }),
    TypeOrmModule.forFeature([User]), // Реєстрація Entity
  ],
})
export class AppModule {}

// users.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}

  async create(email: string, name: string): Promise<User> {
    const user = this.userRepository.create({ email, name });
    return this.userRepository.save(user);
  }

  async findAll(): Promise<User[]> {
    return this.userRepository.find();
  }
}
```

NestJS автоматично керує життєвим циклом DataSource та забезпечує Dependency Injection для репозиторіїв.

---

## Альтернативи TypeORM

### Prisma: schema-first підхід

**Prisma** — сучасний ORM із власною мовою схеми та генерацією типів.

**Відмінності від TypeORM:**

| Характеристика         | TypeORM                     | Prisma                         |
| ---------------------- | --------------------------- | ------------------------------ |
| Визначення схеми       | TypeScript декоратори       | Prisma Schema Language (DSL)   |
| Генерація типів        | Runtime через декоратори    | Compile-time генерація         |
| Міграції               | TypeScript класи            | SQL файли                      |
| Query Builder          | Об'єктно-орієнтований       | Fluent API                     |
| Продуктивність         | Середня                     | Висока (Rust Query Engine)     |

**Приклад Prisma:**

```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  content  String
  userId   Int
  user     User   @relation(fields: [userId], references: [id])
}
```

```typescript
// Використання
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const user = await prisma.user.create({
  data: {
    email: 'test@example.com',
    name: 'Test User',
    posts: {
      create: [
        { title: 'First Post', content: '...' },
      ],
    },
  },
  include: { posts: true },
});
```

**Переваги Prisma:**
- Сильніша типізація (генерація на етапі компіляції).
- Простіша схема (декларативна DSL).
- Вбудований Prisma Studio (GUI для перегляду даних).

**Недоліки Prisma:**
- Менша гнучкість (не можна використовувати чисті TypeScript класи).
- Новіша бібліотека (менше матеріалів для вивчення).
- Додатковий крок генерації (`prisma generate`).

### Sequelize: один з найстаріших ORM для Node.js

**Sequelize** існує з 2010 року та підтримує як JavaScript, так і TypeScript.

```typescript
import { Sequelize, Model, DataTypes } from 'sequelize';

const sequelize = new Sequelize('postgres://user:pass@localhost:5432/mydb');

class User extends Model {
  public id!: number;
  public email!: string;
  public name!: string;
}

User.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  },
  { sequelize, modelName: 'user' }
);

const user = await User.create({ email: 'test@example.com', name: 'Test' });
```

**Переваги Sequelize:**
- Найбільша спільнота та найбільше туторіалів.
- Стабільний та перевірений часом.
- Підтримка багатьох БД.

**Недоліки Sequelize:**
- Застарілий API (менш TypeScript-friendly).
- Важча типізація порівняно з TypeORM або Prisma.
- Повільніша еволюція (рідше оновлення).

### Drizzle: lightweight TypeScript ORM

**Drizzle ORM** — новий гравець (2022), що позиціонується як «headless TypeScript ORM».

```typescript
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle(pool);

const newUser = await db.insert(users).values({
  email: 'test@example.com',
  name: 'Test User',
}).returning();
```

**Переваги Drizzle:**
- Мінімальний runtime overhead (близько до raw SQL).
- SQL-like синтаксис (легше для тих, хто знає SQL).
- Повна типізація без декораторів.

**Недоліки Drizzle:**
- Молода бібліотека (мало матеріалів).
- Менша функціональність порівняно з TypeORM.
- Немає офіційної інтеграції з NestJS.

### MikroORM: TypeScript alternative

**MikroORM** — TypeScript ORM, що є концептуальним конкурентом TypeORM.

```typescript
@Entity()
export class User {
  @PrimaryKey()
  id!: number;

  @Property({ unique: true })
  email!: string;

  @Property()
  name!: string;

  @OneToMany(() => Post, post => post.user)
  posts = new Collection<Post>(this);
}

const orm = await MikroORM.init({
  entities: [User, Post],
  dbName: 'mydb',
  type: 'postgresql',
});

const user = orm.em.create(User, { email: 'test@example.com', name: 'Test' });
await orm.em.persistAndFlush(user);
```

**Переваги MikroORM:**
- Identity Map Pattern (кешування об'єктів у пам'яті).
- Unit of Work (автоматичне відстеження змін).
- Кращі можливості для Domain-Driven Design.

**Недоліки MikroORM:**
- Менша спільнота порівняно з TypeORM.
- Складніша крива навчання (більше концепцій).

### Порівняльна таблиця

| Критерій                    | TypeORM | Prisma | Sequelize | Drizzle | MikroORM |
| --------------------------- | ------- | ------ | --------- | ------- | -------- |
| **TypeScript-first**        | ✅      | ✅     | ⚠️        | ✅      | ✅       |
| **Підтримка декораторів**   | ✅      | ❌     | ❌        | ❌      | ✅       |
| **Type safety**             | ✅      | ✅✅   | ⚠️        | ✅      | ✅       |
| **Продуктивність**          | ⚠️      | ✅     | ⚠️        | ✅✅    | ✅       |
| **Спільнота**               | ✅✅    | ✅     | ✅✅      | ⚠️      | ⚠️       |
| **NestJS інтеграція**       | ✅✅    | ✅     | ✅        | ❌      | ✅       |
| **Крива навчання**          | ⚠️      | ✅     | ⚠️        | ✅      | ❌       |
| **Міграції**                | ✅      | ✅✅   | ✅        | ✅      | ✅       |
| **Raw SQL підтримка**       | ✅      | ✅     | ✅        | ✅      | ✅       |
| **Документація**            | ✅      | ✅✅   | ✅        | ⚠️      | ✅       |

**Легенда:** ✅✅ Відмінно | ✅ Добре | ⚠️ Середнє | ❌ Немає/Слабко

::tip

**Вибір ORM залежить від проєкту:**

- **TypeORM:** Якщо ви використовуєте NestJS або вам подобаються декоратори.
- **Prisma:** Якщо вам важлива максимальна type safety та простота схеми.
- **Drizzle:** Якщо потрібна висока продуктивність та ви комфортно працюєте з SQL.
- **Sequelize:** Якщо підтримуєте legacy проєкт або потребуєте максимальну сумісність з JavaScript.
- **MikroORM:** Якщо будуєте складну Domain-Driven Design архітектуру.

::

---

## Підсумок

::card-group

::card{title="✅ Що ви опанували" icon="i-lucide-check-circle"}

- Зрозуміли концепцію ORM (*Object-Relational Mapping*) як техніку відображення таблиць БД на класи TypeScript.
- Дізналися про переваги ORM: менше boilerplate коду, type safety, автоматичні міграції, спрощення роботи зі зв'язками.
- Усвідомили недоліки ORM: performance overhead, складність оптимізації, крива навчання, "чорна скринька" ефект.
- Навчилися обирати між ORM та raw SQL залежно від типу запиту та вимог до продуктивності.
- Познайомилися з TypeORM та його місцем у Node.js/TypeScript екосистемі.
- Порівняли TypeORM з альтернативами: Prisma, Sequelize, Drizzle, MikroORM.

::

::card{title="🚀 Наступні кроки" icon="i-lucide-arrow-right"}

У наступній лекції ви перейдете до практичного налаштування TypeORM у NestJS проєкті:
- Встановлення необхідних пакетів та конфігурація DataSource.
- Підключення до PostgreSQL через змінні оточення.
- Налаштування Docker Compose для локальної розробки.
- Перевірка з'єднання та graceful shutdown.

::

::

::accordion

::accordion-item{label="❓ Чи можна використовувати TypeORM без TypeScript?" icon="i-lucide-help-circle"}

Технічно так, TypeORM підтримує JavaScript, але ви втратите більшість переваг: type safety, автодоповнення IDE та перевірку типів декораторів. У JavaScript коді доведеться використовувати об'єкти конфігурації замість декораторів, що робить код більш багатослівним.

::

::accordion-item{label="❓ Чи впливає використання ORM на швидкість роботи застосунку у production?" icon="i-lucide-help-circle"}

Так, але у більшості випадків цей вплив незначний (10-20% overhead порівняно з raw SQL). Критичні шляхи (*hot paths*) можна оптимізувати через raw queries або кешування. Для 99% веб-застосунків bottleneck знаходиться не в ORM, а у бізнес-логіці, мережевій затримці або неоптимальних індексах БД.

::

::accordion-item{label="❓ Чи можна мігрувати існуючий проєкт з raw SQL на TypeORM?" icon="i-lucide-help-circle"}

Так, TypeORM дозволяє поступову міграцію. Ви можете:
1. Створити Entity класи на основі існуючих таблиць (TypeORM CLI підтримує реверс-інжиніринг).
2. Почати використовувати репозиторії для нових функцій.
3. Поступово рефакторити старий код, замінюючи raw queries на ORM методи.
4. Залишити складні аналітичні запити як raw SQL.

Гібридний підхід — найбезпечніший для великих проєктів.

::

::

::note

**Корисні ресурси для поглибленого вивчення:**

- [Офіційна документація TypeORM](https://typeorm.io/)
- [TypeORM GitHub Repository](https://github.com/typeorm/typeorm)
- [NestJS + TypeORM Integration Guide](https://docs.nestjs.com/techniques/database)
- [Comparison of Node.js ORMs (2024)](https://blog.logrocket.com/comparing-top-node-js-orms/)

::

---

**Ви успішно завершили другу лекцію модуля!** Тепер ви розумієте, що таке ORM, коли його використовувати, та чому TypeORM є відмінним вибором для TypeScript/NestJS проєктів. У наступній лекції ми перейдемо до практичного налаштування та інтеграції TypeORM у реальний застосунок.