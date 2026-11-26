using System.Text;

// Що порівнює == для різних типів.
int a = 5, b = 5;
Console.WriteLine($"int            a == b                   {a == b}");

int[] x = [1, 2, 3];
int[] y = [1, 2, 3];
int[] z = x;
Console.WriteLine($"int[]          x == y                   {x == y}");
Console.WriteLine($"int[]          x == z                   {x == z}");
Console.WriteLine($"int[]          x.SequenceEqual(y)       {x.SequenceEqual(y)}");

var sb1 = new StringBuilder("Hi");
var sb2 = new StringBuilder("Hi");
Console.WriteLine($"StringBuilder  sb1 == sb2               {sb1 == sb2}");
Console.WriteLine($"StringBuilder  sb1.Equals(sb2)          {sb1.Equals(sb2)}");

string s1 = "Hi";
string s2 = "H";
s2 += "i";
Console.WriteLine($"string         s1 == s2                 {s1 == s2}");
Console.WriteLine($"string         ReferenceEquals(s1, s2)  {object.ReferenceEquals(s1, s2)}");
