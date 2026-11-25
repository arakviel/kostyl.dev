// Арифметика над byte і short виконується в int.
byte a = 200, b = 100;
int sum = a + b;               // byte + byte -> int
byte cut = (byte)(a + b);      // явне приведення: лишаються молодші 8 біт
Console.WriteLine(sum);
Console.WriteLine(cut);
