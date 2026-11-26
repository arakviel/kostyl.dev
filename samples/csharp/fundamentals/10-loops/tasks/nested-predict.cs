Console.Write("continue:");
for (int i = 1; i <= 3; i++)
{
    for (int j = 1; j <= 3; j++)
    {
        if (j == i)
            continue;
        Console.Write($" {i}{j}");
    }
}
Console.WriteLine();

Console.Write("break:");
for (int i = 1; i <= 3; i++)
{
    for (int j = 1; j <= 3; j++)
    {
        if (j == i)
            break;
        Console.Write($" {i}{j}");
    }
}
Console.WriteLine();
