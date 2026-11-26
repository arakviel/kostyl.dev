# 05. Значущі та посилальні типи, null

Приклади до лекції `content/01.csharp/01.fundamentals/05.value-and-reference-types.md`.
Запуск усіх прикладів, що компілюються: `../run-all.sh 05-value-reference < /dev/null`
(програми, які читають введення, отримають кінець введення).

| Файл | Що показує |
|---|---|
| `type-kinds.cs` | `Type.IsValueType` для вбудованих і бібліотечних типів |
| `copy.cs` | присвоєння `int`, `int[]`, `StringBuilder`: копія значення чи посилання |
| `equality.cs` | що порівнює `==`, `Equals`, `ReferenceEquals`, `SequenceEqual` |
| `allocations.cs` | скільки байтів виділяє в купі кожна операція |
| `boxing.cs`, `unbox-wrong.cs` | boxing, unboxing, `InvalidCastException` при розпакуванні в інший тип |
| `strings.cs` | незмінність рядка, інтернування |
| `anonymous.cs`, `anon-object.cs` | анонімні типи, `with`, рівність; передача як `object` |
| `null-ref.cs` | `NullReferenceException` і попередження CS8602 |
| `null-ops.cs` | `?.`, `?[]`, `??`, `??=` |
| `null-assign.cs`, `assign-rhs.cs` | поглиблений розділ: присвоєння через `?.` і `?[]` у C# 14 |
| `nrt-flow.cs` | поглиблений розділ: `NotNullWhen`, оператор `!`, `NullableAttribute` в IL |
| `errors/` | програми з помилками компіляції з лекції: `dotnet build errors/<файл>.cs` |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань |

Анонімний тип у декомпіляторі: `dotnet build anonymous.cs -c Release -o out && ilspycmd -lv CSharp1 out/anonymous.dll`.
