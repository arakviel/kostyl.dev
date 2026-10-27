# Текст до презентації: Перетворення типів даних у Python

## Слайд 1: Титульний слайд
**Тема:** Перетворення типів даних у Python

**Текст:**
Доброго дня! Сьогодні ми вивчимо одну з найважливіших концепцій у програмуванні — перетворення типів даних (Type Conversion або Casting). Це та тема, яка викликає багато помилок у початківців, але коли ви зрозумієте принципи, все стане простим і логічним.

Кожна мова програмування має типи даних: числа, рядки, булеві значення тощо. Python — не виняток. Але що робити, коли вам потрібно число, а у вас є рядок? Або навпаки? Ось тут і приходить на допомогу перетворення типів.

Уявіть: користувач вводить свій вік. Функція `input()` завжди повертає рядок. Але щоб порівняти вік з числом 18, потрібно перетворити рядок у число. Або навпаки: ви хочете вивести повідомлення "Вам 25 років" — тут потрібно число перетворити в рядок для об'єднання.

**Чому це критично важливо:**
1. Взаємодія з користувачем (`input()` повертає рядок)
2. Обробка даних з файлів, бази даних, API
3. Математичні операції вимагають чисел, не рядків
4. Запобігання помилкам TypeError і ValueError

Сьогодні ми детально розглянемо всі способи перетворення типів у Python і навчимося уникати типових помилок.

---

## Слайд 2: Що таке перетворення типів?

**Текст:**
Почнемо з визначення. **Перетворення типів** (також називають "type casting" або просто "casting") — це процес зміни типу даних з одного на інший.

**Проста аналогія:**
Уявіть, що у вас є книга англійською мовою, а вам потрібна українською. Ви перекладаєте її — це і є "перетворення". Зміст залишається той самий (чи майже той самий), але форма (мова) змінюється.

**Приклад 1: Рядок → Число**
```python
age_str = "25"          # Це рядок (текст)
age_int = int(age_str)  # Тепер це число
print(age_int + 5)      # 30 (числове додавання)
```

Без перетворення:
```python
age_str = "25"
print(age_str + 5)      # ❌ TypeError: can only concatenate str to str
```

**Приклад 2: Число → Рядок**
```python
count = 100             # Це число
message = "Count: " + str(count)  # Перетворили в рядок
print(message)          # "Count: 100"
```

Без перетворення:
```python
count = 100
message = "Count: " + count  # ❌ TypeError
```

**Чому це потрібно:**

1. **Input завжди рядок:**
   ```python
   age = input("Enter age: ")  # Завжди str, навіть якщо ввели "25"
   ```

2. **Різні операції вимагають різних типів:**
   - Математика: потрібні числа (int, float)
   - Конкатенація (об'єднання рядків): потрібні рядки (str)

3. **Обмін даними:**
   - Файли зберігають текст → потрібно перетворити в числа
   - API повертають дані у текстовому форматі → потрібно перетворити

**Два типи перетворення:**
Python підтримує два підходи:
1. **Неявне** (implicit) — Python робить автоматично
2. **Явне** (explicit) — ви контролюєте через функції

Розглянемо обидва детально!

---

## Слайд 3: Явне vs Неявне перетворення

**Текст:**
Розберемо відмінності між явним і неявним перетворенням типів.

### Неявне перетворення (Implicit Type Conversion)

Python іноді автоматично перетворює типи, щоб операція була можливою. Це називається **type coercion** (примус типів).

**Приклад:**
```python
x = 5        # int
y = 2.5      # float
z = x + y    # Що буде?
```

Python бачить: "int + float". Він знає, що float може представити будь-яке int значення, але не навпаки. Тому Python автоматично перетворює `x` (int) у float і виконує `5.0 + 2.5 = 7.5`.

```python
print(z)         # 7.5
print(type(z))   # <class 'float'>
```

**Правило неявного перетворення:**
Python перетворює "менш точний" тип у "більш точний":
- int → float (завжди можливо)
- bool → int (True = 1, False = 0)

**Інші приклади:**
```python
# bool → int
print(True + 5)      # 6 (True стає 1)
print(False * 10)    # 0 (False стає 0)

# int → float у порівняннях
print(5 == 5.0)      # True (5 автоматично стає 5.0)
```

**Важливо:** Python НЕ перетворює автоматично між int/float і str!
```python
print("Age: " + 25)  # ❌ TypeError
# Чому? Бо Python не знає, що ви хочете: "Age: 25" (рядок) чи помилку?
```

### Явне перетворення (Explicit Type Conversion)

Це коли **ви** явно кажете Python: "Перетвори це значення в той тип". Це робиться через вбудовані функції:

```python
x = "123"        # str
y = int(x)       # Явно перетворюємо в int
print(y + 10)    # 133
```

**Переваги явного перетворення:**
1. **Читабельність** — зрозуміло, що відбувається
2. **Контроль** — ви керуєте, коли і як перетворювати
3. **Передбачуваність** — код працює так, як ви очікуєте

**Правило Python (PEP 20):**
> "Явне краще за неявне" (Explicit is better than implicit)

Це означає: навіть якщо Python може щось зробити автоматично, краще робити явно, щоб код був зрозумілим.

---

## Слайд 4: Неявне перетворення типів

**Текст:**
Розглянемо детальніше, коли Python автоматично перетворює типи.

### Арифметичні операції з int і float

**Правило:** Якщо в операції беруть участь int і float, результат завжди float.

```python
print(5 + 2.5)       # 7.5 (float)
print(10 - 3.0)      # 7.0 (float)
print(4 * 1.5)       # 6.0 (float)
print(9 / 3.0)       # 3.0 (float)
```

**Чому так?**
Float може представити будь-яке ціле число (з деякими обмеженнями точності), але int не може представити дробові числа. Тому Python обирає float як "безпечніший" варіант.

### Спеціальний випадок: Ділення

У Python 3 звичайне ділення **завжди** повертає float, навіть якщо ділиться нацело:

```python
print(10 / 2)        # 5.0 (не 5!)
print(type(10 / 2))  # <class 'float'>
```

Це може здатися дивним, але це навмисна зміна в Python 3 для уникнення плутанини.

**Для цілочисельного ділення використовуйте `//`:**
```python
print(10 // 2)       # 5 (int)
print(9 // 2)        # 4 (int, дробова частина відкидається)
```

### Boolean у арифметиці

Bool — це насправді підтип int (True = 1, False = 0). Тому bool автоматично перетворюється в int у математичних операціях:

```python
print(True + 5)      # 6 (True = 1)
print(False + 10)    # 10 (False = 0)
print(True * 3)      # 3
print(True + True)   # 2
```

### Порівняння між типами

Python дозволяє порівнювати int і float:

```python
print(5 == 5.0)      # True (5 автоматично стає 5.0 для порівняння)
print(3 < 3.5)       # True
print(10 >= 10.0)    # True
```

Але типи все одно різні:
```python
print(type(5) == type(5.0))  # False
```

### Що НЕ перетворюється автоматично

Python НЕ робить неявне перетворення між:
- **str і int/float:**
  ```python
  "5" + 3          # ❌ TypeError
  "Age: " + 25     # ❌ TypeError
  ```

**Чому?**
Бо неочевидно, що вибрати. Наприклад, `"5" + 3`:
- "53" (рядкова конкатенація)?
- 8 (числове додавання)?
- Помилка?

Python обирає помилку, щоб ви явно сказали, що хочете.

---

## Слайд 5: Неявне перетворення: Приклади

**Текст:**
Ще кілька цікавих прикладів неявного перетворення.

### Bool → Int автоматично

```python
# У математиці
result = True + False + True + True
print(result)  # 3 (1 + 0 + 1 + 1)

# У множенні
print(True * 100)  # 100
print(False * 100) # 0
```

### Bool → Float

```python
print(True + 2.5)    # 3.5 (True → 1 → 1.0)
print(False + 0.5)   # 0.5 (False → 0 → 0.0)
```

### У порівняннях

```python
# Int і float порівнюються за значенням
print(5 == 5.0)      # True
print(3 < 3.1)       # True

# Bool і int
print(True == 1)     # True
print(False == 0)    # True
print(True > False)  # True (1 > 0)
```

### Складніші випадки

```python
# Комбінація типів
x = True + 5 + 2.5   # 1 + 5 + 2.5 = 8.5
print(x)             # 8.5 (float)
print(type(x))       # <class 'float'>

# У функціях
import math
print(math.sqrt(True))   # 1.0 (True → 1 → 1.0)
```

### Що НЕ працює

Пам'ятайте, рядки НЕ перетворюються автоматично:

```python
# ❌ Всі ці приклади викличуть TypeError:
# print("5" + 3)
# print("Hello" * "3")
```

**Правило:** Якщо сумніваєтесь, робіть явне перетворення!

---

## Слайд 6: Функції перетворення типів

**Текст:**
Python надає набір вбудованих функцій для явного перетворення типів. Це функції-конструктори класів.

### Основні функції

| Функція | Тип результату | Призначення |
|---------|----------------|-------------|
| `int()` | `<class 'int'>` | Перетворює в ціле число |
| `float()` | `<class 'float'>` | Перетворює в число з рухомою крапкою |
| `str()` | `<class 'str'>` | Перетворює в рядок |
| `bool()` | `<class 'bool'>` | Перетворює в булеве значення |

### Основні принципи

1. **Функція називається як тип:**
   - Хочете int → викликайте `int()`
   - Хочете str → викликайте `str()`

2. **Може викинути помилку:**
   - ValueError — якщо значення не може бути перетворене
   - TypeError — якщо тип не підтримує перетворення

3. **Повертає новий об'єкт:**
   ```python
   x = "123"
   y = int(x)
   print(x)  # "123" (оригінал не змінився)
   print(y)  # 123 (новий об'єкт)
   ```

### Загальний синтаксис

```python
new_value = type_function(original_value)
```

Приклади:
```python
age = int("25")           # str → int
price = float("19.99")    # str → float
message = str(100)        # int → str
is_valid = bool(1)        # int → bool
```

### Коли використовувати

1. **Input від користувача:**
   ```python
   age = int(input("Enter age: "))
   ```

2. **Формування виводу:**
   ```python
   count = 42
   print("Total: " + str(count))
   # Краще:
   print(f"Total: {count}")
   ```

Тепер розглянемо кожну функцію детально!

---

## Слайд 7: Перетворення в int()

**Текст:**
Функція `int()` — одна з найчастіше використовуваних. Вона перетворює значення в ціле число.

### З рядка (string → int)

```python
print(int("123"))        # 123
print(int("-456"))       # -456
print(int("+789"))       # 789 (знак + опціональний)
```

**Правила:**
- Рядок має містити ТІЛЬКИ цифри (і опціональний знак +/- на початку)
- Пробіли на початку/кінці дозволені
- Інші символи викличуть ValueError

```python
# ✅ Працює
int("  123  ")       # 123 (пробіли ОК)
int("+42")           # 42

# ❌ ValueError
# int("12.5")        # Крапка заборонена
# int("1 2 3")       # Пробіли всередині заборонені
# int("abc")         # Літери заборонені
# int("")            # Порожній рядок заборонений
```

### З float (float → int)

**Важливо:** `int()` **відкидає** дробову частину, не округлює!

```python
print(int(3.14))     # 3 (не 4!)
print(int(9.99))     # 9 (не 10!)
print(int(-2.7))     # -2 (не -3!)
```

Це називається "truncation" (усічення) — просто відкидається все після крапки.

**Якщо потрібне округлення:**
```python
print(round(3.14))   # 3 (математичне округлення)
print(round(3.7))    # 4
print(round(9.5))    # 10 (округлення до найближчого парного)

import math
print(math.floor(3.7))   # 3 (округлення вниз)
print(math.ceil(3.1))    # 4 (округлення вгору)
```

### З bool (bool → int)

```python
print(int(True))     # 1
print(int(False))    # 0
```

Це працює, бо bool — підтип int.

### З None

```python
# int(None)          # ❌ TypeError
```

Python не знає, як перетворити None в int.

### Практичні приклади

```python
# Input від користувача
age_str = input("Enter your age: ")
age = int(age_str)
print(f"Next year you'll be {age + 1}")

# Обчислення
number_str = "42"
count = int(number_str)
result = count * 2
print(result)  # 84
```

---

## Слайд 8: int(): Системи числення

**Текст:**
Одна з потужних можливостей `int()` — перетворення рядків з різних систем числення в десяткову.

### Синтаксис

```python
int(string, base)
```

- `string` — рядок з числом
- `base` — основа системи числення (2-36)

### Двійкова система (binary, base=2)

```python
print(int("1010", 2))        # 10 (у десятковій)
print(int("1111", 2))        # 15
print(int("10000000", 2))    # 128

# З префіксом (опціонально)
print(int("0b1010", 2))      # 10
```

**Як це працює:**
`"1010"` у двійковій = 1×2³ + 0×2² + 1×2¹ + 0×2⁰ = 8 + 0 + 2 + 0 = 10

### Вісімкова система (octal, base=8)

```python
print(int("12", 8))          # 10 (у десятковій)
print(int("77", 8))          # 63
print(int("100", 8))         # 64

# З префіксом
print(int("0o12", 8))        # 10
```

**Як це працює:**
`"12"` у вісімковій = 1×8¹ + 2×8⁰ = 8 + 2 = 10

### Шістнадцяткова система (hexadecimal, base=16)

```python
print(int("A", 16))          # 10
print(int("FF", 16))         # 255
print(int("1A3", 16))        # 419

# З префіксом
print(int("0xFF", 16))       # 255

# Регістр не важливий
print(int("ff", 16))         # 255
print(int("FF", 16))         # 255
```

**Як це працює:**
`"FF"` у hex = 15×16¹ + 15×16⁰ = 240 + 15 = 255

### Автоматичне визначення основи (base=0)

Якщо base=0, Python визначає систему за префіксом:

```python
print(int("0b1010", 0))      # 10 (бінарна)
print(int("0o12", 0))        # 10 (вісімкова)
print(int("0xA", 0))         # 10 (hex)
print(int("10", 0))          # 10 (десяткова, немає префікса)
```

### Практичне застосування

```python
# Перетворення hex кольору
hex_color = "FF"
red_value = int(hex_color, 16)
print(red_value)  # 255
```

---

## Слайд 9: int(): Помилки

**Текст:**
Не всі значення можна перетворити в int. Розберемо типові помилки.

### ValueError — недопустимий формат

Це найпоширеніша помилка при використанні `int()`.

**1. Дробове число у рядку:**
```python
# int("12.5")        # ❌ ValueError: invalid literal for int()
```

Чому? Бо `int()` очікує ТІЛЬКИ цілі числа у рядку.

**Рішення:** Спочатку в float, потім в int:
```python
print(int(float("12.5")))   # ✅ 12
```

**2. Літери або інші символи:**
```python
# int("abc")         # ❌ ValueError
# int("12a")         # ❌ ValueError (літера в кінці)
# int("12.0")        # ❌ ValueError (крапка заборонена)
```

**3. Пробіли всередині:**
```python
# int("1 2 3")       # ❌ ValueError
int("12 ")           # ✅ OK (пробіли в кінці допустимі)
int(" 12")           # ✅ OK (пробіли на початку допустимі)
```

**4. Порожній рядок:**
```python
# int("")            # ❌ ValueError
```

**5. Підкреслення у рядках:**
```python
# int("1_000_000")   # ❌ ValueError
# Підкреслення працюють у літералах, але не в рядках!
```

**Рішення:** Видалити підкреслення:
```python
print(int("1_000_000".replace("_", "")))  # ✅ 1000000
```

**6. Експоненційний запис:**
```python
# int("1e6")         # ❌ ValueError
```

**Рішення:** Через float:
```python
print(int(float("1e6")))    # ✅ 1000000
```

### TypeError — не підтримується

Це помилка типу, коли `int()` не знає, як перетворити об'єкт.

```python
# int(None)          # ❌ TypeError
```

---

## Слайд 10: int(): Цікаві випадки

**Текст:**
Розглянемо деякі нетривіальні випадки використання `int()`.

### Пробіли

Пробіли на початку і в кінці **ігноруються**:

```python
print(int("  123  "))    # 123 ✅
print(int("\t456\n"))    # 456 ✅ (табуляція і новий рядок теж ігноруються)
```

Але пробіли **всередині** викликають ValueError:
```python
# print(int("1 2 3"))    # ❌ ValueError
```

### Знаки + і -

```python
print(int("+123"))       # 123 ✅
print(int("-123"))       # -123 ✅
# print(int("+ 123"))    # ❌ ValueError (пробіл після знака)
```

### Нуль з різними префіксами

```python
print(int("0"))          # 0 ✅
print(int("00"))         # 0 ✅ (провідні нулі ОК)
print(int("000123"))     # 123 ✅
```

Але будьте обережні з вісімковою системою:
```python
print(int("010"))        # 10 (десяткова), не 8!
print(int("010", 8))     # 8 (вісімкова)
```

### Дуже великі числа

Python int має необмежений розмір (обмежений лише пам'яттю):

```python
huge = int("99999999999999999999999999999999")
print(huge)              # Працює!
print(huge + 1)          # Теж працює!
```

### Експоненційний запис

`int()` НЕ розуміє експоненційний запис:

```python
# int("1e6")             # ❌ ValueError
```

**Рішення:** Спочатку в float:
```python
print(int(float("1e6")))        # ✅ 1000000
print(int(float("3.5e2")))      # ✅ 350
```

---

## Слайд 11: Перетворення в float()

**Текст:**
Функція `float()` перетворює значення в число з рухомою крапкою (floating-point number).

### З рядка (string → float)

```python
print(float("3.14"))         # 3.14
print(float("-0.5"))         # -0.5
print(float("2.5e3"))        # 2500.0 (експоненційний запис)
```

**На відміну від int(), float() дозволяє:**
- Крапку (десятковий роздільник)
- Експоненційний запис (1e6, 2.5e-3)
- Спеціальні значення ("inf", "nan")

**Приклади:**
```python
print(float(".5"))           # 0.5 (можна опустити 0 перед крапкою)
print(float("2."))           # 2.0 (можна опустити 0 після крапки)
print(float("  3.14  "))     # 3.14 (пробіли ігноруються)
```

### З int (int → float)

```python
print(float(5))              # 5.0
print(float(-3))             # -3.0
print(float(0))              # 0.0
```

Це завжди працює, бо будь-яке int можна представити як float (з деякими обмеженнями для дуже великих чисел).

### З bool (bool → float)

```python
print(float(True))           # 1.0
print(float(False))          # 0.0
```

### Спеціальні float значення

Python підтримує IEEE 754 спеціальні значення:

**1. Нескінченність (Infinity):**
```python
inf = float("inf")
neg_inf = float("-inf")

print(inf)                   # inf
print(neg_inf)               # -inf
print(inf > 1000000000)      # True (inf більше за все)
print(-inf < -1000000000)    # True

# Арифметика
print(1 / inf)               # 0.0
print(inf + 1)               # inf
print(inf * 2)               # inf
```

**2. Не-число (Not a Number — NaN):**
```python
nan = float("nan")

print(nan)                   # nan
print(nan == nan)            # False (!)
print(nan != nan)            # True (!!)

# NaN не дорівнює навіть самому собі!
# Це особливість IEEE 754
```

**Перевірка спеціальних значень:**
```python
import math

print(math.isinf(inf))       # True
print(math.isnan(nan))       # True
print(math.isfinite(3.14))   # True
print(math.isfinite(inf))    # False
```

### З None

```python
# float(None)                # ❌ TypeError
```

### Практичні приклади

```python
# Input від користувача
price_str = input("Enter price: ")
price = float(price_str)
tax = price * 0.2
total = price + tax
print(f"Total with tax: {total:.2f}")

# Наукові обчислення
speed_of_light = float("3e8")  # 300 000 000 м/с
distance = speed_of_light * 60  # Відстань за 60 секунд
print(f"Light travels {distance:.2e} meters in 60 seconds")
```

---

## Слайд 12: float(): Спеціальні значення

**Текст:**
Детальніше про спеціальні float значення в Python.

### Infinity (Нескінченність)

**Створення:**
```python
inf = float("inf")
neg_inf = float("-inf")
# або
import math
inf = math.inf
neg_inf = -math.inf
```

**Властивості:**
```python
# Порівняння
print(inf > 10**100)         # True
print(inf == float("inf"))   # True
print(inf > neg_inf)         # True

# Арифметика
print(inf + 100)             # inf
print(inf * 2)               # inf
print(inf - 1000)            # inf
print(1 / inf)               # 0.0
```

**Практичне застосування:**
```python
# Ініціалізація для пошуку мінімуму
minimum = float("inf")
numbers = [5, 2, 8, 1, 9]

# (тут буде цикл пізніше, коли вивчите)
# Поки що просто розуміємо концепцію
```

### NaN (Not a Number)

**Створення:**
```python
nan = float("nan")
# або
import math
nan = math.nan
```

**Унікальна властивість — NaN ≠ NaN:**
```python
nan = float("nan")
print(nan == nan)            # False (!)
print(nan != nan)            # True (!)
print(nan is nan)            # True (той самий об'єкт)
```

Чому так? Це визначено стандартом IEEE 754. NaN означає "невизначений результат", і два невизначені результати не обов'язково рівні.

**Перевірка на NaN:**
```python
import math

x = float("nan")
print(x == float("nan"))     # False (не працює!)
print(math.isnan(x))         # True (правильний спосіб)
```

**Арифметика з NaN:**
```python
nan = float("nan")
print(nan + 5)               # nan
print(nan * 2)               # nan
print(nan / 2)               # nan
```

### Перевірка спеціальних значень

```python
import math

x = 3.14
print(math.isnan(x))         # False
print(math.isinf(x))         # False
print(math.isfinite(x))      # True

x = float("inf")
print(math.isinf(x))         # True
print(math.isfinite(x))      # False

x = float("nan")
print(math.isnan(x))         # True
```

---

## Слайд 13: float(): Експоненційний запис

**Текст:**
Функція `float()` підтримує науковий (експоненційний) запис чисел.

### Формат

**Загальний формат:** `аЕb` або `аеb` означає `а × 10^b`

```python
print(float("1e6"))          # 1000000.0 (1 × 10⁶)
print(float("1.5e3"))        # 1500.0 (1.5 × 10³)
print(float("2.5e-4"))       # 0.00025 (2.5 × 10⁻⁴)
```

### Великі числа

```python
# Швидкість світла (м/с)
c = float("3e8")
print(c)                     # 300000000.0

# Відстань до Місяця (м)
moon_distance = float("3.844e8")
print(moon_distance)         # 384400000.0

# Число Авогадро
avogadro = float("6.022e23")
print(avogadro)              # 6.022e+23
```

### Малі числа

```python
# Маса електрона (кг)
electron_mass = float("9.109e-31")
print(electron_mass)         # 9.109e-31

# Постійна Планка
planck = float("6.626e-34")
print(planck)                # 6.626e-34

# Мікросекунда (секунди)
microsecond = float("1e-6")
print(microsecond)           # 1e-06
```

### Регістр не важливий

```python
print(float("1E6"))          # 1000000.0
print(float("1e6"))          # 1000000.0
# Обидва варіанти працюють однаково
```

### Переповнення (Overflow)

Якщо число занадто велике, отримаємо inf:

```python
print(float("1e308"))        # 1e+308 ✅ (майже максимум)
print(float("1e309"))        # inf (переповнення!)
print(float("-1e309"))       # -inf
```

**Діапазон float у Python:**
- Мінімальне додатне: ~2.2e-308
- Максимальне: ~1.8e+308

```python
import sys
print(sys.float_info.min)    # 2.2250738585072014e-308
print(sys.float_info.max)    # 1.7976931348623157e+308
```

---

## Слайд 14: float(): Помилки

**Текст:**
Розберемо типові помилки при використанні `float()`.

### ValueError — недопустимий формат

**1. Кома замість крапки:**
```python
# float("19,99")           # ❌ ValueError
```

У Python десятковий роздільник — це **крапка** (`.`), не кома (`,`).

**Рішення:**
```python
print(float("19.99"))               # ✅ 19.99
# Або замінити кому:
print(float("19,99".replace(",", ".")))  # ✅ 19.99
```

**2. Дві крапки:**
```python
# float("12.34.56")        # ❌ ValueError
```

**3. Порожній рядок:**
```python
# float("")                # ❌ ValueError
```

**4. Літери:**
```python
# float("abc")             # ❌ ValueError
# float("12.3abc")         # ❌ ValueError
```

**5. Пробіли всередині:**
```python
# float("12 . 34")         # ❌ ValueError
# float("12 34")           # ❌ ValueError
```

Але пробіли на початку/кінці ОК:
```python
print(float("  12.34  "))           # ✅ 12.34
```

### TypeError — не підтримується

```python
# float(None)              # ❌ TypeError
```

### Особливі випадки

```python
# inf та nan — валідні
print(float("inf"))                 # ✅ inf
print(float("-infinity"))           # ✅ -inf
print(float("nan"))                 # ✅ nan

# Але будьте обережні:
x = float("nan")
# (x == float("nan"))      # False (не працює!)

# Правильно:
import math
print(math.isnan(x))                # True
```

---

## Слайд 15: Перетворення в str()

**Текст:**
Функція `str()` перетворює будь-яке значення в рядок (string).

### Універсальність str()

`str()` — найбезпечніша функція перетворення. Вона працює з **будь-яким** типом і ніколи не викидає ValueError.

### З чисел

```python
# Int
print(str(123))              # "123"
print(str(-456))             # "-456"
print(str(0))                # "0"

# Float
print(str(3.14))             # "3.14"
print(str(-0.5))             # "-0.5"
print(str(1e6))              # "1000000.0"
print(str(1e-6))             # "1e-06" (експоненційний формат)
```

### З булевих значень

```python
print(str(True))             # "True"
print(str(False))            # "False"
```

**Важливо:** Результат — рядок "True" або "False", не булеве значення!

```python
x = str(True)
print(type(x))               # <class 'str'>
print(x == True)             # False (рядок != bool)
print(x == "True")           # True
```

### З None

```python
print(str(None))             # "None"
```

### Спеціальні float значення

```python
print(str(float("inf")))     # "inf"
print(str(float("-inf")))    # "-inf"
print(str(float("nan")))     # "nan"
```

### str() ніколи не викидає помилку

На відміну від `int()` та `float()`, `str()` завжди повертає щось:

```python
print(str(None))             # "None" ✅
```

Це робить `str()` безпечним для логування і виведення.

### Практичні приклади

```python
# Конкатенація (об'єднання рядків)
age = 25
message = "Age: " + str(age)
print(message)               # "Age: 25"

# Краще використовувати f-strings:
message = f"Age: {age}"      # Простіше і швидше

# Виведення чисел
count = 42
print("Total: " + str(count))
print(f"Total: {count}")     # Краще
```

---

## Слайд 16: str(): Форматування

**Текст:**
Для більшого контролю над форматом рядків використовуйте f-strings.

### F-strings (Python 3.6+)

**Найсучасніший і рекомендований спосіб:**

```python
name = "Alice"
age = 25
print(f"Name: {name}, Age: {age}")  # "Name: Alice, Age: 25"
```

**Форматування чисел:**

```python
# Кількість знаків після коми
pi = 3.14159265359
print(f"{pi:.2f}")           # "3.14" (2 знаки)
print(f"{pi:.5f}")           # "3.14159" (5 знаків)

# Ширина поля
num = 42
print(f"{num:5d}")           # "   42" (ширина 5, вирівнювання праворуч)
print(f"{num:05d}")          # "00042" (заповнення нулями)

# Експоненційний формат
large = 1000000
print(f"{large:e}")          # "1.000000e+06"
print(f"{large:.2e}")        # "1.00e+06" (2 знаки після коми)
```

**Системи числення:**

```python
num = 42
print(f"{num:b}")            # "101010" (двійкова, без префікса)
print(f"{num:o}")            # "52" (вісімкова)
print(f"{num:x}")            # "2a" (hex, малі літери)
print(f"{num:X}")            # "2A" (hex, великі літери)
print(f"{num:#x}")           # "0x2a" (з префіксом)
```

**Вирівнювання:**

```python
text = "Python"
print(f"{text:<10}")         # "Python    " (ліворуч, ширина 10)
print(f"{text:>10}")         # "    Python" (праворуч)
print(f"{text:^10}")         # "  Python  " (центр)
print(f"{text:*^10}")        # "**Python**" (центр, заповнення *)
```

**Відсотки:**

```python
ratio = 0.85
print(f"{ratio:.2%}")        # "85.00%" (автоматично × 100)
```

**Тисячні роздільники:**

```python
big_num = 1000000
print(f"{big_num:,}")        # "1,000,000" (з комами)
print(f"{big_num:_}")        # "1_000_000" (з підкресленнями)
```

---

## Слайд 17: Перетворення в bool()

**Текст:**
Функція `bool()` перетворює значення в булеве (True або False).

### Хибні (Falsy) значення

У Python є рівно **5 типів хибних базових значень**. Все інше — істинне!

**Список Falsy значень:**

1. **None**
   ```python
   print(bool(None))         # False
   ```

2. **False** (очевидно)
   ```python
   print(bool(False))        # False
   ```

3. **Нульові числа:**
   ```python
   print(bool(0))            # False (int)
   print(bool(0.0))          # False (float)
   ```

4. **Порожній рядок:**
   ```python
   print(bool(""))           # False
   ```

**Всі інші значення — True!**

### Істинні (Truthy) значення

```python
# Ненульові числа
print(bool(1))               # True
print(bool(-1))              # True
print(bool(0.1))             # True
print(bool(-100))            # True

# Непорожні рядки
print(bool("0"))             # True (рядок "0", не число!)
print(bool("False"))         # True (рядок "False", не bool!)
print(bool(" "))             # True (пробіл — непорожній рядок)
```

### Класична пастка

```python
# Рядок "False" — це True!
x = "False"
print(bool(x))               # True (непорожній рядок)

# Правильна конверсія рядка в bool:
x = "False"
value = x == "True"          # False
# або
value = x.lower() == "true"  # False
```

### Практичні приклади

```python
# Перевірка на порожній рядок
user_input = input("Enter name: ")
has_name = bool(user_input)
print(f"Has name: {has_name}")

# Перевірка на нуль
value = 0
is_positive = bool(value)
print(f"Is positive: {is_positive}")  # False
```

---

## Слайд 18: bool(): Цікаві випадки

**Текст:**
Деякі несподівані випадки з `bool()`.

### Рядок "False" — це True!

```python
print(bool("False"))         # True (!!)
print(bool("0"))             # True (!!)
print(bool(""))              # False (порожній)
```

Чому? Бо "False" — непорожній рядок, а всі непорожні рядки є truthy.

### Числа: Тільки 0 — False

```python
# Всі ненульові числа — True
print(bool(1))               # True
print(bool(-1))              # True
print(bool(0.1))             # True
print(bool(-1000))           # True

# Тільки нуль — False
print(bool(0))               # False
print(bool(0.0))             # False
print(bool(-0.0))            # False (нуль є нуль)
```

### Спеціальні float значення

```python
import math

print(bool(float("inf")))    # True
print(bool(float("-inf")))   # True
print(bool(float("nan")))    # True (!!)
```

Так, навіть NaN (Not a Number) — truthy!

---

## Слайд 19: Перетворення між системами числення

**Текст:**
Розглянемо детально перетворення чисел між різними системами числення.

### З десяткової в інші системи

Python має три функції для конверсії:

```python
num = 42

# В двійкову
binary = bin(num)
print(binary)                # "0b101010" (з префіксом)
print(bin(num)[2:])          # "101010" (без префікса)

# В вісімкову
octal = oct(num)
print(octal)                 # "0o52"
print(oct(num)[2:])          # "52"

# В шістнадцяткову
hexadecimal = hex(num)
print(hexadecimal)           # "0x2a"
print(hex(num)[2:])          # "2a"
```

**Важливо:** Ці функції повертають **рядки**, не числа!

```python
x = bin(42)
print(type(x))               # <class 'str'>
```

### З інших систем в десяткову

Використовуємо `int()` з параметром `base`:

```python
# З двійкової
print(int("101010", 2))      # 42
print(int("0b101010", 2))    # 42 (з префіксом теж працює)

# З вісімкової
print(int("52", 8))          # 42
print(int("0o52", 8))        # 42

# З шістнадцяткової
print(int("2A", 16))         # 42
print(int("2a", 16))         # 42 (регістр не важливий)
print(int("0x2a", 16))       # 42
```

### Між недесятковими системами

Завжди через десяткову:

```python
# Двійкова → Шістнадцяткова
binary = "11111111"
decimal = int(binary, 2)    # 255
hexadecimal = hex(decimal)  # "0xff"

# Або в один рядок:
hexadecimal = hex(int(binary, 2))
print(hexadecimal)           # "0xff"
```

### Практичні приклади

```python
# Конвертер hex кольорів
hex_color = "FF5733"
r = int(hex_color[0:2], 16)  # FF → 255
g = int(hex_color[2:4], 16)  # 57 → 87
b = int(hex_color[4:6], 16)  # 33 → 51
print(f"RGB: ({r}, {g}, {b})")  # RGB: (255, 87, 51)
```

---

## Слайд 20: Символи та коди: ord() та chr()

**Текст:**
Функції `ord()` та `chr()` дозволяють працювати з Unicode кодами символів.

### chr() — Код → Символ

**Синтаксис:** `chr(code)` — повертає символ з Unicode кодом `code`

```python
# ASCII символи
print(chr(65))               # 'A' (код 65)
print(chr(97))               # 'a' (код 97)
print(chr(48))               # '0' (код 48)

# Різниця між великими і малими літерами
print(chr(65))               # 'A'
print(chr(97))               # 'a' (65 + 32 = 97)

# Спеціальні символи
print(chr(32))               # ' ' (пробіл)
print(chr(10))               # '\n' (новий рядок)
print(chr(9))                # '\t' (табуляція)
```

### Unicode символи

Python підтримує весь Unicode (понад 140 000 символів):

```python
# Кирилиця
print(chr(1040))             # 'А' (велика А)
print(chr(1072))             # 'а' (мала а)
print(chr(1030))             # 'І' (українська І)
print(chr(1031))             # 'Ї' (українська Ї)

# Emoji
print(chr(128512))           # '😀' (smile)
print(chr(128516))           # '😄' (laugh)
print(chr(128077))           # '👍' (thumbs up)

# Математичні символи
print(chr(8734))             # '∞' (нескінченність)
print(chr(960))              # 'π' (пі)
```

### ord() — Символ → Код

**Синтаксис:** `ord(char)` — повертає Unicode код символу `char`

```python
# ASCII
print(ord('A'))              # 65
print(ord('Z'))              # 90
print(ord('a'))              # 97
print(ord('z'))              # 122
print(ord('0'))              # 48
print(ord('9'))              # 57

# Спеціальні
print(ord(' '))              # 32 (пробіл)
print(ord('\n'))             # 10 (новий рядок)
print(ord('\t'))             # 9 (табуляція)

# Кирилиця
print(ord('А'))              # 1040
print(ord('Я'))              # 1071
print(ord('Ї'))              # 1031

# Emoji
print(ord('😀'))             # 128512
print(ord('👍'))             # 128077
```

### ord() приймає ТІЛЬКИ один символ

```python
print(ord('A'))              # ✅ 65
# ord('AB')                  # ❌ TypeError: ord() expected a character
# ord('')                    # ❌ TypeError: ord() expected a character
```

### Діапазони символів

```python
# Великі літери A-Z
print(ord('A'), ord('Z'))    # 65 90

# Малі літери a-z
print(ord('a'), ord('z'))    # 97 122

# Цифри 0-9
print(ord('0'), ord('9'))    # 48 57

# Українська абетка
print(ord('А'), ord('Я'))    # 1040 1071
print(ord('а'), ord('я'))    # 1072 1103
```

---

## Слайд 21: Робота з input()

**Текст:**
`input()` завжди повертає **рядок**, навіть якщо користувач ввів число.

### Проблема

```python
# ❌ Неправильно
age = input("Enter age: ")
print(age + 5)              # TypeError (рядок + число)

# Що відбувається:
# Користувач вводить: 25
# age = "25" (це рядок!)
# "25" + 5 → TypeError
```

### Рішення

```python
# ✅ Правильно
age = int(input("Enter age: "))
print(age + 5)              # Працює!

# Що відбувається:
# Користувач вводить: 25
# input() повертає "25"
# int("25") → 25
# 25 + 5 → 30
```

### Практичні приклади

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

**Приклад 3: Калькулятор площі**
```python
radius = float(input("Enter radius: "))
pi = 3.14159
area = pi * radius ** 2
print(f"Area: {area:.2f}")
```

### Перевірка типу

```python
value = input("Enter value: ")
print(f"Type: {type(value)}")       # завжди <class 'str'>
print(f"Is digit: {value.isdigit()}")
```

---

## Слайд 22: Таблиця сумісності перетворень

**Текст:**
Узагальнимо, які перетворення можливі між типами.

| З / В | int | float | str | bool |
|-------|-----|-------|-----|------|
| **int** | — | ✅ Завжди | ✅ Завжди | ✅ Завжди |
| **float** | ✅ Відкидає дроб | — | ✅ Завжди | ✅ Завжди |
| **str** | ✅ Може ValueError | ✅ Може ValueError | — | ✅ Завжди |
| **bool** | ✅ 0 або 1 | ✅ 0.0 або 1.0 | ✅ "True"/"False" | — |
| **None** | ❌ TypeError | ❌ TypeError | ✅ "None" | ✅ False |

**Пояснення:**

- **int → float:** Завжди працює. `int(3.7)` → `3` (відкидає дробову частину)
- **str → int/float:** Може викинути ValueError, якщо формат неправильний
- **None → bool:** Завжди `False`
- **None → str:** Завжди `"None"`

---

## Слайд 23-24: Типові помилки початківців

**Текст:**
Розглянемо найпоширеніші помилки при роботі з перетворенням типів.

### Помилка 1: Забули перетворити input()

```python
# ❌ Неправильно
age = input("Enter age: ")  # Це завжди str!
print(age + 5)              # TypeError

# ✅ Правильно
age = int(input("Enter age: "))
print(age + 5)
```

**Запам'ятайте:** `input()` **ЗАВЖДИ** повертає рядок!

### Помилка 2: int() відкидає дробову частину

```python
# ❌ Неправильне очікування
print(int(9.99))            # 9, не 10!
print(int(3.7))             # 3, не 4!

# ✅ Якщо потрібне округлення
print(round(9.99))          # 10
print(round(3.7))           # 4
```

**Запам'ятайте:** `int()` не округлює, а **відкидає** дробову частину!

### Помилка 3: float() не приймає коми

```python
# ❌ Неправильно
# price = float("19,99")    # ValueError

# ✅ Правильно
price = float("19.99")      # Крапка, не кома!
```

У Python десятковий роздільник — **крапка**, не кома!

### Помилка 4: str + int

```python
# ❌ Неправильно
# print("Age: " + 25)       # TypeError

# ✅ Правильно (варіант 1)
print("Age: " + str(25))

# ✅ Правильно (варіант 2, найкраще)
print(f"Age: {25}")
```

### Помилка 5: bool("False") → True

```python
# ❌ Неправильне очікування
x = bool("False")           # True (непорожній рядок!)

# ✅ Правильна конверсія рядка в bool
x = "False"
value = (x == "True")       # False
# або
value = (x.lower() == "true")
```

**Запам'ятайте:** Рядок "False" — це **True**, бо він непорожній!

---

## Слайд 25: Найкращі практики

**Текст:**
Рекомендації для правильної роботи з перетворенням типів.

### 1. Явне перетворення

```python
# Погано (неявне, незрозуміло)
result = "5" + str(3)

# Добре (явне)
number = 5
text = str(number) + str(3)
```

### 2. Використовуйте f-strings

```python
# Погано
print("Sum: " + str(10 + 20))

# Добре
print(f"Sum: {10 + 20}")
```

F-strings:
- Швидші
- Зручніші
- Читабельніші
- Підтримують форматування

### 3. Перевіряйте type при debug

```python
value = input("Enter value: ")
print(f"Type: {type(value)}")
print(f"Value: {value}")
```

### 4. Використовуйте змістовні імена змінних

```python
# Погано
x = input("Age: ")
y = int(x)

# Добре
age_str = input("Age: ")
age = int(age_str)
```

---

## Слайд 26-27: Практичні приклади

**Текст:**
Розглянемо реальні застосування перетворення типів.

### Приклад 1: Обчислення віку

```python
birth_year = int(input("Enter birth year: "))
current_year = 2024
age = current_year - birth_year
print(f"Your age: {age}")
```

### Приклад 2: Конвертер температури

```python
celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit:.1f}°F")

# Назад:
fahrenheit = float(input("Enter temperature in Fahrenheit: "))
celsius = (fahrenheit - 32) * 5/9
print(f"{fahrenheit}°F = {celsius:.1f}°C")
```

### Приклад 3: Калькулятор площі кола

```python
radius = float(input("Enter radius: "))
pi = 3.14159
area = pi * radius ** 2
circumference = 2 * pi * radius
print(f"Area: {area:.2f}")
print(f"Circumference: {circumference:.2f}")
```

### Приклад 4: Перевірка типу введених даних

```python
value = input("Enter value: ")
print(f"Type: {type(value)}")
print(f"Is digit: {value.isdigit()}")
print(f"Is alpha: {value.isalpha()}")
print(f"Is alnum: {value.isalnum()}")
```

---

## Слайд 28-30: Вікторини

**Текст:**
Перевіримо розуміння матеріалу.

### Вікторина 1

```python
x = "123"
y = "456"
z = int(x) + int(y)
print(z)
```

**Що буде виведено?**
- A) "123456"
- B) 579
- C) "579"
- D) TypeError

**Відповідь:** B) 579

**Пояснення:** `x` і `y` перетворені в int, тому відбувається числове додавання: 123 + 456 = 579

### Вікторина 2

```python
print(bool("False"))
```

**Що буде виведено?**
- A) True
- B) False
- C) "False"
- D) ValueError

**Відповідь:** A) True

**Пояснення:** "False" — це непорожній рядок, а всі непорожні рядки є truthy (істинними).

### Вікторина 3

```python
print(int(9.99))
```

**Що буде виведено?**
- A) 9
- B) 10
- C) 9.99
- D) ValueError

**Відповідь:** A) 9

**Пояснення:** `int()` відкидає дробову частину, не округлює! Тому 9.99 → 9, а не 10.

---

## Слайд 31: Цікаві факти

**Текст:**
Дізнайтесь цікаві особливості перетворення типів у Python.

🐍 **Факт 1:** `input()` завжди повертає **рядок**, навіть якщо ви ввели число.

🔢 **Факт 2:** `int(3.9)` дає `3`, не `4` — int() не округлює, а відкидає дробову частину!

💡 **Факт 3:** Python 3: `5 / 2` = `2.5` (float), але `5 // 2` = `2` (int, цілочисельне ділення).

⚠️ **Факт 4:** `bool("False")` = `True` — це рядок, не булеве значення! Будь-який непорожній рядок є True.

🎯 **Факт 5:** `None` не можна перетворити в int або float — викличе TypeError.

📊 **Факт 6:** Unicode: `ord('A')` = 65, `chr(65)` = 'A'. Python підтримує весь Unicode, включно з emoji!

---

## Слайд 32: Корисні функції

**Текст:**
Додаткові корисні функції для роботи з типами.

### Перевірка типу

```python
# type() — повертає тип об'єкта
print(type(123))            # <class 'int'>
print(type(3.14))           # <class 'float'>
print(type("text"))         # <class 'str'>

# isinstance() — перевіряє тип
print(isinstance(123, int)) # True
print(isinstance(123, str)) # False
```

### Перевірка рядків

```python
text = "12345"

# Методи перевірки
print(text.isdigit())       # True (тільки цифри)
print(text.isalpha())       # False (тільки літери)
print(text.isalnum())       # True (літери і цифри)

# Приклади:
print("123".isdigit())      # True
print("abc".isalpha())      # True
print("abc123".isalnum())   # True
print("   ".isspace())      # True
```

### Математичні функції

```python
# round() — округлення
print(round(3.7))           # 4
print(round(3.14159, 2))    # 3.14

# abs() — модуль (абсолютне значення)
print(abs(-5))              # 5
print(abs(-3.14))           # 3.14

# pow() — степінь
print(pow(2, 3))            # 8 (2³)
print(2 ** 3)               # 8 (те саме)
```

---

## Слайд 33: Ключові висновки

**Текст:**
Підсумуємо найважливіше про перетворення типів.

✅ **Неявне перетворення:** Python робить автоматично (int + float → float)

✅ **Явне перетворення:** int(), float(), str(), bool() — ви контролюєте

✅ **int()** — відкидає дробову частину, не округлює! int(9.99) = 9

✅ **float()** — підтримує "inf", "nan", експоненційний запис (1e6)

✅ **str()** — працює для будь-якого типу, ніколи не викидає помилку

✅ **bool()** — тільки 5 хибних базових значень (None, False, 0, 0.0, ""), всі інші — True

✅ **Помилки:** ValueError (недопустиме значення), TypeError (не підтримується)

✅ **input()** завжди повертає рядок — не забувайте перетворювати!

✅ **Використовуйте f-strings** для форматування — простіше і швидше

---

## Слайд 34-35: Практичні завдання та домашнє завдання

**Текст:**
Закріплюємо матеріал практичними завданнями.

### Практичні завдання (на уроці)

1. **Калькулятор віку:**
   - Запитайте рік народження
   - Обчисліть вік
   - Виведіть результат

2. **Конвертер одиниць:**
   - Метри ↔ фути (1 метр = 3.28084 фута)
   - Кілограми ↔ фунти (1 кг = 2.20462 фунта)
   - Celsius ↔ Fahrenheit

3. **Простий калькулятор:**
   - Запитайте два числа
   - Виведіть суму, різницю, добуток, частку

### Домашнє завдання

**Завдання 1:**
Напишіть програму, яка запитує два числа і виводить їх суму, різницю, добуток та частку з форматуванням до 2 знаків після коми.

**Завдання 2:**
Створіть конвертер температури, який:
- Запитує температуру в Celsius
- Виводить її в Fahrenheit
- І навпаки

**Завдання 3:**
Напишіть програму, яка запитує число і виводить його в усіх системах числення (binary, octal, hexadecimal) з префіксами та без.

---

## Слайд 36-37: Завершення

**Текст:**
Дякую за увагу! Сьогодні ми вивчили перетворення типів даних у Python — одну з найважливіших концепцій для роботи з даними та взаємодії з користувачем.

**Що ми дізналися:**
- Різниця між явним і неявним перетворенням
- Як працюють int(), float(), str(), bool()
- Типові помилки та як їх уникати
- Робота з різними системами числення
- Функції ord() і chr() для роботи з символами
- Правильна робота з input()

**Пам'ятайте:**
- input() завжди повертає рядок
- int() відкидає, а не округлює
- bool("False") = True (рядок!)
- Використовуйте f-strings для форматування

**Практикуйтесь!** Чим більше ви експериментуєте з перетворенням типів, тим краще зрозумієте, як вони працюють.

---

## Додаткові ресурси

📚 **Документація:**
- [Built-in Functions](https://docs.python.org/3/library/functions.html) — офіційна документація вбудованих функцій
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — типи даних у Python
- [String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods) — методи для роботи з рядками

🎓 **Навчальні матеріали:**
- [Python Type Conversion](https://www.programiz.com/python-programming/type-conversion-and-casting) — детальний туторіал
- [Real Python: Python Type Checking](https://realpython.com/python-type-checking/) — поглиблене вивчення

**Експериментуйте з типами!** Відкрийте Python REPL і спробуйте різні перетворення. Помиляйтесь і вчіться на помилках!

---

**Кінець тексту до презентації**

Цей спрощений матеріал підходить для студентів, які ще не вивчали колекції, функції, умови та цикли. Він зосереджений на базових концепціях перетворення типів та роботі з простими прикладами.
