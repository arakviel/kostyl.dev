// Практика 4: безпечне введення віку.
Console.Write("Вік: ");
string? input = Console.ReadLine();

if (!int.TryParse(input, out int age))
{
    Console.WriteLine($"\"{input}\" — не ціле число");
}
else if (age < 0 || age > 150)
{
    Console.WriteLine($"{age} — поза діапазоном 0–150");
}
else
{
    Console.WriteLine($"Вік: {age}, через 10 років: {age + 10}");
}
