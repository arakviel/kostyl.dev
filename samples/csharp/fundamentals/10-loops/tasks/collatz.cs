int n = 27;
int steps = 0;
int max = n;
while (n != 1)
{
    if (n % 2 == 0)
        n /= 2;
    else
        n = 3 * n + 1;
    steps++;
    if (n > max)
        max = n;
}
Console.WriteLine($"кроків: {steps}, найбільше значення: {max}");
