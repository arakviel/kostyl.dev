# Кортежі та словники у Python

## Зміст

### Кортежі (Tuples)
1. [Вступ до кортежів](#вступ-до-кортежів)
2. [Колекції незмінних об'єктів](#колекції-незмінних-обєктів)
3. [Створення кортежів](#створення-кортежів)
4. [Особливості кортежів](#особливості-кортежів)
5. [Індексація та зрізи](#індексація-та-зрізи)
6. [Операції з кортежами](#операції-з-кортежами)
7. [Розпакування кортежів](#розпакування-кортежів)
8. [Кортежі як ключі словників](#кортежі-як-ключі-словників)
9. [Порівняння кортежів та списків](#порівняння-кортежів-та-списків)
10. [Практичні приклади використання кортежів](#практичні-приклади-використання-кортежів)

### Словники (Dictionaries)
11. [Вступ до словників](#вступ-до-словників)
12. [Асоціативні масиви](#асоціативні-масиви)
13. [Хеш-таблиці](#хеш-таблиці)
14. [Створення словника](#створення-словника)
15. [Доступ до елементів](#доступ-до-елементів)
16. [Методи словника](#методи-словника)
17. [Вкладені словники](#вкладені-словники)
18. [Dictionary comprehension](#dictionary-comprehension)
19. [Практичні приклади використання словників](#практичні-приклади-використання-словників)

---

# Частина 1. Кортежі (Tuples)

---

## Вступ до кортежів

### Що таке кортеж?

**Кортеж** (tuple) — це **упорядкована, незмінна** колекція елементів, записана у круглих дужках та розділена комами.

**Формальне визначення:** Кортеж є екземпляром класу `tuple`, який реалізує послідовність елементів із фіксованою довжиною. На відміну від списку, кортеж не допускає зміни своїх елементів після створення (імутабельність).

**Синтаксис:**

```python
# Простий кортеж
coordinates = (10, 20)

# Кортеж з різними типами
record = ("Іван", 25, 4.85)

# Порожній кортеж
empty = ()

# Кортеж з одним елементом (кома обов'язкова!)
single = (42,)   # ← кортеж
not_tuple = (42)  # ← просто число (в дужках)
```

### Чому кортежі потрібні?

| Задача | Рішення |
|--------|---------|
| Зберігати дані, які не повинні змінюватися | Кортеж |
| Повертати кілька значень з функції | Кортеж |
| Використовувати як ключі словника | Кортеж |
| Захищати дані від випадкової зміни | Кортеж |
| Швидше створення та менше витрат пам'яті | Кортеж |

---

## Колекції незмінних об'єктів

### Що таке імутабельність?

**Імутабельність** (immutability) — це властивість об'єкта, яка означає, що після створення об'єкта його стан (вміст) **не може бути змінений**.

**Мутабельні** (змінні) об'єкти: списки (`list`), словники (`dict`), множини (`set`)
**Імутабельні** (незмінні) об'єкти: кортежі (`tuple`), рядки (`str`), числа (`int`, `float`), frozen sets (`frozenset`)

### Приклади імутабельності:

```python
# Рядок — імутабельний
name = "Python"
# name[0] = "J"  # TypeError: 'str' object does not support item assignment

# Кортеж — імутабельний
point = (10, 20)
# point[0] = 15  # TypeError: 'tuple' object does not support item assignment

# Список — мутабельний
items = [1, 2, 3]
items[0] = 99  # Працює: [99, 2, 3]
```

### Навіщо потрібні незмінні колекції?

1. **Цілісність даних:** Гарантія, що дані не будуть випадково змінені іншою частиною програми.
2. **Безпека при передачі:** Кортеж можна безпечно передавати між функціями, не хвилюючись, що його змінять.
3. **Використання як ключі:** Імутабельні об'єкти можна використовувати як ключі словників та елементи множин.
4. **Ефективність:** Кортежі займають менше пам'яті та створюються швидше за списки.
5. **Неявна угода:** Якщо функція повертає кортеж, викликаючий код знає, що дані не зміняться.

```python
# Кортеж як ключ словника (список не можна!)
distances = {
    (40.7128, -74.0060): "Нью-Йорк",
    (51.5074, -0.1278): "Лондон",
    (48.8566, 2.3522): "Париж",
}

# Спроба використати список як ключ:
# point = [40.7128, -74.0060]
# distances[point] = "Нью-Йорк"  # TypeError: unhashable type: 'list'
```

### Хешованість та імутабельність

Кортежі є **хешованими** (hashable), тобто для них можна обчислити хеш-значення. Це робить їх придатними для використання в якості ключів словників та елементів множин.

```python
# Кортеж з хешованих елементів — хешований
t1 = (1, 2, 3)
print(hash(t1))  # працює

# Кортеж з нехешованих елементів — нехешований
t2 = (1, [2, 3])
# hash(t2)  # TypeError: unhashable type: 'list'
```

---

## Створення кортежів

### Спосіб 1: Прямий запис

```python
# Порожній кортеж
empty = ()

# Кортеж з одним елементом
single = (42,)
single = 42,   # кома також працює

# Кортеж з кількома елементами
numbers = (1, 2, 3, 4, 5)

# Змішані типи
mixed = ("Привіт", 3.14, True, None)

# Вкладений кортеж
nested = ((1, 2), (3, 4), (5, 6))
```

### Спосіб 2: Виклик конструктора `tuple()`

```python
# Зі списку
from_list = tuple([1, 2, 3, 4, 5])
print(from_list)  # (1, 2, 3, 4, 5)

# З рядка
from_string = tuple("Python")
print(from_string)  # ('P', 'y', 't', 'h', 'o', 'n')

# З діапазону
from_range = tuple(range(5))
print(from_range)  # (0, 1, 2, 3, 4)

# Порожній кортеж
empty = tuple()
print(empty)  # ()
```

### Спосіб 3: Неявне створення (без дужок)

```python
# Коми створюють кортеж, навіть без дужок
point = 10, 20, 30
print(type(point))  # <class 'tuple'>
print(point)        # (10, 20, 30)

# При поверненні з функції
def get_coordinates():
    return 10, 20  # Python повертає кортеж

coords = get_coordinates()
print(type(coords))  # <class 'tuple'>
```

### Типова помилка: кортеж з одним елементом

```python
# Це НЕ кортеж, це число:
not_tuple = (42)
print(type(not_tuple))  # <class 'int'>

# Це КОРТЕЖ (потрібна кома):
is_tuple = (42,)
print(type(is_tuple))  # <class 'tuple'>

# Кому можна не ставити після останнього елемента:
also_tuple = (42,)
also_tuple = 42,    # те саме
```

---

## Особливості кортежів

### 1. Незмінність (імутабельність)

```python
point = (10, 20, 30)

# point[0] = 100
# TypeError: 'tuple' object does not support item assignment

# Але якщо кортеж містить мутабельний об'єкт, той можна змінити
data = (1, 2, [3, 4])
data[2][0] = 99
print(data)  # (1, 2, [99, 4])  — список змінився!

# Але сам кортеж залишається тим самим об'єктом
print(id(data))  # одне й те саме значення
```

### 2. Швидкість створення та доступу

```python
import sys
import timeit

# Порівняння розміру в пам'яті
list_obj = [1, 2, 3, 4, 5]
tuple_obj = (1, 2, 3, 4, 5)

print(sys.getsizeof(list_obj))   # 96 (байт)
print(sys.getsizeof(tuple_obj))  # 80 (байт) — менше!

# Порівняння швидкості створення
time_list = timeit.timeit('[1, 2, 3, 4, 5]', number=1_000_000)
time_tuple = timeit.timeit('(1, 2, 3, 4, 5)', number=1_000_000)

print(f"Список:    {time_list:.4f} сек")
print(f"Кортеж:    {time_tuple:.4f} сек")
print(f"Кортеж швидше у {time_list/time_tuple:.1f} разів")
```

### 3. Вбудовані методи

Кортеж має лише два методи:

```python
numbers = (1, 2, 3, 2, 2, 4, 5, 2)

# count() — підрахунок кількості входжень
print(numbers.count(2))  # 4

# index() — пошук першого входження
print(numbers.index(3))  # 3 (індекс)

# numbers.append(6)  # AttributeError: 'tuple' object has no attribute 'append'
```

### 4. Кортежі та пам'ять

```python
import sys

# Python кешує малі кортежі (-5 до 256)
a = (1, 2, 3)
b = (1, 2, 3)
print(a is b)  # True — той самий об'єкт у пам'яті!

# Великі кортежі не кешуються
a = (1000, 2000, 3000)
b = (1000, 2000, 3000)
print(a is b)  # False — різні об'єкти
```

---

## Індексація та зрізи

### Індексація

```python
colors = ("червоний", "оранжевий", "жовтий", "зелений", "синій", "фіолетовий")

# Позитивна індексація (від початку)
print(colors[0])    # червоний
print(colors[2])    # жовтий
print(colors[-1])   # фіолетовий (останній)
print(colors[-3])   # зелений (третій з кінця)

# Помилка виходу за межі
# colors[10]  # IndexError: tuple index out of range
```

### Зрізи (slicing)

```python
numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

# Базові зрізи
print(numbers[2:5])     # (2, 3, 4)
print(numbers[:4])      # (0, 1, 2, 3)
print(numbers[6:])      # (6, 7, 8, 9)
print(numbers[:])       # (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

# З кроком
print(numbers[::2])     # (0, 2, 4, 6, 8)
print(numbers[1::2])    # (1, 3, 5, 7, 9)
print(numbers[::-1])    # (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)

# Від'ємний крок
print(numbers[7:2:-1])  # (7, 6, 5, 4, 3)
```

### Порівняння кортежів

```python
# Лексикографічне порівняння
print((1, 2, 3) < (1, 2, 4))    # True
print((1, 2, 3) < (1, 2))       # False (довший більший)
print((1, 2, 3) == (1, 2, 3))   # True
print((1, 2, 3) != (1, 2, 4))   # True

# Порівняння з різними типами
print((1, "a") < (2, "b"))      # True
print((1, "a") < (1, "b"))      # True
```

---

## Операції з кортежами

### Конкатенація (об'єднання)

```python
t1 = (1, 2, 3)
t2 = (4, 5, 6)

# Оператор +
result = t1 + t2
print(result)  # (1, 2, 3, 4, 5, 6)

# Оператор +=
t1 += t2
print(t1)  # (1, 2, 3, 4, 5, 6)
```

### Повторення

```python
t = (1, 2, 3)

# Оператор *
result = t * 3
print(result)  # (1, 2, 3, 1, 2, 3, 1, 2, 3)

# Оператор *=
t *= 2
print(t)  # (1, 2, 3, 1, 2, 3)
```

### Належність (membership)

```python
colors = ("червоний", "зелений", "синій")

print("червоний" in colors)    # True
print("жовтий" in colors)      # False
print("жовтий" not in colors)  # True
```

### Довжина, мінімум, максимум, сума

```python
numbers = (5, 2, 8, 1, 9, 3)

print(len(numbers))    # 6
print(min(numbers))    # 1
print(max(numbers))    # 9
print(sum(numbers))    # 28

# Підрахунок входжень
print(numbers.count(8))  # 1
```

### Сортування (повертає список!)

```python
numbers = (5, 2, 8, 1, 9, 3)

# Функція sorted() повертає список
sorted_numbers = sorted(numbers)
print(sorted_numbers)     # [1, 2, 3, 5, 8, 9]
print(type(sorted_numbers))  # <class 'list'>

# Сортування у зворотному порядку
sorted_desc = sorted(numbers, reverse=True)
print(sorted_desc)  # [9, 8, 5, 3, 2, 1]
```

---

## Розпакування кортежів

### Базове розпакування

```python
# Розпакування в змінні
point = (10, 20, 30)
x, y, z = point
print(x)  # 10
print(y)  # 20
print(z)  # 30

# Обмін значень (swap)
a, b = 1, 2
a, b = b, a
print(a, b)  # 2 1
```

### Розпакування з оператором *

```python
# Зберегти перший та останній, решту — у список
first, *middle, last = (1, 2, 3, 4, 5)
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5

# Зберегти перші два, решту — у список
first, second, *rest = (1, 2, 3, 4, 5)
print(first)   # 1
print(second)  # 2
print(rest)    # [3, 4, 5]

# Зберегти перший та решту
first, *rest = (1, 2, 3, 4, 5)
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

# Зберегти останній та решту
*rest, last = (1, 2, 3, 4, 5)
print(rest)  # [1, 2, 3, 4]
print(last)  # 5
```

### Розпакування в циклах

```python
# Перебір пар (x, y)
points = [(0, 0), (1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(f"Точка: ({x}, {y})")

# Перебір записів
students = (("Іван", 90), ("Марія", 85), ("Петро", 92))
for name, score in students:
    print(f"{name}: {score}")
```

### Розпакування у функціях

```python
# Функція повертає кілька значень (кортеж)
def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([5, 2, 8, 1, 9])
print(f"Мін: {minimum}, Макс: {maximum}")  # Мін: 1, Макс: 9

# Функція повертає кортеж з різними типами
def get_user_info():
    return "Іван", 25, "іван@email.com"

name, age, email = get_user_info()
print(f"{name}, {age} років, {email}")
```

---

## Кортежі як ключі словників

Оскільки кортежі є хешованими (якщо всі елементи також хешовані), вони можуть використовуватися як ключі словників:

```python
# Координати як ключі
distances = {
    (40.7128, -74.0060): "Нью-Йорк",
    (51.5074, -0.1278): "Лондон",
    (48.8566, 2.3522): "Париж",
}

print(distances[(40.7128, -74.0060)])  # Нью-Йорк

# RGB кольори як ключі
colors = {
    (255, 0, 0): "Червоний",
    (0, 255, 0): "Зелений",
    (0, 0, 255): "Синій",
}

# Двовимірна сітка як словник
grid = {}
grid[(0, 0)] = "Старт"
grid[(1, 2)] = "Скарб"
grid[(3, 4)] = "Фініш"

print(grid[(1, 2)])  # Скарб
```

### Таблиця відстаней між містами

```python
# Кортеж (місто_а, місто_б) -> відстань
roads = {
    ("Київ", "Одеса"): 475,
    ("Київ", "Харків"): 480,
    ("Одеса", "Харків"): 650,
    ("Київ", "Львів"): 540,
    ("Львів", "Одеса"): 800,
}

# Відстань між двома містами (незалежно від напрямку)
def get_distance(city_a, city_b):
    if (city_a, city_b) in roads:
        return roads[(city_a, city_b)]
    elif (city_b, city_a) in roads:
        return roads[(city_b, city_a)]
    else:
        return None

print(get_distance("Київ", "Одеса"))  # 475
print(get_distance("Одеса", "Київ"))  # 475
print(get_distance("Київ", "Дніпро")) # None
```

---

## Порівняння кортежів та списків

| Властивість | Кортеж (`tuple`) | Список (`list`) |
|-------------|------------------|-----------------|
| Синтаксис | `(1, 2, 3)` | `[1, 2, 3]` |
| Змінність | ❌ Незмінний | ✅ Змінний |
| Швидкість створення | Швидше | Повільніше |
| Розмір пам'яті | Менше | Більше |
| Методи | `count()`, `index()` | `append()`, `remove()`, `sort()` та ін. |
| Як ключ словника | ✅ Можна | ❌ Не можна |
| Хешованість | ✅ Так (якщо елементи хешовані) | ❌ Ні |
| Використання | Дані, які не змінюються | Дані, які потребують зміни |

### Коли обирати кортеж:

```python
# Кортеж: дані фіксовані
RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)

# Кортеж: повернення кількох значень
def divide(a, b):
    return a // b, a % b  # цілочисленне ділення та залишок

quotient, remainder = divide(17, 5)

# Кортеж: записи в БД
record = ("Іван", "Петренко", 25, "іван@email.com")

# Список: колекція, яка змінюється
students = ["Іван", "Марія", "Петро"]
students.append("Олена")
```

---

## Практичні приклади використання кортежів

### Приклад 1: Зберігання координат та обчислення відстані

```python
import math

def distance(p1, p2):
    """Обчислює відстань між двома точками (кортежі)."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Точки як кортежі
point_a = (0, 0)
point_b = (3, 4)
point_c = (6, 8)

print(f"Відстань A-B: {distance(point_a, point_b):.2f}")  # 5.00
print(f"Відстань B-C: {distance(point_b, point_c):.2f}")  # 5.00
print(f"Відстань A-C: {distance(point_a, point_c):.2f}")  # 10.00

# Перевірка колінеарності三点
def are_collinear(p1, p2, p3):
    """Перевіряє, чи лежать три точки на одній прямій."""
    return (p2[1] - p1[1]) * (p3[0] - p2[0]) == (p3[1] - p2[1]) * (p2[0] - p1[0])

print(are_collinear(point_a, point_b, point_c))  # True
```

### Приклад 2: Повернення кількох значень з функції

```python
def analyze_numbers(numbers):
    """Аналізує список чисел і повертає статистику як кортеж."""
    return (
        min(numbers),
        max(numbers),
        sum(numbers) / len(numbers),
        sorted(numbers)[len(numbers) // 2],
        len(numbers)
    )

data = [23, 45, 12, 67, 34, 89, 56]
minimum, maximum, average, median, count = analyze_numbers(data)

print(f"Мінімум:     {minimum}")
print(f"Максимум:    {maximum}")
print(f"Середнє:     {average:.2f}")
print(f"Медіана:     {median}")
print(f"Кількість:   {count}")
```

### Приклад 3: Словник з кортежами як ключами для зберігання інформації про студентів

```python
# Студент: (прізвище, ім'я) -> оцінка
grades = {
    ("Петренко", "Іван"): 92,
    ("Коваленко", "Марія"): 88,
    ("Шевченко", "Петро"): 95,
    ("Бондаренко", "Олена"): 79,
    ("Мельник", "Андрій"): 85,
}

# Пошук студента
def find_student(last_name, first_name):
    return grades.get((last_name, first_name), "Не знайдено")

print(find_student("Петренко", "Іван"))    # 92
print(find_student("Тест", "Невідомий"))    # Не знайдено

# Середній бал
average = sum(grades.values()) / len(grades)
print(f"Середній бал: {average:.2f}")  # 87.80

# Найкращий студент
best = max(grades, key=grades.get)
print(f"Найкращий: {best[0]} {best[1]} ({grades[best]})")
```

### Приклад 4: Enumerативний перебір та групування

```python
# Перебір з індексами
colors = ("червоний", "зелений", "синій", "жовтий")
for i, color in enumerate(colors, 1):
    print(f"{i}. {color}")

# Групування даних за допомогою кортежів
data = [
    ("Київ", 25),
    ("Одеса", 28),
    ("Київ", 22),
    ("Харків", 20),
    ("Одеса", 30),
    ("Київ", 27),
]

# Групування за містом
from collections import defaultdict
city_temps = defaultdict(list)
for city, temp in data:
    city_temps[city].append(temp)

for city, temps in city_temps.items():
    avg = sum(temps) / len(temps)
    print(f"{city}: середня {avg:.1f}°C (з {len(temps)} вимірювань)")
```

### Приклад 5: Рекурсивна обробка вкладених кортежів

```python
def flatten(nested_tuple):
    """Розгладжує вкладений кортеж."""
    result = []
    for item in nested_tuple:
        if isinstance(item, tuple):
            result.extend(flatten(item))
        else:
            result.append(item)
    return tuple(result)

nested = ((1, 2), (3, (4, 5)), (6, (7, (8, 9))))
flat = flatten(nested)
print(flat)  # (1, 2, 3, 4, 5, 6, 7, 8, 9)

def tree_depth(nested_tuple):
    """Обчислює глибину вкладеності кортежа."""
    if not isinstance(nested_tuple, tuple):
        return 0
    return 1 + max(tree_depth(item) for item in nested_tuple) if nested_tuple else 0

print(tree_depth(((1, 2), (3, (4, 5)), (6, (7, (8, 9))))))  # 4
```

---

# Частина 2. Словники (Dictionaries)

---

## Вступ до словників

### Що таке словник?

**Словник** (dictionary, dict) — це **упорядкована** (з Python 3.7+) колекція пар **ключ-значення**, де кожен ключ пов'язаний з відповідним значенням.

**Формальне визначення:** Словник є реалізацією асоціативного масиву (або хеш-таблиці), який зберігає дані у вигляді пар `{ключ: значення}`. Ключі повинні бути хешованими (імутабельними) об'єктами, тоді як значення можуть бути будь-якого типу.

**Синтаксис:**

```python
# Порожній словник
empty = {}

# Словник з даними
student = {
    "ім'я": "Іван",
    "вік": 20,
    "група": "ПІ-21",
    "середній_бал": 4.5
}

# Через конструктор dict()
from_dict = dict(name="Іван", age=20)

# Зі списку пар
from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])
```

### Навіщо потрібні словники?

| Задача | Без словника | Зі словником |
|--------|-------------|--------------|
| Зберігати ім'я + вік | `name = "Іван"; age = 20` | `person = {"ім'я": "Іван", "вік": 20}` |
| Підрахунок частоти | Складна логіка | `counts[word] = counts.get(word, 0) + 1` |
| Швидкий пошук | Лінійний перебір O(n) | Доступ за ключем O(1) |

---

## Асоціативні масиви

### Що таке асоціативний масив?

**Асоціативний масив** — це абстрактна структура даних, яка зберігає пари **ключ-значення** та підтримує операції:
- **Вставка** (insert) — додавання нової пари
- **Пошук** (lookup) — отримання значення за ключем
- **Видалення** (delete) — видалення пари за ключем
- **Зміна** (update) — зміна значення для існуючого ключа

### Асоціативний масив vs масив

| Властивість | Звичайний масив | Асоціативний масив |
|-------------|-----------------|-------------------|
| Індекс | Ціле число (0, 1, 2...) | Будь-який хешований об'єкт |
| Доступ | `arr[i]` | `dict[key]` |
| Семантика | Порядковий доступ | Доступ за іменем/ключем |
| Приклад | `[10, 20, 30]` | `{"a": 10, "b": 20, "c": 30}` |

### Python словник як асоціативний масив

```python
# Словник Python — це реалізація асоціативного масиву
capitals = {
    "Україна": "Київ",
    "Польща": "Варшава",
    "Німеччина": "Берлін",
    "Франція": "Париж",
}

# Доступ за ключем
print(capitals["Україна"])  # Київ

# Додавання нової пари
capitals["Італія"] = "Рим"

# Зміна значення
capitals["Польща"] = "Краків"

# Видалення
del capitals["Німеччина"]
```

---

## Хеш-таблиці

### Що таке хеш-таблиця?

**Хеш-таблиця** (hash table) — це структура даних, яка реалізує асоціативний масив за допомогою **хеш-функції**. Вона дозволяє здійснювати операції введення, пошуку та видалення з **середньою складністю O(1)**.

### Як працює хеш-таблиця:

```
Ключ → Хеш-функція → Індекс у масиві → Значення

Приклад:
"Київ"  → hash("Київ")  → 7  → "Столиця"
"Одеса" → hash("Одеса")  → 3  → "Морське місто"
```

### Механізм роботи:

```python
# Внутрішньо Python виконує приблизно таке:
key = "Київ"
hash_value = hash(key)           # Обчислення хеша
index = hash_value % table_size  # Визначення індексу в таблиці
# table[index] = (key, value)   # Збереження пари
```

### Хешованість ключів

```python
# Хешовані (можуть бути ключами):
# - int, float, complex
# - str, bytes
# - tuple (якщо всі елементи хешовані)
# - frozenset

# Не хешовані (не можуть бути ключами):
# - list
# - dict
# - set

# Приклад:
d = {}
d[42] = "число"
d["hello"] = "рядок"
d[(1, 2)] = "кортеж"

# d[[1, 2]] = "список"  # TypeError: unhashable type: 'list'
```

### Колізії хешів

```python
# Різні ключі можуть мати однаковий хеш
# Python автоматично вирішує це (цепкове хешування)

# Демонстрація різних хешів
print(hash("Київ"))     # певне число
print(hash("Одеса"))     # інше число
print(hash((1, 2)))      # ще інше число

# Хеш-таблиця працює навіть при колізіях
# Але ефективність залежить від якості хеш-функції
```

### Складність операцій

| Операція | Середня | Найгірша |
|----------|---------|----------|
| Доступ | O(1) | O(n) |
| Вставка | O(1) | O(n) |
| Видалення | O(1) | O(n) |
| Пошук | O(1) | O(n) |

Найгірший випадок O(n) трапляється дуже рідко (коли всі ключі потрапляють в один слот).

---

## Створення словника

### Спосіб 1: Літерал {}

```python
# Порожній словник
empty = {}

# Словник з даними
person = {
    "ім'я": "Іван",
    "прізвище": "Петренко",
    "вік": 25,
    "місто": "Київ"
}

# З різними типами значень
mixed = {
    "число": 42,
    "рядок": "Привіт",
    "список": [1, 2, 3],
    "вкладений": {"a": 1, "b": 2}
}
```

### Спосіб 2: Конструктор dict()

```python
# З ключовими аргументами
person = dict(ім'я="Іван", вік=25)
print(person)  # {'ім'я': 'Іван', 'вік': 25}

# Зі списку пар
pairs = dict([("a", 1), ("b", 2), ("c", 3)])
print(pairs)  # {'a': 1, 'b': 2, 'c': 3}

# З zip()
keys = ["name", "age", "city"]
values = ["Іван", 25, "Київ"]
person = dict(zip(keys, values))
print(person)  # {'name': 'Іван', 'age': 25, 'city': 'Київ'}

# З dict comprehension
squares = dict((x, x**2) for x in range(5))
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Спосіб 3: Значення за замовчуванням

```python
#.fromkeys() — створення словника з однаковими значеннями
keys = ["a", "b", "c", "d"]
default_dict = dict.fromkeys(keys, 0)
print(default_dict)  # {'a': 0, 'b': 0, 'c': 0, 'd': 0}

# Значення за замовчуванням — різні для кожного ключа
keys = ["a", "b", "c"]
indexed = dict.fromkeys(keys, None)
for i, key in enumerate(keys):
    indexed[key] = i
print(indexed)  # {'a': 0, 'b': 1, 'c': 2}
```

### Спосіб 4: defaultdict

```python
from collections import defaultdict

# Автоматичне створення значень за замовчуванням
word_count = defaultdict(int)
words = ["яблуко", "банан", "яблуко", "вишня", "банан", "яблуко"]
for word in words:
    word_count[word] += 1
print(dict(word_count))  # {'яблуко': 3, 'банан': 2, 'вишня': 1}

# defaultdict зі списком
groups = defaultdict(list)
students = [("Іван", "ПІ-21"), ("Марія", "ПІ-22"), ("Петро", "ПІ-21"), ("Олена", "ПІ-22")]
for name, group in students:
    groups[group].append(name)
print(dict(groups))  # {'ПІ-21': ['Іван', 'Петро'], 'ПІ-22': ['Марія', 'Олена']}
```

---

## Доступ до елементів

### Отримання значень

```python
person = {"ім'я": "Іван", "вік": 25, "місто": "Київ"}

# Квадратні дужки (-KeyError якщо ключа немає)
print(person["ім'я"])  # Іван

# Метод get() ( повертає None або значення за замовчуванням)
print(person.get("вік"))          # 25
print(person.get("країна"))       # None
print(person.get("країна", "Невідомо"))  # Невідомо

# Безпечний доступ
try:
    value = person["незвичайний_ключ"]
except KeyError:
    value = "Ключ не знайдено"
```

### Додавання та зміна

```python
data = {}

# Додавання нової пари
data["ключ1"] = "значення1"
data["ключ2"] = "значення2"

# Зміна існуючого значення
data["ключ1"] = "нове_значення"

# Оновлення декількох пар
data.update({"ключ3": "значення3", "ключ4": "значення4"})

# setdefault — додати, якщо ключа немає
data.setdefault("ключ5", "значення_за_замовчуванням")
data.setdefault("ключ1", "інше_значення")  # не змінить, бо ключ1 вже є
```

### Видалення

```python
person = {"ім'я": "Іван", "вік": 25, "місто": "Київ", "країна": "Україна"}

# del — видалення за ключем (KeyError якщо ключа немає)
del person["країна"]

# pop() — видалення з поверненням значення
age = person.pop("вік")
print(age)  # 25

# pop() з значенням за замовчуванням
salary = person.pop("зарплата", 0)
print(salary)  # 0

# popitem() — видалення останньої пари
last = person.popitem()
print(last)  # ('місто', 'Київ')

# Очищення словника
person.clear()
print(person)  # {}
```

---

## Методи словника

### Повний каталог методів

```python
person = {"ім'я": "Іван", "вік": 25, "місто": "Київ"}
```

### Методи отримання даних

```python
# keys() — усі ключі
print(person.keys())  # dict_keys(['ім'я', 'вік', 'місто'])

# values() — усі значення
print(person.values())  # dict_values(['Іван', 25, 'Київ'])

# items() — усі пари ключ-значення
print(person.items())  # dict_items([('ім'я', 'Іван'), ('вік', 25), ('місто', 'Київ')])

# get() — отримання з значенням за замовчуванням
print(person.get("вік"))                # 25
print(person.get("вік", "Немає"))       # 25
print(person.get("зарплата", 0))        # 0

# copy() — поверхнева копія
copy_person = person.copy()
```

### Методи зміни

```python
# update() — оновлення з іншого словника
person.update({"вік": 26, "місто": "Одеса", "країна": "Україна"})
print(person)

# setdefault() — встановити, якщо ключа немає
person.setdefault("телефон", "+380501234567")
print(person.get("телефон"))  # +380501234567

# pop() — видалити та повернути
removed = person.pop("місто")
print(removed)  # Одеса

# popitem() — видалити останню пару
last_item = person.popitem()
print(last_item)  # ('телефон', '+380501234567')

# clear() — очищення
temp = {"a": 1, "b": 2}
temp.clear()
print(temp)  # {}
```

### Методи перетворення

```python
# fromkeys() — створення з однаковими значеннями
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)
print(d)  # {'a': 0, 'b': 0, 'c': 0}

# set() з items() — отримання множини ключів
keys_set = set(person.keys())
print(keys_set)

# list з items() — отримання списку пар
items_list = list(person.items())
print(items_list)
```

### Перевірка наявності ключа

```python
person = {"ім'я": "Іван", "вік": 25}

# Оператор in
print("ім'я" in person)      # True
print("зарплата" in person)  # False

# Оператор not in
print("вік" not in person)   # False
```

---

## Вкладені словники

### Структури даних з вкладеними словниками

```python
# Словник студентів
students = {
    "Іван": {
        "вік": 20,
        "група": "ПІ-21",
        "оцінки": {"математика": 92, "програмування": 88, "англійська": 75}
    },
    "Марія": {
        "вік": 19,
        "група": "ПІ-22",
        "оцінки": {"математика": 85, "програмування": 95, "англійська": 90}
    },
    "Петро": {
        "вік": 21,
        "група": "ПІ-21",
        "оцінки": {"математика": 78, "програмування": 82, "англійська": 88}
    }
}

# Доступ до вкладених значень
print(students["Іван"]["вік"])                    # 20
print(students["Марія"]["оцінки"]["програмування"])  # 95

# Безпечний доступ
def safe_get(d, *keys):
    """Безпечний доступ до вкладених словників."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return None
    return d

print(safe_get(students, "Іван", "оцінки", "математика"))  # 92
print(safe_get(students, "Олена", "вік"))  # None
```

### Перебір вкладених словників

```python
# Перебір усіх студентів та їх оцінок
for name, info in students.items():
    print(f"\nСтудент: {name}")
    print(f"  Вік: {info['вік']}")
    print(f"  Група: {info['група']}")
    print("  Оцінки:")
    for subject, grade in info['оцінки'].items():
        print(f"    {subject}: {grade}")

# Середній бал по кожному студенту
for name, info in students.items():
    avg = sum(info['оцінки'].values()) / len(info['оцінки'])
    print(f"{name}: {avg:.1f}")

# Найкращий з математики
best_math = max(students.items(), key=lambda x: x[1]['оцінки']['математика'])
print(f"Найкращий з математики: {best_math[0]} ({best_math[1]['оцінки']['математика']})")
```

---

## Dictionary comprehension

### Базовий синтаксис

```python
# {ключ: значення for елемент in коллекція}

# Квадрати чисел
squares = {x: x**2 for x in range(1, 11)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, ..., 10: 100}

# Фільтрація
even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(even_squares)  # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}

# Зміна ключів та значень
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)  # {1: 'a', 2: 'b', 3: 'c'}
```

### Практичні приклади

```python
# Підрахунок символів у рядку
text = "Привіт, світ!"
char_count = {char: text.count(char) for char in set(text)}
print(char_count)

# Створення словника з двох списків
keys = ["ім'я", "вік", "місто"]
values = ["Іван", 25, "Київ"]
person = {k: v for k, v in zip(keys, values)}
print(person)  # {'ім\'я': 'Іван', 'вік': 25, 'місто': 'Київ'}

# Групування за умовою
numbers = range(1, 21)
groups = {
    "парні": [x for x in numbers if x % 2 == 0],
    "непарні": [x for x in numbers if x % 2 != 1],
}
print(groups)

# Перетворення типів
str_numbers = {"a": "1", "b": "2", "c": "3"}
int_numbers = {k: int(v) for k, v in str_numbers.items()}
print(int_numbers)  # {'a': 1, 'b': 2, 'c': 3}
```

---

## Практичні приклади використання словників

### Приклад 1: Підрахунок частоти слів

```python
def count_words(text):
    """Підраховує частоту кожного слова у тексті."""
    words = text.lower().split()
    frequency = {}
    for word in words:
        # Видаляємо пунктуацію
        word = word.strip(".,!?;:\"'()")
        if word:
            frequency[word] = frequency.get(word, 0) + 1
    return frequency

text = """
Python — це мова програмування. Python використовується для веб-розробки,
аналізу даних та штучного інтелекту. Python проста у вивченні.
"""

freq = count_words(text)
for word, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
    print(f"{word:20} {count}")
```

### Приклад 2: Телефонна книга

```python
class PhoneBook:
    def __init__(self):
        self.contacts = {}

    def add(self, name, phone, email=None):
        """Додавання контакту."""
        self.contacts[name] = {"phone": phone, "email": email}
        print(f"Контакт '{name}' додано.")

    def find(self, name):
        """Пошук контакту."""
        return self.contacts.get(name, None)

    def remove(self, name):
        """Видалення контакту."""
        if name in self.contacts:
            del self.contacts[name]
            print(f"Контакт '{name}' видалено.")
        else:
            print(f"Контакт '{name}' не знайдено.")

    def list_all(self):
        """Виведення всіх контактів."""
        if not self.contacts:
            print("Книга порожня.")
            return
        for name, info in self.contacts.items():
            email = info['email'] or "—"
            print(f"  {name}: {info['phone']} | {email}")

    def search_by_phone(self, query):
        """Пошук за номером телефону."""
        results = {}
        for name, info in self.contacts.items():
            if query in info['phone']:
                results[name] = info
        return results

# Використання
book = PhoneBook()
book.add("Іван", "+380501234567", "ivan@email.com")
book.add("Марія", "+380671234567")
book.add("Петро", "+380509876543", "petro@email.com")

print("\nВсі контакти:")
book.list_all()

print("\nПошук за номером +38050:")
for name, info in book.search_by_phone("+38050").items():
    print(f"  {name}: {info['phone']}")
```

### Приклад 3: Конфігурація додатка

```python
# Використання вкладених словників для конфігурації
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp",
        "user": "admin",
        "password": "secret123"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8080,
        "debug": True
    },
    "logging": {
        "level": "INFO",
        "file": "/var/log/myapp.log",
        "max_size_mb": 100
    }
}

def get_config(config, *keys, default=None):
    """Отримання значення з вкладеного словника конфігурації."""
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

# Використання
db_host = get_config(config, "database", "host")
print(f"Database host: {db_host}")  # localhost

log_level = get_config(config, "logging", "level")
print(f"Log level: {log_level}")  # INFO

debug = get_config(config, "server", "debug")
print(f"Debug mode: {debug}")  # True
```

### Приклад 4: Аналіз даних

```python
def analyze_sales(sales_data):
    """Аналіз продажів за допомогою словників."""
    # Загальна сума по кожному товару
    product_totals = {}
    for sale in sales_data:
        product = sale["product"]
        amount = sale["quantity"] * sale["price"]
        product_totals[product] = product_totals.get(product, 0) + amount

    # Продажі по місяцях
    monthly = {}
    for sale in sales_data:
        month = sale["month"]
        amount = sale["quantity"] * sale["price"]
        monthly[month] = monthly.get(month, 0) + amount

    # Найпопулярніший товар за кількістю
    product_qty = {}
    for sale in sales_data:
        product = sale["product"]
        product_qty[product] = product_qty.get(product, 0) + sale["quantity"]

    best_product = max(product_qty, key=product_qty.get)

    return {
        "product_totals": product_totals,
        "monthly": monthly,
        "best_product": best_product,
        "total_revenue": sum(product_totals.values())
    }

# Тестові дані
sales = [
    {"product": "Ноутбук", "quantity": 2, "price": 25000, "month": "Січень"},
    {"product": "Телефон", "quantity": 5, "price": 12000, "month": "Січень"},
    {"product": "Ноутбук", "quantity": 1, "price": 25000, "month": "Лютий"},
    {"product": "Планшет", "quantity": 3, "price": 8000, "month": "Лютий"},
    {"product": "Телефон", "quantity": 3, "price": 12000, "month": "Березень"},
    {"product": "Ноутбук", "quantity": 1, "price": 25000, "month": "Березень"},
]

result = analyze_sales(sales)
print("Дохід по товарах:")
for product, total in result["product_totals"].items():
    print(f"  {product}: {total} грн")
print(f"\nЗагальний дохід: {result['total_revenue']} грн")
print(f"Найпопулярніший товар: {result['best_product']}")

print("\nДохід по місяцях:")
for month, total in result["monthly"].items():
    print(f"  {month}: {total} грн")
```

### Приклад 5: Кешування результатів функції

```python
def memoize(func):
    """Декоратор для кешування результатів функції."""
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            print(f"  Обчислено для {args}")
        else:
            print(f"  Взято з кешу для {args}")
        return cache[args]

    wrapper.cache = cache  # Доступ до кешу
    return wrapper

@memoize
def fibonacci(n):
    """Обчислення чисел Фібоначчі."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Перший виклик:")
print(f"fib(10) = {fibonacci(10)}")
print(f"Довжина кешу: {len(fibonacci.cache)}")

print("\nДругий виклик (з кешу):")
print(f"fib(10) = {fibonacci(10)}")
```
