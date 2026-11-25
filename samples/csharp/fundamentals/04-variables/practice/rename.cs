// Практика 4: перейменуйте studentCount засобами IDE і порівняйте два повідомлення.
int studentCount = -1;
if (studentCount < 0)
{
    Console.WriteLine("Помилка: studentCount має бути >= 0");
    Console.WriteLine($"Помилка: {nameof(studentCount)} має бути >= 0");
}
