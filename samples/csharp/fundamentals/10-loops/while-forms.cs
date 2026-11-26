// 1. while: умова перевіряється перед кожним повтором
int number = 90210;
int digits = 0;
while (number > 0)
{
    number /= 10;
    digits++;
}
Console.WriteLine($"1: цифр у 90210: {digits}");

// 2. умова з кількох частин: пропустити пробіли на початку рядка
string text = "   hello";
int pos = 0;
while (pos < text.Length && text[pos] == ' ')
{
    pos++;
}
Console.WriteLine($"2: перший непробільний символ — '{text[pos]}' на позиції {pos}");

// 3. while (true): вихід лише через break
int value = 1;
while (true)
{
    value *= 3;
    if (value > 500)
        break;
}
Console.WriteLine($"3: перший степінь 3, більший за 500: {value}");

// 4. do-while: тіло виконується хоча б раз, умова — після тіла
int candidate = 49;
do
{
    candidate++;
} while (candidate % 7 != 0);
Console.WriteLine($"4: наступне після 49 кратне 7: {candidate}");
