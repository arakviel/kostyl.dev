// Поглиблений розділ: індекси з кінця і діапазони.
int[] a = [10, 20, 30, 40, 50];

Console.WriteLine($"a[^1] = {a[^1]}, a[^2] = {a[^2]}");
Console.WriteLine($"a[1..3]  = {string.Join(", ", a[1..3])}");
Console.WriteLine($"a[..2]   = {string.Join(", ", a[..2])}");
Console.WriteLine($"a[3..]   = {string.Join(", ", a[3..])}");
Console.WriteLine($"a[1..^1] = {string.Join(", ", a[1..^1])}");

// діапазон над масивом створює новий масив
int[] middle = a[1..^1];
middle[0] = 999;
Console.WriteLine($"middle = {string.Join(", ", middle)}; a = {string.Join(", ", a)}");

// Index і Range — звичайні значення, їх можна зберігати в змінних
Index last = ^1;
Range firstTwo = ..2;
Console.WriteLine($"a[last] = {a[last]}, a[firstTwo] = {string.Join(", ", a[firstTwo])}");
