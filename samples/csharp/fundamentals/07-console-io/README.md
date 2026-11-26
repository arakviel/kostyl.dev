# 07. Консольне введення та виведення

Приклади до лекції `content/01.csharp/01.fundamentals/07.console-io.md`.
Більшість прикладів задає культуру uk-UA першим рядком, щоб вивід збігався з тим,
що бачить користувач з українськими регіональними налаштуваннями.

Запуск усіх прикладів: `../run-all.sh 07-console-io < /dev/null`. Програми з `ReadKey`
(`readkey.cs`, `practice/menu.cs`) запускайте вручну в терміналі: з перенаправленим введенням
вони кидають `InvalidOperationException`, як описано в лекції.

| Файл | Що показує |
|---|---|
| `write.cs` | `Write`, `WriteLine`, друк масиву |
| `three-ways.cs`, `braces.cs` | склеювання, складене форматування, інтерполяція; `{{ }}` і `?:` в інтерполяції |
| `format-numbers.cs`, `format-rounding.cs` | стандартні й власні формати чисел; як вони округлюють половину |
| `alignment.cs` | вирівнювання і таблиці |
| `dates.cs` | формати дати й часу, пастка `mm` / `MM` |
| `read-codes.cs` | `Console.Read`: `printf 'AB\n' \| dotnet run read-codes.cs` |
| `readkey.cs` | `Console.ReadKey`, `intercept: true` |
| `input-loop.cs` | цикл безпечного введення з `TryParse` |
| `colors.cs`, `cursor.cs` | поглиблений розділ: кольори, позиція курсора |
| `streams.cs` | поглиблений розділ: stdout і stderr, `dotnet run streams.cs > out.txt` |
| `encoding.cs` | поглиблений розділ: кодування консолі |
| `datetime-more.cs` | поглиблений розділ: `DateOnly`, `TimeOnly`, `TimeSpan` |
| `errors/` | `ternary.cs` (CS8361) і `format-missing.cs` (`FormatException` під час роботи) |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань |
