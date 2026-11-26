int[] temps = [12, 15, 9, 21, 18];
Console.WriteLine($"Length: {temps.Length}");
Console.WriteLine($"перший: temps[0] = {temps[0]}");
Console.WriteLine($"останній: temps[temps.Length - 1] = {temps[temps.Length - 1]}");

temps[2] = 10;
Console.WriteLine($"після temps[2] = 10: {string.Join(", ", temps)}");

int day = 5;
Console.WriteLine($"temps[{day}] = {temps[day]}");
