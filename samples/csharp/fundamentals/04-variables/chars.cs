// char — 16-бітний код символу UTF-16.
char letter = 'A';
Console.WriteLine(letter + 1);          // char + int -> int
Console.WriteLine((char)(letter + 1));  // назад у char

char yi = 'Ї';
Console.WriteLine((int)yi);
Console.WriteLine('Ї');
Console.WriteLine(sizeof(char));

bool passed = true;
Console.WriteLine(passed);
Console.WriteLine(sizeof(bool));
