// Практика 1: максимум кожного цілого типу плюс один — без перевірки і з перевіркою.
byte b = byte.MaxValue;
short s = short.MaxValue;
int i = int.MaxValue;
long l = long.MaxValue;

Console.WriteLine($"byte   {b} + 1 = {unchecked((byte)(b + 1))}");
Console.WriteLine($"short  {s} + 1 = {unchecked((short)(s + 1))}");
Console.WriteLine($"int    {i} + 1 = {unchecked(i + 1)}");
Console.WriteLine($"long   {l} + 1 = {unchecked(l + 1)}");
Console.WriteLine();
Console.WriteLine($"int  у checked: {checked(i + 1)}");
