using System.Diagnostics;

#if DEBUG
Console.WriteLine("Конфігурація: Debug");
#else
Console.WriteLine("Конфігурація: Release");
#endif

static long SumTo(int n)
{
    long sum = 0;
    for (int i = 1; i <= n; i++)
    {
        sum += i;
    }
    return sum;
}

SumTo(1_000); // перший виклик з JIT — не міряємо

var sw = Stopwatch.StartNew();
long result = SumTo(100_000_000);
sw.Stop();
Console.WriteLine($"Результат: {result}");
Console.WriteLine($"Час: {sw.ElapsedMilliseconds} мс");
