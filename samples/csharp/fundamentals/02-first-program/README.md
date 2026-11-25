# 02. Перша програма: SDK, CLI, IDE і налагоджувач

Приклади до лекції `content/01.csharp/01.fundamentals/02.first-program-and-tooling.md`.

| Файл | Що показує |
|---|---|
| `hello.cs` | file-based програма, shebang, `args` |
| `package.cs` | `#:package Humanizer` |
| `debug-vs-release.cs` | `#if DEBUG`, різниця швидкості Debug і Release |
| `average.cs` | програма з помилкою для налагоджувача |
| `Hello/` | проєкт з шаблону `dotnet new console` |
| `Classic/` | проєкт з шаблону `dotnet new console --use-program-main` |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | матеріали практичних завдань |

Запуск: `dotnet run hello.cs -- a b c`, `dotnet run debug-vs-release.cs -c Release`, `dotnet run --project Hello`.
