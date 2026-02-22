# Стан додатка, куки та сесії в ASP.NET Core

Управління станом додатка в ASP.NET Core є важливим для збереження даних, пов’язаних із запитами, користувачами чи глобальними налаштуваннями. ASP.NET Core надає кілька механізмів для цього: `HttpContext.Items` для зберігання даних протягом одного запиту, куки для збереження даних на стороні клієнта та сесії для тимчасового зберігання даних на сервері. У цьому матеріалі ми розглянемо ці механізми, їхнє застосування, методи управління, а також безпеку та практичні сценарії.

## `HttpContext.Items`

Колекція `HttpContext.Items` — це словник типу `IDictionary<object, object>`, який зберігає дані, пов’язані з поточним запитом. Після завершення запиту ці дані автоматично видаляються.

### Використання `HttpContext.Items`

Колекція ідеально підходить для передачі даних між компонентами middleware в рамках одного запиту.

#### Приклад із middleware
Код із передачею даних через `HttpContext.Items`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Use(async (context, next) =>
{
    context.Items["message"] = "Привіт від ITStep!";
    await next.Invoke();
});

app.MapGet("/", async (context) =>
{
    await context.Response.WriteAsync($"Повідомлення: {context.Items["message"]}");
});

app.Run();
```

**Результат використання `HttpContext.Items`**:
*Зображення: Веб-браузер відображає "Повідомлення: Привіт від ITStep!" для запиту `/`*

**Пояснення**:
- У першому middleware додається ключ `"message"` із значенням.
- У другому middleware це значення використовується для формування відповіді.

### Методи `HttpContext.Items`

Колекція підтримує наступні методи:

- `Add(object key, object value)`: Додає об’єкт із ключем.
- `Clear()`: Видаляє всі об’єкти.
- `ContainsKey(object key)`: Перевіряє наявність ключа.
- `Remove(object key)`: Видаляє об’єкт за ключем.
- `TryGetValue(object key, out object value)`: Отримує значення за ключем.

#### Приклад із методами
Код із перевіркою та видаленням елементів:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Use(async (context, next) =>
{
    context.Items.Add("message", "Привіт від ITStep!");
    await next.Invoke();
});

app.MapGet("/", async (context) =>
{
    if (context.Items.ContainsKey("message"))
    {
        await context.Response.WriteAsync($"Повідомлення: {context.Items["message"]}");
        context.Items.Remove("message");
    }
    else
    {
        await context.Response.WriteAsync("Повідомлення відсутнє");
    }
});

app.Run();
```

**Результат методів `HttpContext.Items`**:
*Зображення: Веб-браузер відображає "Повідомлення: Привіт від ITStep!" для першого запиту, "Повідомлення відсутнє" для наступних*

## Куки

Куки — це невеликі фрагменти даних, які зберігаються на стороні клієнта та передаються з кожним запитом до сервера. Максимальний розмір кук — 4096 байтів.

### Отримання та встановлення кук

- **Отримання**: Через `context.Request.Cookies` (тип `IRequestCookieCollection`).
- **Встановлення**: Через `context.Response.Cookies` (тип `IResponseCookies`).

#### Приклад із куками
Код, що встановлює та отримує куку:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", async (context) =>
{
    if (context.Request.Cookies.ContainsKey("name"))
    {
        string name = context.Request.Cookies["name"];
        await context.Response.WriteAsync($"Привіт, {name}!");
    }
    else
    {
        context.Response.Cookies.Append("name", "Том");
        await context.Response.WriteAsync("Привіт, ITStep!");
    }
});

app.Run();
```

**Результат роботи з куками**:
*Зображення: Веб-браузер відображає "Привіт, ITStep!" для першого запиту, "Привіт, Том!" для наступних. У вкладці Application браузера видно куку `name`*

**Пояснення**:
- При першому запиті кука `name` відсутня, тому встановлюється значення `"Том"`.
- При наступних запитах кука читається, і виводиться персоналізоване повідомлення.

### Методи роботи з куками

- **Для `Request.Cookies`**:
  - `ContainsKey(string key)`: Перевіряє наявність куки.
  - `TryGetValue(string key, out string value)`: Отримує значення куки.
- **Для `Response.Cookies`**:
  - `Append(string key, string value)`: Додає куку.
  - `Delete(string key)`: Видаляє куку.

#### Приклад із `TryGetValue`
Код із використанням `TryGetValue`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", async (context) =>
{
    if (context.Request.Cookies.TryGetValue("name", out var name))
    {
        await context.Response.WriteAsync($"Привіт, {name}!");
    }
    else
    {
        context.Response.Cookies.Append("name", "Том");
        await context.Response.WriteAsync("Привіт, ITStep!");
    }
});

app.Run();
```

**Результат із `TryGetValue`**:
*Зображення: Веб-браузер відображає аналогічний результат, як у попередньому прикладі*

### Налаштування кук

Куки можна налаштувати через перевантаження методу `Append` з параметром `CookieOptions`.

#### Приклад із `CookieOptions`
Код із налаштуванням кук:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", async (context) =>
{
    if (context.Request.Cookies.TryGetValue("name", out var name))
    {
        await context.Response.WriteAsync($"Привіт, {name}!");
    }
    else
    {
        var options = new CookieOptions
        {
            HttpOnly = true,
            Expires = DateTimeOffset.Now.AddDays(7),
            Secure = true
        };
        context.Response.Cookies.Append("name", "Том", options);
        await context.Response.WriteAsync("Привіт, ITStep!");
    }
});

app.Run();
```

**Результат із `CookieOptions`**:
*Зображення: Веб-браузер відображає "Привіт, ITStep!" для першого запиту, кука `name` має термін дії 7 днів і позначена як `HttpOnly`*

**Пояснення**:
- `HttpOnly = true`: Куки недоступні для JavaScript.
- `Expires`: Встановлює термін дії куки.
- `Secure = true`: Куки передаються лише через HTTPS.

### Безпека кук

Куки вразливі до атак, таких як XSS (Cross-Site Scripting) або CSRF (Cross-Site Request Forgery). Для захисту:
- Використовуйте `HttpOnly` для запобігання доступу через JavaScript.
- Використовуйте `Secure` для передачі лише через HTTPS.
- Обмежуйте термін дії куки (`Expires` або `MaxAge`).
- Використовуйте `SameSite` для захисту від CSRF.

## Сесії

Сесії дозволяють зберігати дані на сервері, асоціюючи їх із клієнтом через ідентифікатор, який зберігається в куках. Дані сесії доступні для всіх запитів із одного браузера протягом певного часу.

### Налаштування сесій

Для використання сесій потрібно додати сервіси та middleware:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession();

var app = builder.Build();
app.UseSession();

app.MapGet("/", async (context) =>
{
    if (context.Session.Keys.Contains("name"))
    {
        await context.Response.WriteAsync($"Привіт, {context.Session.GetString("name")}!");
    }
    else
    {
        context.Session.SetString("name", "Том");
        await context.Response.WriteAsync("Привіт, ITStep!");
    }
});

app.Run();
```

**Результат базового використання сесій**:
*Зображення: Веб-браузер відображає "Привіт, ITStep!" для першого запиту, "Привіт, Том!" для наступних. У вкладці Application видно куку `.AspNetCore.Session`*

**Пояснення**:
- `AddDistributedMemoryCache`: Додає кеш для зберігання даних сесії.
- `AddSession`: Реєструє сервіси сесій.
- `UseSession`: Додає middleware для обробки сесій.

### Методи `ISession`

Інтерфейс `ISession` надає методи для роботи з сесіями:

- `Keys`: Список ключів сесії.
- `Clear()`: Очищає сесію.
- `Get(string key)`: Отримує масив байтів.
- `GetInt32(string key)`: Отримує ціле число.
- `GetString(string key)`: Отримує рядок.
- `Set(string key, byte[] value)`: Встановлює масив байтів.
- `SetInt32(string key, int value)`: Встановлює ціле число.
- `SetString(string key, string value)`: Встановлює рядок.
- `Remove(string key)`: Видаляє значення за ключем.

### Налаштування сесій

Сесії можна налаштувати через `SessionOptions`:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.Cookie.Name = ".MyApp.Session";
    options.IdleTimeout = TimeSpan.FromMinutes(60);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

var app = builder.Build();
app.UseSession();

app.MapGet("/", async (context) =>
{
    if (context.Session.Keys.Contains("name"))
    {
        await context.Response.WriteAsync($"Привіт, {context.Session.GetString("name")}!");
    }
    else
    {
        context.Session.SetString("name", "Том");
        await context.Response.WriteAsync("Привіт, ITStep!");
    }
});

app.Run();
```

**Результат із `SessionOptions`**:
*Зображення: Веб-браузер відображає аналогічний результат, кука має назву `.MyApp.Session` і термін дії 60 хвилин*

**Пояснення**:
- `Cookie.Name`: Змінює назву куки сесії.
- `IdleTimeout`: Встановлює час неактивності (60 хвилин).
- `Cookie.HttpOnly`: Захищає куку від JavaScript.
- `Cookie.IsEssential`: Позначка критичності для GDPR.

### Зберігання складних об’єктів

Для зберігання складних об’єктів у сесії потрібна їх серіалізація та десеріалізація.

#### Клас для серіалізації
Клас із методами розширення для `ISession`:

```csharp
using System.Text.Json;

public static class SessionExtensions
{
    public static void Set<T>(this ISession session, string key, T value)
    {
        session.SetString(key, JsonSerializer.Serialize(value));
    }

    public static T? Get<T>(this ISession session, string key)
    {
        var value = session.GetString(key);
        return value == null ? default : JsonSerializer.Deserialize<T>(value);
    }
}
```

#### Приклад із складним об’єктом
Клас `Person` і код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession();

var app = builder.Build();
app.UseSession();

app.MapGet("/", async (context) =>
{
    if (context.Session.Keys.Contains("person"))
    {
        Person? person = context.Session.Get<Person>("person");
        await context.Response.WriteAsync($"Привіт, {person?.Name}, ваш вік: {person?.Age}!");
    }
    else
    {
        Person person = new Person { Name = "Том", Age = 22 };
        context.Session.Set("person", person);
        await context.Response.WriteAsync("Привіт, ITStep!");
    }
});

app.Run();

public class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
}
```

**Результат із складним об’єктом**:
*Зображення: Веб-браузер відображає "Привіт, ITStep!" для першого запиту, "Привіт, Том, ваш вік: 22!" для наступних*

## Практичний сценарій: Лічильник відвідувань

Приклад middleware для підрахунку відвідувань сторінки з використанням сесій:

```csharp
public class VisitCounterMiddleware
{
    private readonly RequestDelegate _next;

    public VisitCounterMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        int visitCount = context.Session.GetInt32("visitCount") ?? 0;
        visitCount++;
        context.Session.SetInt32("visitCount", visitCount);
        context.Response.Headers.Append("X-Visit-Count", visitCount.ToString());
        await _next(context);
    }
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

var app = builder.Build();
app.UseSession();
app.UseMiddleware<VisitCounterMiddleware>();

app.MapGet("/", async (context) =>
{
    int visitCount = context.Session.GetInt32("visitCount") ?? 0;
    await context.Response.WriteAsync($"Ви відвідали цю сторінку {visitCount} разів!");
});

app.Run();
```

**Результат лічильника відвідувань**:
*Зображення: Веб-браузер відображає "Ви відвідали цю сторінку 1 разів!" для першого запиту, число зростає з кожним оновленням*

## Обмеження та безпека

- **HttpContext.Items**:
  - Дані зберігаються лише протягом одного запиту.
  - Підходить для тимчасових даних у межах конвеєра обробки.
- **Куки**:
  - Обмеження розміру (4096 байтів).
  - Вразливі до маніпуляцій на стороні клієнта.
  - Використовуйте `HttpOnly`, `Secure` і `SameSite` для захисту.
- **Сесії**:
  - Залежить від кешу (`IDistributedCache`), який може бути в пам’яті або розподіленим (наприклад, Redis).
  - Обмеження за часом дії (`IdleTimeout`).
  - Куки сесії повинні бути захищені (`HttpOnly`, `Secure`).

## Висновок

ASP.NET Core надає гнучкі інструменти для управління станом додатка: `HttpContext.Items` для короткотривалих даних запиту, куки для зберігання даних на клієнті та сесії для тимчасового зберігання даних на сервері. Кожен механізм має свої сценарії використання, переваги та обмеження. Для безпеки важливо правильно налаштовувати куки та сесії, використовуючи атрибути `HttpOnly`, `Secure` і `SameSite`. У наступних темах можна розглянути використання розподілених кешів (наприклад, Redis) для масштабування сесій або інтеграцію з автентифікацією для збереження стану користувача.

</xaiArtifact>