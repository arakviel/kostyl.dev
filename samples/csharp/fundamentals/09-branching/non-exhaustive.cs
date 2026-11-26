// Неповний switch expression: попередження CS8509 і виняток під час роботи.
int[] values = [1, 2, 3];
foreach (int v in values)
{
    string name = v switch
    {
        1 => "один",
        2 => "два",
    };
    Console.WriteLine(name);
}
