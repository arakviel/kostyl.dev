# Конфігурація CORS

## Короткий зміст

У цій лекції детально розглядається налаштування Cross-Origin Resource Sharing для безпечної взаємодії frontend та backend:

- **Same-Origin Policy** — браузерна політика безпеки, яка забороняє запити між різними origin (protocol + domain + port), необхідність CORS для обходу цієї політики
- **Базова конфігурація** — `app.enableCors()` у `main.ts` для дозволу cross-origin запитів, налаштування для розробки vs продакшену
- **Параметр origin** — обмеження дозволених джерел: string, array of strings, RegExp, або функція для динамічної перевірки, whitelist підхід для продакшену
- **Methods та headers** — дозволені HTTP методи (GET, POST, PUT, DELETE, PATCH), дозволені заголовки (Authorization, Content-Type, custom headers)
- **Credentials** — параметр `credentials: true` для дозволу cookies/authorization headers, вимога точного origin (не wildcard) при використанні credentials
- **Preflight requests** — OPTIONS запити для "складних" запитів (PUT, DELETE, custom headers), maxAge для кешування preflight відповідей
- **CORS у розробці** — дозвіл всіх origin `origin: true` для локальної розробки, використання proxy для обходу CORS в dev режимі
- **CORS у продакшені** — строгі обмеження origin, логування заблокованих запитів, моніторинг спроб несанкціонованого доступу

Розглядаються типові помилки CORS (blocked by CORS policy), налагодження через DevTools, конфігурація для різних сценаріїв (SPA, mobile apps, multiple frontends).
