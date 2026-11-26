// Міні-завдання: які виклики Log відбудуться.
bool r1 = Log("A", false) && Log("B", true);
bool r2 = Log("C", true) || Log("D", false);
bool r3 = Log("E", false) | Log("F", true);
bool r4 = Log("G", true) && Log("H", false) || Log("I", true);
Console.WriteLine($"{r1} {r2} {r3} {r4}");

static bool Log(string name, bool value)
{
    Console.Write(name + " ");
    return value;
}
