# Логування в ASP.NET Core

Логування є критично важливою частиною розробки веб-додатків, оскільки воно дозволяє відстежувати виконання програми, діагностувати помилки та аналізувати поведінку системи. ASP.NET Core надає вбудовану систему логування, яка підтримує різні провайдери, рівні логування та гнучку конфігурацію. У цьому матеріалі ми розглянемо основи логування, використання інтерфейсу `ILogger`, провайдери логування, конфігурацію та фільтрацію логів, а також інтеграцію зі сторонніми бібліотеками, такими як Serilog.

## Ведення логу та `ILogger`

ASP.NET Core використовує інтерфейс `ILogger<T>` для логування. Логер автоматично надається через механізм впровадження залежностей (DI) або доступний через властивість `Logger` об’єкта `WebApplication`.

### Базове логування

Приклад використання вбудованого логера для виведення повідомлення на консоль:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", async (context) =>
{
    app.Logger.LogInformation($"Обробка запиту {context.Request.Path} о {DateTime.Now}");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат базового логування**:
*Зображення: Консоль відображає повідомлення "Обробка запиту / о [дата і час]"*

**Пояснення**:
- Властивість `app.Logger` повертає логер, налаштований для категорії за замовчуванням.
- Метод `LogInformation` виводить повідомлення рівня `Information`.

### Категорія логера

Категорія логера — це текстова мітка, яка асоціюється з повідомленнями логування. Зазвичай як категорію використовують ім’я класу, де застосовується логер.

#### Приклад із категорією
Логер із категорією `Program`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/hello", (ILogger<Program> logger) =>
{
    logger.LogInformation($"Шлях: /hello Час: {DateTime.Now.ToLongTimeString()}");
    return "Привіт, ITStep!";
});

app.Run();
```

**Результат логування з категорією**:
*Зображення: Консоль відображає повідомлення з міткою категорії "Program"*

**Пояснення**:
- Логер, отриманий через DI, типізується класом `Program`, що задає категорію.
- Категорія допомагає ідентифікувати джерело повідомлення в логах.

## Рівні та методи логування

ASP.NET Core підтримує наступні рівні логування (перелічення `LogLevel`):

- **Trace**: Найдетальніші повідомлення, корисні для розробки.
- **Debug**: Інформація для відладки.
- **Information**: Відстеження нормального виконання програми.
- **Warning**: Попередження про нестандартні ситуації.
- **Error**: Помилки, які не зупиняють додаток.
- **Critical**: Критичні помилки, що потребують негайної уваги.
- **None**: Вимкнення логування.

Методи логування відповідають рівням:

- `LogTrace()`
- `LogDebug()`
- `LogInformation()`
- `LogWarning()`
- `LogError()`
- `LogCritical()`

### Приклад використання різних рівнів
Код із різними рівнями логування:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", async (context) =>
{
    var path = context.Request.Path;
    app.Logger.LogCritical($"Критичне: {path}");
    app.Logger.LogError($"Помилка: {path}");
    app.Logger.LogWarning($"Попередження: {path}");
    app.Logger.LogInformation($"Інформація: {path}");
    app.Logger.LogDebug($"Відладка: {path}");
    app.Logger.LogTrace($"Трасування: {path}");

    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат різних рівнів логування**:
![alt text](image-37.png)
*Зображення: Консоль відображає повідомлення з різними рівнями, кожен із відповідним кольором і міткою*

**Пояснення**:
- Рівень `Trace` за замовчуванням відключений.
- Кожен рівень має унікальне форматування в консолі (наприклад, червоний для `Error`).

## Фабрика логера та провайдери логування

Фабрика логера (`ILoggerFactory`) дозволяє створювати логери з певними налаштуваннями.

### Використання `ILoggerFactory`
Приклад створення логера через фабрику:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

ILoggerFactory loggerFactory = LoggerFactory.Create(builder => builder.AddConsole());
ILogger logger = loggerFactory.CreateLogger<Program>();

app.MapGet("/", async (context) =>
{
    logger.LogInformation($"Запит до: {context.Request.Path}");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат використання фабрики**:
*Зображення: Консоль відображає повідомлення "Запит до: /"*

### Отримання фабрики через DI
Фабрика доступна через DI:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/hello", (ILoggerFactory loggerFactory) =>
{
    var logger = loggerFactory.CreateLogger("CustomLogger");
    logger.LogInformation($"Шлях: /hello Час: {DateTime.Now.ToLongTimeString()}");
    return "Привіт, ITStep!";
});

app.Run();
```

**Результат фабрики через DI**:
*Зображення: Консоль відображає повідомлення з категорією "CustomLogger"*

### Провайдери логування

ASP.NET Core підтримує наступні вбудовані провайдери:

- **Console**: Виведення в консоль (`AddConsole`).
- **Debug**: Виведення в `System.Diagnostics.Debug` (`AddDebug`).
- **EventSource**: Логування в ETW на Windows (`AddEventSourceLogger`).
- **EventLog**: Логування в Windows Event Log (`AddEventLog`).

#### Приклад із `AddDebug`
Виведення в Output Visual Studio:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var loggerFactory = LoggerFactory.Create(builder => builder.AddDebug());
ILogger logger = loggerFactory.CreateLogger<Program>();

app.MapGet("/", async (context) =>
{
    logger.LogInformation($"Запит до: {context.Request.Path}");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат Debug-провайдера**:
*Зображення: Вікно Output у Visual Studio відображає повідомлення "Запит до: /"*

## Конфігурація та фільтрація логування

Конфігурація логування визначається через файли, змінні середовища, аргументи командного рядка або код.

### Конфігурація через `appsettings.json`
Файл `appsettings.json`:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

**Пояснення**:
- `Default: Information` — логуються повідомлення рівня `Information` і вище для всіх категорій.
- `Microsoft.AspNetCore: Warning` — логуються повідомлення рівня `Warning` і вище для категорії `Microsoft.AspNetCore`.

#### Налаштування лише `Default`
Файл `appsettings.json` без `Microsoft.AspNetCore`:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  },
  "AllowedHosts": "*"
}
```

### Налаштування для різних провайдерів
Файл `appsettings.json` із провайдерами:

```json
{
  "Logging": {
    "Debug": {
      "LogLevel": {
        "Default": "Debug"
      }
    },
    "Console": {
      "LogLevel": {
        "Default": "Information",
        "Microsoft.AspNetCore": "Warning"
      }
    },
    "LogLevel": {
      "Default": "Error"
    }
  },
  "AllowedHosts": "*"
}
```

**Пояснення**:
- `Debug`: Логує рівень `Debug` для всіх категорій.
- `Console`: Логує `Information` для всіх категорій, крім `Microsoft.AspNetCore` (`Warning`).
- `LogLevel`: Загальний рівень `Error` для всіх провайдерів.

### Програмна конфігурація
Налаштування фільтрів через код:

```csharp
using Microsoft.Extensions.Logging;

var builder = WebApplication.CreateBuilder(args);
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
builder.Logging.AddFilter("System", LogLevel.Information)
              .AddFilter<ConsoleLoggerProvider>("Microsoft", LogLevel.Warning);

var app = builder.Build();

app.MapGet("/", async (context) =>
{
    app.Logger.LogInformation($"Запит до: {context.Request.Path}");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат програмної конфігурації**:
*Зображення: Консоль відображає повідомлення рівня `Information` для категорії `System`*

### Вибір правил фільтрації
Правила фільтрації обираються за наступною логікою:

1. Вибираються правила для конкретного провайдера; якщо їх немає — загальні правила.
2. Вибирається правило з найдовшим збігом категорії.
3. Якщо є кілька правил, використовується останнє за порядком.
4. Якщо правил немає, застосовується `MinimumLevel`.

#### Приклад із `MinimumLevel`
Код із мінімальним рівнем:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
builder.Logging.SetMinimumLevel(LogLevel.Debug);

var app = builder.Build();

app.MapGet("/", async (context) =>
{
    app.Logger.LogDebug($"Відладка: {context.Request.Path}");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат із `MinimumLevel`**:
*Зображення: Консоль відображає повідомлення рівня `Debug`*

## Сторонні провайдери: Serilog

Serilog — популярна бібліотека логування, яка інтегрується з ASP.NET Core.

### Встановлення Serilog
Додайте пакети NuGet:
- `Serilog.AspNetCore`
- `Serilog.Sinks.Console`
- `Serilog.Sinks.File`

### Приклад із Serilog
Файл `Program.cs`:

```csharp
using Serilog;

var builder = WebApplication.CreateBuilder(args);
builder.Host.UseSerilog((context, configuration) =>
{
    configuration.WriteTo.Console();
    configuration.WriteTo.File("logs/app.log", rollingInterval: RollingInterval.Day);
});

var app = builder.Build();

app.MapGet("/", async (context) =>
{
    app.Logger.LogInformation($"Запит до: {context.Request.Path}");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат із Serilog**:
*Зображення: Консоль і файл `logs/app.log` містять повідомлення "Запит до: /"*

**Пояснення**:
- `WriteTo.Console()` виводить логи в консоль.
- `WriteTo.File()` зберігає логи у файл із щоденною ротацією.

### Конфігурація Serilog через `appsettings.json`
Файл `appsettings.json`:

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [
      { "Name": "Console" },
      {
        "Name": "File",
        "Args": { "path": "logs/app.log", "rollingInterval": "Day" }
      }
    ]
  }
}
```

Код програми:

```csharp
using Serilog;

var builder = WebApplication.CreateBuilder(args);
builder.Host.UseSerilog((context, configuration) =>
{
    configuration.ReadFrom.Configuration(context.Configuration);
});

var app = builder.Build();

app.MapGet("/", async (context) =>
{
    app.Logger.LogInformation($"Запит до: {context.Request.Path}");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат конфігурації Serilog**:
*Зображення: Консоль і файл `logs/app.log` містять повідомлення з налаштуваннями з `appsettings.json`*

## Практичний сценарій: Логування запитів і помилок

Приклад middleware для логування запитів і обробки помилок:

```csharp
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        _logger.LogInformation($"Запит: {context.Request.Method} {context.Request.Path} о {DateTime.Now}");
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Помилка при обробці запиту {context.Request.Path}");
            throw;
        }
    }
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Logging.AddConsole();
var app = builder.Build();

app.UseMiddleware<RequestLoggingMiddleware>();

app.MapGet("/", async (context) =>
{
    if (new Random().Next(2) == 0)
        throw new Exception("Тестова помилка");
    await context.Response.WriteAsync("Привіт, ITStep!");
});

app.Run();
```

**Результат логування запитів**:
*Зображення: Консоль відображає логи запитів і помилок, якщо вони виникають*

## Висновок

Логування в ASP.NET Core є гнучким і потужним інструментом, який підтримує різні рівні, провайдери та конфігурації. Вбудовані провайдери, такі як `Console` і `Debug`, підходять для базового використання, тоді як сторонні бібліотеки, як Serilog, додають розширені можливості, такі як збереження логів у файли чи бази даних. Конфігурація через `appsettings.json` або код дозволяє точно налаштувати фільтрацію та формати виведення. У наступних темах можна розглянути інтеграцію логування з централізованими системами, такими як ELK Stack, або використання логування в MVC-додатках.