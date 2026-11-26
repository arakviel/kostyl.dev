using System.Numerics;

// BigInteger: ціле без обмеження розміру (обмежене лише пам'яттю).
BigInteger factorial = 1;
for (int i = 2; i <= 30; i++)
{
    factorial *= i;
}
Console.WriteLine($"30! = {factorial}");
Console.WriteLine($"2^128 = {BigInteger.Pow(2, 128)}");
Console.WriteLine($"long.MaxValue + 1 = {(BigInteger)long.MaxValue + 1}");
