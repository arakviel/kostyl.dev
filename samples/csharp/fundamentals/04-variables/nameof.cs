// nameof повертає ім'я змінної, типу чи методу рядком; обчислюється під час компіляції.
int userAge = -5;
if (userAge < 0)
{
    Console.WriteLine($"Помилка: {nameof(userAge)} = {userAge}, очікується число >= 0");
}

Console.WriteLine(nameof(Console.WriteLine));
Console.WriteLine(nameof(System.Int32));
Console.WriteLine(nameof(userAge.ToString));
