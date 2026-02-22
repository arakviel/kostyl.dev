# Робота зі статичними файлами в ASP.NET Core

Статичні файли, такі як HTML, CSS, JavaScript, зображення тощо, є важливою частиною вебдодатків. ASP.NET Core надає зручні інструменти для роботи зі статичними файлами через middleware, такі як `UseStaticFiles`, `UseDefaultFiles`, `UseDirectoryBrowser` та `UseFileServer`, а також новий компонент `MapStaticAssets`, представлений у ASP.NET Core 9.0. У цьому матеріалі ми розглянемо, як налаштувати каталог для статичних файлів, використовувати файли за замовчуванням, переглядати вміст каталогів, а також оптимізувати доставку статичних ресурсів за допомогою `MapStaticAssets`.

## Налаштування каталогу статичних файлів

За замовчуванням ASP.NET Core використовує папку `wwwroot` як кореневий каталог для статичних файлів. Ця папка визначається параметром `WebRootPath`, а кореневий каталог проєкту — параметром `ContentRootPath`. Якщо папка `wwwroot` відсутня, її потрібно створити вручну.

### Використання `UseStaticFiles`
Middleware `UseStaticFiles` дозволяє обслуговувати статичні файли з папки `wwwroot`.

#### Приклад використання `UseStaticFiles`
Створимо проєкт із папкою `wwwroot`, що містить файл `index.html`:


<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>ITStep</title>
</head>
<body>
    <h1>Головна сторінка</h1>
</body>
</html>


Код програми для обробки статичних файлів:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseStaticFiles();

app.Run(async (context) => await context.Response.WriteAsync("Hello ITStep"));

app.Run();
```

**Результат використання `UseStaticFiles`**:
![alt text](image-28.png)
*Зображення: Веб-браузер відображає вміст файлу `index.html` для запиту `/index.html` і "Hello ITStep" для інших запитів*

**Пояснення**:
- Middleware `UseStaticFiles` автоматично зіставляє запити до файлів у папці `wwwroot`.
- Наприклад, запит `/index.html` повертає вміст файлу `wwwroot/index.html`.

### Зміна каталогу статичних файлів
Якщо потрібно використовувати інший каталог, наприклад `static`, можна змінити `WebRootPath` через `WebApplicationOptions`.

#### Приклад зміни каталогу
Створимо папку `static` із файлом `content.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>ITStep</title>
</head>
<body>
    <h1>Вміст із папки static</h1>
</body>
</html>
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(new WebApplicationOptions { WebRootPath = "static" });
var app = builder.Build();

app.UseStaticFiles();

app.Run(async (context) => await context.Response.WriteAsync("Hello ITStep"));

app.Run();
```

**Результат зміни каталогу**:
![alt text](image-29.png)
*Зображення: Веб-браузер відображає вміст файлу `content.html` для запиту `/content.html`*

## Файли за замовчуванням

Middleware `UseDefaultFiles` дозволяє автоматично повертати файли за замовчуванням (`index.html`, `default.html`, `index.htm`, `default.htm`) для запиту до кореня програми.

### Приклад використання `UseDefaultFiles`
Код із підтримкою файлів за замовчуванням:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseDefaultFiles();
app.UseStaticFiles();

app.Run(async (context) => await context.Response.WriteAsync("Hello ITStep"));

app.Run();
```

**Результат використання `UseDefaultFiles`**:
![alt text](image-30.png)
*Зображення: Веб-браузер відображає вміст файлу `index.html` для запиту `/`*

**Пояснення**:
- `UseDefaultFiles` шукає файли за замовчуванням у папці `wwwroot`.
- Якщо файл знайдено, він повертається; інакше обробка переходить до наступного middleware.

### Нестандартний файл за замовчуванням
Можна вказати власний файл за замовчуванням через `DefaultFilesOptions`:

```csharp
using Microsoft.AspNetCore.Builder;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var options = new DefaultFilesOptions();
options.DefaultFileNames.Clear();
options.DefaultFileNames.Add("hello.html");
app.UseDefaultFiles(options);
app.UseStaticFiles();

app.Run(async (context) => await context.Response.WriteAsync("Hello ITStep"));

app.Run();
```

## Перегляд каталогів із `UseDirectoryBrowser`

Middleware `UseDirectoryBrowser` дозволяє клієнтам переглядати вміст каталогів.

### Приклад використання `UseDirectoryBrowser`
Код для перегляду вмісту папки `wwwroot`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseDirectoryBrowser();
app.UseStaticFiles();

app.Run();
```

**Результат перегляду каталогів**:
![alt text](image-31.png)
*Зображення: Веб-браузер відображає список файлів у папці `wwwroot` для запиту `/`*

### Сопоставлення каталогу з шляхом
Можна зіставити шлях запиту з конкретним каталогом:

```csharp
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseDirectoryBrowser(new DirectoryBrowserOptions
{
    FileProvider = new PhysicalFileProvider(Path.Combine(Directory.GetCurrentDirectory(), @"wwwroot/html")),
    RequestPath = new PathString("/pages")
});
app.UseStaticFiles();

app.Run();
```

**Результат зіставлення каталогу**:
![alt text](image-32.png)
*Зображення: Веб-браузер відображає вміст папки `wwwroot/html` для запиту `/pages`*

## Сопоставлення шляхів із каталогами через `UseStaticFiles`

Middleware `UseStaticFiles` також підтримує зіставлення шляхів із каталогами через `StaticFileOptions`.

### Приклад зіставлення
Сопоставлення шляху `/pages` із папкою `wwwroot/html`:

```csharp
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseStaticFiles();
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(Path.Combine(Directory.GetCurrentDirectory(), @"wwwroot/html")),
    RequestPath = new PathString("/pages")
});

app.Run();
```

**Результат зіставлення**:
![alt text](image-33.png)
*Зображення: Веб-браузер відображає вміст файлу `index.html` для запиту `/pages/index.html`*

## Використання `UseFileServer`

Middleware `UseFileServer` поєднує функціональність `UseStaticFiles`, `UseDefaultFiles` і `UseDirectoryBrowser`.

### Приклад використання `UseFileServer`
Базове використання:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseFileServer();

app.Run();
```

**Результат використання `UseFileServer`**:
![alt text](image-34.png)
*Зображення: Веб-браузер відображає вміст файлу `index.html` для запиту `/`*

### Налаштування `UseFileServer`
Увімкнення перегляду каталогів:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseFileServer(enableDirectoryBrowsing: true);

app.Run();
```

### Сопоставлення з каталогом
Сопоставлення шляху `/pages` із папкою `wwwroot/html`:

```csharp
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseFileServer(new FileServerOptions
{
    EnableDirectoryBrowsing = true,
    FileProvider = new PhysicalFileProvider(Path.Combine(Directory.GetCurrentDirectory(), @"wwwroot\html")),
    RequestPath = new PathString("/pages"),
    EnableDefaultFiles = false
});

app.Run();
```

## Оптимізація з `MapStaticAssets` (ASP.NET Core 9.0)

У ASP.NET Core 9.0 з’явився новий middleware `MapStaticAssets`, який оптимізує доставку статичних ресурсів завдяки сжаттю, відбиткам (fingerprinting) і кешуванню.

### Переваги `MapStaticAssets`
- **Сжаття**: Gzip (у розробці) або Brotli (у продакшені) для JavaScript і CSS.
- **Відбитки (fingerprinting)**: Додає хеш SHA-256 до імені файлу, що запобігає використанню застарілих версій.
- **Кешування**: Використовує директиву `immutable` або `max-age` для довготривалого кешування.
- **ETag**: Генерує теги ETag на основі вмісту файлу.
- **Попереднє завантаження**: Автоматично генерує теги `<link>` для ресурсів.

### Обмеження `MapStaticAssets`
- Не підтримує файли поза `wwwroot`.
- Не підтримує перегляд каталогів, файли за замовчуванням або `FileExtensionContentTypeProvider`.
- Не підходить для динамічних файлів із диска.

### Приклад використання `MapStaticAssets`
Створимо папку `wwwroot` із файлами `index.html` і `js/app.js`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>ITStep</title>
</head>
<body>
    <h1>Головна сторінка</h1>
    <script src="js/app.js"></script>
</body>
</html>
```

```javascript
console.log("Hello ITStep");
```

Код програми:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapStaticAssets();
app.MapGet("/", () => "Hello ITStep");

app.Run();
```

**Результат використання `MapStaticAssets`**:
![alt text](image-35.png)
![alt text](image-36.png)
*Зображення: Веб-браузер відображає вміст файлу `index.html` із виконаним скриптом `app.js` для запиту `/index.html`*

**Пояснення**:
- Запит до `/index.html` повертає файл із папки `wwwroot` із сжаттям і відбитками.
- Запит до `/` повертає "Hello ITStep", оскільки `MapStaticAssets` не підтримує файли за замовчуванням.

### Оптимізація кешування з `MapStaticAssets`
Додавання заголовків кешування та ETag:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapStaticAssets();

app.Run();
```

**Результат оптимізації кешування**:
![alt text](image-35.png)
*Зображення: Заголовки відповіді містять ETag, `immutable` або `max-age`, а файли сжаті через Brotli у продакшені*

## Додаткові можливості та оптимізації

### Використання CDN із `MapStaticAssets`
Для доставки статичних ресурсів ближче до користувача можна налаштувати CDN, додавши базовий URL у `StaticFileOptions`:

```csharp
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(Path.Combine(Directory.GetCurrentDirectory(), "wwwroot")),
    RequestPath = new PathString("/cdn"),
    ServeUnknownFileTypes = true,
    OnPrepareResponse = ctx =>
    {
        ctx.Context.Response.Headers["Cache-Control"] = "public, max-age=31536000";
        ctx.Context.Response.Headers["Content-Security-Policy"] = "default-src 'self' cdn.example.com";
    }
});

app.Run();
```

**Результат використання CDN**:
*Зображення: Статичні файли доступні через `/cdn` із довготривалим кешуванням і CSP-заголовками*

### Обмеження типів файлів
Використання `FileExtensionContentTypeProvider` для обмеження типів файлів:

```csharp
using Microsoft.AspNetCore.StaticFiles;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var provider = new FileExtensionContentTypeProvider();
provider.Mappings[".myapp"] = "application/x-myapp";
app.UseStaticFiles(new StaticFileOptions
{
    ContentTypeProvider = provider,
    ServeUnknownFileTypes = false
});

app.Run();
```

**Результат обмеження типів**:
*Зображення: Веб-браузер відображає файли з розширенням `.myapp` як `application/x-myapp`, інші відхиляються*

## Висновок

ASP.NET Core надає потужні інструменти для роботи зі статичними файлами через middleware `UseStaticFiles`, `UseDefaultFiles`, `UseDirectoryBrowser` і `UseFileServer`. У версії 9.0 доданий `MapStaticAssets`, який оптимізує доставку ресурсів завдяки сжаттю, відбиткам і кешуванню. Вибір між `UseStaticFiles` і `MapStaticAssets` залежить від потреб проєкту: перший підходить для динамічних файлів і гнучкого налаштування, другий — для оптимізації продуктивності статичних ресурсів. У наступних темах можна розглянути інтеграцію статичних файлів із MVC, використання Razor Pages або захист статичних файлів через авторизацію.
