int[] data = [10, 20, 30];
int sum = 0;
for (int i = 0; i <= data.Length; i++)   // <= замість <
{
    sum += data[i];
}
Console.WriteLine(sum);
