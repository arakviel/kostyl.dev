int[][] original = [[1, 2], [3, 4]];
int[][] copy = (int[][])original.Clone();

copy[0][0] = 100;   // внутрішній масив спільний для обох
copy[1] = [7, 7];   // новий рядок лише в копії

Console.WriteLine($"original: [{string.Join(", ", original[0])}] [{string.Join(", ", original[1])}]");
Console.WriteLine($"copy:     [{string.Join(", ", copy[0])}] [{string.Join(", ", copy[1])}]");
