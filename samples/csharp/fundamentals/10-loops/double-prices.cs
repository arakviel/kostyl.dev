int[] prices = [100, 250, 80];
for (int i = 0; i < prices.Length; i++)
{
    prices[i] *= 2;   // змінюється сам елемент масиву
}
Console.WriteLine(string.Join(", ", prices));
