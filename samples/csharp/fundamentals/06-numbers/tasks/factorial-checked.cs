// Міні-завдання: та сама програма в checked зупиняється на першому переповненні.
int product = 1;
for (int n = 1; n <= 14; n++)
{
    product = checked(product * n);
    Console.WriteLine($"{n,2}! = {product}");
}
