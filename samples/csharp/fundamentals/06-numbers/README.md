# 06. Числа та перетворення типів

Приклади до лекції `content/01.csharp/01.fundamentals/06.numbers-and-conversions.md`.
Запуск усіх прикладів: `../run-all.sh 06-numbers < /dev/null`. Частина прикладів навмисно
завершується винятком (`checked.cs`, `checked-project.cs`, `checked-convert.cs`, `floating-overflow.cs`,
`int-divide.cs`, `parse-errors.cs`, `tasks/factorial-checked.cs`, `practice/wrap-table.cs`,
`practice/factorial-limits.cs`) — це очікувана поведінка, яку розбирає лекція.

| Файл | Що показує |
|---|---|
| `twos.cs` | доповняльний код, формат `B8` / `B32` |
| `overflow.cs` | переповнення по колу, пастка `long total = a + c` |
| `checked.cs`, `checked-project.cs` | `checked` / `unchecked`, `CheckForOverflowUnderflow` |
| `checked-il.cs` | `add` / `add.ovf`, `conv.i4` / `conv.ovf.i4` в IL |
| `floating-overflow.cs` | `checked` не стосується `double`, `decimal` перевіряє завжди |
| `implicit.cs`, `explicit.cs`, `checked-convert.cs` | неявні й явні перетворення, втрата точності, насичення |
| `rounding.cs` | приведення, `Math.Round` (до парного), `AwayFromZero`, `Floor`, `Ceiling`, `Convert.ToInt32` |
| `convert-parse.cs`, `parse-errors.cs`, `tryparse.cs` | `Parse`, `TryParse`, `Convert`; `dotnet run parse-errors.cs -- <рядок>` |
| `ieee.cs`, `int-divide.cs` | поглиблений розділ: біти `double`, нескінченність, `NaN`, порівняння з допуском |
| `bigint.cs` | поглиблений розділ: `BigInteger` |
| `culture.cs` | поглиблений розділ: розбір чисел у різних культурах |
| `errors/` | програми з помилками компіляції: `dotnet build errors/<файл>.cs` |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань |

IL: `dotnet build checked-il.cs -c Release -o out && ilspycmd -il out/checked-il.dll`.
