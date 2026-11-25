// Область видимості: змінна живе до кінця свого блоку, у сусідньому блоці ім'я можна повторити.
int total = 0;
for (int i = 1; i <= 2; i++)
{
    int square = i * i;
    total += square;
}
{
    int square = 100;
    Console.WriteLine(square);
}
Console.WriteLine(total);
