// Переповнення цілих: за замовчуванням значення «обертається по колу» без помилки.
int max = int.MaxValue;
int next = max + 1;
Console.WriteLine($"{max} + 1 = {next}");
Console.WriteLine($"{max:B32}");
Console.WriteLine($"{next:B32}");

byte b = 255;
b++;
Console.WriteLine($"byte 255 + 1 = {b}");

long big = long.MaxValue;
big++;
Console.WriteLine($"long.MaxValue + 1 = {big}");

int min = int.MinValue;
Console.WriteLine($"-int.MinValue = {-min}");

int a = 2_000_000_000, c = 2_000_000_000;
long total = a + c;          // додавання в int, переповнення ще до запису в long
long right = (long)a + c;    // додавання в long
Console.WriteLine($"long total = a + c: {total}; (long)a + c: {right}");
