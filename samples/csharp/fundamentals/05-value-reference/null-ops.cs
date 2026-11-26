// Оператори для null: ?. ?[] ?? ??=
string? name = null;
string? city = "Київ";
int[]? scores = null;

Console.WriteLine($"[{name?.Length}]");
Console.WriteLine($"[{city?.Length}]");

int length = name?.Length ?? 0;
Console.WriteLine(length);

Console.WriteLine(scores?[0] ?? -1);

string display = name ?? "гість";
Console.WriteLine(display);

name ??= "Олена";
name ??= "Петро";
Console.WriteLine(name);

Console.WriteLine(city?.ToUpper().Length);
