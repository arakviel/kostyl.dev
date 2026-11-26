// Бітові операції над двома байтами: по стовпчиках, біт за бітом.
byte a = 0b1100_1010;   // 202
byte b = 0b1010_0110;   // 166

Console.WriteLine($"a      = {a:B8}  {a,4}");
Console.WriteLine($"b      = {b:B8}  {b,4}");
Console.WriteLine($"a & b  = {a & b:B8}  {a & b,4}");
Console.WriteLine($"a | b  = {a | b:B8}  {a | b,4}");
Console.WriteLine($"a ^ b  = {a ^ b:B8}  {a ^ b,4}");
Console.WriteLine($"~a     = {(byte)~a:B8}  {(byte)~a,4}");
Console.WriteLine();
Console.WriteLine($"~a без приведення: {~a} (тип {(~a).GetType().Name})");
Console.WriteLine($"a ^ b ^ b = {a ^ b ^ b}");
