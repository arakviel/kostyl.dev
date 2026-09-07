# Фонові задачі та черги

## Короткий зміст

У цій лекції вивчається організація асинхронної обробки завдань через черги з використанням Bull та Redis:

- **Концепція черг** — відкладене виконання задач поза HTTP request-response циклом, producer додає job у чергу, consumer обробляє jobs асинхронно, Redis як message broker
- **Бібліотека @nestjs/bull** — інтеграція Bull (популярна queue library) з NestJS, конфігурація через `BullModule.forRoot()` з Redis connection, реєстрація черг через `BullModule.registerQueue()`
- **Producers** — додавання jobs у чергу через `Queue.add('jobName', data, options)`, options: delay (відкладений старт), attempts (кількість retry), priority
- **Consumers (Processors)** — обробка jobs через декоратор `@Process('jobName')`, отримання job data, виконання асинхронної логіки, повернення результату
- **Job lifecycle** — стани job: waiting → active → completed/failed, progress tracking через `job.progress()`, events для кожного стану
- **Retry logic** — автоматичні retry при помилках, налаштування через attempts та backoff (експоненційна затримка), dead letter queue для permanently failed jobs
- **Job events** — слухачі подій: `@OnQueueActive()`, `@OnQueueCompleted()`, `@OnQueueFailed()` для моніторингу та логування
- **Bull Board** — UI dashboard для моніторингу черг, перегляд активних/completed/failed jobs, retry вручну

Розглядаються практичні сценарії: відправка email через чергу, обробка uploaded images (resize, optimization), генерація PDF звітів, імпорт даних з CSV, cleanup задачі.
