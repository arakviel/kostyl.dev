// Поглиблений розділ: розбір дати без проміжних рядків через ReadOnlySpan<char>.
string date = "2026-11-26";
Parse(date);    // прогрів
ParseSpan(date);

long before = GC.GetAllocatedBytesForCurrentThread();
for (int i = 0; i < 1000; i++)
    Parse(date);
long substringBytes = GC.GetAllocatedBytesForCurrentThread() - before;

before = GC.GetAllocatedBytesForCurrentThread();
for (int i = 0; i < 1000; i++)
    ParseSpan(date);
long spanBytes = GC.GetAllocatedBytesForCurrentThread() - before;

Console.WriteLine($"Parse:     {Parse(date)}, 1000 разів: {substringBytes} Б");
Console.WriteLine($"ParseSpan: {ParseSpan(date)}, 1000 разів: {spanBytes} Б");

static (int, int, int) Parse(string s)
{
    int year = int.Parse(s.Substring(0, 4));     // Substring створює новий рядок
    int month = int.Parse(s.Substring(5, 2));
    int day = int.Parse(s.Substring(8, 2));
    return (year, month, day);
}

static (int, int, int) ParseSpan(string s)
{
    ReadOnlySpan<char> span = s.AsSpan();
    int year = int.Parse(span[..4]);              // вікно в той самий рядок
    int month = int.Parse(span.Slice(5, 2));
    int day = int.Parse(span[8..]);
    return (year, month, day);
}
