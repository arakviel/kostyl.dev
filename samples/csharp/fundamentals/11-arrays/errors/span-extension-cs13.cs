#:property LangVersion=13
// Поглиблений розділ: C# 14 перетворює масив на span і для методів розширення.
int[] readings = [3, -1, 4, -1, 5];
Console.WriteLine($"додатних: {readings.CountPositive()}");

static class SpanExtensions
{
    public static int CountPositive(this ReadOnlySpan<int> items)
    {
        int count = 0;
        foreach (int item in items)
            if (item > 0)
                count++;
        return count;
    }
}
