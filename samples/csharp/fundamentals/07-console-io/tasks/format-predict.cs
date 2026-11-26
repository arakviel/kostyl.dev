using System.Globalization;

// Міні-завдання: передбачте результат кожного формату (культура uk-UA).
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

Console.WriteLine($"{0.075:P1}");
Console.WriteLine($"{1234567:N0}");
Console.WriteLine($"{255:X2}");
Console.WriteLine($"{3.14159:F3}");
Console.WriteLine($"{42:D4}");
Console.WriteLine($"{2.5:F0}");
Console.WriteLine($"{-7.25:0.0}");
