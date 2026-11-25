Console.Write("Ваше ім'я: ");
string? name = Console.ReadLine();

if (name != null)
{
    Console.WriteLine($"Довжина: {name.Length}");
}
else
{
    Console.WriteLine("Введення закінчилося, ім'я не отримано.");
}
