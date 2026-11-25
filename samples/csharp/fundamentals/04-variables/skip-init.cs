#:property AllowUnsafeBlocks=true
// Атрибут SkipLocalsInit прибирає з IL прапорець init: runtime більше не обнуляє локальні змінні.
[module: System.Runtime.CompilerServices.SkipLocalsInit]

int a = 10;
int b = 20;
Console.WriteLine(a + b);
