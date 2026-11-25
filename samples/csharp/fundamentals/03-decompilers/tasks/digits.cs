Console.WriteLine(CountDigits(2026));

static int CountDigits(int value)
{
    int count = 0;
    while (value > 0)
    {
        value /= 10;
        count++;
    }
    return count;
}
