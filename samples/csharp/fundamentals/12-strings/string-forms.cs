// 1. літерал (звичайний, verbatim, raw — лекція 04)
string literal = "Київ";
string path = @"C:\Docs\звіт.txt";
string raw = """Він сказав: "Так".""";

// 2. інтерполяція (лекція 07)
int year = 2026;
string interpolated = $"Рік {year}";

// 3. повторення символу
string line = new string('-', 12);

// 4. з масиву символів: увесь масив або частина
char[] chars = ['р', 'я', 'д', 'о', 'к'];
string fromChars = new string(chars);
string fromPart = new string(chars, 1, 3);

// 5. склеювання елементів масиву через роздільник
string[] parts = ["Київ", "Львів", "Одеса"];
string joined = string.Join(" | ", parts);

// 6. склеювання без роздільника
string concat = string.Concat("ab", "cd", "ef");

// 7. з іншого значення
string fromNumber = 3.ToString() + 14.ToString();

// 8. порожній рядок
string empty = string.Empty;

Console.WriteLine(literal);
Console.WriteLine(path);
Console.WriteLine(raw);
Console.WriteLine(interpolated);
Console.WriteLine(line);
Console.WriteLine($"{fromChars}, {fromPart}");
Console.WriteLine(joined);
Console.WriteLine(concat);
Console.WriteLine(fromNumber);
Console.WriteLine($"empty: Length {empty.Length}, empty == \"\": {empty == ""}");
