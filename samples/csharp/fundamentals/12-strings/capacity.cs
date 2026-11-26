using System.Text;

var sb = new StringBuilder();
int capacity = sb.Capacity;
Console.Write($"Capacity: {capacity}");
for (int i = 0; i < 200; i++)
{
    sb.Append('x');
    if (sb.Capacity != capacity)
    {
        capacity = sb.Capacity;
        Console.Write($" → {capacity} (Length {sb.Length})");
    }
}
Console.WriteLine();
