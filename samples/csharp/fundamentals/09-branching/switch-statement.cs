// switch statement: кілька міток на одну секцію, default, goto case, рядки.
for (int day = 1; day <= 8; day++)
{
    switch (day)
    {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            Console.WriteLine($"{day}: робочий день");
            break;
        case 6:
        case 7:
            Console.WriteLine($"{day}: вихідний");
            break;
        default:
            Console.WriteLine($"{day}: такого дня немає");
            break;
    }
}
Console.WriteLine();

string[] commands = ["start", "restart", "STOP", "help"];
foreach (string command in commands)
{
    Console.Write($"{command}: ");
    switch (command)
    {
        case "restart":
            Console.Write("зупиняю... ");
            goto case "start";
        case "start":
            Console.WriteLine("запускаю");
            break;
        case "stop":
            Console.WriteLine("зупиняю");
            break;
        default:
            Console.WriteLine("невідома команда");
            break;
    }
}
