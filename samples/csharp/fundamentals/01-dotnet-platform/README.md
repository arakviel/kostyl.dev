# 01. Платформа .NET — приклади

Звичайні приклади: `../run-all.sh 01-dotnet-platform`.

`tiers.cs` запускається окремо, бо потрібна Release-збірка і змінні середовища JIT:

```bash
dotnet build tiers.cs -c Release -o out
DOTNET_JitDisasmSummary=1 dotnet out/tiers.dll | grep Square
```

`languages/` — однакова програма на C#, F#, VB: `dotnet build <Проєкт> -c Release`, потім `ilspycmd -il`.
