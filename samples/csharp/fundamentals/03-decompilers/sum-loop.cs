// Цикл із локальними змінними: на ньому лекція читає IL (stloc, ldloc, переходи).
Console.WriteLine(SumTo(3));

static int SumTo(int n)
{
    int sum = 0;
    for (int i = 1; i <= n; i++)
    {
        sum += i;
    }
    return sum;
}
