// switch expression: той самий вибір, що й у switch statement, але як вираз.
for (int day = 1; day <= 8; day++)
{
    string kind = day switch
    {
        1 or 2 or 3 or 4 or 5 => "робочий день",
        6 or 7 => "вихідний",
        _ => "такого дня немає",
    };
    Console.WriteLine($"{day}: {kind}");
}
Console.WriteLine();

string[] commands = ["start", "stop", "STOP", "help"];
foreach (string command in commands)
{
    Console.WriteLine($"{command}: {Reply(command)}");
}

static string Reply(string command) => command.ToLowerInvariant() switch
{
    "start" => "запускаю",
    "stop" => "зупиняю",
    _ => "невідома команда",
};
