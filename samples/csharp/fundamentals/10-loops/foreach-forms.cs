// 1. масив, тип змінної ітерації вказано явно
int[] scores = [90, 75, 60];
int total = 0;
foreach (int score in scores)
{
    total += score;
}
Console.WriteLine($"1: сума балів {total}");

// 2. var: тип змінної виводить компілятор
string[] days = ["пн", "вт", "ср"];
Console.Write("2:");
foreach (var day in days)
{
    Console.Write($" {day}");
}
Console.WriteLine();

// 3. рядок: перебір символів char
int spaces = 0;
foreach (char c in "for while do foreach")
{
    if (c == ' ')
        spaces++;
}
Console.WriteLine($"3: пробілів {spaces}");

// 4. List<T>: список, розмір якого змінюється
List<string> cities = ["Київ", "Львів"];
cities.Add("Одеса");
Console.Write("4:");
foreach (string city in cities)
    Console.Write($" {city}");
Console.WriteLine();

// 5. послідовність чисел без масиву
Console.Write("5:");
foreach (int n in Enumerable.Range(10, 4))
{
    Console.Write($" {n}");
}
Console.WriteLine();

// 6. кортежі з розкладанням на дві змінні
(string Name, int Price)[] items = [("чай", 40), ("кава", 65)];
foreach (var (name, price) in items)
{
    Console.WriteLine($"6: {name} — {price} грн");
}
