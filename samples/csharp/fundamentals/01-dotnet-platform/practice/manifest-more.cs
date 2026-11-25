#:property PublishAot=false

using System.Reflection;
using System.Text.Json;

// Практика 3: нові типи BCL — нові залежності в маніфесті.
string json = JsonSerializer.Serialize(new[] { 1, 2, 3 });
Console.WriteLine(json);

using var client = new HttpClient();
Console.WriteLine($"Тайм-аут HttpClient: {client.Timeout.TotalSeconds} с");

Console.WriteLine("Посилання з маніфесту:");
foreach (AssemblyName reference in Assembly.GetEntryAssembly()!.GetReferencedAssemblies())
{
    Console.WriteLine($"  {reference.Name}, {reference.Version}");
}
