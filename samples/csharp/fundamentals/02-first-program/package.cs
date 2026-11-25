#:package Humanizer@2.14.1

using Humanizer;

Console.WriteLine(TimeSpan.FromMinutes(90).Humanize(2));
Console.WriteLine("file_based_app".Humanize());
Console.WriteLine(1_234_567.ToWords());
