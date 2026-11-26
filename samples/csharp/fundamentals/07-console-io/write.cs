// Write і WriteLine: з переходом на новий рядок і без; перевантаження для різних типів.
Console.Write("Без переходу, ");
Console.Write("той самий рядок.");
Console.WriteLine();
Console.WriteLine("З переходом.");
Console.WriteLine(42);
Console.WriteLine(true);
Console.WriteLine('Ї');

int[] marks = [5, 4, 3];
Console.WriteLine(marks);                       // масив не знає, як себе надрукувати
Console.WriteLine(string.Join(", ", marks));    // елементи через кому
