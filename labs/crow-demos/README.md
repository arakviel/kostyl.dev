# crow-demos

Демо-проєкти до серії лекцій «Веб-сервер на Crow» (`content/02.cpp/992.crow-web`).
Одна папка — одна лекція. Усі демо збираються одним CMake-проєктом.

| Папка | Лекція | Що показує |
| ----- | ------ | ---------- |
| `01-http-basics` | Веб, клієнт-сервер і HTTP | сервер на сирих сокетах, структура HTTP-повідомлення |
| `02-hello-crow` | Перший сервер на Crow | vcpkg + CMake, текст/HTML/JSON відповіді |
| `03-routes` | Маршрути й параметри | `<int>`, `<string>`, `<path>`, query-параметри |
| `04-request-response` | Request і Response | заголовки, статус-коди, типи відповідей, власний 404 |
| `05-crud-todo` | HTTP-методи і CRUD | TODO API: POST, GET, PUT, PATCH, DELETE |
| `06-rest-validation` | REST-дизайн і валідація | рівні валідації, 400/409/415, пагінація, фільтри |
| `07-json-crow` | JSON у Crow | `crow::json::rvalue` і `wvalue`, помилки доступу |
| `08-json-dto` | nlohmann/json і DTO | автоматична серіалізація, DTO, типізовані винятки |
| `09-middleware-chain` | Middleware: ланцюжок | порядок виконання, контекст, ранній вихід |
| `10-middleware-practice` | Middleware на практиці | журнал, API-ключ, rate limit (429), CORS |
| `11-templates` | Шаблони Mustache | MVC, цикли, умови, partials, екранування |
| `12-static-files` | Статика й структура проєкту | `/static`, MIME, захист від path traversal |
| `13-dal-evolution` | Шар доступу до даних | 4 етапи: прямий доступ, функції, DAO, Active Record |
| `14-repository-tests` | Repository, DI, тести | інтерфейс, 2 реалізації, сервіс, doctest + ctest |
| `15-sqlite-repository` | SQLite | SQL, prepared statements, ін'єкція, транзакції |
| `16-sessions-login` | Cookies і сесії | `Set-Cookie`, сесії, argon2id, вхід і вихід |
| `17-rbac-security` | RBAC і безпека | ролі, CSRF, fixation, IDOR, обмеження входу |

Демо 15 містить копію доменного коду з демо 14, щоб кожна папка була самодостатньою.

## Збірка

Потрібні: CMake 3.20+, компілятор C++17, [vcpkg](https://github.com/microsoft/vcpkg) зі змінною `VCPKG_ROOT`.

```bash
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
cmake --build build
```

Перша конфігурація завантажує й збирає залежності з `vcpkg.json` (crow, nlohmann-json, sqlite3, doctest, argon2).

Збирати окреме демо можна за назвою цілі, наприклад `cmake --build build --target hello_crow`.

## Запуск

Виконувані файли лежать у `build/<папка>/`. Більшість приймає порт першим аргументом (за замовчуванням 8080):

```bash
./build/02-hello-crow/hello_crow 8082
curl -i http://localhost:8082/health
```

Якщо порт зайнятий (`lsof -i :8080`), відповідь може прийти від чужої програми.

Деякі демо мають додаткові аргументи:

```bash
./build/14-repository-tests/repository_api 8080 json users.json
./build/15-sqlite-repository/sqlite_repository_api 8080 sqlite users.db
./build/13-dal-evolution/dal_stage3_dao 8080 users.json
```

У демо 17 є тестові користувачі `alice` (admin), `bob` (editor), `carol` (user) з паролями `<ім'я>-password`.

## Тести

Демо 14 і 15 мають модульні тести на doctest:

```bash
cd build && ctest --output-on-failure
```

## Перевірено

macOS (arm64, AppleClang 21, Crow 1.3.5 через vcpkg): усі демо зібрані з нуля й запущені, тести проходять. Код для Windows (Winsock у `01-http-basics`) і Linux не запускався.
