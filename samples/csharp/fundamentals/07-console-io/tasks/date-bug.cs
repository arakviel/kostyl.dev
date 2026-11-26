using System.Globalization;

// Міні-завдання: знайдіть помилку у форматі дати.
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");
DateTime deadline = new DateTime(2026, 12, 22, 9, 15, 0);

Console.WriteLine($"Здати до {deadline:dd.mm.yyyy hh:MM}");
Console.WriteLine($"Здати до {deadline:dd.MM.yyyy HH:mm}");
Console.WriteLine($"Здати до {deadline:dddd, d MMMM yyyy}");
