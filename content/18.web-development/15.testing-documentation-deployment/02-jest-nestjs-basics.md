# Основи Jest у NestJS

## Короткий зміст

У цій лекції вивчаються базові концепції тестування через Jest framework у NestJS:

- **Конфігурація Jest** — файл `jest.config.js` або `package.json`, налаштування testEnvironment (node), roots (src), moduleFileExtensions, coverageDirectory, preset для TypeScript через ts-jest
- **Структура тестів** — `describe()` для групування тестів (test suite), `it()` або `test()` для окремого тест-кейсу, вкладені describe блоки для ієрархічної організації
- **Matchers** — assertion методи: `toBe()` для примітивів, `toEqual()` для об'єктів/масивів, `toThrow()` для помилок, `toBeTruthy()`/`toBeFalsy()`, `toHaveLength()`, `toContain()`, `toMatchObject()`
- **Test.createTestingModule()** — створення ізольованого DI контейнера для тестів, імпорт модулів, providers, controllers, compile для побудови module, get() для отримання instances
- **Setup та teardown** — `beforeEach()` для підготовки перед кожним тестом, `afterEach()` для cleanup, `beforeAll()` для одноразової ініціалізації suite, `afterAll()` для фінального cleanup
- **Async testing** — підтримка async/await у тестах, повернення Promise з тесту, `resolves`/`rejects` matchers для асинхронних assertion
- **Test isolation** — кожен тест має бути незалежним, не покладатися на порядок виконання, cleanup стану між тестами

Розглядаються практичні приклади: написання першого тесту для NestJS сервісу, організація test files (*.spec.ts), running tests через `npm test`, watch mode для TDD.
