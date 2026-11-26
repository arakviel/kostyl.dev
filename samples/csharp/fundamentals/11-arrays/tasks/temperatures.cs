int[] temps = [-3, 2, -7, 0, 5, -1, 4];

int min = temps[0];
int frosty = 0;
int sum = 0;
foreach (int t in temps)
{
    if (t < min)
        min = t;
    if (t < 0)
        frosty++;
    sum += t;
}
Console.WriteLine($"мінімум {min}, днів з морозом {frosty}, сума {sum}");
