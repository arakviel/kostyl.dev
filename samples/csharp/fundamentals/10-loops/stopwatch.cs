// Поглиблений розділ: замір часу циклу. Порівняйте dotnet run і dotnet run -c Release.
using System.Diagnostics;

const int N = 100_000_000;
for (int run = 1; run <= 5; run++)
{
    var sw = Stopwatch.StartNew();
    long sum = Work(N);
    sw.Stop();
    Console.WriteLine($"запуск {run}: {sw.Elapsed.TotalMilliseconds,6:F1} мс, sum = {sum}");
}

static long Work(int n)
{
    long sum = 0;
    for (int i = 0; i < n; i++)
    {
        sum += i % 7;
    }
    return sum;
}
