// 1. зовнішній масив з трьох посилань, кожен рядок створюється окремо
int[][] rows = new int[3][];
rows[0] = [1];
rows[1] = [2, 3];
rows[2] = new int[4];

Console.WriteLine($"rows.Length = {rows.Length}");
for (int i = 0; i < rows.Length; i++)
{
    Console.Write($"рядок {i}, Length {rows[i].Length}:");
    for (int j = 0; j < rows[i].Length; j++)
    {
        Console.Write($" {rows[i][j]}");
    }
    Console.WriteLine();
}

// 2. вираз колекції з вкладеними виразами колекцій
int[][] triangle = [[1], [1, 1], [1, 2, 1]];

// 3. new з ініціалізатором: кожен рядок — окремий new
int[][] pairs = new int[][] { new int[] { 1, 2 }, new[] { 3, 4 } };

Console.Write("triangle:");
foreach (int[] row in triangle)
{
    Console.Write($" [{string.Join(" ", row)}]");
}
Console.WriteLine();
Console.WriteLine($"pairs[1][0] = {pairs[1][0]}");
