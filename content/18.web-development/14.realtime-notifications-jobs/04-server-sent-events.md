# Server-Sent Events (SSE)

## Короткий зміст

У цій лекції вивчається альтернативний метод real-time комунікації через Server-Sent Events:

- **Концепція SSE** — односторонній канал комунікації server → client через HTTP, сервер може push подій у будь-який момент, клієнт автоматично reconnect при обриві з'єднання
- **Декоратор @Sse()** — створення SSE endpoint у NestJS, повернення Observable для потокової відправки даних, Content-Type: text/event-stream
- **Observable** — використання RxJS Observable для генерації потоку подій, `interval()`, `map()`, `filter()` для трансформації даних, `Subject` для ручного контролю
- **Формат SSE повідомлень** — структура: `data:`, `event:`, `id:`, `retry:`, перевід рядка як delimiter, можливість відправки JSON у data field
- **Порівняння SSE vs WebSocket** — SSE: простіша реалізація, автоматичний reconnect, лише server → client; WebSocket: bi-directional, lower latency, більше можливостей
- **Коли використовувати SSE** — live updates для dashboards, news feeds, stock prices, notifications, моніторинг прогресу задач, будь-які сценарії де потрібен лише push від сервера
- **Підтримка браузерами** — широка підтримка через EventSource API, fallback для старих браузерів через polyfills
- **Інтеграція з frontend** — JavaScript EventSource API, підписка на події, обробка reconnect, closing з'єднання

Розглядаються практичні приклади: live dashboard з метриками, прогрес-бар для завантаження файлів, streaming logs, real-time notifications без WebSocket.
