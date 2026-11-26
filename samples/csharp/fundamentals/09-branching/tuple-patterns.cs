// Кортежні шаблони: вибір за кількома значеннями одночасно.
for (int n = 1; n <= 15; n++)
{
    string text = (n % 3, n % 5) switch
    {
        (0, 0) => "FizzBuzz",
        (0, _) => "Fizz",
        (_, 0) => "Buzz",
        _ => n.ToString(),
    };
    Console.Write(text + " ");
}
Console.WriteLine();
Console.WriteLine();

(int x, int y)[] points = [(3, 4), (-2, 5), (0, 7), (0, 0), (6, -1)];
foreach (var (x, y) in points)
{
    string where = (x, y) switch
    {
        (0, 0) => "початок координат",
        (0, _) => "на осі Y",
        (_, 0) => "на осі X",
        (> 0, > 0) => "I чверть",
        (< 0, > 0) => "II чверть",
        (< 0, < 0) => "III чверть",
        (> 0, < 0) => "IV чверть",
    };
    Console.WriteLine($"({x,2}, {y,2}): {where}");
}
