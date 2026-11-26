int[] a = [1, 2, 3];
int[] b = a;
int[] c = (int[])a.Clone();

b[0] = 10;
c[1] = 20;
Twice(a);
Array.Resize(ref b, 4);
b[2] = 30;

Console.WriteLine($"a: {string.Join(", ", a)}");
Console.WriteLine($"b: {string.Join(", ", b)}");
Console.WriteLine($"c: {string.Join(", ", c)}");

static void Twice(int[] items)
{
    for (int i = 0; i < items.Length; i++)
        items[i] *= 2;
}
