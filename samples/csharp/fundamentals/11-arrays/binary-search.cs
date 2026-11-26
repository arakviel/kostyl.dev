int[] sorted = [3, 8, 15, 21, 34, 42, 57, 66];
Console.WriteLine($"BinarySearch(42): {Array.BinarySearch(sorted, 42)}");
Console.WriteLine($"BinarySearch(40): {Array.BinarySearch(sorted, 40)}");

int[] unsorted = [42, 3, 66, 15, 8, 57, 21, 34];
Console.WriteLine($"невідсортований, BinarySearch(42): {Array.BinarySearch(unsorted, 42)}");
Console.WriteLine($"невідсортований, IndexOf(42):      {Array.IndexOf(unsorted, 42)}");
