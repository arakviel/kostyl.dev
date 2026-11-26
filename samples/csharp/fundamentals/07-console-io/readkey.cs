// Console.ReadKey: одна клавіша без Enter.
Console.Write("Продовжити? (y/n) ");
ConsoleKeyInfo key = Console.ReadKey();
Console.WriteLine();
Console.WriteLine($"Key = {key.Key}, KeyChar = '{key.KeyChar}', Modifiers = {key.Modifiers}");

Console.Write("Пароль-цифра (не відображається): ");
ConsoleKeyInfo hidden = Console.ReadKey(intercept: true);
Console.WriteLine();
Console.WriteLine($"Ви натиснули {hidden.KeyChar}");
