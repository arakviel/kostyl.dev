int[] temps = [12, 15, 9, 21, 18, 9, 14];

// 1. сума і середнє
int sum = 0;
foreach (int t in temps)
{
    sum += t;
}
double average = (double)sum / temps.Length;
Console.WriteLine($"1: сума {sum}, середнє {average}");

// 2. максимум та його індекс
int maxIndex = 0;
for (int i = 1; i < temps.Length; i++)
{
    if (temps[i] > temps[maxIndex])
        maxIndex = i;
}
Console.WriteLine($"2: максимум {temps[maxIndex]} у день {maxIndex}");

// 3. лінійний пошук: перший індекс значення
int target = 9;
int found = -1;
for (int i = 0; i < temps.Length; i++)
{
    if (temps[i] == target)
    {
        found = i;
        break;
    }
}
Console.WriteLine($"3: перше {target} на індексі {found}");

// 4. підрахунок за умовою
int warm = 0;
foreach (int t in temps)
{
    if (t > average)
        warm++;
}
Console.WriteLine($"4: днів тепліше за середнє: {warm}");

// 5. розворот на місці: обмін симетричних елементів
for (int i = 0, j = temps.Length - 1; i < j; i++, j--)
{
    int tmp = temps[i];
    temps[i] = temps[j];
    temps[j] = tmp;
}
Console.WriteLine($"5: навпаки: {string.Join(", ", temps)}");
