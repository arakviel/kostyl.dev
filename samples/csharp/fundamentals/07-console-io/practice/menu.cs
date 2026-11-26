// Практика 4: меню з ReadKey — дія за одним натисканням.
int counter = 0;
while (true)
{
    Console.WriteLine($"Лічильник: {counter}");
    Console.Write("[+] додати  [-] відняти  [0] скинути  [q] вийти: ");
    ConsoleKeyInfo key = Console.ReadKey(intercept: true);
    Console.WriteLine(key.KeyChar);

    if (key.KeyChar == '+')
    {
        counter++;
    }
    else if (key.KeyChar == '-')
    {
        counter--;
    }
    else if (key.KeyChar == '0')
    {
        counter = 0;
    }
    else if (key.Key == ConsoleKey.Q)
    {
        break;
    }
    else
    {
        Console.WriteLine($"Невідома клавіша: {key.Key}");
    }
}
Console.WriteLine("Бувайте!");
