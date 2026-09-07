# E2E тестування та покриття коду

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
