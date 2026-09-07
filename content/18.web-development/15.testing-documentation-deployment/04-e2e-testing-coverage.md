# E2E тестування та покриття коду

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати техніку End-to-End тестування HTTP API через бібліотеку Supertest.
- Навчитися створювати та налаштовувати повний NestJS застосунок для E2E тестів через `INestApplication`.
- Зрозуміти стратегію роботи з тестовою базою даних: ізоляція, seeding, cleanup між тестами.
- Освоїти тестування критичних user flows: автентифікація, CRUD операції, обробка помилок.
- Навчитися аналізувати code coverage звіти та встановлювати мінімальні пороги для CI/CD.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **End-to-End Test (E2E):** тест, що перевіряє повний шлях запиту через всі шари застосунку від HTTP endpoint до бази даних.
- **Supertest:** бібліотека для виконання HTTP запитів та assertions у тестах.
- **INestApplication:** екземпляр запущеного NestJS застосунку для тестування.
- **Test Database:** окрема база даних, призначена виключно для тестів, ізольована від production та development БД.
- **Seeding:** попереднє заповнення тестової бази даних фіксованими даними для відтворюваності тестів.

::

::

---

## Короткий зміст

У цій лекції вивчається наскрізне тестування HTTP API та аналіз покриття коду тестами:

- **E2E тестування концепція** — тестування повних user journeys через реальні HTTP запити, перевірка інтеграції всіх layers (контролер → сервіс → репозиторій → БД), closest to production scenarios
- **Supertest** — бібліотека для HTTP assertions, методи request(app.getHttpServer()).get('/endpoint'), expectations через .expect(200), .expect(body), chaining assertions
- **INestApplication** — тестовий екземпляр NestJS застосунку, створення через Test.createTestingModule().compile().createNestApplication(), ініціалізація pipes/guards для реалістичних тестів, shutdown після тестів
- **Тестова база даних** — окрема БД для E2E тестів (test DB або in-memory SQLite), setup у beforeAll: підключення та синхронізація схеми, cleanup у afterEach: очищення таблиць, teardown у afterAll: закриття з'єднання
- **Testing endpoints** — GET для читання даних, POST для створення з validation перевіркою, PUT/PATCH для оновлення, DELETE для видалення, testing authentication (401), authorization (403), validation errors (400)
- **Покриття коду** — команда `jest --coverage` для генерації звіту, папка coverage/ з HTML звітом, metrics: statements, branches, functions, lines, threshold налаштування у jest.config для enforce мінімального coverage
- **CI integration** — running E2E тестів у GitHub Actions, setup test database через Docker services, parallel test execution для швидкості, artifacts для coverage reports

Розглядаються практичні приклади: E2E тест для authentication flow, CRUD операцій з валідацією, testing error scenarios, database seeding для тестів.

---

## Концепція E2E тестування

На попередніх лекціях ми розглянули Unit тести, що перевіряють ізольовану логіку окремих компонентів (сервісів, функцій) із заміною всіх залежностей на моки. Проте така ізоляція має недолік: Unit тести **не перевіряють, чи правильно компоненти працюють разом**. Можлива ситуація, коли всі Unit тести проходять, але застосунок не працює у production через помилки в інтеграції між шарами.

**End-to-End (E2E) тести** вирішують цю проблему, перевіряючи **повний шлях запиту** від точки входу (HTTP endpoint) до бази даних та назад. Ці тести запускають весь NestJS застосунок у максимально наближеному до production режимі, виконують реальні HTTP запити та перевіряють відповіді.

### Що перевіряють E2E тести

Уявіть типовий user flow: користувач реєструється на вашому сайті, заповнює форму реєстрації, натискає кнопку «Sign Up». Що відбувається всередині backend:

1. **HTTP Layer:** Запит `POST /api/auth/register` приймається контролером `AuthController`.
2. **Validation Layer:** `class-validator` перевіряє DTO: чи валідний email, чи достатньо довгий пароль.
3. **Guards Layer:** `AuthGuard` перевіряє, чи користувач вже авторизований (для endpoint реєстрації цей guard зазвичай відсутній, але для інших endpoints критичний).
4. **Business Logic Layer:** `AuthService` перевіряє, чи email вже зареєстрований, хешує пароль через `bcrypt`.
5. **Database Layer:** `UserRepository` зберігає нового користувача у PostgreSQL.
6. **Response Layer:** Контролер повертає `201 Created` з даними користувача та JWT токеном.

Unit тести перевірять окремо кожен компонент:
- Unit тест для `AuthService` перевірить хешування пароля (з mock репозиторію).
- Unit тест для валідаційного DTO перевірить regexp для email.
- Unit тест для `UserRepository` (Integration) перевірить збереження у БД.

Проте **жоден із цих тестів не перевірить повний ланцюг**. Якщо ви забули додати `ValidationPipe` до global pipes, DTO не валідується, і невалідні дані потраплять у сервіс. Якщо у контролері неправильно обробляється виняток від сервісу, клієнт отримає `500 Internal Server Error` замість `400 Bad Request`.

**E2E тест перевіряє весь flow:**

```typescript
it('POST /api/auth/register should create new user', async () => {
  const response = await request(app.getHttpServer())
    .post('/api/auth/register')
    .send({
      email: 'newuser@test.com',
      password: 'SecurePass123!',
      name: 'Test User',
    })
    .expect(201);

  expect(response.body).toHaveProperty('id');
  expect(response.body).toHaveProperty('access_token');
  expect(response.body.email).toBe('newuser@test.com');
  expect(response.body).not.toHaveProperty('password'); // Пароль не має повертатися

  // Перевірка, що користувач реально збережений у БД
  const user = await userRepository.findOne({ where: { email: 'newuser@test.com' } });
  expect(user).toBeDefined();
  expect(user!.password).not.toBe('SecurePass123!'); // Пароль захешований
});
```

Цей тест виконує **реальний HTTP запит**, проходить через всі шари застосунку, зберігає дані у **реальну БД** (тестову) та перевіряє результат. Якщо будь-який компонент у ланцюзі працює некоректно, тест провалиться.

::note
**Чому E2E тести називаються «end-to-end»?** Вони перевіряють шлях від **одного кінця** системи (клієнтський запит) до **іншого кінця** (база даних) та назад. У frontend E2E тестах (наприклад, Cypress, Playwright) «end-to-end» означає шлях від UI форми до відображення результату. У backend E2E тестах — від HTTP endpoint до persistency layer.
::

### Відмінності між E2E та Integration тестами

Межа між E2E та Integration тестами інколи розмита, але є ключова відмінність:

**Integration тести** перевіряють взаємодію **між кількома компонентами**, але **не через HTTP API**. Наприклад, Integration тест може безпосередньо викликати метод сервісу, який взаємодіє з репозиторієм та реальною БД:

```typescript
// Integration тест (без HTTP)
it('should save order to database', async () => {
  const order = await orderService.createOrder('user-1', ['prod-1']);
  
  const saved = await orderRepository.findOne({ where: { id: order.id } });
  expect(saved).toBeDefined();
});
```

**E2E тести** перевіряють **повний стек через HTTP**, імітуючи реальну поведінку клієнта:

```typescript
// E2E тест (через HTTP)
it('POST /api/orders should save order to database', async () => {
  const response = await request(app.getHttpServer())
    .post('/api/orders')
    .set('Authorization', `Bearer ${authToken}`)
    .send({ productIds: ['prod-1'] })
    .expect(201);

  const saved = await orderRepository.findOne({ where: { id: response.body.id } });
  expect(saved).toBeDefined();
});
```

E2E тест перевіряє **все**: HTTP роутинг, middleware, guards, interceptors, pipes, контролери, сервіси, репозиторії. Integration тест пропускає HTTP шар та перевіряє лише сервіс + БД.

---

## Налаштування E2E тестів у NestJS

NestJS проєкти за замовчуванням містять директорію `test/` з прикладом E2E тесту. Розглянемо детально, як налаштувати інфраструктуру для E2E тестування.

### Структура директорій

```
project-root/
├── src/                     # Application code
│   ├── auth/
│   ├── users/
│   ├── orders/
│   └── app.module.ts
├── test/                    # E2E тести (окрема директорія!)
│   ├── auth.e2e-spec.ts
│   ├── users.e2e-spec.ts
│   ├── orders.e2e-spec.ts
│   └── jest-e2e.json        # Окрема конфігурація Jest для E2E
└── package.json
```

**Чому E2E тести у окремій директорії?** Unit/Integration тести розміщуються поруч із кодом (`*.spec.ts`), оскільки тісно пов'язані з конкретними модулями. E2E тести перевіряють **інтеграцію між модулями** та не належать до жодного конкретного модуля, тому зберігаються окремо.

### Конфігурація jest-e2e.json

```json
{
  "moduleFileExtensions": ["js", "json", "ts"],
  "rootDir": ".",
  "testEnvironment": "node",
  "testRegex": ".e2e-spec.ts$",
  "transform": {
    "^.+\\.(t|j)s$": "ts-jest"
  },
  "moduleNameMapper": {
    "^@/(.*)$": "<rootDir>/../src/$1"
  }
}
```

**Ключові відмінності від Unit тестів:**
- **`testRegex`:** шукає файли з суфіксом `.e2e-spec.ts` замість `.spec.ts`.
- **`rootDir`:** вказує на директорію `test/`, а не `src/`.
- **`moduleNameMapper`:** налаштовує path aliases, щоб E2E тести могли імпортувати модулі з `src/`.

### package.json scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:cov": "jest --coverage",
    "test:e2e": "jest --config ./test/jest-e2e.json",
    "test:e2e:watch": "jest --config ./test/jest-e2e.json --watch"
  }
}
```

Команда `npm run test:e2e` запускає лише E2E тести з окремою конфігурацією.

### Встановлення залежностей

E2E тести вимагають додаткову бібліотеку **Supertest** для виконання HTTP assertions:

```bash
npm install --save-dev supertest @types/supertest
```

**Supertest** — це бібліотека, що дозволяє виконувати HTTP запити до Node.js сервера та робити assertions на відповіді. Вона інтегрується з Jest та підтримує promises/async-await.

::tip
Якщо ви використовуєте `fastify` замість `express` у NestJS (через `@nestjs/platform-fastify`), встановіть також адаптер для Supertest:

```bash
npm install --save-dev @nestjs/platform-fastify
```

Проте для більшості проєктів достатньо стандартного `@nestjs/platform-express`, який вже включений у NestJS.
::

---

## Створення та налаштування INestApplication

Основа кожного E2E тесту — створення екземпляра **`INestApplication`**, який представляє запущений NestJS застосунок.

### Базовий приклад E2E тесту

```typescript
// test/auth.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('Authentication (E2E)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule], // Імпортуємо весь застосунок
    }).compile();

    app = moduleFixture.createNestApplication();

    // Налаштовуємо глобальні pipes, як у main.ts
    app.useGlobalPipes(new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }));

    await app.init(); // Ініціалізуємо застосунок
  });

  afterAll(async () => {
    await app.close(); // Закриваємо з'єднання після всіх тестів
  });

  it('/api/auth/register (POST) should register new user', () => {
    return request(app.getHttpServer())
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!',
        name: 'Test User',
      })
      .expect(201)
      .expect((res) => {
        expect(res.body).toHaveProperty('id');
        expect(res.body.email).toBe('test@example.com');
      });
  });
});
```

Розберемо кожен крок детально.


### Test.createTestingModule() для E2E

На відміну від Unit тестів, де ми створюємо тестовий модуль із конкретними providers та моками, для E2E тестів ми імпортуємо **весь `AppModule`**:

```typescript
const moduleFixture = await Test.createTestingModule({
  imports: [AppModule], // Весь застосунок цілком
}).compile();
```

Це завантажує всі модулі, контролери, сервіси, guards, interceptors — весь стек, як у production. **Ніяких моків** — усі залежності реальні.

### createNestApplication() — створення екземпляра

Після компіляції модуля створюємо екземпляр застосунку:

```typescript
app = moduleFixture.createNestApplication();
```

`INestApplication` — це інтерфейс, що представляє запущений NestJS сервер. Він надає методи:
- **`app.init()`** — ініціалізує застосунок (запускає lifecycle hooks, підключає middleware).
- **`app.listen(port)`** — запускає HTTP сервер на вказаному порту (для E2E тестів зазвичай не використовується, оскільки Supertest працює без реального прослуховування порту).
- **`app.getHttpServer()`** — повертає underlying HTTP сервер (Express або Fastify), який передається у Supertest.
- **`app.close()`** — закриває застосунок та звільняє ресурси.

### Відтворення production конфігурації

Критично важливо налаштувати тестовий застосунок **ідентично** до production. У більшості NestJS проєктів файл `src/main.ts` містить глобальні налаштування:

```typescript
// src/main.ts (production)
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Глобальний ValidationPipe
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));

  // CORS
  app.enableCors({ origin: process.env.CORS_ORIGIN });

  // Глобальний prefix
  app.setGlobalPrefix('api');

  await app.listen(3000);
}
```

Ваш E2E тест має відтворити ці самі налаштування:

```typescript
beforeAll(async () => {
  const moduleFixture = await Test.createTestingModule({
    imports: [AppModule],
  }).compile();

  app = moduleFixture.createNestApplication();

  // Відтворюємо конфігурацію з main.ts
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));

  app.setGlobalPrefix('api');

  await app.init();
});
```

Якщо ви забудете додати `ValidationPipe`, ваші DTO не валідуватимуться у E2E тестах, і тести проходитимуть навіть при надсиланні невалідних даних — а у production валідація працюватиме та відкидатиме запити.

::warning
**Синхронізуйте конфігурацію між `main.ts` та E2E setup!** Кожен раз, коли ви додаєте глобальний pipe, guard, interceptor або middleware у `main.ts`, додайте його також у `beforeAll()` E2E тестів. Інакше тести не відображатимуть реальну поведінку production застосунку.

Для великих проєктів рекомендується винести конфігурацію у окрему функцію:

```typescript
// src/app.config.ts
export function configureApp(app: INestApplication) {
  app.useGlobalPipes(new ValidationPipe({ /* ... */ }));
  app.setGlobalPrefix('api');
  // інші налаштування
}

// src/main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  configureApp(app);
  await app.listen(3000);
}

// test/auth.e2e-spec.ts
beforeAll(async () => {
  app = moduleFixture.createNestApplication();
  configureApp(app); // Та сама конфігурація!
  await app.init();
});
```

Це гарантує повну синхронізацію конфігурації.
::

### app.close() — очищення ресурсів

Після завершення всіх тестів у suite обов'язково закривайте застосунок:

```typescript
afterAll(async () => {
  await app.close();
});
```

Це закриває з'єднання з БД, звільняє порти та інші ресурси. Без `app.close()` Jest може не завершитися після тестів (висітиме процес через відкриті з'єднання).

---

## Використання Supertest для HTTP assertions

**Supertest** — це бібліотека, що надає fluent API для виконання HTTP запитів та перевірки відповідей. Вона інтегрується з Jest та дозволяє писати readable assertions.

### Базовий синтаксис

```typescript
import * as request from 'supertest';

it('GET /api/users should return list of users', () => {
  return request(app.getHttpServer())
    .get('/api/users')
    .expect(200)
    .expect('Content-Type', /json/);
});
```

**`request(app.getHttpServer())`** створює Supertest агент для виконання запитів до NestJS сервера.

**Методи HTTP:**
- `.get(path)` — GET запит
- `.post(path)` — POST запит
- `.put(path)` — PUT запит
- `.patch(path)` — PATCH запит
- `.delete(path)` — DELETE запит

**Налаштування запиту:**
- `.send(body)` — встановлює тіло запиту (автоматично серіалізується у JSON)
- `.set(header, value)` — додає HTTP header
- `.query({ key: 'value' })` — додає query parameters
- `.attach(field, path)` — прикріплює файл (для multipart/form-data)

**Assertions:**
- `.expect(status)` — перевіряє HTTP status code
- `.expect(header, value)` — перевіряє HTTP header
- `.expect(callback)` — custom assertion через callback функцію

### Приклади різних типів запитів

**GET запит із query parameters:**

```typescript
it('GET /api/users?role=admin should return only admins', async () => {
  const response = await request(app.getHttpServer())
    .get('/api/users')
    .query({ role: 'admin' })
    .expect(200);

  expect(response.body).toBeInstanceOf(Array);
  expect(response.body.every((u: any) => u.role === 'admin')).toBe(true);
});
```

**POST запит із JSON body:**

```typescript
it('POST /api/posts should create new post', async () => {
  const newPost = {
    title: 'Test Post',
    content: 'Test content',
    authorId: 'user-123',
  };

  const response = await request(app.getHttpServer())
    .post('/api/posts')
    .send(newPost)
    .expect(201);

  expect(response.body).toHaveProperty('id');
  expect(response.body.title).toBe('Test Post');
});
```

**PUT запит для оновлення:**

```typescript
it('PUT /api/posts/:id should update post', async () => {
  const postId = 'existing-post-123';
  const updates = { title: 'Updated Title' };

  await request(app.getHttpServer())
    .put(`/api/posts/${postId}`)
    .send(updates)
    .expect(200)
    .expect((res) => {
      expect(res.body.title).toBe('Updated Title');
    });
});
```

**DELETE запит:**

```typescript
it('DELETE /api/posts/:id should remove post', async () => {
  const postId = 'post-to-delete';

  await request(app.getHttpServer())
    .delete(`/api/posts/${postId}`)
    .expect(204); // No Content

  // Перевірка, що пост реально видалений з БД
  const deleted = await postRepository.findOne({ where: { id: postId } });
  expect(deleted).toBeNull();
});
```

### Додавання Authorization headers

Більшість endpoints вимагають автентифікації. Для тестування захищених endpoints спочатку отримайте JWT токен:

```typescript
describe('Protected endpoints', () => {
  let authToken: string;

  beforeAll(async () => {
    // Реєструємо користувача та отримуємо токен
    const response = await request(app.getHttpServer())
      .post('/api/auth/register')
      .send({
        email: 'testuser@example.com',
        password: 'SecurePass123!',
      });

    authToken = response.body.access_token;
  });

  it('GET /api/profile should return user profile', async () => {
    const response = await request(app.getHttpServer())
      .get('/api/profile')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    expect(response.body.email).toBe('testuser@example.com');
  });

  it('GET /api/profile without token should return 401', async () => {
    await request(app.getHttpServer())
      .get('/api/profile')
      .expect(401);
  });
});
```

### Custom assertions через callback

Для складних перевірок використовуйте callback у `.expect()`:

```typescript
it('GET /api/users should return paginated results', async () => {
  await request(app.getHttpServer())
    .get('/api/users')
    .query({ page: 1, limit: 10 })
    .expect(200)
    .expect((res) => {
      // Custom assertions
      expect(res.body).toHaveProperty('data');
      expect(res.body).toHaveProperty('meta');
      expect(res.body.data).toBeInstanceOf(Array);
      expect(res.body.data.length).toBeLessThanOrEqual(10);
      expect(res.body.meta).toMatchObject({
        currentPage: 1,
        itemsPerPage: 10,
        totalPages: expect.any(Number),
        totalItems: expect.any(Number),
      });
    });
});
```

::tip
**async/await vs return promise:** Обидва підходи працюють для Supertest:

```typescript
// Підхід 1: async/await
it('test', async () => {
  const response = await request(app.getHttpServer()).get('/api/users').expect(200);
  expect(response.body).toBeDefined();
});

// Підхід 2: return promise
it('test', () => {
  return request(app.getHttpServer()).get('/api/users').expect(200);
});
```

Рекомендується **async/await**, оскільки це дозволяє робити додаткові assertions після запиту та покращує читабельність коду.
::

---

## Робота з тестовою базою даних

E2E тести виконують реальні операції з базою даних, тому критично важливо використовувати **окрему тестову БД**, ізольовану від development та production.

### Стратегії для тестової БД

Існує три основні підходи:

**1. Окрема PostgreSQL/MySQL БД для тестів**

Створіть окрему базу даних (наприклад, `myapp_test`) спеціально для тестів:

```typescript
// config/database.config.ts
export const getDatabaseConfig = (): TypeOrmModuleOptions => {
  const isTest = process.env.NODE_ENV === 'test';

  return {
    type: 'postgres',
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    username: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    database: isTest ? 'myapp_test' : process.env.DB_NAME || 'myapp_dev',
    entities: [__dirname + '/../**/*.entity{.ts,.js}'],
    synchronize: isTest, // Автоматична синхронізація схеми для тестів
    dropSchema: isTest, // Очищення схеми перед тестами
  };
};
```

**Переваги:** реалістичні умови (той самий СУБД, що у production).
**Недоліки:** повільніше за in-memory БД, вимагає запущеного PostgreSQL/MySQL.

**2. In-memory SQLite для швидкості**

Для швидкого виконання тестів використовуйте SQLite у пам'яті:

```typescript
export const getTestDatabaseConfig = (): TypeOrmModuleOptions => {
  return {
    type: 'sqlite',
    database: ':memory:', // БД у пам'яті
    entities: [__dirname + '/../**/*.entity{.ts,.js}'],
    synchronize: true,
    dropSchema: true,
  };
};
```

**Переваги:** максимальна швидкість (тести виконуються у 5-10 разів швидше).
**Недоліки:** SQLite має обмеження (немає деяких features PostgreSQL/MySQL), можливі розбіжності у поведінці.

**3. Docker контейнер для кожного тест suite**

Запускайте PostgreSQL/MySQL у Docker контейнері перед тестами:

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  postgres-test:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
    ports:
      - "5433:5432"
```

```bash
# Перед запуском тестів
docker-compose -f docker-compose.test.yml up -d
npm run test:e2e
docker-compose -f docker-compose.test.yml down
```

**Переваги:** повна ізоляція, можна паралельно запускати кілька тест suites.
**Недоліки:** складніше налаштування, вимагає Docker.

::note
Для більшості проєктів рекомендується **підхід 1 (окрема БД)** під час розробки та **підхід 3 (Docker)** у CI/CD pipeline. SQLite підходить для невеликих проєктів або коли швидкість критична, але будьте обережні з PostgreSQL-specific features (JSONB, array columns, full-text search).
::


### Setup та cleanup тестової БД

Типова структура E2E тесту з БД:

```typescript
describe('Users (E2E)', () => {
  let app: INestApplication;
  let dataSource: DataSource;
  let userRepository: Repository<User>;

  beforeAll(async () => {
    // 1. Створюємо тестовий модуль
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    })
      .overrideProvider(DataSource)
      .useFactory({
        factory: async () => {
          // Підключення до тестової БД
          return new DataSource({
            type: 'postgres',
            host: 'localhost',
            port: 5433,
            username: 'test_user',
            password: 'test_pass',
            database: 'test_db',
            entities: [User, Post, Order],
            synchronize: true, // Автоматично створює таблиці
            dropSchema: true, // Видаляє існуючі дані
          }).initialize();
        },
      })
      .compile();

    app = moduleFixture.createNestApplication();
    await app.init();

    dataSource = moduleFixture.get<DataSource>(DataSource);
    userRepository = dataSource.getRepository(User);
  });

  afterAll(async () => {
    // Закриваємо з'єднання з БД
    await dataSource.destroy();
    await app.close();
  });

  beforeEach(async () => {
    // Очищаємо дані між тестами
    await userRepository.clear();
  });

  it('POST /api/users should create user', async () => {
    const response = await request(app.getHttpServer())
      .post('/api/users')
      .send({ email: 'user@test.com', name: 'Test User' })
      .expect(201);

    // Перевірка у БД
    const user = await userRepository.findOne({ where: { email: 'user@test.com' } });
    expect(user).toBeDefined();
    expect(user!.name).toBe('Test User');
  });

  it('GET /api/users/:id should return user', async () => {
    // Підготовка: створюємо користувача безпосередньо через репозиторій
    const user = await userRepository.save({
      email: 'existing@test.com',
      name: 'Existing User',
    });

    // Виконуємо запит
    const response = await request(app.getHttpServer())
      .get(`/api/users/${user.id}`)
      .expect(200);

    expect(response.body.email).toBe('existing@test.com');
  });
});
```

### Seeding — попереднє заповнення даних

Для складних тестів, що вимагають багато підготовчих даних, створіть функції seeding:

```typescript
// test/seeds/user.seed.ts
export async function seedUsers(repository: Repository<User>, count: number = 5): Promise<User[]> {
  const users: User[] = [];

  for (let i = 1; i <= count; i++) {
    const user = repository.create({
      email: `user${i}@test.com`,
      name: `User ${i}`,
      role: i % 2 === 0 ? 'admin' : 'user',
    });
    users.push(await repository.save(user));
  }

  return users;
}

// Використання у тесті
describe('User filtering', () => {
  let users: User[];

  beforeAll(async () => {
    users = await seedUsers(userRepository, 10);
  });

  it('GET /api/users?role=admin should return only admins', async () => {
    const response = await request(app.getHttpServer())
      .get('/api/users')
      .query({ role: 'admin' })
      .expect(200);

    expect(response.body).toHaveLength(5); // 10 користувачів, 50% адміни
    expect(response.body.every((u: any) => u.role === 'admin')).toBe(true);
  });
});
```

### Транзакційні тести для швидкості

Для прискорення тестів можна використовувати транзакції: всі зміни виконуються у транзакції, яка відкочується після тесту:

```typescript
describe('Orders (E2E with transactions)', () => {
  let queryRunner: QueryRunner;

  beforeEach(async () => {
    // Створюємо транзакцію перед кожним тестом
    queryRunner = dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();
  });

  afterEach(async () => {
    // Відкочуємо транзакцію після тесту
    await queryRunner.rollbackTransaction();
    await queryRunner.release();
  });

  it('should create order', async () => {
    // Всі операції виконуються у транзакції
    const order = queryRunner.manager.create(Order, { /* ... */ });
    await queryRunner.manager.save(order);

    // Тест проходить, але зміни не збережуться через rollback
  });
});
```

**Переваги:** значно швидше, оскільки не потрібно фізично очищати таблиці після кожного тесту.
**Недоліки:** складніше налаштування, не працює для тестів, що перевіряють транзакційну логіку самого застосунку.

---

## Тестування критичних user flows

Розглянемо детальні приклади E2E тестів для найпоширеніших сценаріїв.

### Authentication Flow: реєстрація та вхід

```typescript
describe('Authentication Flow (E2E)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('POST /api/auth/register', () => {
    it('should register new user with valid data', async () => {
      const userData = {
        email: 'newuser@test.com',
        password: 'SecurePass123!',
        name: 'New User',
      };

      const response = await request(app.getHttpServer())
        .post('/api/auth/register')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject({
        id: expect.any(String),
        email: 'newuser@test.com',
        name: 'New User',
        access_token: expect.any(String),
      });
      expect(response.body).not.toHaveProperty('password'); // Пароль не повертається
    });

    it('should reject registration with invalid email', async () => {
      const response = await request(app.getHttpServer())
        .post('/api/auth/register')
        .send({
          email: 'invalid-email', // Невалідний email
          password: 'SecurePass123!',
          name: 'User',
        })
        .expect(400);

      expect(response.body.message).toContain('email');
    });

    it('should reject registration with weak password', async () => {
      const response = await request(app.getHttpServer())
        .post('/api/auth/register')
        .send({
          email: 'user@test.com',
          password: '123', // Занадто короткий
          name: 'User',
        })
        .expect(400);

      expect(response.body.message).toContain('password');
    });

    it('should reject duplicate email', async () => {
      const userData = {
        email: 'duplicate@test.com',
        password: 'SecurePass123!',
        name: 'User',
      };

      // Перша реєстрація успішна
      await request(app.getHttpServer())
        .post('/api/auth/register')
        .send(userData)
        .expect(201);

      // Друга реєстрація з тим самим email
      const response = await request(app.getHttpServer())
        .post('/api/auth/register')
        .send(userData)
        .expect(409); // Conflict

      expect(response.body.message).toContain('already exists');
    });
  });

  describe('POST /api/auth/login', () => {
    beforeAll(async () => {
      // Підготовка: реєструємо користувача для тестів входу
      await request(app.getHttpServer())
        .post('/api/auth/register')
        .send({
          email: 'logintest@test.com',
          password: 'LoginPass123!',
          name: 'Login Test User',
        });
    });

    it('should authenticate user with correct credentials', async () => {
      const response = await request(app.getHttpServer())
        .post('/api/auth/login')
        .send({
          email: 'logintest@test.com',
          password: 'LoginPass123!',
        })
        .expect(200);

      expect(response.body).toHaveProperty('access_token');
      expect(typeof response.body.access_token).toBe('string');
      expect(response.body.access_token.length).toBeGreaterThan(20); // JWT має бути довгим
    });

    it('should reject login with incorrect password', async () => {
      const response = await request(app.getHttpServer())
        .post('/api/auth/login')
        .send({
          email: 'logintest@test.com',
          password: 'WrongPassword',
        })
        .expect(401);

      expect(response.body.message).toContain('Invalid credentials');
    });

    it('should reject login for non-existent user', async () => {
      await request(app.getHttpServer())
        .post('/api/auth/login')
        .send({
          email: 'nonexistent@test.com',
          password: 'SomePassword123!',
        })
        .expect(401);
    });
  });

  describe('Protected endpoints', () => {
    let authToken: string;

    beforeAll(async () => {
      // Отримуємо токен для захищених endpoints
      const response = await request(app.getHttpServer())
        .post('/api/auth/login')
        .send({
          email: 'logintest@test.com',
          password: 'LoginPass123!',
        });

      authToken = response.body.access_token;
    });

    it('GET /api/profile should return user profile with valid token', async () => {
      const response = await request(app.getHttpServer())
        .get('/api/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.email).toBe('logintest@test.com');
      expect(response.body.name).toBe('Login Test User');
    });

    it('GET /api/profile should return 401 without token', async () => {
      await request(app.getHttpServer())
        .get('/api/profile')
        .expect(401);
    });

    it('GET /api/profile should return 401 with invalid token', async () => {
      await request(app.getHttpServer())
        .get('/api/profile')
        .set('Authorization', 'Bearer invalid-token-12345')
        .expect(401);
    });
  });
});
```

Цей E2E тест покриває повний authentication flow:
- Реєстрація з валідацією вхідних даних
- Перевірка унікальності email
- Вхід із коректними та некоректними credentials
- Доступ до захищених endpoints з токеном та без нього

### CRUD операції з валідацією

```typescript
describe('Posts CRUD (E2E)', () => {
  let app: INestApplication;
  let authToken: string;
  let userId: string;

  beforeAll(async () => {
    // Setup застосунку та автентифікація
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    await app.init();

    // Реєструємо користувача та отримуємо токен
    const response = await request(app.getHttpServer())
      .post('/api/auth/register')
      .send({
        email: 'author@test.com',
        password: 'AuthorPass123!',
        name: 'Author',
      });

    authToken = response.body.access_token;
    userId = response.body.id;
  });

  afterAll(async () => {
    await app.close();
  });

  describe('POST /api/posts', () => {
    it('should create new post', async () => {
      const newPost = {
        title: 'Test Post Title',
        content: 'This is test content for the post.',
        published: false,
      };

      const response = await request(app.getHttpServer())
        .post('/api/posts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(newPost)
        .expect(201);

      expect(response.body).toMatchObject({
        id: expect.any(String),
        title: 'Test Post Title',
        content: 'This is test content for the post.',
        published: false,
        authorId: userId,
        createdAt: expect.any(String),
      });
    });

    it('should reject post with empty title', async () => {
      const response = await request(app.getHttpServer())
        .post('/api/posts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          title: '', // Порожній заголовок
          content: 'Content',
        })
        .expect(400);

      expect(response.body.message).toContain('title');
    });

    it('should reject post without authentication', async () => {
      await request(app.getHttpServer())
        .post('/api/posts')
        .send({
          title: 'Title',
          content: 'Content',
        })
        .expect(401);
    });
  });

  describe('GET /api/posts', () => {
    let postId: string;

    beforeAll(async () => {
      // Створюємо пост для тестів читання
      const response = await request(app.getHttpServer())
        .post('/api/posts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          title: 'Published Post',
          content: 'Content',
          published: true,
        });

      postId = response.body.id;
    });

    it('should return list of published posts', async () => {
      const response = await request(app.getHttpServer())
        .get('/api/posts')
        .expect(200);

      expect(response.body).toBeInstanceOf(Array);
      expect(response.body.length).toBeGreaterThanOrEqual(1);
      expect(response.body[0]).toMatchObject({
        id: expect.any(String),
        title: expect.any(String),
        published: true,
      });
    });

    it('should return single post by id', async () => {
      const response = await request(app.getHttpServer())
        .get(`/api/posts/${postId}`)
        .expect(200);

      expect(response.body.id).toBe(postId);
      expect(response.body.title).toBe('Published Post');
    });

    it('should return 404 for non-existent post', async () => {
      await request(app.getHttpServer())
        .get('/api/posts/nonexistent-id-12345')
        .expect(404);
    });
  });

  describe('PATCH /api/posts/:id', () => {
    let postId: string;

    beforeEach(async () => {
      // Створюємо пост для кожного тесту оновлення
      const response = await request(app.getHttpServer())
        .post('/api/posts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          title: 'Original Title',
          content: 'Original Content',
          published: false,
        });

      postId = response.body.id;
    });

    it('should update post title', async () => {
      const response = await request(app.getHttpServer())
        .patch(`/api/posts/${postId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({ title: 'Updated Title' })
        .expect(200);

      expect(response.body.title).toBe('Updated Title');
      expect(response.body.content).toBe('Original Content'); // Не змінено
    });

    it('should publish post', async () => {
      const response = await request(app.getHttpServer())
        .patch(`/api/posts/${postId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({ published: true })
        .expect(200);

      expect(response.body.published).toBe(true);
    });

    it('should reject update without authentication', async () => {
      await request(app.getHttpServer())
        .patch(`/api/posts/${postId}`)
        .send({ title: 'New Title' })
        .expect(401);
    });
  });

  describe('DELETE /api/posts/:id', () => {
    it('should delete post', async () => {
      // Створюємо пост
      const createResponse = await request(app.getHttpServer())
        .post('/api/posts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          title: 'Post to Delete',
          content: 'Content',
        });

      const postId = createResponse.body.id;

      // Видаляємо пост
      await request(app.getHttpServer())
        .delete(`/api/posts/${postId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(204);

      // Перевіряємо, що пост більше не існує
      await request(app.getHttpServer())
        .get(`/api/posts/${postId}`)
        .expect(404);
    });

    it('should return 404 when deleting non-existent post', async () => {
      await request(app.getHttpServer())
        .delete('/api/posts/nonexistent-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);
    });
  });
});
```

Цей тест покриває повний CRUD цикл для ресурсу `posts`: створення, читання, оновлення, видалення з перевіркою валідації, автентифікації та обробки помилок.


---

## Аналіз code coverage для E2E тестів

E2E тести також генерують метрики code coverage, проте їх інтерпретація відрізняється від Unit тестів.

### Запуск E2E тестів із coverage

```bash
# E2E тести з coverage звітом
npm run test:e2e -- --coverage

# Або через Jest напряму
jest --config ./test/jest-e2e.json --coverage
```

Результат:

::terminal-preview{title="npm run test:e2e -- --coverage" :cursor="false"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">npm run test:e2e -- --coverage</strong></div>
<div class="line"></div>
<div class="line"> PASS  test/auth.e2e-spec.ts</div>
<div class="line"> PASS  test/users.e2e-spec.ts</div>
<div class="line"> PASS  test/posts.e2e-spec.ts</div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">-----------------|---------|----------|---------|---------|-------------------</span></div>
<div class="line"><span class="text-blue-400 font-bold">File             | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s</span></div>
<div class="line"><span class="text-blue-400 font-bold">-----------------|---------|----------|---------|---------|-------------------</span></div>
<div class="line">All files        |   <span class="text-green-400 font-bold">78.2</span>   |   <span class="text-yellow-400 font-bold">65.3</span>    |  <span class="text-green-400 font-bold">82.1</span>   |  <span class="text-green-400 font-bold">79.5</span>   |</div>
<div class="line"> auth            |   <span class="text-green-400 font-bold">85.0</span>   |   <span class="text-yellow-400 font-bold">75.0</span>    |  <span class="text-green-400 font-bold">90.0</span>   |  <span class="text-green-400 font-bold">86.0</span>   |</div>
<div class="line">  auth.service   |   <span class="text-green-400 font-bold">85.0</span>   |   <span class="text-yellow-400 font-bold">75.0</span>    |  <span class="text-green-400 font-bold">90.0</span>   |  <span class="text-green-400 font-bold">86.0</span>   | 45,67</div>
<div class="line"> users           |   <span class="text-green-400 font-bold">80.5</span>   |   <span class="text-yellow-400 font-bold">70.0</span>    |  <span class="text-green-400 font-bold">85.0</span>   |  <span class="text-green-400 font-bold">81.2</span>   |</div>
<div class="line">  user.service   |   <span class="text-green-400 font-bold">80.5</span>   |   <span class="text-yellow-400 font-bold">70.0</span>    |  <span class="text-green-400 font-bold">85.0</span>   |  <span class="text-green-400 font-bold">81.2</span>   | 23,56-58</div>
<div class="line"> posts           |   <span class="text-yellow-400 font-bold">72.3</span>   |   <span class="text-rose-400 font-bold">55.0</span>    |  <span class="text-green-400 font-bold">78.0</span>   |  <span class="text-yellow-400 font-bold">73.1</span>   |</div>
<div class="line">  post.service   |   <span class="text-yellow-400 font-bold">72.3</span>   |   <span class="text-rose-400 font-bold">55.0</span>    |  <span class="text-green-400 font-bold">78.0</span>   |  <span class="text-yellow-400 font-bold">73.1</span>   | 12,34,78-82</div>
<div class="line"><span class="text-blue-400 font-bold">-----------------|---------|----------|---------|---------|-------------------</span></div>
<div class="line"></div>
<div class="line"><span class="text-green-400 font-bold">Test Suites: 3 passed</span>, 3 total</div>
<div class="line"><span class="text-green-400 font-bold">Tests:       28 passed</span>, 28 total</div>

::

### Комбінування coverage: Unit + E2E

Щоб отримати **загальний coverage** від усіх типів тестів, налаштуйте Jest для збереження проміжних результатів:

```json
// package.json
{
  "scripts": {
    "test:unit": "jest --coverage --coverageDirectory=coverage/unit",
    "test:e2e": "jest --config ./test/jest-e2e.json --coverage --coverageDirectory=coverage/e2e",
    "test:all": "npm run test:unit && npm run test:e2e && npm run coverage:merge"
  }
}
```

Потім використовуйте утиліту `nyc` для об'єднання звітів:

```bash
npm install --save-dev nyc

# Об'єднання coverage звітів
npx nyc merge coverage/unit coverage/e2e --reporter=lcov --report-dir=coverage/combined
```

Це дасть повну картину: який код покритий Unit тестами, який — E2E, а який взагалі не покритий.

### Інтерпретація E2E coverage

**Важливе зауваження:** E2E coverage зазвичай **нижчий** за Unit coverage, і це нормально. Чому?

1. **E2E тести не покривають всі edge cases.** Unit тест може перевірити 10 різних сценаріїв валідації email, тоді як E2E тест перевірить лише 1-2 основні.

2. **E2E тести фокусуються на happy paths.** Вони перевіряють критичні user flows, а не всі можливі комбінації помилок.

3. **Деякий код не викликається через HTTP.** Наприклад, утиліти для логування, обробки внутрішніх подій, CLI команди — все це не покривається E2E тестами.

**Рекомендовані показники:**

::card-group

::card{title="✅ Unit Coverage Target" icon="i-lucide-check-circle"}

- **Statement:** 80-90%
- **Branch:** 75-85%
- **Function:** 85-95%
- **Line:** 80-90%

::

::card{title="✅ E2E Coverage Target" icon="i-lucide-globe"}

- **Statement:** 60-75%
- **Branch:** 50-65%
- **Function:** 65-80%
- **Line:** 60-75%

::

::card{title="✅ Combined Coverage Target" icon="i-lucide-layers"}

- **Statement:** 85-95%
- **Branch:** 80-90%
- **Function:** 90-95%
- **Line:** 85-95%

::

::

Комбінований coverage (Unit + E2E) має бути високим, тоді як окремо E2E coverage може бути помірним.

### Налаштування coverage thresholds

Встановіть мінімальні пороги для блокування CI/CD при недостатньому покритті:

```javascript
// jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 85,
      lines: 85,
      statements: 85,
    },
    './src/auth/': {
      // Критичні модулі мають вищі вимоги
      branches: 90,
      functions: 95,
      lines: 90,
      statements: 90,
    },
  },
};
```

Якщо coverage падає нижче порогів, Jest повертає non-zero exit code, що призведе до провалу CI/CD pipeline.

---

## Інтеграція E2E тестів у CI/CD

Для повної впевненості E2E тести мають запускатися автоматично при кожному push або pull request у CI/CD системі.

### GitHub Actions приклад

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  unit-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Unit tests
        run: npm run test:cov

      - name: Upload Unit coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          flags: unit

  e2e-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run E2E tests
        run: npm run test:e2e -- --coverage
        env:
          DB_HOST: localhost
          DB_PORT: 5432
          DB_USER: test_user
          DB_PASSWORD: test_password
          DB_NAME: test_db
          NODE_ENV: test

      - name: Upload E2E coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          flags: e2e
```

**Ключові моменти:**

1. **Окремі jobs для Unit та E2E.** Unit тести виконуються швидше та не вимагають БД, тому можуть запускатися паралельно.

2. **Docker PostgreSQL через services.** GitHub Actions автоматично запускає PostgreSQL контейнер для E2E тестів.

3. **Health checks.** Перед запуском тестів GitHub чекає, поки PostgreSQL повністю завантажиться (`pg_isready`).

4. **Змінні оточення.** БД credentials передаються через `env` секцію.

5. **Coverage upload.** Результати coverage автоматично завантажуються до Codecov або іншого сервісу для відстеження тенденцій.

### Стратегії для довгих E2E тестів

Якщо E2E тести виконуються довго (10+ хвилин), розгляньте оптимізації:

**1. Паралельне виконання:**

```json
// jest-e2e.json
{
  "maxWorkers": 4 // Запускає 4 тести паралельно
}
```

**2. Selective testing:** запускайте E2E тести лише для змінених модулів:

```yaml
- name: Run E2E tests for changed modules
  run: |
    CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | grep '^src/')
    if echo "$CHANGED_FILES" | grep 'src/auth/'; then
      npm run test:e2e -- auth.e2e-spec.ts
    fi
```

**3. Nightly builds:** запускайте повний набір E2E тестів лише раз на добу (вночі), а при кожному PR — лише smoke tests.

---

## Висновки та best practices

::card-group

::card{title="✅ Фокус на критичних flows" icon="i-lucide-workflow"}

E2E тести мають покривати **найважливіші бізнес-сценарії**: реєстрація, вхід, оплата, створення замовлень. Не намагайтеся протестувати всі edge cases через E2E — це завдання Unit тестів.

::

::card{title="✅ Ізолюйте тестову БД" icon="i-lucide-database"}

Використовуйте окрему БД для тестів, очищайте дані між тестами через `beforeEach()` або транзакційний rollback. Ніколи не запускайте тести на production БД.

::

::card{title="✅ Відтворюйте production конфігурацію" icon="i-lucide-settings"}

Налаштовуйте `INestApplication` у тестах ідентично до `main.ts`: ті самі pipes, guards, interceptors, middleware. Інакше тести не відображатимуть реальну поведінку.

::

::card{title="✅ Комбінуйте з Unit тестами" icon="i-lucide-layers"}

E2E тести не замінюють Unit тести. Використовуйте E2E для перевірки інтеграції, а Unit — для детальної перевірки логіки. Комбінований coverage має бути 85-95%.

::

::

**Практичне завдання:** Створіть E2E тести для blog платформи з наступними flows:
1. **Authentication:** реєстрація, вхід, отримання профілю, вихід.
2. **Posts CRUD:** створення поста (authenticated), читання списку постів (public), оновлення власного поста, видалення.
3. **Comments:** додавання коментаря до поста (authenticated), читання коментарів (public), видалення власного коментаря.
4. **Authorization:** спроба редагувати чужий пост має повертати `403 Forbidden`.

Налаштуйте тестову БД (PostgreSQL у Docker або SQLite in-memory), забезпечте cleanup між тестами, досягніть E2E coverage 65%+ для критичних модулів.

::accordion

::accordion-item{label="❓ Чи потрібно мокувати зовнішні API у E2E тестах?" icon="i-lucide-help-circle"}

**Це залежить від типу API та вашої стратегії.**

**Підхід 1: Моки для зовнішніх сервісів (рекомендовано для більшості випадків)**

Якщо ваш застосунок викликає зовнішні API (платіжні шлюзи, email-сервіси, SMS-провайдери), рекомендується мокувати їх у E2E тестах:

```typescript
beforeAll(async () => {
  const moduleFixture = await Test.createTestingModule({
    imports: [AppModule],
  })
    .overrideProvider(PaymentGateway)
    .useValue({
      charge: jest.fn().mockResolvedValue({ id: 'pay-123', status: 'success' }),
    })
    .compile();
  
  // ...
});
```

**Переваги:**
- Тести виконуються швидше (без реальних мережевих запитів).
- Не залежать від доступності зовнішніх сервісів.
- Не витрачають гроші (реальні платежі у sandbox).
- Можна легко симулювати помилки (timeout, declined card).

**Підхід 2: Реальні виклики до sandbox API**

Для критичних інтеграцій (наприклад, платіжний шлюз) створіть окремі **Integration тести**, що використовують **sandbox оточення** зовнішнього сервісу:

```typescript
it('should process real payment through Stripe sandbox', async () => {
  const response = await request(app.getHttpServer())
    .post('/api/orders/pay')
    .send({ 
      amount: 100, 
      paymentMethod: 'tok_visa' // Stripe test token
    })
    .expect(200);

  expect(response.body.paymentStatus).toBe('success');
});
```

Ці тести запускайте рідше (наприклад, перед кожним релізом), а не при кожному commit.

::

::accordion-item{label="❓ Як тестувати WebSocket endpoints у E2E?" icon="i-lucide-help-circle"}

Для тестування WebSocket з'єднань використовуйте клієнт `socket.io-client`:

```bash
npm install --save-dev socket.io-client
```

```typescript
import { io, Socket } from 'socket.io-client';

describe('WebSocket Chat (E2E)', () => {
  let socket: Socket;

  beforeAll(async () => {
    // Підключення до WebSocket сервера
    socket = io('http://localhost:3000', {
      auth: { token: authToken },
    });

    await new Promise((resolve) => {
      socket.on('connect', resolve);
    });
  });

  afterAll(() => {
    socket.disconnect();
  });

  it('should send and receive chat message', (done) => {
    const testMessage = { room: 'general', text: 'Hello, World!' };

    // Підписка на відповідь
    socket.on('message:received', (data) => {
      expect(data.text).toBe('Hello, World!');
      expect(data.room).toBe('general');
      done();
    });

    // Відправка повідомлення
    socket.emit('message:send', testMessage);
  });
});
```

Зверніть увагу: WebSocket тести часто асинхронні та вимагають `done()` callback або `async/await` з `Promise`.

::

::
