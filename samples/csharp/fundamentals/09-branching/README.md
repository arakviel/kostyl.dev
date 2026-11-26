# 09. Розгалуження: if, ?:, switch, шаблони

Приклади до лекції `content/01.csharp/01.fundamentals/09.branching-and-switch.md`.

Запуск усіх прикладів: `../run-all.sh 09-branching < /dev/null`. Попередження компілятора
(CS8509, CS9336, CS0665) видно лише при першій збірці файлу; щоб побачити їх повторно,
використовуйте `dotnet build файл.cs`.

| Файл | Що показує |
|---|---|
| `if-forms.cs` | усі форми запису `if`: без `else`, з `else`, ланцюжок, вкладений, без дужок, складена умова |
| `dangling-else.cs` | висячий `else`: відступи вводять в оману |
| `if-else.cs` | ланцюжок `else if`, guard clause, змінна з `out` в умові видима після `if` |
| `ternary-forms.cs` | де записують `?:`: присвоєння, аргумент, `return`, інтерполяція |
| `ternary.cs` | тип результату `?:`, target-typed `?:` з `int?` і `object`, ланцюжок `?:` |
| `switch-forms.cs` | усі форми секцій: одна мітка, кілька міток, блок, `goto case`, `default`, `return` |
| `switch-statement.cs` | кілька міток на секцію, `default`, `goto case`, рядки з урахуванням регістру |
| `switch-expression.cs` | той самий вибір через switch expression, метод з `=> … switch` |
| `non-exhaustive.cs` | попередження CS8509 і `SwitchExpressionException` |
| `exhaustive.cs` | повнота без `_`: `< 0`, `0`, `> 0` для `int`, `true` / `false` для `bool` |
| `patterns-is.cs` | `is` з константами, відношенням, `and` / `or` / `not`, `is null` |
| `relational.cs` | діапазони температури, `NaN` потрапляє в `_` |
| `when.cs` | `when` зі змінною, `var x when …` |
| `case-patterns.cs` | шаблони і `when` у мітках `switch` statement |
| `tuple-patterns.cs` | FizzBuzz і чверті координатної площини через кортежні шаблони |
| `switch-il.cs` | поглиблений розділ: таблиця переходів, `beq`, рядки за довжиною, дерево рішень; дивитися через `ilspycmd -il` на Release-збірці |
| `errors/` | CS0029, CS0665, CS0642 (`empty-if.cs`), CS0163, CS8070, CS0128, CS0152, CS0173, CS9135, CS8510, CS9336, CS8509 для `double`, CS8846 |
| `tasks/` | розв'язки міні-завдань «Спробуйте» (`letter-goto.cs` — крок 3 завдання з літерами) |
| `practice/` | розв'язки практичних завдань (`ects-moved.cs` — крок 3 завдання 1) |
