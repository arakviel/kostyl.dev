using System.Globalization;

// DateOnly, TimeOnly, TimeSpan і арифметика дат (фіксовані дати, щоб вивід не залежав від дня запуску).
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

DateOnly start = new DateOnly(2026, 9, 1);
DateOnly exam = new DateOnly(2026, 12, 22);
Console.WriteLine($"Початок семестру: {start:dd.MM.yyyy}, {start:dddd} (DayOfWeek: {start.DayOfWeek})");
Console.WriteLine($"Днів до іспиту:   {exam.DayNumber - start.DayNumber}");
Console.WriteLine($"Через 30 днів:    {start.AddDays(30):d}");

TimeOnly lesson = new TimeOnly(8, 30);
Console.WriteLine($"Пара о {lesson:HH:mm}, кінець о {lesson.AddMinutes(80):HH:mm}");

DateTime from = new DateTime(2026, 11, 25, 9, 0, 0);
DateTime to = new DateTime(2026, 11, 26, 17, 45, 30);
TimeSpan span = to - from;
Console.WriteLine($"Тривалість: {span}, годин усього: {span.TotalHours:F2}");
Console.WriteLine($"Формат: {span:d\\.hh\\:mm}");
Console.WriteLine($"DateTime.Now.Kind = {DateTime.Now.Kind}, DateTime.UtcNow.Kind = {DateTime.UtcNow.Kind}");
