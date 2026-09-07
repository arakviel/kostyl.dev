# Практичні сценарії застосування

## Короткий зміст

У цій лекції розглядаються комплексні практичні приклади інтеграції real-time комунікації, нотифікацій та фонових задач:

- **Welcome email після реєстрації** — при POST /auth/register створюється job у черзі для відправки welcome email, job processor відправляє email через MailerService, retry logic при помилках SMTP, user отримує email через кілька секунд
- **Нагадування про події** — cron job запускається щодня о 9:00, перевіряє БД на події у найближчі 24 години, для кожного користувача створюється job у черзі для відправки email/push нотифікації, tracking відправлених нагадувань
- **Очищення застарілих даних** — cron job раз на тиждень (неділя о 2:00), видалення expired JWT refresh tokens, видалення soft-deleted entities старше 30 днів, архівування старих логів, vacuum database
- **Генерація звітів у фоні** — користувач запитує звіт через API, створюється job у черзі з високим priority, processor генерує PDF/Excel через puppeteer/exceljs, збереження у S3/local storage, відправка in-app notification + email з посиланням на завантаження
- **Real-time чат** — WebSocket Gateway для обміну повідомленнями, rooms для приватних чатів та груп, збереження повідомлень у БД, typing indicators, read receipts, online status tracking
- **Live dashboard** — SSE endpoint для streaming метрик, Observable генерує оновлення кожні 5 секунд, aggregating metrics з БД (active users, requests/sec, errors), frontend EventSource підписується та оновлює charts
- **Комбінований сценарій** — користувач публікує пост → створюється job для генерації thumbnail → WebSocket broadcast followers про новий пост → in-app notifications для followers → email digest раз на тиждень через cron

Кожен сценарій включає: архітектурну схему, code snippets, error handling, моніторинг, best practices для продакшену.
