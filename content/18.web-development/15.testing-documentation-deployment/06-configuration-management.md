# Керування конфігурацією

## Короткий зміст

У цій лекції розглядається управління налаштуваннями застосунку для різних середовищ:

- **@nestjs/config модуль** — офіційне рішення для configuration management, wrapper над dotenv з DI підтримкою, інсталяція та реєстрація через `ConfigModule.forRoot()`
- **.env файли** — зберігання environment variables: DATABASE_URL, JWT_SECRET, PORT, NODE_ENV, формат KEY=VALUE, .env.local для локальних override, .gitignore для безпеки
- **ConfigModule.forRoot() опції** — `isGlobal: true` для доступу у всіх модулях, `envFilePath` для custom шляху до .env, `ignoreEnvFile: true` для production (використання system env vars), `load` для custom configuration files
- **ConfigService** — сервіс для доступу до конфігурації, injection через constructor, методи `get<T>(key)` з type safety, `getOrThrow()` для required variables, default values через другий параметр
- **Валідація через Joi** — schema validation для env variables, забезпечення required fields, type checking (string, number, boolean), допустимі значення через enum, приклад schema для DATABASE_URL, JWT_SECRET, PORT
- **Custom configuration files** — окремі TypeScript файли для логічного групування (database.config.ts, jwt.config.ts), factory functions що повертають configuration object, registerAs() для namespaced config
- **Different configs для середовищ** — .env.development, .env.staging, .env.production, conditional loading на основі NODE_ENV, overrides для local development
- **Best practices** — ніколи не commit .env до git, використання example файлів (.env.example), обов'язкова валідація у production, типізація через TypeScript interfaces

Розглядаються практичні приклади: налаштування database connection через ConfigService, JWT configuration, різні configs для dev/prod, валідація env variables через Joi schema.
