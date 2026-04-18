На цьому уроці ми розглянемо способи доступу до символів [**std::string**](https://acode.com.ua/urok-208-ryadkovi-klasy-std-string-i-std-wstring/) і способи конвертації std::string в [**рядки C-style**](https://acode.com.ua/urok-82-ryadky-c-style/).

Зміст:

1.  [Доступ до символів std::string](https://acode.com.ua/urok-211-dostup-do-symvoliv-std-string-konvertatsiya-std-string-v-ryadky-c-style/#toc-0)
2.  [Конвертація std::string в рядки C-style](https://acode.com.ua/urok-211-dostup-do-symvoliv-std-string-konvertatsiya-std-string-v-ryadky-c-style/#toc-1)

## Доступ до символів std::string

Є два практично ідентичних способи доступу до символів std::string. Найбільш простий і швидкий — використати [**перевантажений оператор індексації \[\]**](https://acode.com.ua/urok-146-perevantazhennya-operatora-indeksatsiyi/).

### char& string::operator\[\](size\_type nIndex)

const char& string::operator\[\](size\_type nIndex) const

   Обидві ці функції повертають символ під індексом `nIndex`.

   Передача невірного індексу призведе до невизначених результатів.

   Використання [**функції length()**](https://acode.com.ua/urok-210-dovzhyna-i-yemnist-std-string/) в якості індексу допустимо тільки для константних рядків і повертає значення, згенероване конструктором за замовчуванням std::string. Це не рекомендується робити.

   Оскільки `char&` — це тип повернення, то ви можете використовувати його для зміни символів рядка.

Наприклад:

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
std::string sSomething("abcdefg");
std::cout << sSomething\[4\] << std::endl;
sSomething\[4\] \= 'A';
std::cout << sSomething << std::endl;
}|

Результат:

`e  abcdAfg`

Інший спосіб доступу до символів std::string повільніший, ніж вищенаведений варіант, тому що використовує [**винятки**](https://acode.com.ua/urok-190-obrobka-vynyatkiv-operatory-throw-try-i-catch/) для перевірки коректності `nIndex`. Якщо ви не впевнені в правильності переданого `nIndex`, то ви повинні використовувати саме цей спосіб (той, що описаний нижче) для доступу до символів рядка.

### char& string::at(size\_type nIndex)

const char& string::at(size\_type nIndex) const

   Обидві ці функції повертають символ під індексом `nIndex`.

   Передача невірного індексу призведе до генерації винятку out\_of\_range.

   Оскільки `char&` — це тип повернення, то ви можете використовувати його для зміни символів рядка.

Наприклад:

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
std::string sSomething("abcdefg");
std::cout << sSomething.at(4) << std::endl;
sSomething.at(4) \= 'A';
std::cout << sSomething << std::endl;
}|

Результат:

`e  abcdAfg`

## Конвертація std::string в рядки C-style

Багато функцій (включаючи всі функції мови C++) очікують форматування рядків як рядків C-style, а не як std::string. З цієї причини std::string надає 3 різних способи конвертації std::string в рядки C-style.

### const char\* string::c\_str() const

   Повертає вміст std::string у вигляді константного рядка C-style.

   Додається нуль-термінатор.

   Рядок C-style належить std::string і не повинен бути видалений.

Наприклад:

|1
|---|
2
3
4
5
6
7
8|#include <iostream>
#include <string>
int main()
{
std::string sSomething("abcdefg");
std::cout << strlen(sSomething.c\_str());
}|

Результат:

`7`

### const char\* string::data() const

   Повертає вміст std::string у вигляді константного рядка C-style.

   Не додається нуль-термінатор.

   Рядок C-style належить std::string і не повинен бути видалений.

Наприклад:

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
std::string sSomething("abcdefg");
const char \*szString \= "abcdefg";
// Функція memcmp() порівнює два вищенаведених рядки C-style і повертає 0, якщо вони рівні
if (memcmp(sSomething.data(), szString, sSomething.length()) \== 0)
std::cout << "The strings are equal";
else
std::cout << "The strings are not equal";
}|

Результат:

`The strings are equal`

### size\_type string::copy(char \*szBuf, size\_type nLength) const

size\_type string::copy(char \*szBuf, size\_type nLength, size\_type nIndex) const

   Відмінність другого варіанту цієї функції від першого полягає в тому, що копіювання не більше `nLength` символів переданого рядка в `szBuf` починається з символу під індексом `nIndex`. У першій же функції копіювання завжди починається з символу під індексом `[0]`.

   Кількість скопійованих символів повертається.

   Caller відповідає за те, щоб не відбулося [**переповнення**](https://acode.com.ua/urok-34-tsilochyselni-typy-danyh-short-int-i-long/#toc-4) рядка `szBuf`.

Наприклад:

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
13|#include <iostream>
#include <string>
int main()
{
std::string sSomething("lorem ipsum dolor sit amet");
char szBuf\[20\];
int nLength \= sSomething.copy(szBuf, 5, 6);
szBuf\[nLength\] \= '\\0'; // завершуємо рядок в буфері
std::cout << szBuf << std::endl;
}|

Результат:

`ipsum`

Якщо вам не потрібна максимальна ефективність, то c\_str() — це найпростіший і найбезпечніший спосіб конвертації std::string в рядки C-style.

Оцінити статтю:

![1 Зірка](article/rating_on.gif "1 Зірка")![2 Зірки](article/rating_on.gif "2 Зірки")![3 Зірки](article/rating_on.gif "3 Зірки")![4 Зірки](article/rating_on.gif "4 Зірки")![5 Зірок](article/rating_on.gif "5 Зірок") (**38** оцінок, середня: **4,95** з 5)

![](article/loading.gif)Завантаження...