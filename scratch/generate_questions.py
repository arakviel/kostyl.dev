import json
import os
import subprocess

questions = [
    {
        "Question Text": "Що станеться при завантаженні цієї HTML-сторінки в браузері?\n\n```html\n<script src=\"script.js\">\n  alert(\"Привіт, світ!\");\n</script>\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Виведеться вікно alert із повідомленням \"Привіт, світ!\", а зовнішній файл script.js проігнорується.",
        "Option 2": "Завантажиться та виконається зовнішній файл script.js, а вміст всередині тегу (виклик alert) буде проігноровано.",
        "Option 3": "Обидва скрипти виконаються: спочатку script.js, а потім alert.",
        "Option 4": "Виникне синтаксична помилка HTML.",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "Якщо в тегу <script> вказано атрибут src, то будь-який вміст всередині тегу ігнорується. Браузер завантажить і виконає лише зовнішній файл."
    },
    {
        "Question Text": "Що станеться під час виконання цього коду?\n\n```javascript\nalert(\"Привіт\")\n[1, 2].forEach(alert);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Спочатку з'явиться вікно \"Привіт\", а потім по черзі вікна \"1\" та \"2\".",
        "Option 2": "З'явиться вікно \"Привіт\", після чого виникне помилка (наприклад, TypeError).",
        "Option 3": "Виведеться тільки \"1\" та \"2\", а перша інструкція проігнорується.",
        "Option 4": "Код виконається без помилок, але нічого не виведе.",
        "Correct Answer": "2",
        "Time in seconds": 45,
        "Answer explanation": "Через відсутність крапки з комою після першого alert, JavaScript не вставиться автоматично перед квадратними дужками. Він трактуватиме це як alert(\"Привіт\")[1, 2].forEach(alert). Оскільки alert повертає undefined, спроба отримати властивість [1, 2] від undefined призведе до помилки."
    },
    {
        "Question Text": "Чи є цей код синтаксично коректним у JavaScript?\n\n```javascript\n/*\n  let message = \"Привіт\";\n  /* вкладений коментар */\n  alert(message);\n*/\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Так, це звичайний багаторядковий коментар.",
        "Option 2": "Ні, вкладені багаторядкові коментарі не підтримуються, тому виникне помилка.",
        "Option 3": "Так, але лише якщо увімкнено суворий режим \"use strict\".",
        "Option 4": "Так, але внутрішній коментар буде розцінено як звичайний текст.",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "У JavaScript вкладені багаторядкові коментарі виду /* ... /* ... */ ... */ не підтримуються. Закриваючий символ */ внутрішнього коментаря закриє весь зовнішній коментар передчасно, що призведе до помилки синтаксису для залишку коду."
    },
    {
        "Question Text": "Що станеться при виконанні цього коду?\n\n```javascript\nalert(\"Початок роботи\");\n\"use strict\";\nx = 5;\nalert(x);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Код завершиться з помилкою ReferenceError: x is not defined.",
        "Option 2": "Код успішно виконається і виведе спочатку \"Початок роботи\", а потім \"5\".",
        "Option 3": "Виникне помилка SyntaxError: \"use strict\" must be first.",
        "Option 4": "Директива \"use strict\" буде проігнорована, оскільки перед нею є інший код (крім коментарів), тому x створиться як глобальна змінна, і код виведе \"5\".",
        "Correct Answer": "4",
        "Time in seconds": 45,
        "Answer explanation": "Директива \"use strict\" має знаходитися на самому початку файлу (дозволяються лише коментарі перед нею). Оскільки перед нею викликається alert(), вона ігнорується, і код виконується в нестрогому режимі. У нестрогому режимі присвоєння неоголошеній змінній x = 5 автоматично створює глобальну змінну, тому помилки не буде."
    },
    {
        "Question Text": "Який буде результат виконання цього коду?\n\n```javascript\nlet message = \"Привіт\";\nlet message = \"Світ\";\nalert(message);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Виведеться \"Світ\".",
        "Option 2": "Виведеться \"Привіт\".",
        "Option 3": "Помилка: SyntaxError (змінну message вже було оголошено).",
        "Option 4": "Виведеться \"ПривітСвіт\".",
        "Correct Answer": "3",
        "Time in seconds": 30,
        "Answer explanation": "Оголошення змінної за допомогою let або const з тим самим ім'ям в тій самій області видимості вдруге призводить до помилки SyntaxError."
    },
    {
        "Question Text": "Виберіть усі ПРАВИЛЬНІ (допустимі) імена змінних у JavaScript.",
        "Question Type": "Checkbox",
        "Option 1": "let $ = 10;",
        "Option 2": "let _user = \"Ivan\";",
        "Option 3": "let 2ndPlace = \"Silver\";",
        "Option 4": "let my-variable = 5;",
        "Option 5": "let return = true;",
        "Correct Answer": "1,2",
        "Time in seconds": 45,
        "Answer explanation": "Імена змінних можуть містити букви, цифри, $ та _, але не можуть починатися з цифри (2ndPlace — неправильно), містити дефіс (my-variable — неправильно) або збігатися з зарезервованими словами (return — зарезервоване слово). Символи $ та _ є допустимими ідентифікаторами."
    },
    {
        "Question Text": "Чому для однієї константи використано великі літери (COLOR_RED), а для іншої — маленькі (pageLoadTime)?\n\n```javascript\nconst pageLoadTime = getPageLoadTime();\nconst COLOR_RED = \"#F00\";\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "COLOR_RED — це глобальна змінна, а pageLoadTime — локальна.",
        "Option 2": "Великі літери використовуються для констант, значення яких відоме до виконання коду (hardcoded), а маленькі — для констант, які обчислюються під час виконання (runtime).",
        "Option 3": "Це лише особисте уподобання розробника, технічної різниці немає і правила іменування не відрізняються.",
        "Option 4": "Константи з великими літерами не дозволяють змінювати значення, а з маленькими — дозволяють.",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "Згідно з практикою розробки, константи у верхньому регістрі (наприклад, COLOR_RED) використовуються для значень, які заздалегідь відомі до початку виконання програми (hardcoded). Для констант, що обчислюються під час виконання (наприклад, pageLoadTime), використовується звичайний верблюжий регістр (camelCase)."
    },
    {
        "Question Text": "Що відбудеться при спробі запустити цей код?\n\n```javascript\n\"use strict\";\nmessage = \"Я люблю JS\";\nalert(message);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Код виведе повідомлення \"Я люблю JS\" без помилок.",
        "Option 2": "Виникне помилка ReferenceError, оскільки змінна message не була оголошена за допомогою let, const або var.",
        "Option 3": "Виникне помилка SyntaxError, тому що рядок \"use strict\" має містити одинарні лапки.",
        "Option 4": "Змінна message автоматично оголоситься як константа.",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "У суворому режимі (\"use strict\") не дозволяється неявне створення змінних без ключових слів let, const або var. Спроба присвоїти значення неоголошеній змінній викликає ReferenceError."
    },
    {
        "Question Text": "Що виведе цей код?\n\n```javascript\nlet data = \"Тест\";\ndata = 42;\ndata = null;\nalert(typeof data);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "\"string\"",
        "Option 2": "\"number\"",
        "Option 3": "\"object\"",
        "Option 4": "\"null\"",
        "Correct Answer": "3",
        "Time in seconds": 30,
        "Answer explanation": "У JavaScript змінні є динамічно типізованими. Спочатку змінній data присвоєно рядок, потім число, а врешті-решт — null. Оператор typeof null повертає \"object\" через історичну помилку в мові JavaScript, яка залишається незмінною для зворотної сумісності."
    },
    {
        "Question Text": "Які значення отримають змінні a, b та c відповідно?\n\n```javascript\nlet a = 1 / 0;\nlet b = \"строка\" * 2;\nlet c = b + 5;\n```",
        "Question Type": "Checkbox",
        "Option 1": "a отримає значення Infinity",
        "Option 2": "b отримає значення NaN",
        "Option 3": "c отримає значення NaN",
        "Option 4": "b та c викликають фатальну помилку, яка зупиняє виконання скрипту.",
        "Correct Answer": "1,2,3",
        "Time in seconds": 45,
        "Answer explanation": "Ділення на нуль 1 / 0 дає Infinity. Множення некоректного рядка на число дає NaN. Оскільки NaN є \"причепливим\" (sticky), будь-яка подальша математична операція з ним (наприклад, NaN + 5) також повертає NaN. Обчислення в JS є безпечними та не зупиняють програму."
    },
    {
        "Question Text": "Що виведе цей код?\n\n```javascript\nlet result = NaN ** 0;\nalert(result);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "NaN",
        "Option 2": "0",
        "Option 3": "1",
        "Option 4": "undefined",
        "Correct Answer": "3",
        "Time in seconds": 30,
        "Answer explanation": "NaN є причепливим значенням і майже в будь-яких математичних операціях повертає NaN. Проте є єдиний виняток: операція піднесення до степеня NaN ** 0 дорівнює 1 (як і будь-яке інше число в степені 0)."
    },
    {
        "Question Text": "Що виведе цей код?\n\n```javascript\nconst value1 = 10;\nconst value2 = 10n;\nalert(typeof value1 === typeof value2);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "true",
        "Option 2": "false",
        "Option 3": "Виникне помилка SyntaxError через невідомий символ n.",
        "Option 4": "Виникне помилка TypeError при порівнянні різних типів.",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "Символ n наприкінці цілого числа позначає тип BigInt. typeof value1 поверне \"number\", а typeof value2 поверне \"bigint\". Вони не є однаковими, тому порівняння повертає false."
    },
    {
        "Question Text": "Що саме буде виведено на екран у вікні alert?\n\n```javascript\nlet user = \"Гість\";\nalert(\"Привіт, ${user}!\");\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Привіт, Гість!",
        "Option 2": "Привіт, ${user}!",
        "Option 3": "Привіт, undefined!",
        "Option 4": "Привіт, !",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "Інтерполяція змінних за допомогою ${...} працює ТІЛЬКИ у зворотних лапках (backticks: `...`). У подвійних \"...\" та одинарних '...' лапках цей запис сприймається як звичайний текст, тому буде виведено дослівно Привіт, ${user}!."
    },
    {
        "Question Text": "Що виведе цей код та чому?\n\n```javascript\nalert(typeof null);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "\"null\", оскільки null є окремим типом даних.",
        "Option 2": "\"object\", тому що null є об'єктом.",
        "Option 3": "\"object\", і це є офіційно визнаною помилкою в реалізації оператора typeof в JavaScript.",
        "Option 4": "\"undefined\", оскільки значення не визначено.",
        "Correct Answer": "3",
        "Time in seconds": 30,
        "Answer explanation": "Результатом typeof null є \"object\". Це відома помилка в мові з її найперших версій, яка зберігається заради сумісності зі старим кодом. Насправді null — це окремий примітивний тип даних, а не об'єкт."
    },
    {
        "Question Text": "Який тип даних поверне typeof alert у браузері?\n\n```javascript\nalert(typeof alert);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "\"object\"",
        "Option 2": "\"function\"",
        "Option 3": "\"undefined\"",
        "Option 4": "\"string\"",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "alert є вбудованою функцією. Оператор typeof для будь-якої функції повертає рядок \"function\". Хоча технічно в JavaScript немає окремого типу даних \"function\" (функції є об'єктами), така поведінка typeof реалізована для зручності."
    },
    {
        "Question Text": "Що буде виведено у вікні alert?\n\n```javascript\nlet num1 = Number(undefined);\nlet num2 = Number(null);\nalert(`${num1}, ${num2}`);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "NaN, 0",
        "Option 2": "0, 0",
        "Option 3": "NaN, NaN",
        "Option 4": "0, NaN",
        "Correct Answer": "1",
        "Time in seconds": 30,
        "Answer explanation": "При перетворенні на число за допомогою Number(), значення undefined перетворюється на NaN, а null перетворюється на 0. Це поширена помилка серед новачків, які очікують 0 в обох випадках."
    },
    {
        "Question Text": "Який тип даних матиме змінна result?\n\n```javascript\nlet result = \"10\" / \"2\";\nalert(typeof result);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "\"string\"",
        "Option 2": "\"number\"",
        "Option 3": "\"NaN\"",
        "Option 4": "\"object\"",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "Математичний оператор ділення / автоматично приводить свої операнди до чисел. Рядки \"10\" та \"2\" перетворюються на числа 10 та 2, відповідно ділення дає 5, яке є типом \"number\"."
    },
    {
        "Question Text": "Що виведе цей код?\n\n```javascript\nlet bool1 = Boolean(\"0\");\nlet bool2 = Boolean(\" \");\nalert(bool1 && bool2);\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "false",
        "Option 2": "true",
        "Option 3": "NaN",
        "Option 4": "0",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "У JavaScript при перетворенні на булевий тип будь-які непусті рядки (включаючи рядок із нулем \"0\" та рядок із пробілом \" \") стають true. Лише абсолютно порожній рядок \"\" стає false. Таким чином, bool1 та bool2 дорівнюють true, і операція true && true дає true."
    },
    {
        "Question Text": "Які з цих змінних отримають значення false?\n\n```javascript\nlet a = Boolean(0);\nlet b = Boolean(\"вітаю\");\nlet c = Boolean(NaN);\nlet d = Boolean(undefined);\n```",
        "Question Type": "Checkbox",
        "Option 1": "a",
        "Option 2": "b",
        "Option 3": "c",
        "Option 4": "d",
        "Correct Answer": "1,3,4",
        "Time in seconds": 45,
        "Answer explanation": "Значення, які інтуїтивно є \"порожніми\" (такі як 0, порожній рядок \"\", null, undefined та NaN), при булевому перетворенні стають false. Будь-які інші значення (наприклад, непустий рядок \"вітаю\") перетворюються на true."
    },
    {
        "Question Text": "Для чого потрібна дана конструкція в JavaScript розробці?\n\n```javascript\n(function() {\n  'use strict';\n  alert(\"Працює!\");\n})()\n```",
        "Question Type": "Multiple Choice",
        "Option 1": "Вона створює новий об'єкт та додає до нього метод alert.",
        "Option 2": "Це спосіб безпечно активувати суворий режим \"use strict\" лише для конкретного блоку коду (функції-обгортки), не впливаючи на інший код.",
        "Option 3": "Вона використовується для оптимізації роботи з кешем браузера.",
        "Option 4": "Це обов'язковий синтаксис для підключення зовнішніх файлів скриптів.",
        "Correct Answer": "2",
        "Time in seconds": 30,
        "Answer explanation": "Директиву 'use strict' можна вказувати на початку окремої функції, щоб увімкнути суворий режим лише для коду всередині неї. Функція-обгортка (function() { ... })() негайно викликається і локалізує строгий режим, що корисно при об'єднанні декількох скриптів (наприклад, у старіших версіях браузерів, де консоль не підтримує strict mode глобально)."
    }
]

with open("/Users/arakviel/Work/kostyl.dev/scratch/temp_questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Temporary JSON written successfully.")
