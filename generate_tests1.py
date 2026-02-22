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

data_01 = [
    {
        "Question Text": "Що є ключовою проблемою розробки на старих платформах ASP.NET Web Forms?",
        "Question Type": "Multiple Choice",
        "Option 1": "Вимога працювати тільки в операційній системі Linux.",
        "Option 2": "Спроба приховати природу HTTP через події та повільний ViewState.",
        "Option 3": "Відсутність підтримки об'єктно-орієнтованого програмування.",
        "Option 4": "Необхідність компіляції напряму через командний рядок.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "Web Forms генерував гігантські приховані поля (ViewState) для збереження стану, що порушувало природу вебу (statelessness)."
    },
    {
        "Question Text": "Оберіть головну характеристику архітектури нового ASP.NET Core (2016).",
        "Question Type": "Multiple Choice",
        "Option 1": "Повна залежність від Internet Information Services.",
        "Option 2": "Підтримка виключно мобільних застосунків.",
        "Option 3": "Кросплатформеність, незалежність від Windows та модульність.",
        "Option 4": "Вбудована підтримка мови Python.",
        "Correct Answer": "3",
        "Time in seconds": "30",
        "Answer explanation": "ASP.NET Core створювався як повністю кросплатформений, модульний і швидший фреймворк, пристосований до Linux і Docker."
    },
    {
        "Question Text": "Чому новий веб-сервер Kestrel обробляє мільйони запитів настільки швидко?",
        "Question Type": "Multiple Choice",
        "Option 1": "Відкриває новий окремий потік операційної системи на кожен HTTP запит.",
        "Option 2": "Він кешує всі відповіді в локальній базі даних.",
        "Option 3": "Використовує пам'ять без аллокацій (zero-allocation) через Spans та асинхронні Pipelines.",
        "Option 4": "Працює віддалено на серверах Azure за замовчуванням.",
        "Correct Answer": "3",
        "Time in seconds": "60",
        "Answer explanation": "Kestrel мінімізує виділення нової пам'яті (щоб не навантажувати Garbage Collector) та працює з System.IO.Pipelines замість стандартних Streams."
    },
    {
        "Question Text": "Чому на бойових серверах Kestrel зазвичай ховають за реверс-проксі (наприклад Nginx)?",
        "Question Type": "Multiple Choice",
        "Option 1": "Оскільки Kestrel не розуміє звичайний HTTP протокол.",
        "Option 2": "Для керування SSL сертифікатами та захисту від DDoS атак.",
        "Option 3": "Тому що Kestrel працює дуже повільно з великою кількістю даних.",
        "Option 4": "Щоб перетворити C# код на JavaScript.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "Реверс-проксі (Reverse Proxy) має розширені функції балансування, захисту від поганого трафіку і працює як додатковий рівень безпеки."
    },
    {
        "Question Text": "Як підхід Minimal API відрізняється від MVC модельних додатків?",
        "Question Type": "Multiple Choice",
        "Option 1": "Minimal API використовує менший об'єм пам'яті, залишаючи ті ж функції",
        "Option 2": "Знімає необхідність використання бази даних.",
        "Option 3": "Централізовано використовує Program.cs для маршрутизації замість великої кількості контролерів і атрибутів.",
        "Option 4": "Виконується виключно на фронтенді.",
        "Correct Answer": "3",
        "Time in seconds": "45",
        "Answer explanation": "Minimal APIs видаляють 'бойлерплейт' і дозволяють створити ендпоінти кількома рядками в Program.cs."
    },
    {
        "Question Text": "Яка фіча мови C# 9.0 дозволила прибрати традиційний `static void Main()` з Program.cs?",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "Top-Level Statements",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "Top-Level Statements дозволили компілятору приховано згенерувати клас Program з Main."
    },
    {
        "Question Text": "ASP.NET Core програма є матрьошкою, де найнижчий рівень - це Kestrel, що є наступним рівнем який обробляє логіку запиту?",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "Middleware",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "Запит від сервера проходить через ланцюжок фільтрів, що називається Middleware Pipeline."
    },
    {
        "Question Text": "ASP.NET Core Minimal APIs швидше за MVC завдяки меншим витратам (Routing overhead) на створення екземплярів класів.",
        "Question Type": "Multiple Choice",
        "Option 1": "Правда",
        "Option 2": "Брехня",
        "Correct Answer": "1",
        "Time in seconds": "30",
        "Answer explanation": "Дійсно, так як маршрути мапляться прямо до делегатів через `MapGet`, без рефлексії над класами-контролерами."
    },
    {
        "Question Text": "Неявні імпорти (Implicit Usings) дозволяють вам...",
        "Question Type": "Multiple Choice",
        "Option 1": "Видаляти класи з коду в рантаймі.",
        "Option 2": "Не вказувати найбільш спільні `using ...` нагорі кожного файлу.",
        "Option 3": "Завантажувати і підтягувати будь які пакети з інтернету.",
        "Option 4": "Асинхронно виконувати I/O операції.",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Answer explanation": "Ця фіча автоматично ховає імпорти базових системних та ASP.NET бібліотек."
    },
    {
        "Question Text": "Що робить `app.Run()` в кінці файлу Minimal API?",
        "Question Type": "Open-Ended",
        "Time in seconds": "60",
        "Answer explanation": "Це вічний цикл, що блокує завершення програми і відкриває Kestrel для прослуховування вхідних HTTP запитів."
    }
]

save_to_excel("01.introduction.xlsx", data_01)

data_02 = [
    {
        "Question Text": "Яка команда консолі .NET CLI швидко згенерує проект 'Minimal API'?",
        "Question Type": "Multiple Choice",
        "Option 1": "dotnet new minimal",
        "Option 2": "dotnet create web_api",
        "Option 3": "dotnet new web",
        "Option 4": "dotnet build web",
        "Correct Answer": "3",
        "Time in seconds": "30",
        "Answer explanation": "Саме `dotnet new web` є командою створення шаблону ASP.NET Core Empty."
    },
    {
        "Question Text": "Що міститься в `.csproj` файлі проекту ASP.NET?",
        "Question Type": "Multiple Choice",
        "Option 1": "XML конфігурації для компілятора та перелік NuGet залежностей.",
        "Option 2": "JSON зі списками середовищ для розробки.",
        "Option 3": "Ключі від зовнішніх баз даних (Connection Strings).",
        "Option 4": "Лише C# код, потрібний для запуску програми.",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "C-Sharp Project (.csproj) це XML-документ з налаштуваннями SDK, платформенними вимогами та пакетами NuGet."
    },
    {
        "Question Text": "Для чого потрібен файл Properties/launchSettings.json?",
        "Question Type": "Multiple Choice",
        "Option 1": "Він визначає змінні середовища та параметри локального запуску тільки на машині розробника.",
        "Option 2": "Він використовується на бойових серверах (Production) для запуску IIS.",
        "Option 3": "Він керує маршрутизуванням запитів (routing).",
        "Option 4": "Тут обов'язково зберігаються справжні паролі до баз даних.",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "Цей файл застосовується лише в середовищі розробки для локального налаштування Kestrel та відкриття портів/браузера."
    },
    {
        "Question Text": "Команда `dotnet watch` дозволяє:",
        "Question Type": "Multiple Choice",
        "Option 1": "Блокувати запити від хакерів під час розробки.",
        "Option 2": "Стежити за змінами у файлах і автоматично перезапускати сервер під час редагування (Hot Reload).",
        "Option 3": "Моніторити статистику CPU запущеного додатку.",
        "Option 4": "Компілювати додаток для віддаленого Production сервера.",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Answer explanation": "dotnet watch перекомпілює чи застосовує мікро-зміни у коді на-льоту для швидкої розробки."
    },
    {
        "Question Text": "У якому файлі розробникам слід зберігати рівні логування та загальні статичні налаштування середовища?",
        "Question Type": "Multiple Choice",
        "Option 1": "launchSettings.json",
        "Option 2": "appsettings.json",
        "Option 3": "web.config",
        "Option 4": ".csproj",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Answer explanation": "Файли appsettings.json та appsettings.Development.json керують поведінкою ASP.NET та дозволяють зберігати загальні змінні конфігурації."
    },
    {
        "Question Text": "У Minimal API лямбда-виразі `app.MapGet()` якщо додати новий маршрут лише для MapPost(), що поверне браузер якщо юзер просто набере URL в адресний рядок?",
        "Question Type": "Multiple Choice",
        "Option 1": "200 Success з результатом виконання.",
        "Option 2": "404 Not Found або 405 Method Not Allowed.",
        "Option 3": "Відкриється модальне вікно запиту даних POST.",
        "Option 4": "Відбудеться компіляційна помилка при запуску C# коду.",
        "Correct Answer": "2",
        "Time in seconds": "45",
        "Answer explanation": "Звичайний перехід за лінком робить метод GET; якщо зареєстровано лише POST - сервер відповість помилкою."
    },
    {
        "Question Text": "ASP.NET Core Minimal API має асинхронну модель на основі пулу потоків і може паралельно обслуговувати безліч з'єднань.",
        "Question Type": "Multiple Choice",
        "Option 1": "Правда",
        "Option 2": "Брехня",
        "Correct Answer": "1",
        "Time in seconds": "30",
        "Answer explanation": "На відміну від Node.js, ASP.NET бере вільні потоки Thread Pool для кожної логіки паралельно."
    },
    {
        "Question Text": "Яким чином builder (WebApplicationBuilder) отримує додаткові аргументи командного рядку (наприклад --port 8080)?",
        "Question Type": "Multiple Choice",
        "Option 1": "Через системні Environment Variables автоматично.",
        "Option 2": "Передачею масиву 'args' з командного рядка в метод CreateBuilder(args).",
        "Option 3": "Такі налаштування неможливі, порт фіксується завжди в Json.",
        "Option 4": "Зчитується з реєстру Windows.",
        "Correct Answer": "2",
        "Time in seconds": "30",
        "Answer explanation": "Масив args передається у фундамент `CreateBuilder` дозволяючи гнучке перевизначення."
    },
    {
        "Question Text": "Яку середу програмування обере 'фанат кросплатформено-сильної IDE з вбудованим ReSharper' за версією матеріалу?",
        "Question Type": "Fill-in-the-Blank",
        "Option 1": "JetBrains Rider",
        "Correct Answer": "1",
        "Time in seconds": "45",
        "Answer explanation": "Rider працює кросплатформово та пропонує передові аналізатори коду."
    },
    {
        "Question Text": "Опишіть, чому ми не зберігаємо реальні 'секрети' у `appsettings.json`?",
        "Question Type": "Open-Ended",
        "Time in seconds": "60",
        "Answer explanation": "Ці файли повинні індексуватись та завантажуватись в систему контролю версій (наприклад Git). Секрети перехопляться зливом, тому їх треба містити в Environment Variables або User Secrets."
    }
]

save_to_excel("02.first-application.xlsx", data_02)
