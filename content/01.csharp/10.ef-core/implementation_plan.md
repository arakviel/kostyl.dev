# План вивчення Entity Framework Core — Повний курс

> Повна версія плану також доступна у `content/01.csharp/10.ef-core/plan.md`

## Мета

Створити повний, глибокий навчальний курс з Entity Framework Core, що охоплює **весь** функціонал фреймворку. Кожна стаття — ~1000 рядків контенту українською мовою, у стилі `prompt.md` (text-first, "why before how", code anatomy, Docus components). Матеріали розміщуються у `content/01.csharp/10.ef-core/`.

## Контекст

- **Попередній матеріал**: ADO.NET (12 статей) — читач вже знає SQL, підключення, командні об'єкти, DataReader, транзакції, Repository pattern
- **Наступний матеріал**: ASP.NET Core — читач буде використовувати EF Core у веб-додатках
- **Стиль**: Аналогічний `07.testing/` — глибока деталізація, ~30-50KB на статтю, академічний але живий виклад

---

## Структура курсу: 7 блоків, 31 стаття

### Блок 1: Основи та Фундамент (статті 01–05)

> Від проблеми до першого робочого ORM-проєкту

---

#### 01. `01.what-is-orm.md` — Що таке ORM? Від SQL до об'єктів

**Проблема-гачок**: Impedance mismatch — чому реляційні таблиці і об'єкти C# не стикуються напряму, і до чого це призводить у реальних проєктах.

**Зміст (~1000 рядків)**:
- Історія доступу до даних: raw SQL → ADO.NET → Data Mappers → ORM
- Academic definition: Object-Relational Mapping як патерн (Martin Fowler)
- Impedance mismatch: 5 конкретних проблем (типи, ідентичність, зв'язки, навігація, гранулярність)
- Патерни доступу до даних: Active Record vs Data Mapper vs Repository
- Порівняння: ADO.NET вручну vs ORM (один і той самий CRUD у двох підходах)
- Аргументи **за** і **проти** ORM (з реальними прикладами)
- Landscape .NET ORM: EF Core, Dapper, NHibernate, LINQ to DB — коли яку обрати
- Dapper vs EF Core: детальне порівняння (performance, developer experience, flexibility)
- EF Core: чому саме він — history, maintainers, ecosystem, community
- Mermaid-діаграма: де ORM знаходиться в архітектурі типового додатку
- Практичні завдання (3 рівні)

---

#### 02. `02.first-project.md` — Перший проєкт: від нуля до CRUD

**Проблема-гачок**: Ми маємо клас `Product` в C# і таблицю `Products` в базі — як їх пов'язати без ручного маппінгу?

**Зміст (~1000 рядків)**:
- Встановлення NuGet-пакетів (EF Core, провайдер, tools)
- Entity class: конвенції іменування, властивості, типи
- DbContext: що це, навіщо, як працює "під капотом"
- DbSet\<T\>: колекція-в-пам'яті чи абстракція таблиці?
- Connection string: формат, секрети, user secrets
- OnConfiguring vs DI: два способи конфігурації (з поясненням, чому DI краще)
  - ⚠️ **Ремарка**: DI (Dependency Injection) буде детально вивчатися у розділі ASP.NET Core. Тут даємо лише короткий огляд синтаксису та мотивацію, чому DI-підхід є кращим
- Database.EnsureCreated() vs Migrations — перший вибір
- Повний CRUD: Create, Read, Update, Delete — покроково з code anatomy
- SaveChanges(): що насправді відбувається при виклику
- Логування SQL: як побачити, що EF Core генерує (EnableSensitiveDataLogging, LogTo)
- PlantUML: діаграма класів DbContext-DbSet-Entity
- Mermaid: lifecycle запиту від LINQ до SQL
- Практичні завдання (3 рівні)

---

#### 03. `03.dbcontext-deep-dive.md` — DbContext: Серце EF Core

**Проблема-гачок**: Чому один і той самий DbContext не можна використовувати в різних потоках? Чому lifetime має значення?

**Зміст (~1000 рядків)**:
- DbContext як Unit of Work + Repository (академічне визначення обох патернів)
- Внутрішня архітектура: StateManager, ChangeTracker, QueryCompiler, Database абстракція
- Lifetime management: Transient vs Scoped vs Singleton — чому Scoped правильний вибір
  - ⚠️ **Ремарка**: Lifetime management та DI-контейнер буде детально вивчатися у розділі ASP.NET Core. Тут пояснюємо концепцію на рівні, достатньому для розуміння DbContext lifecycle
- Реєстрація через AddDbContext / AddDbContextFactory — коли що використовувати
- DbContextFactory: навіщо, коли Scoped недостатньо (Blazor, background services)
- Pooling: AddDbContextPool — як працює, бенчмарки, обмеження
- OnConfiguring vs OnModelCreating — різниця та відповідальності
- DbContextOptions та DbContextOptionsBuilder: builder pattern у деталях
- Множинні DbContext у одному проєкті: bounded contexts, микросервіси
- Thread safety: чому DbContext НЕ є thread-safe (з прикладом race condition)
- IDesignTimeDbContextFactory: навіщо потрібен для міграцій
- Mermaid: lifecycle DbContext від створення до Dispose
- Практичні завдання (3 рівні)

---

#### 04. `04.database-providers.md` — Провайдери баз даних

**Проблема-гачок**: EF Core працює з PostgreSQL, SQL Server, SQLite, MySQL — але як один і той самий код підтримує різні СУБД?

**Зміст (~1000 рядків)**:
- Архітектура провайдерів: абстракції та їх реалізації (Database, RelationalConnection, QuerySqlGenerator)
- SQL Server: Npgsql.EntityFrameworkCore.PostgreSQL — конфігурація, специфічні типи
- PostgreSQL: типи jsonb, arrays, enums, full-text search — як це маппиться
- SQLite: обмеження, коли використовувати (тестування, прототипування, мобільні додатки)
- MySQL / MariaDB: Pomelo.EntityFrameworkCore.MySql
- InMemory: навіщо існує, чому НЕ для продакшн тестів
- Cosmos DB: NoSQL світ через EF Core
- Різниці між провайдерами: типи, міграції, автоінкремент, GUID стратегії
- Як обирати провайдер: матриця рішень
- Provider-specific конфігурація: UseNpgsql(), UseSqlServer() і їх параметри
- Mermaid: стек абстракцій від LINQ до SQL-діалекту конкретної СУБД
- Практичні завдання (3 рівні)

---

#### 05. `05.conventions.md` — Конвенції: Магія без конфігурації

**Проблема-гачок**: Чому EF Core "просто знає", що властивість `Id` — це первинний ключ, а `BlogId` у `Post` — зовнішній? Тут знімаємо магію.

**Зміст (~1000 рядків)**:
- Що таке Convention-over-Configuration і чому це важливо
- Повний перелік вбудованих конвенцій EF Core:
  - Primary Key convention (Id, EntityNameId)
  - Foreign Key convention
  - Table naming convention
  - Column naming, type mapping conventions
  - Required/Optional convention (nullable reference types)
  - Navigation property discovery
  - Index convention
  - Cascade delete convention
- Nullable Reference Types та їх вплив на модель
- Коли конвенції заважають: приклади конфліктів
- Як перевизначити конвенції: Fluent API > Data Annotations > Conventions
- Пріоритет конфігурації: ієрархія та приклади
- Custom conventions (EF Core 7+): IModelFinalizingConvention, IEntityTypeAddedConvention
- Практичні завдання (3 рівні)

---

### Блок 2: Моделювання даних (статті 06–15)

> Серце ORM — як правильно описати структуру бази

---

#### 06. `06.fluent-api-vs-annotations.md` — Fluent API vs Data Annotations

**Зміст (~1000 рядків)**:
- Data Annotations: атрибути [Key], [Required], [MaxLength], [Table], [Column], [ForeignKey], [InverseProperty], [Index]
- Fluent API: HasKey, Property().IsRequired(), HasMaxLength(), ToTable(), HasColumnName()
- Порівняння: що можна лише через Fluent API (owned types, TPH discriminator, many-to-many з payload)
- Організація Fluent API: EntityTypeConfiguration\<T\> (IEntityTypeConfiguration) — окремі файли конфігурації
- ApplyConfigurationsFromAssembly: автоматичне сканування
- Практика: один і той самий маппінг через Annotations і Fluent API — порівняння
- Коли що обирати: практична матриця рішень
- Практичні завдання (3 рівні)

---

#### 07. `07.relationships-basics.md` — Зв'язки: One-to-One, One-to-Many

**Зміст (~1000 рядків)**:
- Теорія зв'язків: Principal, Dependent, Foreign Key, Navigation Property — точні визначення
- One-to-Many: найпоширеніший зв'язок — конвенції, конфігурація, приклади
- Required vs Optional relationships (nullable FK)
- One-to-One: обов'язковий та необов'язковий — нюанси конфігурації
- Navigation properties: Reference vs Collection — як обирати
- DeleteBehavior: Cascade, Restrict, SetNull, NoAction, ClientSetNull — повний огляд та коли що обирати
- Bidirectional vs unidirectional навігація
- Self-referencing relationships (дерева, ієрархії)
- PlantUML: діаграми ER для кожного типу зв'язку
- Практичні завдання (3 рівні)

---

#### 08. `08.relationships-advanced.md` — Зв'язки: Many-to-Many та Складні Сценарії

**Зміст (~1000 рядків)**:
- Many-to-Many: implicit join entity (EF Core 5+) vs explicit join entity
- Many-to-Many з payload: додаткові поля у зв'язковій таблиці
- Skip navigations vs direct navigations
- Alternate Keys: коли PK не є єдиним варіантом для зв'язків
- Composite keys та composite foreign keys
- Backing fields: зв'язок через приватні поля
- Polymorphic associations (антипатерн) та як правильно
- Shadow foreign keys: FK без властивості в entity
- Складні графи об'єктів: стратегії збереження (Add, Attach, Update, Entry)
- Mermaid: діаграми складних зв'язків
- Практичні завдання (3 рівні)

---

#### 09. `09.property-configuration.md` — Властивості: Типи, Конвертери, Компаратори

**Зміст (~1000 рядків)**:
- Column types: маппінг C# типів → SQL типів (int, string, decimal, DateTime, Guid, enum, byte[])
- HasColumnType, HasPrecision: точне керування SQL-типом
- Value Converters (HasConversion): enum → string, strongly typed IDs, encryption, JSON serialization
- Вбудовані конвертери: EnumToStringConverter, BoolToZeroOneConverter тощо
- Value Comparers: чому потрібні для правильного change tracking складних типів
- Value Generators: HasValueGenerator, ValueGeneratedOnAdd/OnUpdate
- Default values: HasDefaultValue, HasDefaultValueSql, HasComputedColumnSql
- Computed columns: stored vs virtual
- Shadow properties: властивості без відповідного поля в entity (аудит, soft delete)
- Backing fields: propertyAccessMode, field-only properties
- Temporal tables підтримка (SQL Server)
- Практичні завдання (3 рівні)

---

#### 10. `10.complex-types-owned.md` — Складні типи: Owned Types та Complex Types

**Зміст (~1000 рядків)**:
- Value Objects (DDD): теорія та мотивація
- Owned Types: OwnsOne, OwnsMany — вкладені типи без ID
- Table splitting: кілька entity → одна таблиця
- Entity splitting: одна entity → кілька таблиць
- Complex Types (EF Core 8+): нові Value Objects без ідентичності
- Keyless Entity Types: HasNoKey — для Views, raw SQL, aggregation
- Порівняння: Owned vs Complex vs Value Converter — коли що обирати
- Nested owned types: Address → Coordinate
- Practical DDD modeling з EF Core
- Практичні завдання (3 рівні)

---

#### 11. `11.json-columns.md` — JSON Columns: Складні дані у JSON

**Зміст (~1000 рядків)**:
- Навіщо зберігати JSON у реляційній БД: сценарії (metadata, settings, dynamic attributes)
- JSON Columns (EF Core 7+): ToJson() — конфігурація та маппінг
- Owned types + JSON: збереження складних об'єктів як JSON
- LINQ-запити до JSON properties: трансляція у SQL (PostgreSQL JSONB, SQL Server JSON)
- Nested JSON objects: OwnsMany + ToJson
- Value comparers для JSON: правильний change tracking
- Indexing JSON properties (provider-specific)
- Обмеження: що не можна робити з JSON Columns
- JSON vs окрема таблиця: матриця рішень (коли JSON, коли нормалізація)
- Provider differences: PostgreSQL JSONB vs SQL Server JSON vs SQLite
- Schema evolution: як версіонувати JSON-структуру
- Практичні завдання (3 рівні)

---

#### 12. `12.inheritance.md` — Успадкування: TPH, TPT, TPC

**Зміст (~1000 рядків)**:
- Три стратегії маппінгу ієрархій класів на таблиці
- **TPH (Table-Per-Hierarchy)**: одна таблиця, discriminator column
  - Конфігурація: HasDiscriminator, HasValue
  - Плюси та мінуси, вплив на null columns
  - Коли обирати: performance vs schema чистота
- **TPT (Table-Per-Type)**: окрема таблиця для кожного типу
  - JOIN-и при кожному запиті — вплив на продуктивність
  - Коли обирати
- **TPC (Table-Per-Concrete-Class)**: EF Core 7+ — окрема таблиця без загальної
  - UseTpcMappingStrategy
  - Sequences для генерації ID
  - Коли обирати
- Порівняльна таблиця: performance, schema, запити, міграції
- Abstract base class vs Interface: що EF Core підтримує
- Mermaid: візуалізація схем БД для кожної стратегії
- Практичні завдання (3 рівні)

---

#### 13. `13.indexes-constraints.md` — Індекси, Обмеження та Схема

**Зміст (~1000 рядків)**:
- Regular indexes: HasIndex — для чого, як вони пришвидшують запити (B-tree пояснення)
- Unique indexes: IsUnique
- Composite indexes: порядок стовпців має значення
- Filtered indexes: HasFilter — часткові індекси
- Include columns: IncludeProperties (covering indexes)
- Full-text indexes (provider-specific)
- Primary Key vs Alternate Key vs Unique Index — різниця
- Check constraints: HasCheckConstraint
- Database sequences: HasSequence, UseHiLo, UseSequence
- Collation: UseCollation — сортування і порівняння
- Database comments: HasComment
- Mermaid: як індекси впливають на план запиту
- Практичні завдання (3 рівні)

---

#### 14. `14.seeding.md` — Seed Data: Початкові дані

**Зміст (~1000 рядків)**:
- HasData(): model-based seeding — як працює, обмеження
- Owned types та seeding: хитрощі та підводні камені
- Seeding зв'язаних сущностей: порядок та FK
- Custom migration-based seeding: SQL в міграціях
- Runtime seeding: DbContext.Database.EnsureCreated + ініціалізація
- IHostedService для seeding в ASP.NET Core
- Bogus (бібліотека): генерація реалістичних тестових даних
- Seeding стратегії для різних середовищ (dev, staging, production)
- Ідемпотентність: як уникнути дублікатів при повторному seeding
- Практичні завдання (3 рівні)

---

#### 15. `15.global-query-filters.md` — Глобальні фільтри запитів

**Зміст (~1000 рядків)**:
- HasQueryFilter: навіщо, як працює "під капотом"
- Soft Delete: реалізація через глобальні фільтри
- Multi-Tenancy через фільтри: TenantId автоматично
- Вимкнення фільтрів: IgnoreQueryFilters() — коли потрібно бачити "все"
- Множинні фільтри на одній entity
- Фільтри та навігаційні властивості: нюанси
- Фільтри та Include: як вони взаємодіють
- Тестування коду з глобальними фільтрами
- Альтернативи: Interceptors, IQueryable extensions
- Практичні завдання (3 рівні)

---

### Блок 3: Запити та LINQ (статті 16–19)

> Як EF Core перетворює C# LINQ в SQL

---

#### 16. `16.linq-queries.md` — LINQ-запити: Основи та Механіка Трансляції

**Зміст (~1000 рядків)**:
- Як працює IQueryable vs IEnumerable: Expression Trees → SQL
- Expression Tree: що це і навіщо EF Core будує дерево замість виконання коду
- Client vs Server evaluation: що виконується на сервері, що — на клієнті (і чому це важливо)
- Базові оператори: Where, Select, OrderBy, Skip, Take, GroupBy, Join
- Проєкції: анонімні типи, DTO-проєкції, Select з обчисленнями
- Pagination: правильна пагінація через Keyset vs Offset
- Aggregation: Count, Sum, Average, Min, Max, Aggregate
- Any, All, Contains — предикати
- First vs Single vs FirstOrDefault vs SingleOrDefault: семантична різниця
- Distinct, Union, Intersect, Except — множинні операції
- Mermaid: pipeline обробки LINQ-запиту від C# до SQL
- Практичні завдання (3 рівні)

---

#### 17. `17.loading-related-data.md` — Завантаження пов'язаних даних

**Зміст (~1000 рядків)**:
- **Eager Loading**: Include(), ThenInclude() — одним запитом
- Filtered Include (EF Core 5+): Where, OrderBy, Take всередині Include
- **Lazy Loading**: Proxies, ILazyLoader — прозоре довантаження
  - Встановлення та конфігурація
  - Небезпека: N+1 problem у деталях
  - Коли це виправдано, а коли — катастрофа
- **Explicit Loading**: Entry().Collection().LoadAsync(), Entry().Reference().LoadAsync()
  - Query(): запити до навігаційних властивостей
- **Split Queries**: AsSplitQuery() — чому один великий JOIN не завжди кращий
  - Cartesian Explosion проблема
  - Глобальне налаштування UseQuerySplittingBehavior
- **No Tracking**: AsNoTracking(), AsNoTrackingWithIdentityResolution()
- Порівняльна таблиця: коли яку стратегію обирати
- Mermaid: SQL-запити, що генеруються кожною стратегією
- Практичні завдання (3 рівні)

---

#### 18. `18.raw-sql.md` — Raw SQL, Stored Procedures, Views

**Зміст (~1000 рядків)**:
- FromSqlRaw / FromSqlInterpolated: коли LINQ недостатньо
- Параметризація: захист від SQL Injection (чому Interpolated безпечний)
- Composing: .Where().OrderBy() на FromSql — коли працює, коли ні
- ExecuteSqlRaw / ExecuteSqlInterpolated: зміна даних через SQL
- SqlQuery\<T\> (EF Core 8+): scalar та non-entity запити
- Stored Procedures: виклик та маппінг результатів
- Database Views: маппінг на Keyless Entity Types
- ToSqlQuery: маппінг entity на довільний SQL
- Table-Valued Functions: маппінг UDF
- Безпека: SQL Injection ризики при роботі з Raw SQL у EF Core
- Практичні завдання (3 рівні)

---

#### 19. `19.advanced-queries.md` — Просунуті запити

**Зміст (~1000 рядків)**:
- Compiled Queries: EF.CompileQuery / EF.CompileAsyncQuery — кеширование Expression Trees
- Коли compiled queries дають реальний приріст, а коли ні
- Global Query Tags: TagWith() — маркування запитів для DBA
- User-defined functions: HasDbFunction для маппінгу DB функцій на C#
- Temporal queries (SQL Server): TemporalAll, TemporalAsOf, TemporalBetween
- Bulk operations (EF Core 7+): ExecuteUpdate, ExecuteDelete — без завантаження entities
- LINQ GroupBy з агрегацією: трансляція у SQL GROUP BY
- Subqueries через LINQ: як EF Core обробляє вкладені запити
- Pagination patterns: Keyset pagination у деталях
- Query caching: як EF Core кешує скомпільовані запити
- Практичні завдання (3 рівні)

---

### Блок 4: Change Tracking та Збереження (статті 20–22)

> Як EF Core знає, що змінилось

---

#### 20. `20.change-tracking.md` — Change Tracker: Як EF Core відстежує зміни

**Зміст (~1000 рядків)**:
- EntityState: Added, Modified, Deleted, Unchanged, Detached — повний опис
- Як Change Tracker працює під капотом: snapshot-based tracking
- Original Values vs Current Values
- DetectChanges(): коли і як EF Core знаходить зміни
- ChangeTracker.Entries\<T\>(): інспекція стану entities
- PropertyEntry: IsModified, OriginalValue, CurrentValue
- Attach vs Add vs Update: різниця та сценарії
- TrackGraph: складні графи об'єктів
- Auto-DetectChanges: вплив на продуктивність, коли вимикати
- ChangeTracker.Clear(): навіщо і коли
- Debug views: ChangeTracker.DebugView.LongView / ShortView
- Mermaid: state machine EntityState transitions
- Практичні завдання (3 рівні)

---

#### 21. `21.saving-data.md` — Збереження даних: SaveChanges та стратегії

**Зміст (~1000 рядків)**:
- SaveChanges(): що відбувається внутрішньо (DetectChanges → SQL Generation → Execution → State Reset)
- SaveChangesAsync: чому завжди async
- Batch operations: як EF Core групує INSERT/UPDATE/DELETE
- Identity insert: коли entity має DB-generated ключ
- Disconnected entities: сценарії Web API (отримав DTO → зберіг)
- Conflict resolution: DbUpdateConcurrencyException
- Transaction management: implicit vs explicit transactions
- Database.BeginTransaction, UseTransaction, TransactionScope
- Savepoints: CreateSavepoint, RollbackToSavepoint
- Retry logic: EnableRetryOnFailure, custom execution strategy
- Events: SaveChanges events (SavingChanges, SavedChanges, SaveChangesFailed)
- Mermaid: sequence diagram SaveChanges
- Практичні завдання (3 рівні)

---

#### 22. `22.concurrency.md` — Управління Конкурентним Доступом

**Зміст (~1000 рядків)**:
- Optimistic vs Pessimistic concurrency control: теорія та практика
- Concurrency Tokens: IsConcurrencyToken — як EF Core додає WHERE у UPDATE
- Row Version / Timestamp: IsRowVersion — автоматичний токен конкурентності
- DbUpdateConcurrencyException: як обробити конфлікт
- Стратегії вирішення конфліктів: Client Wins, Store Wins, Custom Merge
- Entry.GetDatabaseValues(), Entry.OriginalValues, Entry.CurrentValues
- Disconnected concurrency: конкурентність у Web API сценаріях
- ETag pattern для REST API
- Pessimistic locking: коли optimistic не підходить (raw SQL FOR UPDATE)
- Real-world scenarios: booking systems, inventory management
- Mermaid: sequence diagrams конкурентних конфліктів
- Практичні завдання (3 рівні)

---

### Блок 5: Міграції та Управління Схемою (статті 23–25)

> Еволюція бази даних разом з кодом

---

#### 23. `23.migrations-basics.md` — Міграції: Основи

**Зміст (~1000 рядків)**:
- Що таке міграції і навіщо вони потрібні (альтернатива: ручний SQL, DbUp, Flyway)
- dotnet ef migrations add: що створюється (Up, Down, Snapshot)
- dotnet ef database update: як застосовується
- Anatomy of a migration file: BuildTargetModel, Up(), Down()
- ModelSnapshot: навіщо потрібен, чому не можна видаляти
- Скасування міграцій: Remove vs Revert
- dotnet ef migrations script: SQL-скрипти для production
- Idempotent scripts: --idempotent
- Bundles: dotnet ef migrations bundle — self-contained виконуваний файл
- Migrations в CI/CD: стратегії автоматичного застосування
- Mermaid: workflow міграцій від коду до продакшн БД
- Практичні завдання (3 рівні)

---

#### 24. `24.migrations-advanced.md` — Міграції: Просунуті сценарії

**Зміст (~1000 рядків)**:
- Custom migration operations: migrationBuilder.Sql() для складних змін
- Data migrations: переміщення даних між стовпцями, таблицями
- Renaming vs Drop+Create: як EF Core інтерпретує зміни
- Squashing migrations: коли та як (Reset, Squash)
- Multiple DbContext: міграції для різних contexts
- Migration history table: __EFMigrationsHistory — кастомізація
- Schema management: HasDefaultSchema()
- Seeding через міграції: InsertData, UpdateData, DeleteData
- Reverse engineering: dotnet ef dbcontext scaffold — з існуючої БД
- Database-first workflow: scaffold → customize → maintain
- Handling breaking changes: стратегії для production з даними
- Практичні завдання (3 рівні)

---

#### 25. `25.schema-management.md` — Управління Схемою та Database-First

**Зміст (~1000 рядків)**:
- Code-First vs Database-First vs Model-First: повне порівняння
- Scaffold-DbContext: команди, параметри, фільтри таблиць
- T4 Templates для scaffolding: кастомізація згенерованого коду
- Partial classes для розширення згенерованих entities
- Fluent API vs Scaffolded Data Annotations
- Re-scaffolding workflow: як оновлювати модель при зміні БД
- EnsureCreated vs Migrate: відмінності та сценарії
- Database schema comparison tools
- Multi-database scenarios: кілька БД в одному додатку
- Практичні завдання (3 рівні)

---

### Блок 6: Продуктивність та Оптимізація (статті 26–28)

> Від "працює" до "працює швидко"

---

#### 26. `26.performance-fundamentals.md` — Продуктивність: Основи

**Зміст (~1000 рядків)**:
- Чому EF Core може бути повільним: типові антипатерни
- N+1 problem: детальне пояснення, виявлення, вирішення
- Select N+1 → Eager Loading → Split Query: еволюція рішення
- Projection: Select тільки те, що потрібно (і чому це критично)
- AsNoTracking: коли відключати tracking і скільки це дає
- Pagination: Offset vs Keyset — чому Keyset краще для великих наборів
- Count vs Any: коли перевіряти існування
- Buffering vs Streaming: ToList() vs AsAsyncEnumerable()
- Logging generated SQL: як налаштувати та аналізувати
- EF Core Diagnostics: DiagnosticListener, events
- Практичні завдання (3 рівні)

---

#### 27. `27.performance-advanced.md` — Продуктивність: Просунуті Техніки

**Зміст (~1000 рядків)**:
- DbContext pooling: бенчмарки, коли дає реальний ефект
- Compiled Queries: бенчмарки та реальний профіт
- Bulk operations: ExecuteUpdate / ExecuteDelete (EF Core 7+) vs third-party (EFCore.BulkExtensions)
- Batch size: MaxBatchSize — як впливає на INSERT/UPDATE
- Connection resiliency: EnableRetryOnFailure — стратегії повторів
- Query caching internals: як EF Core кешує SQL
- Second-level cache: EFCoreSecondLevelCacheInterceptor
- Memory management: Entity state, ChangeTracker memory impact
- Benchmarking: BenchmarkDotNet для вимірювання EF Core performance
- Database-level optimization: індекси, плани запитів, EXPLAIN ANALYZE
- Практичні завдання (3 рівні)

---

#### 28. `28.diagnostics-logging.md` — Діагностика та Логування

**Зміст (~1000 рядків)**:
- LogTo: простий спосіб логування SQL
- ILoggerFactory integration: структуроване логування
- EnableSensitiveDataLogging: показ значень параметрів
- EnableDetailedErrors: детальніші повідомлення про помилки клієнтської оцінки
- Event Counters: Microsoft.EntityFrameworkCore event counters
- DiagnosticListener: low-level діагностика
- Query tags: TagWith() для ідентифікації запитів у логах
- Slow query detection: як налаштувати алерти
- Application Insights integration
- MiniProfiler: візуалізація SQL-запитів у веб-додатку
- Практичні завдання (3 рівні)

---

### Блок 7: Просунуті Теми та Патерни (статті 29–31)

> Експертний рівень

---

#### 29. `29.interceptors.md` — Interceptors та Events

**Зміст (~1000 рядків)**:
- Що таке Interceptors і чим вони відрізняються від Events
- DbCommandInterceptor: перехоплення SQL-команд
  - ReaderExecuting, ReaderExecuted, CommandFailed
  - Модифікація SQL перед виконанням
- DbConnectionInterceptor: перехоплення підключень
- SaveChangesInterceptor: перехоплення збереження
  - Automatic auditing: CreatedAt, UpdatedAt, CreatedBy
  - Soft delete через interceptor
  - Domain Events dispatching
- IMaterializationInterceptor: перехоплення матеріалізації entities
- IQueryExpressionInterceptor: модифікація Expression Trees
- Порядок виконання interceptors
- Events: SavingChanges, SavedChanges, SaveChangesFailed
- Event vs Interceptor: коли що використовувати
- Real-world: audit trail, multi-tenancy, encryption, query logging
- Практичні завдання (3 рівні)

---

#### 30. `30.testing-with-efcore.md` — Тестування з EF Core

**Зміст (~1000 рядків)**:
- Стратегії тестування: InMemory, SQLite, Testcontainers (поглиблення з 07.testing)
- Repository Pattern та EF Core: мокування через interface
- Спеціальний DbContext для тестів: фабрики, fixtures
- Testing conventions та конфігурацій: ModelValidator
- Integration tests з WebApplicationFactory: EF Core у реальному pipeline
- Test data builders: патерн для створення тестових даних
- Snapshot testing для міграцій: перевірка ModelSnapshot
- Testing concurrency scenarios
- Testing interceptors та custom logic
- Антипатерни тестування з EF Core
- Практичні завдання (3 рівні)

---

#### 31. `31.patterns-and-architecture.md` — Архітектурні Патерни з EF Core

**Зміст (~1000 рядків)**:
- Repository Pattern: за і проти з EF Core (чи потрібен ще один шар абстракції?)
- Specification Pattern: reusable query logic
- Unit of Work: як DbContext вже реалізує цей патерн
- CQRS з EF Core: read/write separation, різні DbContext для читання та запису
- Domain-Driven Design з EF Core: Aggregates, Value Objects, Domain Events
- Bounded Contexts: кілька DbContext у одному додатку
- Clean Architecture з EF Core: шари та залежності
- Multi-tenancy strategies: shared database, separate schemas, separate databases
- Event Sourcing та EF Core: можливості та обмеження
- Microservices та EF Core: один DbContext per service, Outbox pattern
- Практичні завдання (3 рівні)

---

## Структура файлів

```
content/01.csharp/10.ef-core/
├── .navigation.yml                    # title: Entity Framework Core, icon: i-lucide-database
├── plan.md                            # План вивчення (цей файл)
│
│── 01.what-is-orm.md                  # Що таке ORM?
│── 02.first-project.md               # Перший проєкт
│── 03.dbcontext-deep-dive.md          # DbContext
│── 04.database-providers.md           # Провайдери
│── 05.conventions.md                  # Конвенції
│── 06.fluent-api-vs-annotations.md    # Fluent API vs Annotations
│── 07.relationships-basics.md         # Зв'язки: 1-1, 1-N
│── 08.relationships-advanced.md       # Зв'язки: N-N та складні
│── 09.property-configuration.md       # Властивості та конвертери
│── 10.complex-types-owned.md          # Owned Types та Complex Types
│── 11.json-columns.md                 # JSON Columns
│── 12.inheritance.md                  # TPH, TPT, TPC
│── 13.indexes-constraints.md          # Індекси та обмеження
│── 14.seeding.md                      # Початкові дані
│── 15.global-query-filters.md         # Глобальні фільтри
│── 16.linq-queries.md                 # LINQ-запити
│── 17.loading-related-data.md         # Eager, Lazy, Explicit Loading
│── 18.raw-sql.md                      # Raw SQL, Views, SP
│── 19.advanced-queries.md             # Compiled Queries, Bulk
│── 20.change-tracking.md              # Change Tracker
│── 21.saving-data.md                  # SaveChanges та транзакції
│── 22.concurrency.md                  # Оптимістична конкурентність
│── 23.migrations-basics.md            # Міграції: основи
│── 24.migrations-advanced.md          # Міграції: просунуті
│── 25.schema-management.md            # Database-First, Scaffold
│── 26.performance-fundamentals.md     # Продуктивність: основи
│── 27.performance-advanced.md         # Продуктивність: advanced
│── 28.diagnostics-logging.md          # Діагностика та логування
│── 29.interceptors.md                 # Interceptors та Events
│── 30.testing-with-efcore.md          # Тестування
│── 31.patterns-and-architecture.md    # Архітектурні патерни
```

## Навігація

```yaml
# .navigation.yml
title: Entity Framework Core
icon: i-lucide-database
```

## Порядок виконання

Статті мають створюватися послідовно, бо кожна наступна будує на попередніх. Рекомендований порядок — від 01 до 31.

## Залежності від інших розділів

| Стаття | Залежить від |
|--------|-------------|
| 01. What is ORM | 09.ado-net (весь розділ) |
| 04. Database Providers | Базові знання SQL |
| 18. Raw SQL | 09.ado-net/05.parameters-and-sql-injection |
| 21. Saving Data | 09.ado-net/06.transactions |
| 30. Testing | 11.aspnet/07.testing (увесь розділ) |
| 31. Architecture | 04.architecture-best-practices |

## User Review Required

> [!IMPORTANT]
> **Кількість статей**: 31 стаття × ~1000 рядків = ~31,000 рядків контенту. Це масштабний проєкт. Чи задовольняє така структура? Можливо:
> - Деякі теми варто об'єднати (наприклад, Diagnostics + Logging з Performance)?
> - Деякі теми не потрібні (наприклад, Database-First workflow)?
> - Потрібні додаткові теми (наприклад, EF Core з Blazor, EF Core з gRPC)?

> [!IMPORTANT]
> **Іконка навігації**: Зараз `.navigation.yml` має `icon: i-lucide-cpu`. Пропоную змінити на `icon: i-lucide-database` — більш семантично відповідає EF Core.

> [!IMPORTANT]
> **Порядок створення**: Чи є пріоритетні статті, з яких варто почати? Чи просто послідовно від 01 до 31?

## Verification Plan

### Automated Tests
- Перевірка, що всі файли створені та мають мінімум 900 рядків
- Перевірка frontmatter (title, description)
- Перевірка наявності Docus components у кожній статті

### Manual Verification
- Запуск `npm run dev` для перевірки рендерингу
- Перевірка навігації між статтями
- Перевірка діаграм Mermaid та PlantUML
