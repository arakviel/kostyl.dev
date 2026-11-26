// Присвоєння — вираз; складені оператори містять приховане приведення до типу змінної.
int a, b, c;
a = b = c = 5;
Console.WriteLine($"a = {a}, b = {b}, c = {c}");

int total = 10;
total += 5;
total *= 2;
total -= 3;
total /= 4;
total %= 4;
Console.WriteLine($"total = {total}");

byte level = 250;
level += 5;          // компілюється: це (byte)(level + 5)
Console.WriteLine($"level += 5   -> {level}");
level += 10;         // 255 + 10 = 265 не влазить у byte: лишаються молодші 8 біт
Console.WriteLine($"level += 10  -> {level}");

int flags = 0b0001;
flags |= 0b0100;
flags <<= 1;
Console.WriteLine($"flags = {flags:B4}");

string? title = null;
title ??= "Без назви";
Console.WriteLine(title);
