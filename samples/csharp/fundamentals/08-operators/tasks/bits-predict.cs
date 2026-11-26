// Міні-завдання: бітові операції над двома байтами.
byte p = 0b1111_0000;
byte q = 0b1010_1010;
Console.WriteLine($"p & q  = {p & q:B8}");
Console.WriteLine($"p | q  = {p | q:B8}");
Console.WriteLine($"p ^ q  = {p ^ q:B8}");
Console.WriteLine($"~q     = {(byte)~q:B8}");
Console.WriteLine($"q >> 3 = {q >> 3:B8}");
Console.WriteLine($"q << 1 = {q << 1:B9}");
