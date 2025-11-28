# C# & .NET: The Ultimate Roadmap

Цей план є детальним путівником по екосистемі C#. Він побудований за принципом **Stack-Centric** ("Від Ядра до Сфер") і розбитий на атомарні теми для послідовного вивчення.

## 1. The Platform & Fundamentals (Платформа та Основи)

_Мета: Розібратися з інструментами та базовим синтаксисом._

### 1.1. Introduction to Ecosystem

-   Що таке .NET (History, .NET Framework vs .NET Core vs .NET 5+).
-   **Modern .NET**: .NET 8/9/10 Features overview.
-   Архітектура CLR (Common Language Runtime).
-   IL (Intermediate Language) та JIT (Just-In-Time) компіляція (Tiered Compilation, PGO, **RyuJIT details: Loop Unrolling, Inlining, Vectorization (SIMD)**).
-   CTS (Common Type System) та CLS (Common Language Specification).
-   Налаштування середовища (Visual Studio, Rider, VS Code + C# Dev Kit).
-   .NET CLI: Основні команди (`new`, `build`, `run`, `watch`, `publish`).

### 1.2. Program Structure

-   Structure of a C# Program (Namespaces, Classes, Main).
-   Top-level statements (Програми верхнього рівня).
-   Коментарі та XML-документація.

### 1.3. Variables & Data Types

-   Змінні та Константи (`const` vs `readonly`).
-   Вбудовані типи даних (Built-in types).
-   Literals (Integer, Real, Boolean, Character, String, Raw String Literals).
-   Type Conversion (Implicit, Explicit, `Convert`, `Parse`, `TryParse`).
-   Value Types vs Reference Types (Stack vs Heap intro).
-   `var` (Implicit typing).
-   **Nullable Reference Types (NRT)**: `string?` vs `string`, null-forgiving operator `!`, NRT warnings.
-   **Bitwise Operations**: Bit manipulation (`<<`, `>>`, `|`, `&`, `^`), flags enums.

### 1.4. Strings & Text Handling

-   **String Basics**: Immutability concept (чому рядки незмінні).
-   **Literals**: Verbatim strings (`@""`), Raw string literals (`"""..."""`).
-   **Operations**: Concatenation, Split, Join, Replace, Substring.
-   **Interpolation**: `$"Name: {name}"` та formatting (`{date:yyyy-MM-dd}`).
-   **StringBuilder**: Ефективна побудова рядків у циклах (must have for performance).
-   **Regex Basics**: Клас `Regex`, прості патерни (email, phone validation).

### 1.5. Dates & Time

-   **Core Types**: `DateTime` vs `DateTimeOffset` (чому Offset важливий для вебу).
-   **Modern Types**: `DateOnly` & `TimeOnly` (починаючи з .NET 6).
-   **TimeSpan**: Робота з інтервалами часу (різниця дат).
-   **Operations**: Parsing (`DateTime.Parse`), Formatting (`ToString`), Arithmetic (`AddDays`).
-   **TimeZones**: `TimeZoneInfo`, UTC vs Local time best practices.

### 1.6. Control Flow

-   Conditional Statements (`if`, `else`, `switch`, Ternary operator).
-   Loops (`for`, `foreach`, `while`, `do-while`).
-   Jump Statements (`break`, `continue`, `return`).
-   Pattern Matching у `switch` expressions.

### 1.7. Methods

-   Оголошення та виклик методів.
-   Parameter modifiers (`ref`, `out`, `in`).
-   Overloading, Local functions, Recursion.

### 1.8. Debugging Basics

-   **Breakpoints**: Setting, disabling, and removing breakpoints in code.
-   **Locals Window**: Inspecting variable values during execution.
-   **Call Stack**: Understanding execution flow and method call hierarchy.
-   **Conditional Breakpoints**: Triggering breaks based on conditions (saves hours of debugging).
-   **Step Through Code**: Step Into, Step Over, Step Out navigation.
-   **Watch Window**: Monitoring specific variables and expressions.
-   **Immediate Window**: Executing code and evaluating expressions on-the-fly.

### 1.9. Interactive Console (Classic)

-   **System.Console API**: `Write` vs `WriteLine`, `ReadLine` vs `ReadKey`.
-   **Console Customization**: Background/Foreground Colors, Title, Beep.
-   **Cursor Control**: `SetCursorPosition`, `GetCursorPosition`, `CursorVisible` (створення простого меню).
-   **Buffers & Windows**: Розуміння різниці між BufferSize та WindowSize.
-   **Stream Redirection**: Що таке StandardInput, StandardOutput, StandardError (pipes).

## 2. The Core: OOP (Об'єктно-Орієнтоване Програмування)

_Мета: Опанувати парадигму ООП та систему типів._

### 2.1. Package Management

-   **NuGet Basics**: What is NuGet, package repositories, versioning.
-   **Package Sources**: Official NuGet.org, private feeds, GitHub Packages.
-   **Package Installation**: `dotnet add package`, Package Manager UI, `packages.json`.
-   **Dependency Management**: Transitive dependencies, version conflicts, `PackageReference`.
-   **Package Updates**: Checking for updates, compatibility, breaking changes.
-   **Private Packages**: Creating and publishing custom packages.
-   **Global Tools**: Installing .NET CLI tools globally (`dotnet tool install`).

### 2.2. Classes & Objects

-   Class Definition & Object Instantiation.
-   Constructors (Instance, Static, Private, **Primary Constructors**).
-   Object Initializers.
-   Deconstructors.
-   `this` keyword.
-   Static Members (Fields, Methods, Classes).
-   Access Modifiers (`public`, `private`, `protected`, `internal`, `file`).

### 2.3. Properties & Fields

-   Fields vs Properties.
-   Auto-implemented properties.
-   Read-only properties & `init` accessors.
-   **Field keyword** (C# 13/14 preview) - semi-auto properties.
-   Indexers (Індексатори).

### 2.4. OOP Pillars

-   **Encapsulation**: Приховування даних.
-   **Inheritance**: `base` keyword, Constructors in inheritance.
-   **Polymorphism**:
    -   Virtual methods (`virtual`, `override`).
    -   Method Hiding (`new`).
    -   Sealed classes & methods.
-   **Abstraction**: Abstract classes vs Interfaces.

### 2.5. Advanced Types

-   **Structs**: Коли використовувати, відмінності від класів, `ref struct`.
-   **Enums**: Flags attribute, underlying types.
-   **Records**: Positional records, `with` expressions, Value equality.
-   **Tuples**: `ValueTuple`, Deconstruction.
-   **Anonymous Types**.
-   **Nullable Types**: Value types (`int?`) vs Reference types (`string?`), Null-coalescing operators (`??`, `??=`, `?.`).
-   **Discriminated Unions** (Concept/Future C#).

### 2.6. Namespaces

-   Namespace declaration (Block-scoped vs File-scoped).
-   `using` directive, `static using`, `global using`.
-   Alias directive.

## 3. The Advanced Core (Глибина Мови)

_Мета: Вивчити потужні механізми для гнучкого коду._

### 3.1. Generics (Узагальнення)

-   Generic Classes & Methods.
-   Constraints (`where`, `allows ref struct` in C# 13).
-   Covariance & Contravariance (`out`, `in`).
-   Generic Interfaces & Delegates.

### 3.2. Delegates, Events & Lambdas

-   Delegates definition & instantiation.
-   Multicast Delegates.
-   Built-in Delegates: `Action`, `Func`, `Predicate`.
-   Anonymous Methods.
-   **Lambda Expressions**: Syntax, Closures (Замикання), Attributes on lambdas.
-   **Events**: Publisher-Subscriber pattern, `event` keyword, Standard event pattern.

### 3.3. Interfaces Deep Dive

-   Explicit Interface Implementation.
-   Default Interface Methods.
-   Interface Inheritance.
-   Static Abstract Members in Interfaces.

### 3.4. Exception Handling

-   `try`, `catch`, `finally`.
-   Exception Filters (`when`).
-   Throwing exceptions (`throw`, `throw` expression).
-   Custom Exceptions.
-   Best Practices (Fail fast, don't swallow exceptions).

### 3.5. Pattern Matching

-   Type Pattern.
-   Property Pattern.
-   Tuple Pattern.
-   Positional Pattern.
-   Relational & Logical Patterns.
-   List Patterns.

### 3.6. Additional Features

-   Operator Overloading.
-   **Extension Methods** & **Extensions** (C# 14 Roles/Extensions v2 concept).
-   Partial Classes, Methods, Properties (C# 13).
-   Interceptors (Advanced/Compiler feature).
-   **Source Generators**: Roslyn API, `IIncrementalGenerator`, compile-time code generation.

## 4. Architecture & Best Practices (Архітектура та Кращі Практики)

_Мета: Писати код, який легко підтримувати._

### 4.1. Software Design Principles

-   **SOLID Principles** (Deep dive):
    -   **S**ingle Responsibility Principle (SRP).
    -   **O**pen/Closed Principle (OCP).
    -   **L**iskov Substitution Principle (LSP).
    -   **I**nterface Segregation Principle (ISP).
    -   **D**ependency Inversion Principle (DIP).
-   **Other Principles**: DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid), YAGNI (You Aren't Gonna Need It).
-   **Law of Demeter**: Tell-Don't-Ask principle, object coupling.

### 4.2. Design Patterns (GoF)

-   **Creational Patterns**:
    -   **Singleton**: Ensures a class has only one instance.
    -   **Builder**: Constructs complex objects step by step.
    -   **Factory Method**: Creates objects without specifying the exact class.
    -   **Abstract Factory**: Creates families of related objects.
    -   **Prototype**: Clones existing instances.
-   **Structural Patterns**:
    -   **Adapter**: Allows incompatible interfaces to work together.
    -   **Decorator**: Adds behavior to objects dynamically.
    -   **Facade**: Provides a unified interface to a set of interfaces.
    -   **Proxy**: Controls access to an object.
    -   **Bridge**: Separates abstraction from implementation.
    -   **Composite**: Composes objects into tree structures.
    -   **Flyweight**: Uses sharing to support large numbers of fine-grained objects.
-   **Behavioral Patterns**:
    -   **Strategy**: Defines a family of algorithms, encapsulates each one.
    -   **Observer**: Defines a one-to-many dependency between objects.
    -   **Command**: Encapsulates a request as an object.
    -   **State**: Allows an object to alter its behavior when its internal state changes.
    -   **Template Method**: Defines the skeleton of an algorithm.
    -   **Iterator**: Provides a way to access elements of a collection sequentially.
    -   **Visitor**: Defines a new operation without changing the classes.
    -   **Mediator**: Defines simplified communication between classes.
    -   **Memento**: Captures and externalizes an object's internal state.
    -   **Interpreter**: Represents grammar using objects.

### 4.3. Building Professional CLIs

_Мета: Створення зручних інструментів (User Experience)._

-   **System.CommandLine**: (Overview) Parsing arguments, options, commands.
-   **Spectre.Console**:
    -   Styling & Markup (colors, emoji).
    -   Widgets: Tables, Trees, Panels, Rules.
    -   Prompts: Selection, Multi-selection, Text input with validation.
    -   Live Displays: Progress Bars, Status spinners, Live charts.
    -   AnsiConsole features.

### 4.4. Validation & Flow Control

_Мета: Гарантувати цілісність даних та керувати логікою без "Exception Driven Development"._

-   **Defensive Programming**: Guard Clauses (`ArgumentNullException.ThrowIfNull`).
-   **Classic Validation**:
    -   Data Annotations (`[Required]`, `[MaxLength]`).
    -   `IValidatableObject` interface.
    -   **FluentValidation** (Library): Rules, Custom Validators, Localization.
-   **Handling Logic Errors**: Чому Exceptions — це повільно і тільки для "виняткових" ситуацій.
-   **The Result Pattern**:
    -   Концепція: Повернення об'єкта `Result<T>` (Success/Failure) замість `throw`.
    -   Generic Result Wrappers (Implementation).
    -   Railway Oriented Programming (ROP) basics (ланцюжок викликів `OnSuccess`, `OnFailure`).
    -   Libraries: `FluentResults` або `ErrorOr`.

### 4.5. The Modern .NET Host (Microsoft.Extensions)

-   **Dependency Injection**: Container (`IServiceCollection`, `IServiceProvider`), Service lifecycles (Transient, Scoped, Singleton), Scopes, Container internals, Custom containers, DI Best Practices (Constructor injection, avoiding Service Locator anti-pattern), DI Anti-patterns (Captive Dependency, Circular Dependencies).
-   **Configuration**: IConfiguration interface, Configuration providers (JSON files `appsettings.json`, Environment Variables, User Secrets, Command Line), Options Pattern (`IOptions<T>`, `IOptionsSnapshot<T>`, `IOptionsMonitor<T>`), Hot Reload.
-   **Logging**: ILogger abstraction, Serilog integration, Structured Logging (Message templates, properties), High-performance logging with LoggerMessage source generator.
-   **Resilience**: Polly library for transient fault handling (Retries, Circuit Breakers, Bulkhead, Timeout, Fallback policies).
-   **Background Services**: IHostedService interface, BackgroundService base class, Hosted Services Lifecycle (Start, Stop, Graceful shutdown).

## 5. The Standard Library (Робота з Даними)

_Мета: Ефективно маніпулювати даними._

### 5.1. Collections

-   **Generic Collections**: `List<T>`, `Dictionary<T,V>`, `HashSet<T>`, `Queue<T>`, `Stack<T>`, `LinkedList<T>`.
-   **Concurrent Collections**: `ConcurrentDictionary`, `BlockingCollection`, **`System.Threading.Channels`** (Producer/Consumer queues).
-   \*\*Immutable Collections`.
-   `IEnumerable<T>` & `IEnumerator<T>` (Yield return).
-   `Array` class & Multidimensional arrays.
-   **Collection Expressions** (`[]`).

### 5.2. High Performance Types

-   `Span<T>` & `ReadOnlySpan<T>`.
-   `Memory<T>`.
-   Array Slicing (Indices & Ranges).
-   Stackalloc.

### 5.3. LINQ (Language Integrated Query)

-   Query Syntax vs Method Syntax.
-   Deferred Execution vs Immediate Execution.
-   Filtering (`Where`, `OfType`).
-   Projection (`Select`, `SelectMany`).
-   Sorting (`OrderBy`, `ThenBy`).
-   Grouping (`GroupBy`).
-   Joins (`Join`, `GroupJoin`).
-   Aggregation (`Sum`, `Count`, `Aggregate`, `MaxBy`, `MinBy`).
-   Set Operations (`Distinct`, `Union`, `Intersect`).
-   Element Operations (`First`, `Single`, `ElementAt`, `Index`).

## 6. The System: Internals & Concurrency (Системне Програмування)

_Мета: Розуміти процеси, пам'ять та асинхронність._

### 6.1. Memory Management

-   Garbage Collection (Generations, Triggers, LOH/SOH/POH).
-   Unmanaged Resources.
-   `IDisposable` & `using` statement.
-   Finalizers (Destructors).
-   `WeakReference`.
-   **Memory Layout**: Object Header, Method Table Pointer, Structure Padding/Alignment.

### 6.2. Reflection & Dynamic

-   `System.Type`.
-   Reflection API (Inspecting metadata, Invoking members).
-   **Attributes**: Built-in & Custom attributes.
-   **DLR**: `dynamic` keyword, `ExpandoObject`.

### 6.3. Multithreading (Low Level)

-   `Thread` class.
-   Thread Priorities & States.
-   Synchronization Primitives: `lock` (Monitor), `System.Threading.Lock` (C# 13), `Mutex`, `Semaphore`, `AutoResetEvent`.
-   `Interlocked` operations.
-   `Volatile`.

### 6.4. TPL (Task Parallel Library)

-   `Task` & `Task<T>`.
-   Task Lifecycle.
-   Task Continuation (`ContinueWith`).
-   `Parallel` class (`For`, `ForEach`, `Invoke`).
-   `CancellationToken`.

### 6.5. Async/Await

-   Asynchronous Programming Model (TAP).
-   `async` & `await` keywords.
-   State Machine under the hood.
-   `Task.WhenAll`, `Task.WhenAny`.
-   Async Streams (`IAsyncEnumerable`).
-   Best Practices (Avoid `async void`, Deadlocks).

### 6.6. PLINQ (Parallel LINQ)

-   `AsParallel()`.
-   `AsOrdered()`.
-   Degree of Parallelism.

### 6.7. Unsafe Code

-   `unsafe` context.
-   Pointers (`*`, `&`, `->`).
-   `fixed` statement.
-   Function Pointers.

## 7. Networking & Security (Мережа та Безпека)

_Мета: Взаємодія зі світом._

### 7.1. Networking Basics

-   IP Addresses, DNS, Ports.
-   TCP vs UDP protocols.
-   `System.Net.Sockets` (Socket programming basics).

### 7.2. HTTP Client

-   `HttpClient` Lifecycle & `IDisposable` issues.
-   `IHttpClientFactory` (Best Practice).
-   Making GET/POST/PUT/DELETE requests.
-   Headers, Content, Status Codes.
-   Polly (Resilience & Transient Fault Handling).

### 7.3. Modern Web Protocols

-   WebSockets (`System.Net.WebSockets`).
-   SignalR (Concept).
-   gRPC (Protocol Buffers).
-   HTTP/2 & HTTP/3 (QUIC).

### 7.4. Security

-   Cryptography Basics (Hashing vs Encryption).
-   `System.Security.Cryptography`.
-   Hashing (SHA256, HMAC).
-   Encryption (AES, RSA).
-   Secure Strings (Obsolete vs Alternatives).

## 8. I/O & Serialization (Ввід/Вивід)

_Мета: Зберігати та передавати дані._

### 8.1. File System

-   `File`, `Directory`, `Path`, `FileInfo`, `DirectoryInfo`.
-   Streams architecture (`Stream`, `FileStream`, `MemoryStream`).
-   `StreamReader` & `StreamWriter`.
-   `BinaryReader` & `BinaryWriter`.
-   Compression (`GZipStream`, `ZipArchive`).

### 8.2. Serialization

-   **JSON**: `System.Text.Json` (JsonSerializer, Attributes, Custom Converters, Source Generators).
-   **XML**: `System.Xml`, `XmlSerializer`, LINQ to XML (`XDocument`).
-   **Binary**: `MessagePack` / `Protobuf` (Alternatives to `BinaryFormatter`).

## 9. Tooling & Deployment (Інструменти)

_Мета: Тестувати та публікувати._

### 9.1. Unit Testing

-   Test Frameworks (xUnit / NUnit).
-   Asserts.
-   Mocking dependencies (Moq / NSubstitute).
-   **TDD (Test Driven Development)**: Philosophy and workflow.
-   **Testcontainers**: Docker-based integration testing (Database/Redis containers).
-   **Faking/Stubbing vs Mocking**: Differences and when to use each.
-   Integration Testing basics.

### 9.2. Benchmarking & Performance

-   **BenchmarkDotNet**.
-   Profiling (Visual Studio Profiler, dotTrace).
-   Memory Leaks analysis.

### 9.3. Processes & Assemblies

-   `Process` class.
-   AppDomains (Legacy vs Core).
-   Assembly Loading (`AssemblyLoadContext`).

### 9.4. Publishing

-   Build Configurations (Debug/Release).
-   Publish Profiles.
-   Framework-dependent vs Self-contained.
-   Single File Executable.
-   Trimming (Зменшення розміру).
-   Native AOT (Ahead-of-Time compilation).
