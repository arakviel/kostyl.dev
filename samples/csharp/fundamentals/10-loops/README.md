# 10. Цикли

Приклади до лекції `content/01.csharp/01.fundamentals/10.loops.md`.

Запуск усіх прикладів: `../run-all.sh 10-loops < /dev/null`. `byte-counter.cs`, `off-by-one.cs` і
`modify-in-foreach.cs` навмисно завершуються винятком. Програми з `errors/` запускайте через
`dotnet build файл.cs`: `while-semicolon.cs` і `byte-255.cs` компілюються, але не завершуються.

| Файл | Що показує |
|---|---|
| `for-steps.cs` | порядок частин `for`: стан змінних наприкінці кожної ітерації |
| `for-forms.cs` | усі форми `for`: угору, униз, крок, дві змінні, лічильник ззовні, `for (;;)`, без дужок |
| `while-forms.cs` | усі форми `while` і `do-while`: передумова, складена умова, `while (true)`, післяумова |
| `digits.cs` | підрахунок цифр через `while` і `do-while`: різниця для 0 |
| `foreach-forms.cs` | `foreach` по масиву, з `var`, по рядку, по `List<T>`, по `Enumerable.Range`, по кортежах |
| `double-prices.cs` | зміна елементів масиву через `for` з індексом |
| `foreach-expand.cs` | `foreach` і той самий перебір через `GetEnumerator`, `MoveNext`, `Current` |
| `modify-in-foreach.cs` | `InvalidOperationException` при зміні `List` під час `foreach` |
| `remove-backward.cs` | видалення зі списку циклом `for` від кінця |
| `break-continue.cs` | `continue` пропускає від'ємні значення, `break` зупиняє пошук |
| `switch-in-loop.cs` | `break` у `switch` не зупиняє цикл; прапорець в умові циклу |
| `nested.cs` | вкладені цикли з межею, що залежить від зовнішнього лічильника |
| `nested-exit.cs` | вихід із вкладених циклів: лише `break`, прапорець, `goto`, `return` |
| `pitfalls.cs` | зміна лічильника в тілі; дробовий лічильник не досягає 1.0 |
| `byte-counter.cs` | лічильник `byte` до 255 включно в `checked`: `OverflowException` |
| `off-by-one.cs` | `<=` замість `<`: `IndexOutOfRangeException` |
| `foreach-il.cs` | поглиблений розділ: IL `foreach` для масиву, рядка і `List<T>`; дивитися через `ilspycmd -il` на Release-збірці |
| `array-in-foreach.cs` | поглиблений розділ: зміна масиву під час `foreach` без винятку |
| `stopwatch.cs` | поглиблений розділ: `Stopwatch`, Debug проти Release (`dotnet run -c Release stopwatch.cs`) |
| `unused-result.cs` | поглиблений розділ: JIT викидає обчислення без використаного результату |
| `errors/` | CS0136 (`for-shadow.cs`), CS0165 (`loop-unassigned.cs`), CS0029 (`while-int.cs`), CS0642 (`empty-for.cs`, `while-semicolon.cs`), CS0103 (`do-scope.cs`), CS1656 (`foreach-assign.cs`), CS1579 (`foreach-int.cs`), CS0159 і CS0164 (`goto-into.cs`), CS0652 (`byte-256.cs`), без попередження (`byte-255.cs`) |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань (`deposit-guard.cs` — крок 3 завдання 3, `remove-fixed.cs` — крок 3 завдання 4) |
