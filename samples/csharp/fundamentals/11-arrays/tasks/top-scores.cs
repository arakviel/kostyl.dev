int[] scores = [67, 88, 95, 72, 88, 54, 91];
int mine = 72;

Array.Sort(scores);
Array.Reverse(scores);
Console.WriteLine($"від більшого: {string.Join(", ", scores)}");

int[] top = new int[3];
Array.Copy(scores, top, 3);
Console.WriteLine($"трійка: {string.Join(", ", top)}");

Console.WriteLine($"місце бала {mine}: {Array.IndexOf(scores, mine) + 1}");
