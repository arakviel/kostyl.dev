// Міні-завдання: привітання з ?. і ??.
Console.Write("Ім'я: ");
string? input = Console.ReadLine();
string name = input?.Trim() ?? "гість";
Console.WriteLine($"Привіт, {name}! Довжина імені: {name.Length}");
