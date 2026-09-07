# Lifecycle та Rooms у WebSocket

## Короткий зміст

У цій лекції детально вивчається життєвий цикл WebSocket з'єднань та організація клієнтів у групи:

- **OnGatewayInit** — lifecycle hook для ініціалізації Gateway, виконується один раз при старті застосунку, налаштування server instance
- **OnGatewayConnection** — hook викликається при кожному новому підключенні клієнта, отримання socket object, логування підключень, можливість відхилення з'єднання
- **OnGatewayDisconnect** — hook викликається при відключенні клієнта, cleanup операції, видалення з active connections map
- **Tracking connections** — зберігання активних з'єднань у Map або Set, зіставлення socket.id з userId для ідентифікації користувачів
- **Rooms (кімнати)** — логічне групування клієнтів для targeted broadcasting, `socket.join(roomName)` для входу у кімнату, `socket.leave(roomName)` для виходу, приклад: кімната для кожного чату
- **Namespaces** — логічне розділення Gateway на окремі канали (наприклад, /chat, /notifications), кожен namespace має власні rooms та events
- **Broadcasting у rooms** — `server.to(roomName).emit()` для відправки повідомлення всім у кімнаті, `socket.to(roomName).emit()` для всіх у кімнаті окрім відправника
- **Автентифікація WebSocket** — перевірка JWT токена при з'єднанні, витягування userId з токена, зберігання user-socket mapping

Розглядаються практичні сценарії: чат-кімнати для груп, приватні повідомлення між користувачами, broadcast оновлень у конкретну кімнату, моніторинг активних користувачів.
