// Скільки байтів виділяє в керованій купі кожна операція (GC.GetAllocatedBytesForCurrentThread).
int a = 5;
long start;

start = GC.GetAllocatedBytesForCurrentThread();
int b = a;
long copyInt = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
object boxed = a;
long boxing = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
int[] three = new int[3];
long array3 = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
int[] thousand = new int[1000];
long array1000 = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
int[] alias = thousand;
long copyRef = GC.GetAllocatedBytesForCurrentThread() - start;

string text = "Привіт";
start = GC.GetAllocatedBytesForCurrentThread();
string longer = text + "!";
long concat = GC.GetAllocatedBytesForCurrentThread() - start;

Console.WriteLine($"int b = a;                    {copyInt,5} Б");
Console.WriteLine($"object boxed = a;             {boxing,5} Б");
Console.WriteLine($"new int[3]                    {array3,5} Б");
Console.WriteLine($"new int[1000]                 {array1000,5} Б");
Console.WriteLine($"int[] alias = thousand;       {copyRef,5} Б");
Console.WriteLine($"text + \"!\" (7 символів)       {concat,5} Б");
Console.WriteLine($"{b} {boxed} {three.Length} {alias.Length} {longer}");
