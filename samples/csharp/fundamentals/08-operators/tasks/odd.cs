// Міні-завдання: перевірка непарності, яка ламається на від'ємних числах.
int[] numbers = [3, -3, 4, -4, 7, -7];
foreach (int n in numbers)
{
    bool wrong = n % 2 == 1;
    bool right = n % 2 != 0;
    Console.WriteLine($"{n,3}: n % 2 = {n % 2,2}   n % 2 == 1 -> {wrong,-5}   n % 2 != 0 -> {right}");
}
