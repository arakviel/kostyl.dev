---
marp: true
theme: default
paginate: true
---

# Логічні оператори та оператори розгалужень

**Lesson 4: Logical Operators & Conditionals**

*Як приймати рішення в коді*

---

## Що таке умовні оператори?

**Умовні оператори** дозволяють програмі приймати рішення та виконувати різний код залежно від умови

```python
age = 18

if age >= 18:
    print("Ви повнолітній")
else:
    print("Ви неповнолітній")
```

**Аналогія з життя:**
- **ЯКЩО** на вулиці дощ, **ТО** візьми парасольку
- **ІНАКШЕ** парасолька не потрібна

---

## Навіщо потрібні умови?

Умовні оператори — основа програмування:

✅ **Валідація даних**
```python
password = input("Enter password: ")
if len(password) < 8:
    print("Password too short!")
```

✅ **Різна логіка для різних випадків**
```python
score = 85
if score >= 90:
    print("Grade: A")
```

✅ **Інтерактивність**
```python
choice = input("Continue? (y/n): ")
if choice == "y":
    print("Continuing...")
```

---

## Оператори порівняння

Перш ніж вивчати умови, розглянемо оператори порівняння:

| Оператор | Значення | Приклад | Результат |
|----------|----------|---------|-----------|
| `==` | Дорівнює | `5 == 5` | `True` |
| `!=` | Не дорівнює | `5 != 3` | `True` |
| `>` | Більше | `5 > 3` | `True` |
| `<` | Менше | `3 < 5` | `True` |
| `>=` | Більше або дорівнює | `5 >= 5` | `True` |
| `<=` | Менше або дорівнює | `3 <= 5` | `True` |

**Важливо:** Результат порівняння — завжди `bool` (True або False)

---

## Оператори порівняння: Приклади

```python
# Числа
print(5 == 5)        # True
print(5 != 3)        # True
print(10 > 5)        # True
print(3 < 3)         # False (3 не менше за 3)
print(3 <= 3)        # True (3 дорівнює 3)

# Рядки (лексикографічне порівняння)
print("apple" < "banana")   # True
print("ABC" < "abc")        # True (великі літери < малих)
print("hello" == "hello")   # True

# Різні типи
print(5 == 5.0)      # True (значення рівні)
print(5 == "5")      # False (різні типи)
```

---

## Типова помилка: = vs ==

⚠️ **Не плутайте присвоєння з порівнянням!**

```python
# = — присвоєння (assignment)
x = 5               # Присвоїти 5 змінній x

# == — порівняння (comparison)
print(x == 5)       # Чи дорівнює x п'яти? True

# ❌ Типова помилка
x = 5
if x = 10:          # SyntaxError!
    print("Wrong")

# ✅ Правильно
if x == 10:
    print("Correct")
```

**Запам'ятайте:** `=` для присвоєння, `==` для порівняння!

---

## Логічні оператори

Python має три логічні оператори:

| Оператор | Значення | Приклад | Коли True |
|----------|----------|---------|-----------|
| `and` | І (логічне AND) | `True and True` | Обидві умови True |
| `or` | АБО (логічне OR) | `True or False` | Хоча б одна True |
| `not` | НЕ (логічне NOT) | `not False` | Інвертує значення |

```python
# and — обидві умови мають бути True
print(True and True)    # True
print(True and False)   # False

# or — хоча б одна умова має бути True
print(True or False)    # True
print(False or False)   # False

# not — інвертує значення
print(not True)         # False
print(not False)        # True
```

---

## Логічний оператор AND

**and** повертає True, тільки якщо **ОБИ** умови True:

```python
# Таблиця істинності AND
print(True and True)     # True
print(True and False)    # False
print(False and True)    # False
print(False and False)   # False

# Практичний приклад
age = 20
has_license = True

if age >= 18 and has_license:
    print("Can drive")
else:
    print("Cannot drive")
```

**Аналогія:** Щоб отримати кредит, потрібно **І** бути повнолітнім **І** мати дохід.

---

## Логічний оператор OR

**or** повертає True, якщо **ХОЧА Б ОДНА** умова True:

```python
# Таблиця істинності OR
print(True or True)      # True
print(True or False)     # True
print(False or True)     # True
print(False or False)    # False

# Практичний приклад
is_weekend = True
is_holiday = False

if is_weekend or is_holiday:
    print("Day off!")
else:
    print("Work day")
```

**Аналогія:** Щоб не йти на роботу, потрібно **АБО** вихідний **АБО** свято.

---

## Логічний оператор NOT

**not** інвертує (змінює на протилежне) логічне значення:

```python
# NOT інвертує
print(not True)          # False
print(not False)         # True

# Практичний приклад
is_raining = False

if not is_raining:
    print("Go for a walk")
else:
    print("Stay home")

# З порівняннями
x = 5
print(not x > 10)        # True (бо x > 10 = False, not False = True)
```

**Аналогія:** ЯКЩО НЕ йде дощ, то йдемо гуляти.

---

## Комбінування логічних операторів

Можна комбінувати кілька логічних операторів:

```python
age = 25
has_ticket = True
has_id = True

# Комбінація AND
if age >= 18 and has_ticket and has_id:
    print("Can enter")

# Комбінація OR
day = "Saturday"
if day == "Saturday" or day == "Sunday":
    print("Weekend!")

# Комбінація AND і OR
if (age >= 18 and has_ticket) or is_vip:
    print("Access granted")
```

**Пріоритет:** not > and > or  
**Рекомендація:** Використовуйте дужки для ясності!

---

## Пріоритет логічних операторів

Порядок виконання:
1. **not** (найвищий пріоритет)
2. **and**
3. **or** (найнижчий пріоритет)

```python
# Без дужок
result = True or False and False
print(result)  # True (спочатку False and False = False, потім True or False = True)

# З дужками (краще!)
result = (True or False) and False
print(result)  # False

# Практичний приклад
age = 16
has_permission = True
if age >= 18 or age >= 16 and has_permission:
    print("Can watch")
# age >= 16 and has_permission виконується спочатку!
```

---

## Оператор if

**if** — базовий оператор розгалуження:

```python
# Синтаксис
if умова:
    # код виконується, якщо умова True
    print("Умова виконана")

# Приклад
age = 20
if age >= 18:
    print("Ви повнолітній")
```

**Важливо:**
- Після `if` ставиться двокрапка `:`
- Код всередині має бути з **відступом** (4 пробіли або Tab)
- Якщо умова False, код всередині пропускається

---

## Відступи в Python

⚠️ **Python використовує відступи для визначення блоків коду!**

```python
# ✅ Правильно
age = 18
if age >= 18:
    print("Line 1")
    print("Line 2")
print("Line 3")  # Завжди виконується

# ❌ Неправильно (IndentationError)
age = 18
if age >= 18:
print("Error")  # Немає відступу!

# ❌ Неправильно (змішані відступи)
if age >= 18:
    print("Line 1")  # 4 пробіли
	print("Line 2")  # Tab (помилка!)
```

**Стандарт:** Використовуйте **4 пробіли** для відступу.

---

## Оператор else

**else** виконується, якщо умова в `if` була False:

```python
# Синтаксис
if умова:
    # виконується, якщо True
else:
    # виконується, якщо False

# Приклад
age = 15
if age >= 18:
    print("Ви повнолітній")
else:
    print("Ви неповнолітній")

# Ще приклад
password = input("Enter password: ")
if len(password) >= 8:
    print("Password accepted")
else:
    print("Password too short")
```

---

## if-else: Блок-схема

```
         ┌─────────────┐
         │  age >= 18? │
         └──────┬──────┘
                │
       ┌────────┴────────┐
       │                 │
     True              False
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│ "Повнолітній"│  │ "Неповнолітній"  │
└──────────────┘  └──────────────────┘
```

**Завжди виконується тільки ОДИН блок:** або `if`, або `else`.

---

## Оператор elif

**elif** (else if) — перевіряє додаткові умови:

```python
# Синтаксис
if умова1:
    # якщо умова1 True
elif умова2:
    # якщо умова1 False, але умова2 True
elif умова3:
    # якщо умова1 і умова2 False, але умова3 True
else:
    # якщо всі умови False

# Приклад
score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
```

---

## elif: Важливі моменти

```python
score = 95

# ✅ Правильно: перша True умова виконується
if score >= 90:
    print("A")  # Це виконається
elif score >= 80:
    print("B")  # Це НЕ виконається (попередня була True)

# Виведе: A
```

**Важливо:**
- Виконується тільки **ПЕРШИЙ** блок з True умовою
- Інші умови не перевіряються
- `else` — опціональний (можна без нього)
- Можна мати багато `elif`

---

## elif vs окремі if

**Різниця між elif та окремими if:**

```python
score = 95

# З elif — виконається тільки один блок
if score >= 90:
    print("A")      # Виконається
elif score >= 80:
    print("B")      # НЕ виконається

# З окремими if — можуть виконатися обидва
if score >= 90:
    print("A")      # Виконається
if score >= 80:
    print("B")      # ТЕОЖ виконається!
```

**Використовуйте elif**, коли умови взаємовиключні!

---

## Практичний приклад: Оцінювання

```python
score = int(input("Enter your score (0-100): "))

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade: {grade}")
```

**Логіка:**
- Перевіряємо від найвищої оцінки до найнижчої
- Як тільки знаходимо відповідну умову, зупиняємося

---

## Вкладені умови

Можна розміщувати `if` всередині іншого `if`:

```python
age = 20
has_license = True

if age >= 18:
    print("Ви повнолітній")
    
    if has_license:
        print("Можете керувати авто")
    else:
        print("Потрібні права")
else:
    print("Ви неповнолітній")
    print("Права отримувати рано")
```

**Відступи:** Кожен вкладений рівень має додатковий відступ (4 пробіли).

---

## Вкладені умови: Рівні

```python
age = 25
has_license = True
has_car = False

if age >= 18:                      # Рівень 1
    if has_license:                # Рівень 2
        if has_car:                # Рівень 3
            print("Can drive own car")
        else:
            print("Can rent a car")
    else:
        print("Need license first")
else:
    print("Too young")
```

**Рекомендація:** Не робіть занадто глибоку вкладеність (max 2-3 рівні).

---

## Спрощення вкладених умов

**Замість вкладених if, використовуйте and:**

```python
# ❌ Складно (вкладені)
age = 20
has_license = True

if age >= 18:
    if has_license:
        print("Can drive")

# ✅ Простіше (and)
if age >= 18 and has_license:
    print("Can drive")
```

**Правило:** Якщо можна використати `and`, краще не вкладати.

---

## Порівняння рядків

Рядки порівнюються **лексикографічно** (як у словнику):

```python
# Основи
print("apple" < "banana")   # True
print("cat" > "car")        # True (t > r)
print("ABC" < "abc")        # True (великі < малих у Unicode)

# З input
name = input("Enter name: ")
if name == "Admin":
    print("Welcome, Admin!")

# Case-insensitive порівняння
if name.lower() == "admin":
    print("Welcome!")
```

**Важливо:** `"Admin"` ≠ `"admin"` (регістр має значення!)

---

## Корисні методи для рядків

```python
text = "  Hello World  "

# Видалення пробілів
print(text.strip())         # "Hello World"

# Зміна регістру
print(text.lower())         # "  hello world  "
print(text.upper())         # "  HELLO WORLD  "

# Перевірки
print("123".isdigit())      # True
print("abc".isalpha())      # True
print("abc123".isalnum())   # True

# Практичний приклад
password = input("Password: ")
if password.lower() == "secret":
    print("Access granted")
```

---

## Перевірка на входження: in

**in** перевіряє, чи міститься елемент у рядку:

```python
# Для рядків
text = "Hello World"
print("Hello" in text)      # True
print("Python" in text)     # False
print("world" in text)      # False (регістр!)
print("world" in text.lower())  # True

# not in — заперечення
if "error" not in message:
    print("No errors")

# Практичний приклад
email = input("Enter email: ")
if "@" in email and "." in email:
    print("Valid email format")
else:
    print("Invalid email")
```

---

## Перевірка на порожній рядок

```python
# Спосіб 1: Порівняння з ""
name = input("Enter name: ")
if name == "":
    print("Name is empty")

# Спосіб 2: Використання bool() (краще!)
if not name:
    print("Name is empty")

# З видаленням пробілів
if not name.strip():
    print("Name is empty or only spaces")

# Практичний приклад
password = input("Enter password: ")
if not password:
    print("Password cannot be empty!")
else:
    print("Password accepted")
```

---

## Перевірка діапазону: ланцюгові порівняння

Python дозволяє ланцюгові порівняння:

```python
# ✅ Python стиль (ланцюгові порівняння)
age = 25
if 18 <= age <= 65:
    print("Working age")

# ❌ Довгий спосіб (але теж працює)
if age >= 18 and age <= 65:
    print("Working age")

# Ще приклади
score = 85
if 0 <= score <= 100:
    print("Valid score")

if 80 <= score < 90:
    print("Grade B")
```

**Переваги:** Коротше і читабельніше!

---

## Тернарний оператор

**Тернарний оператор** — компактна форма if-else:

```python
# Синтаксис
значення_якщо_True if умова else значення_якщо_False

# Приклад 1: Присвоєння
age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # "adult"

# Приклад 2: В print
score = 85
print("Pass" if score >= 60 else "Fail")

# Еквівалентний звичайний if-else
if score >= 60:
    print("Pass")
else:
    print("Fail")
```

---

## Коли використовувати тернарний оператор

**✅ Використовуйте для простих випадків:**

```python
# Добре — просте присвоєння
min_val = a if a < b else b

# Добре — короткий вивід
print("Even" if num % 2 == 0 else "Odd")
```

**❌ Не використовуйте для складної логіки:**

```python
# Погано — важко читати
result = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"

# Краще — звичайний if-elif-else
if score >= 90:
    result = "A"
elif score >= 80:
    result = "B"
elif score >= 70:
    result = "C"
else:
    result = "F"
```

---

## Оператор is vs ==

**==** порівнює **значення**, **is** порівнює **ідентичність об'єктів**:

```python
# == порівнює значення
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)        # True (значення однакові)
print(a is b)        # False (різні об'єкти)

# is для None
x = None
if x is None:        # ✅ Правильно
    print("x is None")

if x == None:        # ❌ Працює, але не рекомендовано
    print("x is None")

# is для bool
if flag is True:     # ❌ Не рекомендовано
if flag:             # ✅ Краще
```

**Правило:** Використовуйте `is` тільки для `None`, `True`, `False`.

---

## Short-circuit evaluation

Python **не обчислює всі частини** логічного виразу, якщо результат вже зрозумілий:

```python
# OR: якщо перше True, друге не обчислюється
x = True or print("This won't print")
print(x)  # True (print не викликається)

# AND: якщо перше False, друге не обчислюється
x = False and print("This won't print")
print(x)  # False (print не викликається)

# Практичне застосування
age = None
if age and age >= 18:  # Якщо age None, age >= 18 не виконається
    print("Adult")

# Корисно для уникнення помилок
text = ""
if text and text[0] == "A":  # Якщо text порожній, text[0] не викликається
    print("Starts with A")
```

---

## Практичний приклад: Валідація паролю

```python
password = input("Enter password: ")

# Перевірка довжини
if len(password) < 8:
    print("Password must be at least 8 characters")
elif len(password) > 20:
    print("Password too long (max 20)")
else:
    # Перевірка складності
    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    
    if has_digit and has_upper and has_lower:
        print("Strong password!")
    else:
        print("Password should contain digits, uppercase and lowercase")
```

---

## Практичний приклад: Калькулятор

```python
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
operation = input("Enter operation (+, -, *, /): ")

if operation == "+":
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
elif operation == "-":
    result = num1 - num2
    print(f"{num1} - {num2} = {result}")
elif operation == "*":
    result = num1 * num2
    print(f"{num1} * {num2} = {result}")
elif operation == "/":
    if num2 != 0:
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
    else:
        print("Error: Division by zero!")
else:
    print("Invalid operation!")
```

---

## Практичний приклад: Визначення сезону

```python
month = int(input("Enter month (1-12): "))

if month in [12, 1, 2]:
    season = "Winter"
elif month in [3, 4, 5]:
    season = "Spring"
elif month in [6, 7, 8]:
    season = "Summer"
elif month in [9, 10, 11]:
    season = "Autumn"
else:
    season = "Invalid month"

print(f"Season: {season}")

# Альтернатива з if-elif
if 1 <= month <= 12:
    if month == 12 or month <= 2:
        season = "Winter"
    elif month <= 5:
        season = "Spring"
    elif month <= 8:
        season = "Summer"
    else:
        season = "Autumn"
    print(f"Season: {season}")
else:
    print("Invalid month")
```

---

## Типові помилки початківців

```python
# ❌ Помилка 1: Забули двокрапку
if x > 5
    print("Error")  # SyntaxError

# ✅ Правильно
if x > 5:
    print("Correct")

# ❌ Помилка 2: Неправильні відступи
if x > 5:
print("Error")      # IndentationError

# ✅ Правильно
if x > 5:
    print("Correct")

# ❌ Помилка 3: = замість ==
if x = 5:           # SyntaxError
    print("Error")

# ✅ Правильно
if x == 5:
    print("Correct")
```

---

## Типові помилки (продовження)

```python
# ❌ Помилка 4: Логіка "між"
age = 25
if age >= 18 and <= 65:  # SyntaxError
    print("Error")

# ✅ Правильно (варіант 1)
if age >= 18 and age <= 65:
    print("Correct")

# ✅ Правильно (варіант 2, краще)
if 18 <= age <= 65:
    print("Correct")

# ❌ Помилка 5: Порожній if
if x > 5:
    # Нічого не робимо
# IndentationError: expected an indented block

# ✅ Правильно
if x > 5:
    pass  # pass — "нічого не робити"
```

---

## Найкращі практики

✅ **Використовуйте описові імена для булевих змінних:**
```python
# Погано
flag = True
x = False

# Добре
is_valid = True
has_access = False
can_edit = True
```

✅ **Уникайте зайвих порівнянь з True/False:**
```python
# Погано
if is_valid == True:
    print("Valid")

# Добре
if is_valid:
    print("Valid")
```

---

## Найкращі практики (продовження)

✅ **Перевіряйте найпоширеніші випадки спочатку:**
```python
# Якщо більшість користувачів дорослі, перевіряємо це першим
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

✅ **Використовуйте elif замість вкладених if:**
```python
# Погано
if score >= 90:
    grade = "A"
else:
    if score >= 80:
        grade = "B"
    else:
        grade = "C"

# Добре
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

---

## Вікторина: Що буде виведено?

```python
x = 10
y = 5

if x > 5 and y > 5:
    print("A")
elif x > 5 or y > 5:
    print("B")
else:
    print("C")
```

**A)** A  
**B)** B  
**C)** C  
**D)** Помилка  

<details>
<summary>Відповідь</summary>
B — перша умова False (y не > 5), друга умова True (x > 5)
</details>

---

## Вікторина 2

```python
age = 25

if age >= 18:
    print("Adult")
if age >= 21:
    print("Can drink")
```

**Скільки рядків буде виведено?**  
**A)** 0  
**B)** 1  
**C)** 2  
**D)** Помилка  

<details>
<summary>Відповідь</summary>
C — обидва if перевіряються окремо, обидві умови True
</details>

---

## Вікторина 3

```python
score = 85

if score >= 90:
    result = "A"
elif score >= 80:
    result = "B"
elif score >= 70:
    result = "C"

print(result)
```

**Що буде виведено?**  
**A)** A  
**B)** B  
**C)** C  
**D)** Помилка  

<details>
<summary>Відповідь</summary>
B — перша умова False, друга умова True
</details>

---

## Цікаві факти

🐍 Python використовує **відступи** (indentation) замість фігурних дужок `{}` (як C/Java)

💡 **Short-circuit evaluation:** Python не обчислює всі частини логічного виразу

⚡ **Ланцюгові порівняння:** `18 <= age <= 65` — унікальна можливість Python

🎯 `pass` — спеціальне ключове слово для "нічого не робити"

✅ `is` перевіряє **ідентичність об'єктів**, а не значення

🔢 Порівняння рядків: `"ABC" < "abc"` — великі літери < малих у Unicode

---

## Корисні шаблони

**Шаблон 1: Валідація діапазону**
```python
if not (0 <= score <= 100):
    print("Invalid score")
```

**Шаблон 2: Множинна перевірка**
```python
if operation in ["+", "-", "*", "/"]:
    print("Valid operation")
```

**Шаблон 3: Перевірка порожнього значення**
```python
if not text.strip():
    print("Empty or spaces only")
```

**Шаблон 4: Безпечна перевірка**
```python
if text and text[0] == "A":
    print("Starts with A")
```

---

## Ключові висновки

✅ **Оператори порівняння:** ==, !=, <, >, <=, >= повертають bool

✅ **Логічні оператори:** and, or, not для комбінування умов

✅ **if:** Виконує код, якщо умова True

✅ **elif:** Перевіряє додаткові умови (виконується тільки одна)

✅ **else:** Виконується, якщо всі попередні умови False

✅ **Відступи:** 4 пробіли для кожного рівня вкладеності

✅ **Ланцюгові порівняння:** `18 <= age <= 65` (унікально для Python)

✅ **Тернарний оператор:** компактна форма if-else для простих випадків

✅ **in:** перевірка входження в рядок

---

## Практичні завдання

1. **Перевірка пароля**
   - Запитайте пароль
   - Перевірте: довжина >= 8, є цифра, є велика літера

2. **Калькулятор знижки**
   - Ціна товару
   - Якщо >= 1000 → знижка 10%
   - Якщо >= 5000 → знижка 20%

3. **Визначення типу трикутника**
   - Три сторони
   - Рівносторонній / Рівнобедрений / Різносторонній

4. **Конвертер оцінок**
   - Бали 0-100
   - Виведіть оцінку A/B/C/D/F

---

## Домашнє завдання

**Завдання 1: Високосний рік**
Напишіть програму, яка визначає, чи є рік високосним:
- Ділиться на 4 AND (не ділиться на 100 OR ділиться на 400)

**Завдання 2: Валідатор email**
Перевірте email:
- Містить @
- Містить крапку після @
- Довжина >= 5

**Завдання 3: Гра "Вгадай число"**
- Загадайте число 1-10
- Користувач вводить здогадку
- Виведіть: "Більше", "Менше" або "Правильно!"

---

# Дякую за увагу!

**Питання?**

*"Умовні оператори — це мозок вашої програми"*

---

## Додаткові ресурси

📚 **Документація:**
- [Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Boolean Operations](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not)
- [Comparisons](https://docs.python.org/3/library/stdtypes.html#comparisons)

🎓 **Практика:**
- [Python If-Else](https://www.programiz.com/python-programming/if-elif-else)
- [Real Python: Conditionals](https://realpython.com/python-conditional-statements/)

**Практикуйтесь щодня!**
