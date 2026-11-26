// Міні-завдання: True чи False.
var p1 = (1, 2);
var p2 = (1, 2);
Console.WriteLine(p1 == p2);

char[] letters1 = ['o', 'k'];
char[] letters2 = ['o', 'k'];
Console.WriteLine(letters1 == letters2);

string word1 = new string(letters1);
string word2 = new string(letters2);
Console.WriteLine(word1 == word2);

object o1 = 7;
object o2 = 7;
Console.WriteLine(o1 == o2);
Console.WriteLine(o1.Equals(o2));
