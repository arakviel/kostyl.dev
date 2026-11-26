// Шаблони в мітках case: відношення, логічні, when.
int[] amounts = [-5, 0, 42, 7, 250];
foreach (int amount in amounts)
{
    switch (amount)
    {
        case < 0:
            Console.WriteLine($"{amount}: помилка");
            break;
        case 0:
            Console.WriteLine($"{amount}: нуль");
            break;
        case > 100:
            Console.WriteLine($"{amount}: велика сума");
            break;
        case var x when x % 2 == 0:
            Console.WriteLine($"{amount}: парна");
            break;
        default:
            Console.WriteLine($"{amount}: непарна");
            break;
    }
}
