// 1. лічильник угору
Console.Write("1:");
for (int i = 0; i < 5; i++)
{
    Console.Write($" {i}");
}
Console.WriteLine();

// 2. лічильник униз
Console.Write("2:");
for (int i = 5; i > 0; i--)
{
    Console.Write($" {i}");
}
Console.WriteLine();

// 3. крок, більший за одиницю
Console.Write("3:");
for (int i = 0; i <= 20; i += 5)
{
    Console.Write($" {i}");
}
Console.WriteLine();

// 4. дві змінні в заголовку: оголошення і кроки через кому
Console.Write("4:");
for (int left = 0, right = 6; left < right; left++, right--)
{
    Console.Write($" ({left},{right})");
}
Console.WriteLine();

// 5. лічильник оголошено до циклу: він видимий і після циклу
int power;
int steps = 0;
for (power = 1; power < 100; power *= 3)
{
    steps++;
}
Console.WriteLine($"5: кроків {steps}, power = {power}");

// 6. усі три частини порожні: вихід лише через break
int n = 0;
for (;;)
{
    n++;
    if (n * n > 50)
        break;
}
Console.WriteLine($"6: n = {n}");

// 7. тіло з однієї інструкції без фігурних дужок
int sum = 0;
for (int i = 1; i <= 100; i++)
    sum += i;
Console.WriteLine($"7: sum = {sum}");
