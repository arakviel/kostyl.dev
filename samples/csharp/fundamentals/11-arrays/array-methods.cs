int[] scores = [74, 92, 58, 92, 81];

Console.WriteLine($"IndexOf(92):     {Array.IndexOf(scores, 92)}");
Console.WriteLine($"LastIndexOf(92): {Array.LastIndexOf(scores, 92)}");
Console.WriteLine($"IndexOf(100):    {Array.IndexOf(scores, 100)}");
Console.WriteLine($"Contains(58):    {scores.Contains(58)}");

Array.Sort(scores);
Console.WriteLine($"Sort:    {string.Join(", ", scores)}");

Array.Reverse(scores);
Console.WriteLine($"Reverse: {string.Join(", ", scores)}");

int[] marks = new int[5];
Array.Fill(marks, 12);
Console.WriteLine($"Fill:    {string.Join(", ", marks)}");

Array.Clear(marks, 1, 2);
Console.WriteLine($"Clear:   {string.Join(", ", marks)}");

Console.WriteLine($"Min {scores.Min()}, Max {scores.Max()}, Sum {scores.Sum()}");
