# План навчання: WPF + Avalonia — від нуля до професіонала

## Філософія

1. **WPF First** — всі концепції через WPF.
2. **Avalonia як companion** — після кожної значущої WPF-статті: `Xa.avalonia-*.md` показує відмінності.
3. **Послідовність** — жодних forward references.
4. **Слабке ООП** — додаткові пояснення інтерфейсів, подій, поліморфізму де це потрібно. Студенти знають delegates/events.

---

## Принцип контенту: Text-First

> **КРИТИЧНО ВАЖЛИВО.** Матеріал створюється у підході **text-first**. Код — це ілюстрація, а не заміна пояснення. Кожна концепція спершу пояснюється **текстом**, і лише потім показується код.

### Чому Text-First?

Студенти, особливо початківці, **не вміють "читати" код**. Якщо стаття складається з 80% коду і 20% тексту — студент скопіює, запустить, але **не зрозуміє**. Нам потрібен зворотний баланс: **80% тексту, 20% коду**.

### Правила Text-First

1. **Перед кожним блоком коду** — мінімум 2-3 абзаци тексту, що пояснюють:
    - **Що** цей код робить (ціль).
    - **Чому** саме так (мотивація, альтернативи, trade-offs).
    - **Як** це працює під капотом (механізм).

2. **Після кожного блоку коду** — пояснення key takeaways:
    - Що саме сталося?
    - На що звернути увагу?
    - Які типові помилки тут роблять?

3. **Код розбивається на маленькі фрагменти**. Не один великий listing на 50 рядків, а 3-5 маленьких по 5-15 рядків, кожен з текстовим поясненням.

4. **Аналогії та метафори** — для кожної абстрактної концепції:
    - DependencyProperty = "поштова скринька з правилами пріоритету"
    - DataContext = "контекст, який тече по дереву елементів, як вода по трубах"
    - ControlTemplate = "костюм для актора — поведінка та роль залишаються, змінюється лише зовнішність"

5. **Діаграми та візуалізації** — для кожного складного процесу: Value Resolution, Visual/Logical Tree, Event Routing, Binding Pipeline. Використовувати `::mermaid` або `::plant-uml`.

6. **Порівняльні таблиці** — замість довгих текстових порівнянь, використовувати Markdown-таблиці для "X vs Y" (наприклад, CLR Property vs DependencyProperty, UserControl vs Custom Control).

7. **Vocabulary box** — на початку кожної статті (або перед складним розділом) — `::note` з глосарієм нових термінів, що будуть використані в матеріалі.

---

## Принцип XAML-прикладів: `::wpf-preview` для всього

> **ОБОВ'ЯЗКОВО.** Кожен XAML-приклад у матеріалі **ПОВИНЕН** використовувати компонент `::wpf-preview` для живого перегляду. Без винятку.

### Що таке `::wpf-preview`?

Це custom Docus-компонент, що рендерить **Avalonia UI через WebAssembly** у вигляді живого вікна з Fluent Design (Windows 11 стилістика). Студент бачить результат XAML-розмітки безпосередньо у браузері — без встановлення Visual Studio.

**Ключові обмеження та можливості:**

| Аспект          | Деталі                                                                                                      |
| --------------- | ----------------------------------------------------------------------------------------------------------- |
| **Рендеринг**   | Avalonia WASM із Fluent Theme (стилізація під Windows 11)                                                   |
| **Тема**        | Автоматична синхронізація з темою сайту (Dark/Light)                                                        |
| **Events**      | `Click="Button_Click"` **НЕ працює** — тільки `Command="{Binding ShowMessageCommand}"` з `CommandParameter` |
| **Вкладки**     | WASM Preview, MainWindow.xaml, MainWindow.xaml.cs, Output                                                   |
| **Code-behind** | Лише для демонстрації — не виконується реально                                                              |

### Правила використання `::wpf-preview`

1. **Кожен XAML-фрагмент** — обгортається у `::wpf-preview`. Навіть простий `<Button Content="Hello"/>`.

2. **Заголовок (`title`)** — описує, що демонструє приклад:

    ```markdown
    ::wpf-preview{title="StackPanel: вертикальне розташування"}
    ```

3. **Code-behind вкладка** — додавати блок `csharp`, якщо приклад потребує пояснення C#-логіки (навіть якщо вона не виконується):

    ````markdown
    ::wpf-preview{title="Button з Command"}

    ```xml
    <StackPanel Margin="20">
      <Button Content="Натисни мене" Command="{Binding ShowMessageCommand}" CommandParameter="Кнопку натиснуто!" />
    </StackPanel>
    ```

    ```csharp
    // Code-behind: показується у вкладці MainWindow.xaml.cs
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        // У реальному WPF: обробник події Click
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Кнопку натиснуто!");
        }
    }
    ```

    ::
    ````

4. **Для демонстрації подій** — використовувати `Command="{Binding ShowMessageCommand}"` + `CommandParameter="Текст у Output"`. Результат з'явиться у вкладці Output.

5. **Групування прикладів** — якщо стаття містить 5+ прикладів одного контролу (наприклад, різні Stretch modes для Image), використовувати окремий `::wpf-preview` для кожного варіанту, а не один великий.

### ⚠️ Avalonia-адаптація: що враховувати

Оскільки `::wpf-preview` рендерить через **Avalonia**, а не через WPF, є відмінності, які потрібно явно зазначати:

1. **Стилі**: Previewer відображає Avalonia Fluent Theme, а не стандартну тему WPF (Aero/Luna). Зовнішній вигляд кнопок, TextBox, ComboBox тощо **буде відрізнятися** від реального WPF. Додавати `::note` з поясненням:

    ```markdown
    ::note
    Превью використовує Avalonia Fluent Theme і виглядає як Windows 11. У реальному WPF-проєкті зовнішній вигляд контролів буде іншим (класична тема Aero), якщо ви не підключите бібліотеку тем (наприклад, MaterialDesignInXaml або MahApps.Metro).
    ::
    ```

2. **Контроли, яких немає в Avalonia**: Деякі WPF-контроли не мають прямих аналогів в Avalonia (наприклад, `RichTextBox`, `FlowDocument`, `MediaElement`, `Ribbon`, `Frame/Page`). Для таких — використовувати **статичні скріншоти** або `::html-preview` замість `::wpf-preview`, з поміткою:

    ```markdown
    ::warning
    Контрол `RichTextBox` із `FlowDocument` — специфічний для WPF і не має прямого аналогу в Avalonia. Приклад нижче показано як статичний скріншот.
    ::
    ```

3. **Grid.RowDefinitions та інші відмінності синтаксису**: Avalonia використовує скорочений синтаксис (`RowDefinitions="Auto,*,50"`), але в прикладах ми пишемо повний WPF-синтаксис (`<RowDefinition Height="Auto"/>`). Обидва працюватимуть у превью, але додавати `::tip`:

    ```markdown
    ::tip
    У Avalonia доступний скорочений синтаксис: `RowDefinitions="Auto,*,50"`. У WPF працює лише повний синтаксис із вкладеними елементами.
    ::
    ```

4. **Кольори та DynamicResource**: Превью підтримує `DynamicResource` (для теми), але WPF-специфічні системні ресурси (`SystemColors.ControlBrush`) не працюють. Використовувати явні кольори або Avalonia-ресурси.

5. **Де явно зазначати відмінності**: Після **кожного** `::wpf-preview`, де є розбіжність з реальним WPF, додавати `::note` або `::tip` з поясненням. Формат:
    - `::note` — якщо різниця суттєва (інший контрол, відсутня функціональність)
    - `::tip` — якщо різниця косметична (інший шрифт, інший стиль за замовчуванням)

### Кількість `::wpf-preview` на статтю

| Тип статті                              | Мінімум прикладів з `::wpf-preview`   |
| --------------------------------------- | ------------------------------------- |
| Контроли (Button, TextBox, ComboBox...) | 5–8 (кожна ключова властивість)       |
| Layout (Grid, StackPanel...)            | 4–6 (кожна панель + комбінації)       |
| Стилізація (Style, Template, Triggers)  | 3–5 (before/after + варіації)         |
| Data Binding                            | 3–4 (POCO без INPC → з INPC → TwoWay) |
| MVVM                                    | 2–3 (Command, Navigation)             |
| Анімації                                | 2–3 (базова + easing + складна)       |

## Файлова структура

```
content/01.csharp/12.desktop-ui/
├── .navigation.yml                              # title: Desktop UI

│   ── БЛОК 1: Вступ ──
├── 01.what-is-desktop-dev.md
├── 02.wpf-architecture.md
├── 03.first-wpf-app.md
├── 03a.first-avalonia-app.md                    # 🟢 Avalonia companion

│   ── БЛОК 2: XAML ──
├── 04.xaml-basics.md
├── 05.xaml-namespaces-resources.md
├── 05a.avalonia-xaml-differences.md             # 🟢 xmlns, axaml, відмінності
├── 06.xaml-markup-extensions.md

│   ── БЛОК 3: Layout ──
├── 07.layout-panels-part1.md                    # 📄 StackPanel, WrapPanel, DockPanel
├── 07.layout-panels-part2.md                    # 📄 Grid, Canvas, UniformGrid
├── 08.layout-advanced.md
├── 09.layout-responsive.md

│   ── БЛОК 4: Базові контроли ──
├── 10.basic-controls.md
├── 11.text-controls.md
├── 12.selection-controls.md
├── 13.content-controls.md

│   ── БЛОК 5: Property System ──
├── 14.dependency-properties-part1.md            # 📄 Концепція, Value Precedence
├── 14.dependency-properties-part2.md            # 📄 Створення, Metadata, Coercion
├── 14a.avalonia-property-system.md              # 🟢 StyledProperty, DirectProperty
├── 15.attached-properties.md
├── 16.routed-events.md

│   ── БЛОК 6: Data Binding ──
├── 17.data-binding-basics-part1.md              # 📄 Концепція, DataContext, Modes
├── 17.data-binding-basics-part2.md              # 📄 INPC, UpdateSourceTrigger
├── 17a.avalonia-compiled-bindings.md            # 🟢 x:CompileBindings, ReflectionBinding
├── 18.data-binding-advanced.md
├── 19.value-converters.md
├── 20.data-templates.md
├── 21.collections-binding-part1.md              # 📄 ObservableCollection, ItemsControl
├── 21.collections-binding-part2.md              # 📄 ICollectionView, Virtualization

│   ── БЛОК 7: MVVM ──
├── 22.mvvm-pattern.md                           # 🔵 Recap: інтерфейси, поліморфізм
├── 23.viewmodel-implementation.md
├── 24.commands.md
├── 25.mvvm-toolkit.md
├── 25a.avalonia-mvvm-reactiveui.md              # 🟢 ReactiveUI, ViewLocator
├── 26.messenger-pattern.md

│   ── БЛОК 8: Стилізація ──
├── 27.styles-basics.md
├── 27a.avalonia-css-styling.md                  # 🟢 CSS-like селектори, Classes
├── 28.control-templates-part1.md                # 📄 ControlTemplate, TemplateBinding
├── 28.control-templates-part2.md                # 📄 Named Parts, ContentPresenter
├── 28a.avalonia-control-themes.md               # 🟢 Нова система Control Themes
├── 29.triggers-visual-states.md
├── 29a.avalonia-pseudo-classes.md               # 🟢 :pointerover, :pressed замість Triggers
├── 30.resources-themes.md
├── 30a.avalonia-themes-fluent.md                # 🟢 Fluent/Simple, Theme Variants

│   ── БЛОК 9: Просунуті контроли ──
├── 31.collection-controls.md
├── 32.datagrid-part1.md                         # 📄 Columns, AutoGenerate
├── 32.datagrid-part2.md                         # 📄 Sorting, Filtering, Editing
├── 33.treeview-listview.md
├── 34.menus-toolbars.md

│   ── БЛОК 10: Навігація & Custom Controls ──
├── 35.navigation-windows.md
├── 35a.avalonia-navigation-dialogs.md           # 🟢 StorageProvider, кросплатформні діалоги
├── 36.dialogs-file-pickers.md
├── 37.user-controls.md
├── 38.custom-controls.md
├── 38a.avalonia-templated-controls.md           # 🟢 TemplatedControl, Generic.axaml

│   ── БЛОК 11: Анімації & Графіка ──
├── 39.animations-transitions.md
├── 39a.avalonia-animations.md                   # 🟢 Transitions, KeyFrame API
├── 40.media-graphics.md

│   ── БЛОК 12: DI & Data Persistence ──
├── 41.di-integration.md                         # Microsoft.Extensions.DI у WPF + Avalonia
├── 42.data-persistence-part1.md                 # SQLite + EF Core: підключення, DbContext
├── 42.data-persistence-part2.md                 # Repository pattern, Settings API

│   ── БЛОК 13: Тестування ──
├── 43.viewmodel-testing.md                      # xUnit + NSubstitute для ViewModel
├── 44.ui-testing.md                             # WPF UI Automation
├── 44a.avalonia-headless-testing.md             # 🟢 Avalonia Headless Testing

│   ── БЛОК 14: Кросплатформ & Deployment ──
├── 45.avalonia-cross-platform.md                # 🟢 Desktop/Mobile/WASM targets
└── 46.avalonia-packaging-deployment.md          # 🟢 AppImage, DMG, MSI, publish
```

**Підсумок**: 46 основних файлів + Part-файли = **~58 файлів**. З них **16 Avalonia companion** (🟢).

---

## Детальний опис кожної статті

### Блок 1: Вступ у десктопну розробку (3 + 1🟢 статті)

> Цей блок відповідає на фундаментальне питання: **"Що таке десктопний застосунок і чим він відрізняється від веб/консолі?"** Студент, який ніколи не створював GUI, має зрозуміти контекст.

---

#### `01.what-is-desktop-dev.md` — Що таке десктопна розробка?

**Мета**: Мотивація та контекст. Чому десктоп не помер, незважаючи на веб.

**Зміст**:

- **Hook**: Історія — перші GUI (Xerox Alto, Windows 1.0). Скріншоти еволюції інтерфейсів від CLI до сучасних UI.
- **Десктоп vs Консоль vs Веб**: Порівняльна таблиця (взаємодія з користувачем, графіка, доступ до ОС, UX, offline). Коли обирати десктоп: IDE (Visual Studio, Rider), графічні редактори (Photoshop, Figma Desktop), системні утиліти, промислове ПЗ.
- **Огляд технологій десктопу у .NET**: WinForms (легасі, event-driven), WPF (зріла платформа, XAML + DirectX), UWP (обмежена, Windows 10+), WinUI 3 (нова, ще розвивається), MAUI (кросплатформ, мобіль-орієнтована), **Avalonia** (кросплатформ, WPF-подібна). Порівняльна таблиця: підтримувані платформи, вік технології, архітектура рендерингу, зрілість екосистеми.
- **Чому WPF як основа курсу**: Зрілість документації, XAML як стандарт декларативного UI, MVVM як патерн індустрії, легкість переходу на Avalonia. _Стратегія_: "Вивчи WPF → зрозумій Avalonia за тиждень".
- **Що ми побудуємо**: Демонстрація фінального проєкту курсу (скріншот/GIF), щоб мотивувати студента бачити кінцеву мету.
- **Практичні завдання**: Дослідницькі (порівняти 3 десктопні застосунки та визначити їх UI-фреймворк, знайти WPF-програми у реальному світі, порівняти UX десктопної та веб-версії одного продукту).

**Не згадує**: XAML-синтаксис, Binding, MVVM, DependencyProperty — лише огляд на рівні "це існує".

---

#### `02.wpf-architecture.md` — Архітектура WPF: як влаштований графічний інтерфейс

**Мета**: Розуміння внутрішньої архітектури WPF. Чому WPF рендерить через DirectX, а не GDI+. Дати "ментальну карту" платформи.

**Зміст**:

- **Hook**: Чому WPF-застосунки виглядають краще за WinForms? Порівняння рендерингу (GDI+ растровий vs DirectX/Composition векторний). Скріншоти масштабування: WinForms розмивається, WPF — ні.
- **Архітектура WPF** (діаграма Mermaid):
    - `PresentationFramework.dll` → високорівневі контроли (Button, Grid, TextBox).
    - `PresentationCore.dll` → базові типи (Visual, UIElement, ContentElement).
    - `WindowsBase.dll` → threading (Dispatcher), DependencyObject, DependencyProperty.
    - `milcore.dll` → нативний шар, DirectX-рендеринг, Media Integration Layer.
- **Потоковість (Threading Model)**: UI Thread та Dispatcher. Чому не можна змінювати UI з іншого потоку — демонстрація InvalidOperationException. `Dispatcher.Invoke()` та `Dispatcher.BeginInvoke()` для маршалінгу викликів.
- **Logical Tree vs Visual Tree**: Пояснення різниці з діаграмою. Button у Logical Tree — один елемент. Button у Visual Tree — Border → ContentPresenter → TextBlock. Чому це важливо для розуміння стилів і подій (але самі стилі та події — ще попереду, тут лише концепція дерев).
- **Апаратне прискорення**: Rendering Tiers (0 — software fallback, 1 — partial hardware, 2 — full hardware). Як WPF визначає можливості GPU. `RenderCapability.Tier`.
- **Application Lifecycle**: Клас `Application`, події `Startup`, `Exit`, `DispatcherUnhandledException`. `Application.Current` як singleton.
- **Практичні завдання**: Дослідити Logical/Visual Tree через Snoop або Live Visual Tree у Visual Studio. Вивести Rendering Tier на екран. Обробити DispatcherUnhandledException.

**Не згадує**: XAML-синтаксис (ще не введений), Binding, стилі, шаблони.

---

#### `03.first-wpf-app.md` — Перший проєкт: від нуля до вікна

**Мета**: Створити перший WPF-проєкт, зрозуміти структуру файлів, побачити результат на екрані.

**Зміст**:

- **Hook**: "Запустіть це і побачите вікно — ваш перший GUI-застосунок. Після сотень рядків Console.WriteLine — це новий рівень."
- **Створення проєкту**: `dotnet new wpf`, структура файлів (`App.xaml` + `App.xaml.cs`, `MainWindow.xaml` + `MainWindow.xaml.cs`), `.csproj` та `<UseWPF>true</UseWPF>`, `<TargetFramework>net8.0-windows</TargetFramework>`.
- **Анатомія App.xaml**: `StartupUri`, Application-level ресурси (поки тільки згадка, що тут можна зберігати "спільні налаштування"). `Application` як singleton — `Application.Current`.
- **Анатомія MainWindow.xaml**: Перше знайомство з XAML — тег `<Window>`, атрибути `Title`, `Width`, `Height`, `WindowStartupLocation`. Мінімальний вміст — `<TextBlock Text="Привіт, WPF!"/>` та `<Button Content="Натисни мене"/>`.
- **Code-Behind**: `MainWindow.xaml.cs` — клас вікна, обробка подій `Click`. Натискання кнопки змінює текст через `myTextBlock.Text = "Нове значення"`. Пряме звернення до елементів через `x:Name`.
- **Partial classes**: Чому `MainWindow` є `partial`. Як XAML та CS-файл з'єднуються через `InitializeComponent()`. Що відбувається при компіляції — генерація `*.g.cs` файлу.
- **Hot Reload**: XAML Hot Reload для гарячих змін під час роботи застосунку. Налаштування в Visual Studio / Rider. Обмеження: що можна змінити "на льоту", а що ні.
- **Покрокова інструкція** (`::steps`): Створення → Запуск → Модифікація → Результат.
- **Практичні завдання**: (Рівень 1) Створити вікно з привітанням та кнопкою, що змінює текст. (Рівень 2) Кнопка "Змінити колір фону" — через code-behind `Background = Brushes.LightBlue`. Лічильник кліків. (Рівень 3) Вікно з TextBox для введення імені та Button, що формує привітання з цим ім'ям.

**Не згадує**: Data Binding, MVVM, стилі, шаблони, DependencyProperty.

---

#### `03a.first-avalonia-app.md` — 🟢 Перший Avalonia-проєкт

**Мета**: Показати, що Avalonia — це "майже WPF, але кросплатформний". Створити перший проєкт та побачити паралелі.

**Зміст**:

- **Hook**: "Все, що ви щойно зробили у WPF — можна запустити на Linux та macOS. Як?"
- **Що таке Avalonia**: Кросплатформний UI-фреймворк, рендеринг через Skia (SkiaSharp) замість DirectX. Незалежний від Microsoft, open-source, активна спільнота.
- **Avalonia vs WPF — перше порівняння**: Спільне (XAML, Binding, MVVM) та відмінності (кросплатформ, CSS-like стилі). Поки лише огляд — деталі у companion-статтях далі.
- **Створення проєкту**: `dotnet new install Avalonia.Templates`, `dotnet new avalonia.app` vs `dotnet new avalonia.mvvm`. Стуктура файлів: `App.axaml` (не `.xaml`!), `Program.cs` → `BuildAvaloniaApp()`, `MainWindow.axaml`.
- **Порівняння структури**: WPF vs Avalonia side-by-side таблиця (App.xaml → App.axaml, csproj різниця, entry point різниця).
- **Запуск на різних платформах**: Windows, Linux, macOS — демонстрація що той самий код працює скрізь.
- **DevTools**: Вбудований інспектор Avalonia (F12) — аналог Snoop для WPF, але вбудований з коробки. Показ Visual Tree, Properties.
- **Практичні завдання**: Створити "Hello World" Avalonia-проєкт. Порівняти структуру файлів з WPF-проєктом зі статті 03. Запустити на іншій ОС (або через WSL/Docker).

**Не згадує**: Compiled Bindings, ReactiveUI, стилізацію Avalonia — це в пізніших companion-статтях.

---

### Блок 2: XAML — мова розмітки інтерфейсу (3 + 1🟢 статті)

> Цей блок глибоко занурює у XAML як декларативну мову. Студент має зрозуміти, що XAML — це не HTML, а серіалізація об'єктного графу C#.

---

#### `04.xaml-basics.md` — XAML: декларативний інтерфейс

**Мета**: Зрозуміти XAML як мову та її зв'язок з C#-об'єктами.

**Зміст**:

- **Hook**: "Кожен рядок XAML = рядок C#. XAML — це не HTML, а serialization format для об'єктного графу. `<Button Content="OK"/>` — це `new Button { Content = "OK" }`."
- **XAML як XML**: Правила XML — case-sensitivity, вкладеність, обов'язкове закриття тегів, атрибути в лапках. Відмінність від HTML, де браузер "пробачає" помилки.
- **Property Element Syntax vs Attribute Syntax**: `<Button Content="OK"/>` vs `<Button><Button.Content>OK</Button.Content></Button>`. Коли потрібен Property Element — коли значення є складним об'єктом (наприклад, `<Button.Background><LinearGradientBrush>...</LinearGradientBrush></Button.Background>`).
- **Content Property**: Атрибут `[ContentProperty]` на класі. Чому `<Button>Text</Button>` працює — `Content` є content property для `ContentControl`. Інші приклади: `Panel.Children`, `ItemsControl.Items`.
- **Type Converters**: Як рядок `"Red"` стає `Brushes.Red`. Клас `TypeConverter`. Приклади: `"10,20"` → `Thickness`, `"Bold"` → `FontWeight`. Як WPF знаходить потрібний TypeConverter.
- **Attached Property синтаксис**: `Grid.Row="1"` — що це означає синтаксично (концептуально, без глибокого механізму DependencyProperty — це Блок 5).
- **x:Name vs Name**: `x:Name` працює для всіх елементів, `Name` — лише для тих, хто має відповідну CLR-властивість. Рекомендація: завжди використовувати `x:Name`.
- **XAML ↔ C# еквівалент**: Таблиця/sidebar, що показує кожну XAML-конструкцію та її C#-відповідник — щоб студент завжди розумів, що XAML — це "просто інший синтаксис для того ж самого".
- **Практичні завдання**: (Рівень 1) Переписати 5 XAML-фрагментів на C# та навпаки. (Рівень 2) Дослідити Content Property для різних контролів — знайти, який контрол не має Content Property. (Рівень 3) Створити інтерфейс цілком у code-behind (без XAML) та порівняти читабельність.

**Не згадує**: Binding (`{Binding}`), Style, Template, Resources (лише `x:Name`).

---

#### `05.xaml-namespaces-resources.md` — Простори імен та ресурси XAML

**Мета**: Зрозуміти механізм просторів імен XAML та систему обміну ресурсами між елементами.

**Зміст**:

- **Простори імен XAML**: `xmlns` та `xmlns:x`. Що таке `http://schemas.microsoft.com/winfx/2006/xaml/presentation` — маппінг на десятки CLR-namespace'ів. `xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"` — спеціальні директиви XAML. Підключення власних класів: `xmlns:local="clr-namespace:MyApp"`, `xmlns:models="clr-namespace:MyApp.Models"`.
- **Ресурси (Resources)**: Що таке Resource Dictionary — словник `string → object`. `Window.Resources`, `Application.Resources`. Ключі (`x:Key`). Зберігання кольорів, пензлів, рядків, чисел — будь-яких об'єктів у ресурсах.
- **StaticResource vs DynamicResource**: StaticResource — одноразовий lookup при ініціалізації (XAML parse time). DynamicResource — реагує на зміни в runtime (ресурс можна замінити, і UI оновиться). Коли що обирати — StaticResource для продуктивності, DynamicResource для тем.
- **Зовнішні Resource Dictionaries**: Файл `Resources/Colors.xaml`, `Resources/Brushes.xaml`. `MergedDictionaries` — об'єднання кількох словників в одному місці. Організація ресурсів у великих проєктах — паттерн "одна відповідальність на файл".
- **Пошук ресурсів (Resource Lookup)**: Ланцюжок пошуку: Element → Parent → ... → Window → Application → Theme. Діаграма Mermaid. Що відбувається, якщо ресурс не знайдено — `StaticResource` кине виняток, `DynamicResource` мовчки ігнорує.
- **Практичні завдання**: (Рівень 1) Створити палітру кольорів у Window.Resources та використати їх у кількох контролах. (Рівень 2) Перемикати DynamicResource у runtime через кнопку — змінити кольорову тему. (Рівень 3) Винести спільні ресурси в зовнішній файл та підключити через MergedDictionaries до кількох вікон.

**Не згадує**: Styles (будуть у Блоці 8), Binding, Templates.

---

#### `05a.avalonia-xaml-differences.md` — 🟢 XAML в Avalonia: ключові відмінності

**Мета**: Показати студенту, що знаючи WPF XAML, він вже знає 90% Avalonia XAML — але є важливі деталі.

**Зміст**:

- **Розширення файлу**: `.axaml` замість `.xaml`. Причина — уникнення конфліктів з WPF-інструментами у Visual Studio.
- **Namespace URIs**: `xmlns="https://github.com/avaloniaui"` замість `http://schemas.microsoft.com/winfx/2006/xaml/presentation`. Простір `xmlns:x` залишається тим самим.
- **clr-namespace → using:**: У Avalonia рекомендується `xmlns:local="using:MyApp"` замість `xmlns:local="clr-namespace:MyApp"`. Обидва працюють, але `using:` — коротший і канонічний.
- **Ресурси**: Ті ж концепції `StaticResource`/`DynamicResource`, але деякі відмінності — наприклад, `ThemeResource` для тематичних ресурсів.
- **Design preview**: Avalonia Previewer у Rider/VS. Порівняння з WPF Designer.
- **Порівняльна таблиця**: WPF XAML vs Avalonia XAML — side-by-side для 10 ключових конструкцій.
- **Практичні завдання**: Портувати XAML-файл з ресурсами зі статті 05 на Avalonia. Виправити помилки, що виникнуть через різницю namespace.

**Не згадує**: Compiled Bindings, CSS-like стилі, StyledProperty — це в пізніших companion-статтях.

---

#### `06.xaml-markup-extensions.md` — Розширення розмітки XAML

**Мета**: Зрозуміти механізм `{...}` синтаксису в XAML — це не "магія", а виклик класів.

**Зміст**:

- **Що таке Markup Extension**: Клас, що наслідує `MarkupExtension`. Метод `ProvideValue(IServiceProvider)`. Фігурні дужки `{...}` у XAML — це виклик `ProvideValue()`.
- **Вбудовані розширення**:
    - `{StaticResource}` та `{DynamicResource}` (повторення з правильною глибиною — тепер студент розуміє, що це Markup Extensions).
    - `{x:Type}` — для передачі типу як параметра. `{x:Type local:MyClass}` → `typeof(MyClass)`.
    - `{x:Null}` — для явного null. Коли потрібно: наприклад, `Background="{x:Null}"` для скасування успадкованого значення.
    - `{x:Static}` — для звернення до статичних полів/властивостей. `{x:Static SystemColors.HighlightBrush}`.
    - `{x:Array}` — для створення масивів у XAML.
- **`{Binding}` — перше знайомство** (лише preview): Показати `{Binding ElementName=mySlider, Path=Value}` як приклад "прив'язки одного елемента до іншого". Slider → TextBlock.Text. Без пояснення DataContext, INotifyPropertyChanged — це Блок 6. Мета — лише показати, що `{Binding}` — це теж Markup Extension.
- **Створення Custom Markup Extension**: Простий приклад — `LocalizedStringExtension`, що бере рядок з ресурсного файлу за ключем. Показати: клас → атрибут `[MarkupExtensionReturnType]` → використання у XAML.
- **Практичні завдання**: (Рівень 1) Використати `{x:Static}` для підстановки системних кольорів та `DateTime.Now`. (Рівень 2) Створити Slider + TextBlock з `{Binding ElementName}`. (Рівень 3) Створити простий Custom Markup Extension — наприклад, `{Multiply Value=5, Factor=3}`.

**Не згадує**: DataContext, INotifyPropertyChanged, MVVM, Command — `{Binding}` тут лише як preview.

---

### Блок 3: Layout — розташування елементів (4 статті, без Avalonia companion)

> Студент вчиться будувати інтерфейси через систему панелей. Це фундамент для будь-якого GUI. Layout у WPF та Avalonia майже ідентичний, тому окремий Avalonia-companion не потрібен.

---

#### `07.layout-panels-part1.md` — Панелі: StackPanel, WrapPanel, DockPanel

**Мета**: Опанувати три прості панелі та зрозуміти двопрохідну модель layout WPF.

**Зміст**:

- **Hook**: "У WPF немає абсолютного позиціонування за замовчуванням. Немає `position: absolute`. І це — перевага, а не обмеження. Чому?"
- **Модель розташування WPF**: Measure Pass → Arrange Pass (двопрохідний layout). У Measure Pass батьківський елемент запитує у дочірнього: "скільки місця тобі потрібно?". У Arrange Pass — "ось тобі стільки, розташуйся". Чому WPF layout є декларативним, а не піксельним.
- **StackPanel**: Вертикальне (за замовчуванням) та горизонтальне вкладання (`Orientation="Horizontal"`). Поведінка: елементи займають стільки місця, скільки їм потрібно. Коли StackPanel — правильний вибір (прості списки, toolbar-подібні рядки), коли ні (складні форми).
- **WrapPanel**: Перенесення на новий рядок при нестачі місця. `ItemWidth`, `ItemHeight` для рівномірних елементів. Відмінність від StackPanel — автоматичний перенос.
- **DockPanel**: `DockPanel.Dock="Top|Bottom|Left|Right"`. `LastChildFill="True"` — останній елемент заповнює решту простору. Побудова типового інтерфейсу: Menu зверху, StatusBar знизу, Sidebar зліва, Content у центрі.
- **Практичні завдання**: (Рівень 1) Побудувати toolbar з 5 кнопок через StackPanel Horizontal. (Рівень 2) Реалізувати класичний Layout додатку (Menu + Sidebar + Content + StatusBar) через DockPanel. (Рівень 3) Галерея елементів через WrapPanel, що автоматично переносить рядки.

**Не згадує**: Grid (Part 2), Binding, стилі.

---

#### `07.layout-panels-part2.md` — Grid, Canvas, UniformGrid

**Мета**: Опанувати Grid — найпотужнішу панель WPF — та зрозуміти, коли (рідко) потрібен Canvas.

**Зміст**:

- **Grid — основна панель WPF**: Чому Grid — це "швейцарський ніж" layout. RowDefinitions та ColumnDefinitions.
- **Типи розмірів**: `Auto` (по вмісту), `*` (star — пропорційно), `2*` (подвійна пропорція), fixed (`200` — пікселі). Детальне пояснення Star sizing з діаграмами.
- **Grid.Row, Grid.Column**: Розташування елементів. RowSpan, ColumnSpan для об'єднання комірок.
- **SharedSizeGroup**: Синхронізація розмірів колонок між різними Grid-ами. `Grid.IsSharedSizeScope="True"`.
- **Canvas**: Абсолютне позиціонування (`Canvas.Left`, `Canvas.Top`, `Canvas.Right`, `Canvas.Bottom`). Чому це антипатерн для звичайних форм і діалогів — не responsive, не масштабується. Коли Canvas правильний: ігри, діаграми, freeform малювання, drag-and-drop.
- **UniformGrid**: Рівномірний розподіл по рядках/колонках. `Rows`, `Columns`. Спрощений Grid для однакових елементів.
- **Практичні завдання**: (Рівень 1) Калькулятор (4×5 Grid з кнопками). (Рівень 2) Форма логіну: Label+TextBox у Grid з Auto+\* розмірами. (Рівень 3) Dashboard з кількома Grid з SharedSizeGroup для вирівнювання колонок.

**Не згадує**: Binding, стилі, DataTemplate.

---

#### `08.layout-advanced.md` — Просунуті техніки Layout

**Мета**: Покрити Margin, Padding, Alignment, ScrollViewer, ViewBox та інші важливі аспекти розташування.

**Зміст**:

- **Margin vs Padding**: Візуальна діаграма (як CSS box-model, але для WPF). Margin — зовнішні відступи від сусідніх елементів. Padding — внутрішні відступи всередині контролу. Синтаксис: `"10"` (all), `"10,20"` (horizontal,vertical), `"10,20,30,40"` (left,top,right,bottom).
- **Alignment**: `HorizontalAlignment` (Left, Center, Right, Stretch), `VerticalAlignment` (Top, Center, Bottom, Stretch). `HorizontalContentAlignment` та `VerticalContentAlignment` — для вмісту всередині контролу. `Stretch` — заповнює весь доступний простір.
- **MinWidth/MaxWidth, MinHeight/MaxHeight**: Обмеження розмірів. Валідний use case: текстове поле, що розтягується, але не більше ніж 500px.
- **ScrollViewer**: Горизонтальний/вертикальний скролінг. `HorizontalScrollBarVisibility`, `VerticalScrollBarVisibility` (Auto, Visible, Hidden, Disabled). Вкладання ScrollViewer з панелями. Типова помилка: ScrollViewer всередині StackPanel "не працює" — пояснення чому.
- **ViewBox**: Масштабування вмісту. Stretch modes: Uniform (зберігає пропорції), Fill (розтягує), UniformToFill (обрізає), None (натуральний розмір). Практичні use cases.
- **Border**: BorderBrush, BorderThickness, CornerRadius (закруглені кути), Padding.
- **Separator та GridSplitter**: GridSplitter для інтерактивної зміни розмірів колонок/рядків Grid. `ResizeDirection`, `ResizeBehavior`.
- **Вкладання панелей**: Комбінування Grid + StackPanel + DockPanel для складних інтерфейсів. Правило: Grid як основний каркас, StackPanel для простих списків всередині комірок.
- **Практичні завдання**: (Рівень 1) Форма з правильними Margin/Padding та Border. (Рівень 2) Email-клієнт layout (3-колонковий з GridSplitter). (Рівень 3) Форма налаштувань зі ScrollViewer та групуванням через Border.

**Не згадує**: Data Binding, стилі, MVVM.

---

#### `09.layout-responsive.md` — Адаптивний Layout та найкращі практики

**Мета**: Побудова інтерфейсів, що коректно адаптуються при зміні розміру вікна.

**Зміст**:

- **Responsive Layout у WPF**: Star sizing (`*`) як основа. Чому `*` кращий за фіксовані піксельні розміри — демонстрація при resize. Комбінація `Auto` (для фіксованих елементів) + `*` (для розтягуваних).
- **Зміна видимості**: `Visibility` = `Visible` / `Collapsed` / `Hidden`. Різниця: `Hidden` зберігає місце, `Collapsed` — ні. Responsive через приховування елементів при нестачі місця.
- **SizeChanged event**: Реакція на зміну розміру вікна через code-behind. `ActualWidth`, `ActualHeight`. Приклад: приховати sidebar, коли ширина < 800px.
- **MinWidth/MaxWidth як responsive tool**: Елемент, що не стає менше за MinWidth — дає ScrollViewer-у можливість показати скролбар.
- **Flow Panels для responsive**: Використання WrapPanel для адаптивних сіток елементів — аналог CSS Flexbox wrap.
- **Best practices Layout**: Уникання абсолютних розмірів (крім Min/Max), правильне використання Auto vs `*`, мінімізація вкладання панелей (performance — кожен рівень = зайвий layout pass), `UseLayoutRounding="True"` для чіткості піксельних кордонів.
- **Практичні завдання**: (Рівень 1) Зробити форму, що коректно масштабується з вікном. (Рівень 2) Адаптивний dashboard, що ховає sidebar при width < 700px. (Рівень 3) Responsive card grid через WrapPanel, що змінює кількість колонок залежно від ширини.

---

#### `10.layout-avalonia.md` — Layout в Avalonia: відмінності та нові можливості

**Мета**: Розібрати, чим Avalonia відрізняється від WPF у частині layout — що є аналогічним, що змінилось, а що з'явилося нового.

**Зміст**:

- **Що збігається з WPF**: Grid, StackPanel, DockPanel, WrapPanel, Canvas, ScrollViewer, Border — всі ці панелі присутні і мають ідентичний API. Студент може переносити XAML практично без змін.

- **`Spacing` замість Margin-хаку**: У Avalonia `StackPanel`, `Grid`, `StackLayout` мають вбудовану властивість `Spacing` (тип `double`) — відступ між дочірніми елементами. WPF не має такого; там треба було `Margin` на кожному елементі або стиль. Приклад: `<StackPanel Spacing="8">`. Також `Grid` має `RowSpacing` та `ColumnSpacing`.

- **`UniformGrid` → більш гнучкий**: В Avalonia `UniformGrid` підтримує `Rows`, `Columns`, і має кращу поведінку з динамічним контентом. Також є `Panel` базовий клас — можна легко створювати власні панелі.

- **`RelativePanel`**: Аналог WPF `RelativePanel` (є в UWP, в Avalonia теж). Позиціонування елементів відносно один одного та контейнера через Attached Properties: `RelativePanel.AlignLeftWithPanel`, `RelativePanel.Below`, `RelativePanel.RightOf` тощо. Корисний для складних адаптивних layout де Grid занадто жорсткий.

- **`Expander`**: Розгортальний/згортальний контейнер. `Header` — заголовок що завжди видимий. `Content` — вміст що ховається/показується. `IsExpanded`. Анімована зміна висоти. WPF теж має Expander, але Avalonia-версія має кращу анімацію та кастомізацію.

- **`SplitView`**: Панель з двома зонами: зіжмите меню (Pane) + основний вміст (Content). `IsPaneOpen`, `DisplayMode` (Overlay, Inline, CompactOverlay, CompactInline). Аналог UWP SplitView. Ідеально підходить для мобільного/адаптивного дизайну де sidebar ховається за hamburger-menu.

- **`ItemsRepeater`**: Легковісний аналог `ItemsControl`/`ListBox` без VirtualizingStackPanel-overhead. Використовує `Layout` об'єкт (StackLayout, WrapLayout, UniformGridLayout) для розташування елементів. Кастомні `Layout` — створення власних алгоритмів розташування. Аналог UWP ItemsRepeater.

- **`Panel.ZIndex`**: Аналогічний WPF. Але Avalonia додає `Canvas.ZIndex` як зручний аліас.

- **Transitions (анімовані layout-зміни)**: `Transitions` — анімація зміни властивостей (Width, Height, Opacity, Margin). `DoubleTransition`, `ThicknessTransition`. Пряма інтеграція з layout-системою. Приклад: `<StackPanel><StackPanel.Transitions><Transitions><DoubleTransition Property="Height" Duration="0:0:0.3"/></Transitions></StackPanel.Transitions>`.

- **`DataTemplates` у `Panel`**: Avalonia дозволяє прикріпити `DataTemplates` безпосередньо до панелей — до WPF такого немає.

- **Ключові відмінності у поведінці**:
    - `ScrollViewer` у Avalonia за замовчуванням має `HorizontalScrollBarVisibility = Disabled`, `VerticalScrollBarVisibility = Auto` — так само як WPF.
    - `TextBlock.TextWrapping` за замовчуванням `NoWrap` — аналогічно WPF.
    - `Canvas.Left/Top` прив'язані безпосередньо до рендер-трансформацій, що в Avalonia дає кращу продуктивність.

- **Практичні завдання**: (Рівень 1) Порівняти StackPanel зі Spacing в Avalonia та Margin-патерн у WPF. (Рівень 2) Реалізувати SplitView для мобільного layout з hamburger-menu. (Рівень 3) Використати ItemsRepeater + WrapLayout для адаптивної галереї карток.

**Не згадує**: Data Binding на повну (Compiled Bindings будуть у Блоці Data Binding), Styles і Themes.

---

### Блок 4: Базові контроли (4 статті, без Avalonia companion)


> Після розуміння XAML і Layout, студент вивчає бібліотеку стандартних контролів. Контроли у WPF та Avalonia майже ідентичні (ті ж назви, ті ж властивості), тому окремий companion не потрібен.

---

#### `10.basic-controls.md` — Button, Image, ProgressBar та інші базові контроли

**Мета**: Познайомити з найбільш вживаними контролами — кнопки, зображення, індикатори прогресу.

**Зміст**:

- **Button**: Click event у code-behind, `IsDefault` (Enter), `IsCancel` (Escape). `Content` — не лише текст, а будь-який XAML. Приклад: Button зі StackPanel всередині (іконка + текст). Згадка: Command як альтернатива Click — буде у Блоці 7.
- **RepeatButton**: Кнопка, що генерує Click поки натиснута. `Delay`, `Interval`. Use case: кнопки "+"/"-" для числових полів.
- **ToggleButton**: `IsChecked` (nullable bool). Basis для CheckBox та RadioButton (але це наступні статті).
- **Image**: Source (Pack URIs — `pack://application:,,,/Assets/logo.png`), Stretch modes (None, Fill, Uniform, UniformToFill). Як правильно додати зображення до проєкту (Build Action = Resource).
- **ProgressBar**: `Value`, `Minimum`, `Maximum`, `IsIndeterminate` для невизначеного прогресу.
- **Slider**: `Value`, `Minimum`, `Maximum`, `TickFrequency`, `TickPlacement`, `IsSnapToTickEnabled`. Прив'язка Slider → TextBlock через `{Binding ElementName}` (вже знайома з MarkupExtensions).
- **ToolTip**: Прості текстові та складні Structured ToolTips (з XAML-вмістом всередині).
- **Popup**: `Placement` (Bottom, Top, Mouse), `StaysOpen`, `IsOpen`. Відмінність від ToolTip — програмне керування.
- **Практичні завдання**: (Рівень 1) Кнопка з іконкою та текстом. (Рівень 2) Галерея зображень з ProgressBar (симуляція завантаження через Slider). (Рівень 3) Popup з детальною інформацією при наведенні на елемент.

**Не згадує**: Data Binding до ViewModel, MVVM, стилі/шаблони.

---

#### `11.text-controls.md` — Текстові контроли: TextBlock, TextBox, RichTextBox

**Мета**: Розуміти різницю між контролами відображення та введення тексту.

**Зміст**:

- **TextBlock vs Label**: Чому TextBlock для простого тексту (lightweight, не focusable), Label — для accessible контролів з `Target` для AccessKey. Коли використовувати кожен.
- **TextBlock**: `TextWrapping` (Wrap, NoWrap, WrapWithOverflow), `TextTrimming` (CharacterEllipsis, WordEllipsis). Inline elements — `Run`, `Bold`, `Italic`, `Hyperlink`, `LineBreak`. Форматований текст без RichTextBox.
- **TextBox**: `Text`, `TextChanged` event, `AcceptsReturn` (багаторядковий), `AcceptsTab`, `MaxLength`, `IsReadOnly`, `TextWrapping`. Placeholder text — через Adorner або style trick (ще без стилів — тільки code-behind підхід).
- **PasswordBox**: `SecurePassword` (SecureString), `PasswordChanged` event. Чому PasswordBox не має `Text` property — безпека. `PasswordChar` для зміни символу маскування.
- **RichTextBox**: `FlowDocument` як контент. `Paragraphs`, `Bold`, `Italic`. Базове використання для форматованого тексту. `Selection.ApplyPropertyValue()` для зміни стилю виділеного тексту.
- **Практичні завдання**: (Рівень 1) Мітка + TextBox для введення імені. (Рівень 2) Простий текстовий редактор — TextBox з AcceptsReturn + лічильник символів. (Рівень 3) Форма реєстрації з PasswordBox та валідацією довжини пароля через code-behind.

**Не згадує**: Data Binding до моделей, Value Converters, MVVM, стилі.

---

#### `12.selection-controls.md` — Контроли вибору: CheckBox, RadioButton, ComboBox

**Мета**: Опанувати контроли, що дозволяють обирати значення з набору варіантів.

**Зміст**:

- **CheckBox**: `IsChecked` (nullable bool — True/False/null). `IsThreeState` для трьох станів. `Checked`, `Unchecked`, `Indeterminate` events. Типовий use case: налаштування програми.
- **RadioButton**: `GroupName` для логічного групування. `IsChecked`. Як працює ексклюзивний вибір — тільки один RadioButton у групі може бути обраний.
- **ComboBox**: `Items` (ручне додавання через XAML), `SelectedItem`, `SelectedIndex`, `IsEditable` (дозволяє вводити текст). `DisplayMemberPath` для показу конкретної властивості. Примітка: прив'язка через `ItemsSource` до колекцій — у Блоці 6.
- **ListBox**: `SelectedItem`, `SelectionMode` (Single, Multiple, Extended). Відмінність від ComboBox — весь список видимий одразу.
- **DatePicker**: `SelectedDate`, `DisplayDateStart`, `DisplayDateEnd`. `BlackoutDates` для блокування певних дат.
- **Calendar**: `SelectedDate`, `SelectionMode` (SingleDate, SingleRange, MultipleRange, None).
- **Практичні завдання**: (Рівень 1) Форма опитування з CheckBox та RadioButton. (Рівень 2) ComboBox з вибором країни + показ прапорця. (Рівень 3) Форма бронювання з DatePicker, що блокує минулі дати.

**Примітка**: ItemsSource тут заповнюється з code-behind або статичними XAML-елементами. Data Binding для колекцій — у Блоці 6.

---

#### `13.content-controls.md` — Content Model: GroupBox, Expander, TabControl

**Мета**: Зрозуміти Content Model WPF та використати контейнерні контроли для організації інтерфейсу.

**Зміст**:

- **Content Model WPF**: `ContentControl` vs `ItemsControl` (фундаментальна різниця). `ContentControl` має один `Content` — об'єкт будь-якого типу. Чому `Button` може містити `Grid`, `Image`, `StackPanel` — а не лише текст. `ItemsControl` має колекцію `Items`.
- **GroupBox**: `Header` (може бути будь-яким XAML), `Content`. Групування елементів форми — наприклад, "Персональні дані", "Адреса".
- **Expander**: `IsExpanded`, `ExpandDirection` (Down, Up, Left, Right). Анімація розгортання. Використання для FAQ-секцій або колапсованих панелей.
- **TabControl**: `TabItem` з `Header` та `Content`. `SelectedIndex`, `SelectedItem`. Кожен TabItem — окрема "сторінка" з власним вмістом.
- **HeaderedContentControl**: Базовий клас для GroupBox, Expander. Розуміння ієрархії класів.
- **StatusBar**: `StatusBarItem`. Елементи статусного рядка додатку — прогрес, статус, поточний час.
- **Практичні завдання**: (Рівень 1) GroupBox для групування полів форми. (Рівень 2) Settings-вікно з TabControl (3 вкладки: General, Appearance, Advanced). (Рівень 3) Dashboard з кількома Expander-ами та StatusBar.

**Не згадує**: Data Binding, DataTemplate, стилі/шаблони, MVVM.

---

### Блок 5: Property System — серце WPF (3 + 1🟢 статті)

> Цей блок — теоретичне ядро WPF. Без розуміння DependencyProperty неможливо зрозуміти Binding, Style, Animation. Це "під капотом" кожного контролу.

---

#### `14.dependency-properties-part1.md` — Dependency Properties: концепція та Value Resolution

**Мета**: Зрозуміти, чому WPF не використовує звичайні CLR-властивості для UI і як вирішуються конфлікти значень.

**Зміст**:

- **Hook**: "Чому `Button.Background` — це не просто setter? Чому значення ширини елементу може одночасно надходити з animation, style, local value та default? Як WPF вирішує конфлікт?"
- **Проблема**: CLR-властивості не підтримують прив'язку даних, стилі, анімацію, успадкування значень по дереву. У кожного контролу ~100 властивостей — зберігати всі як поля неефективно (більшість мають default value).
- **Рішення — DependencyProperty**: Статичне поле `public static readonly DependencyProperty` + реєстрація через `DependencyProperty.Register()`. Обгортка CLR-property (getter/setter), що під капотом звертається до DependencyObject.GetValue()/SetValue().
- **Чому "Dependency"**: Значення "залежить" від багатьох джерел. WPF автоматично визначає пріоритет.
- **Value Resolution (Property Value Precedence)**: 11 рівнів пріоритету (від найвищого до найнижчого): Animation → Local Value → Style Triggers → Template Triggers → Style Setters → Theme Style → Inheritance → Default. Діаграма пріоритетів з прикладами.
- **Приклад конфлікту**: Style задає `Background = Blue`, але локальне значення `Background="Red"` — що виграє? (Local Value, бо пріоритет вищий).
- **ClearValue()**: Скинути локальне значення, щоб стиль знову діяв.
- **Property Value Inheritance**: Як `FontSize` на Window автоматично успадковується дочірніми елементами.
- **Практичні завдання**: (Рівень 1) Продемонструвати Value Precedence — задати Background через Style та локально, побачити результат. (Рівень 2) Дослідити, які властивості підтримують Inheritance (FontSize, Foreground) і які ні (Background).

**Не згадує**: Attached Properties (наступна стаття), Binding (Блок 6), створення власних DP (Part 2).

---

#### `14.dependency-properties-part2.md` — Dependency Properties: створення та метадані

**Мета**: Навчитися створювати власні DependencyProperty з метаданими, валідацією та coercion.

**Зміст**:

- **Створення власної DependencyProperty**: Покрокова інструкція (`::steps`). `DependencyProperty.Register(name, type, ownerType, metadata)`. CLR wrapper з GetValue/SetValue. Snippet `propdp` у Visual Studio.
- **PropertyMetadata**: `new PropertyMetadata(defaultValue, propertyChangedCallback)`. PropertyChanged callback — реакція на зміну значення.
- **FrameworkPropertyMetadata**: Розширена версія з прапорцями: `AffectsRender`, `AffectsMeasure`, `AffectsArrange`, `BindsTwoWayByDefault`, `Inherits`. Коли використовувати який прапорець.
- **Coercion callback**: `CoerceValueCallback` — обмеження значення перед його встановленням. Приклад: `ProgressBar.Value` не може бути більше за `Maximum`. Ланцюжок: Validate → Coerce → PropertyChanged.
- **Validation callback**: `ValidateValueCallback` — статична перевірка. Повертає bool. Якщо false — кидає ArgumentException. Різниця з Coercion — валідація відхиляє, coercion виправляє.
- **Read-only Dependency Properties**: `DependencyPropertyKey` через `RegisterReadOnly()`. Зовнішній код може читати, але не може встановити значення. Приклад: `ActualWidth`.
- **Metadata Override**: `OverrideMetadata()` для зміни default value у підкласі.
- **Практичні завдання**: (Рівень 1) Створити DependencyProperty `Title` для custom контролу. (Рівень 2) Створити DP з Coercion (наприклад, `Rating` від 0 до 5). (Рівень 3) Створити `RatingControl` — UserControl з DependencyProperty `Value` (0–5), `MaxRating`, PropertyChanged callback для оновлення зірочок.

---

#### `14a.avalonia-property-system.md` — 🟢 Avalonia Property System: StyledProperty та DirectProperty

**Мета**: Показати, що Avalonia має свою систему властивостей, натхненну WPF, але з важливими відмінностями та покращеннями.

**Зміст**:

- **StyledProperty** — аналог DependencyProperty у WPF. Реєстрація: `AvaloniaProperty.Register<OwnerType, ValueType>(nameof(PropertyName))`. Підтримує стилізацію, binding, animation, value precedence.
- **DirectProperty** — властивість без коштовного value storage. Для часто змінюваних значень (наприклад, `Bounds`, `IsPointerOver`). Ефективніша за StyledProperty, але без підтримки стилів та animation. Реєстрація: `AvaloniaProperty.RegisterDirect<>()`.
- **AttachedProperty в Avalonia**: `AvaloniaProperty.RegisterAttached<>()`. Ті ж концепції, як у WPF.
- **Порівняльна таблиця**: DependencyProperty vs StyledProperty vs DirectProperty — коли що обирати.
- **Value Precedence в Avalonia**: Подібна до WPF, але з деякими відмінностями (Animation, LocalValue, Style).
- **AddOwner**: Аналог WPF `AddOwner()` для перевикористання property в іншому типі.
- **Практичні завдання**: Портувати RatingControl зі статті 14 Part 2 на Avalonia, замінивши DependencyProperty на StyledProperty. Порівняти обсяг коду.

**Не згадує**: CSS-like стилі (Блок 8 companion), Compiled Bindings.

---

#### `15.attached-properties.md` — Attached Properties

**Мета**: Зрозуміти attached properties — механізм, що дозволяє батьківському елементу "передавати" властивості дочірнім.

**Зміст**:

- **Hook**: "Як `Grid.Row` працює на `Button`, якщо `Button` нічого не знає про `Grid`? Чому Button не має властивості `Row`?"
- **Концепція**: Attached Property = DependencyProperty, зареєстрована через `RegisterAttached()`. Belong to one class, set on another.
- **Синтаксис**: `DependencyProperty.RegisterAttached(name, type, ownerType, metadata)`. CLR wrapper: `public static void SetXxx(DependencyObject obj, value)` та `public static T GetXxx(DependencyObject obj)`.
- **Існуючі Attached Properties**: `Grid.Row`, `Grid.Column`, `Grid.RowSpan`, `Grid.ColumnSpan`, `DockPanel.Dock`, `Canvas.Left`, `Canvas.Top`, `Panel.ZIndex`, `ScrollViewer.HorizontalScrollBarVisibility`.
- **Як це працює**: Attached property зберігається в DependencyObject дочірнього елемента через SetValue(). Батьківська панель читає це значення під час Layout pass.
- **Створення власних Attached Properties**: Приклад — `Watermark` attached property для TextBox, що показує placeholder text. Приклад — `FocusOnLoad` attached property, що автоматично фокусує елемент при завантаженні.
- **Практичні завдання**: (Рівень 1) Використати Grid.Row/Column та Panel.ZIndex у складному layout. (Рівень 2) Створити attached property `CornerRadius` для будь-якого елемента. (Рівень 3) Створити `FocusOnLoad` attached property з PropertyChanged callback.

**Не згадує**: Behaviors (Advanced), Binding, стилі.

---

#### `16.routed-events.md` — Routed Events: маршрутизація подій

**Мета**: Зрозуміти систему подій WPF — Tunneling, Bubbling, Direct.

**Зміст**:

- **Hook**: "Ви натискаєте на текст всередині кнопки. Хто отримає Click — TextBlock чи Button? Обидва? У якій послідовності?"
- **Проблема**: У WinForms подія приходить лише конкретному контролу. У WPF елемент — це дерево (Visual Tree). Подія має можливість "подорожувати" по дереву.
- **Три стратегії маршрутизації**:
    - **Tunneling (Preview\*)**: Від кореня Visual Tree до елемента-джерела. Naming convention: `PreviewMouseDown`, `PreviewKeyDown`. Використовується для перехоплення подій до того, як вони досягнуть елемента.
    - **Bubbling**: Від елемента-джерела до кореня. `MouseDown`, `Click`, `KeyDown`. Найчастіший тип.
    - **Direct**: Немає маршрутизації — подія приходить тільки до одного елемента. `MouseEnter`, `MouseLeave`.
- **RoutedEventArgs**: `Source` (логічний елемент, що ініціював подію) vs `OriginalSource` (візуальний елемент, де стався input). `Handled = true` — зупинка маршрутизації (але можна продовжити через `AddHandler(event, handler, handledEventsToo: true)`).
- **Реєстрація власної Routed Event**: `EventManager.RegisterRoutedEvent(name, strategy, handlerType, ownerType)`. CLR event wrapper з `AddHandler`/`RemoveHandler`.
- **Class Handlers**: `EventManager.RegisterClassHandler()` — обробка подій на рівні класу (до instance handlers). Як Button "ловить" Enter для IsDefault.
- **Практичні завдання**: (Рівень 1) Дослідити bubbling — вкладені контроли з обробниками на кожному рівні, логування порядку викликів. (Рівень 2) Перехопити Tunneling-подію (PreviewKeyDown) для заборони введення цифр у TextBox. (Рівень 3) Створити власну routed event `ItemSelected` для custom контролу.

---

### Блок 6: Data Binding — з'єднання UI з даними (5 + 1🟢 статті, 2 розбиті на Part)

> Це **переломний блок**. Студент переходить від code-behind до декларативного зв'язування даних. Після цього блоку ручне оновлення UI через TextBox.Text = "..." буде виглядати як антипатерн.

---

#### `17.data-binding-basics-part1.md` — Data Binding: від code-behind до декларативності

**Мета**: Зрозуміти концепцію прив'язки даних, DataContext та режими Binding.

**Зміст**:

- **Hook**: "Уявіть, що ви пишете форму з 50 полями. Для кожного — TextChanged event, ручне оновлення моделі, ручне оновлення UI. А тепер уявіть, що все це автоматично. Це — Data Binding."
- **Проблема code-behind**: "Spaghetti UI" — десятки обробників подій, тісна зв'язність UI та логіки. Показати реальний приклад: 5 TextBox + 5 TextChanged + ручний маппінг = 50 рядків коду. Той самий код через Binding = 5 рядків.
- **Концепція Binding**: Source (джерело даних) → Target (UI-властивість). Binding Expression `{Binding Path=Name}`. Target — завжди DependencyProperty.
- **DataContext**: Що це? Кожен FrameworkElement має DataContext. Успадкування DataContext по Logical Tree — якщо задати DataContext на Window, всі дочірні елементи "бачать" його. Діаграма пошуку DataContext.
- **Встановлення DataContext**: У code-behind: `DataContext = new Person()`. У XAML: через ObjectDataProvider або resource (поки без MVVM).
- **Binding Modes**: `OneWay` (Source → Target), `TwoWay` (Source ↔ Target), `OneTime` (одноразово), `OneWayToSource` (Target → Source), `Default` (залежить від контролу — TextBox.Text = TwoWay, TextBlock.Text = OneWay). Коли який використовувати з прикладами.
- **Перший робочий приклад**: POCO-клас Person → DataContext → TextBlock.Text `{Binding Name}`. Показати, що при запуску текст відображається.
- **Практичні завдання**: (Рівень 1) Створити клас Person, задати DataContext, прив'язати ім'я до TextBlock. (Рівень 2) Форма профілю з 5 полями через Binding. (Рівень 3) Порівняти: та сама форма через code-behind та Binding — порахувати рядки коду.

**Не згадує**: INotifyPropertyChanged (Part 2), MVVM (Блок 7), Commands, Value Converters.

---

#### `17.data-binding-basics-part2.md` — INotifyPropertyChanged: живе оновлення

**Мета**: Вирішити проблему "Binding не оновлює UI при зміні властивості" через INotifyPropertyChanged.

**Зміст**:

- **Проблема**: "Ви встановили Binding, але коли змінюєте властивість у коді — UI не оновлюється. Чому?" Тому що POCO-клас не повідомляє Binding Engine про зміни.
- 🔵 **Recap інтерфейсів** (для студентів зі слабким ООП): Що таке інтерфейс — контракт, який клас зобов'язується виконати. `INotifyPropertyChanged` — це контракт: "я обіцяю повідомити, коли моя властивість зміниться". Посилання на розділ ООП для глибини.
- **INotifyPropertyChanged**: Інтерфейс з одним event: `PropertyChanged`. Як його реалізувати: `OnPropertyChanged()` метод з `[CallerMemberName]`. Чому потрібен `CallerMemberName` — щоб не писати `OnPropertyChanged("Name")` вручну (помилка при рефакторингу).
- **Setter з перевіркою на зміну**: `if (value != _name) { _name = value; OnPropertyChanged(); }` — уникнення зайвих оновлень UI.
- **UpdateSourceTrigger**: `PropertyChanged` (оновлення миттєво при кожному натисканні клавіші), `LostFocus` (оновлення при втраті фокусу — за замовчуванням для TextBox), `Explicit` (оновлення тільки при виклику `BindingExpression.UpdateSource()`).
- **Демонстрація**: TwoWay Binding + INPC = форма, де зміна в TextBox миттєво відображається в TextBlock (і навпаки).
- **Практичні завдання**: (Рівень 1) Додати INPC до класу Person, побачити live-оновлення. (Рівень 2) Форма профілю з TwoWay binding та live-preview. (Рівень 3) Калькулятор: два TextBox → зміна одного миттєво перераховує результат.

---

#### `17a.avalonia-compiled-bindings.md` — 🟢 Compiled Bindings в Avalonia

**Мета**: Показати ключову перевагу Avalonia — compile-time перевірка Binding.

**Зміст**:

- **Проблема Reflection Bindings у WPF**: Binding у WPF використовує Reflection — помилки виявляються лише в runtime (і часто мовчки ігноруються). `{Binding Nane}` (опечатка) — WPF мовчить на продакшні.
- **Compiled Bindings**: `x:CompileBindings="True"` — за замовчуванням у Avalonia. Binding перевіряється компілятором. Опечатка → помилка компіляції.
- **x:DataType**: `x:DataType="vm:MainViewModel"` — вказує тип DataContext для compile-time перевірки. IntelliSense підказує доступні властивості.
- **ReflectionBinding як fallback**: Коли потрібен старий підхід — наприклад, при binding до dynamic data.
- **Performance**: Compiled Bindings не використовують Reflection → швидше, менше алокацій.
- **Порівняльна таблиця**: WPF ReflectionBinding vs Avalonia CompiledBinding — syntax, error handling, performance.
- **Практичні завдання**: Портувати Binding-форму зі статті 17 на Avalonia з Compiled Bindings. Спровокувати compile-time error через опечатку.

---

#### `18.data-binding-advanced.md` — Просунутий Data Binding

**Мета**: Опанувати розширені можливості Binding для складних сценаріїв.

**Зміст**:

- **ElementName Binding**: Прив'язка до іншого UI-елемента. `{Binding ElementName=slider, Path=Value}`. Use case: синхронізація двох контролів.
- **RelativeSource Binding**: `Self` (прив'язка до себе), `FindAncestor` (пошук батька по типу), `TemplatedParent` (всередині ControlTemplate). Приклади кожного з use case.
- **MultiBinding**: Об'єднання кількох джерел в одне значення через `IMultiValueConverter`. Приклад: FullName = FirstName + " " + LastName.
- **PriorityBinding**: Fallback при повільних джерелах — показати placeholder поки дані завантажуються.
- **Binding Failures та Debugging**: Output Window з Binding errors. `PresentationTraceSources.TraceLevel="High"` для діагностики. `FallbackValue` (значення при помилці binding), `TargetNullValue` (значення при null джерела).
- **StringFormat**: Форматування прямо у binding — `{Binding Price, StringFormat='{}{0:C2}'}`. Формати дат, чисел.
- **Validation**: `IDataErrorInfo` (legacy), `INotifyDataErrorInfo` (сучасний), `ValidationRules`. `Validation.ErrorTemplate` для кастомного відображення помилок (червона рамка, tooltip з помилкою).
- **Практичні завдання**: (Рівень 1) Slider + TextBlock через ElementName. (Рівень 2) Калькулятор з MultiBinding — сума двох TextBox. (Рівень 3) Форма реєстрації з INotifyDataErrorInfo та кастомним ErrorTemplate.

---

#### `19.value-converters.md` — Value Converters: перетворення даних

**Мета**: Навчитися перетворювати типи даних між Source та Target у Binding.

**Зміст**:

- **Проблема**: Boolean → Visibility? DateTime → String? Enum → Color? Binding потребує перетворення типів, коли Source property і Target property — різних типів.
- **IValueConverter**: Інтерфейс з методами `Convert()` (Source → Target) та `ConvertBack()` (Target → Source). `parameter` для передачі додаткових даних. `CultureInfo` для локалізації.
- **Стандартні конвертери WPF**: `BooleanToVisibilityConverter` (вбудований). Як використовувати: реєстрація у ресурсах, `Converter={StaticResource conv}`.
- **Створення кастомних конвертерів**: `InverseBoolConverter`, `EnumToBrushConverter`, `NullToVisibilityConverter`, `DateToStringConverter`. Кожен з повним прикладом коду та XAML використанням.
- **MarkupExtension + Converter**: Патерн — конвертер як MarkupExtension для уникнення реєстрації в ресурсах: `Converter={local:InverseBoolConverter}`.
- **IMultiValueConverter**: Для MultiBinding — отримує масив values, повертає одне value.
- **Практичні завдання**: (Рівень 1) BooleanToVisibilityConverter — показати/приховати елемент через CheckBox. (Рівень 2) Створити бібліотеку з 5+ конвертерів. (Рівень 3) Конвертер з ConverterParameter — один конвертер, різна поведінка.

**Не згадує**: DataTemplate (наступна стаття), MVVM.

---

#### `20.data-templates.md` — Data Templates: візуалізація об'єктів

**Мета**: Показати, як перетворити C#-об'єкт у красивий UI-елемент автоматично.

**Зміст**:

- **Проблема**: Коли ви прив'язуєте об'єкт до ContentControl або ListBox, WPF показує `ToString()`. Як показати щось красиве — ім'я, фото, email?
- **DataTemplate**: Визначення у ресурсах або inline. `DataType="{x:Type local:Person}"`. Всередині — XAML з Binding до властивостей об'єкта.
- **Implicit vs Explicit DataTemplates**: Implicit — без `x:Key`, автоматично застосовується до всіх об'єктів цього типу. Explicit — з `x:Key`, застосовується вручну через `ItemTemplate`.
- **DataTemplateSelector**: Клас що override `SelectTemplate()` — програмний вибір шаблону залежно від даних. Приклад: різний шаблон для VIP та звичайних клієнтів.
- **HierarchicalDataTemplate**: Для TreeView — рекурсивний шаблон з `ItemsSource` для дочірніх елементів.
- **ContentTemplate vs ItemTemplate**: Різниця — ContentControl.ContentTemplate vs ItemsControl.ItemTemplate.
- **Практичні завдання**: (Рівень 1) Відображення Person у ContentControl з DataTemplate (ім'я + вік). (Рівень 2) Список контактів — ListBox з DataTemplate (аватар, ім'я, email). (Рівень 3) DataTemplateSelector для різних типів повідомлень (текст, зображення, посилання).

---

#### `21.collections-binding-part1.md` — Прив'язка колекцій: ObservableCollection та ItemsControl

**Мета**: Навчитися прив'язувати колекції C#-об'єктів до UI-списків із автоматичним оновленням.

**Зміст**:

- **Проблема**: `List<T>` не повідомляє UI про додавання/видалення елементів. Додаєте елемент — UI не змінюється.
- **ObservableCollection\<T\>**: Реалізує `INotifyCollectionChanged`. Автоматично сповіщає Binding Engine про Add, Remove, Replace, Reset. Чому не `List<T>`.
- **ItemsControl**: Базовий клас для ListBox, ComboBox, ListView. `ItemsSource` для прив'язки колекції. `ItemTemplate` для DataTemplate. `ItemsPanel` (панель для розташування елементів).
- **Прив'язка**: `ItemsSource="{Binding People}"` де `People` — ObservableCollection\<Person\> у DataContext.
- **SelectedItem та SelectedIndex**: Прив'язка вибраного елемента до ViewModel-property. TwoWay binding за замовчуванням.
- **Додавання/Видалення**: Кнопка "Додати" → код додає в ObservableCollection → UI автоматично показує новий елемент.
- **Практичні завдання**: (Рівень 1) ListBox з ObservableCollection\<string\> + кнопка "Додати". (Рівень 2) Список контактів з DataTemplate, Add/Remove через code-behind. (Рівень 3) Master-Detail: ListBox зліва, деталі справа через SelectedItem.

**Не згадує**: ICollectionView (Part 2), Virtualization (Part 2), MVVM.

---

#### `21.collections-binding-part2.md` — ICollectionView, Filtering, Sorting та Virtualization

**Мета**: Навчитися сортувати, фільтрувати та групувати колекції без зміни вихідних даних, і зрозуміти віртуалізацію.

**Зміст**:

- **ICollectionView**: "Вигляд" на колекцію — сортування, фільтрація, групування без зміни оригінальних даних. `CollectionViewSource.GetDefaultView(collection)`.
- **SortDescription**: `collectionView.SortDescriptions.Add(new SortDescription("Name", ListSortDirection.Ascending))`. Множинне сортування.
- **Filter**: `collectionView.Filter = item => ((Person)item).Age > 18`. Predicate-based фільтрація. Оновлення фільтру через `Refresh()`.
- **GroupDescriptions**: `PropertyGroupDescription("City")`. `GroupStyle` у ListBox для заголовків груп.
- **CollectionViewSource у XAML**: Декларативне визначення сортування та групування.
- **Virtualization**: `VirtualizingStackPanel` — WPF створює UI-елементи тільки для видимих рядків. Чому список з 100,000 елементів працює швидко. `VirtualizingPanel.VirtualizationMode` (Standard vs Recycling). Коли Virtualization не працює (ScrollViewer всередині ItemsControl без фіксованої висоти).
- **Практичні завдання**: (Рівень 1) Сортування списку по імені через SortDescription. (Рівень 2) Фільтрація + сортування: TextBox для пошуку + ComboBox для порядку. (Рівень 3) Повний Todo-додаток — список завдань з фільтрацією (All/Active/Completed), сортуванням та додаванням.

---

### Блок 7: MVVM — архітектурний патерн (5 + 1🟢 статті)

> Найважливіший архітектурний блок. MVVM — стандарт для WPF/Avalonia. Після цього блоку студент ніколи не повернеться до code-behind для бізнес-логіки.

---

#### `22.mvvm-pattern.md` — MVVM: Від Spaghetti до архітектури

**Мета**: Зрозуміти MVVM як патерн, його мотивацію та структуру. Показати "чому", а не лише "як".

**Зміст**:

- **Hook**: "Ваш code-behind файл має 500 рядків. Бізнес-логіка змішана з UI-логікою. Як це тестувати? Як це підтримувати у команді? Як додати нову фічу, не зламавши все?"
- 🔵 **Recap ООП** (для студентів зі слабким ООП): Інтерфейси як контракти (3 абзаци) — що означає `class MyClass : INotifyPropertyChanged`. Поліморфізм — чому ViewModel може бути будь-яким об'єктом. Events — механізм сповіщення (студенти вже знають delegates/events). Посилання на розділ 2.4 (OOP Pillars) для глибини.
- **Проблема code-behind**: Tight coupling (UI залежить від логіки і навпаки), untestable (як тестувати Button.Click?), duplicated logic (та сама логіка в двох вікнах).
- **Еволюція архітектурних патернів**: MVC (1979, Smalltalk) → MVP (WinForms era) → MVVM (2005, John Gossman для WPF). Чому MVVM ідеальний саме для XAML-платформ — через Data Binding як "клей". Діаграма Mermaid.
- **Три компоненти**:
    - **Model**: Бізнес-логіка та дані. Чистий C# без залежності від UI. Може бути: Entity, DTO, Service.
    - **View**: XAML-файл. Мінімальний code-behind — тільки `InitializeComponent()` і, можливо, UI-специфічна логіка (анімації).
    - **ViewModel**: INotifyPropertyChanged, публічні властивості, команди. Посередник між Model і View. Не знає конкретну View.
- **Потік даних**: View ←→ (Data Binding) ←→ ViewModel → Model. Діаграма взаємодії.
- **Золоте правило**: View знає ViewModel (через DataContext). ViewModel **не знає** View. Model не знає ні View, ні ViewModel.
- **Практичні завдання**: (Рівень 1) Визначити Model, View, ViewModel для калькулятора. (Рівень 2) Перенести існуючий code-behind Todo-додаток на MVVM (вручну, без фреймворків). (Рівень 3) Порівняти testability: написати unit-test для ViewModel (просто) vs для code-behind (неможливо без UI).

**Не згадує**: CommunityToolkit.Mvvm (Стаття 25), Messenger (Стаття 26), DI (Блок 12).

---

#### `23.viewmodel-implementation.md` — Реалізація ViewModel: BaseViewModel, Properties, Validation

**Мета**: Створити повноцінну інфраструктуру ViewModel вручну (перед тим, як автоматизувати через Toolkit).

**Зміст**:

- **BaseViewModel / ObservableObject**: Створення базового класу з INotifyPropertyChanged. Метод `SetProperty<T>(ref T field, T value, [CallerMemberName] propertyName)` — перевірка на зміну, оновлення поля, виклик PropertyChanged.
- **Обчислювані властивості (Computed Properties)**: Залежності між властивостями — зміна `FirstName` має оновити `FullName`. Виклик `OnPropertyChanged(nameof(FullName))` після зміни `FirstName`.
- **Валідація у ViewModel**: `INotifyDataErrorInfo` — сучасний підхід. `GetErrors(propertyName)`, `HasErrors`, `ErrorsChanged`. Зберігання помилок у Dictionary. Приклад: "Ім'я має бути від 2 до 50 символів".
- **Показ помилок у View**: `Validation.ErrorTemplate`, `Validation.HasError`, `ToolTip з Binding до Validation.Errors`.
- **DesignTime Data**: `d:DataContext="{d:DesignInstance local:MainViewModel, IsDesignTimeCreatable=True}"`. Перегляд у дизайнері Visual Studio / Rider з fake даними. `d:DesignWidth`, `d:DesignHeight`.
- **Практичні завдання**: (Рівень 1) Створити BaseViewModel та використати для простої форми. (Рівень 2) ViewModel для форми реєстрації з 3+ валідаціями. (Рівень 3) DesignTime data для складного інтерфейсу.

---

#### `24.commands.md` — Commands: замість event handlers

**Мета**: Замінити Click-обробники у code-behind на декларативні команди, що живуть у ViewModel.

**Зміст**:

- **Проблема**: Event handlers живуть у code-behind. ViewModel не може підписатися на `Button.Click`. Як звʼязати натискання кнопки з логікою у ViewModel?
- **ICommand інтерфейс**: `Execute(object? parameter)`, `CanExecute(object? parameter)`, `CanExecuteChanged` event. Binding: `Command="{Binding SaveCommand}"`.
- **RelayCommand** (ручна реалізація): Делегати `Action<object?>` для Execute та `Func<object?, bool>` для CanExecute. Повна реалізація класу (~30 рядків).
- **CanExecute → IsEnabled**: Автоматичне відключення кнопки, коли CanExecute повертає false. `CommandManager.RequerySuggested` для автоматичного перевірки.
- **CommandParameter**: Передача даних з View в Command через `CommandParameter="{Binding SelectedItem}"`.
- **AsyncRelayCommand**: Асинхронне виконання з `Task`-based Execute. `IsBusy` property для показу індикатора завантаження. Handling exceptions.
- **InputBindings / KeyBindings**: `<Window.InputBindings><KeyBinding Key="S" Modifiers="Ctrl" Command="{Binding SaveCommand}"/></Window.InputBindings>`.
- **Практичні завдання**: (Рівень 1) Кнопка "Save" з Command та CanExecute (disabled коли поля пусті). (Рівень 2) CRUD-застосунок з Commands для Add, Edit, Delete. (Рівень 3) AsyncRelayCommand з ProgressBar та Cancel.

---

#### `25.mvvm-toolkit.md` — CommunityToolkit.Mvvm: MVVM без boilerplate

**Мета**: Познайомити з фреймворком, що автоматизує boilerplate через Source Generators.

**Зміст**:

- **Hook**: "Ви щойно написали 50 рядків для однієї властивості з INotifyPropertyChanged та 30 рядків для однієї команди. А тепер — по 1 рядку на кожну."
- **Встановлення**: NuGet `CommunityToolkit.Mvvm`. Чому цей тулкіт — Microsoft-backed, platform-agnostic (працює і в WPF, і в Avalonia).
- **`[ObservableProperty]`**: Атрибут на `private` поле → Source Generator створює публічну властивість з PropertyChanged + partial methods `OnNameChanging(string value)`, `OnNameChanged(string value)` для кастомної логіки.
- **`[RelayCommand]`**: Атрибут на метод → автоматична ICommand-property. Async через `async Task`-метод → автоматичний AsyncRelayCommand з CanBeCanceled.
- **`[NotifyPropertyChangedFor(nameof(FullName))]`**: Залежні властивості — при зміні `FirstName` автоматично оновлюється `FullName`.
- **`[NotifyCanExecuteChangedFor(nameof(SaveCommand))]`**: Автоматичне оновлення CanExecute при зміні властивості.
- **ObservableValidator**: `[Required]`, `[MinLength]`, `[EmailAddress]` — Data Annotations у MVVM. `ValidateAllProperties()`, `GetErrors()`.
- **Source Generators під капотом**: Як подивитися згенерований код (Analyzers → CommunityToolkit.Mvvm.SourceGenerators). Що саме генерується — показати diff між ручним та згенерованим кодом.
- **Практичні завдання**: (Рівень 1) Переписати BaseViewModel на ObservableObject з Toolkit. (Рівень 2) CRUD-додаток з [ObservableProperty] та [RelayCommand]. (Рівень 3) Форма з ObservableValidator та Data Annotations.

---

#### `25a.avalonia-mvvm-reactiveui.md` — 🟢 MVVM в Avalonia: CommunityToolkit + ReactiveUI

**Мета**: Показати два підходи до MVVM в Avalonia та особливий механізм ViewLocator.

**Зміст**:

- **CommunityToolkit.Mvvm в Avalonia**: Працює 1:1 як у WPF. Ті ж `[ObservableProperty]`, `[RelayCommand]` — код ViewModel ідентичний. Портувати ViewModel із WPF → нуль змін.
- **ReactiveUI — альтернативний підхід**: `ReactiveObject` (базовий клас), `this.WhenAnyValue(x => x.SearchText)` (реактивні потоки), `ObservableAsPropertyHelper<T>` (обчислювані реактивні властивості). Коли ReactiveUI кращий — складні reactive pipelines, debounce для пошуку, combineLast.
- **ViewLocator**: Автоматичний зв'язок View ↔ ViewModel за конвенцією імен. `MainViewModel → MainView`. Клас `ViewLocator : IDataTemplate`. Як це працює — DataTemplate з Match за типом.
- **Compiled Bindings + MVVM**: `x:DataType="vm:MainViewModel"` → IntelliSense для Binding, compile-time перевірка. Перевага над WPF.
- **DI в Avalonia MVVM**: Constructor injection у ViewModel через IServiceProvider (детально — у Блоці 12).
- **Практичні завдання**: (Рівень 1) CRUD на CommunityToolkit.Mvvm в Avalonia. (Рівень 2) Search box з ReactiveUI debounce. (Рівень 3) ViewLocator для 3 ViewModel/View пар.

---

#### `26.messenger-pattern.md` — Messenger: комунікація між ViewModel

**Мета**: Як ViewModel'и спілкуються одна з одною без прямих посилань (loose coupling).

**Зміст**:

- **Проблема**: MainViewModel потрібно знати, що SettingsViewModel змінила тему. Пряме посилання `MainViewModel.settingsVm` — порушення MVVM та tight coupling.
- **Mediator Pattern**: Центральний посередник — всі ViewModel підписуються на повідомлення і відправляють їх через посередника.
- **WeakReferenceMessenger**: CommunityToolkit.Mvvm реалізація з слабкими посиланнями (не запобігає Garbage Collection). `WeakReferenceMessenger.Default`.
- **StrongReferenceMessenger**: Альтернатива з сильними посиланнями — швидша, але потребує ручного Unregister.
- **Надсилання та отримання**: `Messenger.Send(new ThemeChangedMessage("Dark"))`, `Messenger.Register<ThemeChangedMessage>(this, (r, msg) => ...)`.
- **Типи повідомлень**: `ValueChangedMessage<T>` (простий), `RequestMessage<T>` (запит-відповідь — ViewModel запитує дані в іншої), `CollectionRequestMessage<T>` (множинна відповідь).
- **Unregister**: `Messenger.Unregister<T>(this)`. Чому важливо відписуватися — memory leaks.
- **Практичні завдання**: (Рівень 1) Надіслати повідомлення про зміну теми між двома ViewModel. (Рівень 2) Навігація між View через Messenger (NavigateMessage). (Рівень 3) RequestMessage — діалог підтвердження, де одна ViewModel запитує в іншої "Зберегти зміни?".

---

### Блок 8: Стилізація та шаблони (4 + 4🟢 статті)

> Студент вчиться кастомізувати зовнішній вигляд будь-якого контролу — від простих стилів до повної перебудови через ControlTemplate.

---

#### `27.styles-basics.md` — Стилі: CSS для WPF

**Мета**: Зрозуміти систему стилів WPF як спосіб уніфікувати зовнішній вигляд.

**Зміст**:

- **Аналогія**: Стилі WPF як CSS для десктопу. Style = набір Setter'ів. Setter = CSS-правило (`Property` + `Value`).
- **Style**: `TargetType` визначає, до якого типу контролу застосувати стиль. `Setter` задає значення властивості. Приклад: всі кнопки мають `Padding="10"`, `FontSize="14"`.
- **Implicit Style**: Стиль без `x:Key` — автоматично застосовується до **всіх** контролів вказаного TargetType у scope. Як CSS wildcard selector.
- **Explicit Style**: Стиль з `x:Key` — застосовується через `Style="{StaticResource myStyle}"`. Як CSS class selector.
- **BasedOn**: Успадкування стилів — один стиль розширює інший. `BasedOn="{StaticResource {x:Type Button}}"`. Аналог CSS cascade.
- **Scope**: Стилі у Resources елемента (тільки для нащадків), Window (для всього вікна), Application (для всього додатку). Ієрархія пріоритетів.
- **Практичні завдання**: (Рівень 1) Створити implicit стиль для всіх кнопок із єдиним FontSize та Padding. (Рівень 2) 3 explicit стилі — PrimaryButton, SecondaryButton, DangerButton із BasedOn. (Рівень 3) Повна стилізація форми — всі TextBox, Label, Button мають єдиний дизайн.

---

#### `27a.avalonia-css-styling.md` — 🟢 CSS-like стилі Avalonia

**Мета**: Показати принципово інший (і потужніший) підхід до стилізації в Avalonia.

**Зміст**:

- **CSS-like Selectors**: Замість `TargetType` — селектори як у CSS. `Button` (за типом), `Button.accent` (за класом), `Button:pointerover` (за станом), `TextBox:focus /template/ Border` (у шаблоні). Повний список доступних селекторів.
- **Style Classes**: `Classes="primary large"` — як CSS-класи. Додавання/видалення через code-behind: `element.Classes.Add("active")`.
- **Nesting та Combinators**: `StackPanel > Button` (прямий нащадок), `StackPanel Button` (будь-який нащадок), `Button:nth-child(2n)`.
- **Каскадність та Specificity**: Правила пріоритету: inline > style > selector. Порівняння з CSS specificity rules.
- **Порівняння з WPF**: Таблиця — WPF Style vs Avalonia Style. Avalonia — значно ближча до CSS, гнучкіша.
- **Практичні завдання**: (Рівень 1) Стилізувати кнопки через класи `primary`/`secondary`. (Рівень 2) Hover-ефект через `:pointerover` селектор. (Рівень 3) Складний селектор для таблиці — пофарбувати кожен парний рядок.

---

#### `28.control-templates-part1.md` — Control Templates: концепція та TemplateBinding

**Мета**: Зрозуміти, що зовнішній вигляд будь-якого контролу можна повністю перевизначити.

**Зміст**:

- **Hook**: "Button у WPF — це не прямокутник з текстом. Це _поведінка_ (Click, Focus, Hover). Зовнішній вигляд — це Template, який можна замінити повністю. Хочете круглу кнопку? Кнопку-зірку? Без обмежень."
- **ControlTemplate**: Визначення всередині Style через `<Setter Property="Template"><Setter.Value><ControlTemplate>...</ControlTemplate></Setter.Value></Setter>`. Або напряму через `Template="{StaticResource myTemplate}"`.
- **TemplateBinding**: Прив'язка до властивостей "батьківського" контролу з шаблону. `{TemplateBinding Background}`, `{TemplateBinding Padding}`. Чому це потрібно — щоб шаблон реагував на зовнішні властивості.
- **Мінімальний приклад**: Button з ControlTemplate — лише `Border` + `ContentPresenter`.
- **Порівняння Default Template vs Custom**: Показати, як виглядає стандартний шаблон Button (через Blend/Snoop), і як створити свій.
- **Практичні завдання**: (Рівень 1) Створити круглу кнопку (Ellipse замість Rectangle). (Рівень 2) Button як іконка без фону — лише ContentPresenter.

**Не згадує**: Named Parts, ContentPresenter/ItemsPresenter деталі (Part 2).

---

#### `28.control-templates-part2.md` — Control Templates: Named Parts та ContentPresenter

**Мета**: Опанувати просунуті механізми шаблонування.

**Зміст**:

- **ContentPresenter**: Де у шаблоні відображається `Content`. Без нього — Content "зникає". `ContentSource`, `ContentTemplate`.
- **ItemsPresenter**: Аналог для ItemsControl — де відображаються Items.
- **Named Parts (PART\_\*)**: Конвенція іменування. Контрол очікує певні елементи в шаблоні — наприклад, `TextBox` очікує `PART_ContentHost`. Якщо елемент відсутній — функціонал не працює, але контрол не падає.
- **OnApplyTemplate()**: Метод, де контрол "знаходить" свої Named Parts через `GetTemplateChild()`.
- **Типові помилки**: Забули ContentPresenter → Content не видно. Неправильна назва PART → функціонал зламаний.
- **Практичні завдання**: (Рівень 1) Кастомний ProgressBar із градієнтом. (Рівень 2) Кастомний CheckBox зі switch-toggle дизайном. (Рівень 3) Кастомний ComboBox із зміненою dropdown-панеллю.

---

#### `28a.avalonia-control-themes.md` — 🟢 Control Themes в Avalonia

**Мета**: Показати нову систему стилізації контролів в Avalonia, що замінює WPF-підхід.

**Зміст**:

- **ControlTheme**: Нова концепція (Avalonia 11+) — спеціальний об'єкт для теми контролу, на відміну від WPF, де тема = implicit Style з ControlTemplate.
- **Selector-based approach**: Використання CSS-like селекторів всередині ControlTheme замість Triggers.
- **Порівняння з WPF**: WPF ControlTemplate + Triggers vs Avalonia ControlTheme + Selectors. Avalonia-підхід більш декларативний.
- **Overriding existing themes**: Як перевизначити тему вбудованого контролу.
- **Практичні завдання**: Портувати ControlTemplate кастомної кнопки зі статті 28 на Avalonia ControlTheme.

---

#### `29.triggers-visual-states.md` — Triggers та Visual State Manager

**Мета**: Додати інтерактивну поведінку стилів — зміна зовнішності контролу в залежності від стану.

**Зміст**:

- **Property Triggers**: `<Trigger Property="IsMouseOver" Value="True"><Setter Property="Background" Value="LightBlue"/></Trigger>`. Автоматичне повернення до попереднього значення при Value=False.
- **Data Triggers**: `<DataTrigger Binding="{Binding IsActive}" Value="True">` — реакція на дані ViewModel.
- **MultiTrigger, MultiDataTrigger**: Кілька умов одночасно.
- **Event Triggers**: Для запуску анімацій — `<EventTrigger RoutedEvent="Loaded">`. Коротке введення (повні анімації — Блок 11).
- **Visual State Manager (VSM)**: `VisualStateGroups`, `VisualState`, `GoToState()`. Transitions між станами. Сучасна альтернатива Triggers.
- **Triggers vs VSM**: Порівняння підходів. Triggers — простіші, VSM — масштабніший та closeer до Avalonia/UWP підходу.
- **Практичні завдання**: (Рівень 1) Кнопка міняє колір при IsMouseOver. (Рівень 2) Панель з Data Trigger — змінює стиль коли IsActive=true. (Рівень 3) Toggle-кнопка з Trigger: змінює текст та колір залежно від IsChecked.

---

#### `29a.avalonia-pseudo-classes.md` — 🟢 Pseudo-classes замість Triggers

**Мета**: Показати, що Avalonia відмовилась від Triggers і замінила їх CSS pseudo-classes.

**Зміст**:

- **Відсутність Triggers**: В Avalonia немає Trigger, DataTrigger. Натомість — pseudo-classes та CSS-like селектори.
- **Вбудовані pseudo-classes**: `:pointerover` (IsMouseOver), `:pressed` (IsPressed), `:focus`, `:disabled`, `:checked`, `:unchecked`, `:empty`.
- **Використання у стилях**: `<Style Selector="Button:pointerover"><Setter Property="Background" Value="Blue"/></Style>`.
- **Custom pseudo-classes**: `PseudoClasses.Set(":active", isActive)` у code-behind або ViewModel. Створення reactive стилів для custom стану.
- **Data-driven styling**: Використання `x:DataType` + compiled bindings + pseudo-classes для реактивних стилів.
- **Порівняння з WPF Triggers**: Таблиця відповідностей — кожен WPF Trigger → Avalonia equivalent.
- **Практичні завдання**: (Рівень 1) Hover-ефект через `:pointerover`. (Рівень 2) Custom pseudo-class `:selected` для custom контролу. (Рівень 3) Портувати всі Trigger-приклади зі статті 29 на Avalonia pseudo-classes.

---

#### `30.resources-themes.md` — Теми та ресурсні словники

**Мета**: Побудувати систему тематизації для великого WPF-додатку.

**Зміст**:

- **Тематизація**: Темна/Світла тема. DynamicResource для runtime-зміни — замінити Resource Dictionary, і всі елементи оновляться. Механізм: `Application.Current.Resources.MergedDictionaries.Clear()` → додати нове.
- **Resource Dictionary організація**: Структура файлів великого проєкту — `Themes/Light.xaml`, `Themes/Dark.xaml`, `Styles/Buttons.xaml`, `Styles/TextBoxes.xaml`.
- **MergedDictionaries**: Об'єднання та заміна словників у runtime.
- **Themed Resources**: `SystemColors`, `SystemFonts` — доступ до системних кольорів ОС.
- **Бібліотеки тем** (огляд): MaterialDesignInXamlToolkit (Material Design), MahApps.Metro (Metro/Modern UI), HandyControl (набір контролів). NuGet установка, базова інтеграція.
- **Практичні завдання**: (Рівень 1) Два Resource Dictionary — Light та Dark. (Рівень 2) Перемикач теми через кнопку/toggle. (Рівень 3) Інтеграція MaterialDesignInXamlToolkit у існуючий проєкт.

---

#### `30a.avalonia-themes-fluent.md` — 🟢 Fluent Theme в Avalonia

**Мета**: Показати систему тематизації Avalonia — вбудовану, потужну, з підтримкою варіантів.

**Зміст**:

- **Fluent Theme**: Вбудована тема Avalonia, що імітує Windows 11 Fluent Design. Підключення: `<FluentTheme />` у App.axaml.
- **Simple Theme**: Мінімальна тема для кастомізації з нуля.
- **Theme Variants**: `RequestedThemeVariant="Dark"` / `"Light"` / `"Default"` (слідує за ОС). Runtime switching.
- **ThemeVariant.Dark / Light**: Ресурси, що автоматично змінюються залежно від теми. `{DynamicResource SystemAccentColor}`.
- **Semi.Avalonia, Material.Avalonia**: Популярні community-теми.
- **Порівняння з WPF theming**: WPF потребує ручної роботи (MergedDictionaries swap). Avalonia — вбудований механізм.
- **Практичні завдання**: (Рівень 1) Перемикач Dark/Light через RequestedThemeVariant. (Рівень 2) Кастомний AccentColor. (Рівень 3) Автоматичне слідування за системною темою.

---

### Блок 9: Просунуті контроли (5 статей)

> Студент опрацьовує складні контроли для роботи з великими наборами даних.

---

#### `31.collection-controls.md` — Контроли колекцій: глибоке занурення

**Мета**: Зрозуміти архітектуру ItemsControl та опанувати просунуте використання ListBox/ListView.

**Зміст**:

- **ItemsControl архітектура**: `ItemsSource` → `ItemContainerGenerator` → `ItemsPanel` → `ItemContainer`. Як WPF перетворює колекцію об'єктів на UI-елементи. Діаграма Mermaid.
- **ItemsPanel**: Заміна стандартної панелі — `VirtualizingStackPanel` → `WrapPanel` або `Canvas` для нестандартних layouts. `<ItemsPanelTemplate><WrapPanel/></ItemsPanelTemplate>`.
- **ItemContainerStyle**: Стилізація контейнера (ListBoxItem) — hover, selected, alternating row colors.
- **ListBox vs ListView**: ListBox — простий список. ListView — розширений з підтримкою GridView для табличного вигляду.
- **AlternationCount та AlternationIndex**: Зебра-стиль для рядків.
- **Практичні завдання**: (Рівень 1) Горизонтальний ListBox з WrapPanel. (Рівень 2) Галерея зображень — ListBox з WrapPanel + DataTemplate. (Рівень 3) Карткова сітка продуктів із ItemContainerStyle.

---

#### `32.datagrid-part1.md` — DataGrid: колонки та базове відображення

**Мета**: Познайомити з DataGrid — потужним контролом для табличних даних.

**Зміст**:

- **DataGrid**: Коли використовувати DataGrid замість ListView — редагування, сортування, великі набори даних.
- **AutoGenerateColumns**: Автоматичне створення колонок з публічних властивостей. `AutoGenerateColumns="False"` для ручного контролю.
- **Типи колонок**: `DataGridTextColumn`, `DataGridCheckBoxColumn`, `DataGridComboBoxColumn`, `DataGridTemplateColumn`. Коли який використовувати.
- **DataGridTemplateColumn**: CellTemplate та CellEditingTemplate — різні шаблони для відображення та редагування.
- **Binding**: `Binding="{Binding Name}"` у колонках.
- **Frozen Columns**: `FrozenColumnCount` — зафіксувати ліві колонки при горизонтальному скролі.
- **Практичні завдання**: (Рівень 1) Таблиця продуктів з 4 колонками. (Рівень 2) DataGridTemplateColumn з кнопкою "Delete" у кожному рядку. (Рівень 3) DataGrid з ComboBoxColumn та CheckBoxColumn.

---

#### `32.datagrid-part2.md` — DataGrid: сортування, фільтрація, редагування

**Мета**: Просунуте використання DataGrid — sorting, filtering, editing, validation.

**Зміст**:

- **Сортування**: Клік по заголовку. `CanUserSortColumns`. Кастомне сортування через ICollectionView.
- **Фільтрація**: ICollectionView.Filter інтеграція — TextBox для пошуку, ComboBox для фільтрації за категорією.
- **Групування**: `GroupStyle` із заголовками та підрахунком елементів.
- **Редагування**: `CellEditEnding`, `RowEditEnding` events. `IsReadOnly` для окремих колонок. `BeginEdit()`, `CancelEdit()`, `CommitEdit()`.
- **Валідація у DataGrid**: `Validation.ErrorTemplate`, `RowValidationRules`. Показ помилок по рядку.
- **Selection**: `SelectionUnit` (Cell, FullRow, CellOrRowHeader), `SelectionMode`.
- **Практичні завдання**: (Рівень 1) DataGrid з сортуванням. (Рівень 2) Таблиця замовлень з фільтрацією по статусу + пошуком по імені. (Рівень 3) Повний CRUD через DataGrid — редагування inline, валідація, видалення.

---

#### `33.treeview-listview.md` — TreeView та GridView

**Мета**: Опанувати ієрархічні та табличні контроли.

**Зміст**:

- **TreeView**: `HierarchicalDataTemplate` — рекурсивне відображення деревоподібних даних. `ItemsSource` для дочірніх елементів. `IsExpanded` binding. Lazy loading для великих дерев.
- **ListView + GridView**: `<ListView.View><GridView>` — табличний вигляд з колонками. `GridViewColumn`, `Header`, `DisplayMemberBinding`, `CellTemplate`. Порівняння з DataGrid — GridView lightweight, DataGrid — featureful.
- **Drag and Drop**: `AllowDrop`, `DragEnter`, `Drop`, `DragOver` events. `DragDrop.DoDragDrop()`. Перетягування елементів між ListBox/TreeView. `AdornerDecorator` для візуального feedback.
- **Практичні завдання**: (Рівень 1) Файловий браузер — TreeView з вкладеними папками. (Рівень 2) Таблиця контактів через ListView + GridView. (Рівень 3) Drag & Drop між двома ListBox.

---

#### `34.menus-toolbars.md` — Меню, Toolbar, ContextMenu, StatusBar

**Мета**: Побудувати повну систему меню та панелей інструментів додатку.

**Зміст**:

- **Menu**: `MenuItem` з `Header`, `Separator`, `Icon`, `InputGestureText` (Ctrl+S). Вкладені підменю. Command binding: `Command="{Binding SaveCommand}"`.
- **ContextMenu**: Контекстне меню на правий клік. Прив'язка до елемента. DataContext inheritance issues та як їх вирішити.
- **ToolBar**: `ToolBarTray` як контейнер. Overflow — елементи, що не вмістились, потрапляють у dropdown. `OverflowMode`.
- **Ribbon** (коротко): Концепція Office-подібного Ribbon. Бібліотека `Fluent.Ribbon`. Лише огляд — не основний підхід.
- **StatusBar**: `StatusBarItem`. Розташування елементів: ліворуч (статус), праворуч (zoom slider), центр (progress).
- **Практичні завдання**: (Рівень 1) Menu з File, Edit, View та keyboard shortcuts. (Рівень 2) ContextMenu для ListBox з Cut/Copy/Paste. (Рівень 3) Повне меню + ToolBar + StatusBar для текстового редактора.

---

### Блок 10: Навігація & Custom Controls (4 + 2🟢 статті)

---

#### `35.navigation-windows.md` — Навігація та керування вікнами

**Мета**: Опанувати роботу з кількома вікнами та MVVM-навігацію без Frame/Page.

**Зміст**:

- **Множинні вікна**: `new Window().Show()` (non-modal), `ShowDialog()` (modal). `Owner` — зв'язок вікон (закриття owner закриває owned). `WindowStartupLocation.CenterOwner`.
- **Передача даних між вікнами**: Через конструктор, через властивості, через Events. `DialogResult` для діалогових вікон.
- **Frame та Page Navigation**: `NavigationService`, `UriSource`. Чому це рідко використовується в реальних додатках — не MVVM-friendly, складно тестувати.
- **MVVM Navigation** (рекомендований підхід): `ContentControl` + `DataTemplate`. Зміна ViewModel у DataContext → DataTemplate автоматично підставляє відповідну View. Реалізація NavigationService як сервісу.
- **Патерн Navigator**: Клас `NavigationStore` з `CurrentViewModel` property. Views реагують через Binding.
- **Практичні завдання**: (Рівень 1) Діалогове вікно з результатом. (Рівень 2) MVVM-навігація з ContentControl для 3 "сторінок" (Home, Settings, About). (Рівень 3) NavigationStore з можливістю "назад" (history stack).

---

#### `35a.avalonia-navigation-dialogs.md` — 🟢 Навігація та діалоги в Avalonia

**Мета**: Показати кросплатформні альтернативи WPF-специфічних API.

**Зміст**:

- **Window.ShowDialog\<T\>()**: Typed result (на відміну від WPF bool?). Зручніший API.
- **StorageProvider API**: `IStorageProvider` — кросплатформний інтерфейс для File Pickers. `OpenFilePickerAsync()`, `SaveFilePickerAsync()`, `OpenFolderPickerAsync()`. Заміна WinForms `OpenFileDialog`.
- **MVVM-friendly Dialogs**: Той самий ContentControl + DataTemplate підхід працює в Avalonia.
- **Platform-specific Dialogs**: Нативні діалоги на кожній ОС через StorageProvider.
- **Практичні завдання**: Портувати File Open/Save діалог з WPF на Avalonia через StorageProvider.

---

#### `36.dialogs-file-pickers.md` — Діалоги та File Pickers (WPF)

**Мета**: Опанувати стандартні діалогові вікна WPF.

**Зміст**:

- **MessageBox**: `MessageBox.Show()`, `MessageBoxImage` (Warning, Error, Info), `MessageBoxButton` (OK, OKCancel, YesNo, YesNoCancel). Returns `MessageBoxResult`.
- **OpenFileDialog, SaveFileDialog**: `Filter` (файлові маски), `FileName`, `Title`, `InitialDirectory`, `CheckFileExists`. Multiple selection через `Multiselect`.
- **FolderBrowserDialog**: Через System.Windows.Forms interop. Чому WPF не має свого — legacy issue.
- **Custom Dialogs**: Створення кастомного діалогу через `Window.ShowDialog()` та `DialogResult`. Патерн: ViewModel для діалогу.
- **MVVM-friendly Dialogs**: Dialog Service pattern — `IDialogService` інтерфейс, реалізація через DI. ViewModel не створює вікна напряму.
- **Практичні завдання**: (Рівень 1) MessageBox для підтвердження видалення. (Рівень 2) Текстовий редактор з Open/Save File. (Рівень 3) IDialogService для MVVM.

---

#### `37.user-controls.md` — UserControl: компонентний підхід

**Мета**: Створювати перевикористовувані UI-компоненти через UserControl.

**Зміст**:

- **UserControl**: Створення файлу (XAML + CS). Додавання DependencyProperty для зовнішнього API. Composition — вкладання стандартних контролів.
- **DependencyProperty як public API**: UserControl з DP`Title`, `IsSearching`, `SearchText` — зовнішній код може прив'язувати через Binding.
- **Events**: Визначення кастомних RoutedEvent для UserControl — `SearchRequested`.
- **DataContext gotcha**: UserControl НЕ повинен задавати свій DataContext — інакше зовнішній Binding зламається. Правильний підхід: RelativeSource Self або ElementName.
- **Патерн**: UserControl як самодостатній компонент з власним ViewModel (для складних контролів).
- **Практичні завдання**: (Рівень 1) SearchBox UserControl (TextBox + Button + DP SearchText). (Рівень 2) HeaderControl з Title, Subtitle, Icon. (Рівень 3) PaginationControl з DP CurrentPage, TotalPages, Command PageChanged.

---

#### `38.custom-controls.md` — Custom Controls: Lookless Controls

**Мета**: Зрозуміти різницю між UserControl та Custom Control і коли обирати кожен.

**Зміст**:

- **UserControl vs Custom Control**: UserControl = composition (складає з існуючих), Custom Control = lookless (поведінка без зовнішності). Custom Control — для бібліотек контролів; UserControl — для конкретного додатку.
- **Створення Custom Control**: Клас, що наслідує Control. `DefaultStyleKey = typeof(MyControl)`. Файл `Themes/Generic.xaml` — стандартний шаблон.
- **Template Parts**: `[TemplatePart(Name = "PART_Header", Type = typeof(ContentPresenter))]`. `OnApplyTemplate()` — пошук частин шаблону через `GetTemplateChild()`.
- **DependencyProperty**: Публічний API контролу — властивості, які можна прив'язувати.
- **Automation Peers**: `AutomationPeer` для accessibility — screen readers, UI Automation testing.
- **Практичні завдання**: (Рівень 1) NumericUpDown — кнопки +/-, TextBox, DependencyProperty Value. (Рівень 2) RatingControl — 5 зірочок, клік змінює рейтинг. (Рівень 3) CircularProgressBar — custom rendering через OnRender.

---

#### `38a.avalonia-templated-controls.md` — 🟢 TemplatedControl в Avalonia

**Мета**: Показати відмінності створення custom controls в Avalonia.

**Зміст**:

- **TemplatedControl**: Аналог WPF Custom Control. Базовий клас для lookless контролів.
- **Generic.axaml замість Generic.xaml**: `Themes/Generic.axaml`. Інший namespace.
- **Відмінності в OnApplyTemplate**: API мінімально відрізняється, але концепція та сама.
- **StyledProperty замість DependencyProperty**: Вже знайомо зі статті 14a.
- **CSS-like стилізація**: ControlTheme + pseudo-classes для станів.
- **Практичні завдання**: Портувати NumericUpDown з WPF (стаття 38) на Avalonia TemplatedControl.

---

### Блок 11: Анімації & Графіка (2 + 1🟢 статті)

---

#### `39.animations-transitions.md` — Анімації у WPF

**Мета**: Навчитися створювати плавні анімації для інтерактивних інтерфейсів.

**Зміст**:

- **Storyboard**: `BeginStoryboard` — контейнер для анімацій. `Storyboard.TargetName`, `Storyboard.TargetProperty`.
- **Types анімацій**: `DoubleAnimation` (числа — Width, Opacity), `ColorAnimation` (кольори — Background), `ThicknessAnimation` (Margin, Padding), `ObjectAnimationUsingKeyFrames` (дискретні значення).
- **From/To/By/Duration**: `From="0" To="1" Duration="0:0:0.5"`. `RepeatBehavior="Forever"`, `AutoReverse="True"`.
- **Property Path**: Анімація вкладених властивостей — `(Button.Background).(SolidColorBrush.Color)`.
- **Easing Functions**: `BounceEase`, `CubicEase`, `ElasticEase`, `CircleEase`. `EasingMode` (EaseIn, EaseOut, EaseInOut). Візуальне порівняння.
- **Event Triggers для анімацій**: `<EventTrigger RoutedEvent="Loaded"><BeginStoryboard>...</BeginStoryboard></EventTrigger>`. На MouseEnter, на Click.
- **Code-behind анімації**: `Storyboard.Begin()`, `Stop()`, `Pause()`, `Resume()`.
- **Практичні завдання**: (Рівень 1) Fade-in при завантаженні (Opacity 0→1). (Рівень 2) Анімована sidebar панель (Width 0→250 з EaseOut). (Рівень 3) Пульсуючий індикатор з RepeatBehavior та AutoReverse.

---

#### `39a.avalonia-animations.md` — 🟢 Анімації Avalonia

**Мета**: Показати принципово інший (і простіший) підхід до анімацій в Avalonia.

**Зміст**:

- **Transitions**: Implicit анімації — property-based. `<Button Transitions><DoubleTransition Property="Opacity" Duration="0:0:0.3"/></Button>`. Зміна Opacity → автоматична плавна анімація. Не потрібен Storyboard!
- **Типи Transitions**: `DoubleTransition`, `BrushTransition`, `ThicknessTransition`, `TransformOperationsTransition`.
- **Easing**: Avalonia використає ті ж easing функції.
- **KeyFrame Animations**: `<Animation Duration="0:0:1"><KeyFrame Cue="0%"><Setter .../></KeyFrame><KeyFrame Cue="100%"><Setter .../></KeyFrame></Animation>`. Більш child-дружній API ніж WPF Storyboard.
- **CSS-подібний підхід**: Анімації через стилі та pseudo-classes — `:pointerover` → Transition автоматично.
- **Порівняння з WPF**: WPF Storyboard (verbose, explicit) vs Avalonia Transitions (concise, implicit). Таблиця.
- **Практичні завдання**: (Рівень 1) Hover-анімація кнопки через Transition. (Рівень 2) KeyFrame анімація обертання. (Рівень 3) Портувати sidebar-анімацію з WPF на Avalonia Transitions.

---

#### `40.media-graphics.md` — 2D/3D графіка та мультимедіа

**Мета**: Використовувати графічні примітиви та мультимедіа у WPF.

**Зміст**:

- **Shapes**: `Rectangle`, `Ellipse`, `Line`, `Polygon`, `Polyline`, `Path`. Fill, Stroke, StrokeThickness.
- **Path та PathGeometry**: Mini-language (`M`, `L`, `C`, `A`, `Z`). Створення складних фігур. SVG → Path Data.
- **Brushes**: `SolidColorBrush`, `LinearGradientBrush` (GradientStops, StartPoint, EndPoint), `RadialGradientBrush`, `ImageBrush`, `VisualBrush` (рендеринг іншого Visual як текстури).
- **Geometries та Drawing**: `RectangleGeometry`, `EllipseGeometry`, `CombinedGeometry`. `DrawingGroup`, `DrawingImage`. Для іконок та складних векторних зображень.
- **Transforms**: `RotateTransform`, `ScaleTransform`, `TranslateTransform`, `SkewTransform`, `TransformGroup`.
- **MediaElement**: Відтворення відео та аудіо. `Source`, `Play()`, `Pause()`, `Stop()`. `MediaTimeline` для Storyboard.
- **Практичні завдання**: (Рівень 1) Набір геометричних фігур (коло, квадрат, трикутник). (Рівень 2) SVG-подібний малюнок через Path. (Рівень 3) Градієнтний фон із VisualBrush ефектом.

---

### Блок 12: DI & Data Persistence (3 статті)

> Цей блок з'єднує десктопний UI з реальними даними. Студент вчиться інтегрувати Microsoft.Extensions.DependencyInjection у WPF/Avalonia та зберігати дані в SQLite через EF Core.

---

#### `41.di-integration.md` — Microsoft.Extensions.DI у десктопних проєктах

**Мета**: Інтегрувати Dependency Injection у WPF та Avalonia проєкти. Навчити створювати ViewModel та сервіси через DI замість `new`.

**Зміст**:

- **Hook**: "У вашому MVVM-додатку MainViewModel створює SettingsViewModel через `new`, а SettingsViewModel створює SettingsService через `new`. Що робити, коли залежностей стає 20? Коли один сервіс потрібен у 5 місцях? Коли потрібно замінити реальний сервіс на mock для тестування?"
- **Проблема**: Ручне створення залежностей (Poor Man's DI). Composition Root розмивається по всьому коду.
- 🔵 **Recap DI** (для студентів зі слабким ООП): Що таке Dependency Injection — принцип, де клас отримує залежності ззовні, а не створює їх сам. `IServiceCollection` — реєстрація. `IServiceProvider` — резолвінг. Lifecycles: `Transient` (новий кожен раз), `Singleton` (один на все), `Scoped` (один на scope). Посилання на розділ 4.5 (Architecture) для глибини.
- **Інтеграція DI у WPF**: Встановлення `Microsoft.Extensions.DependencyInjection`. Налаштування в `App.xaml.cs`: створення `IServiceProvider` в `OnStartup()`. Реєстрація ViewModels як Transient, Services як Singleton/Scoped. Отримання MainWindow через DI. `App.Current.Services` як static accessor.
- **Інтеграція DI у Avalonia**: Аналогічний підхід — налаштування в `App.axaml.cs` або `Program.cs`. `BuildAvaloniaApp()` + DI configuration.
- **ViewModel injection**: Constructor injection — `MainViewModel(INavigationService nav, IDataService data)`. Чому constructor injection кращий за property injection.
- **Service injection**: `IDialogService`, `INavigationService`, `IDataService` — інтерфейси для DI.
- **IServiceScopeFactory**: Для Scoped lifetime у десктопі — коли потрібен новий scope (наприклад, для кожного вікна або кожної операції з DB).
- **Практичні завдання**: (Рівень 1) Підключити DI до існуючого WPF-проєкту, зареєструвати MainViewModel. (Рівень 2) INavigationService через DI — ViewModel не створює інші ViewModel через `new`. (Рівень 3) Повний DI-граф: MainViewModel → IDataService → IDbContextFactory → DbContext.

---

#### `42.data-persistence-part1.md` — SQLite + EF Core у десктопному додатку

**Мета**: Підключити реальне збереження даних через SQLite та Entity Framework Core.

**Зміст**:

- **Чому SQLite для десктопу**: Embedded database — не потрібен окремий сервер. Один файл `.db`. Ідеально для локальних десктопних додатків. Порівняння: SQLite vs LocalDB vs файлові формати (JSON/XML).
- **Встановлення**: NuGet `Microsoft.EntityFrameworkCore.Sqlite`, `Microsoft.EntityFrameworkCore.Design`.
- **DbContext**: Створення контексту для десктопу. `OnConfiguring()` з `UseSqlite($"Data Source={path}")`. Шлях до бази — `Environment.GetFolderPath(SpecialFolder.ApplicationData)`.
- **Entities та DbSet\<T\>**: Моделі даних. Конфігурація через Fluent API (коротке повторення з розділу EF Core).
- **DbContext як Scoped через DI**: `services.AddDbContext<AppDbContext>()`. Чому Scoped, а не Singleton — concurrency issues. `IDbContextFactory<T>` як альтернатива.
- **Міграції**: `dotnet ef migrations add Initial`, `dotnet ef database update`. Автоматичне застосування міграцій при старті додатку: `context.Database.Migrate()`. Первинне наповнення (seeding).
- **Практичні завдання**: (Рівень 1) Підключити SQLite до WPF-проєкту, створити DbContext з одною таблицею. (Рівень 2) Міграція + seed-дані при першому запуску.

**Не згадує**: Repository pattern (Part 2), Settings (Part 2).

---

#### `42.data-persistence-part2.md` — Repository pattern та User Settings

**Мета**: Побудувати чисту архітектуру доступу до даних та систему налаштувань користувача.

**Зміст**:

- **Repository pattern**: `IRepository<T>` з методами GetAll, GetById, Add, Update, Delete. Реалізація через DbContext. Чому Repository — між ViewModel та DbContext (абстракція, testability, можливість заміни storage).
- **Unit of Work**: Збереження через `SaveChangesAsync()`. Коли зберігати — на кожну операцію чи batch.
- **Асинхронність**: `ToListAsync()`, `FindAsync()`, `AddAsync()`. Чому async важливий у десктопі — не блокувати UI Thread.
- **User Settings**: Файлові налаштування додатку. Підходи:
    - `Properties.Settings.Default` — WPF legacy, працює, але не portable.
    - JSON файл через `System.Text.Json` — кросплатформний, простий.
    - `IOptions<T>` через `Microsoft.Extensions.Options` — сучасний DI-friendly підхід.
- **Шлях збереження**: `Environment.GetFolderPath(SpecialFolder.ApplicationData)` / `LocalApplicationData`.
- **Практичні завдання**: (Рівень 1) IRepository\<TodoItem\> з In-Memory реалізацією. (Рівень 2) Repository через SQLite + DbContext. (Рівень 3) Повний CRUD-додаток з SQLite persistence, DI, Repository, Settings (Dark/Light theme preference).

---

### Блок 13: Тестування (2 + 1🟢 статті)

> Професійний рівень — ViewModel та UI повинні бути покриті тестами.

---

#### `43.viewmodel-testing.md` — Тестування ViewModel

**Мета**: Показати, що MVVM робить бізнес-логіку легко тестовуваною, і навчити писати unit-тести для ViewModel.

**Зміст**:

- **Hook**: "Ви дотримались MVVM. Тепер ваш reward — ViewModel можна тестувати без запуску GUI. Без вікон. Без кліків. Просто C#."
- **Чому ViewModel легко тестувати**: ViewModel — чистий C#-клас. Не залежить від UI. Використовує інтерфейси для залежностей → легко mockати.
- **xUnit**: Встановлення, `[Fact]`, `[Theory]`, `[InlineData]`. Arrange-Act-Assert. Naming convention: `MethodName_Scenario_ExpectedResult`.
- **NSubstitute**: Мокування інтерфейсів — `Substitute.For<IDataService>()`. Setup returns: `service.GetAllAsync().Returns(testData)`. Verify calls: `service.Received().DeleteAsync(id)`.
- **Тести для Properties**: Перевірка PropertyChanged — `vm.PropertyChanged += (s, e) => args.Add(e.PropertyName)`. Assert, що зміна FirstName оновлює FullName.
- **Тести для Commands**: `vm.SaveCommand.Execute(null)`. Assert, що `CanExecute` повертає false при порожній формі.
- **Тести для Validation**: Assert, що `vm.HasErrors` = true при невалідних даних.
- **Тести для Messenger**: `WeakReferenceMessenger.Default.Register<T>(recipient, handler)`. Assert, що повідомлення отримане.
- **Практичні завдання**: (Рівень 1) 5 тестів для простої ViewModel з Properties. (Рівень 2) Тести для CRUD ViewModel з мокованим Repository. (Рівень 3) Тести для Navigation з мокованим INavigationService.

---

#### `44.ui-testing.md` — UI Testing (WPF)

**Мета**: Познайомити з автоматизованим тестуванням GUI у WPF.

**Зміст**:

- **UI Automation framework**: Microsoft UI Automation — вбудований фреймворк для тестування UI. `AutomationElement`, `AutomationPeer`.
- **AutomationId**: `AutomationProperties.AutomationId="SaveButton"` — унікальний ID для кожного елемента. Чому важливо: accessibility + testing.
- **FlaUI**: Бібліотека для E2E тестування WPF (обгортка над UI Automation). Встановлення NuGet `FlaUI.UIA3`.
- **Написання тесту**: Запуск додатку → пошук вікна → знаходження елементів → клік/введення тексту → assert результату.
- **Обмеження**: Повільні, brittle (чутливі до змін UI), потребують запущений процес. Чому unit-тести ViewModel важливіші.
- **Практичні завдання**: (Рівень 1) Простий FlaUI тест — запуск додатку, клік на кнопку, перевірка результату. (Рівень 2) E2E тест для форми: введення даних → Submit → перевірка у DataGrid.

---

#### `44a.avalonia-headless-testing.md` — 🟢 Avalonia Headless Testing

**Мета**: Показати унікальну можливість Avalonia — тестування UI без реального вікна.

**Зміст**:

- **Avalonia.Headless**: Рендеринг UI в пам'яті, без реального вікна та GPU. `[AvaloniaTest]` attribute. NuGet `Avalonia.Headless.XUnit`.
- **Headless unit tests**: Створення вікна, знаходження контролів, клік, перевірка стану — все в unit-тесті. Швидко, стабільно, без flaky tests.
- **KeyPress та Click simulation**: `window.KeyPressQwerty(Key.A)`, `button.Focus()` + `window.KeyPressQwerty(Key.Enter)`.
- **Headless screenshots**: `window.CaptureRenderedFrame()` — скріншот у пам'яті для visual regression testing.
- **Порівняння з WPF UI Automation**: Таблиця — speed, stability, setup complexity, platform requirements. Avalonia Headless значно простіший.
- **Практичні завдання**: (Рівень 1) Headless тест — створити вікно, клікнути кнопку, перевірити TextBlock.Text. (Рівень 2) Form тест з KeyPress simulation. (Рівень 3) Visual regression з CaptureRenderedFrame.

---

### Блок 14: Кросплатформ & Deployment (2 статті, Avalonia-only)

> Фінальний блок — збірка та розгортання кросплатформного додатку.

---

#### `45.avalonia-cross-platform.md` — 🟢 Кросплатформна розробка

**Мета**: Навчитися створювати додатки, що працюють на Windows, Linux, macOS, Mobile та WASM.

**Зміст**:

- **Multiple targets**: Desktop (Windows, Linux, macOS), Mobile (Android via Xamarin/NET, iOS), WebAssembly (WASM). Структура мультиплатформного проєкту — shared project + platform-specific projects.
- **Platform-specific code**: `RuntimeInformation.IsOSPlatform(OSPlatform.Windows)`. Conditional compilation: `#if WINDOWS`, `#if LINUX`. Platform-specific DI registrations.
- **Native Menu (macOS)**: `NativeMenu` — системне меню macOS (у Menu Bar). Відмінність від WPF Menu.
- **Clipboard**: `IClipboard` — кросплатформний API. `GetTextAsync()`, `SetTextAsync()`.
- **Drag-n-Drop**: Кросплатформний drag-n-drop через Avalonia API. Відмінності від WPF.
- **File System Access**: `IStorageProvider` (вже знайомий зі статті 35a). Кросплатформні шляхи — `Environment.SpecialFolder`.
- **Tray Icons**: `TrayIcon` — іконка в системному треї.
- **Практичні завдання**: (Рівень 1) Додати platform detection та показати поточну ОС. (Рівень 2) NativeMenu для macOS + звичайне Menu для Windows. (Рівень 3) Зібрати та запустити додаток на 2 різних ОС.

---

#### `46.avalonia-packaging-deployment.md` — 🟢 Пакування та розгортання

**Мета**: Підготувати Avalonia-додаток для розповсюдження на різних платформах.

**Зміст**:

- **dotnet publish**: `dotnet publish -c Release -r win-x64`. Runtime Identifiers (RID): `win-x64`, `linux-x64`, `osx-arm64`.
- **Self-contained vs Framework-dependent**: Self-contained = включає .NET Runtime (~60MB+), Framework-dependent = потребує встановленого .NET (~3MB). Коли що обирати.
- **Trimming та AOT**: `PublishTrimmed=true` — видалення невикористаного коду. NativeAOT для Avalonia — перспективи та обмеження.
- **Windows packaging**: MSI (Windows Installer), MSIX (Modern packaging), Inno Setup (простий installer), Squirrel (auto-updates).
- **Linux packaging**: AppImage (переносний), Flatpak (sandboxed), Snap (Ubuntu), deb/rpm пакети.
- **macOS packaging**: `.app` bundle (структура Info.plist), DMG (disk image для розповсюдження). Code signing та notarization (для macOS Gatekeeper).
- **Auto-updates**: Velopack, NetSparkle — бібліотеки для автоматичного оновлення десктопного додатку.
- **CI/CD**: GitHub Actions для збірки на всіх 3 платформах. Матриця ОС: windows-latest, ubuntu-latest, macos-latest.
- **Практичні завдання**: (Рівень 1) Зібрати self-contained для поточної ОС. (Рівень 2) Створити AppImage для Linux. (Рівень 3) GitHub Actions workflow для мультиплатформної збірки.

---

## Статті, розбиті на Part 1/2

| Стаття                    | Part 1                             | Part 2                          |
| ------------------------- | ---------------------------------- | ------------------------------- |
| 07. Layout Panels         | StackPanel, WrapPanel, DockPanel   | Grid, Canvas, UniformGrid       |
| 14. Dependency Properties | Концепція, Value Precedence        | Створення, Metadata, Coercion   |
| 17. Data Binding Basics   | Концепція, DataContext, Modes      | INPC, UpdateSourceTrigger       |
| 21. Collections Binding   | ObservableCollection, ItemsControl | ICollectionView, Virtualization |
| 28. Control Templates     | ControlTemplate, TemplateBinding   | Named Parts, ContentPresenter   |
| 32. DataGrid              | Columns, AutoGenerate              | Sorting, Filtering, Editing     |
| 42. Data Persistence      | SQLite + EF Core setup             | Repository, Settings            |

---

## Avalonia Companion Articles (16 шт.)

| #   | Стаття               | Ключовий фокус                  |
| --- | -------------------- | ------------------------------- |
| 03a | First Avalonia App   | Проєкт, App.axaml, DevTools     |
| 05a | XAML Differences     | axaml, xmlns, using:            |
| 14a | Property System      | StyledProperty, DirectProperty  |
| 17a | Compiled Bindings    | x:CompileBindings, x:DataType   |
| 25a | MVVM + ReactiveUI    | ViewLocator, ReactiveUI         |
| 27a | CSS-like Styling     | Selectors, Classes              |
| 28a | Control Themes       | ControlTheme vs ControlTemplate |
| 29a | Pseudo-classes       | :pointerover замість Triggers   |
| 30a | Fluent Theme         | Theme Variants, Dark/Light      |
| 35a | Navigation & Dialogs | StorageProvider                 |
| 38a | Templated Controls   | Generic.axaml                   |
| 39a | Animations           | Transitions, KeyFrame           |
| 44a | Headless Testing     | Avalonia.Headless               |
| 45  | Cross-platform       | Multi-target                    |
| 46  | Packaging            | AppImage, DMG, MSI              |

---

## Врахування слабкого ООП

Позначені 🔵 секції в плані — місця, де додаються recap-пояснення:

1. **17.data-binding-basics-part2**: Recap інтерфейсів перед INPC
2. **22.mvvm-pattern**: Recap інтерфейсів, подій, поліморфізму перед MVVM
3. **41.di-integration**: Recap DI принципів
4. У кожному recap — 2-3 абзаци + посилання на повний розділ ООП

---

## Verification Plan

### Automated

- Всі файли існують у `content/01.csharp/12.desktop-ui/`
- Кожен `.md` має frontmatter (`title`, `description`)
- Внутрішні посилання валідні

### Manual

- Жодних forward references
- Відповідність prompt.md: hook → why → code anatomy → practice → summary
- Docus компоненти працюють (Nuxt dev server)
- 3 рівні практичних завдань у кожній статті
