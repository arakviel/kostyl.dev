string[] days = ["пн", "вт", "ср", "чт", "пт", "сб", "нд"];
// 7 днів (рядки) × 3 заміри: ранок, день, вечір
int[,] temps =
{
    { 4, 11, 7 },
    { 3, 12, 8 },
    { 6, 14, 12 },
    { 8, 9, 5 },
    { 5, 13, 10 },
    { 7, 16, 11 },
    { 6, 15, 9 },
};

Console.WriteLine($"Length = {temps.Length}, GetLength(0) = {temps.GetLength(0)}, GetLength(1) = {temps.GetLength(1)}");

for (int day = 0; day < temps.GetLength(0); day++)
{
    int sum = 0;
    for (int m = 0; m < temps.GetLength(1); m++)
        sum += temps[day, m];
    Console.WriteLine($"{days[day]}: середня {sum / temps.GetLength(1)}");
}

string[] names = ["ранок", "день", "вечір"];
for (int m = 0; m < temps.GetLength(1); m++)
{
    int maxDay = 0;
    for (int day = 1; day < temps.GetLength(0); day++)
        if (temps[day, m] > temps[maxDay, m])
            maxDay = day;
    Console.WriteLine($"{names[m]}: максимум {temps[maxDay, m]} ({days[maxDay]})");
}
