// Зсуви: <<, >> (арифметичний для знакових), >>> (логічний, з C# 11), маскування кількості зсуву.
int x = 13;
Console.WriteLine($"13 << 2   = {x << 2}");
Console.WriteLine($"13 >> 2   = {x >> 2}");

int neg = -16;
Console.WriteLine($"-16       = {neg:B32}");
Console.WriteLine($"-16 >> 2  = {neg >> 2:B32}  {neg >> 2}");
Console.WriteLine($"-16 >>> 2 = {neg >>> 2:B32}  {neg >>> 2}");

uint u = 0xF000_0000;
Console.WriteLine($"uint 0xF0000000 >> 4 = 0x{u >> 4:X8}");

int one = 1;
int shift = 33;
Console.WriteLine($"1 << 33 (int)  = {one << shift}");
Console.WriteLine($"1L << 33 (long) = {1L << shift}");
