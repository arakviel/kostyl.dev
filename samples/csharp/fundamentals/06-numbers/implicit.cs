// Неявні перетворення: компілятор дозволяє їх без приведення, але деякі втрачають точність.
int i = 123_456_789;
long l = i;          // без втрат
double d = i;        // без втрат: double точно зберігає будь-який int
float f = i;         // дозволено неявно, але float має лише 24 біти мантиси
Console.WriteLine($"int {i} -> long {l}, double {d}, float {f:F0}");

long big = 9_007_199_254_740_993;
double bd = big;     // double має 53 біти мантиси
Console.WriteLine($"long {big} -> double {bd:F0}");

char c = 'A';
int code = c;
decimal money = i;
Console.WriteLine($"char 'A' -> int {code}; int -> decimal {money}");
