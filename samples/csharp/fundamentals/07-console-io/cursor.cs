// Позиція курсора: прогрес в одному рядку через SetCursorPosition.
Console.Write("Завантаження: ");
(int left, int top) = Console.GetCursorPosition();
for (int percent = 0; percent <= 100; percent += 25)
{
    Console.SetCursorPosition(left, top);
    Console.Write($"{percent,3}%");
    Thread.Sleep(200);
}
Console.WriteLine();
Console.WriteLine("Готово");
