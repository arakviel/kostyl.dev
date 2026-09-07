# Архітектура системи нотифікацій

## Короткий зміст

У цій лекції розглядається побудова повноцінної системи in-app нотифікацій:

- **Архітектура системи** — компоненти: Notification Entity (БД), NotificationService (бізнес-логіка), WebSocket Gateway (real-time доставка), REST API (історія нотифікацій)
- **Entity для notifications** — структура таблиці: id, userId, message, type (info/warning/error/success), isRead, createdAt, metadata (JSON для додаткових даних)
- **NotificationService** — методи: `create()` для створення нотифікації, `markAsRead()` для позначення прочитаної, `getUnreadCount()` для лічильника, `getUserNotifications()` для історії
- **Real-time доставка** — інтеграція з WebSocket Gateway, відправка події 'notification' при створенні нотифікації, target користувача через userId → socket mapping
- **REST endpoints** — `GET /notifications` для отримання списку, `GET /notifications/unread-count` для badge, `PATCH /notifications/:id/read` для marking as read, `DELETE /notifications/:id` для видалення
- **Типи нотифікацій** — enum NotificationType: POST_LIKE, COMMENT_REPLY, FOLLOW, SYSTEM_ALERT, різні іконки та дії для кожного типу
- **Групування та пагінація** — пагінація для списку нотифікацій, сортування за createdAt DESC, фільтрація за isRead, group by type
- **Push при офлайн** — збереження у БД навіть якщо користувач офлайн, доставка при наступному підключенні

Розглядаються практичні сценарії: нотифікації про нові лайки, коментарі, підписки, системні повідомлення, інтеграція з frontend для real-time badge оновлення.
