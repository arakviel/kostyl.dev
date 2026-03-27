# План курсу: ASP.NET Core Web API (Controllers)

> **Принцип кожної статті:** Кожна стаття містить **наскрізний демо-проєкт** що студент відтворює покроково. Демо-проєкт логічно розгортається від простого до складного впродовж статті й є самодостатнім.

## Контекст і задача

Студенти вже **досконало** вивчили:

- **Minimal API (17 статей):** `WebApplication.CreateBuilder`, DI, middleware pipeline, routing (basics + advanced), static files & assets, configuration (fundamentals + options), logging (basics + advanced), state management та session, структура проєкту, OpenAPI (Scalar + Swagger)
- **API Design (14 статей):** Що таке API, формати даних (JSON/XML), парадигми REST, HTTP-методи та статус-коди, REST-організація, URL-номенклатура та CRUD, іменування, валідація, обробка помилок, ідемпотентність, пагінація, безпека, процес проєктування API, OpenAPI специфікація
- **Razor Pages (6 статей):** PageModel, Razor syntax, Tag Helpers, форми і валідація, проєкт Task Manager
- **MVC (16 статей):** Controllers/Actions, Convention/Attribute Routing, Model Binding (`[FromRoute]`, `[FromQuery]`, `[FromBody]`), Views/ViewData/TempData, Filters, Areas, View Components, Display/Editor Templates, FluentValidation, HTMX, File Upload, Globalization/Localization
- **Auth (16 статей):** JWT, Cookie, Identity, OAuth, OIDC/Keycloak, API Keys, Rate Limiting, RBAC/ABAC/ReBAC, Multi-tenancy
- **Caching (5 статей):** Memory Cache, Distributed Cache (Redis), Response Cache, Output Cache
- **Testing (19 статей):** xUnit, Moq, Integration Testing (WebApplicationFactory), Postman, HttpClient, WireMock, Architecture Testing, Performance Testing
- **Notifications (13 статей):** In-app, Polling, SSE, WebSockets, SignalR, Background Services, Hangfire, Web Push, Email, Telegram
- **i18n (2 статті):** Internationalization, Humanizer
- **Payments (окремий курс):** LiqPay, Monobank, Stripe

---

## Що є УНІКАЛЬНИМ у Web API Controllers порівняно з вивченим

Студенти вже знають Minimal API endpoints (`app.MapGet(...)`) і MVC Controllers з Views. **Web API Controllers** — це "третій шлях": Controller-based API **без Views**, що повертає дані (JSON/XML) замість HTML.

| Концепція | Minimal API | MVC Controllers | Web API Controllers |
|---|---|---|---|
| Базовий клас | — | `Controller` | `ControllerBase` |
| Атрибути маршрутів | `app.MapGet("/api/...")` | `[Route]`, `[HttpGet]` | `[Route("api/[controller]")]`, `[ApiController]` |
| Повернення | `Results.Ok(data)` | `View()`, `Json()` | `ActionResult<T>`, automatic JSON |
| Model Binding | параметри handler | `[FromRoute]`, `[FromBody]` | `[FromBody]` (auto JSON), `[FromQuery]` |
| Валідація | ручна або FluentValidation | `ModelState.IsValid` + View | `[ApiController]` auto 400 + ProblemDetails |
| Content Negotiation | ручна | ручна | ✅ Автоматична (JSON/XML/custom) |
| Versioning | ручне | ручне | `Asp.Versioning.Mvc` NuGet |
| Документація | `WithOpenApi()` | — | Swashbuckle / NSwag |

---

## Що НЕ включаємо і чому

| Тема | Причина виключення |
|---|---|
| `WebApplication.CreateBuilder`, DI, Middleware | ✅ Вже Minimal API (01-04) |
| Configuration, Options, Logging | ✅ Вже Minimal API (09-12) |
| Що таке API, REST теорія, HTTP-методи, статус-коди | ✅ Вже API Design (01-06) |
| URL-номенклатура, CRUD, іменування API | ✅ Вже API Design (06-07) |
| Базова валідація (DataAnnotations), обробка помилок | ✅ Вже API Design (08-09) та Razor Pages (05) |
| Ідемпотентність, пагінація, OpenAPI специфікація | ✅ Вже API Design (10-11, 14) |
| Authentication/Authorization (JWT, OAuth, Identity) | ✅ Вже Auth (01-16) |
| Caching (Memory, Distributed, Response, Output) | ✅ Вже Caching (01-05) |
| Testing (unit, integration, Postman, WireMock) | ✅ Вже Testing (01-19) |
| SignalR, Background Services, Hangfire | ✅ Вже Notifications (05-06, 10-12) |
| Filter Pipeline, Areas (загальна концепція) | ✅ Вже MVC (07-08) |
| FluentValidation (загальна концепція) | ✅ Вже MVC (11) |
| Routing basics, Model Binding basics | ✅ Вже MVC (04-05), Minimal API (05-06) |
| File Upload (IFormFile, PhysicalFile) | ✅ Вже MVC (14) |
| Globalization/Localization | ✅ Вже MVC (15) + i18n (01-02) |

---

## Структура курсу (12 статей)

### Блок 1: Від Minimal API до Web API Controllers (2 статті)

#### 01. `01.from-minimal-api-to-controllers.md` — Від Minimal API до Controller-based API

**Унікальне:** Порівняння `app.MapGet` vs `[HttpGet]` на Controller. `ControllerBase` vs `Controller` — чому Web API використовує `ControllerBase` (без View-support). `[ApiController]` — що він включає автоматично: auto model validation + auto 400, `[FromBody]` inference, ProblemDetails для помилок. Та сама REST API написана двома способами. Міграційна таблиця: кожен патерн Minimal API → еквівалент у Web API Controllers. **Демо-проєкт:** Todo API — одне рішення, два підходи: Minimal API program.cs vs TodoController. Порівняння за кількістю коду, тестованістю, масштабованістю.

---

#### 02. `02.controller-base-actionresult.md` — ControllerBase, ActionResult\<T\> та Response Types

**Унікальне:** Ієрархія `ControllerBase` → допоміжні методи (`Ok()`, `Created()`, `NoContent()`, `NotFound()`, `BadRequest()`, `Conflict()`, `Problem()`). `ActionResult<T>` vs `IActionResult` — чому generic версія краща для OpenAPI. `[ProducesResponseType]` атрибути. Повернення файлів з API (`File()`, `PhysicalFile()`). Типові патерни: «знайти або 404», «створити і 201 з Location header». **Демо-проєкт:** `ProductsController` з повним CRUD — правильні статус-коди, Location header для POST, ProblemDetails для помилок.

---

### Блок 2: Ядро Web API (3 статті)

#### 03. `03.content-negotiation.md` — Content Negotiation: JSON, XML та власні форматери

**Унікальне (немає в жодному попередньому курсі):** Механізм Content Negotiation: `Accept` header → вибір формату відповіді. Конфігурація: `AddControllers().AddJsonOptions()`, `AddXmlSerializerFormatters()`. System.Text.Json vs Newtonsoft.Json — коли потрібен Newtonsoft. Кастомні `OutputFormatter` та `InputFormatter` (CSV, YAML, MessagePack). `[Produces("application/json")]`, `[Consumes("application/json")]`. `ObjectResult` глибоко. **Демо-проєкт:** API продуктів що повертає JSON, XML або CSV залежно від `Accept` header. Custom `CsvOutputFormatter`.

---

#### 04. `04.api-versioning.md` — Версіонування API

**Унікальне (немає в жодному попередньому курсі):** Чому версіонування потрібне (breaking changes, backward compatibility). Стратегії версіонування: URL path (`/api/v1/products`), Query string (`?api-version=1.0`), HTTP header (`X-Api-Version`), Media type (`application/vnd.myapp.v1+json`). Пакет `Asp.Versioning.Mvc` (`[ApiVersion("1.0")]`, `[MapToApiVersion("2.0")]`). `ApiVersionReader` комбінований. Deprecation flow: `[ApiVersion("1.0", Deprecated = true)]`. Sunset header. **Демо-проєкт:** e-commerce API з v1 (basic product) та v2 (product з категоріями та рейтингом). Обидві версії працюють одночасно. Migration guide.

---

#### 05. `05.problemdetails-error-handling.md` — ProblemDetails та структурована обробка помилок

**Відмінність від API Design:** API Design (09) — теорія error handling у REST. **Ця стаття** — практична реалізація в ASP.NET Core: `ProblemDetails` (RFC 9457), `ErrorController` vs exception handler middleware, `IExceptionHandler` (.NET 8+), `IProblemDetailsService`, налаштування `UseExceptionHandler` для JSON vs HTML. Custom `ProblemDetails` extensions (error codes, traceability). StatusCodePages middleware для API. Global exception handling policy. **Демо-проєкт:** Створення `GlobalExceptionHandler` що конвертує бізнес-винятки (`NotFoundException`, `ConflictException`, `ValidationException`) у стандартні ProblemDetails з правильними HTTP-кодами та кореляційними ID.

---

### Блок 3: Просунуті концепції (4 статті)

#### 06. `06.filters-for-api.md` — Фільтри у Web API контексті

**Відмінність від MVC (07):** MVC Filters — загальна концепція pipeline. **Ця стаття** — специфіка Web API: `IActionFilter` для API (валідація DTO перед дією), `IExceptionFilter` для API (повернення ProblemDetails замість View), `IResultFilter` для wrapping відповідей (envelope pattern: `{ data: ..., meta: ... }`). `[ServiceFilter]` з Scoped залежностями для API-контексту. Order та виконання фільтрів у ланцюгу. **Демо-проєкт:** `ApiKeyAuthFilter` (авторизація через API-ключ), `RequestValidationFilter` (централізована валідація DTO), `ResponseWrapperFilter` (envelope pattern для всіх відповідей), `CorrelationIdFilter` (traceability).

---

#### 07. `07.pagination-filtering-sorting.md` — Пагінація, фільтрація та сортування: реалізація

**Відмінність від API Design:** API Design (11) — теорія пагінації та списків. **Ця стаття** — практична реалізація: `PagedList<T>`, `PaginationFilter`, заголовки `X-Pagination`. Query-based фільтрація через `[FromQuery]` з DTO (`ProductFilter { MinPrice, MaxPrice, Category, InStock }`). Сортування: dynamic `OrderBy()` через `System.Linq.Dynamic.Core` або expression trees. `PagedResponse<T>` envelope. HATEOAS links у пагінації (`_links: { self, next, prev, first, last }`). **Демо-проєкт:** Products API з фільтрацією (`?category=tech&minPrice=100`), сортуванням (`?sort=price:desc,name:asc`) та cursor-based пагінацією.

---

#### 08. `08.hateoas-resource-expansion.md` — HATEOAS та Resource Expansion

**Унікальне (немає в жодному попередньому курсі):** Що таке HATEOAS (Hypermedia as the Engine of Application State). Richardson Maturity Model (Level 0-3). HAL (Hypertext Application Language) формат. Реалізація `_links` та `_embedded` у відповідях. `LinkGenerator` в ASP.NET Core. Resource expansion через query parameter (`?expand=author,comments`). Sparse fieldsets (`?fields=id,title,author`). Бібліотека рівня 3: коли HATEOAS — overkill. **Демо-проєкт:** Blog API з HATEOAS: `GET /api/articles` повертає `_links` для навігації; `GET /api/articles/5?expand=author,comments` повертає вбудовані пов'язані ресурси.

---

#### 09. `09.minimal-api-vs-controllers-hybrid.md` — Гібридна архітектура: Minimal API + Controllers

**Унікальне (немає в жодному попередньому курсі):** Як комбінувати Minimal API та Controllers у одному проєкті. Стратегії розподілу: CRUD через Controllers, lightweight endpoints через Minimal API. Carter library для організації Minimal API. Vertical Slice Architecture: feature folders замість шарів. Feature-based project structure vs layer-based. `IEndpointRouteBuilder` extensions. **Демо-проєкт:** E-commerce backend: ProductsController (повний CRUD), `HealthEndpoints.cs` (Minimal API health checks), `MetricsEndpoints.cs` (lightweight metrics). Один проєкт, два підходи, спільні сервіси.

---

### Блок 4: Production-Ready (3 статті)

#### 10. `10.api-documentation-generation.md` — Документація API: Swashbuckle, NSwag та клієнтська генерація

**Відмінність від Minimal API (16-17) та API Design (14):** Minimal API — базове підключення Scalar/Swagger. API Design — специфікація OpenAPI. **Ця стаття** — production-level документація для Web API Controllers: XML-коментарі → OpenAPI, Swashbuckle фільтри (`IOperationFilter`, `IDocumentFilter`), аутентифікація у Swagger UI (Bearer token, API Key). NSwag як альтернатива. **Генерація клієнтів:** `NSwag.CodeGeneration` для C# та TypeScript клієнтів. `Refit` автоматичний HTTP-клієнт з інтерфейсу. **Демо-проєкт:** повністю задокументований Products API → згенерований TypeScript SDK → консольний C# клієнт через NSwag.

---

#### 11. `11.health-checks-monitoring.md` — Health Checks та моніторинг API

**Унікальне (немає в жодному попередньому курсі):** `IHealthCheck` інтерфейс, `MapHealthChecks`. Вбудовані чеки: SQL Server, Redis, RabbitMQ. Кастомні health checks (зовнішні API, диск, пам'ять). Health check UI (`AspNetCore.HealthChecks.UI`). Health check tags та фільтри (`liveness` vs `readiness`). `IHealthCheckPublisher` для push-based моніторингу. Structured health response (JSON). Kubernetes probes (`/healthz`, `/readyz`). **Демо-проєкт:** API з 5 health checks (DB, Redis, external API, disk space, memory), `/health` endpoint з JSON-деталями, Health Check UI на `/health-ui`.

---

#### 12. `12.web-api-project.md` — Підсумковий проєкт: Production-Ready REST API

**Унікальне:** Наскрізний проєкт що поєднує **всі 11 попередніх статей**. Book Store REST API:
- `ControllerBase` + `[ApiController]` → books, authors, categories, reviews
- Content Negotiation: JSON + XML
- API Versioning: v1 (basic) + v2 (з рейтингами та рецензіями)
- ProblemDetails для всіх помилок
- Фільтри: CorrelationId, ResponseWrapper, ApiKey
- Пагінація, фільтрація, сортування з HATEOAS links
- XML-documented controllers → Swagger UI з auth
- Health Checks (DB + зовнішні залежності)
- Карта: кожна попередня стаття → де у проєкті застосовано

---

## Послідовність і залежності

```
01. Від Minimal API до Controllers
      ↓
02. ControllerBase, ActionResult<T>
      ↓
03. Content Negotiation ←────────── (немає аналога у попередніх курсах)
04. API Versioning ←─────────────── (немає аналога)
05. ProblemDetails ←─────────────── (розширення API Design 09)
      ↓
06. Фільтри для API ←───────────── (розширення MVC 07 для API-контексту)
07. Пагінація реалізація ←──────── (розширення API Design 11)
08. HATEOAS ←────────────────────── (немає аналога)
09. Гібридна архітектура ←──────── (немає аналога)
      ↓
10. API документація production ← (розширення Minimal API 16-17)
11. Health Checks ←──────────────── (немає аналога)
      ↓
12. Підсумковий проєкт
```

---

## Зв'язки з іншими курсами (мости)

| Цей курс по­си­ла­ється на | Курс | Статті |
|---|---|---|
| REST теорія, HTTP-методи, ідемпотентність | API Design | 01-06, 10 |
| Валідація (DataAnnotations, FluentValidation) | API Design (08), MVC (11) | — |
| DI, middleware, configuration, logging | Minimal API | 01-04, 09-12 |
| Authentication/Authorization для API | Auth | 02 (JWT), 11 (API Keys), 12 (Rate Limiting) |
| Integration Testing (WebApplicationFactory) | Testing | 11-12 |
| Caching стратегії | Caching | 01-05 |
| Background processing | Notifications | 06 (BackgroundService), 10 (Hangfire) |
