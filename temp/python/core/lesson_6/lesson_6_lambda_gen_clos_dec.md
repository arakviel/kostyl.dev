# Лямбда-функції, генератори, замикання та декоратори у Python

## Зміст

### Лямбда-функції
1. [Що таке лямбда-функція?](#що-таке-лямбда-функція)
2. [Синтаксис та правила](#синтаксис-та-правила)
3. [Цілі та завдання лямбда-функцій](#цілі-та-завдання-лямбда-функцій)
4. [Практичні приклади використання лямбда-функцій](#практичні-приклади-використання-лямбда-функцій)

### Генератори
5. [Що таке генератор?](#що-таке-генератор)
6. [Цілі та завдання генераторів](#цілі-та-завдання-генераторів)
7. [Змінні та генератори](#змінні-та-генератори)
8. [Практичні приклади використання генераторів](#практичні-приклади-використання-генераторів)

### Замикання
9. [Що таке замикання?](#що-таке-замикання)
10. [Цілі та завдання замикань](#цілі-та-завдання-замикань)
11. [Змінні та замикання](#змінні-та-замикання)
12. [Практичні приклади використання замикань](#практичні-приклади-використання-замикань)

### Декоратори
13. [Що таке декоратор?](#що-таке-декоратор)
14. [Цілі та завдання декораторів](#цілі-та-завдання-декораторів)
15. [Змінні та декоратори](#змінні-та-декоратори)
16. [Практичні приклади використання декораторів](#практичні-приклади-використання-декораторів)

---

# Частина 1. Лямбда-функції (Lambda Functions)

---

## Що таке лямбда-функція?

### Визначення

**Лямбда-функція** (lambda function) — це **анонімна** (безіменна) функція, яка може бути визначена в одному рядку Python і не потребує формального імені за допомогою `def`.

**Формальне визначення:** Лямбда-функція є об'єктом функції класу `lambda`, який створюється викликом лямбда-виразу. На відміну від звичайних функцій, лямбда-функції можуть містити лише один вираз і не підтримують складні конструкції (циклі, обробку винятків, множинні оператори присвоювання тощо).

### Аналогія

| Звичайна функція | Лямбда-функція |
|------------------|----------------|
| Повний рецепт страви | Швидка порція на один раз |
| Названа функція `def square(x)` | Анонімна `lambda x: x**2` |
| Підходить для складних задач | Підходить для простих операцій |
| Може мати docstring | Не має docstring |
| Підтримує `return` | Неявний return |

### Базовий приклад

```python
# Звичайна функція
def square(x):
    return x ** 2

# Лямбда-функція — те саме, але анонімна
square_lambda = lambda x: x ** 2

# Виклик
print(square(5))          # 25
print(square_lambda(5))   # 25

# Обидві — функції
print(type(square))        # <class 'function'>
print(type(square_lambda)) # <class 'function'>
```

---

## Синтаксис та правила

### Загальний синтаксис

```python
lambda параметри: вираз
```

### Правила

1. **Один вираз:** Лямбда може містити лише один вираз (не блок коду).
2. **Неявний return:** Результат виразу автоматично повертається (без `return`).
3. **Параметри:** Аналогічні параметрам звичайних функцій.
4. **Без анотацій:** Лямбда-функції не підтримують анотації типів.
5. **Без docstring:** Лямбда-функції не можуть мати docstring.

### Варіанти параметрів

```python
# Без параметрів
greet = lambda: "Привіт!"
print(greet())  # Привіт!

# Один параметр
double = lambda x: x * 2
print(double(5))  # 10

# Два параметри
add = lambda a, b: a + b
print(add(3, 4))  # 7

# Значення за замовчуванням
power = lambda base, exp=2: base ** exp
print(power(3))      # 9
print(power(3, 3))   # 27

# *args та **kwargs
sum_all = lambda *args: sum(args)
print(sum_all(1, 2, 3, 4, 5))  # 15

# Умовний вираз (ternary)
is_even = lambda x: "Парне" if x % 2 == 0 else "Непарне"
print(is_even(4))  # Парне
print(is_even(7))  # Непарне
```

### Обмеження лямбда-функцій

```python
# НЕ МОЖНА: множинні вирази
# lambda x: x += 1; print(x)  # SyntaxError

# НЕ МОЖНА: анотації типів
# lambda x: int -> x ** 2  # SyntaxError

# НЕ МОЖНА: docstring
# lambda x: """Docstring""" x ** 2  # SyntaxError

# МОЖНА: вкладений вираз (але не рекомендується)
transform = lambda x: (x ** 2 if x > 0 else -x) + 1
print(transform(3))   # 10
print(transform(-3))  # 4
```

---

## Цілі та завдання лямбда-функцій

### 1. Аргументи функцій вищого порядку

Лямбда-функції найчастіше використовуються як аргументи для функцій `map()`, `filter()`, `sorted()` та інших функцій вищого порядку.

```python
# map(): застосування функції до кожного елемента
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# filter(): фільтрація елементів за умовою
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# sorted(): сортування за ключем
students = [("Іван", 90), ("Марія", 85), ("Петро", 92)]
by_grade = sorted(students, key=lambda s: s[1], reverse=True)
print(by_grade)  # [('Петро', 92), ('Іван', 90), ('Марія', 85)]
```

### 2. Анонімні функції для коротких операцій

Коли створення повноцінної функції `def` є надмірним.

```python
# Без лямбди
def add_five(x):
    return x + 5

# З лямбдою — компактніше
add_five = lambda x: x + 5

# Використання в одному місці
print(list(map(lambda x: x + 5, [1, 2, 3, 4, 5])))
# [6, 7, 8, 9, 10]
```

### 3. Інлайн-визначення функцій

Лямбда-функції дозволяють визначити функцію безпосередньо в місці використання.

```python
# Створення словника з трансформацією
data = {"a": "1", "b": "2", "c": "3"}
converted = dict(map(lambda item: (item[0], int(item[1])), data.items()))
print(converted)  # {'a': 1, 'b': 2, 'c': 3}

# Те саме, але з dictionary comprehension (часто краще)
converted = {k: int(v) for k, v in data.items()}
```

### 4. Карування (partial application)

```python
# Фіксація одного з аргументів
from functools import partial

multiply_by = lambda x, y: x * y
double = partial(multiply_by, 2)
triple = partial(multiply_by, 3)

print(double(5))   # 10
print(triple(5))   # 15

# Те саме без partial
double = lambda y: 2 * y
triple = lambda y: 3 * y
```

### 5. Ключі сортування складних структур

```python
# Сортування словників за значенням
scores = {"Іван": 85, "Марія": 92, "Петро": 78, "Олена": 95}
sorted_names = sorted(scores.keys(), key=lambda name: scores[name], reverse=True)
print(sorted_names)  # ['Олена', 'Марія', 'Іван', 'Петро']

# Сортування за кількома критеріями
people = [
    {"name": "Іван", "age": 25, "salary": 50000},
    {"name": "Марія", "age": 30, "salary": 70000},
    {"name": "Петро", "age": 25, "salary": 60000},
]
# Спочатку за віком, потім за зарплатою
sorted_people = sorted(people, key=lambda p: (p["age"], -p["salary"]))
for p in sorted_people:
    print(f"{p['name']}: {p['age']} років, {p['salary']} грн")
```

---

## Практичні приклади використання лямбда-функцій

### Приклад 1: Обробка колекцій даних

```python
# Дані про товари
products = [
    {"name": "Ноутбук", "price": 25000, "quantity": 5},
    {"name": "Телефон", "price": 12000, "quantity": 10},
    {"name": "Планшет", "price": 8000, "quantity": 8},
    {"name": "Навушники", "price": 1500, "quantity": 20},
]

# Додати поле "вартість" (price * quantity)
products_with_total = list(map(
    lambda p: {**p, "total": p["price"] * p["quantity"]},
    products
))

# Відфільтрувати дорогі товари (ціна > 10000)
expensive = list(filter(lambda p: p["price"] > 10000, products))

# Відсортувати за загальною вартістю
sorted_by_total = sorted(
    products_with_total,
    key=lambda p: p["total"],
    reverse=True
)

print("Товари з загальною вартістю:")
for p in sorted_by_total:
    print(f"  {p['name']:12} | {p['price']:>8} x {p['quantity']:>2} = {p['total']:>8} грн")

print(f"\nДорогі товари (>10000 грн):")
for p in expensive:
    print(f"  {p['name']}: {p['price']} грн")
```

### Приклад 2: Конвеєр обробки даних

```python
from functools import reduce

# Послідовна обробка за допомогою лямбда-функцій
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Крок 1: Фільтрація парних
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Крок 2: Піднесення до квадрату
squares = list(map(lambda x: x**2, evens))

# Крок 3: Сума
total = reduce(lambda a, b: a + b, squares)

print(f"Парні:     {evens}")
print(f"Квадрати:  {squares}")
print(f"Сума:      {total}")

# Те саме з comprehension (часто краще читається)
total_alt = sum(x**2 for x in numbers if x % 2 == 0)
print(f"Сума (альт): {total_alt}")
```

### Приклад 3: Групування та агрегація

```python
from collections import defaultdict

# Групування студентів за оцінкою
students = [
    ("Іван", 90), ("Марія", 85), ("Петро", 92),
    ("Олена", 78), ("Андрій", 88), ("Катерина", 95)
]

# Групування за діапазоном оцінки
def grade_range(grade):
    if grade >= 90: return "відмінно"
    elif grade >= 80: return "добре"
    elif grade >= 70: return "задовільно"
    else: return "незадовільно"

groups = defaultdict(list)
for name, grade in students:
    groups[grade_range(grade)].append(name)

print("Групування за оцінкою:")
for group, names in groups.items():
    print(f"  {group}: {', '.join(names)}")

# Середній бал по групах
avg_by_group = {
    group: sum(grade for name, grade in students if grade_range(grade) == group)
           / sum(1 for name, grade in students if grade_range(grade) == group)
    for group in groups
}
print("\nСередній бал по групах:")
for group, avg in avg_by_group.items():
    print(f"  {group}: {avg:.1f}")
```

### Приклад 4: Функція з лямбдою як параметром

```python
def apply_operation(a, b, operation):
    """Застосовує операцію до двох чисел."""
    return operation(a, b)

# Різні операції
print(apply_operation(10, 5, lambda a, b: a + b))    # 15
print(apply_operation(10, 5, lambda a, b: a - b))    # 5
print(apply_operation(10, 5, lambda a, b: a * b))    # 50
print(apply_operation(10, 5, lambda a, b: a / b))    # 2.0
print(apply_operation(10, 5, lambda a, b: a ** b))   # 100000

# Ланцюг операцій
operations = [
    ("додавання", lambda a, b: a + b),
    ("множення", lambda a, b: a * b),
    ("степінь", lambda a, b: a ** b),
]

a, b = 3, 4
for name, op in operations:
    print(f"{name}: {a} op {b} = {op(a, b)}")
```

---

# Частина 2. Генератори (Generators)

---

## Що таке генератор?

### Визначення

**Генератор** (generator) — це спеціальний тип функції, яка **ліниво** (lazy) генерує послідовність значень за допомогою оператора `yield` замість `return`. Замість того, щоб створювати всю послідовність одразу, генератор повертає значення **по одному**, обчислюючи їх лише тоді, коли вони потрібні.

**Формальне визначення:** Генератор є об'єктом ітератора, створеним генераторною функцією (функцією з оператором `yield`) або генераторним виразом. Генератор зберігає стан виконання між послідовними викликами, дозволяючи ліниву (lazy) оцінку послідовності.

### Приклади генераторів

```python
# Генераторна функція
def countdown(n):
    """Генератор зворотного відліку."""
    while n > 0:
        yield n
        n -= 1

# Виклик генераторної функції створює генератор
gen = countdown(5)
print(type(gen))  # <class 'generator'>

# Отримання значень
print(next(gen))  # 5
print(next(gen))  # 4
print(next(gen))  # 3

# Перебір у циклі
for value in countdown(3):
    print(value)  # 2, 1

# Перетворення на список
all_values = list(countdown(5))
print(all_values)  # [5, 4, 3, 2, 1]
```

### Як працює `yield`

```python
def simple_generator():
    print("Початок")
    yield 1
    print("Після першого yield")
    yield 2
    print("Після другого yield")
    yield 3
    print("Кінець")

gen = simple_generator()

# Викликаємо ітерацію за ітерацією
print("Створено генератор")
val1 = next(gen)  # Виконується до першого yield
print(f"Отримано: {val1}")
val2 = next(gen)  # Виконується до другого yield
print(f"Отримано: {val2}")
val3 = next(gen)  # Виконується до третього yield
print(f"Отримано: {val3}")

# Після вичерпання генератора:
try:
    next(gen)
except StopIteration:
    print("Генератор вичерпано")
```

---

## Цілі та завдання генераторів

### 1. Економія пам'яті

Генератори не зберігають усю послідовність в пам'яті. Вони обчислюють значення **на льоту**.

```python
import sys

# Список: усі значення в пам'яті
list_comp = [x**2 for x in range(1_000_000)]
print(f"Список: {sys.getsizeof(list_comp)} байт")  # ~8 MB

# Генератор: одне значення в пам'яті
gen_exp = (x**2 for x in range(1_000_000))
print(f"Генератор: {sys.getsizeof(gen_exp)} байт")  # ~200 байт
```

### 2. Лінива оцінка (lazy evaluation)

Генератор обчислює значення лише тоді, коли воно потрібне.

```python
def large_sequence():
    """Симуляція великої послідовності."""
    print("Починаємо генерацію...")
    for i in range(10_000_000):
        yield i ** 2

# Генератор не виконається, поки ми не попросимо значення
gen = large_sequence()  # Нічого не друкує

# Обчислення відбувається лише при потребі
first = next(gen)  # Друкує "Починаємо генерацію..." і повертає 0
```

### 3. Нескінченні послідовності

Генератори можуть генерувати нескінченні послідовності.

```python
def fibonacci():
    """Безконечна послідовність Фібоначчі."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Отримання перших 10 чисел Фібоначчі
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Знаходження першого числа Фібоначчі, більшого за 1000
fib = fibonacci()
for num in fib:
    if num > 1000:
        print(f"Перше число > 1000: {num}")
        break
```

### 4. Потокова обробка даних

Генератори дозволяють обробляти дані потоково, не завантажуючи пам'ять.

```python
def read_large_file(file_path):
    """Потокове читання великого файлу."""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Обробка файлу по рядках
def process_file(file_path):
    word_count = 0
    line_count = 0
    for line in read_large_file(file_path):
        line_count += 1
        word_count += len(line.split())
    return line_count, word_count
```

### 5. Пайплайни обробки даних

Генератори можна з'єднувати в ланцюги для послідовної обробки.

```python
def read_data(source):
    """Генератор читання даних."""
    for item in source:
        yield item

def filter_data(data, condition):
    """Генератор фільтрації."""
    for item in data:
        if condition(item):
            yield item

def transform_data(data, func):
    """Генератор трансформації."""
    for item in data:
        yield func(item)

# Пайплайн
raw_data = range(1, 101)
pipeline = transform_data(
    filter_data(
        read_data(raw_data),
        lambda x: x % 3 == 0
    ),
    lambda x: x ** 2
)

# Обробка перших 5 результатів
for i, value in enumerate(pipeline):
    if i >= 5:
        break
    print(value)  # 9, 36, 81, 144, 225
```

---

## Змінні та генератори

### Область видимості змінних у генераторах

Генератор зберігає стан своїх змінних між викликами `next()`.

```python
def accumulator():
    """Генератор, який накопичує суму."""
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)          # Ініціалізація (початок виконання до yield)
print(acc.send(10))  # 10  (total = 10)
print(acc.send(20))  # 30  (total = 10 + 20)
print(acc.send(30))  # 60  (total = 10 + 20 + 30)
```

### Метод `send()` — передача даних у генератор

```python
def echo():
    """Генератор з прийомом даних."""
    while True:
        value = yield
        if value == "стоп":
            break
        print(f"Отримано: {value}")

gen = echo()
next(gen)        # Ініціалізація
gen.send("Привіт")  # Отрижано: Привіт
gen.send("Світ")    # Отрижано: Світ
gen.send("стоп")    # Завершення
```

### Генератори з замиканнями

```python
def make_counter(start=0, step=1):
    """Генератор-лічильник з параметрами."""
    count = start
    while True:
        yield count
        count += step

# Різні лічильники
counter1 = make_counter(0, 1)
counter2 = make_counter(100, 5)

print([next(counter1) for _ in range(5)])  # [0, 1, 2, 3, 4]
print([next(counter2) for _ in range(5)])  # [100, 105, 110, 115, 120]
```

### Генератори та ітератори

```python
class NumberSequence:
    """Клас-ітератор, який працює як генератор."""
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

# Те саме як генератор (компактніше)
def number_sequence(start, end):
    while start < end:
        yield start
        start += 1

# Порівняння
seq_iter = NumberSequence(1, 6)
seq_gen = number_sequence(1, 6)

print(list(seq_iter))  # [1, 2, 3, 4, 5]
print(list(seq_gen))   # [1, 2, 3, 4, 5]
```

---

## Практичні приклади використання генераторів

### Приклад 1: Генератор чисел Фібоначчі

```python
def fibonacci_generator(limit=None):
    """Генератор чисел Фібоначчі з обмеженням."""
    a, b = 0, 1
    count = 0
    while limit is None or count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Перші 15 чисел Фібоначчі
print("Перші 15 чисел Фібоначчі:")
for num in fibonacci_generator(15):
    print(num, end=" ")
print()

# Числа Фібоначчі менші 1000
print("\nЧисла Фібоначчі < 1000:")
for num in fibonacci_generator():
    if num >= 1000:
        break
    print(num, end=" ")
print()

# Сума перших N чисел Фібоначчі
def fib_sum(n):
    return sum(fibonacci_generator(n))

print(f"\nСума перших 10: {fib_sum(10)}")  # 88
```

### Приклад 2: Генератор простих чисел

```python
def primes():
    """Безконечний генератор простих чисел."""
    yield 2
    candidate = 3
    while True:
        is_prime = True
        for i in range(3, int(candidate**0.5) + 1, 2):
            if candidate % i == 0:
                is_prime = False
                break
        if is_prime:
            yield candidate
        candidate += 2

# Перші 20 простих чисел
print("Перші 20 простих чисел:")
prime_gen = primes()
primes_list = [next(prime_gen) for _ in range(20)]
print(primes_list)

# Прості числа до 100
print("\nПрості числа до 100:")
for p in primes():
    if p > 100:
        break
    print(p, end=" ")
print()
```

### Приклад 3: Потокове читання файлу

```python
def read_csv_lazy(filename):
    """Потокове читання CSV без завантаження всього файлу."""
    with open(filename, 'r', encoding='utf-8') as f:
        header = f.readline().strip().split(',')
        for line in f:
            values = line.strip().split(',')
            yield dict(zip(header, values))

# Створення тестового файлу
test_data = """name,age,city,salary
Іван,25,Київ,50000
Марія,30,Одеса,70000
Петро,22,Харків,45000
Олена,28,Київ,65000
Андрій,35,Одеса,80000"""

with open('test_employees.csv', 'w', encoding='utf-8') as f:
    f.write(test_data)

# Потокова обробка
def process_large_csv(filename):
    total_salary = 0
    count = 0
    max_salary = 0
    max_name = ""

    for record in read_csv_lazy(filename):
        salary = int(record['salary'])
        total_salary += salary
        count += 1
        if salary > max_salary:
            max_salary = salary
            max_name = record['name']

    return {
        'average': total_salary / count,
        'max_salary': max_salary,
        'max_name': max_name,
        'count': count
    }

result = process_large_csv('test_employees.csv')
print(f"Середня зарплата: {result['average']:.0f} грн")
print(f"Максимальна: {result['max_salary']} грн ({result['max_name']})")
print(f"Кількість записів: {result['count']}")
```

### Приклад 4: Генератор випадкових даних

```python
import random
import string

def random_name(length=8):
    """Генератор випадкового імені."""
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_data(count=10):
    """Генератор випадкових записів."""
    for _ in range(count):
        yield {
            'name': random_name(),
            'age': random.randint(18, 65),
            'salary': random.randint(30000, 100000),
            'department': random.choice(['IT', 'HR', 'Sales', 'Marketing'])
        }

# Генерація та аналіз даних
data = list(random_data(1000))

# Аналіз за допомогою генераторних виразів
avg_salary = sum(d['salary'] for d in data) / len(data)
it_avg = sum(d['salary'] for d in data if d['department'] == 'IT') / \
         sum(1 for d in data if d['department'] == 'IT')

print(f"Загальна середня зарплата: {avg_salary:.0f} грн")
print(f"Середня зарплата в IT: {it_avg:.0f} грн")

# Групування за віковими групами
age_groups = {}
for d in data:
    group = f"{(d['age'] // 10) * 10}-{(d['age'] // 10) * 10 + 9}"
    age_groups.setdefault(group, []).append(d['salary'])

print("\nСередня зарплата за віковими групами:")
for group, salaries in sorted(age_groups.items()):
    avg = sum(salaries) / len(salaries)
    print(f"  {group} років: {avg:.0f} грн ({len(salaries)} осіб)")
```

### Приклад 5: Пайплайн обробки логів

```python
def parse_log_line(line):
    """Парсинг рядка логу."""
    parts = line.strip().split(' ')
    if len(parts) >= 3:
        return {
            'level': parts[0],
            'timestamp': parts[1],
            'message': ' '.join(parts[2:])
        }
    return None

def filter_by_level(logs, level):
    """Фільтрація за рівнем логу."""
    for log in logs:
        if log and log['level'] == level:
            yield log

def extract_messages(logs):
    """Вилучення повідомлень."""
    for log in logs:
        yield log['message']

# Тестові логи
test_logs = """INFO 2024-01-15 10:30:00 Система запущена
ERROR 2024-01-15 10:31:00 Помилка з'єднання з БД
WARNING 2024-01-15 10:32:00 Високе навантаження на CPU
INFO 2024-01-15 10:33:00 З'єднання відновлено
ERROR 2024-01-15 10:34:00 Timeout при запиті
INFO 2024-01-15 10:35:00 Запит виконано успішно
WARNING 2024-01-15 10:36:00 Мало вільної пам'яті
ERROR 2024-01-15 10:37:00 NullPointerException"""

with open('test_logs.txt', 'w') as f:
    f.write(test_logs)

# Потокова обробка логів
def process_logs(filename):
    with open(filename, 'r') as f:
        logs = (parse_log_line(line) for line in f)
        error_messages = list(extract_messages(filter_by_level(logs, 'ERROR')))
    return error_messages

errors = process_logs('test_logs.txt')
print("Помилки:")
for msg in errors:
    print(f"  - {msg}")
```

---

# Частина 3. Замикання (Closures)

---

## Що таке замикання?

### Визначення

**Замикання** (closure) — це функція, яка **запам'ятовує** змінні зі свого **лексичного оточення** (області видимості), навіть після того, як ці змінні більше не існують у викликаючому коді.

**Формальне визначення:** Замикання — це функція разом із посиланням на зовнішню область видимості, в якій вона була створена. Замикання зберігає значення змінних зовнішньої функції (free variables) у вигляді атрибуту `__closure__`.

### Приклад замикання

```python
def make_greeting(prefix):
    """Зовнішня функція — створює замикання."""
    def greet(name):
        # 'prefix' — це free variable (змінна зовнішньої області)
        return f"{prefix}, {name}!"
    return greet

# Створення замикань
hello = make_greeting("Привіт")
goodbye = make_greeting("До побачення")

# Виклик — функція "пам'ятає" значення prefix
print(hello("Іван"))       # Привіт, Іван!
print(goodbye("Марія"))    # До побачення, Марія!

# Перевірка замикання
print(hello.__closure__)           # (<cell at 0x...>,)
print(hello.__closure__[0].cell_contents)  # Привіт
```

### Структура замикання

```
make_greeting("Привіт")
  │
  ├── Створює функцію greet(name)
  │     │
  │     └── Посилається на 'prefix' = "Привіт"
  │
  └── Повертає greet

hello = greet  (з замиканням на prefix = "Привіт")
```

---

## Цілі та завдання замикань

### 1. Фабрика функцій

Замикання дозволяють створювати функції з попередньо заданими параметрами.

```python
def make_multiplier(factor):
    """Створює функцію множення на заданий коефіцієнт."""
    def multiplier(x):
        return x * factor
    return multiplier

# Різні множники
double = make_multiplier(2)
triple = make_multiplier(3)
times_10 = make_multiplier(10)

print(double(5))    # 10
print(triple(5))    # 15
print(times_10(5))  # 50

# Використання з map()
numbers = [1, 2, 3, 4, 5]
doubled = list(map(double, numbers))
print(doubled)  # [2, 4, 6, 8, 10]
```

### 2. Лічильники та акумулятори

```python
def make_counter(start=0, step=1):
    """Створює лічильник з замиканням."""
    count = start

    def counter():
        nonlocal count
        current = count
        count += step
        return current

    def get_count():
        return count

    counter.get = get_count
    return counter

# Лічильники
c1 = make_counter()
c2 = make_counter(100, 10)

print(c1())  # 0
print(c1())  # 1
print(c1())  # 2
print(c1.get())  # 3

print(c2())  # 100
print(c2())  # 110
```

### 3. Кешування (мемоізація)

```python
def memoize(func):
    """Декоратор для кешування результатів функції."""
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Без кешу це зайняло б багато часу
print(fibonacci(100))  # 354224848179261915075
print(f"Розмір кешу: {len(fibonacci.cache)}")
```

### 4. Інкапсуляція даних

```python
def make_bank_account(owner, initial_balance=0):
    """Банківський рахунок з інкапсуляцією."""
    balance = initial_balance
    transactions = []

    def deposit(amount):
        nonlocal balance
        if amount <= 0:
            return "Сума має бути додатною"
        balance += amount
        transactions.append(f"Поповнення: +{amount}")
        return f"Баланс: {balance}"

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "Недостатньо коштів"
        balance -= amount
        transactions.append(f"Зняття: -{amount}")
        return f"Баланс: {balance}"

    def get_balance():
        return balance

    def get_history():
        return transactions.copy()

    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance,
        'history': get_history,
        'owner': owner
    }

# Використання
account = make_bank_account("Іван", 1000)
print(account['deposit'](500))      # Баланс: 1500
print(account['withdraw'](200))     # Баланс: 1300
print(account['balance']())         # 1300
print(account['history'])           # ['Поповнення: +500', 'Зняття: -200']
```

---

## Змінні та замикання

### Три типи змінних у замиканнях

```python
def outer(x):  # x — параметр (local variable)
    y = 10     # y — локальна змінна outer

    def inner(z):  # z — параметр inner
        # x — free variable (змінна зовнішньої області)
        # y — free variable (змінна зовнішньої області)
        # z — local variable (локальна змінна inner)
        return x + y + z

    return inner
```

### Ключове слово `nonlocal`

`nonlocal` дозволяє змінювати значення змінної зовнішньої області.

```python
def make_accumulator(start=0):
    """Акумулятор з nonlocal."""
    total = start

    def add(value):
        nonlocal total
        total += value
        return total

    return add

acc = make_accumulator()
print(acc(10))   # 10
print(acc(20))   # 30
print(acc(30))   # 60

# Без nonlocal це не працювало б:
def broken_accumulator(start=0):
    total = start

    def add(value):
        # total += value  # UnlocalLocalError!
        total = total + value  # Створює нову локальну змінну
        return total

    return add
```

### Значення захоплюються за посиланням

```python
def make_functions():
    funcs = []
    for i in range(5):
        def func():
            return i  # Захоплює 'i' за посиланням!
        funcs.append(func)
    return funcs

# Усі функції повернуть 4 (останнє значення i)
functions = make_functions()
print([f() for f in functions])  # [4, 4, 4, 4, 4]

# Рішення: зафіксувати значення
def make_functions_fixed():
    funcs = []
    for i in range(5):
        def func(x=i):  # Значення за замовчуванням фіксується при створенні
            return x
        funcs.append(func)
    return funcs

functions = make_functions_fixed()
print([f() for f in functions])  # [0, 1, 2, 3, 4]
```

---

## Практичні приклади використання замикань

### Приклад 1: Декоратор лічильника викликів

```python
def count_calls(func):
    """Декоратор, який підраховує кількість викликів функції."""
    call_count = 0

    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"  Виклик #{call_count} функції '{func.__name__}'")
        return func(*args, **kwargs)

    wrapper.get_count = lambda: call_count
    return wrapper

@count_calls
def say_hello(name):
    print(f"  Привіт, {name}!")

say_hello("Іван")
say_hello("Марія")
say_hello("Петро")

print(f"Загальна кількість викликів: {say_hello.get_count()}")
```

### Приклад 2: Генератор паролів

```python
import random
import string

def make_password_generator(length=12, digits=True, special=True):
    """Генератор паролів з замиканням."""
    chars = string.ascii_letters
    if digits:
        chars += string.digits
    if special:
        chars += "!@#$%^&*"

    def generate():
        return ''.join(random.choices(chars, k=length))

    return generate

# Різні генератори паролів
simple_gen = make_password_generator(8, digits=True, special=False)
secure_gen = make_password_generator(16, digits=True, special=True)

print("Прості паролі:")
for _ in range(3):
    print(f"  {simple_gen()}")

print("\nБезпечні паролі:")
for _ in range(3):
    print(f"  {secure_gen()}")
```

### Приклад 3: Обмежувач частоти (rate limiter)

```python
import time

def rate_limit(max_calls, period):
    """Обмежувач частоти викликів функції."""
    calls = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            # Видаляємо виклики, які вийшли за межі періоду
            calls[:] = [t for t in calls if now - t < period]

            if len(calls) >= max_calls:
                wait_time = period - (now - calls[0])
                print(f"  Зачекайте {wait_time:.1f} сек...")
                return None

            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=3, period=5)
def fast_api_call(data):
    """Симуляція швидкого API-виклику."""
    print(f"  API виклик: {data}")
    return f"Відповідь на {data}"

# Тестування
for i in range(6):
    print(f"\nВиклик {i+1}:")
    result = fast_api_call(f"запит {i+1}")
    time.sleep(0.5)
```

### Приклад 4: Кеш з обмеженим часом життя

```python
import time

def timed_cache(ttl_seconds):
    """Кеш з обмеженим часом життя (TTL)."""
    cache = {}

    def decorator(func):
        def wrapper(*args):
            now = time.time()
            # Перевірка наявності та актуальності
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    print(f"  Кеш для {args}")
                    return result

            # Обчислення та збереження
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

@timed_cache(ttl_seconds=3)
def expensive_computation(n):
    """Дороге обчислення."""
    print(f"  Обчислення для {n}...")
    time.sleep(1)  # Симуляція обчислення
    return n ** 2

# Перший виклик — обчислення
print("Перший виклик:")
print(f"  Результат: {expensive_computation(5)}")

# Другий виклик — з кешу
print("\nДругий виклик (з кешу):")
print(f"  Результат: {expensive_computation(5)}")

# Чекаємо 4 секунди
print("\nЧекаємо 4 секунди...")
time.sleep(4)

# Третій виклик — кеш прострочений
print("\nТретій виклик (кеш прострочений):")
print(f"  Результат: {expensive_computation(5)}")
```

### Приклад 5: Система подій (event emitter)

```python
def make_event_emitter():
    """Система подій з замиканням."""
    listeners = {}

    def on(event, callback):
        """Реєстрація обробника події."""
        if event not in listeners:
            listeners[event] = []
        listeners[event].append(callback)

    def emit(event, *args, **kwargs):
        """Виклик усіх обробників події."""
        if event in listeners:
            for callback in listeners[event]:
                callback(*args, **kwargs)

    def off(event, callback=None):
        """Видалення обробника."""
        if callback is None:
            listeners.pop(event, None)
        elif event in listeners:
            listeners[event] = [cb for cb in listeners[event] if cb != callback]

    return {'on': on, 'emit': emit, 'off': off}

# Використання
emitter = make_event_emitter()

# Обробники
def on_login(user):
    print(f"  {user} увійшов у систему")

def on_login_log(user):
    print(f"  Лог: {user} увійшов о {time.strftime('%H:%M:%S')}")

# Реєстрація
emitter['on']('login', on_login)
emitter['on']('login', on_login_log)

# Виклик події
print("Подія 'login':")
emitter['emit']('login', 'Іван')
```

---

# Частина 4. Декоратори (Decorators)

---

## Що таке декоратор?

### Визначення

**Декоратор** (decorator) — це функція, яка приймає іншу функцію як аргумент та повертає нову функцію, яка зазвичай розширює або модифікує поведінку оригінальної функції.

**Формальне визначення:** Декоратор є функцією вищого порядку (higher-order function), яка реалізує патерн декоратор з книги «Design Patterns» (Gang of Four). Синтаксис `@decorator` є синтаксичним цукром (syntactic sugar) для запису `func = decorator(func)`.

### Базовий приклад

```python
def my_decorator(func):
    """Простий декоратор."""
    def wrapper(*args, **kwargs):
        print("Щось до виклику функції")
        result = func(*args, **kwargs)
        print("Щось після виклику функції")
        return result
    return wrapper

# Використання з @
@my_decorator
def say_hello(name):
    print(f"Привіт, {name}!")

say_hello("Іван")
# Виведення:
# Щось до виклику функції
# Привіт, Іван!
# Щось після виклику функції

# Те саме без @ (синонімічний запис)
def say_hello_v2(name):
    print(f"Привіт, {name}!")

say_hello_v2 = my_decorator(say_hello_v2)
```

### Як працює `@decorator`

```python
# Коли Python бачить:
@decorator
def function():
    pass

# Це еквівалентно:
def function():
    pass
function = decorator(function)
```

---

## Цілі та завдання декораторів

### 1. Логування (logging)

```python
import time
from functools import wraps

def log_execution(func):
    """Декоратор для логування викликів функції."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  Виклик {func.__name__} з аргументами: {args}, {kwargs}")
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"  {func.__name__} повернув: {result} за {duration:.4f} сек")
        return result
    return wrapper

@log_execution
def add(a, b):
    time.sleep(0.1)
    return a + b

@log_execution
def multiply(a, b):
    time.sleep(0.05)
    return a * b

print("Додавання:")
result = add(3, 4)
print(f"Результат: {result}\n")

print("Множення:")
result = multiply(5, 6)
print(f"Результат: {result}")
```

### 2. Вимірювання часу виконання

```python
import time
from functools import wraps

def timer(func):
    """Декоратор для вимірювання часу виконання."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} виконано за {elapsed:.6f} сек")
        return result
    return wrapper

@timer
def slow_function():
    """Повільна функція."""
    total = 0
    for i in range(1_000_000):
        total += i
    return total

result = slow_function()
print(f"  Результат: {result}")
```

### 3. Кешування (мемоізація)

```python
from functools import wraps

def cache(func):
    """Декоратор для кешування результатів."""
    cache_data = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache_data:
            cache_data[args] = func(*args)
            print(f"  Обчислено для {args}")
        else:
            print(f"  З кешу для {args}")
        return cache_data[args]

    wrapper.cache_info = lambda: {
        'hits': len(cache_data),
        'size': len(cache_data)
    }
    return wrapper

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Перший виклик:")
print(f"  fib(10) = {fibonacci(10)}")

print("\nДругий виклик (з кешу):")
print(f"  fib(10) = {fibonacci(10)}")

print(f"\nІнформація про кеш: {fibonacci.cache_info()}")
```

### 4. Перевірка дозволів (авторизація)

```python
from functools import wraps

def require_auth(func):
    """Декоратор для перевірки автентифікації."""
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get('is_authenticated'):
            print(f"  Помилка: користувач {user.get('name', 'Невідомий')} не автентифікований")
            return None
        return func(user, *args, **kwargs)
    return wrapper

def require_role(role):
    """Декоратор для перевірки ролі."""
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get('role') != role:
                print(f"  Помилка: потрібна роль '{role}', у користувача '{user.get('role')}'")
                return None
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_auth
@require_role('admin')
def delete_user(current_user, target_user):
    print(f"  Користувач {target_user} видалений")
    return True

# Тестування
admin = {'name': 'Іван', 'is_authenticated': True, 'role': 'admin'}
user = {'name': 'Марія', 'is_authenticated': True, 'role': 'user'}
anon = {'name': 'Анонім', 'is_authenticated': False}

print("Адмін видаляє:")
delete_user(admin, "test_user")

print("\nЮзер видаляє:")
delete_user(user, "test_user")

print("\nАнонім видаляє:")
delete_user(anon, "test_user")
```

### 5. Повторне виконання (retry)

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    """Декоратор для повторного виконання функції у разі помилки."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  Спроба {attempt}/{max_attempts}: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_function():
    """Ненадійна функція (симуляція)."""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Помилка з'єднання")
    return "Успіх!"

try:
    result = unreliable_function()
    print(f"  Результат: {result}")
except Exception as e:
    print(f"  Фінальна помилка: {e}")
```

### 6. Валідація аргументів

```python
from functools import wraps

def validate_types(*types):
    """Декоратор для перевірки типів аргументів."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            for i, (arg, expected_type) in enumerate(zip(args, types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Аргумент {i+1} має бути {expected_type.__name__}, "
                        f"отримано {type(arg).__name__}"
                    )
            return func(*args)
        return wrapper
    return decorator

def validate_range(min_val=None, max_val=None):
    """Декоратор для перевірки діапазону значень."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if min_val is not None and result < min_val:
                raise ValueError(f"Результат {result} менше за мінімум {min_val}")
            if max_val is not None and result > max_val:
                raise ValueError(f"Результат {result} більше за максимум {max_val}")
            return result
        return wrapper
    return decorator

@validate_types(int, int)
@validate_range(min_val=0)
def add_positive(a, b):
    return a + b

print(add_positive(3, 4))      # 7
print(add_positive(-1, 5))     # ValueError: Результат 4 менше за мінімум 0
# print(add_positive("3", 4))  # TypeError: Аргумент 1 має бути int
```

---

## Змінні та декоратори

### `functools.wraps` — збереження метаданих

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Зберігає метадані оригінальної функції
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Привітання користувача."""
    return f"Привіт, {name}!"

# Без @wraps:
print(greet.__name__)  # wrapper (якщо немає wraps)
print(greet.__doc__)   # Wrapper docstring (якщо немає wraps)

# З @wraps:
print(greet.__name__)  # greet
print(greet.__doc__)   # Привітання користувача.
```

### Декоратори з параметрами

```python
from functools import wraps

def repeat(times):
    """Декоратор, який повторює виклик функції задану кількість разів."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def say_hello(name):
    print(f"Привіт, {name}!")
    return f"Hello {name}"

# Виклик
results = say_hello("Іван")
# Привіт, Іван!
# Привіт, Іван!
# Привіт, Іван!
print(results)  # ['Hello Іван', 'Hello Іван', 'Hello Іван']
```

### Складні декоратори

```python
from functools import wraps
import time

def monitor(log_args=True, log_result=True, log_time=True):
    """Комплексний декоратор моніторингу."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            # Логування аргументів
            if log_args:
                print(f"  [{func_name}] Аргументи: {args}, {kwargs}")

            # Вимірювання часу
            start = time.perf_counter() if log_time else None

            # Виклик функції
            try:
                result = func(*args, **kwargs)
                error = None
            except Exception as e:
                result = None
                error = str(e)

            # Логування результату
            if log_result and error is None:
                print(f"  [{func_name}] Результат: {result}")
            elif error:
                print(f"  [{func_name}] Помилка: {error}")

            # Логування часу
            if log_time:
                elapsed = time.perf_counter() - start
                print(f"  [{func_name}] Час: {elapsed:.6f} сек")

            if error:
                raise Exception(error)
            return result
        return wrapper
    return decorator

@monitor(log_args=True, log_result=True, log_time=True)
def complex_calculation(n):
    """Складне обчислення."""
    return sum(i**2 for i in range(n))

result = complex_calculation(100000)
```

---

## Практичні приклади використання декораторів

### Приклад 1: Кеш з TTL (Time-To-Live)

```python
import time
from functools import wraps

def ttl_cache(seconds=60):
    """Кеш з обмеженим часом життя."""
    cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < seconds:
                    return result

            result = func(*args)
            cache[args] = (result, now)
            return result

        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator

@ttl_cache(seconds=3)
def get_user_data(user_id):
    """Отримання даних користувача (симуляція API)."""
    print(f"  Завантаження даних для user_id={user_id}...")
    time.sleep(0.1)
    return {"id": user_id, "name": f"User_{user_id}", "score": user_id * 10}

# Тестування
print("Перший виклик:")
print(f"  {get_user_data(1)}")

print("\nДругий виклик (з кешу):")
print(f"  {get_user_data(1)}")

print(f"\nЧекаємо 4 секунди...")
time.sleep(4)

print("\nТретій виклик (кеш прострочений):")
print(f"  {get_user_data(1)}")
```

### Приклад 2: Rate limiter для API

```python
import time
from functools import wraps
from collections import defaultdict

class RateLimiter:
    """Клас-декоратор для обмеження частоти викликів."""
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = defaultdict(list)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Очищення старих викликів
            self.calls[func.__name__] = [
                t for t in self.calls[func.__name__]
                if now - t < self.period
            ]

            if len(self.calls[func.__name__]) >= self.max_calls:
                wait = self.period - (now - self.calls[func.__name__][0])
                raise Exception(f"Ліміт викликів перевищено. Зачекайте {wait:.1f} сек")

            self.calls[func.__name__].append(now)
            return func(*args, **kwargs)
        return wrapper

# Використання
@RateLimiter(max_calls=3, period=5)
def api_call(endpoint):
    print(f"  API виклик: {endpoint}")
    return f"Відповідь від {endpoint}"

# Тестування
for i in range(5):
    try:
        print(f"\nВиклик {i+1}:")
        result = api_call(f"/api/data/{i+1}")
        print(f"  Результат: {result}")
    except Exception as e:
        print(f"  Помилка: {e}")
```

### Приклад 3: Singleton (одинак)

```python
from functools import wraps

def singleton(cls):
    """Декоратор Singleton — гарантує один екземпляр класу."""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        self.connected = False
        self.connection_id = id(self)
        print(f"  Створено з'єднання #{self.connection_id}")

    def connect(self):
        self.connected = True
        print(f"  З'єднання #{self.connection_id} встановлено")

    def query(self, sql):
        if not self.connected:
            raise Exception("З'єднання не встановлено")
        return f"Результат запиту: {sql}"

# Тестування
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(f"db1 == db2: {db1 is db2}")  # True
print(f"Один і той самий об'єкт: {db1.connection_id == db2.connection_id}")
```

### Приклад 4: Автоматичне повторне підключення

```python
import time
import random
from functools import wraps

def auto_reconnect(max_retries=3, delay=1):
    """Декоратор для автоматичного перепідключення."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    last_error = e
                    if attempt < max_retries:
                        wait = delay * (2 ** attempt)  # Exponential backoff
                        print(f"  Спроба {attempt + 1}/{max_retries}: {e}")
                        print(f"  Чекаємо {wait} сек...")
                        time.sleep(wait)
            raise last_error
        return wrapper
    return decorator

class FakeDB:
    def __init__(self):
        self.attempt = 0

    @auto_reconnect(max_retries=3, delay=0.5)
    def connect(self):
        self.attempt += 1
        if self.attempt < 3:
            raise ConnectionError(f"З'єднання розірвано (спроба {self.attempt})")
        print(f"  З'єднання встановлено на спробі {self.attempt}")
        return True

db = FakeDB()
try:
    result = db.connect()
    print(f"  Результат: {result}")
except ConnectionError as e:
    print(f"  Фінальна помилка: {e}")
```

### Приклад 5: Генератор декораторів

```python
from functools import wraps
import time

def compose(*decorators):
    """Композиція декораторів."""
    def decorator(func):
        for dec in reversed(decorators):
            func = dec(func)
        return func
    return decorator

# Базові декоратори
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  -> {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    return wrapper

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  Час: {elapsed:.6f} сек")
        return result
    return wrapper

def cache_result(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# Композиція декораторів
@compose(log_call, measure_time, cache_result)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Тестування
print("Обчислення Фібоначчі:")
result = fibonacci(30)
print(f"  Результат: {result}")
```

### Приклад 6: REST API декоратор

```python
from functools import wraps
import json

def api_endpoint(method="GET", path=None, auth_required=False):
    """Декоратор для реєстрації API-ендпоінтів."""
    endpoints = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Перевірка автентифікації
            if auth_required:
                user = kwargs.get('user') or (args[0] if args else None)
                if not user or not user.get('is_authenticated'):
                    return {"error": "Unauthorized"}, 401

            # Виклик функції
            try:
                result = func(*args, **kwargs)
                return {"data": result}, 200
            except Exception as e:
                return {"error": str(e)}, 500

        # Реєстрація ендпоінту
        route = path or f"/{func.__name__}"
        endpoints[route] = {
            'method': method,
            'handler': wrapper,
            'auth_required': auth_required
        }

        wrapper.endpoint_info = {
            'method': method,
            'path': route,
            'auth_required': auth_required
        }
        return wrapper

    decorator.endpoints = endpoints
    return decorator

# Використання
@api_endpoint(method="GET", path="/users")
def get_users():
    return [{"id": 1, "name": "Іван"}, {"id": 2, "name": "Марія"}]

@api_endpoint(method="POST", path="/users", auth_required=True)
def create_user(user, name):
    return {"id": 3, "name": name}

# Тестування
print("GET /users:")
response, status = get_users()
print(f"  Status: {status}, Data: {response['data']}")

print("\nPOST /users (неавтентифікований):")
response, status = create_user(None, "Петро")
print(f"  Status: {status}, Error: {response.get('error')}")

print("\nPOST /users (автентифікований):")
auth_user = {"is_authenticated": True, "name": "Адмін"}
response, status = create_user(auth_user, "Петро")
print(f"  Status: {status}, Data: {response['data']}")
```
