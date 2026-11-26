#:property CheckForOverflowUnderflow=true
// Перевірка переповнення для всієї програми; unchecked вимикає її для окремого виразу.
int max = int.MaxValue;
Console.WriteLine($"unchecked(max + 1) = {unchecked(max + 1)}");
Console.WriteLine("max + 1 без unchecked...");
Console.WriteLine(max + 1);
