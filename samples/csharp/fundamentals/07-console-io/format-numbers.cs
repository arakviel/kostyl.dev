using System.Globalization;

// Стандартні й власні рядки формату для чисел (культура uk-UA, як на українській Windows).
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

double price = 1234.5678;
double share = 0.256;
int count = 42;
int color = 255;

Console.WriteLine($"{"формат",-12} результат");
Console.WriteLine($"{"N",-12} {price:N}");
Console.WriteLine($"{"N0",-12} {price:N0}");
Console.WriteLine($"{"F2",-12} {price:F2}");
Console.WriteLine($"{"F0",-12} {price:F0}");
Console.WriteLine($"{"C",-12} {price:C}");
Console.WriteLine($"{"E2",-12} {price:E2}");
Console.WriteLine($"{"P",-12} {share:P}");
Console.WriteLine($"{"P1",-12} {share:P1}");
Console.WriteLine($"{"D5",-12} {count:D5}");
Console.WriteLine($"{"X",-12} {color:X}");
Console.WriteLine($"{"X4",-12} {color:X4}");
Console.WriteLine($"{"B8",-12} {color:B8}");
Console.WriteLine($"{"0.00",-12} {price:0.00}");
Console.WriteLine($"{"#,0.#",-12} {price:#,0.#}");
Console.WriteLine($"{"000.0",-12} {7.25:000.0}");
Console.WriteLine();
Console.WriteLine($"InvariantCulture, N2: {price.ToString("N2", CultureInfo.InvariantCulture)}");
