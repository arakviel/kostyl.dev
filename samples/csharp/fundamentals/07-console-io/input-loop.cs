// Цикл введення: питати, доки користувач не введе коректне число.
int age;
while (true)
{
    Console.Write("Вік (0–150): ");
    string? input = Console.ReadLine();
    if (input is null)
    {
        Console.WriteLine();
        Console.WriteLine("Введення закінчилося.");
        return;
    }
    if (int.TryParse(input, out age) && age >= 0 && age <= 150)
    {
        break;
    }
    Console.WriteLine($"\"{input}\" — не підходить, спробуйте ще раз.");
}
Console.WriteLine($"Прийнято: {age}");
