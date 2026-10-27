# Модуль 2. Об'єктно-орієнтоване програмування. Частина 1

## Зміст

1. [Вступ до ООП](#вступ-до-ооп)
2. [Поняття ООП](#поняття-ооп)
3. [Інкапсуляція](#інкапсуляція)
4. [Успадкування](#успадкування)
5. [Поліморфізм](#поліморфізм)
6. [Качина типізація (duck typing)](#качина-типізація-duck-typing)
7. [Типи даних, що визначаються користувачем](#типи-даних-що-визначаються-користувачем)

---

## Вступ до ООП

### Що таке об'єктно-орієнтоване програмування?

**Об'єктно-орієнтоване програмування** (ООП, Object-Oriented Programming) — це **парадигма програмування**, заснована на концепції **об'єктів**, які поєднують дані (атрибути) та поведінку (методи) в єдину структуру.

На відміну від **процедурного** програмування, де код організований навколо функцій, ООП організовує навколо **об'єктів**, які моделюють реальні або абстрактні сутності.

### Чому ООП?

**Проблема процедурного підходу:**

```python
# Процедурний підхід — дані та функції розділені
users = [
    {"name": "Іван", "age": 25, "email": "ivan@example.com"},
    {"name": "Марія", "age": 30, "email": "maria@example.com"},
]

def send_email(user, message):
    print(f"Надсилаємо {message} на {user['email']}")

def get_user_age(user):
    return user['age']

def is_adult(user):
    return user['age'] >= 18

# Проблеми:
# 1. Дані розкидані — немає єдиної структури
# 2. Функції не пов'язані з даними
# 3. Додавання нового типу (адміністратор) вимагає зміни всіх функцій
# 4. Конфлікти імен (send_email для користувача vs для листа)
```

**Рішення з ООП:**

```python
# ООП — дані та поведінка об'єднані
class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def send_email(self, message):
        print(f"Надсилаємо {message} на {self.email}")

    def is_adult(self):
        return self.age >= 18

# Кожен користувач — автономний об'єкт
user1 = User("Іван", 25, "ivan@example.com")
user2 = User("Марія", 30, "maria@example.com")

user1.send_email("Ласкаво просимо!")  # Автоматично знає свій email
```

### Чотири стовпи ООП

| Стовп | Опис | Аналогія |
|-------|------|----------|
| **Інкапсуляція** | Приховування внутрішньої реалізації | Банкомат: бачиш кнопки, але не внутрішню електроніку |
| **Успадкування** | Передача властивостей від батьківського класу | Дитина успадкувала риси батьків |
| **Поліморфізм** | Один інтерфейс — різна реалізація | Той самий кнопка "Увімкнути" на телевізорі та магнітофоні |
| **Абстракція** | Спрощення складних систем | На карті метро ти бачиш схему, а не реальну географію |

---

## Поняття ООП

### Ключові терміни

**Клас** (class) — це **шаблон** (blueprint), за яким створюються об'єкти. Визначає, які атрибути та методи матиме об'єкт.

**Об'єкт** (object) — це **екземпляр** класу, конкретна сутність, створена за шаблоном.

**Атрибут** (attribute) — це **змінна**, яка належить об'єкту або класу (дані).

**Метод** (method) — це **функція**, яка належить класу та operує з атрибутами об'єкта.

### Аналогія

```
Клас = Архітектурний план будинку
Об'єкт = Конкретний будинок, побудований за планом
Атрибут = Кількість кімнат, площа, колір стін
Метод = Увімкнути світло, відчинити вікно, прибрати
```

### Приклад: клас та об'єкти

```python
class Car:
    """Клас автомобіля — шаблон для створення машин."""

    # Атрибут класу (спільний для всіх об'єктів)
    wheels = 4

    def __init__(self, brand, model, year):
        """Конструктор — ініціалізація атрибутів об'єкта."""
        self.brand = brand    # Атрибут екземпляра
        self.model = model
        self.year = year
        self.speed = 0        # Початкова швидкість

    def accelerate(self, delta):
        """Метод — збільшення швидкості."""
        self.speed += delta
        print(f"{self.brand} {self.model} розганяється до {self.speed} км/год")

    def brake(self):
        """Метод — гальмування."""
        self.speed = 0
        print(f"{self.brand} {self.model} зупинився")

# Створення об'єктів (екземплярів класу)
car1 = Car("Toyota", "Camry", 2023)
car2 = Car("BMW", "X5", 2024)

# Кожен об'єкт має свої атрибути
print(car1.brand)  # Toyota
print(car2.brand)  # BMW

# Кожен об'єкт викликає ті самі методи незалежно
car1.accelerate(60)  # Toyota Camry розганяється до 60 км/год
car2.accelerate(80)  # BMW X5 розганяється до 80 км/год

# Атрибут класу спільний
print(car1.wheels)  # 4
print(car2.wheels)  # 4
```

### Типи атрибутів

```python
class Example:
    class_attr = "Я атрибут класу"  # Атрибут класу

    def __init__(self):
        self.instance_attr = "Я атрибут екземпляра"  # Атрибут екземпляра

obj = Example()

# Доступ
print(obj.class_attr)       # Я атрибут класу
print(obj.instance_attr)    # Я атрибут екземпляра

# Різниця:
# Атрибут класу — один на всі об'єкти
# Атрибут екземпляра — унікальний для кожного об'єкта
```

### Область видимості атрибутів

```python
class Scope:
    def __init__(self):
        self.public = "Публічний"          # Доступний скрізь
        self._protected = "Захищений"      # Доступний у класі та нащадках (домовленість)
        self.__private = "Приватний"       # Доступний лише у класі (name mangling)

s = Scope()
print(s.public)        # Публічний
print(s._protected)    # Захищений (але краще не використовувати ззовні)
# print(s.__private)   # AttributeError
print(s._Scope__private)  # Приватний (name mangling — technical access)
```

---

## Інкапсуляція

### Що таке інкапсуляція?

**Інкапсуляція** (encapsulation) — це принцип ООП, згідно з яким **внутрішня реалізація** об'єкта прихована від зовнішнього коду, а доступ до даних здійснюється через **контрольований інтерфейс** (методи).

**Формальне визначення:** Інкапсуляція — це механізм об'єднання даних та методів, які operують з цими даними, в єдину одиницю (клас), та обмеження доступу до деяких компонентів об'єкта ззовні.

**Навіщо потрібна:**
1. **Захист даних:** Запобігання випадковій зміні внутрішнього стану.
2. **Інкапсуляція складності:** Зовнішній код не повинен знати, як працює внутрішня логіка.
3. **Підтримка:** Можна змінювати внутрішню реалізацію, не ламаючи зовнішній код.
4. **Тестування:** Легше тестувати компоненти з чітким інтерфейсом.

### Рівні доступу в Python

| Рівень | Синтаксис | Опис |
|--------|-----------|------|
| Публічний | `self.name` | Доступний скрізь |
| Захищений | `self._name` | Доступний у класі та нащадках (домовленість) |
| Приватний | `self.__name` | Name mangling: доступ лише всередині класу |

### Приклад: інкапсуляція в дії

```python
class BankAccount:
    """Банківський рахунок з інкапсуляцією."""

    def __init__(self, owner, balance=0):
        self.owner = owner              # Публічний
        self.__balance = balance        # Приватний — немає прямого доступу!
        self.__transaction_log = []     # Приватний

    def deposit(self, amount):
        """Поповнення рахунку (контрольований доступ)."""
        if amount <= 0:
            raise ValueError("Сума поповнення має бути додатною")
        self.__balance += amount
        self.__log_transaction(f"Поповнення: +{amount}")
        return self.__balance

    def withdraw(self, amount):
        """Зняття коштів (контрольований доступ)."""
        if amount <= 0:
            raise ValueError("Сума зняття має бути додатною")
        if amount > self.__balance:
            raise ValueError("Недостатньо коштів")
        self.__balance -= amount
        self.__log_transaction(f"Зняття: -{amount}")
        return self.__balance

    def get_balance(self):
        """Отримання балансу (read-only властивість)."""
        return self.__balance

    def get_history(self):
        """Отримання історії транзакцій."""
        return self.__transaction_log.copy()

    def __log_transaction(self, message):
        """Приватний метод — логування (внутрішня реалізація)."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__transaction_log.append(f"[{timestamp}] {message}")

# Використання
account = BankAccount("Іван", 1000)
print(account.owner)           # Іван (публічний — OK)
# print(account.__balance)     # AttributeError (приватний — заборонено!)
print(account.get_balance())   # 1000 (контрольований доступ — OK)

account.deposit(500)
account.withdraw(200)
print(account.get_balance())   # 1300

# Історія транзакцій
for entry in account.get_history():
    print(entry)
```

### Інкапсуляція у веб-розробці (Django/Flask)

```python
class User:
    """Модель користувача (стиль Django)."""

    def __init__(self, username, email, password_hash):
        self.__username = username
        self.__email = email
        self.__password_hash = password_hash  # Ніколи не зберігаємо пароль відкрито!
        self.__is_active = True

    @property
    def username(self):
        """Геттер — тільки читання."""
        return self.__username

    @property
    def email(self):
        """Геттер для email."""
        return self.__email

    @email.setter
    def email(self, value):
        """Сеттер з валідацією."""
        if "@" not in value:
            raise ValueError("Невалідний email")
        self.__email = value

    def check_password(self, password):
        """Перевірка паролю (без його розкриття)."""
        # У реальному додатку тут хешування
        return self.__password_hash == hash(password)

    def deactivate(self):
        """Деактивація акаунту."""
        self.__is_active = False

    @property
    def is_active(self):
        return self.__is_active

# Використання
user = User("ivan", "ivan@example.com", hash("secret123"))
print(user.username)           # ivan
print(user.is_active)          # True
# user.__password_hash         # AttributeError — пароль захищений!
user.deactivate()
print(user.is_active)          # False
```

### property — Python-стиль інкапсуляції

```python
class Circle:
    """Коло з інкапсуляцією радіусу."""

    def __init__(self, radius):
        self.__radius = radius  # Приватний атрибут

    @property
    def radius(self):
        """Геттер — отримання радіусу."""
        return self.__radius

    @radius.setter
    def radius(self, value):
        """Сеттер — встановлення з валідацією."""
        if value <= 0:
            raise ValueError("Радіус має бути додатним")
        self.__radius = value

    @property
    def area(self):
        """Властивість-обчислення (тільки читання)."""
        import math
        return math.pi * self.__radius ** 2

    @property
    def circumference(self):
        """Властивість-обчислення."""
        import math
        return 2 * math.pi * self.__radius

# Використання
c = Circle(5)
print(c.radius)          # 5 (геттер)
print(f"Площа: {c.area:.2f}")           # 78.54
print(f"Довжина кола: {c.circumference:.2f}")  # 31.42

c.radius = 10            # Сеттер — працює
# c.radius = -1          # ValueError: Радіус має бути додатним
# c.area = 100           # AttributeError: can't set (тільки читання)
```

---

## Успадкування

### Що таке успадкування?

**Успадкування** (inheritance) — це механізм ООП, за якого **новий клас** (нащадок, дочірній) отримує атрибути та методи **існуючого класу** (батьківського) та може додавати власні або перевизначати успадковані.

**Формальне визначення:** Успадкування реалізує відношення "is-a" (є), де нащадок є спеціалізованим випадком батьківського класу.

**Навіщо потрібне:**
1. **Повторне використання коду:** Не потрібно дублювати спільну логіку.
2. **Ієрархія класів:** Природна організація сутностей (Транспорт → Автомобіль, Мотоцикл).
3. **Розширюваність:** Можна додавати нову функціональність, не змінюючи батьківський клас.
4. **Підтримка поліморфізму:** Різні класи можуть використовуватися через єдиний інтерфейс.

### Базовий синтаксис

```python
class Animal:
    """Батьківський клас — тварина."""

    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.is_alive = True

    def speak(self):
        return f"{self.name} видає звук"

    def describe(self):
        return f"{self.name} — {self.species}"

class Dog(Animal):
    """Дочірній клас — собака (успадковує від Animal)."""

    def __init__(self, name, breed):
        super().__init__(name, species="Собака")  # Виклик батьківського конструктора
        self.breed = breed  # Новий атрибут
        self.tricks = []

    def speak(self):
        """Перевизначення методу (override)."""
        return f"{self.name} гавкає: Гав!"

    def learn_trick(self, trick):
        """Новий метод — тільки для собак."""
        self.tricks.append(trick)

    def show_tricks(self):
        return f"{self.name} знає: {', '.join(self.tricks)}"

class Cat(Animal):
    """Дочірній клас — кіт."""

    def __init__(self, name, color):
        super().__init__(name, species="Кіт")
        self.color = color

    def speak(self):
        return f"{self.name} нявкає: Мяу!"

    def purr(self):
        return f"{self.name} муркоче..."

# Використання
dog = Dog("Рекс", "Німецька вівчарка")
cat = Cat("Мурчик", "Рудий")

print(dog.describe())    # Рекс — Собака (успадкований метод)
print(dog.speak())       # Рекс гавкає: Гав! (перевизначений)
print(cat.speak())       # Мурчик нявкає: Мяu! (перевизначений)

dog.learn_trick("апорт")
dog.learn_trick("сидіти")
print(dog.show_tricks())  # Рекс знає: апорт, сидіти

# Перевірка спадкування
print(isinstance(dog, Animal))  # True (Dog є Animal)
print(isinstance(dog, Dog))     # True
print(isinstance(cat, Dog))     # False
```

### Успадкування у веб-розробці (моделі)

```python
class BaseModel:
    """Базова модель (аналог Django BaseModel)."""

    def __init__(self):
        self.id = None
        self.created_at = None
        self.updated_at = None

    def save(self):
        """Збереження в базу даних."""
        from datetime import datetime
        self.updated_at = datetime.now()
        if self.id is None:
            self.created_at = datetime.now()
            print(f"  Створено запис {self.__class__.__name__} id={id(self)}")
        else:
            print(f"  Оновлено запис {self.__class__.__name__} id={self.id}")

    def delete(self):
        print(f"  Видалено запис {self.__class__.__name__} id={self.id}")

    def to_dict(self):
        """Серіалізація в словник."""
        return {
            "id": self.id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

class User(BaseModel):
    """Модель користувача (успадковує від BaseModel)."""

    def __init__(self, username, email):
        super().__init__()
        self.username = username
        self.email = email
        self.__password_hash = None

    def set_password(self, password):
        self.__password_hash = hash(password)

    def check_password(self, password):
        return self.__password_hash == hash(password)

    def to_dict(self):
        """Розширення серіалізації."""
        data = super().to_dict()  # Виклик батьківського методу
        data.update({
            "username": self.username,
            "email": self.email,
        })
        return data

class Post(BaseModel):
    """Модель посту."""

    def __init__(self, title, content, author):
        super().__init__()
        self.title = title
        self.content = content
        self.author = author  # Посилання на User
        self.likes = 0

    def like(self):
        self.likes += 1

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "title": self.title,
            "content": self.content,
            "author": self.author.username,
            "likes": self.likes,
        })
        return data

# Використання
user = User("ivan", "ivan@example.com")
user.save()  # Створено запис User id=...

post = Post("Перший пост", "Привіт, світ!", user)
post.save()
post.like()
post.like()

print(post.to_dict())
```

### Множинне успадкування

```python
class Printable:
    """Міксін для друку."""
    def print(self):
        print(str(self))

class Serializable:
    """Міксін для серіалізації."""
    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False)

class User(Printable, Serializable):
    """Користувач з друком та серіалізацією."""
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"User({self.name}, {self.email})"

user = User("Іван", "ivan@example.com")
user.print()          # User(Іван, ivan@example.com)
print(user.to_json()) # {"name": "Іван", "email": "ivan@example.com"}
```

---

## Поліморфізм

### Що таке поліморфізм?

**Поліморфізм** (polymorphism, від грецького "багато форм") — це принцип ООП, згідно з яким **різні класи** можуть мати **однакові методи** з різною реалізацією, і зовнішній код може викликати ці методи, не знаючи конкретного типу об'єкта.

**Формальне визначення:** Поліморфізм дозволяє використовувати об'єкти різних класів через єдиний інтерфейс, де конкретна поведінка визначається типом об'єкта в часі виконання (runtime).

### Поліморфізм через перевизначення методів

```python
class Shape:
    """Базовий клас — фігура."""

    def area(self):
        raise NotImplementedError("Підкласи повинні реалізувати area()")

    def perimeter(self):
        raise NotImplementedError("Підкласи повинні реалізувати perimeter()")

    def describe(self):
        return f"{self.__class__.__name__}: площа={self.area():.2f}, периметр={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        import math
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c

# Поліморфізм: одна функція працює з будь-якою фігурою
def print_shape_info(shape: Shape):
    """Функція не знає конкретний тип — працює з будь-якою фігурою."""
    print(shape.describe())

shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]

for shape in shapes:
    print_shape_info(shape)
# Circle: площа=78.54, периметр=31.42
# Rectangle: площа=24.00, периметр=20.00
# Triangle: площа=6.00, периметр=12.00

# Поліморфізм: та сама операція, різні результати
total_area = sum(shape.area() for shape in shapes)
print(f"Загальна площа: {total_area:.2f}")
```

### Поліморфізм у веб-розробці (оплати)

```python
class PaymentMethod:
    """Базовий клас — спосіб оплати."""

    def pay(self, amount):
        raise NotImplementedError

    def refund(self, amount):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__

class CreditCard(PaymentMethod):
    def __init__(self, card_number, expiry):
        self.card_number = card_number
        self.expiry = expiry

    def pay(self, amount):
        print(f"  Оплата кредитною карткою {self.card_number[-4:]}: {amount} грн")
        return True

    def refund(self, amount):
        print(f"  Повернення на картку {self.card_number[-4:]}: {amount} грн")
        return True

class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        print(f"  Оплата через PayPal ({self.email}): {amount} грн")
        return True

    def refund(self, amount):
        print(f"  Повернення через PayPal ({self.email}): {amount} грн")
        return True

class CryptoPayment(PaymentMethod):
    def __init__(self, wallet_address):
        self.wallet = wallet_address

    def pay(self, amount):
        print(f"  Оплата криптою на {self.wallet[:10]}...: {amount} грн")
        return True

# Поліморфізм: єдина функція обробки оплати
def process_payment(method: PaymentMethod, amount: float):
    """Обробка оплати будь-яким способом."""
    print(f"Обробка: {method}")
    return method.pay(amount)

# Тестування з різними способами оплати
methods = [
    CreditCard("4111111111111234", "12/25"),
    PayPal("user@example.com"),
    CryptoPayment("0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"),
]

for method in methods:
    process_payment(method, 500)
    print()
```

---

## Качина типізація (duck typing)

### Що таке качина типізація?

**Качина типізація** (duck typing) — це підхід до визначення типу об'єкта, згідно з яким **важливі не тип об'єкта, а його можливості** (які методи та атрибути він має).

**Класичний афоризм:**

> "Якщо щось виглядає як качка, плаває як качка і крякає як качка, то це качка."

**Формальне визначення:** Качина типізація — це механізм поліморфізму, при якому сумісність об'єктів визначається наявністю необхідних атрибутів та методів, а не належністю до певного класу.

### Приклад

```python
class Duck:
    def quack(self):
        return "Кря-кря!"

    def fly(self):
        return "Лечу!"

class Person:
    def quack(self):
        return "Я імітую качку: Кря-кря!"

    def fly(self):
        return "Я розпростер руки та біжу!"

class Airplane:
    def fly(self):
        return "Лечу на висоті 10000м!"

    def quack(self):
        raise NotImplementedError("Літак не вміє крякати!")

# Функція, яка очікує " качину " поведінку
def make_it_quack_and_fly(thing):
    """Працює з будь-яким об'єктом, який має quack() та fly()."""
    print(thing.quack())
    print(thing.fly())

# Качина типізація: Python не перевіряє тип, а перевіряє наявність методів
make_it_quack_and_fly(Duck())      # Працює
make_it_quack_and_fly(Person())    # Працює
# make_it_quack_and_fly(Airplane()) # AttributeError — немає quack()
```

### Качина типізація vs статична типізація

```python
# Статична типізація (Java/C#): перевіряється тип
# void makeItQuack(Duck duck) { ... }  // Тільки качки!

# Качина типізація (Python): перевіряються можливості
def make_it_quack(duck):
    """Python: якщо є quack() — працюємо."""
    return duck.quack()

# Python не перевіряє тип — перевіряє наявність методу
class FakeDuck:
    def quack(self):
        return "Фейкова качка!"

make_it_quack(FakeDuck())  # Працює! FakeDuck не є Duck, але має quack()
```

### Качина типізація у веб-розробці

```python
# У Django є концепція "file-like objects"
# Будь-який об'єкт з read() / write() може використовуватися як файл

class FakeFile:
    """Імітація файлу — має той самий інтерфейс, що й реальний файл."""
    def __init__(self):
        self.content = ""

    def read(self):
        return self.content

    def write(self, data):
        self.content += data
        return len(data)

    def seek(self, position):
        pass  # Порожня реалізація

    def tell(self):
        return len(self.content)

# Функція, яка працює з "файловим" об'єктом
def process_file(file_obj):
    """Працює з будь-яким об'єктом, який має read() та write()."""
    data = file_obj.read()
    processed = data.upper()
    file_obj.write(processed)

# Працює з реальним файлом
with open("test.txt", "w") as f:
    process_file(f)  # real file

# Працює з фейковим файлом (той самий код!)
fake = FakeFile()
fake.write("привіт світ")
process_file(fake)
print(fake.read())  # ПРИВІТ СВІТ
```

### ABC (Abstract Base Classes) — formalізація качиної типізації

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Абстрактний базовий клас — визначає інтерфейс."""

    @abstractmethod
    def charge(self, amount: float) -> bool:
        """Списання коштів."""
        pass

    @abstractmethod
    def refund(self, amount: float) -> bool:
        """Повернення коштів."""
        pass

    def process_order(self, order_total: float):
        """Конкретний метод — використовує абстрактні."""
        if self.charge(order_total):
            print(f"  Замовлення на {order_total} грн оплачено")
            return True
        return False

class StripeProcessor(PaymentProcessor):
    def __init__(self, api_key):
        self.api_key = api_key

    def charge(self, amount):
        print(f"  Stripe: списано {amount} грн")
        return True

    def refund(self, amount):
        print(f"  Stripe: повернення {amount} грн")
        return True

# Неможливо створити екземпляр абстрактного класу
# p = PaymentProcessor()  # TypeError: Can't instantiate abstract class

# Можна створити тільки конкретний клас
stripe = StripeProcessor("sk_test_xxx")
stripe.process_order(500)
```

---

## Типи даних, що визначаються користувачем

### Що це означає?

Python дозволяє створювати **власні типи даних** за допомогою класів. Ці типи поводяться так само, як вбудовані типи (`int`, `str`, `list`), якщо реалізувати відповідні магічні методи.

### Приклад: власний тип "Гроші"

```python
class Money:
    """Власний тип даних — гроші."""

    def __init__(self, amount, currency="UAH"):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Неможливо додати різні валюти")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Неможливо відняти різні валюти")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor):
        return Money(self.amount * factor, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        if self.currency != other.currency:
            raise ValueError("Неможливо порівнювати різні валюти")
        return self.amount < other.amount

# Використання як вбудованого типу
price = Money(100, "UAH")
discount = Money(20, "UAH")

total = price - discount
print(total)          # 80.00 UAH
print(repr(total))    # Money(80, 'UAH')

double = price * 2
print(double)         # 200.00 UAH

# Порівняння
print(price > discount)  # True
print(price == Money(100, "UAH"))  # True
```

### Інтеграція з веб-фреймворками

```python
class Email:
    """Власний тип для email з валідацією."""

    def __init__(self, address):
        if not self._validate(address):
            raise ValueError(f"Невалідний email: {address}")
        self._address = address

    @staticmethod
    def _validate(address):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, address) is not None

    @property
    def address(self):
        return self._address

    @property
    def domain(self):
        return self._address.split('@')[1]

    @property
    def username(self):
        return self._address.split('@')[0]

    def __str__(self):
        return self._address

    def __repr__(self):
        return f"Email('{self._address}')"

    def __eq__(self, other):
        return self._address.lower() == other._address.lower()

    def __hash__(self):
        return hash(self._address.lower())

# Використання
email = Email("user@example.com")
print(email)           # user@example.com
print(email.domain)    # example.com
print(email.username)  # user

# Можна використовувати як ключ словника
contacts = {email: "Іван"}
print(contacts[Email("USER@EXAMPLE.COM")])  # Іван (ріст регістру)
```

---

### Підсумок частини 1

| Концепція | Ключові ідеї |
|-----------|-------------|
| ООП | Об'єднання даних та поведінки в класах |
| Інкапсуляція | Приховування реалізації, контроль доступу |
| Успадкування | Повторне використання коду, ієрархія класів |
| Поліморфізм | Один інтерфейс — різна реалізація |
| Качина типізація | Важливі можливості, а не тип |
| Власні типи | Створення нових типів через магічні методи |
