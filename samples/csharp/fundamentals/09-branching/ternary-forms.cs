// Де записують ?: — присвоєння, аргумент методу, return, інтерполяція.
int count = 1;
string word = count == 1 ? "файл" : "файли";
Console.WriteLine(word);
Console.WriteLine(count > 0 ? "є файли" : "порожньо");
Console.WriteLine($"знайдено {count} {(count == 1 ? "файл" : "файли")}");
Console.WriteLine(Sign(-7));

static string Sign(int n)
{
    return n < 0 ? "мінус" : "плюс";
}
