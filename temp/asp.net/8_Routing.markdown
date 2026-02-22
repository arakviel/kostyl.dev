# Маршрутизація в ASP.NET Core

Маршрутизація в ASP.NET Core відповідає за зіставлення вхідних HTTP-запитів із маршрутами та вибір відповідної кінцевої точки (endpoint) для їх обробки. Кінцева точка об'єднує шаблон маршруту, якому має відповідати запит, і обробник, який виконує логіку обробки. У цьому матеріалі ми розглянемо основи маршрутизації, методи створення кінцевих точок, роботу з параметрами маршрутів, обмеженнями, передачею залежностей, а також поєднання маршрутів із middleware.

## Основи маршрутизації

Маршрутизація в ASP.NET Core базується на інтерфейсі `Microsoft.AspNetCore.Routing.IEndpointRouteBuilder`, який реалізований у класі `WebApplication`. Це дозволяє використовувати методи для створення кінцевих точок безпосередньо через об'єкт `WebApplication`. Для маршрутизації в конвейєр обробки запитів додаються два middleware:

- **EndpointRoutingMiddleware** (`UseRouting`): Вибирає кінцеву точку, яка відповідає запиту.
- **EndpointMiddleware** (`UseEndpoints`): Виконує обробку запиту обраною кінцевою точкою.

Ці middleware додаються автоматично при використанні кінцевих точок у `WebApplicationBuilder`.

### Метод `Map`
Метод `Map` є найпростішим способом створення кінцевих точок для обробки GET-запитів. Він визначений як метод розширення для `IEndpointRouteBuilder` і має три версії:


public static RouteHandlerBuilder Map(this IEndpointRouteBuilder endpoints, RoutePattern pattern, Delegate handler);
public static IEndpointConventionBuilder Map(this IEndpointRouteBuilder endpoints, string pattern, RequestDelegate requestDelegate);
public static RouteHandlerBuilder Map(this IEndpointRouteBuilder endpoints, string pattern, Delegate handler);


- **pattern**: Шаблон маршруту (`RoutePattern` або `string`), якому має відповідати запит.
- **handler**: Делегат (`Delegate` або `RequestDelegate`), який обробляє запит.

**Примітка**: Не плутайте метод `Map` для маршрутизації з однойменним методом для `IApplicationBuilder`, який використовується для розгалуження конвейєра.

#### Приклад використання `Map`
Створимо просте веб-додаток із кількома кінцевими точками:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", () => "Сторінка головна");
app.Map("/about", () => "Сторінка про нас");
app.Map("/contact", () => "Сторінка контактів");

app.Run();
```

**Результат використання методу Map**:
*Зображення: Веб-браузер відображає "Сторінка головна" для запиту до "/", "Сторінка про нас" для "/about", "Сторінка контактів" для "/contact", і помилку 404 для невідповідного маршруту*

**Пояснення**:
- Кожна кінцева точка відповідає певному маршруту.
- Якщо шлях запиту не відповідає жодній кінцевій точці, повертається помилка 404.

#### Повернення об’єктів
Обробник може повертати не лише рядки, а й об’єкти, які автоматично серіалізуються в JSON:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", () => "Сторінка головна");
app.Map("/user", () => new Person("Том", 37));

app.Run();

record class Person(string Name, int Age);
```

**Результат повернення об’єкта**:
*Зображення: Веб-браузер відображає JSON-об’єкт {"Name":"Том","Age":37} для запиту до "/user"*

#### Виконання дій без повернення
Обробник може не повертати значення, а лише виконувати дії:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", () => "Сторінка головна");
app.Map("/user", () => Console.WriteLine("Запит до /user"));

app.Run();
```

#### Окремий метод обробки
Обробник можна винести в окремий метод:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", IndexHandler);
app.Map("/user", UserHandler);

app.Run();

string IndexHandler() => "Сторінка головна";
Person UserHandler() => new Person("Том", 37);

record class Person(string Name, int Age);
```

#### Використання `RequestDelegate`
Для доступу до `HttpContext` використовується версія методу `Map` із `RequestDelegate`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", () => "Сторінка головна");
app.Map("/about", async (HttpContext context) =>
{
    await context.Response.WriteAsync("Сторінка про нас");
});

app.Run();
```

## Перегляд усіх кінцевих точок

ASP.NET Core дозволяє отримати список усіх кінцевих точок через `IEnumerable<EndpointDataSource>`.

### Приклад виведення кінцевих точок
Виведення простого списку кінцевих точок:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", () => "Сторінка головна");
app.Map("/about", () => "Сторінка про нас");
app.Map("/contact", () => "Сторінка контактів");

app.MapGet("/routes", (IEnumerable<EndpointDataSource> endpointSources) =>
    string.Join("\n", endpointSources.SelectMany(source => source.Endpoints)));

app.Run();
```

**Результат виведення кінцевих точок**:
*Зображення: Веб-браузер відображає список із чотирьох кінцевих точок*

### Детальна інформація про кінцеві точки
Виведення детальної інформації:

```csharp
using System.Text;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", () => "Сторінка головна");
app.Map("/about", () => "Сторінка про нас");
app.Map("/contact", () => "Сторінка контактів");

app.MapGet("/routes", (IEnumerable<EndpointDataSource> endpointSources) =>
{
    var sb = new StringBuilder();
    var endpoints = endpointSources.SelectMany(es => es.Endpoints);
    foreach (var endpoint in endpoints)
    {
        sb.AppendLine(endpoint.DisplayName);
        if (endpoint is RouteEndpoint routeEndpoint)
        {
            sb.AppendLine(routeEndpoint.RoutePattern.RawText);
        }
    }
    return sb.ToString();
});

app.Run();
```

**Результат детального виведення**:
*Зображення: Веб-браузер відображає детальну інформацію про кінцеві точки, включаючи шаблони маршрутів*

## Параметри маршрутів

Шаблони маршрутів можуть містити параметри, позначені фігурними дужками `{}`.

### Приклад із одним параметром
Обробка запиту з параметром `id`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/users/{id}", (string id) => $"ID користувача: {id}");
app.Map("/users", () => "Сторінка користувачів");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат одного параметра**:
*Зображення: Веб-браузер відображає "ID користувача: 134" для запиту "/users/134"*

**Пояснення**:
- Параметр `id` отримує значення останнього сегмента URL, наприклад, "134" для "/users/134".
- Якщо параметр відсутній, спрацьовує інша кінцева точка ("/users").

### Кілька параметрів
Обробка кількох параметрів:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/users/{id}/{name}", (string id, string name) => $"ID: {id} Ім'я: {name}");
app.Map("/users", () => "Сторінка користувачів");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат кількох параметрів**:
*Зображення: Веб-браузер відображає "ID: 123 Ім'я: Том" для запиту "/users/123/Том"*

#### Роздільники параметрів
Параметри мають бути розділені, наприклад, слешем (`/`) або дефісом (`-`):

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/users/{id}-{name}", (string id, string name) => $"ID: {id} Ім'я: {name}");
app.Map("/users", () => "Сторінка користувачів");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат роздільника**:
*Зображення: Веб-браузер відображає "ID: 123 Ім'я: Том" для запиту "/users/123-Том"*

### Необов’язкові параметри
Необов’язкові параметри позначаються знаком `?`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/users/{id?}", (string? id) => $"ID користувача: {id ?? "Не вказано"}");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат необов’язкового параметра**:
*Зображення: Веб-браузер відображає "ID користувача: Не вказано" для "/users" і "ID користувача: 23" для "/users/23"*

**Примітка**: Необов’язкові параметри мають бути в кінці шаблону маршруту.

### Значення за замовчуванням
Параметри можуть мати значення за замовчуванням:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/{controller=Home}/{action=Index}/{id?}", 
    (string controller, string action, string? id) =>
        $"Контролер: {controller}\nДія: {action}\nID: {id ?? "Не вказано"}");

app.Run();
```

**Результат значень за замовчуванням**:
*Зображення: Таблиця з результатами запитів, наприклад, "Контролер: Home Дія: Index ID: Не вказано" для "/" і "Контролер: Book Дія: Show ID: 2" для "/Book/Show/2"*

### Catch-all параметри
Параметри зі знаком `*` або `**` дозволяють обробляти довільну кількість сегментів:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/users/{**info}", (string info) => $"Інформація: {info}");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат catch-all параметра**:
*Зображення: Веб-браузер відображає "Інформація: profile/details/123" для запиту "/users/profile/details/123"*

## Обмеження маршрутів

Обмеження маршрутів дозволяють контролювати значення параметрів маршруту.

### Приклад обмеження
Обмеження параметра `id` на тип `int`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/users/{id:int}", (int id) => $"ID користувача: {id}");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат обмеження**:
*Зображення: Веб-браузер відображає "ID користувача: 123" для "/users/123" і помилку 404 для "/users/hello"*

**Пояснення**: Якщо значення параметра `id` не є цілим числом, запит не зіставляється з маршрутом.

### Список обмежень
ASP.NET Core підтримує наступні обмеження:

- **int**: Ціле число (`IntRouteConstraint`)
- **bool**: `true` або `false` (`BoolRouteConstraint`)
- **datetime**: Дата і час (`DateTimeRouteConstraint`)
- **decimal**: Десяткове число (`DecimalRouteConstraint`)
- **double**: Число з плаваючою комою (`DoubleRouteConstraint`)
- **float**: Число з плаваючою комою (`FloatRouteConstraint`)
- **guid**: GUID (`GuidRouteConstraint`)
- **long**: Довге ціле число (`LongRouteConstraint`)
- **minlength(value)**: Мінімальна довжина рядка (`MinLengthRouteConstraint`)
- **maxlength(value)**: Максимальна довжина рядка (`MaxLengthRouteConstraint`)
- **length(value)**: Точна довжина рядка (`LengthRouteConstraint`)
- **length(min, max)**: Довжина рядка в діапазоні (`LengthRouteConstraint`)
- **min(value)**: Мінімальне число (`MinRouteConstraint`)
- **max(value)**: Максимальне число (`MaxRouteConstraint`)
- **range(min, max)**: Число в діапазоні (`RangeRouteConstraint`)
- **alpha**: Тільки алфавітні символи (`AlphaRouteConstraint`)
- **regex(expression)**: Відповідність регулярному виразу (`RegexRouteConstraint`)
- **required**: Обов’язковий параметр (`RequiredRouteConstraint`)

### Комбінація обмежень
Обмеження можна комбінувати через двокрапку (`:`):

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/users/{name:alpha:minlength(2)}/{age:int:range(1,110)}",
    (string name, int age) => $"Вік: {age}\nІм'я: {name}");
app.Map("/phonebook/{phone:regex(^7-\\d{{3}}-\\d{{3}}-\\d{{4}}$)}",
    (string phone) => $"Телефон: {phone}");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат комбінації обмежень**:
*Зображення: Веб-браузер відображає "Вік: 25 Ім'я: Том" для "/users/Том/25" і "Телефон: 7-123-456-7890" для "/phonebook/7-123-456-7890"*

## Кастомні обмеження маршрутів

Для створення власних обмежень потрібно реалізувати інтерфейс `IRouteConstraint`.

### Приклад кастомного обмеження
Обмеження для перевірки секретного коду:

```csharp
public class SecretCodeConstraint : IRouteConstraint
{
    private readonly string secretCode;
    public SecretCodeConstraint(string secretCode)
    {
        this.secretCode = secretCode;
    }

    public bool Match(HttpContext? httpContext, IRouter? route, string routeKey,
        RouteValueDictionary values, RouteDirection routeDirection)
    {
        return values[routeKey]?.ToString() == secretCode;
    }
}

var builder = WebApplication.CreateBuilder(args);
builder.Services.Configure<RouteOptions>(options =>
    options.ConstraintMap.Add("secretcode", typeof(SecretCodeConstraint)));

var app = builder.Build();

app.Map("/users/{name}/{token:secretcode(123466)}",
    (string name, string token) => $"Ім'я: {name}\nТокен: {token}");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат кастомного обмеження**:
*Зображення: Веб-браузер відображає "Ім'я: Том Токен: 123466" для "/users/Том/123466" і помилку 404 для іншого токена*

### Обмеження на недопустимі значення
Обмеження, яке забороняє певні імена:

```csharp
public class InvalidNamesConstraint : IRouteConstraint
{
    private readonly string[] names = new[] { "Том", "Сем", "Боб" };
    public bool Match(HttpContext? httpContext, IRouter? route, string routeKey,
        RouteValueDictionary values, RouteDirection routeDirection)
    {
        return !names.Contains(values[routeKey]?.ToString());
    }
}

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRouting(options =>
    options.ConstraintMap.Add("invalidnames", typeof(InvalidNamesConstraint)));

var app = builder.Build();

app.Map("/users/{name:invalidnames}", (string name) => $"Ім'я: {name}");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат обмеження недопустимих імен**:
*Зображення: Веб-браузер відображає "Ім'я: Анна" для "/users/Анна" і помилку 404 для "/users/Том"*

## Передача залежностей у кінцеві точки

Залежності, додані до `IServiceCollection`, можна передавати в обробники кінцевих точок через параметри делегата.

### Приклад передачі залежності
Використання сервісу `TimeService`:

```csharp
public class TimeService
{
    public string Time => DateTime.Now.ToLongTimeString();
}

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddTransient<TimeService>();
var app = builder.Build();

app.Map("/time", (TimeService timeService) => $"Час: {timeService.Time}");
app.Map("/", () => "Hello ITStep");

app.Run();
```

**Результат передачі залежності**:
*Зображення: Веб-браузер відображає поточний час для "/time"*

### Окремий метод обробки з залежністю
Використання окремого методу:

```csharp
public class TimeService
{
    public string Time => DateTime.Now.ToLongTimeString();
}

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddTransient<TimeService>();
var app = builder.Build();

app.Map("/time", SendTime);
app.Map("/", () => "Hello ITStep");

app.Run();

string SendTime(TimeService timeService) => $"Час: {timeService.Time}";
```

## Сопоставлення запитів із кінцевими точками

Сопоставлення (URL matching) включає:

1. Вибір кінцевих точок, що відповідають шляху запиту.
2. Видалення тих, що не відповідають обмеженням маршруту.
3. Застосування `MatcherPolicy` для визначення порядку.
4. Вибір кінцевої точки за допомогою `EndpointSelector`.

### Пріоритетність шаблонів
Шаблони маршрутів мають пріоритет за специфічністю:
- Більше сегментів > менше сегментів.
- Статичний сегмент > параметр.
- Параметр з обмеженням > без обмеження.
- Комплексний сегмент > параметр з обмеженням.
- Catch-all параметр — найменш специфічний.

#### Приклад пріоритетності
Статичний сегмент має вищий пріоритет:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/hello", () => "Hello ITStep");
app.Map("/{message}", (string message) => $"Повідомлення: {message}");
app.Map("/", () => "Сторінка головна");

app.Run();
```

**Результат пріоритетності**:
*Зображення: Веб-браузер відображає "Hello ITStep" для "/hello"*

### Складний приклад пріоритетності
Пріоритет статичних сегментів:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/{controller}/Index/5", (string controller) => $"Контролер: {controller}");
app.Map("/Home/{action}/{id}", (string action) => $"Дія: {action}");

app.Run();
```

**Результат складної пріоритетності**:
*Зображення: Веб-браузер відображає "Дія: Index" для "/Home/Index/5"*

## Поєднання кінцевих точок із Middleware

Кінцеві точки виконуються після middleware у конвейєрі обробки.

### Приклад із Middleware
Логування виконання middleware і кінцевих точок:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Use(async (context, next) =>
{
    Console.WriteLine("Перший middleware початок");
    await next.Invoke();
    Console.WriteLine("Перший middleware кінець");
});

app.Map("/", () =>
{
    Console.WriteLine("Кінцева точка головної сторінки");
    return "Сторінка головна";
});

app.Use(async (context, next) =>
{
    Console.WriteLine("Другий middleware початок");
    await next.Invoke();
    Console.WriteLine("Другий middleware кінець");
});

app.Map("/about", () =>
{
    Console.WriteLine("Кінцева точка сторінки про нас");
    return "Сторінка про нас";
});

app.Run();
```

**Результат поєднання**:
*Зображення: Консоль із логами виконання middleware і кінцевих точок*

### Обробка запитів у Middleware
Middleware може обробляти запити за певними адресами:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Use(async (context, next) =>
{
    if (context.Request.Path == "/date")
        await context.Response.WriteAsync($"Дата: {DateTime.Now.ToShortDateString()}");
    else
        await next.Invoke();
});

app.Map("/", () => "Сторінка головна");
app.Map("/about", () => "Сторінка про нас");

app.Run();
```

### Обробка 404 у Middleware
Middleware для обробки помилки 404:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Use(async (context, next) =>
{
    await next.Invoke();
    if (context.Response.StatusCode == 404)
        await context.Response.WriteAsync("Ресурс не знайдено");
});

app.Map("/", () => "Сторінка головна");
app.Map("/about", () => "Сторінка про нас");

app.Run();
```

### Термінальний Middleware
Термінальний middleware перериває конвейєр:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/", () => "Сторінка головна");
app.Map("/about", () => "Сторінка про нас");

app.Run(async context =>
{
    context.Response.StatusCode = 404;
    await context.Response.WriteAsync("Ресурс не знайдено");
});

app.Run();
```

**Результат термінального middleware**:
*Зображення: Веб-браузер відображає "Ресурс не знайдено" для всіх запитів*

## Параметри рядка запиту

Рядок запиту (query string) — це частина URL після `?`, наприклад, `/user?name=Том&age=39`.

### Приклад отримання параметрів
Обробка параметрів рядка запиту:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/user", (string name, int age) => $"Ім'я: {name} Вік: {age}");
app.MapGet("/", () => "Hello ITStep");

app.Run();
```

**Результат параметрів рядка запиту**:
*Зображення: Веб-браузер відображає "Ім'я: Том Вік: 39" для "/user?name=Том&age=39"*

### Необов’язкові параметри
Необов’язкові параметри рядка запиту:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/user", (string name, int? age) => $"Ім'я: {name} Вік: {age ?? 0}");
app.MapGet("/", () => "Hello ITStep");

app.Run();
```

**Результат необов’язкових параметрів**:
*Зображення: Веб-браузер відображає "Ім'я: Сем Вік: 0" для "/user?name=Сем"*

### Пріоритет параметрів маршруту
Параметри маршруту мають вищий пріоритет:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/user/{name}", (string name, int age) => $"Ім'я: {name} Вік: {age}");
app.MapGet("/", () => "Hello ITStep");

app.Run();
```

**Результат пріоритету**:
*Зображення: Веб-браузер відображає "Ім'я: Том Вік: 39" для "/user/Том?age=39"*

### Об’єднання параметрів у об’єкт
Використання атрибута `[AsParameters]`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/user", ([AsParameters] Person person) => $"Ім'я: {person.Name} Вік: {person.Age}");
app.MapGet("/", () => "Hello ITStep");

app.Run();

record class Person(string Name, int Age);
```

**Результат об’єднання параметрів**:
*Зображення: Веб-браузер відображає "Ім'я: Том Вік: 39" для "/user?name=Том&age=39"*

## Висновок

Маршрутизація в ASP.NET Core забезпечує гнучке зіставлення запитів із кінцевими точками за допомогою методу `Map` та інших методів `IEndpointRouteBuilder`. Параметри маршрутів, обмеження, залежності та middleware дозволяють створювати складні сценарії обробки запитів. У наступних темах можна розглянути використання маршрутизації в MVC, атрибути маршрутів або розширені сценарії зіставлення.