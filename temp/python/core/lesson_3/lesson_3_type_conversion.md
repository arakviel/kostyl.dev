---
marp: true
theme: default
paginate: true
style: |
    section {
      font-size: 18px;
    }
    code {
      font-size: 16px;
    }
    pre {
      font-size: 16px;
    }
    table {
      font-size: 18px;
    }
---

# Перетворення типів даних у Python

**Lesson 3: Type Conversion & Casting**

_Як Python перетворює дані з одного типу в інший_

---

## Що таке перетворення типів?

**Перетворення типів** (Type Conversion/Casting) — це процес зміни типу даних з одного на інший

```python
# Рядок → Число
age = int("25")         # "25" → 25
print(age + 5)          # 30

# Число → Рядок
count = str(100)        # 100 → "100"
print("Count: " + count) # "Count: 100"
```

**Чому це потрібно?**

-   Різні операції вимагають різних типів
-   Введення користувача завжди рядок (`input()`)
-   Обмін даними між системами

---

## Явне vs Неявне перетворення

Python підтримує два типи перетворення:

**1. Неявне (Implicit) — Python робить автоматично:**

```python
x = 5        # int
y = 2.5      # float
z = x + y    # 7.5 (int автоматично → float)
print(type(z))  # <class 'float'>
```

**2. Явне (Explicit) — ви контролюєте:**

```python
x = "123"
y = int(x)   # Явно перетворюємо str → int
print(y + 10)  # 133
```

**Правило:** Явне краще за неявне!

---

## Неявне перетворення типів

Python автоматично перетворює типи у певних ситуаціях:

**Арифметичні операції:**

```python
# int + float = float
print(5 + 2.5)       # 7.5 (float)
print(type(5 + 2.5)) # <class 'float'>

# int * float = float
print(3 * 1.5)       # 4.5 (float)

# int / int = float (ділення завжди дає float!)
print(10 / 2)        # 5.0 (не 5!)
```

**Правило:** Менш точний тип → більш точний тип

---

## Неявне перетворення: Приклади

```python
# bool → int (True = 1, False = 0)
print(True + 5)      # 6
print(False * 10)    # 0

# bool → float
print(True + 2.5)    # 3.5

# int → float у порівняннях
print(5 == 5.0)      # True (але типи різні!)
```

**Застереження:** Не всі комбінації працюють!

```python
# ❌ Не можна додавати str + int
print("Age: " + 25)  # TypeError
```

---

## Функції перетворення типів

Python має вбудовані функції для явного перетворення:

| Функція   | Призначення                  | Приклад                  |
| --------- | ---------------------------- | ------------------------ |
| `int()`   | Перетворює в ціле число      | `int("123")` → `123`     |
| `float()` | Перетворює в дробове число   | `float("3.14")` → `3.14` |
| `str()`   | Перетворює в рядок           | `str(123)` → `"123"`     |
| `bool()`  | Перетворює в булеве значення | `bool(1)` → `True`       |

---

## Перетворення в int()

Перетворює значення в ціле число:

**З рядка:**

```python
print(int("123"))           # 123
print(int("-456"))          # -456
print(int("+789"))          # 789
```

**З float (відкидає дробову частину):**

```python
print(int(3.14))            # 3 (не 4!)
print(int(9.99))            # 9
print(int(-2.7))            # -2
```

**З булевого:**

```python
print(int(True))            # 1
print(int(False))           # 0
```

---

## int(): Системи числення

`int()` може перетворювати рядки з різних систем числення:

```python
# Синтаксис: int(string, base)

# Двійкова (base=2)
print(int("1010", 2))       # 10
print(int("0b1010", 2))     # 10 (з префіксом)

# Вісімкова (base=8)
print(int("12", 8))         # 10
print(int("0o12", 8))       # 10

# Шістнадцяткова (base=16)
print(int("A", 16))         # 10
print(int("0xA", 16))       # 10
print(int("FF", 16))        # 255
```

---

## int(): Помилки

Не всі значення можна перетворити:

```python
# ❌ ValueError: недопустимий формат
int("12.5")         # ValueError (є крапка)
int("abc")          # ValueError (не число)
int("12 34")        # ValueError (пробіл)
int("")             # ValueError (порожній рядок)

# ❌ TypeError: не підтримується
int(None)           # TypeError (None)

# ✅ Працює
int("  123  ")      # 123 (пробіли на початку/кінці OK)
```

---

## int(): Цікаві випадки

```python
# Пробіли на початку/кінці — OK
print(int("  123  "))       # 123

# Знак + або - — OK
print(int("+123"))          # 123
print(int("-123"))          # -123

# Підкреслення — ❌ НЕ працюють у рядках!
# int("1_000_000")          # ValueError

# Експоненційний запис — ❌ НЕ працює
# int("1e6")                # ValueError

# Рішення: спочатку в float, потім в int
print(int(float("1e6")))    # 1000000
```

---

## Перетворення в float()

Перетворює значення в число з рухомою крапкою:

**З рядка:**

```python
print(float("3.14"))        # 3.14
print(float("-0.5"))        # -0.5
print(float(".5"))          # 0.5
print(float("2."))          # 2.0
print(float("  3.14  "))    # 3.14 (пробіли ігноруються)
```

**З int:**

```python
print(float(5))             # 5.0
print(float(-3))            # -3.0
```

**З булевого:**

```python
print(float(True))          # 1.0
print(float(False))         # 0.0
```

---

## float(): Спеціальні значення

Python підтримує спеціальні float значення:

```python
# Нескінченність
inf = float("inf")
neg_inf = float("-inf")
print(inf)                  # inf
print(neg_inf)              # -inf
print(inf > 1000000)        # True

# Не-число (Not a Number)
nan = float("nan")
print(nan)                  # nan
print(nan == nan)           # False (!)

# Перевірка на спеціальні значення
import math
print(math.isinf(inf))      # True
print(math.isnan(nan))      # True
```

---

## float(): Експоненційний запис

```python
# float() підтримує науковий запис
print(float("1e6"))         # 1000000.0
print(float("1.5e3"))       # 1500.0
print(float("2.5e-4"))      # 0.00025

# Великі та малі числа
print(float("3e308"))       # 3e+308 (майже максимум)
print(float("1e-308"))      # 1e-308 (майже мінімум)

# Переповнення
print(float("1e309"))       # inf (переповнення!)
```

---

## float(): Помилки

```python
# ❌ ValueError
float("abc")        # ValueError
float("12.34.56")   # ValueError (дві крапки)
float("12,34")      # ValueError (кома замість крапки)
float("")           # ValueError (порожній рядок)

# ❌ TypeError
float(None)         # TypeError (None)

# ✅ Працює
float("inf")        # inf
float("nan")        # nan
float(" 3.14 ")     # 3.14
```

---

## Перетворення в str()

Перетворює будь-яке значення в рядок:

```python
# Числа
print(str(123))             # "123"
print(str(3.14))            # "3.14"
print(str(-5))              # "-5"

# Булеві
print(str(True))            # "True"
print(str(False))           # "False"

# None
print(str(None))            # "None"

# Спеціальні float
print(str(float("inf")))    # "inf"
print(str(float("nan")))    # "nan"
```

---

## str(): Форматування

Для контролю формату використовуйте f-strings:

```python
# f-strings (Python 3.6+)
x = 123
print(f"Number: {x}")       # "Number: 123"

# Форматування чисел
pi = 3.14159
print(f"{pi:.2f}")          # "3.14" (2 знаки після коми)

# Системи числення
num = 42
print(f"{num:b}")           # "101010" (двійкова)
print(f"{num:o}")           # "52" (вісімкова)
print(f"{num:x}")           # "2a" (hex)
print(f"{num:X}")           # "2A" (HEX)
```

---

## Перетворення в bool()

Перетворює значення в True або False:

**Хибні (False) значення:**

```python
print(bool(0))              # False
print(bool(0.0))            # False
print(bool(""))             # False (порожній рядок)
print(bool(None))           # False
print(bool(False))          # False
```

**Всі інші — True:**

```python
print(bool(1))              # True
print(bool(-1))             # True
print(bool("0"))            # True (рядок "0", не число!)
print(bool(" "))            # True (пробіл)
```

---

## bool(): Цікаві випадки

```python
# Всі ненульові числа — True
print(bool(1))              # True
print(bool(-1))             # True
print(bool(0.1))            # True
print(bool(-0.0))           # False (нуль є нуль)

# Рядок "False" — це True!
print(bool("False"))        # True (непорожній рядок)
print(bool("0"))            # True

# Спеціальні значення
print(bool(float("inf")))   # True
print(bool(float("nan")))   # True (!!)
```

---

## Перетворення між системами числення

```python
# Число → Інші системи
num = 42

# До рядків з префіксами
print(bin(num))             # "0b101010"
print(oct(num))             # "0o52"
print(hex(num))             # "0x2a"

# Без префіксів (зріз [2:])
print(bin(num)[2:])         # "101010"
print(oct(num)[2:])         # "52"
print(hex(num)[2:])         # "2a"

# З інших систем → Десяткова
print(int("101010", 2))     # 42
print(int("52", 8))         # 42
print(int("2a", 16))        # 42
```

---

## Символи та коди: ord() та chr()

**chr()** — код → символ  
**ord()** — символ → код

```python
# Символ → Код (Unicode)
print(ord('A'))             # 65
print(ord('a'))             # 97
print(ord('0'))             # 48
print(ord('Ї'))             # 1031

# Код → Символ
print(chr(65))              # 'A'
print(chr(97))              # 'a'
print(chr(48))              # '0'
print(chr(1031))            # 'Ї'

# Emoji
print(chr(128512))          # '😀'
print(ord('😀'))            # 128512
```

---

## Робота з input()

`input()` завжди повертає **рядок**:

```python
# ❌ Неправильно
age = input("Enter age: ")
print(age + 5)              # TypeError (рядок + число)

# ✅ Правильно
age = int(input("Enter age: "))
print(age + 5)              # Працює!

# Для float
price = float(input("Enter price: "))
total = price * 1.2
print(f"Total: {total:.2f}")
```

---

## Таблиця сумісності перетворень

| З / В     | int    | float  | str | bool |
| --------- | ------ | ------ | --- | ---- |
| **int**   | —      | ✅     | ✅  | ✅   |
| **float** | ✅\*   | —      | ✅  | ✅   |
| **str**   | ✅\*\* | ✅\*\* | —   | ✅   |
| **bool**  | ✅     | ✅     | ✅  | —    |
| **None**  | ❌     | ❌     | ✅  | ✅   |

\* — відкидає дробову частину  
\*\* — може викинути ValueError

---

## Типові помилки початківців

```python
# ❌ Помилка 1: Забули перетворити input()
age = input("Enter age: ")  # Це завжди str!
# print(age + 5)            # TypeError

# ✅ Правильно
age = int(input("Enter age: "))
print(age + 5)

# ❌ Помилка 2: int() відкидає дробову частину
print(int(9.99))            # 9, не 10!

# ✅ Якщо потрібне округлення
print(round(9.99))          # 10
```

---

## Типові помилки (продовження)

```python
# ❌ Помилка 3: float() не приймає коми
# price = float("19,99")    # ValueError

# ✅ Правильно
price = float("19.99")

# ❌ Помилка 4: str + int
# print("Age: " + 25)       # TypeError

# ✅ Правильно
print("Age: " + str(25))
print(f"Age: {25}")         # f-strings (найкраще!)

# ❌ Помилка 5: bool("False") → True
x = bool("False")           # True (непорожній рядок!)
```

---

## Найкращі практики

✅ **Явне перетворення:**

```python
# Погано (неявне)
result = "5" + str(3)       # Незрозуміло

# Добре (явне)
number = 5
text = str(number) + str(3)  # "53"
```

✅ **Використовуйте f-strings:**

```python
# Погано
print("Sum: " + str(10 + 20))

# Добре
print(f"Sum: {10 + 20}")
```

---

## Практичні приклади

**Приклад 1: Обчислення віку**

```python
birth_year = int(input("Enter birth year: "))
current_year = 2024
age = current_year - birth_year
print(f"Your age: {age}")
```

**Приклад 2: Конвертер температури**

```python
celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit:.1f}°F")
```

---

## Практичні приклади (продовження)

**Приклад 3: Калькулятор площі кола**

```python
radius = float(input("Enter radius: "))
pi = 3.14159
area = pi * radius ** 2
print(f"Area: {area:.2f}")
```

**Приклад 4: Перевірка типу**

```python
value = input("Enter value: ")
print(f"Type: {type(value)}")       # завжди <class 'str'>
print(f"Is digit: {value.isdigit()}")
```

---

## Вікторина: Що буде виведено?

```python
x = "123"
y = "456"
z = int(x) + int(y)
print(z)
```

**A)** "123456"  
**B)** 579  
**C)** "579"  
**D)** TypeError

<details>
<summary>Відповідь</summary>
B) 579 — x і y перетворені в int, тому відбувається числове додавання
</details>

---

## Вікторина 2

```python
print(bool("False"))
```

**A)** True  
**B)** False  
**C)** "False"  
**D)** ValueError

<details>
<summary>Відповідь</summary>
A) True — "False" це непорожній рядок, а всі непорожні рядки є truthy
</details>

---

## Вікторина 3

```python
print(int(9.99))
```

**A)** 9  
**B)** 10  
**C)** 9.99  
**D)** ValueError

<details>
<summary>Відповідь</summary>
A) 9 — int() відкидає дробову частину, не округлює!
</details>

---

## Цікаві факти

🐍 `input()` завжди повертає **рядок**, навіть якщо ви ввели число

🔢 `int(3.9)` дає `3`, не `4` — int() не округлює!

💡 Python 3: `5 / 2` = `2.5` (float), але `5 // 2` = `2` (int)

⚠️ `bool("False")` = `True` — це рядок, не булеве значення!

🎯 `None` не можна перетворити в int або float (TypeError)

📊 Unicode: `ord('A')` = 65, `chr(65)` = 'A'

---

## Корисні функції

```python
# Перевірка типу
print(type(123))            # <class 'int'>
print(isinstance(123, int)) # True

# Перевірка рядків
print("123".isdigit())      # True
print("abc".isalpha())      # True
print("abc123".isalnum())   # True

# Математика
print(round(3.7))           # 4 (округлення)
print(abs(-5))              # 5 (модуль)
print(pow(2, 3))            # 8 (степінь)
```

---

## Ключові висновки

✅ **Неявне перетворення:** Python робить автоматично (int + float → float)  
✅ **Явне перетворення:** int(), float(), str(), bool()  
✅ **int()** — відкидає дробову частину, не округлює!  
✅ **float()** — підтримує "inf", "nan", експоненційний запис  
✅ **str()** — працює для будь-якого типу  
✅ **bool()** — тільки 5 хибних значень базових типів, всі інші — True  
✅ **Помилки:** ValueError (недопустиме значення), TypeError (не підтримується)  
✅ **input()** завжди повертає рядок!

---

## Практичні завдання

1. **Калькулятор віку**

    - Запитайте рік народження
    - Обчисліть вік

2. **Конвертер одиниць**

    - Метри ↔ фути
    - Кілограми ↔ фунти
    - Celsius ↔ Fahrenheit

3. **Калькулятор**
    - Запитайте два числа
    - Запитайте операцію (+, -, \*, /)
    - Виведіть результат

---

## Домашнє завдання

**Завдання 1:**
Напишіть програму, яка запитує два числа і виводить їх суму, різницю, добуток та частку.

**Завдання 2:**
Створіть конвертер температури, який працює в обидві сторони (Celsius ↔ Fahrenheit).

**Завдання 3:**
Напишіть програму, яка запитує число і виводить його в усіх системах числення (bin, oct, hex).

---

# Дякую за увагу!

**Питання?**

_"Перетворення типів — основа взаємодії з користувачем і обробки даних"_

---

## Додаткові ресурси

📚 **Документація:**

-   [Built-in Functions](https://docs.python.org/3/library/functions.html)
-   [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
-   [String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)

🎓 **Практика:**

-   [Python Type Conversion](https://www.programiz.com/python-programming/type-conversion-and-casting)
-   [Real Python: Python Type Checking](https://realpython.com/python-type-checking/)

**Експериментуйте з типами!**
