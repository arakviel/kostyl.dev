// 1. new з розміром: елементи отримують значення за замовчуванням
int[] zeros = new int[3];

// 2. new з ініціалізатором: розмір рахує компілятор
int[] primes = new int[] { 2, 3, 5, 7 };

// 3. new з розміром і ініціалізатором: кількості мають збігатися
int[] three = new int[3] { 10, 20, 30 };

// 4. скорочений ініціалізатор: лише в оголошенні змінної
string[] days = { "пн", "вт", "ср" };

// 5. вираз колекції (C# 12)
int[] odds = [1, 3, 5, 7, 9];

// 6. new[]: тип елементів виводить компілятор
var letters = new[] { 'a', 'b', 'c' };

// 7. порожній масив
int[] empty = [];

// 8. розмір зі змінної: відомий лише під час роботи програми
int n = 4;
int[] squares = new int[n];
for (int i = 0; i < n; i++)
{
    squares[i] = i * i;
}

Console.WriteLine($"1: Length {zeros.Length}: {string.Join(", ", zeros)}");
Console.WriteLine($"2: Length {primes.Length}: {string.Join(", ", primes)}");
Console.WriteLine($"3: Length {three.Length}: {string.Join(", ", three)}");
Console.WriteLine($"4: Length {days.Length}: {string.Join(", ", days)}");
Console.WriteLine($"5: Length {odds.Length}: {string.Join(", ", odds)}");
Console.WriteLine($"6: {letters.GetType().Name}, Length {letters.Length}: {string.Join(", ", letters)}");
Console.WriteLine($"7: Length {empty.Length}");
Console.WriteLine($"8: Length {squares.Length}: {string.Join(", ", squares)}");
