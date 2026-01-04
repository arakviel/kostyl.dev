---
title: FormData - Робота з формами та файлами
description: Дізнайтеся, як використовувати FormData API для відправлення HTML-форм, завантаження файлів та роботи з multipart/form-data у JavaScript
---

# FormData - Робота з формами та файлами

## Вступ та Контекст

Уявіть типову веб-форму: користувач заповнює імʼя, email, обирає аватар, додає файл резюме і натискає "Відправити". Як відправити всі ці дані — текстові поля, файли, чекбокси — одним запитом на сервер? У старі часи довелося б вручну збирати всі значення, формувати складний формат даних, налаштовувати заголовки...

**FormData API** вирішує цю проблему елегантно: він автоматично збирає всі дані з HTML-форми, підтримує завантаження файлів, правильно встановлює заголовки і чудово працює з Fetch API. Це стандартний спосіб роботи з формами у сучасному JavaScript.

::tip
**Навіщо FormData?**

Без FormData для відправлення файлів довелося б вручну створювати `multipart/form-data` формат, що є складним та схильним до помилок. FormData робить це автоматично, дозволяючи сфокусуватися на бізнес-логіці, а не на технічних деталях протоколу HTTP.
::

### Що ми навчимося робити?

-   Автоматично збирати дані з HTML-форм
-   Програмно створювати та модифікувати FormData об'єкти
-   Завантажувати файли через Fetch API
-   Комбінувати текстові дані з бінарними (Blob, File)
-   Використовувати правильні методи (append vs set)

## Фундаментальні Концепції

### Що таке FormData?

**FormData** — це спеціальний об'єкт, що представляє дані HTML-форми у форматі `key-value` пар. Він автоматично серіалізує дані у формат `multipart/form-data`, який підтримує як текстові поля, так і файли.

```javascript
// Базовий синтаксис
const formData = new FormData([form]);
```

**Параметри:**

-   `form` — опціональний HTML-елемент `<form>`. Якщо передати, FormData автоматично зчитає всі поля з форми

### Ключові особливості

::field-group

:::field{name="Автоматична серіалізація" type="Feature"}
FormData самостійно формує правильний формат `multipart/form-data` з boundary
:::

:::field{name="Підтримка файлів" type="Feature"}
Нативна підтримка завантаження файлів через `<input type="file">`
:::

:::field{name="Правильні заголовки" type="Feature"}
Браузер автоматично встановлює `Content-Type: multipart/form-data` з унікальним boundary
:::

:::field{name="Інтеграція з Fetch" type="Feature"}
FormData можна напряму передати в `body` запиту `fetch()`
:::

::

### Життєвий цикл роботи з формою

::mermaid

```mermaid
sequenceDiagram
    participant U as Користувач
    participant F as HTML Form
    participant FD as FormData
    participant API as fetch()
    participant S as Сервер
    
    U->>F: Заповнює форму
    U->>F: Обирає файли
    U->>F: Натискає Submit
    
    F->>FD: new FormData(form)
    Note over FD: Збір всіх полів та файлів
    
    FD->>API: body: formData
    Note over API: Content-Type встановлюється автоматично
    
    API->>S: POST multipart/form-data
    S->>API: Відповідь
    API->>U: Результат
    
    style FD fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style API fill:#f59e0b,stroke:#b45309,color:#ffffff
```

::

## Методи FormData API

FormData надає набір методів для роботи з даними форми:

::field-group

:::field{name="append(name, value)" type="Method"}
Додає нове поле. Якщо поле вже існує, створює додаткове з тим самим іменем
:::

:::field{name="append(name, blob, fileName)" type="Method"}
Додає файл. Третій параметр — ім'я файлу
:::

:::field{name="set(name, value)" type="Method"}
Встановлює поле. Видаляє всі існуючі поля з таким іменем перед додаванням
:::

:::field{name="delete(name)" type="Method"}
Видаляє всі поля з вказаним іменем
:::

:::field{name="get(name)" type="Method"}
Повертає значення першого поля з вказаним іменем
:::

:::field{name="getAll(name)" type="Method"}
Повертає масив всіх значень полів з вказаним іменем
:::

:::field{name="has(name)" type="Method"}
Перевіряє наявність поля, повертає `boolean`
:::

::

### append() vs set() — критична різниця

Розуміння різниці між `append()` та `set()` важливе для правильної роботи з FormData:

::code-group

```javascript [append() - додає]
const formData = new FormData();

formData.append('tag', 'javascript');
formData.append('tag', 'web');
formData.append('tag', 'tutorial');

// Результат: три поля з ім'ям 'tag'
console.log(formData.getAll('tag')); 
// ['javascript', 'web', 'tutorial']
```

```javascript [set() - замінює]
const formData = new FormData();

formData.set('tag', 'javascript');
formData.set('tag', 'web');       // Замінить попереднє
formData.set('tag', 'tutorial');  // Замінить знову

// Результат: одне поле з ім'ям 'tag'
console.log(formData.getAll('tag')); 
// ['tutorial']
```

::

**Коли використовувати що:**

| Ситуація | Метод | Причина |
| :--- | :--- | :--- |
| Множинний вибір (теги, категорії) | `append()` | Потрібно зберегти всі значення |
| Унікальні поля (email, ім'я) | `set()` | Гарантує одне значення |
| Оновлення існуючого значення | `set()` | Автоматично видаляє старе |
| Додавання до списку | `append()` | Не видаляє існуючі |

## Практична Реалізація

### Автоматичний збір даних з форми

Найпростіший спосіб — передати HTML-форму в конструктор FormData:

```html showLineNumbers
<!DOCTYPE html>
<html>
<head>
  <title>Реєстрація користувача</title>
</head>
<body>
  <form id="registrationForm">
    <input type="text" name="name" placeholder="Ім'я" required>
    <input type="email" name="email" placeholder="Email" required>
    <input type="password" name="password" placeholder="Пароль" required>
    <input type="url" name="avatar" placeholder="URL аватара" value="https://i.imgur.com/yhW6Yw1.jpg">
    <button type="submit">Зареєструватися</button>
  </form>

  <script>
    const form = document.querySelector('#registrationForm');
    
    form.addEventListener('submit', async (event) => {
      event.preventDefault(); // Запобігаємо перезавантаженню сторінки
      
      // FormData автоматично збере ВСІ поля з атрибутом name
      const formData = new FormData(form);
      
      try {
        const response = await fetch('https://api.escuelajs.co/api/v1/users', {
          method: 'POST',
          body: formData // Content-Type встановиться автоматично!
        });
        
        if (!response.ok) {
          throw new Error(`HTTP помилка: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Користувача створено:', result);
        alert('Реєстрація успішна!');
      } catch (error) {
        console.error('Помилка реєстрації:', error);
        alert('Сталася помилка при реєстрації');
      }
    });
  </script>
</body>
</html>
```

**Ключові моменти:**

**Ключові моменти:**

-   **Рядок 20:** `event.preventDefault()` — важливо! Запобігає стандартній поведінці форми (перезавантаження сторінки)
-   **Рядок 23:** `new FormData(form)` автоматично зчитує всі поля з `name` атрибутом  
-   **Рядок 27:** Не встановлюємо `Content-Type` вручну — браузер зробить це автоматично

::warning
**Обов'язковий атрибут name**

FormData зчитує лише поля з атрибутом `name`. Якщо у `<input>` немає `name`, його значення НЕ потрапить у FormData.

```html
<!-- ❌ Це поле буде проігноровано -->
<input type="text" placeholder="Ім'я">

<!-- ✅ Це поле потрапить у FormData -->
<input type="text" name="firstName" placeholder="Ім'я">
```
::

### Програмне створення FormData

Часто потрібно створити FormData програмно, без HTML-форми:

```javascript
// Створення порожнього FormData
const formData = new FormData();

// Додавання текстових полів
formData.append('title', 'Мій новий пост');
formData.append('content', 'Контент поста...');
formData.append('published', 'true');

// Додавання множинних значень
formData.append('tags', 'javascript');
formData.append('tags', 'tutorial');
formData.append('tags', 'web');

// Відправка
const response = await fetch('https://api.escuelajs.co/api/v1/products', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Пост створено:', result);
```

### Завантаження файлів

FormData спрощує завантаження файлів — одна з його ключових переваг:

```html
<form id="uploadForm">
  <input type="file" name="avatar" accept="image/*" required>
  <input type="text" name="description" placeholder="Опис фото">
  <button type="submit">Завантажити</button>
</form>

<script>
async function handleUpload(event) {
  event.preventDefault();
  
  const form = event.target;
  const formData = new FormData(form);
  
  // Можна додати додаткові дані програмно
  formData.append('userId', '12345');
  formData.append('uploadDate', new Date().toISOString());
  
  try {
    const response = await fetch('https://api.escuelajs.co/api/v1/files/upload', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Помилка завантаження');
    
    const result = await response.json();
    console.log('Файл завантажено:', result.location);
  } catch (error) {
    console.error('Помилка:', error);
  }
}

document.querySelector('#uploadForm')
  .addEventListener('submit', handleUpload);
</script>
```

### Робота з множинними файлами

```html
<input type="file" id="multipleFiles" multiple accept="image/*,application/pdf">
<button id="uploadBtn">Завантажити файли</button>

<script>
document.querySelector('#uploadBtn').addEventListener('click', async () => {
  const fileInput = document.querySelector('#multipleFiles');
  const files = fileInput.files; // FileList
  
  if (files.length === 0) {
    alert('Оберіть хоча б один файл');
    return;
  }
  
  const formData = new FormData();
  
  // Додаємо всі файли
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]); // Однакове ім'я для всіх
  }
  
  // Додаємо метадані
  formData.append('totalFiles', files.length);
  formData.append('uploadedBy', 'user123');
  
  try {
    const response = await fetch('https://api.escuelajs.co/api/v1/files/upload', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    console.log('Завантажено файлів:', result.uploadedFiles.length);
  } catch (error) {
    console.error('Помилка завантаження:', error);
  }
});
</script>
```

### Відправлення Blob (згенерованих даних)

Потужна можливість FormData — комбінування звичайних полів з динамічно згенерованими файлами:

```javascript
// Створення зображення на canvas
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 400;
canvas.height = 300;

// Малюємо щось
ctx.fillStyle = '#3b82f6';
ctx.fillRect(0, 0, 400, 300);
ctx.fillStyle = 'white';
ctx.font = 'bold 48px Arial';
ctx.fillText('Hello, World!', 50, 150);

// Конвертуємо canvas в Blob
canvas.toBlob(async (blob) => {
  const formData = new FormData();
  
  // Додаємо Blob як файл (третій параметр — ім'я файлу)
  formData.append('image', blob, 'generated-image.png');
  
  // Додаємо метадані
  formData.append('title', 'Згенероване зображення');
  formData.append('width', canvas.width);
  formData.append('height', canvas.height);
  
  try {
    const response = await fetch('https://api.escuelajs.co/api/v1/files/upload', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    console.log('Зображення збережено:', result.imageUrl);
  } catch (error) {
    console.error('Помилка:', error);
  }
}, 'image/png');
```

::note
**Третій параметр append() для файлів**

Коли додаєте Blob або File через `append()`, третій параметр встановлює ім'я файлу:

```javascript
formData.append('fieldName', blob, 'filename.png');
//                  ↑          ↑          ↑
//               Ім'я поля   Дані    Ім'я файлу
```

Для звичайних рядків третій параметр ігнорується.
::

### Ітерація по FormData

FormData є ітерабельним об'єктом — можна переглянути всі пари `key-value`:

```javascript
const formData = new FormData();
formData.append('name', 'John Doe');
formData.append('email', 'john@example.com');
formData.append('password', 'securepass123');
formData.append('avatar', 'https://i.imgur.com/yhW6Yw1.jpg');

// Метод 1: for...of
console.log('=== Використання for...of ===');
for (const [key, value] of formData) {
  console.log(`${key}: ${value}`);
}
// Виведе:
// name: John Doe
// email: john@example.com
// password: securepass123
// avatar: https://i.imgur.com/yhW6Yw1.jpg



// Метод 2: entries()
console.log('\n=== Використання entries() ===');
for (const entry of formData.entries()) {
  console.log(entry); // ['username', 'john_doe']
}

// Метод 3: keys()
console.log('\n=== Тільки ключі ===');
for (const key of formData.keys()) {
  console.log(key);
}

// Метод 4: values()
console.log('\n=== Тільки значення ===');
for (const value of formData.values()) {
  console.log(value);
}
```

**Практичне застосування — debug:**

```javascript
function logFormData(formData) {
  console.log('FormData містить:');
  for (const [key, value] of formData) {
    // Перевіряємо, чи це файл
    if (value instanceof File) {
      console.log(`${key}: [File] ${value.name} (${value.size} bytes)`);
    } else if (value instanceof Blob) {
      console.log(`${key}: [Blob] ${value.size} bytes`);
    } else {
      console.log(`${key}: ${value}`);
    }
  }
}

// Використання
const formData = new FormData(document.querySelector('#myForm'));
logFormData(formData);
```

## Практичні Сценарії

### Комплексна форма профілю

Реальний приклад: форма профілю з аватаром, текстовими полями та опціями:

```html
<form id="profileForm">
  <h2>Редагування профілю</h2>
  
  <label>
    Аватар:
    <input type="file" name="avatar" accept="image/*">
  </label>
  
  <label>
    Ім'я:
    <input type="text" name="firstName" value="Олександр" required>
  </label>
  
  <label>
    Прізвище:
    <input type="text" name="lastName" value="Коваленко" required>
  </label>
  
  <label>
    Email:
    <input type="email" name="email" value="oleksandr@example.com" required>
  </label>
  
  <label>
    Біографія:
    <textarea name="bio" rows="4">JavaScript розробник...</textarea>
  </label>
  
  <fieldset>
    <legend>Навички (можна обрати декілька):</legend>
    <label><input type="checkbox" name="skills" value="javascript"> JavaScript</label>
    <label><input type="checkbox" name="skills" value="typescript"> TypeScript</label>
    <label><input type="checkbox" name="skills" value="react"> React</label>
    <label><input type="checkbox" name="skills" value="nodejs"> Node.js</label>
  </fieldset>
  
  <button type="submit">Зберегти профіль</button>
</form>

<script>
document.querySelector('#profileForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  
  const formData = new FormData(event.target);
  
  // Додаємо додаткові дані
  formData.append('userId', '123');
  formData.append('updatedAt', new Date().toISOString());
  
  // Логування для дебагу
  console.log('Відправляємо дані:');
  for (const [key, value] of formData) {
    console.log(`${key}:`, value);
  }
  
  try {
    const response = await fetch('https://api.escuelajs.co/api/v1/users/1', {
      method: 'PUT',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const result = await response.json();
    console.log('Профіль оновлено:', result);
    alert('Профіль успішно збережено!');
  } catch (error) {
    console.error('Помилка оновлення профілю:', error);
    alert('Не вдалося зберегти профіль');
  }
});
</script>
```

### Прогрес-бар завантаження

Для відстеження прогресу завантаження використовуємо `XMLHttpRequest` (Fetch поки не підтримує upload progress):

```html
<input type="file" id="fileInput" accept="image/*">
<button id="uploadBtn">Завантажити</button>
<div id="progress" style="display: none;">
  <progress id="progressBar" value="0" max="100"></progress>
  <span id="progressText">0%</span>
</div>

<script>
document.querySelector('#uploadBtn').addEventListener('click', () => {
  const fileInput = document.querySelector('#fileInput');
  const file = fileInput.files[0];
  
  if (!file) {
    alert('Оберіть файл');
    return;
  }
  
  const formData = new FormData();
  formData.append('file', file);
  formData.append('uploadedBy', 'user123');
  
  const xhr = new XMLHttpRequest();
  
  // Відстеження прогресу
  xhr.upload.addEventListener('progress', (event) => {
    if (event.lengthComputable) {
      const percentComplete = Math.round((event.loaded / event.total) * 100);
      
      document.querySelector('#progressBar').value = percentComplete;
      document.querySelector('#progressText').textContent = `${percentComplete}%`;
    }
  });
  
  // Успішне завершення
  xhr.addEventListener('load', () => {
    if (xhr.status >= 200 && xhr.status < 300) {
      const result = JSON.parse(xhr.responseText);
      console.log('Завантажено:', result);
      alert('Файл успішно завантажено!');
    } else {
      alert('Помилка завантаження');
    }
    document.querySelector('#progress').style.display = 'none';
  });
  
  // Відправка
  document.querySelector('#progress').style.display = 'block';
  xhr.open('POST', 'https://api.escuelajs.co/api/v1/files/upload');
  xhr.send(formData);
});
</script>
```

::tip
**Fetch vs XMLHttpRequest для завантаження файлів**

-   **Fetch API**: Сучасний, простий, але поки **не підтримує** відстеження прогресу завантаження (upload progress)
-   **XMLHttpRequest**: Застарілий, але **підтримує** події `xhr.upload.onprogress`

Для простого завантаження без прогрес-бару — використовуйте Fetch. Для прогрес-бару — XMLHttpRequest.
::

## Типові помилки та рішення

### Помилка: Content-Type встановлено вручну

::code-group

```javascript [❌ Неправильно]
const formData = new FormData();
formData.append('name', 'John');

await fetch('/api/upload', {
  method: 'POST',
  headers: {
    // ПОМИЛКА! Не встановлюйте Content-Type вручну
    'Content-Type': 'multipart/form-data'
  },
  body: formData
});
// Запит зламається: відсутній boundary
```

```javascript [✅ Правильно]
const formData = new FormData();
formData.append('name', 'John');

await fetch('/api/upload', {
  method: 'POST',
  // НЕ встановлюємо headers взагалі!
  // Браузер автоматично додасть:
  // Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...
  body: formData
});
```

::

### Помилка: відсутній атрибут name

```html
<!-- ❌ Поле без name — не потрапить у FormData -->
<input type="text" id="name" value="john">

<script>
const form = document.querySelector('form');
const formData = new FormData(form);

console.log(formData.has('name')); // false — поле відсутнє!
</script>
```

```html
<!-- ✅ З атрибутом name -->
<input type="text" name="name" id="name" value="john">

<script>
const form = document.querySelector('form');
const formData = new FormData(form);

console.log(formData.has('name')); // true
console.log(formData.get('name')); // "john"
</script>
```

## Підсумки

FormData API — це потужний інструмент для роботи з HTML-формами та завантаження файлів:

::card-group

:::card{icon="lucide:check-circle"}
#title
Ключові переваги

#description
-   Автоматичний збір даних з HTML-форм
-   Нативна підтримка завантаження файлів
-   Автоматичне встановлення правильних заголовків
-   Проста інтеграція з Fetch API
-   Підтримка множинних значень для одного поля
:::

:::card{icon="lucide:code"}
#title
Основні методи

#description
```javascript
// Створення
const fd = new FormData(form);

// Додавання
fd.append('key', 'value');
fd.set('key', 'value');

// Читання
fd.get('key');
fd.getAll('key');
fd.has('key');

// Видалення
fd.delete('key');
```
:::

:::card{icon="lucide:file-up"}
#title
Завантаження файлів

#description
```javascript
const formData = new FormData();

// З input[type="file"]
formData.append('file', input.files[0]);

// Blob з ім'ям файлу
formData.append('image', blob, 'pic.png');
```
:::

:::card{icon="lucide:shield-alert"}
#title
Критичні правила

#description
-   **НЕ** встановлюйте `Content-Type` вручну
-   **Завжди** додавайте атрибут `name` до полів
-   Використовуйте `append()` для множинних значень
-   Використовуйте `set()` для унікальних полів
:::

::

### Різниця append() vs set()

| Метод | Поведінка | Коли використовувати |
| :--- | :--- | :--- |
| `append()` | Додає нове значення, не видаляє існуючі | Теги, категорії, множинний вибір |
| `set()` | Замінює всі існуючі значення | Унікальні поля (email, ім'я) |

### Шаблон використання

```javascript
// 1. Створення з форми
const formData = new FormData(document.querySelector('#myForm'));

// 2. Додавання файлу
const fileInput = document.querySelector('#avatar');
formData.append('avatar', fileInput.files[0]);

// 3. Додавання метаданих
formData.append('userId', '123');
formData.append('timestamp', Date.now());

// 4. Відправка
const response = await fetch('/api/endpoint', {
  method: 'POST',
  body: formData // Без headers!
});

const result = await response.json();
```

У наступному розділі ми розглянемо, як відстежувати прогрес завантаження та роботу з великими файлами через ReadableStream.

## Додаткові ресурси

-   [MDN: FormData API](https://developer.mozilla.org/en-US/docs/Web/API/FormData) — повна документація
-   [Специфікація FormData](https://xhr.spec.whatwg.org/#interface-formdata) — офіційна специфікація WHATWG
-   [MDN: File API](https://developer.mozilla.org/en-US/docs/Web/API/File) — робота з файлами
-   [MDN: Blob](https://developer.mozilla.org/en-US/docs/Web/API/Blob) — бінарні дані в JavaScript
