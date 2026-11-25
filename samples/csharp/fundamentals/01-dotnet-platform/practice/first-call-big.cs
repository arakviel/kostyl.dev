using System.Diagnostics;

// Практика 4: чи залежить ціна JIT від обсягу роботи методу.
static long SumTo(int n)
{
    long sum = 0;
    for (int i = 1; i <= n; i++)
    {
        sum += i;
    }
    return sum;
}

Stopwatch.StartNew().Stop();

for (int call = 1; call <= 5; call++)
{
    var sw = Stopwatch.StartNew();
    long result = SumTo(1_000_000);
    sw.Stop();
    Console.WriteLine($"Виклик {call}: {sw.Elapsed.TotalMicroseconds,8:F1} мкс (результат {result})");
}
