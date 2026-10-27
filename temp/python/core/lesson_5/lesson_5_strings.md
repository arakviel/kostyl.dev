# 📝 Повний посібник з рядків у Python

## Зміст

1. [Вступ до рядків](#вступ-до-рядків)
2. [Створення рядків](#створення-рядків)
3. [Лапки: одинарні, подвійні, потрійні](#лапки-одинарні-подвійні-потрійні)
4. [Екранування символів](#екранування-символів)
5. [Спеціальні символи](#спеціальні-символи)
6. [Індексація рядків](#індексація-рядків)
7. [Зрізи рядків (Slicing)](#зрізи-рядків-slicing)
8. [Довжина рядка: len()](#довжина-рядка-len)
9. [Незмінність рядків](#незмінність-рядків)
10. [Конкатенація рядків](#конкатенація-рядків)
11. [Множення рядків](#множення-рядків)
12. [Оператор in: перевірка входження](#оператор-in-перевірка-входження)
13. [Порівняння рядків](#порівняння-рядків)
14. [Цикли по рядках](#цикли-по-рядках)
15. [Методи рядків: огляд](#методи-рядків-огляд)
16. [Зміна регістру](#зміна-регістру)
17. [Видалення пробілів](#видалення-пробілів)
18. [Пошук у рядках](#пошук-у-рядках)
19. [Заміна в рядках](#заміна-в-рядках)
20. [Перевірка вмісту рядка](#перевірка-вмісту-рядка)
21. [Форматування рядків: F-strings](#форматування-рядків-f-strings)
22. [Практичні приклади](#практичні-приклади)
23. [Поширені помилки](#поширені-помилки)

---

## Вступ до рядків

### Що таке рядок?

**Рядок (String)** — це **послідовність символів**, оточена лапками.

**Простими словами:** Все, що ви хочете зберегти як текст — це рядок.

### Приклади рядків:

```python
"Привіт"
'Python'
"123"
"Я вивчаю Python!"
""  # Порожній рядок
```

### Тип даних:

```python
text = "Привіт"
print(type(text))  # <class 'str'>
```

**str** = string (рядок)

---

## Створення рядків

### Спосіб 1: Одинарні лапки

```python
text = 'Привіт'
print(text)  # Привіт
```

### Спосіб 2: Подвійні лапки

```python
text = "Світ"
print(text)  # Світ
```

### Спосіб 3: Потрійні лапки

```python
text = """Багаторядковий
текст"""
print(text)
```

### Порожній рядок:

```python
empty1 = ""
empty2 = ''
print(len(empty1))  # 0
```

### Створення через str():

```python
number = 42
text = str(number)
print(text)        # "42"
print(type(text))  # <class 'str'>
```

---

## Лапки: одинарні, подвійні, потрійні

### Одинарні vs Подвійні

**В Python немає різниці!** Обидва варіанти еквівалентні:

```python
text1 = 'Привіт'
text2 = "Привіт"

print(text1 == text2)  # True
```

### Коли використовувати які?

#### Одинарні, якщо в тексті є подвійні:

```python
message = 'Він сказав: "Привіт!"'
print(message)  # Він сказав: "Привіт!"
```

#### Подвійні, якщо в тексті є одинарні:

```python
message = "It's a beautiful day"
print(message)  # It's a beautiful day
```

---

## Екранування символів

### Що таке екранування?

**Екранування** — це спосіб вставити спеціальні символи за допомогою `\`.

### Приклади:

#### Лапки в рядку:

```python
text = 'It\'s a nice day'
print(text)  # It's a nice day

text = "Він сказав: \"Привіт!\""
print(text)  # Він сказав: "Привіт!"
```

#### Зворотна коса риска:

```python
path = "C:\\Users\\Name\\Documents"
print(path)  # C:\Users\Name\Documents
```

---

## Спеціальні символи

### Новий рядок: \n

```python
text = "Рядок 1\nРядок 2"
print(text)
# Рядок 1
# Рядок 2
```

### Табуляція: \t

```python
text = "Ім'я:\tІван"
print(text)  # Ім'я:    Іван
```

### Таблиця спеціальних символів:

| Послідовність | Значення            |
| ------------- | ------------------- |
| `\'`          | Одинарна лапка      |
| `\"`          | Подвійна лапка      |
| `\\`          | Зворотна коса риска |
| `\n`          | Новий рядок         |
| `\t`          | Табуляція           |

---

## Індексація рядків

### Доступ до символів:

```python
text = "Python"

# Позиції: P  y  t  h  o  n
# Індекси: 0  1  2  3  4  5

print(text[0])  # P
print(text[1])  # y
print(text[5])  # n
```

### Від'ємні індекси:

```python
text = "Python"

print(text[-1])  # n (останній)
print(text[-2])  # o (передостанній)
```

---

## Зрізи рядків (Slicing)

### Синтаксис:

```python
text[початок:кінець:крок]
```

### Приклади:

```python
text = "Python"

print(text[0:3])  # Pyt
print(text[:3])   # Pyt (те саме)
print(text[3:])   # hon
print(text[:])    # Python (весь рядок)
```

### Реверс:

```python
text = "Python"
print(text[::-1])  # nohtyP
```

---

## Довжина рядка: len()

```python
text = "Python"
print(len(text))  # 6

text = "Hello World"
print(len(text))  # 11 (пробіл теж символ!)
```

---

## Незмінність рядків

### Рядки незмінні:

```python
text = "Python"

# ❌ Не працює
# text[0] = "J"  # TypeError!

# ✅ Працює (новий рядок)
text = "J" + text[1:]
print(text)  # Jython
```

---

## Конкатенація рядків

### Оператор +:

```python
first = "Hello"
second = "World"

result = first + " " + second
print(result)  # Hello World
```

### З числами:

```python
age = 25
text = "Мені " + str(age) + " років"
print(text)  # Мені 25 років
```

---

## Множення рядків

### Оператор \*:

```python
print("*" * 10)  # **********
print("Ha" * 3)  # HaHaHa
```

---

## Оператор in

```python
text = "Python is awesome"

print("Python" in text)    # True
print("Java" in text)      # False
```

---

## Порівняння рядків

```python
text1 = "Python"
text2 = "python"

print(text1 == text2)  # False (різний регістр!)
print(text1.lower() == text2.lower())  # True
```

---

## Цикли по рядках

```python
text = "Python"

for char in text:
    print(char)
# P
# y
# t
# h
# o
# n
```

---

## Методи рядків: огляд

### Категорії:

1. Зміна регістру
2. Видалення пробілів
3. Пошук
4. Заміна
5. Перевірка вмісту

---

## Зміна регістру

```python
text = "python"

print(text.upper())       # PYTHON
print(text.lower())       # python
print(text.capitalize())  # Python
print(text.title())       # Python
```

---

## Видалення пробілів

```python
text = "  Python  "

print(text.strip())   # "Python"
print(text.lstrip())  # "Python  "
print(text.rstrip())  # "  Python"
```

---

## Пошук у рядках

```python
text = "Python is awesome"

print(text.find("is"))     # 7
print(text.find("Java"))   # -1 (не знайдено)
print(text.count("o"))     # 2
```

---

## Заміна в рядках

```python
text = "Python is awesome"
new_text = text.replace("awesome", "great")
print(new_text)  # Python is great
```

---

## Перевірка вмісту рядка

```python
print("12345".isdigit())    # True
print("Python".isalpha())   # True
print("Python3".isalnum())  # True
print("   ".isspace())       # True
print("python".islower())   # True
print("PYTHON".isupper())   # True
```

---

## Форматування рядків: F-strings

### Синтаксис:

```python
f"текст {змінна} текст"
```

### Приклади:

```python
name = "Іван"
age = 25

message = f"Мене звати {name}, мені {age} років"
print(message)
```

### З виразами:

```python
a = 10
b = 20
print(f"{a} + {b} = {a + b}")  # 10 + 20 = 30
```

### Форматування чисел:

```python
pi = 3.14159
print(f"Pi = {pi:.2f}")  # Pi = 3.14
```

---

## Практичні приклади

### Приклад 1: Валідація email

```python
email = input("Email: ")

if "@" in email and "." in email:
    print("Email правильний")
else:
    print("Email неправильний")
```

### Приклад 2: Паліндром

```python
text = input("Введіть слово: ")

clean_text = text.replace(" ", "").lower()

if clean_text == clean_text[::-1]:
    print("Це паліндром!")
else:
    print("Це не паліндром")
```

---

## Поширені помилки

### Помилка 1: Спроба змінити символ

```python
# ❌ Неправильно
text = "Python"
# text[0] = "J"  # TypeError!

# ✅ Правильно
text = "J" + text[1:]
```

### Помилка 2: Забута конвертація

```python
# ❌ Неправильно
age = 25
# print("Вік: " + age)  # TypeError!

# ✅ Правильно
print(f"Вік: {age}")
```

---

## Підсумок

### Основні концепції:

1. **Рядок** — послідовність символів
2. **Індексація** — доступ до символів (з 0)
3. **Зрізи** — `[start:end:step]`
4. **Незмінність** — не можна змінювати
5. **Методи** — багато вбудованих функцій
6. **F-strings** — найкраще форматування

### Найважливіші методи:

```python
text.upper()          # ВЕЛИКІ ЛІТЕРИ
text.lower()          # малі літери
text.strip()          # видалити пробіли
text.find(sub)        # знайти підрядок
text.replace(old, new)  # замінити
text.isdigit()        # тільки цифри?
len(text)             # довжина
sub in text           # перевірка входження
```

### F-strings:

```python
name = "Іван"
age = 25
print(f"Мене звати {name}, мені {age} років")
```
