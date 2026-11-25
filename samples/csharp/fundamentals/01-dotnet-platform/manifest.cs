#:property PublishAot=false

using System.Reflection;

Assembly app = Assembly.GetEntryAssembly()!;
AssemblyName name = app.GetName();

Console.WriteLine($"Assembly:  {name.Name}");
Console.WriteLine($"Версія:  {name.Version}");
Console.WriteLine("Посилання з маніфесту:");
foreach (AssemblyName reference in app.GetReferencedAssemblies())
{
    Console.WriteLine($"  {reference.Name}, {reference.Version}");
}

Console.WriteLine($"Console живе у: {typeof(Console).Assembly.GetName().Name}");
Console.WriteLine($"int живе у:     {typeof(int).Assembly.GetName().Name}");
