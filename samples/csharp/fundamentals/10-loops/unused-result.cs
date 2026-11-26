// Поглиблений розділ: JIT викидає обчислення, результат якого не використовується.
using System.Diagnostics;

const int N = 1_000_000_000;
for (int run = 1; run <= 3; run++)
{
    var used = Stopwatch.StartNew();
    long sum = Used(N);
    used.Stop();

    var unused = Stopwatch.StartNew();
    Unused(N);
    unused.Stop();

    var empty = Stopwatch.StartNew();
    Empty(N);
    empty.Stop();

    Console.WriteLine($"запуск {run}: з результатом {used.Elapsed.TotalMilliseconds,5:F0} мс, " +
                      $"без результату {unused.Elapsed.TotalMilliseconds,5:F0} мс, " +
                      $"порожній {empty.Elapsed.TotalMilliseconds,4:F0} мс");
}

static long Used(int n)
{
    long sum = 0;
    for (int i = 0; i < n; i++)
        sum += i % 7;
    return sum;
}

static void Unused(int n)
{
    for (int i = 0; i < n; i++)
    {
        int t = i % 7;   // t ніде не використовується
    }
}

static void Empty(int n)
{
    for (int i = 0; i < n; i++)
    {
    }
}
