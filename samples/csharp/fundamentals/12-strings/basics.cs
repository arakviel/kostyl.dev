string city = "Чернігів";

Console.WriteLine($"Length: {city.Length}");
Console.WriteLine($"перший символ: {city[0]}, останній: {city[city.Length - 1]}");

// перебір символів за індексом
for (int i = 0; i < city.Length; i++)
{
    Console.Write($"{i}:{city[i]} ");
}
Console.WriteLine();

// перебір через foreach і підрахунок
int count = 0;
foreach (char c in city)
{
    if (c == 'і')
        count++;
}
Console.WriteLine($"літера і трапляється {count} рази");

// рядок у масив символів і назад
char[] letters = city.ToCharArray();
Array.Reverse(letters);
string reversed = new string(letters);
Console.WriteLine($"навпаки: {reversed}");
