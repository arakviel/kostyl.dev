// Поглиблений розділ: Span<T> — вікно в масив без копіювання.
int[] a = [10, 20, 30, 40, 50];

Span<int> window = a.AsSpan(1, 3);   // елементи з індексами 1, 2, 3
window[0] = 999;                     // змінюється сам масив
Console.WriteLine($"window.Length = {window.Length}, a = {string.Join(", ", a)}");

Span<int> tail = a.AsSpan()[3..];    // діапазон над Span — теж вікно, не копія
tail.Fill(0);
Console.WriteLine($"після tail.Fill(0): a = {string.Join(", ", a)}");

Console.WriteLine($"Sum(a) = {Sum(a)}");                   // int[] → ReadOnlySpan<int>
Console.WriteLine($"Sum(a.AsSpan(1, 2)) = {Sum(a.AsSpan(1, 2))}");

static int Sum(ReadOnlySpan<int> items)
{
    int sum = 0;
    foreach (int item in items)
        sum += item;
    return sum;
}
