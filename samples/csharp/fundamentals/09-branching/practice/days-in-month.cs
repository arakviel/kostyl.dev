// Практика 4: кількість днів у місяці і високосний рік; перевірка через DateTime.DaysInMonth.
int[] years = [2024, 2025, 1900, 2000];
foreach (int year in years)
{
    bool leap = year % 4 == 0 && year % 100 != 0 || year % 400 == 0;
    int february = DaysIn(2, leap);
    Console.WriteLine($"{year}: високосний {leap,-5}  лютий {february}  DateTime: {DateTime.DaysInMonth(year, 2)}");
}
Console.WriteLine();
for (int month = 1; month <= 12; month++)
{
    Console.Write($"{month}:{DaysIn(month, false)} ");
}
Console.WriteLine();

static int DaysIn(int month, bool leap) => month switch
{
    2 => leap ? 29 : 28,
    4 or 6 or 9 or 11 => 30,
    >= 1 and <= 12 => 31,
    _ => throw new ArgumentOutOfRangeException(nameof(month)),
};
