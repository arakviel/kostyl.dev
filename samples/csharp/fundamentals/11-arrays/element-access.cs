// Поглиблений розділ: як runtime звертається до елементів; дивитися через ilspycmd -il і DOTNET_JitDisasm.
using System.Runtime.CompilerServices;

int[] flat = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
int[,] grid = { { 1, 2 }, { 3, 4 } };
int[][] rows = [[1, 2], [3, 4]];
Console.WriteLine(SumLength(flat));
Console.WriteLine(SumTen(flat));
Console.WriteLine(Rect(grid));
Console.WriteLine(Jagged(rows));

// умова i < items.Length: JIT знає, що індекс у межах
[MethodImpl(MethodImplOptions.NoInlining)]
static int SumLength(int[] items)
{
    int sum = 0;
    for (int i = 0; i < items.Length; i++)
        sum += items[i];
    return sum;
}

// умова i < 10: про довжину масиву JIT нічого не знає
[MethodImpl(MethodImplOptions.NoInlining)]
static int SumTen(int[] items)
{
    int sum = 0;
    for (int i = 0; i < 10; i++)
        sum += items[i];
    return sum;
}

[MethodImpl(MethodImplOptions.NoInlining)]
static int Rect(int[,] g) => g[1, 0];

[MethodImpl(MethodImplOptions.NoInlining)]
static int Jagged(int[][] r) => r[1][0];
