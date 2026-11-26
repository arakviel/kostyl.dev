int full = 0;
for (int i = 1; i <= 9; i++)
{
    for (int j = 1; j <= 9; j++)
    {
        Console.Write($"{i * j,3}");
        full++;
    }
    Console.WriteLine();
}
Console.WriteLine($"повна таблиця, множень: {full}");
Console.WriteLine();

int half = 0;
for (int i = 1; i <= 9; i++)
{
    for (int j = 1; j <= i; j++)
    {
        Console.Write($"{i * j,3}");
        half++;
    }
    Console.WriteLine();
}
Console.WriteLine($"трикутник, множень: {half}");
