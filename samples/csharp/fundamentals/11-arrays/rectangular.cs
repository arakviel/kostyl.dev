// 1. new з розмірами: 2 рядки по 3 стовпці, усі елементи — нулі
int[,] grid = new int[2, 3];
grid[0, 0] = 1;
grid[1, 2] = 6;

// 2. new з ініціалізатором: розміри рахує компілятор
int[,] table = new int[,] { { 1, 2, 3 }, { 4, 5, 6 } };

// 3. скорочений ініціалізатор: лише в оголошенні змінної
int[,] same = { { 1, 2, 3 }, { 4, 5, 6 } };

Console.WriteLine($"grid[0, 0] = {grid[0, 0]}, grid[1, 2] = {grid[1, 2]}, grid[1, 0] = {grid[1, 0]}");
Console.WriteLine($"Rank = {table.Rank}, Length = {table.Length}");
Console.WriteLine($"GetLength(0) = {table.GetLength(0)}, GetLength(1) = {table.GetLength(1)}");

for (int row = 0; row < table.GetLength(0); row++)
{
    for (int col = 0; col < table.GetLength(1); col++)
    {
        Console.Write($"{table[row, col],3}");
    }
    Console.WriteLine();
}

Console.Write("foreach:");
foreach (int x in same)
{
    Console.Write($" {x}");
}
Console.WriteLine();

// 4. три виміри
int[,,] cube = new int[2, 3, 4];
Console.WriteLine($"int[,,]: Rank = {cube.Rank}, Length = {cube.Length}, GetLength(2) = {cube.GetLength(2)}");
