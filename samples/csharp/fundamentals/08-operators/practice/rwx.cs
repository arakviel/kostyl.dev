// Практика 3: права доступу rwx з числа 0–7 через бітові операції.
for (int mode = 0; mode <= 7; mode++)
{
    char r = (mode & 0b100) != 0 ? 'r' : '-';
    char w = (mode & 0b010) != 0 ? 'w' : '-';
    char x = (mode & 0b001) != 0 ? 'x' : '-';
    Console.WriteLine($"{mode} = {mode:B3} -> {r}{w}{x}");
}

int chmod = 0b111_101_100;   // 754 у вісімковій: власник rwx, група r-x, інші r--
Console.WriteLine($"754: власник {(chmod >> 6) & 7}, група {(chmod >> 3) & 7}, інші {chmod & 7}");
