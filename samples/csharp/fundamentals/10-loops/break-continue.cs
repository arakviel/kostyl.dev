int[] readings = [12, -1, 8, -5, 30, 7, 99, 4];

// continue: пропустити від'ємні значення (збої датчика)
int sum = 0;
foreach (int r in readings)
{
    if (r < 0)
        continue;
    sum += r;
}
Console.WriteLine($"сума без від'ємних: {sum}");

// break: зупинитися на першому значенні, більшому за 50
int index = -1;
for (int i = 0; i < readings.Length; i++)
{
    if (readings[i] > 50)
    {
        index = i;
        break;
    }
}
Console.WriteLine($"перше значення > 50: readings[{index}] = {readings[index]}");
