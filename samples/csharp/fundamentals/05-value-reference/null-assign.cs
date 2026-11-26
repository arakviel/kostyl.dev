using System.Text;

// C# 14: присвоєння через ?. і ?[] виконується, лише якщо зліва не null.
int[]? scores = null;
scores?[0] = 100;
Console.WriteLine(scores is null);

scores = new int[3];
scores?[0] = 100;
Console.WriteLine(scores?[0]);

StringBuilder? log = null;
log?.Length = 0;
log = new StringBuilder("старий запис");
log?.Length = 0;
Console.WriteLine($"[{log}]");
