# Модуль 2. Об'єктно-орієнтоване програмування. Частина 2

## Зміст

1. [Класи та об'єкти](#класи-та-обєкти)
2. [Атрибути, поля (властивості), методи класу](#атрибути-поля-властивості-методи-класу)
3. [Перевантаження методів](#перевантаження-методів)
4. [Magic-методи, конструктори](#magic-методи-конструктори)

---

## Класи та об'єкти

### Детальний розгляд класу

**Клас** — це не просто шаблон для створення об'єктів. Це складна структура, яка визначає:

1. **Стан** (state) — набір атрибутів (даних), які зберігають інформацію про об'єкт.
2. **Поведінку** (behavior) — набір методів (функцій), які operують з атрибутами.
3. **Ідентичність** (identity) — унікальний ідентифікатор кожного екземпляра (`id()`).

### Життєвий цикл об'єкта

```
1. Створення (instantiation)
   obj = MyClass()

2. Ініціалізація (initialization)
   __init__() викликається автоматично

3. Використання (usage)
   obj.method() / obj.attribute

4. Знищення (destruction)
   __del__() викликається при збиранні сміття
```

### Детальний приклад

```python
class UserAccount:
    """Детальний приклад класу для облікового запису."""

    # Атрибут класу — лічильник створених обліків
    _total_accounts = 0

    def __init__(self, username, email, role="user"):
        """Конструктор — викликається при створенні об'єкта.

        Параметри:
            username (str): Ім'я користувача
            email (str): Email адреса
            role (str): Роль (user, admin, moderator)
        """
        # Атрибути екземпляра — унікальні для кожного об'єкта
        self.username = username
        self.email = email
        self.role = role
        self._is_active = True
        self.__login_attempts = 0  # Приватний

        # Оновлюємо лічильник класу
        UserAccount._total_accounts += 1
        self._id = UserAccount._total_accounts

    def __repr__(self):
        """Строкове представлення для розробника."""
        return f"UserAccount('{self.username}', '{self.email}', role='{self.role}')"

    def __str__(self):
        """Строкове представлення для користувача."""
        return f"{self.username} ({self.role})"

    def login(self, password):
        """Метод — вхід в систему."""
        self.__login_attempts += 1
        if self.__login_attempts > 5:
            self._is_active = False
            return False, "Акаунт заблоковано"
        return True, "Вхід виконано"

    def deactivate(self):
        """Деактивація акаунту."""
        self._is_active = False

    @classmethod
    def get_total_accounts(cls):
        """Класовий метод — отримання загальної кількості акаунтів."""
        return cls._total_accounts

    @classmethod
    def from_string(cls, user_string):
        """Альтернативний конструктор — створення з рядка."""
        username, email, role = user_string.split(":")
        return cls(username, email, role)

# Створення об'єктів
user1 = UserAccount("ivan", "ivan@example.com")
user2 = UserAccount("maria", "maria@example.com", role="admin")

# Кожен об'єкт унікальний
print(id(user1) != id(user2))  # True

# Доступ до атрибутів
print(user1.username)  # ivan
print(user2.role)      # admin

# Виклик методів
success, message = user1.login("password123")
print(f"Спроба 1: {message}")

# Альтернативний конструктор
user3 = UserAccount.from_string("petro:petro@example.com:moderator")
print(user3)  # petro (moderator)

# Атрибут класу
print(UserAccount.get_total_accounts())  # 3
```

### Створення об'єкта: що відбувається "під капотом"

```python
class Demo:
    def __new__(cls, *args, **kwargs):
        """Крок 1: Створення об'єкта (викликається першим)."""
        print("  __new__: створення об'єкта")
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        """Крок 2: Ініціалізація (викликається другим)."""
        print("  __init__: ініціалізація")
        self.value = value

    def __del__(self):
        """Крок 3: Знищення (при збиранні сміття)."""
        print(f"  __del__: знищення об'єкта {self.value}")

print("Створення:")
obj = Demo(42)

print("\nВикористання:")
print(f"  Значення: {obj.value}")

print("\nЗнищення:")
del obj
```

---

## Атрибути, поля (властивості), методи класу

### Типи атрибутів

```python
class AttributeTypes:
    """Демонстрація різних типів атрибутів."""

    # 1. Атрибут класу — спільний для всіх екземплярів
    class_attribute = "Я належу класу"

    def __init__(self, value):
        # 2. Атрибут екземпляра — унікальний для кожного об'єкта
        self.instance_attribute = value

        # 3. Приватний атрибут (name mangling)
        self.__private = "Приватний"

        # 4. Захищений атрибут (домовленість)
        self._protected = "Захищений"

    # 5. Властивість (property) — контрольований доступ
    @property
    def controlled(self):
        """Геттер — читання."""
        return self._controlled_value if hasattr(self, '_controlled_value') else 0

    @controlled.setter
    def controlled(self, value):
        """Сеттер — запис з валідацією."""
        if value < 0:
            raise ValueError("Значення не може бути від'ємним")
        self._controlled_value = value

# Демонстрація
obj1 = AttributeTypes(10)
obj2 = AttributeTypes(20)

# Атрибут класу — один на всіх
print(AttributeTypes.class_attribute)  # Я належу класу
print(obj1.class_attribute)            # Я належу класу

# Атрибут екземпляра — різний для кожного
print(obj1.instance_attribute)  # 10
print(obj2.instance_attribute)  # 20

# Властивість
obj1.controlled = 100
print(obj1.controlled)  # 100
# obj1.controlled = -5  # ValueError
```

### Методи: види та призначення

```python
class MethodDemo:
    """Демонстрація різних типів методів."""

    class_name = "MethodDemo"

    def __init__(self, value):
        self.value = value

    # 1. Метод екземпляра (instance method)
    # Перший параметр — self (посилання на об'єкт)
    def instance_method(self):
        return f"Метод екземпляра: value={self.value}"

    # 2. Класовий метод (class method)
    # Перший параметр — cls (посилання на клас)
    @classmethod
    def class_method(cls):
        return f"Класовий метод: class={cls.class_name}"

    # 3. Статичний метод (static method)
    # Не приймає ні self, ні cls
    @staticmethod
    def static_method(x, y):
        return x + y

    # 4. Властивість (property)
    @property
    def computed(self):
        return self.value ** 2

# Виклик методів
obj = MethodDemo(5)

print(obj.instance_method())  # Метод екземпляра: value=5
print(obj.class_method())     # Класовий метод: class=MethodDemo
print(obj.static_method(3, 4))  # 7
print(obj.computed)           # 25 (властивість — без дужок!)
```

### Властивості (properties) — детально

```python
class Product:
    """Товар з інкапсуляцією ціни та знижки."""

    def __init__(self, name, price):
        self.name = name
        self.__price = price
        self.__discount = 0

    # Геттер для ціни
    @property
    def price(self):
        """Поточна ціна з урахуванням знижки."""
        return self.__price * (1 - self.__discount / 100)

    # Сеттер для ціни
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self.__price = value

    # Deleter (рідко використовується)
    @price.deleter
    def price(self):
        print(f"  Видалення ціни для {self.name}")
        del self.__price

    # Властивість-обчислення (тільки читання)
    @property
    def discount(self):
        return self.__discount

    @discount.setter
    def discount(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Знижка має бути від 0 до 100")
        self.__discount = value

    @property
    def final_price(self):
        """Ціна зі знижкою (тільки читання)."""
        return self.__price * (1 - self.__discount / 100)

    @property
    def savings(self):
        """Сума знижки (тільки читання)."""
        return self.__price * self.__discount / 100

    def __str__(self):
        return f"{self.name}: {self.price:.2f} грн (знижка {self.__discount}%)"

# Використання
product = Product("Ноутбук", 25000)

print(product.price)       # 25000.0 (геттер)
product.price = 20000      # Сеттер
print(product.price)       # 20000.0

product.discount = 15      # Знижка 15%
print(product)             # Ноутбук: 17000.00 грн (знижка 15%)
print(f"Ви заощаджуєте: {product.savings:.2f} грн")

# product.discount = 150   # ValueError: Знижка має бути від 0 до 100
```

### Магічні властивості

```python
class WebPage:
    """Веб-сторінка з магічними властивостями."""

    def __init__(self, title, url, content=""):
        self.title = title
        self.url = url
        self._content = content
        self._visits = 0

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def visits(self):
        return self._visits

    def visit(self):
        self._visits += 1

    @property
    def is_popular(self):
        """Властивість-обчислення."""
        return self._visits > 1000

    @property
    def meta_description(self):
        """Для SEO — автоматичне створення мета-опису."""
        return f"{self.title} — {self._content[:100]}..."

page = WebPage("Python Course", "https://python.org", "Навчання Python")
page.visit()
page.visit()
print(f"Відвідувань: {page.visits}")  # 2
print(f"Популярна: {page.is_popular}")  # False
```

---

## Перевантаження методів

### Що таке перевантаження методів?

**Перевантаження методів** (method overloading) — це можливість визначення **кількох версій методу** з різною кількістю або типами параметрів.

**У Python:** Справжнього перевантаження методів (як у Java/C++) **немає**. Однак це реалізується через:
1. Значення за замовчуванням
2. `*args` та `**kwargs`
3. Диспетчеризацію ( singledispatch)

### Спосіб 1: Значення за замовчуванням

```python
class Calculator:
    """Калькулятор з перевантаженням через значення за замовчуванням."""

    def add(self, a, b=None, c=None):
        """Додавання 2 або 3 чисел."""
        result = a
        if b is not None:
            result += b
        if c is not None:
            result += c
        return result

calc = Calculator()
print(calc.add(2, 3))        # 5
print(calc.add(2, 3, 4))     # 9
print(calc.add(10))           # 10
```

### Спосіб 2: *args та **kwargs

```python
class Logger:
    """Логер з гнучкими параметрами."""

    def log(self, *args, level="INFO", **kwargs):
        """Логування з різною кількістю аргументів."""
        message = " ".join(str(a) for a in args)
        extra = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        if extra:
            message += f" [{extra}]"
        print(f"[{level}] {message}")

logger = Logger()
logger.log("Сервер запущено")                          # Просте повідомлення
logger.log("Помилка", level="ERROR")                   # З рівнем
logger.log("Запит", "/api/users", method="GET")        # З додатковими
```

### Спосіб 3: singledispatch

```python
from functools import singledispatch

@singledispatch
def process(data):
    """Обробка даних різних типів."""
    raise TypeError(f"Непідтримуваний тип: {type(data)}")

@process.register(int)
def _(data):
    return f"Ціле число: {data * 2}"

@process.register(str)
def _(data):
    return f"Рядок: {data.upper()}"

@process.register(list)
def _(data):
    return f"Список: {len(data)} елементів"

# Виклик
print(process(42))        # Ціле число: 84
print(process("hello"))   # Рядок: HELLO
print(process([1, 2, 3])) # Список: 3 елементів
```

### Перевантаження операторів (детально)

```python
class Vector:
    """Вектор з перевантаженням операторів."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Арифметичні оператори
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    # Порівняльні оператори
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.magnitude() < other.magnitude()

    def __le__(self, other):
        return self.magnitude() <= other.magnitude()

    # Представлення
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"

    # Довжина
    def __abs__(self):
        return self.magnitude()

    def __len__(self):
        """Довжина (не зовсім доречно, але для демонстрації)."""
        return 2  # Розмірність вектора

    def magnitude(self):
        import math
        return math.sqrt(self.x**2 + self.y**2)

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __contains__(self, value):
        """Перевірка наявності компоненти."""
        return value == self.x or value == self.y

    def __getitem__(self, index):
        """Доступ за індексом."""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Індекс поза межами")

    def __setitem__(self, index, value):
        """Зміна за індексом."""
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Індекс поза межами")

    def __iter__(self):
        """Ітерація по компонентах."""
        yield self.x
        yield self.y

    def __call__(self, scalar):
        """Виклик як функції — множення на скаляр."""
        return Vector(self.x * scalar, self.y * scalar)

# Використання
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)       # Vector(4, 6)
print(v1 - v2)       # Vector(2, 2)
print(v1 * 2)        # Vector(6, 8)
print(-v1)           # Vector(-3, -4)
print(abs(v1))       # 5.0
print(v1[0], v1[1])  # 3 4

for component in v1:
    print(component)  # 3, 4

print(3 in v1)       # True
print(v1(3))         # Vector(9, 12) — виклик як функції
```

---

## Magic-методи, конструктори

### Що таке магічні методи?

**Магічні методи** (magic methods, dunder methods) — це спеціальні методи з подвійними підкресленнями з обох боків (`__method__`), які дозволяють класу інтегруватися з вбудованими механізмами Python.

### Повний каталог магічних методів

#### 1. Створення та знищення

```python
class Resource:
    """Клас з повним життєвим циклом."""

    _instance_count = 0

    def __new__(cls, *args, **kwargs):
        """Створення об'єкта (викликається перед __init__)."""
        print("  __new__: створення об'єкта")
        instance = super().__new__(cls)
        Resource._instance_count += 1
        instance._id = Resource._instance_count
        return instance

    def __init__(self, name):
        """Ініціалізація об'єкта."""
        print("  __init__: ініціалізація")
        self.name = name

    def __del__(self):
        """Знищення об'єкта (збирання сміття)."""
        print(f"  __del__: знищення {self.name}")

    def __repr__(self):
        """Для розробника (debug, logging)."""
        return f"Resource('{self.name}')"

    def __str__(self):
        """Для користувача (print, str)."""
        return f"Ресурс: {self.name} (#{self._id})"

    def __bool__(self):
        """Для bool() та if/while."""
        return bool(self.name)

    def __sizeof__(self):
        """Розмір об'єкта в байтах."""
        import sys
        return sys.getsizeof(self.__dict__)

print("Створення:")
r = Resource("Database")

print(f"\nПредставлення:")
print(f"  repr: {repr(r)}")
print(f"  str:  {str(r)}")
print(f"  bool: {bool(r)}")

print("\nЗнищення:")
del r
```

#### 2. Арифметичні оператори

```python
class Money:
    """Гроші з повним набором арифметичних операторів."""

    def __init__(self, amount, currency="UAH"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        """Оператор +"""
        if self.currency != other.currency:
            raise ValueError("Різні валюти")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        """Оператор -"""
        if self.currency != other.currency:
            raise ValueError("Різні валюти")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other):
        """Оператор * ( Money * число)"""
        if isinstance(other, (int, float)):
            return Money(self.amount * other, self.currency)
        return NotImplemented

    def __rmul__(self, other):
        """Обернене * (число * Money)"""
        return self.__mul__(other)

    def __truediv__(self, other):
        """Оператор /"""
        if isinstance(other, (int, float)):
            return Money(self.amount / other, self.currency)
        if isinstance(other, Money):
            return self.amount / other.amount
        return NotImplemented

    def __floordiv__(self, other):
        """Оператор //"""
        return Money(self.amount // other, self.currency)

    def __mod__(self, other):
        """Оператор %"""
        return Money(self.amount % other, self.currency)

    def __pow__(self, other):
        """Оператор **"""
        return Money(self.amount ** other, self.currency)

    def __neg__(self):
        """Унарний мінус (-Money)"""
        return Money(-self.amount, self.currency)

    def __pos__(self):
        """Унарний плюс (+Money)"""
        return Money(+self.amount, self.currency)

    def __abs__(self):
        """abs(Money)"""
        return Money(abs(self.amount), self.currency)

    def __round__(self, n=0):
        """round(Money, n)"""
        return Money(round(self.amount, n), self.currency)

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

# Використання
price = Money(100, "UAH")
tax = Money(20, "UAH")

print(price + tax)        # 120.00 UAH
print(price - tax)        # 80.00 UAH
print(price * 2)          # 200.00 UAH
print(3 * price)          # 300.00 UAH (через __rmul__)
print(price / 4)          # 25.00 UAH
print(price / tax)        # 5.0 (відношення)
print(-price)             # -100.00 UAH
print(abs(Money(-50)))    # 50.00 UAH
```

#### 3. Оператори порівняння

```python
class Student:
    """Студент з порівнянням за балом."""

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        """Оператор =="""
        return self.grade == other.grade

    def __ne__(self, other):
        """Оператор !="""
        return self.grade != other.grade

    def __lt__(self, other):
        """Оператор <"""
        return self.grade < other.grade

    def __le__(self, other):
        """Оператор <="""
        return self.grade <= other.grade

    def __gt__(self, other):
        """Оператор >"""
        return self.grade > other.grade

    def __ge__(self, other):
        """Оператор >="""
        return self.grade >= other.grade

    def __hash__(self):
        """Хеш (обов'язковий при __eq__)."""
        return hash((self.name, self.grade))

    def __str__(self):
        return f"{self.name}: {self.grade}"

# Використання
s1 = Student("Іван", 90)
s2 = Student("Марія", 85)
s3 = Student("Петро", 90)

print(s1 == s3)   # True (однаковий бал)
print(s1 > s2)    # True (90 > 85)
print(s2 < s1)    # True

# Можна використовувати в set та як ключі dict
students = {s1, s2, s3}
print(f"Унікальних: {len(students)}")  # 2 (s1 та s3 вважаються однаковими)
```

#### 4. Контейнери (sequence protocol)

```python
class Playlist:
    """Плейлист з реалізацією протоколу контейнера."""

    def __init__(self, name):
        self.name = name
        self.__tracks = []

    def add(self, track):
        self.__tracks.append(track)

    def __len__(self):
        """len(playlist)"""
        return len(self.__tracks)

    def __getitem__(self, index):
        """playlist[index] або ітерація"""
        return self.__tracks[index]

    def __setitem__(self, index, value):
        """playlist[index] = value"""
        self.__tracks[index] = value

    def __delitem__(self, index):
        """del playlist[index]"""
        del self.__tracks[index]

    def __contains__(self, item):
        """item in playlist"""
        return item in self.__tracks

    def __iter__(self):
        """for track in playlist"""
        return iter(self.__tracks)

    def __reversed__(self):
        """reversed(playlist)"""
        return reversed(self.__tracks)

    def __bool__(self):
        """bool(playlist)"""
        return len(self.__tracks) > 0

    def __str__(self):
        return f"Плейлист '{self.name}': {len(self.__tracks)} треків"

# Використання
playlist = MyPlaylist("Rock Mix")
playlist.add("Bohemian Rhapsody")
playlist.add("Stairway to Heaven")
playlist.add("Hotel California")

print(len(playlist))          # 3
print(playlist[0])            # Bohemian Rhapsody
print("Hotel California" in playlist)  # True

for track in playlist:
    print(f"  - {track}")

del playlist[1]
print(f"Після видалення: {playlist}")

print(bool(playlist))         # True
```

#### 5. Виклик як функції та контекстні менеджери

```python
class PriceCalculator:
    """Калькулятор ціни, який можна викликати як функцію."""

    def __init__(self, base_price, discount=0):
        self.base_price = base_price
        self.discount = discount

    def __call__(self, quantity=1, tax_rate=0.2):
        """Виклик об'єкта як функції."""
        subtotal = self.base_price * quantity * (1 - self.discount / 100)
        tax = subtotal * tax_rate
        return subtotal + tax

    def __str__(self):
        return f"PriceCalculator(base={self.base_price}, discount={self.discount}%)"

calc = PriceCalculator(1000, discount=10)

# Об'єкт можна викликати як функцію
total = calc(3)  # 3 товари по 1000 зі знижкою 10% + ПДВ
print(f"Загальна сума: {total}")  # 3240.0

# Перевірка callable
print(callable(calc))  # True
```

```python
class DatabaseConnection:
    """Контекстний менеджер для з'єднання з БД."""

    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.connection = None

    def __enter__(self):
        """Вхід в контекст (with ... as conn)."""
        print(f"  Відкриваємо з'єднання з {self.host}/{self.database}")
        self.connection = f"Connection({self.host})"
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Вихід з контексту (автоматичне закриття)."""
        print(f"  Закриваємо з'єднання")
        self.connection = None
        if exc_type:
            print(f"  Помилка: {exc_val}")
        return False  # Не пригнічуємо винятки

# Використання
with DatabaseConnection("localhost", "mydb") as conn:
    print(f"  Працюємо з {conn}")
# Автоматично закривається навіть при помилці
```

#### 6. Серіалізація та предсталення

```python
class Config:
    """Конфігурація з різними форматами представлення."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        """Для print() та str()."""
        items = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Config({items})"

    def __repr__(self):
        """Для repr() та REPL."""
        items = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Config({items})"

    def __format__(self, format_spec):
        """Для format() та f-рядків."""
        if format_spec == "json":
            import json
            return json.dumps(self.__dict__, ensure_ascii=False)
        elif format_spec == "short":
            return f"Config({len(self.__dict__)} settings)"
        return str(self)

    def __bytes__(self):
        """Для bytes()."""
        return str(self).encode('utf-8')

    def __hash__(self):
        """Для використання як ключа словника."""
        return hash(tuple(sorted(self.__dict__.items())))

config = Config(debug=True, port=8080, host="localhost")

print(str(config))               # Config(debug=True, port=8080, host='localhost')
print(repr(config))              # Config(debug=True, port=8080, host='localhost')
print(f"{config:json}")          # {"debug": true, "port": 8080, "host": "localhost"}
print(f"{config:short}")         # Config(3 settings)
```

#### 7. Атрибути та інтенроспекція

```python
class MyClass:
    """Демонстрація магічних методів для атрибутів."""

    class_attr = 42

    def __init__(self, value):
        self.value = value

    def __getattr__(self, name):
        """Викликається, коли атрибут НЕ знайдено звичайним способом."""
        print(f"  __getattr__: шукаємо {name}")
        return f"Значення для {name} не знайдено"

    def __getattribute__(self, name):
        """Викликається ДЛЯ КОЖНОГО доступу до атрибута."""
        # super().__getattribute__(name) для стандартного пошуку
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        """Викликається при кожній зміні атрибута."""
        print(f"  __setattr__: {name} = {value}")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Викликається при видаленні атрибута."""
        print(f"  __delattr__: видаляємо {name}")
        super().__delattr__(name)

obj = MyClass(10)

# __setattr__ викликається при створенні
# __setattr__: value = 10

print(obj.value)           # 10 (звичайний доступ)
print(obj.nonexistent)     # __getattr__: шукаємо nonexistent

obj.new_attr = "test"      # __setattr__: new_attr = test
del obj.new_attr           # __delattr__: видаляємо new_attr
```

---

### Підсумок частини 2

| Концепція | Магічні методи |
|-----------|---------------|
| Створення | `__new__`, `__init__`, `__del__` |
| Представлення | `__str__`, `__repr__`, `__format__`, `__bytes__` |
| Арифметика | `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__neg__`, `__abs__` |
| Порівняння | `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__hash__` |
| Контейнери | `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__`, `__iter__` |
| Виклик | `__call__` |
| Контекст | `__enter__`, `__exit__` |
| Атрибути | `__getattr__`, `__setattr__`, `__delattr__`, `__getattribute__` |
| Інше | `__bool__`, `__sizeof__`, `__copy__`, `__deepcopy__` |
