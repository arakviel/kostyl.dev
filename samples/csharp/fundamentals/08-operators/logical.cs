// && і || обчислюють праву частину лише за потреби; & і | для bool обчислюють обидві.
Console.WriteLine("false && Check(1):");
bool r1 = false && Check(1);
Console.WriteLine("false & Check(2):");
bool r2 = false & Check(2);
Console.WriteLine("true || Check(3):");
bool r3 = true || Check(3);
Console.WriteLine("true | Check(4):");
bool r4 = true | Check(4);
Console.WriteLine($"результати: {r1} {r2} {r3} {r4}");
Console.WriteLine($"true ^ true = {true ^ true}, true ^ false = {true ^ false}");

string? name = null;
bool ok = name != null && name.Length > 0;   // без && тут був би NullReferenceException
Console.WriteLine($"ім'я задане: {ok}");

static bool Check(int id)
{
    Console.WriteLine($"  Check({id}) викликано");
    return true;
}
