// продажі: 3 магазини (рядки) за 4 тижні (стовпці)
int[,] sales =
{
    { 12, 15, 9, 20 },
    { 7, 11, 14, 10 },
    { 18, 16, 21, 25 },
};

for (int shop = 0; shop < sales.GetLength(0); shop++)
{
    int total = 0;
    for (int week = 0; week < sales.GetLength(1); week++)
        total += sales[shop, week];
    Console.WriteLine($"магазин {shop}: {total}");
}

Console.Write("тижні:");
for (int week = 0; week < sales.GetLength(1); week++)
{
    int total = 0;
    for (int shop = 0; shop < sales.GetLength(0); shop++)
        total += sales[shop, week];
    Console.Write($" {total}");
}
Console.WriteLine();
