// Практика 4: безпечне читання вводу з ?. ?? ??=.
Console.Write("Ім'я: ");
string? name = Console.ReadLine()?.Trim();

Console.Write("Місто: ");
string? city = Console.ReadLine()?.Trim();

if (string.IsNullOrEmpty(name))
{
    name = null;
}
name ??= "гість";
city ??= "невідоме місто";

Console.WriteLine($"{name}, {city}");
Console.WriteLine($"Літер в імені: {name.Length}, у місті: {city?.Length ?? 0}");
