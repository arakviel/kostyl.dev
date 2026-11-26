using System.Globalization;

// Практика 2: калькулятор з перевіркою введення (культура uk-UA: дробова частина через кому).
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

double a = ReadNumber("Перше число: ");
double b = ReadNumber("Друге число: ");

Console.Write("Операція (+ - * /): ");
string? op = Console.ReadLine()?.Trim();

if (op == "+")
{
    Console.WriteLine($"{a} + {b} = {a + b}");
}
else if (op == "-")
{
    Console.WriteLine($"{a} - {b} = {a - b}");
}
else if (op == "*")
{
    Console.WriteLine($"{a} * {b} = {a * b}");
}
else if (op == "/" && b != 0)
{
    Console.WriteLine($"{a} / {b} = {a / b:F4}");
}
else if (op == "/")
{
    Console.WriteLine("Ділити на нуль не можна");
}
else
{
    Console.WriteLine($"Невідома операція \"{op}\"");
}

static double ReadNumber(string prompt)
{
    while (true)
    {
        Console.Write(prompt);
        string? input = Console.ReadLine();
        if (input is null)
        {
            Console.WriteLine();
            Console.WriteLine("Введення закінчилося, беру 0");
            return 0;
        }
        if (double.TryParse(input, out double value))
        {
            return value;
        }
        Console.WriteLine($"\"{input}\" — не число");
    }
}
