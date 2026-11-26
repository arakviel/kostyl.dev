using System.Text;

// Кодування консолі: що друкує програма і як увімкнути UTF-8 явно.
Console.WriteLine($"OutputEncoding: {Console.OutputEncoding.WebName}");
Console.WriteLine($"InputEncoding:  {Console.InputEncoding.WebName}");
Console.OutputEncoding = Encoding.UTF8;
Console.InputEncoding = Encoding.UTF8;
Console.WriteLine("Ґанок, їжак, Євген — кирилиця в UTF-8");
