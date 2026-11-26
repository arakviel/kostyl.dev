// checked не стосується double, а decimal перевіряє переповнення завжди.
double d = double.MaxValue;
double dd = checked(d * 2);
Console.WriteLine($"checked(double.MaxValue * 2) = {dd}");

decimal m = decimal.MaxValue;
Console.WriteLine("unchecked(decimal.MaxValue + 1)...");
decimal mm = unchecked(m + 1);
Console.WriteLine(mm);
