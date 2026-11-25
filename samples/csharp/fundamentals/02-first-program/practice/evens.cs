// Практика 3: програма має порахувати парні числа від 1 до 10 включно (їх 5), але друкує 4.
int count = 0;
int last = 0;

for (int i = 1; i < 10; i++)
{
    if (i % 2 == 0)
    {
        count++;
        last = i;
    }
}

Console.WriteLine($"Парних чисел: {count}");
Console.WriteLine($"Останнє парне: {last}");
