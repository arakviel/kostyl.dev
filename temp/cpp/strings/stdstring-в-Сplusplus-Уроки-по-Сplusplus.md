Вашою першою програмою на мові C++, ймовірно, була всім відома програма “Hello, world!”:

|1
|---|
2
3
4
5
6
7|#include <iostream>
int main()
{
    std::cout << "Hello, world!" << std::endl;
    return 0;
}|

Чи не так? Але що таке `Hello, world!`? `Hello, world!` — це послідовність символів або просто **рядок** (англ. _**“string”**_). У мові C++ ми використовуємо рядки для представлення тексту (імен, адрес, слів і речень). Рядкові літерали (такі як `Hello, world!`) пишуться в подвійних лапках.

Оскільки їх часто використовують в програмах, то більшість сучасних мов програмування мають вбудований **тип даних string**. У мові C++ також є цей тип, але не як основна частина мови, а як частина Стандартної бібліотеки С++.

Зміст:

1.  [Тип даних string](https://acode.com.ua/urok-60-vvedennya-v-std-string/#toc-0)
2.  [Ввід/вивід рядків](https://acode.com.ua/urok-60-vvedennya-v-std-string/#toc-1)
3.  [Використання std::getline()](https://acode.com.ua/urok-60-vvedennya-v-std-string/#toc-2)
4.  [Використання std::getline() з std::cin](https://acode.com.ua/urok-60-vvedennya-v-std-string/#toc-3)
5.  [Додавання рядків](https://acode.com.ua/urok-60-vvedennya-v-std-string/#toc-4)
6.  [Довжина рядків](https://acode.com.ua/urok-60-vvedennya-v-std-string/#toc-5)
7.  [Тест](https://acode.com.ua/urok-60-vvedennya-v-std-string/#toc-6)

## Тип даних string

Щоб мати можливість використовувати рядки в мові C++, спочатку необхідно підключити [**заголовок**](https://acode.com.ua/urok-24-zagolovkovi-fajly/) string. Як тільки це буде зроблено, ми зможемо визначити змінні типу string:

|1
|---|
2
3
4
5|#include <string>
// ...
std::string name;
// ...|

Як і зі звичайними змінними, ми можемо ініціалізовувати змінні типу string або присвоювати їм значення:

|1
|---|
2|std::string name("Sasha"); // ініціалізуємо змінну name рядковим літералом "Sasha"
name \= "Masha"; // присвоюємо змінній name рядковий літерал "Masha"|

Рядки також можуть містити числа:

|1|std::string myID("34"); // "34" тут - це не ціле число 34!|
|---|---|

Варто відзначити, що числа, які присвоюються, тип string обробляє як текст, а не як числа. А це означає, що ними не можна маніпулювати як звичайними числами (наприклад, ви не зможете виконати з ними [**арифметичні операції**](https://acode.com.ua/urok-42-aryfmetychni-operatory/)). Мова C++ автоматично НЕ конвертує їх в значення цілочисельних типів данів або типів з плаваючою крапкою.

## Ввід/вивід рядків

Рядки можна виводити за допомогою [**std::cout**](https://acode.com.ua/urok-14-objects-cout-cin-i-endl/#toc-0):

|1
|---|
2
3
4
5
6
7
8
9
10|#include <iostream>
#include <string>
int main()
{
    std::string name("Sasha");
    std::cout << "My name is " << name;
    return 0;
}|

Результат виконання програми:

`My name is Sasha`

А ось з [**std::cin**](https://acode.com.ua/urok-14-objects-cout-cin-i-endl/#toc-2) справи йдуть трохи інакше. Розглянемо наступний приклад:

|1
|---|
2
3
4
5
6
7
8
9
10
11
12
13
14
15|#include <iostream>
#include <string>
int main()
{
    std::cout << "Enter your full name: ";
    std::string myName;
    std::cin \>> myName; // це працюватиме не так, як очікується, оскільки вилучення даних з потоку std::cin зупиниться на першому пробілі
    std::cout << "Enter your age: ";
    std::string myAge;
    std::cin \>> myAge;
    std::cout << "Your name is " << myName << " and your age is " << myAge;
}|

Результат виконання програми:

`Enter your full name: Sasha Mak  Enter your age: Your name is Sasha and your age is Mak`

Хм, щось не так! Що ж трапилося? Виявляється, оператор виводу (`>>`) повертає символи з вхідного потоку даних тільки до першого пробілу. Всі інші символи залишаються всередині std::cin, очікуючи наступного вилучення.

Тому, коли ми використали оператор `>>` для вилучення даних в змінну `myName`, тільки `Sasha` вдалося витягнути, `Mak` залишився всередині std::cin, очікуючи наступного вилучення. Коли ми використали оператор `>>` знову, щоб витягнути дані в змінну `myAge`, ми отримали `Mak` замість `25`. Якби ми виконали третє вилучення, то отримали б `25`.

## Використання std::getline()

Щоб витягнути цілий рядок з вхідного потоку даних (разом з пробілами), використовуйте **функцію std::getline()**. Вона приймає два параметри: перший — std::cin, другий — змінна типу string.

Ось вищенаведена програма, але вже з використанням std::getline():

|1
|---|
2
3
4
5
6
7
8
9
10
11
12
13
14
15|#include <iostream>
#include <string>
int main()
{
    std::cout << "Enter your full name: ";
    std::string myName;
    std::getline(std::cin, myName); // повністю вилучаємо рядок в змінну myName
    std::cout << "Enter your age: ";
    std::string myAge;
    std::getline(std::cin, myAge); // повністю вилучаємо рядок в змінну myAge
    std::cout << "Your name is " << myName << " and your age is " << myAge;
}|

Тепер програма працює правильно:

`Enter your full name: Sasha Mak  Enter your age: 25  Your name is Sasha Mak and your age is 25`

## Використання std::getline() з std::cin

Вилучення даних з std::cin за допомогою std::getline() іноді може призвести до несподіваних результатів. Наприклад, розглянемо наступну програму:

|1
|---|
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17|#include <iostream>
#include <string>
int main()
{
    std::cout << "Pick 1 or 2: ";
    int choice;
    std::cin \>> choice;
    std::cout << "Now enter your name: ";
    std::string myName;
    std::getline(std::cin, myName);
    std::cout << "Hello, " << myName << ", you picked " << choice << '\\n';
    return 0;
}|

Можливо, ви здивуєтеся, але коли ви запустите цю програму, і вона попросить вас ввести ваше ім’я, вона не чекатиме вашого вводу, а відразу виведе результат (просто пробіл замість вашого імені)!

Пробний запуск програми:

`Pick 1 or 2: 2  Now enter your name: Hello, , you picked 2`

Чому так? Виявляється, коли ви вводите числове значення, потік cin захоплює разом з вашим числом і символ нового рядка. Тому, коли ми ввели `2`, cin фактично отримав `2\n`. Потім він витягнув значення `2` в змінну, залишаючи `\n` (символ нового рядка) у вхідному потоці. Потім, коли std::getline() отримує дані для `myName`, він бачить в потоці `\n` і думає, що ми, мабуть, ввели просто порожній рядок! А це, безумовно, не те, що ми хочемо.

Хорошою практикою вважається видаляти з вхідного потоку даних символ нового рядка. Це можна зробити наступним чином:

|1|std::cin.ignore(32767, '\\n'); // ігноруємо символи нового рядка "\\n" у вхідному потоці довжиною 32767 символів|
|---|---|

Якщо ми вставимо цей рядок безпосередньо після отримання вхідних даних, то символ нового рядка буде видалено з вхідного потоку, і програма працюватиме належним чином:

|1
|---|
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19|#include <iostream>
#include <string>
int main()
{
std::cout << "Pick 1 or 2: ";
int choice;
std::cin \>> choice;
std::cin.ignore(32767, '\\n'); // видаляємо символ нового рядка з вхідного потоку даних
std::cout << "Now enter your name: ";
std::string myName;
std::getline(std::cin, myName);
std::cout << "Hello, " << myName << ", you picked " << choice << '\\n';
return 0;
}|

**Правило: При вводі числових значень не забувайте видаляти символ нового рядка з вхідного потоку даних за допомогою std::cin.ignore().**

## Додавання рядків

Ви можете використовувати оператор `+` для об’єднання двох рядків або оператор `+=` для додавання двох рядків.

У наступній програмі ми протестуємо ці два оператори, а також покажемо, що відбудеться, якщо ви спробуєте використати оператор `+` для додавання двох числових рядків:

|1
|---|
2
3
4
5
6
7
8
9
10
11
12
13
14|#include <iostream>
#include <string>
int main()
{
    std::string x("44");
    std::string y("12");
    std::cout << x + y << "\\n"; // об'єднуємо рядки x і y (а не додаємо числа)
    x += " cats";
    std::cout << x;
    return 0;
}|

Результат виконання програми:

`4412  44 cats`

Зверніть увагу, оператор `+` об’єднав два числових рядки в один (`44` + `12` = `4412`). Він не додавав ці рядки як числа.

## Довжина рядків

Щоб дізнатися довжину рядка, ми можемо зробити наступне:

|1
|---|
2
3
4
5
6
7
8
9
10|#include <iostream>
#include <string>
int main()
{
    std::string myName("Sasha");
    std::cout << myName << " has " << myName.length() << " characters\\n";
    return 0;
}|

Результат виконання програми:

`Sasha has 5 characters`

Зверніть увагу, замість запиту довжини рядка як `length(myName)`, ми пишемо `myName.length()`.

Функція запиту довжини рядка не є звичайною функцією, як ті, що ми використовували раніше. Це особливий тип функції класу std::string, який називається _методом_. Ми поговоримо про це детально, коли будемо розглядати тему класів.

## Тест

Напишіть програму, яка просить у користувача ввести ім’я, прізвище та вік. В результаті вкажіть користувачеві, скільки років він прожив на кожну букву з його імені та прізвища (щоб було простіше, враховуйте також пробіли), наприклад:

`Enter your full name: Tom Cats  Enter your age: 45  You've lived 5.625 years for each letter in your name.`

_**Уточнення**:_ Вік `45` ділиться на `Tom Cats` (8 букв, враховуючи пробіл), що дорівнює `5.625`.

**Відповідь**

|1
|---|
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19|#include <iostream>
#include <string>
int main()
{
    std::cout << "Enter your full name: ";
    std::string myName;
    std::getline(std::cin, myName); // вилучаємо цілий рядок з вхідного потоку даних у змінну myName
    std::cout << "Enter your age: ";
    int myAge; // змінна myAge повинна бути типу int, а не типу string, щоб ми могли виконувати з нею арифметичні операції
    std::cin \>> myAge;
    int letters \= myName.length(); // обчислюємо довжину змінної myName (враховуючи пробіли)
    double agePerLetter \= static\_cast<double\>(myAge) / letters; // використовуємо оператор static\_cast, щоб змінити тип змінної myAge на double (для збереження дробової частини при цілочисельному діленні)
    std::cout << "You've lived " << agePerLetter << " years for each letter in your name.\\n";
    return 0;
}|

Оцінити статтю:

![1 Зірка](stdstring/rating_on.gif "1 Зірка")![2 Зірки](stdstring/rating_on.gif "2 Зірки")![3 Зірки](stdstring/rating_on.gif "3 Зірки")![4 Зірки](stdstring/rating_on.gif "4 Зірки")![5 Зірок](stdstring/rating_half.gif "5 Зірок") (**86** оцінок, середня: **4,88** з 5)

![](stdstring/loading.gif)Завантаження...