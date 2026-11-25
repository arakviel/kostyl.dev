// Який тип виводить компілятор для var з різними літералами.
var a = 42;
var b = 42L;
var c = 3_000_000_000;
var d = 4.5;
var e = 4.5f;
var f = 4.5m;
var g = 'Ї';
var h = "Ї";
var i = true;

Console.WriteLine($"var a = 42;            {a.GetType()}");
Console.WriteLine($"var b = 42L;           {b.GetType()}");
Console.WriteLine($"var c = 3_000_000_000; {c.GetType()}");
Console.WriteLine($"var d = 4.5;           {d.GetType()}");
Console.WriteLine($"var e = 4.5f;          {e.GetType()}");
Console.WriteLine($"var f = 4.5m;          {f.GetType()}");
Console.WriteLine($"var g = 'Ї';           {g.GetType()}");
Console.WriteLine($"var h = \"Ї\";           {h.GetType()}");
Console.WriteLine($"var i = true;          {i.GetType()}");
