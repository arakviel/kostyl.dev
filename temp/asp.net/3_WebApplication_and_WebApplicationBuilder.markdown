# WebApplication і WebApplicationBuilder

## Огляд основного коду

У центрі будь-якого додатка ASP.NET Core, створеного за шаблоном **ASP.NET Core Empty**, лежить файл `Program.cs`. Типовий код цього файлу виглядає так:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello, World!");

app.Run();
```

Цей код демонструє мінімальну структуру додатка:
- `builder` — об’єкт класу `WebApplicationBuilder`, який відповідає за початкову конфігурацію.
- `app` — об’єкт класу `WebApplication`, який керує маршрутами, обробкою запитів і запуском додатка.
- `MapGet` — метод, що визначає маршрут для обробки GET-запитів.
- `Run` — метод, що запускає додаток.

## Клас WebApplicationBuilder

`WebApplicationBuilder` — це клас-будівельник, який створює основу для додатка ASP.NET Core. Він ініціалізується за допомогою статичного методу `WebApplication.CreateBuilder()`.

### Створення об’єкта WebApplicationBuilder
Існує кілька способів створення об’єкта:

1. **З аргументами командного рядка**:
   ```csharp
   var builder = WebApplication.CreateBuilder(args);
   ```
   Аргументи `args` передаються додатку під час запуску, наприклад, через командний рядок.

2. **З об’єктом WebApplicationOptions**:
   ```csharp
   var options = new WebApplicationOptions { Args = args };
   var builder = WebApplication.CreateBuilder(options);
   ```
   Об’єкт `WebApplicationOptions` дозволяє налаштувати додаткові параметри, такі як середовище виконання.

### Основні завдання WebApplicationBuilder
Клас `WebApplicationBuilder` виконує кілька ключових функцій:
- **Налаштування конфігурації**: Додає джерела конфігурації (наприклад, `appsettings.json`).
- **Реєстрація сервісів**: Дозволяє додавати сервіси для Dependency Injection.
- **Налаштування логування**: Визначає, як додаток записуватиме логи.
- **Встановлення середовища**: Вказує, в якому середовищі працює додаток (Development, Production тощо).
- **Конфігурація хостів**: Налаштовує `IHostBuilder` і `IWebHostBuilder` для створення хоста.

### Властивості WebApplicationBuilder
Клас має кілька важливих властивостей для налаштування:
- **`Configuration`**: Об’єкт `ConfigurationManager` для роботи з конфігурацією додатка.
- **`Environment`**: Інформація про середовище виконання (наприклад, `Development` чи `Production`).
- **`Host`**: Об’єкт `IHostBuilder` для налаштування хоста.
- **`Logging`**: Налаштування системи логування.
- **`Services`**: Колекція сервісів для Dependency Injection.
- **`WebHost`**: Об’єкт `IWebHostBuilder` для конфігурації вебсервера (наприклад, Kestrel).

## Клас WebApplication

Після налаштування `WebApplicationBuilder` викликається метод `Build()`, який створює об’єкт `WebApplication`:

```csharp
var app = builder.Build();
```

`WebApplication` — це центральний клас, який керує роботою додатка, обробкою запитів і маршрутизацією. Його вихідний код доступний на [GitHub](https://github.com/dotnet/aspnetcore/blob/main/src/Http/Http.Abstractions/WebApplication.cs).

### Інтерфейси WebApplication
Клас `WebApplication` реалізує три ключові інтерфейси:
- **`IHost`**: Відповідає за запуск і зупинку хоста, який обробляє вхідні запити.
- **`IApplicationBuilder`**: Налаштовує middleware для обробки HTTP-запитів.
- **`IEndpointRouteBuilder`**: Визначає маршрути для обробки запитів.

### Властивості WebApplication
Основні властивості для доступу до функціональності:
- **`Configuration`**: Об’єкт `IConfiguration` для доступу до конфігурації.
- **`Environment`**: Об’єкт `IWebHostEnvironment` для інформації про середовище.
- **`Lifetime`**: Управління подіями життєвого циклу додатка (запуск, зупинка).
- **`Logger`**: Логер додатка за замовчуванням.
- **`Services`**: Колекція сервісів, доступних у додатку.
- **`Urls`**: Список адрес, які використовує сервер (наприклад, `https://localhost:5001`).

### Методи управління хостом
Клас `WebApplication` надає методи для управління додатком:
- **`Run()`**: Синхронно запускає додаток.
- **`RunAsync()`**: Асинхронно запускає додаток.
- **`Start()`**: Синхронно запускає прослуховування запитів.
- **`StartAsync()`**: Асинхронно запускає прослуховування.
- **`StopAsync()`**: Асинхронно зупиняє додаток.

Приклад асинхронного запуску та зупинки:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello, World!");

await app.StartAsync();
await Task.Delay(10000); // Чекаємо 10 секунд
await app.StopAsync();   // Зупиняємо додаток
```

Цей код запускає додаток, чекає 10 секунд і зупиняє його програмно.

## Приклад роботи маршрутів
Маршрути в Minimal API визначаються за допомогою методів, таких як `MapGet`. Наприклад:

```csharp
app.MapGet("/", () => "Hello, World!");
```

Цей код налаштовує маршрут, який повертає рядок `"Hello, World!"` при зверненні до кореня додатка (наприклад, `https://localhost:7256/`). Метод `MapGet` приймає два параметри:
- **Шлях**: У цьому випадку `"/"` (корінь додатка).
- **Обробник**: Лямбда-вираз, що визначає, що повертається за запитом.

## Висновок

Класи `WebApplication` і `WebApplicationBuilder` є основою Minimal API в ASP.NET Core. `WebApplicationBuilder` відповідає за початкову конфігурацію, тоді як `WebApplication` керує маршрутами, обробкою запитів і запуском додатка. Завдяки простоті та гнучкості Minimal API дозволяє створювати легкі вебдодатки з мінімальною кількістю коду. У наступних темах можна розглянути додавання middleware, сервісів або складніших маршрутів.
