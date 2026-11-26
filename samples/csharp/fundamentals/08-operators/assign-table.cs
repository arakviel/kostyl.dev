// Значення з таблиці складених операторів: кожен оператор застосовано до x = 12.
int x;
x = 12; x = 3; Console.WriteLine($"x = 3     -> {x}");
x = 12; x += 3; Console.WriteLine($"x += 3    -> {x}");
x = 12; x -= 3; Console.WriteLine($"x -= 3    -> {x}");
x = 12; x *= 3; Console.WriteLine($"x *= 3    -> {x}");
x = 12; x /= 5; Console.WriteLine($"x /= 5    -> {x}");
x = 12; x %= 5; Console.WriteLine($"x %= 5    -> {x}");
x = 12; x |= 1; Console.WriteLine($"x |= 1    -> {x}");
x = 12; x <<= 1; Console.WriteLine($"x <<= 1   -> {x}");
