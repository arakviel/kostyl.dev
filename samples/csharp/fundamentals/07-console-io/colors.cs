// Кольори тексту і фону, повернення стандартних кольорів.
Console.ForegroundColor = ConsoleColor.Green;
Console.WriteLine("Успіх: файл збережено");
Console.ForegroundColor = ConsoleColor.Yellow;
Console.WriteLine("Увага: диск заповнено на 90%");
Console.ForegroundColor = ConsoleColor.White;
Console.BackgroundColor = ConsoleColor.Red;
Console.Write(" ПОМИЛКА ");
Console.ResetColor();
Console.WriteLine(" з'єднання розірвано");
Console.WriteLine("Звичайний текст після ResetColor");
