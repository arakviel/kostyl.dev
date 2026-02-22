# Конфігурація в ASP.NET Core

Конфігурація в ASP.NET Core визначає базові налаштування додатка, такі як підключення до баз даних, параметри логування чи інші специфічні для проєкту дані. ASP.NET Core надає гнучку систему для роботи з конфігурацією, дозволяючи отримувати налаштування з різних джерел, таких як JSON-файли, змінні середовища, аргументи командного рядка тощо. У цьому матеріалі ми розглянемо основи конфігурації, роботу з різними джерелами, аналіз конфігураційних даних, створення власних провайдерів, а також проекцію конфігурації на класи через паттерн `IOptions`.

## Основи конфігурації

Конфігурація в ASP.NET Core представлена інтерфейсом `IConfiguration`, який дозволяє отримувати та встановлювати налаштування у форматі пар "ключ-значення". Основні джерела конфігурації включають:

- **Аргументи командного рядка**
- **Змінні середовища**
- **Об’єкти в пам’яті (.NET)**
- **Файли (JSON, XML, INI)**
- **Azure Key Vault** (для хмарних додатків)
- **Кастомні джерела**

### Інтерфейс `IConfiguration`

Інтерфейс `IConfiguration` визначає основні методи для роботи з конфігурацією:

```csharp
public interface IConfiguration
{
    string this[string key] { get; set; }
    IEnumerable<IConfigurationSection> GetChildren();
    IChangeToken GetReloadToken();
    IConfigurationSection GetSection(string key);
}
```

- **this[string key]**: Індексатор для доступу до значення за ключем.
- **GetChildren()**: Повертає дочірні секції конфігурації.
- **GetReloadToken()**: Повертає токен для відстеження змін конфігурації.
- **GetSection(string key)**: Повертає секцію конфігурації за ключем.

Інтерфейс `IConfigurationRoot`, який розширює `IConfiguration`, додає методи для роботи з провайдерами:

```csharp
public interface IConfigurationRoot : IConfiguration
{
    IEnumerable<IConfigurationProvider> Providers { get; }
    void Reload();
}
```

- **Providers**: Повертає колекцію провайдерів конфігурації.
- **Reload()**: Перезавантажує дані з усіх джерел.

### Отримання даних конфігурації

Конфігурація доступна через властивість `Configuration` об’єкта `WebApplication`. Наприклад:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Configuration["name"] = "Том";
app.Configuration["age"] = "37";

app.MapGet("/", async (context) =>
{
    string name = app.Configuration["name"];
    string age = app.Configuration["age"];
    await context.Response.WriteAsync($"{name} - {age}");
});

app.Run();
```

**Результат простої конфігурації**:
*Зображення: Веб-браузер відображає "Том - 37" для запиту `/`*

**Пояснення**:
- Налаштування додаються через індексатор `app.Configuration[key]`.
- Якщо ключ відсутній, він створюється; якщо існує, значення перезаписується.

## Додавання джерел конфігурації

Джерела конфігурації додаються через `ConfigurationManager` (властивість `Configuration` об’єкта `WebApplicationBuilder`).

### Конфігурація в пам’яті

Метод `AddInMemoryCollection` дозволяє додавати налаштування з колекції в пам’яті:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddInMemoryCollection(new Dictionary<string, string>
{
    {"name", "Том"},
    {"age", "37"}
});

var app = builder.Build();

app.MapGet("/", async (context) =>
{
    string name = app.Configuration["name"];
    string age = app.Configuration["age"];
    await context.Response.WriteAsync($"{name} - {age}");
});

app.Run();
```

**Результат конфігурації в пам’яті**:
*Зображення: Веб-браузер відображає "Том - 37" для запиту `/`*

### Аргументи командного рядка

Аргументи командного рядка автоматично додаються до конфігурації через `CommandLineConfigurationProvider`. Формат аргументів: `key=value`, `--key value`, або `/key value`.

#### Налаштування через `launchSettings.json`
У файлі `Properties/launchSettings.json` можна додати аргументи:

```json
{
  "profiles": {
    "HelloApp": {
      "commandName": "Project",
      "launchBrowser": true,
      "commandLineArgs": "name=Боб age=37",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      },
      "applicationUrl": "https://localhost:7256;http://localhost:5256",
      "dotnetRunMessages": true
    }
  }
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"{appConfig["name"]} - {appConfig["age"]}");

app.Run();
```

**Результат аргументів командного рядка**:
*Зображення: Веб-браузер відображає "Боб - 37" для запиту `/`*

#### Запуск через консоль
Запуск із командного рядка:

```
cd /path/to/project
dotnet run name=Том age=35
```

**Результат запуску через консоль**:
*Зображення: Веб-браузер відображає "Том - 35" для запиту `/`*

#### Симуляція аргументів
Програмна передача аргументів:

```csharp
var builder = WebApplication.CreateBuilder(new[] { "name=Аліса", "age=29" });
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"{appConfig["name"]} - {appConfig["age"]}");

app.Run();
```

### Змінні середовища

Змінні середовища завантажуються через `EnvironmentVariablesConfigurationProvider` автоматично.

#### Приклад використання змінних середовища
Отримання змінної `JAVA_HOME`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"JAVA_HOME: {appConfig["JAVA_HOME"] ?? "не встановлено"}");

app.Run();
```

**Результат змінних середовища**:
*Зображення: Веб-браузер відображає значення змінної `JAVA_HOME` або "не встановлено"*.

## Конфігурація у файлах (JSON, XML, INI)

Файли є поширеним способом зберігання конфігурації. ASP.NET Core підтримує JSON, XML і INI формати.

### Конфігурація в JSON

Файл `appsettings.json` завантажується за замовчуванням. Додаткові JSON-файли додаються через `AddJsonFile`.

#### Приклад із `config.json`
Файл `config.json`:

```json
{
  "person": "Том",
  "company": "Microsoft"
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("config.json");
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"{appConfig["person"]} - {appConfig["company"]}");

app.Run();
```

**Результат JSON-конфігурації**:
*Зображення: Веб-браузер відображає "Том - Microsoft" для запиту `/`*

#### Складна структура JSON
Файл `config.json` із вкладеною структурою:

```json
{
  "person": {
    "profile": {
      "name": "Томас",
      "email": "tom@gmail.com"
    }
  },
  "company": {
    "name": "Microsoft"
  }
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("config.json");
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) =>
{
    var personName = appConfig["person:profile:name"];
    var companyName = appConfig["company:name"];
    return $"{personName} - {companyName}";
});

app.Run();
```

**Результат складної JSON-конфігурації**:
*Зображення: Веб-браузер відображає "Томас - Microsoft" для запиту `/`*

### Конфігурація в XML

XML-файли завантажуються через `AddXmlFile`.

#### Приклад із `config.xml`
Файл `config.xml`:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<configuration>
  <person>Том</person>
  <company>Microsoft</company>
</configuration>
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddXmlFile("config.xml");
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"{appConfig["person"]} - {appConfig["company"]}");

app.Run();
```

**Результат XML-конфігурації**:
*Зображення: Веб-браузер відображає "Том - Microsoft" для запиту `/`*

#### Складна структура XML
Файл `config.xml` із вкладеною структурою:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<configuration>
  <person>
    <profile>
      <name>Томас</name>
      <email>tom@gmail.com</email>
    </profile>
  </person>
  <company>
    <name>Microsoft</name>
  </company>
</configuration>
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddXmlFile("config.xml");
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) =>
{
    var personName = appConfig["person:profile:name"];
    var companyName = appConfig["company:name"];
    return $"{personName} - {companyName}";
});

app.Run();
```

**Результат складної XML-конфігурації**:
*Зображення: Веб-браузер відображає "Томас - Microsoft" для запиту `/`*

### Конфігурація в INI

INI-файли завантажуються через `AddIniFile`.

#### Приклад із `config.ini`
Файл `config.ini`:

```ini
person=Боб
company=Microsoft
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddIniFile("config.ini");
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"{appConfig["person"]} - {appConfig["company"]}");

app.Run();
```

**Результат INI-конфігурації**:
*Зображення: Веб-браузер відображає "Боб - Microsoft" для запиту `/`*

## Конфігурація за замовчуванням і об’єднання джерел

ASP.NET Core автоматично завантажує конфігурацію з таких джерел у наступному порядку:

1. `ChainedConfigurationProvider` (об’єднує джерела).
2. `appsettings.json`.
3. `appsettings.{Environment}.json` (наприклад, `appsettings.Development.json`).
4. Секрети додатка (у середовищі Development).
5. Змінні середовища.
6. Аргументи командного рядка.

Пізніше додані джерела мають вищий пріоритет.

### Приклад об’єднання джерел
Код із кількома джерелами:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration
    .AddJsonFile("config.json")
    .AddXmlFile("config.xml")
    .AddIniFile("config.ini")
    .AddInMemoryCollection(new Dictionary<string, string>
    {
        {"name", "Сем"},
        {"age", "32"}
    });

var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"{appConfig["name"]} - {appConfig["age"]}");

app.Run();
```

**Результат об’єднання джерел**:
*Зображення: Веб-браузер відображає "Сем - 32" для запиту `/`*

**Пояснення**:
- Налаштування з `AddInMemoryCollection` перезаписують значення з файлів через вищий пріоритет.

## Аналіз конфігурації

Інтерфейс `IConfiguration` дозволяє аналізувати структуру конфігурації.

### Приклад аналізу JSON
Файл `project.json`:

```json
{
  "projectConfig": {
    "dependencies": {
      "Microsoft.Extensions.Configuration": "1.0.0",
      "Microsoft.NETCore.App": {
        "version": "1.0.1",
        "type": "platform"
      }
    },
    "frameworks": {
      "netcoreapp1.0": {
        "imports": ["dotnet5.6", "portable-net45+win8"]
      }
    }
  }
}
```

Код для аналізу:

```csharp
using System.Text;

var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("project.json");
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => GetSectionContent(appConfig.GetSection("projectConfig")));

app.Run();

string GetSectionContent(IConfiguration configSection)
{
    StringBuilder contentBuilder = new();
    foreach (var section in configSection.GetChildren())
    {
        contentBuilder.Append($"\"{section.Key}\":");
        if (section.Value == null)
        {
            string subSectionContent = GetSectionContent(section);
            contentBuilder.Append($"{{\n{subSectionContent}}},\n");
        }
        else
        {
            contentBuilder.Append($"\"{section.Value}\",\n");
        }
    }
    return contentBuilder.ToString();
}
```

**Результат аналізу JSON**:
*Зображення: Веб-браузер відображає структуру конфігурації `project.json` у вигляді тексту*

## Створення власного провайдера конфігурації

Для специфічних джерел можна створити власний провайдер.

### Приклад текстового провайдера
Файл `config.txt`:

```
name
Том
age
33
```

Клас провайдера:

```csharp
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using System.IO;

public class TextConfigurationProvider : ConfigurationProvider
{
    public string FilePath { get; }
    public TextConfigurationProvider(string path)
    {
        FilePath = path;
    }
    public override void Load()
    {
        var data = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        using (StreamReader textReader = new StreamReader(FilePath))
        {
            string? line;
            while ((line = textReader.ReadLine()) != null)
            {
                string key = line.Trim();
                string? value = textReader.ReadLine() ?? "";
                data.Add(key, value);
            }
        }
        Data = data;
    }
}
```

Джерело конфігурації:

```csharp
using Microsoft.Extensions.Configuration;

public class TextConfigurationSource : IConfigurationSource
{
    public string FilePath { get; }
    public TextConfigurationSource(string filename)
    {
        FilePath = filename;
    }
    public IConfigurationProvider Build(IConfigurationBuilder builder)
    {
        string filePath = builder.GetFileProvider().GetFileInfo(FilePath).PhysicalPath;
        return new TextConfigurationProvider(filePath);
    }
}
```

Розширення для `IConfigurationBuilder`:

```csharp
using Microsoft.Extensions.Configuration;

public static class TextConfigurationExtensions
{
    public static IConfigurationBuilder AddTextFile(this IConfigurationBuilder builder, string path)
    {
        if (builder == null) throw new ArgumentNullException(nameof(builder));
        if (string.IsNullOrEmpty(path)) throw new ArgumentException("Путь к файлу не вказано");
        var source = new TextConfigurationSource(path);
        builder.Add(source);
        return builder;
    }
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddTextFile("config.txt");
var app = builder.Build();

app.MapGet("/", (IConfiguration appConfig) => $"{appConfig["name"]} - {appConfig["age"]}");

app.Run();
```

**Результат текстового провайдера**:
*Зображення: Веб-браузер відображає "Том - 33" для запиту `/`*

## Проекція конфігурації на класи

Конфігурацію можна прив’язати до класів за допомогою методів `Bind` або `Get<T>`.

### Приклад із JSON
Файл `person.json`:

```json
{
  "name": "Том",
  "age": 22
}
```

Клас `Person`:

```csharp
public class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("person.json");
var app = builder.Build();

var person = new Person();
app.Configuration.Bind(person);

app.MapGet("/", async (context) => await context.Response.WriteAsync($"{person.Name} - {person.Age}"));

app.Run();
```

**Результат проекції JSON**:
*Зображення: Веб-браузер відображає "Том - 22" для запиту `/`*

### Складна структура
Файл `person.json` із вкладеною структурою:

```json
{
  "age": 28,
  "name": "Том",
  "languages": [
    "English",
    "German",
    "Spanish"
  ],
  "company": {
    "title": "Microsoft",
    "country": "USA"
  }
}
```

Класи:

```csharp
public class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
    public List<string> Languages { get; set; } = new();
    public Company? Company { get; set; }
}

public class Company
{
    public string Title { get; set; } = "";
    public string Country { get; set; } = "";
}
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("person.json");
var app = builder.Build();

var person = app.Configuration.Get<Person>();

app.MapGet("/", async (context) =>
{
    context.Response.ContentType = "text/html; charset=utf-8";
    string name = $"<p>Name: {person.Name}</p>";
    string age = $"<p>Age: {person.Age}</p>";
    string company = $"<p>Company: {person.Company?.Title}</p>";
    string langs = "<p>Languages:</p><ul>";
    foreach (var lang in person.Languages)
    {
        langs += $"<li><p>{lang}</p></li>";
    }
    langs += "</ul>";
    await context.Response.WriteAsync($"{name}{age}{company}{langs}");
});

app.Run();
```

**Результат складної проекції**:
*Зображення: Веб-браузер відображає HTML із даними про ім’я, вік, компанію та мови*

### Проекція секції
Прив’язка секції `company`:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("person.json");
var app = builder.Build();

var company = app.Configuration.GetSection("company").Get<Company>();

app.MapGet("/", async (context) => await context.Response.WriteAsync($"{company.Title} - {company.Country}"));

app.Run();

public class Company
{
    public string Title { get; set; } = "";
    public string Country { get; set; } = "";
}
```

**Результат проекції секції**:
*Зображення: Веб-браузер відображає "Microsoft - USA" для запиту `/`*

## Використання паттерну `IOptions`

Паттерн `IOptions` дозволяє передавати конфігурацію як об’єкти класів через механізм DI.

### Приклад із `IOptions`
Код із використанням `IOptions<Person>`:

```csharp
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("person.json");
builder.Services.Configure<Person>(builder.Configuration);
var app = builder.Build();

app.MapGet("/", (IOptions<Person> options) =>
{
    var person = options.Value;
    return $"{person.Name} - {person.Age}";
});

app.Run();

public class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
}
```

**Результат використання `IOptions`**:
*Зображення: Веб-браузер відображає "Том - 22" для запиту `/`*

### Використання `IOptions` у Middleware
Клас middleware:

```csharp
using Microsoft.Extensions.Options;

public class PersonMiddleware
{
    private readonly RequestDelegate _next;
    public Person Person { get; }
    public PersonMiddleware(RequestDelegate next, IOptions<Person> options)
    {
        _next = next;
        Person = options.Value;
    }
    public async Task InvokeAsync(HttpContext context)
    {
        var stringBuilder = new System.Text.StringBuilder();
        stringBuilder.Append($"<p>Name: {Person.Name}</p>");
        stringBuilder.Append($"<p>Age: {Person.Age}</p>");
        stringBuilder.Append($"<p>Company: {Person.Company?.Title}</p>");
        stringBuilder.Append("<h3>Languages</h3><ul>");
        foreach (string lang in Person.Languages)
            stringBuilder.Append($"<li>{lang}</li>");
        stringBuilder.Append("</ul>");
        await context.Response.WriteAsync(stringBuilder.ToString());
    }
}
```

Код програми:

```csharp
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("person.json");
builder.Services.Configure<Person>(builder.Configuration);
var app = builder.Build();

app.UseMiddleware<PersonMiddleware>();

app.Run();
```

**Результат middleware із `IOptions`**:
*Зображення: Веб-браузер відображає HTML із даними про ім’я, вік, компанію та мови*

## Динамічна конфігурація з `IOptionsSnapshot` і `IOptionsMonitor`

Для динамічних змін конфігурації використовуються `IOptionsSnapshot` (оновлюється для кожного запиту) і `IOptionsMonitor` (відстежує зміни в реальному часі).

### Приклад із `IOptionsSnapshot`
Файл `settings.json`:

```json
{
  "message": "Привіт, ITStep!"
}
```

Код програми:

```csharp
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("settings.json", optional: true, reloadOnChange: true);
builder.Services.Configure<MessageOptions>(builder.Configuration);
var app = builder.Build();

app.MapGet("/", (IOptionsSnapshot<MessageOptions> options) => options.Value.Message);

app.Run();

public class MessageOptions
{
    public string Message { get; set; } = "";
}
```

**Результат використання `IOptionsSnapshot`**:
*Зображення: Веб-браузер відображає "Привіт, ITStep!" для запиту `/`, оновлюється при зміні `settings.json`*

**Пояснення**:
- Параметр `reloadOnChange: true` дозволяє оновлювати конфігурацію при зміні файлу.
- `IOptionsSnapshot` забезпечує свіжу версію об’єкта для кожного запиту.

### Приклад із `IOptionsMonitor`
Код із відстеженням змін:

```csharp
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddJsonFile("settings.json", optional: true, reloadOnChange: true);
builder.Services.Configure<MessageOptions>(builder.Configuration);
var app = builder.Build();

app.MapGet("/", (IOptionsMonitor<MessageOptions> options) => options.CurrentValue.Message);

app.Run();

public class MessageOptions
{
    public string Message { get; set; } = "";
}
```

**Результат використання `IOptionsMonitor`**:
*Зображення: Веб-браузер відображає "Привіт, ITStep!" для запиту `/`, оновлюється в реальному часі при зміні `settings.json`*

**Пояснення**:
- `IOptionsMonitor` відстежує зміни конфігурації та викликає подію при їх зміні.
- Властивість `CurrentValue` повертає актуальний об’єкт.

## Практичний сценарій: Конфігурація підключення до бази даних

Розглянемо приклад із конфігурацією підключення до бази даних.

### Файл `appsettings.json`
Файл `appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Trusted_Connection=True;"
  }
}
```

Клас конфігурації:

```csharp
public class DatabaseOptions
{
    public string DefaultConnection { get; set; } = "";
}
```

Код програми:

```csharp
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);
builder.Services.Configure<DatabaseOptions>(builder.Configuration.GetSection("ConnectionStrings"));
var app = builder.Build();

app.MapGet("/", (IOptions<DatabaseOptions> options) => options.Value.DefaultConnection);

app.Run();
```

**Результат конфігурації бази даних**:
*Зображення: Веб-браузер відображає рядок підключення для запиту `/`*

## Висновок

Конфігурація в ASP.NET Core є потужним інструментом для налаштування додатків. Вона підтримує різноманітні джерела (JSON, XML, INI, змінні середовища, аргументи командного рядка), дозволяє створювати власні провайдери та проеціювати налаштування на класи через `Bind`, `Get<T>` або паттерн `IOptions`. Динамічна конфігурація через `IOptionsSnapshot` і `IOptionsMonitor` додає гнучкості для оновлення налаштувань у реальному часі. У наступних темах можна розглянути використання конфігурації в MVC, інтеграцію з сервісами логування або захист секретних даних через Azure Key Vault.