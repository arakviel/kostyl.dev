// Пріоритет визначає групування, а операнди обчислюються завжди зліва направо.
int result = F(1) + F(2) * F(3);
Console.WriteLine($"F(1) + F(2) * F(3) = {result}");

int[] data = [10, 20, 30];
int i = 0;
data[i] = i = 2;      // індекс обчислено першим (0), потім i = 2, потім data[0] = 2
Console.WriteLine($"data = [{string.Join(", ", data)}], i = {i}");

static int F(int n)
{
    Console.WriteLine($"  обчислюю F({n})");
    return n;
}
