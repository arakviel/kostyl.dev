// Огляд груп операторів: по одному прикладу на групу.
int x = 10;
bool done = false;
Console.WriteLine($"арифметичні:  7 / 2 = {7 / 2}, 7 % 2 = {7 % 2}, -x = {-x}");
Console.WriteLine($"порівняння:   3 < 5 = {3 < 5}, 3 == 5 = {3 == 5}");
Console.WriteLine($"логічні:      true && false = {true && false}, !done = {!done}");
Console.WriteLine($"бітові:       6 & 3 = {6 & 3}, 1 << 4 = {1 << 4}");
x += 5;
Console.WriteLine($"присвоєння:   x += 5 -> x = {x}");
Console.WriteLine($"умовний:      x > 0 ? \"+\" : \"-\" = {(x > 0 ? "+" : "-")}");
