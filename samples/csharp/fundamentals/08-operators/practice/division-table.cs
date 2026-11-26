// Практика 2: ціле ділення і остача для всіх комбінацій знаків, перевірка тотожності.
int[] dividends = [17, -17];
int[] divisors = [5, -5];
Console.WriteLine("   a    b   a / b   a % b   (a / b) * b + a % b   Math.DivRem");
foreach (int a in dividends)
{
    foreach (int b in divisors)
    {
        (int q, int r) = Math.DivRem(a, b);
        Console.WriteLine($"{a,4} {b,4} {a / b,7} {a % b,7} {(a / b) * b + a % b,21}   ({q}, {r})");
    }
}
Console.WriteLine($"Math.Floor(-17 / 5.0) = {Math.Floor(-17 / 5.0)}");
