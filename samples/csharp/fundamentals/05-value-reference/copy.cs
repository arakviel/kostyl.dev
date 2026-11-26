using System.Text;

// Присвоєння: значущий тип копіює значення, посилальний — посилання.
int a = 5;
int b = a;          // копія значення
b = 10;
Console.WriteLine($"a = {a}, b = {b}");

int[] x = [1, 2, 3];
int[] y = x;        // копія посилання: обидві змінні ведуть до одного масиву
y[0] = 99;
Console.WriteLine($"x[0] = {x[0]}, y[0] = {y[0]}");

StringBuilder first = new("Привіт");
StringBuilder second = first;
second.Append(", світе");
Console.WriteLine($"first = {first}, second = {second}");

y = [7, 8, 9];      // y тепер веде до нового масиву, x — до старого
Console.WriteLine($"x[0] = {x[0]}, y[0] = {y[0]}");
