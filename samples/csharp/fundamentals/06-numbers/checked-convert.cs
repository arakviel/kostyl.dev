// checked для перетворення дробового в ціле: замість насичення — виняток.
double huge = 1e10;
Console.WriteLine($"unchecked((int)1e10) = {unchecked((int)huge)}");
Console.WriteLine("checked((int)1e10)...");
Console.WriteLine(checked((int)huge));
