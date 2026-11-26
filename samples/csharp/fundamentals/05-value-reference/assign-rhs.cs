// C# 14: права частина присвоєння через ?[] не обчислюється, якщо зліва null.
int[]? scores = null;
scores?[0] = Next();      // Next() не викликається
scores = new int[1];
scores?[0] = Next();      // Next() викликається
Console.WriteLine(scores?[0]);

static int Next()
{
    Console.WriteLine("Next() викликано");
    return 42;
}
