using System.Globalization;

// Форматування дати й часу: стандартні і власні специфікатори (культура uk-UA).
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");
DateTime moment = new DateTime(2026, 11, 25, 14, 30, 5);

Console.WriteLine($"без формату        {moment}");
Console.WriteLine($"d                  {moment:d}");
Console.WriteLine($"D                  {moment:D}");
Console.WriteLine($"t                  {moment:t}");
Console.WriteLine($"g                  {moment:g}");
Console.WriteLine($"yyyy-MM-dd         {moment:yyyy-MM-dd}");
Console.WriteLine($"dd.MM.yyyy HH:mm   {moment:dd.MM.yyyy HH:mm}");
Console.WriteLine($"dddd, d MMMM       {moment:dddd, d MMMM}");
Console.WriteLine($"yyyy-mm-dd (помилка) {moment:yyyy-mm-dd}");
Console.WriteLine();
Console.WriteLine($"InvariantCulture, D: {moment.ToString("D", CultureInfo.InvariantCulture)}");
Console.WriteLine($"ISO 8601 (o):        {moment:o}");
