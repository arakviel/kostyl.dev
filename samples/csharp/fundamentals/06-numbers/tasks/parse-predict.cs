// Міні-завдання: які рядки double.TryParse і int.TryParse розберуть (InvariantCulture — однаково на всіх машинах).
using System.Globalization;

string[] inputs = ["7", "7.5", "-7.5e2", "7,5", "  7  ", "seven", "1e400"];
foreach (string s in inputs)
{
    bool asInt = int.TryParse(s, CultureInfo.InvariantCulture, out int i);
    bool asDouble = double.TryParse(s, CultureInfo.InvariantCulture, out double d);
    Console.WriteLine($"{"\"" + s + "\"",-10} int: {asInt,-5} {i,-4} double: {asDouble,-5} {d.ToString(CultureInfo.InvariantCulture)}");
}
