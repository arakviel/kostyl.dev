// Арифметичні оператори: ціле ділення, остача з від'ємними числами, дробове ділення, рядки.
int a = 7, b = 2;
Console.WriteLine($" 7 / 2 = {a / b},   7 % 2 = {a % b}");
Console.WriteLine($"-7 / 2 = {-a / b},  -7 % 2 = {-a % b}");
Console.WriteLine($" 7 / -2 = {a / -b},  7 % -2 = {a % -b}");
Console.WriteLine($" 7 / 2.0 = {a / 2.0}, (double)7 / 2 = {(double)a / b}");
Console.WriteLine($" 5.5 % 2 = {5.5 % 2},  -5.5 % 2 = {-5.5 % 2}");
Console.WriteLine($" (7 / 2) * 2 + 7 % 2 = {(a / b) * b + a % b}");
Console.WriteLine();

int sum = 18, count = 4;
double wrong = sum / count;
double right = (double)sum / count;
Console.WriteLine($"середнє: sum / count = {wrong}, (double)sum / count = {right}");
Console.WriteLine();

Console.WriteLine("1" + 2 + 3);
Console.WriteLine(1 + 2 + "3");
Console.WriteLine($"2 ^ 3 = {2 ^ 3}, Math.Pow(2, 3) = {Math.Pow(2, 3)}");
