# Навчальний план React Native для kostyl.dev

## Контекст

Створення повного курсу React Native для студентів, які вже знають **React** та **TypeScript**. Курс розміщується у `content/15.react-native/version2`. Кожен файл — окремий матеріал у форматі Docus MDC (як існуючі C++ та Kubernetes матеріали). Стиль — **академічний, книжковий, розгорнутий, послідовний, технічний**, але зрозумілий.

## Ключові рішення

| Рішення | Вибір |
|---------|-------|
| Фреймворк | Expo (основа) → bare workflow (окрема стаття) |
| Навігація | Expo Router (основа) + React Navigation (альтернатива) |
| State management | Redux Toolkit + RTK Query (студенти знають Redux) |
| Нативні модулі | Окремий модуль (Java/Kotlin/Swift) |
| Мова | Українська |
| API для практики | JSONPlaceholder, PokeAPI тощо |
| Анімації | Animated API + Reanimated + Gesture Handler |

## Інструментарій Docus

- `::react-native-preview` — **живі демо** (core UI, стилізація, layouts)
- `::terminal-preview` — CLI команди (expo start, npx тощо)
- `::code-group` / `::code-tree` — порівняння підходів, структура проєкту
- `::steps` — покрокові інструкції
- `::mermaid` / `::plant-uml` — архітектурні діаграми
- `::note`, `::tip`, `::warning`, `::caution` — акценти
- `::field-group` — документація пропсів компонентів
- `::card-group` — групування концепцій
- `::accordion` — практичні завдання
- `::tabs` — порівняння iOS/Android, різних підходів

---

## Структура курсу: `content/15.react-native/`

Курс поділений на **8 модулів** з **~52 невеликих статей** (кожна 15–40 Кб).

---

### Модуль 0: Вступ та налаштування середовища (3 статті)

#### `01.what-is-react-native.md`
**Що таке React Native і чому це важливо**
- Історія RN (Facebook, 2015) та еволюція (New Architecture, 2024)
- Як RN працює: JS → Bridge/JSI → Нативні компоненти
- Порівняння з іншими підходами: PWA, Ionic, Flutter, нативна розробка
- Діаграма архітектури (PlantUML)
- Навіщо RN знати React-розробнику

#### `02.environment-setup.md`
**Налаштування середовища розробки**
- Встановлення Node.js, npm/yarn
- Expo CLI vs React Native CLI — чому починаємо з Expo
- Створення першого Expo-проєкту (`npx create-expo-app`)
- Запуск на емуляторі/симуляторі та на реальному пристрої (Expo Go)
- Огляд структури проєкту (::code-tree)
- Налаштування VS Code (розширення, налагодження)

#### `03.react-native-vs-react.md`
**Від React до React Native: ключові відмінності**
- Немає DOM → є нативні View, Text, Image
- Немає CSS → є StyleSheet (підмножина CSS + Flexbox)
- Немає `<div>`, `<span>`, `<p>` → є `<View>`, `<Text>`
- Обробка подій: onClick → onPress
- Платформо-залежна поведінка
- Таблиця-маппінг: HTML → RN компоненти (::card-group)
- ::react-native-preview — перший живий приклад

---

### Модуль 1: Основи UI — Core Components (12 статей)

> Охоплює **всі** вбудовані компоненти React Native: як ті, що використовуються щодня, так і утилітні. Кожна стаття — один-два тісно пов'язаних компоненти.

#### `04.view-and-text.md`
**View та Text — фундаментальні будівельні блоки**
- View як `<div>` мобільного світу (але не зовсім)
- Text як єдиний контейнер для тексту (вкладеність, стилі)
- Правило: текст тільки всередині `<Text>`
- Вкладеність View → layout patterns
- Живі приклади (::react-native-preview)

#### `05.stylesheet-and-styling.md`
**StyleSheet — стилізація компонентів**
- StyleSheet.create() — навіщо і як
- Різниця з CSS: camelCase, числові значення, обмежений набір
- Які CSS-властивості доступні, які — ні
- Типізація стилів (ViewStyle, TextStyle, ImageStyle)
- Умовні стилі, масиви стилів `[style1, style2]`
- Inline стилі vs StyleSheet.create — продуктивність
- Platform.select() для платформо-залежних стилів
- ::react-native-preview для кожного підходу

#### `06.flexbox-layout.md`
**Flexbox-розкладка у React Native**
- Flexbox у RN за замовчуванням (column, а не row!)
- flex, flexDirection, justifyContent, alignItems, alignSelf
- flexWrap, gap, rowGap, columnGap
- flexGrow, flexShrink, flexBasis
- position: 'absolute' та 'relative'
- Практичні layout-патерни: header-content-footer, sidebar, grid, overlay
- Діаграми Flexbox (PlantUML / Mermaid)
- Живі приклади (::react-native-preview)

#### `07.image-and-imagebackground.md`
**Image та ImageBackground — робота із зображеннями**
- Локальні зображення (require)
- Мережеві зображення (source={{ uri }}) — обов'язкові width/height
- resizeMode: cover, contain, stretch, center, repeat
- ImageBackground — фон через зображення
- Оптимізація: кешування, placeholder
- expo-image як сучасна заміна Image (кешування, blurhash, анімовані переходи)
- Іконки: @expo/vector-icons (FontAwesome, MaterialIcons, Ionicons тощо)

#### `08.scrollview.md`
**ScrollView — прокручуваний контент**
- Коли і навіщо ScrollView (vs FlatList)
- Горизонтальний та вертикальний скрол
- Властивості: contentContainerStyle, pagingEnabled, showsVerticalScrollIndicator
- Pull-to-refresh (RefreshControl компонент)
- onScroll, onMomentumScrollEnd, scrollTo
- Обмеження ScrollView: рендерить ВСЕ одразу — не підходить для довгих списків

#### `09.pressable-and-touchable.md`
**Pressable, Touchable* та Button — обробка дотиків**
- Button — найпростіший (але не кастомізований)
- TouchableOpacity, TouchableHighlight, TouchableWithoutFeedback (legacy, але ще популярні)
- Pressable — сучасна заміна всіх Touchable* компонентів
- onPress, onLongPress, onPressIn, onPressOut
- Стан натискання: `({pressed}) => style`
- android_ripple — Ripple-ефект на Android
- hitSlop — збільшення зони натискання
- Живі приклади (::react-native-preview)

#### `10.textinput.md`
**TextInput — введення тексту**
- Контрольований vs неконтрольований TextInput
- Основні пропси: placeholder, value, onChangeText, secureTextEntry
- Типи клавіатури: keyboardType (numeric, email-address, phone-pad, url)
- returnKeyType (done, go, next, search, send)
- autoCapitalize, autoCorrect, autoComplete
- Мультирядковий ввід (multiline, numberOfLines, textAlignVertical)
- Керування фокусом: ref.current.focus(), Keyboard.dismiss()
- onSubmitEditing, onFocus, onBlur
- Живі приклади (::react-native-preview)

#### `11.flatlist.md`
**FlatList — ефективні списки**
- Чому FlatList, а не `ScrollView + map()`
- Віртуалізація: як FlatList рендерить лише видимі елементи
- data, renderItem, keyExtractor
- ListHeaderComponent, ListFooterComponent, ListEmptyComponent, ItemSeparatorComponent
- Горизонтальний список (horizontal)
- numColumns — grid layout
- Пагінація (onEndReached, onEndReachedThreshold)
- Pull-to-refresh (onRefresh, refreshing)
- Оптимізація: getItemLayout, windowSize, maxToRenderPerBatch, removeClippedSubviews
- scrollToIndex, scrollToOffset

#### `12.sectionlist.md`
**SectionList — згрупований список**
- Коли SectionList vs FlatList
- sections: масив з title та data
- renderSectionHeader, renderSectionFooter
- stickySectionHeadersEnabled
- Практичний приклад: контакти, згруповані за літерою

#### `13.modal-and-alert.md`
**Modal та Alert — модальні вікна та діалоги**
- Modal: animationType (slide, fade, none), transparent, onRequestClose
- Патерн: контрольований Modal (visible + setVisible)
- Alert.alert() — нативні діалоги
  - Різниця iOS/Android: кількість кнопок, стилі (::tabs)
- ActionSheetIOS (тільки iOS)
- Патерн: кастомний модальний компонент (overlay + Pressable)

#### `14.statusbar-safeareaview-keyboardavoidingview.md`
**StatusBar, SafeAreaView та KeyboardAvoidingView**
- StatusBar: barStyle (light-content/dark-content), backgroundColor (Android), hidden, translucent
- SafeAreaView — notch, Dynamic Island, нижні індикатори
  - Обмеження: працює лише для iOS
  - react-native-safe-area-context — кросплатформне рішення (useSafeAreaInsets)
- KeyboardAvoidingView — уникнення перекриття клавіатурою
  - behavior: 'padding' (iOS) vs 'height' (Android)
  - keyboardVerticalOffset

#### `15.switch-activityindicator-misc.md`
**Switch, ActivityIndicator та утилітні компоненти**
- Switch — перемикач (контрольований), trackColor, thumbColor, ios_backgroundColor
- ActivityIndicator — індикатор завантаження, size (small/large), color
- VirtualizedList — базовий клас для FlatList/SectionList (коли потрібно)
- Linking — відкриття URL, телефон, email, налаштування
- Share — нативний діалог "Поділитися"
- Vibration — вібрація пристрою (deprecated → Expo Haptics)
- Platform API — розгалуження логіки по платформі
- Dimensions API та useWindowDimensions
- PixelRatio — робота з пікселями та DPI
- AppState — стан застосунку (active/background/inactive)

---

### Модуль 2: Community-компоненти та бібліотеки UI (5 статей)

> Компоненти, які **раніше були вбудованими** у React Native, але були виділені в окремі пакети, а також найпопулярніші community-рішення. Це must-know елементи для будь-якого реального додатку.

#### `16.picker-and-datetime.md`
**Picker, DateTimePicker та Select**
- @react-native-picker/picker — випадаючий список (Picker, Picker.Item)
  - iOS: wheel picker, Android: dropdown/dialog
  - Стилізація, mode, selectedValue, onValueChange
- @react-native-community/datetimepicker — вибір дати та часу
  - mode: 'date', 'time', 'datetime' (iOS)
  - display: 'default', 'spinner', 'calendar', 'clock'
  - Різниця iOS/Android (::tabs)
- Альтернативи: react-native-date-picker, expo-date-time-picker

#### `17.slider-checkbox-progressbar.md`
**Slider, CheckBox та ProgressBar**
- @react-native-community/slider — повзунок
  - minimumValue, maximumValue, step, onValueChange
  - Стилізація: thumbTintColor, minimumTrackTintColor, maximumTrackTintColor
- @react-native-community/checkbox (Android) / Switch (iOS fallback)
  - або expo-checkbox як кросплатформний варіант
- ProgressBar:
  - @react-native-community/progress-bar-android (Android)
  - @react-native-community/progress-view (iOS)
  - Патерн: кастомний кросплатформний ProgressBar через View + width animation
- SegmentedControl (iOS): @react-native-segmented-control/segmented-control

#### `18.webview-and-clipboard.md`
**WebView, Clipboard та інші extracted-компоненти**
- react-native-webview — вбудований браузер
  - source={{ uri }}, source={{ html }}
  - onMessage, postMessage — комунікація JS ↔ WebView
  - injectedJavaScript — виконання JS у WebView
  - Обмеження та безпека
- @react-native-clipboard/clipboard — буфер обміну
  - Clipboard.setString(), Clipboard.getString()
  - expo-clipboard як альтернатива

#### `19.bottom-sheet-toast-actionsheet.md`
**Bottom Sheet, Toast та Action Sheet**
- @gorhom/bottom-sheet — модальна панель знизу
  - BottomSheet, BottomSheetModal, BottomSheetScrollView
  - snapPoints, enablePanDownToClose
  - Інтеграція з Reanimated та Gesture Handler
- react-native-toast-message — спливаючі повідомлення
  - Toast.show(), типи (success, error, info)
  - Кастомні шаблони
- @expo/react-native-action-sheet — кросплатформний Action Sheet
  - useActionSheet(), showActionSheetWithOptions

#### `20.ui-libraries-overview.md`
**Огляд UI-бібліотек**
- React Native Paper (Material Design) — ThemeProvider, Button, Card, TextInput, FAB, Snackbar
- NativeBase / Gluestack UI — utility-first підхід
- React Native Elements — найпопулярніша UI-бібліотека
- Tamagui — high-performance, кросплатформний (web + native)
- Коли використовувати UI-бібліотеку vs кастомні компоненти
- Порівняльна таблиця (::card-group)
- Патерн: обгортка UI-бібліотеки (Design System)

---

### Модуль 3: Кастомні компоненти та хуки (3 статті)

#### `21.custom-components.md`
**Створення кастомних компонентів**
- Від простого до складного: Button → Card → ListItem
- Типізація пропсів (TypeScript interfaces)
- children, renderProp, compound components
- forwardRef у RN
- Патерни: Container/Presentational, Compound Components
- Організація файлів компонентів

#### `22.hooks-in-react-native.md`
**Хуки специфічні для React Native**
- useWindowDimensions — реактивні розміри
- useColorScheme — тема пристрою (light/dark)
- AppState + useEffect — стан застосунку
- Keyboard events (Keyboard.addListener)
- BackHandler (Android-специфічний)
- useAnimatedValue (Animated API)

#### `23.platform-specific-code.md`
**Платформо-залежний код**
- Platform.OS, Platform.select(), Platform.Version
- Файли з розширенням: .ios.tsx / .android.tsx
- Стратегії: коли інлайн-перевірки, коли окремі файли
- Конкретні приклади різниць iOS/Android (тіні, шрифти, elevation, ripple)
- ::tabs{iOS / Android} для порівняння

---

### Модуль 4: Навігація (5 статей)

#### `24.navigation-concepts.md`
**Концепції навігації у мобільних додатках**
- Навігація у мобільних vs веб: стек, таби, drawer
- Моделі навігації: Stack, Tab, Drawer, Modal
- Навіщо бібліотека навігації (немає вбудованого router)
- Expo Router vs React Navigation — порівняння
- Діаграма типів навігації (Mermaid)

#### `25.expo-router-basics.md`
**Expo Router: файлова навігація**
- Встановлення та конфігурація
- File-based routing: `app/` директорія
- Основні маршрути: `index.tsx`, `about.tsx`, `[id].tsx`
- `_layout.tsx` — Layouts як концепція
- Link та useRouter — програмна навігація
- Типізація параметрів маршрутів

#### `26.expo-router-advanced.md`
**Expo Router: Tabs, Stack та вкладена навігація**
- Tab-навігація: `(tabs)/_layout.tsx`
- Stack-навігація: `_layout.tsx` з Stack
- Вкладені маршрути та групи `(group)`
- Модальні екрани
- Not-Found (404) екрани
- Protected routes (авторизація)

#### `27.react-navigation-intro.md`
**React Navigation: альтернативний підхід**
- Встановлення та конфігурація (без Expo Router)
- NavigationContainer, Stack.Navigator, Stack.Screen
- Передача параметрів між екранами
- Tab.Navigator, Drawer.Navigator
- Порівняння з Expo Router: переваги/недоліки

#### `28.deep-linking.md`
**Deep Linking та Universal Links**
- Що таке deep linking
- Конфігурація у Expo Router
- URL-схеми (myapp://) та Universal Links (HTTPS)
- Тестування deep links
- Практичний приклад: сторінка профілю через URL

---

### Модуль 5: Робота з даними та мережею (6 статей)

#### `29.fetch-api-basics.md`
**Fetch API та мережеві запити**
- fetch() у React Native — те ж саме, що у React
- GET, POST, PUT, DELETE запити
- Headers, body, Content-Type
- Обробка помилок (network error vs HTTP error)
- async/await + try/catch
- Приклади з JSONPlaceholder API

#### `30.axios-integration.md`
**Axios: HTTP-клієнт для React Native**
- Чому Axios в RN (interceptors, timeout, cancel)
- Створення інстансу з baseURL
- Request/Response interceptors (auth token)
- Практичний приклад: CRUD з API

#### `31.rtk-query.md`
**RTK Query у React Native**
- Налаштування Redux Toolkit + RTK Query в Expo
- createApi, fetchBaseQuery
- Автоматичний кеш, ревалідація, polling
- Hooks: useGetQuery, useMutation
- Оптимістичні оновлення
- Порівняння з TanStack Query (::tabs)

#### `32.async-storage.md`
**AsyncStorage — локальне зберігання**
- @react-native-async-storage/async-storage
- setItem, getItem, removeItem, multiGet
- JSON серіалізація/десеріалізація
- Зберігання налаштувань, токенів, кешу
- Обмеження AsyncStorage (не для великих даних)
- Альтернативи: expo-secure-store, MMKV (react-native-mmkv)

#### `33.sqlite-local-database.md`
**SQLite — локальна база даних**
- expo-sqlite — встановлення та конфігурація
- Створення бази, таблиць, CRUD операції
- Підготовлені запити (prepared statements)
- Міграції схеми
- Практичний приклад: todo-додаток з офлайн-сховищем

#### `34.forms-and-validation.md`
**Форми та валідація**
- Контрольовані форми у RN (useState для кожного поля)
- React Hook Form у React Native (студенти знають)
- Zod/Yup для валідації
- Патерн: форма реєстрації/логіну
- Показ помилок валідації у мобільному UI

---

### Модуль 6: Анімації та жести (4 статті)

#### `35.animated-api-basics.md`
**Animated API — основи анімацій**
- Animated.Value, Animated.View, Animated.Text, Animated.Image
- Animated.timing(), spring(), decay()
- useNativeDriver: true — навіщо і коли (та обмеження)
- Інтерполяція: inputRange, outputRange
- Паралельні та послідовні анімації (parallel, sequence, stagger)
- LayoutAnimation — прості layout-переходи

#### `36.reanimated-intro.md`
**React Native Reanimated — продуктивні анімації**
- Навіщо Reanimated (UI thread vs JS thread)
- Shared Values: useSharedValue
- Animated Styles: useAnimatedStyle
- withTiming, withSpring, withDecay, withRepeat
- Worklets — функції на UI-потоці
- Entering/Exiting animations (FadeIn, SlideInLeft тощо)
- Layout transitions
- Порівняння з Animated API (::tabs)

#### `37.gesture-handler.md`
**React Native Gesture Handler**
- Tap, Pan, Pinch, Rotation, LongPress, Fling
- GestureDetector + Gesture API (v2)
- Composable gestures (simultaneous, exclusive, race)
- Інтеграція з Reanimated (useAnimatedGestureHandler)
- Swipeable, DrawerLayout (готові компоненти)
- Практичний приклад: Swipe-to-delete, Drag-and-drop

#### `38.animation-patterns.md`
**Практичні анімаційні патерни**
- Skeleton loading (placeholder animation)
- Fade-in списків (FlatList + entering)
- Shared Element Transitions (react-native-shared-element)
- Pull-to-refresh з кастомною анімацією
- Bottom Sheet з жестами (інтеграція з @gorhom/bottom-sheet)
- Animated header при скролі (Animated.event + interpolate)
- Lottie-анімації (lottie-react-native) — коротке знайомство

---

### Модуль 7: Expo API та нативні можливості (5 статей)

#### `39.expo-api-overview.md`
**Огляд Expo SDK — нативні API через JavaScript**
- Expo SDK — що входить, як встановити окремі модулі
- Система дозволів (permissions): requestPermissionsAsync
- expo-constants, expo-device — інформація про пристрій
- expo-font — завантаження кастомних шрифтів
- expo-splash-screen — контроль сплеш-скріну
- expo-haptics — тактильний відгук
- Вибір модулів: Expo vs Community
- Діаграма популярних Expo-модулів (Mermaid)

#### `40.camera-and-media.md`
**Камера, медіа та файлова система**
- expo-camera — фото та відео
- expo-image-picker — вибір з галереї
- expo-file-system — робота з файлами
- expo-media-library — збереження у галерею
- expo-av — аудіо та відео плеєр
- Практичний приклад: аватарка профілю

#### `41.location-and-maps.md`
**Геолокація та карти**
- expo-location — поточна позиція, відстеження
- react-native-maps — інтерактивна карта
- Маркери, регіони, кастомні маркери
- Фонова геолокація (обмеження)
- Практичний приклад: карта з точками

#### `42.notifications.md`
**Push-сповіщення**
- Локальні сповіщення (expo-notifications)
- Push-сповіщення через Expo Push Service
- Конфігурація: Android channels, iOS permissions
- Обробка навігації при натисканні на сповіщення
- Практичний приклад: нагадування

#### `43.native-modules.md`
**Створення нативних модулів**
- Навіщо нативні модулі (коли Expo недостатньо)
- Expo Modules API — сучасний підхід
- Створення модуля на Swift (iOS)
- Створення модуля на Kotlin (Android)
- Turbo Modules — огляд New Architecture
- Коли потрібен eject / bare workflow

---

### Модуль 8: Архітектура, тестування та реліз (8 статей)

#### `44.project-architecture.md`
**Архітектура React Native проєкту**
- Feature-based структура (features/, shared/, app/)
- Шари: UI → Hooks → Services → API
- Barrel exports (index.ts)
- Абсолютні імпорти (path aliases)
- Конфігурація TypeScript для RN
- ::code-tree — приклад реальної структури

#### `45.theming-and-dark-mode.md`
**Теми та Dark Mode**
- useColorScheme — визначення теми пристрою
- Створення Theme Context
- Типізовані теми (colors, spacing, typography)
- Динамічне перемикання теми
- React Native Paper / Tamagui (приклад інтеграції з UI-бібліотекою)

#### `46.testing.md`
**Тестування React Native додатків**
- Jest — модульні тести (бізнес-логіка)
- React Native Testing Library — компонентні тести
- render, fireEvent, waitFor, screen
- Мокування нативних модулів (jest.mock)
- Тестування хуків (renderHook)
- E2E-тестування (Detox/Maestro — огляд)

#### `47.debugging.md`
**Налагодження (Debugging)**
- React Native DevTools
- Flipper (desktop debugger)
- Console.log, console.warn, console.error
- Network Inspector
- React DevTools (component tree, profiler)
- Performance Monitor — FPS, memory
- Поширені помилки та їх вирішення

#### `48.performance.md`
**Оптимізація продуктивності**
- Як працює рендеринг у RN (JS thread vs UI thread vs Shadow thread)
- React.memo, useMemo, useCallback — коли це потрібно
- FlatList оптимізація (getItemLayout, removeClippedSubviews)
- Уникнення re-renders: InteractionManager, batch updates
- Зображення: кешування, стиснення, expo-image
- Hermes engine — що це і навіщо
- Profiling з React DevTools

#### `49.building-and-deployment.md`
**Збірка та публікація**
- Expo Application Services (EAS Build)
- Збірка для iOS (TestFlight, App Store)
- Збірка для Android (Google Play, APK/AAB)
- Конфігурація app.json / app.config.ts
- Іконки, сплеш-скрін (expo-splash-screen)
- OTA Updates (expo-updates)
- Версіонування та CI/CD (огляд)

#### `50.bare-workflow.md`
**Bare Workflow та eject з Expo**
- Коли потрібен bare workflow
- `npx expo prebuild` — генерація нативного коду
- Структура bare-проєкту (ios/, android/)
- Конфігурація Gradle та Xcode
- Додавання нативних залежностей вручну
- Повернення до managed workflow (CNG — Continuous Native Generation)

#### `51.final-project.md`
**Фінальний проєкт: повний мобільний додаток**
- Специфікація проєкту: мобільний додаток «Трекер завдань» або «Каталог покемонів»
- Вимоги: навігація, API-запити, локальне зберігання, форми, анімації
- Архітектурні рішення
- Чеклист для оцінювання
- Поради для портфоліо

---

### Допоміжні файли

#### `.navigation.yml`
```yaml
title: React Native
icon: i-devicon-react
```

#### `index.md`
Головна сторінка курсу з описом, передумовами та структурою.

---

## Зведена таблиця: всі UI-елементи у курсі

| Категорія | Компонент/API | Стаття | Тип |
|-----------|--------------|--------|-----|
| **Core Layout** | View | 04 | built-in |
| | Text | 04 | built-in |
| | ScrollView | 08 | built-in |
| | FlatList | 11 | built-in |
| | SectionList | 12 | built-in |
| | VirtualizedList | 15 | built-in |
| | SafeAreaView | 14 | built-in |
| | KeyboardAvoidingView | 14 | built-in |
| **Стилізація** | StyleSheet | 05 | built-in |
| | Flexbox | 06 | built-in |
| | Platform | 15, 23 | built-in |
| | Dimensions / useWindowDimensions | 15 | built-in |
| | PixelRatio | 15 | built-in |
| **Медіа** | Image | 07 | built-in |
| | ImageBackground | 07 | built-in |
| | expo-image | 07 | expo |
| | @expo/vector-icons | 07 | expo |
| **Введення** | TextInput | 10 | built-in |
| | Switch | 15 | built-in |
| | Pressable | 09 | built-in |
| | TouchableOpacity | 09 | built-in |
| | TouchableHighlight | 09 | built-in |
| | TouchableWithoutFeedback | 09 | built-in |
| | Button | 09 | built-in |
| **Модальні** | Modal | 13 | built-in |
| | Alert | 13 | built-in |
| | ActionSheetIOS | 13 | built-in (iOS) |
| **Системні** | StatusBar | 14 | built-in |
| | ActivityIndicator | 15 | built-in |
| | RefreshControl | 08 | built-in |
| | AppState | 15 | built-in |
| | Linking | 15 | built-in |
| | Share | 15 | built-in |
| | Vibration | 15 | built-in |
| | BackHandler | 22 | built-in (Android) |
| | Keyboard | 22 | built-in |
| **Community (extracted)** | @react-native-picker/picker | 16 | community |
| | @react-native-community/datetimepicker | 16 | community |
| | @react-native-community/slider | 17 | community |
| | @react-native-community/checkbox | 17 | community |
| | ProgressBar / ProgressView | 17 | community |
| | SegmentedControl | 17 | community (iOS) |
| | react-native-webview | 18 | community |
| | @react-native-clipboard/clipboard | 18 | community |
| **Community (popular)** | @gorhom/bottom-sheet | 19 | community |
| | react-native-toast-message | 19 | community |
| | @expo/react-native-action-sheet | 19 | community |
| | react-native-safe-area-context | 14 | community |
| **UI-бібліотеки** | React Native Paper | 20 | library |
| | NativeBase / Gluestack UI | 20 | library |
| | React Native Elements | 20 | library |
| | Tamagui | 20 | library |
