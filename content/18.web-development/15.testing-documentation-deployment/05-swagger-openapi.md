# Swagger, OpenAPI, Scalar та Arazzo

## Короткий зміст

У цій лекції вивчається автоматична генерація інтерактивної документації API через OpenAPI специфікацію:

- **Специфікація OpenAPI 3.0** — industry standard для опису REST API, структура: info, servers, paths, components (schemas, securitySchemes), tags, формат JSON або YAML
- **@nestjs/swagger інтеграція** — встановлення пакету, налаштування через `SwaggerModule.setup('/api/docs', app, document)`, генерація OpenAPI document через `SwaggerModule.createDocument(app, config)`
- **Декоратори для endpoints** — `@ApiTags()` для групування endpoints, `@ApiOperation()` для опису операції (summary, description), `@ApiResponse()` для документування можливих відповідей з кодами та схемами, `@ApiParam()`, `@ApiQuery()`, `@ApiBody()`
- **Декоратори для DTO** — `@ApiProperty()` для документування полей з типом, description, example, required, `@ApiPropertyOptional()` для опціональних полів, enum для обмеження значень
- **Автентифікація у Swagger** — `@ApiBearerAuth()` для JWT endpoints, налаштування security schemes у SwaggerConfig, UI для введення Bearer токена та тестування protected routes
- **Версіонування API** — підтримка multiple versions через окремі Swagger documents, URL versioning (/v1, /v2), header versioning, deprecation notices
- **Scalar** — сучасна альтернатива Swagger UI з кращим дизайном, інтеграція через `@scalar/nestjs-api-reference`, features: theme customization, improved navigation, better request/response examples, OpenAPI 3.1 підтримка
- **Arazzo Specification** — офіційна специфікація від OpenAPI Initiative для описування workflows та послідовностей API викликів, визначення multi-step processes з умовною логікою, передача параметрів між кроками (outputs → inputs), success/failure criteria, use cases: onboarding flows, checkout processes, approval workflows, testing scenarios
- **Генерація клієнтів** — автоматична генерація TypeScript/JavaScript клієнтів з OpenAPI spec через openapi-generator, SDK для frontend без ручного написання

Розглядаються практичні приклади: налаштування Swagger для NestJS проєкту, документування CRUD endpoints, switching на Scalar UI, опис складного workflow через Arazzo Specification.
