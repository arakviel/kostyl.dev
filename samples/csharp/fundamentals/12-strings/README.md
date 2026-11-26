# 12. Рядки

Приклади до лекції `content/01.csharp/01.fundamentals/12.strings.md`.

Запуск усіх прикладів: `../run-all.sh 12-strings < /dev/null`. `substring-error.cs` навмисно завершується
винятком. Заміри `concat-vs-builder.cs` запускайте в Release: `dotnet run -c Release concat-vs-builder.cs`.

| Файл | Що показує |
|---|---|
| `basics.cs` | `Length`, індексатор, перебір `for` і `foreach`, `ToCharArray` і `new string` |
| `string-forms.cs` | усі способи створити рядок: літерали, інтерполяція, `new string`, `Join`, `Concat`, `ToString`, `string.Empty` |
| `search.cs` | `IndexOf`, `LastIndexOf`, `IndexOfAny`, `Contains`, `StartsWith`, `EndsWith`, усі входження, `IsNullOrWhiteSpace` |
| `slicing.cs` | `Substring`, `Split` з опціями і кількома роздільниками, `Trim`, `TrimStart`, `Trim(символи)` |
| `substring-error.cs` | `ArgumentOutOfRangeException` з `Substring` |
| `modify.cs` | `Replace`, `Insert`, `Remove`, `ToUpper`, `ToLower`, `PadLeft`, `PadRight`, ланцюжок методів |
| `compare.cs` | `==`, `Equals` і `string.Compare` з `StringComparison`, пошук без урахування регістру |
| `culture-search.cs` | м'який перенос: `Contains` і `==` за кодами, `IndexOf`, `StartsWith`, `Compare` за культурою |
| `concat-vs-builder.cs` | замір `+=` проти `StringBuilder`: час і виділена пам'ять |
| `builder.cs` | методи `StringBuilder`: `Append`, `AppendLine`, `Insert`, `Replace`, індексатор, `Length--` |
| `capacity.cs` | як росте `Capacity` у `StringBuilder` |
| `unicode.cs` | поглиблений розділ: сурогатна пара, `Rune`, складена і розкладена `й`, `Normalize`, `StringInfo` |
| `turkish.cs` | поглиблений розділ: `ToUpper` і `ToLower` у tr-TR, `ToUpperInvariant`, `OrdinalIgnoreCase` |
| `span-parse.cs` | поглиблений розділ: розбір дати через `Substring` і через `ReadOnlySpan<char>`, виділені байти |
| `errors/` | CS0200 (`index-assign.cs`) |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань |
