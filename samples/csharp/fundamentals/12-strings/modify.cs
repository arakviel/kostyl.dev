string phone = "050-123-45-67";
Console.WriteLine($"Replace('-', ' '):     {phone.Replace('-', ' ')}");
Console.WriteLine($"Replace(\"-\", \"\"):      {phone.Replace("-", "")}");
Console.WriteLine($"Insert(0, \"+38\"):      {phone.Insert(0, "+38")}");
Console.WriteLine($"Remove(3):             {phone.Remove(3)}");
Console.WriteLine($"Remove(3, 4):          {phone.Remove(3, 4)}");

string name = "Олена Коваль";
Console.WriteLine($"ToUpper():             {name.ToUpper()}");
Console.WriteLine($"ToLower():             {name.ToLower()}");

Console.WriteLine($"[{"7".PadLeft(3, '0')}] [{"кава".PadRight(8)}] [{"кава".PadLeft(8, '.')}]");

// ланцюжок: кожен метод повертає новий рядок, і наступний викликається на ньому
string input = "  НОВИЙ   звіт  ";
string result = input.Trim().ToLower().Replace("  ", " ").Replace("  ", " ");
Console.WriteLine($"ланцюжок: [{result}]");
Console.WriteLine($"input не змінився: [{input}]");
