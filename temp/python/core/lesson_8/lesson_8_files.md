# 📁 Повний посібник з роботи з файлами у Python

## Зміст

### Основи роботи з файлами

1. [Вступ до роботи з файлами](#вступ-до-роботи-з-файлами)
2. [Навіщо потрібна робота з файлами?](#навіщо-потрібна-робота-з-файлами)
3. [Що таке файл?](#що-таке-файл)
4. [Типи файлів](#типи-файлів)
5. [Шляхи до файлів](#шляхи-до-файлів)

### Відкриття та закриття файлів

6. [Функція open()](#функція-open)
7. [Режими відкриття файлів](#режими-відкриття-файлів)
8. [Закриття файлів: close()](#закриття-файлів-close)
9. [Context manager: with](#context-manager-with)
10. [Кодування файлів](#кодування-файлів)

### Читання файлів

11. [Метод read()](#метод-read)
12. [Метод readline()](#метод-readline)
13. [Метод readlines()](#метод-readlines)
14. [Читання файлу в циклі](#читання-файлу-в-циклі)
15. [Читання великих файлів](#читання-великих-файлів)

### Запис у файли

16. [Метод write()](#метод-write)
17. [Метод writelines()](#метод-writelines)
18. [Дозапис у файл](#дозапис-у-файл)
19. [Створення нового файлу](#створення-нового-файлу)
20. [Перезапис файлу](#перезапис-файлу)

### Навігація по файлу

21. [Метод seek()](#метод-seek)
22. [Метод tell()](#метод-tell)
23. [Переміщення по файлу](#переміщення-по-файлу)

### Робота зі шляхами

24. [Модуль os.path](#модуль-ospath)
25. [Модуль pathlib](#модуль-pathlib)
26. [Абсолютні та відносні шляхи](#абсолютні-та-відносні-шляхи)
27. [Об'єднання шляхів](#обєднання-шляхів)
28. [Розбір шляхів](#розбір-шляхів)

### Операції з файлами

29. [Перевірка існування](#перевірка-існування)
30. [Створення директорій](#створення-директорій)
31. [Видалення файлів](#видалення-файлів)
32. [Видалення директорій](#видалення-директорій)
33. [Копіювання файлів](#копіювання-файлів)
34. [Переміщення файлів](#переміщення-файлів)
35. [Перейменування файлів](#перейменування-файлів)

### Інформація про файли

36. [Розмір файлу](#розмір-файлу)
37. [Дата створення та модифікації](#дата-створення-та-модифікації)
38. [Атрибути файлів](#атрибути-файлів)
39. [Перебір файлів у директорії](#перебір-файлів-у-директорії)
40. [Рекурсивний перебір](#рекурсивний-перебір)

### Робота з різними форматами

41. [Текстові файли (.txt)](#текстові-файли-txt)
42. [CSV файли](#csv-файли)
43. [JSON файли](#json-файли)
44. [Бінарні файли](#бінарні-файли)
45. [Тимчасові файли](#тимчасові-файли)

### Обробка помилок

46. [Файлові винятки](#файлові-винятки)
47. [FileNotFoundError](#filenotfounderror)
48. [PermissionError](#permissionerror)
49. [IsADirectoryError](#isadirectoryerror)
50. [Безпечна робота з файлами](#безпечна-робота-з-файлами)

### Практика

51. [Практичні приклади](#практичні-приклади)
52. [Поширені помилки](#поширені-помилки)
53. [Найкращі практики](#найкращі-практики)
54. [Оптимізація роботи з файлами](#оптимізація-роботи-з-файлами)

---

## Вступ до роботи з файлами

### Що таке файл?

**Файл** — це іменована область на диску, де зберігаються дані.

**Простими словами:** Файл — це як записник на вашому комп'ютері, де ви можете зберігати інформацію, яка залишається навіть після закриття програми.

### Навіщо працювати з файлами?

1. **Збереження даних між запусками** — дані не зникають після закриття програми
2. **Обмін даними** — файли можна передавати між програмами
3. **Великі об'єми даних** — не все можна тримати в пам'яті
4. **Конфігурація** — налаштування програми
5. **Логування** — запис історії роботи

### Аналогія:

**Без файлів (тільки змінні):**

```python
name = "Іван"
# Закрили програму → дані втрачено 😢
```

**З файлами:**

```python
# Зберігаємо
with open("name.txt", "w") as file:
    file.write("Іван")

# Закрили програму, відкрили знову
# Читаємо
with open("name.txt", "r") as file:
    name = file.read()  # "Іван" ✅ Дані збережено!
```

---

## Навіщо потрібна робота з файлами?

### 1. Постійне зберігання даних

```python
# Збереження налаштувань гри
settings = {
    "volume": 80,
    "difficulty": "hard",
    "player_name": "Іван"
}

import json
with open("settings.json", "w") as file:
    json.dump(settings, file)

# Наступного разу налаштування завантажаться
```

### 2. Обробка великих даних

```python
# Не можемо завантажити 1 ГБ файл у пам'ять
# Читаємо по частинах
with open("huge_log.txt", "r") as file:
    for line in file:  # Читає по одному рядку
        process(line)
```

### 3. Логування

```python
# Запис історії роботи програми
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info("Програма запущена")
logging.error("Виникла помилка")
```

### 4. Імпорт/Експорт даних

```python
# Експорт даних у CSV для Excel
import csv

users = [
    ["Іван", 25, "Київ"],
    ["Марія", 30, "Львів"]
]

with open("users.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Ім'я", "Вік", "Місто"])
    writer.writerows(users)
```

### 5. Конфігурація

```python
# config.ini
# [DATABASE]
# host = localhost
# port = 5432

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

host = config["DATABASE"]["host"]
```

---

## Що таке файл?

### Структура файлу:

```
📁 Файл = Ім'я + Розширення + Вміст
```

**Приклад:**

```
document.txt
├── Ім'я: document
├── Розширення: .txt
└── Вміст: "Привіт, світ!"
```

### Компоненти:

1. **Ім'я файлу** — `document`
2. **Розширення** — `.txt` (тип файлу)
3. **Шлях** — де знаходиться файл
4. **Вміст** — дані всередині

### Повний шлях:

```
C:\Users\Ivan\Documents\document.txt
│    │      │      │         │      └─ розширення
│    │      │      │         └──────── ім'я
│    │      │      └────────────────── директорія
│    │      └───────────────────────── батьківська директорія
│    └──────────────────────────────── батьківська директорія
└───────────────────────────────────── диск (Windows)

/home/ivan/documents/document.txt
│   │    │     │         │      └─ розширення
│   │    │     │         └──────── ім'я
│   │    │     └────────────────── директорія
│   │    └──────────────────────── домашня директорія
│   └───────────────────────────── користувач
└───────────────────────────────── корінь (Linux/Mac)
```

---

## Типи файлів

### Текстові файли

**Файли, які можна прочитати як текст.**

```python
# .txt - простий текст
# .py - код Python
# .html - веб-сторінка
# .csv - дані у таблиці
# .json - структуровані дані
# .xml - структуровані дані
# .md - Markdown документ
```

**Особливості:**

- ✅ Можна відкрити в блокноті
- ✅ Кожен символ = 1-4 байти
- ✅ Є поняття "рядок"

### Бінарні файли

**Файли, які містять байти (не текст).**

```python
# .jpg, .png - зображення
# .mp3, .wav - аудіо
# .mp4, .avi - відео
# .exe - програми (Windows)
# .pdf - документи
# .zip - архіви
```

**Особливості:**

- ❌ Не можна прочитати як текст
- ✅ Зберігають будь-які дані
- ✅ Компактніші

### Порівняння:

```python
# Текстовий файл
"Hello" → H e l l o (5 символів)

# Бінарний файл
"Hello" → 48 65 6C 6C 6F (5 байтів у hex)
```

---

## Шляхи до файлів

### Абсолютний шлях

**Повний шлях від кореня диску.**

**Windows:**

```python
"C:\\Users\\Ivan\\Documents\\file.txt"
"C:/Users/Ivan/Documents/file.txt"  # Теж працює
```

**Linux/Mac:**

```python
"/home/ivan/documents/file.txt"
```

### Відносний шлях

**Шлях відносно поточної директорії.**

```python
"file.txt"              # Файл у поточній директорії
"data/file.txt"         # Файл у піддиректорії data
"../file.txt"           # Файл у батьківській директорії
"../../file.txt"        # На два рівні вгору
```

### Поточна директорія:

```python
import os

# Отримати поточну директорію
current = os.getcwd()
print(current)  # C:\Users\Ivan\Projects\MyApp

# Змінити поточну директорію
os.chdir("C:\\Users\\Ivan\\Documents")
```

### Спеціальні символи:

```python
.   # Поточна директорія
..  # Батьківська директорія
~   # Домашня директорія користувача (Linux/Mac)
/   # Корінь диску (Linux/Mac)
\   # Розділювач директорій (Windows)
/   # Розділювач директорій (універсальний)
```

---

## Функція open()

### Синтаксис:

```python
file = open(filename, mode='r', encoding=None)
```

### Параметри:

1. **`filename`** — ім'я або шлях до файлу
2. **`mode`** — режим відкриття (за замовчуванням `'r'`)
3. **`encoding`** — кодування (для текстових файлів)

### Простий приклад:

```python
# Відкрити файл для читання
file = open("example.txt", "r")

# Прочитати вміст
content = file.read()
print(content)

# Закрити файл
file.close()
```

### Що повертає open()?

**File object** — об'єкт, через який ми працюємо з файлом.

```python
file = open("example.txt", "r")
print(type(file))  # <class '_io.TextIOWrapper'>
```

### Методи file object:

```python
file.read()       # Прочитати весь файл
file.readline()   # Прочитати один рядок
file.readlines()  # Прочитати всі рядки у список
file.write()      # Записати текст
file.close()      # Закрити файл
file.seek()       # Переміститись у файлі
file.tell()       # Поточна позиція
```

---

## Режими відкриття файлів

### Основні режими:

| Режим  | Опис                            | Створює? | Очищає? | Читання | Запис |
| ------ | ------------------------------- | -------- | ------- | ------- | ----- |
| `'r'`  | Читання (read)                  | ❌       | ❌      | ✅      | ❌    |
| `'w'`  | Запис (write)                   | ✅       | ✅      | ❌      | ✅    |
| `'a'`  | Дозапис (append)                | ✅       | ❌      | ❌      | ✅    |
| `'x'`  | Створення (exclusive creation)  | ✅       | ❌      | ❌      | ✅    |
| `'r+'` | Читання та запис                | ❌       | ❌      | ✅      | ✅    |
| `'w+'` | Запис та читання (очищає файл!) | ✅       | ✅      | ✅      | ✅    |
| `'a+'` | Дозапис та читання              | ✅       | ❌      | ✅      | ✅    |

### Додаткові прапорці:

| Прапорець | Опис                               |
| --------- | ---------------------------------- |
| `'b'`     | Бінарний режим                     |
| `'t'`     | Текстовий режим (за замовчуванням) |

### Детальний опис режимів:

#### Режим 'r' (read):

```python
# Читання існуючого файлу
file = open("example.txt", "r")
content = file.read()
file.close()

# Якщо файл не існує → FileNotFoundError
```

**Коли використовувати:**

- Файл вже існує
- Потрібно тільки читати

#### Режим 'w' (write):

```python
# Створює новий файл або ОЧИЩАЄ існуючий!
file = open("example.txt", "w")
file.write("Новий вміст")
file.close()

# ⚠️ УВАГА: Старий вміст видалено!
```

**Коли використовувати:**

- Створити новий файл
- Перезаписати файл

#### Режим 'a' (append):

```python
# Додає в кінець файлу
file = open("log.txt", "a")
file.write("Новий рядок\n")
file.close()

# ✅ Старий вміст збережено
```

**Коли використовувати:**

- Логування
- Додавання записів

#### Режим 'x' (exclusive):

```python
# Створює файл, але помилка якщо вже існує
try:
    file = open("new_file.txt", "x")
    file.write("Вміст")
    file.close()
except FileExistsError:
    print("Файл вже існує!")
```

**Коли використовувати:**

- Гарантовано новий файл
- Не хочемо перезаписати існуючий

#### Режим 'r+' (read and write):

```python
# Читання та запис (не очищає файл)
file = open("example.txt", "r+")
content = file.read()
file.write("\nДодатковий текст")
file.close()
```

#### Режим 'w+' (write and read):

```python
# Очищає файл, дозволяє читати та писати
file = open("example.txt", "w+")
file.write("Новий вміст")
file.seek(0)  # Повернутись на початок
content = file.read()
file.close()
```

### Бінарні режими:

```python
# Читання бінарного файлу
file = open("image.png", "rb")
data = file.read()
file.close()

# Запис бінарного файлу
file = open("image.png", "wb")
file.write(binary_data)
file.close()
```

### Таблиця: Що відбувається з файлом?

| Режим | Файл не існує | Файл існує   | Вміст         |
| ----- | ------------- | ------------ | ------------- |
| `'r'` | ❌ Помилка    | ✅ Відкриває | Зберігається  |
| `'w'` | ✅ Створює    | ✅ Відкриває | ❌ Очищається |
| `'a'` | ✅ Створює    | ✅ Відкриває | Зберігається  |
| `'x'` | ✅ Створює    | ❌ Помилка   | —             |

---

## Закриття файлів: close()

### Навіщо закривати файли?

1. **Звільнення ресурсів** — файл займає ресурси ОС
2. **Збереження даних** — дані можуть не записатись без close()
3. **Дозвіл іншим програмам** — інші програми не зможуть відкрити файл

### Базовий приклад:

```python
file = open("example.txt", "r")
content = file.read()
file.close()  # ✅ Обов'язково закрити!
```

### Проблема: забули закрити

```python
# ❌ Погано
file = open("example.txt", "r")
content = file.read()
# Забули file.close()

# Файл залишається відкритим → витік ресурсів
```

### Проблема: виняток до close()

```python
# ❌ Погано
file = open("example.txt", "r")
content = file.read()
result = int(content)  # Може виникнути ValueError!
file.close()  # Не виконається при винятку!
```

### Рішення 1: try-finally

```python
# ✅ Краще
file = open("example.txt", "r")
try:
    content = file.read()
    result = int(content)
finally:
    file.close()  # Виконається завжди
```

### Рішення 2: with statement (НАЙКРАЩЕ!)

```python
# ✅ Найкраще
with open("example.txt", "r") as file:
    content = file.read()
    result = int(content)
# Файл автоматично закритий
```

---

## Context manager: with

### Що таке with?

**`with`** — конструкція, яка **автоматично закриває файл** після використання.

### Синтаксис:

```python
with open(filename, mode) as file:
    # Робота з файлом
# Файл автоматично закрито
```

### Переваги:

1. ✅ Автоматичне закриття
2. ✅ Працює навіть при винятках
3. ✅ Чистіший код
4. ✅ Рекомендований спосіб

### Порівняння:

**Без with:**

```python
file = open("example.txt", "r")
try:
    content = file.read()
    print(content)
finally:
    file.close()
```

**З with:**

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

### Множинні файли:

```python
# Відкрити кілька файлів одночасно
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    content = infile.read()
    outfile.write(content.upper())
```

### Приклад з винятком:

```python
try:
    with open("example.txt", "r") as file:
        content = file.read()
        result = int(content)  # Може бути ValueError
except ValueError:
    print("Невірний формат")
except FileNotFoundError:
    print("Файл не знайдено")
# Файл закритий, навіть якщо був виняток!
```

### Перевірка, чи закритий файл:

```python
with open("example.txt", "r") as file:
    print(file.closed)  # False (файл відкритий)
    content = file.read()

print(file.closed)  # True (файл закритий)
```

---

## Кодування файлів

### Що таке кодування?

**Кодування** — спосіб перетворення символів у байти.

### Приклад:

```
Символ "А" → UTF-8 → D0 90 (2 байти)
Символ "A" → UTF-8 → 41 (1 байт)
```

### Популярні кодування:

| Кодування | Опис                             | Коли використовувати |
| --------- | -------------------------------- | -------------------- |
| `utf-8`   | Універсальне, підтримує всі мови | ✅ За замовчуванням  |
| `cp1251`  | Кирилиця (Windows)               | Старі Windows файли  |
| `ascii`   | Тільки англійські символи        | Старі файли          |
| `latin-1` | Західноєвропейські мови          | Рідко                |

### Вказати кодування:

```python
# UTF-8 (рекомендовано)
with open("file.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Windows-1251 (кирилиця, старі файли)
with open("file.txt", "r", encoding="cp1251") as file:
    content = file.read()
```

### Проблема: неправильне кодування

```python
# Файл збережений у cp1251, відкриваємо як utf-8
with open("file.txt", "r", encoding="utf-8") as file:
    content = file.read()  # ❌ Кракозябри!
    print(content)  # Ð¿Ñ€Ð¸Ð²Ñ–Ñ‚
```

### Рішення:

```python
# Вказати правильне кодування
with open("file.txt", "r", encoding="cp1251") as file:
    content = file.read()  # ✅ Привіт
```

### Автовизначення кодування:

```python
import chardet

# Прочитати байти
with open("file.txt", "rb") as file:
    raw_data = file.read()

# Визначити кодування
result = chardet.detect(raw_data)
encoding = result['encoding']

print(f"Кодування: {encoding}")

# Прочитати з правильним кодуванням
with open("file.txt", "r", encoding=encoding) as file:
    content = file.read()
```

### За замовчуванням:

```python
import locale

# Отримати кодування за замовчуванням
default_encoding = locale.getpreferredencoding()
print(default_encoding)  # Windows: cp1251, Linux/Mac: utf-8
```

**Рекомендація:** Завжди явно вказуйте `encoding="utf-8"`!

---

## Метод read()

### Що робить read()?

**Читає весь файл або вказану кількість символів.**

### Синтаксис:

```python
file.read(size=-1)  # size = кількість символів (-1 = весь файл)
```

### Прочитати весь файл:

```python
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()  # Весь файл як рядок
    print(content)
```

**Якщо файл:**

```
Привіт
Світ
Python
```

**Результат:**

```python
content = "Привіт\nСвіт\nPython\n"
```

### Прочитати N символів:

```python
with open("example.txt", "r", encoding="utf-8") as file:
    first_10 = file.read(10)  # Перші 10 символів
    next_5 = file.read(5)     # Наступні 5 символів
    rest = file.read()        # Решта файлу
```

### Повторне читання:

```python
with open("example.txt", "r") as file:
    content1 = file.read()  # Весь файл
    content2 = file.read()  # Порожній рядок (курсор в кінці)

print(len(content2))  # 0
```

### Повернутись на початок:

```python
with open("example.txt", "r") as file:
    content1 = file.read()

    file.seek(0)  # Повернутись на початок

    content2 = file.read()  # Знову весь файл
```

### Обробка великих файлів:

```python
# ❌ Погано для великих файлів (читає все в пам'ять)
with open("huge_file.txt", "r") as file:
    content = file.read()  # Може бути кілька ГБ!

# ✅ Краще читати по частинах
with open("huge_file.txt", "r") as file:
    while True:
        chunk = file.read(1024)  # Читати по 1 КБ
        if not chunk:
            break
        process(chunk)
```

---

## Метод readline()

### Що робить readline()?

**Читає ОДИН рядок з файлу.**

### Синтаксис:

```python
file.readline(size=-1)
```

### Базовий приклад:

**Файл example.txt:**

```
Перший рядок
Другий рядок
Третій рядок
```

**Код:**

```python
with open("example.txt", "r", encoding="utf-8") as file:
    line1 = file.readline()  # "Перший рядок\n"
    line2 = file.readline()  # "Другий рядок\n"
    line3 = file.readline()  # "Третій рядок\n"
    line4 = file.readline()  # "" (файл закінчився)
```

### Читання всіх рядків у циклі:

```python
with open("example.txt", "r", encoding="utf-8") as file:
    while True:
        line = file.readline()
        if not line:  # Порожній рядок = кінець файлу
            break
        print(line.strip())  # strip() видаляє \n
```

### Обмеження розміру:

```python
with open("example.txt", "r") as file:
    line = file.readline(10)  # Максимум 10 символів
```

### readline() зберігає \n:

```python
with open("example.txt", "r") as file:
    line = file.readline()
    print(repr(line))  # "Перший рядок\n"

    # Видалити \n
    line = line.strip()
    print(repr(line))  # "Перший рядок"
```

---

## Метод readlines()

### Що робить readlines()?

**Читає ВСІ рядки файлу у список.**

### Синтаксис:

```python
file.readlines()
```

### Базовий приклад:

**Файл example.txt:**

```
Перший рядок
Другий рядок
Третій рядок
```

**Код:**

```python
with open("example.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

print(lines)
# ['Перший рядок\n', 'Другий рядок\n', 'Третій рядок\n']
```

### Обробка списку рядків:

```python
with open("example.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    print(line.strip())  # Видалити \n
```

### Видалити \n одразу:

```python
with open("example.txt", "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file.readlines()]

print(lines)
# ['Перший рядок', 'Другий рядок', 'Третій рядок']
```

### Порівняння методів:

| Метод         | Повертає          | Коли використовувати |
| ------------- | ----------------- | -------------------- |
| `read()`      | Рядок (весь файл) | Маленькі файли       |
| `readline()`  | Рядок (один)      | Послідовне читання   |
| `readlines()` | Список рядків     | Всі рядки в пам'яті  |

### Проблема з великими файлами:

```python
# ❌ Погано (завантажує весь файл у пам'ять)
with open("huge_file.txt", "r") as file:
    lines = file.readlines()  # Кілька ГБ!

# ✅ Краще (читає по одному рядку)
with open("huge_file.txt", "r") as file:
    for line in file:
        process(line)
```

---

## Читання файлу в циклі

### Найкращий спосіб: ітерація по файлу

```python
with open("example.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

**Переваги:**

1. ✅ Пам'ять ефективно (читає по одному рядку)
2. ✅ Простий синтаксис
3. ✅ Працює з великими файлами

### Порівняння методів:

#### Спосіб 1: Ітерація (КРАЩЕ!)

```python
with open("file.txt", "r") as file:
    for line in file:
        print(line.strip())
```

#### Спосіб 2: readlines()

```python
with open("file.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())
```

#### Спосіб 3: readline() в циклі

```python
with open("file.txt", "r") as file:
    while True:
        line = file.readline()
        if not line:
            break
        print(line.strip())
```

#### Спосіб 4: read().split()

```python
with open("file.txt", "r") as file:
    content = file.read()
    lines = content.split('\n')
    for line in lines:
        print(line)
```

### З нумерацією рядків:

```python
with open("file.txt", "r", encoding="utf-8") as file:
    for line_num, line in enumerate(file, start=1):
        print(f"{line_num}: {line.strip()}")
```

**Виведення:**

```
1: Перший рядок
2: Другий рядок
3: Третій рядок
```

### Фільтрація рядків:

```python
# Читати тільки непорожні рядки
with open("file.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:  # Якщо не порожній
            print(line)
```

```python
# Читати тільки рядки, що починаються з "#"
with open("config.txt", "r") as file:
    for line in file:
        if line.startswith("#"):
            print(line.strip())
```

---

## Читання великих файлів

### Проблема:

```python
# ❌ Файл 10 ГБ → read() завантажить 10 ГБ у пам'ять!
with open("huge.txt", "r") as file:
    content = file.read()  # Може не вистачити RAM
```

### Рішення 1: Читання по рядках

```python
# ✅ Читає по одному рядку (пам'ять ефективно)
with open("huge.txt", "r", encoding="utf-8") as file:
    for line in file:
        process_line(line)
```

### Рішення 2: Читання блоками (chunks)

```python
# ✅ Читає по 1 МБ
chunk_size = 1024 * 1024  # 1 МБ

with open("huge.txt", "r", encoding="utf-8") as file:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        process_chunk(chunk)
```

### Рішення 3: Бінарні файли

```python
# Читання великого бінарного файлу
chunk_size = 8192  # 8 КБ

with open("large_file.bin", "rb") as file:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        process_binary_chunk(chunk)
```

### Практичний приклад: підрахунок рядків

```python
def count_lines(filename):
    """Підрахунок рядків у файлі (пам'ять ефективно)"""
    count = 0
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            count += 1
    return count

# Працює навіть з файлами по кілька ГБ
lines = count_lines("huge.txt")
print(f"Рядків: {lines}")
```

### Практичний приклад: пошук у файлі

```python
def find_in_file(filename, search_text):
    """Знайти текст у великому файлі"""
    with open(filename, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            if search_text in line:
                print(f"Рядок {line_num}: {line.strip()}")

find_in_file("huge_log.txt", "ERROR")
```

---

## Метод write()

### Що робить write()?

**Записує рядок у файл.**

### Синтаксис:

```python
file.write(string)
```

### Базовий приклад:

```python
# Створити та записати файл
with open("example.txt", "w", encoding="utf-8") as file:
    file.write("Привіт, світ!")
    file.write("\n")
    file.write("Це другий рядок")
```

**Результат у файлі:**

```
Привіт, світ!
Це другий рядок
```

### write() НЕ додає \n автоматично:

```python
with open("example.txt", "w") as file:
    file.write("Перший рядок")
    file.write("Другий рядок")
```

**Результат:**

```
Перший рядокДругий рядок
```

**Правильно:**

```python
with open("example.txt", "w") as file:
    file.write("Перший рядок\n")
    file.write("Другий рядок\n")
```

**Результат:**

```
Перший рядок
Другий рядок
```

### Запис змінних:

```python
name = "Іван"
age = 25

with open("user.txt", "w", encoding="utf-8") as file:
    file.write(f"Ім'я: {name}\n")
    file.write(f"Вік: {age}\n")
```

### Запис у циклі:

```python
numbers = [1, 2, 3, 4, 5]

with open("numbers.txt", "w") as file:
    for num in numbers:
        file.write(f"{num}\n")
```

### Повернене значення:

```python
with open("example.txt", "w") as file:
    bytes_written = file.write("Привіт!")
    print(bytes_written)  # Кількість записаних символів
```

---

## Метод writelines()

### Що робить writelines()?

**Записує список рядків у файл.**

### Синтаксис:

```python
file.writelines(list_of_strings)
```

### Базовий приклад:

```python
lines = ["Перший рядок\n", "Другий рядок\n", "Третій рядок\n"]

with open("example.txt", "w", encoding="utf-8") as file:
    file.writelines(lines)
```

**Результат:**

```
Перший рядок
Другий рядок
Третій рядок
```

### writelines() НЕ додає \n:

```python
# ❌ Без \n
lines = ["Перший", "Другий", "Третій"]

with open("example.txt", "w") as file:
    file.writelines(lines)
```

**Результат:**

```
ПершийДругийТретій
```

**✅ З \n:**

```python
lines = ["Перший\n", "Другий\n", "Третій\n"]

with open("example.txt", "w") as file:
    file.writelines(lines)
```

### Додати \n автоматично:

```python
lines = ["Перший", "Другий", "Третій"]

with open("example.txt", "w", encoding="utf-8") as file:
    file.writelines(line + "\n" for line in lines)
```

**Або:**

```python
lines = ["Перший", "Другий", "Третій"]

with open("example.txt", "w", encoding="utf-8") as file:
    for line in lines:
        file.write(line + "\n")
```

### Порівняння write() та writelines():

```python
# Варіант 1: write() в циклі
with open("file.txt", "w") as file:
    for line in lines:
        file.write(line + "\n")

# Варіант 2: writelines() з генератором
with open("file.txt", "w") as file:
    file.writelines(line + "\n" for line in lines)

# Обидва дають однаковий результат
```

---

## Дозапис у файл

### Режим 'a' (append):

```python
# Додати текст у кінець файлу
with open("log.txt", "a", encoding="utf-8") as file:
    file.write("Новий запис\n")
```

### Приклад: логування

```python
import datetime

def log(message):
    """Додати запис у лог"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("app.log", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")

# Використання
log("Програма запущена")
log("Користувач увійшов")
log("Помилка з'єднання")
```

**Файл app.log:**

```
[2025-11-07 21:49:00] Програма запущена
[2025-11-07 21:49:05] Користувач увійшов
[2025-11-07 21:49:10] Помилка з'єднання
```

### Приклад: збереження історії

```python
def save_history(action):
    """Зберегти дію в історію"""
    with open("history.txt", "a", encoding="utf-8") as file:
        file.write(f"{action}\n")

save_history("Відкрив файл: document.txt")
save_history("Відредагував рядок 10")
save_history("Зберіг файл")
```

### Створення файлу при дозапису:

```python
# Якщо файл не існує - створить
# Якщо існує - додасть у кінець
with open("new_or_existing.txt", "a") as file:
    file.write("Текст\n")
```

---

## Створення нового файлу

### Режим 'x' (exclusive creation):

```python
try:
    with open("new_file.txt", "x", encoding="utf-8") as file:
        file.write("Вміст нового файлу")
    print("✅ Файл створено")
except FileExistsError:
    print("❌ Файл вже існує")
```

### Переваги режиму 'x':

1. ✅ Безпека — не перезапише існуючий файл
2. ✅ Явність — зрозуміло, що створюємо новий

### Порівняння з 'w':

```python
# Режим 'w' - перезапише існуючий файл!
with open("file.txt", "w") as file:
    file.write("Новий вміст")
# ⚠️ Старий вміст втрачено

# Режим 'x' - помилка якщо існує
try:
    with open("file.txt", "x") as file:
        file.write("Вміст")
except FileExistsError:
    print("Файл вже існує, не перезаписуємо")
```

### Створення з перевіркою:

```python
import os

def safe_create_file(filename, content):
    """Створити файл тільки якщо не існує"""
    if os.path.exists(filename):
        print(f"❌ Файл {filename} вже існує")
        return False

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"✅ Файл {filename} створено")
    return True

safe_create_file("report.txt", "Звіт за 2025 рік")
```

---

## Перезапис файлу

### Режим 'w' (write):

```python
# Очистити файл та записати новий вміст
with open("data.txt", "w", encoding="utf-8") as file:
    file.write("Новий вміст\n")
    file.write("Старий вміст видалено\n")
```

**⚠️ УВАГА:** Режим 'w' **видаляє** старий вміст!

### Безпечний перезапис:

```python
import os
import shutil

def safe_overwrite(filename, new_content):
    """Безпечний перезапис з резервною копією"""
    backup_name = filename + ".backup"

    # Створити резервну копію
    if os.path.exists(filename):
        shutil.copy2(filename, backup_name)
        print(f"📦 Створено копію: {backup_name}")

    try:
        # Записати новий вміст
        with open(filename, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"✅ Файл {filename} оновлено")

        # Видалити backup якщо все OK
        if os.path.exists(backup_name):
            os.remove(backup_name)

    except Exception as e:
        # Відновити з backup при помилці
        if os.path.exists(backup_name):
            shutil.copy2(backup_name, filename)
            print(f"❌ Помилка, файл відновлено з backup")
        raise

safe_overwrite("important.txt", "Новий вміст")
```

---

## Метод seek()

### Що робить seek()?

**Переміщує курсор у файлі.**

### Синтаксис:

```python
file.seek(offset, whence=0)
```

**Параметри:**

- `offset` — кількість байтів для переміщення
- `whence` — точка відліку:
    - `0` — від початку файлу (за замовчуванням)
    - `1` — від поточної позиції
    - `2` — від кінця файлу

### Приклади:

```python
with open("example.txt", "r") as file:
    # Прочитати все
    content = file.read()

    # Повернутись на початок
    file.seek(0)

    # Прочитати знову
    content2 = file.read()
```

### Переміщення до конкретної позиції:

```python
with open("example.txt", "r") as file:
    # Перейти до 10-го байту
    file.seek(10)

    # Прочитати з 10-го байту
    content = file.read()
```

### Переміщення від кінця:

```python
with open("example.txt", "r") as file:
    # Перейти на 10 байтів від кінця
    file.seek(-10, 2)

    # Прочитати останні 10 байтів
    last_bytes = file.read()
```

### Переміщення від поточної позиції:

```python
with open("example.txt", "r") as file:
    file.read(5)  # Прочитати 5 байтів

    # Перемістись на 3 байти вперед від поточної позиції
    file.seek(3, 1)

    rest = file.read()
```

---

## Метод tell()

### Що робить tell()?

**Повертає поточну позицію курсору у файлі.**

### Синтаксис:

```python
position = file.tell()
```

### Приклад:

```python
with open("example.txt", "r") as file:
    print(f"Початок: {file.tell()}")  # 0

    file.read(10)  # Прочитати 10 байтів
    print(f"Після read(10): {file.tell()}")  # 10

    file.read(5)  # Прочитати ще 5
    print(f"Після read(5): {file.tell()}")  # 15
```

### Комбінація seek() та tell():

```python
with open("example.txt", "r") as file:
    # Запам'ятати позицію
    start_pos = file.tell()

    # Прочитати частину
    data = file.read(100)

    # Повернутись на збережену позицію
    file.seek(start_pos)

    # Прочитати знову
    data2 = file.read(100)
```

### Практичний приклад: читання блоків

```python
def read_blocks(filename, block_size=1024):
    """Читати файл блоками та показувати прогрес"""
    with open(filename, "rb") as file:
        # Отримати розмір файлу
        file.seek(0, 2)  # Перейти в кінець
        file_size = file.tell()
        file.seek(0)  # Повернутись на початок

        blocks_read = 0
        while True:
            block = file.read(block_size)
            if not block:
                break

            blocks_read += 1
            position = file.tell()
            progress = (position / file_size) * 100

            print(f"Блок {blocks_read}: {progress:.1f}% ({position}/{file_size} байт)")

read_blocks("large_file.bin")
```

---

## Переміщення по файлу

### Читання файлу з різних позицій:

```python
with open("data.txt", "r") as file:
    # Прочитати початок
    file.seek(0)
    header = file.read(100)

    # Прочитати кінець
    file.seek(-100, 2)  # 100 байтів від кінця
    footer = file.read()

    # Прочитати середину
    file.seek(500)
    middle = file.read(100)
```

### Пропуск заголовку:

```python
# CSV файл з заголовком
with open("data.csv", "r", encoding="utf-8") as file:
    header = file.readline()  # Пропустити заголовок

    for line in file:
        # Обробка даних
        process_line(line)
```

### Читання з кінця:

```python
def read_last_lines(filename, n=10):
    """Прочитати останні N рядків файлу"""
    with open(filename, "rb") as file:
        file.seek(0, 2)  # Кінець файлу
        file_size = file.tell()

        # Оцінка: ~80 байтів на рядок
        estimated_pos = max(0, file_size - (n * 80))
        file.seek(estimated_pos)

        lines = file.readlines()

        # Повернути останні N рядків
        return [line.decode('utf-8') for line in lines[-n:]]

last_10 = read_last_lines("log.txt", 10)
for line in last_10:
    print(line.strip())
```

---

## Модуль os.path

### Що таке os.path?

**Модуль для роботи зі шляхами до файлів.**

### Імпорт:

```python
import os.path
# Або
from os.path import exists, join, split
```

### Основні функції:

#### exists() - перевірка існування:

```python
import os.path

if os.path.exists("file.txt"):
    print("✅ Файл існує")
else:
    print("❌ Файл не існує")
```

#### isfile() - це файл?:

```python
if os.path.isfile("data.txt"):
    print("✅ Це файл")
```

#### isdir() - це директорія?:

```python
if os.path.isdir("my_folder"):
    print("✅ Це директорія")
```

#### join() - об'єднання шляхів:

```python
# Універсальне об'єднання (працює на Windows/Linux/Mac)
path = os.path.join("folder", "subfolder", "file.txt")
print(path)
# Windows: folder\subfolder\file.txt
# Linux: folder/subfolder/file.txt
```

#### split() - розділення шляху:

```python
path = "/home/user/documents/file.txt"

directory, filename = os.path.split(path)
print(directory)  # /home/user/documents
print(filename)   # file.txt
```

#### basename() - тільки ім'я файлу:

```python
path = "/home/user/documents/file.txt"
name = os.path.basename(path)
print(name)  # file.txt
```

#### dirname() - тільки директорія:

```python
path = "/home/user/documents/file.txt"
directory = os.path.dirname(path)
print(directory)  # /home/user/documents
```

#### splitext() - відокремити розширення:

```python
path = "document.txt"
name, ext = os.path.splitext(path)
print(name)  # document
print(ext)   # .txt
```

#### abspath() - абсолютний шлях:

```python
# Поточна директорія: /home/user/project

relative = "file.txt"
absolute = os.path.abspath(relative)
print(absolute)  # /home/user/project/file.txt
```

#### getsize() - розмір файлу:

```python
size = os.path.getsize("file.txt")
print(f"Розмір: {size} байт")
```

### Практичний приклад:

```python
import os.path

def analyze_file(filepath):
    """Аналіз файлу"""
    if not os.path.exists(filepath):
        print(f"❌ Файл {filepath} не існує")
        return

    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        directory, filename = os.path.split(filepath)
        name, ext = os.path.splitext(filename)

        print(f"📁 Файл: {filename}")
        print(f"📂 Директорія: {directory}")
        print(f"📝 Ім'я: {name}")
        print(f"🔖 Розширення: {ext}")
        print(f"📏 Розмір: {size} байт")
    else:
        print(f"❌ {filepath} - це не файл")

analyze_file("document.txt")
```

---

## Модуль pathlib

### Що таке pathlib?

**Сучасний модуль для роботи зі шляхами** (рекомендовано з Python 3.4+).

### Переваги над os.path:

1. ✅ Об'єктно-орієнтований підхід
2. ✅ Зручніший синтаксис
3. ✅ Підтримка операторів `/`
4. ✅ Більше методів

### Імпорт:

```python
from pathlib import Path
```

### Створення Path:

```python
# Шлях до файлу
path = Path("folder/file.txt")

# Поточна директорія
current = Path.cwd()

# Домашня директорія
home = Path.home()
```

### Об'єднання шляхів з /:

```python
# Елегантний синтаксис!
path = Path("folder") / "subfolder" / "file.txt"
print(path)  # folder/subfolder/file.txt
```

### Перевірка існування:

```python
path = Path("file.txt")

if path.exists():
    print("✅ Існує")

if path.is_file():
    print("✅ Це файл")

if path.is_dir():
    print("✅ Це директорія")
```

### Читання та запис:

```python
path = Path("example.txt")

# Прочитати весь файл
content = path.read_text(encoding="utf-8")

# Записати файл
path.write_text("Новий вміст", encoding="utf-8")

# Бінарні дані
binary_data = path.read_bytes()
path.write_bytes(binary_data)
```

### Атрибути шляху:

```python
path = Path("/home/user/documents/report.txt")

print(path.name)        # report.txt
print(path.stem)        # report
print(path.suffix)      # .txt
print(path.parent)      # /home/user/documents
print(path.parts)       # ('/', 'home', 'user', 'documents', 'report.txt')
```

### Змінити компоненти:

```python
path = Path("document.txt")

# Змінити розширення
new_path = path.with_suffix(".pdf")
print(new_path)  # document.pdf

# Змінити ім'я
new_path = path.with_name("report.txt")
print(new_path)  # report.txt

# Змінити stem (ім'я без розширення)
new_path = path.with_stem("report")
print(new_path)  # report.txt
```

### Інформація про файл:

```python
path = Path("file.txt")

if path.exists():
    stat = path.stat()

    print(f"Розмір: {stat.st_size} байт")
    print(f"Створено: {stat.st_ctime}")
    print(f"Змінено: {stat.st_mtime}")
```

### Перебір файлів:

```python
# Файли в директорії
folder = Path("my_folder")

for file in folder.iterdir():
    print(file)

# Тільки .txt файли
for txt_file in folder.glob("*.txt"):
    print(txt_file)

# Рекурсивний пошук
for py_file in folder.rglob("*.py"):
    print(py_file)
```

### Порівняння os.path vs pathlib:

| Операція          | os.path                      | pathlib                      |
| ----------------- | ---------------------------- | ---------------------------- |
| Об'єднання шляхів | `os.path.join(a, b, c)`      | `Path(a) / b / c`            |
| Існує?            | `os.path.exists(path)`       | `Path(path).exists()`        |
| Це файл?          | `os.path.isfile(path)`       | `Path(path).is_file()`       |
| Розмір            | `os.path.getsize(path)`      | `Path(path).stat().st_size`  |
| Читання           | `open(path).read()`          | `Path(path).read_text()`     |
| Запис             | `open(path, 'w').write(...)` | `Path(path).write_text(...)` |

---

## Абсолютні та відносні шляхи

### Абсолютний шлях

**Повний шлях від кореня диску.**

```python
# Windows
"C:\\Users\\Ivan\\Documents\\file.txt"

# Linux/Mac
"/home/ivan/documents/file.txt"
```

**Характеристики:**

- ✅ Точно визначає розташування
- ✅ Працює з будь-якої директорії
- ❌ Не переносимий між системами

### Відносний шлях

**Шлях відносно поточної директорії.**

```python
"file.txt"              # У поточній директорії
"data/file.txt"         # У піддиректорії data
"../file.txt"           # У батьківській директорії
"../../data/file.txt"   # На два рівні вгору, потім в data
```

**Характеристики:**

- ✅ Переносимий
- ✅ Коротший
- ❌ Залежить від поточної директорії

### Конвертація:

```python
from pathlib import Path

# Відносний → Абсолютний
relative = Path("file.txt")
absolute = relative.resolve()
print(absolute)  # /home/user/project/file.txt

# Абсолютний → Відносний
absolute = Path("/home/user/project/data/file.txt")
relative = absolute.relative_to("/home/user/project")
print(relative)  # data/file.txt
```

### Поточна директорія:

```python
import os
from pathlib import Path

# os
current = os.getcwd()

# pathlib
current = Path.cwd()
```

---

## Об'єднання шляхів

### os.path.join():

```python
import os

path = os.path.join("folder", "subfolder", "file.txt")
print(path)
# Windows: folder\subfolder\file.txt
# Linux: folder/subfolder/file.txt
```

### pathlib з /:

```python
from pathlib import Path

path = Path("folder") / "subfolder" / "file.txt"
print(path)  # folder/subfolder/file.txt
```

### Практичні приклади:

#### Створення шляху до файлу конфігурації:

```python
from pathlib import Path

# Домашня директорія + .config + app + settings.json
config_path = Path.home() / ".config" / "myapp" / "settings.json"
print(config_path)
# /home/user/.config/myapp/settings.json
```

#### Створення шляху до файлу логу:

```python
from pathlib import Path
import datetime

# Логи у піддиректорії logs
log_dir = Path("logs")
today = datetime.date.today()
log_file = log_dir / f"{today}.log"

print(log_file)  # logs/2025-11-07.log
```

---

## Розбір шляхів

### Компоненти шляху:

```python
from pathlib import Path

path = Path("/home/user/documents/report_2025.txt")

print(path.parts)      # ('/', 'home', 'user', 'documents', 'report_2025.txt')
print(path.parent)     # /home/user/documents
print(path.parents[0]) # /home/user/documents
print(path.parents[1]) # /home/user
print(path.name)       # report_2025.txt
print(path.stem)       # report_2025
print(path.suffix)     # .txt
print(path.anchor)     # / (корінь)
```

### Практичний приклад: обробка файлів за типом

```python
from pathlib import Path

def process_file(filepath):
    """Обробка файлу залежно від розширення"""
    path = Path(filepath)

    if path.suffix == ".txt":
        print(f"📝 Текстовий файл: {path.name}")
    elif path.suffix == ".py":
        print(f"🐍 Python файл: {path.name}")
    elif path.suffix in [".jpg", ".png", ".gif"]:
        print(f"🖼️ Зображення: {path.name}")
    else:
        print(f"❓ Невідомий тип: {path.name}")

process_file("document.txt")
process_file("script.py")
process_file("photo.jpg")
```

---

## Перевірка існування

### os.path.exists():

```python
import os

if os.path.exists("file.txt"):
    print("✅ Існує")
else:
    print("❌ Не існує")
```

### Path.exists():

```python
from pathlib import Path

path = Path("file.txt")
if path.exists():
    print("✅ Існує")
```

### Перевірка типу:

```python
from pathlib import Path

path = Path("something")

if path.exists():
    if path.is_file():
        print("📄 Це файл")
    elif path.is_dir():
        print("📁 Це директорія")
    elif path.is_symlink():
        print("🔗 Це символічне посилання")
```

### Безпечне відкриття файлу:

```python
from pathlib import Path

def safe_read(filename):
    """Безпечне читання файлу"""
    path = Path(filename)

    if not path.exists():
        print(f"❌ Файл {filename} не існує")
        return None

    if not path.is_file():
        print(f"❌ {filename} - не файл")
        return None

    try:
        return path.read_text(encoding="utf-8")
    except PermissionError:
        print(f"❌ Немає доступу до {filename}")
        return None
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return None

content = safe_read("data.txt")
if content:
    print(content)
```

---

## Створення директорій

### os.mkdir() - створити одну директорію:

```python
import os

# Створити директорію
os.mkdir("new_folder")

# Помилка якщо вже існує!
```

### os.makedirs() - створити з батьківськими:

```python
import os

# Створити всі відсутні директорії в шляху
os.makedirs("parent/child/grandchild")

# З параметром exist_ok - не помилка якщо існує
os.makedirs("folder", exist_ok=True)
```

### Path.mkdir():

```python
from pathlib import Path

# Створити директорію
folder = Path("new_folder")
folder.mkdir()

# З батьківськими директоріями
folder = Path("parent/child/grandchild")
folder.mkdir(parents=True, exist_ok=True)
```

### Параметри mkdir():

```python
folder.mkdir(
    parents=True,   # Створити батьківські директорії
    exist_ok=True   # Не помилка якщо існує
)
```

### Безпечне створення:

```python
from pathlib import Path

def create_folder(folder_name):
    """Безпечне створення директорії"""
    folder = Path(folder_name)

    if folder.exists():
        if folder.is_dir():
            print(f"ℹ️ Директорія {folder_name} вже існує")
            return True
        else:
            print(f"❌ {folder_name} існує, але це не директорія")
            return False

    try:
        folder.mkdir(parents=True)
        print(f"✅ Директорія {folder_name} створена")
        return True
    except Exception as e:
        print(f"❌ Помилка створення: {e}")
        return False

create_folder("logs/2025/november")
```

---

## Видалення файлів

### os.remove() - видалити файл:

```python
import os

# Видалити файл
os.remove("file.txt")

# Помилка якщо файл не існує або це директорія!
```

### Path.unlink() - видалити файл:

```python
from pathlib import Path

path = Path("file.txt")
path.unlink()

# З missing_ok (Python 3.8+)
path.unlink(missing_ok=True)  # Не помилка якщо не існує
```

### Безпечне видалення:

```python
from pathlib import Path

def safe_delete_file(filename):
    """Безпечне видалення файлу"""
    path = Path(filename)

    if not path.exists():
        print(f"ℹ️ Файл {filename} не існує")
        return True

    if not path.is_file():
        print(f"❌ {filename} - не файл")
        return False

    try:
        path.unlink()
        print(f"✅ Файл {filename} видалено")
        return True
    except PermissionError:
        print(f"❌ Немає прав для видалення {filename}")
        return False
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

safe_delete_file("temp.txt")
```

### Видалення групи файлів:

```python
from pathlib import Path

def delete_old_logs(log_dir, pattern="*.log"):
    """Видалити всі лог файли"""
    folder = Path(log_dir)

    deleted = 0
    for log_file in folder.glob(pattern):
        try:
            log_file.unlink()
            deleted += 1
            print(f"🗑️ Видалено: {log_file.name}")
        except Exception as e:
            print(f"❌ Не вдалось видалити {log_file.name}: {e}")

    print(f"✅ Видалено {deleted} файлів")

delete_old_logs("logs")
```

---

## Видалення директорій

### os.rmdir() - видалити порожню директорію:

```python
import os

# Видалити порожню директорію
os.rmdir("empty_folder")

# Помилка якщо директорія не порожня!
```

### shutil.rmtree() - видалити з вмістом:

```python
import shutil

# Видалити директорію з усім вмістом
shutil.rmtree("folder_with_files")

# ⚠️ НЕБЕЗПЕЧНО! Видаляє все безповоротно!
```

### Path.rmdir() - видалити порожню:

```python
from pathlib import Path

folder = Path("empty_folder")
folder.rmdir()  # Тільки якщо порожня
```

### Безпечне видалення директорії:

```python
from pathlib import Path
import shutil

def safe_remove_directory(folder_name):
    """Безпечне видалення директорії"""
    folder = Path(folder_name)

    if not folder.exists():
        print(f"ℹ️ Директорія {folder_name} не існує")
        return True

    if not folder.is_dir():
        print(f"❌ {folder_name} - не директорія")
        return False

    # Підрахунок файлів
    files = list(folder.rglob("*"))
    file_count = len([f for f in files if f.is_file()])

    if file_count > 0:
        confirm = input(f"⚠️ Директорія містить {file_count} файлів. Видалити? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Видалення скасовано")
            return False

    try:
        shutil.rmtree(folder)
        print(f"✅ Директорія {folder_name} видалена")
        return True
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

safe_remove_directory("old_project")
```

---

## Копіювання файлів

### shutil.copy() - копіювати файл:

```python
import shutil

# Копіювати файл
shutil.copy("source.txt", "destination.txt")

# Або в іншу директорію
shutil.copy("file.txt", "backup/")
```

### shutil.copy2() - зберегти метадані:

```python
import shutil

# Копіювати з збереженням дати модифікації
shutil.copy2("source.txt", "destination.txt")
```

### shutil.copytree() - копіювати директорію:

```python
import shutil

# Копіювати всю директорію
shutil.copytree("source_folder", "destination_folder")

# З ігноруванням деяких файлів
shutil.copytree(
    "source",
    "destination",
    ignore=shutil.ignore_patterns("*.pyc", "__pycache__")
)
```

### Безпечне копіювання:

```python
from pathlib import Path
import shutil

def safe_copy_file(source, destination):
    """Безпечне копіювання файлу"""
    src = Path(source)
    dst = Path(destination)

    # Перевірки
    if not src.exists():
        print(f"❌ Файл {source} не існує")
        return False

    if not src.is_file():
        print(f"❌ {source} - не файл")
        return False

    if dst.exists():
        confirm = input(f"⚠️ Файл {destination} вже існує. Перезаписати? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Копіювання скасовано")
            return False

    # Створити директорію призначення якщо не існує
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(src, dst)
        print(f"✅ Файл скопійовано: {source} → {destination}")
        return True
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

safe_copy_file("report.txt", "backup/report_backup.txt")
```

---

## Переміщення файлів

### shutil.move() - перемістити:

```python
import shutil

# Перемістити файл
shutil.move("file.txt", "new_location/file.txt")

# Перемістити директорію
shutil.move("old_folder", "new_location/old_folder")
```

### Безпечне переміщення:

```python
from pathlib import Path
import shutil

def safe_move(source, destination):
    """Безпечне переміщення файлу/директорії"""
    src = Path(source)
    dst = Path(destination)

    if not src.exists():
        print(f"❌ {source} не існує")
        return False

    if dst.exists():
        confirm = input(f"⚠️ {destination} вже існує. Замінити? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Переміщення скасовано")
            return False

        # Видалити існуючий
        if dst.is_file():
            dst.unlink()
        else:
            shutil.rmtree(dst)

    # Створити батьківську директорію
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        print(f"✅ Переміщено: {source} → {destination}")
        return True
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

safe_move("old_file.txt", "archive/old_file.txt")
```

---

## Перейменування файлів

### os.rename():

```python
import os

# Перейменувати файл
os.rename("old_name.txt", "new_name.txt")
```

### Path.rename():

```python
from pathlib import Path

old_path = Path("old_name.txt")
new_path = old_path.rename("new_name.txt")
```

### Масове перейменування:

```python
from pathlib import Path

def rename_files(directory, old_pattern, new_pattern):
    """Перейменувати файли за патерном"""
    folder = Path(directory)

    for file in folder.glob(old_pattern):
        # Замінити частину імені
        new_name = file.name.replace(old_pattern.replace("*", ""), new_pattern)
        new_path = file.parent / new_name

        file.rename(new_path)
        print(f"✏️ {file.name} → {new_name}")

# Перейменувати всі .tmp на .txt
rename_files("data", "*.tmp", ".txt")
```

### Додати префікс:

```python
from pathlib import Path

def add_prefix(directory, prefix):
    """Додати префікс до всіх файлів"""
    folder = Path(directory)

    for file in folder.iterdir():
        if file.is_file():
            new_name = prefix + file.name
            new_path = file.parent / new_name
            file.rename(new_path)
            print(f"✏️ {file.name} → {new_name}")

add_prefix("photos", "2025_")
```

---

## Розмір файлу

### os.path.getsize():

```python
import os

size = os.path.getsize("file.txt")
print(f"Розмір: {size} байт")
```

### Path.stat().st_size:

```python
from pathlib import Path

path = Path("file.txt")
size = path.stat().st_size
print(f"Розмір: {size} байт")
```

### Форматування розміру:

```python
def format_size(bytes):
    """Форматувати розмір файлу"""
    for unit in ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} ПБ"

size = Path("large_file.bin").stat().st_size
print(f"Розмір: {format_size(size)}")
```

### Розмір директорії:

```python
from pathlib import Path

def get_directory_size(directory):
    """Обчислити розмір директорії"""
    folder = Path(directory)
    total_size = 0

    for file in folder.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size

    return total_size

size = get_directory_size("my_project")
print(f"Розмір директорії: {format_size(size)}")
```

---

## Дата створення та модифікації

### os.path.getmtime() - дата модифікації:

```python
import os
import datetime

# Timestamp
mtime = os.path.getmtime("file.txt")

# Конвертувати в читабельний формат
date = datetime.datetime.fromtimestamp(mtime)
print(f"Змінено: {date}")
```

### Path.stat():

```python
from pathlib import Path
import datetime

path = Path("file.txt")
stat = path.stat()

# Дата створення (Windows)
ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
print(f"Створено: {ctime}")

# Дата модифікації
mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
print(f"Змінено: {mtime}")

# Дата останнього доступу
atime = datetime.datetime.fromtimestamp(stat.st_atime)
print(f"Доступ: {atime}")
```

### Пошук нових файлів:

```python
from pathlib import Path
import datetime

def find_recent_files(directory, days=7):
    """Знайти файли, змінені за останні N днів"""
    folder = Path(directory)
    now = datetime.datetime.now().timestamp()
    cutoff = now - (days * 24 * 60 * 60)

    recent_files = []
    for file in folder.rglob("*"):
        if file.is_file():
            mtime = file.stat().st_mtime
            if mtime > cutoff:
                date = datetime.datetime.fromtimestamp(mtime)
                recent_files.append((file, date))

    # Сортувати за датою
    recent_files.sort(key=lambda x: x[1], reverse=True)

    return recent_files

files = find_recent_files("project", days=7)
for file, date in files:
    print(f"{date:%Y-%m-%d %H:%M} - {file.name}")
```

---

## Атрибути файлів

### os.stat():

```python
import os

stat_info = os.stat("file.txt")

print(f"Розмір: {stat_info.st_size}")
print(f"Створено: {stat_info.st_ctime}")
print(f"Змінено: {stat_info.st_mtime}")
print(f"Доступ: {stat_info.st_atime}")
print(f"Mode: {stat_info.st_mode}")
print(f"Inode: {stat_info.st_ino}")
```

### Path.stat():

```python
from pathlib import Path

path = Path("file.txt")
stat = path.stat()

print(f"📏 Розмір: {stat.st_size} байт")
print(f"📅 Створено: {stat.st_ctime}")
print(f"📝 Змінено: {stat.st_mtime}")
print(f"👁️ Доступ: {stat.st_atime}")
```

### Повна інформація про файл:

```python
from pathlib import Path
import datetime

def file_info(filepath):
    """Детальна інформація про файл"""
    path = Path(filepath)

    if not path.exists():
        print(f"❌ Файл {filepath} не існує")
        return

    stat = path.stat()

    print(f"📁 Файл: {path.name}")
    print(f"📂 Директорія: {path.parent}")
    print(f"📏 Розмір: {format_size(stat.st_size)}")
    print(f"🔖 Розширення: {path.suffix}")

    ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
    mtime = datetime.datetime.fromtimestamp(stat.st_mtime)

    print(f"📅 Створено: {ctime:%Y-%m-%d %H:%M:%S}")
    print(f"📝 Змінено: {mtime:%Y-%m-%d %H:%M:%S}")

    # Права доступу (Linux/Mac)
    import stat as stat_module
    mode = stat.st_mode
    is_readable = bool(mode & stat_module.S_IRUSR)
    is_writable = bool(mode & stat_module.S_IWUSR)
    is_executable = bool(mode & stat_module.S_IXUSR)

    print(f"🔒 Читання: {'✅' if is_readable else '❌'}")
    print(f"✏️ Запис: {'✅' if is_writable else '❌'}")
    print(f"▶️ Виконання: {'✅' if is_executable else '❌'}")

file_info("document.txt")
```

---

## Перебір файлів у директорії

### os.listdir():

```python
import os

# Отримати список файлів та папок
files = os.listdir("my_folder")
for name in files:
    print(name)
```

### Path.iterdir():

```python
from pathlib import Path

folder = Path("my_folder")

# Перебрати всі елементи
for item in folder.iterdir():
    if item.is_file():
        print(f"📄 {item.name}")
    elif item.is_dir():
        print(f"📁 {item.name}")
```

### Фільтрація за розширенням:

```python
from pathlib import Path

folder = Path("documents")

# Тільки .txt файли
for txt_file in folder.glob("*.txt"):
    print(txt_file.name)

# Тільки .py файли
for py_file in folder.glob("*.py"):
    print(py_file.name)
```

### Кілька розширень:

```python
from pathlib import Path

folder = Path("media")

# Зображення
image_extensions = ["*.jpg", "*.png", "*.gif"]

for pattern in image_extensions:
    for image in folder.glob(pattern):
        print(image.name)
```

---

## Рекурсивний перебір

### os.walk():

```python
import os

# Перебрати всі файли рекурсивно
for root, dirs, files in os.walk("project"):
    print(f"Директорія: {root}")
    for file in files:
        full_path = os.path.join(root, file)
        print(f"  📄 {file}")
```

### Path.rglob():

```python
from pathlib import Path

folder = Path("project")

# Всі .py файли рекурсивно
for py_file in folder.rglob("*.py"):
    print(py_file)
```

### Практичний приклад: підрахунок файлів:

```python
from pathlib import Path
from collections import defaultdict

def count_files_by_extension(directory):
    """Підрахувати файли за розширенням"""
    folder = Path(directory)
    counts = defaultdict(int)

    for file in folder.rglob("*"):
        if file.is_file():
            ext = file.suffix or "(без розширення)"
            counts[ext] += 1

    print(f"📊 Статистика для {directory}:")
    for ext, count in sorted(counts.items()):
        print(f"  {ext}: {count} файлів")

    total = sum(counts.values())
    print(f"📁 Всього: {total} файлів")

count_files_by_extension("my_project")
```

### Пошук великих файлів:

```python
from pathlib import Path

def find_large_files(directory, min_size_mb=10):
    """Знайти файли більші за N МБ"""
    folder = Path(directory)
    min_size_bytes = min_size_mb * 1024 * 1024

    large_files = []

    for file in folder.rglob("*"):
        if file.is_file():
            size = file.stat().st_size
            if size > min_size_bytes:
                large_files.append((file, size))

    # Сортувати за розміром (найбільші спочатку)
    large_files.sort(key=lambda x: x[1], reverse=True)

    print(f"📊 Файли більше {min_size_mb} МБ:")
    for file, size in large_files:
        print(f"  {format_size(size)} - {file}")

    return large_files

find_large_files("project", min_size_mb=5)
```

---

## Текстові файли (.txt)

### Читання:

```python
# Простий спосіб
with open("text.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# По рядках
with open("text.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

### Запис:

```python
# Перезапис
with open("text.txt", "w", encoding="utf-8") as file:
    file.write("Перший рядок\n")
    file.write("Другий рядок\n")

# Дозапис
with open("text.txt", "a", encoding="utf-8") as file:
    file.write("Додатковий рядок\n")
```

### Практичний приклад: обробка лог-файлу

```python
def analyze_log(log_file):
    """Аналіз лог-файлу"""
    errors = 0
    warnings = 0
    info = 0

    with open(log_file, "r", encoding="utf-8") as file:
        for line in file:
            if "ERROR" in line:
                errors += 1
            elif "WARNING" in line:
                warnings += 1
            elif "INFO" in line:
                info += 1

    print(f"📊 Аналіз {log_file}:")
    print(f"  ❌ Errors: {errors}")
    print(f"  ⚠️ Warnings: {warnings}")
    print(f"  ℹ️ Info: {info}")
    print(f"  📁 Всього рядків: {errors + warnings + info}")

analyze_log("app.log")
```

---

## CSV файли

### Читання CSV:

```python
import csv

# Читання CSV
with open("data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)

    # Пропустити заголовок
    header = next(reader)
    print(f"Заголовки: {header}")

    # Прочитати дані
    for row in reader:
        print(row)
```

### Запис CSV:

```python
import csv

data = [
    ["Ім'я", "Вік", "Місто"],
    ["Іван", 25, "Київ"],
    ["Марія", 30, "Львів"],
    ["Петро", 22, "Одеса"]
]

with open("users.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

### CSV як словник:

```python
import csv

# Читання як словник
with open("users.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"Ім'я: {row['Ім\'я']}, Вік: {row['Вік']}")

# Запис як словник
users = [
    {"name": "Іван", "age": 25, "city": "Київ"},
    {"name": "Марія", "age": 30, "city": "Львів"}
]

with open("users.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["name", "age", "city"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(users)
```

---

## JSON файли

### Читання JSON:

```python
import json

# Прочитати JSON файл
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    print(data)
```

### Запис JSON:

```python
import json

data = {
    "name": "Іван",
    "age": 25,
    "skills": ["Python", "JavaScript", "SQL"]
}

# Записати JSON файл
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
```

### Параметри json.dump():

```python
json.dump(
    data,
    file,
    indent=2,           # Відступи для читабельності
    ensure_ascii=False, # Не екранувати кирилицю
    sort_keys=True      # Сортувати ключі
)
```

### Практичний приклад: конфігурація

```python
import json
from pathlib import Path

class Config:
    """Менеджер конфігурації"""

    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.data = self.load()

    def load(self):
        """Завантажити конфігурацію"""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save(self):
        """Зберегти конфігурацію"""
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        """Отримати значення"""
        return self.data.get(key, default)

    def set(self, key, value):
        """Встановити значення"""
        self.data[key] = value
        self.save()

# Використання
config = Config()
config.set("theme", "dark")
config.set("language", "uk")
theme = config.get("theme")
print(f"Тема: {theme}")
```

---

## Бінарні файли

### Читання бінарного файлу:

```python
# Прочитати весь файл
with open("image.png", "rb") as file:
    data = file.read()
    print(f"Розмір: {len(data)} байт")
```

### Запис бінарного файлу:

```python
# Записати байти
binary_data = b'\x89PNG\r\n\x1a\n'

with open("output.bin", "wb") as file:
    file.write(binary_data)
```

### Копіювання бінарного файлу:

```python
def copy_binary_file(source, destination):
    """Копіювати бінарний файл"""
    with open(source, "rb") as src:
        with open(destination, "wb") as dst:
            # Копіювати по 8 КБ
            while True:
                chunk = src.read(8192)
                if not chunk:
                    break
                dst.write(chunk)

    print(f"✅ Скопійовано: {source} → {destination}")

copy_binary_file("image.png", "backup/image.png")
```

### Читання структурованих даних:

```python
import struct

# Прочитати 4 байти як integer
with open("data.bin", "rb") as file:
    data = file.read(4)
    number = struct.unpack('i', data)[0]
    print(f"Число: {number}")

# Записати integer як 4 байти
with open("data.bin", "wb") as file:
    number = 12345
    data = struct.pack('i', number)
    file.write(data)
```

---

## Тимчасові файли

### tempfile модуль:

```python
import tempfile

# Тимчасовий файл (автоматично видалиться)
with tempfile.TemporaryFile(mode='w+t') as temp:
    temp.write("Тимчасові дані\n")
    temp.seek(0)
    content = temp.read()
    print(content)
# Файл автоматично видалено
```

### Іменований тимчасовий файл:

```python
import tempfile

# Тимчасовий файл з ім'ям
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp:
    temp.write("Тимчасові дані")
    temp_path = temp.name
    print(f"Тимчасовий файл: {temp_path}")

# Файл існує після закриття
print(f"Файл існує: {Path(temp_path).exists()}")

# Видалити вручну
Path(temp_path).unlink()
```

### Тимчасова директорія:

```python
import tempfile
from pathlib import Path

# Тимчасова директорія
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Створити файли у тимчасовій директорії
    file1 = temp_path / "file1.txt"
    file1.write_text("Вміст 1")

    file2 = temp_path / "file2.txt"
    file2.write_text("Вміст 2")

    print(f"Тимчасова директорія: {temp_dir}")
    print(f"Файлів: {len(list(temp_path.iterdir()))}")
# Директорія та всі файли автоматично видалені
```

---

## Файлові винятки

### Основні винятки:

| Виняток              | Коли виникає                       |
| -------------------- | ---------------------------------- |
| `FileNotFoundError`  | Файл не знайдено                   |
| `PermissionError`    | Немає прав доступу                 |
| `IsADirectoryError`  | Очікується файл, але це директорія |
| `NotADirectoryError` | Очікується директорія, але це файл |
| `FileExistsError`    | Файл вже існує (режим 'x')         |
| `IOError`            | Загальна помилка вводу/виводу      |

---

## FileNotFoundError

### Коли виникає:

```python
# Спроба відкрити неіснуючий файл
file = open("missing.txt", "r")  # ❌ FileNotFoundError
```

### Обробка:

```python
try:
    with open("file.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("❌ Файл не знайдено")
```

### Безпечне читання:

```python
from pathlib import Path

def safe_read(filename):
    """Безпечне читання з обробкою помилок"""
    try:
        path = Path(filename)
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"❌ Файл {filename} не знайдено")
        return None
    except PermissionError:
        print(f"❌ Немає доступу до {filename}")
        return None
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return None
```

---

## PermissionError

### Коли виникає:

```python
# Спроба записати в захищений файл
with open("/etc/passwd", "w") as file:  # ❌ PermissionError
    file.write("data")
```

### Обробка:

```python
try:
    with open("protected.txt", "w") as file:
        file.write("Дані")
except PermissionError:
    print("❌ Немає прав для запису")
```

---

## IsADirectoryError

### Коли виникає:

```python
# Спроба відкрити директорію як файл
with open("my_folder", "r") as file:  # ❌ IsADirectoryError
    content = file.read()
```

### Перевірка:

```python
from pathlib import Path

path = Path("something")

if path.exists():
    if path.is_file():
        with open(path, "r") as file:
            content = file.read()
    elif path.is_dir():
        print("❌ Це директорія, а не файл")
```

---

## Безпечна робота з файлами

### Шаблон безпечної роботи:

```python
from pathlib import Path

def safe_file_operation(filename, operation="read"):
    """Універсальна безпечна робота з файлами"""
    path = Path(filename)

    try:
        # Перевірки
        if operation == "read":
            if not path.exists():
                print(f"❌ Файл {filename} не існує")
                return None
            if not path.is_file():
                print(f"❌ {filename} - не файл")
                return None

        # Операція
        if operation == "read":
            return path.read_text(encoding="utf-8")
        elif operation == "write":
            path.write_text("Дані", encoding="utf-8")
            return True

    except FileNotFoundError:
        print(f"❌ Файл {filename} не знайдено")
    except PermissionError:
        print(f"❌ Немає доступу до {filename}")
    except IsADirectoryError:
        print(f"❌ {filename} - це директорія")
    except Exception as e:
        print(f"❌ Несподівана помилка: {e}")

    return None
```

---

## Практичні приклади

### Приклад 1: Менеджер замі
