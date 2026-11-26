string[] commands = ["add", "add", "stop", "add"];

// break у switch завершує лише секцію switch, цикл триває
int count = 0;
foreach (string command in commands)
{
    switch (command)
    {
        case "add":
            count++;
            break;
        case "stop":
            break;
    }
}
Console.WriteLine($"break у switch: count = {count}");

// прапорець в умові циклу зупиняє цикл
count = 0;
bool running = true;
for (int i = 0; i < commands.Length && running; i++)
{
    switch (commands[i])
    {
        case "add":
            count++;
            break;
        case "stop":
            running = false;
            break;
    }
}
Console.WriteLine($"прапорець: count = {count}");
