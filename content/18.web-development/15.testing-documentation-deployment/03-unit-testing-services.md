# Unit-тестування сервісів

## Короткий зміст

У цій лекції детально вивчається тестування бізнес-логіки у сервісах з ізоляцією залежностей:

- **Unit-тестування концепція** — тестування smallest testable units (методів сервісу) у повній ізоляції від зовнішніх залежностей (БД, інші сервіси, HTTP), швидкі тести для швидкого feedback
- **Мокування залежностей** — заміна реальних залежностей на mock objects, `jest.fn()` для створення mock функцій, `jest.spyOn()` для шпигунства за викликами методів, налаштування return values через `mockReturnValue()`, `mockResolvedValue()`
- **Мок-репозиторії TypeORM** — створення mock repository через `jest.fn()` для методів find, findOne, save, remove, реєстрація у testing module через custom providers, `getRepositoryToken()` для injection token
- **Testing providers з залежностями** — мокування сервісів у constructor injection, createTestingModule з providers array, overrideProvider() для заміни реальних providers на mocks
- **Isolated testing patterns** — AAA pattern (Arrange-Act-Assert), Given-When-Then, тестування edge cases (null, undefined, empty arrays), error scenarios (throwing exceptions)
- **Assertion на виклики** — перевірка що метод був викликаний: `toHaveBeenCalled()`, `toHaveBeenCalledWith()`, `toHaveBeenCalledTimes()`, важливість verify правильних аргументів
- **Coverage метрики** — statement coverage, branch coverage, function coverage, line coverage, цільові показники для production code

Розглядаються практичні приклади: тестування CRUD методів сервісу, мокування repository для різних scenarios, testing business validation logic, error handling tests.
