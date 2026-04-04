# Avalonia WASM Host for kostyl.dev

Цей проект є WebAssembly-хостом для превьюера XAML-коду (Avalonia UI). Він компілюється в WASM-бінарники, які Nuxt-компонент `WpfPreview.vue` використовує через `iframe`.

## 🚀 Команда для збірки (Build)

Якщо ви змінили C# код у цьому проекті (наприклад, додали нові шрифти, команди або логіку), виконайте цю команду в корені репозиторію:

```bash
dotnet publish tools/AvaloniaHost/AvaloniaHost.Browser/AvaloniaHost.Browser.csproj -c Release -o public/avalonia
```

> [!IMPORTANT]
> **Після збірки:** Nuxt автоматично побачить оновлені файли в `public/avalonia`. Якщо превью не оновлюється — очистіть кеш браузера або перезапустіть `npm run dev`.

## 🛠 Обслуговування та структура

### 1. Додавання шрифтів
Шрифти (як-от Segoe UI) лежать у `tools/AvaloniaHost/AvaloniaHost/Assets/Fonts`. Вони зареєстровані як `AvaloniaResource` у `.csproj` файлі. Якщо ви додаєте новий шрифт, переконайтеся, що він включений у проект і зареєстрований в `App.axaml`.

### 2. Логіка подій та команд
- Уся логіка (ViewModel) знаходиться в `AvaloniaHost/ViewModels/MainViewModel.cs`.
- Зв'язок із JavaScript (Vue) здійснюється в `AvaloniaHost.Browser/Program.cs` через `JSImport`.

### 3. Очищення результатів
При збірці в `public/avalonia` можуть залишатися зайві `.pdb` файли або старі папки `wwwroot`. Найкраще перед новим `publish` видалити вміст `public/avalonia`.

## 🧩 Як працює міст (Bridge)

1.  **Vue -> Avalonia**: `WpfPreview.vue` відсилає `postMessage` зі зміненим XAML.
2.  **Avalonia -> Vue**: C# код викликає `KostylBridge.LogToVue("msg")`, що відправляє `postMessage` назад у Vue для відображення в табі **Output**.
