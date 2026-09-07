# Серіалізація та компресія

## Короткий зміст

У цій лекції вивчається оптимізація HTTP відповідей через трансформацію даних та стиснення:

- **ClassSerializerInterceptor** — автоматична трансформація entities у JSON, використання class-transformer декораторів, глобальна реєстрація через `app.useGlobalInterceptors()`, працює з Plain-to-Class transformation
- **@Exclude() декоратор** — виключення полів з response (password, internal fields), захист sensitive data, застосування на рівні класу або property, можливість exclude за умовою
- **@Expose() декоратор** — явне включення полів у response, whitelist підхід для максимальної безпеки, computed properties через @Expose() getter methods
- **Transformation groups** — різні серіалізації для різних контекстів, groups: 'admin', 'user', 'public', декоратор `@SerializeOptions({ groups: ['admin'] })` на контролері, conditional exposure через groups
- **Type transformation** — автоматичне перетворення типів (Date → ISO string, BigInt → string), custom transformers через @Transform() декоратор, nested object transformation
- **Compression middleware** — стиснення HTTP responses через compression package, підтримка gzip та deflate, автоматичне визначення Accept-Encoding, threshold для мінімального розміру response
- **Response interceptors** — custom interceptors для трансформації структури response, wrapping data у {success, data, metadata}, error normalization, pagination metadata injection
- **Огляд платіжних інтеграцій** — Stripe для міжнародних платежів (webhooks, subscription billing), LiqPay для України (checkout widget, callback handling), Fondy для СНД (tokenization, recurring payments), загальні концепції: idempotency keys, webhook verification, PCI compliance

Розглядаються практичні приклади: налаштування ClassSerializerInterceptor, hiding password field, groups для admin/user responses, compression для великих payloads, integration з payment providers.
