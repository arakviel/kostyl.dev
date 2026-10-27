# 💾 Повний посібник з роботи з даними: JSON та CSV

## Зміст

### Вступ
1.  [Навіщо потрібні формати даних?](#навіщо-потрібні-формати-даних)
2.  [Структуровані та неструктуровані дані](#структуровані-та-неструктуровані-дані)

### Частина 1: JSON (JavaScript Object Notation)
3.  [Що таке JSON?](#що-таке-json)
4.  [Синтаксис JSON та відповідність Python](#синтаксис-json-та-відповідність-python)
5.  [Модуль `json` у Python](#модуль-json-у-python)
6.  [Серіалізація: з Python у JSON](#серіалізація-з-python-у-json)
    -   [`json.dumps()`: перетворення у рядок](#jsondumps-перетворення-у-рядок)
    -   [Pretty-printing: `indent` та `sort_keys`](#pretty-printing-indent-та-sort_keys)
    -   [`json.dump()`: запис у файл](#jsondump-запис-у-файл)
7.  [Десеріалізація: з JSON у Python](#десеріалізація-з-json-у-python)
    -   [`json.loads()`: парсинг з рядка](#jsonloads-парсинг-з-рядка)
    -   [`json.load()`: читання з файлу](#jsonload-читання-з-файлу)
8.  [Обробка складних та вкладених даних](#обробка-складних-та-вкладених-даних)
9.  [Обробка помилок: `JSONDecodeError`](#обробка-помилок-jsondecodeerror)
10. [Практичний приклад: конфігураційний файл](#практичний-приклад-конфігураційний-файл)

### Частина 2: CSV (Comma-Separated Values)
11. [Що таке CSV?](#що-таке-csv)
12. [Чому не варто парсити CSV вручну?](#чому-не-варто-парсити-csv-вручну)
13. [Модуль `csv` у Python](#модуль-csv-у-python)
14. [Читання з CSV файлів](#читання-з-csv-файлів)
    -   [`csv.reader()`: читання по рядках](#csvreader-читання-по-рядках)
    -   [`csv.DictReader()`: читання у словники](#csvdictreader-читання-у-словники)
15. [Запис у CSV файли](#запис-у-csv-файли)
    -   [Важливість `newline=''`](#важливість-newline)
    -   [`csv.writer()`: запис списків](#csvwriter-запис-списків)
    -   [`csv.DictWriter()`: запис словників](#csvdictwriter-запис-словників)
16. [Діалекти та параметри форматування](#діалекти-та-параметри-форматування)
    -   [Параметр `delimiter`](#параметр-delimiter)
    -   [Параметри `quotechar` та `quoting`](#параметри-quotechar-та-quoting)
17. [Практичний приклад: обробка табличних даних](#практичний-приклад-обробка-табличних-даних)

### Висновки
18. [JSON vs. CSV: що і коли використовувати?](#json-vs-csv-що-і-коли-використовувати)
19. [Підсумки](#підсумки)

---
## Вступ

### Навіщо потрібні формати даних?

У попередніх лекціях ми навчилися працювати з файлами, читаючи та записуючи в них переважно простий текст. Але що робити, якщо нам потрібно зберегти складну структуру даних, наприклад, список словників, або налаштування програми?

```python
users = [
    {'id': 1, 'name': 'Іван', 'role': 'admin'},
    {'id': 2, 'name': 'Марія', 'role': 'user'}
]
```
Якщо ми просто запишемо це у файл за допомогою `str(users)`, ми отримаємо рядок, який потім буде дуже складно і ненадійно розібрати (парсити) назад у структуру Python.

**Формати даних** — це стандартизовані способи представлення структурованих даних у текстовому вигляді. Вони дозволяють різним програмам, навіть написаним різними мовами, легко обмінюватися інформацією.

**Основні задачі форматів даних:**
1.  **Збереження стану:** Зберегти налаштування або дані програми між запусками.
2.  **Обмін даними:** Передати дані з однієї програми в іншу (наприклад, з Python-скрипта в Excel).
3.  **Веб-API:** Отримувати дані з веб-серверів. Більшість сучасних API використовують JSON.
4.  **Конфігурація:** Зберігати конфігураційні параметри програми у зрозумілому для людини форматі.

---

### Структуровані та неструктуровані дані

-   **Неструктуровані дані:** Простий текстовий файл (`.txt`), книга, стаття. Немає чіткої, машиночитаємої структури.
-   **Структуровані дані:** Дані, організовані за певними правилами. Наприклад, таблиця в базі даних або XML-документ. Комп'ютеру легко їх "зрозуміти".

**JSON** і **CSV** — це два найпопулярніші формати для представлення структурованих даних у текстових файлах.

---
## Частина 1: JSON (JavaScript Object Notation)

### Що таке JSON?

**JSON** — це легкий текстовий формат для обміну даними, який є зрозумілим як для людини, так і для комп'ютера. Хоча він походить з JavaScript, сьогодні він є стандартом де-факто для веб-API та конфігураційних файлів у всіх мовах програмування.

**Аналогія:** JSON — це як універсальний перекладач для структур даних. Ви "говорите" йому на Python, а він перекладає це на універсальну мову, яку зрозуміє будь-яка інша програма.

**Приклад JSON:**
```json
{
    "firstName": "Іван",
    "lastName": "Петренко",
    "isActive": true,
    "role": null,
    "age": 30,
    "courses": [
        "Python Core",
        "Data Science"
    ],
    "contact": {
        "email": "ivan.petrenko@example.com",
        "phone": "+380501234567"
    }
}
```

---

### Синтаксис JSON та відповідність Python

Синтаксис JSON дуже схожий на синтаксис об'єктів та списків у Python, що робить роботу з ним надзвичайно простою.

| JSON                 | Python             | Опис                                      |
| -------------------- | ------------------ | ----------------------------------------- |
| `object` (об'єкт)    | `dict` (словник)   | Набір пар "ключ-значення"                 |
| `array` (масив)      | `list` (список)    | Впорядкована колекція значень            |
| `string` (рядок)     | `str` (рядок)      | Текст у подвійних лапках (`"`)            |
| `number` (число)     | `int`, `float`     | Цілі або дійсні числа                     |
| `true` / `false`     | `True` / `False`   | Булеві значення (пишуться з малої літери!) |
| `null`               | `None`             | Порожнє значення                         |

**Ключові відмінності:**
-   Ключі в JSON **завжди** є рядками у подвійних лапках.
-   JSON не має специфічного типу для кортежів (`tuple`) або множин (`set`). Вони зазвичай перетворюються на масиви (`array`).
-   Логічні значення та `null` пишуться з малої літери.

---

### Модуль `json` у Python

Python має вбудований модуль `json`, який надає всі необхідні інструменти для роботи з цим форматом. Його не потрібно встановлювати.

```python
import json
```

Робота з модулем `json` ділиться на два основні процеси:
1.  **Серіалізація (Serialization) або кодування (Encoding):** Перетворення об'єкта Python у рядок формату JSON. `(dict -> str)`
2.  **Десеріалізація (Deserialization) або декодування (Decoding):** Перетворення (парсинг) рядка формату JSON в об'єкт Python. `(str -> dict)`

---

### Серіалізація: з Python у JSON

#### `json.dumps()`: перетворення у рядок

Функція `json.dumps()` (dump string) бере об'єкт Python і повертає рядок у форматі JSON.

```python
import json

# Створюємо словник Python
data = {
    "name": "Марія",
    "age": 28,
    "is_student": False,
    "courses": ["History", "Art"],
    "credentials": None
}

# Серіалізуємо у рядок
json_string = json.dumps(data)

print("Тип результату:", type(json_string))
print("Результат (неформатований):")
print(json_string)
# {"name": "Марія", "age": 28, "is_student": false, "courses": ["History", "Art"], "credentials": null}
```
Як бачимо, `False` перетворилось на `false`, `None` — на `null`, а одинарні лапки замінились на подвійні.

#### Pretty-printing: `indent` та `sort_keys`

Отриманий рядок важко читати. `dumps()` має параметри для форматування:

-   `indent`: кількість пробілів для відступу. Робить JSON-рядок читабельним для людини.
-   `sort_keys`: сортувати ключі в об'єктах за алфавітом.

```python
import json

data = {
    "name": "Марія",
    "age": 28,
    "is_student": False,
    "courses": ["History", "Art"],
    "credentials": None
}

# Серіалізуємо з форматуванням
pretty_json_string = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
# ensure_ascii=False потрібно для коректного відображення кирилиці

print("\nРезультат (форматований):")
print(pretty_json_string)
```

**Вивід:**
```json
{
    "age": 28,
    "courses": [
        "History",
        "Art"
    ],
    "credentials": null,
    "is_student": false,
    "name": "Марія"
}
```
Такий вивід набагато легше читати та аналізувати.

#### `json.dump()`: запис у файл

Функція `json.dump()` (без 's') робить те ж саме, але записує результат напряму у **файловий об'єкт**, а не повертає рядок. Це більш ефективно.

```python
import json

data_to_save = {
    "user_id": 12345,
    "username": "super_coder",
    "settings": {
        "theme": "dark",
        "notifications": True
    }
}

# Використовуємо 'with' для безпечної роботи з файлом
with open("user_settings.json", "w", encoding="utf-8") as json_file:
    # Записуємо дані у файл з форматуванням
    json.dump(data_to_save, json_file, indent=4, ensure_ascii=False)

print("Дані успішно збережено у файл user_settings.json")
```
Якщо ви відкриєте створений файл `user_settings.json`, ви побачите гарно відформатований JSON.

---

### Десеріалізація: з JSON у Python

#### `json.loads()`: парсинг з рядка

Функція `json.loads()` (load string) бере рядок, що містить JSON, і перетворює його на об'єкт Python.

```python
import json

# Уявімо, що ми отримали цей рядок з веб-API
json_string = '{"id": 9, "title": "Infinix INBOOK", "price": 1099, "brand": "Infinix"}'

# Десеріалізуємо рядок у словник Python
product_data = json.loads(json_string)

print("Тип результату:", type(product_data))
print("Результат (словник Python):")
print(product_data)
print(f"Назва товару: {product_data['title']}")
```

#### `json.load()`: читання з файлу

Функція `json.load()` (без 's') читає дані з **файлового об'єкта** і перетворює їх на об'єкт Python.

Давайте прочитаємо файл `user_settings.json`, який ми створили раніше.

```python
import json

try:
    with open("user_settings.json", "r", encoding="utf-8") as json_file:
        # Завантажуємо дані з файлу
        loaded_data = json.load(json_file)
    
    print("Дані успішно завантажено з файлу.")
    print("Тип результату:", type(loaded_data))
    print("Завантажені дані:")
    print(loaded_data)
    
    # Тепер ми можемо працювати з ними як зі звичайним словником
    if loaded_data['settings']['notifications']:
        print("Сповіщення увімкнені.")

except FileNotFoundError:
    print("Помилка: файл user_settings.json не знайдено.")

```

---

### Обробка складних та вкладених даних

Сила JSON у його здатності представляти вкладені структури. Робота з ними в Python є інтуїтивною.

```python
import json

complex_json = """
{
    "quiz": {
        "sport": {
            "q1": {
                "question": "Which one is correct team name in NBA?",
                "options": [
                    "New York Bulls",
                    "Los Angeles Kings",
                    "Golden State Warriros",
                    "Huston Rocket"
                ],
                "answer": "Huston Rocket"
            }
        },
        "maths": {
            "q1": {
                "question": "5 + 7 = ?",
                "options": [ "10", "11", "12", "13" ],
                "answer": "12"
            }
        }
    }
}
"""

data = json.loads(complex_json)

# Доступ до вкладених даних
math_question = data['quiz']['maths']['q1']['question']
print(f"Питання з математики: {math_question}")

sport_options = data['quiz']['sport']['q1']['options']
print(f"Варіанти відповідей про спорт: {sport_options}")

# Прохід по вкладених елементах
for option in sport_options:
    print(f"- {option}")
```

---

### Обробка помилок: `JSONDecodeError`

Що станеться, якщо текст у файлі або рядку не є валідним JSON? Модуль `json` видасть помилку `json.decoder.JSONDecodeError`.

**Приклад невалідного JSON (зайва кома):**
```
{"name": "Іван",}
```

```python
import json

invalid_json = '{"name": "Іван",}' # Кома після останнього елемента

try:
    data = json.loads(invalid_json)
except json.decoder.JSONDecodeError as e:
    print("Помилка декодування JSON!")
    print(f"Тип помилки: {type(e)}")
    print(f"Повідомлення: {e}")
```
**Вивід:**
```
Помилка декодування JSON!
Тип помилки: <class 'json.decoder.JSONDecodeError'>
Повідомлення: Expecting property name enclosed in double quotes: line 1 column 16 (char 15)
```
Завжди загортайте `json.load()` та `json.loads()` у блок `try...except`, якщо ви не впевнені у надійності джерела даних.

---

### Практичний приклад: конфігураційний файл

Давайте створимо програму, яка читає налаштування з `config.json`, виконує якусь дію, і створює новий `config.json` за замовчуванням, якщо його не існує.

**Файл `config_manager.py`:**
```python
import json

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "server_ip": "127.0.0.1",
    "port": 8080,
    "debug_mode": False
}

def load_config():
    """Завантажує конфігурацію з файлу або створює файл за замовчуванням."""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            print(f"Знайдено і завантажено '{CONFIG_FILE}'.")
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл '{CONFIG_FILE}' не знайдено. Створюємо новий.")
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    except json.JSONDecodeError:
        print(f"Помилка в синтаксисі '{CONFIG_FILE}'. Використовуються налаштування за замовчуванням.")
        return DEFAULT_CONFIG

# Основна логіка
if __name__ == "__main__":
    config = load_config()
    
    print("\nПоточні налаштування:")
    print(config)
    
    ip = config.get("server_ip", "localhost")
    port = config.get("port", 8000)
    
    if config.get("debug_mode"):
        print("\nПрограма працює в режимі налагодження.")
    
    print(f"\nПідключаємось до сервера {ip}:{port}...")
    print("Робота завершена.")
```
Запустіть цей скрипт двічі. Перший раз він створить файл, другий — прочитає його. Потім спробуйте вручну зламати синтаксис у `config.json` і подивіться, як відпрацює обробка помилок.

---
## Частина 2: CSV (Comma-Separated Values)

### Що таке CSV?

**CSV** — це текстовий формат для представлення табличних даних, де кожний рядок файлу відповідає рядку таблиці, а значення в стовпцях розділені певним символом, найчастіше комою.

**Аналогія:** CSV — це найпростіший спосіб записати електронну таблицю (як в Excel або Google Sheets) у текстовий файл.

**Приклад `users.csv`:**
```csv
FirstName,LastName,Age,City
Іван,Петренко,30,Київ
Марія,Сидоренко,25,Львів
Петро,Коваленко,42,Одеса
```
-   Перший рядок зазвичай є **заголовком** (header), що описує стовпці.
-   Кожен наступний рядок — це один запис.

---

### Чому не варто парсити CSV вручну?

На перший погляд, можна просто читати файл по рядках і використовувати `line.strip().split(',')`.

```python
# ❌ Поганий, ненадійний підхід
with open("users.csv", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(',')
        print(parts)
```
**Це не спрацює, якщо:**
1.  **Значення містить кому:** `... ,"вул. Хрещатик, 24", ...`. `split(',')` розділить адресу на дві частини.
2.  **Значення взято в лапки:** `"Марія","Сидоренко",25,"Львів"`
3.  **Значення містить переноси рядків:** Текстові поля можуть бути багаторядковими, якщо вони взяті в лапки.

Стандартний модуль `csv` розроблено спеціально для коректної обробки всіх цих випадків. **Завжди використовуйте його!**

---

### Модуль `csv` у Python

Модуль `csv` є частиною стандартної бібліотеки і надає інструменти для читання та запису CSV файлів.

```python
import csv
```

---

### Читання з CSV файлів

#### `csv.reader()`: читання по рядках

`csv.reader` створює об'єкт, який ітерується по рядках CSV файлу. Кожен рядок повертається як **список рядків**.

**Файл `products.csv`:**
```csv
id,name,price
101,Ноутбук,35000
102,Миша,800
103,"Монітор 27"", Full HD",7200
```
**Код для читання:**
```python
import csv

try:
    with open("products.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        
        # Пропускаємо заголовок
        header = next(reader)
        print(f"Заголовки: {header}")
        
        print("\nДані:")
        # Ітеруємось по решті рядків
        for row in reader:
            # row - це список рядків: ['101', 'Ноутбук', '35000']
            product_id = int(row[0])
            name = row[1]
            price = int(row[2])
            print(f"ID: {product_id}, Назва: {name}, Ціна: {price} грн")

except FileNotFoundError:
    print("Файл products.csv не знайдено.")
```

#### `csv.DictReader()`: читання у словники

Це набагато зручніший спосіб, оскільки він автоматично використовує перший рядок як ключі і повертає кожен рядок як словник.

```python
import csv

try:
    with open("products.csv", "r", encoding="utf-8") as f:
        # DictReader автоматично знайде заголовок
        reader = csv.DictReader(f)
        
        print("Дані (зі словників):")
        # кожний row - це словник: {'id': '101', 'name': 'Ноутбук', 'price': '35000'}
        for row in reader:
            # Доступ до даних за назвою стовпця - набагато чистіше!
            name = row['name']
            price = int(row['price'])
            print(f"Назва: {name}, Ціна: {price} грн")

except FileNotFoundError:
    print("Файл products.csv не знайдено.")
```
**`DictReader` є рекомендованим способом читання для більшості завдань.**

---

### Запис у CSV файли

#### Важливість `newline=''`

При відкритті файлу для запису CSV **завжди** вказуйте `newline=''`.
```python
with open("output.csv", "w", encoding="utf-8", newline='') as f:
    # ...
```
Це пов'язано з тим, як різні ОС обробляють символи кінця рядка (`\n` на Linux/Mac, `\r\n` на Windows). Без `newline=''` модуль `csv` може додавати зайві пусті рядки у файл на Windows.

#### `csv.writer()`: запис списків

`csv.writer` створює об'єкт для запису даних у CSV. Дані мають бути у вигляді списків.

```python
import csv

data_to_write = [
    ['рік', 'модель', 'ціна'],
    [2021, 'Tesla Model S', 3200000],
    [2022, 'Ford Mustang Mach-E', 2100000],
    [2023, 'Hyundai Ioniq 5', 1800000]
]

with open("cars.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    
    # Записати всі рядки одразу
    writer.writerows(data_to_write)
    
    # Або можна записувати по одному
    # writer.writerow(data_to_write[0])
    # writer.writerow(data_to_write[1])
    
print("Файл cars.csv створено.")
```

#### `csv.DictWriter()`: запис словників

Аналогічно до `DictReader`, цей спосіб є більш зручним та надійним, оскільки працює зі словниками.

```python
import csv

data_to_write = [
    {'рік': 2021, 'модель': 'Tesla Model S', 'ціна': 3200000},
    {'рік': 2022, 'модель': 'Ford Mustang Mach-E', 'ціна': 2100000},
    {'рік': 2023, 'модель': 'Hyundai Ioniq 5', 'ціна': 1800000}
]

# Список ключів, які будуть заголовками
field_names = ['рік', 'модель', 'ціна']

with open("cars_dict.csv", "w", encoding="utf-8", newline='') as f:
    # Створюємо DictWriter, передаючи йому імена полів
    writer = csv.DictWriter(f, fieldnames=field_names)
    
    # Записуємо рядок заголовків
    writer.writeheader()
    
    # Записуємо всі дані
    writer.writerows(data_to_write)
    
print("Файл cars_dict.csv створено.")
```

---

### Діалекти та параметри форматування

Не всі CSV-файли однакові. Іноді замість коми використовується крапка з комою, а замість подвійних лапок — одинарні. `csv` дозволяє це налаштувати.

#### Параметр `delimiter`
Вказує, який символ використовується для розділення стовпців.

**Файл `data.tsv` (Tab-Separated Values):**
```csv
Назва\tКатегорія\tКількість
Яблука\tФрукти\t150
Картопля\tОвочі\t500
```
**Код для читання:**
```python
import csv

with open("data.tsv", "r", encoding="utf-8", newline='') as f:
    # Вказуємо, що розділювач - це символ табуляції
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        print(row)
```

#### Параметри `quotechar` та `quoting`

-   `quotechar`: символ, який використовується для обрамлення полів (за замовчуванням `"`).
-   `quoting`: керує тим, коли `quotechar` буде використовуватись при записі.
    -   `csv.QUOTE_MINIMAL`: тільки для полів, що містять `delimiter` або `quotechar`. (За замовчуванням).
    -   `csv.QUOTE_ALL`: обрамляти всі поля.
    -   `csv.QUOTE_NONNUMERIC`: обрамляти всі нечислові поля.
    -   `csv.QUOTE_NONE`: не обрамляти нічого (видасть помилку, якщо `delimiter` є в даних).

**Приклад запису з `QUOTE_ALL`:**
```python
import csv

data = [['1', 'some text', '12.5']]

with open("quoted.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerows(data)
```
**Результат у `quoted.csv`:**
```csv
"1","some text","12.5"
```
---

### Практичний приклад: обробка табличних даних

**Завдання:** прочитати `cars.csv`, збільшити ціну на 10% для всіх авто, випущених після 2021 року, і записати результат у новий файл `updated_cars.csv`.

```python
import csv

INPUT_FILE = "cars.csv"
OUTPUT_FILE = "updated_cars.csv"

try:
    with open(INPUT_FILE, "r", encoding="utf-8", newline='') as infile, \
         open(OUTPUT_FILE, "w", encoding="utf-8", newline='') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Використовуємо імена полів з оригінального файлу
        fieldnames = reader.fieldnames
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Записуємо заголовок
        writer.writeheader()
        
        print("Обробка даних...")
        
        for row in reader:
            # Створюємо копію рядка для зміни
            updated_row = row.copy()
            
            year = int(row['рік'])
            price = int(row['ціна'])
            
            if year > 2021:
                new_price = int(price * 1.1)
                updated_row['ціна'] = new_price
                print(f"Оновлено ціну для {row['модель']}: {price} -> {new_price}")
            
            writer.writerow(updated_row)

    print(f"\nГотово! Результат збережено у {OUTPUT_FILE}")

except FileNotFoundError:
    print(f"Помилка: вхідний файл {INPUT_FILE} не знайдено.")

```

---
## Висновки

### JSON vs. CSV: що і коли використовувати?

| Характеристика          | JSON                                       | CSV                                              |
| ----------------------- | ------------------------------------------ | ------------------------------------------------ |
| **Структура**           | Ієрархічна (дерево, вкладеність)            | Таблична (плоска, рядки та стовпці)              |
| **Типи даних**          | Підтримує числа, рядки, булеві, масиви, об'єкти, `null` | Все є рядками, потрібна ручна конвертація        |
| **Читабельність**       | Добре читається з відступами (`indent`)    | Легко читається у табличних редакторах (Excel)   |
| **Розмір файлу**        | Більший через синтаксис (дужки, лапки, ключі) | Дуже компактний, мінімум зайвих символів         |
| **Найкраще підходить для** | - Веб-API<br>- Конфігураційні файли<br>- Збереження складних об'єктів | - Експорт/імпорт у бази даних, Excel<br>- Великі набори однотипних даних<br>- Логи |

---
### Підсумки

-   **JSON** ідеальний для збереження даних зі складною, вкладеною структурою та різними типами даних. Модуль `json` робить серіалізацію (`dumps`, `dump`) та десеріалізацію (`loads`, `load`) тривіальною.
-   **CSV** найкраще підходить для великих обсягів табличних (плоских) даних. Модуль `csv` надає надійні інструменти (`reader`, `writer`, `DictReader`, `DictWriter`) для роботи з ними, коректно обробляючи всі нюанси формату.
-   Вибір формату залежить від вашого завдання. Обидва є потужними інструментами в арсеналі Python-розробника.

```