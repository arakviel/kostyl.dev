// Міні-завдання: тип і значення результату ?:.
int a = 5;
var r1 = a > 3 ? 10 : 2.5;
var r2 = a > 3 ? 'Y' : 'N';
var r3 = a > 3 ? a / 2 : a / 2.0;
int? r4 = a > 9 ? a : null;
string r5 = a > 3 ? a > 4 ? "більше 4" : "4" : "не більше 3";
Console.WriteLine($"{r1} {r1.GetType().Name}");
Console.WriteLine($"{r2} {r2.GetType().Name}");
Console.WriteLine($"{r3} {r3.GetType().Name}");
Console.WriteLine($"[{r4}] {r4.HasValue}");
Console.WriteLine(r5);
