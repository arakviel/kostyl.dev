// 1. лічильник змінюється ще й у тілі: половину елементів пропущено
int[] data = [1, 2, 3, 4, 5, 6];
Console.Write("1:");
for (int i = 0; i < data.Length; i++)
{
    Console.Write($" {data[i]}");
    i++;   // помилка: i збільшується двічі за ітерацію
}
Console.WriteLine();

// 2. дробовий лічильник: 1.0 так і не з'являється
double x = 0;
for (int step = 1; step <= 10; step++)
{
    x += 0.1;
}
Console.WriteLine($"2: 0.1 додано 10 разів: {x:R}, x == 1.0 — {x == 1.0}");
