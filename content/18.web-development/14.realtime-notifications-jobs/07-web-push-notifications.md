# Web Push нотифікації

## Короткий зміст

У цій лекції розглядається реалізація браузерних push-нотифікацій через Web Push API:

- **Web Push API** — стандарт для відправки нотифікацій у браузер навіть коли сайт закритий, підтримка Chrome, Firefox, Edge, Safari (з iOS 16.4+)
- **Service Workers** — фоновий скрипт для отримання push подій, реєстрація Service Worker, обробка події 'push', показ notification через Notification API
- **VAPID ключі** — пара public/private ключів для автентифікації push сервера, генерація через `web-push generate-vapid-keys`, публічний ключ передається на frontend, приватний — на backend
- **Бібліотека web-push** — Node.js бібліотека для відправки push через Web Push Protocol, метод `sendNotification(subscription, payload, options)`
- **Push subscription** — об'єкт з endpoint та keys (p256dh, auth), отримується на frontend через `serviceWorkerRegistration.pushManager.subscribe()`, передається на backend для збереження
- **Subscription management** — Entity для зберігання subscriptions (userId, endpoint, keys, device info), CRUD операції: create subscription при subscribe, delete при unsubscribe
- **Відправка push** — метод у Service для відправки push всім subscriptions користувача, payload у форматі JSON з title, body, icon, badge, actions
- **Permissions** — запит дозволу на нотифікації через `Notification.requestPermission()`, handling відмови, re-request logic

Розглядаються практичні приклади: підписка на push при вході, відправка push при новому повідомленні, click handling у Service Worker, deep links у застосунок, fallback для браузерів без підтримки.
