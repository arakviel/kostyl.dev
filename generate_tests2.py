import os
import pandas as pd

def save_to_excel(filename, data):
    dir_path = "tests/13.aspnet/01.minimal-api"
    os.makedirs(dir_path, exist_ok=True)
    
    df = pd.DataFrame(data)
    
    columns = [
        "Question Text", "Question Type", "Option 1", "Option 2", "Option 3", "Option 4", "Option 5",
        "Correct Answer", "Time in seconds", "Image Link", "Answer explanation"
    ]
    
    for col in columns:
        if col not in df.columns:
            df[col] = ""
            
    df = df[columns]
    
    filepath = os.path.join(dir_path, filename)
    df.to_excel(filepath, index=False)
    print(f"Saved {filepath} with {len(df)} questions.")


data_03 = [
    {
        "Question Text": "Патерн Builder (Будівельник) у контексті WebApplicationBuilder потрібен, оскільки:",
        "Question Type": "Multiple Choice",
        "Option 1": "Він дозволяє динамічно міняти порт Kestrel на-льоту після збірки.",
        "Option 2": "Цей клас дозволяє уникати антипаттерну конфігурації 'Telescoping Constructor', де конструктор мав би тисячі параметрів.",
        "Option 3": "Лише він може збирати фронтенд код (Razor, React) у WebAssembly.",
        "Option 4": "Він автоматично закриває програму після 1000 запитів.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "Замість створення `new WebApplication(...)` із безліччю сервісів, ми використовуємо 'порожній аркуш' будівельника, щоб зареєструвати налаштування і лише потім викликати `Build()`."
    },
    {
        "Question Text": "Яка головна проблема у тісно пов'язаному (Tight Coupling) класі, де залежності створюються через ключове слово `new` всередині самого конструктора коду?",
        "Question Type": "Multiple Choice",
        "Option 1": "Неефективність використання пам’яті (Memory Leak).",
        "Option 2": "Неможливість підсунути Mock-об'єкти для написання Unit-тестів або швидко змінити загальну реалізацію без зміни цього класу.",
        "Option 3": "Викликає переповнення стеку (Stack Overflow).",
        "Option 4": "Бази даних перестають реагувати на SQL-ін'єкції.",
        "Correct Answer": "2",
        "Time in seconds": "60",
        "Answer explanation": "Зв'язність забороняє тестування і гнучкість; класс повинен залежати від абстракцій (інтерфейсів), а не безпосередньої конкретики."
    },
    {
        "Question Text": "Що означає Lifetime об'єкту типу Singleton у IoC-контейнері `builder.Services`?",
        "Question Type": "Multiple Choice",
        "Option 1": "Один екземпляр на один HTTP запит від користувача.",
        "Option 2": "Один екземпляр класу на всю життя всього додатку.",
        "Option 3": "Кожен виклик залежності виділяє повністю новий екземпляр класу.",
        "Option 4": "Застосується виключно в середовищі розробки Development.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "При AddSingleton Контейнер створює об'єкт РІВНО ОДИН РАЗ і надає його щоразу, коли хтось його потребує."
    },
    {
        "Question Text": "З яким життєвим циклом в ASP.NET DI-контейнері ідеально реєструвати репозиторій доступу до бази даних Entity Framework (напр. DbContext) і чому?",
        "Question Type": "Multiple Choice",
        "Option 1": "Transient, бо база має часто перевідкриватись.",
        "Option 2": "Scoped, бо дані повинні зберігати стан та транзакції строго в межах поточного HTTP запиту клієнта.",
        "Option 3": "Singleton, оскільки доступ до БД швидкий коли він один для всіх юзерів.",
        "Option 4": "Усі варіанти небезпечні для бази даних.",
        "Correct Answer": "2",
        "Time in seconds": "60",
        "Answer explanation": "Scoped гарантує, що всі компоненти, яким потрібна база даних протягом одного запиту, будуть працювати з однією і тією ж транзакцією/конектом."
    },
    {
        "Question Text": "Методи розширення (Extension Methods), як от `builder.Services.AddControllers()`, дозволяють...",
        "Question Type": "Multiple Choice",
        "Option 1": "Додатково запускати нові сервери AWS.",
        "Option 2": "Приховувати сотні налаштувань реєстрації всередині лаконічного виклику та групувати логіку `IServiceCollection`.",
        "Option 3": "Шифрувати дані перед відправкою.",
        "Option 4": "Негайно компілювати код бази даних.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "Команда-метод налаштовує сотні рядків `ISchemaGenerator` тощо за межами Program.cs для модульної архітектури."
    },
    {
        "Question Text": "Під час зчитування ключів конфігурації, хто отримує найвищий пріоритет (хто перепише параметри у випадку конфлікту)?",
        "Question Type": "Multiple Choice",
        "Option 1": "appsettings.json.",
        "Option 2": "Методи розширення (Extension Methods).",
        "Option 3": "Змінні середовища системи (Environment Variables) або Командні аргументи (--port).",
        "Option 4": "Сервіси з життєвим циклом Singleton.",
        "Correct Answer": "3",
        "Time in seconds": "30",
        "Answer explanation": "ASP.NET Core збирає ієрархію налаштувань. Змінні ОС та CLI аргументи - найпріоритетніші 'накази'."
    },
    {
        "Question Text": "Патерн Options (`IOptions<T>`) у ASP.NET Core пропонує...",
        "Question Type": "Multiple Choice",
        "Option 1": "Безпечне збереження JWT секретів у User Secrets.",
        "Option 2": "Автоматичний запис помилок у консоль.",
        "Option 3": "Прив'язку JSON-секцій `appsettings.json` до суворо типізованих C#-класів через DI Контейнер.",
        "Option 4": "Закриття бази даних.",
        "Correct Answer": "3",
        "Time in seconds": "45",
        "Answer explanation": "Options Pattern дозволяє не читати рядки-ключі магічно через `config['Key:Sub']` а ін'єктувати об'єкт моделі налаштувань."
    },
    {
        "Question Text": "Розробник зберіг ключі до розрахункового серверу Stripe в `appsettings.json` і відправив зміни в публічний Git. Які наслідки очікуються?",
        "Question Type": "Multiple Choice",
        "Option 1": "Жодних, `appsettings.json` завжди прихований в Azure.",
        "Option 2": "Компілятор C# видасть помилку.",
        "Option 3": "Боти в Git знайдуть секрети і зловмисники скористаються ними.",
        "Option 4": "Платформа автоматично видалить рядок",
        "Correct Answer": "3",
        "Time in seconds": "30",
        "Answer explanation": "У базовий `appsettings.json` ніколи не можна комітити реальні секрети, краще використовувати змінні середовища."
    },
    {
        "Question Text": "Яка частина Життєвого Циклу (`IHostApplicationLifetime`) ідеальна для закриття відкритих з'єднань і файлів перед 'смертю' додатка?",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "ApplicationStopped",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "ApplicationStopped виконується коли всі клієнти відімкнулись і ми проводимо остаточну очистку ресурсів."
    },
    {
        "Question Text": "Що робить метод ApplicationStopping під час відключення сервера?",
        "Question Type": "Open-Ended",
        "Time in seconds": "60",
        "Answer explanation": "Цей хук викликається коли користувач натискає Ctrl+C. Сервер припиняє приймати _нові_ запити, але дає час для коректного завершення (Graceful Shutdown) вже активним/працюючим маршрутам."
    }
]

save_to_excel("03.webapplication-builder.xlsx", data_03)

data_04 = [
    {
        "Question Text": "За яким принципом відпрацьовує Middleware (Конвеєр) в ASP.NET Core?",
        "Question Type": "Multiple Choice",
        "Option 1": "Випадковим чином, залежно від навантаження.",
        "Option 2": "У вигляді матрьошки: запит обробляється до кінцевого Endpoint, і після відповіді повертається 'нагору' через ті самі Middleware.",
        "Option 3": "Лише в одному напрямку: перевірка, маршрут, видача браузеру - і обрив.",
        "Option 4": "Завжди спочатку викликається контролер коду.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "Викликаючи next(), система 'пірнає' в наступний фільтр, а після його завершення код поточної функції продовжується і може мутувати відповідь."
    },
    {
        "Question Text": "Що таке об'єкт `HttpContext` у пайплайні?",
        "Question Type": "Multiple Choice",
        "Option 1": "Файл із конфігураціями серверу.",
        "Option 2": "Зібраний з байтів абстрактний і повністю укомплектований об'єкт одного окремого клієнтського HTTP-запиту з Request та Response.",
        "Option 3": "Інтерфейс для з'єднання C# і бази SQL.",
        "Option 4": "Кешована сторінка помилки HTML.",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Answer explanation": "Кожного разу Kestrel збирає байти запиту у HttpContext для читання (Request) та формування відповіді (Response) і його користувача (User)."
    },
    {
        "Question Text": "Що відбудеться, якщо в методі розширення `app.Use(...)` програміст забуде викликати ключовий `await next()`, але при цьому не встановить статусний код або тіло в HttpRequest?",
        "Question Type": "Multiple Choice",
        "Option 1": "Запит зациклиться.",
        "Option 2": "Пайплайн завершиться на цьому роботі, а обчислювання не дійде до справжньої кінцевої точки (MapGet), клієнт отримає пусту або поламану сторінку.",
        "Option 3": "Нічого серйозного, фреймворк автоматично виконає 'next()'.",
        "Option 4": "Програма моментально впаде з помилкою 500.",
        "Correct Answer": "2",
        "Time in seconds": "60",
        "Answer explanation": "У такому випадку Middleware діє як Термінатор (`Run`), розриваючи ланцюжок і не передаючи запит до кінцевого отримувача логіки."
    },
    {
        "Question Text": "Чому мутація статусу HTTP вказувати код 500 після того як ви виконали метод запису `context.Response.WriteAsync()` призведе до аварійного 'Headers already sent'?",
        "Question Type": "Multiple Choice",
        "Option 1": "Не дозволяється використовувати код 500 в ASP.NET Core.",
        "Option 2": "Дійсно, всі Headers та метод Статус-коду мусять віддаватись браузеру ПЕРЕД відправкою байтів тіла відповіді; Kestrel уже закінчив перемовини і почав лити байти.",
        "Option 3": "ASP.NET забороняє будь-які дії у відповідь без Middleware Logger.",
        "Option 4": "Браузер відхилить запит автоматично.",
        "Correct Answer": "2",
        "Time in seconds": "60",
        "Answer explanation": "Якщо хоча б один байт 'відповіді' уже 'полетів' до браузера - змінити HTTP-заголовки уже програмно неможливо."
    },
    {
        "Question Text": "У якому рекомендованому порядку потрібно ставити перевірки на Конвеєрі?",
        "Question Type": "Multiple Choice",
        "Option 1": "Auth -> ExceptionHandler -> Routing.",
        "Option 2": "UseRouting -> UseAuthentication -> UseEndpoints(MapGet).",
        "Option 3": "Спочатку логіку Controllers, тільки після - UseAuthentication.",
        "Option 4": "Порядок вказується при компіляції випадково.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "Kestrel мусить виставити UseRouting, щоб знати, який шлях викликано, а UseAuthentication - щоб захистити ці роути паролем/правами до виконання коду."
    },
    {
        "Question Text": "Що робить Middleware-метод `app.Map('/admin', ...)` у конвеєрі?",
        "Question Type": "Multiple Choice",
        "Option 1": "Він перейменовує всі файли з префіксом admin.",
        "Option 2": "Він розгалужує конвеєр на іншу повністю ізольовану під-гілку, яка ніколи не дійде до головного 'Run'.",
        "Option 3": "Парсить параметри адміністратора.",
        "Option 4": "Він кешує всі дані сервера.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "`Map()` створює паралельний міні-додаток і конвеєр лише для тих запитів, мітка шляху яких сходиться із роутом (напр. '/admin')."
    },
    {
        "Question Text": "Де саме повинен знаходитися обробник `UseExceptionHandler()`(або DeveloperExceptionPage)?",
        "Question Type": "Multiple Choice",
        "Option 1": "На самому початку пайплайну, щоб перехопити ('catch') паніку і помилки з усіх інших глибших Middleware під собою.",
        "Option 2": "В кінці пайплайну після всіх MapGet.",
        "Option 3": "Лише всередині класу бази даних.",
        "Option 4": "Всередині app.Map()",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "Через те, що помилка завжди стріляє у ланцюжку 'вгору' - перший блок очікує і може елегантно конвертувати краш у статус-код 500."
    },
    {
        "Question Text": "Яка ієрархія (матрьошка) ілюструє поведінку Middleware?",
        "Question Type": "Multiple Choice",
        "Option 1": "M1(start) -> M2(start) -> EndPoint -> M2(end) -> M1(end)",
        "Option 2": "M1 -> M2 -> M3 -> Client",
        "Option 3": "M3 -> M2 -> M1",
        "Option 4": "Рандомізована асинхронність",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "Зверніть увагу: виклик await next() занурює нас у наступний шар, а коли той повертається - ми випливаємо з нижніх циклів вверх до Kestrel."
    },
    {
        "Question Text": "Ключовий метод завершення у конвеєру (переважно для fallback/404), який зовні не передає запит далі (не має `next`), називається:",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "Run()",
        "Correct Answer": "1",
        "Time in seconds": "30",
        "Answer explanation": "`Run` є термінатором (Terminal Middleware), який зупиняє розкручування конвеєра на своєму рівні."
    },
    {
        "Question Text": "Якому правилу (Золоте Середовище) завжди слід коритися при написанні Inline Middleware щоб убезпечитись від Race Conditions?",
        "Question Type": "Open-Ended",
        "Time in seconds": "60",
        "Answer explanation": "Цілком уникнути зберігання даних про користувача/стан сервера у глобальних 'зовнішніх' або статичних змінних (Closure), бо Middleware виступає Singleton'ом один на весь сервер; застосовуйте Scoped DI."
    }
]

save_to_excel("04.request-pipeline-middleware.xlsx", data_04)
