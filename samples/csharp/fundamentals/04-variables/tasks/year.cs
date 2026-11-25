// Міні-завдання: одне число в трьох системах числення.
int dec = 2026;
int hex = 0x7EA;
int bin = 0b111_1110_1010;

Console.WriteLine($"{dec} {hex} {bin}");
Console.WriteLine(dec == hex && hex == bin);
Console.WriteLine($"{dec:X} {Convert.ToString(dec, 2)}");
