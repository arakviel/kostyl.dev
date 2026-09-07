# WebSocket Gateway у NestJS

## Короткий зміст

У цій лекції вивчається практична реалізація WebSocket сервера у NestJS з використанням Socket.IO:

- **Декоратор @WebSocketGateway()** — створення WebSocket gateway класу, конфігурація порту та namespace, опції для Socket.IO (cors, transports, path)
- **Інтеграція Socket.IO** — популярна бібліотека для WebSocket з fallback на long-polling, інсталяція `@nestjs/websockets` та `@nestjs/platform-socket.io`, адаптер для Socket.IO
- **Декоратор @SubscribeMessage()** — обробка подій від клієнта, прив'язка методу до події (наприклад, 'message', 'chat'), отримання payload події
- **Емітування подій** — відправка даних клієнту через `socket.emit()` для одного клієнта, `server.emit()` для всіх підключених, acknowledgments для підтвердження доставки
- **Broadcasting** — розсилка повідомлень: `socket.broadcast.emit()` для всіх окрім відправника, `server.to(room).emit()` для конкретної кімнати
- **Налаштування CORS** — дозвіл WebSocket з'єднань з frontend домену, конфігурація через `cors: { origin: 'http://localhost:3000' }` у gateway options
- **Dependency Injection** — ін'єкція сервісів у Gateway через constructor, використання репозиторіїв для збереження повідомлень

Розглядаються практичні приклади: створення простого чату, відправка повідомлень між користувачами, інтеграція з JWT автентифікацією для WebSocket.
