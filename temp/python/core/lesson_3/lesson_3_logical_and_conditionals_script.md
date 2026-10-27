# Текст до презентації: Логічні оператори та оператори розгалужень

## Слайд 1: Титульний слайд
**Тема:** Логічні оператори та оператори розгалужень

**Текст:**
Доброго дня! Сьогодні ми вивчимо одну з найважливіших тем у програмуванні — умовні оператори та логічні операції. Це той момент, коли ваші програми стають "розумними" і можуть приймати рішення.

До цього моменту наші програми виконувалися лінійно — рядок за рядком, завжди в одному порядку. Але реальні програми потребують гнучкості: різна логіка для різних ситуацій.

**Приклади з життя:**
- Банкомат: ЯКЩО пін-код правильний, ТО дозволити доступ, ІНАКШЕ відмовити
- Погодний додаток: ЯКЩО температура < 0, ТО "Холодно", ЯКЩО < 15, ТО "Прохолодно", ІНАКШЕ "Тепло"
- Інтернет-магазин: ЯКЩО сума >= 1000, ТО знижка 10%

Сьогодні ми навчимося створювати таку логіку в Python. Ми розглянемо:
1. Оператори порівняння (==, !=, <, >, <=, >=)
2. Логічні оператори (and, or, not)
3. Умовні оператори (if, elif, else)
4. Вкладені умови
5. Практичні застосування

**Чому це важливо:**
Без умовних операторів неможливо створити жодну корисну програму. Це основа основ програмування, незалежно від мови.

---

## Слайд 2: Що таке умовні оператори?

**Текст:**
Розпочнемо з визначення. **Умовні оператори** (conditional statements) дозволяють програмі виконувати різний код залежно від того, чи виконується певна умова.

**Базова структура:**
```python
if умова:
    # цей код виконається, якщо умова True
else:
    # цей код виконається, якщо умова False
```

**Простий приклад:**
```python
age = 18

if age >= 18:
    print("Ви повнолітній")
else:
    print("Ви неповнолітній")
```

**Що відбувається покроково:**
1. Python обчислює умову `age >= 18`
2. Результат — булеве значення (True або False)
3. Якщо True — виконується перший блок
4. Якщо False — виконується блок else

**Аналогія з життя:**
Уявіть світлофор:
- ЯКЩО горить зелений → йдіть
- ІНАКШЕ → стійте

Або погода:
- ЯКЩО йде дощ → візьміть парасольку
- ІНАКШЕ → парасолька не потрібна

**Ключові терміни:**
- **Умова** (condition) — вираз, який повертає True або False
- **Блок коду** (code block) — група інструкцій з відступом
- **Розгалуження** (branching) — вибір одного з декількох шляхів виконання

**Важливо розуміти:**
Програма не виконує обидва блоки! Вона вибирає ОДИН з них залежно від умови. Це як розвилка на дорозі — ви можете піти тільки в один бік.

---

## Слайд 3: Навіщо потрібні умови?

**Текст:**
Розглянемо, чому умовні оператори настільки важливі в програмуванні.

### 1. Валідація даних

Перш ніж обробляти дані користувача, потрібно перевірити їх коректність:

```python
password = input("Enter password: ")

if len(password) < 8:
    print("Password too short! Must be at least 8 characters.")
else:
    print("Password accepted")
```

**Чому це важливо:**
- Запобігає помилкам
- Покращує безпеку
- Забезпечує коректність даних

### 2. Різна логіка для різних випадків

Програма повинна по-різному реагувати на різні ситуації:

```python
score = 85

if score >= 90:
    print("Grade: A - Excellent!")
elif score >= 80:
    print("Grade: B - Very good!")
elif score >= 70:
    print("Grade: C - Good")
else:
    print("Grade: F - Need improvement")
```

### 3. Інтерактивність

Програми взаємодіють з користувачем і реагують на його дії:

```python
choice = input("Continue? (y/n): ")

if choice == "y":
    print("Continuing...")
    # Продовжуємо виконання
else:
    print("Exiting...")
    # Завершуємо програму
```

### 4. Обробка помилок

```python
age = input("Enter age: ")

if age.isdigit():
    age = int(age)
    print(f"Your age: {age}")
else:
    print("Error: Age must be a number!")
```

### 5. Бізнес-логіка

```python
total = 1500

if total >= 1000:
    discount = 0.1  # 10% знижка
    print(f"You get {discount * 100}% discount!")
else:
    discount = 0
    print("No discount")

final_price = total * (1 - discount)
print(f"Final price: {final_price}")
```

**Висновок:**
Без умовних операторів програми були б "тупими" — вони б завжди робили одне і те саме, незалежно від ситуації. Умови роблять програми "розумними" та адаптивними.

---

## Слайд 4: Оператори порівняння

**Текст:**
Перш ніж вивчати умовні оператори, потрібно зрозуміти, як Python порівнює значення. Для цього існують **оператори порівняння** (comparison operators).

### Таблиця операторів

| Оператор | Назва | Значення | Приклад | Результат |
|----------|-------|----------|---------|-----------|
| `==` | Рівність | Перевіряє рівність | `5 == 5` | `True` |
| `!=` | Нерівність | Перевіряє нерівність | `5 != 3` | `True` |
| `>` | Більше | Лівий > правого | `5 > 3` | `True` |
| `<` | Менше | Лівий < правого | `3 < 5` | `True` |
| `>=` | Більше або дорівнює | Лівий >= правого | `5 >= 5` | `True` |
| `<=` | Менше або дорівнює | Лівий <= правого | `3 <= 5` | `True` |

**Ключовий момент:**
Результат порівняння — ЗАВЖДИ булеве значення (`True` або `False`). Це не рядок, не число — це спеціальний тип даних.

```python
result = 5 > 3
print(result)        # True
print(type(result))  # <class 'bool'>
```

### Приклади з різними типами

**Числа:**
```python
print(10 == 10)      # True
print(10 == 10.0)    # True (значення рівні)
print(5 != 3)        # True
print(7 > 10)        # False
print(3 <= 3)        # True (3 дорівнює 3)
```

**Рядки:**
Python порівнює рядки **лексикографічно** — за алфавітом, як у словнику:

```python
print("apple" < "banana")   # True ('a' < 'b')
print("cat" > "car")        # True ('t' > 'r')
print("Hello" == "hello")   # False (регістр має значення!)
```

**Як це працює:**
Python порівнює символи по одному, використовуючи їх Unicode-коди:
- 'a' = 97, 'b' = 98 → 'a' < 'b'
- 'A' = 65, 'a' = 97 → 'A' < 'a' (великі літери < малих)

**Різні типи:**
```python
print(5 == "5")      # False (int != str)
print(5 == 5.0)      # True (значення рівні)
print(True == 1)     # True (True = 1)
```

**Важливе застереження:**
Порівнювати можна майже все, але не завжди це має сенс:
```python
print("10" > "2")    # False! (порівнює рядки, '1' < '2')
print(10 > 2)        # True (порівнює числа)
```

---

## Слайд 5: Оператори порівняння: Приклади

**Текст:**
Розглянемо більше практичних прикладів використання операторів порівняння.

### Порівняння чисел

```python
# Прості порівняння
age = 25
print(age > 18)          # True
print(age < 30)          # True
print(age == 25)         # True
print(age != 20)         # True

# З float
price = 19.99
print(price > 20)        # False
print(price < 20)        # True
print(price == 19.99)    # True

# Граничні випадки
print(5 > 5)             # False (5 не більше за 5)
print(5 >= 5)            # True (5 дорівнює 5)
print(5 < 5)             # False
print(5 <= 5)            # True
```

**Коли використовувати >= vs >:**
- `age > 18` — "старше за 18" (19, 20, 21...)
- `age >= 18` — "18 або старше" (18, 19, 20...)

### Порівняння рядків

```python
# Рівність
name = "Alice"
print(name == "Alice")   # True
print(name == "alice")   # False (регістр!)

# Лексикографічне порівняння
print("apple" < "banana")    # True
print("zebra" > "aardvark")  # True

# Цікаві випадки
print("10" < "2")            # True (порівнює символи: '1' < '2')
print("abc" < "abd")         # True ('c' < 'd')
```

**Практичні застосування:**

1. **Перевірка паролю:**
```python
password = input("Enter password: ")
if password == "secret123":
    print("Access granted")
```

2. **Перевірка віку:**
```python
age = int(input("Enter age: "))
if age >= 18:
    print("You can vote")
```

3. **Діапазони:**
```python
temperature = 25
if temperature > 30:
    print("Hot!")
elif temperature < 10:
    print("Cold!")
```

### Порівняння з None

```python
value = None
print(value == None)     # True (але краще використати is)
print(value is None)     # True (рекомендовано)
```

**Правило:**
Для порівняння з `None` завжди використовуйте `is`, а не `==`.

---

## Слайд 6: Типова помилка: = vs ==

**Текст:**
Це одна з найпоширеніших помилок початківців, яка викликає багато плутанини!

### Різниця

**`=` — оператор присвоєння (assignment)**
Присвоює значення змінній:
```python
x = 5  # Присвоїти змінній x значення 5
```

**`==` — оператор порівняння (comparison)**
Порівнює два значення:
```python
x == 5  # Чи дорівнює x п'яти? Повертає True або False
```

### Візуальна різниця

```python
# Присвоєння
x = 10
# Читається: "x отримує значення 10"
# Результат: змінна x тепер містить 10

# Порівняння
x == 10
# Читається: "чи дорівнює x десяти?"
# Результат: True (булеве значення)
```

### Типова помилка

```python
x = 5

# ❌ НЕПРАВИЛЬНО
if x = 10:              # SyntaxError: invalid syntax
    print("This won't work")

# ✅ ПРАВИЛЬНО
if x == 10:             # Порівняння
    print("This will work")
```

**Чому виникає помилка:**
Python очікує умову (вираз, що повертає True/False), а отримує оператор присвоєння.

### Ще приклади помилок

```python
# ❌ Помилка 1: Використання = в умові
age = 18
if age = 20:
    print("Error")

# ✅ Правильно
if age == 20:
    print("Correct")

# ❌ Помилка 2: Плутанина в логіці
name = "Alice"
if name = "Bob":  # Намагаємося присвоїти, а не порівняти
    print("Error")

# ✅ Правильно
if name == "Bob":
    print("Correct")
```

### Як запам'ятати

**Правило "двійного знаку":**
- `=` — одинарний → ДАТИ значення (assignment)
- `==` — подвійний → ПОРІВНЯТИ значення (comparison)

**Мнемоніка:**
- "Одне дорівнює" → присвоїти
- "Два дорівнюють" → порівняти

**Аналогія з життя:**
- `x = 5` — "Нехай x буде 5" (команда)
- `x == 5` — "Чи є x п'ятьма?" (питання)

### Інші мови програмування

Цікаво, що в деяких мовах (C, Java, JavaScript) така помилка може не викликати SyntaxError, а призвести до несподіваної поведінки:

```javascript
// JavaScript (не Python!)
let x = 5;
if (x = 10) {  // Присвоїти 10 і перевірити (10 = truthy)
    console.log("This will execute!");  // Виконається!
}
```

В Python це неможливо — Python захищає вас від цієї помилки!

---

## Слайд 7: Логічні оператори

**Текст:**
Тепер, коли ми знаємо, як порівнювати значення, навчимося комбінувати умови за допомогою **логічних операторів** (logical operators).

### Три логічні оператори

Python має три логічні оператори, що дозволяють створювати складні умови:

1. **`and`** — логічне "І" (AND)
   - Повертає True, тільки якщо **ОБІ** умови True
   - Аналог: "І це, І те"

2. **`or`** — логічне "АБО" (OR)
   - Повертає True, якщо **ХОЧА Б ОДНА** умова True
   - Аналог: "Або це, або те (або обидва)"

3. **`not`** — логічне "НЕ" (NOT)
   - Інвертує (змінює на протилежне) логічне значення
   - Аналог: "Навпаки"

### Базові приклади

```python
# and — обидві умови повинні бути True
print(True and True)     # True
print(True and False)    # False
print(False and True)    # False
print(False and False)   # False

# or — хоча б одна умова повинна бути True
print(True or True)      # True
print(True or False)     # True
print(False or True)     # True
print(False or False)    # False

# not — інвертує значення
print(not True)          # False
print(not False)         # True
```

### Таблиці істинності

**AND (І):**
```
A     | B     | A and B
------|-------|--------
True  | True  | True
True  | False | False
False | True  | False
False | False | False
```

**OR (АБО):**
```
A     | B     | A or B
------|-------|--------
True  | True  | True
True  | False | True
False | True  | True
False | False | False
```

**NOT (НЕ):**
```
A     | not A
------|------
True  | False
False | True
```

### Чому це потрібно

Логічні оператори дозволяють перевіряти кілька умов одночасно:

```python
# Без логічних операторів (вкладені if)
age = 25
has_license = True

if age >= 18:
    if has_license:
        print("Can drive")

# З логічними операторами (простіше!)
if age >= 18 and has_license:
    print("Can drive")
```

**Переваги:**
- Код коротший і зрозуміліший
- Менше рівнів вкладеності
- Легше читати логіку

---

## Слайд 8: Логічний оператор AND

**Текст:**
Розглянемо детальніше оператор **and** (логічне "І").

### Як працює AND

`and` повертає `True` **тільки** якщо **ОБІ** умови є `True`. Якщо хоча б одна `False` — результат `False`.

**Таблиця істинності:**
```python
True and True    # True  ✅
True and False   # False ❌
False and True   # False ❌
False and False  # False ❌
```

**Правило:** "Обидві або жодної"

### Практичні приклади

**Приклад 1: Перевірка віку та прав**
```python
age = 20
has_license = True

if age >= 18 and has_license:
    print("You can drive a car")
else:
    print("You cannot drive")

# Пояснення:
# age >= 18 → True
# has_license → True
# True and True → True
# Виведе: "You can drive a car"
```

**Приклад 2: Діапазон значень**
```python
score = 85

if score >= 80 and score <= 90:
    print("Grade: B")

# score >= 80 → True
# score <= 90 → True
# True and True → True
```

**Приклад 3: Множинні умови**
```python
age = 25
has_ticket = True
has_id = True

if age >= 18 and has_ticket and has_id:
    print("Can enter the concert")

# Всі три умови мають бути True
```

### Аналогії з життя

**1. Вступ до університету:**
"Щоб вступити, потрібно **І** здати ЗНО, **І** мати атестат"
```python
has_zno = True
has_certificate = True

if has_zno and has_certificate:
    print("Can enroll")
```

**2. Доступ до системи:**
"Щоб увійти, потрібно **І** правильний логін, **І** правильний пароль"
```python
login = "admin"
password = "secret"

if login == "admin" and password == "secret":
    print("Access granted")
```

**3. Знижка в магазині:**
"Знижка, якщо **І** день народження, **І** сума > 1000"
```python
is_birthday = True
total = 1500

if is_birthday and total >= 1000:
    print("You get 20% discount!")
```

### Важливі моменти

**1. Порядок має значення для оптимізації:**
```python
# Якщо age < 18, has_license не перевіряється (short-circuit)
if age >= 18 and has_license:
    print("Can drive")
```

**2. Можна комбінувати з порівняннями:**
```python
x = 10
if x > 5 and x < 15:
    print("x is between 5 and 15")
```

**3. Краще використовувати дужки для складних виразів:**
```python
if (age >= 18 and age <= 65) and (has_job or has_savings):
    print("Eligible for loan")
```

### Типова помилка

```python
# ❌ НЕПРАВИЛЬНО
if age >= 18 and <= 65:  # SyntaxError
    print("Error")

# ✅ ПРАВИЛЬНО
if age >= 18 and age <= 65:
    print("Correct")

# ✅ АБО ЩЕ КРАЩЕ (ланцюгове порівняння)
if 18 <= age <= 65:
    print("Best")
```

---

## Слайд 9: Логічний оператор OR

**Текст:**
Тепер розглянемо оператор **or** (логічне "АБО").

### Як працює OR

`or` повертає `True`, якщо **ХОЧА Б ОДНА** з умов є `True`. Повертає `False` тільки якщо **ОБІ** умови `False`.

**Таблиця істинності:**
```python
True or True    # True  ✅
True or False   # True  ✅
False or True   # True  ✅
False or False  # False ❌
```

**Правило:** "Хоча б одна або обидві"

### Практичні приклади

**Приклад 1: Вихідні дні**
```python
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's a weekend! 🎉")
else:
    print("It's a workday 💼")

# day == "Saturday" → True
# True or (щось) → True (друга умова не перевіряється)
```

**Приклад 2: Знижка**
```python
is_student = True
is_senior = False

if is_student or is_senior:
    print("You get a 10% discount!")

# is_student → True
# True or False → True
```

**Приклад 3: Альтернативні умови входу**
```python
has_key = False
knows_password = True

if has_key or knows_password:
    print("Door unlocked")

# has_key → False
# knows_password → True
# False or True → True
```

### Аналогії з життя

**1. Вихідний день:**
"Не йти на роботу, якщо **АБО** вихідний, **АБО** свято"
```python
is_weekend = True
is_holiday = False

if is_weekend or is_holiday:
    print("Day off!")
```

**2. Знижка в кафе:**
"Знижка, якщо **АБО** студент, **АБО** пенсіонер, **АБО** день народження"
```python
if is_student or is_senior or is_birthday:
    discount = 0.15
```

**3. Дозволені способи оплати:**
"Можна оплатити **АБО** карткою, **АБО** готівкою, **АБО** через додаток"
```python
payment_method = "card"

if payment_method == "card" or payment_method == "cash" or payment_method == "app":
    print("Payment accepted")
```

### Множинні OR

```python
# Багато альтернатив
fruit = "apple"

if fruit == "apple" or fruit == "banana" or fruit == "orange":
    print("This is a fruit")

# Краще використати in (коли вивчите списки):
# if fruit in ["apple", "banana", "orange"]:
```

### Комбінування AND і OR

```python
# Дужки для ясності!
age = 25
is_student = True
has_coupon = False

# Знижка для студентів АБО для всіх з купоном
if (age < 26 and is_student) or has_coupon:
    print("Discount available!")

# Без дужок порядок: and виконується першим
if age < 26 and is_student or has_coupon:  # Теж саме
    print("Discount available!")
```

### Short-circuit evaluation

Python оптимізує обчислення:

```python
# Якщо перша умова True, друга НЕ перевіряється
if True or expensive_operation():
    print("First was True")
# expensive_operation() НЕ викликається!

# Якщо перша умова False, друга ПЕРЕВІРЯЄТЬСЯ
if False or expensive_operation():
    print("Checking second condition")
# expensive_operation() викликається
```

---

## Слайд 10: Логічний оператор NOT

**Текст:**
Останній логічний оператор — **not** (логічне "НЕ" або заперечення).

### Як працює NOT

`not` інвертує (змінює на протилежне) логічне значення:
- `not True` → `False`
- `not False` → `True`

**Таблиця істинності:**
```python
not True   # False
not False  # True
```

**Правило:** "Навпаки"

### Базові приклади

```python
# Інверсія булевих значень
print(not True)          # False
print(not False)         # True

# З порівняннями
x = 5
print(not x > 10)        # True (бо x > 10 = False, not False = True)
print(not x == 5)        # False (бо x == 5 = True, not True = False)

# З змінними
is_raining = False
print(not is_raining)    # True
```

### Практичні приклади

**Приклад 1: Перевірка погоди**
```python
is_raining = False

if not is_raining:
    print("Go for a walk! ☀️")
else:
    print("Stay home 🌧️")

# not is_raining → not False → True
```

**Приклад 2: Перевірка доступу**
```python
is_banned = True

if not is_banned:
    print("Access granted")
else:
    print("Access denied")

# not is_banned → not True → False
```

**Приклад 3: Перевірка на порожній рядок**
```python
username = input("Enter username: ")

if not username:  # Якщо рядок порожній
    print("Username cannot be empty!")

# Порожній рядок → False
# not False → True (умова виконується)
```

### Еквівалентні вирази

Іноді `not` можна замінити на протилежний оператор порівняння:

```python
x = 10

# З not
if not x > 5:
    print("x not greater than 5")

# Без not (краще!)
if x <= 5:
    print("x not greater than 5")

# З not
if not x == 10:
    print("x not equal to 10")

# Без not (краще!)
if x != 10:
    print("x not equal to 10")
```

**Рекомендація:** Якщо можна уникнути `not`, краще використати протилежний оператор — це читабельніше.

### Подвійне заперечення

```python
x = True

print(not not x)     # True (подвійне not)
# not x → False
# not False → True

# Подвійне not = оригінальне значення
```

Але це погана практика — просто використовуйте оригінальне значення!

### Комбінування NOT з AND/OR

```python
age = 16
has_permission = False

# Якщо НЕ (дорослий АБО є дозвіл)
if not (age >= 18 or has_permission):
    print("Access denied")

# Розбір:
# age >= 18 → False
# has_permission → False
# False or False → False
# not False → True
```

**Правило Де Моргана:**
```python
# not (A and B) = (not A) or (not B)
# not (A or B) = (not A) and (not B)

# Приклад:
not (x > 5 and y < 10)
# Те саме що:
not (x > 5) or not (y < 10)
# Те саме що:
x <= 5 or y >= 10
```

---

## Слайд 11: Комбінування логічних операторів

**Текст:**
У реальних програмах часто потрібно перевіряти кілька умов одночасно, комбінуючи різні логічні оператори.

### Множинні умови

```python
age = 25
has_ticket = True
has_id = True
is_banned = False

# Всі умови разом
if age >= 18 and has_ticket and has_id and not is_banned:
    print("Can enter the venue")

# Покрокове обчислення:
# age >= 18 → True
# has_ticket → True
# has_id → True
# not is_banned → not False → True
# True and True and True and True → True
```

### Комбінування AND і OR

```python
# Знижка для студентів до 25 років АБО для всіх з купоном
age = 22
is_student = True
has_coupon = False

if (age < 25 and is_student) or has_coupon:
    print("10% discount!")

# Без дужок (and має вищий пріоритет):
if age < 25 and is_student or has_coupon:
    print("Same result")
```

### Пріоритет операторів

**Порядок виконання (від вищого до нижчого):**
1. **not** (найвищий)
2. **and**
3. **or** (найнижчий)

```python
# Приклад 1
result = not False and True or False
# Крок 1: not False → True
# Крок 2: True and True → True
# Крок 3: True or False → True
print(result)  # True

# Приклад 2
result = True or False and False
# Крок 1: False and False → False
# Крок 2: True or False → True
print(result)  # True
```

### Використання дужок

**Завжди використовуйте дужки для складних виразів!**

```python
# Без дужок (незрозуміло)
if age >= 18 and has_license or is_vip and not is_banned:
    print("Confusing!")

# З дужками (зрозуміло)
if (age >= 18 and has_license) or (is_vip and not is_banned):
    print("Clear!")
```

### Практичний приклад: Складна валідація

```python
username = "admin"
password = "secret123"
is_verified = True
login_attempts = 2

# Складна умова входу
if (username == "admin" and password == "secret123" and is_verified) \
   and login_attempts < 3:
    print("Login successful!")
else:
    print("Login failed")

# Розбиваємо на частини для читабельності:
correct_credentials = username == "admin" and password == "secret123"
valid_user = correct_credentials and is_verified
allowed_attempts = login_attempts < 3

if valid_user and allowed_attempts:
    print("Login successful!")
```

### Типові помилки

```python
# ❌ Помилка 1: Забули дужки
if age >= 18 and has_ticket or has_vip_pass and not is_banned:
    # Важко зрозуміти логіку!

# ✅ Правильно
if (age >= 18 and has_ticket) or (has_vip_pass and not is_banned):
    # Зрозуміла логіка

# ❌ Помилка 2: Зайві дужки
if ((age >= 18) and (has_ticket)):  # Зайві дужки
    print("OK")

# ✅ Достатньо
if age >= 18 and has_ticket:
    print("OK")
```

---

## Слайд 12: Пріоритет логічних операторів

**Текст:**
Розуміння пріоритету операторів критично важливе для написання коректного коду.

### Таблиця пріоритетів

**Від вищого до нижчого:**

1. **Дужки `()`** — найвищий пріоритет
2. **Порівняння** (`==`, `!=`, `<`, `>`, `<=`, `>=`)
3. **`not`** — логічне заперечення
4. **`and`** — логічне "І"
5. **`or`** — логічне "АБО" (найнижчий)

### Приклади обчислення

**Приклад 1:**
```python
result = True or False and False
# Крок 1: False and False → False (and першим)
# Крок 2: True or False → True
print(result)  # True
```

**Приклад 2:**
```python
result = not False and True or False
# Крок 1: not False → True
# Крок 2: True and True → True
# Крок 3: True or False → True
print(result)  # True
```

**Приклад 3:**
```python
result = True and not False or False and True
# Крок 1: not False → True
# Крок 2: True and True → True
# Крок 3: False and True → False
# Крок 4: True or False → True
print(result)  # True
```

### З дужками

**Дужки змінюють порядок:**

```python
# Без дужок
result = True or False and False
print(result)  # True

# З дужками
result = (True or False) and False
# Крок 1: True or False → True
# Крок 2: True and False → False
print(result)  # False
```

### Практичний приклад

```python
age = 16
has_permission = True

# Без дужок (and виконується першим)
if age >= 18 or age >= 16 and has_permission:
    print("Can watch the movie")

# Розбір:
# age >= 16 and has_permission → True and True → True
# age >= 18 or True → False or True → True

# З дужками (для ясності)
if (age >= 18) or (age >= 16 and has_permission):
    print("Can watch the movie")
```

### Рекомендації

1. **Використовуйте дужки** для складних виразів, навіть якщо вони не обов'язкові
2. **Розбивайте** складні умови на частини з окремими змінними
3. **Коментуйте** складну логіку

```python
# ❌ Погано (незрозуміло)
if a and b or c and d and not e or f:
    print("What?")

# ✅ Добре (з дужками)
if (a and b) or (c and d and not e) or f:
    print("Better")

# ✅ Найкраще (з змінними)
condition1 = a and b
condition2 = c and d and not e
if condition1 or condition2 or f:
    print("Best!")
```

---

## Слайд 13: Оператор if

**Текст:**
Тепер, коли ми знаємо логічні оператори, розглянемо сами умовні оператори. Почнемо з базового — **if**.

### Синтаксис

```python
if умова:
    # код виконується, якщо умова True
    інструкція1
    інструкція2
    ...
```

**Ключові елементи:**
1. Ключове слово `if`
2. Умова (вираз, що повертає True/False)
3. Двокрапка `:`
4. Блок коду з відступом (4 пробіли)

### Базовий приклад

```python
age = 20

if age >= 18:
    print("Ви повнолітній")
    print("Можете голосувати")

print("Ця стрічка завжди виконується")
```

**Що відбувається:**
1. Python обчислює `age >= 18` → `True`
2. Оскільки True, виконується блок з відступом
3. Код без відступу виконується завжди

### Блоки коду

**Блок коду** — це група інструкцій, що виконуються разом:

```python
if True:
    print("Line 1")  # Частина блоку
    print("Line 2")  # Частина блоку
    print("Line 3")  # Частина блоку
print("Line 4")      # НЕ частина блоку
```

### Порожній блок

Python не дозволяє порожні блоки:

```python
# ❌ Помилка
if age >= 18:
    # нічого тут немає
# IndentationError

# ✅ Використовуйте pass
if age >= 18:
    pass  # "нічого не робити"
```

`pass` — спеціальне ключове слово, що означає "нічого не робити". Використовується як заглушка.

### Практичні приклади

**Приклад 1: Валідація паролю**
```python
password = input("Enter password: ")

if len(password) < 8:
    print("Password too short!")
    print("Must be at least 8 characters")
```

**Приклад 2: Перевірка числа**
```python
number = int(input("Enter a number: "))

if number > 0:
    print("Positive number")

if number < 0:
    print("Negative number")

if number == 0:
    print("Zero")
```

**Приклад 3: Множинні перевірки**
```python
score = 95

if score >= 90:
    print("Excellent!")
    grade = "A"
    bonus_points = 10
    print(f"Your grade: {grade}")
    print(f"Bonus points: {bonus_points}")
```

---

## Слайд 14: Відступи в Python

**Текст:**
Відступи (indentation) — це не просто "гарний код" у Python. Це **частина синтаксису мови**!

### Чому це важливо

На відміну від інших мов (C, Java, JavaScript), де блоки коду позначаються фігурними дужками `{}`, Python використовує **відступи**.

**Інші мови (JavaScript):**
```javascript
if (age >= 18) {
    console.log("Adult");
    console.log("Can vote");
}
```

**Python:**
```python
if age >= 18:
    print("Adult")
    print("Can vote")
```

### Правила відступів

**1. Стандартний відступ — 4 пробіли**

PEP 8 (Python Style Guide) рекомендує використовувати **4 пробіли** для кожного рівня відступу.

```python
# ✅ Правильно (4 пробіли)
if age >= 18:
    print("Adult")

# ✅ Також правильно, але не рекомендовано (2 пробіли)
if age >= 18:
  print("Adult")

# ❌ Неправильно (Tab)
if age >= 18:
	print("Adult")  # НЕ використовуйте Tab!
```

**2. Консистентність у всьому файлі**

```python
# ❌ Помилка: змішані відступи
if age >= 18:
    print("Line 1")  # 4 пробіли
  print("Line 2")    # 2 пробіли - IndentationError!
```

**3. Всередині блоку — однаковий відступ**

```python
# ✅ Правильно
if age >= 18:
    print("Line 1")
    print("Line 2")
    print("Line 3")

# ❌ Неправильно
if age >= 18:
    print("Line 1")
     print("Line 2")  # Один зайвий пробіл!
```

### Типові помилки

**Помилка 1: Відсутність відступу**
```python
if age >= 18:
print("Error")  # IndentationError: expected an indented block
```

**Помилка 2: Неправильний відступ**
```python
if age >= 18:
    print("Adult")
  print("Error")  # IndentationError: unindent does not match
```

**Помилка 3: Змішування пробілів і табів**
```python
if age >= 18:
    print("Line 1")  # 4 пробіли
	print("Line 2")  # 1 Tab - TabError!
```

### Рекомендації IDE

Більшість сучасних редакторів (VS Code, PyCharm) автоматично:
- Конвертують Tab у пробіли
- Підсвічують помилки відступів
- Автоматично додають відступи після `:`

**Налаштування VS Code:**
```json
{
    "editor.tabSize": 4,
    "editor.insertSpaces": true
}
```

### Візуалізація

```python
if умова:
····код1    # 4 пробіли (відступ 1)
····код2    # 4 пробіли (відступ 1)
код3        # 0 пробілів (без відступу)
```

**Правило:** Код з однаковим відступом належить до одного блоку.

---

## Слайд 15: Оператор else

**Текст:**
Часто потрібно виконати один код, якщо умова True, і інший код, якщо False. Для цього використовується **else**.

### Синтаксис

```python
if умова:
    # виконується, якщо умова True
    код1
else:
    # виконується, якщо умова False
    код2
```

**Важливо:** Виконується **ТІЛЬКИ ОДИН** з блоків — або `if`, або `else`.

### Базовий приклад

```python
age = 15

if age >= 18:
    print("Ви повнолітній")
    print("Можете голосувати")
else:
    print("Ви неповнолітній")
    print("Ще не можете голосувати")

# Якщо age >= 18 → виконається перший блок
# Інакше → виконається другий блок
```

### Логіка роботи

```
    age >= 18?
       / \
     Yes  No
      |    |
     if  else
```

**Покрокове виконання:**
1. Python перевіряє умову `age >= 18`
2. Якщо True → виконується блок `if`, блок `else` пропускається
3. Якщо False → блок `if` пропускається, виконується блок `else`
4. Після if-else програма продовжує виконання

### Практичні приклади

**Приклад 1: Парність числа**
```python
number = int(input("Enter a number: "))

if number % 2 == 0:
    print(f"{number} is even")
else:
    print(f"{number} is odd")
```

**Приклад 2: Валідація паролю**
```python
password = input("Enter password: ")

if len(password) >= 8:
    print("Password accepted ✓")
    print("Account created")
else:
    print("Password too short ✗")
    print("Must be at least 8 characters")
```

**Приклад 3: Знижка**
```python
total = float(input("Enter total: "))

if total >= 1000:
    discount = total * 0.1
    final = total - discount
    print(f"Discount: {discount}")
    print(f"Final price: {final}")
else:
    print("No discount")
    print(f"Total: {total}")
```

### Без else

`else` — опціональний. Можна використовувати тільки `if`:

```python
age = 15

if age < 18:
    print("Access denied")

# Якщо age >= 18, нічого не виводиться
```

### Множинні if vs if-else

```python
# Множинні if (обидва можуть виконатися)
if score >= 90:
    print("Excellent!")
if score >= 60:
    print("Pass")  # Виконається, якщо score >= 90

# if-else (тільки один виконається)
if score >= 90:
    print("Excellent!")
else:
    print("Not excellent")  # НЕ виконається, якщо score >= 90
```

---

## Слайд 16: if-else: Блок-схема

**Текст:**
Візуалізуємо логіку роботи if-else за допомогою блок-схеми.

### Блок-схема

```
      START
         |
         ▼
    ┌─────────┐
    │ age = ? │
    └────┬────┘
         │
         ▼
   ┌──────────────┐
   │ age >= 18 ?  │──── Умова (ромб)
   └──────┬───────┘
          │
   ┌──────┴──────┐
   │             │
 True          False
   │             │
   ▼             ▼
┌───────────┐ ┌────────────────┐
│ "Повно-   │ │ "Неповно-      │
│  літній"  │ │  літній"       │
└─────┬─────┘ └────────┬───────┘
      │                │
      └────────┬───────┘
               │
               ▼
     ┌────────────────┐
     │ Продовження... │
     └────────────────┘
          │
          ▼
         END
```

### Пояснення блок-схеми

**Елементи:**
- **Овал** — початок/кінець
- **Прямокутник** — дія/операція
- **Ромб** — умова/рішення
- **Стрілки** — потік виконання

**Логіка:**
1. Програма доходить до умови
2. Перевіряє умову (True або False)
3. Йде тільки одним шляхом
4. Обидва шляхи зливаються далі

### Приклад коду з блок-схеми

```python
# Точка входу
age = int(input("Enter age: "))

# Умова (ромб)
if age >= 18:
    # True гілка (лівий шлях)
    print("Ви повнолітній")
else:
    # False гілка (правий шлях)
    print("Ви неповнолітній")

# Злиття шляхів (продовження програми)
print("Thank you!")
```

### Складніша блок-схема (з множинними діями)

```
         age >= 18?
            / \
          Yes  No
           |    |
  ┌────────┤    ├─────────┐
  │        |    |         │
  ▼        ▼    ▼         ▼
"Adult"  "Can  "Minor"  "Cannot
         vote"           vote"
  │        │    │         │
  └────────┴────┴─────────┘
           │
      "Thank you!"
```

Код:
```python
if age >= 18:
    print("Adult")
    print("Can vote")
else:
    print("Minor")
    print("Cannot vote")
print("Thank you!")
```

### Важливість візуалізації

Блок-схеми допомагають:
- **Планувати** логіку перед написанням коду
- **Розуміти** потік виконання програми
- **Знаходити** помилки в логіці
- **Пояснювати** алгоритм іншим

**Порада:** Для складної логіки спочатку намалюйте блок-схему, а потім пишіть код!

---

## Слайд 17: Оператор elif

**Текст:**
Часто потрібно перевірити не дві, а більше альтернатив. Для цього використовується **elif** (скорочення від "else if").

### Синтаксис

```python
if умова1:
    # якщо умова1 True
elif умова2:
    # якщо умова1 False, але умова2 True
elif умова3:
    # якщо умова1 і умова2 False, але умова3 True
else:
    # якщо всі умови False
```

### Базовий приклад

```python
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")

# Виведе: "Grade: B"
```

**Що відбувається:**
1. Перевіряється `score >= 90` → False
2. Перевіряється `score >= 80` → True
3. Виконується цей блок: "Grade: B"
4. Всі інші elif і else **пропускаються**

### Важливо: Тільки один блок виконується!

```python
score = 95

if score >= 90:
    print("A")  # Виконається ЦЕЙ блок
elif score >= 80:
    print("B")  # НЕ виконається (попередня умова була True)
elif score >= 70:
    print("C")  # НЕ виконається
else:
    print("F")  # НЕ виконається

# Виведе тільки: "A"
```

**Правило:** Як тільки одна з умов виконалася (True), всі наступні elif і else **ігноруються**.

### Логіка роботи

```
score >= 90?
   / \
 Yes  No
  |    |
  A    score >= 80?
         / \
       Yes  No
        |    |
        B   score >= 70?
               / \
             Yes  No
              |    |
              C    F
```

**Кожна умова перевіряється ТІЛЬКИ якщо всі попередні були False.**

### Практичні приклади

**Приклад 1: Визначення сезону**
```python
month = int(input("Enter month (1-12): "))

if month == 12 or month == 1 or month == 2:
    print("Winter ❄️")
elif month == 3 or month == 4 or month == 5:
    print("Spring 🌸")
elif month == 6 or month == 7 or month == 8:
    print("Summer ☀️")
elif month == 9 or month == 10 or month == 11:
    print("Autumn 🍂")
else:
    print("Invalid month!")
```

**Приклад 2: Знижка залежно від суми**
```python
total = float(input("Enter total: "))

if total >= 10000:
    discount = 0.20  # 20%
    print("VIP discount: 20%")
elif total >= 5000:
    discount = 0.15  # 15%
    print("Gold discount: 15%")
elif total >= 1000:
    discount = 0.10  # 10%
    print("Silver discount: 10%")
else:
    discount = 0
    print("No discount")

final_price = total * (1 - discount)
print(f"Final price: {final_price}")
```

**Приклад 3: Вікові категорії**
```python
age = int(input("Enter age: "))

if age < 0:
    print("Invalid age")
elif age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
elif age < 65:
    print("Adult")
else:
    print("Senior")
```

### Кількість elif

Можна мати скільки завгодно `elif`:

```python
if condition1:
    # ...
elif condition2:
    # ...
elif condition3:
    # ...
elif condition4:
    # ...
# ... ще 100 elif
else:
    # ...
```

Але занадто багато `elif` — ознака поганого дизайну. Краще використати інші підходи (словники, класи тощо), але це вже складніші теми.

### else — опціональний

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
# Немає else — якщо score < 70, нічого не виведеться
```

---

(Продовження в наступній частині через обмеження розміру...)
