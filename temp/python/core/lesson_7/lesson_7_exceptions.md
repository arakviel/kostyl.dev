# ⚠️ Повний посібник з винятків у Python

## Зміст

### Основи винятків
1. [Вступ до винятків](#вступ-до-винятків)
2. [Навіщо потрібні винятки?](#навіщо-потрібні-винятки)
3. [Що таке помилка (Error)?](#що-таке-помилка-error)
4. [Що таке виняток (Exception)?](#що-таке-виняток-exception)
5. [Різниця між помилками та винятками](#різниця-між-помилками-та-винятками)

### Обробка винятків
6. [Блок try-except: основи](#блок-try-except-основи)
7. [Обробка конкретних винятків](#обробка-конкретних-винятків)
8. [Множинні except блоки](#множинні-except-блоки)
9. [Отримання інформації про виняток](#отримання-інформації-про-виняток)
10. [Блок else](#блок-else)
11. [Блок finally](#блок-finally)
12. [Комбінація try-except-else-finally](#комбінація-try-except-else-finally)

### Типи винятків
13. [Вбудовані винятки Python](#вбудовані-винятки-python)
14. [ZeroDivisionError](#zerodivisionerror)
15. [ValueError](#valueerror)
16. [TypeError](#typeerror)
17. [IndexError та KeyError](#indexerror-та-keyerror)
18. [FileNotFoundError](#filenotfounderror)
19. [AttributeError](#attributeerror)
20. [NameError](#nameerror)
21. [ImportError та ModuleNotFoundError](#importerror-та-modulenotfounderror)

### Генерація винятків
22. [Оператор raise](#оператор-raise)
23. [Raising з повідомленням](#raising-з-повідомленням)
24. [Re-raising винятків](#re-raising-винятків)
25. [Raising в умовах](#raising-в-умовах)

### Власні винятки
26. [Створення власних винятків](#створення-власних-винятків)
27. [Ієрархія винятків](#ієрархія-винятків)
28. [Власні винятки з даними](#власні-винятки-з-даними)
29. [Практичні приклади власних винятків](#практичні-приклади-власних-винятків)

### Спеціальні теми
30. [Assertions](#assertions)
31. [Context managers та винятки](#context-managers-та-винятки)
32. [Traceback](#traceback)
33. [Логування винятків](#логування-винятків)
34. [Exception chaining](#exception-chaining)

### Практика
35. [Практичні приклади](#практичні-приклади)
36. [Поширені помилки](#поширені-помилки)
37. [Найкращі практики](#найкращі-практики)
38. [Коли НЕ використовувати винятки](#коли-не-використовувати-винятки)

---

## Вступ до винятків

### Що таке виняток?

**Виняток (Exception)** — це **подія**, яка виникає під час виконання програми і **перериває** нормальний потік виконання коду.

**Простими словами:** Коли Python зустрічає проблему, яку не може вирішити, він "викидає" (raise) виняток і зупиняє програму (якщо ви не обробите цей виняток).

### Приклад помилки:

```python
# Ділення на нуль
result = 10 / 0
```

**Виведення:**
```
Traceback (most recent call last):
  File "main.py", line 2, in <module>
    result = 10 / 0
ZeroDivisionError: division by zero
```

**Що сталося?**
1. Python спробував виконати `10 / 0`
2. Виявив помилку (ділення на нуль)
3. Створив виняток `ZeroDivisionError`
4. Зупинив програму

### Без обробки винятків:

```python
print("Початок програми")
result = 10 / 0  # ❌ Тут програма впаде
print("Кінець програми")  # Цей рядок не виконається!
```

### З обробкою винятків:

```python
print("Початок програми")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Помилка: не можна ділити на нуль!")

print("Кінець програми")  # ✅ Цей рядок виконається!
```

**Виведення:**
```
Початок програми
Помилка: не можна ділити на нуль!
Кінець програми
```

---

## Навіщо потрібні винятки?

### 1. Уникнути аварійного завершення програми

**Без обробки:**
```python
age = int(input("Вік: "))  # Користувач вводить "abc"
# ValueError! Програма впаде 💥
```

**З обробкою:**
```python
try:
    age = int(input("Вік: "))
except ValueError:
    print("Будь ласка, введіть число!")
    age = 0
```

### 2. Надати корисне повідомлення користувачу

**Погано:**
```python
file = open("data.txt")  # FileNotFoundError: [Errno 2] No such file...
```

**Добре:**
```python
try:
    file = open("data.txt")
except FileNotFoundError:
    print("❌ Файл data.txt не знайдено. Перевірте назву файлу.")
```

### 3. Відновлення після помилки

```python
attempts = 3

for i in range(attempts):
    try:
        age = int(input("Введіть вік: "))
        break  # Успішно ввели - виходимо
    except ValueError:
        print(f"Некоректне значення. Спроба {i+1} з {attempts}")
else:
    print("Вичерпано всі спроби!")
    age = 0
```

### 4. Централізована обробка помилок

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Ділити на нуль не можна!")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Помилка: {e}")
```

### 5. Відокремлення "нормального" коду від обробки помилок

```python
# Без винятків - код переплутаний з перевірками
def process_file(filename):
    if not file_exists(filename):
        return None
    if not has_permission(filename):
        return None
    if not valid_format(filename):
        return None
    return read_file(filename)

# З винятками - чистий основний код
def process_file(filename):
    try:
        return read_file(filename)
    except FileNotFoundError:
        print("Файл не знайдено")
    except PermissionError:
        print("Немає доступу")
    except ValueError:
        print("Невірний формат")
    return None
```

---

## Що таке помилка (Error)?

### Типи помилок в Python:

Python розрізняє три типи помилок:

#### 1. Синтаксичні помилки (Syntax Errors)

**Помилки в синтаксисі коду** — Python не може навіть запустити програму.

```python
# ❌ Забули двокрапку
if x > 5
    print("Більше 5")

# SyntaxError: invalid syntax
```

```python
# ❌ Неправильний відступ
def greet():
print("Привіт!")

# IndentationError: expected an indented block
```

**Синтаксичні помилки НЕ можна обробити try-except!** Їх треба виправляти в коді.

#### 2. Помилки часу виконання (Runtime Errors)

**Помилки, що виникають під час виконання** — ці помилки МОЖНА обробити.

```python
# ❌ Ділення на нуль
result = 10 / 0  # ZeroDivisionError

# ❌ Доступ до неіснуючого індексу
numbers = [1, 2, 3]
print(numbers[10])  # IndexError

# ❌ Перетворення невалідного рядка
age = int("abc")  # ValueError
```

#### 3. Логічні помилки (Logic Errors)

**Програма працює, але результат неправильний** — найскладніші для знаходження.

```python
# Хочемо обчислити середнє
total = 10 + 20 + 30
average = total / 2  # ❌ Помилка: має бути / 3

print(average)  # 30.0 (неправильно, має бути 20.0)
```

**Логічні помилки треба шукати через налагодження (debugging).**

---

## Що таке виняток (Exception)?

### Визначення:

**Exception** — це об'єкт Python, який представляє помилку часу виконання.

### Ієрархія винятків:

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── FloatingPointError
    │   └── OverflowError
    ├── AssertionError
    ├── AttributeError
    ├── BufferError
    ├── EOFError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── MemoryError
    ├── NameError
    │   └── UnboundLocalError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    ├── RuntimeError
    │   └── RecursionError
    ├── TypeError
    ├── ValueError
    └── ... (багато інших)
```

### Базові класи:

- **`BaseException`** — базовий клас для ВСІХ винятків
- **`Exception`** — базовий клас для винятків, які можна обробити
- **`SystemExit`**, **`KeyboardInterrupt`** — спеціальні винятки

**Правило:** Завжди обробляйте `Exception` або його підкласи, а не `BaseException`.

---

## Різниця між помилками та винятками

### Помилки (Errors):

**Критичні проблеми**, які зазвичай НЕ можна обробити:

```python
# SystemError - внутрішня помилка Python
# MemoryError - закінчилась пам'ять
# KeyboardInterrupt - Ctrl+C
```

### Винятки (Exceptions):

**Очікувані проблеми**, які МОЖНА обробити:

```python
# ValueError - невірне значення
# FileNotFoundError - файл не знайдено
# ZeroDivisionError - ділення на нуль
```

### Таблиця порівняння:

| Критерій       | Помилки (Errors)      | Винятки (Exceptions)    |
|----------------|-----------------------|-------------------------|
| Обробка        | ❌ Зазвичай ні        | ✅ Так                  |
| Відновлення    | ❌ Складно/неможливо  | ✅ Можливо              |
| Приклади       | MemoryError, SystemError | ValueError, TypeError |
| Частота        | Рідко                 | Часто                   |

---

## Блок try-except: основи

### Синтаксис:

```python
try:
    # Код, який може викликати виняток
    # ...
except:
    # Код, який виконається, якщо виникне виняток
    # ...
```

### Схема роботи:

```
┌──────────────┐
│  try блок    │
└──────┬───────┘
       │
       ▼
  Виняток?
       │
   ┌───┴───┐
   │       │
  Так     Ні
   │       │
   ▼       │
┌──────┐   │
│except│   │
└──┬───┘   │
   │       │
   └───┬───┘
       │
       ▼
   Продовж
```

### Простий приклад:

```python
try:
    number = int(input("Введіть число: "))
    print(f"Ви ввели: {number}")
except:
    print("Це не число!")
```

**Тестування:**

```
Введіть число: 42
Ви ввели: 42

Введіть число: abc
Це не число!
```

### Що відбувається:

1. Python **спробує** виконати код в блоці `try`
2. Якщо виникне **будь-який** виняток — перейде до блоку `except`
3. Якщо винятку **немає** — блок `except` пропускається

### Приклад з діленням:

```python
try:
    a = 10
    b = 0
    result = a / b
    print(f"Результат: {result}")
except:
    print("Сталася помилка!")

print("Програма продовжує працювати")
```

**Виведення:**
```
Сталася помилка!
Програма продовжує працювати
```

### Без try-except:

```python
a = 10
b = 0
result = a / b  # ❌ ZeroDivisionError! Програма впаде
print(f"Результат: {result}")  # Не виконається
```

**Виведення:**
```
Traceback (most recent call last):
  File "main.py", line 3, in <module>
    result = a / b
ZeroDivisionError: division by zero
```

---

## Обробка конкретних винятків

### Навіщо вказувати конкретний виняток?

**Погано (ловить все):**
```python
try:
    age = int(input("Вік: "))
except:
    print("Помилка!")  # Яка саме?
```

**Добре (ловить конкретний виняток):**
```python
try:
    age = int(input("Вік: "))
except ValueError:
    print("Помилка: введіть число, а не текст!")
```

### Синтаксис:

```python
try:
    # код
except НазваВинятку:
    # обробка
```

### Приклади:

#### ValueError:

```python
try:
    age = int("abc")  # Не можна перетворити "abc" в число
except ValueError:
    print("Не можна перетворити в число!")
```

#### ZeroDivisionError:

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Ділити на нуль не можна!")
```

#### IndexError:

```python
try:
    numbers = [1, 2, 3]
    print(numbers[10])  # Індекс 10 не існує
except IndexError:
    print("Індекс поза межами списку!")
```

#### KeyError:

```python
try:
    person = {"name": "Іван", "age": 25}
    print(person["email"])  # Ключ "email" не існує
except KeyError:
    print("Ключ не знайдено у словнику!")
```

### Чому це краще?

1. **Точність** — знаємо, яка саме помилка
2. **Корисні повідомлення** — можемо пояснити користувачу
3. **Не ховає інші помилки** — інші винятки не будуть заглушені

---

## Множинні except блоки

### Обробка різних винятків по-різному:

```python
try:
    # Код, який може викликати різні винятки
    age = int(input("Вік: "))
    result = 100 / age
    print(f"Результат: {result}")
except ValueError:
    print("❌ Помилка: введіть число!")
except ZeroDivisionError:
    print("❌ Помилка: вік не може бути нулем!")
```

### Тестування:

```
# Тест 1: введемо "abc"
Вік: abc
❌ Помилка: введіть число!

# Тест 2: введемо 0
Вік: 0
❌ Помилка: вік не може бути нулем!

# Тест 3: введемо 25
Вік: 25
Результат: 4.0
```

### Порядок except блоків:

**ВАЖЛИВО:** Від **конкретного** до **загального**!

```python
# ✅ Правильно (від конкретного до загального)
try:
    # код
except ValueError:
    print("ValueError")
except TypeError:
    print("TypeError")
except Exception:
    print("Інша помилка")

# ❌ Неправильно (загальний перший)
try:
    # код
except Exception:  # Спіймає ВСЕ! Наступні блоки ніколи не спрацюють
    print("Помилка")
except ValueError:  # ❌ Unreachable code!
    print("ValueError")
```

### Обробка кількох винятків в одному except:

```python
try:
    # код
except (ValueError, TypeError):
    print("ValueError або TypeError")
```

**Приклад:**

```python
def process_number(value):
    try:
        number = int(value)
        result = 100 / number
        return result
    except (ValueError, TypeError):
        print("Помилка типу або значення")
        return None
    except ZeroDivisionError:
        print("Ділення на нуль")
        return None

print(process_number("abc"))   # Помилка типу або значення → None
print(process_number(0))       # Ділення на нуль → None
print(process_number(10))      # 10.0
```

---

## Отримання інформації про виняток

### Використання `as`:

```python
try:
    age = int("abc")
except ValueError as e:
    print(f"Помилка: {e}")
    print(f"Тип: {type(e)}")
```

**Виведення:**
```
Помилка: invalid literal for int() with base 10: 'abc'
Тип: <class 'ValueError'>
```

### Практичні приклади:

#### Файли:

```python
try:
    file = open("missing.txt", "r")
except FileNotFoundError as e:
    print(f"❌ Файл не знайдено: {e.filename}")
```

#### Словники:

```python
person = {"name": "Іван"}

try:
    email = person["email"]
except KeyError as e:
    print(f"❌ Ключ {e} не існує")
```

#### Списки:

```python
numbers = [1, 2, 3]

try:
    value = numbers[10]
except IndexError as e:
    print(f"❌ Помилка індексу: {e}")
```

### Отримання деталей винятку:

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Повідомлення: {e}")
    print(f"Тип: {type(e).__name__}")
    print(f"Args: {e.args}")
```

**Виведення:**
```
Повідомлення: division by zero
Тип: ZeroDivisionError
Args: ('division by zero',)
```

---

## Блок else

### Що таке else в try-except?

**`else`** — блок, який виконується **тільки якщо НЕ було винятку** в блоці `try`.

### Синтаксис:

```python
try:
    # Код, який може викликати виняток
except НазваВинятку:
    # Обробка винятку
else:
    # Виконається ТІЛЬКИ якщо не було винятку
```

### Приклад:

```python
try:
    age = int(input("Вік: "))
except ValueError:
    print("Некоректне значення!")
else:
    print(f"✅ Вік прийнято: {age}")
    print("Дані збережено")
```

**Тестування:**

```
# Тест 1: введемо "abc"
Вік: abc
Некоректне значення!

# Тест 2: введемо 25
Вік: 25
✅ Вік прийнято: 25
Дані збережено
```

### Навіщо потрібен else?

**Без else:**
```python
try:
    age = int(input("Вік: "))
    print(f"✅ Вік прийнято: {age}")  # ❌ Виконається і при винятку!
except ValueError:
    print("Некоректне значення!")
```

**З else:**
```python
try:
    age = int(input("Вік: "))
except ValueError:
    print("Некоректне значення!")
else:
    print(f"✅ Вік прийнято: {age}")  # ✅ Тільки якщо все ОК
```

### Практичний приклад: читання файлу

```python
try:
    file = open("data.txt", "r")
except FileNotFoundError:
    print("❌ Файл не знайдено")
else:
    # Файл успішно відкрито
    content = file.read()
    print(f"✅ Прочитано {len(content)} символів")
    file.close()
```

### Відмінність else від коду після try:

```python
# Варіант 1: Код після try
try:
    age = int(input("Вік: "))
except ValueError:
    print("Помилка!")
print("Цей код виконається ЗАВЖДИ")

# Варіант 2: else
try:
    age = int(input("Вік: "))
except ValueError:
    print("Помилка!")
else:
    print("Цей код ТІЛЬКИ якщо немає винятку")
```

---

## Блок finally

### Що таке finally?

**`finally`** — блок, який виконується **ЗАВЖДИ**, незалежно від того, був виняток чи ні.

### Синтаксис:

```python
try:
    # Код
except НазваВинятку:
    # Обробка
finally:
    # Виконається ЗАВЖДИ
```

### Схема роботи:

```
try блок
   │
   ├─ Виняток? → except блок
   │              │
   └──────────────┴─→ finally блок (ЗАВЖДИ)
```

### Приклад:

```python
try:
    number = int(input("Число: "))
    result = 100 / number
    print(f"Результат: {result}")
except ValueError:
    print("❌ Не число")
except ZeroDivisionError:
    print("❌ Нуль")
finally:
    print("🔒 Блок finally завжди виконується")
```

**Тестування:**

```
# Тест 1: введемо "abc"
Число: abc
❌ Не число
🔒 Блок finally завжди виконується

# Тест 2: введемо 0
Число: 0
❌ Нуль
🔒 Блок finally завжди виконується

# Тест 3: введемо 10
Число: 10
Результат: 10.0
🔒 Блок finally завжди виконується
```

### Навіщо потрібен finally?

**Основне призначення:** Звільнення ресурсів (файли, з'єднання, блокування).

#### Приклад: робота з файлом

**Без finally (небезпечно):**
```python
try:
    file = open("data.txt", "r")
    content = file.read()
    # Якщо тут виникне виняток, файл не закриється!
    result = int(content)
except ValueError:
    print("Помилка читання")
# ❌ file.close() не буде викликано при винятку!
```

**З finally (безпечно):**
```python
file = None
try:
    file = open("data.txt", "r")
    content = file.read()
    result = int(content)
except FileNotFoundError:
    print("❌ Файл не знайдено")
except ValueError:
    print("❌ Невірний формат")
finally:
    if file:
        file.close()  # ✅ Файл завжди закриється
        print("🔒 Файл закрито")
```

### finally виконується навіть при return:

```python
def test():
    try:
        print("1. Try блок")
        return "Повертаємо значення"
    finally:
        print("2. Finally блок")  # ✅ Виконається перед return!

result = test()
print(f"3. Результат: {result}")
```

**Виведення:**
```
1. Try блок
2. Finally блок
3. Результат: Повертаємо значення
```

### finally виконується навіть при break/continue:

```python
for i in range(3):
    try:
        print(f"Ітерація {i}")
        if i == 1:
            break
    finally:
        print(f"Finally для ітерації {i}")
```

**Виведення:**
```
Ітерація 0
Finally для ітерації 0
Ітерація 1
Finally для ітерації 1
```

---

## Комбінація try-except-else-finally

### Повна форма:

```python
try:
    # Код, який може викликати виняток
except НазваВинятку:
    # Обробка винятку
else:
    # Якщо НЕ було винятку
finally:
    # Завжди виконується
```

### Порядок виконання:

```
1. try блок
   ├─ Виняток?
   │  ├─ Так → except блок → finally блок
   │  └─ Ні  → else блок → finally блок
   └─ finally блок (ЗАВЖДИ)
```

### Повний приклад:

```python
def divide_numbers(a, b):
    print("=" * 40)
    print(f"Ділимо {a} на {b}")
    
    try:
        result = a / b
    except ZeroDivisionError:
        print("❌ Помилка: ділення на нуль")
        return None
    except TypeError:
        print("❌ Помилка: неправильний тип")
        return None
    else:
        print(f"✅ Успішно: результат = {result}")
        return result
    finally:
        print("🔒 Обчислення завершено")

# Тестування
divide_numbers(10, 2)
divide_numbers(10, 0)
divide_numbers("10", 2)
```

**Виведення:**
```
========================================
Ділимо 10 на 2
✅ Успішно: результат = 5.0
🔒 Обчислення завершено
========================================
Ділимо 10 на 0
❌ Помилка: ділення на нуль
🔒 Обчислення завершено
========================================
Ділимо 10 на 2
❌ Помилка: неправильний тип
🔒 Обчислення завершено
```

### Практичний приклад: робота з базою даних

```python
def update_database(data):
    connection = None
    
    try:
        # Підключення до БД
        connection = connect_to_db()
        print("✅ Підключено до бази даних")
        
        # Оновлення даних
        connection.update(data)
        print("✅ Дані оновлено")
        
    except ConnectionError:
        print("❌ Помилка підключення до БД")
    except ValueError:
        print("❌ Невірні дані")
    else:
        # Якщо все ОК - commit
        connection.commit()
        print("✅ Зміни збережено")
    finally:
        # Завжди закриваємо з'єднання
        if connection:
            connection.close()
            print("🔒 З'єднання закрито")
```

---

## Вбудовані винятки Python

### Найпоширеніші винятки:

| Виняток                  | Коли виникає                                    |
|--------------------------|-------------------------------------------------|
| `ValueError`             | Невірне значення                                |
| `TypeError`              | Невірний тип                                    |
| `ZeroDivisionError`      | Ділення на нуль                                 |
| `IndexError`             | Індекс поза межами                              |
| `KeyError`               | Ключ не знайдено у словнику                     |
| `FileNotFoundError`      | Файл не знайдено                                |
| `AttributeError`         | Атрибут не існує                                |
| `NameError`              | Змінна не визначена                             |
| `ImportError`            | Помилка імпорту модуля                          |
| `ModuleNotFoundError`    | Модуль не знайдено                              |
| `RuntimeError`           | Загальна помилка виконання                      |
| `RecursionError`         | Перевищено ліміт рекурсії                       |
| `MemoryError`            | Недостатньо пам'яті                             |
| `OverflowError`          | Результат занадто великий                       |
| `AssertionError`         | assert не виконався                             |
| `StopIteration`          | Ітератор закінчився                             |
| `KeyboardInterrupt`      | Ctrl+C                                          |
| `SystemExit`             | sys.exit()                                      |

### Повна ієрархія:

```python
# Вивести всі вбудовані винятки
import builtins

exceptions = [name for name in dir(builtins) if name.endswith('Error') or name.endswith('Exception')]
for exc in sorted(exceptions):
    print(exc)
```

---

## ZeroDivisionError

### Коли виникає?

Ділення або ділення з остачею на **нуль**.

### Приклади:

```python
# Звичайне ділення
result = 10 / 0  # ❌ ZeroDivisionError

# Цілочисельне ділення
result = 10 // 0  # ❌ ZeroDivisionError

# Остача від ділення
result = 10 % 0  # ❌ ZeroDivisionError

# Divmod
result = divmod(10, 0)  # ❌ ZeroDivisionError
```

### Обробка:

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("❌ Ділити на нуль не можна!")
        return None

print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # ❌ Ділити на нуль не можна! → None
```

### Альтернатива (без винятків):

```python
def safe_divide(a, b):
    if b == 0:
        print("❌ Ділити на нуль не можна!")
        return None
    return a / b
```

**Що краще?** Залежить від ситуації:
- Якщо нуль **рідкісний** → винятки
- Якщо нуль **частий** → перевірка if

---

## ValueError

### Коли виникає?

Операція отримує **правильний тип**, але **неправильне значення**.

### Приклади:

#### int() з невалідним рядком:

```python
age = int("abc")  # ❌ ValueError: invalid literal for int()
```

#### float() з невалідним рядком:

```python
price = float("12.34.56")  # ❌ ValueError: could not convert string
```

#### Пошук в списку неіснуючого елемента:

```python
numbers = [1, 2, 3]
index = numbers.index(10)  # ❌ ValueError: 10 is not in list
```

#### Розпакування з неправильною кількістю значень:

```python
a, b = [1, 2, 3]  # ❌ ValueError: too many values to unpack
```

#### Конвертація з невалідної системи числення:

```python
number = int("1A", 2)  # ❌ ValueError: invalid literal for int() with base 2
```

### Обробка:

```python
def get_age():
    while True:
        try:
            age = int(input("Вік: "))
            if age < 0 or age > 150:
                raise ValueError("Вік має бути від 0 до 150")
            return age
        except ValueError as e:
            print(f"❌ Помилка: {e}")
            print("Спробуйте ще раз")

age = get_age()
print(f"✅ Вік: {age}")
```

---

## TypeError

### Коли виникає?

Операція застосована до **неправильного типу**.

### Приклади:

#### Неможливі операції:

```python
result = "5" + 10  # ❌ TypeError: can only concatenate str to str
```

```python
result = len(123)  # ❌ TypeError: object of type 'int' has no len()
```

#### Неправильна кількість аргументів:

```python
def greet(name):
    print(f"Привіт, {name}!")

greet()  # ❌ TypeError: missing 1 required positional argument
greet("Іван", "Петро")  # ❌ TypeError: takes 1 positional argument but 2 were given
```

#### Неможливі операції з типами:

```python
numbers = [1, 2, 3]
numbers[0] = "text"  # ✅ Працює для списків

numbers = (1, 2, 3)
numbers[0] = "text"  # ❌ TypeError: 'tuple' object does not support item assignment
```

#### None не є ітерованим:

```python
for item in None:  # ❌ TypeError: 'NoneType' object is not iterable
    print(item)
```

### Обробка:

```python
def add_values(a, b):
    try:
        return a + b
    except TypeError:
        print(f"❌ Не можна додати {type(a).__name__} і {type(b).__name__}")
        return None

print(add_values(5, 10))      # 15
print(add_values("5", "10"))  # "510"
print(add_values("5", 10))    # ❌ Не можна додати str і int → None
```

---

## IndexError та KeyError

### IndexError - індекс поза межами

#### Коли виникає?

Доступ до **неіснуючого індексу** списку, кортежу або рядка.

```python
numbers = [1, 2, 3]
print(numbers[10])  # ❌ IndexError: list index out of range

text = "Python"
print(text[100])  # ❌ IndexError: string index out of range
```

#### Обробка:

```python
def safe_get(lst, index):
    try:
        return lst[index]
    except IndexError:
        print(f"❌ Індекс {index} не існує (розмір списку: {len(lst)})")
        return None

numbers = [10, 20, 30]
print(safe_get(numbers, 1))   # 20
print(safe_get(numbers, 10))  # ❌ Індекс 10 не існує → None
```

#### Альтернатива:

```python
def safe_get(lst, index):
    if 0 <= index < len(lst):
        return lst[index]
    return None
```

### KeyError - ключ не знайдено

#### Коли виникає?

Доступ до **неіснуючого ключа** словника.

```python
person = {"name": "Іван", "age": 25}
print(person["email"])  # ❌ KeyError: 'email'
```

#### Обробка:

```python
person = {"name": "Іван", "age": 25}

# Варіант 1: try-except
try:
    email = person["email"]
except KeyError:
    email = "не вказано"

# Варіант 2: get() (КРАЩЕ!)
email = person.get("email", "не вказано")
```

#### Практичний приклад:

```python
def get_user_info(user_id):
    users = {
        1: {"name": "Іван", "age": 25},
        2: {"name": "Марія", "age": 30}
    }
    
    try:
        return users[user_id]
    except KeyError:
        print(f"❌ Користувач з ID {user_id} не знайдено")
        return None

print(get_user_info(1))   # {'name': 'Іван', 'age': 25}
print(get_user_info(999)) # ❌ Користувач з ID 999 не знайдено → None
```

---

## FileNotFoundError

### Коли виникає?

Спроба відкрити **неіснуючий файл** для читання.

### Приклади:

```python
# Читання неіснуючого файлу
file = open("missing.txt", "r")  # ❌ FileNotFoundError

# Видалення неіснуючого файлу
import os
os.remove("missing.txt")  # ❌ FileNotFoundError
```

### Обробка:

```python
def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"❌ Файл '{filename}' не знайдено")
        return None

content = read_file("data.txt")
if content:
    print(content)
```

### Створення файлу, якщо не існує:

```python
import os

def read_or_create(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"📝 Файл '{filename}' не знайдено, створюємо новий")
        with open(filename, "w") as file:
            file.write("Початковий вміст\n")
        return "Початковий вміст\n"

content = read_or_create("log.txt")
print(content)
```

### Перевірка існування файлу:

```python
import os

def safe_read(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read()
    else:
        print(f"❌ Файл '{filename}' не існує")
        return None
```

---

## AttributeError

### Коли виникає?

Спроба отримати **неіснуючий атрибут** або метод об'єкта.

### Приклади:

```python
# Неіснуючий метод
text = "Python"
text.append("!")  # ❌ AttributeError: 'str' object has no attribute 'append'

# Неіснуючий атрибут
numbers = [1, 2, 3]
print(numbers.size)  # ❌ AttributeError: 'list' object has no attribute 'size'

# None не має методів
result = None
result.upper()  # ❌ AttributeError: 'NoneType' object has no attribute 'upper'
```

### Обробка:

```python
def safe_upper(value):
    try:
        return value.upper()
    except AttributeError:
        print(f"❌ {type(value).__name__} не має методу upper()")
        return value

print(safe_upper("python"))  # PYTHON
print(safe_upper(123))       # ❌ int не має методу upper() → 123
print(safe_upper(None))      # ❌ NoneType не має методу upper() → None
```

### Перевірка наявності атрибута:

```python
# hasattr() - перевірити наявність атрибута
text = "Python"

if hasattr(text, "upper"):
    print(text.upper())  # PYTHON
else:
    print("Метод upper() не існує")

# getattr() - отримати атрибут зі значенням за замовчуванням
value = getattr(text, "size", 0)  # Якщо немає "size", поверне 0
```

---

## NameError

### Коли виникає?

Використання **неоголошеної змінної** або імені.

### Приклади:

```python
print(unknown_variable)  # ❌ NameError: name 'unknown_variable' is not defined

result = x + 10  # ❌ NameError: name 'x' is not defined

# Друкарська помилка
name = "Іван"
print(nane)  # ❌ NameError: name 'nane' is not defined
```

### Обробка (рідко потрібна):

```python
try:
    print(some_variable)
except NameError:
    print("❌ Змінна не визначена")
    some_variable = "значення за замовчуванням"
    print(some_variable)
```

**Зазвичай NameError краще виправити в коді, а не обробляти!**

### Перевірка наявності змінної:

```python
# globals() - всі глобальні змінні
if "my_var" in globals():
    print(my_var)
else:
    print("Змінна my_var не визначена")

# locals() - всі локальні змінні
def func():
    x = 10
    if "x" in locals():
        print(x)
```

---

## ImportError та ModuleNotFoundError

### ModuleNotFoundError - модуль не знайдено

#### Коли виникає?

Спроба імпортувати **неіснуючий модуль**.

```python
import non_existent_module  # ❌ ModuleNotFoundError: No module named 'non_existent_module'

from math import non_existent_function  # ❌ ImportError: cannot import name
```

#### Обробка:

```python
try:
    import numpy as np
    print("✅ NumPy встановлено")
except ModuleNotFoundError:
    print("❌ NumPy не встановлено. Встановіть: pip install numpy")
    np = None

# Використання
if np:
    array = np.array([1, 2, 3])
else:
    array = [1, 2, 3]
```

### ImportError - помилка імпорту

#### Коли виникає?

Модуль існує, але **не можна імпортувати** певне ім'я.

```python
from math import non_existent  # ❌ ImportError: cannot import name 'non_existent'
```

#### Обробка:

```python
try:
    from collections import OrderedDict
    print("✅ OrderedDict доступний")
except ImportError:
    print("❌ OrderedDict недоступний, використовуємо dict")
    OrderedDict = dict
```

### Практичний приклад: опціональні залежності

```python
# JSON завжди є
import json

# Спроба імпортувати швидший модуль
try:
    import ujson as json_parser
    print("✅ Використовуємо ujson (швидкий)")
except ModuleNotFoundError:
    json_parser = json
    print("ℹ️ Використовуємо json (стандартний)")

# Використання
data = json_parser.loads('{"name": "Іван"}')
```

---

## Оператор raise

### Що таке raise?

**`raise`** — це оператор, який **викидає** (створює) виняток вручну.

### Синтаксис:

```python
raise НазваВинятку("повідомлення")
```

### Базовий приклад:

```python
age = -5

if age < 0:
    raise ValueError("Вік не може бути від'ємним!")

print(f"Вік: {age}")  # Не виконається
```

**Виведення:**
```
ValueError: Вік не може бути від'ємним!
```

### Коли використовувати raise?

1. **Валідація вхідних даних**
2. **Неможливі стани програми**
3. **Бізнес-логіка**

### Приклад: валідація функції

```python
def divide(a, b):
    if not isinstance(a, (int, float)):
        raise TypeError("a має бути числом")
    if not isinstance(b, (int, float)):
        raise TypeError("b має бути числом")
    if b == 0:
        raise ValueError("b не може бути нулем")
    
    return a / b

# Використання
try:
    result = divide(10, 2)
    print(result)  # 5.0
    
    result = divide(10, 0)  # ❌ ValueError
except (TypeError, ValueError) as e:
    print(f"Помилка: {e}")
```

---

## Raising з повідомленням

### Повідомлення винятку:

```python
raise ValueError("Детальний опис помилки")
```

### Корисні повідомлення:

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"Вік не може бути від'ємним: отримано {age}")
    if age > 150:
        raise ValueError(f"Вік занадто великий: отримано {age} (максимум 150)")
    
    return age

# Тестування
try:
    set_age(-5)
except ValueError as e:
    print(f"❌ {e}")  # ❌ Вік не може бути від'ємним: отримано -5
```

### Багато деталей:

```python
def process_payment(amount, account):
    if amount <= 0:
        raise ValueError(
            f"Сума має бути додатною. "
            f"Отримано: {amount}, рахунок: {account}"
        )
    
    # Обробка платежу
    pass
```

---

## Re-raising винятків

### Що таке re-raise?

**Перевикидання** винятку після його обробки.

### Синтаксис:

```python
try:
    # код
except СomeException as e:
    # Логування або часткова обробка
    print(f"Виняток: {e}")
    raise  # Перевикинути той самий виняток
```

### Приклад: логування та перевикидання

```python
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        print(f"📝 Лог: Спроба ділення на нуль")
        raise  # Перевикинути виняток далі

# Використання
try:
    result = divide(10, 0)
except ZeroDivisionError:
    print("❌ Обробка помилки на вищому рівні")
```

**Виведення:**
```
📝 Лог: Спроба ділення на нуль
❌ Обробка помилки на вищому рівні
```

### Зміна типу винятку:

```python
def read_config(filename):
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        # Перетворюємо на інший тип винятку
        raise ValueError(f"Конфігураційний файл '{filename}' не знайдено")

# Використання
try:
    config = read_config("config.ini")
except ValueError as e:
    print(f"❌ {e}")
```

---

## Raising в умовах

### Валідація параметрів:

```python
def create_user(name, age, email):
    if not name:
        raise ValueError("Ім'я не може бути порожнім")
    
    if not isinstance(age, int):
        raise TypeError("Вік має бути цілим числом")
    
    if age < 18:
        raise ValueError("Користувач має бути повнолітнім (18+)")
    
    if "@" not in email:
        raise ValueError("Невірний формат email")
    
    return {"name": name, "age": age, "email": email}

# Тестування
try:
    user = create_user("Іван", 25, "ivan@example.com")
    print("✅ Користувач створений:", user)
    
    user = create_user("", 25, "ivan@example.com")
except ValueError as e:
    print(f"❌ {e}")
```

### Бізнес-логіка:

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сума має бути додатною")
        
        if amount > self.balance:
            raise ValueError(
                f"Недостатньо коштів. "
                f"Баланс: {self.balance}, запитано: {amount}"
            )
        
        self.balance -= amount
        return self.balance

# Використання
account = BankAccount(1000)

try:
    account.withdraw(500)
    print(f"✅ Баланс: {account.balance}")  # 500
    
    account.withdraw(700)  # ❌ Недостатньо
except ValueError as e:
    print(f"❌ {e}")
```

---

## Створення власних винятків

### Навіщо потрібні власні винятки?

1. **Специфічна логіка додатку**
2. **Краща категоризація помилок**
3. **Додаткові дані у винятку**

### Базовий синтаксис:

```python
class MyException(Exception):
    pass
```

### Простий приклад:

```python
class NegativeNumberError(Exception):
    """Виняток для від'ємних чисел"""
    pass

def square_root(number):
    if number < 0:
        raise NegativeNumberError("Не можна обчислити корінь від від'ємного числа")
    return number ** 0.5

# Використання
try:
    result = square_root(-4)
except NegativeNumberError as e:
    print(f"❌ {e}")
```

### З повідомленням за замовчуванням:

```python
class InvalidAgeError(Exception):
    """Виняток для невірного віку"""
    def __init__(self, age):
        self.age = age
        super().__init__(f"Невірний вік: {age}")

def set_age(age):
    if age < 0 or age > 150:
        raise InvalidAgeError(age)
    return age

# Використання
try:
    set_age(-5)
except InvalidAgeError as e:
    print(f"❌ {e}")  # ❌ Невірний вік: -5
```

---

## Ієрархія винятків

### Створення ієрархії:

```python
# Базовий виняток для всього додатку
class AppError(Exception):
    """Базовий виняток додатку"""
    pass

# Специфічні винятки
class ValidationError(AppError):
    """Помилка валідації"""
    pass

class DatabaseError(AppError):
    """Помилка бази даних"""
    pass

class AuthenticationError(AppError):
    """Помилка автентифікації"""
    pass

# Використання
try:
    raise ValidationError("Невірні дані")
except AppError as e:
    # Спіймає будь-який виняток додатку
    print(f"Помилка: {e}")
```

### Переваги ієрархії:

```python
# Можна ловити загальний виняток
try:
    # Різні операції
    raise ValidationError("...")
except AppError:
    print("Будь-яка помилка додатку")

# Або конкретний
try:
    # Операція
    raise ValidationError("...")
except ValidationError:
    print("Конкретно помилка валідації")
```

### Практичний приклад:

```python
class APIError(Exception):
    """Базова помилка API"""
    pass

class ConnectionError(APIError):
    """Помилка з'єднання"""
    pass

class TimeoutError(APIError):
    """Таймаут"""
    pass

class AuthError(APIError):
    """Помилка автентифікації"""
    pass

def call_api(url):
    # Симуляція різних помилок
    if "invalid" in url:
        raise AuthError("Невірний токен")
    if "slow" in url:
        raise TimeoutError("Перевищено час очікування")
    return {"status": "ok"}

# Використання
try:
    response = call_api("https://api.example.com/invalid")
except AuthError:
    print("❌ Проблема з автентифікацією")
except TimeoutError:
    print("❌ Занадто довго чекали")
except APIError:
    print("❌ Інша API помилка")
```

---

## Власні винятки з даними

### Додавання додаткових даних:

```python
class InsufficientFundsError(Exception):
    """Недостатньо коштів на рахунку"""
    
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.shortage = amount - balance
        
        message = (
            f"Недостатньо коштів. "
            f"Баланс: {balance}, потрібно: {amount}, "
            f"не вистачає: {self.shortage}"
        )
        super().__init__(message)

# Використання
try:
    balance = 100
    amount = 150
    
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
        
except InsufficientFundsError as e:
    print(f"❌ {e}")
    print(f"Баланс: {e.balance}")
    print(f"Запит: {e.amount}")
    print(f"Не вистачає: {e.shortage}")
```

**Виведення:**
```
❌ Недостатньо коштів. Баланс: 100, потрібно: 150, не вистачає: 50
Баланс: 100
Запит: 150
Не вистачає: 50
```

### Виняток з контекстом:

```python
class ValidationError(Exception):
    """Помилка валідації з деталями"""
    
    def __init__(self, field, value, reason):
        self.field = field
        self.value = value
        self.reason = reason
        
        message = f"Поле '{field}' має невірне значення '{value}': {reason}"
        super().__init__(message)

# Використання
def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError("age", age, "має бути цілим числом")
    if age < 0:
        raise ValidationError("age", age, "не може бути від'ємним")
    if age > 150:
        raise ValidationError("age", age, "занадто великий")

try:
    validate_age("25")
except ValidationError as e:
    print(f"❌ {e}")
    print(f"Поле: {e.field}")
    print(f"Значення: {e.value}")
```

---

## Практичні приклади власних винятків

### Приклад 1: E-commerce система

```python
class CartError(Exception):
    """Базова помилка кошика"""
    pass

class ItemNotFoundError(CartError):
    """Товар не знайдено"""
    def __init__(self, item_id):
        self.item_id = item_id
        super().__init__(f"Товар з ID {item_id} не знайдено")

class OutOfStockError(CartError):
    """Товар закінчився"""
    def __init__(self, item_name, requested, available):
        self.item_name = item_name
        self.requested = requested
        self.available = available
        super().__init__(
            f"Товар '{item_name}': запитано {requested}, "
            f"доступно лише {available}"
        )

class InvalidQuantityError(CartError):
    """Невірна кількість"""
    pass

# Використання
class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.stock = {"яблуко": 10, "банан": 5}
    
    def add_item(self, item_name, quantity):
        if quantity <= 0:
            raise InvalidQuantityError("Кількість має бути додатною")
        
        if item_name not in self.stock:
            raise ItemNotFoundError(item_name)
        
        if quantity > self.stock[item_name]:
            raise OutOfStockError(
                item_name, 
                quantity, 
                self.stock[item_name]
            )
        
        self.items[item_name] = quantity
        print(f"✅ Додано {quantity} x {item_name}")

# Тестування
cart = ShoppingCart()

try:
    cart.add_item("яблуко", 5)
    cart.add_item("банан", 10)  # Більше ніж є
except OutOfStockError as e:
    print(f"❌ {e}")
    print(f"Доступно: {e.available}")
```

### Приклад 2: Файлова система

```python
class FileSystemError(Exception):
    """Базова помилка файлової системи"""
    pass

class FileEmptyError(FileSystemError):
    """Файл порожній"""
    def __init__(self, filename):
        super().__init__(f"Файл '{filename}' порожній")

class InvalidFormatError(FileSystemError):
    """Невірний формат"""
    def __init__(self, filename, expected, actual):
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"Файл '{filename}': очікується {expected}, "
            f"отримано {actual}"
        )

def read_config(filename):
    try:
        with open(filename, "r") as file:
            content = file.read().strip()
            
            if not content:
                raise FileEmptyError(filename)
            
            if not content.startswith("[CONFIG]"):
                raise InvalidFormatError(
                    filename, 
                    "[CONFIG] header", 
                    content[:20]
                )
            
            return content
            
    except FileNotFoundError:
        raise FileSystemError(f"Файл '{filename}' не знайдено")

# Використання
try:
    config = read_config("settings.ini")
except FileSystemError as e:
    print(f"❌ Помилка: {e}")
```

---

## Assertions

### Що таке assertion?

**Assertion** — це твердження, яке має бути істинним. Якщо ні — викидається `AssertionError`.

### Синтаксис:

```python
assert умова, "повідомлення"
```

### Базовий приклад:

```python
age = 150

assert age >= 0, "Вік не може бути від'ємним"
assert age <= 120, f"Вік занадто великий: {age}"

print("Всі перевірки пройдено")
```

### Коли використовувати assertions?

**Assertions для:**
- Перевірки внутрішньої логіки (debugging)
- Умов, які "ніколи не повинні" трапитись
- Розробки та тестування

**НЕ для:**
- Валідації вводу користувача
- Обробки помилок у production коді

### Приклади:

#### Перевірка типів:

```python
def divide(a, b):
    assert isinstance(a, (int, float)), "a має бути числом"
    assert isinstance(b, (int, float)), "b має бути числом"
    assert b != 0, "b не може бути нулем"
    
    return a / b
```

#### Перевірка стану:

```python
class BankAccount:
    def __init__(self, balance):
        assert balance >= 0, "Початковий баланс не може бути від'ємним"
        self.balance = balance
    
    def withdraw(self, amount):
        assert amount > 0, "Сума має бути додатною"
        assert amount <= self.balance, "Недостатньо коштів"
        
        self.balance -= amount
```

### Вимкнення assertions:

**Assertions можна вимкнути** флагом `-O` (оптимізація):

```bash
python -O script.py
```

Тому **не використовуйте** assertions для критичної валідації!

```python
# ❌ Погано (можна вимкнути)
assert user_age >= 18, "Має бути 18+"

# ✅ Добре (завжди працює)
if user_age < 18:
    raise ValueError("Має бути 18+")
```

---

## Context managers та винятки

### Що таке context manager?

**Context manager** — об'єкт, який керує ресурсами (файли, з'єднання тощо).

### Синтаксис:

```python
with вираз as змінна:
    # Використання ресурсу
```

### Переваги:

Ресурс **завжди звільняється**, навіть якщо виникне виняток.

### Приклад: файли

**Без with:**
```python
file = open("data.txt", "r")
try:
    content = file.read()
finally:
    file.close()  # Треба не забути!
```

**З with:**
```python
with open("data.txt", "r") as file:
    content = file.read()
# Файл автоматично закритий
```

### Винятки в with:

```python
try:
    with open("data.txt", "r") as file:
        content = file.read()
        # Якщо тут виняток - файл все одно закриється!
        result = int(content)
except FileNotFoundError:
    print("❌ Файл не знайдено")
except ValueError:
    print("❌ Невірний формат")
```

### Множинні context managers:

```python
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        outfile.write(line.upper())
```

### Створення власного context manager:

```python
class DatabaseConnection:
    def __enter__(self):
        print("🔌 Підключення до БД")
        self.connection = "connection_object"
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("🔒 Закриття з'єднання")
        # exc_type - тип винятку (None якщо немає)
        # exc_value - сам виняток
        # traceback - traceback об'єкт
        
        if exc_type is not None:
            print(f"⚠️ Виникла помилка: {exc_value}")
        
        return False  # False = виняток буде піднято далі

# Використання
try:
    with DatabaseConnection() as conn:
        print(f"📝 Працюємо з {conn}")
        raise ValueError("Щось пішло не так")
except ValueError as e:
    print(f"❌ Обробка: {e}")
```

**Виведення:**
```
🔌 Підключення до БД
📝 Працюємо з connection_object
⚠️ Виникла помилка: Щось пішло не так
🔒 Закриття з'єднання
❌ Обробка: Щось пішло не так
```

---

## Traceback

### Що таке traceback?

**Traceback** — це **слід виконання**, який показує, де саме виникла помилка.

### Приклад traceback:

```python
def func_a():
    func_b()

def func_b():
    func_c()

def func_c():
    result = 10 / 0  # Помилка тут!

func_a()
```

**Виведення:**
```
Traceback (most recent call last):
  File "script.py", line 9, in <module>
    func_a()
  File "script.py", line 2, in func_a
    func_b()
  File "script.py", line 5, in func_b
    func_c()
  File "script.py", line 8, in func_c
    result = 10 / 0
ZeroDivisionError: division by zero
```

### Читання traceback (знизу вгору):

```
1. ZeroDivisionError в рядку 8 (func_c)
2. func_c викликано з func_b (рядок 5)
3. func_b викликано з func_a (рядок 2)
4. func_a викликано з основного коду (рядок 9)
```

### Модуль traceback:

```python
import traceback

try:
    result = 10 / 0
except ZeroDivisionError:
    # Вивести traceback
    traceback.print_exc()
    
    # Або отримати як рядок
    tb_str = traceback.format_exc()
    print("Traceback as string:")
    print(tb_str)
```

### Логування traceback:

```python
import logging
import traceback

logging.basicConfig(level=logging.ERROR)

try:
    result = 10 / 0
except ZeroDivisionError:
    logging.error("Помилка ділення:")
    logging.error(traceback.format_exc())
```

---

## Логування винятків

### Навіщо логувати винятки?

1. **Debugging** — знайти причину помилки
2. **Моніторинг** — відстежити проблеми в production
3. **Статистика** — скільки і яких помилок

### Базове логування:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    result = 10 / 0
except ZeroDivisionError:
    logging.error("Помилка ділення на нуль", exc_info=True)
```

### Логування з деталями:

```python
import logging

logger = logging.getLogger(__name__)

def divide(a, b):
    try:
        result = a / b
        logger.info(f"Ділення {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        logger.error(f"Спроба ділення {a} на нуль", exc_info=True)
        return None

divide(10, 2)
divide(10, 0)
```

### Логування в файл:

```python
import logging

logging.basicConfig(
    filename='errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

try:
    # Код
    result = 10 / 0
except Exception as e:
    logging.exception("Сталася помилка:")
```

---

## Exception chaining

### Що таке exception chaining?

**Exception chaining** — зв'язування одного винятку з іншим.

### Синтаксис:

```python
raise НовийВиняток() from СтарийВиняток
```

### Приклад:

```python
try:
    result = int("abc")
except ValueError as e:
    raise RuntimeError("Не вдалося обробити дані") from e
```

**Виведення:**
```
ValueError: invalid literal for int() with base 10: 'abc'

The above exception was the direct cause of the following exception:

RuntimeError: Не вдалося обробити дані
```

### Практичний приклад:

```python
class ConfigError(Exception):
    pass

def read_config(filename):
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError as e:
        raise ConfigError(f"Не вдалося завантажити конфігурацію") from e

try:
    config = read_config("missing.ini")
except ConfigError as e:
    print(f"❌ {e}")
    print(f"Причина: {e.__cause__}")
```

### Suppress original exception:

```python
try:
    result = int("abc")
except ValueError:
    raise RuntimeError("Помилка") from None  # Приховує оригінальний виняток
```

---

## Практичні приклади

### Приклад 1: Безпечний калькулятор

```python
def safe_calculator():
    """Калькулятор з обробкою помилок"""
    
    print("Простий калькулятор")
    print("Операції: +, -, *, /")
    print("Введіть 'quit' для виходу")
    
    while True:
        try:
            # Введення
            command = input("\nВведіть вираз (наприклад, 5 + 3): ").strip()
            
            if command.lower() == "quit":
                print("До побачення!")
                break
            
            # Розбір виразу
            parts = command.split()
            if len(parts) != 3:
                raise ValueError("Формат: число операція число")
            
            a = float(parts[0])
            operator = parts[1]
            b = float(parts[2])
            
            # Обчислення
            if operator == "+":
                result = a + b
            elif operator == "-":
                result = a - b
            elif operator == "*":
                result = a * b
            elif operator == "/":
                if b == 0:
                    raise ZeroDivisionError("Ділення на нуль неможливе")
                result = a / b
            else:
                raise ValueError(f"Невідома операція: {operator}")
            
            print(f"✅ Результат: {result}")
            
        except ValueError as e:
            print(f"❌ Помилка значення: {e}")
        except ZeroDivisionError as e:
            print(f"❌ {e}")
        except KeyboardInterrupt:
            print("\n👋 Перервано користувачем")
            break
        except Exception as e:
            print(f"❌ Неочікувана помилка: {e}")

# Запуск
safe_calculator()
```

### Приклад 2: Робота з JSON файлами

```python
import json

class JSONManager:
    """Менеджер JSON файлів з обробкою помилок"""
    
    @staticmethod
    def read_json(filename):
        """Читання JSON файлу"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                print(f"✅ Файл '{filename}' прочитано")
                return data
                
        except FileNotFoundError:
            print(f"❌ Файл '{filename}' не знайдено")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Невірний JSON формат: {e}")
            return None
        except PermissionError:
            print(f"❌ Немає прав для читання '{filename}'")
            return None
    
    @staticmethod
    def write_json(filename, data):
        """Запис у JSON файл"""
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
                print(f"✅ Дані збережено у '{filename}'")
                return True
                
        except PermissionError:
            print(f"❌ Немає прав для запису '{filename}'")
            return False
        except TypeError as e:
            print(f"❌ Дані не можна серіалізувати: {e}")
            return False

# Використання
manager = JSONManager()

# Читання
data = manager.read_json("users.json")
if data:
    print(f"Користувачів: {len(data)}")

# Запис
new_data = {"name": "Іван", "age": 25}
manager.write_json("user.json", new_data)
```

### Приклад 3: Система валідації

```python
class ValidationError(Exception):
    """Помилка валідації"""
    pass

class Validator:
    """Валідатор даних користувача"""
    
    @staticmethod
    def validate_email(email):
        """Валідація email"""
        if not email:
            raise ValidationError("Email не може бути порожнім")
        
        if "@" not in email:
            raise ValidationError("Email має містити @")
        
        parts = email.split("@")
        if len(parts) != 2:
            raise ValidationError("Email має містити рівно один @")
        
        if not parts[0]:
            raise ValidationError("Email має містити ім'я перед @")
        
        if not parts[1]:
            raise ValidationError("Email має містити домен після @")
        
        if "." not in parts[1]:
            raise ValidationError("Домен має містити крапку")
        
        return True
    
    @staticmethod
    def validate_age(age):
        """Валідація віку"""
        if not isinstance(age, int):
            raise ValidationError("Вік має бути цілим числом")
        
        if age < 0:
            raise ValidationError("Вік не може бути від'ємним")
        
        if age > 150:
            raise ValidationError("Вік занадто великий")
        
        return True
    
    @staticmethod
    def validate_phone(phone):
        """Валідація телефону"""
        # Видалити пробіли та дефіси
        clean_phone = phone.replace(" ", "").replace("-", "")
        
        if not clean_phone:
            raise ValidationError("Телефон не може бути порожнім")
        
        # Перевірка чи тільки цифри та +
        if not all(c.isdigit() or c == "+" for c in clean_phone):
            raise ValidationError("Телефон може містити тільки цифри та +")
        
        if len(clean_phone) < 10:
            raise ValidationError("Телефон занадто короткий")
        
        return True

def register_user(name, email, age, phone):
    """Реєстрація користувача з валідацією"""
    errors = []
    
    try:
        Validator.validate_email(email)
    except ValidationError as e:
        errors.append(f"Email: {e}")
    
    try:
        Validator.validate_age(age)
    except ValidationError as e:
        errors.append(f"Вік: {e}")
    
    try:
        Validator.validate_phone(phone)
    except ValidationError as e:
        errors.append(f"Телефон: {e}")
    
    if errors:
        print("❌ Помилки валідації:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print(f"✅ Користувач {name} зареєстрований")
    return True

# Тестування
register_user("Іван", "ivan@example.com", 25, "+380501234567")
register_user("Марія", "invalid-email", -5, "123")
```

---

## Поширені помилки

### Помилка 1: Занадто широкий except

**❌ Погано:**
```python
try:
    # код
except:
    print("Помилка")  # Спіймає ВСЕ, навіть KeyboardInterrupt!
```

**✅ Краще:**
```python
try:
    # код
except Exception as e:
    print(f"Помилка: {e}")
```

**✅ Ще краще:**
```python
try:
    # код
except ValueError as e:
    print(f"Помилка значення: {e}")
except TypeError as e:
    print(f"Помилка типу: {e}")
```

### Помилка 2: Ігнорування винятків

**❌ Погано:**
```python
try:
    result = risky_operation()
except:
    pass  # Тихо ігнорує всі помилки!
```

**✅ Краще:**
```python
try:
    result = risky_operation()
except SpecificError as e:
    logging.error(f"Помилка: {e}")
    result = default_value
```

### Помилка 3: Перехоплення BaseException

**❌ Погано:**
```python
try:
    # код
except BaseException:  # Спіймає SystemExit, KeyboardInterrupt
    print("Помилка")
```

**✅ Краще:**
```python
try:
    # код
except Exception:  # Не спіймає системні винятки
    print("Помилка")
```

### Помилка 4: Забути raise в except

**❌ Погано:**
```python
try:
    important_operation()
except SomeError:
    print("Помилка")
    # Забули raise - програма продовжує працювати з помилкою!
```

**✅ Краще:**
```python
try:
    important_operation()
except SomeError as e:
    print(f"Помилка: {e}")
    raise  # Перевикинути виняток
```

### Помилка 5: Неправильний порядок except

**❌ Погано:**
```python
try:
    # код
except Exception:  # Спіймає все
    print("Загальна помилка")
except ValueError:  # Ніколи не виконається!
    print("ValueError")
```

**✅ Правильно:**
```python
try:
    # код
except ValueError:  # Конкретний перший
    print("ValueError")
except TypeError:
    print("TypeError")
except Exception:  # Загальний останній
    print("Загальна помилка")
```

---

## Найкращі практики

### 1. Ловіть конкретні винятки

**✅ Добре:**
```python
try:
    age = int(input("Вік: "))
except ValueError:
    print("Введіть число")
```

**❌ Погано:**
```python
try:
    age = int(input("Вік: "))
except:
    print("Помилка")
```

### 2. Не ігноруйте винятки

**✅ Добре:**
```python
try:
    data = process()
except ValueError as e:
    logging.error(f"Помилка обробки: {e}")
    data = None
```

**❌ Погано:**
```python
try:
    data = process()
except ValueError:
    pass  # Тихо ігнорує
```

### 3. Використовуйте finally для очищення

**✅ Добре:**
```python
file = None
try:
    file = open("data.txt")
    # робота з файлом
finally:
    if file:
        file.close()
```

**Або краще - with:**
```python
with open("data.txt") as file:
    # робота з файлом
```

### 4. Не використовуйте винятки для контролю потоку

**❌ Погано:**
```python
try:
    return my_dict[key]
except KeyError:
    return None
```

**✅ Краще:**
```python
return my_dict.get(key, None)
```

### 5. Додавайте корисні повідомлення

**✅ Добре:**
```python
if age < 0:
    raise ValueError(f"Вік не може бути від'ємним: отримано {age}")
```

**❌ Погано:**
```python
if age < 0:
    raise ValueError("Invalid age")
```

### 6. Створюйте власні винятки для бізнес-логіки

**✅ Добре:**
```python
class InsufficientFundsError(Exception):
    pass

if amount > balance:
    raise InsufficientFundsError(f"Баланс: {balance}, потрібно: {amount}")
```

### 7. Логуйте винятки

**✅ Добре:**
```python
import logging

try:
    risky_operation()
except Exception:
    logging.exception("Помилка в risky_operation")
    raise
```

### 8. Не ховайте traceback

**✅ Добре:**
```python
try:
    process()
except ValueError:
    logging.error("Помилка", exc_info=True)
    raise
```

**❌ Погано:**
```python
try:
    process()
except ValueError as e:
    raise ValueError("Нова помилка")  # Втрачено оригінальний traceback
```

**✅ Краще:**
```python
try:
    process()
except ValueError as e:
    raise ValueError("Нова помилка") from e  # Зберігаємо traceback
```

---

## Коли НЕ використовувати винятки

### 1. Для контролю потоку (if краще)

**❌ Погано:**
```python
try:
    value = my_dict[key]
except KeyError:
    value = None
```

**✅ Краще:**
```python
value = my_dict.get(key, None)
```

### 2. Для валідації вводу (перевірка краще)

**❌ Погано:**
```python
try:
    age = int(input("Вік: "))
except ValueError:
    age = 0
```

**✅ Краще (якщо ввід постійно невалідний):**
```python
age_str = input("Вік: ")
if age_str.isdigit():
    age = int(age_str)
else:
    print("Введіть число")
    age = 0
```

### 3. Для очікуваних випадків

**❌ Погано:**
```python
try:
    result = numbers[index]
except IndexError:
    result = None
```

**✅ Краще:**
```python
if 0 <= index < len(numbers):
    result = numbers[index]
else:
    result = None
```

### 4. Для перевірки типів (isinstance краще)

**❌ Погано:**
```python
try:
    result = value.upper()
except AttributeError:
    result = value
```

**✅ Краще:**
```python
if isinstance(value, str):
    result = value.upper()
else:
    result = value
```

### Коли ВИКОРИСТОВУВАТИ винятки:

1. ✅ Помилки, які рідко трапляються
2. ✅ Проблеми з ресурсами (файли, мережа, БД)
3. ✅ Критичні помилки, які треба обробити
4. ✅ Коли неможливо передбачити проблему

### Правило EAFP vs LBYL:

**EAFP (Easier to Ask for Forgiveness than Permission):**
```python
# Спробуй, обробиш помилку потім
try:
    value = my_dict[key]
except KeyError:
    value = None
```

**LBYL (Look Before You Leap):**
```python
# Перевір спочатку
if key in my_dict:
    value = my_dict[key]
else:
    value = None
```

**Коли що:**
- EAFP: Якщо успіх **частіший** за помилку
- LBYL: Якщо помилка **частіша** за успіх

---

## Підсумок

### Основні концепції:

1. **Виняток** — подія, що перериває виконання
2. **`try-except`** — обробка винятків
3. **`else`** — виконується якщо немає винятку
4. **`finally`** — виконується завжди
5. **`raise`** — створити виняток
6. **Власні винятки** — для специфічної логіки

### Структура обробки:

```python
try:
    # Код, який може викликати виняток
except ConcreteException as e:
    # Обробка конкретного винятку
except AnotherException as e:
    # Обробка іншого винятку
else:
    # Якщо не було винятку
finally:
    # Завжди виконується (очищення ресурсів)
```

### Найпоширеніші винятки:

| Виняток                | Коли                       |
|------------------------|----------------------------|
| `ValueError`           | Невірне значення           |
| `TypeError`            | Невірний тип               |
| `ZeroDivisionError`    | Ділення на нуль            |
| `IndexError`           | Індекс поза межами         |
| `KeyError`             | Ключ не знайдено           |
| `FileNotFoundError`    | Файл не знайдено           |
| `AttributeError`       | Атрибут не існує           |
| `NameError`            | Змінна не визначена        |

### Власні винятки:

```python
class MyError(Exception):
    """Власний виняток"""
    def __init__(self, message):
        super().__init__(message)

raise MyError("Опис помилки")
```

### Найкращі практики:

1. ✅ Ловіть конкретні винятки
2. ✅ Не ігноруйте помилки
3. ✅ Використовуйте finally для очищення
4. ✅ Додавайте корисні повідомлення
5. ✅ Логуйте винятки
6. ✅ Створюйте власні винятки для бізнес-логіки
7. ❌ Не використовуйте для контролю потоку
8. ❌ Не ховайте traceback

### Коли використовувати винятки:

- ✅ Рідкісні помилки
- ✅ Проблеми з ресурсами
- ✅ Критичні помилки
- ❌ Контроль потоку
- ❌ Часті перевірки
- ❌ Валідація вводу

**Успіхів у роботі з винятками! ⚠️✨**
