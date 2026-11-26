// IEEE 754: біти double, точне значення 0.1, нескінченність, NaN, від'ємний нуль, порівняння з допуском.
double x = 0.1;
long bits = BitConverter.DoubleToInt64Bits(x);
Console.WriteLine($"біти 0.1: {bits:B64}");
Console.WriteLine($"0.1 насправді: {x:F25}");

double sum = 0;
for (int i = 0; i < 10; i++)
{
    sum += 0.1;
}
Console.WriteLine($"0.1 десять разів: {sum}, == 1.0? {sum == 1.0}");
Console.WriteLine($"різниця: {Math.Abs(sum - 1.0)}");
Console.WriteLine($"з допуском 1e-9: {Math.Abs(sum - 1.0) < 1e-9}");

double zero = 0;
Console.WriteLine($"1.0 / 0 = {1.0 / zero}, -1.0 / 0 = {-1.0 / zero}, 0.0 / 0 = {0.0 / zero}");

double nan = double.NaN;
Console.WriteLine($"NaN == NaN: {nan == nan}, double.IsNaN(NaN): {double.IsNaN(nan)}");

double negZero = -0.0;
Console.WriteLine($"-0.0 == 0.0: {negZero == 0.0}, 1 / -0.0 = {1 / negZero}");
Console.WriteLine($"double.Epsilon = {double.Epsilon}");
