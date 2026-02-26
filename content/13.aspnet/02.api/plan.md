---
title: HTTP API (REST)
description: Повний навчальний модуль з проєктування та розробки HTTP API (REST) на основі ASP.NET Core Minimal API.
---

# HTTP API (REST)

Цей модуль охоплює всі аспекти проєктування та розробки HTTP API — від базових концепцій до просунутих паттернів. Матеріал базується на книзі Сергія Константинова «API» та адаптований для практичної розробки на **ASP.NET Core Minimal API**.

::card-group

::card{title="01. Що таке API" icon="i-lucide-plug" to="./01.what-is-api"}
Визначення API, клієнт-серверна архітектура, типи API.
::

::card{title="02. Формати даних" icon="i-lucide-braces" to="./02.data-formats"}
JSON, XML, TOML, бінарні формати. Стиснення: gzip, brotli.
::

::card{title="03. Парадигми API та REST" icon="i-lucide-git-branch" to="./03.api-paradigms-rest"}
RPC → REST. 6 обмежень Філдінга. HTTP API vs gRPC vs GraphQL.
::

::card{title="04. HTTP-методи та статус-коди" icon="i-lucide-arrow-right-left" to="./04.http-methods-status-codes"}
GET/POST/PUT/DELETE/PATCH. URL-адресація. Заголовки. Коди 1xx–5xx.
::

::card{title="05. Організація API за REST" icon="i-lucide-layers" to="./05.rest-organizing"}
Stateless-дизайн, мікросервіси, ETag, JWT-авторизація.
::

::card{title="06. URL та CRUD" icon="i-lucide-link" to="./06.url-design-crud"}
Номенклатура URL, path vs query, CRUD від 2 URL до 10.
::

::card{title="07. Іменування та стандарти" icon="i-lucide-text-cursor-input" to="./07.api-design-naming"}
Явне > неявне, конкретні імена, стандарти дат і валют.
::

::card{title="08. Валідація та ліміти" icon="i-lucide-shield-check" to="./08.api-design-validation"}
Обмеження, валідація введення, інформативні помилки.
::

::card{title="09. Помилки в HTTP API" icon="i-lucide-alert-triangle" to="./09.error-handling-http"}
4xx, 5xx, RFC 9457, три підходи до системи помилок.
::

::card{title="10. Ідемпотентність" icon="i-lucide-repeat" to="./10.idempotency-sync"}
Токени, чернетки, оптимістичний контроль паралелізму.
::

::card{title="11. Пагінація" icon="i-lucide-list" to="./11.pagination-lists"}
limit/offset, курсори, мутабельні та іммутабельні списки.
::

::card{title="12. Безпека та кешування" icon="i-lucide-lock" to="./12.security-auth"}
TLS, JWT, UUID, rate limiting, Cache-Control, i18n.
::

::card{title="13. Процес проєктування" icon="i-lucide-clipboard-check" to="./13.api-design-process"}
Покроковий алгоритм, code style, OpenAPI/Swagger.
::

::
