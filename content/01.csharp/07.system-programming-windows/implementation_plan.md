# Системне Програмування C# (Windows) — `07.system-programming-windows`

Нова папка `07.system-programming-windows`. Модуль `06` ігнорується (буде видалений). 20 файлів, 5 блоків. Фокус: **багатопоточність** та **асинхронність** від А до Я.

---

## Блок A: Фундамент ОС (01–03)

---

### 📄 `01.how-os-works.md` — Як Працює Операційна Система

1. **Що таке ОС?**
   - Ядро (kernel), user mode vs kernel mode
   - Аналогія: ОС — менеджер ресторану (розподіляє столики, офіціантів, кухню)

2. **Що таке Процес?**
   - Визначення на рівні Windows
   - Ізоляція: власний адресний простір, handles, security context
   - PID, Virtual Address Space, Handle Table, PEB
   - Working Set, Private Bytes, Virtual Size
   - Аналогія: процес — "квартира" (ізольоване середовище)

3. **Що таке Потік (Thread)?**
   - Одиниця виконання всередині процесу
   - Власний стек (~1MB), регістри, instruction pointer
   - Спільний address space з іншими потоками процесу
   - Main Thread — entry point процесу
   - Аналогія: потоки — "мешканці квартири" (спільна кухня/ванна)

4. **Scheduling: Як ОС Розподіляє CPU**
   - Preemptive multitasking: time slicing
   - Context switch: що зберігається/відновлюється, ціна (~1-10μs)
   - Quantum (time slice) у Windows: ~15ms
   - Priority-based scheduling, round-robin для однакових пріоритетів

5. **CPU Cores vs Threads**
   - Фізичний паралелізм (multi-core) vs конкурентність (time-slicing)
   - Hyper-Threading / SMT
   - **Concurrency vs Parallelism** — ключова різниця з діаграмами
   - Закон Амдала (з формулою та прикладами)

6. **Process vs Thread vs Task: Зведена Таблиця**
   - Ресурси, ізоляція, вартість створення, use cases
   - Mermaid діаграма: Process → Threads → Shared Resources

---

### 📄 `02.processes-in-dotnet.md` — Процеси в .NET

1. **System.Diagnostics.Process: Повний API**
   - `Process.GetCurrentProcess()` — поточний процес
   - `Process.GetProcesses()`, `GetProcessesByName()`, `GetProcessById()`
   - Властивості: `Id`, `ProcessName`, `StartTime`, `WorkingSet64`, `Threads`, `Modules`
   - ⚡ Практика: утиліта "мій Task Manager" в консолі

2. **Task Manager та Performance Monitor**
   - Як читати CPU %, Memory, Handles, Threads columns
   - Моніторинг власного .NET додатку

3. **Запуск Зовнішніх Процесів**
   - `Process.Start()`, `ProcessStartInfo`
   - `FileName`, `Arguments`, `WorkingDirectory`
   - `UseShellExecute` vs direct execution
   - `Verb` (RunAs для адміністратора)
   - Приклад: відкрити блокнот, браузер, консольну програму

4. **Дочірні Процеси та Комунікація**
   - `RedirectStandardInput/Output/Error`
   - Синхронне та асинхронне читання stdout
   - `OutputDataReceived` event
   - `WaitForExit()`, `ExitCode`
   - ⚡ Практика: Запуск `ping` і парсинг результатів
   - ⚡ Практика: Запуск `dotnet build` з відображенням прогресу

5. **Завершення Процесів**
   - `Kill()`, `CloseMainWindow()` — graceful vs forceful
   - `HasExited`, `EnableRaisingEvents`, `Exited` event

6. **Міжпроцесна Комунікація (IPC)**
   - Named Pipes: `NamedPipeServerStream`, `NamedPipeClientStream`
   - Memory-Mapped Files: `MemoryMappedFile`
   - ⚡ Практика: два .NET процеси обмінюються даними через Named Pipe

7. **Практичні Завдання**
   - Рівень 1: Console Process Explorer
   - Рівень 2: Batch Launcher з моніторингом
   - Рівень 3: IPC Chat між двома процесами

---

### 📄 `03.appdomains-assemblies.md` — Application Domains та Збірки

1. **AppDomain: Історія та Сучасність**
   - .NET Framework: логічна ізоляція, плагіни, sandbox
   - .NET Core/.NET 5+: один AppDomain на процес

2. **AssemblyLoadContext (Сучасна Альтернатива)**
   - `AssemblyLoadContext.Default`
   - Власний `AssemblyLoadContext`, collectible contexts
   - Завантаження/вивантаження збірок у runtime
   - ⚡ Практика: плагін-система — завантаження DLL у runtime

3. **Збірки (Assemblies)**
   - Strong naming, версіонування, Assembly metadata
   - Deps file, runtime config

4. **Практичні Завдання**
   - Рівень 1: Assembly Inspector
   - Рівень 2: Hot-Reload Plugin System

---

## Блок B: Багатопоточність — ВСЕ від А до Я (04–11)

---

### 📄 `04.thread-fundamentals.md` — Потоки: Основи

1. **Проблема: Чому Потрібна Багатопотоковість?**
   - Frozen UI — класичний приклад
   - Benchmark: послідовна vs паралельна обробка
   - Еволюція: від single-core до multi-core (timeline діаграма)

2. **Клас Thread: Фундаментальний API**
   - `ThreadStart` — делегат без параметрів
   - `ParameterizedThreadStart` — передача `object?`
   - Lambda expressions (рекомендовано) + **closure pitfall** (`int i` в циклі!)
   - `thread.Start()`, `new Thread()` — створення vs запуск

3. **Отримання Результатів з Потоку**
   - Shared variable (з Join)
   - Object instance container
   - `Task<T>` (preview: буде детально в темі 11)

4. **Background vs Foreground Threads**
   - Вплив на завершення процесу (таблиця + sequence diagram)
   - `IsBackground = true`
   - Коли що використовувати

5. **Життєвий Цикл Потоку**
   - `ThreadState` flags enum: Unstarted → Running → WaitSleepJoin → Stopped
   - Діаграма переходів (stateDiagram-v2)
   - Deprecated: `Suspend`, `Resume`, `Abort` → чому CancellationToken

6. **Thread Priorities**
   - `ThreadPriority` enum: Lowest → Highest
   - Preemptive scheduling, round-robin
   - Priority Inversion (Mars Pathfinder 1997!)
   - Best practices: залишайте Normal для 99% випадків

7. **Ключові Методи**
   - `Thread.Sleep(ms)` — призупинення; `Sleep(0)` vs `Yield()`
   - `Thread.Join()` — очікування з timeout
   - `Thread.CurrentThread` — поточний потік
   - Naming threads: `thread.Name` — для debugging

8. **Практичні Завдання**
   - Рівень 1: Parallel Countdown
   - Рівень 2: Multi-threaded File Downloader
   - Рівень 3: Thread Pool (ручна реалізація)

---

### 📄 `05.shared-state-problems.md` — Проблеми Спільного Стану ⚠️

> **КЛЮЧОВА ТЕМА**. Без розуміння проблем — синхронізація не має сенсу.

1. **Race Condition**
   - Визначення: результат залежить від порядку виконання потоків
   - Приклад: банківський рахунок — два потоки знімають одночасно
   - Check-then-act pattern — чому він небезпечний
   - ⚡ Демонстрація з кодом + Mermaid sequence diagram

2. **Data Race**
   - Визначення: одночасний доступ до пам'яті, де хоча б один — запис
   - Різниця з Race Condition (можна мати одне без іншого)
   - `i++` — **НЕ атомарна** операція! (Read → Modify → Write)
   - ⚡ Демонстрація: 10 потоків інкрементують лічильник → результат < очікуваного

3. **Visibility Problem (Проблема Видимості)**
   - CPU cache hierarchy: L1/L2/L3 cache, store buffers
   - Потік A записує значення, потік B його НЕ бачить
   - Memory reordering: компілятор та CPU переставляють інструкції
   - ⚡ Демонстрація: boolean flag не видно іншому потоку

4. **Torn Reads**
   - Часткове зчитування 64-bit значень на 32-bit системах
   - `long`/`double` — не atomic на x86-32

5. **Lost Update**
   - Read-Modify-Write без захисту
   - Відмінність від Race Condition

6. **Memory Model .NET**
   - Happens-before relationship (концепція)
   - Acquire/Release semantics (що це означає)
   - Чому "просто volatile" — не завжди достатньо

7. **Таксономія Проблем: Зведена Таблиця**
   - Проблема → Причина → Наслідок → Рішення (посилання на теми 06–08)

8. **Висновок: Навіщо Синхронізація**
   - Кожна проблема має рішення → наступні три теми

---

### 📄 `06.synchronization-fundamentals.md` — Синхронізація: Основи

1. **Critical Section — Концепція**
   - Mutual exclusion: тільки один потік одночасно
   - Аналогія: одномісна вбиральня з замком

2. **`lock` Statement**
   - Синтаксис, правила вибору lock object (таблиця: ✅ vs ❌)
   - `private readonly object _lock = new()` — золотий стандарт
   - ❌ `lock(this)`, ❌ `lock("string")`, ❌ `lock(typeof(...))`

3. **Під Капотом: lock → Monitor**
   - Компілятор генерує `Monitor.Enter/Exit` + `try/finally`
   - Чому `try/finally` — гарантія звільнення при exceptions

4. **Monitor Class: Повний Контроль**
   - `Monitor.TryEnter(timeout)` — неблокуюча спроба
   - `Monitor.Wait()` / `Monitor.Pulse()` / `Monitor.PulseAll()` — signaling
   - ⚡ Практика: BlockingQueue через Wait/Pulse (з sequence diagram)
   - Правило: `while` замість `if` перед `Wait()` (spurious wakeup)

5. **`System.Threading.Lock` (C# 13/.NET 9)**
   - Новий тип, оптимізований для сучасних CPU
   - `Lock.EnterScope()` — ref struct з using
   - Порівняння з old `object` lock (таблиця)

6. **Deadlock: Взаємне Блокування**
   - 4 умови Coffman: mutual exclusion, hold-and-wait, no preemption, circular wait
   - ⚡ Приклад: два потоки, два locks, circular wait
   - **Запобігання**: Lock ordering, timeout (`Monitor.TryEnter`), lock hierarchy
   - Dining Philosophers Problem
   - Deadlock detection в production

7. **Livelock та Starvation**
   - Livelock: потоки активні, але не прогресують (аналогія: двоє в коридорі)
   - Starvation: потік ніколи не отримує lock

8. **Практичні Завдання**
   - Рівень 1: Thread-safe counter + bank account
   - Рівень 2: Producer-Consumer з Monitor.Wait/Pulse
   - Рівень 3: Deadlock simulator + resolver

---

### 📄 `07.synchronization-advanced.md` — Синхронізація: Kernel-Level та Advanced

1. **Mutex: Cross-Process Synchronization**
   - Local Mutex (in-process) vs Named Mutex (system-wide)
   - `WaitOne()`, `ReleaseMutex()`, `AbandonedMutexException`
   - ⚡ Практика: Single-instance application
   - Порівняння з lock/Monitor (таблиця: scope, performance, ownership)

2. **Semaphore та SemaphoreSlim**
   - Обмежена кількість одночасних потоків (аналогія: парковка)
   - `SemaphoreSlim(initialCount, maxCount)`
   - `WaitAsync()` — async support (preview: деталі в темі 16)
   - ⚡ Практика: Connection Pool, Rate Limiter

3. **AutoResetEvent та ManualResetEvent(Slim)**
   - Signaling між потоками
   - Auto: турнікет (один пройшов — закрився)
   - Manual: ворота (відкрились — всі проходять)
   - `Set()`, `Reset()`, `WaitOne()` / `Wait()`
   - ⚡ Практика: Producer-Consumer з signaling

4. **CountdownEvent**
   - Координація завершення N операцій
   - `Signal()`, `Wait()`, `AddCount()`
   - ⚡ Практика: Parallel initialization (чекаємо 5 сервісів)

5. **Barrier**
   - Синхронізація фаз паралельних потоків
   - `SignalAndWait()`, post-phase callback
   - ⚡ Практика: Multi-phase data pipeline

6. **ReaderWriterLockSlim**
   - Read/Write access pattern: множинні readers АБО один writer
   - `EnterReadLock()`, `EnterWriteLock()`, `EnterUpgradeableReadLock()`
   - `LockRecursionPolicy`
   - ⚡ Практика: Thread-safe cache

7. **Зведена Таблиця: Коли Що Використовувати**
   - Примітив → Scope → Async Support → Use Case

8. **Практичні Завдання**
   - Рівень 1: Thread-safe LRU Cache з ReaderWriterLockSlim
   - Рівень 2: Parallel Pipeline з Barrier
   - Рівень 3: Worker coordination з CountdownEvent + Semaphore

---

### 📄 `08.interlocked-volatile-lockfree.md` — Atomic Operations та Lock-Free

1. **`Interlocked` Class: Атомарні Операції**
   - `Increment`, `Decrement`, `Add`
   - `Exchange` — atomic swap
   - `CompareExchange` — CAS (Compare-And-Swap): фундамент lock-free
   - `Read` — atomic read для 64-bit на 32-bit

2. **CAS (Compare-And-Swap) Pattern**
   - Як працює CAS під капотом (CPU instruction `CMPXCHG`)
   - CAS loop: retry pattern
   - ⚡ Практика: Lock-free counter через CAS

3. **`volatile` Keyword**
   - Що гарантує: заборона кешування та reordering для цієї змінної
   - Чого **НЕ** гарантує: не дає atomicity для `i++`
   - Коли використовувати: boolean flags, simple read/write
   - ❌ Поширена помилка: `volatile int counter; counter++` — це НЕ thread-safe!

4. **`Thread.MemoryBarrier()`**
   - Full fence: запобігає reordering з обох сторін
   - Коли потрібен (рідко в прикладному коді)

5. **SpinLock та SpinWait**
   - User-mode spinning vs kernel transition
   - `SpinLock.Enter()`, `SpinLock.Exit()` — для дуже коротких critical sections
   - `SpinWait.SpinOnce()`, `SpinWait.SpinUntil()` — adaptive spinning
   - Коли spinning краще за lock, коли гірше

6. **Lock-Free Data Structures**
   - ⚡ Практика: Lock-free Stack через CAS + `Interlocked.CompareExchange`
   - ABA Problem — що це, як вирішувати

7. **Практичні Завдання**
   - Рівень 1: Atomic counter benchmarks
   - Рівень 2: Lock-free queue (single-producer, single-consumer)
   - Рівень 3: Compare: lock vs Interlocked vs SpinLock benchmarks

---

### 📄 `09.thread-pool.md` — ThreadPool

1. **Чому Створювати Thread — Дорого?**
   - Overhead: ~1MB стеку, kernel object, context switch cost
   - Benchmark: `new Thread()` vs `ThreadPool.QueueUserWorkItem()`
   - Аналогія: таксі (Thread) vs автобус (ThreadPool)

2. **Архітектура ThreadPool**
   - Worker threads та I/O completion port (IOCP) threads
   - Hill Climbing Algorithm: динамічне додавання/видалення потоків
   - `ThreadPool.SetMinThreads()`, `SetMaxThreads()`
   - `ThreadPool.ThreadCount`, `PendingWorkItemCount`

3. **Використання ThreadPool**
   - `ThreadPool.QueueUserWorkItem(callback)` — без стану
   - `ThreadPool.QueueUserWorkItem(callback, state, preferLocal)` — зі станом
   - `ThreadPool.UnsafeQueueUserWorkItem` — без ExecutionContext flow
   - ⚡ Практика: паралельна обробка колекції

4. **RegisteredWaitHandle**
   - `ThreadPool.RegisterWaitForSingleObject()` — ефективне очікування

5. **ExecutionContext та SynchronizationContext**
   - Що передається між потоками, навіщо
   - SynchronizationContext — введення (деталі → тема 13)

6. **Проблеми ThreadPool**
   - Thread starvation: коли всі потоки зайняті блокуючими операціями
   - Антипатерн: `Thread.Sleep()` в ThreadPool
   - Long-running tasks — коли ThreadPool не підходить
   - Діагностика: ETW, `PendingWorkItemCount`

7. **Практичні Завдання**
   - Рівень 1: Parallel File Scanner
   - Рівень 2: Connection Pool
   - Рівень 3: Thread starvation detector

---

### 📄 `10.concurrent-collections.md` — Concurrent та Immutable Collections

1. **Чому Звичайні Колекції Не Thread-Safe?**
   - `List<T>` + два потоки = corruption
   - `Dictionary<K,V>` + конкурентний доступ = exception

2. **ConcurrentDictionary<TKey, TValue>**
   - `GetOrAdd`, `AddOrUpdate`, `TryAdd`, `TryRemove`, `TryUpdate`
   - Під капотом: striped locking (не один lock на всю колекцію)
   - ⚡ Практика: Thread-safe word counter

3. **ConcurrentQueue<T>, ConcurrentStack<T>, ConcurrentBag<T>**
   - Lock-free implementations
   - `TryDequeue`, `TryPop`, `TryTake`
   - ConcurrentBag: thread-local storage optimization

4. **BlockingCollection<T>**
   - Bounded producer/consumer
   - `Add()` (blocks if full), `Take()` (blocks if empty)
   - `CompleteAdding()`, `GetConsumingEnumerable()`
   - ⚡ Практика: Multi-producer, multi-consumer pipeline

5. **Immutable Collections**
   - `ImmutableList<T>`, `ImmutableDictionary<K,V>`, `ImmutableStack<T>`
   - Builder pattern: `ImmutableList.CreateBuilder<T>()`
   - Thread safety через immutability (ніхто не змінює → не потрібен lock)
   - Коли Immutable краще за Concurrent (таблиця)

6. **Практичні Завдання**
   - Рівень 1: Thread-safe URL cache
   - Рівень 2: Log aggregator з BlockingCollection
   - Рівень 3: Concurrent web crawler з ConcurrentDictionary (visited URLs)

---

### 📄 `11.tpl-parallel-plinq.md` — TPL, Parallel та PLINQ

1. **Від Thread до Task: Еволюція**
   - Task як абстракція "одиниці роботи"
   - Task vs Thread (таблиця: результат, exceptions, cancellation, pooling)

2. **Task та Task<T>**
   - `Task.Run()` (рекомендовано), `Task.Factory.StartNew()` (`LongRunning`, `DenyChildAttach`)
   - Cold vs Hot tasks, `new Task()` + `Start()` — чому не рекомендується
   - `TaskStatus` enum, lifecycle діаграма
   - `.Result`, `.GetAwaiter().GetResult()` — блокуюче очікування

3. **Composing Tasks**
   - `Task.WhenAll()`, `Task.WhenAny()`, `Task.WhenEach()` (.NET 9)
   - `Task.Delay()`, `Task.FromResult()`, `Task.CompletedTask`
   - `ContinueWith` (legacy) — проблеми з SynchronizationContext

4. **CancellationToken**
   - `CancellationTokenSource`, `CancellationToken`
   - `ThrowIfCancellationRequested()`, `IsCancellationRequested`
   - `token.Register(callback)`, linked tokens, timeout
   - ⚡ Практика: Download з progress + cancellation

5. **Exception Handling**
   - `AggregateException`, `Flatten()`, `Handle()`
   - Unobserved: `TaskScheduler.UnobservedTaskException`
   - ⚡ Практика: error handling з WhenAll

6. **Parallel Class: Data Parallelism**
   - `Parallel.For()`, `Parallel.ForEach()`, `Parallel.Invoke()`
   - `ParallelOptions`: `MaxDegreeOfParallelism`, `CancellationToken`
   - Thread-local state, `Break()` vs `Stop()`
   - `Parallel.ForEachAsync()` (.NET 6+)
   - ⚡ Практика: Parallel image processing

7. **PLINQ**
   - `AsParallel()`, `AsOrdered()`, `WithDegreeOfParallelism(N)`
   - `WithCancellation()`, `WithExecutionMode()`, `WithMergeOptions()`
   - `ForAll()`, `Aggregate()`, partitioning strategies
   - Коли НЕ використовувати (Amdahl's Law, overhead)

8. **Практичні Завдання**
   - Рівень 1: Parallel File Processor + CancellationToken
   - Рівень 2: Monte Carlo π calculation з Parallel + PLINQ
   - Рівень 3: MapReduce з WhenAll

---

## Блок C: Асинхронність — ВСЕ від А до Я (12–16)

---

### 📄 `12.async-fundamentals.md` — Async/Await: Фундамент

1. **Проблема: Чому Async?**
   - I/O-bound vs CPU-bound (аналогія: офіціант vs кухар)
   - Blocking I/O: потік чекає відповідь мережі → thread starvation
   - Non-blocking I/O: потік вільний поки чекаємо
   - C10K problem, масштабування

2. **Історія: APM → EAP → TAP**
   - `BeginRead/EndRead` (legacy), `BackgroundWorker` (legacy)
   - TAP — сучасний стандарт, чому переміг

3. **`async` та `await`: Синтаксис**
   - `async` — що робить (і чого НЕ: не робить метод паралельним!)
   - `await` — точка "призупинення" та повернення потоку
   - Return types: `Task`, `Task<T>`, `ValueTask`, `ValueTask<T>`, `void`
   - Naming convention: `Async` суфікс
   - ⚡ Приклад: async file read, async HTTP GET

4. **State Machine Під Капотом**
   - Що компілятор генерує з async/await
   - `IAsyncStateMachine` interface
   - Кожен `await` — точка зупинки (стан автомата)
   - Розбір згенерованого коду (SharpLab/ILSpy)
   - ⚡ Практика: порівняння sync vs async в SharpLab

5. **Exception Handling в Async**
   - `await` автоматично unwrap `AggregateException`
   - Exceptions у `Task.WhenAll` — перший + `.Exception`
   - ❌ `async void` — exceptions "втрачаються"!!

6. **Практичні Завдання**
   - Рівень 1: Async File Copier з progress reporting
   - Рівень 2: Concurrent API Caller (WhenAll + WhenAny)
   - Рівень 3: Async pipeline з error recovery

---

### 📄 `13.async-context-configureawait.md` — SynchronizationContext та ConfigureAwait

1. **SynchronizationContext**
   - Що це: абстракція для контексту виконання (UI thread, ASP.NET)
   - UI SynchronizationContext: WPF, WinForms
   - `SynchronizationContext.Current`, `Post()`, `Send()`

2. **ConfigureAwait(false)**
   - Default: continuation повертається на captured context
   - `ConfigureAwait(false)`: продовжити на будь-якому потоці
   - Правило: завжди `ConfigureAwait(false)` в бібліотечному коді
   - `ConfigureAwait(true)` у UI-коді

3. **Deadlock Scenario ⚠️**
   - UI thread + `.Result` → deadlock (повний розбір із діаграмою)
   - ASP.NET (old) + `.Result` → deadlock
   - Як уникнути: ніколи `.Result`/`.Wait()` в sync context

4. **ExecutionContext**
   - Що передається: SecurityContext, логічний call context
   - `AsyncLocal<T>` — "thread-local" для async (передається через await)
   - ⚡ Практика: Correlation ID через AsyncLocal

5. **Практичні Завдання**
   - Рівень 1: Deadlock demo + fix
   - Рівень 2: AsyncLocal-based RequestContext
   - Рівень 3: Custom SynchronizationContext

---

### 📄 `14.async-advanced.md` — Async: Просунуті Паттерни

1. **TaskCompletionSource<T>**
   - Перетворення callback-based API на async
   - Перетворення event-based API на async
   - ⚡ Практика: wrap FileSystemWatcher → Task

2. **IAsyncEnumerable<T>: Async Streams**
   - `yield return` в async контексті
   - `await foreach` + `WithCancellation()`
   - `[EnumeratorCancellation]` attribute
   - ⚡ Практика: streaming data з paginated API

3. **IAsyncDisposable та `await using`**
   - Коли потрібен async Dispose (DB connections, streams)

4. **ValueTask та ValueTask<T>**
   - Struct-based, no heap allocation для sync completion
   - Коли використовувати vs Task
   - ⚠️ Обмеження: не await двічі, не `.Result` до completion

5. **Best Practices (Повний Список)**
   - ❌ `async void` — тільки для event handlers
   - ❌ `.Result`/`.Wait()` — deadlock
   - ❌ `Task.Run()` в ASP.NET (fake async)
   - ✅ `ConfigureAwait(false)` в бібліотеках
   - ✅ CancellationToken скрізь
   - ✅ Prefer `ValueTask` для hot paths

6. **Common Pitfalls**
   - Sync-over-async (`.Result` / `.GetAwaiter().GetResult()`)
   - Fire-and-forget правильно: `_ = DoWorkAsync()`
   - `Lazy<Task<T>>` — lazy async init
   - Retry pattern з async

7. **Custom Awaitables (Для Допитливих)**
   - `GetAwaiter()` pattern, `ICriticalNotifyCompletion`

8. **Практичні Завдання**
   - Рівень 1: TaskCompletionSource wrapper для timer
   - Рівень 2: Async Producer-Consumer з IAsyncEnumerable
   - Рівень 3: Custom AsyncLock

---

### 📄 `15.channels.md` — System.Threading.Channels

1. **Producer-Consumer: Мотивація**
   - Чому `BlockingCollection` не підходить для async (блокує потоки)
   - Channels = async-native producer/consumer

2. **Channel<T> API**
   - `Channel.CreateBounded<T>(capacity)`, `CreateUnbounded<T>()`
   - `ChannelWriter<T>`: `WriteAsync`, `TryWrite`, `Complete`
   - `ChannelReader<T>`: `ReadAsync`, `ReadAllAsync`, `WaitToReadAsync`
   - ⚡ Практика: Log processing pipeline

3. **BoundedChannelOptions**
   - `BoundedChannelFullMode`: Wait, DropNewest, DropOldest, DropWrite
   - `SingleReader`, `SingleWriter` — performance optimizations

4. **Multi-stage Pipelines**
   - Побудова pipeline: Channel₁ → Transform → Channel₂ → Load
   - ⚡ Практика: ETL Pipeline (Extract → Transform → Load)

5. **BackgroundService + Channel**
   - Queue-based async processing
   - ⚡ Практика: Email sending queue

6. **Benchmarks**: Channel vs `BlockingCollection` vs `ConcurrentQueue` + SemaphoreSlim

7. **Практичні Завдання**
   - Рівень 1: Chat Server
   - Рівень 2: Image Processing Pipeline
   - Рівень 3: Rate-limited API Client

---

### 📄 `16.async-synchronization.md` — Асинхронна Синхронізація

1. **Чому `lock` Не Можна з `await`**
   - Compiler error: cannot `await` inside `lock`
   - Причина: lock = thread-affine, async = thread-agnostic

2. **SemaphoreSlim.WaitAsync() — Async Lock**
   - `new SemaphoreSlim(1, 1)` = async-compatible mutex
   - Pattern: `await semaphore.WaitAsync()` + `try/finally { Release() }`
   - ⚡ Практика: Async-safe resource access

3. **Throttling та Rate Limiting**
   - SemaphoreSlim(N) для обмеження concurrent async operations
   - ⚡ Практика: Max 5 concurrent HTTP requests

4. **Timeout + Cancellation Patterns**
   - `Task.WhenAny(task, Task.Delay(timeout))` — manual timeout
   - `CancellationTokenSource.CancelAfter()` — auto timeout
   - Linked cancellation tokens для ієрархії

5. **Nito.AsyncEx (Бібліотека)**
   - `AsyncLock`, `AsyncAutoResetEvent`, `AsyncManualResetEvent`
   - `AsyncCollection<T>`, `AsyncLazy<T>`

6. **Практичні Завдання**
   - Рівень 1: Async Mutex для file access
   - Рівень 2: Throttled web scraper
   - Рівень 3: Resilient service з timeout, retry, circuit breaker

---

## Блок D: Unsafe Code (17)

### 📄 `17.unsafe-code.md` — Unsafe Code та Вказівники
- `unsafe` контекст, `AllowUnsafeBlocks`
- Вказівники: `int*`, `byte*`, `void*`, операції `&`, `*`, `->`
- Pointer arithmetic, `fixed` statement (pinning)
- `stackalloc` + `Span<T>`, `sizeof`, `Marshal.SizeOf`
- Function pointers (`delegate*`, C# 9+)
- Практика: Fast Array Copy, Image Pixel Manipulation

---

## Блок E: Windows API (18–20)

### 📄 `18.pinvoke-winapi.md` — P/Invoke та Windows API
- Win32 API: kernel32, user32, advapi32; Handles, HWND
- `[DllImport]` vs `[LibraryImport]` (.NET 7+)
- Marshalling: strings, structs, callbacks, `SafeHandle`, `Marshal` class
- Практика: MessageBox, GetSystemInfo, EnumWindows, Window automation

### 📄 `19.windows-registry.md` — Реєстр Windows
- Архітектура: Hives, Keys, Values; `regedit`
- `Microsoft.Win32.Registry` API: read/write/delete/monitor
- Автозапуск, файлові асоціації, WOW64, P/Invoke `RegNotifyChangeKeyValue`

### 📄 `20.windows-hooks-services.md` — Hooks, Hotkeys та Services
- Hooks: `SetWindowsHookEx`, `WH_KEYBOARD_LL`, `WH_MOUSE_LL`
- Hotkeys: `RegisterHotKey/UnregisterHotKey`, message loop
- Windows Services: `BackgroundService`, `sc.exe`, Event Log
- Tray Apps: `NotifyIcon`, context menu

---

## Підсумок: 20 Файлів

| # | Файл | Блок | Залежить від |
|:--|:-----|:-----|:-------------|
| 01 | How OS Works | A | — |
| 02 | Processes in .NET | A | 01 |
| 03 | AppDomains & Assemblies | A | 02 |
| 04 | Thread Fundamentals | B | 01 |
| 05 | **Shared State Problems** ⚠️ | B | 04 |
| 06 | Synchronization Fundamentals | B | 05 |
| 07 | Synchronization Advanced | B | 06 |
| 08 | Interlocked, Volatile, Lock-Free | B | 05 |
| 09 | ThreadPool | B | 04, 06 |
| 10 | Concurrent Collections | B | 06, 08 |
| 11 | TPL, Parallel, PLINQ | B | 09 |
| 12 | Async Fundamentals | C | 11 |
| 13 | SyncContext & ConfigureAwait | C | 12 |
| 14 | Async Advanced Patterns | C | 12 |
| 15 | Channels | C | 12, 14 |
| 16 | Async Synchronization | C | 07, 12 |
| 17 | Unsafe Code | D | 01 |
| 18 | P/Invoke & WinAPI | E | 17 |
| 19 | Windows Registry | E | 18 |
| 20 | Windows Hooks & Services | E | 18, 12 |
