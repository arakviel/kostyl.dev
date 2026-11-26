# 08. Оператори та вирази

Приклади до лекції `content/01.csharp/01.fundamentals/08.operators.md`.

Запуск усіх прикладів: `../run-all.sh 08-operators < /dev/null`. `practice/seconds.cs` читає
число з клавіатури: `echo 90061 | dotnet run practice/seconds.cs`.

| Файл | Що показує |
|---|---|
| `overview.cs` | по одному прикладу на кожну групу операторів |
| `arith-all.cs` | усі арифметичні оператори для `int` і `double`, `++` і `--` |
| `arith.cs` | ціле ділення, знак остачі, `%` для `double`, ділення в `int` перед присвоєнням у `double`, `+` з рядками, `^` — не степінь |
| `min-div.cs` | `int.MinValue / -1` кидає `OverflowException` без `checked` |
| `increment.cs` | префіксний і постфіксний `++`, `k++ + ++k`, `m = m++` |
| `compare.cs` | усі оператори порівняння; `char` за кодом, `string ==`, `0.1 + 0.2 == 0.3` |
| `logical.cs` | `&&` і `\|\|` зі скороченим обчисленням проти `&` і `\|`; перевірка на `null` |
| `bitwise.cs` | `&`, `\|`, `^`, `~` над байтами у форматі `B8`; `~` для `byte` дає `int` |
| `shifts.cs` | `<<`, `>>`, `>>>` (C# 11), зсув `uint`, маскування кількості зсуву (`1 << 33`) |
| `assign-table.cs` | значення з таблиці складених операторів для `x = 12` |
| `compound.cs` | ланцюжок присвоєнь, складені оператори, приховане приведення `byte += 10`, `??=` |
| `precedence.cs` | пріоритет і асоціативність, `(x & 1) == 0` |
| `eval-order.cs` | порядок обчислення операндів зліва направо, `data[i] = i = 2` |
| `flags.cs` | поглиблений розділ: прапорці в бітах, `BitOperations` |
| `il-logic.cs` | поглиблений розділ: `&&` в IL (`brfalse.s` проти `and`); дивитися через `ilspycmd -il` на Release-збірці |
| `errors/` | `if-int.cs` (CS0029), `and-equals.cs` (CS0019), `string-less.cs` і `chain-compare.cs` (CS0019), `assign-literal.cs` (CS0131), `byte-plus.cs` (CS0266) |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань |
