// Практика 1: секунди в години, хвилини і секунди через / і %.
Console.Write("Секунд: ");
string? input = Console.ReadLine();
if (!int.TryParse(input, out int total) || total < 0)
{
    Console.WriteLine("Потрібне невід'ємне ціле число");
    return;
}

int days = total / 86_400;
int hours = total % 86_400 / 3600;
int minutes = total % 3600 / 60;
int seconds = total % 60;
Console.WriteLine($"{total} с = {days} д {hours:D2}:{minutes:D2}:{seconds:D2}");
Console.WriteLine($"перевірка: {days * 86_400 + hours * 3600 + minutes * 60 + seconds}");
