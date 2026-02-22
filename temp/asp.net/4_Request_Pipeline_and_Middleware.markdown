# Конвеєр обробки запитів і middleware в ASP.NET Core

Обробка вхідних запитів — одна з ключових функцій вебдодатка ASP.NET Core. У цій статті ми розглянемо, як працює конвеєр обробки запитів і як middleware (компоненти проміжної обробки) дозволяють налаштувати логіку обробки. Ми також детально розберемо об’єкти `HttpContext`, `HttpRequest` і `HttpResponse`, а також методи для роботи з ними.

## Конвеєр обробки запитів

У ASP.NET Core обробка запитів здійснюється через **конвеєр обробки** (request pipeline), який складається з послідовності компонентів middleware. Кожен компонент обробляє запит і може або завершити обробку (термінальний middleware), або передати запит наступному компоненту в конвеєрі. Після обробки останнім компонентом відповідь повертається назад через конвеєр до клієнта.

**Схема роботи конвеєра**:
Схема конвеєра обробки запитів middleware в ASP.NET Core
![Схема конвеєра обробки запитів middleware в ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/index/_static/request-delegate-pipeline.png?view=aspnetcore-8.0)
Схема конвеєра обробки запитів middleware в ASP.NET Core
![Схема конвеєра обробки запитів middleware в ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/index/_static/middleware-pipeline.svg?view=aspnetcore-8.0)

```Csharp
namespace FirstCoreWebApplication
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            var app = builder.Build();

            //Configuring Middleware Component using Use and Run Extension Method

            //First Middleware Component Registered using Use Extension Method
            app.Use(async (context, next) =>
            {
                await context.Response.WriteAsync("Middleware1: Incoming Request\n");
                //Calling the Next Middleware Component
                await next();
                await context.Response.WriteAsync("Middleware1: Outgoing Response\n");
            });

            //Second Middleware Component Registered using Use Extension Method
            app.Use(async (context, next) =>
            {
                await context.Response.WriteAsync("Middleware2: Incoming Request\n");
                //Calling the Next Middleware Component
                await next();
                await context.Response.WriteAsync("Middleware2: Outgoing Response\n");
            });

            //Third Middleware Component Registered using Run Extension Method
            app.Run(async (context) =>
            {
                await context.Response.WriteAsync("Middleware3: Incoming Request handled and response generated\n");
                //Terminal Middleware Component i.e. cannot call the Next Component
            });

            //This will Start the Application
            app.Run();
        }
    }
}
```

[thomaslevesque](https://thomaslevesque.com/2018/03/27/understanding-the-asp-net-core-middleware-pipeline/)

### Принцип роботи
1. Сервер (наприклад, Kestrel) отримує вхідний HTTP-запит.
2. Запит передається першому компоненту middleware у конвеєрі.
3. Кожен компонент може:
   - Обробити запит і сформувати відповідь (термінальний middleware).
   - Виконати часткову обробку та передати запит наступному компоненту.
4. Після обробки останнім компонентом відповідь повертається клієнту через той самий конвеєр.

Компоненти middleware додаються за допомогою методів розширення `Run`, `Map` і `Use` інтерфейсу `IApplicationBuilder`, який реалізовано класом `WebApplication`.

## Компоненти Middleware

Middleware — це програмні компоненти, які вбудовуються в конвеєр обробки запитів. Вони можуть бути:
- **Вбудованими**: Визначеними як методи в `Program.cs` (inline middleware).
- **Окремими класами**: Використовуються для складніших сценаріїв.

Middleware працює з об’єктом `HttpContext`, який передається через делегат `RequestDelegate`:

```
public delegate Task RequestDelegate(HttpContext context);
```

### Об’єкт HttpContext
`HttpContext` інкапсулює всю інформацію про HTTP-запит і відповідь. Його основні властивості:

- **`Connection`**: Інформація про підключення (наприклад, IP-адреса клієнта).
- **`Features`**: Колекція HTTP-функціональностей, доступних для запиту.
- **`Items`**: Словник для зберігання даних у межах одного запиту.
- **`Request`**: Об’єкт `HttpRequest` із даними про запит.
- **`RequestAborted`**: Сигналізує про переривання запиту.
- **`RequestServices`**: Доступ до контейнера сервісів для Dependency Injection.
- **`Response`**: Об’єкт `HttpResponse` для формування відповіді.
- **`Session`**: Дані сесії для поточного запиту.
- **`TraceIdentifier`**: Унікальний ідентифікатор запиту для логування.
- **`User`**: Інформація про автентифікованого користувача.
- **`WebSockets`**: Управління підключеннями WebSocket.

Ці властивості дозволяють middleware отримувати дані про запит і формувати відповідь.

## Вбудовані компоненти Middleware

ASP.NET Core надає набір готових middleware для типових завдань. Ось деякі з них:
- **`Authentication`**: Підтримка автентифікації користувачів.
- **`Authorization`**: Контроль доступу на основі авторизації.
- **`CORS`**: Дозволяє крос-доменні запити.
- **`DeveloperExceptionPage`**: Відображає детальну інформацію про помилки в режимі розробки.
- **`StaticFiles`**: Обробка статичних файлів (CSS, JS, зображень).
- **`ResponseCaching`**: Кешування відповідей для підвищення продуктивності.
- **`HttpsRedirection`**: Перенаправлення HTTP-запитів на HTTPS.
- **`EndpointRouting`**: Маршрутизація запитів до ендпоінтів.
- **`Session`**: Підтримка сесій користувача.
- **`WebSockets`**: Робота з протоколом WebSocket.

Ці middleware додаються за допомогою методів розширення `UseXXX`. Наприклад, для додавання `WelcomePageMiddleware` (відображає стандартну привітальну сторінку):

```Csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseWelcomePage();

app.Run();
```

**Результат роботи WelcomePageMiddleware**:
*Зображення: Привітальна сторінка, створена WelcomePageMiddleware*

## Метод Run і термінальний Middleware

Метод `Run` додає **термінальний middleware**, який завершує обробку запиту і не передає його далі по конвеєру. Він визначений як метод розширення для `IApplicationBuilder`:

```Csharp
IApplicationBuilder.Run(RequestDelegate handler)
```

### Приклад використання Run
Просте middleware, яке повертає текстовий відповідь:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) => await context.Response.WriteAsync("Hello from ITStep!"));

app.Run();
```

У цьому прикладі middleware повертає рядок "Hello from ITStep!" для всіх запитів. Метод `context.Response.WriteAsync` відправляє відповідь клієнту.

**Важливо**:
1. Метод `Run` для middleware відрізняється від методу `Run` класу `WebApplication`, який запускає додаток.
2. Метод `Run` для middleware потрібно викликати в кінці конвеєра, оскільки він завершує обробку.

### Винос middleware в окремий метод
Для кращої читабельності код middleware можна винести в окремий метод:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(HandleRequest);

app.Run();

async Task HandleRequest(HttpContext context)
{
    await context.Response.WriteAsync("Hello from ITStep 2!");
}
```

## Життєвий цикл Middleware

Middleware створюються один раз під час запуску додатка і використовуються для всіх запитів протягом його роботи. Це означає, що стан, визначений у middleware, може зберігатися між запитами. Наприклад:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

int x = 2;
app.Run(async (context) =>
{
    x = x * 2; // x стає 4, 8, 16... при кожному запиті
    await context.Response.WriteAsync($"Result: {x}");
});

app.Run();
```

**Результат роботи middleware**:
*Зображення: Зміна значення змінної x при кожному запиті*

**Примітка**: У браузері Google Chrome можуть надсилатися додаткові запити (наприклад, до `favicon.ico`), що може впливати на результат.

## Об’єкт HttpResponse: Формування відповіді

Об’єкт `HttpResponse` (доступний через `context.Response`) дозволяє налаштувати відповідь клієнту. Його основні властивості:
- **`Body`**: Потік для запису тіла відповіді.
- **`ContentLength`**: Довжина вмісту відповіді.
- **`ContentType`**: Тип вмісту (наприклад, `text/plain`).
- **`Headers`**: Заголовки відповіді.
- **`StatusCode`**: Код стану HTTP (наприклад, 200, 404).
- **`Cookies`**: Куки, що відправляються клієнту.

### Методи для відправки відповіді
- **`WriteAsync()`**: Відправляє текстовий вміст.
- **`WriteAsJsonAsync()`**: Відправляє дані у форматі JSON.
- **`Redirect()`**: Перенаправляє на інший URL.
- **`SendFileAsync()`**: Відправляє файл.

Приклад відправки тексту з кодуванням:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    await context.Response.WriteAsync("Hello from ITStep!", System.Text.Encoding.UTF8);
});

app.Run();
```

### Установка заголовків
Заголовки встановлюються через властивість `Headers` (тип `IHeaderDictionary`):

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    var response = context.Response;
    response.Headers.ContentLanguage = "uk-UA";
    response.Headers.ContentType = "text/plain; charset=utf-8";
    response.Headers.Append("secret-id", "256");
    await response.WriteAsync("Привіт від ITStep!");
});

app.Run();
```

**Результат із заголовками**:
*Зображення: Відповідь із кастомними заголовками*

### Установка кодів стану
Код стану встановлюється через `StatusCode`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    context.Response.StatusCode = 404;
    await context.Response.WriteAsync("Resource Not Found");
});

app.Run();
```

### Відправка HTML
Для відправки HTML потрібно встановити `ContentType` на `text/html`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    context.Response.ContentType = "text/html; charset=utf-8";
    await context.Response.WriteAsync("<h2>Hello from ITStep!</h2><h3>Welcome to ASP.NET Core</h3>");
});

app.Run();
```

**Результат із HTML**:
*Зображення: Веб-сторінка з HTML-вмістом*

## Об’єкт HttpRequest: Отримання даних запиту

Об’єкт `HttpRequest` (доступний через `context.Request`) містить інформацію про вхідний запит. Його основні властивості:
- **`Body`**: Потік із даними тіла запиту.
- **`ContentType`**: Тип вмісту запиту.
- **`Headers`**: Заголовки запиту.
- **`Method`**: HTTP-метод (GET, POST тощо).
- **`Path`**: Шлях запиту (наприклад, `/users`).
- **`Query`**: Параметри рядка запиту.
- **`Cookies`**: Куки, надіслані клієнтом.

### Отримання заголовків
Заголовки доступні через `Headers` (тип `IHeaderDictionary`):

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    context.Response.ContentType = "text/html; charset=utf-8";
    var stringBuilder = new System.Text.StringBuilder("<table>");
    foreach (var header in context.Request.Headers)
    {
        stringBuilder.Append($"<tr><td>{header.Key}</td><td>{header.Value}</td></tr>");
    }
    stringBuilder.Append("</table>");
    await context.Response.WriteAsync(stringBuilder.ToString());
});

app.Run();
```

**Результат із заголовками запиту**:
*Зображення: Таблиця із заголовками запиту*

### Отримання шляху запиту
Властивість `Path` повертає шлях запиту:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    var path = context.Request.Path;
    await context.Response.WriteAsync($"Path: {path}");
});

app.Run();
```

### Умовна обробка за шляхом
Можна реалізувати умовну логіку залежно від шляху:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    var path = context.Request.Path;
    var now = DateTime.Now;
    var response = context.Response;

    if (path == "/date")
        await response.WriteAsync($"Date: {now.ToShortDateString()}");
    else if (path == "/time")
        await response.WriteAsync($"Time: {now.ToShortTimeString()}");
    else
        await response.WriteAsync("Hello from ITStep!");
});

app.Run();
```

**Результат умовної обробки**:
*Зображення: Відповідь залежно від шляху запиту (/date, /time тощо)*

### Рядок запиту
Рядок запиту (query string) — це частина URL після символу `?`, наприклад:

```
https://localhost:7256/users?name=Tom&age=37
```

- **Path**: `/users`
- **Query String**: `?name=Tom&age=37`

Параметри рядка запиту доступні через властивість `Query`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    context.Response.ContentType = "text/html; charset=utf-8";
    var stringBuilder = new System.Text.StringBuilder("<h3>Параметри рядка запиту</h3><table>");
    stringBuilder.Append("<tr><td>Параметр</td><td>Значення</td></tr>");
    foreach (var param in context.Request.Query)
    {
        stringBuilder.Append($"<tr><td>{param.Key}</td><td>{param.Value}</td></tr>");
    }
    stringBuilder.Append("</table>");
    await context.Response.WriteAsync(stringBuilder.ToString());
});

app.Run();
```

**Результат із параметрами рядка запиту**:
*Зображення: Таблиця з параметрами рядка запиту*

### Отримання окремих параметрів
Параметри можна отримати за ключем:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(async (context) =>
{
    string name = context.Request.Query["name"];
    string age = context.Request.Query["age"];
    await context.Response.WriteAsync($"{name} - {age}");
});

app.Run();
```

**Результат із параметрами**:
*Зображення: Виведення параметрів name і age*

## Висновок

Конвеєр обробки запитів і middleware є основою обробки HTTP-запитів у ASP.NET Core. Middleware дозволяють гнучко налаштувати обробку запитів, використовуючи вбудовані компоненти або власні реалізації. Об’єкти `HttpContext`, `HttpRequest` і `HttpResponse` надають повний доступ до даних запиту та відповіді, дозволяючи створювати динамічні та інтерактивні вебдодатки. У наступних темах можна розглянути створення власних middleware або використання вбудованої маршрутизації.
