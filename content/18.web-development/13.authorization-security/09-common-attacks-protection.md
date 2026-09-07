# Захист від поширених атак

## Короткий зміст

У цій лекції детально вивчаються найпоширеніші типи атак на веб-застосунки та методи захисту:

- **XSS (Cross-Site Scripting)** — ін'єкція JavaScript коду через користувацький ввід, типи: Reflected XSS, Stored XSS, DOM-based XSS; захист через Content Security Policy, санітизацію HTML, escape спецсимволів, використання textContent замість innerHTML
- **CSRF (Cross-Site Request Forgery)** — виконання небажаних дій від імені автентифікованого користувача, захист через CSRF tokens (synchronizer token pattern), SameSite cookies (Strict/Lax), перевірка Origin/Referer заголовків
- **SQL Injection** — ін'єкція SQL команд через користувацький ввід, приклади атак через WHERE умови, захист через параметризовані запити (prepared statements), ORM best practices (TypeORM автоматично екранує параметри), валідація та санітизація вводу
- **NoSQL Injection** — аналогічні атаки для NoSQL баз (MongoDB), ін'єкція через query operators ($where, $regex), захист через валідацію типів, використання схем валідації, заборона прямого прокидання user input у queries
- **Path Traversal** — несанкціонований доступ до файлів через маніпуляцію шляхами (../../etc/passwd), захист через whitelist дозволених шляхів, валідацію імен файлів, використання path.resolve() та перевірку результату
- **Command Injection** — виконання системних команд через user input, уникнення child_process.exec() з user input, використання spawn() з масивом аргументів, валідація команд через whitelist
- **OWASP Top 10** — огляд найкритичніших вразливостей для backend: Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration

Розглядаються практичні приклади атак, демонстрація вразливого та захищеного коду, інструменти для тестування безпеки (OWASP ZAP, Burp Suite), регулярні security audits.
