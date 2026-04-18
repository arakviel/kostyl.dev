Щоб додати один [**рядок**](https://acode.com.ua/urok-208-ryadkovi-klasy-std-string-i-std-wstring/) до іншого, можна використати перевантажений оператор `+=`, функцію append() або функцію push\_back().

## string& string::operator+=(const string& str)

string& string::append(const string& str)

   Обидві функції додають до std::string рядок `str`.

   Повертають [**прихований вказівник \*this**](https://acode.com.ua/urok-129-pryhovanyj-vkazivnyk-this/), що дозволяє «зв’язувати» об’єкти.

   [**Генерують виняток**](https://acode.com.ua/urok-190-obrobka-vynyatkiv-operatory-throw-try-i-catch/) length\_error, якщо результат перевищує максимально допустиму кількість символів.

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
std::string sString("one");
sString += std::string(" two");
std::string sThree(" three");
sString.append(sThree);
std::cout << sString << std::endl;
}|

Результат:

`one two three`

Існує також різновид функції append(), який може додавати підрядок.

## string& string::append(const string& str, size\_type index, size\_type num)

   Ця функція додає до std::string рядок `str` з кількістю символів, які вказані в `num`, починаючи з `index`.

   Повертає прихований вказівник \*this, що дозволяє «зв’язувати» об’єкти.

   Генерує виняток out\_of\_range, якщо `index` некоректний.

   Генерує виняток length\_error, якщо результат перевищує максимально допустиму кількість символів.

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
11|#include <iostream>
#include <string>
int main()
{
std::string sString("one ");
const std::string sTemp("twothreefour");
sString.append(sTemp, 8, 4); // додаємо до std::string підрядок sTemp довжиною 4, починаючи з символа під індексом 8
std::cout << sString << std::endl;
}|

Результат:

`one four`

Оператор `+=` і функція append() також мають версії, які працюють з [**рядками C-style**](https://acode.com.ua/urok-82-ryadky-c-style/).

## string& string::operator+=(const char\* str)

string& string::append(const char\* str)

   Обидві функції додають до std::string рядок C-style `str`.

   Повертають прихований вказівник \*this, що дозволяє «зв’язувати» об’єкти.

   Генерують виняток length\_error, якщо результат перевищує максимально допустиму кількість символів.

   `str` не повинен бути `NULL`.

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
11|#include <iostream>
#include <string>
int main()
{
std::string sString("one");
sString += " two";
sString.append(" three");
std::cout << sString << std::endl;
}|

Результат:

`one two three`

І є ще один різновид функції append(), який працює з рядками C-style.

## string& string::append(const char\* str, size\_type len)

   Додає до std::string кількість символів (які вказані в `len`) рядка C-style `str`.

   Повертає прихований вказівник \*this, що дозволяє «зв’язувати» об’єкти.

   Генерує виняток length\_error, якщо результат перевищує максимально допустиму кількість символів.

   Ігнорує спеціальні символи (враховуючи `"`).

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
std::string sString("two ");
sString.append("fivesix", 4);
std::cout << sString << std::endl;
}|

Результат:

`two five`

Ця функція небезпечна, тому використовувати її не рекомендується. Існують також функції, які додають окремі (поодинокі) символи.

## string& string::operator+=(char c)

void string::push\_back(char c)

   Обидві функції додають до std::string символ `c`.

   Оператор `+=` повертає прихований вказівник \*this, що дозволяє «зв’язувати» об’єкти.

   Обидві функції генерують виняток length\_error, якщо результат перевищує максимально допустиму кількість символів.

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
11|#include <iostream>
#include <string>
int main()
{
std::string sString("two");
sString += ' ';
sString.push\_back('3');
std::cout << sString << std::endl;
}|

Результат:

`two 3`

## string& string::append(size\_type num, char c)

   Ця функція додає до std::string кількість входжень (які вказані в `num`) символа `c`.

   Повертає прихований вказівник \*this, що дозволяє «зв’язувати» об’єкти.

   Генерує виняток length\_error, якщо результат перевищує максимально допустиму кількість символів.

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
std::string sString("eee");
sString.append(5, 'f');
std::cout << sString << std::endl;
}|

Результат:

`eeefffff`

Є ще одна (остання) варіація функції append(), використання якої ви не зрозумієте, якщо не знайомі з [**ітераторами**](https://acode.com.ua/urok-206-iteratory-stl/).

## string& string::append(InputIterator start, InputIterator end)

   Ця функція додає до std::string всі символи з діапазону `(start, end)`.

   Повертає прихований вказівник \*this, що дозволяє «зв’язувати» об’єкти.

   Генерує виняток length\_error, якщо результат перевищує максимально допустиму кількість символів.

На наступному уроці ми розглянемо вставку символів в std::string.

Оцінити статтю:

![1 Зірка](stdstring/rating_on.gif "1 Зірка")![2 Зірки](stdstring/rating_on.gif "2 Зірки")![3 Зірки](stdstring/rating_on.gif "3 Зірки")![4 Зірки](stdstring/rating_on.gif "4 Зірки")![5 Зірок](stdstring/rating_on.gif "5 Зірок") (**36** оцінок, середня: **4,97** з 5)

![](stdstring/loading.gif)Завантаження...