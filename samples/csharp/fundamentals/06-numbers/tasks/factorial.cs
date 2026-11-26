// Міні-завдання: факторіал у int — де результат перестає бути правдою.
int product = 1;
for (int n = 1; n <= 14; n++)
{
    product *= n;
    Console.WriteLine($"{n,2}! = {product}");
}
