# РОБОЧА ПРОГРАМА НАВЧАЛЬНОЇ ДИСЦИПЛІНИ

## «РОЗРОБКА WEB-ЗАСТОСУВАНЬ»

---

## 1. ОПИС НАВЧАЛЬНОЇ ДИСЦИПЛІНИ

| Параметр | Значення |
|---|---|
| **Галузь знань** | 12 — Інформаційні технології |
| **Спеціальність** | 121 — Інженерія програмного забезпечення |
| **Освітній рівень** | Бакалавр |
| **Курс** | 4 |
| **Кількість кредитів ЄКТС** | 4 |
| **Загальна кількість годин** | 120 |
| **Лекції** | 30 год (15 занять × 2 акад. год) |
| **Практичні заняття** | 26 год (13 занять × 2 акад. год, у т.ч. 2 контрольні роботи) |
| **Самостійна робота** | 64 год |
| **Форма підсумкового контролю** | Екзамен |
| **Мова викладання** | Українська |

> Одна пара (заняття) має тривалість 1 год 10 хв (70 хвилин) та обліковується як 2 академічні години.

---

## 2. МЕТА ТА ЗАВДАННЯ ДИСЦИПЛІНИ

### 2.1. Мета дисципліни

Формування у студентів фундаментальних теоретичних знань та стійких практичних навичок проєктування, розроблення, захисту, тестування та супроводу серверної частини сучасних масштабованих вебзастосувань.

### 2.2. Завдання дисципліни

Завдання навчальної дисципліни «Розробка WEB-застосувань» полягають у формуванні у студентів теоретичних знань та практичних навичок щодо:
- функціонування комп'ютерних мереж, стеку протоколів TCP і IP, протоколів HTTP, HTTPS та взаємодії клієнта і сервера;
- побудови модульної архітектури серверних систем з використанням принципів Dependency Injection, конвеєра обробки запитів та архітектурного стилю REST;
- взаємодії з реляційними базами даних через технології ORM, використання патерну Repository, транзакцій та міграцій схеми даних;
- застосування stateful та stateless підходів, збереження стану за допомогою cookies, сесій та JWT токенів;
- організації безпеки вебзастосувань, впровадження автентифікації, протоколу OAuth 2.0, моделей доступу RBAC і ABAC та захисту від загроз OWASP;
- реалізації асинхронних черг фонових задач, планувальників і комунікації в реальному часі через WebSocket та Server-Sent Events;
- верифікації коду за допомогою модульного й наскрізного тестування, генерації специфікації Swagger і OpenAPI, використання контейнеризації Docker.

### 2.3. Очікувані результати навчання

У результаті вивчення навчальної дисципліни студент повинен:
- проєктувати багатошарову архітектуру серверних вебзастосувань та розробляти стандартизовані REST API;
- ефективно застосовувати стек протоколів TCP і IP, протокол HTTP, керуючі заголовки та механізми збереження стану (cookies, сесії, токени);
- моделювати схеми баз даних і реалізовувати операції з персистентними даними за допомогою ORM, зв'язків між сутностями та міграцій;
- впроваджувати комплексну систему безпеки, автентифікацію на основі JWT токенів і OAuth 2.0, авторизацію за ролями (RBAC) та атрибутами (ABAC);
- налаштовувати захист від кібератак (CSRF, XSS, ін'єкції) та обмежувати частоту запитів за допомогою Rate Limiting;
- організовувати двосторонню взаємодію у реальному часі через WebSocket, потокові події Server-Sent Events та обробку фонових завдань у чергах;
- розробляти автоматизовані Unit та E2E тести для всебічної перевірки надійності серверного коду;
- документувати програмні інтерфейси за стандартом OpenAPI і Swagger та готувати вебзастосунки до розгортання засобами Docker.

### 2.4. Пререквізити

- Основи об'єктно-орієнтованого програмування, базові алгоритми та структури даних;
- Базові знання синтаксису мов вебпрограмування;
- Основи реляційних баз даних та декларативної мови запитів SQL;
- Практичні навички роботи із системами контролю версій вихідного коду.

---

## 3. ПРОГРАМА НАВЧАЛЬНОЇ ДИСЦИПЛІНИ

### Розділ 1. Мережеві технології, TypeScript та основи NestJS

**Тема 1. Архітектура комп'ютерних мереж та мережеві протоколи**  
Багаторівневі моделі мережевої взаємодії OSI та TCP/IP. Адресація, порти та сокети. Протоколи транспортного рівня TCP та UDP. Прикладні протоколи DNS, SMTP, WebSocket та SSH. Концепція клієнт-серверної архітектури серверної частини вебзастосунків.

**Тема 2. Протокол HTTP та захищена передача даних HTTPS**  
Структура запитів і відповідей протоколу HTTP. Методи запитів, їхня семантика та ідемпотентність. Класифікація кодів відповідей та керуючі заголовки. Механізми безпеки: політика одного джерела та CORS, протокол HTTPS (TLS). Збереження стану засобами Cookies, сесій та токенів.

**Тема 3. Система типів мови TypeScript**  
Статична типізація у веброзробці. Примітивні, спеціальні та об'єктні типи даних. Об'єднання (Union), перетини (Intersection) та літеральні типи. Звуження типів (Type Narrowing), типізація функцій та конфігурація компілятора.

**Тема 4. Розширені засоби мови TypeScript**  
Оголошення та наслідування інтерфейсів і класів. Узагальнені типи (Generics) та обмеження типів. Метапрограмування на основі декораторів. Вбудовані службові типи (Utility Types), перерахування (Enum) та організація модульної структури.

**Тема 5. Платформа Node.js як середовище виконання серверних застосунків**  
Архітектура платформи Node.js: рушій V8, бібліотека libuv та однопотокова модель із циклом подій (Event Loop). Модульні системи CommonJS та ES Modules. Вбудовані модулі для роботи з файловою системою, потоками даних (Streams) та мережевими з'єднаннями.

**Тема 6. Асинхронне програмування у Node.js**  
Парадигми асинхронної обробки: зворотні виклики (Callbacks), проміси (Promises) та синтаксис Async/Await. Подієво-орієнтований патерн EventEmitter. Багатопотокова та фонова обробка засобами Worker Threads і Child Processes.

**Тема 7. Фреймворк NestJS. Контролери та маршрутизація**  
Архітектурні засади NestJS та реалізація інверсії керування (IoC) й ін'єкції залежностей (DI). Контролери як рівень обробки HTTP-запитів. Декоратори маршрутизації, параметризація запитів та об'єкти передачі даних (DTO).

### Розділ 2. Серверна розробка з NestJS

**Тема 8. Провайдери, сервіси та модульна система NestJS**  
Провайдери та інкапсуляція бізнес-логіки у сервісах. Спеціалізовані провайдери та області їхньої видимості (Scopes). Модульна декомпозиція застосунку: функціональні, спільні, глобальні та динамічні модулі. Хуки життєвого циклу компонентів.

**Тема 9. Валідація даних та конвеєр обробки запитів у NestJS**  
Конвеєр обробки запитів (Request Pipeline). Автоматична валідація та трансформація даних за допомогою Pipes та бібліотеки class-validator. Проміжні обробники (Middleware), захисні гварди доступу (Guards), інтерцептори (Interceptors) та фільтри виключень (Exception Filters).

**Тема 10. Інтеграція реляційних баз даних засобами TypeORM**  
Концепція об'єктно-реляційного відображення (ORM). Налаштування підключення до PostgreSQL через TypeOrmModule. Оголошення сутностей (Entities), типи колонок та автозгенеровані стовпці. Реалізація патерну Repository для виконання операцій CRUD та пагінації.

**Тема 11. Зв'язки між сутностями, міграції та оптимізація запитів**  
Моделювання зв'язків One-to-One, One-to-Many, Many-to-Many та каскадні операції. Стратегії завантаження пов'язаних даних. Керування схемою бази даних за допомогою міграцій. Формування складних запитів, транзакції та індексація засобами QueryBuilder.

**Тема 12. Механізми автентифікації у вебзастосунках**  
Автентифікація на основі сесій та токенів. Структура і життєвий цикл JSON Web Token (JWT). Інтеграція стратегій Passport.js (Local, JWT). Хешування паролів та механізми оновлення токенів (Refresh Tokens). Потоки авторизації сторонніми провайдерами за протоколом OAuth 2.0.

**Тема 13. Авторизація та безпека серверних застосунків**  
Моделі розмежування доступу: рольова (RBAC) та атрибутивна (ABAC/CASL) авторизація. Налаштування політики CORS, захисних HTTP-заголовків (Helmet) та обмеження частоти запитів (Rate Limiting). Захист від поширених вразливостей (XSS, CSRF, Injection).

**Тема 14. Комунікація у реальному часі, нотифікації та фонові задачі**  
Організація двостороннього зв'язку через WebSocket Gateways та потокової передачі подій (SSE). Архітектура систем нотифікацій (Email через SMTP/Nodemailer, Web Push). Черги асинхронних завдань на основі Redis (Bull) та планувальники періодичних задач (Schedulers/Cron).

**Тема 15. Тестування, документування та розгортання застосунків**  
Стратегія тестування: модульні (Unit) та наскрізні (E2E) тести з використанням Jest і Supertest. Автоматична генерація інтерактивної документації API за стандартом Swagger/OpenAPI. Контейнеризація за допомогою Docker та налаштування процесів безперервної інтеграції (CI/CD).

---

## 4. ТЕМАТИЧНИЙ ПЛАН ДИСЦИПЛІНИ

### 4.1. Розподіл навчального часу за темами

| № | Тема | Лекції | Практ. | Сам. р. | Разом |
|---|---|:---:|:---:|:---:|:---:|
| | **Модуль 1. Мережеві технології, TypeScript та основи NestJS** | | | | |
| 1 | Архітектура комп'ютерних мереж та мережеві протоколи | 2 | — | 4 | 6 |
| 2 | Протокол HTTP та захищена передача даних HTTPS | 2 | 2 | 4 | 8 |
| 3 | Система типів мови TypeScript | 2 | 2 | 4 | 8 |
| 4 | Розширені засоби мови TypeScript | 2 | 2 | 4 | 8 |
| 5 | Платформа Node.js як середовище виконання серверних застосунків | 2 | — | 4 | 6 |
| 6 | Асинхронне програмування у Node.js | 2 | — | 4 | 6 |
| 7 | Фреймворк NestJS. Контролери та маршрутизація | 2 | 2 | 4 | 8 |
| | **Модульна контрольна робота № 1** | — | 2 | — | 2 |
| | **Разом за модулем 1** | **14** | **10** | **28** | **52** |
| | **Модуль 2. Серверна розробка з NestJS** | | | | |
| 8 | Провайдери, сервіси та модульна система NestJS | 2 | 2 | 4 | 8 |
| 9 | Валідація даних та конвеєр обробки запитів у NestJS | 2 | 2 | 4 | 8 |
| 10 | Інтеграція реляційних баз даних засобами TypeORM | 2 | 2 | 5 | 9 |
| 11 | Зв'язки між сутностями, міграції та оптимізація запитів | 2 | 2 | 5 | 9 |
| 12 | Механізми автентифікації у вебзастосунках | 2 | 2 | 4 | 8 |
| 13 | Авторизація та безпека серверних застосунків | 2 | — | 5 | 7 |
| 14 | Комунікація у реальному часі, нотифікації та фонові задачі | 2 | 2 | 5 | 9 |
| | **Модульна контрольна робота № 2** | — | 2 | — | 2 |
| 15 | Тестування, документування та розгортання застосунків | 2 | 2 | 4 | 8 |
| | **Разом за модулем 2** | **16** | **16** | **36** | **68** |
| | **Разом** | **30** | **26** | **64** | **120** |

---

## 5. ЗМІСТ ЛЕКЦІЙНОГО КУРСУ

---

### Лекція 1. Архітектура комп'ютерних мереж та мережеві протоколи
**(2 год)**

1. Еволюція веброзробки: від статичних сторінок до мікросервісів.
2. Модель взаємодії клієнт-сервер. Багатошарова архітектура (presentation, business logic, data access).
3. Поняття backend та frontend. Роль серверної частини у вебзастосунку.
4. Еталонна модель OSI: сім рівнів, інкапсуляція, протоколи кожного рівня.
5. Стек протоколів TCP/IP: порівняння з OSI, практичне застосування.
6. IP-адресація (IPv4, IPv6), порти, сокети. Протоколи TCP та UDP.
7. DNS: ієрархія, типи записів (A, AAAA, CNAME, MX, TXT), процес резолвінгу.
8. Протокол SMTP: призначення, команди (HELO, MAIL FROM, RCPT TO, DATA). MIME-типи. POP3 vs IMAP.
9. Протокол WebSocket: мотивація, відмінності від HTTP, повнодуплексний зв'язок, рукостискання (Upgrade), фрейми.
10. SSH: безпечний віддалений доступ, автентифікація за ключами, тунелювання.
11. Огляд сучасних серверних технологій: Node.js, Python (Django, Flask), Java (Spring), Go.

**Ключові поняття:** клієнт-сервер, OSI, TCP/IP, DNS, SMTP, WebSocket, SSH, IP-адреса, порт, сокет.

---

### Лекція 2. Протокол HTTP та захищена передача даних HTTPS
**(2 год)**

1. Протокол HTTP: історія версій (HTTP/1.0, HTTP/1.1, HTTP/2, HTTP/3 — QUIC).
2. Структура HTTP-запиту: стартовий рядок (request line), заголовки, тіло.
3. Структура HTTP-відповіді: статусний рядок (status line), заголовки, тіло.
4. Методи HTTP: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS. Ідемпотентність та безпечність методів.
5. Коди відповідей HTTP: класифікація (1xx — інформаційні, 2xx — успіх, 3xx — перенаправлення, 4xx — помилка клієнта, 5xx — помилка сервера). Найпоширеніші коди.
6. Заголовки запитів та відповідей: Content-Type, Accept, Authorization, Cache-Control, User-Agent, Set-Cookie.
7. CORS (Cross-Origin Resource Sharing): Same-Origin Policy, preflight-запити, CORS-заголовки.
8. HTTPS: протокол TLS (Transport Layer Security), сертифікати, процес рукостискання, шифрування.
9. Механізми збереження стану: Cookie (атрибути: HttpOnly, Secure, SameSite, Path, Expires), Session, Token.
10. Інструменти тестування та аналізу HTTP: Postman, cURL, HTTPie, DevTools (вкладка Network).
11. Формати обміну даними: JSON, XML, Form Data, Multipart.

**Ключові поняття:** HTTP, HTTPS, TLS, метод, код відповіді, заголовок, CORS, Cookie, Session, Token, JSON.

---

### Лекція 3. Система типів мови TypeScript
**(2 год)**

1. TypeScript як надмножина JavaScript: мотивація, переваги статичної типізації.
2. Встановлення та конфігурація: Node.js, npm, tsc. Файл `tsconfig.json`: ключові параметри (`target`, `module`, `strict`, `outDir`, `rootDir`).
3. Примітивні типи: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`.
4. Спеціальні типи: `any`, `unknown`, `void`, `never`. Відмінності `any` та `unknown`.
5. Масиви та кортежі (Tuple). Типізація масивів: `number[]` vs `Array<number>`.
6. Об'єктні типи. Type aliases (`type`). Index signatures.
7. Union types (`|`), Intersection types (`&`). Практичні сценарії.
8. Literal types. Тип `as const`. Template literal types.
9. Type narrowing: `typeof`, `instanceof`, `in`, discriminated unions.
10. Type assertions (`as`). Non-null assertion (`!`). Коли та як використовувати.
11. Функції: типізація параметрів, значень повернення, optional та default параметри, rest parameters.
12. Перевантаження функцій (function overloads). Стрілкові функції.

**Ключові поняття:** статична типізація, type alias, union type, intersection type, type narrowing, type assertion, literal type.

---

### Лекція 4. Розширені засоби мови TypeScript
**(2 год)**

1. Інтерфейси (`interface`): оголошення, розширення (`extends`), злиття декларацій (declaration merging).
2. Порівняння `interface` та `type`: коли що використовувати. Практичні рекомендації.
3. Класи в TypeScript: модифікатори доступу (`public`, `private`, `protected`, `readonly`).
4. Абстрактні класи та абстрактні методи. Реалізація інтерфейсів (`implements`).
5. Generics: generic-функції, generic-класи, generic-інтерфейси. Constraints (`extends`). Default type parameters.
6. Перерахування (`enum`): числові, рядкові, const enum. Переваги та недоліки.
7. Декоратори: декоратори класів, методів, властивостей, параметрів. Фабрики декораторів. `experimentalDecorators` та `emitDecoratorMetadata`.
8. Utility types: `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `Readonly<T>`, `ReturnType<T>`, `Exclude<T, U>`, `Extract<T, U>`.
9. Mapped types: `[K in keyof T]`. Conditional types: `T extends U ? X : Y`. Infer keyword.
10. Модульна система: `import`/`export`, named та default exports, barrel files (`index.ts`).
11. Strict mode: `strictNullChecks`, `strictFunctionTypes`, `noImplicitAny`, `noImplicitReturns`.

**Ключові поняття:** interface, generics, enum, decorator, utility types, mapped types, conditional types, strict mode.

---

### Лекція 5. Платформа Node.js як середовище виконання серверних застосунків
**(2 год)**

1. Що таке Node.js: рушій V8, libuv, однопотокова модель з неблокуючим I/O.
2. Історія Node.js. Версії LTS та Current. Відмінності від браузерного JavaScript.
3. Глобальні об'єкти: `global`, `process`, `console`, `__dirname`, `__filename`, `Buffer`, `setTimeout`/`setInterval`.
4. Event Loop: фази (timers, pending callbacks, poll, check, close callbacks). Мікро- та макрозадачі. `process.nextTick()`, `setImmediate()`.
5. Модульна система: CommonJS (`require`/`module.exports`) vs ES Modules (`import`/`export`). Відмінності, інтероперабельність.
6. npm та package.json: ініціалізація проєкту, залежності (`dependencies`, `devDependencies`), скрипти, семантичне версіонування (semver). Lock-файли.
7. Вбудовані модулі: `path` (маніпуляції зі шляхами), `os` (системна інформація), `url` (парсинг URL), `crypto` (хешування, шифрування).
8. Модуль `http`: створення HTTP-сервера без фреймворків. Обробка запитів та відповідей.
9. Модуль `fs`: читання та запис файлів (синхронний та асинхронний API). `fs/promises`.
10. Робота з потоками (Streams): Readable, Writable, Duplex, Transform. Piping. Практичне застосування.
11. Менеджери версій Node.js: nvm, fnm. Інструменти: nodemon, ts-node, tsx.

**Ключові поняття:** V8, libuv, Event Loop, CommonJS, ES Modules, npm, semver, Stream, Buffer.

---

### Лекція 6. Асинхронне програмування у Node.js
**(2 год)**

1. Синхронний vs асинхронний код: блокування потоку, наслідки для продуктивності.
2. Callbacks: патерн Error-First Callback. Callback Hell (Pyramid of Doom).
3. Promises: стани (pending, fulfilled, rejected). Створення (`new Promise`), ланцюжки (`.then`, `.catch`, `.finally`).
4. Комбінатори Promise: `Promise.all()`, `Promise.allSettled()`, `Promise.race()`, `Promise.any()`.
5. Async/Await: синтаксичний цукор над Promises. Обробка помилок (`try/catch`).
6. Паралельне vs послідовне виконання асинхронних операцій. Практичні патерни.
7. EventEmitter: патерн «Спостерігач» (Observer) у Node.js. Створення власних подій, підписка (`on`, `once`, `off`), `emit`.
8. Worker Threads: багатопотоковість у Node.js. `worker_threads` модуль. Коли використовувати.
9. Child Processes: `child_process` модуль (`exec`, `spawn`, `fork`). Делегування CPU-інтенсивних задач.
10. Обробка помилок у Node.js: `uncaughtException`, `unhandledRejection`, graceful shutdown.
11. Порівняння фреймворків для Node.js: Express, Fastify, Koa, Hapi, NestJS — архітектура, продуктивність, екосистема.

**Ключові поняття:** callback, Promise, async/await, EventEmitter, Worker Threads, Child Process, graceful shutdown.

---

### Лекція 7. Фреймворк NestJS. Контролери та маршрутизація
**(2 год)**

1. NestJS: філософія, архітектура, натхнення Angular. TypeScript-first підхід.
2. Ядро NestJS: модулі (`@Module`), контролери (`@Controller`), провайдери (`@Injectable`).
3. Ін'єкція залежностей (Dependency Injection): IoC-контейнер, принцип інверсії залежностей (DIP).
4. NestJS CLI: встановлення, створення проєкту (`nest new`), генерація компонентів (`nest generate`).
5. Структура проєкту NestJS: `main.ts`, `app.module.ts`, `app.controller.ts`, `app.service.ts`. Конвенції іменування.
6. Контролери: роль в архітектурі. Декоратори маршрутів: `@Get()`, `@Post()`, `@Put()`, `@Patch()`, `@Delete()`.
7. Параметри маршруту: `@Param()`, `@Query()`, `@Body()`, `@Headers()`.
8. DTO (Data Transfer Objects): визначення, застосування для типізації вхідних даних. Відмінність від Entity.
9. Об'єкти Request та Response. Декоратори `@Req()`, `@Res()`. Library-specific vs Standard approach.
10. HTTP-статус коди: `@HttpCode()`, `@Header()`, `@Redirect()`.
11. Асинхронні обробники: робота з `Promise` та `Observable`. Wildcard routes.

**Ключові поняття:** NestJS, IoC, Dependency Injection, Module, Controller, Provider, DTO, routing.

---

### Лекція 8. Провайдери, сервіси та модульна система NestJS
**(2 год)**

1. Провайдери: концепція, декоратор `@Injectable()`, реєстрація у модулі.
2. Сервіси як основні провайдери: інкапсуляція бізнес-логіки, розділення відповідальностей.
3. Custom Providers: `useValue`, `useClass`, `useFactory`, `useExisting`. Практичні сценарії.
4. Injection tokens: рядкові та символьні токени. Декоратор `@Inject()`.
5. Scope провайдерів: `DEFAULT` (singleton), `REQUEST`, `TRANSIENT`. Вплив на продуктивність.
6. Модулі: структура `@Module()` — `imports`, `controllers`, `providers`, `exports`.
7. Feature modules: ізоляція функціональності. Генерація модулів через CLI.
8. Shared modules та реекспорт. `@Global()` модулі: переваги та ризики.
9. Dynamic modules: патерн `forRoot()`, `forRootAsync()`, `forFeature()`. Конфігурація модулів.
10. Circular dependencies: проблема, `forwardRef()` як рішення.
11. Життєвий цикл додатку NestJS: хуки `onModuleInit`, `onModuleDestroy`, `onApplicationBootstrap`, `onApplicationShutdown`.

**Ключові поняття:** Provider, Service, Custom Provider, Scope, Module, Dynamic Module, Lifecycle hooks.

---

### Лекція 9. Валідація даних та конвеєр обробки запитів у NestJS
**(2 год)**

1. Pipes: концепція, вбудовані pipes (`ValidationPipe`, `ParseIntPipe`, `ParseUUIDPipe`, `DefaultValuePipe`).
2. Бібліотеки `class-validator` та `class-transformer`: декоратори валідації (`@IsString()`, `@IsEmail()`, `@Min()`, `@MaxLength()`, `@IsOptional()`, `@ValidateNested()`).
3. Глобальна валідація: `app.useGlobalPipes()`. Опції: `whitelist`, `transform`, `forbidNonWhitelisted`.
4. Custom Pipes: створення власних pipes для трансформації та валідації даних.
5. Middleware: функціональний та класовий підхід. Реєстрація в модулі через `NestModule.configure()`.
6. Порівняння middleware NestJS з Express middleware. Порядок виконання. Глобальний middleware.
7. Guards: інтерфейс `CanActivate`, `ExecutionContext`. Рівні застосування: глобальний, контролерний, маршрутний.
8. Interceptors: інтерфейс `NestInterceptor`, `CallHandler`, `Observable`. Use cases: логування, кешування, трансформація відповіді, timeout.
9. Exception Filters: вбудовані виключення (`HttpException`, `NotFoundException`, `BadRequestException`). Custom Exception Filters.
10. Request Pipeline — порядок виконання: Middleware → Guards → Interceptors (before) → Pipes → Handler → Interceptors (after) → Exception Filters.

**Ключові поняття:** Pipe, Middleware, Guard, Interceptor, Exception Filter, ValidationPipe, Request Pipeline.

---

### Лекція 10. Інтеграція реляційних баз даних засобами TypeORM
**(2 год)**

1. Реляційні бази даних: таблиці, стовпці, типи даних, первинні та зовнішні ключі. Нормалізація.
2. PostgreSQL: встановлення (Docker), psql, pgAdmin. Основні SQL-команди (DDL, DML).
3. ORM (Object-Relational Mapping): концепція, переваги та недоліки порівняно з raw SQL.
4. TypeORM: встановлення, підключення до PostgreSQL у NestJS (`TypeOrmModule.forRoot()`). Конфігурація через `ConfigModule`.
5. Entity: декоратор `@Entity()`, `@Column()`, `@PrimaryGeneratedColumn()` (uuid, increment).
6. Типи колонок: string, number, boolean, date, enum, json, jsonb, array. Nullable, default values.
7. Автоматичні колонки: `@CreateDateColumn()`, `@UpdateDateColumn()`, `@DeleteDateColumn()` (Soft Delete). `@VersionColumn()`.
8. Repository Pattern: `@InjectRepository()`, базові методи (`find`, `findOne`, `findOneBy`, `save`, `remove`, `update`, `delete`).
9. `TypeOrmModule.forFeature()`: реєстрація Entity у Feature Modules.
10. Пагінація: offset-based (`skip`, `take`) та cursor-based підходи. Фільтрація та сортування.

**Ключові поняття:** PostgreSQL, ORM, TypeORM, Entity, Repository, Column, PrimaryGeneratedColumn, Soft Delete.

---

### Лекція 11. Зв'язки між сутностями, міграції та оптимізація запитів
**(2 год)**

1. Типи зв'язків: One-to-One (`@OneToOne`, `@JoinColumn`), One-to-Many / Many-to-One (`@OneToMany`, `@ManyToOne`), Many-to-Many (`@ManyToMany`, `@JoinTable`).
2. Eager vs Lazy loading. Параметр `eager: true`. Опція `relations` у `find()`.
3. Cascade operations: `cascade: true`, типи каскадів (`insert`, `update`, `remove`). `onDelete`, `onUpdate`.
4. Міграції: навіщо потрібні, чому `synchronize: true` — лише для розробки.
5. CLI для міграцій: `migration:generate`, `migration:create`, `migration:run`, `migration:revert`.
6. Data Source: конфігурація для CLI. Файл `data-source.ts`.
7. QueryBuilder: `createQueryBuilder()`, `select`, `where`, `andWhere`, `orWhere`, `orderBy`, `skip`, `take`, `leftJoinAndSelect`, `innerJoinAndSelect`.
8. Raw SQL-запити: `query()` метод. Параметризовані запити.
9. Transactions: `DataSource.transaction()`, `QueryRunner`. Ізоляція транзакцій.
10. Індекси: `@Index()`, `@Unique()`. Складені індекси. Вплив на продуктивність запитів.

**Ключові поняття:** OneToOne, OneToMany, ManyToMany, Migration, QueryBuilder, Transaction, Index, Cascade.

---

### Лекція 12. Механізми автентифікації у вебзастосунках
**(2 год)**

1. Автентифікація vs авторизація: визначення, відмінності, взаємозв'язок.
2. Стратегії автентифікації: огляд підходів (Session-based, Token-based, OAuth, SSO).
3. Cookie-based sessions: механізм, `express-session`, сховища сесій (Redis). Переваги та недоліки.
4. JWT (JSON Web Token): структура (Header, Payload, Signature), алгоритми підпису (HS256, RS256). Час життя токена.
5. Бібліотека `@nestjs/jwt`: `JwtModule`, `JwtService`. Генерація та верифікація токенів.
6. Passport.js: концепція стратегій. Інтеграція з NestJS (`@nestjs/passport`).
7. Local Strategy: автентифікація за email/паролем. `AuthGuard('local')`.
8. JWT Strategy: `AuthGuard('jwt')`, витягування payload з токена. Захист маршрутів.
9. Хешування паролів: бібліотека `bcrypt`, salt rounds, `argon2` як альтернатива.
10. Refresh Tokens: концепція, ротація, зберігання (БД, Redis). Access + Refresh flow.
11. OAuth 2.0: потоки авторизації (Authorization Code, Client Credentials, PKCE). Інтеграція з Google, GitHub через Passport strategies. OpenID Connect — огляд.

**Ключові поняття:** JWT, Passport, Strategy, AuthGuard, bcrypt, Refresh Token, OAuth 2.0, Cookie session, PKCE.

---

### Лекція 13. Авторизація та безпека серверних застосунків
**(2 год)**

1. Моделі авторизації: DAC, MAC, RBAC, ABAC — порівняння.
2. Role-Based Access Control (RBAC): ролі, ієрархія ролей. Реалізація у NestJS: декоратор `@Roles()`, `RolesGuard`.
3. Permission-Based Access Control: дозволи (permissions), зв'язок ролей та дозволів. Декоратор `@Permissions()`.
4. Attribute-Based Access Control (ABAC): атрибути суб'єкта, ресурсу, дії, контексту. Бібліотека CASL.
5. Custom декоратори: `@CurrentUser()`, `@Public()`. Використання `SetMetadata()` та `Reflector`.
6. Policies та Policy-based авторизація у NestJS.
7. CORS: детальна конфігурація `app.enableCors()` (origin, methods, headers, credentials).
8. Helmet: захист HTTP-заголовків. Конфігурація у NestJS.
9. Rate Limiting: `@nestjs/throttler` — захист від brute force та DDoS. `ThrottlerGuard`, `@Throttle()`, `@SkipThrottle()`.
10. Захист від поширених атак: XSS (Content Security Policy), CSRF (CSRF tokens, SameSite cookies), SQL Injection (параметризовані запити), NoSQL Injection.
11. HTTPS у продакшені: сертифікати, Let's Encrypt, reverse proxy (Nginx).

**Ключові поняття:** RBAC, ABAC, Permission, CASL, CORS, Helmet, Rate Limiting, XSS, CSRF, SQL Injection.

---

### Лекція 14. Комунікація у реальному часі, нотифікації та фонові задачі
**(2 год)**

1. Канали комунікації в реальному часі: polling, long-polling, Server-Sent Events (SSE), WebSocket — порівняння, сценарії використання.
2. WebSocket у NestJS: `@WebSocketGateway()`, `@SubscribeMessage()`. Бібліотека Socket.IO: інтеграція, адаптер.
3. Lifecycle hooks WebSocket: `OnGatewayInit`, `OnGatewayConnection`, `OnGatewayDisconnect`. Rooms та Namespaces. Broadcasting.
4. Server-Sent Events (SSE) у NestJS: декоратор `@Sse()`, `Observable`, інтервальна відправка подій. Порівняння з WebSocket.
5. Система нотифікацій: архітектура. In-app нотифікації: зберігання у БД, відправка через WebSocket/SSE.
6. Email-нотифікації: бібліотека `nodemailer`. Інтеграція з NestJS (`@nestjs-modules/mailer`). Шаблони листів (Handlebars, Pug). SMTP-конфігурація.
7. Web Push нотифікації: Push API, Service Workers, VAPID-ключі. Бібліотека `web-push`. Огляд архітектури.
8. Фонові задачі (Background Jobs): бібліотека `@nestjs/bull` (Bull + Redis). Черги, producers, consumers, job events, retry logic.
9. Планувальники (Schedulers): `@nestjs/schedule`. Декоратори `@Cron()`, `@Interval()`, `@Timeout()`. Cron-вирази.
10. Практичні сценарії: відправка email після реєстрації, нагадування, очищення застарілих даних, генерація звітів у фоні.

**Ключові поняття:** WebSocket Gateway, SSE, Socket.IO, nodemailer, Web Push, Bull Queue, Cron, Background Job, Scheduler.

---

### Лекція 15. Тестування, документування та розгортання застосунків
**(2 год)**

1. Піраміда тестування: Unit → Integration → E2E. Стратегія тестування backend.
2. Jest у NestJS: конфігурація, `describe`, `it`, `expect`. `Test.createTestingModule()`.
3. Unit-тестування сервісів: мокування залежностей (`jest.fn()`, `jest.spyOn()`), мок-репозиторії.
4. E2E-тестування: `supertest`, `INestApplication`, тестова база даних. Покриття коду: `jest --coverage`.
5. Swagger/OpenAPI: специфікація OpenAPI 3.0. `@nestjs/swagger`: налаштування `SwaggerModule.setup()`.
6. Декоратори Swagger: `@ApiTags()`, `@ApiOperation()`, `@ApiResponse()`, `@ApiProperty()`, `@ApiBearerAuth()`. Версіонування API.
7. Конфігурація: `@nestjs/config`, `ConfigModule`, `.env` файли. Валідація змінних середовища (`Joi`).
8. Docker: образи, контейнери, `Dockerfile` для NestJS (multi-stage build). Docker Compose: NestJS + PostgreSQL + Redis.
9. CI/CD: концепція, GitHub Actions — приклад pipeline (lint → test → build → deploy).
10. Логування: вбудований `Logger`, бібліотека `winston` / `pino`. Структуроване логування.
11. Моніторинг: Health checks (`@nestjs/terminus`). Метрики (Prometheus). Огляд платіжних інтеграцій (Stripe, LiqPay, Fondy).
12. Серіалізація: `ClassSerializerInterceptor`, `@Exclude()`, `@Expose()`. Компресія відповідей.

**Ключові поняття:** Jest, Unit Test, E2E Test, Swagger, OpenAPI, Docker, CI/CD, ConfigModule, Health Check, Logging, Monitoring.

---

## 6. ЗМІСТ ПРАКТИЧНИХ ЗАНЯТЬ

---

### Практична робота № 1. Дослідження мережевих протоколів засобами інструментів розробника
**(2 год)**

**Мета:** Набути практичних навичок аналізу мережевої взаємодії клієнта та сервера з використанням інструментів розробника.

**Завдання:**
1. Налаштувати робоче середовище: встановити Node.js (LTS), VS Code (з розширеннями), Postman.
2. Проаналізувати HTTP-запити та відповіді за допомогою DevTools (вкладка Network): метод, URL, статус, заголовки, тіло.
3. Виконати GET, POST, PUT, DELETE запити через Postman до публічного API (JSONPlaceholder).
4. Дослідити заголовки запитів та відповідей: Content-Type, Accept, Cache-Control, CORS-заголовки.
5. Виконати HTTP-запити через cURL з терміналу: різні методи, передача заголовків та тіла.
6. Проаналізувати різницю між HTTP та HTTPS з'єднаннями (TLS handshake у DevTools).
7. Дослідити Cookie: створення, передача, атрибути (HttpOnly, Secure, SameSite).

**Форма звітності:** Письмовий звіт зі скриншотами та аналізом результатів.

---

### Практична робота № 2. Базові засоби системи типів TypeScript
**(2 год)**

**Мета:** Оволодіти базовим синтаксисом TypeScript, навчитися використовувати систему типів для створення надійного коду.

**Завдання:**
1. Ініціалізувати TypeScript-проєкт: `npm init -y`, `npm i -D typescript`, `npx tsc --init`.
2. Створити змінні з різними типами: примітивні, масиви, кортежі, об'єктні типи, type aliases.
3. Реалізувати інтерфейси для опису структур даних предметної області (варіант за номером у журналі).
4. Написати функції з типізованими параметрами та значеннями повернення (optional, default, rest params).
5. Використати Union та Intersection types для моделювання складних типів.
6. Реалізувати type narrowing з використанням `typeof`, `instanceof`, discriminated unions.
7. Продемонструвати type assertions та non-null assertion operator.

**Форма звітності:** Репозиторій з вихідним кодом та коментарями.

---

### Практична робота № 3. Узагальнення, декоратори та утиліти типів TypeScript
**(2 год)**

**Мета:** Освоїти розширені можливості TypeScript, необхідні для роботи з NestJS.

**Завдання:**
1. Реалізувати generic-функції та generic-класи (типізована колекція, generic репозиторій).
2. Створити generic-інтерфейс для типізованої HTTP-відповіді (`ApiResponse<T>`).
3. Написати декоратори: класу (логування створення екземпляра), методу (вимірювання часу виконання), властивості (валідація значення).
4. Використати Utility Types (`Partial`, `Required`, `Pick`, `Omit`, `Record`) для трансформації існуючих типів.
5. Реалізувати Enum для статусів замовлення та ролей користувача.
6. Написати програму з модульною структурою (`import`/`export`, barrel files).
7. Налаштувати strict mode та виправити всі помилки типізації.

**Форма звітності:** Репозиторій з вихідним кодом.

---

### Практична робота № 4. Розроблення REST-ендпоінтів засобами NestJS
**(2 год)**

**Мета:** Навчитися створювати проєкт NestJS, конфігурувати контролери та реалізовувати REST-ендпоінти.

**Завдання:**
1. Встановити NestJS CLI (`npm i -g @nestjs/cli`), створити новий проєкт (`nest new`).
2. Ознайомитися зі структурою проєкту: `main.ts`, `app.module.ts`, конфігурація.
3. Створити контролер для ресурсу предметної області (за варіантом) через `nest generate controller`.
4. Реалізувати CRUD-ендпоінти: `GET /`, `GET /:id`, `POST /`, `PUT /:id`, `DELETE /:id`.
5. Створити DTO для запитів (`CreateDto`, `UpdateDto`) з типізацією.
6. Використати декоратори `@Param()`, `@Query()`, `@Body()`, `@HttpCode()`, `@Header()`.
7. Протестувати ендпоінти через Postman або Thunder Client.
8. Реалізувати простий сервіс з in-memory масивом та впровадити його у контролер.

**Форма звітності:** Працюючий проєкт NestJS з документованими ендпоінтами.

---

### Практична робота № 5. Модульна архітектура та ін'єкція залежностей у NestJS
**(2 год)**

**Мета:** Засвоїти принципи ін'єкції залежностей та модульної архітектури NestJS.

**Завдання:**
1. Створити Feature Module для ресурсу: `nest generate module`, `nest generate service`.
2. Перенести сервіс та контролер у Feature Module. Налаштувати `imports`/`exports`.
3. Створити другий Feature Module з власним сервісом та контролером.
4. Реалізувати Shared Module зі спільними утилітами (наприклад, `SlugService`).
5. Створити Custom Provider з використанням `useFactory` (наприклад, конфігурація).
6. Продемонструвати роботу DI: залежність одного сервісу від іншого.
7. Реалізувати lifecycle hook `onModuleInit` для логування ініціалізації модуля.

**Форма звітності:** Проєкт з модульною архітектурою (мінімум 3 модулі).

---

### Практична робота № 6. Валідація вхідних даних та обробка запитів у NestJS
**(2 год)**

**Мета:** Навчитися валідувати вхідні дані, створювати middleware та обробляти помилки.

**Завдання:**
1. Встановити `class-validator` та `class-transformer`.
2. Додати декоратори валідації до DTO: `@IsString()`, `@IsInt()`, `@IsEmail()`, `@MinLength()`, `@IsOptional()`, `@IsEnum()`.
3. Налаштувати глобальний `ValidationPipe` з опціями `whitelist`, `transform`, `forbidNonWhitelisted`.
4. Створити Custom Pipe для трансформації даних (наприклад, `TrimPipe`, `ParseSlugPipe`).
5. Реалізувати Middleware для логування запитів (метод, URL, IP, час обробки).
6. Створити Custom Exception Filter для уніфікованого формату помилок (JSON з полями `statusCode`, `message`, `error`, `timestamp`).
7. Реалізувати Interceptor для вимірювання часу обробки запиту (логування latency).

**Форма звітності:** Проєкт з валідацією, middleware та обробкою помилок.

---

### Практична робота № 7. Реалізація операцій CRUD засобами TypeORM та PostgreSQL
**(2 год)**

**Мета:** Навчитися інтегрувати PostgreSQL у NestJS-проєкт та реалізувати операції CRUD з використанням TypeORM.

**Завдання:**
1. Запустити PostgreSQL через Docker (`docker run` або `docker-compose.yml`).
2. Підключити TypeORM: `@nestjs/typeorm`, `typeorm`, `pg`. Конфігурація `TypeOrmModule.forRoot()`.
3. Створити Entity для ресурсу предметної області: різні типи колонок (string, number, boolean, enum, date).
4. Використати `@CreateDateColumn()`, `@UpdateDateColumn()`.
5. Реалізувати повний CRUD через Repository: `find`, `findOneBy`, `save`, `update`, `remove`.
6. Замінити in-memory сховище із попередніх робіт на PostgreSQL.
7. Реалізувати пагінацію (offset-based з `skip`/`take`) та фільтрацію (за query-параметрами).

**Форма звітності:** Проєкт з підключеною БД та повним CRUD.

---

### Практична робота № 8. Моделювання зв'язків між сутностями та керування міграціями
**(2 год)**

**Мета:** Навчитися моделювати зв'язки між сутностями та керувати схемою бази даних через міграції.

**Завдання:**
1. Створити додаткові Entity та встановити зв'язки:
   - One-to-Many / Many-to-One (наприклад, User → Posts).
   - Many-to-Many (наприклад, Posts ↔ Tags).
2. Налаштувати cascade операції (`cascade: true`).
3. Реалізувати ендпоінти з завантаженням зв'язаних сутностей (опція `relations`).
4. Відключити `synchronize: true`. Створити файл `data-source.ts` для CLI.
5. Створити та запустити міграцію: `migration:generate`, `migration:run`.
6. Використати QueryBuilder для складного запиту (фільтрація + сортування + join).
7. Реалізувати транзакцію для атомарної операції (наприклад, створення замовлення з позиціями).

**Форма звітності:** Проєкт зі зв'язками між сутностями та міграціями.

---

### Практична робота № 9. Реалізація автентифікації та рольової авторизації
**(2 год)**

**Мета:** Реалізувати повний цикл автентифікації та авторизації у NestJS-застосунку.

**Завдання:**
1. Створити модулі `AuthModule` та `UsersModule`.
2. Реалізувати Entity `User` з полями: email, password (хешований), role (enum).
3. Реалізувати реєстрацію: хешування пароля через `bcrypt`, збереження в БД. Перевірка унікальності email.
4. Реалізувати логін: перевірка credentials, генерація JWT (access + refresh tokens).
5. Налаштувати Passport JWT Strategy для захисту маршрутів.
6. Створити декоратори `@Public()` (для відкритих маршрутів) та `@CurrentUser()` (для отримання поточного користувача).
7. Реалізувати RBAC: enum `Role`, декоратор `@Roles()`, `RolesGuard`. Захистити адміністративні маршрути.
8. Протестувати захищені маршрути через Postman (з та без токена, з різними ролями).

**Форма звітності:** Проєкт з автентифікацією та авторизацією.

---

### Практична робота № 10. Комунікація у реальному часі та система нотифікацій
**(2 год)**

**Мета:** Реалізувати WebSocket-з'єднання, SSE та систему email-нотифікацій.

**Завдання:**
1. Встановити залежності: `@nestjs/websockets`, `@nestjs/platform-socket.io`, `socket.io`.
2. Створити WebSocket Gateway з підтримкою CORS. Реалізувати `@SubscribeMessage()` для обміну повідомленнями.
3. Реалізувати lifecycle hooks: логування підключення/відключення. Rooms: приєднання, Broadcasting.
4. Створити простий HTML-клієнт на Socket.IO для тестування WebSocket.
5. Реалізувати SSE-ендпоінт (`@Sse()`) для потокових оновлень (наприклад, лічильник або стрічка подій).
6. Налаштувати email-нотифікації: `@nestjs-modules/mailer` + `nodemailer`. Конфігурація SMTP (Mailtrap для тестування).
7. Реалізувати відправку вітального email при реєстрації користувача. Використати HTML-шаблон.

**Форма звітності:** Працюючий WebSocket-сервер з HTML-клієнтом, SSE-ендпоінт, email-нотифікації.

---

### Практична робота № 11. Автоматизоване тестування та документування API
**(2 год)**

**Мета:** Навчитися писати автоматизовані тести та генерувати інтерактивну документацію API.

**Завдання:**
1. Написати unit-тести для одного сервісу: мокування репозиторію (`jest.fn()`), тестування CRUD-методів.
2. Написати unit-тести для контролера: мокування сервісу.
3. Написати E2E-тест для одного ендпоінта: `supertest`, тестовий модуль з `Test.createTestingModule()`.
4. Налаштувати покриття коду (`jest --coverage`). Проаналізувати звіт.
5. Встановити `@nestjs/swagger`. Налаштувати `SwaggerModule` у `main.ts`.
6. Додати Swagger-декоратори до контролерів та DTO: `@ApiTags()`, `@ApiOperation()`, `@ApiResponse()`, `@ApiProperty()`.
7. Додати `@ApiBearerAuth()` для захищених маршрутів. Налаштувати Bearer Auth у Swagger UI.
8. Перевірити згенеровану документацію у браузері (`/api/docs`).

**Форма звітності:** Проєкт з тестами (coverage ≥ 60%) та Swagger-документацією.

---

## 7. МОДУЛЬНІ КОНТРОЛЬНІ РОБОТИ

---

### Модульна контрольна робота № 1
**(Після лекції 7 — «Вступ до NestJS. Контролери та маршрутизація»)**

**Теми:** Комп'ютерні мережі (OSI, TCP/IP, DNS, SMTP, WebSocket, SSH) · Протокол HTTP/HTTPS · Основи та розширені можливості TypeScript · Платформа Node.js (Event Loop, модулі, асинхронність) · Архітектура NestJS · Контролери та маршрутизація.

**Структура (максимум 50 балів):**

| Складова | Бали | Опис |
|---|:---:|---|
| Теоретична частина | 20 | 10 тестових питань (по 2 бали): мережеві протоколи, HTTP, TypeScript, Node.js, архітектура NestJS |
| Практична частина | 30 | Завдання за варіантом: реалізувати контролер NestJS з CRUD-ендпоінтами, DTO, типізацією TypeScript |

---

### Модульна контрольна робота № 2
**(Після лекції 14 — «Real-time комунікація, нотифікації та фонові задачі»)**

**Теми:** Провайдери, сервіси, модулі · Валідація, Pipes, Middleware · TypeORM (Entity, Repository, зв'язки, міграції) · Автентифікація (JWT, OAuth 2.0) · Авторизація (RBAC, ABAC, безпека) · WebSocket, SSE, нотифікації · Фонові задачі та планувальники.

**Структура (максимум 50 балів):**

| Складова | Бали | Опис |
|---|:---:|---|
| Теоретична частина | 20 | 10 тестових питань (по 2 бали): TypeORM, JWT/OAuth, RBAC, WebSocket, нотифікації, фонові задачі |
| Практична частина | 30 | Завдання за варіантом: реалізувати модуль NestJS з Entity, зв'язками, сервісом, захищеними маршрутами (JWT + RBAC) |

---

## 8. ТЕМИ ДЛЯ САМОСТІЙНОГО ВИВЧЕННЯ

| № | Тема | Годин | Форма контролю |
|---|---|:---:|---|
| 1 | Історія розвитку вебтехнологій. Стандарти W3C та WHATWG | 4 | Реферат |
| 2 | Протоколи транспортного рівня: TCP та UDP. Надійність доставки, congestion control | 4 | Реферат |
| 3 | Порівняльний аналіз серверних фреймворків: Express, Fastify, Koa, Hapi, NestJS | 4 | Порівняльна таблиця з обґрунтуванням |
| 4 | TypeScript: Conditional Types, Template Literal Types, Mapped Types у практиці | 4 | Практичне завдання з кодом |
| 5 | Патерни проєктування у серверній розробці (Repository, Strategy, Observer, Factory) | 4 | Реферат з прикладами коду |
| 6 | NoSQL бази даних: MongoDB (документо-орієнтована), Redis (ключ-значення). Порівняння з SQL | 5 | Реферат з порівнянням SQL/NoSQL |
| 7 | Альтернативні ORM: Prisma (schema-first), Drizzle (TypeScript-first) — порівняння з TypeORM | 4 | Порівняльний аналіз |
| 8 | OAuth 2.0 та OpenID Connect: поглиблене вивчення потоків авторизації | 5 | Реферат зі схемами потоків |
| 9 | GraphQL: специфікація, переваги порівняно з REST, інтеграція з NestJS (`@nestjs/graphql`) | 5 | Реферат з прикладом schema |
| 10 | Мікросервісна архітектура: принципи, паттерни, NestJS Microservices (TCP, gRPC, NATS) | 5 | Реферат зі схемою архітектури |
| 11 | Кешування: стратегії (Cache-Aside, Write-Through), інтеграція Redis з NestJS (`@nestjs/cache-manager`) | 4 | Практичне завдання |
| 12 | Черги повідомлень: RabbitMQ, Apache Kafka — концепції, use cases, інтеграція з NestJS (`@nestjs/bull`) | 4 | Реферат з порівнянням |
| 13 | Інтеграція платіжних систем: Stripe, LiqPay, Fondy. Архітектура обробки платежів, webhooks | 4 | Реферат зі схемою інтеграції |
| 14 | Безпека вебзастосувань: OWASP Top 10. Практичні приклади атак та методи захисту | 4 | Реферат з прикладами атак та захисту |
| 15 | Контейнеризація та оркестрація: Docker (best practices, multi-stage builds), Kubernetes (pods, services, deployments) | 4 | Реферат з Dockerfile |
| | **Разом** | **64** | |

---

## 9. СИСТЕМА ОЦІНЮВАННЯ

### 9.1. Розподіл балів

| Вид діяльності | Кількість | Бали за одиницю | Максимум |
|---|:---:|:---:|:---:|
| Практичні роботи | 11 | до 5 балів | 55 |
| Модульна контрольна робота № 1 | 1 | до 50 балів | 50 |
| Модульна контрольна робота № 2 | 1 | до 50 балів | 50 |
| Самостійна робота | 15 | до 3 балів | 45 |
| **Усього за семестр** | | | **200** |

> Підсумкова оцінка за семестр обчислюється як сума балів, нормалізована до 100-бальної шкали:
> **Оцінка = (Набрані бали / 200) × 100**

### 9.2. Шкала оцінювання ЄКТС

| Оцінка ЄКТС | Бали (100-бальна шкала) | Національна шкала |
|:---:|:---:|---|
| A | 90–100 | Відмінно |
| B | 82–89 | Добре |
| C | 74–81 | Добре |
| D | 64–73 | Задовільно |
| E | 60–63 | Задовільно |
| FX | 35–59 | Незадовільно (з правом перескладання) |
| F | 0–34 | Незадовільно (з обов'язковим повторним курсом) |

### 9.3. Умови допуску до екзамену

Студент допускається до екзамену за умови:
- виконання не менше 8 із 11 практичних робіт;
- складання обох модульних контрольних робіт;
- набору не менше 30 балів (із 100 за нормалізованою шкалою) за результатами семестрової роботи.

---

## 10. ПЕРЕЛІК ПИТАНЬ ДЛЯ ПІДСУМКОВОГО КОНТРОЛЮ (ЕКЗАМЕНУ)

> Екзаменаційні білети формуються на основі наведеного переліку запитань. Структура запитань чергується за правилом: три теоретичних питання та одне практичне завдання для перевірки прикладних навичок написання коду.

### Модуль 1. Мережеві технології, TypeScript та основи NestJS

1. Еталонна модель взаємодії відкритих систем OSI: призначення та функції кожного із семи рівнів.
2. Стек протоколів TCP і IP: порівняльний аналіз із моделлю OSI та принципи інкапсуляції пакетів даних.
3. Прикладні мережеві протоколи DNS, SMTP та SSH: призначення, базові команди та принципи функціонування.
4. *Практичне завдання:* Скласти схему мережевого запиту від клієнта до сервера із зазначенням протоколів на кожному рівні моделі TCP і IP (Application, Transport, Internet, Network Access).
5. Протокол передачі гіпертексту HTTP: еволюція версій від HTTP 1.1 до HTTP 3 та особливості протоколу QUIC.
6. Анатомія HTTP-повідомлень: структура стартового рядка, обов'язкові заголовки та формати тіла запиту й відповіді.
7. Методи протоколу HTTP: призначення, семантика, концепція безпечності та ідемпотентності методів.
8. *Практичне завдання:* Скласти текстовий приклад валідного сирого HTTP-запиту методом POST для створення нового ресурсу із передачею JSON-тіла та заголовків `Content-Type`, `Accept`, `Authorization`.
9. Класифікація статус-кодів відповідей HTTP: призначення груп 1xx, 2xx, 3xx, 4xx, 5xx та приклади найуживаніших кодів.
10. Механізми забезпечення безпеки у вебмережі: політика одного джерела (Same-Origin Policy), механізм CORS та протокол HTTPS (TLS).
11. Механізми збереження стану у вебдодатках: порівняння cookies, серверних сесій та токенів автентифікації.
12. *Практичне завдання:* Написати приклад конфігурації заголовка `Set-Cookie` із зазначенням безпекових атрибутів `HttpOnly`, `Secure`, `SameSite` та `Max-Age`.
13. Концепція статичної типізації мови TypeScript: архітектура компілятора tsc та призначення конфігураційного файлу `tsconfig.json`.
14. Базові та спеціальні типи даних у TypeScript: відмінності у поведінці та безпеці типів `any`, `unknown`, `void` і `never`.
15. Складені типи даних: синтаксис та застосування об'єднань (Union Types), перетинів (Intersection Types) та літеральних типів.
16. *Практичне завдання:* Оголосити псевдонім типу (Type Alias) для структури користувача із обов'язковими, необов'язковими полями та полями тільки для читання (`readonly`).
17. Механізми звуження типів (Type Narrowing): використання операторів `typeof`, `instanceof`, `in` та користувацьких перевірок типів.
18. Дискримінантні об'єднання (Discriminated Unions): принципи побудови та безпечне опрацювання варіантів через конструкцію `switch`.
19. Типізація функцій у TypeScript: параметри за замовчуванням, необов'язкові параметри, rest-параметри та перевантаження функцій.
20. *Практичне завдання:* Написати функцію-предикат типу (Custom Type Guard), яка перевіряє, чи переданий об'єкт `unknown` належить до інтерфейсу з визначеним числовим полем `id`.
21. Інтерфейси в TypeScript: оголошення, наслідування, злиття декларацій (Declaration Merging) та порівняння з Type Aliases.
22. Об'єктно-орієнтоване програмування в TypeScript: модифікатори доступу, статичні члени, гетери, сетери та абстрактні класи.
23. Параметричний поліморфізм (Generics): оголошення узагальнених функцій, інтерфейсів і класів та обмеження типів (Generic Constraints).
24. *Практичне завдання:* Реалізувати узагальнений інтерфейс для пагінованої відповіді API `PaginatedResponse<T>`, що містить масив елементів типу `T` та метадані сторінки.
25. Метапрограмування на основі декораторів у TypeScript: типи декораторів (класів, методів, властивостей, параметрів) та фабрики декораторів.
26. Вбудовані службові типи (Utility Types): призначення та механізм роботи `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`.
27. Службові типи для функцій і трансформацій: `Exclude`, `Extract`, `NonNullable`, `ReturnType`, `Parameters` та базові принципи Mapped Types.
28. *Практичне завдання:* Створити тип за допомогою службових утиліт `Omit` та `Partial`, який формує DTO для оновлення сутності без можливості зміни первинного ключа `id`.
29. Архітектура платформи Node.js: рушій V8, системна бібліотека libuv та однопотокова подієво-орієнтована модель із неблокуючим I/O.
30. Цикл подій (Event Loop) у Node.js: послідовність і призначення фаз (timers, pending callbacks, poll, check, close callbacks).
31. Модульні системи платформи: порівняльний аналіз стандартів CommonJS і ES Modules та керування пакетами через `package.json`.
32. *Практичне завдання:* Написати скрипт для Node.js із використанням вбудованого модуля `fs/promises` для асинхронного читання контенту JSON-файлу та його парсингу.
33. Еволюція асинхронності в JavaScript: патерн зворотних викликів (Callbacks), проблема Callback Hell та об'єкти Promise.
34. Життєвий цикл та комбінатори Promise: призначення і поведінка методів `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`.
35. Синтаксичні конструкції `async` і `await`: внутрішній механізм функціонування та стратегії опрацювання виключень через `try-catch`.
36. *Практичне завдання:* Написати асинхронну функцію, яка паралельно завантажує дані з двох джерел за допомогою `Promise.all` та повертає комбінований результат.
37. Подієво-орієнтована архітектура: клас `EventEmitter`, реєстрація обробників подій та реалізація патерну Observer у Node.js.
38. Багатопотоковість та процеси у Node.js: призначення модулів `worker_threads` та `child_process` для виконання ресурсомістких завдань.
39. Стратегії обробки глобальних помилок і критичних станів у Node.js: `uncaughtException`, `unhandledRejection` та концепція Graceful Shutdown.
40. *Практичне завдання:* Реалізувати клас, що наслідує `EventEmitter`, генерує подію при зміні внутрішнього стану та передає дані слухачам.
41. Архітектурна філософія фреймворку NestJS: трирівнева модульна структура та реалізація інверсії керування (IoC).
42. Контролери у NestJS: оголошення через декоратор `@Controller`, визначення базового маршруту та мапінг HTTP-методів.
43. Декоратори вилучення параметрів запиту: призначення та використання `@Param`, `@Query`, `@Body`, `@Headers`, `@Req`, `@Res`.
44. *Практичне завдання:* Написати клас контролера `ProductsController` із маршрутами для отримання списку товарів (GET) та створення нового товару (POST).
45. Об'єкти передачі даних (DTO): призначення в архітектурі NestJS, типізація вхідних даних та відмінність від сутностей бази даних.
46. Керування параметрами HTTP-відповіді у контролерах: декоратори `@HttpCode`, `@Header`, `@Redirect` та особливості асинхронних обробників.
47. Конвенції структуризації проєкту NestJS: призначення файлів `main.ts`, `app.module.ts` та генерація коду засобами NestJS CLI.
48. *Практичне завдання:* Реалізувати DTO-клас `CreateUserDto` для реєстрації користувача із полями `email`, `password` та `username`.

### Модуль 2. Серверна розробка з NestJS

49. Концепція провайдерів у NestJS: роль декоратора `@Injectable` та реєстрація компонентів бізнес-логіки.
50. Ін'єкція залежностей (Dependency Injection) у конструктор: типи впровадження, токени ін'єкції та декоратор `@Inject`.
51. Спеціалізовані провайдери (Custom Providers): синтаксис та сценарії використання `useValue`, `useClass`, `useFactory`, `useExisting`.
52. *Практичне завдання:* Реалізувати сервіс `UsersService`, який містить методи для пошуку користувача за ідентифікатором та додавання нового користувача у масив.
53. Області видимості провайдерів (Injection Scopes): характеристики та продуктивність Scopes `DEFAULT` (Singleton), `REQUEST`, `TRANSIENT`.
54. Модульна система NestJS: структура декоратора `@Module` (imports, controllers, providers, exports) та інкапсуляція компонентів.
55. Динамічні модулі (Dynamic Modules): патерни `forRoot`, `forRootAsync`, `forFeature` та вирішення циклічних залежностей через `forwardRef`.
56. *Практичне завдання:* Оголосити модуль `UsersModule`, що імпортує необхідні сервіси, реєструє `UsersController` та експортує `UsersService` для інших модулів.
57. Конвеєр обробки запитів (Request Pipeline) у NestJS: життєвий цикл запиту та послідовність виконання Middleware, Guards, Interceptors, Pipes, Filters.
58. Трансформація та валідація даних через Pipes: вбудовані пайпи та глобальне підключення `ValidationPipe`.
59. Декларативна валідація DTO: застосування декораторів бібліотек `class-validator` та `class-transformer`.
60. *Практичне завдання:* Додати валідаційні декоратори бібліотеки `class-validator` до DTO-класу для перевірки коректності email, мінімальної довжини пароля та обов'язкового рядка.
61. Проміжні обробники (Middleware): реалізація інтерфейсу `NestMiddleware`, конфігурація маршрутів та сценарії використання.
62. Захисні перехоплювачі (Guards): інтерфейс `CanActivate`, доступ до `ExecutionContext` та прийняття рішення про допуск до обробника.
63. Перехоплювачі (Interceptors) та фільтри виключень (Exception Filters): логування, трансформація відповідей та стандартизація помилок через `HttpException`.
64. *Практичне завдання:* Реалізувати користувацький Exception Filter, що перехоплює виключення `HttpException` та повертає JSON-відповідь стандартизованого формату із таймстемпом.
65. Концепція об'єктно-реляційного відображення (ORM): переваги, обмеження та налаштування модуля `TypeOrmModule` у NestJS.
66. Оголошення сутностей (Entities) у TypeORM: декоратори `@Entity`, `@Column`, типи стовпців, генерація первинних ключів через `@PrimaryGeneratedColumn`.
67. Спеціальні автоматичні стовпці: `@CreateDateColumn`, `@UpdateDateColumn`, `@DeleteDateColumn` та концепція м'якого видалення (Soft Delete).
68. *Практичне завдання:* Оголосити клас сутності `User` для TypeORM із первинним UUID-ключем, унікальним email, хешем пароля та автоматичними датами створення й оновлення.
69. Патерн Repository у TypeORM: отримання екземпляра репозиторію через `@InjectRepository` та базові методи CRUD.
70. Методи пошуку в репозиторії: параметри `find`, `findOne`, `findOneBy`, фільтрація, сортування (`order`) та вибір окремих полів (`select`).
71. Стратегії реалізації пагінації даних: зіставлення пагінації на основі зміщення (`skip`, `take`) та курсорної пагінації (Cursor-based pagination).
72. *Практичне завдання:* Реалізувати метод сервісу, який виконує пагінований пошук активних сутностей у репозиторії з використанням параметрів `skip` та `take`.
73. Моделювання зв'язків між сутностями у TypeORM: декларація відношень One-to-One, One-to-Many, Many-to-One, Many-to-Many та декоратор `@JoinColumn`.
74. Стратегії завантаження пов'язаних сутностей: зіставлення жадібного (Eager Loading) та лінивого (Lazy Loading) завантаження, параметр `relations`.
75. Каскадні операції в ORM: конфігурація `cascade` (insert, update, remove) та поведінка зовнішніх ключів при видаленні (`onDelete: CASCADE`).
76. *Практичне завдання:* Оголосити зв'язок один до багатьох між сутністю `Author` та сутністю `Book` у TypeORM із підтримкою каскадного збереження.
77. Керування схемою бази даних за допомогою міграцій: життєвий цикл міграцій, генерація, застосування та відкат змін у продакшені.
78. Побудова складних запитів через QueryBuilder: вибірка, фільтрація, використання об'єднань `leftJoinAndSelect` та `innerJoinAndSelect`.
79. Атомарність та цілісність даних: реалізація транзакцій через `DataSource.transaction` та механізм `QueryRunner`, рівні ізоляції транзакцій.
80. *Практичне завдання:* Написати фрагмент коду з використанням `createQueryBuilder` для вибірки користувачів разом із їхніми замовленнями за певний діапазон дат.
81. Фундаментальні відмінності між процесами автентифікації, авторизації та ідентифікації користувача.
82. Порівняльний аналіз стратегій автентифікації: сесійна автентифікація на основі cookies та безстанкова автентифікація на основі токенів.
83. Структура та криптографічні засади JSON Web Token (JWT): будова частин Header, Payload, Signature та алгоритми підпису (HS256, RS256).
84. *Практичне завдання:* Написати функцію генерації пари токенів (Access Token та Refresh Token) із зазначенням різного часу життя за допомогою `@nestjs/jwt`.
85. Безпечне збереження облікових даних: механізми одностороннього хешування паролів, додавання солі (Salt) та бібліотека bcrypt.
86. Життєвий цикл пари токенів (Access і Refresh Tokens): стратегії ротації, зберігання refresh-токенів та безпечне відкликання доступу.
87. Архітектура протоколу OAuth 2.0 та OpenID Connect: ролі учасників, потік Authorization Code Flow та делегування авторизації.
88. *Практичне завдання:* Реалізувати JWT-стратегію для Passport.js (`JwtStrategy`), що витягує Bearer-токен із заголовка запиту та валідує його корисне навантаження (payload).
89. Моделі керування доступом: порівняльний аналіз рольової моделі (RBAC) та атрибутивної моделі (ABAC).
90. Реалізація рольового доступу в NestJS: створення декоратора `@Roles`, передача метаданих через `Reflector` та перевірка прав у `RolesGuard`.
91. Захист серверних застосунків від загроз переліку OWASP Top 10: протидія атакам CSRF, XSS, SQL-ін'єкціям, конфігурація CORS, Helmet та Rate Limiting.
92. *Практичне завдання:* Реалізувати `RolesGuard` у NestJS, який зчитує дозволені ролі з метаданих маршруту та зіставляє їх із роллю користувача з об'єкта запиту.
93. Технології обміну даними у реальному часі: порівняння опитування (Polling), довгих запитів (Long Polling), Server-Sent Events (SSE) та протоколу WebSocket.
94. Організація WebSocket-шлюзів у NestJS: декоратори `@WebSocketGateway`, `@SubscribeMessage`, робота з кімнатами (Rooms) та просторами імен (Namespaces).
95. Асинхронна обробка завдань у чергах та планувальники: архітектура черг на основі Redis (бібліотека Bull), планування періодичних задач за розкладом Cron.
96. *Практичне завдання:* Реалізувати метод WebSocket-шлюзу у NestJS для обробки вхідного повідомлення від клієнта та розсилки оновлення всім підключеним клієнтам у кімнаті.
97. Піраміда тестування бекенд-застосунків: відмінності, цілі та методологія модульного (Unit), інтеграційного та наскрізного (E2E) тестування.
98. Мокування залежностей у Jest: створення тестових модулів через `Test.createTestingModule`, підміна репозиторіїв і сервісів шпигунами та моками.
99. Автоматичне документування API та контейнеризація: специфікація OpenAPI і Swagger, конфігурація Dockerfile для NestJS та основи конвеєрів CI і CD.
100. *Практичне завдання:* Написати модульний Unit-тест на Jest для сервісу, який перевіряє коректність виклику методу репозиторію `findOne` із замокованими даними.

---

## 11. РЕКОМЕНДОВАНА ЛІТЕРАТУРА

### 11.1. Основна література

1. Буров Є. В., Митник М. М. *Комп'ютерні мережі: підручник. Том перший* / за заг. ред. В. В. Пасічника. — Львів: «Магнолія 2006», 2024. — 464 с. — (Серія «Комп'ютинг»).
2. Кульчицький О. Й. *Сучасні технології розробки серверних вебзастосувань: навчальний посібник*. — Київ: КПІ ім. Ігоря Сікорського, 2022. — 216 с.
3. Boris Cherny. *Programming TypeScript: Making Your JavaScript Applications Scale*. — O'Reilly Media, 2019. — 352 p.
4. Mario Casciaro, Luciano Mammino. *Node.js Design Patterns: Design and implement production-grade Node.js applications using proven patterns and techniques*. — 3rd ed. — Packt Publishing, 2020. — 664 p.
5. Patrick Desjardins. *Enterprise-Ready Node.js: Build robust, maintainable, and highly available back-end applications using NestJS and TypeScript*. — Packt Publishing, 2023. — 424 p.

### 11.2. Додаткова література

6. Пасічник В. В., Резніченко В. А. *Організація баз даних та знань*. — Київ: Видавнича група BHV, 2006. — 384 с.
7. Andrew S. Tanenbaum, David J. Wetherall. *Computer Networks*. — 6th ed. — Pearson, 2021. — 960 p.
8. Mark Richards, Neal Ford. *Fundamentals of Software Architecture: An Engineering Approach*. — O'Reilly Media, 2020. — 432 p.
9. Sam Newman. *Building Microservices: Designing Fine-Grained Systems*. — 2nd ed. — O'Reilly Media, 2021. — 616 p.
10. Eric Freeman, Elisabeth Robson. *Head First Design Patterns*. — 2nd ed. — O'Reilly Media, 2020. — 694 p.

### 11.3. Інформаційні ресурси

11. NestJS Documentation (офіційна документація фреймворку). — [https://docs.nestjs.com](https://docs.nestjs.com)
12. TypeScript Documentation & Handbook. — [https://www.typescriptlang.org/docs/handbook/](https://www.typescriptlang.org/docs/handbook/)
13. Node.js Documentation. — [https://nodejs.org/docs/](https://nodejs.org/docs/)
14. PostgreSQL Documentation. — [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
15. TypeORM Documentation. — [https://typeorm.io](https://typeorm.io)
16. Socket.IO Documentation. — [https://socket.io/docs/](https://socket.io/docs/)
17. MDN Web Docs — HTTP. — [https://developer.mozilla.org/en-US/docs/Web/HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
18. OWASP Foundation — Web Security Testing Guide. — [https://owasp.org/](https://owasp.org/)
19. Swagger / OpenAPI Specification. — [https://swagger.io/specification/](https://swagger.io/specification/)
20. Bull Queue Documentation. — [https://docs.bullmq.io/](https://docs.bullmq.io/)
21. Jest Documentation. — [https://jestjs.io/docs/getting-started](https://jestjs.io/docs/getting-started)

---

## 12. КАЛЕНДАРНО-ТЕМАТИЧНИЙ ПЛАН

| Тиждень | Лекція | Практичне заняття / Контрольна |
|:---:|---|---|
| 1 | Лекція 1. Архітектура комп'ютерних мереж та мережеві протоколи | — |
| 2 | Лекція 2. Протокол HTTP та захищена передача даних HTTPS | Практична робота № 1. Дослідження мережевих протоколів |
| 3 | Лекція 3. Система типів мови TypeScript | Практична робота № 2. Базові засоби системи типів TypeScript |
| 4 | Лекція 4. Розширені засоби мови TypeScript | Практична робота № 3. Узагальнення, декоратори та утиліти типів |
| 5 | Лекція 5. Платформа Node.js як середовище виконання | — |
| 6 | Лекція 6. Асинхронне програмування у Node.js | — |
| 7 | Лекція 7. Фреймворк NestJS. Контролери та маршрутизація | Практична робота № 4. Розроблення REST-ендпоінтів засобами NestJS |
| 8 | Лекція 8. Провайдери, сервіси та модульна система NestJS | **Модульна контрольна робота № 1** |
| 9 | Лекція 9. Валідація даних та конвеєр обробки запитів | Практична робота № 5. Модульна архітектура та ін'єкція залежностей |
| 10 | Лекція 10. Інтеграція реляційних баз даних засобами TypeORM | Практична робота № 6. Валідація вхідних даних та обробка запитів |
| 11 | Лекція 11. Зв'язки між сутностями, міграції та оптимізація запитів | Практична робота № 7. Реалізація операцій CRUD засобами TypeORM |
| 12 | Лекція 12. Механізми автентифікації у вебзастосунках | Практична робота № 8. Моделювання зв'язків та керування міграціями |
| 13 | Лекція 13. Авторизація та безпека серверних застосунків | Практична робота № 9. Реалізація автентифікації та рольової авторизації |
| 14 | Лекція 14. Комунікація у реальному часі, нотифікації та фонові задачі | Практична робота № 10. Комунікація у реальному часі та система нотифікацій |
| 15 | Лекція 15. Тестування, документування та розгортання застосунків | **Модульна контрольна робота № 2** |
| 16 | — | Практична робота № 11. Автоматизоване тестування та документування API |
| 17 | — | **Екзамен** |

> Календарно-тематичний план може коригуватися відповідно до навчального графіку закладу освіти. Практичні заняття тижнів 9–16 виконуються за матеріалами лекцій попереднього тижня.

---

## 13. ПОЛІТИКА НАВЧАЛЬНОЇ ДИСЦИПЛІНИ

### 13.1. Академічна доброчесність
Студенти зобов'язані дотримуватися принципів академічної доброчесності відповідно до Закону України «Про освіту» (ст. 42). Плагіат, копіювання коду без розуміння та вказання авторства, використання згенерованого коду без власного аналізу — є підставою для зниження оцінки або анулювання роботи.

### 13.2. Відвідування
Відвідування лекцій — рекомендоване. Відвідування практичних занять та модульних контрольних робіт — обов'язкове. У разі пропуску практичного заняття студент зобов'язаний виконати роботу самостійно та захистити її під час консультації.

### 13.3. Дедлайни
Практичні роботи приймаються протягом двох тижнів після проведення заняття. Після закінчення дедлайну максимальний бал зменшується на 40%.

### 13.4. Використання штучного інтелекту
Використання ШІ-інструментів (GitHub Copilot, ChatGPT тощо) дозволяється як допоміжний засіб навчання. Студент повинен розуміти та бути здатним пояснити кожен рядок написаного коду. На модульних контрольних роботах та екзамені використання ШІ заборонено.

### 13.5. Комунікація
Консультації проводяться за розкладом кафедри. Питання щодо практичних робіт та навчального матеріалу можуть надсилатися на електронну пошту викладача або через систему управління навчанням (LMS).

---

*Робочу програму складено відповідно до вимог Закону України «Про вищу освіту», стандартів ЄКТС та рекомендацій щодо організації освітнього процесу у закладах вищої освіти України.*

---

## 14. ДОДАТОК: ПОПЕРЕДНІЙ РОЗГОРНУТИЙ ПЛАН (ДЛЯ ДОВІДКИ)

> Нижче наведено попередній розгорнутий варіант детального опису тем (з повним переліком технологій та понять) для збереження контексту та зручності копіювання.

### Розділ 1. Мережеві технології, TypeScript та основи NestJS

* **Тема 1. Архітектура комп'ютерних мереж та мережеві протоколи**  
  Еволюція веброзробки: від статичних сторінок до мікросервісів. Модель взаємодії клієнт-сервер. Багатошарова архітектура (presentation, business logic, data access). Поняття backend та frontend. Роль серверної частини у вебзастосунку. Еталонна модель OSI: сім рівнів, інкапсуляція, протоколи кожного рівня. Стек протоколів TCP/IP: порівняння з OSI, практичне застосування. IP-адресація (IPv4, IPv6), порти, сокети. Протоколи TCP та UDP. DNS: ієрархія, типи записів (A, AAAA, CNAME, MX, TXT), процес резолвінгу. Протокол SMTP: призначення, команди (HELO, MAIL FROM, RCPT TO, DATA). MIME-типи. POP3 vs IMAP. Протокол WebSocket: мотивація, відмінності від HTTP, повнодуплексний зв’язок, рукостискання (Upgrade), фрейми. SSH: безпечний віддалений доступ, автентифікація за ключами, тунелювання. Огляд сучасних серверних технологій: Node.js, Python (Django, Flask), Java (Spring), Go.

* **Тема 2. Протокол HTTP та захищена передача даних HTTPS**  
  Протокол HTTP: історія версій (HTTP/1.0, HTTP/1.1, HTTP/2, HTTP/3 — QUIC). Структура HTTP-запиту: стартовий рядок (request line), заголовки, тіло. Структура HTTP-відповіді: статусний рядок (status line), заголовки, тіло. Методи HTTP: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS. Ідемпотентність та безпечність методів. Коди відповідей HTTP: класифікація (1xx — інформаційні, 2xx — успіх, 3xx — перенаправлення, 4xx — помилка клієнта, 5xx — помилка сервера). Найпоширеніші коди. Заголовки запитів та відповідей: Content-Type, Accept, Authorization, Cache-Control, User-Agent, Set-Cookie. CORS (Cross-Origin Resource Sharing): Same-Origin Policy, preflight-запити, CORS-заголовки. HTTPS: протокол TLS (Transport Layer Security), сертифікати, процес рукостискання, шифрування. Механізми збереження стану: Cookie (атрибути: HttpOnly, Secure, SameSite, Path, Expires), Session, Token. Інструменти тестування та аналізу HTTP: Postman, cURL, HTTPie, DevTools (вкладка Network). Формати обміну даними: JSON, XML, Form Data, Multipart.

* **Тема 3. Система типів мови TypeScript**  
  TypeScript як надмножина JavaScript: мотивація, переваги статичної типізації. Встановлення та конфігурація: Node.js, npm, tsc. Файл `tsconfig.json`: ключові параметри (`target`, `module`, `strict`, `outDir`, `rootDir`). Примітивні типи: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`. Спеціальні типи: `any`, `unknown`, `void`, `never`. Відмінності `any` та `unknown`. Масиви та кортежі (Tuple). Типізація масивів: `number[]` vs `Array<number>`. Об'єктні типи. Type aliases (`type`). Index signatures. Union types (`|`), Intersection types (`&`). Практичні сценарії. Literal types. Тип `as const`. Template literal types. Type narrowing: `typeof`, `instanceof`, `in`, discriminated unions. Type assertions (`as`). Non-null assertion (`!`). Коли та як використовувати. Функції: типізація параметрів, значень повернення, optional та default параметри, rest parameters. Перевантаження функцій (function overloads). Стрілкові функції.

* **Тема 4. Розширені засоби мови TypeScript**  
  Інтерфейси (`interface`): оголошення, розширення (`extends`), злиття декларацій (declaration merging). Порівняння `interface` та `type`: коли що використовувати. Практичні рекомендації. Класи в TypeScript: модифікатори доступу (`public`, `private`, `protected`, `readonly`). Абстрактні класи та абстрактні методи. Реалізація інтерфейсів (`implements`). Generics: generic-функції, generic-класи, generic-інтерфейси. Constraints (`extends`). Default type parameters. Перерахування (`enum`): числові, рядкові, const enum. Переваги та недоліки. Декоратори: декоратори класів, методів, властивостей, параметрів. Фабрики декораторів. `experimentalDecorators` та `emitDecoratorMetadata`. Utility types: `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `Readonly<T>`, `ReturnType<T>`, `Exclude<T, U>`, `Extract<T, U>`. Mapped types: `[K in keyof T]`. Conditional types: `T extends U ? X : Y`. Infer keyword. Модульна система: `import`/`export`, named та default exports, barrel files (`index.ts`). Strict mode: `strictNullChecks`, `strictFunctionTypes`, `noImplicitAny`, `noImplicitReturns`.

* **Тема 5. Платформа Node.js як середовище виконання серверних застосунків**  
  Що таке Node.js: рушій V8, libuv, однопотокова модель з неблокуючим I/O. Історія Node.js. Версії LTS та Current. Відмінності від браузерного JavaScript. Глобальні об'єкти: `global`, `process`, `console`, `__dirname`, `__filename`, `Buffer`, `setTimeout`/`setInterval`. Event Loop: фази (timers, pending callbacks, poll, check, close callbacks). Мікро- та макрозадачі. `process.nextTick()`, `setImmediate()`. Модульна система: CommonJS (`require`/`module.exports`) vs ES Modules (`import`/`export`). Відмінності, інтероперабельність. npm та package.json: ініціалізація проєкту, залежності (`dependencies`, `devDependencies`), скрипти, семантичне версіонування (semver). Lock-файли. Вбудовані модулі: `path` (маніпуляції зі шляхами), `os` (системна інформація), `url` (парсинг URL), `crypto` (хешування, шифрування). Модуль `http`: створення HTTP-сервера без фреймворків. Обробка запитів та відповідей. Модуль `fs`: читання та запис файлів (синхронний та асинхронний API). `fs/promises`. Робота з потоками (Streams): Readable, Writable, Duplex, Transform. Piping. Практичне застосування. Менеджери версій Node.js: nvm, fnm. Інструменти: nodemon, ts-node, tsx.

* **Тема 6. Асинхронне програмування у Node.js**  
  Синхронний vs асинхронний код: блокування потоку, наслідки для продуктивності. Callbacks: патерн Error-First Callback. Callback Hell (Pyramid of Doom). Promises: стани (pending, fulfilled, rejected). Створення (`new Promise`), ланцюжки (`.then`, `.catch`, `.finally`). Комбінатори Promise: `Promise.all()`, `Promise.allSettled()`, `Promise.race()`, `Promise.any()`. Async/Await: синтаксичний цукор над Promises. Обробка помилок (`try/catch`). Паралельне vs послідовне виконання асинхронних операцій. Практичні патерни. EventEmitter: патерн «Спостерігач» (Observer) у Node.js. Створення власних подій, підписка (`on`, `once`, `off`), `emit`. Worker Threads: багатопотоковість у Node.js. `worker_threads` модуль. Коли використовувати. Child Processes: `child_process` модуль (`exec`, `spawn`, `fork`). Делегування CPU-інтенсивних задач. Обробка помилок у Node.js: `uncaughtException`, `unhandledRejection`, graceful shutdown. Порівняння фреймворків для Node.js: Express, Fastify, Koa, Hapi, NestJS — архітектура, продуктивність, екосистема.

### Розділ 2. Серверна розробка з NestJS

* **Тема 7. Фреймворк NestJS. Контролери та маршрутизація**  
  NestJS: філософія, архітектура, натхнення Angular. TypeScript-first підхід. Ядро NestJS: модулі (`@Module`), контролери (`@Controller`), провайдери (`@Injectable`). Ін'єкція залежностей (Dependency Injection): IoC-контейнер, принцип інверсії залежностей (DIP). NestJS CLI: встановлення, створення проєкту (`nest new`), генерація компонентів (`nest generate`). Структура проєкту NestJS: `main.ts`, `app.module.ts`, `app.controller.ts`, `app.service.ts`. Конвенції іменування. Контролери: роль в архітектурі. Декоратори маршрутів: `@Get()`, `@Post()`, `@Put()`, `@Patch()`, `@Delete()`. Параметри маршруту: `@Param()`, `@Query()`, `@Body()`, `@Headers()`. DTO (Data Transfer Objects): визначення, застосування для типізації вхідних даних. Відмінність від Entity. Об'єкти Request та Response. Декоратори `@Req()`, `@Res()`. Library-specific vs Standard approach. HTTP-статус коди: `@HttpCode()`, `@Header()`, `@Redirect()`. Асинхронні обробники: робота з `Promise` та `Observable`. Wildcard routes.

* **Тема 8. Провайдери, сервіси та модульна система NestJS**  
  Провайдери: концепція, декоратор `@Injectable()`, реєстрація у модулі. Сервіси як основні провайдери: інкапсуляція бізнес-логіки, розділення відповідальностей. Custom Providers: `useValue`, `useClass`, `useFactory`, `useExisting`. Практичні сценарії. Injection tokens: рядкові та символьні токени. Декоратор `@Inject()`. Scope провайдерів: `DEFAULT` (singleton), `REQUEST`, `TRANSIENT`. Вплив на продуктивність. Модулі: структура `@Module()` — `imports`, `controllers`, `providers`, `exports`. Feature modules: ізоляція функціональності. Генерація модулів через CLI. Shared modules та реекспорт. `@Global()` модулі: переваги та ризики. Dynamic modules: патерн `forRoot()`, `forRootAsync()`, `forFeature()`. Конфігурація модулів. Circular dependencies: проблема, `forwardRef()` як рішення. Життєвий цикл додатку NestJS: хуки `onModuleInit`, `onModuleDestroy`, `onApplicationBootstrap`, `onApplicationShutdown`.

* **Тема 9. Валідація даних та конвеєр обробки запитів у NestJS**  
  Pipes: концепція, вбудовані pipes (`ValidationPipe`, `ParseIntPipe`, `ParseUUIDPipe`, `DefaultValuePipe`). Бібліотеки `class-validator` та `class-transformer`: декоратори валідації (`@IsString()`, `@IsEmail()`, `@Min()`, `@MaxLength()`, `@IsOptional()`, `@ValidateNested()`). Глобальна валідація: `app.useGlobalPipes()`. Опції: `whitelist`, `transform`, `forbidNonWhitelisted`. Custom Pipes: створення власних pipes для трансформації та валідації даних. Middleware: функціональний та класовий підхід. Реєстрація в модулі через `NestModule.configure()`. Порівняння middleware NestJS з Express middleware. Порядок виконання. Глобальний middleware. Guards: інтерфейс `CanActivate`, `ExecutionContext`. Рівні застосування: глобальний, контролерний, маршрутний. Interceptors: інтерфейс `NestInterceptor`, `CallHandler`, `Observable`. Use cases: логування, кешування, трансформація відповіді, timeout. Exception Filters: вбудовані виключення (`HttpException`, `NotFoundException`, `BadRequestException`). Custom Exception Filters. Request Pipeline — порядок виконання: Middleware → Guards → Interceptors (before) → Pipes → Handler → Interceptors (after) → Exception Filters.

* **Тема 10. Інтеграція реляційних баз даних засобами TypeORM**  
  Реляційні бази даних: таблиці, стовпці, типи даних, первинні та зовнішні ключі. Нормалізація. PostgreSQL: встановлення (Docker), psql, pgAdmin. Основні SQL-команди (DDL, DML). ORM (Object-Relational Mapping): концепція, переваги та недоліки порівняно з raw SQL. TypeORM: встановлення, підключення до PostgreSQL у NestJS (`TypeOrmModule.forRoot()`). Конфігурація через `ConfigModule`. Entity: декоратор `@Entity()`, `@Column()`, `@PrimaryGeneratedColumn()` (uuid, increment). Типи колонок: string, number, boolean, date, enum, json, jsonb, array. Nullable, default values. Автоматичні колонки: `@CreateDateColumn()`, `@UpdateDateColumn()`, `@DeleteDateColumn()` (Soft Delete). `@VersionColumn()`. Repository Pattern: `@InjectRepository()`, базові методи (`find`, `findOne`, `findOneBy`, `save`, `remove`, `update`, `delete`). `TypeOrmModule.forFeature()`: реєстрація Entity у Feature Modules. Пагінація: offset-based (`skip`, `take`) та cursor-based підходи. Фільтрація та сортування.

* **Тема 11. Зв'язки між сутностями, міграції та оптимізація запитів**  
  Типи зв'язків: One-to-One (`@OneToOne`, `@JoinColumn`), One-to-Many / Many-to-One (`@OneToMany`, `@ManyToOne`), Many-to-Many (`@ManyToMany`, `@JoinTable`). Eager vs Lazy loading. Параметр `eager: true`. Опція `relations` у `find()`. Cascade operations: `cascade: true`, типи каскадів (`insert`, `update`, `remove`). `onDelete`, `onUpdate`. Міграції: навіщо потрібні, чому `synchronize: true` — лише для розробки. CLI для міграцій: `migration:generate`, `migration:create`, `migration:run`, `migration:revert`. Data Source: конфігурація для CLI. Файл `data-source.ts`. QueryBuilder: `createQueryBuilder()`, `select`, `where`, `andWhere`, `orWhere`, `orderBy`, `skip`, `take`, `leftJoinAndSelect`, `innerJoinAndSelect`. Raw SQL-запити: `query()` метод. Параметризовані запити. Transactions: `DataSource.transaction()`, `QueryRunner`. Ізоляція транзакцій. Індекси: `@Index()`, `@Unique()`. Складені індекси. Вплив на продуктивність запитів.

* **Тема 12. Механізми автентифікації у вебзастосунках**  
  Автентифікація vs авторизація: визначення, відмінності, взаємозв'язок. Стратегії автентифікації: огляд підходів (Session-based, Token-based, OAuth, SSO). Cookie-based sessions: механізм, `express-session`, сховища сесій (Redis). Переваги та недоліки. JWT (JSON Web Token): структура (Header, Payload, Signature), алгоритми підпису (HS256, RS256). Час життя токена. Бібліотека `@nestjs/jwt`: `JwtModule`, `JwtService`. Генерація та верифікація токенів. Passport.js: концепція стратегій. Інтеграція з NestJS (`@nestjs/passport`). Local Strategy: автентифікація за email/паролем. `AuthGuard('local')`. JWT Strategy: `AuthGuard('jwt')`, витягування payload з токена. Захист маршрутів. Хешування паролів: бібліотека `bcrypt`, salt rounds, `argon2` як альтернатива. Refresh Tokens: концепція, ротація, зберігання (БД, Redis). Access + Refresh flow. OAuth 2.0: потоки авторизації (Authorization Code, Client Credentials, PKCE). Інтеграція з Google, GitHub через Passport strategies. OpenID Connect — огляд.

* **Тема 13. Авторизація та безпека серверних застосунків**  
  Моделі авторизації: DAC, MAC, RBAC, ABAC — порівняння. Role-Based Access Control (RBAC): ролі, ієрархія ролей. Реалізація у NestJS: декоратор `@Roles()`, `RolesGuard`. Permission-Based Access Control: дозволи (permissions), зв'язок ролей та дозволів. Декоратор `@Permissions()`. Attribute-Based Access Control (ABAC): атрибути суб'єкта, ресурсу, дії, контексту. Бібліотека CASL. Custom декоратори: `@CurrentUser()`, `@Public()`. Використання `SetMetadata()` та `Reflector`. Policies та Policy-based авторизація у NestJS. CORS: детальна конфігурація `app.enableCors()` (origin, methods, headers, credentials). Helmet: захист HTTP-заголовків. Конфігурація у NestJS. Rate Limiting: `@nestjs/throttler` — захист від brute force та DDoS. `ThrottlerGuard`, `@Throttle()`, `@SkipThrottle()`. Захист від поширених атак: XSS (Content Security Policy), CSRF (CSRF tokens, SameSite cookies), SQL Injection (параметризовані запити), NoSQL Injection. HTTPS у продакшені: сертифікати, Let's Encrypt, reverse proxy (Nginx).

* **Тема 14. Комунікація у реальному часі, нотифікації та фонові задачі**  
  Канали комунікації в реальному часі: polling, long-polling, Server-Sent Events (SSE), WebSocket — порівняння, сценарії використання. WebSocket у NestJS: `@WebSocketGateway()`, `@SubscribeMessage()`. Бібліотека Socket.IO: інтеграція, адаптер. Lifecycle hooks WebSocket: `OnGatewayInit`, `OnGatewayConnection`, `OnGatewayDisconnect`. Rooms та Namespaces. Broadcasting. Server-Sent Events (SSE) у NestJS: декоратор `@Sse()`, `Observable`, інтервальна відправка подій. Порівняння з WebSocket. Система нотифікацій: архітектура. In-app нотифікації: зберігання у БД, відправка через WebSocket/SSE. Email-нотифікації: бібліотека `nodemailer`. Інтеграція з NestJS (`@nestjs-modules/mailer`). Шаблони листів (Handlebars, Pug). SMTP-конфігурація. Web Push нотифікації: Push API, Service Workers, VAPID-ключі. Бібліотека `web-push`. Огляд архітектури. Фонові задачі (Background Jobs): бібліотека `@nestjs/bull` (Bull + Redis). Черги, producers, consumers, job events, retry logic. Планувальники (Schedulers): `@nestjs/schedule`. Декоратори `@Cron()`, `@Interval()`, `@Timeout()`. Cron-вирази. Практичні сценарії: відправка email після реєстрації, нагадування, очищення застарілих даних, генерація звітів у фоні.

* **Тема 15. Тестування, документування та розгортання застосунків**  
  Піраміда тестування: Unit → Integration → E2E. Стратегія тестування backend. Jest у NestJS: конфігурація, `describe`, `it`, `expect`. `Test.createTestingModule()`. Unit-тестування сервісів: мокування залежностей (`jest.fn()`, `jest.spyOn()`), мок-репозиторії. E2E-тестування: `supertest`, `INestApplication`, тестова база даних. Покриття коду: `jest --coverage`. Swagger/OpenAPI: специфікація OpenAPI 3.0. `@nestjs/swagger`: налаштування `SwaggerModule.setup()`. Декоратори Swagger: `@ApiTags()`, `@ApiOperation()`, `@ApiResponse()`, `@ApiProperty()`, `@ApiBearerAuth()`. Версіонування API. Конфігурація: `@nestjs/config`, `ConfigModule`, `.env` файли. Валідація змінних середовища (`Joi`). Docker: образи, контейнери, `Dockerfile` для NestJS (multi-stage build). Docker Compose: NestJS + PostgreSQL + Redis. CI/CD: концепція, GitHub Actions — приклад pipeline (lint → test → build → deploy). Логування: вбудований `Logger`, бібліотека `winston` / `pino`. Структуроване логування. Моніторинг: Health checks (`@nestjs/terminus`). Метрики (Prometheus). Огляд платіжних інтеграцій (Stripe, LiqPay, Fondy). Серіалізація: `ClassSerializerInterceptor`, `@Exclude()`, `@Expose()`. Компресія відповідей.

---

## 15. МАТЕРІАЛИ ДЛЯ НАВЧАЛЬНОЇ ПРОГРАМИ (ВСТУП, МЕТА ТА ЗАВДАННЯ)

### ВСТУП

Програма вивчення навчальної дисципліни «Розробка WEB-застосувань» складена відповідно до освітньо-професійної програми підготовки фахового молодшого бакалавра галузі знань 12 «Інформаційні технології» спеціальності 121 «Інженерія програмного забезпечення».

**Предметом вивчення** навчальної дисципліни є теоретичні засади, архітектурні патерни, інженерні підходи та практичні засоби проєктування, розроблення, захисту, тестування й розгортання серверної частини сучасних масштабованих вебзастосувань.

**Міждисциплінарні зв’язки:** студент, для успішного оволодіння матеріалом даної дисципліни, повинен мати практичні знання з дисциплін:
- «Основи програмування та алгоритмічні мови»;
- «Об’єктно-орієнтоване програмування»;
- «Організація баз даних та знань»;
- «Основи програмної інженерії»;
- «Професійна практика програмної інженерії».

**Програма навчальної дисципліни складається з таких розділів:**
1. Розділ 1. Мережеві технології, TypeScript та основи NestJS;
2. Розділ 2. Серверна розробка з NestJS.

---

### 1. Мета та завдання навчальної дисципліни

**1.1. Метою викладання навчальної дисципліни «Розробка WEB-застосувань» є:**  
Формування у здобувачів освіти системи фундаментальних теоретичних знань і стійких практичних навичок, необхідних для вирішення комплексних задач повного життєвого циклу проєктування, розроблення, верифікації, безпеки та розгортання надійної серверної частини клієнт-серверних вебзастосувань промислового рівня з використанням сучасного інструментарію.

**1.2. Основними завданнями вивчення дисципліни «Розробка WEB-застосувань» є вивчення основ, засвоєння та використання на практиці:**
- функціонування комп'ютерних мереж, стеку протоколів TCP і IP, протоколів прикладного рівня HTTP та HTTPS;
- методів взаємодії вебклієнтів і вебсерверів, керуючих заголовків та механізмів збереження стану (cookies, сесії, токени);
- мови статичної типізації TypeScript та платформи серверного виконання Node.js;
- архітектурних засад побудови модульних серверних систем, інверсії керування (IoC) та ін'єкції залежностей (DI) на базі фреймворку NestJS;
- конвеєра обробки запитів, валідації вхідних даних через DTO та безпечного опрацювання виключень;
- взаємодії з реляційними базами даних через технології об'єктно-реляційного відображення (ORM), використання патерну Repository, транзакцій та міграцій;
- впровадження механізмів автентифікації на основі JWT токенів і протоколу OAuth 2.0, моделей авторизації (RBAC, ABAC) та захисту від загроз OWASP;
- організації комунікації у реальному часі через WebSocket та Server-Sent Events, а також черг асинхронної обробки фонових задач;
- автоматизованого модульного й наскрізного тестування, документування програмних інтерфейсів за стандартом OpenAPI і Swagger та контейнеризації додатків засобами Docker.

