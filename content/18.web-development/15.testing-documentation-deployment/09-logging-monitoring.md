# Логування та моніторинг

## Короткий зміст

У цій лекції розглядається організація логування та моніторингу для production-ready застосунків:

- **Вбудований Logger** — NestJS Logger клас, методи: log(), error(), warn(), debug(), verbose(), context parameter для ідентифікації джерела логу, використання у сервісах через DI
- **Structured logging** — логування у JSON форматі замість plain text, fields: timestamp, level, message, context, metadata, переваги для parsing та aggregation у log management systems
- **Winston** — популярна Node.js logging бібліотека, transports для різних outputs (console, file, external services), log levels та filtering, format customization, rotation для log files
- **Pino** — найшвидша logging бібліотека для Node.js, low overhead, structured JSON logs за замовчуванням, async logging для performance, prettifier для development
- **Log levels** — error для помилок (500, exceptions), warn для попереджень (deprecated APIs), info для важливих подій (user login, order placed), debug для troubleshooting, verbose для детальної інформації
- **Context logging** — correlation IDs для трейсингу request через multiple services, middleware для генерації requestId, передача через AsyncLocalStorage або cls-hooked
- **Health checks** — `@nestjs/terminus` для health endpoints, перевірка: database connection, Redis connection, disk space, memory usage, HTTP GET /health для monitoring systems
- **Prometheus metrics** — збір метрик для моніторингу: request count, response time, error rate, custom business metrics, exposition через /metrics endpoint, scraping Prometheus сервером
- **Alerting** — автоматичні alerts при критичних метриках: error rate > threshold, response time > SLA, database connection failures, integration з PagerDuty/Opsgenie для on-call

Розглядаються практичні приклади: налаштування Winston з daily rotation, structured logging з correlation IDs, health checks для всіх dependencies, Prometheus metrics для NestJS, alerting rules.
