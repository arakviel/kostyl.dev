// Міні-завдання: оцінка-літера словами; кілька міток на одну секцію.
char[] grades = ['A', 'b', 'C', 'd', 'F', 'x'];
foreach (char g in grades)
{
    switch (g)
    {
        case 'A':
        case 'a':
            Console.WriteLine($"{g}: відмінно");
            break;
        case 'B':
        case 'b':
            Console.WriteLine($"{g}: добре");
            break;
        case 'C':
        case 'c':
        case 'D':
        case 'd':
            Console.WriteLine($"{g}: задовільно");
            break;
        case 'F':
        case 'f':
            Console.WriteLine($"{g}: незадовільно");
            break;
        default:
            Console.WriteLine($"{g}: невідома оцінка");
            break;
    }
}
