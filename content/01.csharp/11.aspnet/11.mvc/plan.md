# План курсу: ASP.NET Core MVC

> **Принцип кожної статті:** Кожна стаття містить **наскрізний демо-проєкт** що студент відтворює покроково (copy-paste по трохи, не все одразу). Демо-проєкт логічно розгортається від простого до складного впродовж статті й є самодостатнім.

## Контекст і задача

Студенти вже **досконало** вивчили:
- **Minimal API (18 статей):** `WebApplication.CreateBuilder`, middleware pipeline, routing (basics + advanced), static files & assets, configuration (fundamentals + options), logging (basics + advanced), state management та session, структура проєкту, OpenAPI (Scalar + Swagger)
- **Razor Pages (6 статей):** перехід від Minimal API, `PageModel`, Razor синтаксис, Tag Helpers (`asp-for`, `asp-page`, `asp-validation-for` тощо), форми та валідація, повноцінний проєкт Task Manager

Тому **MVC-курс** не повторює:
- ❌ `WebApplication.CreateBuilder`, DI, middleware (вже з Minimal API)
- ❌ Конфігурацію, логування, session/state (вже з Minimal API)
- ❌ Razor синтаксис (`@page`, `@model`, `@foreach`) (вже з Razor Pages)
- ❌ Tag Helpers (`asp-for`, `asp-page`, `asp-validation-for`) (вже з Razor Pages)
- ❌ Основи форм та валідації на рівні DataAnnotations (вже з Razor Pages)
- ❌ `_Layout`, `_ViewStart`, `_ViewImports`, Partial Views (вже з Razor Pages)

---

## Що є УНІКАЛЬНИМ у MVC порівняно з Razor Pages

| Концепція | Razor Pages | MVC |
|---|---|---|
| Unit організації | `PageModel` (page-centric) | `Controller` → `Action` (action-centric) |
| Routing | convention через файлову структуру `Pages/` | explicit attribute routing + convention routing |
| Результати дій | `Page()`, `RedirectToPage()` | `View()`, `RedirectToAction()`, `Json()`, `Content()` |
| Передача даних у View | властивості `PageModel` | `ViewBag`, `ViewData`, `TempData`, `ViewModel` |
| Область (Area) | немає | `[Area]` + Areas folder structure |
| Filters | Page Filters | Action/Result/Exception/Authorization Filters |
| Прив'язка моделі | `[BindProperty]` | параметри методу, `[FromRoute]`, `[FromQuery]`, `[FromBody]` |
| Компоненти View | Partial Views | Partial Views + **View Components** + **Display/Editor Templates** |

---

## Структура курсу (17 статей)

### Блок 0: Архітектура (1 стаття)

#### 01. `01.mvc-pattern.md` — Патерн MVC: архітектура, що змінила веб

**Унікальне:** Стаття **виключно про патерн**, без коду ASP.NET. Що таке Model-View-Controller як архітектурний патерн, його історія (SmallTalk-80, Trygve Reenskaug). Проблема яку вирішує: Separation of Concerns, Fat Controller Anti-pattern. Ролі: Model (дані + бізнес-логіка), View (представлення), Controller (координатор). Lifecycle HTTP-запиту в MVC. Варіації: MVP, MVVM, MVT — порівняльна таблиця. Діаграми PlantUML: sequence diagram запиту через MVC. **Демо-проєкт:** схема (без коду) роботи інтернет-магазину через MVC — хто за що відповідає.

---

### Блок 1: Від Razor Pages до MVC (1 стаття)

#### 02. `02.from-razor-pages.md` — Від Razor Pages до MVC: концептуальний перехід

**Унікальне:** Порівняльна таблиця `PageModel` vs `Controller+Action`. Коли обирати MVC над Razor Pages. Мінімальна різниця в `Program.cs` (`AddControllersWithViews()`, `MapDefaultControllerRoute()`). **Демо-проєкт:** перетворення існуючої Razor Page на Controller + Action крок за кроком.

---

### Блок 2: Ядро MVC (4 статті)

#### 03. `03.controllers-actions.md` — Controllers та Actions: серце MVC

**Унікальне:** `Controller` vs `ControllerBase`. Action methods: конвенції іменування, `async Task<IActionResult>`. Hierarchy `IActionResult` → `ActionResult<T>`. Повернення результатів: `View()`, `PartialView()`, `Json()`, `Content()`, `File()`, `StatusCode()`, `RedirectToAction()`. Атрибути: `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]`, `[NonAction]`. **Демо-проєкт:** `LibraryController` з повним CRUD — покроково від порожнього класу до всіх action methods.

---

#### 04. `04.routing-mvc.md` — Маршрутизація в MVC: Convention vs Attribute

**Унікальне:** Convention routing (`MapDefaultControllerRoute()`, `{controller=Home}/{action=Index}/{id?}`). **Attribute routing:** `[Route]`, `[HttpGet("{id}")]`, route tokens `[controller]`, `[action]`. Areas routing. **Демо-проєкт:** `BlogController` з attribute routing (`/blog/{year}/{month}/{slug}`), Areas routing для `/admin/blog/`.

---

#### 05. `05.model-binding.md` — Model Binding: від HTTP до C#

**Унікальне:** Прив'язка через параметри методу (не `[BindProperty]`!). Порядок пошуку: Route → Query → Form → Body. `[FromRoute]`, `[FromQuery]`, `[FromForm]`, `[FromBody]`, `[FromHeader]`, `[FromServices]`. Custom Model Binders через `IModelBinder`. `TryUpdateModelAsync`. **Демо-проєкт:** `ProductSearchController` з фільтрацією `[FromQuery]`, сортуванням `[FromRoute]`, і custom Model Binder для `Money` типу.

---

#### 06. `06.views-viewdata-tempdata.md` — Views, ViewData, ViewBag, TempData і ViewModel

**Унікальне:** Файлова структура Views. **Три способи передачі даних:** `ViewData["key"]`, `ViewBag.Property`, strongly-typed ViewModel. `TempData` (cross-request). Partial Views у MVC-контексті. **Демо-проєкт:** `MovieController` — демонстрація всіх 3 способів передачі даних; TempData для Flash Messages після redirect.

---

### Блок 3: Розширений MVC (4 статті)

#### 07. `07.filters.md` — Filters: аспектно-орієнтоване програмування в MVC

**Унікальне:** Filter pipeline: Authorization → Resource → Action → Exception → Result. 5 типів фільтрів. Async варіанти. `[ServiceFilter]`, `[TypeFilter]`. Global filters через `MvcOptions.Filters`. **Демо-проєкт:** `ExecutionTimeFilter`, `MaintenanceModeFilter` (глобальний 503), `AuditLogFilter`.

---

#### 08. `08.areas.md` — Areas: структурування великих застосунків

**Унікальне:** Нема в Razor Pages і Minimal API. Структура папок. `[Area("Admin")]`, `MapAreaControllerRoute`. Cross-area links через `asp-area`. **Демо-проєкт:** застосунок з `Areas/Admin/` (Dashboard, ArticleManager, UserManager) та `Areas/Public/` (ArticleList, ArticleDetails).

---

#### 09. `09.view-components.md` — View Components: повторювані незалежні блоки UI

**Унікальне:** `ViewComponent` базовий клас, `InvokeAsync()`, `Views/Shared/Components/`. View Component vs Partial View vs Tag Helper. DI у View Component. **Демо-проєкт:** `ShoppingCartViewComponent`, `NotificationBellViewComponent`, `BreadcrumbViewComponent`.

---

#### 10. `10.display-editor-templates.md` — Display та Editor Templates

**Унікальне:** `DisplayTemplates/` і `EditorTemplates/`. `Html.DisplayFor()`, `Html.EditorFor()`. `[UIHint]` атрибут. Templates для складних типів (Money, DateRange, Address). **Демо-проєкт:** `ProductCard` Display Template, `MoneyEditor` Editor Template.

---

### Блок 4: Просунуті концепції (6 статей)

#### 11. `11.validation-advanced.md` — Валідація: IValidatableObject та FluentValidation

**Унікальне:** `IValidatableObject`, cross-field validation. Remote validation (`[Remote]`). Custom `ValidationAttribute`. **FluentValidation** інтеграція з MVC. **Демо-проєкт:** форма реєстрації з `[Remote]`, FluentValidation для складного замовлення (cross-field rules).

---

#### 12. `12.htmx.md` — HTMX: інтерактивність через HTML-атрибути

**Унікальне (окрема детальна стаття):** Філософія «HTML over the wire». Всі core атрибути: `hx-get/post/put/delete`, `hx-target`, `hx-swap` (всі режими), `hx-trigger`, `hx-include`, `hx-indicator`, `hx-push-url`. Extensions. SSE з HTMX. `hx-boost`. Out-of-band swaps. Порівняння з Alpine.js та React. **Демо-проєкт:** «Живий» список задач без перезавантаження сторінки — чистим HTMX.

---

#### 13. `13.ajax-htmx-mvc.md` — HTMX у MVC: інтерактивний UI без SPA

**Унікальне:** `JsonResult`, `PartialViewResult` для HTMX. Partial View як HTMX-відповідь. `HX-Redirect` заголовок. AntiForgery token з HTMX. **Демо-проєкт:** live-search, lazy loading таблиці, inline edit клітинки.

---

#### 14. `14.htmx-project.md` — Практичний проєкт: Каталог товарів з HTMX

**Унікальне:** Наскрізний проєкт від `dotnet new` до завершеного застосунку. Каталог товарів «ProductHub» що об'єднує всі знання зі статей 12–13: live-search з debounce, фільтрація по категоріям, infinite scroll, inline edit, модальне вікно створення товару, кошик з OOB swaps, toast-сповіщення, AntiForgery інтеграція. Покрокова побудова — кожен крок copy-paste.

---

#### 15. `15.file-upload.md` — Завантаження та обробка файлів

**Унікальне:** `IFormFile`, `IFormFileCollection`. Валідація (MIME, розмір, розширення). Збереження (wwwroot vs поза webroot). Streaming. `FileResult`, `PhysicalFileResult`. **Демо-проєкт:** `UserProfileController` — аватар, галерея, download protected файлів.

---

#### 16. `16.globalization-localization.md` — Глобалізація та Локалізація MVC

**Унікальне:** `IStringLocalizer<T>`, `IHtmlLocalizer<T>`, `IViewLocalizer`. Ресурсні файли `.resx`. `RequestLocalizationMiddleware`. Culture через URL, cookie, Accept-Language. **Демо-проєкт:** uk-UA / en-US / pl-PL перемикач у навбарі, локалізовані помилки валідації.

---

#### 17. `17.mvc-project.md` — Підсумковий проєкт: Блог-платформа

**Унікальне:** Наскрізний проєкт що поєднує **всі 16 попередніх статей**. MultiArea: PublicArea (читання, HTMX коментарі) + AdminArea (управління). Кожен крок будується на попередньому: Controllers → Routing → Model Binding → Views → Filters → Areas → View Components → Templates → Validation → HTMX → HTMX Project → File Upload → Localization.

---

## Послідовність і залежності

```
01. Патерн MVC (теорія)
      ↓
02. Від Razor Pages до MVC
      ↓
03. Controllers та Actions
      ↓
04. Routing в MVC ← (міст: Routing з Minimal API)
      ↓
05. Model Binding
      ↓
06. Views, ViewData, TempData, ViewModel
      ↓
07. Filters
08. Areas
09. View Components
10. Display/Editor Templates
      ↓
11. Validation Advanced ← (міст: Forms з Razor Pages)
12. HTMX (технологія)
      ↓
13. HTMX у MVC (інтеграція)
      ↓
14. HTMX Project (каталог товарів)
15. File Upload
16. Globalization/Localization
      ↓
17. Підсумковий проєкт
```

---

## Що НЕ включаємо і чому

| Тема | Причина виключення |
|---|---|
| `WebApplication.CreateBuilder`, DI | ✅ Вже Minimal API (01-03) |
| Middleware pipeline | ✅ Вже Minimal API (04) |
| Configuration, Options | ✅ Вже Minimal API (09-10) |
| Logging | ✅ Вже Minimal API (11-12) |
| Session/State Management | ✅ Вже Minimal API (13-14) |
| OpenAPI/Swagger | ✅ Вже Minimal API (16-17) |
| Static Files/Assets | ✅ Вже Minimal API (07-08) |
| Razor синтаксис | ✅ Вже Razor Pages (03) |
| Tag Helpers (asp-for etc.) | ✅ Вже Razor Pages (04) |
| Базова валідація DataAnnotations | ✅ Вже Razor Pages (05) |
| `_Layout`, `_ViewStart`, `_ViewImports` | ✅ Вже Razor Pages (01) |
| Authentication/Authorization | ✅ Окремий курс (03.auth) |
| Testing | ✅ Окремий курс (07.testing) |
| Caching | ✅ Окремий курс (06.caching) |
| Notifications/SignalR | ✅ Окремий курс (04.notifications) |
