// Приведення, Convert, Parse і TryParse.
string text = "42";
int a = int.Parse(text);
int b = Convert.ToInt32(text);
Console.WriteLine($"int.Parse(\"42\") = {a}, Convert.ToInt32(\"42\") = {b}");

string? missing = null;
Console.WriteLine($"Convert.ToInt32(null) = {Convert.ToInt32(missing)}");

double x = 12.6;
Console.WriteLine($"(int)12.6 = {(int)x}, Convert.ToInt32(12.6) = {Convert.ToInt32(x)}");
Console.WriteLine($"Convert.ToInt32(true) = {Convert.ToInt32(true)}, Convert.ToBoolean(0) = {Convert.ToBoolean(0)}");
Console.WriteLine($"Convert.ToString(42, 2) = {Convert.ToString(42, 2)}, Convert.ToInt32(\"101010\", 2) = {Convert.ToInt32("101010", 2)}");

if (int.TryParse("abc", out int number))
{
    Console.WriteLine($"число: {number}");
}
else
{
    Console.WriteLine($"\"abc\" — не число, number = {number}");
}
