int[] readings = [5, -2, 7, 0, 9, 3];
int sum = 0;
int used = 0;
foreach (int r in readings)
{
    if (r == 0)
        break;      // 0 — кінець даних
    if (r < 0)
        continue;   // від'ємні — збої, пропускаємо
    sum += r;
    used++;
}
Console.WriteLine($"сума: {sum}, використано значень: {used}");
