#:package Humanizer@2.14.1

using Humanizer;

Console.WriteLine("PascalCaseString".Humanize());
Console.WriteLine(5.ToOrdinalWords());
Console.WriteLine(TimeSpan.FromDays(16).Humanize());
