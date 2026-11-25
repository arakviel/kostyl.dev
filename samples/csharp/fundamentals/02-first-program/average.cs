// Програма з помилкою для навчання роботи з налагоджувачем.
// Очікується середнє 4,5, а програма друкує 4.
int[] grades = [5, 4, 3, 6];

int sum = 0;
for (int i = 0; i < grades.Length; i++)
{
    sum += grades[i];
}

double average = sum / grades.Length;
Console.WriteLine($"Сума: {sum}");
Console.WriteLine($"Середнє: {average}");
