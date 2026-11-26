// Умовний оператор ?: — тип результату, target-typed, правоасоціативність.
int n = 7;
string parity = n % 2 == 0 ? "парне" : "непарне";
Console.WriteLine($"{n} — {parity}");

int a = 3, b = 8;
int max = a > b ? a : b;
Console.WriteLine($"max = {max}");

double ratio = n > 5 ? 1 : 0.5;   // int і double: тип результату double
Console.WriteLine($"ratio = {ratio} ({ratio.GetType().Name})");

int? maybe = n > 5 ? n : null;    // target-typed: тип бере зі змінної зліва
Console.WriteLine($"maybe = {maybe}");

object any = n > 5 ? n : "мало";  // теж target-typed: int і string зводяться до object
Console.WriteLine($"any = {any} ({any.GetType().Name})");

int t = 25;
string weather = t < 0 ? "мороз" : t < 15 ? "холодно" : t < 25 ? "тепло" : "спека";
Console.WriteLine($"{t}° — {weather}");
