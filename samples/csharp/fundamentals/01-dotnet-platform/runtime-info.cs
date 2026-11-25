using System.Runtime.InteropServices;

Console.WriteLine($"Середовище: {RuntimeInformation.FrameworkDescription}");
Console.WriteLine($"Версія CLR: {Environment.Version}");
Console.WriteLine($"ОС:         {RuntimeInformation.OSDescription}");
Console.WriteLine($"Процесор:   {RuntimeInformation.ProcessArchitecture}");
Console.WriteLine($"RID:        {RuntimeInformation.RuntimeIdentifier}");
