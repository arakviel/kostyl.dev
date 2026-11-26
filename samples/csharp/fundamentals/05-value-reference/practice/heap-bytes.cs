// Практика 2: скільки байтів у купі виділяє кожна операція.
int a = 5;
int[] numbers = new int[100];
string text = "Привіт";
long start;

start = GC.GetAllocatedBytesForCurrentThread();
int b = a;
long r1 = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
object o = 3.14;
long r2 = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
int[] ints = new int[100];
long r3 = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
long[] longs = new long[100];
long r4 = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
string twice = text + text;
long r5 = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
int[] alias = numbers;
long r6 = GC.GetAllocatedBytesForCurrentThread() - start;

Console.WriteLine($"1. int b = a;              {r1,4} Б");
Console.WriteLine($"2. object o = 3.14;        {r2,4} Б");
Console.WriteLine($"3. new int[100]            {r3,4} Б");
Console.WriteLine($"4. new long[100]           {r4,4} Б");
Console.WriteLine($"5. text + text (12 літер)  {r5,4} Б");
Console.WriteLine($"6. int[] alias = numbers;  {r6,4} Б");
Console.WriteLine($"{b} {o} {ints.Length} {longs.Length} {twice} {alias.Length}");
