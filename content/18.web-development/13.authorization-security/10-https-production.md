# HTTPS у продакшені

## Короткий зміст

У цій лекції вивчається налаштування HTTPS для безпечної передачі даних у продакшн середовищі:

- **TLS сертифікати** — криптографічні сертифікати для підтвердження ідентичності сервера, структура: public key, private key, certificate chain, CA (Certificate Authority)
- **Let's Encrypt** — безкоштовні TLS сертифікати з автоматичним оновленням, використання Certbot для отримання сертифікатів, wildcards для субдоменів (*.example.com)
- **Reverse proxy (Nginx)** — термінація TLS на рівні reverse proxy замість Node.js застосунку, конфігурація Nginx для HTTPS, проксування до NestJS на localhost, переваги: кращa продуктивність TLS, централізоване керування сертифікатами
- **Reverse proxy (Traefik)** — сучасна альтернатива Nginx з автоматичним отриманням Let's Encrypt сертифікатів, інтеграція з Docker, автоматичне оновлення
- **HTTP → HTTPS редирект** — автоматичне перенаправлення HTTP трафіку на HTTPS, конфігурація на рівні Nginx/Traefik, код відповіді 301 Moved Permanently
- **HSTS (HTTP Strict Transport Security)** — примусове використання HTTPS на рівні браузера після першого відвідування, заголовок Strict-Transport-Security з maxAge, includeSubDomains для всіх субдоменів, preload для включення у браузерні списки
- **Автоматичне оновлення сертифікатів** — cron jobs для Certbot, systemd timers, моніторинг дати закінчення сертифікатів, алерти при проблемах з оновленням
- **Налаштування у NestJS** — HTTPS listener у NestJS (опціонально), використання fs для читання сертифікатів, HTTPSOptions конфігурація

Розглядаються практичні сценарії: налаштування HTTPS для VPS через Nginx + Certbot, конфігурація для Docker Compose з Traefik, тестування TLS через ssllabs.com, моніторинг експірації сертифікатів, troubleshooting типових проблем (mixed content, certificate chain issues).
