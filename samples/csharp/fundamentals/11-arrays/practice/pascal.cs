const int Rows = 8;
int[][] triangle = new int[Rows][];
for (int i = 0; i < Rows; i++)
{
    triangle[i] = new int[i + 1];
    triangle[i][0] = 1;
    triangle[i][i] = 1;
    for (int j = 1; j < i; j++)
    {
        triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
    }
}

int elements = 0;
foreach (int[] row in triangle)
{
    Console.WriteLine(string.Join(" ", row));
    elements += row.Length;
}
Console.WriteLine($"елементів: {elements}, у прямокутному {Rows} × {Rows}: {Rows * Rows}");
