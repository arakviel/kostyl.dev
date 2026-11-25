# 03. Декомпілятори та обфускатори

Приклади до лекції `content/01.csharp/01.fundamentals/03.decompilers-and-obfuscators.md`.
Інструменти: `dotnet tool install -g ilspycmd` (11.2), `dotnet tool install -g Obfuscar.GlobalTool` (2.2.50).

| Файл | Що показує |
|---|---|
| `License/` | програма з ключем у коді; `obfuscar.xml` — налаштування Obfuscar |
| `sum-loop.cs` | IL циклу: `.locals init`, `stloc`/`ldloc`, `br.s`, `ble.s` |
| `interpolation.cs` | інтерполяція рядків і `ilspycmd -lv CSharp1` |
| `decode-strings.cs` | відновлення рядків, прихованих Obfuscar (поглиблений розділ) |
| `find-utf16.cs` | пошук рядка UTF-16 у будь-якому файлі: `dotnet run find-utf16.cs -- <файл> <текст>` |
| `tasks/` | розв'язки міні-завдань «Спробуйте» |
| `practice/` | розв'язки практичних завдань |

Обфускація: `cd License && dotnet build -c Release && obfuscar.console obfuscar.xml`,
далі `cp bin/Release/net10.0/License.runtimeconfig.json obfuscated/ && dotnet obfuscated/License.dll`.
