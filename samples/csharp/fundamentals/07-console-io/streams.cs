// stdout і stderr: перенаправлення > забирає у файл лише звичайний вивід.
Console.WriteLine("рядок 1: звичайний вивід (stdout)");
Console.Error.WriteLine("рядок 2: повідомлення про помилку (stderr)");
Console.WriteLine($"рядок 3: stdout перенаправлено у файл? {Console.IsOutputRedirected}");
