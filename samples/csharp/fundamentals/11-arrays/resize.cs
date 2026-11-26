int[] a = [1, 2, 3];
int[] b = a;

Array.Resize(ref a, 5);
a[0] = 100;

Console.WriteLine($"a: {string.Join(", ", a)} (Length {a.Length})");
Console.WriteLine($"b: {string.Join(", ", b)} (Length {b.Length})");
Console.WriteLine($"a і b ведуть до одного масиву: {ReferenceEquals(a, b)}");
