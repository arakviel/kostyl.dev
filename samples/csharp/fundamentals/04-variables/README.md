# 04. Змінні, вбудовані типи і літерали

Приклади до лекції `content/01.csharp/01.fundamentals/04.variables-types-literals.md`.
Запуск усіх прикладів, що компілюються: `../run-all.sh 04-variables`.

| Файл | Що показує |
|---|---|
| `declare.cs` | усі способи оголосити змінну |
| `definite.cs` | присвоєння в обох гілках if (definite assignment) |
| `var-types.cs`, `var-il.cs` | тип, який виводить `var`; IL з явним типом і з `var` однаковий |
| `const-fold.cs` | константи обчислено компілятором: в IL — `ldc.i4 3600` |
| `names.cs` | `@class`, кириличне ім'я, `nameof(@class)` |
| `scopes.cs` | області видимості, однакове ім'я в сусідніх блоках |
| `ranges.cs`, `real-types.cs` | розміри й діапазони цілих і дробових типів |
| `byte-sum.cs` | `byte + byte` дає `int`, приведення `(byte)` |
| `chars.cs`, `defaults.cs` | `char` як код UTF-16, `bool`, значення за замовчуванням |
| `int-literals.cs` | `0x`, `0b`, `_`, тип літерала без суфікса і з суфіксами |
| `escapes.cs`, `strings.cs` | escape-послідовності, пастка `\x`, звичайні, verbatim і raw-рядки |
| `nameof.cs` | `nameof` і рядки в IL |
| `skip-init.cs`, `utf8-raw.cs` | поглиблені розділи: `SkipLocalsInit`, літерали `u8` і `$$"""` |
| `cpp/shadow.cpp` | shadowing у C++: `clang++ -Wall -Wextra shadow.cpp && ./a.out` друкує 10 |
| `errors/` | програми з помилками компіляції з лекції: `dotnet build errors/<файл>.cs` |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань; `practice/errors/broken.cs` — умова завдання 2 |

IL: `dotnet build <файл>.cs -c Release -o out && ilspycmd -il out/<файл>.dll`.
