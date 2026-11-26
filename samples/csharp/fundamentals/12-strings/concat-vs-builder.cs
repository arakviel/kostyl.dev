// Замір: склеювання += проти StringBuilder. Запускати з -c Release.
using System.Diagnostics;
using System.Text;

int[] sizes = [5_000, 10_000, 20_000, 40_000];
Concat(100);    // прогрів: перший виклик включає роботу JIT
Builder(100);

foreach (int n in sizes)
{
    long before = GC.GetAllocatedBytesForCurrentThread();
    var sw = Stopwatch.StartNew();
    string s1 = Concat(n);
    sw.Stop();
    long concatBytes = GC.GetAllocatedBytesForCurrentThread() - before;
    double concatMs = sw.Elapsed.TotalMilliseconds;

    before = GC.GetAllocatedBytesForCurrentThread();
    sw.Restart();
    string s2 = Builder(n);
    sw.Stop();
    long builderBytes = GC.GetAllocatedBytesForCurrentThread() - before;
    double builderMs = sw.Elapsed.TotalMilliseconds;

    Console.WriteLine($"n = {n,6}: += {concatMs,7:F1} мс, {concatBytes / 1_000_000.0,7:F1} МБ | " +
                      $"StringBuilder {builderMs,4:F2} мс, {builderBytes / 1_000_000.0,4:F2} МБ | однакові: {s1 == s2}");
}

static string Concat(int n)
{
    string result = "";
    for (int i = 0; i < n; i++)
        result += "x";
    return result;
}

static string Builder(int n)
{
    var sb = new StringBuilder();
    for (int i = 0; i < n; i++)
        sb.Append("x");
    return sb.ToString();
}
