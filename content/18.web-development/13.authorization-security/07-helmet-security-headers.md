# Helmet та захисні HTTP заголовки

## Короткий зміст

У цій лекції вивчається використання бібліотеки Helmet для автоматичного налаштування захисних HTTP заголовків:

- **Призначення Helmet** — middleware для встановлення безпечних HTTP заголовків за замовчуванням, захист від типових веб-вразливостей
- **Content Security Policy (CSP)** — заголовок для обмеження джерел контенту (scripts, styles, images, fonts), захист від XSS атак через injection, директиви default-src, script-src, style-src
- **X-Frame-Options** — захист від clickjacking атак, заборона вбудовування сторінки у `<iframe>`, значення DENY, SAMEORIGIN
- **X-Content-Type-Options** — заборона MIME-sniffing браузером, примус використання Content-Type з сервера, значення nosniff
- **Strict-Transport-Security (HSTS)** — примусове використання HTTPS, автоматичний редирект HTTP → HTTPS на стороні браузера, параметр maxAge та includeSubDomains
- **Referrer-Policy** — контроль передачі Referer заголовка, захист приватної інформації в URL, значення no-referrer, same-origin, strict-origin
- **Інтеграція у NestJS** — встановлення `helmet` пакету, використання `app.use(helmet())` у `main.ts`, конфігурація для статичного контенту
- **Кастомізація політик** — налаштування CSP для різних середовищ (дозвіл inline scripts у dev, заборона у prod), whitelist для trusted domains

Розглядаються типові проблеми після увімкнення Helmet (блокування inline scripts, fonts з CDN), способи їх вирішення, тестування політик через browser console, моніторинг порушень CSP через report-uri.
