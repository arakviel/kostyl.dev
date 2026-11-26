// Boxing: значення копіюється в новий об'єкт у купі.
int a = 5;
object boxed = a;      // boxing: копія a в купі
a = 10;
Console.WriteLine($"a = {a}, boxed = {boxed}");

int back = (int)boxed; // unboxing: копія значення з об'єкта
Console.WriteLine(back);

object o1 = 5;
object o2 = 5;
Console.WriteLine($"o1 == o2: {o1 == o2}");
Console.WriteLine($"o1.Equals(o2): {o1.Equals(o2)}");
