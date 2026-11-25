// Міні-завдання: який тип виведе компілятор.
var a = 7 / 2;
var b = 7 / 2.0;
var c = 'a' + 1;
var d = 10_000_000_000;
var e = 1.5f * 2;

Console.WriteLine($"a = {a}, {a.GetType().Name}");
Console.WriteLine($"b = {b}, {b.GetType().Name}");
Console.WriteLine($"c = {c}, {c.GetType().Name}");
Console.WriteLine($"d = {d}, {d.GetType().Name}");
Console.WriteLine($"e = {e}, {e.GetType().Name}");
