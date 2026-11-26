string[] inputs = ["EXIT", "Help", "save", "  help  "];
foreach (string input in inputs)
{
    string command = input.Trim();
    string answer;
    if (command.Equals("help", StringComparison.OrdinalIgnoreCase))
        answer = "довідка";
    else if (command.Equals("exit", StringComparison.OrdinalIgnoreCase))
        answer = "вихід";
    else
        answer = "невідома команда";
    Console.WriteLine($"[{input}] → {answer}");
}
