# Модуль 2. Об'єктно-орієнтоване програмування. Частина 3

## Зміст

1. [Статичні методи та методи класу](#статичні-методи-та-методи-класу)
2. [Успадкування та інкапсуляція](#успадкування-та-інкапсуляція)
3. [Множинне успадкування та MRO](#множинне-успадкування-та-mro)
4. [Поліморфізм (детально)](#поліморфізм-детально)
5. [Перевантаження операторів](#перевантаження-операторів)
6. [Реалізація магічних методів](#реалізація-магічних-методів)

---

## Статичні методи та методи класу

### Три типи методів класу

| Тип | Декоратор | Перший параметр | Призначення |
|-----|-----------|-----------------|-------------|
| Метод екземпляра | — | `self` | Operує з атрибутами конкретного об'єкта |
| Класовий метод | `@classmethod` | `cls` | Operує з класом загалом (не з конкретним об'єктом) |
| Статичний метод | `@staticmethod` | — | Не Operує ні з self, ні з cls (самостійна функція) |

### Метод екземпляра (instance method)

```python
class User:
    def __init__(self, name, email):
        self.name = name      # Атрибут екземпляра
        self.email = email

    def greet(self):
        """Метод екземпляра — operує з self."""
        return f"Привіт, я {self.name} ({self.email})"

user = User("Іван", "ivan@example.com")
print(user.greet())  # Привіт, я Іван (ivan@example.com)
```

### Класовий метод (class method)

```python
class User:
    _next_id = 1  # Лічильник для всіх користувачів

    def __init__(self, name, email):
        self.id = User._next_id
        User._next_id += 1
        self.name = name
        self.email = email

    @classmethod
    def get_next_id(cls):
        """Класовий метод — operує з cls (класом), а не з об'єктом."""
        return cls._next_id

    @classmethod
    def from_string(cls, user_string):
        """Альтернативний конструктор — створення з рядка."""
        name, email = user_string.split(":")
        return cls(name, email)

    @classmethod
    def from_dict(cls, data):
        """Альтернативний конструктор — створення з словника."""
        return cls(data["name"], data["email"])

# Класовий метод викликається на КЛАСІ, не на об'єкті
print(User.get_next_id())  # 1

user1 = User("Іван", "ivan@example.com")
print(User.get_next_id())  # 2

user2 = User.from_string("Марія:maria@example.com")
print(User.get_next_id())  # 3

user3 = User.from_dict({"name": "Петро", "email": "petro@example.com"})
print(User.get_next_id())  # 4
```

### Статичний метод (static method)

```python
class MathHelper:
    """Допоміжний клас зі статичними методами."""

    @staticmethod
    def is_even(n):
        """Перевірка на парність — не потребує self чи cls."""
        return n % 2 == 0

    @staticmethod
    def factorial(n):
        """Обчислення факторіалу."""
        if n < 0:
            raise ValueError("Факторіал від'ємного числа не визначений")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def validate_email(email):
        """Валідація email."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

# Статичні методи викликаються на КЛАСІ або об'єкті
print(MathHelper.is_even(4))        # True
print(MathHelper.factorial(5))      # 120
print(MathHelper.validate_email("test@example.com"))  # True

# Можна і через об'єкт (але не рекомендується)
helper = MathHelper()
print(helper.is_even(3))  # False
```

### Порівняння: коли що використовувати

```python
class PaymentSystem:
    """Система оплати — демонстрація всіх трьох типів."""

    _total_transactions = 0
    _tax_rate = 0.2

    def __init__(self, amount):
        self.amount = amount
        PaymentSystem._total_transactions += 1

    # Метод екземпляра: operує з конкретним платежем
    def calculate_total(self):
        """Обчислення суми з урахуванням податку."""
        return self.amount * (1 + self._tax_rate)

    # Класовий метод: operує з класом загалом
    @classmethod
    def set_tax_rate(cls, rate):
        """Встановлення податкової ставки для всіх платежів."""
        cls._tax_rate = rate

    @classmethod
    def get_transaction_count(cls):
        """Отримання загальної кількості транзакцій."""
        return cls._total_transactions

    # Статичний метод: утиліта, не пов'язана з класом чи об'єктом
    @staticmethod
    def validate_amount(amount):
        """Валідація суми (незалежна логіка)."""
        if not isinstance(amount, (int, float)):
            raise TypeError("Сума має бути числом")
        if amount <= 0:
            raise ValueError("Сума має бути додатною")
        return True

# Використання
PaymentSystem.set_tax_rate(0.2)  # Класовий метод
PaymentSystem.validate_amount(100)  # Статичний метод

payment = PaymentSystem(100)
print(payment.calculate_total())  # Метод екземпляра: 120.0
print(f"Транзакцій: {PaymentSystem.get_transaction_count()}")  # 1
```

### Методи класу у веб-розробці (Django)

```python
class Article:
    """Модель статті (стиль Django model)."""

    _total_views = 0

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.views = 0
        self.is_published = False

    # Метод екземпляра — публікація конкретної статті
    def publish(self):
        self.is_published = True
        print(f"  Статтю '{self.title}' опубліковано")

    def add_view(self):
        self.views += 1
        Article._total_views += 1

    # Класовий метод — альтернативні конструктори
    @classmethod
    def create_draft(cls, title, author):
        """Створення чернетки."""
        return cls(title, "Чернетка...", author)

    @classmethod
    def from_dict(cls, data):
        """Створення з словника (наприклад, з JSON API)."""
        article = cls(data["title"], data["content"], data["author"])
        if data.get("is_published"):
            article.publish()
        return article

    @classmethod
    def get_popular(cls, min_views=100):
        """Отримання популярних статей (класовий метод пошуку)."""
        # У реальному Django: cls.objects.filter(views__gte=min_views)
        return f"Статті з {min_views}+ переглядами"

    # Статичний метод — утиліта
    @staticmethod
    def validate_title(title):
        """Валідація заголовка."""
        if len(title) < 5:
            raise ValueError("Заголовок занадто короткий")
        if len(title) > 200:
            raise ValueError("Заголовок занадто довгий")
        return True

    def __str__(self):
        status = "✓" if self.is_published else "○"
        return f"[{status}] {self.title} ({self.views} переглядів)"

# Використання
Article.validate_title("Як вивчити Python")  # Статичний

draft = Article.create_draft("Нова стаття", "Іван")  # Класовий
draft.publish()  # Метод екземпляра
draft.add_view()

print(draft)  # [✓] Нова стаття (1 перегляд)
```

---

## Успадкування та інкапсуляція

### Рівні доступу в ієрархії класів

```python
class Base:
    """Батьківський клас."""

    def __init__(self):
        self.public = "Публічний"
        self._protected = "Захищений"      # Доступний у нащадків
        self.__private = "Приватний"       # Name mangling → _Base__private

    def public_method(self):
        return "Публічний метод"

    def _protected_method(self):
        return "Захищений метод"

    def __private_method(self):
        return "Приватний метод"

    def get_private(self):
        """Доступ до приватного через публічний метод."""
        return self.__private

class Child(Base):
    """Дочірній клас."""

    def access_parent(self):
        """Доступ до атрибутів батьківського класу."""
        print(self.public)           # OK — публічний
        print(self._protected)       # OK — захищений (доступний нащадкам)
        # print(self.__private)      # AttributeError — приватний!
        # print(self.__private_method())  # AttributeError

        # Обхід name mangling (технічний доступ, але краще уникати)
        print(self._Base__private)   # OK, але порушує інкапсуляцію!

child = Child()
child.access_parent()
# Публічний
# Захищений
# Приватний

# Зовнішній код
print(child.public)           # OK
print(child._protected)       # OK (але не рекомендується)
# print(child.__private)      # AttributeError
# print(child._Base__private) # Технічно можна, але погана практика
```

### Інкапсуляція у веб-розробці (реальний приклад)

```python
class BaseModel:
    """Базова модель з інкапсуляцією (стиль ORM)."""

    def __init__(self):
        self._id = None
        self._created_at = None
        self._updated_at = None
        self.__is_dirty = False  # Приватний: чи був змінений

    @property
    def id(self):
        """ID — тільки читання ззовні."""
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    def _mark_dirty(self):
        """Захищений метод — позначення змін (внутрішня логіка)."""
        self.__is_dirty = True

    def save(self):
        """Збереження (контрольований доступ)."""
        from datetime import datetime
        if self.__is_dirty or self._id is None:
            self._updated_at = datetime.now()
            if self._id is None:
                self._created_at = datetime.now()
                self._id = id(self)
            self.__is_dirty = False
            print(f"  Збережено {self.__class__.__name__} #{self._id}")

    def to_dict(self):
        """Серіалізація (тільки публічні дані)."""
        raise NotImplementedError

class User(BaseModel):
    def __init__(self, username, email):
        super().__init__()
        self.__username = username  # Приватний
        self.__email = email        # Приватний
        self.__password_hash = None

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Невалідний email")
        self.__email = value
        self._mark_dirty()  # Виклик захищеного методу

    def set_password(self, password):
        self.__password_hash = hash(password)
        self._mark_dirty()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

# Використання
user = User("ivan", "ivan@example.com")
user.save()           # Збережено User #...
user.email = "new@example.com"
user.save()           # Збережено User #... (оновлення)
```

---

## Множинне успадкування та MRO

### Що таке множинне успадкування?

**Множинне успадкування** (multiple inheritance) — це механізм, за якого клас може успадкувати атрибути та методи від **декількох** батьківських класів одночасно.

```python
class Father:
    def greet(self):
        return "Привіт від батька"

    def skill(self):
        return "Вмію будувати"

class Mother:
    def greet(self):
        return "Привіт від матері"

    def skill(self):
        return "Вмію готувати"

class Child(Father, Mother):
    pass

child = Child()
print(child.greet())  # Привіт від батька (перший у MRO)
print(child.skill())  # Вмію будувати (перший у MRO)
```

### Проблема алмазу (Diamond Problem)

```python
# Проблема: A → B, A → C, B → D, C → D
# Який метод D викликати: з B чи з C?

class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

d = D()
print(d.method())  # B (не C!)
print(D.__mro__)   # Порядок розв'язання методів
```

### MRO (Method Resolution Order)

**MRO** (Method Resolution Order) — це алгоритм **C3 Linearization**, який визначає порядок пошуку методів у ланцюгу успадкування.

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    def method(self):
        return "D"

# Перевірка MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Python шукає метод у порядку MRO:
# D → B → C → A → object

d = D()
print(d.method())  # D (знайдено в D)

# Якщо D не має method:
class E(B, C):
    pass

e = E()
print(e.method())  # B (знайдено в B, який йде перед C в MRO)
print(E.__mro__)
# (<class 'E'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

### Правила C3 Linearization

```
1. Дочірній клас завжди перший у MRO
2. Батьківські класи зберігають порядок зліва направо
3. Клас не з'являється у MRO раніше свого батька
4. Загальний предок з'являється після всіх нащадків
```

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

class E(C, B):
    pass

# D(B, C) → D, B, C, A, object (B перший)
# E(C, B) → E, C, B, A, object (C перший)

print(D.__mro__)
print(E.__mro__)

# Складніша ієрархія
class X:
    pass

class Y:
    pass

class Z(X, Y):
    pass

class W(Y, X):
    pass

class V(Z, W):
    pass

print(V.__mro__)
# V → Z → X → W → Y → object
```

### super() у множинному успадкуванні

```python
class Base:
    def __init__(self):
        print(f"  Base.__init__")

class Left(Base):
    def __init__(self):
        print(f"  Left.__init__")
        super().__init__()  # Викликає НАСТУПНИЙ у MRO, а не батьківський!

class Right(Base):
    def __init__(self):
        print(f"  Right.__init__")
        super().__init__()

class Diamond(Left, Right):
    def __init__(self):
        print(f"  Diamond.__init__")
        super().__init__()

print("Створення Diamond:")
d = Diamond()
# Diamond.__init__
# Left.__init__
# Right.__init__
# Base.__init__

print(f"\nMRO: {[c.__name__ for c in Diamond.__mro__]}")
# ['Diamond', 'Left', 'Right', 'Base', 'object']
```

### Міксіни (Mixins) — практичний патерн

```python
class Loggable:
    """Міксін для логування."""

    def log(self, message):
        print(f"  [{self.__class__.__name__}] {message}")

class Serializable:
    """Міксін для серіалізації."""

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def to_json(self):
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

class Validatable:
    """Міксін для валідації."""

    _validators = {}

    @classmethod
    def add_validator(cls, field, func):
        if cls not in cls._validators:
            cls._validators[cls] = {}
        cls._validators[cls][field] = func

    def validate(self):
        validators = self._validators.get(self.__class__, {})
        errors = []
        for field, validator in validators.items():
            value = getattr(self, field, None)
            if not validator(value):
                errors.append(f"{field}: невалідне значення")
        return errors

class User(Loggable, Serializable, Validatable):
    """Користувач з логуванням, серіалізацією та валідацією."""

    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age

# Використання міксінів
user = User("ivan", "ivan@example.com", 25)

# Від Loggable
user.log("Користувач створений")

# Від Serializable
print(user.to_json())

# Від Validatable
User.add_validator("email", lambda e: "@" in (e or ""))
User.add_validator("age", lambda a: a and a >= 18)
errors = user.validate()
print(f"Помилки: {errors}")  # []
```

---

## Поліморфізм (детально)

### Статичний vs динамічний поліморфізм

```python
# Статичний поліморфізм (перевантаження методів)
# Python НЕ підтримує (але є аналоги через *args)

class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(1, 2))        # 3
print(calc.add(1, 2, 3, 4))  # 10

# Динамічний поліморфізм (перевизначення методів)
class Animal:
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return "Гав!"

class Cat(Animal):
    def speak(self):
        return "Мяу!"

def make_speak(animal: Animal):
    """Поліморфізм: функція не знає тип об'єкта."""
    print(animal.speak())

animals = [Dog(), Cat()]
for a in animals:
    make_speak(a)  # Гав! / Мяу!
```

### Абстрактний клас як контракт

```python
from abc import ABC, abstractmethod

class StorageBackend(ABC):
    """Абстрактний клас — контракт для сховища даних."""

    @abstractmethod
    def get(self, key: str):
        """Отримання значення за ключем."""
        pass

    @abstractmethod
    def set(self, key: str, value):
        """Встановлення значення."""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Видалення за ключем."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Перевірка наявності ключа."""
        pass

    # Конкретний метод — використовує абстрактні
    def update(self, data: dict):
        """Оновлення кількох значень."""
        for key, value in data.items():
            self.set(key, value)

    def get_or_set(self, key: str, default):
        """Отримання або створення зі значенням за замовчуванням."""
        if self.exists(key):
            return self.get(key)
        self.set(key, default)
        return default

class InMemoryStorage(StorageBackend):
    """Реалізація: пам'ять."""

    def __init__(self):
        self.__data = {}

    def get(self, key):
        return self.__data.get(key)

    def set(self, key, value):
        self.__data[key] = value

    def delete(self, key):
        self.__data.pop(key, None)

    def exists(self, key):
        return key in self.__data

class FileStorage(StorageBackend):
    """Реалізація: файл."""

    def __init__(self, filepath):
        self.__filepath = filepath

    def get(self, key):
        try:
            with open(self.__filepath, 'r') as f:
                for line in f:
                    k, v = line.strip().split(':', 1)
                    if k == key:
                        return v
        except FileNotFoundError:
            pass
        return None

    def set(self, key, value):
        lines = []
        found = False
        try:
            with open(self.__filepath, 'r') as f:
                for line in f:
                    k, v = line.strip().split(':', 1)
                    if k == key:
                        lines.append(f"{key}:{value}\n")
                        found = True
                    else:
                        lines.append(line)
        except FileNotFoundError:
            pass
        if not found:
            lines.append(f"{key}:{value}\n")
        with open(self.__filepath, 'w') as f:
            f.writelines(lines)

    def delete(self, key):
        lines = []
        try:
            with open(self.__filepath, 'r') as f:
                for line in f:
                    k, v = line.strip().split(':', 1)
                    if k != key:
                        lines.append(line)
        except FileNotFoundError:
            pass
        with open(self.__filepath, 'w') as f:
            f.writelines(lines)

    def exists(self, key):
        return self.get(key) is not None

# Використання через абстрактний інтерфейс
def demo_storage(storage: StorageBackend, name: str):
    print(f"\n{name}:")
    storage.set("user:1", "Іван")
    storage.set("user:2", "Марія")
    print(f"  user:1 = {storage.get('user:1')}")
    print(f"  user:2 = {storage.get('user:2')}")
    print(f"  user:3 = {storage.get('user:3')}")
    storage.delete("user:1")
    print(f"  Після видалення user:1: {storage.exists('user:1')}")

demo_storage(InMemoryStorage(), "InMemoryStorage")
demo_storage(FileStorage("/tmp/storage.txt"), "FileStorage")
```

---

## Перевантаження операторів

### Повний каталог операторів

#### Арифметичні оператори

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):       # self + other
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):      # other + self (обернений додаток)
        return self.__add__(other)

    def __iadd__(self, other):      # self += other
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):       # self - other
        return Vector(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):      # other - self
        if isinstance(other, (int, float)):
            return Vector(other - self.x, other - self.y)
        return NotImplemented

    def __mul__(self, scalar):      # self * scalar
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):     # scalar * self
        return self.__mul__(scalar)

    def __truediv__(self, scalar):  # self / scalar
        return Vector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar): # self // scalar
        return Vector(self.x // scalar, self.y // scalar)

    def __mod__(self, other):       # self % other
        import math
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __pow__(self, power):       # self ** power
        import math
        magnitude = math.sqrt(self.x**2 + self.y**2) ** power
        angle = math.atan2(self.y, self.x) * power
        return Vector(magnitude * math.cos(angle), magnitude * math.sin(angle))

    def __neg__(self):              # -self
        return Vector(-self.x, -self.y)

    def __pos__(self):              # +self
        return Vector(+self.x, +self.y)

    def __abs__(self):              # abs(self)
        import math
        return math.sqrt(self.x**2 + self.y**2)

    def __matmul__(self, other):    # self @ other (скалярний добуток)
        return self.x * other.x + self.y * other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

# Використання
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)     # Vector(4, 6)
print(v1 - v2)     # Vector(2, 2)
print(v1 * 2)      # Vector(6, 8)
print(2 * v1)      # Vector(6, 8) — через __rmul__
print(v1 @ v2)     # 11 (скалярний добуток)
print(abs(v1))     # 5.0
print(-v1)         # Vector(-3, -4)

v1 += v2
print(v1)          # Vector(4, 6) — через __iadd__
```

#### Порівняльні оператори

```python
class Version:
    """Версія ПЗ з порівнянням."""

    def __init__(self, major, minor, patch=0):
        self.major = major
        self.minor = minor
        self.patch = patch

    def _as_tuple(self):
        return (self.major, self.minor, self.patch)

    def __eq__(self, other):
        return self._as_tuple() == other._as_tuple()

    def __ne__(self, other):
        return self._as_tuple() != other._as_tuple()

    def __lt__(self, other):
        return self._as_tuple() < other._as_tuple()

    def __le__(self, other):
        return self._as_tuple() <= other._as_tuple()

    def __gt__(self, other):
        return self._as_tuple() > other._as_tuple()

    def __ge__(self, other):
        return self._as_tuple() >= other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch})"

# Використання
v1 = Version(1, 0, 0)
v2 = Version(1, 1, 0)
v3 = Version(1, 0, 0)

print(v1 < v2)    # True
print(v1 == v3)    # True
print(v2 >= v1)    # True

# Можна використовувати в sorted()
versions = [Version(2, 0), Version(1, 1), Version(1, 0, 1), Version(1, 1, 0)]
print(sorted(versions))  # [1.0.1, 1.1.0, 1.1.0, 2.0.0]
```

#### Бітові оператори

```python
class Flags:
    """Бітові прапорці."""

    READ = 1      # 001
    WRITE = 2     # 010
    EXECUTE = 4   # 100

    def __init__(self, value=0):
        self.value = value

    def __and__(self, other):       # self & other
        return Flags(self.value & other.value)

    def __or__(self, other):        # self | other
        return Flags(self.value | other.value)

    def __xor__(self, other):       # self ^ other
        return Flags(self.value ^ other.value)

    def __invert__(self):           # ~self
        return Flags(~self.value)

    def __lshift__(self, n):        # self << n
        return Flags(self.value << n)

    def __rshift__(self, n):        # self >> n
        return Flags(self.value >> n)

    def __contains__(self, flag):   # flag in self
        return (self.value & flag.value) == flag.value

    def __str__(self):
        flags = []
        if self.value & self.READ:
            flags.append("READ")
        if self.value & self.WRITE:
            flags.append("WRITE")
        if self.value & self.EXECUTE:
            flags.append("EXECUTE")
        return f"Flags({', '.join(flags) or 'NONE'})"

# Використання
permissions = Flags(Flags.READ | Flags.WRITE)
print(permissions)  # Flags(READ, WRITE)

print(Flags.READ in permissions)     # True
print(Flags.EXECUTE in permissions)  # False

permissions |= Flags.EXECUTE
print(permissions)  # Flags(READ, WRITE, EXECUTE)
```

---

## Реалізація магічних методів

### Комплексний приклад: інтерфейс кошика для інтернет-магазину

```python
from datetime import datetime

class Product:
    """Товар з повним набором магічних методів."""

    def __init__(self, name, price, category="Інше"):
        self.name = name
        self.price = price
        self.category = category
        self._reviews = []
        self._created_at = datetime.now()

    # Представлення
    def __str__(self):
        return f"{self.name} — {self.price:.2f} грн"

    def __repr__(self):
        return f"Product('{self.name}', {self.price}, '{self.category}')"

    def __format__(self, format_spec):
        if format_spec == "brief":
            return self.name
        elif format_spec == "full":
            return f"{self.name} ({self.category}) — {self.price:.2f} грн"
        return f"{self.price:.2f} {format_spec}" if format_spec else str(self)

    # Арифметика
    def __add__(self, other):
        """Додавання товарів — створення набору."""
        if isinstance(other, Product):
            return [self, other]
        return NotImplemented

    def __mul__(self, quantity):
        """Множення на кількість."""
        if isinstance(quantity, int) and quantity > 0:
            return CartItem(self, quantity)
        return NotImplemented

    def __rmul__(self, quantity):
        return self.__mul__(quantity)

    # Порівняння
    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __lt__(self, other):
        return self.price < other.price

    def __le__(self, other):
        return self.price <= other.price

    def __hash__(self):
        return hash((self.name, self.price))

    # Контейнерні протоколи
    def __len__(self):
        """Кількість відгуків."""
        return len(self._reviews)

    def __contains__(self, review):
        return review in self._reviews

    def __iter__(self):
        return iter(self._reviews)

    def __bool__(self):
        return self.price > 0

    # Виклик
    def __call__(self, review_text, rating=5):
        """Додавання відгуку викликом товару."""
        self._reviews.append({"text": review_text, "rating": rating})

    # Атрибути
    def __getattr__(self, name):
        """Динамічні атрибути."""
        if name.startswith("review_"):
            index = int(name.split("_")[1])
            if 0 <= index < len(self._reviews):
                return self._reviews[index]
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    # Контекст
    def __enter__(self):
        """Контекстний менеджер — тимчасова знижка."""
        self._original_price = self.price
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.price = self._original_price
        return False

class CartItem:
    """Елемент кошика."""

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity} = {self.total:.2f} грн"

    def __add__(self, other):
        """Об'єднання однакових товарів."""
        if isinstance(other, CartItem) and self.product == other.product:
            return CartItem(self.product, self.quantity + other.quantity)
        return NotImplemented

    def __iadd__(self, quantity):
        """Збільшення кількості."""
        self.quantity += quantity
        return self

class ShoppingCart:
    """Кошик з повним набором магічних методів."""

    def __init__(self, owner="Гість"):
        self.owner = owner
        self.__items = []

    def add(self, product, quantity=1):
        """Додавання товару."""
        for item in self.__items:
            if item.product == product:
                item.quantity += quantity
                return
        self.__items.append(CartItem(product, quantity))

    def remove(self, product):
        """Видалення товару."""
        self.__items = [i for i in self.__items if i.product != product]

    # Контейнерні протоколи
    def __len__(self):
        return sum(item.quantity for item in self.__items)

    def __getitem__(self, index):
        return self.__items[index]

    def __setitem__(self, index, item):
        self.__items[index] = item

    def __delitem__(self, index):
        del self.__items[index]

    def __contains__(self, product):
        return any(item.product == product for item in self.__items)

    def __iter__(self):
        return iter(self.__items)

    def __bool__(self):
        return len(self.__items) > 0

    # Представлення
    def __str__(self):
        if not self.__items:
            return f"Кошик ({self.owner}): порожній"
        items = "\n  ".join(str(item) for item in self.__items)
        return f"Кошик ({self.owner}):\n  {items}\n  Разом: {self.total:.2f} грн"

    def __repr__(self):
        return f"ShoppingCart(owner='{self.owner}', items={len(self.__items)})"

    # Арифметика
    @property
    def total(self):
        return sum(item.total for item in self.__items)

    def __add__(self, other):
        """Об'єднання кошиків."""
        if isinstance(other, ShoppingCart):
            new_cart = ShoppingCart(f"{self.owner} + {other.owner}")
            for item in self.__items:
                new_cart.add(item.product, item.quantity)
            for item in other.__items:
                new_cart.add(item.product, item.quantity)
            return new_cart
        return NotImplemented

    def __iadd__(self, item):
        """Додавання товару через +=."""
        if isinstance(item, CartItem):
            self.add(item.product, item.quantity)
        elif isinstance(item, Product):
            self.add(item)
        return self

    # Контекстний менеджер
    def __enter__(self):
        print(f"  Кошик {self.owner} відкрито")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Кошик {self.owner} закрито")
        if exc_type:
            print(f"  Помилка: {exc_val}")
        return False

    # Серіалізація
    def to_dict(self):
        return {
            "owner": self.owner,
            "items": [
                {"product": item.product.name, "quantity": item.quantity, "total": item.total}
                for item in self.__items
            ],
            "total": self.total
        }

# Використання
laptop = Product("Ноутбук", 25000, "Техніка")
mouse = Product("Миша", 1500, "Аксесуари")
keyboard = Product("Клавіатура", 3000, "Аксесуари")

# Представлення
print(laptop)                    # Ноутбук — 25000.00 грн
print(f"{laptop:brief}")        # Ноутбук
print(f"{laptop:full}")         # Ноутбук (Техніка) — 25000.00 грн
print(f"{laptop:грн}")         # 25000.00 грн

# Порівняння
print(laptop > mouse)           # True
print(laptop == Product("Ноутбук", 25000))  # True

# Виклик — додавання відгуку
laptop("Чудовий ноутбук!", 5)
laptop("Гарна клавіатура", 4)
print(f"Відгуки: {len(laptop)}")  # 2

# Контекстний менеджер — тимчасова знижка
with laptop:
    laptop.price = 20000
    print(f"Ціна зі знижкою: {laptop}")  # 20000.00 грн
print(f"Ціна після: {laptop}")  # 25000.00 грн

# Кошик
cart1 = ShoppingCart("Іван")
cart1.add(laptop, 1)
cart1.add(mouse, 2)

cart2 = ShoppingCart("Марія")
cart2.add(keyboard, 1)
cart2.add(mouse, 1)

print(cart1)
# Кошик (Іван):
#   Ноутбук x1 = 25000.00 грн
#   Миша x2 = 3000.00 грн
#   Разом: 28000.00 грн

# Об'єднання кошиків
combined = cart1 + cart2
print(combined)

# Операції з кошиком
print(f"Товарів у кошику: {len(cart1)}")  # 3
print(f"Ноутбук в кошику: {laptop in cart1}")  # True
```

---

### Підсумок частини 3

| Концепція | Деталі |
|-----------|--------|
| Статичні методи | `@staticmethod` — незалежна утиліта |
| Класові методи | `@classmethod` — operує з класом, альтернативні конструктори |
| Name mangling | `__attr` → `_Class__attr` — приховування |
| MRO | C3 Linearization — порядок пошуку методів |
| `super()` | Виклик наступного у MRO, а не батьківського |
| Міксіни | Класи-додатки для розширення функціональності |
| Перевантаження | `__add__`, `__sub__`, `__mul__` та ін. |
| Обернені оператори | `__radd__`, `__rmul__` — коли operands в різному порядку |
| Вбудовані операції | `len()`, `str()`, `bool()`, `iter()` через магічні методи |
