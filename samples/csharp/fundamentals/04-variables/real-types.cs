// Типи з рухомою точкою і decimal: розмір, межі, точність.
Console.WriteLine($"float   {sizeof(float),2} Б  max {float.MaxValue}");
Console.WriteLine($"double  {sizeof(double),2} Б  max {double.MaxValue}");
Console.WriteLine($"decimal {sizeof(decimal),2} Б  max {decimal.MaxValue}");
Console.WriteLine();

float f = 16_777_217;
Console.WriteLine($"float f = 16_777_217  ->  {f}");

double d = 0.1 + 0.2;
Console.WriteLine($"double:  0.1 + 0.2 = {d}, дорівнює 0.3? {d == 0.3}");

decimal m = 0.1m + 0.2m;
Console.WriteLine($"decimal: 0.1 + 0.2 = {m}, дорівнює 0.3? {m == 0.3m}");
