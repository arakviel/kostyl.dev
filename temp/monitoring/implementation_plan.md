# План: 13.monitoring — Моніторинг ASP.NET (.NET 10) з Grafana LGTM стеком

## Параметри

- **Версія .NET:** 10
- **Стек:** LGTM (Loki + Grafana + Tempo + Prometheus)
- **Інфраструктура:** Docker Compose
- **Глибина:** Академічна (рівна суміш теорії і практики)
- **Мова:** Українська
- **Додаткові теми:** Grafana Alloy, k6, Pyroscope, OnCall/PagerDuty

---

## Передумови студента

Знає .NET 10 Minimal API, базовий Docker Compose, `ILogger` (з попередніх розділів курсу).

---

## Структура файлів

```
content/01.csharp/11.aspnet/13.monitoring/
├── .navigation.yml
├── 01.observability-intro.md
├── 02.health-checks.md
├── 03.dotnet-metrics.md
├── 04.prometheus-intro.md
├── 05.aspnet-prometheus.md
├── 06.promql.md
├── 07.grafana-setup.md
├── 08.grafana-dashboards-advanced.md
├── 09.serilog-structured-logging.md
├── 10.grafana-loki-alloy.md
├── 11.opentelemetry-tracing.md
├── 12.grafana-tempo.md
├── 13.lgtm-full-stack.md
├── 14.grafana-alerts.md
├── 15.grafana-oncall.md
├── 16.k6-load-testing.md
└── 17.pyroscope-profiling.md
```

---

## Трек 1: Метрики → Prometheus → Grafana

### 01. `01.observability-intro.md`

**Тема:** Спостережуваність (Observability) vs Моніторинг

**Зміст:**

- Що таке Observability: вміти задавати будь-яке питання про систему без передбачення питання заздалегідь
- Моніторинг vs Observability (реактивний vs проактивний підхід)
- Три стовпи: Метрики (Metrics), Логи (Logs), Трейси (Traces)
- Четвертий стовп: Profiling (огляд, детально — у файлі 17)
- Еволюція: `Console.WriteLine` → `ILogger` → structured logs → full observability
- Чому недостатньо лише логів у production
- Огляд усього LGTM стеку як "карта подорожі" курсу
- PlantUML: як три стовпи доповнюють один одного при розслідуванні інциденту
- Таблиця: "яке питання — який інструмент"

**Що вводиться вперше:** концепції observability, термінологія
**Залежності:** немає

---

### 02. `02.health-checks.md`

**Тема:** ASP.NET Core Health Checks

**Зміст:**

- Що таке health check і навіщо (Load Balancer, Kubernetes liveness/readiness, monitoring)
- Вбудований `IHealthCheck` інтерфейс
- Реєстрація через `AddHealthChecks()` та `MapHealthChecks()`
- Кастомні health checks: база даних, зовнішній API, диск, пам'ять
- Формати відповіді: `Healthy`, `Degraded`, `Unhealthy`
- Бібліотека `AspNetCore.HealthChecks.*` (community): SQL Server, Redis, RabbitMQ
- `HealthCheckUI` — веб-інтерфейс для health checks
- Окремі ендпоінти `/health/live` та `/health/ready` (Kubernetes патерн)
- Повний приклад: Minimal API + 3 кастомні checks + UI

**Що вводиться вперше:** Health Checks (перший крок до observability)
**Залежності:** 01

---

### 03. `03.dotnet-metrics.md`

**Тема:** Вбудовані метрики .NET 10

**Зміст:**

- Що таке метрика: числовий вимір у часі
- `System.Diagnostics.Metrics` API (.NET 6+, зрілий у .NET 10)
- Типи інструментів: `Counter<T>`, `ObservableCounter<T>`, `Histogram<T>`, `Gauge<T>`, `ObservableGauge<T>`, `UpDownCounter<T>`
- Детальне порівняння типів з прикладами та коли що обирати
- Що .NET 10 вже вимірює сам: `System.Runtime`, `Microsoft.AspNetCore.Hosting`, `Microsoft.AspNetCore.Http.Connections`, `System.Net.Http`, Kestrel
- Перелік вбудованих метрик ASP.NET Core з поясненням кожної
- Кастомні метрики для бізнес-логіки (приклад: лічильник замовлень, гістограма розміру кошика)
- `dotnet-counters` CLI: перегляд метрик у реальному часі без зовнішніх інструментів
- Tags/Labels в метриках: чому це важливо

**Що вводиться вперше:** `System.Diagnostics.Metrics` API, `dotnet-counters`
**Залежності:** 01

---

### 04. `04.prometheus-intro.md`

**Тема:** Prometheus — введення та самостійний запуск

**Зміст:**

- Що таке Prometheus: time-series database + scraping engine
- Pull-модель vs Push-модель: детальне порівняння, чому Prometheus обрав pull
- Архітектура: Prometheus Server, Exporters, Alertmanager, Pushgateway
- Типи метрик у Prometheus: Counter, Gauge, Histogram, Summary (порівняння з .NET типами)
- Формат метрик: text exposition format (як виглядає `/metrics` ендпоінт)
- `prometheus.yml`: `global`, `scrape_configs`, `static_configs`
- Запуск Prometheus через Docker Compose (поки що без .NET — scrape себе)
- Prometheus Web UI: Graph, Targets, Status, TSDB Status
- Labels: найважливіша концепція Prometheus, cardinality

**Що вводиться вперше:** Prometheus, Docker Compose для моніторингу, `/metrics` формат
**Залежності:** 03

---

### 05. `05.aspnet-prometheus.md`

**Тема:** Підключення ASP.NET Core .NET 10 до Prometheus

**Зміст:**

- OpenTelemetry SDK: що це і чому саме він (vendor-neutral)
- Пакети: `OpenTelemetry`, `OpenTelemetry.Extensions.Hosting`, `OpenTelemetry.Instrumentation.AspNetCore`, `OpenTelemetry.Instrumentation.Runtime`, `OpenTelemetry.Exporter.Prometheus.AspNetCore`
- Реєстрація OTel MeterProvider у Minimal API
- Автоматична інструментація ASP.NET Core та Runtime метрик
- Публікація `/metrics` ендпоінту (тільки для внутрішнього доступу — security!)
- Оновлення `prometheus.yml`: додаємо scrape нашого .NET додатку
- Оновлення Docker Compose: додаємо .NET app контейнер
- Перевірка в Prometheus UI: бачимо реальні метрики з нашого додатку
- Приклад кастомної метрики через OTel + перевірка в Prometheus

**Що вводиться вперше:** OpenTelemetry SDK, інтеграція .NET → Prometheus
**Залежності:** 04

---

### 06. `06.promql.md`

**Тема:** PromQL — мова запитів Prometheus

**Зміст:**

- Instant vector vs Range vector: ключова відмінність
- Типи даних: instant vector, range vector, scalar, string
- Базові селектори: `{}` фільтрація за labels, `=`, `!=`, `=~`, `!~`
- **Counter функції:** `rate()`, `increase()`, `irate()` — різниця та коли що
- **Histogram функції:** `histogram_quantile()` — P50, P95, P99 latency
- **Агрегації:** `sum`, `avg`, `max`, `min`, `count`, `topk`, `bottomk`
- Клаузи `by()` та `without()`: групування результатів
- Бінарні оператори: арифметика між метриками
- Практичні запити для ASP.NET 10:
    - RPS (requests per second)
    - Error rate (%)
    - P95 latency
    - Active HTTP connections
    - GC pause time
    - Thread pool queue length
- Subqueries: запити над запитами

**Що вводиться вперше:** PromQL
**Залежності:** 05

---

### 07. `07.grafana-setup.md`

**Тема:** Grafana — встановлення та перший дашборд

**Зміст:**

- Що таке Grafana: платформа для візуалізації даних з будь-яких джерел
- Додавання Grafana до існуючого Docker Compose (разом з Prometheus)
- Перший вхід, зміна пароля, структура UI
- **Datasources:** що це, додавання Prometheus datasource
- **Panels:** типи — Time series, Stat, Gauge, Bar gauge, Table, Pie chart
- Detailing: як налаштувати вісі, одиниці виміру (ms, bytes, req/s), кольори порогів
- Перший дашборд з нуля: 4 панелі для ASP.NET (RPS, Error rate, P95 latency, Active connections)
- `Explore`: ad-hoc запити без дашборду
- Grafana provisioning через файли: `datasources.yml` (datasource as code)

**Що вводиться вперше:** Grafana, дашборди, Explore
**Залежності:** 06

---

### 08. `08.grafana-dashboards-advanced.md`

**Тема:** Grafana дашборди — просунутий рівень

**Зміст:**

- **Variables:** Query variables (з Prometheus label values), Custom variables, Interval variables
- Використання variables у PromQL: `$instance`, `$job`, `$__rate_interval`
- **Annotations:** маркування подій на графіку (деплой, інцидент)
- **Repeat panels/rows:** один шаблон → багато панелей по instance
- **Transformations:** Join, Filter, Rename, Calculate field — всередині Grafana без PromQL
- **Links:** посилання між дашбордами, drill-down
- **Provisioning дашбордів як код:** `dashboards.yml` + JSON файли, GitOps підхід
- Імпорт готових дашбордів з grafana.com:
    - ASP.NET Core dashboard (ID: 19924 або актуальний)
    - .NET Runtime Metrics dashboard
    - Node Exporter (для системних метрик Docker хоста)

**Що вводиться вперше:** Variables, provisioning as code, готові дашборди
**Залежності:** 07

---

## Трек 2: Логи → Loki (потребує Трек 1 до файлу 07)

### 09. `09.serilog-structured-logging.md`

**Тема:** Serilog та структуровані логи в .NET 10

**Зміст:**

- Проблема неструктурованих логів у production: `grep` не масштабується
- Structured logging: лог як об'єкт, не рядок
- Serilog vs вбудований `ILogger`: порівняння, коли що обирати
- Встановлення: `Serilog.AspNetCore`, інтеграція з .NET 10 DI
- **Sinks:** `Console` (з форматом JSON), `File` (rolling), огляд інших
- **Enrichers:** `WithMachineName()`, `WithThreadId()`, `WithCorrelationId()` (через `Serilog.Context`)
- **Destructuring:** `@` оператор — логування складних об'єктів
- **Log levels та фільтрація:** `MinimumLevel`, `Override` per namespace
- `LogContext.PushProperty`: динамічне збагачення логів у middleware
- Correlation ID middleware: як пов'язати всі логи одного запиту
- Конфігурація через `appsettings.json` vs код
- Повний приклад: Minimal API з Serilog, correlation ID, JSON output

**Що вводиться вперше:** Serilog, structured logging, correlation ID
**Залежності:** 01 (незалежна від Prometheus треку, але потрібна для файлу 10)

---

### 10. `10.grafana-loki-alloy.md`

**Тема:** Grafana Loki + Grafana Alloy — централізовані логи

**Зміст:**

- Що таке Loki: "Prometheus для логів" — індексує лише metadata (labels), не текст
- Loki vs Elasticsearch: детальне порівняння (cost, scalability, query model)
- **Grafana Alloy:** новий уніфікований агент (замінює Promtail, Grafana Agent) — що змінилось і чому
- Архітектура Alloy: компоненти, pipelines, конфігурація `.alloy` файл
- Docker Compose: додаємо Loki + Alloy
- Alloy конфігурація: `local.file` → `loki.process` → `loki.write`
- Serilog Loki sink (`Serilog.Sinks.Grafana.Loki`): пряма відправка без файлу
- Порівняння підходів: file → Alloy vs direct Loki sink
- **LogQL основи:** `{job="api"}`, `|=` (contains), `|~` (regex), `| json`, `| line_format`
- LogQL метрики: `rate()`, `count_over_time()` — метрики з логів
- Grafana Explore з Loki: пошук логів, Live tail
- Додавання Loki datasource у Grafana provisioning

**Що вводиться вперше:** Loki, Alloy, LogQL
**Залежності:** 09, 07

---

## Трек 3: Трейси → Tempo (потребує файл 05 для OTel SDK, файл 07 для Grafana)

### 11. `11.opentelemetry-tracing.md`

**Тема:** Distributed Tracing та OpenTelemetry в .NET 10

**Зміст:**

- Проблема: як дослідити запит, що пройшов через 5 мікросервісів?
- Що таке distributed tracing: Trace, Span, SpanContext
- Ієрархія spans: root span → child spans → листові spans
- **W3C TraceContext:** стандарт propagation (заголовки `traceparent`, `tracestate`)
- `Activity` API в .NET 10: це і є трейсинг (OTel побудований поверх нього)
- `ActivitySource` та `Activity`: створення кастомних spans
- `ActivityEvent`: логування подій всередині span
- `ActivityTag`: атрибути span (схоже на labels у метриках)
- OTel `TracerProvider` та `AddSource()`: реєстрація інструментації
- Автоматична інструментація: `AddAspNetCoreInstrumentation()`, `AddHttpClientInstrumentation()`, `AddEntityFrameworkCoreInstrumentation()`
- Sampling: чому не можна зберігати 100% трейсів у production, AlwaysOn vs TraceIdRatioBased vs ParentBased
- Кореляція трейсів з логами: `TraceId` та `SpanId` у Serilog enricher

**Що вводиться вперше:** Tracing, Activity API, W3C TraceContext, sampling
**Залежності:** 05 (OTel SDK вже є)

---

### 12. `12.grafana-tempo.md`

**Тема:** Grafana Tempo — зберігання та перегляд трейсів

**Зміст:**

- Що таке Tempo: object storage-first tracing backend (S3, GCS, Azure Blob)
- Tempo vs Jaeger vs Zipkin: коли що обирати
- Tempo архітектура: Distributor, Ingester, Querier, Compactor
- Docker Compose: додаємо Tempo з local storage (для розробки)
- OTel конфігурація: `AddOtlpExporter()` → Tempo (OTLP протокол)
- Tempo конфіг: `tempo.yml` — storage, receivers, search
- Grafana Tempo datasource: додавання через provisioning
- **TraceQL:** мова запитів Tempo — `{}`, `{ .http.status_code = 500 }`, `| select()`
- Search: пошук трейсів за service, duration, attributes
- Span detail view: аналіз одного трейсу
- **Derived fields у Loki datasource:** автоматичне посилання з лога (TraceId) → Tempo трейс
- **Exemplars:** посилання з Prometheus метрики → конкретний трейс (потребує підтримки в OTel exporter)

**Що вводиться вперше:** Tempo, OTLP, TraceQL, derived fields
**Залежності:** 11, 07

---

## Трек 4: Повний стек + Alerting + Додаткові інструменти

### 13. `13.lgtm-full-stack.md`

**Тема:** Повний LGTM стек — все разом у Docker Compose

**Зміст:**

- Огляд архітектури: всі компоненти та їх взаємодія
- Єдиний `docker-compose.yml` з усіма сервісами:
    - `.NET 10 API` (наш додаток)
    - `Prometheus`
    - `Grafana`
    - `Loki`
    - `Grafana Alloy`
    - `Tempo`
- Мережева конфігурація: internal network для сервісів, зовнішній доступ лише до Grafana
- Volumes та persistence: що треба зберігати між рестартами
- Health checks для Docker Compose сервісів (depends_on з condition)
- Grafana provisioning: datasources + dashboards в одному репо
- **Correlations у Grafana Explore:**
    - Metrics → Traces (через Exemplars)
    - Logs → Traces (через Derived fields)
    - Traces → Logs (через TraceId пошук у Loki)
- Сценарій інциденту: від alert → metrics → logs → traces → знайдено причину
- `.env` файл для конфігурації (без хардкоду паролів!)
- Production-ready checklist: що змінити перед виходом у prod

**Що вводиться вперше:** Correlations між трьома стовпами, production considerations
**Залежності:** 10, 12

---

### 14. `14.grafana-alerts.md`

**Тема:** Grafana Unified Alerting

**Зміст:**

- Grafana Alerting vs Prometheus Alertmanager: різниця, чому Grafana Unified Alerting
- **Alert Rule:** умова спрацювання (PromQL або LogQL запит), pending period, annotations
- **Alert states:** Normal → Pending → Firing → Resolved
- Групування alert rules у папки та групи
- **Contact Points:** Email, Telegram Bot, Slack, Webhook
    - Детальна настройка Telegram: BotFather, chat ID, повідомлення
    - Детальна настройка Email: SMTP конфігурація
- **Notification Policies:** маршрутизація alerts до contact points, matchers
- **Silences:** тимчасове вимкнення alert (planned maintenance)
- **Alert History:** перегляд минулих спрацювань
- Практичні alert rules для ASP.NET:
    - Error rate > 5%
    - P95 latency > 1s
    - Health check Unhealthy
    - Memory usage > 80%
    - Pod restart count (якщо Kubernetes)

**Що вводиться вперше:** Grafana Alerting, Contact Points, Notification Policies
**Залежності:** 13

---

### 15. `15.grafana-oncall.md`

**Тема:** Grafana OnCall — управління черговістю та інцидентами

**Зміст:**

- Що таке On-Call і чому це важливо: інцидент о 3:00 ночі
- Grafana OnCall (open-source) vs PagerDuty: порівняння
- Встановлення OnCall як Docker Compose сервісу
- **On-Call Schedules:** розклад чергувань, ротація команди, overrides
- **Escalation Chains:** ланцюжок ескалації (спробуй чергового → через 5хв → team lead → ...)
- **Integrations:** Grafana Alerting → OnCall (автоматичне routing alerts)
- Мобільний додаток Grafana OnCall: push notifications
- **PagerDuty інтеграція:** OnCall як міст між Grafana та PagerDuty
- **Incident lifecycle:** Firing → Acknowledged → Resolved
- Post-mortem culture: що робити після інциденту

**Що вводиться вперше:** OnCall, incident management, escalation
**Залежності:** 14

---

### 16. `16.k6-load-testing.md`

**Тема:** k6 — навантажувальне тестування та спостереження через LGTM

**Зміст:**

- Що таке навантажувальне тестування і навіщо (до, а не після production)
- k6 vs JMeter vs Locust: порівняння
- Встановлення k6 (Docker або binary)
- **k6 скрипти:** TypeScript/JavaScript, `http.get()`, `http.post()`, `check()`, `sleep()`
- **Virtual Users (VU) та сценарії:** `constant-vus`, `ramping-vus`, `constant-arrival-rate`
- **k6 метрики:** вбудовані (`http_req_duration`, `http_req_failed`, `vus`) та кастомні `Trend`, `Counter`
- **k6 → Prometheus Remote Write:** передача метрик k6 до нашого Prometheus
- Grafana k6 дашборд: імпорт готового дашборду
- **Практичний сценарій:** рампінг від 10 до 500 VU за 5 хвилин
- Спостереження під навантаженням через LGTM стек: що деградує першим
- Порогові значення (`thresholds`): автоматичний fail при порушенні SLO
- Результати k6 у CI/CD pipeline

**Що вводиться вперше:** k6, load testing, Remote Write
**Залежності:** 13

---

### 17. `17.pyroscope-profiling.md`

**Тема:** Pyroscope — continuous profiling, четвертий стовп observability

**Зміст:**

- Що таке profiling і чим відрізняється від трейсингу
- Continuous Profiling vs on-demand profiling (вмикаємо завжди, не тільки при підозрі)
- **Flame graphs:** як читати, що означає ширина блоку
- Що можна профілювати: CPU, Heap allocations, Goroutines, Block, Mutex
- **Pyroscope:** архітектура, storage, query language
- Додавання Pyroscope до Docker Compose
- **.NET 10 + Pyroscope SDK:** `Pyroscope.Profiler.Native` (auto-instrumentation) або managed SDK
- Конфігурація: `applicationName`, labels, push interval
- Grafana Pyroscope datasource та `Explore Profiles`
- **Кореляція профілів з трейсами:** `pyroscope.profile.id` у OTel span → перехід від трейсу до flame graph
- Практичний приклад: знаходимо memory leak через continuous profiling
- Коли profiling замінює трейсинг і навпаки

**Що вводиться вперше:** Pyroscope, continuous profiling, flame graphs
**Залежності:** 13

---

## Граф залежностей

```
01 (Observability Intro)
 ├── 02 (Health Checks)
 ├── 03 (Dotnet Metrics)
 │    └── 04 (Prometheus Intro)
 │         └── 05 (ASP.NET → Prometheus)
 │              ├── 06 (PromQL)
 │              │    └── 07 (Grafana Setup)
 │              │         └── 08 (Grafana Dashboards Advanced)
 │              │              └── [потрібен для 10 та 12]
 │              └── 11 (OTel Tracing)
 │                   └── 12 (Grafana Tempo) ──────────┐
 └── 09 (Serilog)                                      │
      └── 10 (Loki + Alloy) ──────────────────────────┤
                                                       ▼
                                              13 (LGTM Full Stack)
                                               ├── 14 (Grafana Alerts)
                                               │    └── 15 (OnCall)
                                               ├── 16 (k6)
                                               └── 17 (Pyroscope)
```

---

## Технічний стек (пакети NuGet)

```xml
<!-- OpenTelemetry Core -->
<PackageReference Include="OpenTelemetry" />
<PackageReference Include="OpenTelemetry.Extensions.Hosting" />

<!-- Instrumentation -->
<PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" />
<PackageReference Include="OpenTelemetry.Instrumentation.Runtime" />
<PackageReference Include="OpenTelemetry.Instrumentation.Http" />
<PackageReference Include="OpenTelemetry.Instrumentation.EntityFrameworkCore" />

<!-- Exporters -->
<PackageReference Include="OpenTelemetry.Exporter.Prometheus.AspNetCore" />
<PackageReference Include="OpenTelemetry.Exporter.OpenTelemetryProtocol" />

<!-- Serilog -->
<PackageReference Include="Serilog.AspNetCore" />
<PackageReference Include="Serilog.Enrichers.CorrelationId" />
<PackageReference Include="Serilog.Sinks.Grafana.Loki" />

<!-- Health Checks -->
<PackageReference Include="AspNetCore.HealthChecks.UI" />
<PackageReference Include="AspNetCore.HealthChecks.UI.Client" />
<PackageReference Include="AspNetCore.HealthChecks.UI.InMemory.Storage" />

<!-- Pyroscope -->
<PackageReference Include="Pyroscope" />
```

## Docker Compose сервіси (фінальний стек)

| Сервіс       | Image                    | Порт       | Призначення          |
| ------------ | ------------------------ | ---------- | -------------------- |
| `api`        | custom .NET 10           | 8080       | Наш ASP.NET додаток  |
| `prometheus` | prom/prometheus:latest   | 9090       | Збір метрик          |
| `grafana`    | grafana/grafana:latest   | 3000       | Візуалізація (UI)    |
| `loki`       | grafana/loki:latest      | 3100       | Зберігання логів     |
| `alloy`      | grafana/alloy:latest     | 12345      | Агент збору логів    |
| `tempo`      | grafana/tempo:latest     | 3200, 4317 | Зберігання трейсів   |
| `pyroscope`  | grafana/pyroscope:latest | 4040       | Continuous profiling |

---

_Створено: 2026-05-27_
_Версія: 1.0_
