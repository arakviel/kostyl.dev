// Явні перетворення (приведення): відкидання дробової частини, обрізання бітів, насичення.
double price = 3.99;
double negative = -3.99;
Console.WriteLine($"(int)3.99 = {(int)price}, (int)-3.99 = {(int)negative}");

int big = 300;
Console.WriteLine($"(byte)300 = {(byte)big}");

long three = 3_000_000_000;
Console.WriteLine($"(int)3_000_000_000L = {(int)three}");

double huge = 1e10;
double nan = double.NaN;
Console.WriteLine($"(int)1e10 = {(int)huge}, (int)NaN = {(int)nan}");

double tenth = 0.1;
float tenthF = (float)tenth;
Console.WriteLine($"(float)0.1 = {tenthF}, назад у double: {(double)tenthF}");

decimal money = 19.99m;
Console.WriteLine($"(double)19.99m = {(double)money}, (int)19.99m = {(int)money}");
