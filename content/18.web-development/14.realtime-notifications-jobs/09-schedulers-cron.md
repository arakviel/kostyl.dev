# Планувальники та Cron jobs

## Короткий зміст

У цій лекції розглядається автоматизоване виконання періодичних задач через планувальники:

- **Бібліотека @nestjs/schedule** — офіційний модуль для scheduling у NestJS, конфігурація через `ScheduleModule.forRoot()`, підтримка cron, intervals, timeouts
- **Декоратор @Cron()** — виконання задачі за розкладом cron, синтаксис cron expression (`'0 0 * * *'` = щодня о опівночі), підтримка named cron patterns (`CronExpression.EVERY_DAY_AT_MIDNIGHT`)
- **Cron expressions** — формат: секунди хвилини години день_місяця місяць день_тижня, wildcards та ranges, приклади: `'*/5 * * * *'` кожні 5 хвилин, `'0 9 * * 1-5'` робочі дні о 9:00
- **Декоратор @Interval()** — виконання через фіксовані інтервали часу (мілісекунди), приклад: `@Interval(10000)` кожні 10 секунд, простіше за cron для простих інтервалів
- **Декоратор @Timeout()** — одноразове виконання через затримку, корисно для delayed tasks при старті застосунку
- **Динамічне керування** — `SchedulerRegistry` для runtime управління jobs, методи `addCronJob()`, `deleteCronJob()`, `getCronJobs()`, pause/resume через job.stop() та job.start()
- **Timezone** — налаштування timezone для cron jobs через options `{ timeZone: 'Europe/Kiev' }`, важливо для глобальних застосунків
- **Best practices** — ідемпотентність задач (безпечний re-run), distributed locks для horizontal scaling (лише один instance виконує job), error handling та алерти

Розглядаються практичні сценарії: щоденне резервне копіювання БД, очищення expired sessions, генерація weekly/monthly звітів, sending reminders, aggregating metrics, health checks.
