// Практика 4: порядок обчислення і групування в одному виразі.
int result = T("a", 2) + T("b", 3) * T("c", 4) - T("d", 5) / T("e", 1);
Console.WriteLine();
Console.WriteLine($"result = {result}");

bool flag = T("f", 0) > 1 && T("g", 2) > 1 || T("h", 3) > 1;
Console.WriteLine();
Console.WriteLine($"flag = {flag}");

static int T(string name, int value)
{
    Console.Write($"{name}={value} ");
    return value;
}
