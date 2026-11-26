int[] source = [1, 2, 3, 4, 5];

int[] alias = source;                        // не копія: те саме посилання
int[] clone = (int[])source.Clone();         // 1. Clone
int[] copied = new int[5];
Array.Copy(source, copied, source.Length);   // 2. Array.Copy: увесь масив
int[] part = new int[3];
Array.Copy(source, 1, part, 0, 3);           // 3. Array.Copy: 3 елементи з індексу 1
int[] bigger = new int[7];
source.CopyTo(bigger, 2);                    // 4. CopyTo: у більший масив з позиції 2
int[] spread = [.. source];                  // 5. розгортання у виразі колекції
int[] linq = source.ToArray();               // 6. ToArray

source[0] = 100;

Console.WriteLine($"source: {string.Join(", ", source)}");
Console.WriteLine($"alias:  {string.Join(", ", alias)}");
Console.WriteLine($"clone:  {string.Join(", ", clone)}");
Console.WriteLine($"copied: {string.Join(", ", copied)}");
Console.WriteLine($"part:   {string.Join(", ", part)}");
Console.WriteLine($"bigger: {string.Join(", ", bigger)}");
Console.WriteLine($"spread: {string.Join(", ", spread)}");
Console.WriteLine($"linq:   {string.Join(", ", linq)}");
