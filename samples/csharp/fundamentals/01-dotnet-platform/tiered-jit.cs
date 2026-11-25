using System.Diagnostics;

static long SumTo(int n)
{
    long sum = 0;
    for (int i = 1; i <= n; i++)
    {
        sum += i;
    }
    return sum;
}

Stopwatch.StartNew().Stop(); // прогрів самого Stopwatch, щоб він не потрапив у замір

for (int call = 1; call <= 5; call++)
{
    var sw = Stopwatch.StartNew();
    long result = SumTo(1_000);
    sw.Stop();
    Console.WriteLine($"Виклик {call}: {sw.Elapsed.TotalMicroseconds,8:F1} мкс (результат {result})");
}
