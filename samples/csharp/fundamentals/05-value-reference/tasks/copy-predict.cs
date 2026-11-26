// Міні-завдання: що надрукує програма.
int[] first = [10, 20, 30];
int[] second = first;
int count = first.Length;

second[1] = 0;
count = 0;
second = [1, 2];

Console.WriteLine($"{first[0]} {first[1]} {first.Length} {second.Length} {count}");
