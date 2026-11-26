// Знайти a і b від 1 до 9, для яких a * b == 24 і a + b == 10.

// 1. лише break: виходить із внутрішнього циклу, зовнішній триває
int checks = 0;
for (int a = 1; a <= 9; a++)
{
    for (int b = 1; b <= 9; b++)
    {
        checks++;
        if (a * b == 24 && a + b == 10)
        {
            Console.WriteLine($"break: {a} × {b}");
            break;
        }
    }
}
Console.WriteLine($"break: перевірок {checks}");

// 2. прапорець в умові зовнішнього циклу
checks = 0;
bool found = false;
for (int a = 1; a <= 9 && !found; a++)
{
    for (int b = 1; b <= 9; b++)
    {
        checks++;
        if (a * b == 24 && a + b == 10)
        {
            Console.WriteLine($"прапорець: {a} × {b}");
            found = true;
            break;
        }
    }
}
Console.WriteLine($"прапорець: перевірок {checks}");

// 3. goto на мітку після обох циклів
checks = 0;
for (int a = 1; a <= 9; a++)
{
    for (int b = 1; b <= 9; b++)
    {
        checks++;
        if (a * b == 24 && a + b == 10)
        {
            Console.WriteLine($"goto: {a} × {b}");
            goto done;
        }
    }
}
Console.WriteLine("goto: не знайдено");
done:
Console.WriteLine($"goto: перевірок {checks}");

// 4. return з методу завершує обидва цикли
Console.WriteLine($"return: {FindPair()}");

static string FindPair()
{
    for (int a = 1; a <= 9; a++)
    {
        for (int b = 1; b <= 9; b++)
        {
            if (a * b == 24 && a + b == 10)
                return $"{a} × {b}";
        }
    }
    return "не знайдено";
}
