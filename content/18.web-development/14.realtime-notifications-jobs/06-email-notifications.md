# Email нотифікації

## Короткий зміст

У цій лекції вивчається відправка email повідомлень через NestJS застосунок:

- **Бібліотека nodemailer** — популярна Node.js бібліотека для відправки email, підтримка SMTP, SendGrid, AWS SES, інших провайдерів
- **Інтеграція @nestjs-modules/mailer** — офіційний модуль для NestJS, wrapper над nodemailer з DI підтримкою, конфігурація через `MailerModule.forRoot()`
- **SMTP конфігурація** — налаштування SMTP сервера: host, port, secure (TLS), auth (user, password), приклади: Gmail SMTP, SendGrid SMTP, Mailgun, власний SMTP
- **HTML шаблони листів** — template engines: Handlebars, Pug, EJS для динамічних email, folder structure для шаблонів, передача змінних у template (username, verificationLink)
- **Відправка email** — MailerService з методом `sendMail()`, параметри: to, from, subject, template, context (дані для шаблону), attachments для файлів
- **Тестування email** — Mailtrap для dev середовища (fake SMTP), MailHog для локального тестування, перегляд відправлених email без реальної доставки
- **Best practices** — асинхронна відправка через черги (не блокувати HTTP request), retry logic при помилках SMTP, rate limiting для запобігання спаму, unsubscribe links для транзакційних email
- **Типи email** — welcome email після реєстрації, password reset, email verification, order confirmations, newsletter, promotional emails

Розглядаються практичні приклади: welcome email з шаблоном, password reset з токеном, email verification workflow, використання черг для масових розсилок.
