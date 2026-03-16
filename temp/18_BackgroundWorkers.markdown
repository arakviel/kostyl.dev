# Background Workers в ASP.NET Core

## 🎯 Що таке Background Workers?

**Background Workers** (фонові воркери) - це сервіси, які виконують завдання у фоновому режимі, незалежно від HTTP-запитів користувачів.

### 🏭 Аналогія з реального життя
Уявіть собі ресторан:
- **Офіціанти** (Controllers) - обслуговують клієнтів, приймають замовлення
- **Кухарі** (Background Workers) - готують їжу у фоновому режимі, навіть коли немає клієнтів
- **Прибиральники** (Cleanup Workers) - прибирають ресторан після закриття

### � Детальне пояснення концепції

**Звичайний веб-додаток** працює так:
1. Користувач надсилає HTTP-запит
2. Сервер обробляє запит
3. Сервер повертає відповідь
4. З'єднання закривається

**З Background Workers:**
1. Веб-додаток обслуговує користувачів (як завжди)
2. **ПАРАЛЕЛЬНО** фонові сервіси виконують свою роботу
3. Фонові сервіси працюють **незалежно** від користувачів

### 🎭 Життєвий цикл Background Workers

```
Запуск додатку → Старт Background Workers → Робота у фоні → Зупинка додатку → Graceful Shutdown
```

## 📚 Теоретичні основи: Ієрархія класів

### 🏗️ Архітектура Background Workers в .NET

```
IHostedService (інтерфейс)
    ↓
BackgroundService (абстрактний клас)
    ↓
Ваш клас (конкретна реалізація)
```

## �🔧 Основні типи Background Workers

### 📖 Теорія: Що таке IHostedService?

**IHostedService** - це базовий інтерфейс в .NET Core для сервісів, які:
- Запускаються разом з додатком
- Працюють у фоновому режимі
- Зупиняються разом з додатком

```csharp
public interface IHostedService
{
    Task StartAsync(CancellationToken cancellationToken);
    Task StopAsync(CancellationToken cancellationToken);
}
```

**Аналогія**: IHostedService - це як "контракт працівника", який говорить:
- "Я знаю, коли почати роботу" (StartAsync)
- "Я знаю, коли закінчити роботу" (StopAsync)

### 📖 Теорія: Що таке BackgroundService?

**BackgroundService** - це абстрактний клас, який:
- Реалізує IHostedService
- Спрощує створення довготривалих фонових завдань
- Надає метод ExecuteAsync для основної логіки

```csharp
public abstract class BackgroundService : IHostedService
{
    protected abstract Task ExecuteAsync(CancellationToken stoppingToken);

    // Внутрішня реалізація StartAsync та StopAsync
}
```

**Аналогія**: BackgroundService - це як "досвідчений працівник", який:
- Знає, як правильно почати і закінчити роботу
- Вам потрібно лише сказати, що саме робити (ExecuteAsync)

### 🔄 Порівняння підходів

| Аспект | IHostedService | BackgroundService |
|--------|----------------|-------------------|
| **Складність** | Більше коду | Менше коду |
| **Контроль** | Повний контроль | Спрощений |
| **Використання** | Складні сценарії | Прості циклічні завдання |
| **Аналогія** | Архітектор будинку | Будівельник за планом |

## 🧠 Глибока теорія: Як це працює всередині?

### 🔄 CancellationToken - Теорія сигналізації

**CancellationToken** - це механізм для "ввічливого" зупинення фонових завдань.

```csharp
// Аналогія: CancellationToken - це як "дзвінок на перерву" в школі
public async Task DoWork(CancellationToken cancellationToken)
{
    while (!cancellationToken.IsCancellationRequested) // "Чи дзвенить дзвінок?"
    {
        // Робимо роботу
        await SomeWork();

        // Перевіряємо знову
        cancellationToken.ThrowIfCancellationRequested(); // "Якщо дзвенить - зупиняємося"
    }
}
```

**Чому це важливо?**
- ❌ **Без CancellationToken**: Додаток "вбиває" процес силою
- ✅ **З CancellationToken**: Процес завершується акуратно

### 🏗️ Dependency Injection в Background Workers

**Проблема**: Background Workers живуть довго, а деякі сервіси (Scoped) - коротко.

```csharp
// ❌ НЕПРАВИЛЬНО - DbContext живе коротко, а Worker - довго
public class BadWorker : BackgroundService
{
    private readonly AppDbContext _context; // Проблема!

    public BadWorker(AppDbContext context)
    {
        _context = context; // Цей контекст може "померти"
    }
}

// ✅ ПРАВИЛЬНО - створюємо "короткоживучі" сервіси за потреби
public class GoodWorker : BackgroundService
{
    private readonly IServiceProvider _serviceProvider; // "Фабрика сервісів"

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var scope = _serviceProvider.CreateScope(); // "Створюємо новий набір інструментів"
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        // Використовуємо свіжий контекст
    }
}
```

**Аналогія**:
- **IServiceProvider** - це як "склад інструментів"
- **Scope** - це як "набір інструментів для конкретної роботи"
- **Scoped Service** - це як "одноразовий інструмент"

### 🎯 Життєвий цикл сервісів

| Тип сервісу | Час життя | Аналогія |
|-------------|-----------|----------|
| **Singleton** | Весь час роботи додатку | Директор компанії |
| **Scoped** | Один HTTP-запит | Касир в магазині (одна зміна) |
| **Transient** | Кожне використання | Одноразовий стаканчик |

**Background Workers** - це Singleton, тому вони не можуть напряму використовувати Scoped сервіси.

## 🔧 Детальний розбір типів Background Workers

### 1. BackgroundService - Детальна теорія

**BackgroundService** - це абстрактний клас, який:

```csharp
public abstract class BackgroundService : IHostedService, IDisposable
{
    private Task _executingTask;
    private readonly CancellationTokenSource _stoppingCts = new();

    // Ваш код йде сюди
    protected abstract Task ExecuteAsync(CancellationToken stoppingToken);

    // .NET автоматично викликає це при старті
    public virtual Task StartAsync(CancellationToken cancellationToken)
    {
        _executingTask = ExecuteAsync(_stoppingCts.Token);
        return _executingTask.IsCompleted ? _executingTask : Task.CompletedTask;
    }

    // .NET автоматично викликає це при зупинці
    public virtual async Task StopAsync(CancellationToken cancellationToken)
    {
        _stoppingCts.Cancel(); // Сигналізуємо про зупинку
        await _executingTask; // Чекаємо завершення
    }
}
```

**Що це означає?**
- Ви пишете тільки `ExecuteAsync` - основну логіку
- .NET сам керує запуском і зупинкою
- Автоматична обробка CancellationToken

**Приклад простого BackgroundService:**

```csharp
public class SimpleWorker : BackgroundService
{
    private readonly ILogger<SimpleWorker> _logger;

    public SimpleWorker(ILogger<SimpleWorker> logger)
    {
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // Аналогія: як нічний сторож, який обходить будівлю кожну годину
        while (!stoppingToken.IsCancellationRequested)
        {
            _logger.LogInformation("Патрулювання о {Time}", DateTime.Now);

            // Чекаємо годину до наступного обходу
            await Task.Delay(TimeSpan.FromHours(1), stoppingToken);
        }
    }
}
```

### 2. IHostedService - Детальна теорія

**IHostedService** дає вам **повний контроль** над життєвим циклом:

```csharp
public class AdvancedWorker : IHostedService
{
    private readonly ILogger<AdvancedWorker> _logger;
    private Timer _timer;
    private int _executionCount = 0;

    public AdvancedWorker(ILogger<AdvancedWorker> logger)
    {
        _logger = logger;
    }

    // Викликається при старті додатку
    public Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Advanced Worker запущено");

        // Аналогія: як будильник, який дзвенить кожні 30 секунд
        _timer = new Timer(DoWork, null, TimeSpan.Zero, TimeSpan.FromSeconds(30));

        return Task.CompletedTask;
    }

    // Викликається при зупинці додатку
    public Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Advanced Worker зупинено");

        // Вимикаємо будильник
        _timer?.Change(Timeout.Infinite, 0);

        return Task.CompletedTask;
    }

    private void DoWork(object state)
    {
        var count = Interlocked.Increment(ref _executionCount);
        _logger.LogInformation("Виконання #{Count} о {Time}", count, DateTime.Now);
    }

    public void Dispose()
    {
        _timer?.Dispose();
    }
}
```

### 🔍 Коли використовувати що?

#### ✅ Використовуйте BackgroundService коли:
- Потрібен **простий циклічний процес**
- Логіка виконується **безперервно**
- Не потрібен складний контроль часу

**Приклади:**
- Обробка черги повідомлень
- Моніторинг файлової системи
- Періодичне очищення кешу

#### ✅ Використовуйте IHostedService коли:
- Потрібен **точний контроль** над запуском/зупинкою
- Використовуєте **Timer** для планування
- Потрібна **складна логіка ініціалізації**

**Приклади:**
- Планувальник завдань (як cron)
- Ініціалізація зовнішніх з'єднань
- Складні сценарії запуску

### 🎭 Внутрішня робота .NET Host

Коли ви запускаєте ASP.NET Core додаток:

```
1. Створення Host
   ↓
2. Реєстрація всіх IHostedService
   ↓
3. Виклик StartAsync() для всіх сервісів (паралельно)
   ↓
4. Додаток працює
   ↓
5. Сигнал зупинки (Ctrl+C, SIGTERM)
   ↓
6. Виклик StopAsync() для всіх сервісів (паралельно)
   ↓
7. Очікування завершення (до 30 секунд за замовчуванням)
   ↓
8. Примусове завершення якщо потрібно
```

**Аналогія**: Як управління рестораном:
1. **Відкриття** - всі працівники приходять на роботу
2. **Робочий день** - кожен виконує свої обов'язки
3. **Закриття** - всім дають сигнал завершити роботу
4. **Очікування** - чекають поки всі закінчать
5. **Вимкнення світла** - якщо хтось не встиг

## 🧵 Теорія Threading та Performance

### 🎯 Як Background Workers використовують потоки?

**Важливо розуміти**: Background Workers **НЕ** створюють нові потоки автоматично!

```csharp
// ❌ БЛОКУЮЧИЙ код - займає потік з ThreadPool
public class BadWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            Thread.Sleep(1000); // ПОГАНО! Блокує потік
            DoSyncWork(); // ПОГАНО! Синхронна робота
        }
    }
}

// ✅ АСИНХРОННИЙ код - звільняє потоки
public class GoodWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await Task.Delay(1000, stoppingToken); // ДОБРЕ! Не блокує
            await DoAsyncWork(); // ДОБРЕ! Асинхронна робота
        }
    }
}
```

**Аналогія**:
- **Thread.Sleep** - як працівник, який спить на робочому місці
- **Task.Delay** - як працівник, який йде на перерву і звільняє місце

### ⚡ Performance та ресурси

#### 📊 Споживання ресурсів

| Тип операції | Споживання потоків | Споживання пам'яті |
|--------------|-------------------|-------------------|
| **Синхронний Background Worker** | 1 потік постійно | Середнє |
| **Асинхронний Background Worker** | 0-1 потік (за потреби) | Низьке |
| **Timer-based Worker** | 0 потоків (між викликами) | Дуже низьке |

#### 🎛️ Налаштування Performance

```csharp
public class OptimizedWorker : BackgroundService
{
    private readonly ILogger<OptimizedWorker> _logger;
    private readonly SemaphoreSlim _semaphore;

    public OptimizedWorker(ILogger<OptimizedWorker> logger)
    {
        _logger = logger;
        // Обмежуємо кількість паралельних операцій
        _semaphore = new SemaphoreSlim(Environment.ProcessorCount);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // Створюємо канал для обробки повідомлень
        var channel = Channel.CreateUnbounded<WorkItem>();
        var reader = channel.Reader;

        // Запускаємо кілька обробників паралельно
        var processors = Enumerable.Range(0, Environment.ProcessorCount)
            .Select(_ => ProcessItems(reader, stoppingToken))
            .ToArray();

        // Чекаємо завершення всіх обробників
        await Task.WhenAll(processors);
    }

    private async Task ProcessItems(ChannelReader<WorkItem> reader, CancellationToken cancellationToken)
    {
        await foreach (var item in reader.ReadAllAsync(cancellationToken))
        {
            await _semaphore.WaitAsync(cancellationToken);
            try
            {
                await ProcessItem(item);
            }
            finally
            {
                _semaphore.Release();
            }
        }
    }
}
```

### 🔄 Теорія Task Management

#### 📝 Правильне управління Task'ами

```csharp
public class TaskManagementWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // ✅ Правильно: використовуємо ConfigureAwait(false)
        await SomeAsyncOperation().ConfigureAwait(false);

        // ✅ Правильно: обробляємо кілька завдань паралельно
        var tasks = new List<Task>();
        for (int i = 0; i < 10; i++)
        {
            tasks.Add(ProcessItemAsync(i, stoppingToken));
        }
        await Task.WhenAll(tasks);

        // ✅ Правильно: використовуємо timeout
        using var cts = CancellationTokenSource.CreateLinkedTokenSource(stoppingToken);
        cts.CancelAfter(TimeSpan.FromMinutes(5));

        try
        {
            await LongRunningOperation(cts.Token);
        }
        catch (OperationCanceledException) when (cts.Token.IsCancellationRequested)
        {
            // Операція перевищила timeout
        }
    }
}
```

## 🔧 Практичні приклади з теорією

### 1. Email Service - Повний розбір

**Теорія**: Email Service - це класичний приклад Producer-Consumer pattern.
- **Producer** - контролери додають email'и в чергу
- **Consumer** - Background Worker обробляє чергу

**Архітектурний патерн:**
```
HTTP Request → Controller → Додає email в БД → Повертає відповідь
                                ↓
Background Worker → Читає з БД → Відправляє email → Оновлює статус
```

**Детальний розбір коду:**

```csharp
// 🏗️ Наслідуємося від BackgroundService для автоматичного управління життєвим циклом
public class EmailSenderService : BackgroundService
{
    // 📦 Dependency Injection - отримуємо залежності через конструктор
    private readonly ILogger<EmailSenderService> _logger; // Для логування
    private readonly IServiceProvider _serviceProvider;   // "Фабрика сервісів" для створення Scoped

    // 🏗️ Конструктор - .NET автоматично передає залежності
    public EmailSenderService(
        ILogger<EmailSenderService> logger,
        IServiceProvider serviceProvider)
    {
        _logger = logger;
        _serviceProvider = serviceProvider;
    }

    // 🎯 Основна логіка - викликається автоматично при старті додатку
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Email Service запущено");

        // 🔄 Основний цикл - працює до сигналу зупинки
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // 📧 Обробляємо чергу email'ів
                var processedCount = await ProcessEmailQueue(stoppingToken);

                if (processedCount > 0)
                {
                    _logger.LogInformation("Оброблено {Count} email'ів", processedCount);
                }

                // ⏰ Чекаємо 1 хвилину перед наступною перевіркою
                // ВАЖЛИВО: використовуємо Task.Delay з CancellationToken
                await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
            }
            catch (OperationCanceledException)
            {
                // 🛑 Нормальна зупинка - виходимо з циклу
                _logger.LogInformation("Email Service отримав сигнал зупинки");
                break;
            }
            catch (Exception ex)
            {
                // 🚨 Неочікувана помилка - логуємо і продовжуємо роботу
                _logger.LogError(ex, "Помилка в Email Service");

                // Чекаємо перед повторною спробою
                await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
            }
        }

        _logger.LogInformation("Email Service зупинено");
    }

    // 🔧 Приватний метод для обробки черги
    private async Task<int> ProcessEmailQueue(CancellationToken cancellationToken)
    {
        // 🏭 КРИТИЧНО ВАЖЛИВО: створюємо новий scope для Scoped сервісів
        // Чому? Тому що Background Worker живе довго (Singleton),
        // а DbContext живе коротко (Scoped)
        using var scope = _serviceProvider.CreateScope();

        // 📦 Отримуємо сервіси з нового scope
        var emailService = scope.ServiceProvider.GetRequiredService<IEmailService>();
        var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        // 📋 Отримуємо email'и для відправки
        var pendingEmails = await dbContext.Emails
            .Where(e => e.Status == EmailStatus.Pending)
            .Take(10) // Обробляємо по 10 за раз (batch processing)
            .ToListAsync(cancellationToken);

        var processedCount = 0;

        // 🔄 Обробляємо кожен email
        foreach (var email in pendingEmails)
        {
            // 🛑 Перевіряємо, чи не потрібно зупинятися
            cancellationToken.ThrowIfCancellationRequested();

            try
            {
                // 📧 Відправляємо email
                await emailService.SendAsync(email.To, email.Subject, email.Body);

                // ✅ Позначаємо як відправлений
                email.Status = EmailStatus.Sent;
                email.SentAt = DateTime.UtcNow;

                processedCount++;
            }
            catch (Exception ex)
            {
                // ❌ Позначаємо як помилку
                email.Status = EmailStatus.Failed;
                email.ErrorMessage = ex.Message;

                _logger.LogError(ex, "Не вдалося відправити email {EmailId}", email.Id);
            }
        }

        // 💾 Зберігаємо всі зміни в базі даних
        if (pendingEmails.Any())
        {
            await dbContext.SaveChangesAsync(cancellationToken);
        }

        return processedCount;
    }
}
```

## 🚨 Типові помилки початківців (з поясненнями)

### ❌ Помилка #1: Неправильне використання Scoped сервісів

```csharp
// НЕПРАВИЛЬНО - призведе до помилки
public class BadEmailService : BackgroundService
{
    private readonly AppDbContext _context; // ❌ DbContext є Scoped!

    public BadEmailService(AppDbContext context)
    {
        _context = context; // ❌ Цей контекст "помре" через деякий час
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            // ❌ Спроба використати "мертвий" контекст
            var emails = await _context.Emails.ToListAsync(); // EXCEPTION!
        }
    }
}
```

**Чому це не працює?**
- Background Worker живе **весь час роботи додатку** (Singleton)
- DbContext живе **тільки один HTTP-запит** (Scoped)
- Коли HTTP-запит закінчується, DbContext "вмирає"
- Background Worker намагається використати "мертвий" DbContext

### ❌ Помилка #2: Блокування потоків

```csharp
// НЕПРАВИЛЬНО - блокує потоки
public class BadWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            Thread.Sleep(1000);           // ❌ Блокує потік!
            var result = SomeMethod();    // ❌ Синхронний виклик!
            File.ReadAllText("file.txt"); // ❌ Блокуючий I/O!
        }
    }
}

// ПРАВИЛЬНО - асинхронно
public class GoodWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await Task.Delay(1000, stoppingToken);        // ✅ Не блокує!
            var result = await SomeMethodAsync();          // ✅ Асинхронно!
            await File.ReadAllTextAsync("file.txt");      // ✅ Асинхронний I/O!
        }
    }
}
```

### ❌ Помилка #3: Ігнорування CancellationToken

```csharp
// НЕПРАВИЛЬНО - ігнорує сигнали зупинки
public class BadWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (true) // ❌ Ніколи не зупиниться!
        {
            await DoWork(); // ❌ Не передає CancellationToken
            await Task.Delay(1000); // ❌ Не передає CancellationToken
        }
    }
}

// ПРАВИЛЬНО - реагує на сигнали зупинки
public class GoodWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested) // ✅ Перевіряє сигнал
        {
            await DoWork(stoppingToken); // ✅ Передає CancellationToken
            await Task.Delay(1000, stoppingToken); // ✅ Передає CancellationToken
        }
    }
}
```

### 2. IHostedService
Інтерфейс для більш гнучкого контролю життєвого циклу.

```csharp
public class DataBackupService : IHostedService
{
    private Timer _timer;
    private readonly ILogger<DataBackupService> _logger;

    public DataBackupService(ILogger<DataBackupService> logger)
    {
        _logger = logger;
    }

    public Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Backup service started");

        // Запуск таймера для щоденного бекапу о 2:00
        _timer = new Timer(DoBackup, null,
            GetTimeUntilNextRun(),
            TimeSpan.FromDays(1));

        return Task.CompletedTask;
    }

    public Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Backup service stopped");
        _timer?.Change(Timeout.Infinite, 0);
        return Task.CompletedTask;
    }

    private void DoBackup(object state)
    {
        _logger.LogInformation("Starting database backup...");
        // Логіка бекапу
    }

    private TimeSpan GetTimeUntilNextRun()
    {
        var now = DateTime.Now;
        var nextRun = DateTime.Today.AddDays(1).AddHours(2);
        return nextRun - now;
    }
}
```

## 📋 Практичні приклади використання

### 1. Обробка файлів
```csharp
public class FileProcessorService : BackgroundService
{
    private readonly ILogger<FileProcessorService> _logger;
    private readonly string _watchFolder;

    public FileProcessorService(
        ILogger<FileProcessorService> logger,
        IConfiguration configuration)
    {
        _logger = logger;
        _watchFolder = configuration["FileProcessor:WatchFolder"];
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var watcher = new FileSystemWatcher(_watchFolder);

        watcher.Created += async (sender, e) =>
        {
            await ProcessFile(e.FullPath);
        };

        watcher.EnableRaisingEvents = true;

        // Тримаємо сервіс активним
        await Task.Delay(Timeout.Infinite, stoppingToken);
    }

    private async Task ProcessFile(string filePath)
    {
        try
        {
            _logger.LogInformation($"Processing file: {filePath}");

            // Обробка файлу
            await Task.Delay(1000); // Симуляція обробки

            _logger.LogInformation($"File processed: {filePath}");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error processing file: {filePath}");
        }
    }
}
```

### 2. Очищення застарілих даних
```csharp
public class CleanupService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<CleanupService> _logger;

    public CleanupService(
        IServiceProvider serviceProvider,
        ILogger<CleanupService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await CleanupOldData();

            // Очищення кожні 6 годин
            await Task.Delay(TimeSpan.FromHours(6), stoppingToken);
        }
    }

    private async Task CleanupOldData()
    {
        using var scope = _serviceProvider.CreateScope();
        var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        try
        {
            var cutoffDate = DateTime.UtcNow.AddDays(-30);

            var oldLogs = await dbContext.Logs
                .Where(l => l.CreatedAt < cutoffDate)
                .ToListAsync();

            dbContext.Logs.RemoveRange(oldLogs);
            await dbContext.SaveChangesAsync();

            _logger.LogInformation($"Cleaned up {oldLogs.Count} old log entries");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during cleanup operation");
        }
    }
}
```

## ⚙️ Реєстрація Background Workers

### У Program.cs (ASP.NET Core 6+)
```csharp
var builder = WebApplication.CreateBuilder(args);

// Реєстрація Background Services
builder.Services.AddHostedService<EmailSenderService>();
builder.Services.AddHostedService<DataBackupService>();
builder.Services.AddHostedService<FileProcessorService>();
builder.Services.AddHostedService<CleanupService>();

var app = builder.Build();
```

### У Startup.cs (старіші версії)
```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddHostedService<EmailSenderService>();
    services.AddHostedService<DataBackupService>();
}
```

## 🎛️ Управління життєвим циклом

### Graceful Shutdown
```csharp
public class GracefulBackgroundService : BackgroundService
{
    private readonly ILogger<GracefulBackgroundService> _logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        try
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                await DoWork(stoppingToken);
                await Task.Delay(1000, stoppingToken);
            }
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("Service was cancelled gracefully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Service encountered an error");
        }
        finally
        {
            _logger.LogInformation("Service cleanup completed");
        }
    }

    private async Task DoWork(CancellationToken cancellationToken)
    {
        // Перевіряємо cancellation token регулярно
        cancellationToken.ThrowIfCancellationRequested();

        // Виконуємо роботу
        await Task.Delay(100, cancellationToken);
    }
}
```

## 🚨 Найкращі практики

### 1. ✅ Використання Scoped Services
```csharp
// ❌ Неправильно - DbContext є Scoped
public class BadService : BackgroundService
{
    private readonly AppDbContext _context; // Проблема!

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // DbContext може бути disposed
        var data = await _context.Users.ToListAsync();
    }
}

// ✅ Правильно - створюємо scope
public class GoodService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        var data = await context.Users.ToListAsync();
    }
}
```

### 2. ✅ Обробка помилок
```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    while (!stoppingToken.IsCancellationRequested)
    {
        try
        {
            await DoWork();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in background service");

            // Затримка перед повторною спробою
            await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
        }
    }
}
```

### 3. ✅ Моніторинг та логування
```csharp
public class MonitoredBackgroundService : BackgroundService
{
    private readonly ILogger<MonitoredBackgroundService> _logger;
    private readonly IMetrics _metrics;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var stopwatch = Stopwatch.StartNew();

            try
            {
                await ProcessItems();

                _metrics.Counter("background_service_success").Increment();
                _logger.LogInformation("Background task completed successfully");
            }
            catch (Exception ex)
            {
                _metrics.Counter("background_service_error").Increment();
                _logger.LogError(ex, "Background task failed");
            }
            finally
            {
                _metrics.Histogram("background_service_duration")
                    .Record(stopwatch.ElapsedMilliseconds);
            }

            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}
```

## 🔄 Альтернативи Background Workers

### 1. Hangfire
Для складних завдань з планувальником:
```csharp
// Встановлення: Install-Package Hangfire
BackgroundJob.Enqueue(() => SendEmail("user@example.com"));
BackgroundJob.Schedule(() => GenerateReport(), TimeSpan.FromHours(1));
RecurringJob.AddOrUpdate(() => CleanupOldFiles(), Cron.Daily);
```

### 2. Quartz.NET
Для enterprise-рівня планування:
```csharp
// Встановлення: Install-Package Quartz
services.AddQuartz(q =>
{
    q.UseMicrosoftDependencyInjection();
    q.UseSimpleTypeLoader();
    q.UseInMemoryStore();
});

services.AddQuartzHostedService(q => q.WaitForJobsToComplete = true);
```

### 3. Azure Service Bus / RabbitMQ
Для розподілених систем:
```csharp
// Аналогія: як поштова служба
// Background Worker = поштар, який розносить листи
public class MessageProcessorService : BackgroundService
{
    private readonly IServiceBusReceiver _receiver;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var message in _receiver.ReceiveMessagesAsync(stoppingToken))
        {
            await ProcessMessage(message);
        }
    }
}
```

## 📊 Порівняння підходів

| Підхід | Простота | Функціональність | Масштабованість | Коли використовувати |
|--------|----------|------------------|-----------------|---------------------|
| BackgroundService | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Прості циклічні завдання |
| IHostedService | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Контроль життєвого циклу |
| Hangfire | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Складне планування |
| Quartz.NET | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Enterprise планування |

## 🎯 Коли використовувати Background Workers

### ✅ Ідеальні сценарії:
- 📧 **Відправка email'ів** - як поштова служба
- 🗄️ **Обробка файлів** - як конвеєр на заводі
- 🧹 **Очищення даних** - як прибиральна служба
- 📊 **Генерація звітів** - як бухгалтерія в кінці дня
- 🔄 **Синхронізація з API** - як кур'єр між офісами

### ❌ Не підходить для:
- Завдань, які потребують негайного результату
- Інтерактивної взаємодії з користувачем
- Завдань, які залежать від HTTP-контексту

## 🛠️ Практичний приклад: Система нотифікацій

```csharp
// Аналогія: як диспетчер швидкої допомоги
public class NotificationDispatcherService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<NotificationDispatcherService> _logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await ProcessNotificationQueue();
            await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
        }
    }

    private async Task ProcessNotificationQueue()
    {
        using var scope = _serviceProvider.CreateScope();
        var notificationService = scope.ServiceProvider
            .GetRequiredService<INotificationService>();

        var pendingNotifications = await notificationService
            .GetPendingNotificationsAsync();

        foreach (var notification in pendingNotifications)
        {
            try
            {
                await SendNotification(notification);
                await notificationService.MarkAsSentAsync(notification.Id);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Failed to send notification {NotificationId}",
                    notification.Id);

                await notificationService.MarkAsFailedAsync(notification.Id);
            }
        }
    }

    private async Task SendNotification(Notification notification)
    {
        // Логіка відправки (email, SMS, push)
        switch (notification.Type)
        {
            case NotificationType.Email:
                await SendEmail(notification);
                break;
            case NotificationType.SMS:
                await SendSMS(notification);
                break;
            case NotificationType.Push:
                await SendPushNotification(notification);
                break;
        }
    }
}
```

## 🎯 Висновки

Background Workers - це потужний інструмент для автоматизації фонових процесів у вашому додатку. Як і працівники в реальному житті, вони:

- 🔄 **Працюють незалежно** - не блокують основні процеси
- ⏰ **Виконують роботу за розкладом** - регулярно або за потреби
- 🛡️ **Забезпечують надійність** - з правильною обробкою помилок
- 📊 **Підтримують моніторинг** - для контролю роботи

**Пам'ятайте**: як і прибиральники в ресторані працюють незалежно від клієнтів, Background Workers виконують свою роботу незалежно від веб-запитів, забезпечуючи стабільну роботу додатку.

### 🚀 Наступні кроки:
1. Визначте, які завдання у вашому додатку можна винести у фон
2. Оберіть підходящий тип Background Worker
3. Реалізуйте з правильною обробкою помилок
4. Додайте логування та моніторинг
5. Протестуйте graceful shutdown
```