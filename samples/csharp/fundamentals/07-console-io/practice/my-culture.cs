using System.Globalization;

// Практика 3: як форматує ваша система (без жодного налаштування культури в коді).
double money = 1234567.891;
DateTime day = new DateTime(2026, 3, 8, 7, 5, 0);

Console.WriteLine($"Культура:          {CultureInfo.CurrentCulture.Name} ({CultureInfo.CurrentCulture.DisplayName})");
Console.WriteLine($"Число (N2):        {money:N2}");
Console.WriteLine($"Гроші (C):         {money:C}");
Console.WriteLine($"Дата (d):          {day:d}");
Console.WriteLine($"Дата (D):          {day:D}");
Console.WriteLine($"Без формату:       {day}");
Console.WriteLine($"Invariant (N2):    {money.ToString("N2", CultureInfo.InvariantCulture)}");
Console.WriteLine($"Invariant (d):     {day.ToString("d", CultureInfo.InvariantCulture)}");
