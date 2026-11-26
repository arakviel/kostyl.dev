// Практика 2: до якого n факторіал поміщається в long і decimal (checked зупиняє програму на першому переповненні).
long asLong = 1;
decimal asDecimal = 1;
double asDouble = 1;
for (int n = 1; n <= 30; n++)
{
    asDouble *= n;
    asDecimal *= n;                       // decimal перевіряє переповнення завжди
    if (n <= 20)
    {
        asLong = checked(asLong * n);
    }
    Console.WriteLine($"{n,2}! long: {(n <= 20 ? asLong.ToString() : "-"),20}  decimal: {asDecimal,31}  double: {asDouble:E3}");
}
