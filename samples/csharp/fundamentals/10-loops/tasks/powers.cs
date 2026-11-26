int count = 0;
for (int p = 1; p < 1000; p *= 2)
{
    Console.Write($"{p} ");
    count++;
}
Console.WriteLine();
Console.WriteLine($"степенів двійки, менших за 1000: {count}");
