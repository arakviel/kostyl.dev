# Залишок плану для курсу "Тестування ASP.NET Minimal API"

Оскільки ми деталізували попередні теми (розбивши xUnit та Integration Testing на кілька частин для збереження глибокого `text-first` підходу), нумерація зсунулася. Наразі написано **12 статей**. 

Беручи до уваги ваше побажання "розділяти наступні теми на дві частини і не жаліти пояснень", ось пропонований план для завершення курсу у тому ж преміальному стилі (по ~1000 рядків тексту кожна):

---

## Частина VI: Інструментарій та Мокування HTTP

### `13.postman-professional.md`
**"Професійний Postman: Колекції, Змінні та GitHub Інтеграція"**
- **Hook**: Ваш API росте, і тестувати його через Swagger стає занадто незручно. Як організувати і автоматизувати тести так, щоб їх використовувала вся команда?
- Postman по-дорослому: відходимо від разових запитів до структурованих Колекцій (Collections).
- Робота зі змінними: Global, Collection, Environment. Чому хардкод токенів та URL — це антипатерн.
- Pre-request Scripts: автоматичне отримання та інжект JWT токену перед запитом.
- Tests (Postman Sandbox): написання автоматизованих assertions на JavaScript (`pm.test()`, `pm.response.to.have.status()`).
- Тестування workflow: передача даних між запитами (напр. взяти ID зі створеного ресурсу і передати в наступний GET).
- CI/CD з Postman: запуск колекцій з командного рядка за допомогою `Newman`.
- **Нова фіча — Postman GitHub Integration**: як підключити Postman до GitHub, щоб зберігати колекції у репозиторії (контроль версій для ваших API контрактів).
- **Практика**: Створити колекцію для вашого Minimal API, налаштувати автоматичний логін, додати тести для кожного ендпоінту і засинхронізувати з GitHub.

### `14.httpclient-testing.md`
**"HttpClient у Тестах Частина 1: Архітектура та MockHttpMessageHandler"**
- **Hook**: Ваш сервіс викликає платіжний шлюз. Як протестувати це, не знявши реальні гроші?
- Архітектура HttpClient у .NET: чому не можна просто замокати `HttpClient`.
- Проблема socket exhaustion та роль `IHttpClientFactory`.
- Глибоке занурення у `HttpMessageHandler` та `DelegatingHandler`.
- Патерн створення власного `MockHttpMessageHandler`.
- Бібліотека `RichardSzalay.MockHttp`: fluent API для налаштування відповідей (наприклад `When("*/api/users").Respond("application/json", "{...}")`).
- Тестування Typed Clients, куди інжектиться `HttpClient`.
- **Практика**: 3 рівні завдань на ізольоване тестування сервісів-споживачів сторонніх API.

### `15.wiremock-net.md`
**"HttpClient у Тестах Частина 2: WireMock.Net та Resilience"**
- **Hook**: MockHttpMessageHandler не ловить помилки формування URL чи заголовків на рівні мережі. Нам потрібен справжній сервер.
- Що таке WireMock.Net: in-process HTTP server, що слухає реальний TCP порт.
- Налаштування WireMock server у `IAsyncLifetime`.
- Request Matching: по URL, Headers, Body (JSON Path), GraphQL.
- Налаштування Response: templating, затримки (latency simulation).
- Fault Injection: імітація 500 Internal Server Error, 503 Service Unavailable, таймаутів.
- Тестування Resilience: перевірка політик примусового повторення `Polly` (Retry, Circuit Breaker) за допомогою WireMock.
- **Практика**: Створення інтеграційного тесту, де WireMock імітує нестабільний сторонній сервіс.

---

## Частина VII: Патерни, Інструменти та Архітектура

### `16.testing-patterns.md`
**"Патерни та Анти-патерни Тестування: Test Smells"**
- **Hook**: Тести, які важче підтримувати, ніж production код. Чому тести стають "крихкими" (fragile)?
- Каталог Test Smells: Obscure Test, Mystery Guest, Fragile Test, Test Logic in Production.
- Патерн **Object Mother**: створення стандартних тестових об'єктів (напр. `ValidCustomer()`).
- Патерн **Test Data Builder**: еволюція Object Mother через Fluent API (вже згадувався у DB testing, тут — глибше абстрагування).
- Використання `Bogus` для генерації реалістичних фейкових даних (імена, email, адреси) і інтеграція з Builders.
- DRY vs DAMP у тестах: чому дублювання коду в тестах іноді краще за абстракцію.
- **Практика**: Рефакторинг "поганого" тесту з "запашком" у чистий DAMP-тест з Builder-ами.

### `17.advanced-testing-tools.md`
**"Просунуті інструменти: Time, Snapshots та Властивості"**
- **Hook**: Як протестувати код, який робить `if (DateTime.Now.DayOfWeek == DayOfWeek.Friday)`?
- **Тестування Часу**: проблема неявної залежності. Введення абстракції `TimeProvider` (.NET 8) та `FakeTimeProvider`.
- Машина часу в тестах: просування часу вперед (`Advance()`) для тестування таймаутів та expiring cache.
- **Snapshot Testing (Verify)**: заміна тисячі Assert-ів на один `Verify(result)`.
    - Як працює Approval Testing. Порівняння JSON, HTML, або складних об'єктів візуально.
- **Property-Based Testing (FsCheck)**: генерація тисяч випадкових інпутів замість `[InlineData]`.
    - Знаходження edge cases, про які ви не подумали.
- **Практика**: Написання тестів для time-sensitive логіки (напр. генерація токену, що діє 15 хвилин).

### `18.architecture-testing.md`
**"Тестування Архітектури з NetArchTest"**
- **Hook**: Хто перевірить, що розробники не зроблять посилання з Domain шару на Infrastructure?
- Fitness Functions: тестування самого коду як даних.
- Знайомство з `NetArchTest.Rules`.
- Написання тестів на архітектуру: 
    - `Domain` не має залежностей від інших проєктів.
    - Всі Minimal API ендпоінти мають специфічні атрибути чи фільтри.
    - Всі класи, що реалізують `IRequestHandler`, мають закінчуватися на `Handler`.
    - Всі record-класи в просторі `Entities` є `sealed`.
- Інтеграція архітектурних тестів у CI/CD pipeline.
- Очищення та фіналізація курсу.
- **Практика**: Створення набору з 5 суворих архітектурних тестів для поточного Minimal API проєкту.

---

**Загалом:** план передбачає ще **6 великих статей (13—18)**, які повністю розкриють продвинуті концепції тестування для ASP.NET Minimal API і закриють курс. Кожна буде написана з детальними текстовими поясненнями та продуманими Docus-компонентами.
