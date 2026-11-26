// Висячий else: відступи вводять в оману, else належить найближчому if.
int a = 5, b = -1;
if (a > 0)
    if (b > 0)
        Console.WriteLine("обидва додатні");
else
    Console.WriteLine("a не додатне?");
