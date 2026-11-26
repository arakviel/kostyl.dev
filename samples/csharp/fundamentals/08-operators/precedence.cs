// Пріоритет і асоціативність.
Console.WriteLine($"2 + 3 * 4      = {2 + 3 * 4}");
Console.WriteLine($"(2 + 3) * 4    = {(2 + 3) * 4}");
Console.WriteLine($"10 - 4 - 3     = {10 - 4 - 3}");
Console.WriteLine($"2 * 3 % 4      = {2 * 3 % 4}");
Console.WriteLine($"1 + 2 << 1     = {1 + 2 << 1}");
Console.WriteLine($"5 > 3 == true  = {5 > 3 == true}");
Console.WriteLine($"6 & 3 | 8      = {(6 & 3 | 8)}");

int x = 6;
bool isEven = (x & 1) == 0;
Console.WriteLine($"(x & 1) == 0   = {isEven}");
