// Міні-завдання: скільки байтів у купі займають різні об'єкти.
long start;

start = GC.GetAllocatedBytesForCurrentThread();
int[] empty = new int[0];
long emptyBytes = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
int[] ten = new int[10];
long tenBytes = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
object boxedDouble = 3.14;
long doubleBytes = GC.GetAllocatedBytesForCurrentThread() - start;

start = GC.GetAllocatedBytesForCurrentThread();
object boxedDecimal = 3.14m;
long decimalBytes = GC.GetAllocatedBytesForCurrentThread() - start;

Console.WriteLine($"new int[0]       {emptyBytes} Б");
Console.WriteLine($"new int[10]      {tenBytes} Б");
Console.WriteLine($"object = 3.14    {doubleBytes} Б");
Console.WriteLine($"object = 3.14m   {decimalBytes} Б");
Console.WriteLine($"{empty.Length} {ten.Length} {boxedDouble} {boxedDecimal}");
