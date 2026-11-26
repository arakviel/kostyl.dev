// три способи перевірити числа 2..50 на простоту; checks — скільки разів обчислено n % d
int checksAll = 0, checksBreak = 0, checksSqrt = 0;
int primes = 0;
Console.Write("прості:");
for (int n = 2; n <= 50; n++)
{
    // 1. усі дільники від 2 до n - 1, без break
    bool prime = true;
    for (int d = 2; d < n; d++)
    {
        checksAll++;
        if (n % d == 0)
            prime = false;
    }

    // 2. ті самі дільники, але break на першому знайденому
    for (int d = 2; d < n; d++)
    {
        checksBreak++;
        if (n % d == 0)
            break;
    }

    // 3. break і лише дільники до кореня: d * d <= n
    for (int d = 2; d * d <= n; d++)
    {
        checksSqrt++;
        if (n % d == 0)
            break;
    }

    if (prime)
    {
        Console.Write($" {n}");
        primes++;
    }
}
Console.WriteLine();
Console.WriteLine($"простих: {primes}");
Console.WriteLine($"без break: {checksAll}, з break: {checksBreak}, з break і d * d <= n: {checksSqrt}");
