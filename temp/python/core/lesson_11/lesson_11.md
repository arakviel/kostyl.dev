# 🤖 Створення Telegram-ботів за допомогою pyTelegramBotAPI (синхронний підхід)

## Зміст

### Вступ до Telegram-ботів
1.  [Що таке Telegram-бот?](#що-таке-telegram-бот)
2.  [Можливості Telegram-ботів](#можливості-telegram-ботів)
3.  [Як працюють боти: polling vs. webhooks](#як-працюють-боти-polling-vs-webhooks)
4.  [Створення бота та отримання токена через BotFather](#створення-бота-та-отримання-токена-через-botfather)

### Підготовка середовища
5.  [Створення віртуального середовища](#створення-віртуального-середовища)
6.  [Встановлення бібліотеки `pyTelegramBotAPI`](#встановлення-бібліотеки-pytelegrambotapi)

### Ваш перший бот: "Привіт, Світ!"
7.  [Ініціалізація бота](#ініціалізація-бота)
8.  [Обробник команди `/start`](#обробник-команди-start)
9.  [Надсилання текстових повідомлень: `bot.send_message()`](#надсилання-текстових-повідомлень-botsend_message)
10. [Запуск бота: `bot.polling()`](#запуск-бота-botpolling)
11. [Повний код першого бота](#повний-код-першого-бота)

### Типи обробників повідомлень
12. [Обробка інших команд](#обробка-інших-команд)
13. [Обробка текстових повідомлень (фільтрація)](#обробка-текстових-повідомлень-фільтрація)
14. [Обробка повідомлень за регулярним виразом: `regexp`](#обробка-повідомлень-за-регулярним-виразом-regexp)
15. [Обробка різних типів контенту: `content_types`](#обробка-різних-типів-контенту-content_types)

### Відповіді та надсилання різного контенту
16. [Відповідь на повідомлення: `bot.reply_to()`](#відповідь-на-повідомлення-botreply_to)
17. [Надсилання фото, аудіо, документів, стікерів](#надсилання-фото-аудіо-документів-стікерів)
    -   [Надсилання фото](#надсилання-фото)
    -   [Надсилання документів](#надсилання-документів)
    -   [Надсилання стікерів](#надсилання-стікерів)
18. [Пересилання повідомлень: `bot.forward_message()`](#пересилання-повідомлень-botforward_message)

### Інтерактивні елементи: клавіатури
19. [Клавіатури у Telegram-ботах](#клавіатури-у-telegram-ботах)
20. [Звичайна клавіатура: `ReplyKeyboardMarkup`](#звичайна-клавіатура-replykeyboardmarkup)
    -   [Створення та використання](#створення-та-використання)
    -   [Параметри клавіатури](#параметри-клавіатури)
21. [Вбудована (inline) клавіатура: `InlineKeyboardMarkup`](#вбудована-inline-клавіатура-inlinekeyboardmarkup)
    -   [Створення Inline-клавіатури](#створення-inline-клавіатури)
    -   [Обробка натискань на Inline-кнопки: `callback_query_handler`](#обробка-натискань-на-inline-кнопки-callback_query_handler)
    -   [Оновлення повідомлень з Inline-клавіатурою](#оновлення-повідомлень-з-inline-клавіатурою)

### Управління станом користувача (базовий підхід)
22. [Навіщо керувати станом?](#навіщо-керувати-станом)
23. [Зберігання стану у словнику в пам'яті](#зберігання-стану-у-словнику-в-памяті)
24. [Приклад: покрокове опитування користувача](#приклад-покрокове-опитування-користувача)

### Обробка помилок та логування
25. [Базова обробка помилок](#базова-обробка-помилок)
26. [Логування у боті](#логування-у-боті)

### Запуск бота та деплоймент
27. [Робота бота у фоновому режимі](#робота-бота-у-фоновому-режимі)
28. [Використання `nohup` (Linux/macOS)](#використання-nohup-linuxmacos)

### Висновки та подальші кроки
29. [Підсумки](#підсумки-1)
30. [Куди рухатись далі?](#куди-рухатись-далі)

---

## Вступ до Telegram-ботів

### Що таке Telegram-бот?

**Telegram-бот** — це спеціальний обліковий запис у Telegram, яким керує програма, а не людина. Боти можуть відповідати на повідомлення, виконувати команди, надсилати різний медіаконтент і навіть взаємодіяти з веб-службами.

**Простими словами:** Ваш бот — це як віртуальний співрозмовник у Telegram, який може робити безліч корисних речей автоматично, відповідно до вашого коду.

### Можливості Telegram-ботів

Боти в Telegram можуть бути надзвичайно функціональними:
*   **Інформаційні боти:** Надсилають новини, погоду, курси валют, розклад.
*   **Сервісні боти:** Нагадування, конвертери, перекладачі, менеджери завдань.
*   **Ігрові боти:** Прості ігри, вікторини.
*   **Боти-помічники:** Оформлення замовлень, підтримка клієнтів, бронювання.
*   **Інтеграційні боти:** Зв'язок з іншими сервісами (GitHub, Trello, CRM-системи).
*   **Медіа-боти:** Пошук та надсилання музики, відео, зображень.

Практично будь-яку рутинну задачу, що передбачає текстову або просту медіа-взаємодію, можна автоматизувати за допомогою бота.

### Як працюють боти: polling vs. webhooks

Існує два основні способи, якими бот отримує оновлення (повідомлення, команди тощо) від користувачів:

1.  **Polling (опитування):** Бот періодично "запитує" сервери Telegram: "Чи є для мене нові повідомлення?". Якщо є, він їх забирає і обробляє.
    *   **Переваги:** Простий у налаштуванні, не вимагає публічної IP-адреси або домену.
    *   **Недоліки:** Може бути менш ефективним для дуже великих навантажень (багато запитів до серверів).
    *   **Наш підхід:** Ми будемо використовувати polling, оскільки він ідеально підходить для синхронного програмування та початкового вивчення.

2.  **Webhooks (вебхуки):** Ви налаштовуєте свій сервер, і коли приходить нове повідомлення, сервери Telegram **самі надсилають** це повідомлення на вашу унікальну URL-адресу.
    *   **Переваги:** Миттєва реакція, більш масштабований для великих проектів.
    *   **Недоліки:** Вимагає публічного домену/IP та SSL-сертифіката, складніший у налаштуванні.
    *   **Чому не зараз:** Для webhooks часто потрібне асинхронне програмування (бо сервер має вміти обробляти багато запитів одночасно), тому ми його поки що не розглядаємо.

### Створення бота та отримання токена через BotFather

Щоб створити бота, вам потрібен обліковий запис Telegram. Весь процес відбувається прямо в Telegram за допомогою спеціального бота під назвою **BotFather**.

**Кроки:**
1.  **Знайдіть BotFather:** Відкрийте Telegram і в пошуку наберіть `@BotFather`. Оберіть офіційного бота (з синьою галочкою).
2.  **Запустіть BotFather:** Натисніть "Start" або відправте `/start`.
3.  **Створіть нового бота:** Відправте команду `/newbot`.
4.  **Виберіть ім'я бота:** BotFather попросить вас ввести відображуване ім'я для вашого бота. Це ім'я, яке бачитимуть користувачі (наприклад, "Мій Перший Бот").
5.  **Виберіть username для бота:** Після цього BotFather попросить вас ввести унікальний username для бота. Це ім'я має закінчуватися на `bot` (наприклад, `MyFirstPythonBot`, `AwesomeHelperBot`). Воно має бути унікальним у всій системі Telegram.
6.  **Отримайте токен:** Якщо username успішний, BotFather надішле вам повідомлення з **токеном** вашого бота. Токен виглядає як довгий рядок символів (наприклад, `123456789:AAH_random_string_of_characters`).

**⚠️ УВАГА:** Токен вашого бота — це як пароль. Нікому його не показуйте і не публікуйте у відкритих репозиторіях (наприклад, на GitHub). Якщо токен потрапить у чужі руки, ваш бот може бути зламаний. Для безпечного зберігання токена ми будемо використовувати змінні середовища або окремий файл, який не буде додаватися до контролю версій.

---

## Підготовка середовища

Ми будемо працювати у Python, тому потрібно підготувати наше робоче місце.

### Створення віртуального середовища

Це повторення матеріалу з попередньої лекції, але це **критично важливо** для будь-якого Python-проекту.

1.  **Створіть папку для проекту:**
    ```bash
    mkdir telegram_bot_project
    cd telegram_bot_project
    ```
2.  **Створіть віртуальне середовище:**
    ```bash
    python -m venv venv
    ```
3.  **Активуйте віртуальне середовище:**
    *   **Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux (bash/zsh):**
        ```bash
        source venv/bin/activate
        ```
    Після активації в командному рядку з'явиться `(venv)` на початку.

### Встановлення бібліотеки `pyTelegramBotAPI`

Тепер, коли середовище активоване, ми можемо встановити бібліотеку.

```bash
pip install pyTelegramBotAPI
```
Перевірте, що бібліотека встановлена:
```bash
pip list
```
Ви повинні побачити `pyTelegramBotAPI` у списку.

---
## Ваш перший бот: "Привіт, Світ!"

Давайте напишемо найпростішого бота, який буде відповідати на команду `/start`.

### Ініціалізація бота

Створіть файл `bot.py` у папці `telegram_bot_project`.

Зберігайте токен бота в змінній середовища або в окремому файлі, який ви не будете комітити в Git. Для простоти прикладу, ми поки що залишимо його прямо в коді, але **в реальних проектах так робити не можна!**

```python
# bot.py
import telebot
import os

# ⚠️ УВАГА: У реальних проектах токен слід брати зі змінних середовища
# BOT_TOKEN = os.environ.get('BOT_TOKEN')
# або з конфігураційного файлу, який не комітиться в Git.
# Для прикладу - хардкодимо. ЗАМІНІТЬ 'YOUR_BOT_TOKEN' НА ВАШ ТОКЕН!
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Ініціалізуємо бота, передаючи йому токен
# Цей об'єкт 'bot' буде нашим інтерфейсом для взаємодії з Telegram API.
bot = telebot.TeleBot(BOT_TOKEN)

print("Бот ініціалізовано. Готовий до запуску...")
```
Замініть `YOUR_BOT_TOKEN` на токен, який вам надав BotFather.

### Обробник команди `/start`

Щоб бот реагував на певні повідомлення, нам потрібні **обробники (handlers)**. Обробник — це звичайна функція Python, яку бібліотека викликає, коли отримує повідомлення, що відповідає певним критеріям.

Ми використовуємо декоратор `@bot.message_handler()` для реєстрації функції як обробника.

```python
# bot.py (продовження)

# Цей декоратор каже, що функція 'send_welcome' має обробляти повідомлення
# типу "команда" (commands), а саме команду "/start".
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Ця функція буде викликана, коли користувач відправить команду /start.
    'message' - це об'єкт, що містить всю інформацію про отримане повідомлення.
    """
    # message.chat.id - унікальний ID чату, куди потрібно відправити відповідь.
    # message.from_user.first_name - ім'я користувача, який відправив повідомлення.
    bot.send_message(message.chat.id, 
                     f"Привіт, {message.from_user.first_name}! Я твій перший Telegram-бот.")
    bot.send_message(message.chat.id, 
                     "Я вмію відповідати на команду /start.")
    print(f"Користувач {message.from_user.username} ({message.chat.id}) відправив /start.")

```

### Надсилання текстових повідомлень: `bot.send_message()`

Метод `bot.send_message()` — це основний спосіб надсилання текстових повідомлень користувачам.
*   Перший аргумент: `chat_id` (куди надсилати).
*   Другий аргумент: `text` (що надсилати).

Ви можете використовувати HTML або Markdown для форматування тексту, вказавши параметр `parse_mode`.

```python
# bot.py (продовження)

# Приклад форматування тексту
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "<b>Доступні команди:</b>\n" \
                "/start - Почати взаємодію\n" \
                "/help - Показати цю довідку\n" \
                "<i>Надішліть будь-який текст, і я спробую відповісти.</i>"
    
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')
    print(f"Користувач {message.from_user.username} запитав /help.")

```

### Запуск бота: `bot.polling()`

Щоб бот почав працювати і отримувати повідомлення, його потрібно запустити. Метод `bot.polling()` запускає цикл опитування, який постійно перевіряє нові повідомлення на серверах Telegram.

```python
# bot.py (продовження)

if __name__ == '__main__':
    print("Бот запускається...")
    # non_stop=True - бот не зупиниться при виникненні помилок,
    # а спробує продовжити роботу.
    # interval=0 - як часто опитувати нові повідомлення (у секундах, 0 - максимально швидко).
    bot.polling(non_stop=True, interval=0)
    print("Бот зупинено.") # Цей рядок буде виведений тільки після зупинки polling (напр., Ctrl+C)
```
**Важливо:** `bot.polling()` блокує виконання програми. Це означає, що весь код після `bot.polling()` не буде виконаний, поки бот працює.

### Повний код першого бота

Створіть файл `main.py` (або `bot.py`) та вставте в нього цей код.

```python
# main.py
import telebot
import os

# ⚠️ УВАГА: ЗАМІНІТЬ 'YOUR_BOT_TOKEN' НА ВАШ ТОКЕН!
# У реальних проектах токен слід брати зі змінних середовища.
# Наприклад: BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
BOT_TOKEN = 'YOUR_BOT_TOKEN'

if BOT_TOKEN == 'YOUR_BOT_TOKEN':
    print("⚠️ Будь ласка, замініть 'YOUR_BOT_TOKEN' на реальний токен вашого бота!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name if message.from_user.first_name else "друже"
    bot.send_message(message.chat.id, 
                     f"Привіт, {user_name}! Я твій перший Telegram-бот.👋")
    bot.send_message(message.chat.id, 
                     "Я вмію відповідати на команди /start та /help.")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} відправив /start.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "<b>Доступні команди:</b>\n" \
                "/start - Почати взаємодію з ботом\n" \
                "/help - Показати цю довідку\n" \
                "<i>Спробуй надіслати мені будь-який текст.</i>"
    
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} запитав /help.")

# Обробник для будь-якого текстового повідомлення, яке не є командою
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text) # Бот просто повторює текст користувача
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} надіслав: '{message.text}'")

if __name__ == '__main__':
    print("Бот запускається...")
    try:
        # non_stop=True: бот не зупиняється при виникненні помилок
        # interval=0: опитує нові повідомлення якомога швидше
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(f"Бот зупинено через помилку: {e}")
    finally:
        print("Бот зупинено.")

```
Збережіть файл, замініть токен і запустіть його: `python main.py`. Тепер відкрийте Telegram, знайдіть свого бота за username і відправте йому `/start`!

---
## Типи обробників повідомлень

`pyTelegramBotAPI` пропонує різні способи фільтрації повідомлень для обробників, що дозволяє створювати гнучку логіку бота.

### Обробка інших команд

Ми вже бачили `commands=['start']`. Можна вказати список команд.

```python
# ...
@bot.message_handler(commands=['about', 'info'])
def send_about(message):
    bot.send_message(message.chat.id, 
                     "Цей бот створено в рамках курсу Python Core.")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} запитав /about.")
# ...
```

### Обробка текстових повідомлень (фільтрація)

За допомогою параметра `func` в `@bot.message_handler()` можна передати функцію, яка повертає `True` або `False` для фільтрації повідомлень.

```python
# ...
# Обробник для повідомлень, що містять слово "привіт"
@bot.message_handler(func=lambda message: "привіт" in message.text.lower())
def handle_hello(message):
    bot.send_message(message.chat.id, "Привіт! Радий тебе чути!")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} привітався.")

# Обробник для повідомлень, що містять слово "як справи"
@bot.message_handler(func=lambda message: "як справи" in message.text.lower())
def handle_how_are_you(message):
    bot.send_message(message.chat.id, "Все чудово! Працюю :)")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} запитав як справи.")

# Якщо функція-фільтр повертає True, обробник буде викликаний.
# Якщо у вас є декілька обробників, повідомлення буде оброблене першим обробником,
# фільтр якого повернув True. Порядок реєстрації обробників має значення.
# Тому обробники для специфічних випадків краще ставити вище, ніж загальні.
# Наприклад, `func=lambda message: True` (який завжди True) завжди має бути останнім.

```

### Обробка повідомлень за регулярним виразом: `regexp`

Для більш складної фільтрації тексту можна використовувати регулярні вирази за допомогою параметра `regexp`.

```python
# ...
import re

# Обробник для повідомлень, що містять числа (наприклад, "моє число 123")
@bot.message_handler(regexp=r".*\d+.*") # будь-який текст, що містить хоча б одну цифру
def handle_numbers(message):
    numbers = re.findall(r'\d+', message.text)
    bot.send_message(message.chat.id, f"Я знайшов числа у твоєму повідомленні: {', '.join(numbers)}")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} надіслав текст з числами.")
# ...
```

### Обробка різних типів контенту: `content_types`

Боти можуть реагувати не тільки на текст, але й на фотографії, стікери, аудіо, відео, файли та багато іншого.

```python
# ...
# Обробник для фотографій
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # message.photo - це список об'єктів PhotoSize.
    # Останній елемент у списку зазвичай є фотографією найбільшої якості/розміру.
    file_id = message.photo[-1].file_id
    bot.send_message(message.chat.id, "Дякую за фото! Я отримав його.")
    # Якщо хочете зберегти фото, потрібно додатково отримати file_path
    # file_info = bot.get_file(file_id)
    # downloaded_file = bot.download_file(file_info.file_path)
    # with open("downloaded_photo.jpg", 'wb') as new_file:
    #    new_file.write(downloaded_file)
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} надіслав фото (file_id: {file_id}).")

# Обробник для стікерів
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id) # Бот повторить стікер
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} надіслав стікер.")

# Можна вказати декілька типів контенту
@bot.message_handler(content_types=['audio', 'video', 'document'])
def handle_media(message):
    bot.send_message(message.chat.id, "Я отримав від тебе медіафайл або документ.")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} надіслав медіа.")

```
Повний список `content_types` можна знайти в документації `pyTelegramBotAPI`.

---
## Відповіді та надсилання різного контенту

Бот може не тільки надсилати прості текстові повідомлення, а й більш складні відповіді.

### Відповідь на повідомлення: `bot.reply_to()`

`bot.reply_to(message, text)` надсилає повідомлення, яке виглядає як відповідь на повідомлення користувача.

```python
# ...
@bot.message_handler(func=lambda message: "добре" in message.text.lower())
def handle_fine(message):
    bot.reply_to(message, "Це чудово! Продовжуємо працювати :)")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} відповів 'добре'.")
```

### Надсилання фото, аудіо, документів, стікерів

Кожен тип контенту має свій метод `bot.send_...()`.

#### Надсилання фото
Можна надсилати фото за:
1.  **URL-адресою**
2.  **`file_id`** (якщо фото вже завантажувалось в Telegram, це економить трафік)
3.  **Локальним шляхом до файлу**

```python
# ...
@bot.message_handler(commands=['photo'])
def send_random_photo(message):
    # Надсилаємо фото за URL
    bot.send_photo(message.chat.id, "https://picsum.photos/200/300", 
                   caption="Ось випадкове фото з інтернету!")
    
    # Надсилаємо фото за локальним шляхом (переконайтесь, що 'my_photo.jpg' існує)
    # with open('my_photo.jpg', 'rb') as photo:
    #     bot.send_photo(message.chat.id, photo, caption="Моє локальне фото.")

    # Надсилаємо фото за file_id (якщо ви вже його отримали раніше)
    # photo_file_id = "AgACAgIAAxkBAAI..." # Приклад file_id
    # bot.send_photo(message.chat.id, photo_file_id)
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} запитав фото.")
```

#### Надсилання документів
Надсилання документів (`.pdf`, `.docx` тощо) аналогічно фото.

```python
# ...
@bot.message_handler(commands=['document'])
def send_document_example(message):
    # Надсилаємо документ за URL
    # bot.send_document(message.chat.id, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf")
    
    # Надсилаємо локальний документ (переконайтесь, що 'my_document.pdf' існує)
    # with open('my_document.pdf', 'rb') as doc:
    #     bot.send_document(message.chat.id, doc, caption="Корисний документ.")
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} запитав документ.")
```

#### Надсилання стікерів
```python
# ...
@bot.message_handler(commands=['sticker'])
def send_cool_sticker(message):
    # Щоб отримати file_id стікера:
    # 1. Надсилайте стікер боту @idstickerbot.
    # 2. Він дасть вам file_id стікера.
    # Приклад file_id
    sticker_id = "CAACAgIAAxkBAAEExw8mB9k_Y-jK4J7mR_uP5j_1Y_oAAQACAwADwDZPE3Yf-5g0AAAAAAEC"
    bot.send_sticker(message.chat.id, sticker_id)
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} запитав стікер.")
```

### Пересилання повідомлень: `bot.forward_message()`

Ви можете пересилати будь-яке повідомлення від одного користувача (або чату) до іншого.

```python
# ...
# Обробник для пересилання повідомлень
@bot.message_handler(commands=['forwardme'])
def forward_message_example(message):
    # Пересилаємо повідомлення користувача (те, на яке він відповість цією командою)
    # до нього ж самого. Можна пересилати в будь-який chat_id
    bot.forward_message(message.chat.id, # Куди пересилаємо
                        message.chat.id, # Звідки беремо повідомлення
                        message.message_id) # ID повідомлення, яке пересилаємо
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} попросив переслати.")
```

---
## Інтерактивні елементи: клавіатури

Клавіатури дозволяють зробити бота більш інтерактивним, надаючи користувачеві кнопки замість необхідності вводити текст.

### Клавіатури у Telegram-ботах

Існує два основні типи клавіатур:
1.  **Звичайна (Reply Keyboard):** З'являється над полем вводу тексту, замінюючи стандартну клавіатуру. При натисканні кнопки її текст надсилається боту як звичайне повідомлення. Може бути прихована.
2.  **Вбудована (Inline Keyboard):** З'являється прямо під повідомленням бота. При натисканні кнопки боту надсилається спеціальний `callback_query`, а не текстове повідомлення. Не зникає сама по собі.

### Звичайна клавіатура: `ReplyKeyboardMarkup`

#### Створення та використання

```python
# ...
from telebot import types

@bot.message_handler(commands=['keyboard'])
def send_keyboard(message):
    # Створюємо об'єкт клавіатури
    markup = types.ReplyKeyboardMarkup(row_width=2) # row_width=2 означає 2 кнопки в рядку

    # Створюємо кнопки
    itembtn1 = types.KeyboardButton('Привіт')
    itembtn2 = types.KeyboardButton('Як справи?')
    itembtn3 = types.KeyboardButton('Покажи фото')
    itembtn4 = types.KeyboardButton('Приховати клавіатуру')

    # Додаємо кнопки до клавіатури
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    # Надсилаємо повідомлення з клавіатурою
    bot.send_message(message.chat.id, "Обери опцію:", reply_markup=markup)
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} отримав звичайну клавіатуру.")

# Обробник для тексту кнопок звичайної клавіатури
@bot.message_handler(func=lambda message: message.text == 'Привіт')
def handle_button_hello(message):
    bot.send_message(message.chat.id, "І тобі привіт!")

@bot.message_handler(func=lambda message: message.text == 'Як справи?')
def handle_button_how_are_you(message):
    bot.send_message(message.chat.id, "В мене все чудово, дякую, що запитав!")

@bot.message_handler(func=lambda message: message.text == 'Покажи фото')
def handle_button_show_photo(message):
    bot.send_photo(message.chat.id, "https://picsum.photos/200/300")

# Приховати клавіатуру
@bot.message_handler(func=lambda message: message.text == 'Приховати клавіатуру')
def hide_keyboard(message):
    # ReplyKeyboardRemove приховує ReplyKeyboardMarkup
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Клавіатуру приховано.", reply_markup=markup)
```

#### Параметри клавіатури
`ReplyKeyboardMarkup` має кілька корисних параметрів:
-   `row_width`: кількість кнопок у одному рядку.
-   `resize_keyboard=True`: автоматично підлаштовує розмір клавіатури.
-   `one_time_keyboard=True`: клавіатура приховується після першого натискання.
-   `selective=True`: клавіатура відображається тільки для вибраних користувачів (у групових чатах).

```python
# ...
@bot.message_handler(commands=['onetimereply'])
def send_one_time_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Так'), types.KeyboardButton('Ні'))
    bot.send_message(message.chat.id, "Це одноразова клавіатура?", reply_markup=markup)
```

### Вбудована (inline) клавіатура: `InlineKeyboardMarkup`

Inline-клавіатура прикріплюється до самого повідомлення. Коли користувач натискає на Inline-кнопку, боту надсилається `CallbackQuery` замість звичайного текстового повідомлення. Це дозволяє створювати складніші інтерактивні інтерфейси.

#### Створення Inline-клавіатури

```python
# ...
@bot.message_handler(commands=['inline'])
def send_inline_keyboard(message):
    markup = types.InlineKeyboardMarkup(row_width=2) # row_width також працює тут

    # InlineKeyboardButton може мати різні типи дій:
    # callback_data: дані, які будуть надіслані боту (обробляються callback_query_handler)
    # url: відкрити посилання
    # switch_inline_query: почати inline-запит
    # switch_inline_query_current_chat: почати inline-запит у поточному чаті

    itembtnA = types.InlineKeyboardButton('Кнопка A', callback_data='button_A_pressed')
    itembtnB = types.InlineKeyboardButton('Кнопка B', callback_data='button_B_pressed')
    itembtnC = types.InlineKeyboardButton('Google', url='https://www.google.com')
    itembtnD = types.InlineKeyboardButton('Показати ID', callback_data='show_chat_id')

    markup.add(itembtnA, itembtnB, itembtnC, itembtnD)

    bot.send_message(message.chat.id, "Обери опцію (inline):", reply_markup=markup)
    print(f"[{message.chat.id}] Користувач @{message.from_user.username} отримав inline-клавіатуру.")

```

#### Обробка натискань на Inline-кнопки: `callback_query_handler`

Натискання на Inline-кнопки обробляються окремим типом обробника — `@bot.callback_query_handler()`.

```python
# ...
@bot.callback_query_handler(func=lambda call: True) # Обробляє всі callback-запити
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'button_A_pressed':
                bot.send_message(call.message.chat.id, "Ти натиснув кнопку A!")
                print(f"[{call.message.chat.id}] Користувач @{call.message.from_user.username} натиснув кнопку A.")
            elif call.data == 'button_B_pressed':
                bot.send_message(call.message.chat.id, "Ти натиснув кнопку B!")
                print(f"[{call.message.chat.id}] Користувач @{call.message.from_user.username} натиснув кнопку B.")
            elif call.data == 'show_chat_id':
                bot.send_message(call.message.chat.id, f"ID цього чату: <code>{call.message.chat.id}</code>", parse_mode='HTML')
                print(f"[{call.message.chat.id}] Користувач @{call.message.from_user.username} запитав chat ID.")
            
            # Важливо! Після обробки callback-запиту потрібно викликати answer_callback_query
            # Це прибирає "годинник" з кнопки та дозволяє відправити сповіщення користувачеві
            bot.answer_callback_query(call.id, text="Вибір прийнято!") 

    except Exception as e:
        print(f"Помилка в callback_inline: {e}")
```

#### Оновлення повідомлень з Inline-клавіатурою

Часто при роботі з Inline-клавіатурами зручно змінювати (редагувати) вже надіслане повідомлення бота, щоб уникнути спаму або відобразити новий стан.

```python
# ...
@bot.message_handler(commands=['edit_message'])
def send_editable_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Змінити текст", callback_data="edit_text"))
    bot.send_message(message.chat.id, "Оригінальне повідомлення.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "edit_text")
def edit_message_callback(call):
    if call.message:
        # Редагуємо повідомлення: змінюємо текст та прибираємо клавіатуру
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Текст повідомлення було змінено! Клавіатуру прибрано.")
        bot.answer_callback_query(call.id, text="Повідомлення оновлено.")
```

---
## Управління станом користувача (базовий підхід)

Боти stateless (безстатусними) за своєю природою — кожен запит обробляється незалежно. Але для складної взаємодії (наприклад, покрокове опитування) боту потрібно "пам'ятати" попередні дії користувача.

### Навіщо керувати станом?

*   **Покрокові процеси:** Реєстрація, замовлення, анкети.
*   **Контекст розмови:** Розуміння, про що користувач говорить зараз.
*   **Персоналізація:** Зберігання налаштувань користувача.

Для складних ботів зазвичай використовують бази даних (SQL, NoSQL), але для простих випадків можна обійтися словником у пам'яті.

### Зберігання стану у словнику в пам'яті

Ми можемо використовувати глобальний словник, де ключем буде `chat_id` користувача, а значенням — його поточний стан або дані.

```python
# bot.py (глобальна змінна)
user_states = {} # Словник для зберігання стану користувачів
# Наприклад: {chat_id: 'awaiting_name', chat_id: 'awaiting_age'}
user_data = {}   # Словник для тимчасового зберігання даних користувача
# Наприклад: {chat_id: {'name': 'Іван', 'age': None}}
```

### Приклад: покрокове опитування користувача

Давайте зробимо бота, який запитає ім'я та вік користувача.

```python
# ...
from telebot import types

# Глобальні словники для стану та даних
user_states = {} # {chat_id: 'step_name' або 'step_age'}
user_data = {}   # {chat_id: {'name': '...', 'age': ...}}


@bot.message_handler(commands=['register'])
def cmd_register(message):
    chat_id = message.chat.id
    user_states[chat_id] = 'awaiting_name'
    user_data[chat_id] = {} # Очищуємо попередні дані
    bot.send_message(chat_id, "Привіт! Давай зареєструємось. Як тебе звати?")
    print(f"[{chat_id}] Користувач @{message.from_user.username} почав реєстрацію.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_name')
def get_name(message):
    chat_id = message.chat.id
    name = message.text
    user_data[chat_id]['name'] = name
    user_states[chat_id] = 'awaiting_age'
    bot.send_message(chat_id, f"Приємно познайомитись, {name}! Скільки тобі років?")
    print(f"[{chat_id}] Користувач @{message.from_user.username} ввів ім'я: {name}.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_age')
def get_age(message):
    chat_id = message.chat.id
    try:
        age = int(message.text)
        if age <= 0 or age > 120:
            raise ValueError("Невірний вік")
        
        user_data[chat_id]['age'] = age
        
        final_name = user_data[chat_id]['name']
        final_age = user_data[chat_id]['age']
        
        bot.send_message(chat_id, 
                         f"Дякую, {final_name}! Тобі {final_age} років. Реєстрацію завершено.")
        
        # Очищуємо стан після завершення
        del user_states[chat_id]
        del user_data[chat_id]
        print(f"[{chat_id}] Користувач @{message.from_user.username} завершив реєстрацію: {final_name}, {final_age}.")

    except (ValueError, KeyError):
        bot.send_message(chat_id, "Будь ласка, введи коректний вік числом.")
        print(f"[{chat_id}] Користувач @{message.from_user.username} ввів невірний вік.")

# Не забувайте, що порядок обробників має значення.
# Цей обробник має бути ПІСЛЯ всіх обробників, які перевіряють стан.
# Інакше він може перехопити повідомлення, призначене для get_name або get_age.
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#    # ...
```
Це базовий підхід. У реальних проектах для керування станом використовують спеціалізовані бібліотеки (наприклад, FSM - Finite State Machine) або бази даних.

---
## Обробка помилок та логування

Будь-яка програма може містити помилки. Важливо, щоб ваш бот був стійким і продовжував працювати, навіть якщо виникли непередбачені ситуації.

### Базова обробка помилок

Метод `bot.polling()` має параметр `on_polling_error`, який можна використовувати для обробки помилок, що виникають під час опитування.

Також, кожний обробник можна обгортати в `try...except` блок.

```python
# ...
import logging

# Налаштовуємо базове логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Функція для обробки помилок polling
def polling_error_handler(error_string):
    logging.error(f"Помилка при polling: {error_string}")

# ... (ваш код бота)

@bot.message_handler(commands=['divide'])
def handle_divide(message):
    try:
        parts = message.text.split() # /divide 10 2
        num1 = float(parts[1])
        num2 = float(parts[2])
        result = num1 / num2
        bot.send_message(message.chat.id, f"Результат ділення: {result}")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Будь ласка, вкажіть два числа: /divide <число1> <число2>")
    except ZeroDivisionError:
        bot.send_message(message.chat.id, "На нуль ділити не можна!")
    except Exception as e:
        logging.error(f"Невідома помилка в handle_divide: {e}")
        bot.send_message(message.chat.id, "Виникла невідома помилка. Спробуйте пізніше.")


if __name__ == '__main__':
    logging.info("Бот запускається...")
    try:
        bot.polling(non_stop=True, interval=0, on_polling_error=polling_error_handler)
    except Exception as e:
        logging.critical(f"Критична помилка запуску бота: {e}")
    finally:
        logging.info("Бот зупинено.")

```
Логування допомагає відстежувати роботу бота та діагностувати проблеми без прямого доступу до консолі.

### Логування у боті

Модуль `logging` — це стандартний спосіб для запису інформації про події, помилки та стан програми.

```python
import logging

# Базова конфігурація логування
# level=logging.INFO означає, що будуть записуватися повідомлення INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("bot.log", encoding="utf-8"), # Запис у файл
                        logging.StreamHandler() # Вивід у консоль
                    ])

logger = logging.getLogger(__name__) # Отримуємо логер для поточного модуля

# Приклад використання в коді бота:
# logger.info("Бот запущено.")
# logger.warning("Отримано невідому команду.")
# logger.error("Не вдалося відправити повідомлення користувачеві %s", message.chat.id)
```

---
## Запуск бота та деплоймент

Ваш бот працює, поки працює скрипт Python. Якщо ви закриєте термінал, бот зупиниться. Для постійної роботи бота потрібен більш надійний спосіб.

### Робота бота у фоновому режимі

На сервері (Linux-системи) для запуску скриптів у фоновому режимі часто використовують утиліти `nohup` або `screen`/`tmux`. Для більш серйозних проектів застосовують `systemd` або Docker.

### Використання `nohup` (Linux/macOS)

`nohup` дозволяє запускати команду так, що вона ігнорує сигнал SIGHUP (що надсилається терміналу при його закритті).

```bash
# Перейдіть у папку проекту
cd telegram_bot_project

# Активуйте віртуальне середовище
source venv/bin/activate

# Запустіть бота
nohup python main.py > bot.log 2>&1 &
```
Пояснення команди:
*   `nohup`: запускає команду, роблячи її стійкою до розриву зв'язку терміналу.
*   `python main.py`: запускає ваш скрипт бота.
*   `> bot.log`: перенаправляє стандартний вивід у файл `bot.log`.
*   `2>&1`: перенаправляє стандартний потік помилок (stderr) також у `bot.log`.
*   `&`: запускає команду у фоновому режимі, звільняючи термінал.

Щоб перевірити, чи працює бот:
```bash
ps aux | grep main.py
```
Щоб зупинити бота:
```bash
kill <PID> # PID - це номер процесу, який ви отримаєте з ps aux
```
Для професійного деплойменту варто розглянути хостинги, які спеціалізуються на Python (Heroku, PythonAnywhere, DigitalOcean) або використання Docker.

---
## Висновки та подальші кроки

### Підсумки

Ви успішно навчились створювати Telegram-бота за допомогою бібліотеки `pyTelegramBotAPI`, використовуючи синхронний підхід. Ми розглянули:
*   Створення бота через BotFather.
*   Ініціалізацію та запуск бота.
*   Обробку різних типів повідомлень та команд.
*   Надсилання різного контенту (текст, фото, стікери).
*   Створення інтерактивних клавіатур (`ReplyKeyboardMarkup`, `InlineKeyboardMarkup`).
*   Базове керування станом користувача.
*   Обробку помилок та логування.
*   Прості способи запуску бота у фоновому режимі.

### Куди рухатись далі?

Ось декілька напрямків для подальшого вивчення:
1.  **Бази даних:** Для зберігання постійних даних користувачів та їхнього стану використовуйте SQLite (для простих проектів) або PostgreSQL/MySQL (для складних).
2.  **Асинхронне програмування:** Коли ви вивчите `async/await`, ви зможете використовувати такі бібліотеки, як `aiogram` або `python-telegram-bot` (в асинхронному режимі), що є більш продуктивним для великих та складних ботів.
3.  **Вебхуки:** Якщо ваш бот стане дуже популярним, перехід на webhooks дозволить йому реагувати миттєво та обробляти більше запитів.
4.  **Складніші FSM (Finite State Machine):** Для керування станом користувача є готові бібліотеки, які спрощують написання покрокової логіки.
5.  **Тестування:** Навчіться писати тести для свого бота, щоб переконатися, що він працює коректно.
6.  **Деплоймент:** Освойте Docker для контейнеризації бота та сервіси хмарних провайдерів для його розгортання.

Бажаю успіхів у створенні ваших власних Telegram-ботів!
