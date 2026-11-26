# 11. Масиви

Приклади до лекції `content/01.csharp/01.fundamentals/11.arrays.md`.

Запуск усіх прикладів: `../run-all.sh 11-arrays < /dev/null`. `index.cs` і `jagged-null.cs` навмисно
завершуються винятком. Програми з `errors/` запускайте через `dotnet build файл.cs`.

| Файл | Що показує |
|---|---|
| `array-forms.cs` | усі способи створити масив: `new T[n]`, ініціалізатори, вираз колекції, `new[]`, порожній, розмір зі змінної |
| `defaults.cs` | значення елементів за замовчуванням для `int`, `double`, `bool`, `char`, `string` |
| `index.cs` | `Length`, перший і останній елемент, запис за індексом, `IndexOutOfRangeException` |
| `algorithms.cs` | сума і середнє, максимум з індексом, лінійний пошук, підрахунок, розворот на місці |
| `parameter.cs` | масив як параметр: зміна елементів видна викликачу, присвоєння параметру — ні |
| `copy.cs` | `Clone`, `Array.Copy`, `CopyTo`, `[.. a]`, `ToArray` проти копії посилання |
| `resize.cs` | `Array.Resize` створює новий масив, інше посилання веде до старого |
| `array-methods.cs` | `IndexOf`, `LastIndexOf`, `Contains`, `Sort`, `Reverse`, `Fill`, `Clear`, `Min`/`Max`/`Sum` |
| `sort-strings.cs` | сортування українських слів за культурою uk-UA і за кодами символів |
| `binary-search.cs` | `BinarySearch` на відсортованому і невідсортованому масиві, від'ємний результат |
| `rectangular.cs` | `int[,]`: створення, індекс `[i, j]`, `Rank`, `Length`, `GetLength`, `foreach`, `int[,,]` |
| `jagged.cs` | `int[][]`: рядки різної довжини, вирази колекцій, `new int[][] { … }` |
| `jagged-null.cs` | `new int[2][]` — рядки `null`, `NullReferenceException` |
| `jagged-clone.cs` | `Clone` рваного масиву копіює посилання на рядки |
| `index-range.cs` | поглиблений розділ: `^1`, `1..3`, `..2`, `3..`, діапазон над масивом копіює |
| `span.cs` | поглиблений розділ: `Span<T>` як вікно без копіювання, параметр `ReadOnlySpan<int>` |
| `span-extension.cs` | поглиблений розділ: C# 14 викликає метод розширення для `ReadOnlySpan<int>` на масиві |
| `element-access.cs` | поглиблений розділ: IL `ldelem` / `Get`, перевірка меж і loop cloning через `DOTNET_JitDisasm` на Release-збірці |
| `errors/` | CS0650 (`cpp-declarator.cs`), CS0270 (`size-in-type.cs`), CS0847 (`init-mismatch.cs`), CS0820 (`var-initializer.cs`), CS9176 (`var-collection.cs`), CS1525 (`assign-initializer.cs`), CS9174 (`rect-collection.cs`), CS0022 (`rect-index.cs`, `jagged-index.cs`), CS0178 (`jagged-size.cs`), CS1929 (`span-extension-cs13.cs`) |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань |
