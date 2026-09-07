# Rate Limiting та Throttling

## Короткий зміст

У цій лекції розглядається захист API від зловживань через обмеження частоти запитів:

- **Rate Limiting** — обмеження кількості запитів від одного клієнта за проміжок часу, захист від brute force атак (підбір паролів), DDoS атак, зловживання API
- **Бібліотека @nestjs/throttler** — офіційний модуль для rate limiting у NestJS, інтеграція через `ThrottlerModule.forRoot()`, налаштування TTL (time to live) та limit (максимум запитів)
- **ThrottlerGuard** — глобальний Guard для застосування rate limiting до всіх маршрутів, автоматичне відстеження запитів по IP адресі, відповідь 429 Too Many Requests при перевищенні ліміту
- **Декоратор @Throttle()** — route-specific налаштування ліміту, override глобальних налаштувань для окремих ендпоінтів (наприклад, жорсткіший ліміт для `/auth/login`)
- **Декоратор @SkipThrottle()** — виключення маршрутів з rate limiting (наприклад, health checks, webhooks від trusted провайдерів)
- **Сховища для rate limiting** — in-memory storage (за замовчуванням) для single-instance застосунків, Redis storage для horizontal scaling та distributed rate limiting
- **Кастомні стратегії** — власна логіка throttling на основі userId замість IP, різні ліміти для різних ролей (admin має більший ліміт)
- **Response headers** — заголовки X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset для інформування клієнта про стан ліміту

Розглядаються практичні сценарії: захист логіну від brute force (5 спроб за 15 хвилин), обмеження API endpoints (100 запитів на годину), sliding window vs fixed window алгоритми.
