// Префіксний і постфіксний інкремент: значення виразу і значення змінної.
int i = 5;
int post = i++;   // спочатку значення 5, потім i стає 6
Console.WriteLine($"post = {post}, i = {i}");

int j = 5;
int pre = ++j;    // спочатку j стає 6, потім значення 6
Console.WriteLine($"pre = {pre}, j = {j}");

int k = 5;
int r = k++ + ++k;   // 5 (k стає 6) + 7 (k стає 7)
Console.WriteLine($"k++ + ++k = {r}, k = {k}");

int m = 1;
m = m++;             // значення виразу m++ — 1, і воно записується назад у m
Console.WriteLine($"m = m++  ->  m = {m}");
