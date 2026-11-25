// Escape-послідовності в символьних і рядкових літералах.
Console.WriteLine("Ім'я\tОцінка");
Console.WriteLine("Рядок 1\nРядок 2");
Console.WriteLine("Лапки: \"так\", апостроф: \'");
Console.WriteLine("Шлях: C:\\Users\\student");
Console.WriteLine("\u0406\u0422 = ІТ");
Console.WriteLine("\e[32mзелений\e[0m і звичайний");

string wrong = "\x41BC";
string right = "\x0041BC";
Console.WriteLine($"\"\\x41BC\":   довжина {wrong.Length}, код першого символу {(int)wrong[0]:X4}");
Console.WriteLine($"\"\\x0041BC\": довжина {right.Length}, текст {right}");
